# 📌 Pinterest Auto-Affiliate Automation System — Master Project State & Handoff Guide

> **Last Updated**: August 1, 2026  
> **Repository**: `G:\CLI\pinterest-auto-affiliate`  
> **Remote Origin**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`  
> **Live Showcase**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)  
> **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)  
> **Terms of Service**: [https://adityasnalawade742-design.github.io/terms-of-service.html](https://adityasnalawade742-design.github.io/terms-of-service.html)  
> **Company Name**: Cozy Room Finds  
> **App Name**: Cozy Room Decor Publisher Pro  
> **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`  

---

## 1. Executive Summary & Accomplishments

This project is an **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **9 Amazon country storefronts** (`US`, `IN`, `UK`, `DE`, `SE`, `SG`, `CA`, `AU`, `JP`) with zero 404 errors.

### Recent Major Hardening (August 1, 2026):
1. **100% Pinterest Support Rejection Issue Resolution**:
   - Company (`Cozy Room Finds`) & App (`Cozy Room Decor Publisher Pro`) names matched across [index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html), [privacy-policy.html](file:///G:/CLI/pinterest-auto-affiliate/privacy-policy.html), [terms-of-service.html](file:///G:/CLI/pinterest-auto-affiliate/terms-of-service.html), and all 9 bridge landing pages.
   - Added high-visibility glowing gold email badge pill displaying **`aditya.s.nalawade742@gmail.com`** (100% matched with Pinterest Business profile `@adityasnalawade0703`).
   - Created full n8n OAuth 2.0 video demo guide in [`PINTEREST_RE_APPLICATION_GUIDE.md`](file:///G:/CLI/pinterest-auto-affiliate/PINTEREST_RE_APPLICATION_GUIDE.md).

2. **Legal & Compliance Infrastructure**:
   - Published live [`terms-of-service.html`](file:///G:/CLI/pinterest-auto-affiliate/terms-of-service.html).
   - Standardized single high-visibility email badge pill across all footer footings.

3. **Git & GitHub Pages Build Health**:
   - Fixed `mode 160000` nested submodule build failure by removing `github_pages` from tracking and updating `.gitignore`.
   - Verified 100% automated green deployments on GitHub Pages.

---

## 2. Master Catalog Matrix (9 Active Portfolio Products)

| # | ASIN | Product Title | Target ASIN Override | Direct Regions (Direct Listing) | Landing Page URL |
| :-: | :--- | :--- | :--- | :--- | :--- |
| 1 | **`B0DZD1X83N`** | Minimalist Wood Base Table Lamp | `B0DZD1X83N` | `["US"]` | [bridge_B0DZD1X83N.html](./bridge_B0DZD1X83N.html) |
| 2 | **`B0GYDXHF4G`** | Flame Aroma Essential Oil Diffuser | `B0GYDXHF4G` | `["US"]` | [bridge_B0GYDXHF4G.html](./bridge_B0GYDXHF4G.html) |
| 3 | **`B0FXLYXM32`** | White Wavy Wall Vanity Mirror | `B0FXLYXM32` | `["US", "IN", "UK", "DE", "SE", "CA", "AU"]` | [bridge_B0FXLYXM32.html](./bridge_B0FXLYXM32.html) |
| 4 | **`B0C2YLN3H4`** | White Ceramic Donut Vase Set (2-Pack) | `B0C2YLN3H4` | `["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]` | [bridge_B0C2YLN3H4.html](./bridge_B0C2YLN3H4.html) |
| 5 | **`B07HP22QTZ`** | Crystal Prism Window Suncatcher | `B07HP22QTZ` | `["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]` | [bridge_B07HP22QTZ.html](./bridge_B07HP22QTZ.html) |
| 6 | **`B0BZXNSW5K`** | Touch Bedside Table Lamp | `B0BZXNSW5K` | `["US"]` | [bridge_B0BZXNSW5K.html](./bridge_B0BZXNSW5K.html) |
| 7 | **`B0DXKGL1T2`** | Lily of the Valley Flower Lamp | `B0DDTPCDLB` | `["US", "UK", "DE", "SE", "CA", "JP"]` | [bridge_B0DXKGL1T2.html](./bridge_B0DXKGL1T2.html) |
| 8 | **`B0D1FRDFFX`** | Glass Mushroom Table Lamp | `B0D1FRDFFX` | `["US"]` | [bridge_B0D1FRDFFX.html](./bridge_B0D1FRDFFX.html) |
| 9 | **`B0D8P8CSYP`** | Cute Bird Dimmable Touch Night Lamp | `B0D8P8CSYP` | `["US", "IN"]` | [bridge_B0D8P8CSYP.html](./bridge_B0D8P8CSYP.html) |

---

## 3. Core Architecture & System Modules

### 🖥️ `web_console_server.py` (Interactive Web Server)
- Runs locally at `http://localhost:5000`.
- Endpoints `/api/auth/pinterest` & `/api/auth/callback` render live OAuth authorization screens.
- Endpoint `/api/extract?target={ASIN}` extracts full Amazon photo suite and metadata.
- Endpoint `/api/generate` launches background campaign generation.

### 🎨 `modules/html_overlay_engine.py` (Playwright 1200x1600 Visual Overlay)
- Uses Playwright to render pixel-perfect 1200x1600 Pinterest pin graphics with adaptive gradient scrims.

### 🌐 `modules/bridge_creator.py` (Universal Multi-Region Geo-Redirector Engine)
- Generates luxury glassmorphism landing pages with 100% affiliate tag attachment (`tag=smartdeal0358-21`).
- Displays uniform high-visibility developer email contact (`aditya.s.nalawade742@gmail.com`) and legal footer links.

### 🔄 `n8n_pinterest_affiliate_workflow.json` (n8n Integration)
- Workflow for automated product processing, image generation, pin metadata, and posting via Pinterest API v5 (`POST /v5/pins`).

---

## 4. How to Resume Work in Any Session or Account

When starting a fresh session or switching accounts:

1. **Open Workspace**: Point to `G:\CLI\pinterest-auto-affiliate`.
2. **Run Zero-Drift Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
3. **Rebuild & Deploy Landing Pages**:
   ```bash
   python rebuild_EVERY_single_bridge.py
   ```
4. **Launch Web Console**:
   ```bash
   python -u web_console_server.py
   ```

Everything is committed, pushed to `main`, and deployed live on GitHub Pages!
