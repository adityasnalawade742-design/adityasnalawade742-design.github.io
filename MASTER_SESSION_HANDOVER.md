# 📋 Master Session Handover Document — Pinterest Auto-Affiliate System

> **Date**: August 3, 2026  
> **Status**: ACTIVE & 100% HEALTHY  
> **Verification**: All 7 critical modules pass `check_fixes.py` (100% PASS)  

---

## 1. Quick Start for New Sessions or AGY Account Switch

If you switch accounts or start a fresh session, execute these commands to verify state and resume:

```bash
# 1. Verify zero-drift system health
python check_fixes.py

# 2. Run system health check
python run_daily_health_check.py

# 3. Launch Web Console Server
python -u web_console_server.py
```
Open `http://localhost:5000` to manage products, send n8n batches, or preview price tag overlays.

---

## 2. Key Accomplishments & Fixes

1. **Grid & Bridge SEO Canonical Tags**:
   - Added canonical link tags (`<link rel="canonical">`) across `index.html`, all 9 `bridge_{asin}.html` files, and `modules/bridge_creator.py` template.

2. **Buyer Review Matching**:
   - Replaced duplicate bedside lamp reviews across non-lamp bridge pages with product-specific reviews (suncatchers, donut vases, mushroom lamp, bird lamp).
   - Updated template to use `{{ product.buyer_review }}` with a universal home decor fallback.

3. **Homepage Grid Attributes & Currency Selector**:
   - Added 11 missing currency options (`ARS`, `CNY`, `HKD`, `TWD`, `QAR`, `KWD`, `BHD`, `OMR`, `NGN`, `KES`, `UYU`) to `index.html` dropdown.
   - Enhanced `update_showcase_index_page()` in `bridge_creator.py` to write `data-base-usd`, `data-category`, `data-direct-regions`, and `data-price-us` data attributes onto new grid cards automatically.

4. **Web Console & n8n Pipeline Reliability**:
   - Added non-blocking `try/except` for git operations in `run_async_generation`.
   - Fixed pre-cached local image detection in `handle_api_prepare_n8n_batch`.
   - Added 0-byte corrupt image file size guards (`st_size > 5000`) in `handle_api_create_bridge_page`.

---

## 3. Core Files Map

- **`index.html`**: Portfolio showcase grid with global currency engine and search filters.
- **`bridge_{ASIN}.html`**: High-converting glassmorphism landing pages with geo-redirection.
- **`web_console_server.py`**: Local Flask/http.server console handling discovery, extraction, n8n dispatching, and overlay rendering.
- **`admin_console.html`**: Web Console UI dashboard (`http://localhost:5000`).
- **`modules/bridge_creator.py`**: Jinja2 landing page builder and showcase card injector.
- **`modules/html_overlay_engine.py`**: Playwright JPEG renderer for Pinterest pins.
- **`modules/pinterest_publisher.py`**: Pinterest API v5 publication engine.
- **`check_fixes.py`**: Automated verification test suite.

---

## 4. Brand & Affiliate Credentials

- **Company Name**: Cozy Room Finds
- **App Name**: Cozy Room Decor Publisher Pro (App ID: 1596368)
- **Developer Email**: `aditya.s.nalawade742@gmail.com`
- **Pinterest Profile**: `@adityasnalawade0703`
- **Primary US Store Tag**: `smartdeal0358-20`
