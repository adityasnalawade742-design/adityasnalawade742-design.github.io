# 📌 Pinterest Auto-Affiliate Automation System — Master Project State & Handoff Guide

> **Last Updated**: August 3, 2026  
> **Repository**: `G:\CLI\pinterest-auto-affiliate`  
> **Remote Origin**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`  
> **Live Showcase**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)  
> **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)  
> **Terms of Service**: [https://adityasnalawade742-design.github.io/terms-of-service.html](https://adityasnalawade742-design.github.io/terms-of-service.html)  
> **Company Name**: Cozy Room Finds  
> **App Name**: Cozy Room Decor Publisher Pro  
> **App ID**: 1596368  
> **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`  
> **Pinterest Account**: `@adityasnalawade0703`  
> **Git Branch**: `main`  
> **System Health Verification Status**: ✅ **100% PASS** (`check_fixes.py`)  

---

## 1. System Overview

An **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **21 Amazon country storefronts** with zero 404 errors.

---

## 2. Complete Summary of Fixed Issues & New Features

### A. Homepage (`index.html`) & SEO Fixes
- ✅ **Added SEO Canonical Tag**: Added `<link rel="canonical" href="https://adityasnalawade742-design.github.io/index.html">`.
- ✅ **Fixed SVG Favicon Encoding**: Fixed data URI entity encoding issue (`&lt;svg...&gt;` → standard `<svg...>`).
- ✅ **Cleaned Grid Structure**: Removed orphaned `<!-- Card TESTASIN12 -->` comment.
- ✅ **Standardized Asset Paths**: Fixed image path for ASIN `B0C2YLN3H4` (`focus_product_B0C2YLN3H4_hook.jpg`).
- ✅ **Currency Dropdown Sync**: Expanded dropdown to 46 currencies (added `ARS`, `CNY`, `HKD`, `TWD`, `QAR`, `KWD`, `BHD`, `OMR`, `NGN`, `KES`, `UYU`).

### B. Landing/Bridge Pages Audit & Fixes (All 9 Products)
- ✅ **Added Canonical Links**: Added `<link rel="canonical" href=".../bridge_{asin}.html">` to all 9 bridge pages.
- ✅ **Product-Specific Buyer Reviews**: Replaced hardcoded bedside lamp reviews on non-lamp products (suncatcher, ceramic donut vases, mushroom lamp, bird lamp) with product-specific verified buyer reviews.

### C. Core Generator & Source Template Engine (`modules/bridge_creator.py`)
- ✅ **Template Canonical Tag**: Added `<link rel="canonical">` into `BRIDGE_PAGE_TEMPLATE` for future products.
- ✅ **Dynamic Review Fallback**: Replaced hardcoded lamp review with `{{ product.buyer_review or '...' }}` with universal home decor fallback.
- ✅ **Universal Feature Fallbacks**: Replaced USB-C/linen shade lamp fallbacks with universal room aesthetic features.
- ✅ **Clean Title Formatting**: Fixed `update_showcase_index_page()` so titles shorter than 50 chars don't get unwanted `...` appended.
- ✅ **Index Card Data Attributes**: Updated `update_showcase_index_page()` to populate `data-base-usd`, `data-category`, `data-direct-regions`, `data-price-us`, and `data-price-{region}` attributes automatically for newly injected cards.

### D. Web Console Server (`web_console_server.py` & `admin_console.html`)
- ✅ **Safe Git Push Execution**: Wrapped single campaign git push in `try/except` with `check=False` to prevent network timeouts from failing tasks.
- ✅ **Local Image Fallback in Batch Prep**: Updated `handle_api_prepare_n8n_batch` to recognize pre-cached local images in `raw_images/raw_{asin}.jpg`.
- ✅ **0-Byte Image Guard**: Added `st_size > 5000` size checks in `handle_api_create_bridge_page` to prevent 0-byte corrupt image traps.

---

## 3. Active Portfolio Products (9 Items)

| # | ASIN | Product Title | USD Price | Landing Page |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **`B0DZD1X83N`** | Minimalist Wood Base Bedside Table Lamp | $20.00 | [bridge_B0DZD1X83N.html](./bridge_B0DZD1X83N.html) |
| 2 | **`B0GYDXHF4G`** | Flame Aroma Essential Oil Diffuser | $35.00 | [bridge_B0GYDXHF4G.html](./bridge_B0GYDXHF4G.html) |
| 3 | **`B0FXLYXM32`** | White Wavy Floor Standing Mirror | $76.49 | [bridge_B0FXLYXM32.html](./bridge_B0FXLYXM32.html) |
| 4 | **`B0C2YLN3H4`** | Modern Ceramic Donut Vase Set of 2 | $28.99 | [bridge_B0C2YLN3H4.html](./bridge_B0C2YLN3H4.html) |
| 5 | **`B07HP22QTZ`** | Hanging Crystal Suncatcher Prism | $12.99 | [bridge_B07HP22QTZ.html](./bridge_B07HP22QTZ.html) |
| 6 | **`B0BZXNSW5K`** | Touch Control Dimmable Bedside Lamp | $19.99 | [bridge_B0BZXNSW5K.html](./bridge_B0BZXNSW5K.html) |
| 7 | **`B0DXKGL1T2`** | Lily of the Valley Flower Desk Lamp | $38.57 | [bridge_B0DXKGL1T2.html](./bridge_B0DXKGL1T2.html) |
| 8 | **`B0D1FRDFFX`** | Handmade Glass Mushroom Ambient Lamp | $35.98 | [bridge_B0D1FRDFFX.html](./bridge_B0D1FRDFFX.html) |
| 9 | **`B0D8P8CSYP`** | Cute Bird Touch Control Nightstand Lamp | $18.99 | [bridge_B0D8P8CSYP.html](./bridge_B0D8P8CSYP.html) |

---

## 4. How to Resume Work in Any Session or AGY Account

When starting a new session or switching AGY accounts:

1. **Verify System Integrity**:
   ```bash
   python check_fixes.py
   ```
2. **Run Zero-Drift Daily Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
3. **Launch Web Console Server**:
   ```bash
   python -u web_console_server.py
   ```
4. **Open Admin Console**: Go to `http://localhost:5000` in your browser.

All code edits, template fixes, and landing pages are saved in Git and deployed live on GitHub Pages!

---

## 5. Amazon Associate Store IDs Across Regions

| Region | Store ID |
| :--- | :--- |
| 🇺🇸 US | `smartdeal0358-20` |
| 🇨🇦 CA | `smartdeal0302-20` |
| 🇮🇳 IN | `smartdeal0358-21` |
| 🇬🇧 UK / GB | `smartdea04b3a-21` |
| 🇩🇪 DE | `smartdeal0bb4-21` |
| 🇫🇷 FR | `smartdeal0962-21` |
| 🇪🇸 ES | `smartdeal0b46-21` |
| 🇮🇹 IT | `smartdea03a8d-21` |
| All others (SE, NL, PL, TR, BE, MX, BR, SG, AE, SA, EG, JP, AU) | OneLink → nearest native tag |
