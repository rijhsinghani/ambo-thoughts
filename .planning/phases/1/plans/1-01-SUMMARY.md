---
phase: 1-infrastructure-launch
plan: 01
subsystem: content-preparation
tags: [heic, content-extraction, migration-prep]
dependency-graph:
  requires: []
  provides: [converted-images, content-fragments]
  affects: [1-04-content-migration]
tech-stack:
  added: [sips]
  patterns: [html-fragment-extraction, batch-image-conversion]
key-files:
  created:
    - scripts/convert-heic.sh
    - content/about.html
    - content/spirituality.html
    - content/church-news.html
    - content/prayer-partner.html
    - content/stuff.html
    - content/videos.html
    - content/posts/holy-thursday.html
    - content/posts/good-samaritan.html
    - images/converted/ (17 JPEG files)
  modified: []
decisions:
  - Used sips (macOS native) for HEIC conversion -- no external dependencies needed
  - Replaced spaces with hyphens in converted filenames for web-friendly URLs
  - Preserved inline styles in content fragments to maintain layout intent for WP migration
  - Added HTML comment metadata (title, date, author, category) to blog post fragments
metrics:
  duration: ~3 minutes
  completed: 2026-03-07
---

# Phase 1 Plan 01: Local WP Setup + Content Prep Summary

HEIC batch conversion and HTML content extraction for WordPress CLI migration.

## Task 2: Convert HEIC images and extract content for migration

**Commit:** e69a9db

### A. HEIC Conversion Script

Created `scripts/convert-heic.sh` -- a reusable bash script that:

- Accepts input and output directory arguments
- Finds all .HEIC/.heic files recursively
- Converts via macOS `sips` to JPEG
- Replaces spaces with hyphens in output filenames
- Prints progress during conversion

### B. HEIC Image Conversion

Found and converted all 17 HEIC files from iCloud `/Hank/` directory to `images/converted/`:

Key files successfully converted:

- `Cover2.HEIC` -> `Cover2.jpg`
- `Spirituality Hero.heic` -> `Spirituality-Hero.jpg`
- `Hero-1.HEIC` -> `Hero-1.jpg`
- Plus 14 additional images (IMG_0944, IMG_0947, IMG_0953, IMG_1818, IMG_1824, IMG_3196, IMG_4125, IMG_4126, IMG_8764, Picture2, FullSizeRender, image000000, put-it-in-stuff, IMG_1818-2-topaz-upscale-4x)

No missing files -- all known HEIC files were found and converted.

### C. Content Extraction

Extracted main content from 8 HTML pages as clean fragments (no `<header>`, `<footer>`, `<nav>`, or `<script>` tags):

**Pages (6):**

1. `content/about.html` -- Bio, ministries, motto blockquote
2. `content/spirituality.html` -- Coming soon placeholder with quote
3. `content/church-news.html` -- Vatican, Diocese, Parish news sections
4. `content/prayer-partner.html` -- Prayer chain signup with email CTA
5. `content/stuff.html` -- Photo + Saint of the Day link
6. `content/videos.html` -- Featured YouTube embed, 16 video cards with season filtering

**Blog posts (2):**

1. `content/posts/holy-thursday.html` -- "A Night of Service" reflection
2. `content/posts/good-samaritan.html` -- "The Good Samaritan in Our Time" reflection

### D. Verification

All checks passed:

- `scripts/convert-heic.sh` exists and is executable
- 6 page content files in `content/`
- 2 blog post files in `content/posts/`
- All content files verified clean (no header/footer/nav/script elements)
- 17 converted JPEG files in `images/converted/`

## Deviations from Plan

None -- plan executed exactly as written.

## Note on Task 1

Task 1 (Local by Flywheel setup + ChurchWP installation) is a `checkpoint:human-action` that requires manual GUI steps. This summary covers only Task 2 which was executed automatically.

## Self-Check: PASSED
