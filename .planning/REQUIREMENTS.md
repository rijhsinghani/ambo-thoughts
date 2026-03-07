# Requirements: Ambo Thoughts WordPress Redesign

**Version:** 1.0
**Date:** 2026-03-07
**Source:** PROJECT.md, research/SUMMARY.md

---

## HOSTING

### REQ-HOSTING-001: VPS Provisioning

**Priority:** P0
**Phase:** 1
DigitalOcean Droplet (1 vCPU, 1GB RAM, 25GB SSD) running Ubuntu 24.04 LTS. Estimated cost ~$6/mo.

### REQ-HOSTING-002: Web Server Stack

**Priority:** P0
**Phase:** 1
Nginx 1.24+ as web server with PHP-FPM 8.3 (ppa:ondrej/php) and MariaDB 10.11 LTS as database.

### REQ-HOSTING-003: Security Hardening

**Priority:** P0
**Phase:** 1
SSH key-only authentication (disable password auth). UFW firewall allowing only ports 80, 443, and SSH. fail2ban installed and configured. Disable xmlrpc.php in Nginx config. File permissions: directories 755, files 644, wp-config.php 600.

### REQ-HOSTING-004: SSL Certificate

**Priority:** P0
**Phase:** 1
Certbot + Let's Encrypt for free SSL. Force HTTP-to-HTTPS redirect in Nginx. Install WordPress as HTTPS from day one to prevent mixed content issues.

### REQ-HOSTING-005: Automated Backups

**Priority:** P0
**Phase:** 1
UpdraftPlus plugin configured for automated backups to Google Drive. Must include both database and file backups.

### REQ-HOSTING-006: Page Caching

**Priority:** P1
**Phase:** 1
Nginx FastCGI cache (disk-based) for full-page caching -- serves HTML without invoking PHP. Do NOT install WP Super Cache. PHP-FPM configured with `pm = ondemand`, `max_children = 5` for 1GB VPS.

### REQ-HOSTING-007: Object Caching

**Priority:** P1
**Phase:** 1
Redis server installed on VPS. Redis Object Cache plugin (by Till Kruss) for database query caching. Limit post revisions to 5.

### REQ-HOSTING-008: Security Plugin

**Priority:** P0
**Phase:** 1
Wordfence plugin for firewall, login protection, and malware scanning. No second security plugin.

### REQ-HOSTING-009: wp-config.php Environment Management

**Priority:** P0
**Phase:** 1
Mark Jaquith's `local-config.php` pattern. Local config gitignored, production uses environment variables. `DISALLOW_FILE_EDIT: true` in production.

### REQ-HOSTING-010: Deployment Pipeline

**Priority:** P1
**Phase:** 1
Local by Flywheel for development. Git tracks `wp-content/themes/churchwp-child/`, `scripts/`, `.gitignore`. Deploy via rsync over SSH + WP-CLI. Git ignores WordPress core, parent theme, `wp-config.php`, `uploads/`, plugin directories. Database sync is production-to-local only via `wp db export` + `wp search-replace`.

---

## THEME

### REQ-THEME-001: ChurchWP Parent Theme

**Priority:** P0
**Phase:** 1
Purchase and install ChurchWP from ThemeForest (~$59). Install bundled plugins: ThemeSLR Framework, WPBakery Page Builder, Slider Revolution.

### REQ-THEME-002: Child Theme Setup

**Priority:** P0
**Phase:** 1
All customizations in `churchwp-child/` directory. Never edit parent theme files. Override only `header.php` and `footer.php` from parent -- do not copy all templates. Document all overridden files.

### REQ-THEME-003: Color Customization

**Priority:** P0
**Phase:** 1
Replace ChurchWP default green with Navy/Gold scheme. Use ChurchWP Theme Panel first for global colors, then CSS custom properties for what the panel misses:

- `--navy: #001f5b`
- `--navy-light: #0a2d6e`
- `--navy-dark: #00132e`
- `--gold: #c9a84c`
- `--gold-light: #d4b968`
- `--cream: #f5f0e8`
- `--white: #ffffff`
- `--text-dark: #2c2c2c`
- `--text-muted: #6b7280`
- `--blue-accent: #1a80b6`

### REQ-THEME-004: Typography

**Priority:** P1
**Phase:** 1
Playfair Display for headings, system sans-serif stack for body text. Configure via Theme Panel or child theme CSS.

### REQ-THEME-005: Bundled Plugin Compatibility

**Priority:** P0
**Phase:** 1
Verify ChurchWP bundled plugin versions (ThemeSLR, WPBakery, Slider Revolution) are compatible with PHP 8.3. Test in Local by Flywheel before production deployment.

---

## DESIGN

### REQ-DESIGN-001: Header

**Priority:** P0
**Phase:** 1
Cross logo (`images/deacons-cross.png`) centered in header. Navy background with white border (enlarged). Remove phone/address from ChurchWP default header layout.

### REQ-DESIGN-002: Navigation Menu

**Priority:** P0
**Phase:** 1
Menu items: Home, Homilies, Spirituality, Church News, About, Stuff, Prayer Partner, Contact. Menu extends right to accommodate multi-word items.

### REQ-DESIGN-003: Hero Slider

**Priority:** P0
**Phase:** 1
Slider Revolution with 3 slides:

1. "Ambo Thoughts" with subtitles "Spirituality" and "Bereavement"
2. "Preach the Gospel at all times; use words when necessary." -- St. Francis of Assisi
3. "Be still, and know that I am God" -- Psalm 46:10

### REQ-DESIGN-004: Homepage Latest Homilies Section

**Priority:** P1
**Phase:** 2
Section labeled "Homilies" (not "Sermons"). Show latest video homily cards. Links to full homilies archive. Depends on Homily CPT (REQ-HOMILY-001).

### REQ-DESIGN-005: Homepage Gallery Section

**Priority:** P1
**Phase:** 1
"New Life in the Spirit" theme. Featured YouTube video embed (`_a_zLTOxr0o`).

### REQ-DESIGN-006: Homepage Church News Section

**Priority:** P1
**Phase:** 1
Buttons linking to VaticanNews.com and dioceseoftrenton.org/news.

### REQ-DESIGN-007: Homepage Bio Section

**Priority:** P1
**Phase:** 1
Deacon Henry bio preview with link to full About page. Content: ordained 2008, Co-Cathedral of St. Robert Bellarmine, Freehold NJ.

### REQ-DESIGN-008: Remove Irrelevant ChurchWP Sections

**Priority:** P0
**Phase:** 1
Remove "church love, faith love" section from ChurchWP homepage template. Not relevant to this ministry.

### REQ-DESIGN-009: Branding Text

**Priority:** P0
**Phase:** 1
H1: "Ambo Thoughts". H2: "Spiritual Direction & Bereavement". H2: "with Deacon Cugini". Spelling is "Ambo Thoughts" (ambo = church pulpit/lectern).

---

## CONTENT

### REQ-CONTENT-001: About Page

**Priority:** P0
**Phase:** 1
Migrate existing bio content. Deacon Henry Cugini -- ordained Roman Catholic Permanent Deacon, Diocese of Trenton. Ordained by Bishop Smith on May 8, 2008. Assigned to Co-Cathedral of St. Robert Bellarmine, Freehold, NJ. Ministries: Spiritual Direction, Annulment Advocate, Hospital/Homebound, Bereavement. Certified Spiritual Director, Pastoral Counselor, Bereavement Counselor/Facilitator. Professed member of Third Order of St. Francis (Secular Franciscan).

### REQ-CONTENT-002: Spirituality Page

**Priority:** P0
**Phase:** 1
See REQ-SPIRITUALITY requirements for full specification.

### REQ-CONTENT-003: Church News Page

**Priority:** P0
**Phase:** 1
See REQ-NEWS requirements for full specification.

### REQ-CONTENT-004: Contact Page

**Priority:** P0
**Phase:** 1
See REQ-CONTACT requirements for full specification.

### REQ-CONTENT-005: Pictures/Gallery Page

**Priority:** P0
**Phase:** 1
See REQ-GALLERY requirements for full specification.

### REQ-CONTENT-006: Prayer Partner Page

**Priority:** P0
**Phase:** 1
Migrate prayer chain signup/information content from `prayer-partner.html`.

### REQ-CONTENT-007: Stuff Page

**Priority:** P1
**Phase:** 1
Migrate miscellaneous content from `stuff.html`.

### REQ-CONTENT-008: Videos Page

**Priority:** P0
**Phase:** 1
Video homilies archive with YouTube embeds. Use Embed Plus for YouTube plugin for lazy-loaded responsive video embeds.

### REQ-CONTENT-009: Blog Post Migration

**Priority:** P1
**Phase:** 1
Migrate existing blog posts to WordPress:

- `blog/2026-holy-thursday-reflection.html` -- "Holy Thursday: A Night of Service"
- `blog/sample-homily.html` -- "The Good Samaritan in Our Time"

### REQ-CONTENT-010: Motto Display

**Priority:** P1
**Phase:** 1
"Preach the Gospel at all times and if necessary use words..." displayed prominently (hero slider slide 2 and About page). No watermark on quote display.

---

## HOMILY

### REQ-HOMILY-001: Custom Post Type Registration

**Priority:** P0
**Phase:** 2
Register `homily` CPT in child theme's `inc/homily-cpt.php`. `show_in_rest: true` for REST API and Gutenberg support. No sermon plugin -- CPT is permanent, portable, and maps to pipeline output.

### REQ-HOMILY-002: Taxonomies

**Priority:** P0
**Phase:** 2
Custom taxonomy `homily_season` with terms: Advent, Lent, Easter, Ordinary Time, and other liturgical seasons as needed. Taxonomy registered with `show_in_rest: true`.

### REQ-HOMILY-003: Custom Meta Fields

**Priority:** P0
**Phase:** 2
Meta fields registered for homily CPT: `youtube_id`, `pull_quote`, `scripture_refs`, `transcript`, `drive_file_id`, `homily_date`. All exposed via REST API.

### REQ-HOMILY-004: Single Homily Template

**Priority:** P0
**Phase:** 2
`single-homily.php` in child theme. Use standard WordPress template tags, NOT WPBakery shortcodes (avoid lock-in). Display YouTube embed, pull quote, scripture references, transcript, and liturgical season.

### REQ-HOMILY-005: Homily Archive Template

**Priority:** P0
**Phase:** 2
`archive-homily.php` in child theme with filtering by liturgical season taxonomy. Paginated list of homily cards.

### REQ-HOMILY-006: REST API Endpoint

**Priority:** P0
**Phase:** 2
REST endpoint at `wp-json/wp/v2/homilies` for pipeline integration. Authentication via WordPress Application Passwords (built into core since WP 5.6). Credentials in environment variables, never in code.

### REQ-HOMILY-007: Pipeline Integration

**Priority:** P0
**Phase:** 2
Adapt existing `process_homilies.py` to POST to WordPress REST API instead of generating static HTML. Create `wp_publisher.py` module. Uses YouTube Data API + Google Drive API via Application Default Credentials (ADC).

### REQ-HOMILY-008: Existing Homily Content Migration

**Priority:** P1
**Phase:** 2
Migrate existing homily content from old site (blog posts, video pages) into the Homily CPT.

---

## NEWS

### REQ-NEWS-001: Vatican News Link

**Priority:** P0
**Phase:** 1
Prominent button/link to VaticanNews.com on Church News page and homepage Church News section.

### REQ-NEWS-002: Diocese of Trenton Link

**Priority:** P0
**Phase:** 1
Prominent button/link to dioceseoftrenton.org/news on Church News page and homepage Church News section.

---

## SPIRITUALITY

### REQ-SPIRITUALITY-001: Hero Image

**Priority:** P0
**Phase:** 1
Hero image from `Spirituality Hero.heic` (converted to JPEG/WebP per REQ-GALLERY-003).

### REQ-SPIRITUALITY-002: Gospel Quote

**Priority:** P0
**Phase:** 1
"Preach the Gospel at all times; use words when necessary" -- St. Francis of Assisi. Displayed without watermark.

### REQ-SPIRITUALITY-003: Bible Verse Feed

**Priority:** P2
**Phase:** 2
Bible Verse of the Day plugin for daily scripture display. Investigate RSS feeds from verseoftheday.com or daily Catholic bible verse sources.

---

## CONTACT

### REQ-CONTACT-001: Dual-Email Contact Form

**Priority:** P0
**Phase:** 1
Contact Form 7 form that sends submissions to BOTH deacon267@verizon.net AND hcugini@stroberts.cc simultaneously.

### REQ-CONTACT-002: Form Submission Storage

**Priority:** P1
**Phase:** 1
Flamingo plugin to store all CF7 submissions in the WordPress database as backup in case email delivery fails.

### REQ-CONTACT-003: Spam Prevention

**Priority:** P0
**Phase:** 1
Contact Form 7 built-in spam prevention (honeypot, quiz, or reCAPTCHA). Wordfence firewall provides additional bot protection.

### REQ-CONTACT-004: WP Mail SMTP

**Priority:** P0
**Phase:** 1
WP Mail SMTP plugin configured for reliable email delivery (VPS mail goes to spam without it). Recommended provider: Resend (already in use across other projects). Set SPF/DKIM DNS records.

---

## GALLERY

### REQ-GALLERY-001: Photo Gallery Plugin

**Priority:** P0
**Phase:** 1
FooGallery plugin with lazy loading and lightbox support for the Pictures/Gallery page.

### REQ-GALLERY-002: Photo Sources

**Priority:** P0
**Phase:** 1
Upload photos from iCloud `/Hank/` directory: `Cover.jpeg`, `Cover2.HEIC`, `Cover3.jpg` (from `/Sameer/Edited/`), `Spirituality Hero.heic`, `Hero-1.HEIC`, and `High Res/` directory (Easter Vigil, Midnight Mass photos).

### REQ-GALLERY-003: HEIC Image Conversion

**Priority:** P0
**Phase:** 1
Batch convert ALL HEIC images to JPEG/WebP locally before uploading to WordPress. Use `sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"` on macOS. Do not rely on server-side HEIC support (fragile).

### REQ-GALLERY-004: Image Compression

**Priority:** P1
**Phase:** 1
Smush plugin for automatic image compression on upload.

### REQ-GALLERY-005: Homepage Video Embed

**Priority:** P1
**Phase:** 1
YouTube embed of "New Life In the Spirit" video (`_a_zLTOxr0o`) using Embed Plus for YouTube plugin for lazy-loaded responsive embed.

---

## MIGRATION

### REQ-MIGRATION-001: URL Redirects

**Priority:** P0
**Phase:** 1
Map all old `.html` URLs to new WordPress permalinks. Nginx rule: `location ~ ^/(.+)\.html$ { return 301 /$1/; }`. Handle `/ambo-thoughts/` subdirectory path from GitHub Pages URL structure.

### REQ-MIGRATION-002: SEO Preservation

**Priority:** P0
**Phase:** 1
Rank Math plugin for SEO, sitemaps, schema markup, and redirect manager. Submit new sitemap to Google Search Console. Run `wp search-replace` for any HTTP URLs to prevent mixed content.

### REQ-MIGRATION-003: DNS Cutover

**Priority:** P0
**Phase:** 1
Lower DNS TTL to 300 seconds 48 hours before cutover. Keep GitHub Pages running during DNS propagation. Update DNS A record to point to VPS IP. Resolve domain name (open question: ambothoughts.com or other) before VPS setup.

### REQ-MIGRATION-004: Content Transfer

**Priority:** P0
**Phase:** 1
Transfer all content from current static HTML pages to WordPress pages/posts. Source files:

- `index.html` (homepage)
- `about.html`
- `blog.html` + `blog/*.html`
- `spirituality.html`
- `church-news.html`
- `contact.html`
- `pictures.html`
- `prayer-partner.html`
- `stuff.html`
- `videos.html`

### REQ-MIGRATION-005: GitHub Pages Decommission

**Priority:** P1
**Phase:** 1
After DNS propagation is confirmed complete and site is verified on VPS, disable GitHub Pages hosting. Keep repository as archive.

---

## ADMIN

### REQ-ADMIN-001: Role Management

**Priority:** P0
**Phase:** 3
Deacon Henry gets Editor role, NOT Administrator. Disable plugin/theme install from admin panel. Simplified admin panel (remove unnecessary menu items).

### REQ-ADMIN-002: Training Documentation

**Priority:** P0
**Phase:** 3
1-page "How To" admin training document with screenshots covering: creating/editing pages, managing contact form submissions, adding photos to gallery, basic WordPress navigation.

### REQ-ADMIN-003: Uptime Monitoring

**Priority:** P1
**Phase:** 3
UptimeRobot monitoring (free tier) configured with alerts for site downtime.

### REQ-ADMIN-004: Activity Logging

**Priority:** P1
**Phase:** 3
Simple History plugin for logging admin actions and changes.

### REQ-ADMIN-005: Update Management

**Priority:** P0
**Phase:** 3
Disable plugin/theme auto-updates. Monthly manual update cycle. Documented maintenance runbook covering: monthly update procedure, backup verification, security scan review.

### REQ-ADMIN-006: Plugin Blacklist

**Priority:** P1
**Phase:** 1
Do NOT install: Jetpack (bloated), Elementor (conflicts with WPBakery), WP Super Cache (Nginx FastCGI cache is superior), MonsterInsights (overkill), any second security plugin, Yoast (Rank Math is more capable in free tier).

---

## Traceability Matrix

| Phase | P0 Requirements                                                                                                                                                                                                                                | P1 Requirements                                                                                                                          | P2 Requirements  |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| 1     | HOSTING-001 through 005, 008, 009; THEME-001 through 003, 005; DESIGN-001 through 003, 008, 009; CONTENT-001 through 006, 008; NEWS-001, 002; SPIRITUALITY-001, 002; CONTACT-001, 003, 004; GALLERY-001 through 003; MIGRATION-001 through 004 | HOSTING-006, 007, 010; THEME-004; DESIGN-005 through 007; CONTENT-007, 009, 010; CONTACT-002; GALLERY-004, 005; MIGRATION-005; ADMIN-006 | --               |
| 2     | HOMILY-001 through 007; DESIGN-004                                                                                                                                                                                                             | HOMILY-008                                                                                                                               | SPIRITUALITY-003 |
| 3     | ADMIN-001, 002, 005                                                                                                                                                                                                                            | ADMIN-003, 004                                                                                                                           | --               |

**Total requirements:** 62
**P0 (launch blockers):** 38
**P1 (should have):** 20
**P2 (nice to have):** 2
