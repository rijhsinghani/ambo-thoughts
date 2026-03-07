# Domain Pitfalls

**Domain:** WordPress church website on self-managed VPS
**Researched:** 2026-03-07
**Updated:** 2026-03-07 (enhanced with current 2025-2026 security research)

## Critical Pitfalls

Mistakes that cause rewrites, security breaches, or major issues.

### Pitfall 1: Theme Customizations Lost on Update

**What goes wrong:** Direct edits to ChurchWP parent theme files (style.css, functions.php, template files) are wiped when the theme updates. The Navy/Gold color scheme, custom header layout, removed sections -- all gone.
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
**Why it happens:** WordPress is the #1 CMS target (powers 40%+ of the web as of 2025). Default installs expose wp-login.php, XML-RPC, and directory listings. VPS providers ship with password SSH auth enabled.
**Consequences:** Site defacement, malware injection, spam relay, SEO poisoning, data breach. Recovery requires full server rebuild.
**Prevention (mandatory checklist):**

1. **SSH:** Key-only authentication, disable password auth in `/etc/ssh/sshd_config` (`PasswordAuthentication no`), change default port from 22
2. **Firewall:** UFW -- allow only 80, 443, and SSH port. `ufw default deny incoming && ufw default allow outgoing`
3. **Fail2ban:** Install with WordPress jail using [WP fail2ban plugin](https://wordpress.org/plugins/wp-fail2ban/) to bridge WP auth events to fail2ban. Configure `maxretry=5, findtime=600, bantime=3600`. Create local config in `/etc/fail2ban/jail.local` (never modify `jail.conf` directly -- package updates overwrite it).
4. **XML-RPC:** Disable via nginx: `location = /xmlrpc.php { deny all; return 444; }` -- not needed for this site (no mobile app, no Jetpack). **Critical 2025 context:** Attackers now use `system.multicall` to bundle hundreds of brute-force guesses into a single HTTP request, evading rate limits. Blocking at nginx level (not just a plugin) is essential because plugin-level blocking still lets PHP parse the request, wasting server resources on a 1GB VPS.
5. **File permissions:** Directories 755, files 644, wp-config.php 600. Owner should be `www-data` for web server, NOT root
6. **wp-login.php:** Either rename login URL with WPS Hide Login plugin OR rate-limit at nginx level. Rate-limiting at nginx is more reliable:
   ```nginx
   location = /wp-login.php {
       limit_req zone=login burst=3 nodelay;
       include fastcgi_params;
       fastcgi_pass unix:/run/php/php-fpm.sock;
   }
   ```
7. **Security headers** in nginx: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy` (start with report-only)
8. **Disable file editing:** Add `define('DISALLOW_FILE_EDIT', true);` to wp-config.php -- prevents code editing from admin panel
9. **Automatic security updates:** Enable for WordPress core minor versions
10. **Unattended OS upgrades:** Install `unattended-upgrades` on Ubuntu/Debian for automatic security patches to the OS itself, not just WordPress

**Detection:** Monitor `/var/log/auth.log` and fail2ban logs. Set up UptimeRobot or similar for uptime monitoring.

**Confidence:** HIGH (standard VPS hardening, verified with [Unihost 2025 guide](https://unihost.com/blog/securing-wordpress-vps-2025/), [VPS.DO fail2ban guide](https://vps.do/fail2ban-vps/), [Patchstack 2025 report](https://patchstack.com/whitepaper/state-of-wordpress-security-in-2025/))

### Pitfall 3: HEIC Images Not Displaying or Failing Upload

**What goes wrong:** The existing photos (Cover2.HEIC, Spirituality Hero.heic, Hero-1.HEIC, High Res/ directory photos) are in Apple HEIC format. Uploading to WordPress fails or produces images that won't render in non-Safari browsers.
**Why it happens:** WordPress 6.7+ added HEIC support, but it depends on the server having ImageMagick 7.0.8-26+ compiled with HEIC/HEIF support. Most VPS default ImageMagick installs do NOT include HEIC codec support. The libheif library must be separately installed.
**Consequences:** Upload errors, broken images on the site, or silently generated thumbnails that fail. Gallery pages with broken images make the site look unprofessional.
**Prevention:**

- **Option A (recommended):** Batch-convert all HEIC files to WebP/JPEG BEFORE uploading to WordPress. On macOS, use `sips` (built-in): `for f in *.HEIC; do sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"; done`. Or use ImageMagick locally: `magick convert input.HEIC output.webp`
- **Option B:** Install libheif + ImageMagick 7 on the VPS and verify HEIC support with `identify -list format | grep HEIC`. This is fragile and adds server maintenance burden.
- **Option A is strongly preferred** -- convert once locally, upload web-ready formats. Removes server dependency entirely.
- Generate WebP versions for performance: WordPress 5.8+ can serve WebP if uploaded, and plugins like ShortPixel can auto-generate WebP from JPEG uploads
- **Future-proofing for Deacon Henry:** Tell him to set iPhone to "Most Compatible" format (Settings > Camera > Formats) so future photos are JPEG, not HEIC. Otherwise every photo he takes and uploads will hit this issue.

**Detection:** Test upload of one HEIC file to WordPress media library immediately after setup. Check `identify -list format | grep HEIC` on server.

**Confidence:** HIGH (WordPress 6.7 HEIC support verified via [Make WordPress Core](https://make.wordpress.org/core/2024/08/15/automatic-conversion-of-heic-images-to-jpeg-in-wordpress-6-7/), but server-side ImageMagick HEIC support is the real bottleneck)

### Pitfall 4: SSL/TLS Mixed Content After Migration

**What goes wrong:** After setting up Let's Encrypt SSL, the site loads over HTTPS but images, CSS, or JS still reference HTTP URLs. Browsers show "Not Secure" warning or block resources entirely.
**Why it happens:** WordPress stores absolute URLs in the database (in post content, widget text, theme options). Migrating content or importing with HTTP URLs embeds them permanently. ChurchWP theme options may store absolute URLs for slider images, logos, etc.
**Consequences:** Browser security warnings scare visitors. Mixed content blocks resources in modern browsers. Google penalizes mixed content sites.
**Prevention:**

- Set `WP_HOME` and `WP_SITEURL` to HTTPS in wp-config.php from day one -- never install as HTTP first
- If the database already has HTTP URLs, use WP-CLI: `wp search-replace 'http://ambothoughts.com' 'https://ambothoughts.com' --all-tables`
- Nginx config: force HTTP to HTTPS redirect: `return 301 https://$host$request_uri;`
- Install Really Simple SSL plugin as a safety net (it catches mixed content at runtime)
- Check ChurchWP theme options panel -- slider images, logo URLs, and custom CSS may contain hardcoded HTTP URLs
- **Let's Encrypt renewal:** Certbot auto-renewal via systemd timer or cron. Test with `certbot renew --dry-run`. Renewal failures are silent -- set up monitoring.
- **OCSP Stapling:** As of August 2025, Let's Encrypt no longer supports OCSP. Do NOT enable `ssl_stapling` in nginx config for LE certs -- it will cause warnings.

**Detection:** After SSL setup, run [Why No Padlock](https://www.whynopadlock.com/) or browser DevTools Console to find mixed content. Check certbot timer: `systemctl status certbot.timer`.

**Confidence:** HIGH (well-documented issue, OCSP change verified via [Let's Encrypt community](https://community.letsencrypt.org/))

### Pitfall 5: No Backup Strategy = Unrecoverable Disaster

**What goes wrong:** The VPS disk fails, gets hacked, or a bad update corrupts the database. Without off-server backups, the entire site is lost -- content, media, configuration, everything.
**Why it happens:** Self-managed VPS means YOU are responsible for backups. DigitalOcean droplet backups cost extra ($1.20/mo for a $6 droplet) and only keep weekly snapshots. No managed hosting safety net exists.
**Consequences:** Complete site loss. All of Deacon Henry's content, blog posts, homily archives, photo galleries -- gone. Rebuilding from scratch. For a church ministry site, this could mean years of spiritual content lost.
**Prevention:**

- **Automated daily database backup:** Use `mysqldump` via cron to export the WordPress database daily. Compress with gzip. Keep 7 daily, 4 weekly, 3 monthly rotations.
  ```bash
  mysqldump -u wp_user -p'password' wordpress_db | gzip > /backups/db/wp_$(date +%Y%m%d).sql.gz
  ```
- **Automated weekly file backup:** `wp-content/uploads/` directory (user media), child theme, wp-config.php. The rest can be reinstalled.
- **Off-server storage (mandatory):** Backups on the same VPS are useless if the VPS dies. Options:
  - UpdraftPlus plugin (free) to Google Drive -- easiest for this use case
  - `rclone` to Backblaze B2 ($0.005/GB/mo) via cron -- cheapest
  - DigitalOcean Spaces ($5/mo, 250GB) -- same provider, easy setup
- **Test restore annually:** A backup you have never tested restoring is not a backup. Spin up a $5 droplet, restore, verify, destroy.
- **wp-config.php secrets:** Store a copy of wp-config.php (with database credentials, auth keys) in a password manager or encrypted note. This file is the single point of failure for site recovery.

**Detection:** Set up cron job to check backup file age. Alert if no backup in 48 hours. UpdraftPlus sends email on backup success/failure.

**Confidence:** HIGH (verified via [WordPress Developer Handbook - Backups](https://developer.wordpress.org/advanced-administration/security/backup/))

## Moderate Pitfalls

### Pitfall 6: DNS Cutover Downtime (GitHub Pages to VPS)

**What goes wrong:** Changing DNS from GitHub Pages IP to VPS IP causes extended downtime because DNS caches hold the old IP for hours.
**Why it happens:** Default DNS TTL is often 3600s (1 hour) or higher. Some ISP resolvers ignore TTL and cache for 24+ hours. During propagation, some visitors hit old server, some hit new.
**Prevention:**

1. **48 hours before cutover:** Lower DNS A record TTL to 300 seconds (5 minutes)
2. **Wait for old TTL to expire** before changing the A record (if old TTL was 3600s, wait 1 hour minimum after setting 300s)
3. **Keep old GitHub Pages site running** during propagation -- both old and new should serve content
4. **Perform cutover during low-traffic hours** (late evening US Eastern for a NJ church site)
5. **After propagation completes** (verify with `dig` from multiple locations), raise TTL back to 3600s
6. **If using a custom domain** (not the rijhsinghani.github.io subdomain), the GitHub Pages CNAME config will need to be removed after cutover

**Detection:** Use `dig +short ambothoughts.com` from multiple DNS resolvers to verify propagation. Use [whatsmydns.net](https://www.whatsmydns.net/) for global check.

**Confidence:** HIGH (standard DNS migration practice)

### Pitfall 7: WordPress Performance Degradation on Small VPS

**What goes wrong:** A $6 VPS (1 vCPU, 1GB RAM) runs WordPress adequately at first, then becomes sluggish as plugins accumulate, database grows, or a traffic spike hits.
**Why it happens:** Each PHP-FPM worker consumes ~64MB RAM. With 1GB total RAM (minus OS overhead ~300MB), you get ~10 workers maximum. WordPress with multiple plugins can use 128MB+ per request. Unoptimized wp_options table autoloads grow over time.
**Consequences:** 503 errors during traffic spikes (Easter, Christmas -- peak church website traffic). Slow admin panel frustrates Deacon Henry. Search engines downrank slow sites.
**Prevention:**

- **Nginx + PHP-FPM stack (not Apache):** Best performance-to-cost ratio for small VPS. Apache with mod_php uses significantly more RAM per connection.
- **PHP-FPM config:** `pm = ondemand`, `pm.max_children = 4-6` for 1GB VPS. Do NOT use `pm = dynamic` on small VPS -- idle workers waste RAM
- **Nginx microcaching:** Cache full pages for 60s for anonymous users. Church site is 99% anonymous traffic -- massive win. Caching can reduce server resource needs by 70-90%.
- **Object cache:** Install Redis + Redis Object Cache plugin. Reduces database queries per page from 50+ to <10. Redis uses ~25MB RAM -- budget for this.
- **Database maintenance:** Schedule monthly cleanup of transients, post revisions (limit to 5: `define('WP_POST_REVISIONS', 5);`), and spam comments
- **Image optimization:** Use ShortPixel or Smush to compress on upload. Enable lazy loading (WordPress default since 5.5). Serve WebP where possible.
- **Caching plugin:** WP Super Cache or W3 Total Cache for full-page caching to disk. Nginx serves cached HTML directly, bypassing PHP entirely.
- **Plugin discipline:** Only install plugins you actually need. Each plugin adds PHP execution time and memory. Target: under 15 active plugins total.
- **Swap file:** Create a 1GB swap file as a safety net for memory spikes. Not a replacement for RAM, but prevents OOM kills: `fallocate -l 1G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile`
- **Minimum VPS spec recommendation:** $6/mo DigitalOcean droplet (1 vCPU, 1GB RAM) is sufficient for this low-traffic church site WITH caching. Without caching, consider $12/mo (2GB RAM).

**Detection:** Monitor with `htop` for RAM/CPU. Set up New Relic free tier or WP Query Monitor plugin for slow queries.

**Confidence:** HIGH (PHP-FPM worker math verified via [ManagingWP](https://managingwp.io/2025/10/01/why-php-fpm-process-worker-limits-matter-preventing-server-outages-with-standardized-pool-configuration/) and [SpinupWP](https://spinupwp.com/doc/how-php-workers-impact-wordpress-performance/), Nginx recommendation from [Contabo optimization guide](https://contabo.com/blog/the-ultimate-wordpress-vps-performance-optimization-checklist/))

### Pitfall 8: Admin Handoff to Non-Technical User

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
- **Disable plugin/theme install from admin:** `define('DISALLOW_FILE_MODS', true);` -- this also disables updates from admin, so you must handle updates via WP-CLI or SSH
- **Create a simple 1-page "How To" guide** for Deacon Henry covering: how to create a post, how to add images, how to edit a page. Include screenshots. Avoid technical jargon.
- **Set up automatic WordPress core updates** for minor/security versions so the site stays patched without admin intervention
- **Password management:** Use a strong, unique password for Deacon Henry's account. Consider setting up 2FA with a simple plugin like WP 2FA -- but weigh usability. A complex 2FA setup may lock him out.

**Detection:** Periodically check the activity log (install Simple History plugin) to see what actions Deacon Henry is taking.

**Confidence:** HIGH (standard WordPress admin management pattern)

### Pitfall 9: SEO Loss During Static HTML to WordPress Migration

**What goes wrong:** Existing pages at `rijhsinghani.github.io/ambo-thoughts/about.html` become 404s after migration because WordPress uses `/about/` URL structure (no .html extension). Search engines drop indexed pages.
**Why it happens:** WordPress uses "pretty permalinks" (`/post-name/`) by default, which don't match the old `.html` URL structure. GitHub Pages subdirectory paths also differ from a root domain setup.
**Consequences:** Existing Google indexing lost. Backlinks from church directories or diocesan sites break. 404 errors for bookmarked pages. One missing redirect can break SEO momentum -- long-tail pages that brought organic visitors quietly vanish.
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
- **Avoid redirect chains:** Each redirect hop loses ~10% SEO authority. Map directly from old URL to final new URL -- never chain through intermediate URLs.
- **Submit updated sitemap** to Google Search Console after migration
- **Keep old GitHub Pages site** running with meta refresh redirects for 3-6 months as a fallback
- **Use Redirection plugin** in WordPress for any URLs you discover later that 404

**Detection:** Monitor Google Search Console for crawl errors and 404s after migration. Check Google Analytics for traffic drops.

**Confidence:** HIGH (standard migration practice, verified via [ParallelDevs](https://www.paralleldevs.com/blog/how-use-301-redirects-when-redesigning-or-migrating-wordpress-site-without-losing-seo/) and [Semrush 301 guide](https://www.semrush.com/blog/301-redirects/))

### Pitfall 10: Contact Form Spam Floods

**What goes wrong:** The contact form (sending to deacon267@verizon.net and hcugini@stroberts.cc) gets hammered with spam submissions -- fake pharmaceutical ads, SEO services, phishing links. Deacon Henry's inbox fills with junk and legitimate prayer requests get buried.
**Why it happens:** WordPress contact forms are a top spam target. Bots crawl the web for exposed form endpoints. A church website contact form is especially attractive because it's always publicly accessible and rarely has aggressive filtering.
**Consequences:** Important messages from parishioners missed. Deacon Henry loses trust in the contact form. If the transactional email service sends too many spam-originated emails, the sending domain's reputation degrades and legitimate emails start bouncing.
**Prevention (layered approach -- use all three):**

1. **Honeypot field (invisible):** Most form plugins (WPForms, Contact Form 7) support hidden honeypot fields that bots fill out but humans don't see. Zero user friction. Catches ~70% of basic bots.
2. **reCAPTCHA v3 or hCaptcha:** Invisible challenge that scores visitors. reCAPTCHA v3 requires no user interaction. hCaptcha is more privacy-friendly (no Google tracking -- appropriate for a church site). Configure threshold to block scores below 0.5.
3. **Minimum submission time:** Block submissions that happen in under 2 seconds (bots fill forms instantly). WPForms has this built-in.
4. **Akismet:** Free for personal/non-commercial sites (this church site qualifies). Checks submissions against a global spam database. Catches sophisticated spam that honeypots miss.
5. **Do NOT use CAPTCHA alone** -- it's annoying for elderly parishioners and doesn't stop all bots.

**Detection:** Check spam folder in form plugin weekly. Monitor transactional email service for sending reputation.

**Confidence:** HIGH (verified via [WPForms spam guide](https://wpforms.com/how-to-build-spam-free-wordpress-contact-forms-the-ultimate-guide/) and [WPBeginner](https://www.wpbeginner.com/plugins/how-to-block-contact-form-spam-in-wordpress/))

### Pitfall 11: Ongoing VPS Maintenance Burden

**What goes wrong:** You set up the VPS, hand it off, and stop maintaining it. Six months later: PHP version is outdated with known CVEs, Ubuntu has unpatched vulnerabilities, MySQL hasn't been optimized, SSL certificate silently expired, and the site gets compromised.
**Why it happens:** Self-managed VPS means ALL server administration falls on you. There is no managed hosting team. Unlike GitHub Pages (zero maintenance), a VPS requires active, ongoing attention. This is the hidden cost of the $6/mo price tag.
**Consequences:** Security breach, site downtime, performance degradation, SSL expiration (browsers show scary warnings to church visitors).
**Prevention (monthly maintenance routine -- budget 1-2 hours/month):**

- **OS security patches:** `apt update && apt upgrade -y` monthly, or enable `unattended-upgrades` for automatic security patches
- **PHP version management:** PHP gets security-only updates for 2 years after release, then EOL. Track your PHP version's EOL date. PHP 8.1 EOL was Dec 2025. Use PHP 8.2+ (security support through Dec 2026) or PHP 8.3 (active support through Nov 2026).
- **MySQL/MariaDB updates:** `apt upgrade` covers this on Ubuntu. Run `mysqlcheck --optimize --all-databases` quarterly to defragment tables.
- **SSL certificate monitoring:** Certbot auto-renews, but failures are silent. Add a cron check:
  ```bash
  # Alert if cert expires in < 14 days
  openssl x509 -enddate -noout -in /etc/letsencrypt/live/domain/cert.pem | cut -d= -f2
  ```
- **Disk space monitoring:** WordPress uploads, logs, and database dumps accumulate. Set up alert at 80% disk usage. Rotate logs with `logrotate`.
- **WordPress core updates:** WordPress 6.9 (late 2025) disabled auto-updates for minor core releases by default. You must manually trigger or re-enable auto-updates.
- **Fail2ban log review:** Check `fail2ban-client status wordpress` monthly to see ban activity. Persistent attackers may need permanent IP blocks.
- **Consider managed alternative:** If maintenance becomes burdensome, migrate to managed WordPress hosting (Cloudways ~$14/mo, or even WordPress.com Business ~$25/mo) to eliminate server admin entirely. The $6/mo VPS saves money but costs time.

**Detection:** Set up a simple monitoring dashboard: UptimeRobot (free, uptime), StatusCake (free, SSL expiry), `df -h` cron alert (disk space).

**Confidence:** HIGH (inherent to self-managed VPS hosting)

## Minor Pitfalls

### Pitfall 12: ChurchWP Bundled Plugin Conflicts

**What goes wrong:** ChurchWP bundles plugins (Visual Composer/WPBakery, Revolution Slider, etc.) that conflict with separately installed versions or other plugins.
**Why it happens:** ThemeForest themes bundle commercial plugins at specific versions. The bundled license does NOT give you a separate plugin license -- you cannot download updates directly from WPBakery. Plugin updates only come when the theme author pushes a theme update. If you install the plugin separately (e.g., a newer WPBakery from its official site), the two versions conflict. ChurchWP has already deprecated its Massive Addons and TSLR Maps plugins.
**Prevention:**

- Use ONLY the bundled plugin versions that ChurchWP provides
- Do NOT install separate copies of WPBakery, Revolution Slider, or other bundled plugins
- Replace deprecated TSLR Maps with Google Maps Embed (per ChurchWP docs)
- Remove the deprecated Massive Addons plugin if not needed
- Before installing any new plugin, test on staging for conflicts with ChurchWP's bundled plugins
- Accept that bundled plugin updates lag behind official releases -- this is a known limitation of ThemeForest themes

**Detection:** After plugin install, check for PHP errors in `wp-content/debug.log` (enable `WP_DEBUG_LOG` in wp-config.php).

**Confidence:** MEDIUM (ChurchWP-specific details from [ThemeForest listing](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148), bundled license limitation confirmed via [Envato Forums](https://forums.envato.com/t/i-purchased-theme-from-themeforest-and-i-got-wp-bakery-page-builder-how-i-can-activate-wp-bakery-licence/285743))

### Pitfall 13: ThemeForest Theme Lock-in

**What goes wrong:** After building the site with ChurchWP's bundled page builder (WPBakery), custom post types, and shortcodes, switching themes later requires rebuilding every page from scratch.
**Why it happens:** ThemeForest themes use proprietary shortcodes and page builder elements that only render with that specific theme active. Content is stored with `[shortcode]` tags that become visible garbage text without the theme. WPBakery specifically leaves behind shortcode clutter that requires manual cleanup.
**Prevention:**

- Use the WordPress block editor (Gutenberg) for page content whenever possible instead of WPBakery shortcodes
- Store critical content (bio, ministry info) as standard WordPress pages with standard blocks, not in theme-specific widgets
- Keep ChurchWP-specific elements (sliders, custom layouts) limited to the homepage and a few showcase pages
- Document which pages use theme-specific elements vs standard WordPress content

**Detection:** Temporarily switch to a default theme (Twenty Twenty-Four) and check which pages break.

**Confidence:** HIGH (well-known ThemeForest lock-in pattern, WPBakery shortcode clutter confirmed via [SeedProd WPBakery review](https://www.seedprod.com/wpbakery-review/))

### Pitfall 14: Contact Form Email Delivery Failures

**What goes wrong:** WordPress contact form emails (to deacon267@verizon.net and hcugini@stroberts.cc) go to spam or never arrive because the VPS IP has no email reputation.
**Why it happens:** PHP's `mail()` function sends from the VPS IP, which has no SPF/DKIM records. Gmail, Outlook, and Verizon aggressively filter VPS-originated email.
**Prevention:**

- Do NOT rely on PHP mail(). Install WP Mail SMTP plugin.
- Use a transactional email service: Resend (you already use this), SendGrid free tier (100/day), or Mailgun free tier
- Set SPF and DKIM DNS records for the domain
- Test form delivery to both Verizon and stroberts.cc addresses after setup -- these older email providers are especially aggressive with spam filtering

**Detection:** Submit a test contact form immediately after setup. Check spam folders.

**Confidence:** HIGH (universal WordPress email problem)

### Pitfall 15: WordPress Auto-Update Breaks Site

**What goes wrong:** An automatic WordPress core, theme, or plugin update introduces a fatal PHP error, white-screening the site. This can happen at 2 AM and go unnoticed until someone reports it.
**Why it happens:** WordPress auto-updates minor versions by default (though WordPress 6.9 changed this -- see below). Plugins may auto-update if enabled. A PHP incompatibility or plugin conflict crashes the site. Developers don't test updates for compatibility with every theme/plugin combination.
**2025-2026 policy shift:** WordPress 6.9 (final major release of 2025) turned off auto-updates for minor core releases by default, giving users more control. This means the site will NOT auto-patch unless you explicitly re-enable it or manually update. This is a double-edged sword: more stability but requires manual security patching.
**Prevention:**

- Re-enable auto-updates for WordPress core minor/security versions (they were turned off in 6.9): `add_filter('allow_minor_auto_core_updates', '__return_true');`
- Disable auto-updates for plugins and themes: `add_filter('auto_update_plugin', '__return_false');` and `add_filter('auto_update_theme', '__return_false');`
- **Update strategy:** Update plugins one at a time, not in bulk. Test after each. Bulk updates make it impossible to identify which plugin caused a breakage.
- Install WP Rollback plugin for emergency theme/plugin downgrades
- Keep backups current before ANY update (see Pitfall 5)
- Enable `WP_DEBUG_LOG` (not `WP_DEBUG_DISPLAY`) so errors go to log file, not visitor-facing

**Detection:** UptimeRobot monitoring (free tier) pings the site every 5 minutes. Email alert on downtime.

**Confidence:** HIGH (WordPress 6.9 auto-update change verified via [WP Builder Lab](https://wpbuilderlab.com/wordpress-turns-off-auto-updates-2025-guide/) and [NHance Digital](https://www.nhancedigital.com/why-auto-update-is-a-dangerous-game-for-professional-wordpress-sites-in-2026/))

### Pitfall 16: ChurchWP Theme Abandonment

**What goes wrong:** The ChurchWP theme author stops maintaining the theme. No more updates, no PHP compatibility fixes, no security patches. The theme becomes incompatible with newer WordPress versions.
**Why it happens:** ThemeForest themes are often built by small teams or solo developers. Revenue declines as sales slow. The author moves on. ChurchWP's last update was January 2025 (PHP compatibility fixes). If another year passes without updates, this becomes a concern.
**Consequences:** PHP deprecation warnings appear as PHP versions advance. WordPress core changes break theme functionality. Security vulnerabilities go unpatched. Eventually forced to rebuild on a different theme -- hitting the lock-in problem (Pitfall 13) at the worst possible time.
**Prevention:**

- Check ChurchWP's ThemeForest page for update history before purchasing. Look for consistent updates over the past 2 years.
- Build with Gutenberg blocks wherever possible (not WPBakery) to minimize theme dependency
- Keep the child theme well-documented so a developer can patch compatibility issues manually if needed
- Have a backup theme plan: Flavor theme or flavor by flavor-developer (also on ThemeForest) as a migration target if ChurchWP dies
- Accept the risk: for a ~$59 theme on a small church site, this is an acceptable trade-off. Rebuilding a simple site takes days, not months.

**Detection:** Check ThemeForest listing quarterly for update activity. Set a calendar reminder.

**Confidence:** MEDIUM (general ThemeForest risk, ChurchWP specifically updated as of Jan 2025)

## Phase-Specific Warnings

| Phase Topic         | Likely Pitfall                      | Mitigation                                                        |
| ------------------- | ----------------------------------- | ----------------------------------------------------------------- |
| VPS Setup           | Unsecured server (Pitfall 2)        | Complete security hardening checklist before installing WordPress |
| VPS Setup           | No backup strategy (Pitfall 5)      | Configure automated backups to off-server storage before launch   |
| Theme Customization | Lost customizations (Pitfall 1)     | Child theme FIRST, before any CSS/PHP changes                     |
| Content Migration   | HEIC upload failures (Pitfall 3)    | Batch convert to JPEG/WebP locally before upload                  |
| Content Migration   | Broken URLs (Pitfall 9)             | Map all old URLs, configure nginx 301 redirects                   |
| SSL Setup           | Mixed content (Pitfall 4)           | Install as HTTPS from the start, never HTTP                       |
| DNS Cutover         | Extended downtime (Pitfall 6)       | Lower TTL 48 hours before, keep old site running                  |
| Contact Form        | Spam floods (Pitfall 10)            | Layered: honeypot + hCaptcha + Akismet + min submission time      |
| Contact Form        | Email delivery (Pitfall 14)         | WP Mail SMTP + Resend, test both recipient addresses              |
| Admin Handoff       | Accidental breakage (Pitfall 8)     | Editor role, not Admin. Simplify panel. Training doc.             |
| Post-Launch         | Performance degradation (Pitfall 7) | Caching stack from day one: nginx microcache + Redis + page cache |
| Post-Launch         | Update breakage (Pitfall 15)        | Re-enable core minor auto-updates, disable plugin auto-updates    |
| Ongoing             | VPS maintenance burden (Pitfall 11) | Monthly maintenance routine, 1-2 hours. Or migrate to managed.    |
| Long-term           | Theme abandonment (Pitfall 16)      | Build with Gutenberg, minimize WPBakery dependency                |

## Sources

- [Best Practices for Securing WordPress on VPS 2025 - Unihost](https://unihost.com/blog/securing-wordpress-vps-2025/)
- [VPS Hardening with Fail2Ban - VPS.DO](https://vps.do/fail2ban-vps/)
- [WordPress Security Hardening Guide 2025 - WP Security Ninja](https://wpsecurityninja.com/wordpress-security-hardening-guide/)
- [State of WordPress Security 2025 - Patchstack](https://patchstack.com/whitepaper/state-of-wordpress-security-in-2025/)
- [XML-RPC Brute-Force Exploitation 2025 - Medium](https://medium.com/@medjahdii/the-hidden-danger-in-wordpress-xml-rpc-brute-force-exploitation-explained-2025-edition-6b21f3e311dc)
- [XML-RPC Security Risks - Patchstack](https://patchstack.com/articles/xml-rpc-in-wordpress/)
- [XML-RPC in WordPress - Kinsta](https://kinsta.com/blog/xmlrpc-php/)
- [WordPress Brute Force Protection - Developer Handbook](https://developer.wordpress.org/advanced-administration/security/brute-force/)
- [WP fail2ban Plugin](https://wordpress.org/plugins/wp-fail2ban/)
- [WordPress Child Themes - Developer Handbook](https://developer.wordpress.org/themes/advanced-topics/child-themes/)
- [HEIC Support in WordPress 6.7 - Make WordPress Core](https://make.wordpress.org/core/2024/08/15/automatic-conversion-of-heic-images-to-jpeg-in-wordpress-6-7/)
- [HEIC to JPEG Plugin](https://wordpress.org/plugins/heic-to-jpeg/)
- [HEIC/HEIF Workflow - ShortPixel](https://shortpixel.com/blog/heic-heif-on-wordpress-an-end-to-end-workflow-from-iphone-upload-to-webp-avif/)
- [301 Redirects for WordPress Migration - ParallelDevs](https://www.paralleldevs.com/blog/how-use-301-redirects-when-redesigning-or-migrating-wordpress-site-without-losing-seo/)
- [301 Redirects and SEO - Semrush](https://www.semrush.com/blog/301-redirects/)
- [WordPress SEO Migration Checklist 2025 - LitExtension](https://litextension.com/blog/wordpress-seo-migration/)
- [WordPress Backup Strategy 2025 - WebHostMost](https://blog.webhostmost.com/wordpress-backup-strategy-2025/)
- [WordPress Backups - Developer Handbook](https://developer.wordpress.org/advanced-administration/security/backup/)
- [WordPress Turns Off Auto-Updates 2025 - WP Builder Lab](https://wpbuilderlab.com/wordpress-turns-off-auto-updates-2025-guide/)
- [Auto-Update Risks 2026 - NHance Digital](https://www.nhancedigital.com/why-auto-update-is-a-dangerous-game-for-professional-wordpress-sites-in-2026/)
- [Contact Form Spam Prevention - WPForms](https://wpforms.com/how-to-build-spam-free-wordpress-contact-forms-the-ultimate-guide/)
- [Block Contact Form Spam - WPBeginner](https://www.wpbeginner.com/plugins/how-to-block-contact-form-spam-in-wordpress/)
- [PHP-FPM Worker Limits - ManagingWP](https://managingwp.io/2025/10/01/why-php-fpm-process-worker-limits-matter-preventing-server-outages-with-standardized-pool-configuration/)
- [PHP Workers and WordPress Performance - SpinupWP](https://spinupwp.com/doc/how-php-workers-impact-wordpress-performance/)
- [WordPress VPS Performance Optimization - Contabo](https://contabo.com/blog/the-ultimate-wordpress-vps-performance-optimization-checklist/)
- [WordPress VPS Optimization 2025 - WiliVM](https://www.wilivm.com/blog/how-to-optimize-vps-for-wordpress-speed-in-2025/)
- [WPBakery Review 2026 - SeedProd](https://www.seedprod.com/wpbakery-review/)
- [ThemeForest Bundled Plugin Licensing - Envato Forums](https://forums.envato.com/t/i-purchased-theme-from-themeforest-and-i-got-wp-bakery-page-builder-how-i-can-activate-wp-bakery-licence/285743)
- [ChurchWP - ThemeForest](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148)
- [PublishPress Capabilities Plugin](https://wordpress.org/plugins/capability-manager-enhanced/)
- [WordPress Security Best Practices 2026 - WP Rocket](https://wp-rocket.me/blog/wordpress-security-best-practices/)
