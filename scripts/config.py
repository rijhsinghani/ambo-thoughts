"""
Configuration for the Ambo Thoughts video processing pipeline.

All paths, API settings, and constants live here so the main script
stays free of magic strings.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Google Cloud / API identifiers
# ---------------------------------------------------------------------------
GCP_PROJECT: str = "videoprocessing-456318"
YOUTUBE_CHANNEL_ID: str = "UCoRGN5UJJ1f-BCGjbxqWenA"
DRIVE_FOLDER_ID: str = "1O9qoJWNl7aG9ZhgwnzLSrfSWk_cZpJpR"

# ---------------------------------------------------------------------------
# OAuth2 scopes
# ---------------------------------------------------------------------------
SCOPES: list[str] = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/drive.readonly",
]

# ---------------------------------------------------------------------------
# Gemini
# ---------------------------------------------------------------------------
GEMINI_MODEL: str = "gemini-2.5-pro"

# ---------------------------------------------------------------------------
# File system paths  (relative to the project root)
# ---------------------------------------------------------------------------
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS_DIR: Path = PROJECT_ROOT / "scripts"

MANIFEST_FILE: Path = SCRIPTS_DIR / "manifest.json"
TEMPLATE_FILE: Path = PROJECT_ROOT / "blog" / "homily-template.html"
OUTPUT_DIR: Path = PROJECT_ROOT / "blog"
