---
phase: 1-infrastructure-launch
plan: 04
type: execute
wave: 2
depends_on: [01]
files_modified:
  - scripts/migrate-content.sh
autonomous: false
requirements:
  - REQ-CONTENT-001
  - REQ-CONTENT-002
  - REQ-CONTENT-003
  - REQ-CONTENT-004
  - REQ-CONTENT-005
  - REQ-CONTENT-006
  - REQ-CONTENT-007
  - REQ-CONTENT-008
  - REQ-CONTENT-009
  - REQ-CONTENT-010
  - REQ-NEWS-001
  - REQ-NEWS-002
  - REQ-SPIRITUALITY-001
  - REQ-SPIRITUALITY-002
  - REQ-GALLERY-001
  - REQ-GALLERY-002
  - REQ-GALLERY-004
  - REQ-GALLERY-005
  - REQ-DESIGN-005
  - REQ-DESIGN-006
  - REQ-DESIGN-007
  - REQ-MIGRATION-004

must_haves:
  truths:
    - "About page displays Deacon Henry bio with photo"
    - "Spirituality page shows hero image (converted from HEIC) and St. Francis quote without watermark"
    - "Church News page has prominent buttons linking to VaticanNews.com and dioceseoftrenton.org/news"
    - "Contact page exists as a placeholder (form deferred)"
    - "Pictures page displays photo gallery with lightbox using FooGallery"
    - "Prayer Partner page has prayer chain content"
    - "Stuff page has miscellaneous content migrated"
    - "Videos page shows YouTube embeds via Embed Plus plugin"
    - "Homepage has Gallery section with 'New Life in the Spirit' YouTube embed"
    - "Homepage has Church News section with Vatican News and Diocese buttons"
    - "Homepage has Bio section with Deacon Henry preview"
    - "2 blog posts migrated (Holy Thursday, Good Samaritan)"
  artifacts:
    - path: "scripts/migrate-content.sh"
      provides: "WP-CLI content migration automation script"
  key_links:
    - from: "Pictures page"
      to: "FooGallery plugin"
      via: "FooGallery shortcode in page content"
    - from: "Videos page"
      to: "Embed Plus for YouTube"
      via: "YouTube embed blocks/shortcodes"
    - from: "Homepage"
      to: "Gallery/News/Bio sections"
      via: "WPBakery page builder rows"
---

<objective>
Migrate all existing content from the static HTML site into WordPress pages, upload images to the media library, install content plugins (FooGallery, Embed Plus, Smush), and configure the homepage sections.

Purpose: This is the bulk of the Phase 1 deliverable -- all 8 pages populated with real content, replacing ChurchWP demo content. The site transitions from a demo to the actual Ambo Thoughts ministry site.

Output: All 8 WordPress pages with real content, 2 blog posts, photo gallery configured, video embeds working, homepage sections (Gallery, News, Bio) populated.
</objective>

<context>
@.planning/PROJECT.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/plans/1-01-SUMMARY.md

Source content files:
@about.html
@spirituality.html
@church-news.html
@contact.html
@pictures.html
@prayer-partner.html
@stuff.html
@videos.html
@blog/2026-holy-thursday-reflection.html
@blog/sample-homily.html
@content/ (extracted HTML fragments from Plan 01)
</context>

<tasks>

<task type="auto">
  <name>Task 1: Install content plugins and upload media</name>
  <files>scripts/migrate-content.sh</files>
  <action>
    All work in Local by Flywheel "Open Site Shell". Create `scripts/migrate-content.sh` to document all commands.

    **A. Install and activate content plugins:**
    ```bash
    wp plugin install foogallery --activate        # REQ-GALLERY-001
    wp plugin install developer
    wp plugin install embed-plus-for-youtube --activate  # REQ-GALLERY-005, REQ-CONTENT-008
    wp plugin install wp-smushit --activate         # REQ-GALLERY-004
    ```

    **B. Upload images to WordPress media library:**
    Use `wp media import` for each image. All images are in the repo `images/` directory.

    Hero images (already JPEG):
    ```bash
    wp media import images/hero/hero-1.jpg --title="Ambo Thoughts Hero"
    wp media import images/hero/picture2.jpg --title="St. Francis Quote Background"
    wp media import images/hero/picture3.jpg --title="Psalm 46:10 Background"
    ```

    About page:
    ```bash
    wp media import images/deacon-henry.jpg --title="Deacon Henry Cugini"
    wp media import images/deacon-henry-hero.jpg --title="Deacon Henry Hero"
    ```

    Logo (already uploaded via Customizer in Plan 03, but ensure in media library):
    ```bash
    wp media import images/deacons-cross.png --title="Deacon's Cross Logo"
    ```

    Blog images:
    ```bash
    wp media import images/blog/holy-thursday.jpg --title="Holy Thursday"
    wp media import images/blog/good-samaritan.jpg --title="Good Samaritan"
    wp media import images/blog/lent.jpg --title="Lent"
    wp media import images/blog/sample-homily.jpg --title="Sample Homily"
    ```

    Gallery/other images:
    ```bash
    wp media import images/ambo-hero.jpg --title="Ambo Hero"
    wp media import images/church-bg.jpg --title="Church Background"
    wp media import images/stuff-photo.jpg --title="Stuff Photo"
    ```

    Converted HEIC images (from Plan 01, if available):
    ```bash
    # Import any converted images from images/converted/ directory
    for img in images/converted/*.jpg; do
      [ -f "$img" ] && wp media import "$img" --title="$(basename "${img%.*}")"
    done
    ```

    Hero slider images (easter vigil, midnight mass):
    ```bash
    wp media import images/hero/easter-vigil-candles.jpg --title="Easter Vigil Candles"
    wp media import images/hero/easter-vigil-procession.jpg --title="Easter Vigil Procession"
    wp media import images/hero/midnight-mass-incense.jpg --title="Midnight Mass Incense"
    ```

    **C. Run Smush bulk optimization** after all images are uploaded:
    - Go to WP Admin > Smush > Bulk Smush
    - Or trigger via: `wp smush optimize_library` (if WP-CLI extension available)

  </action>
  <verify>
    - `wp plugin list --status=active --format=csv` shows foogallery, embed-plus-for-youtube, wp-smushit
    - `wp media list --format=count` shows 15+ images in media library
    - Images are accessible in WP Admin > Media Library
  </verify>
  <done>
    - FooGallery, Embed Plus for YouTube, and Smush plugins installed and active
    - All site images uploaded to WordPress media library
    - Images optimized by Smush
  </done>
</task>

<task type="auto">
  <name>Task 2: Create all pages, blog posts, and configure homepage sections</name>
  <files>scripts/migrate-content.sh</files>
  <action>
    Continue in Local by Flywheel "Open Site Shell". Append commands to `scripts/migrate-content.sh`.

    **A. Delete ChurchWP demo content:**
    ```bash
    # Delete all demo pages (keep only what we'll create)
    wp post list --post_type=page --format=ids | xargs -I {} wp post delete {} --force
    # Delete all demo posts
    wp post list --post_type=post --format=ids | xargs -I {} wp post delete {} --force
    ```

    **B. Create pages using content from `content/` directory (from Plan 01):**

    For each page, use `wp post create` with the extracted HTML content. If content files from Plan 01 are clean HTML fragments, use them directly. Otherwise, extract content from the original HTML files.

    ```bash
    # About page (REQ-CONTENT-001)
    wp post create --post_type=page --post_title="About" --post_status=publish \
      --post_content="$(cat content/about.html)"

    # Spirituality page (REQ-CONTENT-002, REQ-SPIRITUALITY-001, REQ-SPIRITUALITY-002)
    # Must include: hero image (Spirituality Hero converted from HEIC), St. Francis quote without watermark
    wp post create --post_type=page --post_title="Spirituality" --post_status=publish \
      --post_content="$(cat content/spirituality.html)"

    # Church News page (REQ-CONTENT-003, REQ-NEWS-001, REQ-NEWS-002)
    # Must include: prominent buttons to VaticanNews.com and dioceseoftrenton.org/news
    wp post create --post_type=page --post_title="Church News" --post_status=publish \
      --post_content="$(cat content/church-news.html)"

    # Contact page -- PLACEHOLDER ONLY (form deferred per user decision)
    wp post create --post_type=page --post_title="Contact" --post_status=publish \
      --post_content="<p>For inquiries, please reach out to Deacon Henry Cugini.</p><p>Contact form coming soon.</p>"

    # Pictures/Gallery page (REQ-CONTENT-005, REQ-GALLERY-001)
    # Create a FooGallery first, then reference it
    wp post create --post_type=page --post_title="Pictures" --post_status=publish \
      --post_content="[foogallery id=\"GALLERY_ID\"]"

    # Prayer Partner page (REQ-CONTENT-006)
    wp post create --post_type=page --post_title="Prayer Partner" --post_status=publish \
      --post_content="$(cat content/prayer-partner.html)"

    # Stuff page (REQ-CONTENT-007)
    wp post create --post_type=page --post_title="Stuff" --post_status=publish \
      --post_content="$(cat content/stuff.html)"

    # Videos page (REQ-CONTENT-008)
    # YouTube embeds will use Embed Plus plugin's embed format
    wp post create --post_type=page --post_title="Videos" --post_status=publish \
      --post_content="$(cat content/videos.html)"

    # Homilies page (landing page -- CPT archive comes in Phase 2)
    wp post create --post_type=page --post_title="Homilies" --post_status=publish \
      --post_content="<p>Video homilies by Deacon Henry Cugini. Full archive coming soon.</p>"
    ```

    **C. Create blog posts (REQ-CONTENT-009):**
    ```bash
    wp post create --post_type=post --post_title="Holy Thursday: A Night of Service" \
      --post_status=publish --post_content="$(cat content/posts/holy-thursday.html)"

    wp post create --post_type=post --post_title="The Good Samaritan in Our Time" \
      --post_status=publish --post_content="$(cat content/posts/good-samaritan.html)"
    ```

    **D. Create FooGallery for Pictures page (REQ-GALLERY-001, REQ-GALLERY-002):**
    - In WP Admin > FooGallery > Add Gallery
    - Name: "Ministry Gallery"
    - Add all gallery photos from media library (hero images, easter vigil, midnight mass, etc.)
    - Set layout to responsive grid with lazy loading enabled
    - Enable lightbox
    - Copy the gallery shortcode and update the Pictures page content with the correct gallery ID

    **E. Set up homepage content (REQ-DESIGN-005, REQ-DESIGN-006, REQ-DESIGN-007):**

    Edit the homepage (front page) in WPBakery or via WP-CLI:

    1. **Gallery Section** -- "New Life in the Spirit" heading with YouTube embed:
       - Add YouTube embed for video ID `_a_zLTOxr0o` using Embed Plus shortcode or standard WordPress embed
       - Heading: "New Life in the Spirit"

    2. **Church News Section** -- Two prominent buttons:
       - Button 1: "Vatican News" linking to https://www.vaticannews.va/en.html
       - Button 2: "Diocese of Trenton News" linking to https://dioceseoftrenton.org/news

    3. **Bio Section** -- Deacon Henry preview:
       - Photo: deacon-henry.jpg from media library
       - Brief bio text (first paragraph from about.html)
       - "Read More" button linking to About page

    4. **Set as front page:**
    ```bash
    # Get homepage ID
    HOMEPAGE_ID=$(wp post list --post_type=page --name=home --field=ID 2>/dev/null || echo "")
    # If no "home" page, create one or use the existing front page
    wp option update show_on_front page
    wp option update page_on_front $HOMEPAGE_ID
    ```

    **F. Update navigation menu to point to real pages:**
    After all pages are created, update the menu items from Plan 03 to point to the actual page IDs:
    ```bash
    # Clear existing menu items and re-create with page IDs
    wp menu item list "Main Navigation" --format=ids | xargs -I {} wp menu item delete {}

    wp menu item add-post "Main Navigation" $HOMEPAGE_ID --title="Home"
    wp menu item add-post "Main Navigation" $HOMILIES_ID --title="Homilies"
    wp menu item add-post "Main Navigation" $SPIRITUALITY_ID --title="Spirituality"
    wp menu item add-post "Main Navigation" $CHURCHNEWS_ID --title="Church News"
    wp menu item add-post "Main Navigation" $ABOUT_ID --title="About"
    wp menu item add-post "Main Navigation" $STUFF_ID --title="Stuff"
    wp menu item add-post "Main Navigation" $PRAYERPARTNER_ID --title="Prayer Partner"
    wp menu item add-post "Main Navigation" $CONTACT_ID --title="Contact"
    ```

    **G. Motto display (REQ-CONTENT-010):**
    - Ensure "Preach the Gospel at all times and if necessary use words..." appears on:
      - Slider slide 2 (handled in Plan 05)
      - About page (as a prominent quote block within the bio content)
    - No watermark on the quote display

  </action>
  <verify>
    - `wp post list --post_type=page --post_status=publish --format=table` shows 9 pages (Home, About, Spirituality, Church News, Contact, Pictures, Prayer Partner, Stuff, Videos, Homilies)
    - `wp post list --post_type=post --post_status=publish --format=table` shows 2 blog posts
    - Visit each page in browser -- content displays correctly
    - Pictures page shows FooGallery with photos and lightbox works
    - Videos page shows YouTube embeds (lazy-loaded via Embed Plus)
    - Homepage shows Gallery section, Church News buttons, Bio preview
    - Navigation menu links to all real pages
  </verify>
  <done>
    - All 9 pages created and published with content from static site
    - 2 blog posts migrated
    - FooGallery configured on Pictures page with uploaded photos
    - YouTube embeds working on Videos page via Embed Plus
    - Homepage has 3 sections: Gallery (YouTube embed), Church News (external links), Bio (photo + text)
    - Navigation menu points to all real pages
    - Contact page is placeholder (form deferred)
    - Motto quote displayed on About page
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>All 8+ pages with migrated content, photo gallery, video embeds, and homepage sections.</what-built>
  <how-to-verify>
    1. Open Local by Flywheel site and visit each page:
       - **About**: Bio text visible, Deacon Henry photo displayed
       - **Spirituality**: Hero image visible, St. Francis quote (no watermark)
       - **Church News**: Two buttons (Vatican News, Diocese of Trenton) -- click both to verify links
       - **Contact**: Placeholder text (no form -- expected)
       - **Pictures**: Photo gallery with thumbnails, click to open lightbox
       - **Prayer Partner**: Prayer chain content
       - **Stuff**: Miscellaneous content
       - **Videos**: YouTube video embeds load and play
       - **Homilies**: Placeholder landing page
    2. Visit homepage:
       - Gallery section with "New Life in the Spirit" YouTube embed
       - Church News section with two external link buttons
       - Bio section with Deacon Henry photo and "Read More" link
    3. Test navigation: click each menu item, verify it goes to correct page
    4. Check blog: visit blog listing, verify 2 posts appear
  </how-to-verify>
  <resume-signal>Type "approved" or list pages that need content fixes.</resume-signal>
</task>

</tasks>

<verification>
- All pages accessible and rendering content
- Gallery lightbox functional
- YouTube embeds load (lazy-loaded via Embed Plus)
- Navigation menu complete and functional
- Homepage sections populated
</verification>

<success_criteria>
All existing static site content is now living in WordPress pages with proper media, galleries, and video embeds. The site looks and feels like the Ambo Thoughts ministry site, not a ChurchWP demo.
</success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-04-SUMMARY.md`
</output>
