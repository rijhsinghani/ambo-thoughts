# Architecture Patterns

**Domain:** Church ministry website (WordPress redesign from static HTML)
**Researched:** 2026-03-07

## Recommended Architecture

```
+---------------------------------------------------+
|                   VPS (Production)                 |
|  Ubuntu 22.04 / 24.04 LTS                        |
|  +-----------+  +---------+  +------------------+ |
|  | Nginx     |  | PHP-FPM |  | MariaDB/MySQL    | |
|  | (reverse  |->| 8.2+    |->| (WordPress DB)   | |
|  |  proxy +  |  |         |  |                   | |
|  |  SSL/TLS) |  +---------+  +------------------+ |
|  +-----------+                                     |
|                                                    |
|  /var/www/ambothoughts.com/                       |
|  +-- wp-content/                                  |
|      +-- themes/churchwp/          (parent)       |
|      +-- themes/churchwp-child/    (child theme)  |
|      +-- plugins/                                 |
|      +-- uploads/                                 |
+---------------------------------------------------+
         |
         | REST API (wp-json/wp/v2/posts)
         v
+---------------------------------------------------+
|  Homily Pipeline (local/cron)                     |
|  scripts/process_homilies.py                      |
|  - Google Drive -> Gemini analysis -> ffmpeg trim |
|  - YouTube upload -> transcript -> WP REST API    |
+---------------------------------------------------+

+---------------------------------------------------+
|  Local Development                                |
|  Local by Flywheel OR Docker                      |
|  Same child theme under Git version control       |
|  Deploy via rsync + WP-CLI search-replace         |
+---------------------------------------------------+
```

### Component Boundaries

| Component                        | Responsibility                                                       | Communicates With                                 |
| -------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------- |
| **Nginx**                        | TLS termination, static file serving, reverse proxy to PHP-FPM       | PHP-FPM, Let's Encrypt                            |
| **PHP-FPM 8.2+**                 | WordPress execution, REST API handling                               | MariaDB, filesystem                               |
| **MariaDB**                      | WordPress data (posts, options, users, meta)                         | PHP-FPM                                           |
| **ChurchWP (parent theme)**      | Base templates, Visual Composer integration, theme options panel     | ThemeSLR Framework plugin                         |
| **churchwp-child (child theme)** | Navy/Gold color overrides, template customizations, custom functions | Parent theme                                      |
| **Homily pipeline**              | Video processing, YouTube upload, blog post creation via REST API    | WordPress REST API, Google Drive, YouTube, Gemini |
| **UpdraftPlus**                  | Automated backups to Google Drive or S3                              | Remote storage                                    |

### Data Flow

1. **Content creation (manual):** Admin dashboard -> WordPress editor -> MariaDB -> rendered pages
2. **Homily pipeline (automated):** Google Drive video -> Gemini analysis -> ffmpeg trim -> YouTube upload -> Python script POSTs to `wp-json/wp/v2/posts` -> new WordPress post with embedded YouTube video
3. **Visitor request:** Browser -> Nginx (cached static HTML via WP Super Cache) -> PHP-FPM -> MariaDB -> rendered page

---

## 1. ChurchWP Child Theme Strategy

### Why a Child Theme

ChurchWP is a ThemeForest theme (v2.3, January 2025, PHP 8.x compatible). Direct modifications to the parent theme will be lost on update. All customizations go in a child theme.

**Confidence: HIGH** (WordPress official documentation)

### Child Theme File Structure

```
wp-content/themes/churchwp-child/
+-- style.css              # Theme header + Navy/Gold CSS overrides
+-- functions.php          # Enqueue styles, register CPT, REST API mods
+-- screenshot.png         # Theme thumbnail (1200x900)
+-- header.php             # Override: remove phone/address, center cross logo
+-- footer.php             # Override: simplified footer for ministry site
+-- template-parts/        # Any partial overrides from parent
+-- assets/
|   +-- css/
|   |   +-- custom.css     # Additional styles beyond variable overrides
|   +-- images/
|       +-- deacons-cross.png
+-- inc/
    +-- rest-api.php        # Custom REST API endpoint modifications
    +-- homily-cpt.php      # Custom post type registration (if not using plugin)
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
Text Domain:  ambothoughts
*/
```

The `Template: churchwp` line MUST match the parent theme's folder name exactly.

### Color Override Strategy

ChurchWP uses its Theme Panel for colors (not the WordPress Customizer). The override approach:

1. **Theme Panel first:** Set primary/accent colors via Theme Panel > Styling Settings. ChurchWP's theme panel supports skin colors and global fonts. Set navy as primary, gold as accent here.

2. **Child theme CSS for what the panel misses:** The theme panel won't cover every element. Override remaining green/default colors in `style.css`:

```css
/* --- Navy & Gold overrides for ChurchWP --- */
:root {
  --navy: #001f5b;
  --navy-light: #0a2d6e;
  --navy-dark: #00132e;
  --gold: #c9a84c;
  --gold-light: #d4b968;
  --cream: #f5f0e8;
}

/* Override ChurchWP's default accent color (green) */
.tslr-btn,
.tslr-btn:hover,
a.tslr-btn,
.widget .tagcloud a:hover,
.pagination .current {
  background-color: var(--gold);
  color: var(--navy);
}

/* Override link colors site-wide */
a {
  color: var(--gold);
}
a:hover {
  color: var(--gold-light);
}

/* Header background */
.header-wrapper,
.tslr-header {
  background-color: var(--navy-dark);
}
```

3. **Typography in child theme:**

```css
/* Playfair Display for headings, system sans for body */
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

Also set body font via Theme Panel > Styling Settings > Body Font Family if ChurchWP's panel supports Google Fonts (it does per docs: "added body font family theme options with font-size, font-weight and line-height").

### functions.php (Child Theme)

```php
<?php
/**
 * Ambo Thoughts child theme functions.
 */

// Enqueue parent + child styles
add_action('wp_enqueue_scripts', 'ambothoughts_enqueue_styles');
function ambothoughts_enqueue_styles() {
    // Parent theme style
    wp_enqueue_style(
        'churchwp-parent-style',
        get_template_directory_uri() . '/style.css'
    );
    // Child theme style (loads after parent)
    wp_enqueue_style(
        'ambothoughts-style',
        get_stylesheet_directory_uri() . '/style.css',
        array('churchwp-parent-style'),
        wp_get_theme()->get('Version')
    );
}

// Include custom modules
require_once get_stylesheet_directory() . '/inc/homily-cpt.php';
require_once get_stylesheet_directory() . '/inc/rest-api.php';
```

### Template Override Rules

Only copy and modify the specific template files you need to change. For this project:

- **header.php** -- Remove ChurchWP's default phone number and address bar. Center the deacon's cross logo. Adjust nav menu for the 8 pages.
- **front-page.php or page templates** -- May need to override homepage layout for the 3-slide hero + homily cards + gallery + news + bio sections.

Do NOT copy all parent templates into the child theme. Only override what you change.

**Confidence: HIGH** (WordPress official child theme docs)

---

## 2. ChurchWP Theme Options Panel vs WordPress Customizer

ChurchWP uses its own **ThemeSLR Framework plugin** for theme options, NOT the standard WordPress Customizer. This is common for ThemeForest themes.

### Theme Panel Location

WordPress Admin > Theme Panel (separate menu item, not under Appearance > Customize)

### Theme Panel Tabs

| Tab                  | What to Set for Ambo Thoughts                                                                                 |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| **General Settings** | Disable page preloader (unnecessary overhead)                                                                 |
| **Styling Settings** | Primary color: #001f5b (navy), Accent: #c9a84c (gold), Body font: system sans, Heading font: Playfair Display |
| **Header Settings**  | Logo: deacons-cross.png, Remove top bar (phone/address), Configure main nav                                   |
| **Footer Settings**  | Simplified footer with ministry info                                                                          |
| **Contact Settings** | deacon267@verizon.net, hcugini@stroberts.cc                                                                   |
| **Blog Settings**    | Archive layout, single post layout                                                                            |
| **Social Media**     | YouTube channel link                                                                                          |
| **Demo Importer**    | Import demo content as starting point, then customize                                                         |

### When to Use Theme Panel vs Child Theme CSS

- **Theme Panel:** Global colors, fonts, logo, footer content, blog layout — anything the panel exposes
- **Child theme CSS:** Specific element overrides the panel doesn't cover, responsive tweaks, custom component styling
- **WordPress Customizer:** Site identity (site title, tagline, favicon), menus, widgets — standard WP features ChurchWP doesn't override

**Confidence: MEDIUM** (based on ChurchWP docs at themeslr.com; exact panel options need verification after purchase)

---

## 3. ChurchWP Required/Bundled Plugins

Based on documentation, ChurchWP bundles these plugins (installed via admin prompt after theme activation):

| Plugin                                               | Status     | Purpose                                           |
| ---------------------------------------------------- | ---------- | ------------------------------------------------- |
| **ThemeSLR Framework**                               | Required   | Powers the Theme Panel options                    |
| **WPBakery Page Builder** (formerly Visual Composer) | Bundled    | Drag-and-drop page builder, 30+ custom shortcodes |
| **Slider Revolution**                                | Bundled    | Hero slider (3-slide hero for homepage)           |
| **Contact Form 7**                                   | Compatible | Contact form (but WPForms Lite is better UX)      |

**Important:** WPBakery and Revolution Slider licenses are tied to the theme purchase. They auto-update through the theme, not independently.

---

## 4. Custom Post Type: Homilies

### Recommendation: Register a Custom Post Type in the Child Theme

Use a custom post type (`homily`) rather than standard posts with categories because:

1. **Separate from blog posts** -- Homilies have unique fields (scripture references, liturgical season, YouTube embed, transcript, pull quote) that don't apply to regular blog posts
2. **Dedicated archive** -- `/homilies/` archive page with its own template
3. **REST API addressable** -- `wp-json/wp/v2/homilies` endpoint for the pipeline
4. **Portable** -- If the theme changes, the CPT registration in functions.php travels with it

### Why NOT Use Church Content Plugin

The Church Content plugin (churchthemes.com) creates a `ctc_sermon` post type. It's well-built but:

- Designed for themes from churchthemes.com, not ChurchWP
- Adds Events, People, Locations CPTs you don't need
- The sermon fields don't match the pipeline's output (no transcript field, no pull_quote, no liturgical_season)
- ChurchWP may have its own sermon functionality that conflicts

**Build a lean CPT instead.** Here's the registration:

### inc/homily-cpt.php

```php
<?php
/**
 * Register the Homily custom post type and taxonomies.
 */

add_action('init', 'ambothoughts_register_homily_cpt');
function ambothoughts_register_homily_cpt() {
    $labels = array(
        'name'               => 'Homilies',
        'singular_name'      => 'Homily',
        'add_new'            => 'Add New Homily',
        'add_new_item'       => 'Add New Homily',
        'edit_item'          => 'Edit Homily',
        'view_item'          => 'View Homily',
        'all_items'          => 'All Homilies',
        'search_items'       => 'Search Homilies',
        'not_found'          => 'No homilies found.',
        'menu_icon'          => 'dashicons-book-alt',
    );

    register_post_type('homily', array(
        'labels'             => $labels,
        'public'             => true,
        'has_archive'        => true,
        'rewrite'            => array('slug' => 'homilies'),
        'supports'           => array('title', 'editor', 'excerpt', 'thumbnail', 'custom-fields'),
        'show_in_rest'       => true,  // Critical: enables REST API + Gutenberg
        'rest_base'          => 'homilies',
        'menu_position'      => 5,
        'taxonomies'         => array('homily_season'),
    ));

    // Liturgical Season taxonomy
    register_taxonomy('homily_season', 'homily', array(
        'labels'            => array(
            'name'          => 'Liturgical Seasons',
            'singular_name' => 'Liturgical Season',
        ),
        'hierarchical'      => true,
        'show_in_rest'      => true,
        'rewrite'           => array('slug' => 'season'),
    ));
}

// Register custom meta fields for REST API access
add_action('init', 'ambothoughts_register_homily_meta');
function ambothoughts_register_homily_meta() {
    $meta_fields = array(
        'youtube_id'        => 'string',
        'pull_quote'        => 'string',
        'scripture_refs'    => 'string',  // JSON-encoded array
        'transcript'        => 'string',
        'drive_file_id'     => 'string',
        'homily_date'       => 'string',  // Liturgical date
    );

    foreach ($meta_fields as $key => $type) {
        register_post_meta('homily', $key, array(
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => $type,
            'auth_callback' => function() {
                return current_user_can('edit_posts');
            },
        ));
    }
}
```

**Confidence: HIGH** (WordPress CPT API is stable and well-documented)

---

## 5. Plugin Architecture (Minimal Set)

Keep plugins minimal. Every plugin is an attack surface and performance cost.

### Required Plugins (Install These)

| Plugin                    | Version        | Purpose                                  | Why This One                                                                            |
| ------------------------- | -------------- | ---------------------------------------- | --------------------------------------------------------------------------------------- |
| **ThemeSLR Framework**    | (bundled)      | ChurchWP theme options                   | Required by theme                                                                       |
| **WPBakery Page Builder** | (bundled)      | Page layouts, shortcodes                 | Required by theme for demo content                                                      |
| **Slider Revolution**     | (bundled)      | Homepage hero slider                     | 3-slide hero per design spec                                                            |
| **WPForms Lite**          | Latest         | Contact form                             | Free, drag-and-drop, sends to two emails (deacon267@verizon.net + hcugini@stroberts.cc) |
| **Yoast SEO**             | Latest         | SEO meta, sitemaps, schema               | Industry standard, handles structured data for sermons                                  |
| **WP Super Cache**        | Latest         | Page caching                             | Free, lightweight, pairs well with Nginx. Generates static HTML files                   |
| **Wordfence Security**    | Latest (free)  | Firewall, login protection, malware scan | Best free WordPress security plugin                                                     |
| **UpdraftPlus**           | Latest (free)  | Automated backups                        | Schedule daily DB + weekly full backup to Google Drive                                  |
| **Application Passwords** | Core (WP 5.6+) | REST API auth for homily pipeline        | Built into WordPress core, no plugin needed                                             |

### Explicitly Do NOT Install

| Plugin                                          | Why Not                                              |
| ----------------------------------------------- | ---------------------------------------------------- |
| Jetpack                                         | Bloated, most features unnecessary for this site     |
| Elementor                                       | Conflicts with WPBakery (ChurchWP's bundled builder) |
| All-in-One WP Migration                         | Only needed once; use WP-CLI instead                 |
| MonsterInsights                                 | Overkill; add GA4 tag directly or via Yoast          |
| Additional security plugins alongside Wordfence | One security plugin only                             |

**Confidence: HIGH** (well-established WordPress plugin recommendations)

---

## 6. Deployment Pipeline: Local to VPS

### Environment Setup

#### Local Development

Use **Local by Flywheel** (free, macOS native). It provisions:

- WordPress instance at `ambothoughts.local`
- PHP 8.2, MySQL 8.0, Nginx
- One-click SSL

Alternative: Docker with `wordpress:php8.2-apache` + `mariadb:11` containers.

#### Production VPS

DigitalOcean or Linode droplet ($6-12/mo):

- Ubuntu 22.04 LTS
- Nginx + PHP-FPM 8.2 + MariaDB 10.11
- Let's Encrypt SSL via Certbot
- WP-CLI installed globally

### What Goes in Git

```
ambothoughts-wp/                    # New repo for WordPress customizations
+-- wp-content/
|   +-- themes/churchwp-child/      # Child theme (version controlled)
|   +-- mu-plugins/                 # Must-use plugins if any
+-- scripts/
|   +-- process_homilies.py         # Homily pipeline (adapted for WP REST API)
|   +-- config.py                   # Pipeline config
|   +-- deploy.sh                   # Deployment script
+-- .gitignore                      # Ignore wp-core, uploads, wp-config.php
```

**Do NOT put in Git:** WordPress core, parent theme (purchased), `wp-config.php`, `wp-content/uploads/`, plugin directories (managed via WP-CLI).

### wp-config.php Environment Management

Use the **local-config.php pattern** (Mark Jaquith's approach):

```php
// wp-config.php (committed to repo as template, NOT with real credentials)
<?php
// Load environment-specific config
if (file_exists(dirname(__FILE__) . '/local-config.php')) {
    require dirname(__FILE__) . '/local-config.php';
    define('WP_LOCAL_DEV', true);
} else {
    // Production credentials
    define('DB_NAME',     getenv('WP_DB_NAME')     ?: 'ambothoughts_prod');
    define('DB_USER',     getenv('WP_DB_USER')     ?: 'wp_user');
    define('DB_PASSWORD', getenv('WP_DB_PASSWORD'));
    define('DB_HOST',     getenv('WP_DB_HOST')     ?: 'localhost');
    define('WP_LOCAL_DEV', false);
}

// Environment type (WordPress 5.5+)
define('WP_ENVIRONMENT_TYPE', WP_LOCAL_DEV ? 'local' : 'production');

// Disable file editing in production
if (!WP_LOCAL_DEV) {
    define('DISALLOW_FILE_EDIT', true);
    define('DISALLOW_FILE_MODS', false); // Allow plugin updates
}
```

`local-config.php` is in `.gitignore` and contains local DB credentials.

### Deployment Script (deploy.sh)

```bash
#!/bin/bash
# Deploy child theme + pipeline scripts to production VPS
set -euo pipefail

REMOTE_USER="deploy"
REMOTE_HOST="ambothoughts.com"
REMOTE_PATH="/var/www/ambothoughts.com"
THEME_PATH="$REMOTE_PATH/wp-content/themes/churchwp-child"

echo "=== Deploying Ambo Thoughts ==="

# 1. Sync child theme files
rsync -avz --delete \
  --exclude '.git' \
  --exclude '.DS_Store' \
  wp-content/themes/churchwp-child/ \
  "$REMOTE_USER@$REMOTE_HOST:$THEME_PATH/"

# 2. Sync pipeline scripts
rsync -avz \
  scripts/ \
  "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/scripts/"

# 3. Clear caches on production
ssh "$REMOTE_USER@$REMOTE_HOST" << 'REMOTE'
  cd /var/www/ambothoughts.com
  wp cache flush
  wp super-cache flush
  echo "Caches flushed."
REMOTE

echo "=== Deploy complete ==="
```

### Database Sync (Local <-> Production)

**Direction: Production -> Local only.** Never push local DB to production after launch.

```bash
# Export production DB
ssh deploy@ambothoughts.com "cd /var/www/ambothoughts.com && wp db export - | gzip" \
  > prod-backup-$(date +%Y%m%d).sql.gz

# Import locally (Local by Flywheel shell)
gunzip -c prod-backup-*.sql.gz | wp db import -

# Replace production URLs with local
wp search-replace 'https://ambothoughts.com' 'https://ambothoughts.local' \
  --all-tables --precise --recurse-objects
```

WP-CLI's `search-replace` handles serialized data in options/meta correctly (critical -- `sed` will corrupt serialized PHP arrays).

**Confidence: HIGH** (WP-CLI search-replace is the standard approach)

---

## 7. Homily Pipeline Integration (REST API)

### Adapting process_homilies.py for WordPress

The existing pipeline generates static HTML. For WordPress, replace Step 7 (HTML generation) with a REST API call to create WordPress posts.

### Authentication Setup

1. In WordPress admin: Users > Profile > Application Passwords
2. Create an application password for "Homily Pipeline"
3. Store credentials as environment variables (never in code)

### Python REST API Client

Add to `process_homilies.py` (or a new `wp_publisher.py` module):

```python
import requests
import base64
import os
import json

WP_URL = os.environ.get('WP_URL', 'https://ambothoughts.com')
WP_USER = os.environ.get('WP_API_USER', 'pipeline-bot')
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

    # Build YouTube embed for content
    youtube_id = homily_record.get('youtube_id', '')
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

    # Build post content
    transcript = homily_record.get('transcript', '')
    content = embed_html + transcript

    post_data = {
        'title': homily_record.get('title', 'Untitled Homily'),
        'content': content,
        'status': 'publish',
        'excerpt': homily_record.get('description', ''),
        'meta': {
            'youtube_id': youtube_id,
            'pull_quote': homily_record.get('pull_quote', ''),
            'scripture_refs': json.dumps(
                homily_record.get('scripture_refs', [])
            ),
            'transcript': transcript,
            'drive_file_id': homily_record.get('drive_file_id', ''),
            'homily_date': homily_record.get('date', ''),
        },
    }

    response = requests.post(
        endpoint,
        headers=_wp_headers(),
        json=post_data,
        timeout=30,
    )
    response.raise_for_status()

    post_id = response.json()['id']
    return post_id
```

### Pipeline Modification

In `process_all()`, replace the `generate_all_pages(manifest)` call with:

```python
# Step 7 — Publish to WordPress (replaces static HTML generation)
if not skip_upload:
    wp_post_id = create_homily_post(homily_record)
    homily_record['wp_post_id'] = wp_post_id
    log.info("Published to WordPress: post ID %d", wp_post_id)
```

### REST API Endpoint Summary

| Endpoint                       | Method | Purpose                 |
| ------------------------------ | ------ | ----------------------- |
| `/wp-json/wp/v2/homilies`      | POST   | Create new homily       |
| `/wp-json/wp/v2/homilies`      | GET    | List all homilies       |
| `/wp-json/wp/v2/homilies/{id}` | GET    | Get single homily       |
| `/wp-json/wp/v2/homilies/{id}` | PUT    | Update homily           |
| `/wp-json/wp/v2/homily_season` | GET    | List liturgical seasons |
| `/wp-json/wp/v2/media`         | POST   | Upload featured image   |

**Confidence: HIGH** (WordPress REST API is stable, well-documented; `show_in_rest: true` on CPT registration exposes these endpoints automatically)

---

## 8. Backup Strategy

### UpdraftPlus Configuration

| Setting                      | Value                                       | Rationale                                |
| ---------------------------- | ------------------------------------------- | ---------------------------------------- |
| **Files backup schedule**    | Weekly                                      | Content doesn't change daily             |
| **Database backup schedule** | Daily                                       | Posts/comments change more often         |
| **Remote storage**           | Google Drive (free 15GB)                    | Already have Google account for pipeline |
| **Retention**                | 4 weekly file backups, 14 daily DB backups  | 2-week recovery window                   |
| **Include**                  | Plugins, themes, uploads, other directories | Full site restore capability             |
| **Exclude**                  | Cache directories, temp files               | Reduce backup size                       |

### Server-Level Backup (Belt and Suspenders)

```bash
# /etc/cron.daily/wp-backup.sh
#!/bin/bash
BACKUP_DIR="/backups/ambothoughts"
SITE_DIR="/var/www/ambothoughts.com"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR"

# Database dump
wp db export "$BACKUP_DIR/db-$DATE.sql" --path="$SITE_DIR" --allow-root
gzip "$BACKUP_DIR/db-$DATE.sql"

# Files (only wp-content, not core)
tar czf "$BACKUP_DIR/files-$DATE.tar.gz" \
  -C "$SITE_DIR" wp-content/

# Retain 30 days
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete
```

### Restore Procedure

1. UpdraftPlus: Dashboard > UpdraftPlus > Existing Backups > Restore
2. Manual: `wp db import backup.sql && rsync wp-content/`
3. After restore: `wp cache flush && wp rewrite flush`

**Confidence: HIGH** (UpdraftPlus is the most-used WordPress backup plugin, 3M+ installs)

---

## Patterns to Follow

### Pattern 1: Theme Panel First, CSS Override Second

**What:** Always check if ChurchWP's theme panel can handle the customization before writing CSS.
**When:** Any visual change (colors, fonts, layouts).
**Why:** Theme panel values persist through child theme updates and are admin-editable. CSS overrides require developer intervention.

### Pattern 2: One Plugin Per Function

**What:** Never install two plugins that serve the same purpose.
**When:** Adding any new plugin.
**Why:** Plugin conflicts are the #1 cause of WordPress site breakage.

### Pattern 3: WP-CLI for All Server Operations

**What:** Use WP-CLI instead of the admin dashboard for database operations, plugin management, and cache clearing.
**When:** Deployment, migration, maintenance.
**Why:** Scriptable, reproducible, faster. Critical for `search-replace` which handles serialized data.

```bash
# Examples
wp plugin install wordfence --activate
wp plugin update --all
wp search-replace 'old-domain.com' 'new-domain.com' --all-tables
wp cache flush
wp cron event run --all
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Editing Parent Theme Files

**What:** Making changes directly in `wp-content/themes/churchwp/`
**Why bad:** All changes lost on theme update. ChurchWP updates periodically (last: Jan 2025).
**Instead:** Always use the child theme. Copy only the specific template file you need to override.

### Anti-Pattern 2: Using WPBakery for Custom Homily Templates

**What:** Building the homily single post template with WPBakery shortcodes.
**Why bad:** Creates vendor lock-in. If you ever leave WPBakery, all content becomes `[vc_row][vc_column]` garbage.
**Instead:** Use the child theme's `single-homily.php` template with standard WordPress template tags. WPBakery is fine for static pages (homepage, about) but not for programmatically-generated content.

### Anti-Pattern 3: Storing Credentials in wp-config.php in Git

**What:** Committing database passwords, API keys, or application passwords to version control.
**Why bad:** Security risk. Even private repos can leak.
**Instead:** Use `local-config.php` (gitignored) or environment variables. For the homily pipeline, use env vars: `WP_APP_PASSWORD`, `GOOGLE_API_KEY`.

### Anti-Pattern 4: Using sed for Database URL Replacement

**What:** Using `sed` or manual SQL to change URLs in the WordPress database.
**Why bad:** WordPress stores serialized PHP arrays in options and post meta. `sed` changes string lengths without updating the serialization header, corrupting data silently.
**Instead:** Always use `wp search-replace` which handles serialized data correctly.

---

## Scalability Considerations

| Concern           | Current (< 100 visitors/day)      | Growth (1K visitors/day)      | Unlikely (10K+/day)            |
| ----------------- | --------------------------------- | ----------------------------- | ------------------------------ |
| **Caching**       | WP Super Cache (static HTML)      | Same, add Nginx FastCGI cache | CDN (Cloudflare free tier)     |
| **Database**      | Single MariaDB on VPS             | Same, add query caching       | Read replica (unlikely needed) |
| **Media**         | wp-content/uploads on disk        | Same, add lazy loading        | CDN for static assets          |
| **Homily videos** | YouTube embeds (zero server load) | Same                          | Same (YouTube handles scale)   |
| **SSL**           | Let's Encrypt auto-renew          | Same                          | Same                           |

This site will realistically stay under 1K visitors/day. YouTube embeds offload all video serving. The VPS + caching setup handles this comfortably.

---

## Sources

- [WordPress Child Themes -- Theme Handbook](https://developer.wordpress.org/themes/advanced-topics/child-themes/) (HIGH confidence)
- [ChurchWP Official Documentation](http://themeslr.com/docs/churchwp/) (MEDIUM confidence -- docs are sparse)
- [ChurchWP on ThemeForest](https://themeforest.net/item/church-religion-sermons-donations-wordpress-theme-churchwp/19128148) (HIGH confidence)
- [WordPress REST API -- Posts Reference](https://developer.wordpress.org/rest-api/reference/posts/) (HIGH confidence)
- [Church Content Plugin](https://wordpress.org/plugins/church-theme-content/) (HIGH confidence)
- [WP-CLI search-replace](https://developer.wordpress.org/cli/commands/search-replace/) (HIGH confidence)
- [WordPress wp-config.php Multi-Environment](https://markjaquith.wordpress.com/2018/02/05/tips-for-configuring-wordpress-environments/) (HIGH confidence)
- [UpdraftPlus](https://wordpress.org/plugins/updraftplus/) (HIGH confidence)
- [WordPress REST API with Python](https://robingeuens.com/blog/python-wordpress-api/) (MEDIUM confidence)
- [WordPress Theme Structure](https://developer.wordpress.org/themes/core-concepts/theme-structure/) (HIGH confidence)
