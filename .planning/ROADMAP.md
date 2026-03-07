# ROADMAP: Ambo Thoughts WordPress Redesign

**Milestone:** v1 -- WordPress Launch
**Phases:** 3
**Granularity:** Coarse

---

## Phases

- [ ] **Phase 1: Infrastructure + Launch Site** - Secure VPS with themed WordPress, all existing content migrated, SSL cutover from GitHub Pages
- [ ] **Phase 2: Homily Content System** - Custom Post Type for homilies with pipeline integration and liturgical taxonomy
- [ ] **Phase 3: Admin Handoff + Operational Hardening** - Editor role, monitoring, training docs, maintenance runbook

---

## Phase Details

### Phase 1: Infrastructure + Launch Site

**Goal**: Visitors can access the full Ambo Thoughts site on a secure, performant WordPress VPS with all existing content migrated from GitHub Pages
**Depends on**: Nothing (first phase). Requires user to purchase ChurchWP theme and provision DigitalOcean droplet.
**Requirements**: HOSTING-_, THEME-_, DESIGN-_, CONTENT-_, SEO-_, SECURITY-_, BACKUP-_, MIGRATE-_
**Estimated Complexity**: L (largest phase -- server setup, theme customization, 8+ pages of content migration, DNS cutover)

**Success Criteria** (what must be TRUE when this phase completes):

1. The site loads at the production domain over HTTPS with no mixed-content warnings
2. All 8 pages (About, Spirituality, Church News, Contact, Pictures, Prayer Partner, Stuff, Videos) display their content correctly with Navy/Gold branding
3. The contact form delivers messages to both deacon267@verizon.net and hcugini@stroberts.cc
4. The homepage hero slider cycles through all 3 slides (Ambo Thoughts, St. Francis quote, Psalm 46:10)
5. Google can crawl the site (sitemap submitted, Rank Math configured, old .html URLs redirect to new permalinks)

**Plans**: TBD

---

### Phase 2: Homily Content System

**Goal**: Homilies are structured content with liturgical metadata, browsable by visitors and publishable via the automated pipeline
**Depends on**: Phase 1 (WordPress must be running on production)
**Requirements**: HOMILY-_, PIPELINE-_, TAXONOMY-\*
**Estimated Complexity**: M (CPT registration, two templates, REST API endpoint, pipeline adaptation, Bible verse widget)

**Success Criteria** (what must be TRUE when this phase completes):

1. A visitor can browse homilies filtered by liturgical season (Advent, Lent, Easter, Ordinary Time) on the archive page
2. Each homily page displays the embedded YouTube video, pull quote, scripture references, and transcript
3. The `process_homilies.py` pipeline can create a new homily post via REST API using Application Passwords, and it appears on the site within seconds
4. The Spirituality page displays a daily Bible verse that updates automatically

**Plans**: TBD

---

### Phase 3: Admin Handoff + Operational Hardening

**Goal**: Deacon Henry can independently manage site content, and the site runs reliably with monitoring and documented maintenance procedures
**Depends on**: Phase 2 (all features must be complete before handoff)
**Requirements**: ADMIN-_, MONITOR-_, DOCS-\*
**Estimated Complexity**: S (configuration and documentation, no new features)

**Success Criteria** (what must be TRUE when this phase completes):

1. Deacon Henry can log in as Editor, create/edit pages and posts, and upload images -- but cannot install plugins, change themes, or modify settings
2. UptimeRobot sends an alert when the site goes down
3. A maintenance runbook exists covering monthly updates, backup verification, and emergency recovery steps

**Plans**: TBD

---

## Progress

| Phase                                    | Plans Complete | Status      | Completed |
| ---------------------------------------- | -------------- | ----------- | --------- |
| 1. Infrastructure + Launch Site          | 0/?            | Not started | -         |
| 2. Homily Content System                 | 0/?            | Not started | -         |
| 3. Admin Handoff + Operational Hardening | 0/?            | Not started | -         |

---

## Coverage

Requirements are referenced by category (REQUIREMENTS.md is being written in parallel).
Cross-reference will be completed after both files exist.

| Category    | Phase | Description                                                              |
| ----------- | ----- | ------------------------------------------------------------------------ |
| HOSTING-\*  | 1     | VPS provisioning, Nginx, PHP-FPM, MariaDB, Redis                         |
| THEME-\*    | 1     | ChurchWP child theme, Navy/Gold CSS, header/footer                       |
| DESIGN-\*   | 1     | Hero slider, homepage sections, page layouts                             |
| CONTENT-\*  | 1     | Page content migration (all 8 pages), photo gallery, video embeds        |
| SEO-\*      | 1     | Rank Math, sitemaps, redirects from old URLs                             |
| SECURITY-\* | 1     | SSH hardening, UFW, fail2ban, Wordfence, file permissions                |
| BACKUP-\*   | 1     | UpdraftPlus to Google Drive                                              |
| MIGRATE-\*  | 1     | DNS cutover, SSL, old URL redirects, GitHub Pages deprecation            |
| HOMILY-\*   | 2     | Custom Post Type, single/archive templates                               |
| PIPELINE-\* | 2     | REST API endpoint, process_homilies.py adaptation, Application Passwords |
| TAXONOMY-\* | 2     | Liturgical season taxonomy, scripture references, meta fields            |
| ADMIN-\*    | 3     | Editor role, simplified admin panel, activity logging                    |
| MONITOR-\*  | 3     | UptimeRobot, disable auto-updates                                        |
| DOCS-\*     | 3     | Training document, maintenance runbook                                   |
