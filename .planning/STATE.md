# Project State

**Project:** Ambo Thoughts WordPress Redesign
**Milestone:** v1 — WordPress Launch
**Current Phase:** 1 (Infrastructure + Launch Site)
**Status:** IN PROGRESS
**Current Plan:** 1-02 (complete)

## Phase Progress

| Phase | Name                                  | Status      | Notes                        |
| ----- | ------------------------------------- | ----------- | ---------------------------- |
| 1     | Infrastructure + Launch Site          | IN PROGRESS | Plan 02 complete (LEMP + WP) |
| 2     | Homily Content System                 | BLOCKED     | Depends on Phase 1           |
| 3     | Admin Handoff + Operational Hardening | BLOCKED     | Depends on Phase 2           |
| 4     | Video Blog                            | BLOCKED     | Depends on Phase 1           |

## Prerequisites

- [x] Purchase ChurchWP theme from ThemeForest (~$59)
- [x] Provision GCP e2-micro VM (104.196.102.152)
- [x] Install LEMP stack + WordPress
- [x] Content migration from static HTML to WordPress
- [ ] Confirm domain name (pending)

## Open Questions

See `.planning/research/SUMMARY.md` § Open Questions for full list.

## Recent Activity

- 2026-03-07: Project initialized — PROJECT.md, config.json, research (4 agents), REQUIREMENTS.md (62 reqs), ROADMAP.md (3 phases)
- 2026-03-07: Added Phase 4 (Video Blog) — process Hank's Google Drive videos into blog/video pages
- 2026-03-07: Plan 1-02 complete — LEMP stack + WordPress on GCP e2-micro (104.196.102.152)
- 2026-03-13: Content migration — homily posts, hero images, page content all on WordPress
- 2026-03-17: Fixed upload permissions (chown uploads dir) and activated TinyMCE Advanced for font controls
- 2026-03-17: Site audit — documented concerns in .planning/CONCERNS.md
- 2026-03-17: Updated PROJECT.md — references now point to WordPress site, not static .html files
