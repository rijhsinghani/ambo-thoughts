# Architecture Patterns

**Domain:** Church/Ministry WordPress Website (Ambo Thoughts Redesign)
**Researched:** 2026-03-07
**Overall Confidence:** HIGH

## System Overview

```
+------------------+     +-----------+     +--------------------+
| Local by Flywheel|     |  GitHub   |     | DigitalOcean VPS   |
| (Development)    |---->|  (Git)    |---->| (Production)       |
|                  |     |           |     |                    |
| PHP 8.3 / Nginx  |     | wp-content|     | Nginx + PHP-FPM    |
| MariaDB          |     | child     |     | MariaDB + Redis    |
| WP-CLI           |     | theme     |     | WordPress + ChurchWP|
+------------------+     | scripts   |     +--------------------+
                          +-----------+            ^
                                                   |
+------------------+                               |
| process_homilies |  WP REST API (Application     |
| .py (Gemini AI)  |  Passwords + Basic Auth)      |
| Google Drive     |-------------------------------+
| YouTube Upload   |
+------------------+
```

## Component Boundaries

| Component                               | Responsibility                                            | Communicates With                                                                              |
| --------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Local by Flywheel                       | Development environment, theme editing, content preview   | GitHub (git push), VPS (rsync deploy)                                                          |
| GitHub repo                             | Version control for child theme + deployment scripts      | Local (git pull), VPS (deploy trigger)                                                         |
| DigitalOcean VPS                        | Production WordPress hosting                              | Visitors (HTTPS), Homily pipeline (REST API)                                                   |
| Homily pipeline (`process_homilies.py`) | Video processing, YouTube upload, content generation      | Google Drive (source video), YouTube (upload), VPS WordPress (REST API to create homily posts) |
| ChurchWP parent theme                   | Base layout, WPBakery page builder, responsive design     | Child theme (template overrides, CSS)                                                          |
| ChurchWP child theme                    | Navy/Gold branding, custom CPT templates, color overrides | Parent theme (inherits), WPBakery (shortcode styling)                                          |

---

## 1. Child Theme Strategy

### File Structure

```
wp-content/themes/churchwp-child/
  style.css              # Theme header + Navy/Gold CSS overrides
  functions.php          # Enqueue parent styles, register CPT, custom functions
  screenshot.png         # Theme thumbnail (1200x900 recommended)

  # Template overrides (only files that need changes)
  header.php             # Custom header if ChurchWP header needs modification
  single-homily.php      # Template for individual homily posts (CPT)
  archive-homily.php     # Template for homily archive/listing page

  # Assets
  assets/
    css/
      custom-colors.css  # Navy/Gold color system (CSS custom properties)
      wpbakery-overrides.css  # WPBakery element color overrides
    js/
      custom.js          # Any custom JavaScript (minimal)
    images/
      logo.png           # Site logo
      favicon.ico        # Favicon

  # Includes (organized PHP)
  inc/
    cpt-homily.php       # Custom Post Type registration
    rest-api.php         # REST API endpoint customizations for homily pipeline
    theme-setup.php      # Menus, widget areas, theme support
```

### style.css Header (Required)

```css
/*
 Theme Name:   Ambo Thoughts
 Theme URI:    https://ambothoughts.com
 Description:  Child theme of ChurchWP for Deacon Henry Cugini's ministry site
 Author:       Sameer Rijhsinghani
 Template:     churchwp
 Version:      1.0.0
 Text Domain:  ambo-thoughts
*/

/* Parent theme styles are enqueued via functions.php, not @import */
```

**Critical note on `Template` value:** The `Template` header must exactly match the parent theme's directory name. After installing ChurchWP from ThemeForest, check the folder name in `wp-content/themes/` -- ThemeForest themes use inconsistent naming. Run `ls wp-content/themes/` after installation to confirm. It may be `churchwp`, `developer`, or something else entirely.

**Confidence:** HIGH -- this is the WordPress-documented child theme pattern.

### functions.php

```php
<?php
/**
 * Ambo Thoughts Child Theme Functions
 */

// Enqueue parent + child styles properly
add_action('wp_enqueue_scripts', function () {
    // Parent theme stylesheet
    wp_enqueue_style(
        'churchwp-parent-style',
        get_template_directory_uri() . '/style.css',
        [],
        wp_get_theme()->parent()->get('Version')
    );

    // Child theme stylesheet
    wp_enqueue_style(
        'ambo-child-style',
        get_stylesheet_uri(),
        ['churchwp-parent-style'],
        wp_get_theme()->get('Version')
    );

    // Custom color overrides
    wp_enqueue_style(
        'ambo-custom-colors',
        get_stylesheet_directory_uri() . '/assets/css/custom-colors.css',
        ['ambo-child-style'],
        wp_get_theme()->get('Version')
    );

    // WPBakery overrides (loaded last for specificity)
    wp_enqueue_style(
        'ambo-wpbakery-overrides',
        get_stylesheet_directory_uri() . '/assets/css/wpbakery-overrides.css',
        ['ambo-custom-colors'],
        wp_get_theme()->get('Version')
    );
});

// Load organized includes
require_once get_stylesheet_directory() . '/inc/theme-setup.php';
require_once get_stylesheet_directory() . '/inc/cpt-homily.php';
require_once get_stylesheet_directory() . '/inc/rest-api.php';
```

**Why separate CSS files instead of one big style.css:** Maintainability. `custom-colors.css` defines the palette (change gold shade = one file). `wpbakery-overrides.css` handles the WPBakery specificity battle (can be dropped entirely if WPBakery is ever replaced). Loading order via `wp_enqueue_style` dependencies ensures correct cascade.

**Confidence:** HIGH -- `wp_enqueue_style` with parent dependency is the WordPress-documented approach. Using `@import` in style.css is deprecated practice.

### Navy/Gold Color System

```css
/* assets/css/custom-colors.css */

:root {
  /* Primary palette */
  --ambo-navy: #001f5b;
  --ambo-navy-light: #0a2d6e;
  --ambo-navy-dark: #00132e;
  --ambo-gold: #c9a84c;
  --ambo-gold-light: #d4b968;
  --ambo-gold-dark: #a88b3d;
  --ambo-cream: #f5f0e8;

  /* Semantic usage */
  --ambo-bg-primary: #ffffff;
  --ambo-bg-secondary: var(--ambo-cream);
  --ambo-text-primary: var(--ambo-navy);
  --ambo-text-body: #333333;
  --ambo-accent: var(--ambo-gold);
  --ambo-link: var(--ambo-gold);
  --ambo-link-hover: var(--ambo-gold-light);
}

/* Global overrides */
body {
  color: var(--ambo-text-body);
}

a {
  color: var(--ambo-link);
}

a:hover {
  color: var(--ambo-link-hover);
}

h1,
h2,
h3,
h4,
h5,
h6 {
  color: var(--ambo-text-primary);
}

/* Header */
.header-wrapper,
.tslr-header {
  background-color: var(--ambo-navy-dark);
}

/* Typography */
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap");

h1,
h2,
h3,
h4,
h5,
h6,
.tslr-heading,
.entry-title {
  font-family: "Playfair Display", Georgia, serif;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue",
    Arial, sans-serif;
}
```

```css
/* assets/css/wpbakery-overrides.css */

/* WPBakery buttons */
.vc_btn3-color-primary,
.vc_btn3-color-juicy-pink,
.wpb_button {
  background-color: var(--ambo-navy) !important;
  border-color: var(--ambo-navy) !important;
  color: #ffffff !important;
}

.vc_btn3-color-primary:hover,
.vc_btn3-color-juicy-pink:hover {
  background-color: var(--ambo-gold) !important;
  border-color: var(--ambo-gold) !important;
}

/* ChurchWP accent color overrides */
.tslr-btn,
.tslr-btn:hover,
a.tslr-btn,
.widget .tagcloud a:hover,
.pagination .current {
  background-color: var(--ambo-gold);
  color: var(--ambo-navy);
}
```

**Why `!important` is acceptable here:** WPBakery injects inline styles and high-specificity selectors. Child theme CSS cannot win specificity battles against inline styles without `!important`. This is the [documented WPBakery approach](https://kb.wpbakery.com/docs/learning-more/custom-css/).

**Why CSS custom properties over hardcoded hex values:** Changing the exact shade of navy or gold later requires editing exactly one file instead of hunting through dozens of rules.

**Confidence:** HIGH for the pattern; MEDIUM for the exact WPBakery/ChurchWP class names (`.tslr-btn`, `.tslr-header`, etc. need verification after theme installation via browser DevTools).

### ChurchWP Theme Options Panel

ChurchWP uses its own **ThemeSLR Framework plugin** for theme options, NOT the standard WordPress Customizer.

| Tab                  | What to Set                                                               |
| -------------------- | ------------------------------------------------------------------------- |
| **Styling Settings** | Primary color: #001f5b (navy), Accent: #c9a84c (gold), Body/Heading fonts |
| **Header Settings**  | Logo, remove top bar (phone/address not needed), main nav config          |
| **Footer Settings**  | Simplified footer with ministry info                                      |
| **Contact Settings** | deacon267@verizon.net, hcugini@stroberts.cc                               |
| **Blog Settings**    | Archive layout, single post layout                                        |
| **Social Media**     | YouTube channel link                                                      |
| **Demo Importer**    | Import demo content as starting point, then customize                     |
| **General Settings** | Disable page preloader (unnecessary overhead)                             |

**When to use Theme Panel vs child theme CSS:**

- **Theme Panel:** Global colors, fonts, logo, footer -- anything the panel exposes
- **Child theme CSS:** Specific element overrides the panel misses, WPBakery shortcode styling, responsive tweaks
- **WordPress Customizer:** Site identity (title, tagline, favicon), menus, widgets

**Confidence:** MEDIUM -- based on ChurchWP docs at themeslr.com; exact panel options need verification after purchase.

### Template Override Rules

Only copy and modify the specific template files you need to change:

- **header.php** -- Remove default phone/address bar, center the deacon's cross logo, adjust nav
- **single-homily.php** -- Custom template for homily detail pages (YouTube embed, transcript, scripture refs)
- **archive-homily.php** -- Homily listing page with cards
- **front-page.php** -- Homepage layout (3-slide hero + homily cards + gallery + news + bio)

Do NOT copy all parent templates into the child theme. Only override what you change.

---

## 2. Deployment Pipeline: Local by Flywheel to VPS

### Architecture: rsync over SSH

Direct rsync from local machine to VPS. No CI/CD pipeline needed for a single-developer church site.

```
Local by Flywheel → (git commit) → GitHub → (manual: scripts/deploy.sh) → rsync → VPS
```

### What Goes in Git vs What Doesn't

```
# IN GIT (tracked)
wp-content/
  themes/churchwp-child/       # All child theme files
  mu-plugins/                  # Must-use plugins (if any custom code)
scripts/
  deploy.sh                    # Deployment script
  pull-db.sh                   # Database pull script
  backup.sh                    # Backup script
  process_homilies.py          # Homily pipeline (already exists)
  config.py                    # Pipeline config (already exists)
  requirements.txt             # Python dependencies (already exists)
wp-config-sample.php           # Template wp-config (no secrets)
.gitignore

# NOT IN GIT (ignored)
wp-config.php                  # Contains database credentials
local-config.php               # Environment-specific settings
wp-content/uploads/            # Media files (sync separately via rsync)
wp-content/themes/churchwp/    # Parent theme (installed via ThemeForest, not git)
wp-content/plugins/            # Plugins (installed via WP admin, managed via WP-CLI)
wp-content/upgrade/            # WordPress upgrade files
wp-content/cache/              # Cache files
wp-admin/                      # WordPress core
wp-includes/                   # WordPress core
*.sql / *.sql.gz               # Database dumps
```

**Confidence:** HIGH -- this is the standard WordPress git workflow documented by [WP Engine](https://wpengine.com/support/git/), [Roots](https://roots.io/twelve-factor-03-config/), and [Sal Ferrarello's .gitignore](https://gist.github.com/salcode/9940509).

### Updated .gitignore

```gitignore
# WordPress core (never track)
/wp-admin/
/wp-includes/
/wp-*.php
!/wp-config-sample.php
/index.php
/license.txt
/readme.html
/xmlrpc.php

# wp-config (contains secrets)
wp-config.php
local-config.php

# Content - only track child theme and mu-plugins
wp-content/uploads/
wp-content/plugins/
wp-content/themes/churchwp/
wp-content/upgrade/
wp-content/cache/
wp-content/debug.log

# Keep child theme tracked (negate ignore)
!wp-content/themes/churchwp-child/
!wp-content/mu-plugins/

# OS files
.DS_Store
Thumbs.db

# Editor
*.swp
*.swo
*~
.idea/
.vscode/

# Python
__pycache__/
*.pyc
scripts/.env
scripts/client_secrets.json
scripts/*.token.json
scripts/manifest.json

# Database dumps
*.sql
*.sql.gz

# Local Flywheel
.localwp/

# Claude
.claude/
```

### Deploy Script

```bash
#!/bin/bash
# scripts/deploy.sh - Deploy child theme to production VPS
set -euo pipefail

VPS_USER="deploy"
VPS_HOST="YOUR_VPS_IP"
WP_PATH="/var/www/ambothoughts"
SSH_KEY="~/.ssh/ambo_deploy"

echo "=== Deploying Ambo Thoughts child theme ==="

# 1. Sync child theme files
rsync -avz --delete \
  --exclude='.DS_Store' \
  --exclude='*.map' \
  -e "ssh -i ${SSH_KEY}" \
  wp-content/themes/churchwp-child/ \
  ${VPS_USER}@${VPS_HOST}:${WP_PATH}/wp-content/themes/churchwp-child/

# 2. Sync must-use plugins (if any)
if [ -d "wp-content/mu-plugins" ]; then
  rsync -avz --delete \
    -e "ssh -i ${SSH_KEY}" \
    wp-content/mu-plugins/ \
    ${VPS_USER}@${VPS_HOST}:${WP_PATH}/wp-content/mu-plugins/
fi

# 3. Clear caches on production
ssh -i ${SSH_KEY} ${VPS_USER}@${VPS_HOST} "
  cd ${WP_PATH}
  wp cache flush 2>/dev/null || true
  sudo rm -rf /var/cache/nginx/*
  sudo systemctl reload nginx
"

echo "=== Deploy complete ==="
```

**Why rsync over WP Migrate DB or All-in-One Migration:**

- rsync transfers only changed bytes (delta compression), making subsequent deploys near-instant
- No plugin dependency or database involvement for theme deploys
- `--delete` flag ensures production mirrors local exactly (removes stale files)
- WP Migrate DB is for database transfers, not theme files
- All-in-One Migration is a one-time tool, not a repeatable workflow

**Confidence:** HIGH -- rsync + WP-CLI is the [industry standard for WordPress VPS deployments](https://wpshout.com/quick-guides/migrate-wordpress-wp-cli-rsync/).

### Database Sync (Production to Local)

Database flows **production -> local** only. Never push a local database to production after go-live (content is managed in production WP admin by Deacon Henry).

```bash
#!/bin/bash
# scripts/pull-db.sh - Pull production database to local
set -euo pipefail

VPS_USER="deploy"
VPS_HOST="YOUR_VPS_IP"
WP_PATH="/var/www/ambothoughts"
LOCAL_SITE_URL="http://ambothoughts.local"
PROD_URL="https://ambothoughts.com"

echo "=== Pulling production database ==="

# Export from production
ssh ${VPS_USER}@${VPS_HOST} \
  "cd ${WP_PATH} && wp db export - | gzip" \
  > /tmp/ambo-db-backup.sql.gz

# Import to local (Local by Flywheel has WP-CLI built in)
cd ~/Local\ Sites/ambo-thoughts/app/public
gunzip -c /tmp/ambo-db-backup.sql.gz | wp db import -

# Search-replace URLs (handles serialized data correctly)
wp search-replace "${PROD_URL}" "${LOCAL_SITE_URL}" \
  --all-tables --precise --recurse-objects

echo "=== Database synced ==="
```

**Critical:** Always use `wp search-replace` for URL changes. Using `sed` or manual SQL will corrupt serialized PHP arrays stored in options and post meta.

---

## 3. wp-config.php Environment Management

### Recommended Pattern: local-config.php Override

Use the [Mark Jaquith pattern](https://markjaquith.wordpress.com/2018/02/05/tips-for-configuring-wordpress-environments/) with WordPress's built-in `WP_ENVIRONMENT_TYPE` constant.

**wp-config.php (committed as template only, with placeholder values):**

```php
<?php
/**
 * WordPress Configuration - Ambo Thoughts
 *
 * Environment-specific settings loaded from local-config.php
 * which is NOT committed to git.
 */

// Load environment-specific config (database creds, debug, etc.)
if (file_exists(__DIR__ . '/local-config.php')) {
    require_once __DIR__ . '/local-config.php';
} else {
    die('Missing local-config.php -- copy local-config-sample.php and fill in values.');
}

// Shared settings (all environments)
$table_prefix = 'wp_';

define('DISALLOW_FILE_EDIT', true);         // No theme/plugin editing in admin
define('WP_POST_REVISIONS', 5);             // Limit post revisions
define('AUTOSAVE_INTERVAL', 120);           // 2 minutes
define('EMPTY_TRASH_DAYS', 30);

// Security salts -- generate fresh at https://api.wordpress.org/secret-key/1.1/salt/
// PASTE GENERATED SALTS HERE

if (!defined('ABSPATH')) {
    define('ABSPATH', __DIR__ . '/');
}
require_once ABSPATH . 'wp-settings.php';
```

**local-config.php for Local Development (NOT in git):**

```php
<?php
define('WP_ENVIRONMENT_TYPE', 'local');

define('DB_NAME', 'local');
define('DB_USER', 'root');
define('DB_PASSWORD', 'root');
define('DB_HOST', 'localhost');

define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', true);
define('SCRIPT_DEBUG', true);

define('WP_HOME', 'http://ambothoughts.local');
define('WP_SITEURL', 'http://ambothoughts.local');
```

**local-config.php for Production VPS (NOT in git):**

```php
<?php
define('WP_ENVIRONMENT_TYPE', 'production');

define('DB_NAME', 'wordpress_ambo');
define('DB_USER', 'wp_ambo');
define('DB_PASSWORD', 'STRONG_PASSWORD_HERE');
define('DB_HOST', 'localhost');

define('WP_DEBUG', false);
define('WP_DEBUG_LOG', true);      // Log errors to file but don't display
define('WP_DEBUG_DISPLAY', false);

define('WP_HOME', 'https://ambothoughts.com');
define('WP_SITEURL', 'https://ambothoughts.com');

// Force HTTPS
define('FORCE_SSL_ADMIN', true);
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
```

**Why this pattern over `.env` files:** For a non-technical admin's site on a simple VPS, PHP files are easier to manage than `.env` files or system-level environment variables. The `local-config.php` pattern is battle-tested and requires zero additional tooling. Roots' Bedrock uses `.env` which is cleaner but adds Composer dependency -- overkill for this project.

**Confidence:** HIGH -- `local-config.php` pattern is recommended by [Mark Jaquith](https://markjaquith.wordpress.com/2018/02/05/tips-for-configuring-wordpress-environments/) (WordPress core contributor) and documented in the [WordPress Advanced Administration Handbook](https://developer.wordpress.org/advanced-administration/wordpress/wp-config/).

---

## 4. WordPress REST API Integration for Homily Pipeline

### Current State

The existing `process_homilies.py` generates static HTML pages (Step 7: `generate_homily_page()` and `generate_all_pages()`). For the WordPress migration, Step 7 needs to create WordPress posts via the REST API instead.

### Architecture Change

```
BEFORE (current static site):
  process_homilies.py → static HTML files → blog/homily-{slug}.html

AFTER (WordPress):
  process_homilies.py → WP REST API → WordPress homily CPT posts
```

### Authentication: Application Passwords (Built into WordPress 5.6+)

No plugin needed. Application Passwords are a core WordPress feature.

**Setup:**

1. WordPress Admin -> Users -> Edit User (admin account)
2. Scroll to "Application Passwords" section
3. Name: "Homily Pipeline"
4. Click "Add New Application Password"
5. Save the generated password (shown once, cannot be retrieved later)
6. Store as environment variable: `WP_APP_PASSWORD`

**Why Application Passwords over JWT or OAuth:**

- Built into WordPress core (no plugin to maintain or break)
- Can be revoked individually without changing the admin password
- Each password has its own audit trail (last used, IP address)
- Simple Basic Auth is sufficient for a server-to-server pipeline over HTTPS

**Confidence:** HIGH -- [Application Passwords are documented in the WordPress REST API Handbook](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/).

### CPT Registration with REST API Support

```php
// inc/cpt-homily.php

add_action('init', function () {
    register_post_type('homily', [
        'labels' => [
            'name'               => 'Homilies',
            'singular_name'      => 'Homily',
            'add_new_item'       => 'Add New Homily',
            'edit_item'          => 'Edit Homily',
            'view_item'          => 'View Homily',
            'all_items'          => 'All Homilies',
            'search_items'       => 'Search Homilies',
            'not_found'          => 'No homilies found',
        ],
        'public'             => true,
        'has_archive'        => true,
        'menu_icon'          => 'dashicons-microphone',
        'supports'           => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
        'rewrite'            => ['slug' => 'homilies'],
        'show_in_rest'       => true,           // CRITICAL: enables REST API
        'rest_base'          => 'homilies',     // API endpoint: /wp-json/wp/v2/homilies
        'rest_controller_class' => 'WP_REST_Posts_Controller',
        'menu_position'      => 5,
    ]);

    register_taxonomy('liturgical_season', 'homily', [
        'labels'       => ['name' => 'Liturgical Seasons', 'singular_name' => 'Season'],
        'hierarchical' => true,
        'show_in_rest' => true,   // CRITICAL: enables REST API for taxonomy
        'rest_base'    => 'liturgical_season',
        'rewrite'      => ['slug' => 'season'],
    ]);

    // Register custom meta fields for REST API access
    $meta_fields = [
        'youtube_video_id'  => 'string',
        'homily_date'       => 'string',
        'scripture_reading' => 'string',
        'pull_quote'        => 'string',
        'drive_file_id'     => 'string',
    ];

    foreach ($meta_fields as $key => $type) {
        register_post_meta('homily', $key, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => $type,
            'auth_callback' => function () {
                return current_user_can('edit_posts');
            },
        ]);
    }
});
```

**Critical:** `show_in_rest => true` is required on both the CPT and taxonomy for the REST API to work. Without it, the `/wp-json/wp/v2/homilies` endpoint returns 404. Also, `register_post_meta()` with `show_in_rest => true` is required for custom meta fields to be readable/writable via the API.

### Python REST API Client (Pipeline Modification)

Replace the static HTML generation (Steps 6-7) in `process_homilies.py` with a WordPress REST API call:

```python
import base64
import requests
import os
import json

WP_URL = os.environ.get('WP_URL', 'https://ambothoughts.com')
WP_USER = os.environ.get('WP_API_USER', 'admin')
WP_APP_PASSWORD = os.environ.get('WP_APP_PASSWORD')

def _wp_headers():
    """Build auth headers for WordPress REST API."""
    credentials = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(credentials.encode()).decode()
    return {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
    }

def create_homily_post(homily_record: dict) -> int:
    """Create a homily CPT post via WordPress REST API.

    Returns the WordPress post ID.
    """
    endpoint = f"{WP_URL}/wp-json/wp/v2/homilies"

    youtube_id = homily_record.get('youtube_id', '')
    transcript = homily_record.get('transcript', '')

    # Build YouTube embed block for WordPress content
    embed_html = ''
    if youtube_id:
        embed_html = (
            f'<!-- wp:embed {{"url":"https://youtu.be/{youtube_id}",'
            f'"type":"video","providerNameSlug":"youtube"}} -->\n'
            f'<figure class="wp-block-embed is-type-video '
            f'is-provider-youtube wp-block-embed-youtube">'
            f'<div class="wp-block-embed__wrapper">\n'
            f'https://youtu.be/{youtube_id}\n'
            f'</div></figure>\n'
            f'<!-- /wp:embed -->\n\n'
        )

    post_data = {
        'title': homily_record.get('title', 'Untitled Homily'),
        'content': embed_html + transcript,
        'status': 'publish',
        'excerpt': homily_record.get('description', ''),
        'meta': {
            'youtube_video_id': youtube_id,
            'pull_quote': homily_record.get('pull_quote', ''),
            'scripture_reading': json.dumps(
                homily_record.get('scripture_refs', [])
            ),
            'drive_file_id': homily_record.get('drive_file_id', ''),
            'homily_date': homily_record.get('date', ''),
        },
    }

    # Set liturgical season taxonomy term
    season = homily_record.get('liturgical_season')
    if season:
        # Get or create the taxonomy term
        term_resp = requests.get(
            f"{WP_URL}/wp-json/wp/v2/liturgical_season",
            headers=_wp_headers(),
            params={'search': season},
            timeout=10,
        )
        terms = term_resp.json()
        if terms:
            post_data['liturgical_season'] = [terms[0]['id']]
        else:
            # Create the term
            create_resp = requests.post(
                f"{WP_URL}/wp-json/wp/v2/liturgical_season",
                headers=_wp_headers(),
                json={'name': season},
                timeout=10,
            )
            if create_resp.ok:
                post_data['liturgical_season'] = [create_resp.json()['id']]

    response = requests.post(
        endpoint,
        headers=_wp_headers(),
        json=post_data,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()['id']
```

### Pipeline Modification Point

In `process_all()`, replace `generate_all_pages(manifest)` with:

```python
# Step 7 -- Publish to WordPress (replaces static HTML generation)
if not skip_upload:
    wp_post_id = create_homily_post(homily_record)
    homily_record['wp_post_id'] = wp_post_id
    log.info("Published to WordPress: post ID %d", wp_post_id)
```

### REST API Endpoint Summary

| Endpoint                           | Method | Purpose                       |
| ---------------------------------- | ------ | ----------------------------- |
| `/wp-json/wp/v2/homilies`          | POST   | Create new homily             |
| `/wp-json/wp/v2/homilies`          | GET    | List all homilies             |
| `/wp-json/wp/v2/homilies/{id}`     | GET    | Get single homily             |
| `/wp-json/wp/v2/homilies/{id}`     | PUT    | Update homily                 |
| `/wp-json/wp/v2/liturgical_season` | GET    | List liturgical seasons       |
| `/wp-json/wp/v2/liturgical_season` | POST   | Create liturgical season term |
| `/wp-json/wp/v2/media`             | POST   | Upload featured image         |

**Confidence:** HIGH -- WordPress REST API for custom post types is [well-documented](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-rest-api-support-for-custom-content-types/). The existing pipeline's data structures map cleanly to WordPress post fields.

---

## 5. DNS Cutover Strategy: GitHub Pages to VPS

### Current State

The site currently lives on GitHub Pages with the domain `ambothoughts.com` (or similar) pointed at GitHub's servers.

### Cutover Plan

**Phase 1: Preparation (48+ hours before cutover)**

1. Lower DNS TTL to 300 seconds (5 minutes) on all records
   - This ensures DNS caches expire quickly during the switch
   - Must be done at least 48 hours in advance (so old high-TTL records expire)
2. Set up WordPress on VPS completely (content migrated, theme configured)
3. Issue an initial SSL certificate using standalone mode (before DNS points to VPS):
   ```bash
   sudo certbot certonly --standalone -d ambothoughts.com -d www.ambothoughts.com
   ```
   Or test via the VPS IP address directly

**Phase 2: Pre-Switch Testing**

```bash
# Test the VPS site locally by editing /etc/hosts
echo "YOUR_VPS_IP ambothoughts.com www.ambothoughts.com" | sudo tee -a /etc/hosts

# Browse to https://ambothoughts.com -- should show WordPress site
# Test all pages, contact form, homily archive

# IMPORTANT: Remove the /etc/hosts entry after testing
sudo sed -i '' '/ambothoughts.com/d' /etc/hosts
```

**Phase 3: DNS Switch**

At the domain registrar, update DNS records:

```
# Remove existing CNAME/A records pointing to GitHub
# Add new records:
A     @     YOUR_VPS_IP        TTL: 300
A     www   YOUR_VPS_IP        TTL: 300
```

**Phase 4: Post-Switch (0-48 hours)**

1. Keep GitHub Pages running for 48 hours (serves visitors during DNS propagation)
2. Monitor VPS access logs: `tail -f /var/log/nginx/access.log`
3. Issue/renew SSL certificate once DNS is pointing to VPS:
   ```bash
   sudo certbot --nginx -d ambothoughts.com -d www.ambothoughts.com
   ```
4. After 48 hours, disable GitHub Pages in the repo settings
5. Raise DNS TTL back to 3600 seconds (1 hour)

**Phase 5: Old URL Redirects**

The current static site has URLs like `/blog/homily-{slug}.html`, `/videos.html`, `/about.html`. Set up Nginx rewrite rules to redirect old URLs to new WordPress URLs so existing links and bookmarks keep working:

```nginx
# /etc/nginx/conf.d/ambo-redirects.conf

# Old static HTML pages -> WordPress pages
rewrite ^/about\.html$          /about/          permanent;
rewrite ^/contact\.html$        /contact/        permanent;
rewrite ^/videos\.html$         /videos/         permanent;
rewrite ^/spirituality\.html$   /spirituality/   permanent;
rewrite ^/pictures\.html$       /gallery/        permanent;
rewrite ^/blog\.html$           /homilies/       permanent;
rewrite ^/church-news\.html$    /church-news/    permanent;
rewrite ^/prayer-partner\.html$ /prayer-partner/ permanent;
rewrite ^/stuff\.html$          /stuff/          permanent;

# Old homily detail pages -> WordPress CPT singles
rewrite ^/blog/homily-(.+)\.html$ /homilies/$1/ permanent;

# Old index
rewrite ^/index\.html$ / permanent;
```

**Confidence:** HIGH -- DNS cutover with TTL lowering is the [standard zero-downtime migration approach](https://www.cloudways.com/blog/zero-downtime-migration-for-wordpress-sites/). Nginx rewrite rules are straightforward.

---

## 6. Security Architecture

### VPS Hardening

| Layer     | Implementation                                                               |
| --------- | ---------------------------------------------------------------------------- |
| SSH       | Key-only auth, disable password auth, disable root login                     |
| Firewall  | UFW: allow 80, 443, SSH port only                                            |
| WordPress | `DISALLOW_FILE_EDIT` in wp-config, Wordfence for firewall + login protection |
| Nginx     | Rate limiting on `wp-login.php`, block `xmlrpc.php`                          |
| SSL       | Let's Encrypt with auto-renewal via systemd timer                            |
| Updates   | Unattended-upgrades for OS security patches                                  |
| Backups   | UpdraftPlus weekly + DigitalOcean automated snapshots                        |

### Nginx Security Headers

```nginx
# Add to server block
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Block xmlrpc.php (not needed for this site)
location = /xmlrpc.php {
    deny all;
    access_log off;
    log_not_found off;
}

# Rate limit login page
location = /wp-login.php {
    limit_req zone=login burst=3 nodelay;
    include fastcgi_params;
    fastcgi_pass unix:/run/php/php8.3-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

**Confidence:** HIGH -- standard WordPress VPS security practices.

---

## 7. Backup Strategy

| Backup Type   | Tool         | Frequency    | Retention    | Storage                  |
| ------------- | ------------ | ------------ | ------------ | ------------------------ |
| Full site     | UpdraftPlus  | Weekly       | 4 weeks      | Google Drive (free 15GB) |
| Database only | WP-CLI cron  | Daily        | 7 days       | Local on VPS             |
| VPS snapshot  | DigitalOcean | Weekly       | 4 snapshots  | DigitalOcean ($1.20/mo)  |
| Child theme   | Git          | Every deploy | Full history | GitHub                   |

**Daily DB backup cron (on VPS):**

```bash
# /etc/cron.d/ambo-db-backup
0 3 * * * deploy cd /var/www/ambothoughts && wp db export /var/backups/ambo/db-$(date +\%Y\%m\%d).sql && gzip /var/backups/ambo/db-$(date +\%Y\%m\%d).sql && find /var/backups/ambo/ -name "*.sql.gz" -mtime +7 -delete
```

---

## 8. Data Flow Summary

### Content Management (Manual)

```
Deacon Henry (WP Admin) -> WordPress Editor -> MariaDB -> Nginx FastCGI Cache -> Visitor
```

### Homily Pipeline (Automated)

```
Google Drive (Mass recordings)
    |
    v
process_homilies.py
    |-- Gemini AI: frame analysis (find homily timestamps)
    |-- ffmpeg: trim video to homily segment
    |-- YouTube API: upload trimmed homily
    |-- Gemini AI: transcribe + generate blog content
    |
    v
WordPress REST API (Application Passwords auth)
    |-- Create homily CPT post (title, transcript, excerpt)
    |-- Set custom meta (youtube_id, homily_date, scripture, pull_quote)
    |-- Assign liturgical_season taxonomy term
    |
    v
WordPress renders homily on frontend
```

### Theme Development (Developer)

```
Local by Flywheel (edit child theme)
    |
    v
git commit + push to GitHub
    |
    v
scripts/deploy.sh (rsync child theme to VPS)
    |
    v
Nginx cache flush -> site reflects changes
```

---

## 9. Patterns to Follow

### Pattern 1: Child Theme Only, Never Edit Parent

All customizations go in `churchwp-child/`. Never modify files in `churchwp/`. Parent theme updates replace the directory entirely.

### Pattern 2: Theme Panel First, CSS Override Second

Always check if ChurchWP's Theme Panel can handle a customization before writing CSS. Panel values persist through updates and are admin-editable.

### Pattern 3: CSS Custom Properties for Brand Colors

Define all brand colors as CSS custom properties in one file. When the shade of navy or gold needs adjustment, change one file.

### Pattern 4: Application Passwords for API Auth

Use WordPress Application Passwords for the homily pipeline. They can be revoked individually, leave audit trails, and don't expose the admin password.

### Pattern 5: Production DB is Source of Truth

After go-live, content (posts, pages, media) is managed in production only. Database flows production -> local, never local -> production. Exception: during initial setup before go-live.

### Pattern 6: WP-CLI for All Server Operations

Use WP-CLI for database operations, plugin management, cache clearing, URL search-replace. It handles serialized data correctly and is scriptable/reproducible.

### Pattern 7: Nginx Rewrites Over .htaccess

Nginx doesn't support `.htaccess`. WordPress permalink rewriting uses `try_files $uri $uri/ /index.php?$args;` in the Nginx server block.

---

## 10. Anti-Patterns to Avoid

### Anti-Pattern 1: Editing the Parent Theme

**What:** Modifying PHP, CSS, or JS files inside `wp-content/themes/churchwp/`.
**Consequence:** Parent theme updates overwrite all changes. This is the #1 cause of "my site broke after updating the theme."
**Instead:** Create template overrides in the child theme.

### Anti-Pattern 2: Using WPBakery Design Options for Global Branding

**What:** Setting Navy/Gold colors through WPBakery's per-element "Design Options" tab.
**Consequence:** Per-element styling stores CSS as post meta (inline styles in the database). Changing the gold shade later means editing every single page and element.
**Instead:** Use the child theme's CSS with custom properties. WPBakery Design Options are for one-off spacing/padding tweaks, not global branding.

### Anti-Pattern 3: Pushing Local Database to Production

**What:** Exporting the local database and importing to production after go-live.
**Consequence:** Overwrites all content Deacon Henry has created. WordPress stores absolute URLs in the database, so local URLs will break the site.
**Instead:** Content changes happen in production WP admin. Code changes deploy via rsync.

### Anti-Pattern 4: Using sed for Database URL Replacement

**What:** Using `sed` or manual SQL to change URLs when migrating.
**Consequence:** WordPress stores serialized PHP arrays in options and post meta. `sed` changes string lengths without updating the serialization header, corrupting data silently.
**Instead:** Always use `wp search-replace` which handles serialized data correctly.

### Anti-Pattern 5: Storing Plugins in Git

**What:** Committing `wp-content/plugins/` to the repository.
**Consequence:** Plugins are updated via WP admin. Git versions conflict with admin-updated versions. Plugin license keys and paid plugins shouldn't be in version control.
**Instead:** Track plugins as a documented list. Install/update plugins through WP admin.

### Anti-Pattern 6: Using WPBakery for Programmatic Content Templates

**What:** Building the homily single post template with WPBakery shortcodes.
**Consequence:** Creates vendor lock-in. If WPBakery is ever replaced, all content becomes `[vc_row][vc_column]` garbage.
**Instead:** Use standard WordPress template tags in `single-homily.php`. WPBakery is fine for static pages (homepage, about) but not for programmatically-generated content.

---

## 11. Scalability Considerations

| Concern  | At launch (~10 visitors/day)      | At 100 visitors/day | At 1000+ visitors/day      |
| -------- | --------------------------------- | ------------------- | -------------------------- |
| Server   | $6/mo 1GB Droplet is plenty       | Same                | Upgrade to $12/mo 2GB      |
| Caching  | Nginx FastCGI cache, 60min TTL    | Same                | Add CDN (Cloudflare free)  |
| Database | MariaDB with Redis object cache   | Same                | Same                       |
| Media    | Served from VPS disk              | Same                | CDN or DigitalOcean Spaces |
| Videos   | YouTube embeds (zero server load) | Same                | Same                       |

For a Catholic deacon's ministry site, 1000+ daily visitors would be exceptional. The $6/mo VPS with FastCGI cache handles expected traffic without issue.

---

## 12. ChurchWP Bundled Plugins

| Plugin                    | Status     | Purpose                        | Notes                                             |
| ------------------------- | ---------- | ------------------------------ | ------------------------------------------------- |
| **ThemeSLR Framework**    | Required   | Powers the Theme Panel options | Must install for theme to function                |
| **WPBakery Page Builder** | Bundled    | Drag-and-drop page builder     | License tied to theme purchase, updates via theme |
| **Slider Revolution**     | Bundled    | Homepage hero slider           | License tied to theme purchase                    |
| **Contact Form 7**        | Compatible | Contact form                   | Use this or WPForms Lite (see FEATURES.md)        |

**WPBakery lock-in warning:** WPBakery uses proprietary shortcodes (`[vc_row]`, `[vc_column]`, etc.) for page content. Pages built with WPBakery become dependent on it. This is acceptable for static pages (homepage, about) but NOT for the homily CPT template. Homily content should use standard WordPress blocks/HTML so the pipeline's REST API output doesn't depend on WPBakery.

---

## Sources

- [WordPress Child Themes -- Theme Handbook](https://developer.wordpress.org/themes/advanced-topics/child-themes/) -- HIGH confidence
- [WPBakery Custom CSS Documentation](https://kb.wpbakery.com/docs/learning-more/custom-css/) -- HIGH confidence
- [WordPress REST API: Adding Custom Content Types](https://developer.wordpress.org/rest-api/extending-the-rest-api/adding-rest-api-support-for-custom-content-types/) -- HIGH confidence
- [WordPress Application Passwords Integration Guide](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/) -- HIGH confidence
- [WordPress REST API Authentication Handbook](https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/) -- HIGH confidence
- [WordPress wp_get_environment_type()](https://developer.wordpress.org/reference/functions/wp_get_environment_type/) -- HIGH confidence
- [WordPress Advanced Administration: wp-config.php](https://developer.wordpress.org/advanced-administration/wordpress/wp-config/) -- HIGH confidence
- [Mark Jaquith: Tips for Configuring WordPress Environments](https://markjaquith.wordpress.com/2018/02/05/tips-for-configuring-wordpress-environments/) -- HIGH confidence
- [Sal Ferrarello WordPress .gitignore](https://gist.github.com/salcode/9940509) -- HIGH confidence
- [WP Engine: Git Version Control for WordPress](https://wpengine.com/support/git/) -- HIGH confidence
- [WPShout: Migrate WordPress with WP-CLI and rsync](https://wpshout.com/quick-guides/migrate-wordpress-wp-cli-rsync/) -- MEDIUM confidence
- [GridPane: WordPress Migration with WP-CLI and rsync](https://gridpane.com/kb/how-to-migrate-a-wordpress-website-with-wp-cli-and-rsync/) -- MEDIUM confidence
- [Cloudways: Zero Downtime WordPress Migration 2025](https://www.cloudways.com/blog/zero-downtime-migration-for-wordpress-sites/) -- MEDIUM confidence
- [Robin Geuens: Python WordPress API Guide](https://robingeuens.com/blog/python-wordpress-api/) -- MEDIUM confidence
- [WordPress REST API Posts Reference](https://developer.wordpress.org/rest-api/reference/posts/) -- HIGH confidence
- [ChurchWP ThemeForest Listing](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148) -- HIGH confidence
- [WordPress Child Theme Development Guide 2026](https://www.fysalyaqoob.com/guides/wordpress-child-theme-development-guide-2026/) -- MEDIUM confidence
