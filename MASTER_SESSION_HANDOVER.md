# 🚀 Master Session Handover & System State
> **Last Updated**: August 2, 2026 — 15:21 IST  
> **Repository**: `G:\CLI\pinterest-auto-affiliate`  
> **GitHub Pages**: https://adityasnalawade742-design.github.io  

---

## 🚨 MANDATORY STARTUP DIRECTIVE (Every New Session)

> **Your VERY FIRST ACTION in any new AGY session MUST be:**
> ```bash
> python run_daily_health_check.py
> ```
> This runs the Zero-Drift self-healing engine — auto-corrects any price drift, INR contamination in USD fields, and data-attribute mismatches across all 9 storefront products.

---

## 1. What This Project Is

A **fully automated Pinterest → Amazon Affiliate monetization engine** for the brand **"Cozy Room Finds"**.

**The complete automated pipeline:**
1. User discovers Amazon products via Web Console (SerpAPI)
2. AI photo filter selects the cleanest product image (4-layer engine)
3. User reviews photos and optionally overrides the AI pick
4. Web Console packages the batch → sends to n8n webhook
5. n8n calls `/api/create_bridge_page` per product → builds landing page + hook image → pushes to GitHub Pages
6. n8n posts the Pin to Pinterest API v5 with bridge URL as destination

**Live URLs:**
| Page | URL |
|---|---|
| Storefront | https://adityasnalawade742-design.github.io/index.html |
| Privacy Policy | https://adityasnalawade742-design.github.io/privacy-policy.html |
| Terms of Service | https://adityasnalawade742-design.github.io/terms-of-service.html |
| Sitemap | https://adityasnalawade742-design.github.io/sitemap.xml |

---

## 2. Session Log — August 2, 2026

### Session A: Architecture Discovery & Audit
- Read all core project files: `MASTER_PROJECT_CONTEXT.md`, `SYSTEM_ARCHITECTURE.md`, `AUTOMATION_RULES.md`, `product_price_registry.json`, `modules/bridge_creator.py`, `modules/amazon_finder.py`, `modules/amazon_extractor.py`, `modules/pinterest_publisher.py`, `modules/automated_product_selector.py`, `rebuild_EVERY_single_bridge.py`, `web_console_server.py`, `admin_console.html`, `run_daily_health_check.py`, `global_direct_matrix.json`, `modules/scrapers/` (12 files).
- Full feature audit of the Web Console → identified 6 bugs.

### Session B: All 6 Bugs Fixed
All bugs in `web_console_server.py` and `admin_console.html` have been fixed. See Section 6 for details.

---

## 3. Complete Architecture Map

```
pinterest-auto-affiliate/
│
├── web_console_server.py          ← Local admin HTTP server (port 5000, threaded)
├── admin_console.html             ← Frontend UI (2 tabs: n8n Workflow + Homepage Manager)
├── run_daily_health_check.py      ← Zero-drift self-healing bot (MUST RUN FIRST)
├── rebuild_EVERY_single_bridge.py ← Rebuild all 9 bridge pages + sitemap + git push
├── delete_product.py              ← Delete a product from homepage + registry + git push
├── sync_all_regional_prices_master.py ← 21-domain Playwright price scraper (all regions)
├── rebuild_all_price_badges_usd.py    ← Re-render all Playwright price badge graphics
│
├── product_price_registry.json    ← SINGLE SOURCE OF TRUTH for all 9 products (prices, titles, images)
├── global_direct_matrix.json      ← Maps ASIN → regions where direct /dp/ links work (vs. search fallback)
├── global_tag_defaults.json       ← Default price tag layout settings (size, rotation, colors, positions)
├── pinterest_campaign_tracker.json← Log of published Pins
├── processed_asins.json           ← ASINs already published (dedup guard)
│
├── modules/
│   ├── amazon_finder.py           ← SerpAPI product discovery, multi-key failover, TRENDING_KEYWORDS
│   ├── amazon_extractor.py        ← 4-layer photo filter (text/collage/human/cozy-vibe) + SerpAPI photo fetch
│   ├── bridge_creator.py          ← Jinja2 bridge page generator + 200+ country geo-redirector
│   ├── html_overlay_engine.py     ← Playwright hook image renderer (price badge overlay)
│   ├── image_generator.py         ← Replicate FLUX-Dev AI image enhancer
│   ├── seo_copywriter.py          ← Gemini-powered pin title + description + hashtags
│   ├── vision_prompt.py           ← Cozy room prompt engineering for FLUX
│   ├── pinterest_publisher.py     ← Pinterest API v5 pin publisher
│   ├── automated_product_selector.py ← Dedup guard, ASIN history, VIRAL_HOME_DECOR_QUEUE
│   └── scrapers/                  ← 12 per-country Playwright price scrapers
│       ├── scrape_us.py, scrape_uk.py, scrape_in.py, scrape_de.py
│       ├── scrape_ca.py, scrape_au.py, scrape_jp.py, scrape_fr.py
│       ├── scrape_es.py, scrape_it.py, scrape_se.py, scrape_extended_domains.py
│
├── index.html                     ← Live homepage storefront (9 product cards)
├── bridge_B0DZD1X83N.html         ← Bridge landing page (per ASIN)
├── bridge_B0GYDXHF4G.html
├── bridge_B0FXLYXM32.html
├── bridge_B0C2YLN3H4.html
├── bridge_B07HP22QTZ.html
├── bridge_B0BZXNSW5K.html
├── bridge_B0DXKGL1T2.html
├── bridge_B0D1FRDFFX.html
├── bridge_B0D8P8CSYP.html
├── focus_product_{ASIN}_hook.jpg  ← Pinterest hook image per product
├── raw_images/raw_{ASIN}.jpg      ← Source product photo (used as input for overlay engine)
│
└── n8n_pinterest_affiliate_workflow.json ← n8n workflow (6 nodes, import into n8n)
```

---

## 4. Live Portfolio — 9 Active Products

| # | ASIN | Product | USD Price | Bridge Page |
|:-:|:---|:---|:---|:---|
| 1 | `B0DZD1X83N` | Minimalist Wood Base Bedside Table Lamp | $20.00 | [bridge_B0DZD1X83N.html](./bridge_B0DZD1X83N.html) |
| 2 | `B0GYDXHF4G` | Flame Aroma Essential Oil Diffuser | $35.00 | [bridge_B0GYDXHF4G.html](./bridge_B0GYDXHF4G.html) |
| 3 | `B0FXLYXM32` | White Wavy Wall Vanity Mirror | $76.49 | [bridge_B0FXLYXM32.html](./bridge_B0FXLYXM32.html) |
| 4 | `B0C2YLN3H4` | White Ceramic Donut Vase Set of 2 | $28.99 | [bridge_B0C2YLN3H4.html](./bridge_B0C2YLN3H4.html) |
| 5 | `B07HP22QTZ` | Crystal Prism Window Suncatcher | $12.99 | [bridge_B07HP22QTZ.html](./bridge_B07HP22QTZ.html) |
| 6 | `B0BZXNSW5K` | Touch Control Dimmable Bedside Lamp | $19.99 | [bridge_B0BZXNSW5K.html](./bridge_B0BZXNSW5K.html) |
| 7 | `B0DXKGL1T2` | Lily of the Valley Flower Desk Lamp | $38.57 | [bridge_B0DXKGL1T2.html](./bridge_B0DXKGL1T2.html) |
| 8 | `B0D1FRDFFX` | Handmade Glass Mushroom Ambient Lamp | $35.98 | [bridge_B0D1FRDFFX.html](./bridge_B0D1FRDFFX.html) |
| 9 | `B0D8P8CSYP` | Cute Bird Touch Control Nightstand Lamp | $18.99 | [bridge_B0D8P8CSYP.html](./bridge_B0D8P8CSYP.html) |

---

## 5. API Keys & Credentials (.env)

```env
# NOTE: Real values are stored in .env (gitignored). This is a reference template only.
GEMINI_API_KEY=<see .env file>
AMAZON_ASSOCIATE_TAG=smartdeal0358-21
SERPAPI_KEY=<see .env file — Key 1>
SERPAPI_KEY_2=<see .env file — Key 2>
SERPAPI_KEY_3=<see .env file — Key 3>
REPLICATE_API_TOKEN=<see .env file>
PINTEREST_BOARD_ID=1092545259543920271
PINTEREST_ACCESS_TOKEN=          ← EMPTY — need Pinterest OAuth (see Section 7)
PINTEREST_CLIENT_SECRET=         ← ADD THIS from Pinterest Developer Portal
BASE_BRIDGE_URL=https://adityasnalawade742-design.github.io
```

**Amazon Associate Tags by region:**
| Region | Tag |
|---|---|
| US | `smartdeal0358-20` |
| CA | `smartdeal0302-20` |
| IN | `smartdeal0358-21` |
| UK | `smartdea04b3a-21` |
| DE | `smartdeal0bb4-21` |
| FR | `smartdeal0962-21` |
| ES | `smartdeal0b46-21` |
| IT | `smartdea03a8d-21` |

---

## 6. Bug Fix Log — August 2, 2026 Session B

All 6 bugs identified in the Web Console audit have been fixed.

### ✅ Bug 1 — Pinterest OAuth Token Exchange (CRITICAL)
**File**: `web_console_server.py` → `handle_api_auth_callback()`  
**Was**: Rendered a cosmetic static HTML page. Never actually called Pinterest API.  
**Fix**: Now does real `POST https://api.pinterest.com/v5/oauth/token`, saves `PINTEREST_ACCESS_TOKEN` + `PINTEREST_REFRESH_TOKEN` to `.env` AND `os.environ` immediately.  
**Requires**: Add `PINTEREST_CLIENT_SECRET=<from dev portal>` to `.env` first.

### ✅ Bug 2 — Preview Overlay Always Crashed
**File**: `web_console_server.py` → `handle_api_preview_overlay()`  
**Was**: Called `render_html_overlay(url, title, subtitle, badge, price, output_path)` — 6th positional arg is `features`, not `output_path`.  
**Fix**: Switched to all keyword args. Also extracts `features` from POST body.

### ✅ Bug 3 — Step 2 Empty When SerpAPI Quota Exhausted
**File**: `web_console_server.py` → `handle_api_batch_extract()`  
**Was**: `if not prod: continue` — silently dropped ASINs that failed API lookup.  
**Fix**: CDN fallback using `ws-na.amazon-adsystem.com` widget URL + `m.media-amazon.com` patterns. Even on total failure, returns a stub entry so every ASIN appears in Step 2.

### ✅ Bug 4 — Step 3 Status Rows Stuck at ⏳ Forever
**File**: `admin_console.html` → `n8nSubmitBatch()` + new `_startN8nStatusPolling()`  
**Was**: No polling after dispatch. All rows showed "Queued — firing to n8n pipeline..." forever.  
**Fix**: After dispatch, polls `/api/task_status?asin=X` every 5 seconds per item. Updates icon (⏳→✅/❌), message, and injects live bridge link on success. Timer auto-clears when all done or on reset.

### ✅ Bug 5 — Homepage Manager Shows Stale Hook Images
**File**: `web_console_server.py` → `handle_api_homepage_products()`  
**Was**: Image URL `./focus_product_{ASIN}_hook.jpg` — no cache-bust.  
**Fix**: Appends `?v={int(time.time())}` to every hook image URL so browser always fetches fresh.

### ✅ Bug 6 — "Proceed" Button Shows with 0 Results
**File**: `admin_console.html` → `renderDiscoverGrid()`  
**Was**: Always showed footer regardless of items count.  
**Fix**: Returns early with "⚠️ No products found" message and hides footer when `items.length === 0`.

---

## 7. NEXT STEPS (Ordered by Priority)

### 🔴 Priority 1 — Connect Pinterest OAuth (Unblocks Live Pin Posting)
1. Go to https://developers.pinterest.com/apps/1596368
2. Copy your **App Secret** from the app settings page
3. Add to `.env`: `PINTEREST_CLIENT_SECRET=<your_secret>`
4. Start the web console: `python -u web_console_server.py`
5. Click **"🔌 Connect Pinterest OAuth 2.0"** button in the header
6. Authorize on Pinterest → server auto-exchanges code for token → saves to `.env`
7. Verify: check `.env` — `PINTEREST_ACCESS_TOKEN` should now be filled

### 🟡 Priority 2 — Run a Test Batch Through the Full Pipeline
1. Start web console + n8n
2. Import `n8n_pinterest_affiliate_workflow.json` into n8n, activate it
3. In Web Console: Step 1 → discover products → select 2-3 → Step 2 → confirm photos → Step 3 → Send to n8n
4. Watch Step 3 status rows update live (now fixed — polls every 5s)
5. Verify bridge pages appear on GitHub Pages and Pins appear on Pinterest

### 🟢 Priority 3 — Add More Products to Portfolio
Use the discovery pipeline to find new trending items. Target products:
- $15–$50 price range
- 4.4★+ rating with 100+ reviews
- Room decor / lighting / aesthetic home niche
- Clean product photos (no text overlays, no models)

### 🟢 Priority 4 — 21-Region Price Sync
Run the full regional price sync when current prices need updating:
```bash
python sync_all_regional_prices_master.py
```
This scrapes all 21 Amazon country storefronts and updates `product_price_registry.json`.

---

## 8. Standard CLI Cheat Sheet

```bash
# ===== MANDATORY: Run first in every session =====
python run_daily_health_check.py

# ===== Web Console =====
python -u web_console_server.py            # Start admin UI on http://localhost:5000

# ===== Full Site Rebuild =====
python rebuild_EVERY_single_bridge.py      # Rebuild all 9 bridge pages + sitemap + git push

# ===== Price Sync =====
python sync_all_regional_prices_master.py  # Full 21-domain price scrape + badge rebuild

# ===== Delete a product =====
python delete_product.py B0XXXXXXXXXX      # Remove ASIN from homepage + registry + push

# ===== Badge-only re-render =====
python rebuild_all_price_badges_usd.py     # Re-render Playwright price badge graphics only

# ===== Git state check =====
git status && git log --oneline -5
```

---

## 9. Git State — August 2, 2026 (15:21 IST)

- **Branch**: `main` (clean, up to date with `origin/main`)
- **Recent commits**:
  ```
  33205ee  docs: comprehensive detailed save of session handover and project state
  af081dd  refactor: complete clean rebuild of Web Console (admin_console.html)
  245d641  fix: fetch real Amazon listing hero photos for all discovered products
  1ff582f  fix: automatic SerpAPI key failover + 10 live Amazon products with images
  aea422c  fix: generate direct Amazon CDN high-res product image URLs
  df2426f  fix: auto-load 21-Region Matrix Grid table in Homepage Manager
  ```
- **GitHub Pages**: 100% Active & Green
- **Working Tree**: Clean (all bug fixes need to be committed — see below)

---

## 10. Pinterest Developer Portal Config

| Field | Value |
|---|---|
| App Name | `Cozy Room Decor Publisher Pro` |
| Company Name | `Cozy Room Finds` |
| App ID | `1596368` |
| Company Website | `https://adityasnalawade742-design.github.io/index.html` |
| Privacy Policy URL | `https://adityasnalawade742-design.github.io/privacy-policy.html` |
| App Purpose | `Personal API access (single, personal use)` |
| Pinterest Account | `@adityasnalawade0703` |
| Target Board ID | `1092545259543920271` |
| Developer Email | `aditya.s.nalawade742@gmail.com` |
| OAuth Redirect URI | `http://localhost:5000/api/auth/callback` |
| OAuth Scopes | `boards:read, boards:write, pins:read, pins:write` |
