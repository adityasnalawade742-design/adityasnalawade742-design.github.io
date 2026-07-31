# 📌 Pinterest Auto-Affiliate Automation System — Master Project State & Handoff Guide

> **Last Updated**: July 29, 2026  
> **Repository**: `G:\CLI\pinterest-auto-affiliate`  
> **Remote Origin**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`  
> **Live Showcase**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)  
> **Official Regional Affiliate Tags**:
> - 🇺🇸 **US**: `smartdeal0358-20`
> - 🇨🇦 **CA**: `smartdeal0302-20`
> - 🇮🇳 **IN**: `smartdeal0358-21`
> - 🇬🇧 **UK**: `smartdea04b3a-21`
> - 🇩🇪 **DE**: `smartdeal0bb4-21`
> - 🇫🇷 **FR**: `smartdeal0962-21`
> - 🇪🇸 **ES**: `smartdeal0b46-21`
> - 🇮🇹 **IT**: `smartdea03a8d-21`

---

## 1. Executive Summary & Accomplishments

This project is an **end-to-end automated affiliate marketing & landing page generation platform** built for Pinterest traffic. It automatically extracts Amazon product listing data, filters photos for seller text/infographics/hands, applies Playwright high-resolution 1200x1600 visual pin overlays with dynamic gradient scrims, builds high-converting glassmorphism landing pages, and routes global visitors across **9 Amazon country storefronts** (`US`, `IN`, `UK`, `DE`, `SE`, `SG`, `CA`, `AU`, `JP`) with zero 404 errors.

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

*Note: Product `B0DLN5S5K9` was explicitly deleted per user directive.*

---

## 3. Core Architecture & System Modules

### 🖥️ `web_console_server.py` (Interactive Web Server)
- Runs locally at `http://localhost:5000`.
- Endpoint `/api/extract?target={ASIN}` extracts full Amazon photo suite and metadata.
- Endpoint `/api/generate` launches background campaign generation.
- **Remote Image Downloader**: Handled HTTP image URLs directly to prevent Windows `OSError: [Errno 22]` path errors.

### 🎨 `modules/html_overlay_engine.py` (Playwright 1200x1600 Visual Overlay)
- Uses Playwright to render pixel-perfect 1200x1600 Pinterest pin graphics.
- **Smart Brightness Engine**: Measures pixel luminance across top and bottom 25% zones using ITU-R BT.601 formula:
  $$\text{Luminance} = (0.299 \times R) + (0.587 \times G) + (0.114 \times B)$$
- **Adaptive Scrim Opacities**:
  - Bright / Glowing Lamp Scenes ($\text{Luminance} > 70$): Sets `0.55` top / `0.65` bottom dark gradient scrims.
  - Dark Room Scenes ($\text{Luminance} \le 70$): Sets `0.35` top / `0.45` bottom dark gradient scrims.
  - Guarantees **7:1 AAA WCAG contrast ratio** for white headline text and price pills.

### 🌐 `modules/bridge_creator.py` (Universal Multi-Region Geo-Redirector Engine)
- Generates luxury glassmorphism landing pages.
- **JavaScript `applyGeoRedirect(countryCode)`**:
  - Detects visitor country across 9 global Amazon storefronts (`US`, `IN`, `UK`, `DE`, `SE`, `SG`, `CA`, `AU`, `JP`).
  - **100% Tag Attachment**: Appends `tag=smartdeal0358-21` to all direct listing URLs (`amazon.com/dp/{asin}?tag=smartdeal0358-21`) AND local search fallback URLs (`amazon.in/s?k={keywords}&tag=smartdeal0358-21`).
  - **Zero 404 Fallback**: If an item is unlisted in a specific country, automatically falls back to local search and displays the *"Item Ships Globally from Amazon US"* notice box.

### ⚡ `modules/image_generator.py` (Replicate FLUX-Dev & Safety Timeout Guard)
- Generates 8K commercial room backgrounds using Replicate FLUX-Dev API.
- **20-Second Hard Timeout Guard**: Caps Replicate API predictions at 20s max. If queue spikes occur, instantly falls back to using the clean listing photo without process timeouts.

### 🔨 `rebuild_EVERY_single_bridge.py` (Master Rebuilder)
- Script to rebuild 100% of all landing pages across the repository using the latest catalog mapping and geo-redirect rules.

---

## 4. Key Scripts & Utility Tooling

| Script Name | Purpose | How to Run |
| :--- | :--- | :--- |
| `web_console_server.py` | Starts Web Console at `http://localhost:5000` | `python -u web_console_server.py` |
| `rebuild_EVERY_single_bridge.py` | Rebuilds 100% of landing pages and pushes to GitHub | `python rebuild_EVERY_single_bridge.py` |
| `audit_all_affiliate_tags.py` | Verifies `tag=smartdeal0358-21` across all cards & JS code | `python audit_all_affiliate_tags.py` |
| `fast_audit_9_storefronts.py` | Audits ASIN direct availability across 9 global Amazon stores | `python fast_audit_9_storefronts.py` |

---

## 5. How to Resume Work in a New Conversation / AGY Account

When starting a fresh conversation or switching AGY accounts, follow these 3 simple steps:

1. **Open Workspace**: Point AGY CLI to `G:\CLI\pinterest-auto-affiliate`.
2. **Read Master State**: Inspect `PROJECT_STATE.md` (this file) to recall project setup.
3. **Verify/Run**:
   - Check Web Console: `python -u web_console_server.py`
   - Rebuild catalog if needed: `python rebuild_EVERY_single_bridge.py`
   - Verify affiliate tags: `python audit_all_affiliate_tags.py`

Everything is committed, pushed to `main`, and deployed live on GitHub Pages!
