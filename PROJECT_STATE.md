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
> **Git Branch & Commit**: `main` (`7579949`)

---

## 1. System Overview

An **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **21 Amazon country storefronts** with zero 404 errors.

---

## 2. Complete Change History (August 2–3, 2026 Updates)

### Web Console 3.0 & n8n Pipeline Integration:
- ✅ **Rebuilt Web Console (`admin_console.html`)**: Redesigned into 2 clean tabs (`📌 Send to n8n Workflow` and `🏠 Homepage Manager`). Step 1 products start unselected for total control.
- ✅ **Real Amazon Listing Photos (`modules/amazon_finder.py`)**: Resolved 43-byte transparent placeholder image issues by fetching real Amazon listing hero photos (`https://m.media-amazon.com/images/I/..._SL1500_.jpg`).
- ✅ **SerpAPI Key Failover (`modules/amazon_finder.py`)**: Added automatic key failover across `SERPAPI_KEYS` array (Keys #1, #2, #3).
- ✅ **Backend Endpoints (`web_console_server.py`)**: Added `POST /api/prepare_n8n_batch` (packages product/photo selections, downloads images, writes SEO copy) and `POST /api/create_bridge_page` (called by n8n per-product to build bridge HTML and render hook image).
- ✅ **n8n Workflow (`n8n_pinterest_affiliate_workflow.json`)**: Updated to a 6-node pipeline with 1-by-1 product looping, local bridge builder node, and Pinterest API v5 POST publisher. Fixed Node 6 log expression to preserve ASIN and Bridge URL.
- ✅ **Restored Original Portfolio**: Restored `B0DZD1X83N` and `B0GYDXHF4G` back to the live homepage.
- ✅ **40+ Bug Audit & Fixes (Pass 1 & Pass 2)**: Replaced hardcoded paths, fixed n8n race conditions, added empty POST body guards, added file existence checks, cleaned retired seed ASINs, fixed rating count template tags, and added scraper error logging.

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

When opening a new session or changing AGY accounts:

1. **Read Handover Docs**:
   - `MASTER_SESSION_HANDOVER.md`
   - `PROJECT_STATE.md`
2. **Run Zero-Drift Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
3. **Verify All Fixes**:
   ```bash
   python check_fixes.py
   ```
4. **Launch Web Console**:
   ```bash
   python -u web_console_server.py
   ```
5. **Open Browser**: Go to `http://localhost:5000`.

Everything is committed, pushed to `main`, and deployed live on GitHub Pages!

---

## 5. Amazon Associate Store IDs Across Regions

| Region | Store ID |
| :--- | :--- |
| 🇺🇸 US | `smartdeal0358-20` |
| 🇨🇦 CA | `smartdeal0302-20` |
| 🇮🇳 IN | `smartdeal0358-21` |
| 🇬🇧 UK | `smartdea04b3a-21` |
| 🇩🇪 DE | `smartdeal0bb4-21` |
| 🇫🇷 FR | `smartdeal0962-21` |
| 🇪🇸 ES | `smartdeal0b46-21` |
| 🇮🇹 IT | `smartdea03a8d-21` |
| All others (SE, NL, PL, TR, BE, MX, BR, SG, AE, SA, EG, JP, AU) | OneLink → nearest native tag |
