# Phase 1: Infrastructure + Launch Site - Research

**Researched:** 2026-03-07
**Domain:** WordPress VPS hosting, ChurchWP theme customization, content migration
**Confidence:** HIGH

## Summary

Phase 1 covers four major workstreams: (1) VPS provisioning and security hardening on DigitalOcean, (2) WordPress installation with ChurchWP theme and Navy/Gold customization, (3) content migration from static HTML pages to WordPress via WP-CLI, and (4) deployment pipeline from Local by Flywheel to production. Every component in this phase is a well-documented WordPress pattern with extensive community guides.

The most critical sequencing constraint is that VPS security hardening MUST happen before WordPress installation -- bots scan new droplets within hours. The second key constraint is that HEIC images must be batch-converted locally before upload (server-side HEIC support is fragile). The domain is deferred, so initial setup uses the VPS IP address with SSL deferred until a domain is configured.

**Primary recommendation:** Use Local by Flywheel for development with "Open Site Shell" for WP-CLI access. Import ChurchWP demo data first, then customize. Deploy to DigitalOcean via rsync + WP-CLI database migration.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

1. **Local Development Environment:** Use Local by Flywheel (not Docker, not MAMP)
2. **Demo Import Strategy:** Import ChurchWP demo data first, then customize (Theme Panel > Demo Importer, then Revolution Slider import, then color/font customization, then page-by-page content replacement)
3. **SMTP & Contact Form:** DEFERRED -- skip contact form setup for Phase 1. Contact page exists as placeholder.
4. **Content Migration Approach:** WP-CLI automation where possible (`wp post create`, `wp media import`, `wp menu`). WPBakery only for visual layout adjustments.
5. **VPS Setup:** DigitalOcean $6/mo droplet, manual LEMP stack setup (Ubuntu 24.04 LTS, Nginx 1.24+, PHP-FPM 8.3, MariaDB 10.11 LTS, Redis, Certbot)
6. **Domain Strategy:** Skip domain for now, use VPS IP address initially. SSL deferred until domain ready. All configs designed for easy domain swap via `wp search-replace`.
7. **Hero Slider:** 3 slides using Revolution Slider (bundled with ChurchWP) with specific content per CONTEXT.md
8. **Header Layout:** Cross logo centered, Navy background, white border, no contact info
9. **Homepage Sections (Phase 1):** Gallery, Church News, Bio sections only. Latest Homilies deferred to Phase 2.
10. **Image Handling:** Batch convert HEIC locally with `sips`, upload JPEG/WebP. Smush plugin for compression.

### Claude's Discretion

- Exact Nginx configuration details (FastCGI cache tuning, PHP-FPM pool settings)
- WP-CLI script organization and execution order
- Child theme file structure beyond the mandated header.php/footer.php overrides
- Deployment script implementation details

### Deferred Ideas (OUT OF SCOPE)

- RSS feed for spirituality page (verseoftheday.com) -- Phase 2
- Latest Homilies homepage section -- Phase 2 (needs Homily CPT)
- Bible Verse of the Day plugin -- Phase 2
- Homily CPT and pipeline integration -- Phase 2
- Admin role management and training -- Phase 3
- UptimeRobot monitoring -- Phase 3
- Contact form (CF7, Flamingo, WP Mail SMTP, Resend) -- deferred from Phase 1
  </user_constraints>

<phase_requirements>

## Phase Requirements

| ID                   | Description                                                 | Research Support                                 |
| -------------------- | ----------------------------------------------------------- | ------------------------------------------------ |
| REQ-HOSTING-001      | VPS Provisioning (DO 1vCPU/1GB/25GB, Ubuntu 24.04)          | VPS setup commands section                       |
| REQ-HOSTING-002      | Web Server Stack (Nginx + PHP-FPM 8.3 + MariaDB 10.11)      | LEMP install commands section                    |
| REQ-HOSTING-003      | Security Hardening (SSH keys, UFW, fail2ban, xmlrpc, perms) | Security hardening section                       |
| REQ-HOSTING-004      | SSL Certificate (Certbot + Let's Encrypt)                   | SSL section -- NOTE: deferred until domain ready |
| REQ-HOSTING-005      | Automated Backups (UpdraftPlus to Google Drive)             | Plugin stack -- install & configure              |
| REQ-HOSTING-006      | Page Caching (Nginx FastCGI cache)                          | FastCGI cache configuration section              |
| REQ-HOSTING-007      | Object Caching (Redis + Redis Object Cache plugin)          | Redis setup section                              |
| REQ-HOSTING-008      | Security Plugin (Wordfence)                                 | Plugin stack -- install & activate               |
| REQ-HOSTING-009      | wp-config.php Environment Management                        | wp-config pattern section                        |
| REQ-HOSTING-010      | Deployment Pipeline (Local > rsync > VPS)                   | Deployment pipeline section                      |
| REQ-THEME-001        | ChurchWP Parent Theme + bundled plugins                     | ChurchWP installation section                    |
| REQ-THEME-002        | Child Theme Setup (churchwp-child/)                         | Child theme architecture section                 |
| REQ-THEME-003        | Color Customization (Navy/Gold)                             | Color customization section                      |
| REQ-THEME-004        | Typography (Playfair Display + system sans)                 | Typography section                               |
| REQ-THEME-005        | Bundled Plugin Compatibility (PHP 8.3)                      | Test in Local by Flywheel first                  |
| REQ-DESIGN-001       | Header (cross logo, navy bg, no contact info)               | Header customization section                     |
| REQ-DESIGN-002       | Navigation Menu (8 items)                                   | WP-CLI menu commands section                     |
| REQ-DESIGN-003       | Hero Slider (3 Revolution Slider slides)                    | Revolution Slider section                        |
| REQ-DESIGN-005       | Homepage Gallery Section (YouTube embed)                    | Content migration section                        |
| REQ-DESIGN-006       | Homepage Church News Section                                | Content migration section                        |
| REQ-DESIGN-007       | Homepage Bio Section                                        | Content migration section                        |
| REQ-DESIGN-008       | Remove "church love, faith love" section                    | Demo customization process                       |
| REQ-DESIGN-009       | Branding Text (Ambo Thoughts, subtitles)                    | Slider + header customization                    |
| REQ-CONTENT-001      | About Page                                                  | WP-CLI content migration section                 |
| REQ-CONTENT-002      | Spirituality Page                                           | WP-CLI content migration section                 |
| REQ-CONTENT-003      | Church News Page                                            | WP-CLI content migration section                 |
| REQ-CONTENT-004      | Contact Page (placeholder only -- form deferred)            | WP-CLI page creation                             |
| REQ-CONTENT-005      | Pictures/Gallery Page (FooGallery)                          | Gallery plugin section                           |
| REQ-CONTENT-006      | Prayer Partner Page                                         | WP-CLI content migration section                 |
| REQ-CONTENT-007      | Stuff Page                                                  | WP-CLI content migration section                 |
| REQ-CONTENT-008      | Videos Page (YouTube embeds via Embed Plus)                 | Video embed section                              |
| REQ-CONTENT-009      | Blog Post Migration (2 posts)                               | WP-CLI post creation section                     |
| REQ-CONTENT-010      | Motto Display                                               | Slider slide 2 + About page                      |
| REQ-NEWS-001         | Vatican News Link                                           | Content migration section                        |
| REQ-NEWS-002         | Diocese of Trenton Link                                     | Content migration section                        |
| REQ-SPIRITUALITY-001 | Hero Image (convert HEIC)                                   | HEIC conversion section                          |
| REQ-SPIRITUALITY-002 | Gospel Quote (no watermark)                                 | Content migration section                        |
| REQ-GALLERY-001      | FooGallery plugin                                           | Plugin stack section                             |
| REQ-GALLERY-002      | Photo Sources (iCloud /Hank/)                               | Image handling section                           |
| REQ-GALLERY-003      | HEIC Image Conversion                                       | HEIC conversion section                          |
| REQ-GALLERY-004      | Image Compression (Smush)                                   | Plugin stack section                             |
| REQ-GALLERY-005      | Homepage Video Embed (Embed Plus)                           | Plugin stack section                             |
| REQ-MIGRATION-001    | URL Redirects (.html to WP permalinks)                      | Nginx redirect rules section                     |
| REQ-MIGRATION-002    | SEO Preservation (Rank Math, sitemap)                       | SEO plugin section                               |
| REQ-MIGRATION-003    | DNS Cutover                                                 | Deferred until domain ready                      |
| REQ-MIGRATION-004    | Content Transfer (all static pages)                         | WP-CLI migration section                         |
| REQ-MIGRATION-005    | GitHub Pages Decommission                                   | After DNS propagation                            |
| REQ-ADMIN-006        | Plugin Blacklist                                            | Don't Hand-Roll section                          |

</phase_requirements>

## Standard Stack

### Core

| Library/Tool      | Version                  | Purpose                     | Why Standard                                         |
| ----------------- | ------------------------ | --------------------------- | ---------------------------------------------------- |
| Local by Flywheel | Latest                   | Local WordPress development | Zero-config, built-in WP-CLI, GUI, free              |
| WordPress         | 6.7+                     | CMS platform                | Target platform                                      |
| ChurchWP          | Latest (ThemeForest)     | Parent theme                | Church-specific design, bundled plugins              |
| Nginx             | 1.24+ (ppa:ondrej/nginx) | Web server                  | FastCGI cache support, low memory footprint          |
| PHP-FPM           | 8.3 (ppa:ondrej/php)     | PHP processor               | WordPress recommended, Ubuntu 24.04 default PPA      |
| MariaDB           | 10.11 LTS                | Database                    | Drop-in MySQL replacement, Ubuntu 24.04 default repo |
| Redis/Valkey      | Latest                   | Object cache                | Reduces DB queries, standard on VPS WordPress        |
| WP-CLI            | Latest                   | WordPress CLI automation    | Standard for scripted WordPress management           |
| Certbot           | Latest                   | SSL certificates            | Let's Encrypt automation -- deferred until domain    |

### Supporting (Plugins)

| Plugin                          | Purpose                             | When to Use                   |
| ------------------------------- | ----------------------------------- | ----------------------------- |
| ThemeSLR Framework              | ChurchWP theme options panel        | Bundled -- install with theme |
| WPBakery Page Builder           | Page layouts                        | Bundled -- install with theme |
| Slider Revolution               | Hero slider                         | Bundled -- install with theme |
| Rank Math                       | SEO, sitemaps, redirects            | After WordPress install       |
| Wordfence                       | Security firewall, malware scan     | After WordPress install       |
| UpdraftPlus                     | Automated backups to Google Drive   | After WordPress install       |
| FooGallery                      | Photo gallery with lightbox         | For Pictures page             |
| Embed Plus for YouTube          | Lazy-loaded responsive video embeds | For Videos page + homepage    |
| Smush                           | Image compression on upload         | Before bulk media upload      |
| Redis Object Cache (Till Kruss) | Database query caching              | After Redis server installed  |

### Alternatives Considered

| Instead of    | Could Use      | Tradeoff                                                                 |
| ------------- | -------------- | ------------------------------------------------------------------------ |
| MariaDB       | MySQL 8.4      | MariaDB is in Ubuntu 24.04 default repos, simpler install                |
| PHP 8.3       | PHP 8.4        | 8.4 is available via ondrej PPA but 8.3 has wider plugin compat          |
| Rank Math     | Yoast          | Rank Math free tier includes redirect manager + unlimited focus keywords |
| Nginx FastCGI | WP Super Cache | FastCGI serves HTML without invoking PHP at all -- strictly superior     |

**Installation (VPS):**

```bash
# LEMP stack
sudo add-apt-repository ppa:ondrej/nginx -y && sudo add-apt-repository ppa:ondrej/php -y
sudo apt update && sudo apt dist-upgrade -y
sudo apt install nginx mariadb-server redis-server -y
sudo apt install php8.3-fpm php8.3-common php8.3-mysql php8.3-xml php8.3-intl \
  php8.3-curl php8.3-gd php8.3-imagick php8.3-cli php8.3-mbstring \
  php8.3-opcache php8.3-redis php8.3-soap php8.3-zip -y

# WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp
```

## Architecture Patterns

### Recommended Project Structure (Git-tracked)

```
ambo-thoughts/
├── wp-content/themes/churchwp-child/    # Child theme (ALL customizations here)
│   ├── style.css                        # Theme metadata + CSS overrides
│   ├── functions.php                    # Enqueue parent styles, custom functions
│   ├── header.php                       # Override: cross logo, no contact info
│   ├── footer.php                       # Override: custom footer
│   ├── css/
│   │   └── custom.css                   # Navy/Gold CSS custom properties
│   └── inc/
│       └── (empty for Phase 1)          # Phase 2: homily-cpt.php goes here
├── scripts/
│   ├── setup-vps.sh                     # VPS provisioning automation
│   ├── deploy.sh                        # rsync deployment script
│   ├── migrate-content.sh               # WP-CLI content migration
│   └── convert-heic.sh                  # HEIC batch conversion
├── content/                             # Extracted HTML content for WP-CLI import
│   ├── about.html                       # About page content (HTML body only)
│   ├── spirituality.html
│   ├── church-news.html
│   ├── prayer-partner.html
│   ├── stuff.html
│   ├── videos.html
│   └── posts/
│       ├── holy-thursday.html
│       └── good-samaritan.html
├── nginx/
│   └── wordpress.conf                   # Nginx server block template
├── .gitignore                           # WP core, parent theme, uploads, plugins, wp-config
└── README.md
```

### Pattern 1: Local by Flywheel Development Setup

**What:** Local by Flywheel provides a GUI-based local WordPress environment with built-in WP-CLI
**When to use:** All local development and testing

**Setup steps:**

1. Download from https://localwp.com/ and install to /Applications
2. Launch Local, click "+ Create a New Site"
3. Site name: "ambo-thoughts"
4. Choose "Custom" environment: PHP 8.3, Nginx, MySQL 8.0
5. Set admin credentials (username/password/email)
6. Click "Add Site" -- WordPress installs automatically

**Site paths on macOS:**

```
~/Local Sites/ambo-thoughts/app/public/          # WordPress root
~/Local Sites/ambo-thoughts/app/public/wp-content/  # Themes, plugins, uploads
~/Local Sites/ambo-thoughts/conf/                 # Nginx/PHP/MySQL configs
~/Local Sites/ambo-thoughts/logs/                 # Server logs
```

**WP-CLI access:** Right-click site in Local GUI > "Open Site Shell" -- this opens a terminal with WP-CLI pre-configured and PHP/MySQL paths set.

### Pattern 2: ChurchWP Demo Import Then Customize

**What:** Import all demo data first to get the full layout structure, then replace content
**When to use:** Initial theme setup

**Steps:**

1. In WordPress admin: Appearance > Themes > Add New > Upload Theme
2. Upload `churchwp.zip` (parent) > Install > Activate
3. Upload `churchwp-child.zip` > Install > Activate
4. Install required plugins when prompted (ThemeSLR Framework, WPBakery, Revolution Slider)
   - WordPress will show "Begin installing plugins" notice
   - Install from bundled .zip files in the theme package
5. Go to Theme Panel > Demo Importer > Import demo data
   - This imports: `content.xml` (pages/posts), `theme-options.txt` (panel settings), `widgets.wie` (widget config)
   - Revolution Sliders (`main_home_slider.zip`) import automatically with demo
6. After import: customize colors via Theme Panel > Styling, then replace content page-by-page

### Pattern 3: wp-config.php Environment Management

**What:** Mark Jaquith's local-config.php pattern for environment-specific settings
**When to use:** All environments

```php
// wp-config.php (top, before any other config)
if ( file_exists( __DIR__ . '/local-config.php' ) ) {
    require __DIR__ . '/local-config.php';
    define( 'WP_LOCAL_DEV', true );
} else {
    // Production settings
    define( 'DB_NAME',     getenv('WP_DB_NAME')     ?: 'wordpress');
    define( 'DB_USER',     getenv('WP_DB_USER')     ?: 'wpuser');
    define( 'DB_PASSWORD', getenv('WP_DB_PASSWORD') ?: '');
    define( 'DB_HOST',     getenv('WP_DB_HOST')     ?: 'localhost');
    define( 'WP_DEBUG',    false );
    define( 'DISALLOW_FILE_EDIT', true );
}
```

```php
// local-config.php (gitignored)
define( 'DB_NAME',     'local' );
define( 'DB_USER',     'root' );
define( 'DB_PASSWORD', 'root' );
define( 'DB_HOST',     'localhost:/path/to/mysql.sock' );
define( 'WP_DEBUG',    true );
define( 'WP_DEBUG_LOG', true );
```

### Pattern 4: Deployment via rsync + WP-CLI

**What:** Deploy child theme and scripts from local to production
**When to use:** Every deployment

```bash
#!/bin/bash
# deploy.sh
VPS_USER="deploy"
VPS_HOST="YOUR_VPS_IP"
VPS_PATH="/home/$VPS_USER/ambo-thoughts/public"

# Sync child theme
rsync -avz --delete \
  ~/Local\ Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/ \
  $VPS_USER@$VPS_HOST:$VPS_PATH/wp-content/themes/churchwp-child/

# Sync uploaded media (one-way, don't delete remote)
rsync -avz \
  ~/Local\ Sites/ambo-thoughts/app/public/wp-content/uploads/ \
  $VPS_USER@$VPS_HOST:$VPS_PATH/wp-content/uploads/

# Database: export local, import remote, search-replace URLs
ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && wp cache flush"
```

**Database sync (production-to-local only):**

```bash
# On VPS
wp db export ~/backup.sql
# Copy to local
scp $VPS_USER@$VPS_HOST:~/backup.sql ~/
# In Local Site Shell
wp db import ~/backup.sql
wp search-replace 'http://YOUR_VPS_IP' 'http://ambo-thoughts.local'
```

### Anti-Patterns to Avoid

- **Editing parent theme files:** All changes lost on theme update. Always use child theme.
- **Git-tracking WordPress core or plugins:** Bloats repo, conflicts on updates. Track child theme and scripts only.
- **Installing WP Super Cache alongside FastCGI cache:** Redundant and can conflict. FastCGI cache is server-level and superior.
- **Using Elementor with WPBakery:** Direct conflict. ChurchWP bundles WPBakery -- use it or plain HTML.
- **Installing Yoast alongside Rank Math:** Only one SEO plugin.

## Don't Hand-Roll

| Problem                   | Don't Build                  | Use Instead            | Why                                                               |
| ------------------------- | ---------------------------- | ---------------------- | ----------------------------------------------------------------- |
| Page caching              | PHP-based cache plugin       | Nginx FastCGI cache    | Serves static HTML without invoking PHP at all                    |
| Image compression         | ImageMagick scripts          | Smush plugin           | Handles lossy/lossless, lazy load, bulk optimize                  |
| Photo gallery             | Custom lightbox JS           | FooGallery plugin      | Responsive, lazy-loaded, accessibility, lightbox built-in         |
| SEO / sitemaps            | Manual meta tags             | Rank Math plugin       | Schema, sitemaps, redirect manager, breadcrumbs                   |
| Security scanning         | Custom fail2ban rules for WP | Wordfence plugin       | WAF, login limiting, malware scan, IP blocking                    |
| Video embeds              | Manual iframe/embed          | Embed Plus for YouTube | Lazy-loading, responsive, GDPR-friendly, schema markup            |
| Backups                   | Custom cron + mysqldump      | UpdraftPlus            | Scheduled, encrypted, Google Drive integration, one-click restore |
| HEIC conversion on server | ImageMagick 7+ with libheif  | Local `sips` command   | Server-side HEIC support is fragile and version-dependent         |

**Key insight:** Every "simple" WordPress feature (gallery, caching, SEO, security) has edge cases that mature plugins handle. The plugin ecosystem exists specifically because these problems are deceptively complex.

## Common Pitfalls

### Pitfall 1: VPS Left Unsecured After Provisioning

**What goes wrong:** Bots scan new DigitalOcean IPs within hours. Unsecured droplets get compromised within days.
**Why it happens:** Eager to install WordPress before hardening the server.
**How to avoid:** Security hardening is the FIRST step after droplet creation, BEFORE installing any web software.
**Warning signs:** Failed SSH login attempts in `/var/log/auth.log`, unknown processes, modified files.

### Pitfall 2: Theme Customizations Lost on Update

**What goes wrong:** Editing `churchwp/header.php` directly -- changes overwritten on next theme update.
**Why it happens:** Easier to edit parent theme files than set up child theme properly.
**How to avoid:** Create child theme FIRST. Only override `header.php` and `footer.php` from parent. Use Theme Panel for everything possible.
**Warning signs:** Modified files in `wp-content/themes/churchwp/` (parent directory).

### Pitfall 3: HEIC Images Fail to Upload

**What goes wrong:** WordPress rejects HEIC uploads or images display as broken.
**Why it happens:** Server-side HEIC support requires ImageMagick 7.0.8-26+ with libheif -- most servers lack this.
**How to avoid:** Batch convert ALL HEIC to JPEG locally before upload using macOS `sips`.
**Warning signs:** Upload errors mentioning "file type not allowed" or broken image icons.

### Pitfall 4: Mixed Content After Migration

**What goes wrong:** Browser shows "not secure" warning, some assets blocked, padlock missing.
**Why it happens:** Content imported with `http://` URLs or hardcoded HTTP paths in theme/content.
**How to avoid:** Install WordPress with HTTPS from day one (or IP without SSL initially, then switch cleanly). Run `wp search-replace` after any URL change.
**Warning signs:** Browser console showing mixed content warnings.

### Pitfall 5: Let's Encrypt Requires a Domain (Not IP)

**What goes wrong:** `certbot` fails because Let's Encrypt does not issue certificates for bare IP addresses.
**Why it happens:** Decision to skip domain means SSL is not possible initially.
**How to avoid:** This is expected. Run WordPress over HTTP on the VPS IP initially. When domain is ready: add DNS A record, run `certbot --nginx -d yourdomain.com`, then `wp search-replace 'http://VPS_IP' 'https://yourdomain.com'`.
**Warning signs:** Certbot error "No names were found in your configuration files."

### Pitfall 6: PHP-FPM OOM on 1GB VPS

**What goes wrong:** Server becomes unresponsive, MariaDB or PHP-FPM killed by OOM.
**Why it happens:** Default PHP-FPM `pm = dynamic` spawns too many workers for 1GB RAM.
**How to avoid:** Use `pm = ondemand`, `pm.max_children = 5`, `pm.process_idle_timeout = 10s`, `pm.max_requests = 500`.
**Warning signs:** `dmesg | grep -i oom`, high swap usage, slow responses.

## Code Examples

### HEIC Batch Conversion (macOS sips)

```bash
#!/bin/bash
# convert-heic.sh -- Run locally on macOS before uploading to WordPress
# Source: macOS sips command (built-in)

INPUT_DIR="$1"
OUTPUT_DIR="${2:-./converted}"
mkdir -p "$OUTPUT_DIR"

for f in "$INPUT_DIR"/*.{HEIC,heic}; do
  [ -f "$f" ] || continue
  basename=$(basename "$f")
  outname="${basename%.*}.jpg"
  echo "Converting: $basename -> $outname"
  sips -s format jpeg "$f" --out "$OUTPUT_DIR/$outname"
done

echo "Conversion complete. Files in $OUTPUT_DIR"
```

### VPS Security Hardening Commands

```bash
# Source: SpinupWP guide + DigitalOcean security tutorials

# 1. Create deploy user
adduser deploy
usermod -aG sudo deploy

# 2. Copy SSH key to deploy user
mkdir -p /home/deploy/.ssh
cp /root/.ssh/authorized_keys /home/deploy/.ssh/
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys

# 3. Disable root login and password auth
sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh.service

# 4. UFW Firewall
apt install ufw -y
ufw allow ssh
ufw allow http
ufw allow https
ufw enable

# 5. fail2ban
apt install fail2ban -y
systemctl enable --now fail2ban.service
```

### MariaDB WordPress Database Setup

```bash
# Source: MariaDB official docs + WordPress Codex
sudo mysql_secure_installation

sudo mysql -u root <<EOF
CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';
FLUSH PRIVILEGES;
EOF
```

### WordPress Download and Install via WP-CLI

```bash
# Source: WP-CLI official docs (developer.wordpress.org/cli/commands/)

# On VPS, as deploy user
cd /home/deploy/ambo-thoughts/public

# Download WordPress core
wp core download

# Create wp-config.php
wp config create \
  --dbname=wordpress \
  --dbuser=wpuser \
  --dbpass='STRONG_PASSWORD_HERE' \
  --dbhost=localhost \
  --extra-php <<PHP
define( 'DISALLOW_FILE_EDIT', true );
define( 'WP_POST_REVISIONS', 5 );
define( 'FS_METHOD', 'direct' );
PHP

# Install WordPress (use IP initially, no SSL)
wp core install \
  --url="http://YOUR_VPS_IP" \
  --title="Ambo Thoughts" \
  --admin_user=admin \
  --admin_password='STRONG_ADMIN_PASSWORD' \
  --admin_email='your@email.com'

# Set permalink structure
wp rewrite structure '/%postname%/' --hard

# Delete default content
wp post delete 1 --force  # "Hello World"
wp post delete 2 --force  # Sample page
```

### Nginx Server Block for WordPress (No SSL / IP-only)

```nginx
# /etc/nginx/sites-available/ambo-thoughts
# Source: SpinupWP guide, adapted for IP-only (no SSL)

# FastCGI cache path (OUTSIDE server block)
fastcgi_cache_path /home/deploy/ambo-thoughts/cache levels=1:2 keys_zone=ambo:100m inactive=60m;

server {
    listen 80;
    listen [::]:80;
    server_name _;  # Accept any -- IP-based, no domain yet

    root /home/deploy/ambo-thoughts/public;
    index index.php;

    client_max_body_size 64m;

    # FastCGI cache bypass rules
    set $skip_cache 0;
    if ($request_method = POST) { set $skip_cache 1; }
    if ($query_string != "") { set $skip_cache 1; }
    if ($request_uri ~* "/wp-admin/|/wp-json/|/xmlrpc.php|wp-.*.php|/feed/|index.php|sitemap(_index)?.xml") {
        set $skip_cache 1;
    }
    if ($http_cookie ~* "comment_author|wordpress_[a-f0-9]+|wp-postpass|wordpress_no_cache|wordpress_logged_in") {
        set $skip_cache 1;
    }

    add_header Fastcgi-Cache $upstream_cache_status;

    # WordPress permalinks
    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    # PHP handling with FastCGI cache
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
        fastcgi_index index.php;
        include fastcgi.conf;

        fastcgi_cache ambo;
        fastcgi_cache_bypass $skip_cache;
        fastcgi_no_cache $skip_cache;
        fastcgi_cache_valid 200 60m;
    }

    # Block xmlrpc.php
    location = /xmlrpc.php { deny all; }

    # Static file caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|webp|woff|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Deny access to sensitive files
    location ~ /\.ht { deny all; }
    location ~ /wp-config.php { deny all; }

    # Old URL redirects (GitHub Pages .html URLs)
    location ~ ^/(.+)\.html$ {
        return 301 /$1/;
    }
}
```

### PHP-FPM Pool Configuration (1GB VPS)

```ini
; /etc/php/8.3/fpm/pool.d/www.conf (key settings)
; Source: PHP.net manual + WordPress VPS guides

[www]
user = deploy
group = deploy
listen = /run/php/php8.3-fpm.sock
listen.owner = www-data
listen.group = www-data

pm = ondemand
pm.max_children = 5
pm.process_idle_timeout = 10s
pm.max_requests = 500

php_admin_value[memory_limit] = 256M
php_admin_value[upload_max_filesize] = 64M
php_admin_value[post_max_size] = 64M
php_admin_value[max_execution_time] = 300
```

### Nginx Global Config Additions

```nginx
# Add to /etc/nginx/nginx.conf inside http {} block
# Source: SpinupWP guide

# FastCGI cache key
fastcgi_cache_key "$scheme$request_method$http_host$request_uri";

# Gzip compression
gzip on;
gzip_proxied any;
gzip_comp_level 5;
gzip_types text/plain text/css application/json application/javascript
           text/xml application/xml application/xml+rss text/javascript;

server_tokens off;
client_max_body_size 64m;
```

### WP-CLI Content Migration Script

```bash
#!/bin/bash
# migrate-content.sh -- Run in Local by Flywheel Site Shell or on VPS
# Source: WP-CLI official docs (developer.wordpress.org/cli/commands/)

# Create pages from content files
wp post create ./content/about.html \
  --post_type=page --post_title='About' --post_status=publish

wp post create ./content/spirituality.html \
  --post_type=page --post_title='Spirituality' --post_status=publish

wp post create ./content/church-news.html \
  --post_type=page --post_title='Church News' --post_status=publish

wp post create ./content/contact.html \
  --post_type=page --post_title='Contact' --post_status=publish

wp post create ./content/pictures.html \
  --post_type=page --post_title='Pictures' --post_status=publish

wp post create ./content/prayer-partner.html \
  --post_type=page --post_title='Prayer Partner' --post_status=publish

wp post create ./content/stuff.html \
  --post_type=page --post_title='Stuff' --post_status=publish

wp post create ./content/videos.html \
  --post_type=page --post_title='Videos' --post_status=publish

# Create blog posts
wp post create ./content/posts/holy-thursday.html \
  --post_type=post --post_title='Holy Thursday: A Night of Service' --post_status=publish

wp post create ./content/posts/good-samaritan.html \
  --post_type=post --post_title='The Good Samaritan in Our Time' --post_status=publish

# Import media (images from repo)
wp media import ./images/deacons-cross.png --title="Deacon's Cross Logo"
wp media import ./images/deacon-henry.jpg --title="Deacon Henry Cugini"
wp media import ./images/deacon-henry-hero.jpg --title="Deacon Henry Hero"
wp media import ./images/ambo-hero.jpg --title="Ambo Hero"
wp media import ./images/hero/*.jpg --title="Hero Slider Image"
wp media import ./images/blog/*.jpg --title="Blog Image"
wp media import ./images/church-bg.jpg --title="Church Background"
# Import converted HEIC images
wp media import ./converted/*.jpg --title="Gallery Photo"

# Create navigation menu
wp menu create "Main Menu"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=about --field=ID) --title="About"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=spirituality --field=ID) --title="Spirituality"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=church-news --field=ID) --title="Church News"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=stuff --field=ID) --title="Stuff"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=prayer-partner --field=ID) --title="Prayer Partner"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=contact --field=ID) --title="Contact"
wp menu item add-custom "Main Menu" "Home" "/"
wp menu item add-post "Main Menu" $(wp post list --post_type=page --name=videos --field=ID) --title="Homilies"

# Assign menu to primary location
wp menu location assign "Main Menu" primary

# Set homepage to static page (if using static front page)
wp option update show_on_front 'page'
wp option update page_on_front $(wp post list --post_type=page --pagename=home --field=ID 2>/dev/null || echo "")
```

### Child Theme Setup

```css
/* wp-content/themes/churchwp-child/style.css */
/*
Theme Name:   ChurchWP Child
Theme URI:    https://ambothoughts.com
Description:  Ambo Thoughts child theme for ChurchWP
Author:       Sameer Rijhsinghani
Template:     churchwp
Version:      1.0.0
*/

/* Navy & Gold Color Overrides */
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

```php
<?php
// wp-content/themes/churchwp-child/functions.php

// Enqueue parent theme styles
add_action( 'wp_enqueue_scripts', 'churchwp_child_enqueue_styles' );
function churchwp_child_enqueue_styles() {
    wp_enqueue_style(
        'churchwp-parent-style',
        get_parent_theme_file_uri( 'style.css' ),
        array(),
        wp_get_theme()->parent()->get( 'Version' )
    );
    wp_enqueue_style(
        'churchwp-child-style',
        get_stylesheet_uri(),
        array( 'churchwp-parent-style' ),
        wp_get_theme()->get( 'Version' )
    );
}
```

### Revolution Slider Customization

```
Steps to customize the hero slider (done via WordPress admin GUI):

1. After demo import, go to Slider Revolution in admin sidebar
2. The "main_home_slider" should already be imported from demo data
3. Click to edit the slider
4. For each slide:
   a. Click the slide to select it
   b. Change background image: Slide Options > Background > Image
      - Slide 1: upload hero/hero-1.jpg
      - Slide 2: upload hero/picture2.jpg
      - Slide 3: upload hero/picture3.jpg
   c. Edit text layers (click text to select, edit in layer panel):
      - Slide 1: "Ambo Thoughts" (H1), "Spirituality" + "Bereavement" (subtitles)
      - Slide 2: "Preach the Gospel at all times; use words when necessary."
                  "-- St. Francis of Assisi"
      - Slide 3: "Be still, and know that I am God"
                  "-- Psalm 46:10"
5. Delete any slides beyond 3 (demo may have more)
6. Save slider

Note: Revolution Slider is a visual editor -- this step cannot be automated via WP-CLI.
It must be done through the WordPress admin GUI.
```

### File Permissions (Production)

```bash
# Source: WordPress Codex + hardening guides
# Run as root on VPS

# Set ownership
chown -R deploy:www-data /home/deploy/ambo-thoughts/public

# Directories: 755, Files: 644
find /home/deploy/ambo-thoughts/public -type d -exec chmod 755 {} \;
find /home/deploy/ambo-thoughts/public -type f -exec chmod 644 {} \;

# wp-config.php: 600 (owner read/write only)
chmod 600 /home/deploy/ambo-thoughts/public/wp-config.php

# uploads writable by web server
chmod -R 775 /home/deploy/ambo-thoughts/public/wp-content/uploads
```

### Redis Setup

```bash
# Source: SpinupWP caching guide

# Install (Ubuntu 24.04 may use valkey as Redis replacement)
sudo apt install redis-server -y
# OR if valkey is available:
# sudo apt install valkey-server valkey-redis-compat -y

sudo systemctl enable --now redis-server.service

# Verify
redis-cli ping  # Should return PONG

# In WordPress admin: install "Redis Object Cache" plugin by Till Kruss
# Settings > Redis > Enable Object Cache

# Add to wp-config.php (before "That's all, stop editing!")
define( 'WP_REDIS_HOST', '127.0.0.1' );
define( 'WP_REDIS_PORT', 6379 );
```

## State of the Art

| Old Approach          | Current Approach              | When Changed       | Impact                                                   |
| --------------------- | ----------------------------- | ------------------ | -------------------------------------------------------- |
| MySQL 5.7             | MariaDB 10.11 LTS / MySQL 8.x | 2023+              | MariaDB in Ubuntu 24.04 default repos                    |
| PHP 7.4/8.0           | PHP 8.3 (8.4 available)       | 2024               | WordPress 6.4+ requires PHP 7.4 minimum, recommends 8.1+ |
| WP Super Cache        | Nginx FastCGI cache           | Always been better | Server-level caching, no PHP invocation                  |
| Yoast SEO             | Rank Math                     | 2020+              | Rank Math free tier more capable than Yoast free         |
| Sermon Manager plugin | Custom Post Type              | Dec 2025           | Sermon Manager closed/abandoned on WordPress.org         |
| Password SSH auth     | SSH key + ed25519             | Current standard   | Stronger than RSA, shorter keys                          |
| Let's Encrypt manual  | Certbot with auto-renewal     | Standard           | Certbot handles nginx config + renewal cron              |

**Deprecated/outdated:**

- Sermon Manager WordPress plugin: closed on WordPress.org Dec 2025
- WP Super Cache on Nginx: redundant when FastCGI cache is configured
- PHP 7.x: End of life, security risk

## Open Questions

1. **ChurchWP Theme Panel exact options**
   - What we know: Theme Panel has Styling, Header, Footer, General sections
   - What's unclear: Exact color pickers, which elements can be styled via panel vs CSS
   - Recommendation: Explore after installing demo data. Use Theme Panel first, CSS overrides second.

2. **ChurchWP bundled plugin versions vs PHP 8.3 compatibility**
   - What we know: ChurchWP bundles WPBakery, Revolution Slider, ThemeSLR Framework
   - What's unclear: Exact versions and PHP 8.3 compatibility
   - Recommendation: Test in Local by Flywheel first (PHP 8.3 environment). If incompatible, try PHP 8.2 as fallback.

3. **Homepage structure after demo import**
   - What we know: Demo import creates sample pages including homepage with sections
   - What's unclear: Whether homepage uses WPBakery page builder or theme-specific template
   - Recommendation: After demo import, inspect the homepage in WPBakery editor to understand the section structure before modifying.

4. **WPBakery vs Classic Editor for content pages**
   - What we know: ChurchWP bundles WPBakery, some pages may use WPBakery shortcodes
   - What's unclear: Whether migrated content should use WPBakery layouts or classic editor
   - Recommendation: Use WPBakery for the homepage (complex layout), classic editor or simple WPBakery for inner pages (About, Spirituality, etc.)

## Validation Architecture

### Test Framework

| Property           | Value                                                           |
| ------------------ | --------------------------------------------------------------- |
| Framework          | Manual validation (WordPress site, no automated test framework) |
| Config file        | N/A -- WordPress CMS, not a code project                        |
| Quick run command  | `curl -sI http://VPS_IP \| head -5`                             |
| Full suite command | Manual checklist (see below)                                    |

### Phase Requirements to Test Map

| Req ID          | Behavior                   | Test Type   | Automated Command                                                                                                                      | File Exists? |
| --------------- | -------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| HOSTING-001     | VPS accessible via SSH     | smoke       | `ssh deploy@VPS_IP 'echo OK'`                                                                                                          | N/A          |
| HOSTING-002     | Nginx + PHP-FPM running    | smoke       | `curl -sI http://VPS_IP \| grep nginx`                                                                                                 | N/A          |
| HOSTING-003     | SSH password auth disabled | smoke       | `ssh -o PasswordAuthentication=yes deploy@VPS_IP 2>&1 \| grep denied`                                                                  | N/A          |
| HOSTING-006     | FastCGI cache active       | smoke       | `curl -sI http://VPS_IP \| grep Fastcgi-Cache`                                                                                         | N/A          |
| HOSTING-007     | Redis connected            | smoke       | `ssh deploy@VPS_IP 'redis-cli ping'`                                                                                                   | N/A          |
| THEME-001       | ChurchWP active            | smoke       | `wp theme status churchwp-child` (via SSH)                                                                                             | N/A          |
| DESIGN-003      | Hero slider renders        | manual-only | Visual check -- 3 slides cycle                                                                                                         | N/A          |
| CONTENT-001-008 | All pages exist            | smoke       | `for p in about spirituality church-news contact pictures prayer-partner stuff videos; do curl -sI http://VPS_IP/$p/ \| head -1; done` | N/A          |
| MIGRATION-001   | .html redirects work       | smoke       | `curl -sI http://VPS_IP/about.html \| grep 301`                                                                                        | N/A          |

### Sampling Rate

- **Per task commit:** Visual check in Local by Flywheel browser
- **Per wave merge:** Run smoke test commands against VPS
- **Phase gate:** Full manual checklist from ROADMAP.md success criteria

### Wave 0 Gaps

- [ ] `scripts/smoke-test.sh` -- curl-based validation of all pages and redirects
- [ ] No automated test framework needed -- this is a WordPress content site, not a code project

## Sources

### Primary (HIGH confidence)

- [SpinupWP - VPS Setup](https://spinupwp.com/hosting-wordpress-setup-secure-virtual-server/) - SSH hardening, UFW, fail2ban commands
- [SpinupWP - Nginx/PHP/MySQL Install](https://spinupwp.com/hosting-wordpress-yourself-nginx-php-mysql/) - LEMP stack install commands for Ubuntu 24.04
- [SpinupWP - Caching Configuration](https://spinupwp.com/hosting-wordpress-yourself-server-monitoring-caching/) - Redis + FastCGI cache config
- [SpinupWP - Nginx WordPress Config](https://spinupwp.com/hosting-wordpress-yourself-setting-up-sites/) - Full Nginx server block with SSL
- [WP-CLI Official Docs](https://developer.wordpress.org/cli/commands/) - post create, media import, menu commands
- [WordPress Child Themes Handbook](https://developer.wordpress.org/themes/advanced-topics/child-themes/) - Child theme setup pattern
- [DigitalOcean LEMP Tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-wordpress-with-lemp-on-ubuntu) - WordPress LEMP on Ubuntu
- [Slider Revolution Manual](https://www.sliderrevolution.com/manual/importing-slides-from-templates-and-other-modules/) - Import and customize slides
- [Local by Flywheel Install Docs](https://localwp.com/help-docs/getting-started/installing-local/) - macOS installation

### Secondary (MEDIUM confidence)

- [ChurchWP ThemeForest Page](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148) - Feature list and bundled plugins
- [ChurchWP Documentation](http://themeslr.com/docs/churchwp/) - Theme Panel options, demo import, plugin list
- [Linode FastCGI Cache Guide](https://www.linode.com/docs/guides/how-to-use-nginx-fastcgi-page-cache-with-wordpress/) - Alternative FastCGI reference

### Tertiary (LOW confidence)

- ChurchWP exact Theme Panel color pickers -- need to verify after purchase/install
- Bundled plugin PHP 8.3 compatibility -- need to test in Local by Flywheel

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH - Every component is industry-standard WordPress VPS hosting
- Architecture: HIGH - Child theme + WP-CLI + rsync is the standard WordPress development pattern
- Pitfalls: HIGH - All pitfalls are well-documented WordPress operational issues
- ChurchWP specifics: MEDIUM - Demo import process and Theme Panel options need verification after purchase

**Research date:** 2026-03-07
**Valid until:** 2026-04-07 (stable -- WordPress VPS patterns don't change quickly)
