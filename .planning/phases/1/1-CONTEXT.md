# Phase 1 Context: Infrastructure + Launch Site

**Phase Goal:** Visitors can access the full Ambo Thoughts site on a secure, performant WordPress VPS with all existing content migrated from GitHub Pages

---

## Decisions

### 1. Local Development Environment

**Decision:** Use Local by Flywheel (not Docker, not MAMP)
**Rationale:** Zero-config WordPress dev, GUI-based, built-in WP-CLI, matches production stack settings. User approved this approach. ChurchWP docs reference standard WordPress admin panels which Local by Flywheel provides out of the box.

### 2. Demo Import Strategy

**Decision:** Import ChurchWP demo data first, then customize
**Rationale:** The demo import (`sampledata/content.xml`, `theme-options.txt`, `widgets.wie`, slider exports) gives us the full ChurchWP layout as a starting point. We then:

1. Import demo data via Theme Panel > Demo Importer
2. Import Revolution Slider templates (`main_home_slider.zip`)
3. Customize Theme Panel colors/fonts to Navy/Gold
4. Replace demo content page-by-page with Ambo Thoughts content
5. Delete unused demo pages/posts when done

This is faster than building from scratch because ChurchWP's layout structure (header, footer, widget areas, slider) is already configured in the demo.

### 3. SMTP Provider & Contact Form

**Decision:** DEFERRED — skip contact form setup for Phase 1
**Rationale:** User requested skipping contact form for now. CF7, Flamingo, WP Mail SMTP, and Resend configuration will be handled in a later pass. Contact page will exist as a placeholder.

### 4. Content Migration Approach

**Decision:** WP-CLI automation where possible, WPBakery for visual layout
**Rationale:** User prefers automation via WP-CLI. Use `wp post create` for pages/posts, `wp media import` for images, `wp menu` for navigation setup. WPBakery only for visual layout adjustments that can't be scripted.

**Content source mapping:**
| Source File | WordPress Page | Key Content |
|-------------|---------------|-------------|
| `about.html` | About | Bio text, `deacon-henry.jpg` photo |
| `spirituality.html` | Spirituality | Hero image (convert HEIC), St. Francis quote |
| `church-news.html` | Church News | Vatican News + Diocese of Trenton buttons |
| `contact.html` | Contact | CF7 form (replace Formspree) |
| `pictures.html` | Pictures | FooGallery with /Hank/ photos |
| `prayer-partner.html` | Prayer Partner | Prayer chain info + contact link |
| `stuff.html` | Stuff | Misc content |
| `videos.html` | Videos | YouTube embeds via Embed Plus |
| `blog/*.html` | Blog posts | 2 posts: Holy Thursday, Good Samaritan |

### 5. VPS Setup Approach

**Decision:** DigitalOcean $6/mo droplet, manual LEMP stack setup (not managed WordPress hosting)
**Rationale:** Full control, matches research recommendations. Stack: Ubuntu 24.04 LTS, Nginx 1.24+, PHP-FPM 8.3, MariaDB 10.11 LTS, Redis, Certbot. User confirmed using their own DigitalOcean account.

### 6. Domain Strategy

**Decision:** Skip domain for now, use VPS IP address initially
**Rationale:** User explicitly said "skip domain." We'll set up WordPress with the VPS IP, configure SSL later when domain is ready. DNS cutover will be a separate step. All nginx configs and wp-config values will be designed for easy domain swap via `wp search-replace`.

### 7. Hero Slider Content

**Decision:** 3 slides using Revolution Slider (bundled with ChurchWP)
**Rationale:** PROJECT.md specifies exactly 3 slides (down from the current 4):

1. "Ambo Thoughts" / Subtitles: Spirituality, Bereavement — background: `hero/hero-1.jpg`
2. "Preach the Gospel at all times; use words when necessary." / St. Francis — background: `hero/picture2.jpg`
3. "Be still, and know that I am God" / Psalm 46:10 — background: `hero/picture3.jpg`

Import `main_home_slider.zip` as template, then customize slides.

### 8. Header Layout

**Decision:** Cross logo centered, Navy background, white border, no contact info
**Rationale:** Per PROJECT.md — remove phone/address from ChurchWP default header. Use `images/deacons-cross.png` (180KB, already exists). Menu items: Home, Homilies, Spirituality, Church News, About, Stuff, Prayer Partner, Contact.

### 9. Homepage Sections (Phase 1 scope)

**Decision:** 3 sections for Phase 1, defer Latest Homilies to Phase 2
**Rationale:** REQ-DESIGN-004 (Latest Homilies) is assigned to Phase 2 since it depends on Homily CPT. Phase 1 homepage delivers:

1. **Gallery Section** — "New Life in the Spirit" + YouTube embed (`_a_zLTOxr0o`)
2. **Church News Section** — Buttons to Vatican News + Diocese of Trenton
3. **Bio Section** — Deacon Henry preview with link to About page
4. Remove "church love, faith love" section from ChurchWP template

### 10. Image Handling

**Decision:** Batch convert HEIC locally with `sips`, upload JPEG/WebP
**Rationale:** Per research — server-side HEIC support is fragile (requires ImageMagick 7.0.8-26+ with libheif). Convert before upload using macOS `sips` command. Smush plugin handles compression on upload.

**Existing images ready to use (no conversion needed):**

- `images/deacons-cross.png` — Logo
- `images/deacon-henry.jpg` — About page photo
- `images/deacon-henry-hero.jpg` — Hero variant
- `images/ambo-hero.jpg` — Hero background
- `images/hero/*.jpg` — All 7 hero slider images
- `images/blog/*.jpg` — All 4 blog images
- `images/church-bg.jpg` — Contact section background

**Needs HEIC conversion (from iCloud /Hank/):**

- `Cover2.HEIC`, `Spirituality Hero.heic`, `Hero-1.HEIC`
- Any HEIC files in `High Res/` directory

---

## Code Context

### Reusable from Current Site

| Asset               | Location                     | Reuse in WordPress                              |
| ------------------- | ---------------------------- | ----------------------------------------------- |
| Color palette       | `css/style.css` `:root` vars | Map to child theme CSS custom properties        |
| Logo                | `images/deacons-cross.png`   | WordPress Site Identity / header                |
| Hero images         | `images/hero/*.jpg`          | Revolution Slider backgrounds                   |
| Blog images         | `images/blog/*.jpg`          | WordPress media library                         |
| Deacon photos       | `images/deacon-henry*.jpg`   | About page, bio section                         |
| About bio text      | `about.html`                 | Copy to About page in WP                        |
| Contact form fields | `contact.html`               | Recreate in CF7 (Name, Email, Subject, Message) |
| Prayer partner text | `prayer-partner.html`        | Copy to Prayer Partner page                     |
| Nav structure       | All HTML files               | WordPress menu (8 items)                        |

### ChurchWP Package Assets

| Asset              | Location                                                               | Purpose                 |
| ------------------ | ---------------------------------------------------------------------- | ----------------------- |
| Parent theme       | `~/Downloads/churchwp_package/theme/churchwp.zip`                      | Install as parent theme |
| Child theme        | `~/Downloads/churchwp_package/theme/churchwp-child.zip`                | Base for customizations |
| WPBakery           | `~/Downloads/churchwp_package/plugins/js_composer.zip`                 | Page builder (bundled)  |
| Revolution Slider  | `~/Downloads/churchwp_package/plugins/revslider.zip`                   | Hero slider             |
| ThemeSLR Framework | `~/Downloads/churchwp_package/plugins/themeslr-framework-churchwp.zip` | Theme options panel     |
| Demo content       | `~/Downloads/churchwp_package/sampledata/content.xml`                  | Demo import baseline    |
| Theme options      | `~/Downloads/churchwp_package/sampledata/theme-options.txt`            | Theme panel settings    |
| Widgets            | `~/Downloads/churchwp_package/sampledata/widgets.wie`                  | Widget configuration    |
| Hero slider        | `~/Downloads/churchwp_package/sampledata/main_home_slider.zip`         | RevSlider template      |

### Key Integration Points

1. **Formspree → CF7**: Replace `https://formspree.io/f/deacon267@verizon.net` with CF7 form. Add second recipient `hcugini@stroberts.cc`.
2. **Static hero → RevSlider**: Current 4-slide vanilla JS slider becomes 3-slide Revolution Slider with same content.
3. **Netlify Identity → Remove**: The `admin/index.html` and Netlify CMS integration are no longer needed (was from Decap CMS project). Delete completely.
4. **GitHub Pages → VPS**: All static files become WordPress pages. Nginx handles old URL redirects.

---

## Deferred Ideas

- RSS feed for spirituality page (verseoftheday.com) → Phase 2
- Latest Homilies homepage section → Phase 2 (needs Homily CPT)
- Bible Verse of the Day plugin → Phase 2
- Homily CPT and pipeline integration → Phase 2
- Admin role management and training → Phase 3
- UptimeRobot monitoring → Phase 3

---

## Phase Boundary

This phase delivers a complete, static-content WordPress site. All pages have content, but the homily system is NOT built yet — the Videos page will have manual YouTube embeds, not CPT-driven content. The homepage will have 3 sections (Gallery, News, Bio) but NOT the Latest Homilies section.
