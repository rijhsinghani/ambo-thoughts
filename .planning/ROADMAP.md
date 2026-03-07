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
**Requirements**: HOSTING-\*, THEME-\*, DESIGN-\*, CONTENT-\*, NEWS-\*, SPIRITUALITY-\*, GALLERY-\*, MIGRATION-\*, ADMIN-006
**Estimated Complexity**: L (largest phase -- server setup, theme customization, 8+ pages of content migration, DNS cutover)

**Success Criteria** (updated per user decisions):

1. Site loads at production VPS IP over HTTP (SSL deferred -- no domain yet)
2. All 8 pages display correctly with Navy/Gold branding
3. Contact form is SKIPPED (deferred per user request)
4. Homepage hero slider cycles through 3 slides (Ambo Thoughts, St. Francis quote, Psalm 46:10)
5. Google crawling/SEO deferred until domain is set up (Rank Math + sitemap ready)

**Plans:** 6 plans in 3 waves

Plans:

- [ ] 1-01-PLAN.md -- Local WordPress setup (Local by Flywheel + ChurchWP + demo import + HEIC conversion)
- [ ] 1-02-PLAN.md -- VPS infrastructure (DO droplet + LEMP stack + security hardening + WordPress install)
- [ ] 1-03-PLAN.md -- Theme customization (Navy/Gold colors + header + typography + navigation)
- [ ] 1-04-PLAN.md -- Content migration (all 8 pages + gallery + video embeds + homepage sections)
- [ ] 1-05-PLAN.md -- Hero slider (3-slide Revolution Slider configuration)
- [ ] 1-06-PLAN.md -- Deployment (rsync to VPS + SEO + backups + final verification)

---

### Phase 2: Homily Content System

**Goal**: Homilies are structured content with liturgical metadata, browsable by visitors and publishable via the automated pipeline
**Depends on**: Phase 1 (WordPress must be running on production)
**Requirements**: HOMILY-\*, PIPELINE-\*, TAXONOMY-\*
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
**Requirements**: ADMIN-\*, MONITOR-\*, DOCS-\*
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
| 1. Infrastructure + Launch Site          | 0/6            | Planned     | -         |
| 2. Homily Content System                 | 0/?            | Not started | -         |
| 3. Admin Handoff + Operational Hardening | 0/?            | Not started | -         |

---

## Coverage

| Category        | Phase | Description                                                              |
| --------------- | ----- | ------------------------------------------------------------------------ |
| HOSTING-\*      | 1     | VPS provisioning, Nginx, PHP-FPM, MariaDB, Redis                         |
| THEME-\*        | 1     | ChurchWP child theme, Navy/Gold CSS, header/footer                       |
| DESIGN-\*       | 1     | Hero slider, homepage sections, page layouts                             |
| CONTENT-\*      | 1     | Page content migration (all 8 pages), photo gallery, video embeds        |
| NEWS-\*         | 1     | Vatican News + Diocese of Trenton links                                  |
| SPIRITUALITY-\* | 1     | Hero image, gospel quote                                                 |
| GALLERY-\*      | 1     | FooGallery, HEIC conversion, image compression, video embed              |
| MIGRATION-\*    | 1     | URL redirects, SEO, DNS cutover, content transfer                        |
| HOMILY-\*       | 2     | Custom Post Type, single/archive templates                               |
| PIPELINE-\*     | 2     | REST API endpoint, process_homilies.py adaptation, Application Passwords |
| TAXONOMY-\*     | 2     | Liturgical season taxonomy, scripture references, meta fields            |
| ADMIN-\*        | 3     | Editor role, simplified admin panel, activity logging                    |
| MONITOR-\*      | 3     | UptimeRobot, disable auto-updates                                        |
| DOCS-\*         | 3     | Training document, maintenance runbook                                   |
