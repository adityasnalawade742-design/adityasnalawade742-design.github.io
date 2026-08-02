# 📌 Pinterest Auto-Affiliate Automation System — Master Project State & Handoff Guide

> **Last Updated**: August 2, 2026
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

---

## 1. Executive Summary & Accomplishments

This project is an **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **21 Amazon country storefronts** with zero 404 errors.

---

## 2. Complete Change History (Newest First)

### August 2, 2026 — n8n Workflow Redesign
- ✅ Added **"📌 Send to n8n" tab** to `admin_console.html` (3-step: discover → image review → send)
- ✅ Added `POST /api/prepare_n8n_batch` endpoint to `web_console_server.py`
- ✅ Added `POST /api/create_bridge_page` endpoint to `web_console_server.py` (called by n8n per-product)
- ✅ Redesigned `n8n_pinterest_affiliate_workflow.json` — now 6 nodes with proper per-product loop, bridge page builder node, and immediate ACK response
- ✅ Latest commit: `2f0dff9`

### August 1, 2026 — Pinterest API Standard Access Re-Application
- ✅ Resolved 100% of Pinterest Support rejection points
- ✅ Company & App names matched across all pages
- ✅ Added high-visibility email badge (`aditya.s.nalawade742@gmail.com`) to all footers
- ✅ Created `terms-of-service.html` live on GitHub Pages
- ✅ Fixed `mode 160000` nested submodule build failure

### July 31, 2026 — System Hardening
- ✅ Zero-Drift Self-Healing Bot: 100% Pass (9 products)
- ✅ 45-Currency Parity Audit: 405/405 Tests Pass
- ✅ 72 Outbound Affiliate Links: 100% Active
- ✅ Regional ASIN Variant Mapper active for B0DZD1X83N (DE/SE → B0F946YHSZ)

---

## 3. Master Catalog Matrix (9 Active Portfolio Products)

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

## 4. Core Architecture & System Modules

### 🖥️ `web_console_server.py` (Interactive Web Server — Port 5000)
- Open `http://localhost:5000` to access the full admin dashboard
- **Tabs**: 10-Product Selector | Homepage Manager | Single ASIN Inspector | **📌 Send to n8n** (NEW)
- **Key Endpoints**:
  - `GET /api/discover` — search Amazon products
  - `GET /api/extract` — extract single product photos
  - `POST /api/batch_extract` — extract photos for multiple ASINs
  - `POST /api/generate` — generate single campaign (AI image + bridge + pin)
  - `POST /api/batch_generate` — generate batch campaigns
  - `POST /api/prepare_n8n_batch` — **(NEW)** prep product+image selections for n8n
  - `POST /api/create_bridge_page` — **(NEW)** called by n8n to build bridge page + hook image per product
  - `POST /api/n8n/dispatch-batch` — legacy direct dispatch (still works)
  - `POST /api/sync_prices` — trigger 21-domain price sync
  - `GET /api/auth/pinterest` → Pinterest OAuth 2.0 flow

### 🎨 `modules/html_overlay_engine.py` (Playwright 1200×1600 Visual Overlay)
- Renders Pinterest pin graphics with adaptive gradient scrims
- Uses Gemini Vision as dual-image Art Director for price tag positioning

### 🌐 `modules/bridge_creator.py` (Universal Multi-Region Geo-Redirector Engine)
- Generates glassmorphism landing pages with 100% affiliate tag attachment
- Geo-redirects 200+ countries to their local Amazon storefront

### 🔄 `n8n_pinterest_affiliate_workflow.json` (n8n Integration — REDESIGNED Aug 2)
- **6-node workflow**: Webhook → ACK → Split per product → Build bridge page → Merge → Post pin
- Webhook path: `pinterest-batch`
- Calls local server at `localhost:5000/api/create_bridge_page` per product
- Posts to Pinterest API v5 with unique SEO title + description + bridge URL

---

## 5. How to Resume Work in Any Session or Account

When starting a fresh session or switching accounts:

1. **Read this file** — you're on the right track.
2. **Open Workspace**: Point to `G:\CLI\pinterest-auto-affiliate`.
3. **Run Zero-Drift Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
4. **Launch Web Console**:
   ```bash
   python -u web_console_server.py
   ```
5. **Open browser**: `http://localhost:5000`
6. **To use the n8n workflow**: Click **📌 Send to n8n** tab → Search products → Review images → Send.

Everything is committed, pushed to `main`, and deployed live on GitHub Pages!

---

## 6. Official Amazon Associate Store IDs

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

---

## 7. Git Commit History (Last 5)

```
2f0dff9  feat: new n8n Send to n8n tab with 3-step workflow, bridge page builder endpoint, redesigned 6-node n8n workflow
28112ac  fix: debug pass - fix render_html_overlay args, NoneType crash, path.exists, duplicate import, sys.stdout corruption
25d30ef  feat: complete batch curation, manual image selector, and auto-bridge n8n workflow dispatch
984d701  docs: update master demo video guide for n8n workflow canvas and App ID 1596368
ad34a49  rebuild 100% of all portfolio landing pages with universal multi-region geo-redirector
```
