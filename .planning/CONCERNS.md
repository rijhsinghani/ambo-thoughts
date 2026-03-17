# Site Concerns — Ambo Thoughts WordPress (104.196.102.152)

**Audit Date:** 2026-03-17
**Status:** Open — address before domain launch

---

## High Severity

### Hardcoded IP in front-page.php

Hero images reference `http://104.196.102.152/wp-content/uploads/...` directly. When a domain is added, images will still load from the bare IP — potentially causing mixed content issues under HTTPS. Also breaks if the VM IP changes.

**Fix:** Replace hardcoded IP URLs with `get_site_url()` or use relative paths.

---

## Medium Severity

### Hardcoded Post ID in front-page.php

`get_permalink(6709)` is used for the "View All Homilies" link. If this post is ever deleted or recreated, the link silently breaks with no error.

**Fix:** Use `get_permalink(get_page_by_path('homilies'))` or a menu/option instead.

### Duplicate Open Graph Meta Tags

The child theme's `functions.php` adds hand-rolled OG/Twitter Card tags, but Rank Math SEO is installed and also generates OG tags. Both run simultaneously, causing duplicate `og:title`, `og:description`, etc. in the HTML `<head>`.

**Fix:** Remove the custom OG implementation from `functions.php` and let Rank Math handle it.

### Stale Duplicate WordPress Installation

A second full WordPress install exists at `/home/deploy/ambo-thoughts/public/` with a live `wp-config.php` containing production database credentials. Not currently web-accessible, but it's a stale attack surface.

**Fix:** Delete `/home/deploy/ambo-thoughts/public/` entirely, or at minimum remove its `wp-config.php`.

### Parent Theme File Modified

`churchwp/functions.php` was touched on March 16, 9 days after the initial theme install (March 7). Any future ChurchWP parent theme update will overwrite this change.

**Fix:** Identify what changed and move it to the child theme's `functions.php`.

---

## Low Severity

### WP_DEBUG Enabled in Production

`wp-config.php` has `WP_DEBUG true`. Logs to file only (`WP_DEBUG_DISPLAY false`), but debug mode has performance implications and information disclosure risk if display is ever toggled accidentally.

**Fix:** Set `WP_DEBUG false` before going live with a domain.

### Inline CSS in header.php

The child theme's `header.php` contains ~60 lines of inline `<style>` CSS. This bypasses browser caching and duplicates some rules already in `css/custom.css`.

**Fix:** Move all CSS into `css/custom.css` and remove the inline block.

### Extensive CSS Overrides with !important

`css/custom.css` is ~700 lines of CSS overrides using `!important` throughout. Any ChurchWP parent theme update that renames CSS classes will silently break the Navy/Gold design.

**Fix:** Manageable but fragile — document which parent theme classes are overridden so updates can be reconciled.

### Translation Loading Deprecation Warnings

Both `js_composer` (WPBakery) and `churchwp`/`themeslr` plugins trigger `_load_textdomain_just_in_time` PHP 8.x deprecation notices. Not breaking now, but will become hard errors in future WordPress/PHP versions.

**Fix:** Plugin-level issue — watch for plugin updates that resolve this.

---

## Summary

The WordPress core is untouched and all plugins are standard. Custom code is properly isolated in the child theme (`front-page.php`, `header.php`, `functions.php`, `css/custom.css`). The main pre-launch priorities are: (1) replace hardcoded IPs with dynamic URLs, (2) remove duplicate OG tag generation, and (3) clean up the stale duplicate WP install.
