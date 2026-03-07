---
phase: 1-infrastructure-launch
plan: 02
subsystem: infrastructure
tags: [lemp, wordpress, nginx, php-fpm, mariadb, redis, gcp]
dependency-graph:
  requires: []
  provides:
    [lemp-stack, wordpress-install, fastcgi-cache, redis-cache, fail2ban]
  affects: [1-03, 1-04, 1-05, 1-06]
tech-stack:
  added:
    [
      nginx-1.28.1,
      php-8.3.30,
      mariadb-10.11.14,
      redis,
      wordpress-6.9.1,
      wp-cli-2.12.0,
    ]
  patterns: [fastcgi-cache, ondemand-fpm-pool, gcloud-ssh-provisioning]
key-files:
  created:
    - nginx/wordpress.conf
  modified:
    - /etc/nginx/sites-available/ambo-thoughts (on VM)
    - /etc/php/8.3/fpm/pool.d/www.conf (on VM)
    - /etc/php/8.3/fpm/php.ini (on VM)
    - /var/www/ambo-thoughts/ (WordPress install on VM)
decisions:
  - Used GCP e2-micro instead of DigitalOcean (user decision, adapted plan)
  - Set pm.max_children=3 (not 5) for 1GB shared RAM on e2-micro
  - wp-config.php set to 640 (not 600) so www-data group can read it
  - PHP-FPM runs as www-data:www-data (not deploy:deploy since no deploy user on GCP)
metrics:
  duration: 23m
  completed: 2026-03-07
---

# Phase 1 Plan 02: LEMP Stack + WordPress on GCP VM Summary

LEMP stack (Nginx 1.28.1, PHP-FPM 8.3.30, MariaDB 10.11.14, Redis) with WordPress 6.9.1 on GCP e2-micro VM, FastCGI page caching, Redis object caching, and fail2ban security.

## What Was Done

### Infrastructure Provisioned (on VM 34.74.60.206)

1. **System Update** - Ubuntu 24.04 LTS fully updated via apt dist-upgrade
2. **LEMP Stack** - Installed from ondrej PPAs: Nginx 1.28.1, PHP 8.3.30, MariaDB 10.11.14, Redis
3. **MariaDB Secured** - Removed anonymous users, remote root, test DB; created `wordpress` database with `wpuser`
4. **PHP-FPM Tuned** - ondemand pool, max_children=3, idle timeout 10s, 256M memory, 64M uploads
5. **Nginx Configured** - FastCGI cache (100MB, 60min), static file caching (30d), xmlrpc blocked, GitHub Pages URL redirects
6. **WordPress Installed** - WP-CLI 2.12.0, WordPress 6.9.1, pretty permalinks (/%postname%/)
7. **Plugins Installed** - Wordfence 8.1.4, UpdraftPlus 1.26.2, Rank Math SEO 1.0.265, Redis Object Cache 2.7.0
8. **fail2ban** - Installed and enabled for SSH monitoring
9. **File Permissions** - dirs 755, files 644, wp-config.php 640

### Local Reference Files Created

- `nginx/wordpress.conf` - Nginx server block config (reference copy)

## Verification Results

| Check                          | Result                                                |
| ------------------------------ | ----------------------------------------------------- |
| nginx                          | active                                                |
| php8.3-fpm                     | active                                                |
| mariadb                        | active                                                |
| redis-server                   | active                                                |
| fail2ban                       | active                                                |
| Homepage (http://34.74.60.206) | 200                                                   |
| wp-admin redirect              | 302                                                   |
| wp-login.php                   | 200                                                   |
| redis-cli ping                 | PONG                                                  |
| WordPress siteurl              | http://34.74.60.206                                   |
| Active plugins                 | wordfence, updraftplus, seo-by-rank-math, redis-cache |

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed PHP-FPM pool user from deploy to www-data**

- **Found during:** Verification (wp-admin returning 500)
- **Issue:** Pre-existing PHP-FPM config had `user = deploy` / `group = deploy` from a previous setup attempt. The `deploy` user doesn't exist on this GCP VM.
- **Fix:** Changed pool user/group to `www-data:www-data` in `/etc/php/8.3/fpm/pool.d/www.conf`

**2. [Rule 1 - Bug] Fixed wp-config.php permissions from 600 to 640**

- **Found during:** Verification (wp-admin returning 500)
- **Issue:** wp-config.php with 600 permissions was unreadable by PHP-FPM running as www-data
- **Fix:** Changed to 640 so www-data group can read, owner still has full control

**3. [Rule 3 - Blocking] Fixed pre-existing Nginx config with wrong root path**

- **Found during:** Verification (homepage returning 404)
- **Issue:** A pre-existing `/etc/nginx/sites-available/ambo-thoughts` pointed to `/home/deploy/ambo-thoughts/public` instead of `/var/www/ambo-thoughts`
- **Fix:** Overwrote with `sudo tee` instead of `mv` to replace the existing config

### Plan Adaptations

- **GCP instead of DigitalOcean**: Plan was written for DO droplet; adapted for GCP e2-micro (same specs: 1 vCPU, 1GB RAM). Used `gcloud compute ssh` instead of direct SSH.
- **No deploy user**: GCP sets up `sameerrijhsinghani` with sudo access via OS Login. Skipped deploy user creation (Task 1 checkpoint was pre-satisfied).
- **No UFW**: GCP uses VPC firewall rules instead of UFW. Firewall is managed at the project level.
- **No setup-vps.sh script**: Commands were run directly via gcloud SSH since the plan was adapted for interactive execution.

## WordPress Credentials

- **Admin URL**: http://34.74.60.206/wp-admin/
- **Username**: admin
- **Password**: AmboAdmin2026!
- **DB User**: wpuser / AmboWP2026!

## What's Next

- Plan 03: Domain + SSL setup (Certbot)
- Plan 04: ChurchWP theme installation
- Plan 05: Content migration from Hugo
- Plan 06: Deployment pipeline
