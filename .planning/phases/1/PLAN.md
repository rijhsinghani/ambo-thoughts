# Phase 1: Infrastructure + Launch Site -- Execution Plan

**Phase Goal:** Visitors can access the full Ambo Thoughts site on a secure, performant WordPress VPS with all existing content migrated from GitHub Pages

**Plans:** 6 plans in 3 waves
**Estimated Total Effort:** ~4-6 hours hands-on (mix of automated and manual WordPress admin work)

---

## Wave Structure

| Wave | Plans                     | Can Run In Parallel       | Autonomous                              |
| ---- | ------------------------- | ------------------------- | --------------------------------------- |
| 1    | Plan 01, Plan 02          | Yes                       | No (both have human-action checkpoints) |
| 2    | Plan 03, Plan 04, Plan 05 | Yes (independent files)   | No (all have human-verify checkpoints)  |
| 3    | Plan 06                   | No (depends on all above) | No (final human-verify checkpoint)      |

---

## Dependency Graph

```
Wave 1 (parallel):
  Plan 01: Local WP Setup ──────┐
  Plan 02: VPS Infrastructure ──┤
                                │
Wave 2 (parallel, after 01):    │
  Plan 03: Theme Customization ─┤ (depends on 01)
  Plan 04: Content Migration ───┤ (depends on 01)
  Plan 05: Hero Slider ─────────┤ (depends on 01)
                                │
Wave 3 (sequential):            │
  Plan 06: Deployment ──────────┘ (depends on 02, 03, 04, 05)
```

---

## Plans

### Plan 01: Local WordPress Setup (Wave 1)

- **File:** `1-01-PLAN.md`
- **Goal:** Set up Local by Flywheel site with ChurchWP theme, demo data imported, HEIC images converted, and content extracted for migration
- **Prerequisites:** ChurchWP purchased and downloaded, Local by Flywheel installed
- **Requirements:** REQ-THEME-001, REQ-THEME-002, REQ-THEME-005, REQ-GALLERY-003
- **Tasks:** 2 (1 human-action checkpoint + 1 auto)
- **Key Output:** Running local WordPress with ChurchWP demo baseline

### Plan 02: VPS Infrastructure (Wave 1)

- **File:** `1-02-PLAN.md`
- **Goal:** Provision and harden DigitalOcean VPS with LEMP stack and WordPress installed
- **Prerequisites:** DigitalOcean account with billing
- **Requirements:** REQ-HOSTING-001 through 009, REQ-MIGRATION-001, REQ-ADMIN-006
- **Tasks:** 2 (1 human-action checkpoint + 1 auto)
- **Key Output:** Hardened VPS running WordPress at http://VPS_IP

### Plan 03: Theme Customization (Wave 2)

- **File:** `1-03-PLAN.md`
- **Goal:** Apply Navy/Gold branding, custom header, typography, and navigation to ChurchWP child theme
- **Prerequisites:** Plan 01 complete (Local WP with ChurchWP demo)
- **Requirements:** REQ-THEME-003, REQ-THEME-004, REQ-DESIGN-001, REQ-DESIGN-002, REQ-DESIGN-008, REQ-DESIGN-009
- **Tasks:** 2 (1 auto + 1 human-verify checkpoint)
- **Key Output:** Branded child theme files ready for deployment

### Plan 04: Content Migration (Wave 2)

- **File:** `1-04-PLAN.md`
- **Goal:** Create all pages with migrated content, install gallery/video plugins, configure homepage sections
- **Prerequisites:** Plan 01 complete (Local WP with media and content files ready)
- **Requirements:** REQ-CONTENT-001 through 010, REQ-NEWS-001/002, REQ-SPIRITUALITY-001/002, REQ-GALLERY-001/002/004/005, REQ-DESIGN-005/006/007, REQ-MIGRATION-004
- **Tasks:** 3 (2 auto + 1 human-verify checkpoint)
- **Key Output:** All 8 pages, 2 blog posts, gallery, video embeds, homepage sections

### Plan 05: Hero Slider (Wave 2)

- **File:** `1-05-PLAN.md`
- **Goal:** Configure Revolution Slider with 3 branded slides
- **Prerequisites:** Plan 01 complete (RevSlider imported with demo)
- **Requirements:** REQ-DESIGN-003
- **Tasks:** 2 (1 auto + 1 human-verify checkpoint)
- **Key Output:** 3-slide hero slider on homepage

### Plan 06: Deployment (Wave 3)

- **File:** `1-06-PLAN.md`
- **Goal:** Deploy complete local site to production VPS, configure SEO and backups
- **Prerequisites:** Plans 02, 03, 04, 05 all complete
- **Requirements:** REQ-HOSTING-005, REQ-HOSTING-010, REQ-MIGRATION-002, REQ-MIGRATION-003, REQ-MIGRATION-005
- **Tasks:** 3 (2 auto + 1 human-verify checkpoint)
- **Key Output:** Live site at http://VPS_IP

---

## Requirements Coverage

### Covered in Phase 1 Plans

| Requirement              | Plan | Notes                                          |
| ------------------------ | ---- | ---------------------------------------------- |
| REQ-HOSTING-001          | 02   | DO droplet provisioning                        |
| REQ-HOSTING-002          | 02   | LEMP stack                                     |
| REQ-HOSTING-003          | 02   | Security hardening                             |
| REQ-HOSTING-004          | --   | SSL deferred (no domain)                       |
| REQ-HOSTING-005          | 06   | UpdraftPlus config on production               |
| REQ-HOSTING-006          | 02   | Nginx FastCGI cache                            |
| REQ-HOSTING-007          | 02   | Redis Object Cache                             |
| REQ-HOSTING-008          | 02   | Wordfence installed                            |
| REQ-HOSTING-009          | 02   | wp-config.php env management                   |
| REQ-HOSTING-010          | 06   | Deployment pipeline (rsync + WP-CLI)           |
| REQ-THEME-001            | 01   | ChurchWP parent theme install                  |
| REQ-THEME-002            | 01   | Child theme setup                              |
| REQ-THEME-003            | 03   | Navy/Gold colors                               |
| REQ-THEME-004            | 03   | Playfair Display typography                    |
| REQ-THEME-005            | 01   | PHP 8.3 compatibility test                     |
| REQ-DESIGN-001           | 03   | Header layout                                  |
| REQ-DESIGN-002           | 03   | Navigation menu                                |
| REQ-DESIGN-003           | 05   | Hero slider (3 slides)                         |
| REQ-DESIGN-005           | 04   | Homepage gallery section                       |
| REQ-DESIGN-006           | 04   | Homepage church news section                   |
| REQ-DESIGN-007           | 04   | Homepage bio section                           |
| REQ-DESIGN-008           | 03   | Remove irrelevant sections                     |
| REQ-DESIGN-009           | 03   | Branding text                                  |
| REQ-CONTENT-001..010     | 04   | All page content                               |
| REQ-NEWS-001/002         | 04   | Vatican News + Diocese links                   |
| REQ-SPIRITUALITY-001/002 | 04   | Hero image + gospel quote                      |
| REQ-GALLERY-001..005     | 04   | Gallery, photos, video embed                   |
| REQ-GALLERY-003          | 01   | HEIC conversion                                |
| REQ-MIGRATION-001        | 02   | URL redirects (Nginx)                          |
| REQ-MIGRATION-002        | 06   | SEO (Rank Math)                                |
| REQ-MIGRATION-003        | 06   | DNS cutover (deferred until domain)            |
| REQ-MIGRATION-004        | 04   | Content transfer                               |
| REQ-MIGRATION-005        | 06   | GitHub Pages decommission (after verification) |
| REQ-ADMIN-006            | 02   | Plugin blacklist enforced                      |

### Explicitly Deferred (per CONTEXT.md)

| Requirement           | Reason                                                 |
| --------------------- | ------------------------------------------------------ |
| REQ-HOSTING-004 (SSL) | No domain yet -- SSL requires domain for Let's Encrypt |
| REQ-CONTACT-001..004  | Contact form deferred per user request                 |
| REQ-DESIGN-004        | Latest Homilies section -- Phase 2 (needs Homily CPT)  |

---

## Execution Order

1. Start Plans 01 and 02 in parallel (Wave 1)
2. After Plan 01 completes, start Plans 03, 04, 05 in parallel (Wave 2)
3. After Plans 02 + 03 + 04 + 05 all complete, run Plan 06 (Wave 3)

**Critical path:** Plan 01 -> Plan 04 -> Plan 06 (content migration is the longest chain)

---

## Success Criteria (Phase 1)

1. Site loads at production VPS IP over HTTP (SSL deferred -- no domain yet)
2. All 8 pages display correctly with Navy/Gold branding
3. Contact form is SKIPPED (deferred per user request)
4. Homepage hero slider cycles through 3 slides
5. Google crawling/SEO deferred until domain is set up (Rank Math + sitemap ready)
