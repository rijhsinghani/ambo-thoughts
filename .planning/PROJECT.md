# PROJECT: Ambo Thoughts WordPress Redesign

## Overview

Complete redesign of the Ambo Thoughts website using WordPress with the ChurchWP theme on a self-managed VPS. Replaces the current static HTML + GitHub Pages + Decap CMS approach with a full WordPress CMS that a non-technical admin can manage independently.

**Client:** Deacon Henry Cugini, Diocese of Trenton
**Site purpose:** Spiritual Direction & Bereavement ministry
**Current site:** WordPress on GCP e2-micro (http://104.196.102.152) — ChurchWP theme with Navy/Gold child theme
**Previous site:** Static HTML on GitHub Pages (rijhsinghani.github.io/ambo-thoughts) — retired

## Key Decisions

| Decision     | Choice                                          | Rationale                                                |
| ------------ | ----------------------------------------------- | -------------------------------------------------------- |
| Platform     | WordPress                                       | Full CMS, admin-friendly, plugin ecosystem               |
| Theme        | ChurchWP (ThemeForest, ~$59)                    | Dark/elegant church design matching vision               |
| Hosting      | GCP e2-micro VM (104.196.102.152)               | Free tier eligible, full control                         |
| Dev approach | Direct on server via SSH + WP-CLI               | No local dev environment needed                          |
| Color scheme | Navy (#001f5b) & Gold (#c9a84c)                 | Replace ChurchWP green with blue/navy, keep gold accents |
| Typography   | Playfair Display (headings), system sans (body) | Matches existing elegant feel                            |

## Branding

- **H1:** "Ambo Thoughts"
- **H2:** "Spiritual Direction & Bereavement"
- **H2:** "with Deacon Cugini"
- **Spelling:** "Ambo Thoughts" (ambo = church pulpit/lectern)

## Design Specifications

### Color Variables (from existing CSS)

```css
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
```

### Header

- Cross logo centered (existing: `images/deacons-cross.png`)
- Remove phone/address from ChurchWP default header
- Navy background, white border (make bigger)
- Menu extends right for multi-word items (Home, Homilies, Spirituality, Church News, About, Stuff, Prayer Partner, Contact)

### Hero Slider (3 slides)

1. **"Ambo Thoughts"** / Subtitles: Spirituality, Bereavement
2. **"Preach the Gospel at all times; use words when necessary."** / St. Francis of Assisi
3. **"Be still, and know that I am God"** / Psalm 46:10

### Homepage Sections (previews linking to full pages)

1. **Latest Homilies** — Label as "Homilies" (not "Sermons"). Dependent on video homilies pipeline (`scripts/process_homilies.py`). Show latest video homily cards.
2. **Gallery** — "New Life in the Spirit" theme. Featured video: YouTube embed `_a_zLTOxr0o`.
3. **Church News** — Buttons linking to VaticanNews.com and dioceseoftrenton.org/news
4. **Bio section** — Reuse existing about content (Deacon Henry bio, ordination 2008, Co-Cathedral of St. Robert Bellarmine, Freehold NJ)
5. **Cut:** "church love, faith love" section from ChurchWP template — not relevant

### Pages

| Page                 | Key Content                                                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Homilies**         | Book cover photo as main image, buttons per homily. Connected to video pipeline.                                                                     |
| **Spirituality**     | Hero from "Spirituality Hero.heic", "Preach the gospel" quote (no watermark). Investigate RSS feeds (verseoftheday.com, daily Catholic bible verse). |
| **Church News**      | External links to VaticanNews.com and dioceseoftrenton.org/news                                                                                      |
| **About**            | Existing bio content — ordained 2008, Diocese of Trenton, ministries list                                                                            |
| **Gallery/Pictures** | Photo gallery from /Hank/ directory                                                                                                                  |
| **Contact**          | Form to deacon267@verizon.net AND hcugini@stroberts.cc                                                                                               |
| **Prayer Partner**   | Prayer chain signup/info                                                                                                                             |
| **Stuff**            | Miscellaneous content                                                                                                                                |
| **Videos**           | Video homilies archive                                                                                                                               |

### Photos (source: iCloud `/Hank/` directory)

- `Cover.jpeg`, `Cover2.HEIC`, `Cover3.jpg` (in `/Sameer/Edited/`)
- `Spirituality Hero.heic`, `Hero-1.HEIC`
- `High Res/` directory (Easter Vigil, Midnight Mass photos)
- Note: HEIC images must be converted to web formats (JPEG/WebP) for WordPress

## Content (Now on WordPress)

All content has been migrated from static HTML to WordPress pages managed via WPBakery Page Builder.

### WordPress Pages (by Post ID)

| Page         | WP Admin URL                                                   |
| ------------ | -------------------------------------------------------------- |
| Homepage     | http://104.196.102.152/wp-admin/post.php?post=6706&action=edit |
| Homilies     | http://104.196.102.152/wp-admin/post.php?post=6709&action=edit |
| Spirituality | http://104.196.102.152/wp-admin/post.php?post=6710&action=edit |
| About        | http://104.196.102.152/wp-admin/post.php?post=6707&action=edit |

### About Bio

Deacon Henry Cugini — ordained Roman Catholic Permanent Deacon, Diocese of Trenton. Ordained by Bishop Smith on May 8, 2008. Assigned to Co-Cathedral of St. Robert Bellarmine, Freehold, NJ. Ministries: Spiritual Direction, Annulment Advocate, Hospital/Homebound, Bereavement. Certified Spiritual Director, Pastoral Counselor, Bereavement Counselor/Facilitator. Professed member of Third Order of St. Francis (Secular Franciscan).

**Motto:** "Preach the Gospel at all times and if necessary use words..."

### YouTube Channel

- Featured video: "New Life In the Spirit" (`_a_zLTOxr0o`)
- Homily pipeline exists: `scripts/process_homilies.py` (uses YouTube Data API + Google Drive API)

### External Links

- VaticanNews.com
- dioceseoftrenton.org/news
- Contact emails: deacon267@verizon.net, hcugini@stroberts.cc

## Technical Context

### WordPress Stack

- **Server:** GCP e2-micro VM (104.196.102.152), Ubuntu 24.04
- **Web server:** Nginx 1.28.1 + PHP-FPM 8.3
- **Database:** MariaDB 10.11
- **Cache:** Redis object cache
- **Theme:** ChurchWP (parent) + churchwp-child (Navy/Gold customizations)
- **Page builder:** WPBakery (js_composer)
- **Key plugins:** Wordfence, UpdraftPlus, Rank Math SEO, RevSlider, FooGallery, TinyMCE Advanced

### Homily Pipeline

- `scripts/process_homilies.py` — YouTube homily processing pipeline
- `scripts/config.py` — Pipeline configuration
- Uses Application Default Credentials (ADC) for Google APIs
- Scopes: youtube.upload, youtube, drive.readonly

### Legacy Static Site (retired)

The original static HTML files (`index.html`, `blog.html`, etc.) remain in this repo for reference but are no longer the live site. All content is now managed in WordPress at http://104.196.102.152.

## Prerequisites (Completed)

- [x] Purchase ChurchWP from ThemeForest (~$59)
- [x] Provision GCP e2-micro VM (104.196.102.152)
- [x] Install LEMP stack + WordPress
- [ ] Confirm domain name (pending)

## Milestone: v1 — WordPress Launch

Replace static site with fully functional WordPress site on VPS with all existing content migrated, ChurchWP theme customized to Navy/Gold design, and admin access configured for Deacon Henry.
