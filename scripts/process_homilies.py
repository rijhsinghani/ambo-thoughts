#!/usr/bin/env python3
"""
Ambo Thoughts — Video Processing Pipeline
==========================================

Orchestrates the full workflow:
  1. List videos in a Google Drive folder
  2. Analyse each with Gemini to find homily timestamps & metadata
  3. Trim with ffmpeg (streaming from Drive — no full download)
  4. Upload the trimmed clip to YouTube
  5. Generate a word-for-word transcript via Gemini
  6. Generate blog content via Gemini
  7. Write static HTML pages from a template

Usage:
    python process_homilies.py                   # process all new videos
    python process_homilies.py --test 2          # process only first 2 new videos
    python process_homilies.py --skip-upload      # skip YouTube upload (testing)
    python process_homilies.py --regenerate-pages # rebuild HTML from manifest
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from PIL import Image

import google.auth
import google.auth.transport.requests
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from slugify import slugify

from config import (
    DRIVE_FOLDER_ID,
    GEMINI_MODEL,
    MANIFEST_FILE,
    OUTPUT_DIR,
    SCOPES,
    TEMPLATE_FILE,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("ambo-pipeline")


# ===================================================================
# Authentication helpers
# ===================================================================


def _get_credentials():
    """Return valid OAuth2 credentials via Application Default Credentials.

    Requires: gcloud auth application-default login --scopes=<SCOPES>
    """
    creds, project = google.auth.default(scopes=SCOPES)

    if not creds.valid:
        log.info("Refreshing Application Default Credentials …")
        creds.refresh(google.auth.transport.requests.Request())

    log.info("ADC credentials ready (project=%s).", project)
    return creds


def get_youtube_service():
    """Build and return an authenticated YouTube Data API v3 service."""
    creds = _get_credentials()
    service = build("youtube", "v3", credentials=creds)
    log.info("YouTube service ready.")
    return service


def get_drive_service():
    """Build and return an authenticated Google Drive v3 service."""
    creds = _get_credentials()
    service = build("drive", "v3", credentials=creds)
    log.info("Drive service ready.")
    return service


def get_gemini_model() -> genai.GenerativeModel:
    """Initialise and return the Gemini generative model.

    Expects GOOGLE_API_KEY in the environment (or Application Default
    Credentials configured for Vertex AI).
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        log.warning(
            "GOOGLE_API_KEY not set — falling back to Application Default "
            "Credentials.  Set the env var if you hit auth errors."
        )

    model = genai.GenerativeModel(GEMINI_MODEL)
    log.info("Gemini model (%s) ready.", GEMINI_MODEL)
    return model


# ===================================================================
# Step 1 — List Drive videos
# ===================================================================


def list_drive_videos(drive_service) -> list[dict[str, Any]]:
    """Return every video file inside the shared Drive folder.

    Each item is a dict with keys: id, name, size.
    """
    query = (
        f"'{DRIVE_FOLDER_ID}' in parents "
        "and mimeType contains 'video/' "
        "and trashed = false"
    )
    results: list[dict[str, Any]] = []
    page_token: str | None = None

    while True:
        resp = (
            drive_service.files()
            .list(
                q=query,
                fields="nextPageToken, files(id, name, size)",
                pageSize=100,
                pageToken=page_token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            )
            .execute()
        )
        for f in resp.get("files", []):
            results.append(
                {
                    "id": f["id"],
                    "name": f["name"],
                    "size": int(f.get("size", 0)),
                }
            )
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    log.info("Found %d video(s) in Drive folder.", len(results))
    return results


# ===================================================================
# Step 2 — Analyse with Gemini
# ===================================================================

ANALYSIS_PROMPT = """\
You are analyzing a Catholic Mass recording. Deacon Henry Cugini delivers \
the homily. Please identify:

1. The exact timestamp when the homily begins (when the deacon starts \
speaking at the ambo/pulpit after the Gospel reading)
2. The exact timestamp when the homily ends (when he concludes and before \
the next part of Mass continues)
3. A compelling title for this homily
4. The liturgical season and specific Sunday/feast day if identifiable
5. 3-5 key themes discussed
6. A 2-3 sentence description suitable for a blog listing
7. Any Scripture references mentioned
8. One impactful pull quote from the homily

Return as JSON with keys: homily_start, homily_end, title, \
liturgical_season, date_guess, themes, description, scripture_refs, \
pull_quote
"""


def _upload_to_gemini_file_api(filepath: Path) -> Any:
    """Upload a local file to the Gemini File API and wait until active."""
    log.info("Uploading %s to Gemini File API …", filepath.name)
    gemini_file = genai.upload_file(path=str(filepath))

    while gemini_file.state.name == "PROCESSING":
        log.info("  … Gemini processing %s", filepath.name)
        time.sleep(10)
        gemini_file = genai.get_file(gemini_file.name)

    if gemini_file.state.name != "ACTIVE":
        raise RuntimeError(
            f"Gemini file upload failed — state: {gemini_file.state.name}"
        )

    log.info("Gemini file %s is ACTIVE.", gemini_file.name)
    return gemini_file


def _extract_frames_from_drive(
    file_id: str, frame_interval_secs: int = 60
) -> tuple[Path, list[Path]]:
    """Extract one frame per interval from a Drive video using ffmpeg streaming.

    Returns (tmp_dir, list_of_frame_paths).  Each frame filename encodes
    its timestamp so Gemini can reference it, e.g. frame_0300.jpg = 5:00.
    """
    creds = _get_credentials()
    if creds.expired:
        creds.refresh(google.auth.transport.requests.Request())
    token = creds.token
    drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

    tmp_dir = Path(tempfile.mkdtemp(prefix="ambo_frames_"))
    output_pattern = str(tmp_dir / "frame_%04d.jpg")

    cmd: list[str] = [
        "ffmpeg",
        "-y",
        "-headers",
        f"Authorization: Bearer {token}\r\n",
        "-i",
        drive_url,
        "-vf",
        f"fps=1/{frame_interval_secs}",
        "-q:v",
        "3",
        "-vsync",
        "vfr",
        output_pattern,
    ]

    log.info(
        "Extracting frames every %ds from Drive video %s …",
        frame_interval_secs,
        file_id,
    )
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        log.error("ffmpeg frame extraction stderr:\n%s", result.stderr[-2000:])
        raise RuntimeError(f"ffmpeg frame extraction failed (code {result.returncode})")

    frames = sorted(tmp_dir.glob("frame_*.jpg"))
    log.info("Extracted %d frames.", len(frames))
    return tmp_dir, frames


def _extract_audio_segment_from_drive(
    file_id: str, start_secs: float, duration_secs: float
) -> Path:
    """Extract an audio-only segment from a Drive video via ffmpeg streaming.

    Much smaller than video — sends just the homily portion to Gemini for
    content analysis and transcription.
    """
    creds = _get_credentials()
    if creds.expired:
        creds.refresh(google.auth.transport.requests.Request())
    token = creds.token
    drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

    tmp_path = Path(tempfile.mkdtemp(prefix="ambo_audio_")) / "homily_audio.mp3"
    cmd: list[str] = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_secs),
        "-headers",
        f"Authorization: Bearer {token}\r\n",
        "-i",
        drive_url,
        "-t",
        str(duration_secs),
        "-vn",
        "-c:a",
        "libmp3lame",
        "-q:a",
        "4",
        str(tmp_path),
    ]

    log.info(
        "Extracting audio segment (start=%.0fs, dur=%.0fs) …", start_secs, duration_secs
    )
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log.error("ffmpeg audio extraction stderr:\n%s", result.stderr[-2000:])
        raise RuntimeError(f"ffmpeg audio extraction failed (code {result.returncode})")

    log.info(
        "Audio segment extracted: %s (%.1f MB)",
        tmp_path.name,
        tmp_path.stat().st_size / 1e6,
    )
    return tmp_path


FRAME_ANALYSIS_PROMPT = """\
You are looking at frames extracted from a Catholic Mass recording, one frame \
every {interval} seconds. Each frame is numbered sequentially starting from 0 \
(frame_0001.jpg = {interval}s into the video, frame_0002.jpg = {interval2}s, etc).

Deacon Henry Cugini delivers the homily during this Mass. The homily happens \
after the Gospel reading — the deacon walks to the ambo (pulpit) and speaks \
for roughly 8-20 minutes.

Examine each frame and identify:
1. Which frame number the homily BEGINS (deacon is at the ambo, speaking)
2. Which frame number the homily ENDS (deacon finishes, next part of Mass begins)

Also note any visual cues: is the deacon standing at a pulpit/ambo? Is there \
a congregation visible? Are there other priests/deacons near the altar?

Return as JSON: {{"homily_start_frame": N, "homily_end_frame": N, \
"start_timestamp": "HH:MM:SS", "end_timestamp": "HH:MM:SS", \
"confidence": "high/medium/low", "notes": "brief description of what you see"}}
"""

CONTENT_ANALYSIS_PROMPT = """\
You are analyzing the audio of a Catholic homily by Deacon Henry Cugini. \
Please provide:

1. A compelling title for this homily
2. The liturgical season and specific Sunday/feast day if identifiable
3. 3-5 key themes discussed
4. A 2-3 sentence description suitable for a blog listing
5. Any Scripture references mentioned
6. One impactful pull quote from the homily

Return as JSON with keys: title, liturgical_season, date_guess, themes, \
description, scripture_refs, pull_quote
"""


def analyze_video_with_gemini(
    model: genai.GenerativeModel,
    drive_service,
    file_id: str,
    filename: str,
) -> dict[str, Any]:
    """Two-phase video analysis: frames for timestamps, audio for content.

    Phase 1: Extract a frame every 60s, send to Gemini to find when
             the homily starts and ends (visual analysis).
    Phase 2: Extract just the audio of the homily segment, send to Gemini
             for content analysis (title, themes, scripture, etc).

    This avoids uploading the entire 1-hour video.
    """
    frame_interval = 60  # one frame per minute

    # --- Phase 1: Frame-based timestamp detection ---
    log.info("Phase 1: Extracting frames for timestamp detection …")
    tmp_dir, frames = _extract_frames_from_drive(file_id, frame_interval)

    try:
        # Upload frames to Gemini
        log.info("Uploading %d frames to Gemini …", len(frames))
        frame_images = []
        for f in frames:
            frame_images.append(Image.open(f))

        prompt = FRAME_ANALYSIS_PROMPT.format(
            interval=frame_interval,
            interval2=frame_interval * 2,
        )

        response = model.generate_content(
            [*frame_images, prompt],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            ),
        )

        frame_analysis: dict[str, Any] = json.loads(response.text)
        log.info(
            "Frame analysis: start=%s, end=%s (confidence=%s)",
            frame_analysis.get("start_timestamp"),
            frame_analysis.get("end_timestamp"),
            frame_analysis.get("confidence"),
        )

        homily_start = frame_analysis.get("start_timestamp", "00:20:00")
        homily_end = frame_analysis.get("end_timestamp", "00:35:00")

    finally:
        # Clean up frame files
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # --- Phase 2: Audio-based content analysis ---
    log.info("Phase 2: Extracting homily audio for content analysis …")
    start_secs = _timestamp_to_seconds(homily_start)
    end_secs = _timestamp_to_seconds(homily_end)
    duration = end_secs - start_secs

    # Add 30s buffer on each side for safety
    safe_start = max(0, start_secs - 30)
    safe_duration = duration + 60

    audio_path = _extract_audio_segment_from_drive(file_id, safe_start, safe_duration)

    try:
        gemini_audio = _upload_to_gemini_file_api(audio_path)

        log.info("Sending content analysis prompt to Gemini …")
        response = model.generate_content(
            [gemini_audio, CONTENT_ANALYSIS_PROMPT],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            ),
        )

        content_analysis: dict[str, Any] = json.loads(response.text)
        log.info("Content analysis complete for %s.", filename)

    finally:
        try:
            audio_path.unlink(missing_ok=True)
            audio_path.parent.rmdir()
        except OSError:
            pass

    # Merge both analyses
    analysis: dict[str, Any] = {
        "homily_start": homily_start,
        "homily_end": homily_end,
        **content_analysis,
    }
    return analysis


# ===================================================================
# Step 3 — Trim with ffmpeg (stream from Drive)
# ===================================================================


def _timestamp_to_seconds(ts: str) -> float:
    """Convert HH:MM:SS or MM:SS to seconds."""
    parts = ts.split(":")
    parts = [float(p) for p in parts]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0]


def trim_video(
    file_id: str,
    start_time: str,
    end_time: str,
    output_path: Path,
) -> Path:
    """Stream a video from Drive and trim it with ffmpeg.

    Uses a fresh access token so ffmpeg can authenticate against the
    Drive REST endpoint directly — no full local download required.
    """
    creds = _get_credentials()
    if creds.expired:
        creds.refresh(google.auth.transport.requests.Request())
    token = creds.token

    start_secs = _timestamp_to_seconds(start_time)
    end_secs = _timestamp_to_seconds(end_time)
    duration = end_secs - start_secs

    if duration <= 0:
        raise ValueError(f"Invalid trim window: start={start_time} end={end_time}")

    drive_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

    cmd: list[str] = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start_secs),
        "-i",
        drive_url,
        "-headers",
        f"Authorization: Bearer {token}\r\n",
        "-t",
        str(duration),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    log.info(
        "Trimming %s → %s  (start=%s, duration=%.0fs) …",
        file_id,
        output_path.name,
        start_time,
        duration,
    )

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        log.error("ffmpeg stderr:\n%s", result.stderr[-2000:])
        raise RuntimeError(f"ffmpeg exited with code {result.returncode}")

    log.info(
        "Trim complete: %s (%s bytes).", output_path.name, output_path.stat().st_size
    )
    return output_path


# ===================================================================
# Step 4 — Upload to YouTube
# ===================================================================


def upload_to_youtube(
    youtube_service,
    video_path: Path,
    title: str,
    description: str,
    tags: list[str],
) -> str:
    """Upload a video to YouTube via resumable upload.

    Returns the YouTube video ID.
    """
    body: dict[str, Any] = {
        "snippet": {
            "title": title,
            "description": (
                description + "\n\nWatch more homilies at "
                "https://ambothoughts.com/blog.html"
            ),
            "tags": tags,
            "categoryId": "29",  # Nonprofits & Activism
        },
        "status": {
            "privacyStatus": "unlisted",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
        chunksize=10 * 1024 * 1024,  # 10 MB chunks
    )

    request = youtube_service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    log.info("Uploading %s to YouTube …", video_path.name)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            log.info("  … upload %d%% complete", int(status.progress() * 100))

    video_id: str = response["id"]
    log.info(
        "YouTube upload complete: https://youtu.be/%s",
        video_id,
    )
    return video_id


# ===================================================================
# Step 5 — Generate transcript
# ===================================================================

TRANSCRIPT_PROMPT = """\
Transcribe this Catholic homily word for word. Use proper punctuation, \
paragraph breaks, and correct Catholic terminology (Eucharist, \
Transubstantiation, etc). Format as clean paragraphs.
"""


def generate_transcript(model: genai.GenerativeModel, video_path: Path) -> str:
    """Upload the trimmed video to Gemini and get a full transcription."""
    gemini_file = _upload_to_gemini_file_api(video_path)

    log.info("Requesting transcript from Gemini …")
    response = model.generate_content([gemini_file, TRANSCRIPT_PROMPT])
    transcript: str = response.text.strip()
    log.info("Transcript received (%d characters).", len(transcript))
    return transcript


# ===================================================================
# Step 6 — Generate blog content
# ===================================================================

BLOG_CONTENT_PROMPT = """\
You are writing blog content for a Catholic deacon's website called \
"Ambo Thoughts". Using the transcript and analysis below, generate:

1. An SEO-friendly blog title (compelling, includes a keyword)
2. A 2-3 sentence description for the listing page
3. Key themes — each with a one-sentence explanation
4. Scripture references formatted as "Book Chapter:Verse"
5. One impactful pull quote from the homily

TRANSCRIPT:
{transcript}

ANALYSIS:
{analysis}

Return as JSON with keys: seo_title, listing_description, \
themed_explanations (list of {{theme, explanation}}), \
scripture_refs_formatted (list of strings), pull_quote
"""


def generate_blog_content(
    model: genai.GenerativeModel,
    transcript: str,
    analysis: dict[str, Any],
) -> dict[str, Any]:
    """Use Gemini to create polished blog content from the transcript."""
    prompt = BLOG_CONTENT_PROMPT.format(
        transcript=transcript,
        analysis=json.dumps(analysis, indent=2),
    )

    log.info("Generating blog content with Gemini …")
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
        ),
    )

    blog_content: dict[str, Any] = json.loads(response.text)
    log.info("Blog content generated.")
    return blog_content


# ===================================================================
# Step 7 — Generate HTML pages
# ===================================================================


def _read_template() -> str:
    """Read the HTML template from disk."""
    if not TEMPLATE_FILE.exists():
        log.error("Template not found at %s", TEMPLATE_FILE)
        sys.exit(1)
    return TEMPLATE_FILE.read_text(encoding="utf-8")


def _format_themes_html(themes: list[str] | list[dict]) -> str:
    """Turn a list of themes into theme-tag pill elements matching the CSS."""
    items: list[str] = []
    for t in themes:
        if isinstance(t, dict):
            label = t.get("theme", "")
            items.append(f'<span class="theme-tag">{label}</span>')
        else:
            items.append(f'<span class="theme-tag">{t}</span>')
    return "\n".join(items)


def _format_scripture_html(refs: list[str]) -> str:
    """Format scripture references as an HTML list."""
    if not refs:
        return "<p><em>No specific scripture references identified.</em></p>"
    items = [f"<li>{r}</li>" for r in refs]
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def generate_homily_page(
    homily_data: dict[str, Any],
    template_html: str,
    prev_homily: dict[str, Any] | None,
    next_homily: dict[str, Any] | None,
) -> Path:
    """Render a single homily HTML page and write it to OUTPUT_DIR."""
    slug: str = homily_data.get("slug", "untitled")
    output_path = OUTPUT_DIR / f"homily-{slug}.html"

    themes_html = _format_themes_html(homily_data.get("themes", []))
    scripture_html = _format_scripture_html(homily_data.get("scripture_refs", []))

    transcript = homily_data.get("transcript", "")
    # Wrap plain-text paragraphs in <p> tags if not already HTML
    if transcript and not transcript.strip().startswith("<"):
        paragraphs = [p.strip() for p in transcript.split("\n\n") if p.strip()]
        transcript = "\n".join(f"<p>{p}</p>" for p in paragraphs)

    prev_link = ""
    if prev_homily:
        prev_slug = prev_homily.get("slug", "")
        prev_title = prev_homily.get("title", "Previous")
        prev_link = (
            f'<a href="homily-{prev_slug}.html" class="prev-link">'
            f"&larr; {prev_title}</a>"
        )

    next_link = ""
    if next_homily:
        next_slug = next_homily.get("slug", "")
        next_title = next_homily.get("title", "Next")
        next_link = (
            f'<a href="homily-{next_slug}.html" class="next-link">'
            f"{next_title} &rarr;</a>"
        )

    youtube_id = homily_data.get("youtube_id", "")

    html = template_html
    replacements: dict[str, str] = {
        "{{TITLE}}": homily_data.get("title", "Untitled Homily"),
        "{{DATE}}": homily_data.get("date", ""),
        "{{YOUTUBE_ID}}": youtube_id,
        "{{DESCRIPTION}}": homily_data.get("description", ""),
        "{{THEMES}}": themes_html,
        "{{TRANSCRIPT}}": transcript,
        "{{SCRIPTURE_REFS}}": scripture_html,
        "{{PULL_QUOTE}}": homily_data.get("pull_quote", ""),
        "{{PREV_LINK}}": prev_link,
        "{{NEXT_LINK}}": next_link,
        "{{SLUG}}": slug,
    }

    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    log.info("Wrote %s", output_path)
    return output_path


def generate_all_pages(manifest: dict[str, Any]) -> None:
    """(Re)generate every homily HTML page and update the blog listing."""
    template_html = _read_template()
    homilies: list[dict[str, Any]] = manifest.get("homilies", [])

    for i, homily in enumerate(homilies):
        prev_homily = homilies[i - 1] if i > 0 else None
        next_homily = homilies[i + 1] if i < len(homilies) - 1 else None
        generate_homily_page(homily, template_html, prev_homily, next_homily)

    log.info("Generated %d HTML page(s).", len(homilies))

    # Update the blog listing page with homily cards
    _update_blog_listing(homilies)


def _update_blog_listing(homilies: list[dict[str, Any]]) -> None:
    """Replace the HOMILY_CARDS_PLACEHOLDER in blog.html with actual cards."""
    from config import PROJECT_ROOT

    blog_html_path = PROJECT_ROOT / "blog.html"
    if not blog_html_path.exists():
        log.warning("blog.html not found — skipping listing update.")
        return

    blog_html = blog_html_path.read_text(encoding="utf-8")

    # Build homily card HTML
    cards: list[str] = []
    for h in homilies:
        youtube_id = h.get("youtube_id", "")
        slug = h.get("slug", "")
        title = h.get("title", "Untitled")
        date = h.get("date", "")
        season = h.get("liturgical_season", "")
        desc = h.get("description", "")
        meta_parts = [p for p in [date, season] if p]
        meta = " &bull; ".join(meta_parts)

        thumb_url = (
            f"https://img.youtube.com/vi/{youtube_id}/mqdefault.jpg"
            if youtube_id
            else ""
        )

        card = f"""          <article class="homily-card">
            <a href="blog/homily-{slug}.html" class="homily-card-thumb">
              <img src="{thumb_url}" alt="{title}" loading="lazy" />
              <span class="play-overlay">&#9654;</span>
            </a>
            <div class="homily-card-body">
              <p class="homily-card-meta">{meta}</p>
              <h3>{title}</h3>
              <p class="homily-card-excerpt">{desc}</p>
              <a href="blog/homily-{slug}.html" class="homily-card-link">Watch &amp; Read &rarr;</a>
            </div>
          </article>"""
        cards.append(card)

    cards_html = (
        "\n\n".join(cards) if cards else "          <!-- No homilies processed yet -->"
    )

    # Replace the placeholder comment
    blog_html = re.sub(
        r"<!-- HOMILY_CARDS_PLACEHOLDER -->.*?(?=</div>)",
        cards_html + "\n",
        blog_html,
        flags=re.DOTALL,
    )

    blog_html_path.write_text(blog_html, encoding="utf-8")
    log.info("Updated blog.html with %d homily card(s).", len(cards))

    # Also update index.html with the latest 3 homilies
    _update_index_page(homilies[:3])


def _update_index_page(latest_homilies: list[dict[str, Any]]) -> None:
    """Replace the LATEST_HOMILIES_PLACEHOLDER in index.html with up to 3 cards."""
    from config import PROJECT_ROOT

    index_path = PROJECT_ROOT / "index.html"
    if not index_path.exists():
        log.warning("index.html not found — skipping homepage update.")
        return

    index_html = index_path.read_text(encoding="utf-8")

    cards: list[str] = []
    for h in latest_homilies:
        youtube_id = h.get("youtube_id", "")
        slug = h.get("slug", "")
        title = h.get("title", "Untitled")
        date = h.get("date", "")
        season = h.get("liturgical_season", "")
        meta_parts = [p for p in [date, season] if p]
        meta = " &bull; ".join(meta_parts)
        thumb_url = (
            f"https://img.youtube.com/vi/{youtube_id}/mqdefault.jpg"
            if youtube_id
            else ""
        )

        card = f"""            <article class="homily-card">
              <a href="blog/homily-{slug}.html" class="homily-card-thumb">
                <img src="{thumb_url}" alt="{title}" loading="lazy" />
                <span class="play-overlay">&#9654;</span>
              </a>
              <div class="homily-card-body">
                <p class="homily-card-meta">{meta}</p>
                <h3>{title}</h3>
                <a href="blog/homily-{slug}.html" class="homily-card-link">Watch &amp; Read &rarr;</a>
              </div>
            </article>"""
        cards.append(card)

    cards_html = (
        "\n\n".join(cards)
        if cards
        else "            <!-- No homilies processed yet -->"
    )

    index_html = re.sub(
        r"<!-- LATEST_HOMILIES_PLACEHOLDER -->.*?(?=</div>)",
        cards_html + "\n",
        index_html,
        flags=re.DOTALL,
    )

    index_path.write_text(index_html, encoding="utf-8")
    log.info("Updated index.html with %d latest homily card(s).", len(cards))


# ===================================================================
# Manifest management
# ===================================================================


def load_manifest() -> dict[str, Any]:
    """Load the manifest from disk or return an empty structure."""
    if MANIFEST_FILE.exists():
        data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        log.info(
            "Loaded manifest with %d homily(ies).",
            len(data.get("homilies", [])),
        )
        return data
    log.info("No existing manifest — starting fresh.")
    return {"homilies": []}


def save_manifest(manifest: dict[str, Any]) -> None:
    """Persist the manifest to disk."""
    MANIFEST_FILE.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    log.info("Manifest saved (%d homilies).", len(manifest.get("homilies", [])))


# ===================================================================
# Main orchestrator
# ===================================================================


def _build_tags(analysis: dict[str, Any]) -> list[str]:
    """Build a YouTube tag list from analysis data."""
    tags: list[str] = [
        "homily",
        "Catholic",
        "Deacon Henry Cugini",
        "Ambo Thoughts",
    ]
    season = analysis.get("liturgical_season", "")
    if season:
        tags.append(season)
    for theme in analysis.get("themes", [])[:3]:
        if isinstance(theme, str):
            tags.append(theme)
    return tags


def process_all(
    *,
    test_limit: int | None = None,
    skip_upload: bool = False,
    regenerate_pages: bool = False,
) -> None:
    """Run the full pipeline."""

    manifest = load_manifest()

    # --regenerate-pages: skip processing, just rebuild HTML
    if regenerate_pages:
        log.info("Regenerating HTML pages from existing manifest …")
        generate_all_pages(manifest)
        return

    # --- Authenticate all services ---
    log.info("Authenticating services …")
    youtube_service = get_youtube_service()
    drive_service = get_drive_service()
    model = get_gemini_model()

    # --- List Drive videos ---
    drive_videos = list_drive_videos(drive_service)

    # --- Determine which videos are new ---
    processed_ids: set[str] = {h["drive_file_id"] for h in manifest.get("homilies", [])}
    new_videos = [v for v in drive_videos if v["id"] not in processed_ids]
    log.info(
        "%d new video(s) to process (of %d total).",
        len(new_videos),
        len(drive_videos),
    )

    if test_limit is not None:
        new_videos = new_videos[:test_limit]
        log.info("--test %d: limiting to %d video(s).", test_limit, len(new_videos))

    # --- Process each new video ---
    for idx, video in enumerate(new_videos, start=1):
        file_id = video["id"]
        filename = video["name"]
        log.info(
            "=== [%d/%d] Processing: %s ===",
            idx,
            len(new_videos),
            filename,
        )

        try:
            # Step 2 — Analyse
            log.info("Step 2: Analysing with Gemini …")
            analysis = analyze_video_with_gemini(
                model, drive_service, file_id, filename
            )

            homily_start: str = analysis.get("homily_start", "00:00:00")
            homily_end: str = analysis.get("homily_end", "00:10:00")
            title: str = analysis.get("title", filename)
            slug = slugify(title, max_length=60)

            # Step 3 — Trim
            log.info("Step 3: Trimming with ffmpeg …")
            tmp_path = Path(tempfile.gettempdir()) / f"homily_{slug}.mp4"
            trim_video(file_id, homily_start, homily_end, tmp_path)

            # Step 4 — Upload to YouTube
            youtube_id = ""
            youtube_url = ""
            if skip_upload:
                log.info("Step 4: Skipping YouTube upload (--skip-upload).")
            else:
                log.info("Step 4: Uploading to YouTube …")
                tags = _build_tags(analysis)
                youtube_id = upload_to_youtube(
                    youtube_service,
                    tmp_path,
                    title,
                    analysis.get("description", ""),
                    tags,
                )
                youtube_url = f"https://youtu.be/{youtube_id}"

            # Step 5 — Transcript
            log.info("Step 5: Generating transcript …")
            transcript = generate_transcript(model, tmp_path)

            # Step 6 — Blog content
            log.info("Step 6: Generating blog content …")
            blog_content = generate_blog_content(model, transcript, analysis)

            # Merge everything into a homily record
            homily_record: dict[str, Any] = {
                "drive_file_id": file_id,
                "drive_filename": filename,
                "homily_start": homily_start,
                "homily_end": homily_end,
                "youtube_id": youtube_id,
                "youtube_url": youtube_url,
                "title": blog_content.get("seo_title", title),
                "description": blog_content.get(
                    "listing_description",
                    analysis.get("description", ""),
                ),
                "themes": analysis.get("themes", []),
                "scripture_refs": blog_content.get(
                    "scripture_refs_formatted",
                    analysis.get("scripture_refs", []),
                ),
                "pull_quote": blog_content.get(
                    "pull_quote", analysis.get("pull_quote", "")
                ),
                "transcript": transcript,
                "liturgical_season": analysis.get("liturgical_season", ""),
                "date": analysis.get("date_guess", ""),
                "slug": slug,
            }

            manifest["homilies"].append(homily_record)

            # Save after each video for crash recovery
            save_manifest(manifest)

            # Clean up temp file
            try:
                tmp_path.unlink(missing_ok=True)
            except OSError:
                pass

            log.info("=== Finished: %s ===\n", title)

        except Exception:
            log.exception("Failed to process %s — skipping.", filename)
            continue

    # --- Step 7 — Generate all HTML pages ---
    log.info("Step 7: Generating HTML pages …")
    generate_all_pages(manifest)

    # --- Summary ---
    total = len(manifest.get("homilies", []))
    log.info(
        "Pipeline complete. %d homily(ies) in manifest, %d processed this run.",
        total,
        len(new_videos),
    )


# ===================================================================
# CLI entry point
# ===================================================================


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ambo Thoughts video processing pipeline",
    )
    parser.add_argument(
        "--test",
        type=int,
        metavar="N",
        default=None,
        help="Process only the first N unprocessed videos.",
    )
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Skip the YouTube upload step (useful for testing trimming).",
    )
    parser.add_argument(
        "--regenerate-pages",
        action="store_true",
        help="Regenerate HTML pages from the existing manifest without "
        "reprocessing any videos.",
    )
    args = parser.parse_args()

    process_all(
        test_limit=args.test,
        skip_upload=args.skip_upload,
        regenerate_pages=args.regenerate_pages,
    )


if __name__ == "__main__":
    main()
