---
phase: 1-infrastructure-launch
plan: 05
type: execute
wave: 2
depends_on: [01]
files_modified: []
autonomous: false
requirements:
  - REQ-DESIGN-003

must_haves:
  truths:
    - "Homepage hero slider cycles through exactly 3 slides automatically"
    - "Slide 1 shows 'Ambo Thoughts' with subtitles 'Spirituality' and 'Bereavement'"
    - "Slide 2 shows 'Preach the Gospel at all times; use words when necessary.' attributed to St. Francis of Assisi"
    - "Slide 3 shows 'Be still, and know that I am God' attributed to Psalm 46:10"
    - "Each slide has an appropriate hero background image"
  artifacts: []
  key_links:
    - from: "Revolution Slider"
      to: "Homepage"
      via: "RevSlider shortcode or widget in homepage template"
---

<objective>
Configure the Revolution Slider with 3 slides matching the Ambo Thoughts branding -- specific text, backgrounds, and styling per the locked design decisions.

Purpose: The hero slider is the first thing visitors see. It establishes the ministry identity with the site name, St. Francis quote, and Psalm 46:10.

Output: 3-slide Revolution Slider configured and displaying on the homepage with correct text, backgrounds, and Navy/Gold styling.
</objective>

<context>
@.planning/PROJECT.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/plans/1-01-SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Configure Revolution Slider with 3 slides</name>
  <action>
    Work in Local by Flywheel WordPress admin. The demo import from Plan 01 should have imported the `main_home_slider.zip` Revolution Slider template. We will customize it to have exactly 3 slides.

    **A. Open Revolution Slider editor:**
    - Go to WP Admin > Slider Revolution
    - Find the imported homepage slider (likely named "Main Home Slider" or similar from demo)
    - If no slider was imported, create a new slider named "Ambo Thoughts Hero"

    **B. Configure slider settings:**
    - Auto-rotation: ON (cycle through slides)
    - Transition delay: 5-7 seconds per slide
    - Transition effect: fade or slide (keep it elegant, not flashy)
    - Navigation: dots or arrows (minimal)
    - Full-width layout

    **C. Configure Slide 1:**
    - Background image: `images/hero/hero-1.jpg` (upload from media library if not already there)
    - Text layers:
      - H1: "Ambo Thoughts" (large, centered, white or gold text)
      - H2: "Spiritual Direction & Bereavement" (smaller, below H1)
      - H2: "with Deacon Cugini" (below the subtitle)
    - Text styling: Playfair Display font if available in RevSlider, white text with subtle shadow for readability
    - Optional: Navy overlay on background for text readability

    **D. Configure Slide 2:**
    - Background image: `images/hero/picture2.jpg`
    - Text layers:
      - Main quote: "Preach the Gospel at all times; use words when necessary." (elegant, centered)
      - Attribution: "-- St. Francis of Assisi" (smaller, italic, below quote)
    - No watermark on the quote (per REQ-SPIRITUALITY-002 / REQ-CONTENT-010)
    - Text styling: white or cream text, Playfair Display for quote, italic for attribution

    **E. Configure Slide 3:**
    - Background image: `images/hero/picture3.jpg`
    - Text layers:
      - Main quote: "Be still, and know that I am God" (elegant, centered)
      - Attribution: "-- Psalm 46:10" (smaller, below quote)
    - Text styling: consistent with slide 2

    **F. Delete any extra slides from demo import:**
    - The demo may have 4+ slides -- delete all except the 3 we configured
    - Ensure exactly 3 slides remain

    **G. Ensure slider displays on homepage:**
    - Verify the slider shortcode is in the homepage content (or RevSlider widget is in the correct widget area)
    - If not displaying, add the RevSlider shortcode to the homepage: `[rev_slider alias="slider-alias"]`
    - The alias comes from the slider settings in RevSlider editor

  </action>
  <verify>
    - Visit the homepage in browser
    - Slider auto-cycles through exactly 3 slides
    - Slide 1: "Ambo Thoughts" / "Spiritual Direction & Bereavement" / "with Deacon Cugini"
    - Slide 2: St. Francis quote with attribution
    - Slide 3: Psalm 46:10 with attribution
    - All slides have background images
    - Text is readable against backgrounds
  </verify>
  <done>
    - Revolution Slider has exactly 3 slides with correct text and backgrounds
    - Slider auto-rotates on homepage
    - Text styling is Navy/Gold themed and readable
    - No extra demo slides remain
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>3-slide Revolution Slider with Ambo Thoughts branding, St. Francis quote, and Psalm 46:10.</what-built>
  <how-to-verify>
    1. Open Local by Flywheel site homepage
    2. Watch the slider cycle through all 3 slides (wait ~15 seconds)
    3. Verify Slide 1: "Ambo Thoughts" title with subtitles, hero background image
    4. Verify Slide 2: St. Francis quote, no watermark, attributed correctly
    5. Verify Slide 3: Psalm 46:10, attributed correctly
    6. Check text readability against background images
    7. Check that navigation dots/arrows work for manual slide switching
    8. Confirm no extra demo slides (only 3 total)
  </how-to-verify>
  <resume-signal>Type "approved" or describe what needs adjustment (e.g., "text too small", "wrong background on slide 2", "add more delay between slides").</resume-signal>
</task>

</tasks>

<verification>
- Slider displays on homepage with 3 slides
- Auto-rotation works
- Each slide has correct text content per CONTEXT.md Decision 7
</verification>

<success_criteria>
The homepage hero slider matches the locked design decision: 3 slides cycling through "Ambo Thoughts" branding, St. Francis quote, and Psalm 46:10 with appropriate hero background images and Navy/Gold styling.
</success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-05-SUMMARY.md`
</output>
