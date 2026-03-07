# Research Summary

**Project:** Ambo Thoughts WordPress Redesign
**Synthesized:** 2026-03-07

---

## Executive Summary

This project migrates Deacon Henry Cugini's ministry website from static HTML on GitHub Pages to a self-managed WordPress site on a DigitalOcean VPS. The research confirms this is a well-trodden path with HIGH confidence across all major decisions. The recommended stack (Nginx + PHP-FPM 8.3 + MariaDB + Redis on a $6/mo VPS) is the standard performant WordPress hosting setup, and the ChurchWP ThemeForest theme provides a church-specific design foundation that needs only color/branding customization via a child theme.

The most architecturally significant decision is using a Custom Post Type for homilies instead of a sermon plugin. This enables clean REST API integration with the existing `process_homilies.py` pipeline, avoids dependency on abandoned/fragile sermon plugins (Sermon Manager was closed on WordPress.org in Dec 2025), and keeps the content structure lean. The CPT + custom taxonomies (liturgical season, scripture reference) + custom meta fields (youtube_id, transcript, pull_quote) maps directly to the pipeline's output.

The primary risks are operational, not technical: VPS security hardening must happen before WordPress install (bots scan within hours), HEIC images must be batch-converted before upload (server-side HEIC support is fragile), and the DNS cutover from GitHub Pages needs TTL lowering 48 hours in advance. The admin handoff to a non-technical user (Deacon Henry) requires role restriction to Editor and a simplified admin panel.

---

## Stack Decision

| Layer             | Technology              | Version                   | Monthly Cost  |
| ----------------- | ----------------------- | ------------------------- | ------------- |
| VPS               | DigitalOcean Droplet    | 1 vCPU, 1GB RAM, 25GB SSD | $6.00         |
| OS                | Ubuntu                  | 24.04 LTS                 | --            |
| Web Server        | Nginx                   | 1.24+                     | --            |
| PHP               | PHP-FPM                 | 8.3 (ppa:ondrej/php)      | --            |
| Database          | MariaDB                 | 10.11 LTS                 | --            |
| Object Cache      | Redis                   | Latest                    | --            |
| Page Cache        | Nginx FastCGI Cache     | (disk-based)              | --            |
| SSL               | Certbot + Let's Encrypt | Latest                    | Free          |
| Theme             | ChurchWP (ThemeForest)  | Latest                    | $59 one-time  |
| Local Dev         | Local by Flywheel       | Latest                    | Free          |
| Deployment        | rsync over SSH + WP-CLI | --                        | --            |
| **Total ongoing** |                         |                           | **~$8.20/mo** |

**Confidence:** HIGH across the board. Every component is the industry-standard choice for WordPress VPS hosting.

---

## Plugin Stack

| Plugin                 | Purpose                                                    | Cost    | Phase |
| ---------------------- | ---------------------------------------------------------- | ------- | ----- |
| ThemeSLR Framework     | ChurchWP theme options panel                               | Bundled | 1     |
| WPBakery Page Builder  | Page layouts (bundled with theme)                          | Bundled | 1     |
| Slider Revolution      | Homepage hero slider                                       | Bundled | 1     |
| Contact Form 7         | Dual-email contact form                                    | Free    | 1     |
| Flamingo               | Store CF7 submissions in DB as backup                      | Free    | 1     |
| WP Mail SMTP           | Reliable email delivery (VPS mail goes to spam without it) | Free    | 1     |
| Rank Math              | SEO, sitemaps, schema markup, redirect manager             | Free    | 1     |
| Wordfence              | Firewall, login protection, malware scan                   | Free    | 1     |
| UpdraftPlus            | Automated backups to Google Drive                          | Free    | 1     |
| FooGallery             | Photo gallery with lazy loading + lightbox                 | Free    | 1     |
| Embed Plus for YouTube | Lazy-loaded responsive video embeds                        | Free    | 1     |
| Smush                  | Image compression on upload                                | Free    | 1     |
| Redis Object Cache     | Database query caching (by Till Kruss)                     | Free    | 1     |
| Bible Verse of the Day | Daily scripture on Spirituality page                       | Free    | 2     |

**Total: 14 plugins, all free tier. $0 recurring plugin cost.**

**Do NOT install:** Jetpack (bloated), Elementor (conflicts with WPBakery), WP Super Cache (Nginx FastCGI cache is superior), MonsterInsights (overkill), any second security plugin.

Note: STACK.md recommends Nginx FastCGI cache over WP Super Cache. FEATURES.md lists WP Super Cache. ARCHITECTURE.md lists both. **Decision: Use Nginx FastCGI cache (server-level) + Redis Object Cache (plugin-level). Skip WP Super Cache entirely** -- FastCGI cache serves HTML without invoking PHP at all, which is strictly superior on a 1GB VPS.

Note: FEATURES.md recommends Contact Form 7, ARCHITECTURE.md recommends WPForms Lite, FEATURES.md recommends Rank Math, ARCHITECTURE.md recommends Yoast. **Decision: CF7 + Rank Math.** CF7 is lighter (no upsell nags) and Rank Math free tier is substantially more capable than Yoast free (unlimited focus keywords, redirect manager, schema markup all included free).

---

## Architecture Decisions

### 1. Child Theme (MANDATORY)

All customizations go in `churchwp-child/`. Navy (#001f5b) / Gold (#c9a84c) color overrides via CSS custom properties. Playfair Display for headings, system sans-serif for body. Override only `header.php` and `footer.php` from parent -- do not copy all templates.

Use ChurchWP's Theme Panel first for global colors/fonts/logo. CSS overrides only for what the panel misses.

### 2. Custom Post Type for Homilies

Register `homily` CPT in child theme's `inc/homily-cpt.php` with:

- `show_in_rest: true` (enables REST API + Gutenberg)
- Taxonomy: `homily_season` (Advent, Lent, Easter, Ordinary Time, etc.)
- Meta fields: `youtube_id`, `pull_quote`, `scripture_refs`, `transcript`, `drive_file_id`, `homily_date`
- REST endpoint: `wp-json/wp/v2/homilies`

No sermon plugin. Sermon Manager is closed/abandoned. CPT is permanent, portable, and maps to the pipeline output.

### 3. Homily Pipeline Integration

Adapt existing `process_homilies.py` to POST to WordPress REST API instead of generating static HTML. Authentication via WordPress Application Passwords (built into core since WP 5.6). Credentials in environment variables, never in code.

### 4. Deployment Pipeline

```
Local by Flywheel --> GitHub repo --> rsync over SSH --> Production VPS
```

Git tracks: `wp-content/themes/churchwp-child/`, `scripts/`, `.gitignore`. Git ignores: WordPress core, parent theme, `wp-config.php`, `uploads/`, plugin directories. Database sync is production-to-local only via `wp db export` + `wp search-replace`.

### 5. wp-config.php Environment Management

Mark Jaquith's `local-config.php` pattern. Local config gitignored, production uses environment variables. `DISALLOW_FILE_EDIT: true` in production.

---

## Critical Pitfalls (Top 5)

| #   | Pitfall                                 | Severity | Phase             | Mitigation                                                                                                                                                                            |
| --- | --------------------------------------- | -------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **VPS left unsecured**                  | CRITICAL | VPS Setup         | SSH key-only auth, UFW firewall (80/443/SSH only), fail2ban, disable xmlrpc.php in nginx, file permissions (dirs 755, files 644, wp-config 600)                                       |
| 2   | **Theme customizations lost on update** | CRITICAL | Theme Setup       | Child theme FIRST before any changes. Never edit parent theme. Document overridden files.                                                                                             |
| 3   | **HEIC images fail to upload/display**  | CRITICAL | Content Migration | Batch convert ALL HEIC to JPEG/WebP locally before upload: `sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"`. Do not rely on server-side HEIC support.                                |
| 4   | **SSL mixed content after migration**   | MODERATE | SSL/DNS           | Install WordPress as HTTPS from day one. Run `wp search-replace` for any HTTP URLs. Force HTTP-to-HTTPS redirect in nginx.                                                            |
| 5   | **SEO loss from URL changes**           | MODERATE | DNS Cutover       | Map all old `.html` URLs to new WordPress permalinks. Nginx rule: `location ~ ^/(.+)\.html$ { return 301 /$1/; }`. Handle `/ambo-thoughts/` subdirectory path. Submit sitemap to GSC. |

### Additional Operational Risks

- **Contact form emails go to spam**: Use WP Mail SMTP with Resend (already in use across other projects). Set SPF/DKIM DNS records.
- **Admin breaks site**: Give Deacon Henry Editor role, not Administrator. Disable plugin/theme install from admin panel.
- **DNS cutover downtime**: Lower TTL to 300s 48 hours before cutover. Keep GitHub Pages running during propagation.
- **Performance on 1GB VPS**: PHP-FPM `pm = ondemand`, `max_children = 5`. Nginx FastCGI cache + Redis object cache. Limit post revisions to 5.

---

## Open Questions (Consolidated & Deduplicated)

| #   | Question                                                                          | Impacts                                | When to Resolve                  |
| --- | --------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------- |
| 1   | What is the final domain name? (ambothoughts.com? Already registered?)            | DNS, SSL, deployment script, wp-config | Before VPS setup                 |
| 2   | Does Deacon Henry have a DigitalOcean account, or create one under your account?  | Billing, access management             | Before VPS setup                 |
| 3   | ChurchWP exact Theme Panel options -- what can be set in panel vs CSS?            | Child theme CSS scope                  | After theme purchase/install     |
| 4   | ChurchWP bundled plugin versions -- do they conflict with PHP 8.3?                | Server config                          | After theme purchase/install     |
| 5   | Which SMTP service for contact form? Resend (existing) vs Gmail SMTP vs SendGrid? | WP Mail SMTP config                    | Phase 1                          |
| 6   | Which Google account for UpdraftPlus backups and pipeline credentials?            | Backup storage, API auth               | Phase 1                          |
| 7   | Exact page-to-page content mapping from old site to new site?                     | Migration plan, redirect rules         | Before Phase 1 content migration |
| 8   | Does the homily pipeline need to run on the VPS or stay local/Cloud Run?          | Deployment architecture                | Phase 2                          |

---

## Phase Implications

### Phase 1: Infrastructure + Launch Site

**Rationale:** Get a secure, performant VPS running with the themed WordPress site and all existing static content migrated. This is the critical path -- everything else builds on it.

**Delivers:**

- Production VPS (hardened, cached, backed up)
- ChurchWP child theme with Navy/Gold branding
- All 8 existing pages migrated (About, Spirituality, Church News, Contact, Pictures, Prayer Partner, Stuff, Videos)
- Contact form with dual-email delivery
- Photo gallery (FooGallery)
- YouTube video embeds (Embed Plus)
- SEO configured (Rank Math)
- Security (Wordfence) + Backups (UpdraftPlus)
- SSL + DNS cutover from GitHub Pages

**Pitfalls to avoid:** #1 (VPS security), #2 (child theme), #3 (HEIC conversion), #4 (mixed content), #5 (SEO/URL redirects)

**Research needed:** LOW -- all components are well-documented WordPress patterns. No phase research needed.

### Phase 2: Homily Content System

**Rationale:** Once the site is live with static content, build the structured homily system and pipeline integration. This is the differentiator -- automated homily publishing from the existing video pipeline.

**Delivers:**

- Homily CPT with liturgical season taxonomy
- Custom meta fields (youtube_id, transcript, pull_quote, scripture_refs)
- Single homily template (`single-homily.php`) in child theme
- Homily archive page (`archive-homily.php`) with season filtering
- REST API endpoint for pipeline integration
- Adapted `process_homilies.py` / `wp_publisher.py` module
- Bible Verse of the Day on Spirituality page
- Migrate existing homily content from old site into CPT

**Pitfalls to avoid:** WPBakery lock-in (use standard WordPress template tags for homily templates, NOT WPBakery shortcodes)

**Research needed:** LOW -- WordPress CPT + REST API is thoroughly documented. Pipeline adaptation is straightforward (replace HTML generation with REST POST).

### Phase 3: Admin Handoff + Operational Hardening

**Rationale:** After content system is complete, prepare for long-term operation by a non-technical admin.

**Delivers:**

- Editor role for Deacon Henry with simplified admin panel
- Admin training document (1-page "How To" with screenshots)
- UptimeRobot monitoring (free tier)
- Disable plugin/theme auto-updates (manual monthly cycle)
- Activity logging (Simple History plugin)
- Documented maintenance runbook (monthly updates, backup verification)

**Pitfalls to avoid:** #7 (admin breaks site), #12 (auto-update breakage)

**Research needed:** NONE -- standard WordPress admin management.

---

## Confidence Assessment

| Area         | Confidence | Notes                                                                                                |
| ------------ | ---------- | ---------------------------------------------------------------------------------------------------- |
| Stack        | HIGH       | Every component is the industry standard. Verified against official docs and multiple benchmarks.    |
| Features     | HIGH       | All plugins are 100K+ installs (except Bible Verse of the Day at 4K). No exotic choices.             |
| Architecture | HIGH       | Child theme + CPT + REST API is core WordPress. Pipeline integration is a straightforward HTTP POST. |
| Pitfalls     | HIGH       | All pitfalls are well-documented WordPress operational issues with standard mitigations.             |

**Overall: HIGH.** This is a conventional WordPress project. The only MEDIUM-confidence area is ChurchWP's exact Theme Panel capabilities (need to verify after purchase). Everything else follows established patterns.

**Gaps:**

- ChurchWP theme panel options cannot be fully verified until after purchase/install
- Exact bundled plugin versions and PHP 8.3 compatibility need testing
- Domain name and hosting account ownership need confirmation from Deacon Henry
- SMTP provider decision (recommend Resend since already in use across projects)

---

## Sources

Aggregated from STACK.md (10 sources), FEATURES.md (13 sources), ARCHITECTURE.md (10 sources), PITFALLS.md (16 sources). All HIGH-confidence sources are official WordPress documentation, WordPress.org plugin pages, and established hosting guides. See individual research files for full source lists.
