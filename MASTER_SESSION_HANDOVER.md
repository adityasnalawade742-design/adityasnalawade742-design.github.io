# 🚀 Master Session Handover & Complete System State
> **Last Updated**: August 3, 2026 — 13:35 IST  
> **Repository Root**: `G:\CLI\pinterest-auto-affiliate`  
> **GitHub Pages URL**: https://adityasnalawade742-design.github.io  
> **System Health Status**: 100% VERIFIED & STABLE — All 40+ Bugs Fixed + Broken Test Card Purged + Mushroom Lamp Custom Raw Image Integrated  
> **Git Branch & Commit**: `main` (`0a7587e`)

---

## 🚨 MANDATORY STARTUP DIRECTIVE (Every New Session / Account)

> **When opening a new AGY account or starting a new session, your VERY FIRST ACTION must be:**
> ```bash
> python run_daily_health_check.py
> ```
> This executes the Zero-Drift self-healing engine to verify price parity, correct any data attribute discrepancies across `index.html`, `product_price_registry.json`, and all 9 landing pages, and automatically deploy self-healed updates live to GitHub Pages.
>
> **To verify all 40+ system audit fixes at any time:**
> ```bash
> python check_fixes.py
> ```

---

## 1. Executive Summary & Core Capabilities

This codebase powers **"Cozy Room Finds"**, a fully automated **Pinterest → Amazon Affiliate Monetization Engine**.

### 🌟 Key Capabilities & Features:
1. **Automated Product Discovery**: Discovers viral, high-converting home decor products ($15–$50 price point) via SerpAPI or 0-cost direct Amazon search scraper.
2. **AI Photo Filtering & Quality Engine**: Scores product photos on a 0–100 scale, filtering out text overlays, multi-item split collages, and human presence (hands/faces) to ensure clean product graphics.
3. **Canva-Quality Visual Pin Generation**: Uses Playwright to render high-resolution 1200x1600 Pinterest pin graphics featuring custom price tag badges, ambient gradient scrims, and feature callouts.
4. **Glassmorphism Landing Pages**: Jinja2-powered bridge page generator producing mobile-first, high-converting landing pages with dynamic pricing, star ratings, and buyer reviews.
5. **21-Region Storefront Matrix & Geo-Redirector**: Client-side JS geo-redirector that maps visitors from 200+ countries to their local native Amazon storefront (US, UK, IN, DE, FR, ES, IT, CA, AU, JP, SE, NL, PL, TR, BE, MX, BR, SG, AE, SA, EG) with zero 404s.
6. **Master Web Console 3.0**: Dual-tab web dashboard (`http://localhost:5000`):
   - **Tab 1**: Product Discovery, Image Review & Selection, and n8n Batch Dispatch Monitor.
   - **Tab 2**: Live Homepage Showcase Manager & 21-Region Global Storefront Matrix Table.
7. **Automated n8n Integration**: 6-node n8n workflow (`n8n_pinterest_affiliate_workflow.json`) for automated 1-by-1 product processing and live Pinterest API v5 pin posting.
8. **SQLite + Excel Registry Sync**: Dual database tracking (`cache/registry.db`) with background auto-export to `product_registry.xlsx` (Published & Rejected sheets) and raw image lifecycle auto-cleanup.

---

## 2. Recent Session Fixes & New Features (August 3, 2026)

### 🧹 Purged Broken Test Product (`TESTASIN12`)
- **Problem**: `index.html` contained a leftover dummy test card `TESTASIN12` ("Aesthetic Cozy Mushroom Lamp Test") pointing to missing image files and yielding a GitHub Pages 404 error on click.
- **Fix**: Executed `delete_product.py TESTASIN12`, decomposing the wrapper DOM element from `index.html`, unblocking history, and syncing clean code live to GitHub.

### 🍄 Integrated Custom Raw Source Image for Mushroom Lamp (`B0D1FRDFFX`)
- **Action**: Saved `raw_B0D1FRDFFX_console.jpg` into `raw_images/raw_B0D1FRDFFX.jpg`.
- **Re-rendered Overlays**: Executed `rebuild_all_price_badges_usd.py` with Playwright Smart Luminance engine (Opacity: 0.55 top, 0.65 bottom) generating high-resolution 1200x1600 pin graphic (`focus_product_B0D1FRDFFX_hook.jpg`).
- **Landing Page Rebuild**: Rebuilt `bridge_B0D1FRDFFX.html` and synced live to GitHub Pages.

---

## 3. Complete Summary of All 40+ Bugs Fixed Across 2 Audit Passes

### 🔴 Pass 1 Fixes (28 Critical & High Issues)
- **C1**: Replaced hardcoded `G:/CLI/...` paths with dynamic `Path(__file__).resolve().parent`.
- **C2**: Fixed static `?v=3` query params in `bridge_creator.py` by switching to dynamic `?v={int(time.time())}` timestamp cache-busting.
- **C3**: Added `Path.exists()` guards around raw source images before rendering.
- **C4**: Fixed n8n workflow execution chain so nodes run sequentially (`1 -> 1b -> 2 -> 3 -> 4 -> 5 -> 6`).
- **C5/C6**: Ensured `chosen_photo_url` is passed from Node 3 and added null-guards in Node 5.
- **H1**: Added `try/except ValueError` in `run_daily_health_check.py` for safe float parsing of prices.
- **H2**: Stripped leading/trailing whitespace (`pt.get_text(strip=True)`) before DOM text updates.
- **H3**: Preserved dictionary structure (`product = dict(product_data)`) during template rendering.
- **H4**: Switched `delete_product.py` from regex card removal to BeautifulSoup DOM decomposition (`card_wrapper.decompose()`).
- **H5**: Increased Playwright page load timeout in `validate_all_affiliate_urls.py` to 400ms to allow client-side Cloudflare geo-redirects.
- **H6**: Added support for `prismatic_sunlight` theme in `seo_copywriter.py`.
- **H7**: Returned clean `{"status": "API_ERROR"}` dictionary on Pinterest publisher connection exceptions.
- **H8**: Set `check=False` on all git commit operations to avoid crashing scripts when git reports "nothing to commit".
- **M1/M2/M3**: Generated dynamic editorial copy driven by `seo.description` and `product.features` instead of hardcoded lamp copy.
- **L3/L4**: Fixed cross-compatibility between `GB` and `UK` country codes in direct matrix and price lookups.
- **L6**: Updated Node 6 in n8n workflow to reference `$json.final_asin` cleanly.

### 🟠 Pass 2 Fixes (12 New System-Wide Findings)
- **NH1**: Fixed `daily_price_updater.py` line 282 `KeyError` on `data["url"]` by replacing with `data.get("url", "")` + skip guard.
- **NH2**: Replaced non-cwd `os.system()` calls in `daily_price_updater.py` with `subprocess.run(..., cwd=str(BASE_DIR), check=False)`.
- **NM1**: Replaced silent `except Exception: pass` in all regional scrapers (`scrape_us.py`, `scrape_uk.py`, `scrape_in.py`, `scrape_de.py`, `scrape_extended_domains.py`) with explicit error logging.
- **NM2**: Fixed `NameError: name 'item' is not defined` in `web_console_server.py` `/api/create_bridge_page` endpoint (`item.get` → `data.get`).
- **NM3**: Corrected default n8n webhook URL in `web_console_server.py` from `/webhook/process-product` to the real endpoint `/webhook/pinterest-batch`.
- **NM4**: Removed fragile `pattern_img` regex replacement in `daily_price_updater.py` that injected hardcoded broken HTML into `index.html`.
- **NM5**: Purged retired legacy ASINs (`B0BDRSG2BT`, `B0GGHJ1J4L`) from `DEFAULT_REGISTRY` seed in `daily_price_updater.py`.
- **NL1**: Applied missing `return {"status": "API_ERROR", ...}` inside exception block in `modules/pinterest_publisher.py`.
- **NL2**: Added file existence check (`if not registry_file.exists()...`) before reading in `run_daily_health_check.py`.
- **NL3**: Added registry existence check and set `check=False` on git commit in `sync_exact_amazon_prices.py`.
- **NL4**: Added `content_length > 0` guard to `handle_api_delete_homepage_product` in `web_console_server.py` to prevent `JSONDecodeError` on empty POST bodies.
- **NL5**: Updated rating-box template in `bridge_creator.py` to use dynamic `product.reviews or '1,200'` review count instead of hardcoded `(1,240+ Verified Reviews)`.
- **N8N Node 6 Fix**: Updated Node 6 expression in `n8n_pinterest_affiliate_workflow.json` to reference `$node['4. Merge...'].json.final_asin` and `$node['4. Merge...'].json.final_bridge_url` so log output preserves the ASIN and Bridge URL even after Node 5's HTTP response.

---

## 4. Complete Repository Architecture Map

```
pinterest-auto-affiliate/
│
├── web_console_server.py          ← Multi-threaded admin HTTP server (port 5000)
├── admin_console.html             ← Master Web Console 3.0 UI (Discover, Review, n8n, Homepage)
├── run_daily_health_check.py      ← Automated zero-drift self-healing health check
├── check_fixes.py                 ← Automated verification script checking all 40+ bug fixes
├── rebuild_EVERY_single_bridge.py ← Rebuild all 9 landing pages + sitemap + git push
├── delete_product.py              ← Delete product from index.html + registry + push live
├── sync_all_regional_prices_master.py ← 21-domain Playwright price scraper (all regions)
├── sync_exact_amazon_prices.py    ← Multi-region price sync for all 21 Amazon domains
├── daily_price_updater.py         ← Daily automated price updater & graphic re-renderer
├── rebuild_all_price_badges_usd.py    ← Re-render Playwright price badge graphics
├── validate_all_affiliate_urls.py ← 400ms Cloudflare-aware affiliate link auditor
│
├── n8n_local_bridge.py            ← CLI / n8n bridge script
├── n8n_pinterest_affiliate_workflow.json ← 6-node n8n workflow JSON (import to n8n)
│
├── processed_asins.json           ← Active published ASIN history (dedup guard)
├── product_price_registry.json    ← Single source of truth for pricing & metadata
├── global_direct_matrix.json      ← 21-region direct product vs search fallback matrix
├── global_tag_defaults.json       ← Saved visual tag position & layout defaults
├── product_registry.xlsx          ← Auto-synced Excel workbook (Published & Rejected sheets)
│
├── cache/
│   ├── image_cache.db             ← SQLite high-res image URL cache
│   └── registry.db                ← SQLite Published/Rejected ASIN database (<1ms lookup)
│
├── modules/
│   ├── product_registry.py        ← SQLite + Excel auto-sync & raw image lifecycle manager
│   ├── amazon_finder.py           ← SerpAPI product discovery + 0-cost direct Amazon search scraper
│   ├── amazon_extractor.py        ← 4-layer photo filter (text/collage/human/cozy) + fallback guard
│   ├── bridge_creator.py          ← Jinja2 bridge page builder + 200+ country geo-redirector
│   ├── html_overlay_engine.py     ← Playwright 1200x1600 visual pin graphic overlay engine
│   ├── image_generator.py         ← Replicate FLUX-Dev AI image generation
│   ├── seo_copywriter.py          ← Gemini SEO title, description, and hashtag generator
│   ├── vision_prompt.py           ← Cozy room prompt engineering for FLUX
│   ├── pinterest_publisher.py     ← Pinterest API v5 pin publisher
│   ├── automated_product_selector.py ← Dedup guard, ASIN history, VIRAL_HOME_DECOR_QUEUE
│   └── scrapers/                  ← 12 per-country Playwright price scrapers
│       ├── scrape_us.py, scrape_uk.py, scrape_in.py, scrape_de.py
│       ├── scrape_ca.py, scrape_au.py, scrape_jp.py, scrape_fr.py
│       ├── scrape_es.py, scrape_it.py, scrape_se.py, scrape_extended_domains.py
│
├── index.html                     ← Live homepage storefront (9 product cards)
├── bridge_B0DZD1X83N.html         ← Landing page per product
├── bridge_B0GYDXHF4G.html
├── bridge_B0FXLYXM32.html
├── bridge_B0C2YLN3H4.html
├── bridge_B07HP22QTZ.html
├── bridge_B0BZXNSW5K.html
├── bridge_B0DXKGL1T2.html
├── bridge_B0D1FRDFFX.html
├── bridge_B0D8P8CSYP.html
├── focus_product_{ASIN}_hook.jpg  ← High-res Pinterest hook graphic per product
└── raw_images/raw_{ASIN}.jpg      ← Source product photo downloaded for overlay engine
```

---

## 5. Active Portfolio — 9 Live Products

| # | ASIN | Product Title | USD Price | Live Landing Page |
|:-:|:---|:---|:---|:---|
| 1 | `B0DZD1X83N` | Minimalist Wood Base Bedside Table Lamp | $20.00 | [bridge_B0DZD1X83N.html](./bridge_B0DZD1X83N.html) |
| 2 | `B0GYDXHF4G` | Flame Aroma Essential Oil Diffuser | $35.00 | [bridge_B0GYDXHF4G.html](./bridge_B0GYDXHF4G.html) |
| 3 | `B0FXLYXM32` | White Wavy Floor Standing Mirror | $76.49 | [bridge_B0FXLYXM32.html](./bridge_B0FXLYXM32.html) |
| 4 | `B0C2YLN3H4` | Modern Ceramic Donut Vase Set of 2 | $28.99 | [bridge_B0C2YLN3H4.html](./bridge_B0C2YLN3H4.html) |
| 5 | `B07HP22QTZ` | Hanging Crystal Suncatcher Prism | $12.99 | [bridge_B07HP22QTZ.html](./bridge_B07HP22QTZ.html) |
| 6 | `B0BZXNSW5K` | Touch Control Dimmable Bedside Lamp | $19.99 | [bridge_B0BZXNSW5K.html](./bridge_B0BZXNSW5K.html) |
| 7 | `B0DXKGL1T2` | Lily of the Valley Flower Desk Lamp | $38.57 | [bridge_B0DXKGL1T2.html](./bridge_B0DXKGL1T2.html) |
| 8 | `B0D1FRDFFX` | Handmade Glass Mushroom Ambient Lamp | $35.98 | [bridge_B0D1FRDFFX.html](./bridge_B0D1FRDFFX.html) |
| 9 | `B0D8P8CSYP` | Cute Bird Touch Control Nightstand Lamp | $18.99 | [bridge_B0D8P8CSYP.html](./bridge_B0D8P8CSYP.html) |

---

## 6. Amazon Associate Regional Store IDs

| Region | Store ID |
|:---|:---|
| 🇺🇸 US | `smartdeal0358-20` |
| 🇨🇦 CA | `smartdeal0302-20` |
| 🇮🇳 IN | `smartdeal0358-21` |
| 🇬🇧 UK | `smartdea04b3a-21` |
| 🇩🇪 DE | `smartdeal0bb4-21` |
| 🇫🇷 FR | `smartdeal0962-21` |
| 🇪🇸 ES | `smartdeal0b46-21` |
| 🇮🇹 IT | `smartdea03a8d-21` |
| All 14 Extended Regions (SE, NL, PL, TR, BE, MX, BR, SG, AE, SA, EG, JP, AU) | OneLink fallback to nearest native tag |

---

## 7. How to Resume Work in Any AGY Session or Account

When starting a new session or changing AGY accounts:

1. **Run Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
2. **Run Bug Verification Check**:
   ```bash
   python check_fixes.py
   ```
3. **Start Web Console Server**:
   ```bash
   python -u web_console_server.py
   ```
4. **Access Web Console**: Open `http://localhost:5000` in your browser.

All fixes are committed, pushed to `main`, and live on GitHub Pages!
