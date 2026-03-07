---
phase: 1-infrastructure-launch
plan: 03
type: execute
wave: 2
depends_on: [01]
files_modified:
  - wp-content/themes/churchwp-child/style.css
  - wp-content/themes/churchwp-child/functions.php
  - wp-content/themes/churchwp-child/css/custom.css
  - wp-content/themes/churchwp-child/header.php
autonomous: false
requirements:
  - REQ-THEME-003
  - REQ-THEME-004
  - REQ-DESIGN-001
  - REQ-DESIGN-002
  - REQ-DESIGN-008
  - REQ-DESIGN-009

must_haves:
  truths:
    - "Site displays Navy (#001f5b) and Gold (#c9a84c) color scheme instead of ChurchWP default green"
    - "Header shows centered cross logo on Navy background with white border, no phone/address"
    - "Navigation menu shows all 8 items: Home, Homilies, Spirituality, Church News, About, Stuff, Prayer Partner, Contact"
    - "Headings use Playfair Display font, body uses system sans-serif"
    - "The 'church love, faith love' demo section is removed from homepage"
    - "Branding text reads 'Ambo Thoughts' (H1), 'Spiritual Direction & Bereavement' (H2), 'with Deacon Cugini' (H2)"
  artifacts:
    - path: "wp-content/themes/churchwp-child/css/custom.css"
      provides: "Navy/Gold CSS custom properties and color overrides"
      contains: "--navy: #001f5b"
    - path: "wp-content/themes/churchwp-child/header.php"
      provides: "Custom header with cross logo, no contact info"
    - path: "wp-content/themes/churchwp-child/functions.php"
      provides: "Enqueue parent styles, custom.css, Google Fonts"
  key_links:
    - from: "churchwp-child/functions.php"
      to: "churchwp-child/css/custom.css"
      via: "wp_enqueue_style in functions.php"
    - from: "churchwp-child/header.php"
      to: "images/deacons-cross.png"
      via: "logo image reference"
---

<objective>
Customize the ChurchWP child theme with Navy/Gold branding, custom header layout, typography, and navigation menu. Remove irrelevant demo sections.

Purpose: This transforms the generic ChurchWP demo into the Ambo Thoughts visual identity. All subsequent content work (Plan 04, Plan 05) will appear within this customized design.

Output: Child theme files with Navy/Gold colors, Playfair Display typography, custom header with cross logo, and navigation menu configured.
</objective>

<context>
@.planning/PROJECT.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/RESEARCH.md
@.planning/phases/1/plans/1-01-SUMMARY.md

Source files to reference:
@css/style.css (existing color variables to replicate)
@images/deacons-cross.png (logo file)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Apply Navy/Gold colors, typography, and header customization</name>
  <files>
    wp-content/themes/churchwp-child/style.css
    wp-content/themes/churchwp-child/functions.php
    wp-content/themes/churchwp-child/css/custom.css
    wp-content/themes/churchwp-child/header.php
  </files>
  <action>
    All work happens in the Local by Flywheel site at `~/Local Sites/ambo-thoughts/app/public/`.
    Use "Open Site Shell" in Local for any WP-CLI commands.

    **A. Theme Panel settings first (via WP-CLI or WordPress admin):**
    - Set primary color to Navy (#001f5b) via Theme Panel > Styling
    - Set accent/secondary color to Gold (#c9a84c)
    - Upload `images/deacons-cross.png` as site logo via Appearance > Customize > Site Identity
    - Set site title to "Ambo Thoughts", tagline to "Spiritual Direction & Bereavement"
    - Try Theme Panel first for every color/font change -- only use CSS for what the panel misses

    **B. Create `css/custom.css` in child theme** with CSS custom properties:
    ```css
    :root {
      --navy: #001f5b;
      --navy-light: #0a2d6e;
      --navy-dark: #00132e;
      --gold: #c9a84c;
      --gold-light: #d4b968;
      --cream: #f5f0e8;
      --white: #ffffff;
      --text-dark: #2c2c2c;
      --text-muted: #6b7280;
      --blue-accent: #1a80b6;
    }
    ```
    - Override ChurchWP's default green/blue accent colors with Navy/Gold throughout:
      - Header background: var(--navy)
      - Links and buttons: var(--gold)
      - Button hover states: var(--gold-light)
      - Footer background: var(--navy-dark)
      - Section backgrounds alternating between white and cream
    - Inspect the ChurchWP demo site to identify all CSS selectors that use the default green color and override each one
    - Add Playfair Display import and typography rules:
      - `@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');`
      - Headings (h1-h6): font-family: 'Playfair Display', serif
      - Body: font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

    **C. Update `functions.php`:**
    - Ensure parent theme styles are enqueued properly
    - Enqueue `css/custom.css` after parent styles (so overrides work)
    - Register Google Fonts (Playfair Display) if not using @import in CSS

    **D. Create `header.php` override:**
    - Copy ONLY header.php from parent theme to child theme
    - Modify to:
      - Center the cross logo (deacons-cross.png) with increased size
      - Navy background with white border (make border bigger than default)
      - Remove phone number and address fields from header (ChurchWP default includes these)
      - Keep the navigation menu area
    - Do NOT copy all parent template files -- only header.php and footer.php per REQ-THEME-002

    **E. Configure navigation menu via WP-CLI:**
    In Local Site Shell:
    ```bash
    wp menu create "Main Navigation"
    wp menu location assign "Main Navigation" primary
    ```
    Create menu items in order (pages will be created in Plan 04, so use custom links or page IDs from demo):
    - Home (front page)
    - Homilies
    - Spirituality
    - Church News
    - About
    - Stuff
    - Prayer Partner
    - Contact

    **F. Remove irrelevant demo sections:**
    - Identify and remove the "church love, faith love" section from the ChurchWP homepage template
    - This may require editing the homepage in WPBakery or removing a WPBakery row from the page content
    - If it's a widget, remove via `wp widget delete`

  </action>
  <verify>
    In Local by Flywheel, visit the site:
    - Header shows cross logo centered on Navy background, no phone/address
    - No green/default ChurchWP colors visible -- all Navy/Gold
    - Navigation shows 8 menu items
    - Headings render in Playfair Display (check DevTools > Computed > font-family)
    - "church love, faith love" section is gone from homepage
  </verify>
  <done>
    - Child theme CSS applies Navy/Gold palette everywhere (no ChurchWP default green remaining)
    - Header displays cross logo centered, Navy background, white border, no contact info
    - Playfair Display loads for headings, system sans-serif for body
    - Navigation menu has all 8 items in correct order
    - Homepage "church love, faith love" section removed
    - Branding text correct: "Ambo Thoughts", "Spiritual Direction & Bereavement"
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Navy/Gold theme customization with custom header, typography, navigation, and removed irrelevant demo sections.</what-built>
  <how-to-verify>
    1. Open Local by Flywheel, click "Open Site" for ambo-thoughts
    2. Check header: cross logo centered, Navy background, white border, NO phone/address
    3. Check colors: Navy and Gold throughout, no green/default ChurchWP colors
    4. Check navigation: 8 menu items visible (Home, Homilies, Spirituality, Church News, About, Stuff, Prayer Partner, Contact)
    5. Check typography: headings should look serif/elegant (Playfair Display)
    6. Scroll homepage: "church love, faith love" section should be gone
    7. Check site title area: "Ambo Thoughts" branding visible
  </how-to-verify>
  <resume-signal>Type "approved" or describe what needs adjustment (e.g., "gold is too dark", "menu order wrong", "logo too small").</resume-signal>
</task>

</tasks>

<verification>
- `ls ~/Local\ Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/css/custom.css` exists
- `ls ~/Local\ Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/header.php` exists
- `grep "#001f5b" ~/Local\ Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/css/custom.css` finds Navy color
- `wp menu list` shows "Main Navigation" with 8 items
</verification>

<success_criteria>
The local WordPress site visually matches the Ambo Thoughts Navy/Gold brand identity with correct header layout, typography, and navigation. Ready for content to be placed into this design (Plan 04) and hero slider to be configured (Plan 05).
</success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-03-SUMMARY.md`
</output>
