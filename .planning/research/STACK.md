# Technology Stack

**Project:** Ambo Thoughts WordPress Redesign
**Researched:** 2026-03-07

## Recommended Stack

### VPS Provider

| Technology   | Tier                                      | Purpose            | Why                                                                                                                                                                                         |
| ------------ | ----------------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DigitalOcean | $6/mo Droplet (1 vCPU, 1GB RAM, 25GB SSD) | Production hosting | 1-click WordPress image, better docs/tutorials than Linode, NYC datacenter (low latency for NJ), $4/mo for managed backups. Upgrade to $12/mo (2GB) if Redis + WordPress gets tight on RAM. |

**Alternative:** Linode (Akamai) offers identical specs at $5/mo with slightly more bandwidth. Either works. DigitalOcean wins on WordPress-specific documentation and 1-click apps.

**Confidence:** HIGH -- both providers are well-established; pricing verified from official sites.

### Web Server

| Technology | Version                   | Purpose                    | Why                                                                                                              |
| ---------- | ------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Nginx      | 1.24+ (Ubuntu 24.04 repo) | Reverse proxy + web server | 170% faster than Apache for static files, 40% less RAM, built-in FastCGI cache. For a 1GB VPS, every MB matters. |

**Not Apache.** Apache with mod_rewrite is the WordPress default, but Nginx + PHP-FPM is the modern standard for VPS hosting. WordPress `.htaccess` rules don't apply to Nginx, but the `try_files` directive replaces them trivially.

**Confidence:** HIGH -- nginx dominance for WordPress VPS is well-documented across multiple benchmarks.

### PHP

| Technology | Version                  | Purpose           | Why                                                                                                                                            |
| ---------- | ------------------------ | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| PHP-FPM    | 8.3 (via ppa:ondrej/php) | WordPress runtime | WordPress officially recommends PHP 8.3. ChurchWP theme confirms PHP 8.x compatibility. PHP 8.3 brings 5-15% performance improvement over 8.1. |

**Key PHP extensions required:**

```bash
sudo apt install php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd \
  php8.3-mbstring php8.3-xml php8.3-zip php8.3-intl php8.3-imagick \
  php8.3-redis php8.3-opcache
```

**Confidence:** HIGH -- verified against WordPress.org/about/requirements/ (recommends 8.3+).

### Database

| Technology | Version                          | Purpose            | Why                                                                                                                                                                                                                |
| ---------- | -------------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| MariaDB    | 10.11 LTS (Ubuntu 24.04 default) | WordPress database | WordPress officially supports MariaDB 10.6+. MariaDB uses less RAM than MySQL 8, has faster reads for WordPress's read-heavy workload, and is the default on Ubuntu/Debian. No reason to install MySQL separately. |

**Confidence:** HIGH -- WordPress.org officially lists MariaDB 10.6+ as supported. MariaDB 10.11 is the current LTS.

### SSL

| Technology              | Purpose               | Why                                                          |
| ----------------------- | --------------------- | ------------------------------------------------------------ |
| Certbot + Let's Encrypt | Free SSL certificates | Industry standard, auto-renews via systemd timer. Zero cost. |

**Setup command:**

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d ambothoughts.com -d www.ambothoughts.com
```

Certbot automatically installs a systemd timer (`/etc/systemd/system/snap.certbot.renew.timer`) or cron job (`/etc/cron.d/certbot`) that runs twice daily. Certificates renew when within 30 days of expiry (90-day cert lifetime).

**Verify auto-renewal works:**

```bash
sudo certbot renew --dry-run
```

**Confidence:** HIGH -- standard practice, well-documented.

### Caching (Two Layers)

| Technology          | Purpose         | RAM Budget      | Why                                                                                                                                 |
| ------------------- | --------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Nginx FastCGI Cache | Full-page cache | ~0 (disk-based) | Serves cached HTML directly from Nginx without hitting PHP at all. Sub-millisecond response for cached pages. Free in terms of RAM. |
| Redis               | Object cache    | 64-128MB        | Caches database queries, reducing MariaDB load. Install `Redis Object Cache` plugin by Till Kruss.                                  |

**FastCGI cache config snippet** (add to nginx.conf):

```nginx
# Define cache zone (outside server block)
fastcgi_cache_path /var/cache/nginx levels=1:2 keys_zone=WORDPRESS:10m
                   max_size=500m inactive=60m use_temp_path=off;

# Inside server block
set $skip_cache 0;
if ($request_method = POST) { set $skip_cache 1; }
if ($query_string != "") { set $skip_cache 1; }
if ($request_uri ~* "/wp-admin/|/xmlrpc.php|wp-.*.php|/feed/") { set $skip_cache 1; }
if ($http_cookie ~* "comment_author|wordpress_[a-f0-9]+|wp-postpass|wordpress_logged_in") { set $skip_cache 1; }

fastcgi_cache WORDPRESS;
fastcgi_cache_valid 200 60m;
fastcgi_cache_bypass $skip_cache;
fastcgi_no_cache $skip_cache;
add_header X-FastCGI-Cache $upstream_cache_status;
```

**Why not WP Super Cache or W3 Total Cache?** Nginx FastCGI cache operates at the web server level -- PHP never executes for cached requests. Plugin-based page caches still invoke PHP to serve the cached file. On a 1GB VPS, skipping PHP entirely is a significant win.

**Redis config** (`/etc/redis/redis.conf`):

```
maxmemory 64mb
maxmemory-policy allkeys-lru
```

**Confidence:** HIGH -- this is the standard performant WordPress VPS caching stack, well-documented by SpinupWP, RunCloud, and others.

### PHP-FPM Tuning (1GB VPS)

**Configuration** (`/etc/php/8.3/fpm/pool.d/www.conf`):

```ini
; Use ondemand for low-traffic church site -- spawns workers only when needed
pm = ondemand
pm.max_children = 5
pm.process_idle_timeout = 10s
pm.max_requests = 500

; Memory limit per process
php_admin_value[memory_limit] = 128M
```

**RAM budget breakdown (1GB VPS):**
| Component | RAM |
|-----------|-----|
| OS + Nginx | ~150MB |
| MariaDB | ~200MB |
| Redis | ~64MB |
| PHP-FPM (5 workers x 40-60MB avg) | ~250MB |
| Buffer | ~360MB |

**Formula:** `pm.max_children = (Available RAM for PHP) / (Avg worker size)`. With ~400MB available for PHP and ~60MB per WordPress worker: `400/60 = ~6`. Use 5 for safety margin.

**If upgrading to 2GB VPS:** Increase `pm.max_children` to 10, switch `pm = dynamic` with `pm.start_servers = 2`, `pm.min_spare_servers = 1`, `pm.max_spare_servers = 3`.

**OPcache settings** (`/etc/php/8.3/fpm/conf.d/10-opcache.ini`):

```ini
opcache.enable=1
opcache.memory_consumption=128
opcache.interned_strings_buffer=16
opcache.max_accelerated_files=10000
opcache.revalidate_freq=60
opcache.save_comments=1
```

**Confidence:** HIGH -- formula and recommendations verified across multiple hosting guides.

### Local Development

| Technology        | Purpose                         | Why                                                                                                                                                                               |
| ----------------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Local by Flywheel | Local WordPress dev environment | GUI-based, one-click site creation, built-in WP-CLI and SSH, uses Docker containers under the hood. Perfect for a solo developer working on a single WordPress site. Zero config. |

**Not Docker/wp-env.** Docker compose gives more control but requires writing and maintaining docker-compose.yml, understanding volumes, networking. For a church website redesign (not plugin/theme development), Local by Flywheel is the right tool -- spin up a site in 30 seconds, import/export with one click.

**Local by Flywheel setup:**

1. Download from https://localwp.com/
2. Create new site: "Ambo Thoughts"
3. Choose "Custom" environment: PHP 8.3, Nginx, MariaDB
4. Match production stack exactly

**Confidence:** HIGH -- Local by Flywheel is the most recommended tool for solo WordPress development.

### Deployment Pipeline

**Architecture:** Local (Flywheel) --> GitHub repo --> Production VPS (via rsync over SSH)

No staging server needed for a low-traffic church site. Use Local by Flywheel as the staging environment.

**What goes in Git:**

```
wp-content/
  themes/churchwp-child/    # Child theme customizations
  mu-plugins/               # Must-use plugins (if any custom code)
  uploads/.gitkeep          # Track structure, not media files
scripts/
  deploy.sh                 # Deployment script
  backup.sh                 # Backup script
.gitignore                  # Ignore wp-core, uploads, wp-config.php
```

**Deployment script** (`scripts/deploy.sh`):

```bash
#!/bin/bash
set -euo pipefail

VPS_USER="deploy"
VPS_HOST="your-vps-ip"
WP_PATH="/var/www/ambothoughts"

# Sync child theme
rsync -avz --delete \
  wp-content/themes/churchwp-child/ \
  ${VPS_USER}@${VPS_HOST}:${WP_PATH}/wp-content/themes/churchwp-child/

# Clear caches on production
ssh ${VPS_USER}@${VPS_HOST} "
  cd ${WP_PATH} && \
  wp cache flush && \
  sudo rm -rf /var/cache/nginx/* && \
  sudo systemctl reload nginx
"

echo "Deployed successfully."
```

**Database sync (production --> local for content updates):**

```bash
# Export from production
ssh deploy@vps "cd /var/www/ambothoughts && wp db export - | gzip" > db-backup.sql.gz

# Import to Local by Flywheel
gunzip -c db-backup.sql.gz | wp db import -
wp search-replace 'https://ambothoughts.com' 'http://ambothoughts.local'
```

**WP-CLI** is pre-installed in Local by Flywheel and should be installed on the VPS:

```bash
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp
```

**Confidence:** MEDIUM -- this is a standard approach but specifics depend on the final domain name and VPS IP.

### ChurchWP Theme

| Item                    | Detail                                                |
| ----------------------- | ----------------------------------------------------- |
| Source                  | ThemeForest (~$59 one-time)                           |
| Developer               | ThemeSLR                                              |
| PHP Compatibility       | PHP 8.x confirmed                                     |
| WordPress Compatibility | 6.x+                                                  |
| Bundled plugins         | Visual Composer (WPBakery), Slider Revolution, others |
| Child theme             | Required -- never edit the parent theme directly      |

**Child theme approach:** Create `churchwp-child/` with `style.css` (Template: churchwp) and `functions.php`. All Navy/Gold color overrides, custom header, menu changes go in the child theme. This ensures ChurchWP updates don't wipe customizations.

**Confidence:** MEDIUM -- PHP 8.x compatibility confirmed from ThemeForest listing, but exact bundled plugin versions need verification after purchase.

## Full Server Setup Sequence

```bash
# 1. Create DigitalOcean Droplet: Ubuntu 24.04 LTS, 1GB RAM, NYC region
# 2. SSH in and run:

# System updates
sudo apt update && sudo apt upgrade -y

# Install Nginx
sudo apt install nginx -y

# Install PHP 8.3
sudo add-apt-repository ppa:ondrej/php -y
sudo apt install php8.3-fpm php8.3-mysql php8.3-curl php8.3-gd \
  php8.3-mbstring php8.3-xml php8.3-zip php8.3-intl php8.3-imagick \
  php8.3-redis php8.3-opcache -y

# Install MariaDB
sudo apt install mariadb-server -y
sudo mysql_secure_installation

# Install Redis
sudo apt install redis-server -y

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Install WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp

# Create WordPress database
sudo mysql -e "CREATE DATABASE wordpress_ambo;"
sudo mysql -e "CREATE USER 'wp_ambo'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';"
sudo mysql -e "GRANT ALL ON wordpress_ambo.* TO 'wp_ambo'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Download WordPress
cd /var/www
sudo wp core download --path=ambothoughts --allow-root
sudo chown -R www-data:www-data ambothoughts
```

## Alternatives Considered

| Category     | Recommended       | Alternative                  | Why Not                                                                                        |
| ------------ | ----------------- | ---------------------------- | ---------------------------------------------------------------------------------------------- |
| Web server   | Nginx             | Apache                       | Higher RAM usage, slower static file serving, overkill .htaccess flexibility not needed        |
| Database     | MariaDB 10.11     | MySQL 8.0                    | MySQL uses more RAM, MariaDB is Ubuntu default, WordPress supports both equally                |
| PHP version  | 8.3               | 8.2                          | 8.3 is WordPress-recommended, better performance, 8.2 still works but why not latest           |
| Page cache   | Nginx FastCGI     | WP Super Cache plugin        | Plugin-based caches still invoke PHP; FastCGI serves from Nginx directly                       |
| Object cache | Redis             | Memcached                    | Redis persists across restarts, supports more data structures, better WordPress plugin support |
| Local dev    | Local by Flywheel | Docker/wp-env                | Overkill for single-site church project; Local has GUI, one-click import/export                |
| VPS provider | DigitalOcean      | Linode (Akamai)              | Nearly identical; DO has better WordPress docs and 1-click marketplace                         |
| Hosting type | Self-managed VPS  | Managed WP (Flywheel/Kinsta) | $15-30/mo vs $6/mo; overkill for low-traffic church site                                       |

## Monthly Cost Estimate

| Item                                 | Cost              |
| ------------------------------------ | ----------------- |
| DigitalOcean Droplet (1GB)           | $6/mo             |
| DigitalOcean Backups                 | $1.20/mo          |
| Domain (ambothoughts.com or similar) | ~$12/year ($1/mo) |
| SSL (Let's Encrypt)                  | Free              |
| ChurchWP theme                       | $59 one-time      |
| **Total ongoing**                    | **~$8.20/mo**     |

## Sources

- [WordPress Official Requirements](https://wordpress.org/about/requirements/) -- PHP 8.3+, MariaDB 10.6+ or MySQL 8.0+
- [Nginx vs Apache WordPress Benchmarks 2025](https://www.quape.com/best-web-server-wordpress-2025/) -- Nginx 170% faster
- [PHP-FPM Tuning for WordPress](https://www.dchost.com/blog/en/php-fpm-settings-for-wordpress-and-woocommerce-pm-pm-max_children-and-pm-max_requests/) -- pm.max_children formula
- [SpinupWP: Redis + FastCGI Cache Setup](https://spinupwp.com/hosting-wordpress-yourself-server-monitoring-caching/) -- Caching architecture
- [Let's Encrypt on Nginx 2025](https://wehaveservers.com/blog/linux-sysadmin/lets-encrypt-on-nginx-free-ssl-with-auto-renew-2025/) -- Certbot auto-renewal
- [Local by Flywheel](https://localwp.com/) -- Local WordPress development
- [ChurchWP ThemeForest Listing](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148) -- Theme compatibility
- [2026 VPS Battle: DO vs Linode vs Vultr](https://www.ssdnodes.com/blog/digitalocean-vs-linode-vs-vultr/) -- VPS comparison
- [WordPress Deployment with Git & CI/CD](https://www.dopethemes.com/how-to-automate-wordpress-deployment-with-git-ci-cd-pipelines/) -- Deployment patterns
