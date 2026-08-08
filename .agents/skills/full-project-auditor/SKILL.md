---
name: full-project-auditor
description: >-
  Master 20-step deep project diagnostic skill for Antigravity / AGY.
  Executes comprehensive audits across architecture, code quality, logic errors, runtime failures,
  API integrations, SQLite database, security, dependencies, frontend UI/UX, price sync zero-drift,
  21-domain zero-404 geo-matrices, affiliate tag compliance, error handling, edge cases, and production readiness.
  Use whenever the user requests "audit my entire project", "full system diagnostic", or "check project health".
---

# 🔍 Master Full Project Auditor Skill (`full-project-auditor`)

This skill defines the 20-step comprehensive diagnostic procedure for auditing the entire **Pinterest Auto-Affiliate Platform** codebase and runtime ecosystem.

---

## 📋 The 20-Step Full Audit Protocol

Whenever requested to perform a full project audit, execute the following 20 steps systematically:

### 1. Project Architecture Audit
- Verify system blueprints in `SYSTEM_ARCHITECTURE.md`, `AUTOMATION_RULES.md`, and `MASTER_PROJECT_CONTEXT.md`.
- Inspect entrypoints: `main.py`, `web_console_server.py`, `daily_price_updater.py`, `rebuild_EVERY_single_bridge.py`.

### 2. Code Quality & Linting Audit
- Run static syntax checkers:
  ```bash
  python check_fixes.py
  python scratch/deep_codebase_audit.py
  ```
- Check for unresolved `TODO` markers, dead imports, or non-standard formatting.

### 3. Logic & Contract Verification
- Ensure function signatures match across calling sites (`modules/amazon_finder.py`, `modules/amazon_extractor.py`, `modules/bridge_creator.py`, `modules/html_overlay_engine.py`).
- Enforce the **Empty Subtitle Policy** (`subtitle=""`).

### 4. Runtime Error Traceback Analysis
- Check Flask proxy logs (`web_console_server.py`) and command output for uncaught exceptions.
- Inspect `serpapi_cache.json` and output directory state.

### 5. API Integration Health (`SerpAPI`, `Replicate`, `Gemini`, `Pinterest API v5`)
- Validate API key loading in `config.py` (`GEMINI_API_KEY`, `SERPAPI_KEYS`, `REPLICATE_API_TOKEN`, `PINTEREST_ACCESS_TOKEN`).
- Test local API endpoints:
  ```bash
  python scratch/test_all_endpoints.py
  ```

### 6. Database & Registry Persistence (`product_price_registry.json`)
- Verify registry integrity (`product_price_registry.json`) for active ASINs.
- Confirm SQLite image cache (`modules/image_cache_db.py`) and tracking databases (`product_registry.xlsx`).

### 7. Storefront & Admin Authentication
- Verify admin mode protection (`index.html?admin=true`).
- Confirm public visitors see 0 delete buttons on `index.html`.

### 8. Security & Secret Detection Audit
- Verify `.env` is listed in `.gitignore`.
- Ensure no raw API tokens or client secrets are committed into static HTML or public JavaScript files.

### 9. Dependency & Requirements Audit
- Verify packages in `requirements.txt` (`beautifulsoup4`, `jinja2`, `playwright`, `pillow`, `requests`, `google-generativeai`, `python-dotenv`).

### 10. Frontend Storefront UI/UX Audit (`index.html`)
- Verify 1-click search clear (`✕`), category chips (`✨ All Finds`, `💡 Aesthetic Lighting`, `🌿 Room Decor`, `🏺 Ceramic Vases`, `🪞 Vanity Mirrors`), and responsive glassmorphism CSS.

### 11. Responsive Mobile Bridge Audit (`bridge_*.html`)
- Test mobile viewport rendering, hero image badges, and discount percentage pills (`🔥 SAVE 20% OFF`).

### 12. Performance & Image Caching Audit
- Confirm cache-busting query strings (`?v={timestamp}`) are appended to media URLs.
- Check clean raw image storage in `raw_images/`.

### 13. Zero-Drift Price Synchronization Audit
- Run price alignment check across registry, `index.html`, bridge HTML files, and Playwright badges:
  ```bash
  python scratch/audit_index_prices.py
  python run_daily_health_check.py
  ```

### 14. 21-Domain International Zero-404 Audit
- Run the 189-point Playwright zero-404 audit script:
  ```bash
  python scratch/master_zero_404_audit.py
  ```

### 15. Revenue Protection & Affiliate Tag Audit
- Verify 100% of outgoing CTA links carry tag `smartdeal0358-21` (or official regional store IDs):
  ```bash
  python audit_all_affiliate_tags.py
  python validate_all_affiliate_urls.py
  ```

### 16. Edge Case & Regional Out-of-Stock Audit
- Test handling for regional out-of-stock items (soft glowing red 🔴 `⚠️ NOT AVAILABLE IN YOUR REGION` badge + search fallback CTA).

### 17. Race Condition & File Lock Audit
- Verify file write safety during parallel image rendering or batch bridge page generation.

### 18. Configuration & Sitemap Audit
- Validate `sitemap.xml`, `robots.txt`, `vercel.json`, `affiliate_tag_config.json`, and `global_direct_matrix.json`.

### 19. SEO & Schema.org JSON-LD Audit
- Confirm canonical tags (`<link rel="canonical">`), OpenGraph meta tags, and `ItemList` JSON-LD schema on `index.html`.

### 20. Production Deployment Readiness Audit
- Run Git deployment status check:
  ```bash
  python scratch/verify_deployment.py
  git status
  ```

---

## 📊 Summary Output Format
Upon completing the 20 steps, provide a structured markdown report summarizing:
1. **Pass/Fail Audit Score** (e.g. `20/20 PASS`).
2. **Critical Findings or Warnings** (if any).
3. **Actionable Remediation Steps**.
