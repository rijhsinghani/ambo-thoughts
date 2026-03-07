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
| Security                  | Self-managed VPS requires it        | Low        | Wordfence (free)              |
| Backups                   | Disaster recovery for VPS           | Low        | UpdraftPlus (free)            |
| Analytics                 | Understand visitor behavior         | Low        | Google Site Kit (free)        |
| SSL/HTTPS                 | Browser trust, SEO signal           | Low        | Let's Encrypt on VPS          |

## Differentiators

Features that elevate beyond a basic church brochure site.

| Feature                           | Value Proposition                    | Complexity | Recommended Solution                                   |
| --------------------------------- | ------------------------------------ | ---------- | ------------------------------------------------------ |
| Homily video pipeline integration | Auto-publish from YouTube channel    | Medium     | Custom integration with existing `process_homilies.py` |
| Prayer Partner signup             | Community engagement, return visits  | Low        | WPForms Lite or CF7 additional form                    |
| Liturgical season organization    | Navigate homilies by church calendar | Medium     | Custom taxonomy on CPT                                 |
| Church news aggregation           | One-stop for Vatican/Diocese news    | Low        | RSS block or curated links page                        |
| Hero slider with quotes           | Inspirational first impression       | Low        | ChurchWP built-in slider                               |
| Social sharing on homilies        | Parishioners share sermons           | Low        | AddToAny (free, 1.2KB footprint)                       |

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
| Accessibility overlay plugin    | FTC fined AccessiBe $1M in Jan 2025 for deceptive claims; overlays don't work     | Build accessibility into theme/content properly             |

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

**Why not Yoast:** Yoast's free version is deliberately crippled to push premium. For a ministry site that will never pay for SEO premium, Rank Math Free gives substantially more out of the box. Multiple independent comparisons (Kinsta, Zapier, Rank Fuse) confirm Rank Math's free tier is more feature-complete.

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
- Best Core Web Vitals scores among free gallery plugins (2026 comparison)

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

**Alternative approach:** WordPress natively embeds YouTube URLs as responsive iframes. For a site with only a few videos per page, the native embed + a general lazy-load plugin may be sufficient. Embed Plus is recommended because it consolidates video-specific optimizations in one plugin.

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

### 7. Security: Wordfence (Free)

**Recommendation: Use Wordfence Free** because it provides server-level firewall and malware scanning, which is critical for a self-managed VPS where no hosting company is providing security.

| Attribute       | Detail     |
| --------------- | ---------- |
| Cost            | Free       |
| Active Installs | 5,000,000+ |
| Rating          | 4.7/5      |
| Confidence      | HIGH       |

**Why Wordfence over Sucuri for this site:**

- **Wordfence is local (server-side):** On a self-managed VPS, you want deep file-level scanning, login protection, and firewall rules running on the server itself. Wordfence integrates at the PHP level and can detect file changes, brute-force attempts, and malware in real time.
- **Sucuri is cloud-based (DNS proxy):** Sucuri's WAF requires routing DNS through their CDN, which adds complexity for a simple VPS setup. Its free plugin only offers post-hack auditing -- the WAF is premium only ($199/yr).
- **Free tier is generous:** Wordfence Free includes the full Web Application Firewall (WAF), malware scanner, login security (2FA, reCAPTCHA), and brute-force protection. The only limitation: firewall rules update 30 days after premium users get them.

**Critical VPS-specific setup:**

- Enable brute-force protection (limit login attempts)
- Set up 2FA for admin login (built into Wordfence Free)
- Configure weekly malware scans
- Block XML-RPC if not needed (common WordPress attack vector)

**Why not Sucuri:** Cloud WAF requires DNS changes and costs $199/yr. For a small ministry site on a VPS, Wordfence's server-level protection is more appropriate and free.

### 8. Backup: UpdraftPlus (Free)

**Recommendation: Use UpdraftPlus Free** for automated backups to remote storage.

| Attribute       | Detail     |
| --------------- | ---------- |
| Cost            | Free       |
| Active Installs | 3,000,000+ |
| Rating          | 4.8/5      |
| Confidence      | HIGH       |

**Why UpdraftPlus:**

- Most popular WordPress backup plugin (3M+ installs)
- Free tier includes scheduled backups to Google Drive, Dropbox, Amazon S3, or FTP
- One-click restore from within WordPress admin
- Separates database and file backups for flexibility

**Recommended backup schedule:**

- Database: Daily (small, fast)
- Files: Weekly (larger, includes uploads/media)
- Retention: Keep 4 weeks of backups
- Destination: Google Drive (free 15GB is more than enough for this site)

**VPS-specific note:** Since this is a self-managed VPS (not managed hosting), backups are entirely your responsibility. There is no hosting company running backups for you. UpdraftPlus is non-negotiable for disaster recovery.

### 9. Caching: WP Super Cache (Free)

**Recommendation: Use WP Super Cache** for page caching on the VPS.

| Attribute       | Detail     |
| --------------- | ---------- |
| Cost            | Free       |
| Active Installs | 2,000,000+ |
| Rating          | 4.3/5      |
| Confidence      | HIGH       |

**Why WP Super Cache over alternatives:**

- **Simple mode** requires near-zero configuration -- perfect for a non-technical admin
- Generates static HTML files served directly by Apache/Nginx, bypassing PHP entirely
- Lightweight with minimal server resource usage on a small VPS
- Made by Automattic (WordPress.com parent company)
- Includes GZIP compression and browser caching

**Why not LiteSpeed Cache:** LiteSpeed Cache is superior BUT only if the VPS runs LiteSpeed/OpenLiteSpeed web server. If the VPS runs Apache or Nginx (far more common), LiteSpeed Cache loses its core advantage. WP Super Cache works with any web server.

**Why not W3 Total Cache:** Extremely powerful but complex to configure. W3TC's settings panel overwhelms non-technical admins. WP Super Cache's "Simple" mode checkbox is all that's needed.

**Why not WP Rocket:** Premium only ($59/yr). Not justified for a small ministry site when WP Super Cache handles the basics for free.

**VPS optimization note:** If the VPS runs Nginx, server-level caching (fastcgi_cache) is more efficient than any plugin. But WP Super Cache provides a good baseline that works regardless of server software.

### 10. Analytics: Google Site Kit (Free)

**Recommendation: Use Google Site Kit** for analytics. It is Google's official WordPress plugin.

| Attribute       | Detail     |
| --------------- | ---------- |
| Cost            | Free       |
| Active Installs | 4,000,000+ |
| Rating          | 4.0/5      |
| Confidence      | HIGH       |

**Why Site Kit over MonsterInsights:**

- **Official Google plugin:** Direct integration with Google Analytics (GA4), Search Console, PageSpeed Insights, and AdSense -- all from one dashboard
- **Completely free:** MonsterInsights locks useful features (event tracking, popular posts) behind a $99.60/yr Pro tier
- **Simpler for this use case:** A ministry site needs pageviews, top pages, and traffic sources. Site Kit provides this in the WordPress dashboard without complexity
- **No third-party dependency:** Data flows directly from Google, not through MonsterInsights' servers

**Why not MonsterInsights:** MonsterInsights has better in-dashboard reporting, but the free version is limited and the premium is expensive. For a ministry site where Deacon Henry (or his admin) just needs to see "how many people visited this week," Site Kit is sufficient and free.

**Setup requirements:**

- Google Analytics 4 (GA4) property (create via analytics.google.com)
- Google Search Console verification (Site Kit handles this automatically)
- Measurement ID added via the plugin's setup wizard

### 11. Social Sharing: AddToAny (Free)

**Recommendation: Use AddToAny Share Buttons** for lightweight social sharing on homily posts and blog pages.

| Attribute       | Detail   |
| --------------- | -------- |
| Cost            | Free     |
| Active Installs | 500,000+ |
| Rating          | 4.4/5    |
| Confidence      | HIGH     |

**Why AddToAny:**

- Adds only 1.2KB to page load -- negligible performance impact
- SVG icons (vector, no image requests)
- Supports 100+ sharing services (Facebook, Twitter/X, email, WhatsApp, Pinterest, etc.)
- No account needed, no tracking, no ads
- Configurable placement (below posts, floating sidebar, etc.)

**Best placement for this site:**

- Below each homily post (share sermons with parishioners)
- On the blog/news pages
- NOT on the contact page or static info pages (unnecessary there)

**Why not Sassy Social Share:** Similar quality but AddToAny has a larger install base and longer track record. Both are fine choices.

### 12. Cookie Consent / Privacy Policy

**Recommendation: Use GDPR Cookie Compliance by Moove Agency** for cookie consent, plus create a Privacy Policy page.

| Attribute       | Detail               |
| --------------- | -------------------- |
| Cost            | Free (Pro available) |
| Active Installs | 200,000+             |
| Rating          | 4.7/5                |
| Confidence      | MEDIUM               |

**Why this matters for a church site:**

- If using Google Analytics (GA4), you are setting cookies that require consent under GDPR/ePrivacy
- Church sites serve a broad audience including international visitors
- A cookie banner + privacy policy demonstrates responsibility and trust

**Why GDPR Cookie Compliance (Moove):**

- Clean, customizable banner that matches site branding
- Blocks scripts (GA4, YouTube embeds) until consent is given
- Built-in cookie scanner
- Generates privacy policy template content
- WCAG-accessible banner design

**Privacy Policy page:**

- WordPress has a built-in Privacy Policy page template (Settings > Privacy)
- Customize it to mention: contact form data collection, Google Analytics, YouTube embeds, and any cookies
- Link it in the site footer

**Alternative: CookieYes** (1M+ installs) is also excellent and has a larger user base, but its free tier has a 100 pages/month scan limit. Moove has no such limit.

### 13. Accessibility (ADA Compliance)

**Recommendation: Do NOT use an accessibility overlay plugin.** Build accessibility into the theme and content instead.

| Attribute  | Detail                                               |
| ---------- | ---------------------------------------------------- |
| Cost       | Free (built into good practices)                     |
| Complexity | Low-Medium (mostly content and theme decisions)      |
| Confidence | HIGH (FTC enforcement actions confirm overlay risks) |

**Why overlays are harmful:**

- The FTC fined AccessiBe $1M in January 2025 for deceptive marketing about their AI accessibility widget
- Overlay plugins inject JavaScript that interferes with screen readers and keyboard navigation
- They create a false sense of compliance without fixing underlying HTML issues
- The National Federation of the Blind and other disability organizations actively oppose overlays

**What to do instead (built into implementation):**

1. **Choose an accessible theme:** ChurchWP should be tested for WCAG 2.1 AA compliance. Check for proper heading hierarchy, color contrast, keyboard navigation
2. **Alt text on all images:** When uploading church photos, always fill in the alt text field
3. **Color contrast:** Verify that Navy/Gold color scheme meets WCAG AA contrast ratios (4.5:1 for text). Use WebAIM's contrast checker
4. **Form labels:** Contact Form 7 generates accessible forms with proper `<label>` elements by default
5. **Video captions:** YouTube auto-generates captions for homily videos. Verify they're enabled
6. **Heading structure:** Use H1 > H2 > H3 hierarchy properly (don't skip levels for styling)
7. **Link text:** Use descriptive link text ("Read today's Mass readings") not "click here"

**Testing tool:** Install WP ADA Compliance Check Basic (free plugin, 10K+ installs) for automated scanning of accessibility issues during development. Remove it after launch if desired -- it's a development tool, not a runtime solution.

### 14. Church News Aggregation: Static Links Page (No Plugin)

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

### 15. Additional Infrastructure Plugins

| Plugin           | Purpose                                  | Cost | Installs | Notes                                                |
| ---------------- | ---------------------------------------- | ---- | -------- | ---------------------------------------------------- |
| **WP Mail SMTP** | Reliable email delivery for contact form | Free | 4M+      | Critical -- VPS mail often goes to spam without SMTP |
| **Flamingo**     | Store CF7 submissions in DB              | Free | 500K+    | Backup in case email delivery fails                  |
| **Smush**        | Image compression on upload              | Free | 1M+      | Auto-compress church photos on upload                |

---

## Feature Dependencies

```
Contact Form 7 --> WP Mail SMTP (email delivery depends on SMTP config)
Contact Form 7 --> Flamingo (submission storage as backup)
Homily CPT --> Embed Plus for YouTube (homily display includes video)
FooGallery --> Smush (gallery photos should be compressed)
Rank Math --> Google Search Console (setup wizard connects them)
Google Site Kit --> GA4 Property (must create in Google Analytics first)
GDPR Cookie Compliance --> Google Site Kit (must block GA4 until consent given)
GDPR Cookie Compliance --> Embed Plus (must block YouTube cookies until consent)
All features --> Wordfence + UpdraftPlus (security and backup are prerequisites)
```

## MVP Recommendation

**Phase 1 (Launch):** Get the site live with all existing content migrated.

Prioritize:

1. ChurchWP theme installed and customized (Navy/Gold)
2. Contact Form 7 with dual-email delivery + WP Mail SMTP + Flamingo
3. All static pages migrated (About, Spirituality, Church News, Prayer Partner, Stuff)
4. FooGallery for the Pictures page
5. Embed Plus for YouTube videos on Videos page
6. Rank Math SEO configured
7. Infrastructure plugins (Wordfence, UpdraftPlus, WP Super Cache, Smush)
8. Privacy Policy page + GDPR Cookie Compliance banner
9. Google Site Kit (GA4)

**Phase 2 (Content System):** Structured homily management and enhancements.

10. Homily Custom Post Type with taxonomies
11. YouTube integration in homily posts
12. Bible Verse of the Day on Spirituality page
13. AddToAny social sharing on homily posts
14. Connect existing `process_homilies.py` pipeline to create WordPress posts via REST API
15. Accessibility audit with WP ADA Compliance Check

**Defer:**

- Online donations: Not requested, parish has own system
- Event calendar: No events to manage currently
- RSS aggregation: Static links page is sufficient
- Member portal: Not applicable for this ministry

## Plugin Count Summary

**Total recommended plugins: 14** (all free tier)

| Category       | Plugin                 | Status | Phase |
| -------------- | ---------------------- | ------ | ----- |
| Contact        | Contact Form 7         | Free   | 1     |
| Contact backup | Flamingo               | Free   | 1     |
| Email          | WP Mail SMTP           | Free   | 1     |
| SEO            | Rank Math              | Free   | 1     |
| Gallery        | FooGallery             | Free   | 1     |
| Video          | Embed Plus for YouTube | Free   | 1     |
| Security       | Wordfence              | Free   | 1     |
| Backup         | UpdraftPlus            | Free   | 1     |
| Performance    | WP Super Cache         | Free   | 1     |
| Images         | Smush                  | Free   | 1     |
| Analytics      | Google Site Kit        | Free   | 1     |
| Privacy        | GDPR Cookie Compliance | Free   | 1     |
| Devotional     | Bible Verse of the Day | Free   | 2     |
| Social         | AddToAny Share Buttons | Free   | 2     |

**Total recurring cost: $0** (all free plugins + ChurchWP one-time $59 + VPS $5-12/mo)

---

## Sources

- [WPBeginner: Contact Form 7 vs WPForms](https://www.wpbeginner.com/opinion/contact-form-7-vs-wpforms/) - MEDIUM confidence
- [Contact Form 7 - WordPress.org](https://wordpress.org/plugins/contact-form-7/) - HIGH confidence
- [Zapier: Rank Math vs Yoast SEO 2025](https://zapier.com/blog/rank-math-vs-yoast/) - MEDIUM confidence
- [Kinsta: Rank Math vs Yoast](https://kinsta.com/blog/rank-math-vs-yoast/) - MEDIUM confidence
- [FooGallery Plugin Comparison 2026](https://fooplugins.com/gallery-plugin-comparison-2026/) - MEDIUM confidence
- [Embed Plus for YouTube - WordPress.org](https://wordpress.org/plugins/youtube-embed-plus/) - HIGH confidence
- [Bible Verse of the Day - WordPress.org](https://wordpress.org/plugins/bible-verse-of-the-day/) - HIGH confidence
- [Sermon Manager - WordPress.org](https://wordpress.org/plugins/sermon-manager-for-wordpress/) - HIGH confidence (CLOSED plugin, confirmed)
- [ChurchThemes: Sermon WordPress Plugins](https://churchthemes.com/sermon-plugins-wordpress/) - MEDIUM confidence
- [Kinsta: Sucuri vs Wordfence](https://kinsta.com/blog/sucuri-vs-wordfence/) - MEDIUM confidence
- [WPBeginner: Wordfence vs Sucuri](https://www.wpbeginner.com/opinion/wordfence-vs-sucuri-which-one-is-better-compared/) - MEDIUM confidence
- [UpdraftPlus - WordPress.org](https://wordpress.org/plugins/updraftplus/) - HIGH confidence
- [SuperSoju: WordPress Caching Plugin Comparison](https://supersoju.com/blog/2025/10/03/wordpress-caching-plugin-comparison-w3-total-cache-vs-wp-rocket-vs-wp-super-cache-vs-litespeed-cache/) - MEDIUM confidence
- [WPBeginner: MonsterInsights vs Site Kit](https://www.wpbeginner.com/opinion/monsterinsights-vs-site-kit/) - MEDIUM confidence
- [Sassy Social Share - WordPress.org](https://wordpress.org/plugins/sassy-social-share/) - HIGH confidence
- [WPBeginner: Best Social Media Plugins 2026](https://www.wpbeginner.com/plugins/best-social-media-plugins-for-wordpress/) - MEDIUM confidence
- [Moove GDPR Cookie Compliance](https://www.mooveagency.com/wordpress-plugins/gdpr-cookie-compliance/) - HIGH confidence
- [CookieYes - WordPress.org](https://www.cookieyes.com/product/wordpress-plugin/) - HIGH confidence
- [Equalize Digital: WordPress ADA Compliance Plugin Myth](https://equalizedigital.com/dont-fall-for-the-wordpress-ada-compliance-plugin-myth/) - MEDIUM confidence
- [AccessibilityChecker: WordPress ADA Compliance](https://www.accessibilitychecker.org/guides/wordpress-accessibility/) - MEDIUM confidence
- [Jotform: Best WordPress Church Plugins 2026](https://www.jotform.com/blog/wordpress-church-plug-in/) - MEDIUM confidence
- [ILOVEWP: Most Popular WordPress Plugins for Churches 2026](https://www.ilovewp.com/resources/wordpress-for-churches/most-popular-wordpress-plugins-for-churches/) - MEDIUM confidence
