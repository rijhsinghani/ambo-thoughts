---
phase: 1-infrastructure-launch
plan: 06
type: execute
wave: 3
depends_on: [02, 03, 04, 05]
files_modified:
  - scripts/deploy.sh
autonomous: false
requirements:
  - REQ-HOSTING-005
  - REQ-HOSTING-010
  - REQ-MIGRATION-002
  - REQ-MIGRATION-003
  - REQ-MIGRATION-005

must_haves:
  truths:
    - "Site loads at http://VPS_IP and displays the fully customized Ambo Thoughts homepage"
    - "All 8 pages display correctly on the production VPS with Navy/Gold branding"
    - "Hero slider cycles through 3 slides on production"
    - "Photo gallery and YouTube embeds work on production"
    - "Rank Math SEO is configured with sitemap generated"
    - "UpdraftPlus backup is configured"
    - "WordPress admin login works on production"
  artifacts:
    - path: "scripts/deploy.sh"
      provides: "Deployment script for rsync + WP-CLI database migration"
  key_links:
    - from: "Local by Flywheel"
      to: "VPS"
      via: "rsync over SSH + WP-CLI database export/import"
    - from: "Nginx (production)"
      to: "WordPress files"
      via: "/home/deploy/ambo-thoughts/public/"
---

<objective>
Deploy the fully customized local WordPress site to the production VPS, configure production-specific settings (SEO, backups), and verify the complete site works at the VPS IP address.

Purpose: This is the final step that takes all local work (theme, content, slider) and makes it live on the production server. After this plan, Phase 1 success criteria are met.

Output: Live Ambo Thoughts WordPress site accessible at http://VPS_IP with all content, branding, and functionality verified.
</objective>

<context>
@.planning/PROJECT.md
@.planning/phases/1/1-CONTEXT.md
@.planning/phases/1/plans/1-01-SUMMARY.md
@.planning/phases/1/plans/1-02-SUMMARY.md
@.planning/phases/1/plans/1-03-SUMMARY.md
@.planning/phases/1/plans/1-04-SUMMARY.md
@.planning/phases/1/plans/1-05-SUMMARY.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Deploy local site to production VPS</name>
  <files>scripts/deploy.sh</files>
  <action>
    **Create `scripts/deploy.sh`** with the full deployment procedure. The VPS IP will come from Plan 02's summary.

    **A. Upload ChurchWP parent theme and plugins to VPS:**
    The VPS from Plan 02 has bare WordPress installed. It needs the ChurchWP theme and plugins.

    ```bash
    VPS_USER="deploy"
    VPS_HOST="VPS_IP"  # Replace with actual IP from Plan 02
    VPS_PATH="/home/$VPS_USER/ambo-thoughts/public"

    # Upload parent theme
    scp ~/Downloads/churchwp_package/theme/churchwp.zip $VPS_USER@$VPS_HOST:/tmp/
    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && wp theme install /tmp/churchwp.zip"

    # Upload bundled plugins
    scp ~/Downloads/churchwp_package/plugins/themeslr-framework-churchwp.zip $VPS_USER@$VPS_HOST:/tmp/
    scp ~/Downloads/churchwp_package/plugins/js_composer.zip $VPS_USER@$VPS_HOST:/tmp/
    scp ~/Downloads/churchwp_package/plugins/revslider.zip $VPS_USER@$VPS_HOST:/tmp/

    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp plugin install /tmp/themeslr-framework-churchwp.zip --activate && \
      wp plugin install /tmp/js_composer.zip --activate && \
      wp plugin install /tmp/revslider.zip --activate"
    ```

    **B. Rsync child theme from local to VPS:**
    ```bash
    rsync -avz --delete \
      ~/Local\ Sites/ambo-thoughts/app/public/wp-content/themes/churchwp-child/ \
      $VPS_USER@$VPS_HOST:$VPS_PATH/wp-content/themes/churchwp-child/
    ```

    **C. Install content plugins on VPS:**
    ```bash
    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp plugin install foogallery --activate && \
      wp plugin install embed-plus-for-youtube --activate && \
      wp plugin install wp-smushit --activate"
    ```

    **D. Export local database and import to production:**
    In Local Site Shell:
    ```bash
    wp db export ~/ambo-local-export.sql
    ```

    Then:
    ```bash
    scp ~/ambo-local-export.sql $VPS_USER@$VPS_HOST:/tmp/

    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp db import /tmp/ambo-local-export.sql && \
      wp search-replace 'http://ambo-thoughts.local' 'http://VPS_IP' --all-tables && \
      wp search-replace 'ambo-thoughts.local' 'VPS_IP' --all-tables && \
      wp cache flush"
    ```

    **E. Rsync uploads (media library):**
    ```bash
    rsync -avz \
      ~/Local\ Sites/ambo-thoughts/app/public/wp-content/uploads/ \
      $VPS_USER@$VPS_HOST:$VPS_PATH/wp-content/uploads/
    ```

    **F. Activate child theme on production:**
    ```bash
    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp theme activate churchwp-child && \
      wp rewrite flush --hard"
    ```

    **G. Fix file permissions on VPS:**
    ```bash
    ssh $VPS_USER@$VPS_HOST "\
      find $VPS_PATH -type d -exec chmod 755 {} \; && \
      find $VPS_PATH -type f -exec chmod 644 {} \; && \
      chmod 600 $VPS_PATH/wp-config.php"
    ```

    **H. Rsync Revolution Slider data:**
    The slider config is in the database (already synced), but if slider template import is needed:
    ```bash
    scp ~/Downloads/churchwp_package/sampledata/main_home_slider.zip $VPS_USER@$VPS_HOST:/tmp/
    # Import via WP-CLI if available, otherwise verify slider came through DB export
    ```

  </action>
  <verify>
    - `curl -s -o /dev/null -w "%{http_code}" http://VPS_IP` returns 200
    - `ssh deploy@VPS_IP "cd /home/deploy/ambo-thoughts/public && wp theme list --status=active --format=csv"` shows churchwp-child
    - `curl http://VPS_IP` contains "Ambo Thoughts"
    - `curl http://VPS_IP/about/` returns 200
    - `curl http://VPS_IP/spirituality/` returns 200
  </verify>
  <done>
    - All WordPress files, themes, plugins, database, and media deployed to VPS
    - Child theme active on production
    - URLs updated from local to VPS IP
    - File permissions correct
  </done>
</task>

<task type="auto">
  <name>Task 2: Configure production-specific settings (SEO, backups, permalinks)</name>
  <action>
    SSH to VPS and configure production-only settings.

    **A. Rank Math SEO configuration (REQ-MIGRATION-002):**
    ```bash
    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp option update permalink_structure '/%postname%/' && \
      wp rewrite flush --hard"
    ```
    - Rank Math was installed in Plan 02
    - Via WP Admin on production (http://VPS_IP/wp-admin/):
      - Run Rank Math setup wizard
      - Set site type: "Personal Blog / Non-profit"
      - Enable sitemap module
      - Enable redirect module (for old URL handling)
      - Verify sitemap at http://VPS_IP/sitemap_index.xml
    - Note: Google Search Console submission deferred until domain is set up (per user decision)

    **B. UpdraftPlus backup configuration (REQ-HOSTING-005):**
    - In WP Admin > Settings > UpdraftPlus Backups
    - This requires user to authenticate with Google Drive (checkpoint below)
    - Set schedule: Files weekly, Database daily
    - Remote storage: Google Drive
    - Include: plugins, themes, uploads, database
    - Exclude: wp-core (can be reinstalled)

    **C. Verify Wordfence is active and configured:**
    - Visit WP Admin > Wordfence
    - Run initial scan
    - Verify firewall is in learning mode (normal for first week)

    **D. Test old URL redirects (REQ-MIGRATION-001):**
    ```bash
    # Test .html redirect
    curl -s -o /dev/null -w "%{http_code}" http://VPS_IP/about.html
    # Should return 301

    curl -s -o /dev/null -w "%{redirect_url}" http://VPS_IP/about.html
    # Should redirect to http://VPS_IP/about/
    ```

    **E. Set DISALLOW_FILE_EDIT in production wp-config:**
    Verify this was set in Plan 02. If not:
    ```bash
    ssh $VPS_USER@$VPS_HOST "cd $VPS_PATH && \
      wp config set DISALLOW_FILE_EDIT true --raw"
    ```

    **F. SSL note:**
    SSL is deferred per user decision (no domain yet). When domain is ready:
    ```bash
    # Future steps (NOT done now):
    # sudo certbot --nginx -d yourdomain.com
    # wp search-replace 'http://VPS_IP' 'https://yourdomain.com' --all-tables
    ```

  </action>
  <verify>
    - `curl http://VPS_IP/sitemap_index.xml` returns XML sitemap
    - `curl -s -o /dev/null -w "%{http_code}" http://VPS_IP/about.html` returns 301
    - `ssh deploy@VPS_IP "cd /home/deploy/ambo-thoughts/public && wp config get DISALLOW_FILE_EDIT"` returns true
    - Wordfence scan completes without critical findings
  </verify>
  <done>
    - Rank Math configured with sitemap generated
    - UpdraftPlus backup schedule set (pending Google Drive auth)
    - Wordfence active with initial scan complete
    - Old .html URLs redirect to WordPress permalinks
    - DISALLOW_FILE_EDIT enabled in production
  </done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Complete Ambo Thoughts WordPress site deployed to production VPS with all content, branding, SEO, backups, and security configured.</what-built>
  <how-to-verify>
    **Full site walkthrough at http://VPS_IP:**

    1. **Homepage**: Hero slider cycles through 3 slides (Ambo Thoughts, St. Francis, Psalm 46:10). Below slider: Gallery section with YouTube embed, Church News buttons, Bio preview. Navy/Gold branding throughout.

    2. **Each page** (click through navigation):
       - About: Deacon Henry bio and photo
       - Spirituality: Hero image, St. Francis quote
       - Church News: Vatican News + Diocese of Trenton buttons (click to verify external links)
       - Contact: Placeholder text (form deferred -- expected)
       - Pictures: Photo gallery with lightbox
       - Prayer Partner: Prayer chain content
       - Stuff: Misc content
       - Videos: YouTube embeds play correctly

    3. **Admin**: Login at http://VPS_IP/wp-admin/ -- verify access works

    4. **Technical checks**:
       - Visit http://VPS_IP/about.html -- should redirect to /about/
       - Visit http://VPS_IP/sitemap_index.xml -- should show XML sitemap
       - Check browser: no mixed content warnings (should be clean HTTP, no HTTPS attempts)

    5. **UpdraftPlus**: If you want to set up Google Drive backup now, go to WP Admin > UpdraftPlus and authenticate. Otherwise this can be done later.

  </how-to-verify>
  <resume-signal>Type "approved" if the site looks correct at the VPS IP, or describe any issues.</resume-signal>
</task>

</tasks>

<verification>
- http://VPS_IP loads Ambo Thoughts homepage
- All 8 pages render correctly
- Hero slider has 3 slides
- Navy/Gold branding consistent
- Gallery and video embeds functional
- Old URL redirects working
- SEO sitemap generated
- Admin login works
</verification>

<success_criteria>
Phase 1 is complete when:

1. Site loads at production VPS IP over HTTP (SSL deferred -- no domain yet)
2. All 8 pages display correctly with Navy/Gold branding
3. Contact form is SKIPPED (deferred per user request) -- placeholder page exists
4. Homepage hero slider cycles through 3 slides
5. Google crawling/SEO deferred until domain is set up (but Rank Math and sitemap are ready)
   </success_criteria>

<output>
After completion, create `.planning/phases/1/plans/1-06-SUMMARY.md`
</output>
