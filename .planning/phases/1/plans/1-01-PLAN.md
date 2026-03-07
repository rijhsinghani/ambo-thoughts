---
phase: 1-infrastructure-launch
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/convert-heic.sh
  - scripts/migrate-content.sh
  - content/about.html
  - content/spirituality.html
  - content/church-news.html
  - content/prayer-partner.html
  - content/stuff.html
  - content/videos.html
  - content/posts/holy-thursday.html
  - content/posts/good-samaritan.html
autonomous: false
requirements:
  - REQ-THEME-001
  - REQ-THEME-002
  - REQ-THEME-005
  - REQ-GALLERY-003

must_haves:
  truths:
    - "Local by Flywheel site 'ambo-thoughts' is running and accessible at ambo-thoughts.local"
    - "ChurchWP parent theme and child theme are both installed and child theme is active"
    - "All bundled plugins (ThemeSLR Framework, WPBakery, Revolution Slider) are installed and active"
    - "ChurchWP demo data is fully imported (pages, posts, widgets, slider)"
    - "HEIC images are converted to JPEG and ready for upload"
  artifacts:
    - path: "~/Local Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/"
      provides: "Active child theme"
    - path: "scripts/convert-heic.sh"
      provides: "HEIC batch conversion script"
    - path: "content/"
      provides: "Extracted HTML content files for WP-CLI migration"
  key_links:
    - from: "churchwp-child"
      to: "churchwp (parent)"
      via: "Template: churchwp in style.css"
---

<objective>
Set up the local WordPress development environment in Local by Flywheel with ChurchWP theme installed, demo data imported, and all source content prepared for migration.

Purpose: This is the development foundation -- all theme customization (Plan 03), content migration (Plan 04), and slider work (Plan 05) depend on having a working local WordPress with ChurchWP demo data as the starting baseline.

Output: Running Local by Flywheel WordPress site with ChurchWP child theme active, demo data imported, HEIC images converted, and content files extracted and ready for WP-CLI import.
</objective>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/RESEARCH.md
</context>

<tasks>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Create Local by Flywheel site and install ChurchWP</name>
  <what-built>Nothing yet -- this requires the user to perform GUI actions in Local by Flywheel and WordPress admin.</what-built>
  <how-to-verify>
    The user must complete these steps manually (Local by Flywheel is a GUI app, and theme upload requires WordPress admin):

    **A. Create the Local site:**
    1. Open Local by Flywheel
    2. Click "+ Create a New Site"
    3. Site name: "ambo-thoughts"
    4. Choose "Custom" environment: PHP 8.3, Nginx, MySQL 8.0
    5. Set admin credentials (remember these)
    6. Click "Add Site"

    **B. Install ChurchWP theme:**
    1. Open the site in WordPress admin (click "WP Admin" in Local)
    2. Go to Appearance > Themes > Add New > Upload Theme
    3. Upload `~/Downloads/churchwp_package/theme/churchwp.zip` -- Install but DO NOT activate
    4. Upload `~/Downloads/churchwp_package/theme/churchwp-child.zip` -- Install and Activate
    5. When prompted to install required plugins, click "Begin installing plugins"
    6. Install all three bundled plugins from the package:
       - ThemeSLR Framework: `~/Downloads/churchwp_package/plugins/themeslr-framework-churchwp.zip`
       - WPBakery: `~/Downloads/churchwp_package/plugins/js_composer.zip`
       - Revolution Slider: `~/Downloads/churchwp_package/plugins/revslider.zip`
    7. Activate all three plugins

    **C. Import demo data:**
    1. Go to Theme Panel > Demo Importer (or Starter Sites)
    2. Import the full demo (content.xml, theme-options.txt, widgets.wie)
    3. Go to Slider Revolution > import `~/Downloads/churchwp_package/sampledata/main_home_slider.zip`
    4. Visit the site frontend -- you should see the full ChurchWP demo site

    **D. Verify:**
    - Frontend shows ChurchWP demo homepage with hero slider
    - Appearance > Themes shows churchwp-child as active
    - Plugins page shows ThemeSLR Framework, WPBakery, Revolution Slider all active

  </how-to-verify>
  <resume-signal>Type "done" when Local by Flywheel site is running with ChurchWP demo data imported, or describe any issues.</resume-signal>
</task>

<task type="auto">
  <name>Task 2: Convert HEIC images and extract content for migration</name>
  <files>
    scripts/convert-heic.sh
    content/about.html
    content/spirituality.html
    content/church-news.html
    content/prayer-partner.html
    content/stuff.html
    content/videos.html
    content/posts/holy-thursday.html
    content/posts/good-samaritan.html
  </files>
  <action>
    **A. Create HEIC conversion script** at `scripts/convert-heic.sh`:
    - Accept input directory and output directory as arguments
    - Use `sips -s format jpeg "$f" --out "$OUTPUT_DIR/$outname"` for each .HEIC/.heic file
    - Print conversion progress
    - Make executable with chmod +x

    **B. Run the HEIC conversion:**
    - Identify all HEIC files that need conversion. Known files from CONTEXT.md:
      - `Cover2.HEIC` (from iCloud /Hank/ or /Sameer/Edited/)
      - `Spirituality Hero.heic`
      - `Hero-1.HEIC`
      - Any HEIC files in `High Res/` directory
    - If iCloud /Hank/ directory is not accessible, note which files are missing and skip (user will provide later)
    - Convert any HEIC files found to `images/converted/` directory

    **C. Extract page content for WP-CLI migration:**
    - Create `content/` directory with subdirectory `posts/`
    - For each existing HTML page (about.html, spirituality.html, church-news.html, prayer-partner.html, stuff.html, videos.html):
      - Extract ONLY the main content body (strip header, footer, nav, scripts)
      - Save as clean HTML fragments in `content/{page}.html`
    - For blog posts (blog/2026-holy-thursday-reflection.html, blog/sample-homily.html):
      - Extract title and body content
      - Save as `content/posts/holy-thursday.html` and `content/posts/good-samaritan.html`
    - These files will be used by Plan 04 with `wp post create --post_content="$(cat content/about.html)"`

  </action>
  <verify>
    - `ls scripts/convert-heic.sh` exists and is executable
    - `ls content/*.html` shows 6 content files
    - `ls content/posts/*.html` shows 2 blog post files
    - Each content file contains clean HTML (no header/footer/nav/script tags)
  </verify>
  <done>
    - HEIC conversion script exists and any available HEIC files are converted
    - All 8 page content files extracted as clean HTML fragments in content/ directory
    - 2 blog post content files extracted in content/posts/
  </done>
</task>

</tasks>

<verification>
- Local by Flywheel site accessible at ambo-thoughts.local
- ChurchWP child theme active, parent theme installed
- All 3 bundled plugins active (ThemeSLR, WPBakery, RevSlider)
- Demo data visible on frontend (hero slider, sample pages)
- Content files ready in content/ directory for Plan 04
</verification>

<success_criteria>
Local WordPress development environment is fully operational with ChurchWP demo as baseline. All source content is prepared and ready for theme customization (Plan 03), content migration (Plan 04), and slider configuration (Plan 05).
</success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-01-SUMMARY.md`
</output>
