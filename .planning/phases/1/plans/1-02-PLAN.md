---
phase: 1-infrastructure-launch
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/setup-vps.sh
  - nginx/wordpress.conf
  - nginx/nginx-global.conf
autonomous: false
requirements:
  - REQ-HOSTING-001
  - REQ-HOSTING-002
  - REQ-HOSTING-003
  - REQ-HOSTING-004
  - REQ-HOSTING-006
  - REQ-HOSTING-007
  - REQ-HOSTING-008
  - REQ-HOSTING-009
  - REQ-MIGRATION-001
  - REQ-ADMIN-006

must_haves:
  truths:
    - "VPS is accessible via SSH with key-only auth (no root, no password)"
    - "Nginx serves a default page on the VPS IP over HTTP port 80"
    - "WordPress is installed and accessible at http://VPS_IP with wp-admin login working"
    - "UFW firewall blocks all ports except 80, 443, and SSH"
    - "fail2ban is running and monitoring SSH"
    - "Redis is running and accepting connections"
    - "PHP-FPM 8.3 is running with ondemand pool settings for 1GB VPS"
  artifacts:
    - path: "scripts/setup-vps.sh"
      provides: "VPS provisioning automation script"
    - path: "nginx/wordpress.conf"
      provides: "Nginx server block with FastCGI cache and URL redirects"
    - path: "/home/deploy/ambo-thoughts/public/"
      provides: "WordPress installation on VPS"
  key_links:
    - from: "Nginx"
      to: "PHP-FPM 8.3"
      via: "unix:/run/php/php8.3-fpm.sock"
    - from: "WordPress"
      to: "MariaDB"
      via: "wpuser@localhost/wordpress database"
    - from: "Nginx FastCGI cache"
      to: "PHP-FPM"
      via: "fastcgi_cache ambo zone"
---

<objective>
Provision and harden a DigitalOcean VPS with the full LEMP stack (Nginx, PHP-FPM 8.3, MariaDB, Redis) and install WordPress -- ready to receive the customized theme and content from the local development environment.

Purpose: This is the production infrastructure. Without it, the local WordPress work has nowhere to deploy. Security hardening MUST happen before WordPress install (bots scan new droplets within hours).

Output: A hardened VPS running WordPress at http://VPS_IP with Nginx FastCGI caching, Redis object caching, and all security measures in place.
</objective>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/RESEARCH.md
</context>

<tasks>

<task type="checkpoint:human-action" gate="blocking">
  <name>Task 1: Provision DigitalOcean droplet</name>
  <what-built>Nothing -- the user must create the droplet in their DigitalOcean account.</what-built>
  <how-to-verify>
    The user must create the droplet (requires DO account + billing):

    1. Log in to DigitalOcean (cloud.digitalocean.com)
    2. Create Droplet:
       - Region: closest to NJ (nyc1 or nyc3)
       - Image: Ubuntu 24.04 LTS
       - Size: Basic, Regular, $6/mo (1 vCPU, 1GB RAM, 25GB SSD)
       - Authentication: SSH Key (add your SSH public key)
       - Hostname: ambo-thoughts
    3. Note the droplet IP address
    4. Verify SSH access: `ssh root@YOUR_VPS_IP`

    Provide the VPS IP address when done.

  </how-to-verify>
  <resume-signal>Provide the VPS IP address, e.g. "done - IP is 123.45.67.89"</resume-signal>
</task>

<task type="auto">
  <name>Task 2: Harden VPS, install LEMP stack, and install WordPress</name>
  <files>
    scripts/setup-vps.sh
    nginx/wordpress.conf
    nginx/nginx-global.conf
  </files>
  <action>
    **Create `scripts/setup-vps.sh`** -- a comprehensive VPS setup script that the executor will run commands from via SSH. Also create the Nginx config files locally for reference and rsync.

    The script should be organized in sections and designed to be run section-by-section (not all at once) via SSH to the VPS. Each section should be clearly commented.

    **Section 1: Security Hardening (FIRST -- before anything else)**
    - Create `deploy` user with sudo access
    - Copy root's SSH authorized_keys to deploy user
    - Set correct permissions on .ssh (700) and authorized_keys (600)
    - Disable root login: `PermitRootLogin no` in /etc/ssh/sshd_config
    - Disable password auth: `PasswordAuthentication no`
    - Restart ssh.service
    - Install and enable UFW: allow ssh, http, https only
    - Install and enable fail2ban

    **Section 2: LEMP Stack Installation**
    - Add PPAs: `ppa:ondrej/nginx` and `ppa:ondrej/php`
    - `apt update && apt dist-upgrade -y`
    - Install: nginx, mariadb-server, redis-server
    - Install PHP 8.3 packages: php8.3-fpm php8.3-common php8.3-mysql php8.3-xml php8.3-intl php8.3-curl php8.3-gd php8.3-imagick php8.3-cli php8.3-mbstring php8.3-opcache php8.3-redis php8.3-soap php8.3-zip
    - Run `mysql_secure_installation`
    - Create WordPress database and user:
      ```
      CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
      CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
      GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';
      FLUSH PRIVILEGES;
      ```

    **Section 3: PHP-FPM Configuration for 1GB VPS**
    - Edit `/etc/php/8.3/fpm/pool.d/www.conf`:
      - `user = deploy`, `group = deploy`
      - `listen.owner = www-data`, `listen.group = www-data`
      - `pm = ondemand`
      - `pm.max_children = 5`
      - `pm.process_idle_timeout = 10s`
      - `pm.max_requests = 500`
      - `php_admin_value[memory_limit] = 256M`
      - `php_admin_value[upload_max_filesize] = 64M`
      - `php_admin_value[post_max_size] = 64M`
      - `php_admin_value[max_execution_time] = 300`
    - Restart php8.3-fpm

    **Section 4: Nginx Configuration**
    - Create `nginx/wordpress.conf` locally with the full server block from RESEARCH.md:
      - FastCGI cache path: `/home/deploy/ambo-thoughts/cache`
      - Root: `/home/deploy/ambo-thoughts/public`
      - FastCGI cache bypass rules for POST, query strings, wp-admin, logged-in cookies
      - Block xmlrpc.php
      - Static file caching (30d expiry)
      - Old .html URL redirects: `location ~ ^/(.+)\.html$ { return 301 /$1/; }`
      - Handle /ambo-thoughts/ subdirectory redirects from GitHub Pages
      - Deny access to .ht files and wp-config.php
    - Create `nginx/nginx-global.conf` with http {} additions:
      - `fastcgi_cache_key "$scheme$request_method$http_host$request_uri"`
      - gzip compression settings
      - `server_tokens off`
    - Deploy configs to VPS:
      - Copy wordpress.conf to `/etc/nginx/sites-available/ambo-thoughts`
      - Symlink to sites-enabled, remove default
      - Add global config additions to nginx.conf
      - `nginx -t` to test, then restart nginx

    **Section 5: WordPress Installation via WP-CLI**
    - Install WP-CLI on VPS:
      ```
      curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
      chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp
      ```
    - Create site directory: `mkdir -p /home/deploy/ambo-thoughts/public`
    - Set ownership: `chown -R deploy:deploy /home/deploy/ambo-thoughts`
    - As deploy user:
      ```
      cd /home/deploy/ambo-thoughts/public
      wp core download
      wp config create --dbname=wordpress --dbuser=wpuser --dbpass='PASSWORD' --dbhost=localhost \
        --extra-php <<'PHP'
      define('DISALLOW_FILE_EDIT', true);
      define('WP_POST_REVISIONS', 5);
      define('FS_METHOD', 'direct');
      PHP
      wp core install --url="http://VPS_IP" --title="Ambo Thoughts" \
        --admin_user=admin --admin_password='STRONG_ADMIN_PASSWORD' --admin_email='your@email.com'
      wp rewrite structure '/%postname%/' --hard
      ```
    - Set file permissions: directories 755, files 644, wp-config.php 600

    **Section 6: Redis Object Cache**
    - Verify redis-server is running: `systemctl status redis-server`
    - Install Redis Object Cache plugin via WP-CLI: `wp plugin install redis-cache --activate`
    - Enable Redis: `wp redis enable`

    **Section 7: Install Security and Utility Plugins**
    - `wp plugin install wordfence --activate` (REQ-HOSTING-008)
    - `wp plugin install updraftplus --activate` (REQ-HOSTING-005 -- configure backup destination later via admin)
    - `wp plugin install wordpress-seo-premium` -- NO, use Rank Math: `wp plugin install seo-by-rank-math --activate` (REQ-MIGRATION-002)
    - Do NOT install: Jetpack, Elementor, WP Super Cache, MonsterInsights, Yoast (REQ-ADMIN-006)

    **Section 8: Verify**
    - `curl -I http://VPS_IP` returns 200
    - `curl -I http://VPS_IP/wp-admin/` returns 302 (redirect to login)
    - `ssh deploy@VPS_IP "wp --path=/home/deploy/ambo-thoughts/public option get siteurl"` returns http://VPS_IP

  </action>
  <verify>
    - `ssh deploy@VPS_IP "systemctl is-active nginx php8.3-fpm mariadb redis-server"` -- all show "active"
    - `curl -s -o /dev/null -w "%{http_code}" http://VPS_IP` returns 200
    - `ssh deploy@VPS_IP "wp --path=/home/deploy/ambo-thoughts/public plugin list --status=active --format=csv"` shows wordfence, updraftplus, seo-by-rank-math, redis-cache
    - `ssh deploy@VPS_IP "ufw status"` shows ports 22, 80, 443 only
    - `ssh deploy@VPS_IP "sudo fail2ban-client status"` shows jails active
  </verify>
  <done>
    - VPS is hardened (SSH key-only, UFW, fail2ban)
    - LEMP stack running (Nginx + PHP-FPM 8.3 + MariaDB 10.11 + Redis)
    - WordPress installed and accessible at http://VPS_IP
    - Nginx FastCGI cache configured
    - Redis Object Cache enabled
    - Wordfence, UpdraftPlus, Rank Math installed and active
    - File permissions correct (dirs 755, files 644, wp-config 600)
    - xmlrpc.php blocked, old .html URLs redirect
  </done>
</task>

</tasks>

<verification>
- SSH to VPS as deploy user (not root) with key authentication
- `curl http://VPS_IP` returns WordPress default page
- WordPress admin login works at http://VPS_IP/wp-admin/
- `redis-cli ping` returns PONG on VPS
- `nginx -t` passes on VPS
- UFW blocks all ports except 22, 80, 443
</verification>

<success_criteria>
Production VPS is fully provisioned, hardened, and running WordPress with all infrastructure plugins. Ready to receive the customized ChurchWP theme and content from the local environment via rsync deployment (Plan 06).
</success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-02-SUMMARY.md`
</output>
