# Domain Pitfalls

**Domain:** WordPress church website on self-managed VPS
**Researched:** 2026-03-07

## Critical Pitfalls

Mistakes that cause rewrites, security breaches, or major issues.

### Pitfall 1: Theme Customizations Lost on Update

**What goes wrong:** Direct edits to ChurchWP parent theme files (style.css, functions.php, template files) are wiped when the theme updates. The Navy/Gold color scheme, custom header layout, removed sections — all gone.
**Why it happens:** WordPress replaces the entire parent theme directory during updates. ThemeForest themes like ChurchWP bundle their own update mechanism that overwrites everything.
**Consequences:** Hours of CSS/PHP customization work destroyed. Site reverts to default ChurchWP green styling. If Deacon Henry triggers an update from the admin panel, the site breaks without warning.
**Prevention:**

- Create a ChurchWP child theme before making ANY customizations
- All CSS overrides (Navy/Gold variables, header changes) go in the child theme's `style.css`
- All PHP template overrides go in the child theme directory
- Export WordPress Customizer settings separately (they are stored in the database, not theme files, but can reference parent theme specifics)
- Document which parent theme files were overridden in the child theme
- Test parent theme updates on a staging environment before production
  **Detection:** After any theme update, check if the site reverted to default ChurchWP colors/layout.

**Confidence:** HIGH (well-documented WordPress pattern)

### Pitfall 2: VPS Left Unsecured After WordPress Install

**What goes wrong:** WordPress on an unhardened VPS gets compromised within days. Bots constantly scan for wp-login.php and xmlrpc.php. A $5 VPS with default settings is a sitting duck.
**Why it happens:** WordPress is the #1 CMS target. Default installs expose wp-login.php, XML-RPC, and directory listings. VPS providers ship with password SSH auth enabled.
**Consequences:** Site defacement, malware injection, spam relay, SEO poisoning, data breach. Recovery requires full server rebuild.
**Prevention (mandatory checklist):**

1. **SSH:** Key-only authentication, disable password auth in `/etc/ssh/sshd_config` (`PasswordAuthentication no`), change default port from 22
2. **Firewall:** UFW — allow only 80, 443, and SSH port. `ufw default deny incoming && ufw default allow outgoing`
3. **Fail2ban:** Install with WordPress jail using [WP fail2ban plugin](https://wordpress.org/plugins/wp-fail2ban/) to bridge WP auth events to fail2ban. Configure `maxretry=5, findtime=600, bantime=3600`
4. **XML-RPC:** Disable via nginx: `location = /xmlrpc.php { deny all; return 444; }` — not needed for this site (no mobile app, no Jetpack)
5. **File permissions:** Directories 755, files 644, wp-config.php 600. Owner should be `www-data` for web server, NOT root
6. **wp-login.php:** Either rename login URL with WPS Hide Login plugin OR rate-limit at nginx level
7. **Security headers** in nginx: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy` (start with report-only)
8. **Disable file editing:** Add `define('DISALLOW_FILE_EDIT', true);` to wp-config.php — prevents code editing from admin panel
9. **Automatic security updates:** Enable for WordPress core minor versions
   **Detection:** Monitor `/var/log/auth.log` and fail2ban logs. Set up UptimeRobot or similar for uptime monitoring.

**Confidence:** HIGH (standard VPS hardening, verified with multiple sources)

### Pitfall 3: HEIC Images Not Displaying or Failing Upload

**What goes wrong:** The existing photos (Cover2.HEIC, Spirituality Hero.heic, Hero-1.HEIC, High Res/ directory photos) are in Apple HEIC format. Uploading to WordPress fails or produces images that won't render in non-Safari browsers.
**Why it happens:** WordPress 6.7+ added HEIC support, but it depends on the server having ImageMagick 7.0.8-26+ compiled with HEIC/HEIF support. Most VPS default ImageMagick installs do NOT include HEIC codec support. The libheif library must be separately installed.
**Consequences:** Upload errors, broken images on the site, or silently generated thumbnails that fail. Gallery pages with broken images make the site look unprofessional.
**Prevention:**

- **Option A (recommended):** Batch-convert all HEIC files to WebP/JPEG BEFORE uploading to WordPress. On macOS, use `sips` (built-in): `for f in *.HEIC; do sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"; done`. Or use ImageMagick locally: `magick convert input.HEIC output.webp`
- **Option B:** Install libheif + ImageMagick 7 on the VPS and verify HEIC support with `identify -list format | grep HEIC`. This is fragile and adds server maintenance burden.
- **Option A is strongly preferred** — convert once locally, upload web-ready formats. Removes server dependency entirely.
- Generate WebP versions for performance: WordPress 5.8+ can serve WebP if uploaded, and plugins like ShortPixel can auto-generate WebP from JPEG uploads
  **Detection:** Test upload of one HEIC file to WordPress media library immediately after setup. Check `identify -list format | grep HEIC` on server.

**Confidence:** HIGH (WordPress 6.7 HEIC support verified via [Make WordPress Core](https://make.wordpress.org/core/2024/08/15/automatic-conversion-of-heic-images-to-jpeg-in-wordpress-6-7/), but server-side ImageMagick HEIC support is the real bottleneck)

### Pitfall 4: SSL/TLS Mixed Content After Migration

**What goes wrong:** After setting up Let's Encrypt SSL, the site loads over HTTPS but images, CSS, or JS still reference HTTP URLs. Browsers show "Not Secure" warning or block resources entirely.
**Why it happens:** WordPress stores absolute URLs in the database (in post content, widget text, theme options). Migrating content or importing with HTTP URLs embeds them permanently. ChurchWP theme options may store absolute URLs for slider images, logos, etc.
**Consequences:** Browser security warnings scare visitors. Mixed content blocks resources in modern browsers. Google penalizes mixed content sites.
**Prevention:**

- Set `WP_HOME` and `WP_SITEURL` to HTTPS in wp-config.php from day one — never install as HTTP first
- If the database already has HTTP URLs, use WP-CLI: `wp search-replace 'http://ambothoughts.com' 'https://ambothoughts.com' --all-tables`
- Nginx config: force HTTP to HTTPS redirect: `return 301 https://$host$request_uri;`
- Install Really Simple SSL plugin as a safety net (it catches mixed content at runtime)
- Check ChurchWP theme options panel — slider images, logo URLs, and custom CSS may contain hardcoded HTTP URLs
- **Let's Encrypt renewal:** Certbot auto-renewal via systemd timer or cron. Test with `certbot renew --dry-run`. Renewal failures are silent — set up monitoring.
- **OCSP Stapling:** As of August 2025, Let's Encrypt no longer supports OCSP. Do NOT enable `ssl_stapling` in nginx config for LE certs — it will cause warnings.
  **Detection:** After SSL setup, run [Why No Padlock](https://www.whynopadlock.com/) or browser DevTools Console to find mixed content. Check certbot timer: `systemctl status certbot.timer`.

**Confidence:** HIGH (well-documented issue, OCSP change verified via [Let's Encrypt community](https://community.letsencrypt.org/))

## Moderate Pitfalls

### Pitfall 5: DNS Cutover Downtime (GitHub Pages to VPS)

**What goes wrong:** Changing DNS from GitHub Pages IP to VPS IP causes extended downtime because DNS caches hold the old IP for hours.
**Why it happens:** Default DNS TTL is often 3600s (1 hour) or higher. Some ISP resolvers ignore TTL and cache for 24+ hours. During propagation, some visitors hit old server, some hit new.
**Prevention:**

1. **48 hours before cutover:** Lower DNS A record TTL to 300 seconds (5 minutes)
2. **Wait for old TTL to expire** before changing the A record (if old TTL was 3600s, wait 1 hour minimum after setting 300s)
3. **Keep old GitHub Pages site running** during propagation — both old and new should serve content
4. **Perform cutover during low-traffic hours** (late evening US Eastern for a NJ church site)
5. **After propagation completes** (verify with `dig` from multiple locations), raise TTL back to 3600s
6. **If using a custom domain** (not the rijhsinghani.github.io subdomain), the GitHub Pages CNAME config will need to be removed after cutover
   **Detection:** Use `dig +short ambothoughts.com` from multiple DNS resolvers to verify propagation. Use [whatsmydns.net](https://www.whatsmydns.net/) for global check.

**Confidence:** HIGH (standard DNS migration practice)

### Pitfall 6: WordPress Performance Degradation on Small VPS

**What goes wrong:** A $5 VPS (1 vCPU, 1GB RAM) runs WordPress adequately at first, then becomes sluggish as plugins accumulate, database grows, or a traffic spike hits.
**Why it happens:** Each PHP-FPM worker consumes ~64MB RAM. With 1GB total RAM (minus OS overhead ~300MB), you get ~10 workers maximum. WordPress with multiple plugins can use 128MB+ per request. Unoptimized wp_options table autoloads grow over time.
**Consequences:** 503 errors during traffic spikes (Easter, Christmas — peak church website traffic). Slow admin panel frustrates Deacon Henry. Search engines downrank slow sites.
**Prevention:**

- **PHP-FPM config:** `pm = ondemand`, `pm.max_children = 4-6` for 1GB VPS. Do NOT use `pm = dynamic` on small VPS — idle workers waste RAM
- **Nginx microcaching:** Cache full pages for 60s for anonymous users. Church site is 99% anonymous traffic — massive win.
- **Object cache:** Install Redis + Redis Object Cache plugin. Reduces database queries per page from 50+ to <10
- **Database maintenance:** Schedule monthly cleanup of transients, post revisions (limit to 5: `define('WP_POST_REVISIONS', 5);`), and spam comments
- **Image optimization:** Use ShortPixel or Smush to compress on upload. Enable lazy loading (WordPress default since 5.5). Serve WebP where possible.
- **Caching plugin:** WP Super Cache or W3 Total Cache for full-page caching to disk. Nginx serves cached HTML directly, bypassing PHP entirely.
- **Minimum VPS spec recommendation:** $6/mo DigitalOcean droplet (1 vCPU, 1GB RAM) is sufficient for this low-traffic church site WITH caching. Without caching, consider $12/mo (2GB RAM).
  **Detection:** Monitor with `htop` for RAM/CPU. Set up New Relic free tier or WP Query Monitor plugin for slow queries.

**Confidence:** HIGH (PHP-FPM worker math verified via [ManagingWP](https://managingwp.io/2025/10/01/why-php-fpm-process-worker-limits-matter-preventing-server-outages-with-standardized-pool-configuration/) and [SpinupWP](https://spinupwp.com/doc/how-php-workers-impact-wordpress-performance/))

### Pitfall 7: Admin Handoff to Non-Technical User

**What goes wrong:** Deacon Henry, a non-technical admin, accidentally breaks the site by: updating the parent theme (losing customizations), installing incompatible plugins, editing PHP files, deleting critical pages, or changing permalink structure.
**Why it happens:** WordPress admin panel exposes powerful/dangerous features by default. The full admin dashboard is overwhelming for content-focused users.
**Prevention:**

- **Create an Editor role** for Deacon Henry, NOT Administrator. Editor can create/edit posts and pages but cannot install plugins, change themes, or modify settings.
- **Keep a separate Administrator account** (yours) for maintenance tasks
- **Simplify the admin panel** with [PublishPress Capabilities](https://wordpress.org/plugins/capability-manager-enhanced/):
  - Hide: Appearance, Plugins, Tools, Settings, Users menus
  - Hide: Dashboard widgets (WordPress Events, Quick Draft)
  - Hide: Admin bar links (About WordPress, Visit Site during editing)
  - Show: Posts, Pages, Media, Comments only
- **Disable file editing:** `define('DISALLOW_FILE_EDIT', true);` in wp-config.php
- **Disable plugin/theme install from admin:** `define('DISALLOW_FILE_MODS', true);` — this also disables updates from admin, so you must handle updates via WP-CLI or SSH
- **Create a simple 1-page "How To" guide** for Deacon Henry covering: how to create a post, how to add images, how to edit a page. Include screenshots.
- **Set up automatic WordPress core updates** for minor/security versions so the site stays patched without admin intervention
  **Detection:** Periodically check the activity log (install Simple History plugin) to see what actions Deacon Henry is taking.

**Confidence:** HIGH (standard WordPress admin management pattern)

### Pitfall 8: SEO Loss During Static HTML to WordPress Migration

**What goes wrong:** Existing pages at `rijhsinghani.github.io/ambo-thoughts/about.html` become 404s after migration because WordPress uses `/about/` URL structure (no .html extension). Search engines drop indexed pages.
**Why it happens:** WordPress uses "pretty permalinks" (`/post-name/`) by default, which don't match the old `.html` URL structure. GitHub Pages subdirectory paths also differ from a root domain setup.
**Consequences:** Existing Google indexing lost. Backlinks from church directories or diocesan sites break. 404 errors for bookmarked pages.
**Prevention:**

- **Map all old URLs to new URLs** before migration:
  ```
  /about.html           -> /about/
  /blog.html            -> /blog/
  /blog/sample-homily.html -> /sample-homily/ (or /homilies/sample-homily/)
  /spirituality.html    -> /spirituality/
  /church-news.html     -> /church-news/
  /contact.html         -> /contact/
  /pictures.html        -> /gallery/ (or /pictures/)
  /prayer-partner.html  -> /prayer-partner/
  /stuff.html           -> /stuff/
  /videos.html          -> /videos/
  ```
- **Set up 301 redirects** in nginx for every old URL pattern:
  ```nginx
  # Strip .html extension redirects
  location ~ ^/(.+)\.html$ {
      return 301 /$1/;
  }
  ```
- **Handle the GitHub Pages subdirectory path** if people bookmarked `/ambo-thoughts/about.html`:
  ```nginx
  location /ambo-thoughts/ {
      rewrite ^/ambo-thoughts/(.*)$ /$1 permanent;
  }
  ```
- **Submit updated sitemap** to Google Search Console after migration
- **Keep old GitHub Pages site** running with meta refresh redirects for 3-6 months as a fallback
- **Use Redirection plugin** in WordPress for any URLs you discover later that 404
  **Detection:** Monitor Google Search Console for crawl errors and 404s after migration. Check Google Analytics for traffic drops.

**Confidence:** HIGH (standard migration practice, verified via [ParallelDevs](https://www.paralleldevs.com/blog/how-use-301-redirects-when-redesigning-or-migrating-wordpress-site-without-losing-seo/))

## Minor Pitfalls

### Pitfall 9: ChurchWP Bundled Plugin Conflicts

**What goes wrong:** ChurchWP bundles plugins (Visual Composer/WPBakery, Revolution Slider, etc.) that conflict with separately installed versions or other plugins.
**Why it happens:** ThemeForest themes bundle commercial plugins at specific versions. If you install the plugin separately (e.g., a newer WPBakery from its official site), the two versions conflict. ChurchWP has already deprecated its Massive Addons and TSLR Maps plugins.
**Prevention:**

- Use ONLY the bundled plugin versions that ChurchWP provides
- Do NOT install separate copies of WPBakery, Revolution Slider, or other bundled plugins
- Replace deprecated TSLR Maps with Google Maps Embed (per ChurchWP docs)
- Remove the deprecated Massive Addons plugin if not needed
- Before installing any new plugin, test on staging for conflicts with ChurchWP's bundled plugins
  **Detection:** After plugin install, check for PHP errors in `wp-content/debug.log` (enable `WP_DEBUG_LOG` in wp-config.php).

**Confidence:** MEDIUM (ChurchWP-specific details from [ThemeForest listing](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148), general pattern well-known)

### Pitfall 10: ThemeForest Theme Lock-in

**What goes wrong:** After building the site with ChurchWP's bundled page builder (WPBakery), custom post types, and shortcodes, switching themes later requires rebuilding every page from scratch.
**Why it happens:** ThemeForest themes use proprietary shortcodes and page builder elements that only render with that specific theme active. Content is stored with `[shortcode]` tags that become visible garbage text without the theme.
**Prevention:**

- Use the WordPress block editor (Gutenberg) for page content whenever possible instead of WPBakery shortcodes
- Store critical content (bio, ministry info) as standard WordPress pages with standard blocks, not in theme-specific widgets
- Keep ChurchWP-specific elements (sliders, custom layouts) limited to the homepage and a few showcase pages
- Document which pages use theme-specific elements vs standard WordPress content
  **Detection:** Temporarily switch to a default theme (Twenty Twenty-Four) and check which pages break.

**Confidence:** HIGH (well-known ThemeForest lock-in pattern)

### Pitfall 11: Contact Form Email Delivery Failures

**What goes wrong:** WordPress contact form emails (to deacon267@verizon.net and hcugini@stroberts.cc) go to spam or never arrive because the VPS IP has no email reputation.
**Why it happens:** PHP's `mail()` function sends from the VPS IP, which has no SPF/DKIM records. Gmail, Outlook, and Verizon aggressively filter VPS-originated email.
**Prevention:**

- Do NOT rely on PHP mail(). Install WP Mail SMTP plugin.
- Use a transactional email service: Resend (you already use this), SendGrid free tier (100/day), or Mailgun free tier
- Set SPF and DKIM DNS records for the domain
- Test form delivery to both Verizon and stroberts.cc addresses after setup — these older email providers are especially aggressive with spam filtering
  **Detection:** Submit a test contact form immediately after setup. Check spam folders.

**Confidence:** HIGH (universal WordPress email problem)

### Pitfall 12: WordPress Auto-Update Breaks Site

**What goes wrong:** An automatic WordPress core, theme, or plugin update introduces a fatal PHP error, white-screening the site.
**Why it happens:** WordPress auto-updates minor versions by default. Plugins may auto-update if enabled. A PHP incompatibility or plugin conflict crashes the site.
**Prevention:**

- Enable auto-updates ONLY for WordPress core minor/security versions (default behavior)
- Disable auto-updates for plugins and themes: `add_filter('auto_update_plugin', '__return_false');` and `add_filter('auto_update_theme', '__return_false');`
- Install WP Rollback plugin for emergency theme/plugin downgrades
- Keep a monthly backup schedule (UpdraftPlus to Google Drive or Backblaze B2)
- Enable `WP_DEBUG_LOG` (not `WP_DEBUG_DISPLAY`) so errors go to log file, not visitor-facing
  **Detection:** UptimeRobot monitoring (free tier) pings the site every 5 minutes. Email alert on downtime.

**Confidence:** HIGH (common WordPress operational issue)

## Phase-Specific Warnings

| Phase Topic         | Likely Pitfall                      | Mitigation                                                        |
| ------------------- | ----------------------------------- | ----------------------------------------------------------------- |
| VPS Setup           | Unsecured server (Pitfall 2)        | Complete security hardening checklist before installing WordPress |
| Theme Customization | Lost customizations (Pitfall 1)     | Child theme FIRST, before any CSS/PHP changes                     |
| Content Migration   | HEIC upload failures (Pitfall 3)    | Batch convert to JPEG/WebP locally before upload                  |
| Content Migration   | Broken URLs (Pitfall 8)             | Map all old URLs, configure nginx 301 redirects                   |
| SSL Setup           | Mixed content (Pitfall 4)           | Install as HTTPS from the start, never HTTP                       |
| DNS Cutover         | Extended downtime (Pitfall 5)       | Lower TTL 48 hours before, keep old site running                  |
| Admin Handoff       | Accidental breakage (Pitfall 7)     | Editor role, not Admin. Simplify panel. Training doc.             |
| Post-Launch         | Performance degradation (Pitfall 6) | Caching stack from day one: nginx microcache + Redis + page cache |
| Post-Launch         | Update breakage (Pitfall 12)        | Disable plugin/theme auto-updates, monthly manual update cycle    |

## Sources

- [WordPress Brute Force Protection - Developer Handbook](https://developer.wordpress.org/advanced-administration/security/brute-force/)
- [WordPress Security Hardening 2026 - GigaPress](https://gigapress.net/wordpress-security-hardening-12-steps-to-protect-your-site-in-2026/)
- [WP fail2ban Plugin](https://wordpress.org/plugins/wp-fail2ban/)
- [WordPress Child Themes - Developer Handbook](https://developer.wordpress.org/themes/advanced-topics/child-themes/)
- [HEIC Support in WordPress 6.7 - Make WordPress Core](https://make.wordpress.org/core/2024/08/15/automatic-conversion-of-heic-images-to-jpeg-in-wordpress-6-7/)
- [HEIC Support Plugin](https://wordpress.org/plugins/heic-support/)
- [301 Redirects for WordPress Migration - ParallelDevs](https://www.paralleldevs.com/blog/how-use-301-redirects-when-redesigning-or-migrating-wordpress-site-without-losing-seo/)
- [WordPress SEO Migration Checklist 2025 - LitExtension](https://litextension.com/blog/wordpress-seo-migration/)
- [PHP-FPM Worker Limits - ManagingWP](https://managingwp.io/2025/10/01/why-php-fpm-process-worker-limits-matter-preventing-server-outages-with-standardized-pool-configuration/)
- [PHP Workers and WordPress Performance - SpinupWP](https://spinupwp.com/doc/how-php-workers-impact-wordpress-performance/)
- [Nginx Security Hardening for WordPress - SpinupWP](https://spinupwp.com/hosting-wordpress-yourself-nginx-security-tweaks-woocommerce-caching-auto-server-updates/)
- [Let's Encrypt SSL on Nginx 2025](https://www.onlinehashcrack.com/guides/tutorials/howto-let-s-encrypt-ssl-on-nginx-2025-deploy-fast.php)
- [Fix Mixed Content in WordPress - Hostinger](https://www.hostinger.com/tutorials/fix-mixed-content-wordpress)
- [Zero-Downtime DNS Migration - Unihost](https://unihost.com/blog/zero-downtime-migration/)
- [WordPress File Permissions - WPThrill](https://wpthrill.com/wordpress-file-permissions-755-vs-644-vs-600/)
- [PublishPress Capabilities Plugin](https://wordpress.org/plugins/capability-manager-enhanced/)
- [ChurchWP - ThemeForest](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148)
- [WordPress VPS Optimization 2025 - WiliVM](https://www.wilivm.com/blog/how-to-optimize-vps-for-wordpress-speed-in-2025/)
