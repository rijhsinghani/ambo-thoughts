# Feature Landscape

**Domain:** Church/Ministry WordPress Website (Catholic Deacon, Spiritual Direction & Bereavement)
**Researched:** 2026-03-07
**Overall Confidence:** HIGH (well-established WordPress plugin ecosystem with abundant documentation)

## Table Stakes

Features visitors expect on a church/ministry website. Missing = site feels incomplete or amateur.

| Feature                   | Why Expected                        | Complexity | Recommended Solution          |
| ------------------------- | ----------------------------------- | ---------- | ----------------------------- |
| Contact form (dual email) | Visitors need to reach Deacon Henry | Low        | Contact Form 7                |
| Homily/sermon archive     | Core content of the ministry        | Medium     | Custom Post Type (no plugin)  |
| Photo gallery             | Visual life of the parish           | Low        | FooGallery (free)             |
| About/bio page            | Credibility, who is the deacon      | Low        | Standard WordPress page       |
| Mobile responsive         | 60%+ traffic is mobile              | Low        | ChurchWP theme handles this   |
| SEO basics                | Discoverability for seekers         | Low        | Rank Math (free)              |
| YouTube video embeds      | Homily videos are primary content   | Low        | Embed Plus for YouTube        |
| RSS / Verse of the Day    | Spiritual content freshness         | Low        | Bible Verse of the Day plugin |

## Differentiators

Features that elevate beyond a basic church brochure site.

| Feature                           | Value Proposition                    | Complexity | Recommended Solution                                   |
| --------------------------------- | ------------------------------------ | ---------- | ------------------------------------------------------ |
| Homily video pipeline integration | Auto-publish from YouTube channel    | Medium     | Custom integration with existing `process_homilies.py` |
| Prayer Partner signup             | Community engagement, return visits  | Low        | WPForms Lite or CF7 additional form                    |
| Liturgical season organization    | Navigate homilies by church calendar | Medium     | Custom taxonomy on CPT                                 |
| Church news aggregation           | One-stop for Vatican/Diocese news    | Low        | RSS block or curated links page                        |
| Hero slider with quotes           | Inspirational first impression       | Low        | ChurchWP built-in slider                               |

## Anti-Features

Features to explicitly NOT build. Scope control for a small ministry site.

| Anti-Feature                    | Why Avoid                                                                         | What to Do Instead                                          |
| ------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Online donations/tithing        | Deacon Henry didn't request it; adds PCI complexity; parish likely has own system | Add later only if explicitly requested                      |
| Member login/portal             | No community platform needed; adds maintenance burden                             | Keep site fully public                                      |
| Event calendar plugin           | No recurring events to manage; adds admin overhead                                | Simple page with upcoming events or link to parish calendar |
| Live streaming integration      | YouTube channel handles this already                                              | Embed YouTube videos directly                               |
| Church management system (ChMS) | Way overbuilt for a personal ministry site                                        | Not applicable                                              |
| E-commerce / bookstore          | Out of scope entirely                                                             | Link to external resources if needed                        |
| Forum / comments system         | Spam magnet; low engagement for ministry sites                                    | Contact form is sufficient                                  |

---

## Plugin Recommendations (Detail)

### 1. Contact Form: Contact Form 7

**Recommendation: Use Contact Form 7** because it handles dual-email delivery natively in the free version, has 10M+ active installs, and the non-technical admin never needs to touch it after setup.

| Attribute        | Detail                             |
| ---------------- | ---------------------------------- |
| Cost             | Free                               |
| Active Installs  | 10,000,000+                        |
| Last Updated     | Feb 2026 (v6.1.5)                  |
| WordPress Compat | 6.7+ (tested to 6.9.1)             |
| Rating           | 4.0/5 (2,153 reviews)              |
| Confidence       | HIGH (official WordPress.org data) |

**Dual-email setup:** In the Mail tab, set the "To" field to:

```
deacon267@verizon.net, hcugini@stroberts.cc
```

Both addresses receive every submission. No paid upgrade needed.

**Why not WPForms Lite:** WPForms Lite also supports comma-separated recipients in a single notification, so it works too. However, CF7 is lighter weight (no upsell nags in the admin), and for a site where the admin will rarely touch the form config, CF7's set-and-forget nature is ideal. WPForms' drag-and-drop builder is overkill when you need exactly one contact form.

**Why not Gravity Forms:** Paid only ($59+/year). Unnecessary for a single contact form.

**Setup notes:**

- Add Flamingo plugin (free) alongside CF7 to store submissions in the WordPress database as backup
- Configure WP Mail SMTP (free) to ensure deliverability via a real SMTP provider (Gmail SMTP or the VPS's mail service)

### 2. SEO: Rank Math (Free)

**Recommendation: Use Rank Math Free** because it offers more features at the free tier than Yoast Free, which matters for a site that won't upgrade to premium.

| Attribute       | Detail                              |
| --------------- | ----------------------------------- |
| Cost            | Free (Pro: $6.99/mo if ever needed) |
| Active Installs | 3,000,000+                          |
| Rating          | 4.9/5                               |
| Confidence      | HIGH                                |

**Key free-tier advantages over Yoast Free:**

- Unlimited focus keywords per post (Yoast: 1)
- Built-in 404 monitoring
- Redirect manager (Yoast: premium only)
- Schema markup (Yoast: premium only)
- Google Search Console integration in setup wizard

**Why not Yoast:** Yoast's free version is deliberately crippled to push premium. For a ministry site that will never pay for SEO premium, Rank Math Free gives substantially more out of the box.

### 3. Photo Gallery: FooGallery (Free)

**Recommendation: Use FooGallery** for displaying church photos (Easter Vigil, Midnight Mass, parish events).

| Attribute       | Detail               |
| --------------- | -------------------- |
| Cost            | Free (Pro available) |
| Active Installs | 200,000+             |
| Last Updated    | Active development   |
| Rating          | 4.5/5                |
| Confidence      | HIGH                 |

**Why FooGallery:**

- Built-in lazy loading (1.2s load time in independent tests)
- Lightbox included in free version
- Gutenberg block support
- Simple admin: upload photos, create gallery, insert block
- Responsive grid layouts included free

**Why not NextGEN Gallery:** NextGEN is powerful but heavier and more complex than needed. FooGallery is simpler for an admin who just needs to upload event photos.

**Why not native WordPress gallery:** The built-in gallery block is basic -- no lightbox, no lazy loading, limited layout options.

**Photo prep note:** HEIC images from the `/Hank/` directory must be converted to JPEG or WebP before uploading. Batch convert with:

```bash
# macOS (using sips)
for f in *.HEIC; do sips -s format jpeg "$f" --out "${f%.HEIC}.jpg"; done
# Or use ImageMagick for WebP
for f in *.HEIC; do convert "$f" "${f%.HEIC}.webp"; done
```

### 4. YouTube Video Embeds: Embed Plus for YouTube

**Recommendation: Use Embed Plus for YouTube** for lazy-loaded, responsive video embeds.

| Attribute       | Detail               |
| --------------- | -------------------- |
| Cost            | Free (Pro available) |
| Active Installs | 100,000+             |
| Last Updated    | Dec 2025             |
| Rating          | 4.6/5                |
| Confidence      | HIGH                 |

**Key capabilities:**

- Facade/lazy loading: replaces heavy iframe with thumbnail until clicked (significant page speed gain)
- Responsive sizing: auto-adjusts to container width
- Gallery mode: can pull from a YouTube channel or playlist
- SEO schema markup for videos (free)
- Deferred JavaScript loading

**Alternative approach:** WordPress natively embeds YouTube URLs as responsive iframes. For a site with only a few videos per page, the native embed + a general lazy-load plugin (like WP Rocket's free lazy load or Lazy Load for Videos plugin) may be sufficient. Embed Plus is recommended because it consolidates video-specific optimizations in one plugin.

### 5. Bible Verse of the Day: Bible Verse of the Day Plugin

**Recommendation: Use Bible Verse of the Day** for the Spirituality page.

| Attribute        | Detail                                                   |
| ---------------- | -------------------------------------------------------- |
| Cost             | Free                                                     |
| Active Installs  | 4,000+                                                   |
| Last Updated     | Jan 2026 (v2.8)                                          |
| WordPress Compat | 5.3+ (tested to 6.9.1)                                   |
| Rating           | 4.9/5 (11 reviews)                                       |
| Confidence       | MEDIUM (small user base but well-maintained, 4.9 rating) |

**How it works:**

- Pulls daily verse from DailyVerses.net
- Available as widget, shortcode `[bibleverseoftheday_niv]`, or Gutenberg block (v2.8+)
- Supports multiple translations (NIV, KJV, ESV, NKJV, NLT, NASB, NRSV)
- Fallback: shows previous verse or John 3:16 if connection fails
- CSS classes for custom styling to match Navy/Gold theme

**For Catholic-specific content:** This plugin uses Protestant bible translations. For Catholic-specific daily readings (which include OT, Psalm, NT, and Gospel for each day's Mass), consider:

- The **Mass Readings** widget from USCCB.org (embed via iframe or RSS)
- Manual links to USCCB daily readings page
- The existing verseoftheday.com RSS feed can be displayed via **Feedzy RSS Feeds** (free, 50K+ installs) using shortcode `[feedzy-rss feeds="URL"]`

**Recommendation:** Use the Bible Verse of the Day plugin for simplicity. Add a "Today's Mass Readings" link to USCCB.org for the Catholic liturgical content.

### 6. Homily/Sermon Management: Custom Post Type (No Plugin)

**Recommendation: Use a Custom Post Type (CPT) registered in the theme's `functions.php`** rather than a sermon management plugin.

| Attribute  | Detail                      |
| ---------- | --------------------------- |
| Cost       | Free (built into WordPress) |
| Dependency | None (no plugin to abandon) |
| Confidence | HIGH                        |

**Why NOT a sermon plugin:**

- **Sermon Manager** (formerly #1): CLOSED on WordPress.org as of Dec 2025 due to security issues. Do not use.
- **CP Sermons:** Not on WordPress.org. Third-party hosted. Uncertain longevity.
- **Series Engine:** $99 paid. Overkill for one deacon's homilies.
- **Advanced Sermons:** Newer, less proven. Premium features locked.

**Why a Custom Post Type works better:**

- Deacon Henry's homilies are simpler than a multi-pastor mega-church sermon library
- A CPT called `homily` with custom taxonomies (`liturgical_season`, `scripture_reference`) is lightweight and permanent
- YouTube embed via a custom field (ACF or native custom fields)
- No risk of plugin abandonment (it's core WordPress functionality)
- ChurchWP theme likely supports custom post type templates

**Implementation outline:**

```php
// In functions.php or a site-specific plugin
register_post_type('homily', [
    'labels' => ['name' => 'Homilies', 'singular_name' => 'Homily'],
    'public' => true,
    'has_archive' => true,
    'menu_icon' => 'dashicons-microphone',
    'supports' => ['title', 'editor', 'thumbnail', 'excerpt'],
    'rewrite' => ['slug' => 'homilies'],
]);

register_taxonomy('liturgical_season', 'homily', [
    'labels' => ['name' => 'Liturgical Seasons'],
    'hierarchical' => true,
    'rewrite' => ['slug' => 'season'],
]);
```

**Taxonomies to create:**

- `liturgical_season`: Advent, Christmas, Ordinary Time, Lent, Easter, etc.
- `scripture_reference`: Optional, for filtering by Bible book

**Custom fields (via ACF Free or native):**

- `youtube_video_id`: For embedding the homily video
- `homily_date`: The liturgical date of the homily
- `scripture_reading`: The Gospel/reading reference

### 7. Church News Aggregation: Static Links Page (No Plugin)

**Recommendation: Use a standard WordPress page with curated links** rather than RSS aggregation.

| Attribute  | Detail   |
| ---------- | -------- |
| Cost       | Free     |
| Complexity | Very Low |
| Confidence | HIGH     |

**Why not RSS aggregation:**

- VaticanNews.com and dioceseoftrenton.org may not have stable, well-formatted RSS feeds
- RSS aggregation plugins add maintenance burden (broken feeds, formatting issues)
- The existing site already uses simple button links to external news sites
- For a site managed by a non-technical admin, a static page with links is more reliable

**Implementation:**

- WordPress page with button blocks linking to VaticanNews.com and dioceseoftrenton.org/news
- Optionally add Feedzy RSS Feeds (free) later if Deacon Henry wants auto-updating headlines
- Keep it simple: the current approach works and the admin understands it

### 8. Additional Recommended Plugins (Infrastructure)

| Plugin             | Purpose                                  | Cost | Installs | Notes                                                |
| ------------------ | ---------------------------------------- | ---- | -------- | ---------------------------------------------------- |
| **WP Mail SMTP**   | Reliable email delivery for contact form | Free | 4M+      | Critical -- VPS mail often goes to spam without SMTP |
| **Flamingo**       | Store CF7 submissions in DB              | Free | 500K+    | Backup in case email delivery fails                  |
| **UpdraftPlus**    | Automated backups                        | Free | 3M+      | Weekly full-site backup to Google Drive or Dropbox   |
| **Wordfence**      | Security (firewall + malware scan)       | Free | 5M+      | Essential for self-managed VPS                       |
| **WP Super Cache** | Page caching for speed                   | Free | 2M+      | Lightweight; good match for small VPS                |
| **Smush**          | Image compression on upload              | Free | 1M+      | Auto-compress church photos on upload                |

---

## Feature Dependencies

```
Contact Form 7 → WP Mail SMTP (email delivery depends on SMTP config)
Homily CPT → YouTube Embed Plugin (homily display includes video)
FooGallery → Smush (gallery photos should be compressed)
Rank Math → Google Search Console (setup wizard connects them)
All features → Wordfence + UpdraftPlus (security and backup are prerequisites)
```

## MVP Recommendation

**Phase 1 (Launch):** Get the site live with all existing content migrated.

Prioritize:

1. ChurchWP theme installed and customized (Navy/Gold)
2. Contact Form 7 with dual-email delivery
3. All static pages migrated (About, Spirituality, Church News, Prayer Partner, Stuff)
4. FooGallery for the Pictures page
5. Embed Plus for YouTube videos on Videos page
6. Rank Math SEO configured
7. Infrastructure plugins (WP Mail SMTP, Wordfence, UpdraftPlus, WP Super Cache)

**Phase 2 (Content System):** Structured homily management.

8. Homily Custom Post Type with taxonomies
9. YouTube integration in homily posts
10. Bible Verse of the Day on Spirituality page
11. Connect existing `process_homilies.py` pipeline to create WordPress posts via REST API

**Defer:**

- Online donations: Not requested, parish has own system
- Event calendar: No events to manage currently
- RSS aggregation: Static links page is sufficient
- Member portal: Not applicable for this ministry

## Plugin Count Summary

**Total recommended plugins: 10** (all free tier)

| Category       | Plugin                 | Status |
| -------------- | ---------------------- | ------ |
| Contact        | Contact Form 7         | Free   |
| Contact backup | Flamingo               | Free   |
| SEO            | Rank Math              | Free   |
| Gallery        | FooGallery             | Free   |
| Video          | Embed Plus for YouTube | Free   |
| Devotional     | Bible Verse of the Day | Free   |
| Email          | WP Mail SMTP           | Free   |
| Security       | Wordfence              | Free   |
| Backup         | UpdraftPlus            | Free   |
| Performance    | WP Super Cache         | Free   |
| Images         | Smush                  | Free   |

**Total recurring cost: $0** (all free plugins + ChurchWP one-time $59 + VPS $5-12/mo)

---

## Sources

- [WPBeginner: Contact Form 7 vs WPForms](https://www.wpbeginner.com/opinion/contact-form-7-vs-wpforms/) - MEDIUM confidence
- [Contact Form 7 - WordPress.org](https://wordpress.org/plugins/contact-form-7/) - HIGH confidence
- [Zapier: Rank Math vs Yoast SEO 2025](https://zapier.com/blog/rank-math-vs-yoast/) - MEDIUM confidence
- [FooGallery Plugin Comparison 2026](https://fooplugins.com/gallery-plugin-comparison-2026/) - MEDIUM confidence
- [Embed Plus for YouTube - WordPress.org](https://wordpress.org/plugins/youtube-embed-plus/) - HIGH confidence
- [Bible Verse of the Day - WordPress.org](https://wordpress.org/plugins/bible-verse-of-the-day/) - HIGH confidence
- [Sermon Manager - WordPress.org](https://wordpress.org/plugins/sermon-manager-for-wordpress/) - HIGH confidence (CLOSED plugin, confirmed)
- [ChurchThemes: Sermon WordPress Plugins](https://churchthemes.com/sermon-plugins-wordpress/) - MEDIUM confidence
- [GiveWP - WordPress.org](https://wordpress.org/plugins/give/) - HIGH confidence
- [The Events Calendar - WordPress.org](https://wordpress.org/plugins/the-events-calendar/) - HIGH confidence
- [WPForms: Multiple Email Recipients](https://wpforms.com/docs/setup-form-notification-wpforms/) - HIGH confidence
- [Jotform: Best WordPress Church Plugins 2025](https://www.jotform.com/blog/wordpress-church-plug-in/) - MEDIUM confidence
- [Themeisle: WordPress RSS Feed Plugins 2025](https://themeisle.com/blog/wordpress-rss-feed-plugins/) - MEDIUM confidence
