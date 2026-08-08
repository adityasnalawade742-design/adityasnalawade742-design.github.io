# 🚀 Pinterest Auto Affiliate Platform: Master Progress, Architecture & Handover Record

> **SINGLE SOURCE OF TRUTH & AGENT HANDOVER GUIDE**: This document details the entire state of the project, technical architecture, verified asset counts, dynamic precision prompt strength engine, error fixes, and operational standard workflows. Any AGY instance or AI assistant can inspect this document to immediately resume work from where we left off with zero context loss.

---

## 📌 Executive Summary & System Coordinates

* **Platform Name**: Pinterest Auto Affiliate System
* **Live Storefront URL**: [https://adityasnalawade742-design.github.io/](https://adityasnalawade742-design.github.io/)
* **Remote Git Repository**: [https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git](https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git)
* **Master Local Directory**: `G:\CLI\pinterest-auto-affiliate`
* **Target Git Branch**: `main` (Automatically triggers GitHub Pages deployment)
* **Affiliate Tag Integrity**: **`smartdeal0358-21`** (100% compliance across 21 international Amazon domains)

---

## 📊 Current System State & Verified Disk Assets

* 📦 **Active Storefront Catalog** (`index.html`): **21 Products**
* 🖼️ **Raw Amazon Seller Images** (`raw_images/`): **21 Files** (100% 1:1 match, 0 missing, 0 corrupt)
* 🎨 **Clean Flux Dev AI Images** (`flux_clean_images/`): **21 Files** (100% 1:1 match, 0 missing, 0 corrupt)
* 🏷️ **Graphic Price Overlay Badges** (`focus_product_{ASIN}_hook.jpg`): **21 Re-rendered Files** (Stamped on top of `flux_clean_images/`)
* 🌐 **Live GitHub Pages Sync**: `origin/main` (100% Up to Date, Zero Drift)

---

## ⚙️ Core Technical Engines & Architecture

### 1. 🎨 Dynamic Precision `prompt_strength` Engine (`modules/amazon_extractor.py`)
To prevent object hallucination, item count alteration, or loss of fragile material textures (like glass, metal rings, or mirror curves), the engine dynamically evaluates product titles and backgrounds to assign hyper-precise Img2Img prompt strengths:

| Tier | Category & Keywords | Precision Strength | Fidelity Target |
| :--- | :--- | :--- | :--- |
| **Tier 1** | **Multi-Packs & Intricate Item Sets**<br>*`set of`, `pack of`, `2-piece`, `3-piece`, `suncatcher`, `prism`, `crystal`* | **`0.28`** | Locks **100% exact item count and physical geometry**. Prevents Flux Dev from duplicating or altering items. |
| **Tier 2** | **Fragile Glass & Ambient Lighting**<br>*`glass mushroom`, `striped glass`, `bedside lamp`, `candle warmer`, `flame diffuser`* | **`0.44`** | Protects fragile glass transparency, hand-blown textures, and warm ambient mist/glow intensity. |
| **Tier 3** | **Mirrors & Thinker Sculptures**<br>*`vanity mirror`, `wavy mirror`, `thinker statue`, `sculpture`* | **`0.48`** | Locks frame curves, border lines, and reflection geometry while enhancing room background depth. |
| **Tier 4** | **Pure White Studio Cutouts**<br>*`is_white_bg = True`* | **`0.80`** | Synthesizes a brand-new, complete 3:4 Architectural Digest room scene from scratch around the product cutout. |

* **Central API**: `calculate_precision_prompt_strength(title: str, is_white_bg: bool = False)` in [`modules/amazon_extractor.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/amazon_extractor.py).

---

### 2. 📂 Dedicated Clean AI Image Storage (`flux_clean_images/`)
* All Replicate **Flux Dev** AI lifestyle outputs are automatically saved into a dedicated directory: `flux_clean_images/clean_focus_product_{ASIN}.jpg`.
* This guarantees that clean, text-free AI lifestyle room photos are preserved permanently, separate from raw seller source photos (`raw_images/raw_{ASIN}.jpg`).

---

### 3. 🏷️ Priority #1 Price Overlay Image Selection (`daily_price_updater.py`)
* Whenever a daily price update runs, [`daily_price_updater.py`](file:///G:/CLI/pinterest-auto-affiliate/daily_price_updater.py) checks **`flux_clean_images/` as Priority #1**.
* Playwright re-renders the floating glassmorphic price tag badge (`focus_product_{ASIN}_hook.jpg`) directly on top of the clean Flux Dev AI room photo instead of raw seller photos.

---

### 4. 🗑️ Single-Command Product Deletion Engine (`delete_product.py`)
* Standardized deletion command: `python delete_product.py <ASIN>`
* Automatically removes landing page `bridge_{ASIN}.html`, storefront card `card-{ASIN}`, registry entry `product_price_registry.json`, geo-matrix entry `global_direct_matrix.json`, raw images, clean Flux images, and commits the deletion live to GitHub main.
* Successfully executed for `B0GYDXHF4G` (Flame Aroma Diffuser), reducing catalog size from 22 to 21 active products cleanly.

---

### 5. 🛡️ Automated Zero-Drift Health Check & Self-Healing (`run_daily_health_check.py`)
* Command: `python run_daily_health_check.py`
* Automatically compares live Amazon prices against `index.html` data attributes, self-heals mismatches, and commits updates to GitHub Pages (`main` branch).

---

## 📦 Verified Active Product Catalog (21 ASINs)

| # | ASIN | Product Title | Price | Raw Seller Image | Clean Flux Dev Image | Live Amazon Link | Bridge Landing Page |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `B0BYP7XB7S` | LCCCK White & Silver Ceramic Vases | $38.99 | [`raw_B0BYP7XB7S.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0BYP7XB7S.jpg) | [`clean_focus_product_B0BYP7XB7S.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0BYP7XB7S.jpg) | [Amazon](https://www.amazon.com/dp/B0BYP7XB7S) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0BYP7XB7S.html) |
| 2 | `B0FFG48KCY` | Abstract Reading Thinker Statues | $19.99 | [`raw_B0FFG48KCY.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0FFG48KCY.jpg) | [`clean_focus_product_B0FFG48KCY.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0FFG48KCY.jpg) | [Amazon](https://www.amazon.com/dp/B0FFG48KCY) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0FFG48KCY.html) |
| 3 | `B0D1G6ZL7Y` | Glass Mushroom Table Lamp | $35.99 | [`raw_B0D1G6ZL7Y.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0D1G6ZL7Y.jpg) | [`clean_focus_product_B0D1G6ZL7Y.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0D1G6ZL7Y.jpg) | [Amazon](https://www.amazon.com/dp/B0D1G6ZL7Y) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0D1G6ZL7Y.html) |
| 4 | `B0DC6HDMRM` | Lukasa Candle Warmer Lamp | $24.99 | [`raw_B0DC6HDMRM.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0DC6HDMRM.jpg) | [`clean_focus_product_B0DC6HDMRM.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0DC6HDMRM.jpg) | [Amazon](https://www.amazon.com/dp/B0DC6HDMRM) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0DC6HDMRM.html) |
| 5 | `B0BPM41R5C` | Ceramic Hand Sculpture Ring Holder | $16.99 | [`raw_B0BPM41R5C.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0BPM41R5C.jpg) | [`clean_focus_product_B0BPM41R5C.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0BPM41R5C.jpg) | [Amazon](https://www.amazon.com/dp/B0BPM41R5C) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0BPM41R5C.html) |
| 6 | `B0D5YNHXQ7` | Glivpny Vintage Ceramic Mushroom Lamp | $84.06 | [`raw_B0D5YNHXQ7.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0D5YNHXQ7.jpg) | [`clean_focus_product_B0D5YNHXQ7.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0D5YNHXQ7.jpg) | [Amazon](https://www.amazon.com/dp/B0D5YNHXQ7) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0D5YNHXQ7.html) |
| 7 | `B0D6YRJLCP` | Gold Metal Arch Standing Mirror | $12.49 | [`raw_B0D6YRJLCP.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0D6YRJLCP.jpg) | [`clean_focus_product_B0D6YRJLCP.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0D6YRJLCP.jpg) | [Amazon](https://www.amazon.com/dp/B0D6YRJLCP) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0D6YRJLCP.html) |
| 8 | `B0BXP7YWHJ` | CEMABT White Ceramic Donut Vases | $9.99 | [`raw_B0BXP7YWHJ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0BXP7YWHJ.jpg) | [`clean_focus_product_B0BXP7YWHJ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0BXP7YWHJ.jpg) | [Amazon](https://www.amazon.com/dp/B0BXP7YWHJ) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0BXP7YWHJ.html) |
| 9 | `B0C7WFZZ7D` | Hollow Ceramic Snuggle Vase Set | $12.49 | [`raw_B0C7WFZZ7D.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0C7WFZZ7D.jpg) | [`clean_focus_product_B0C7WFZZ7D.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0C7WFZZ7D.jpg) | [Amazon](https://www.amazon.com/dp/B0C7WFZZ7D) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0C7WFZZ7D.html) |
| 10 | `B0BQGC76VX` | Irregular Wavy Wall Mirror | $44.09 | [`raw_B0BQGC76VX.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0BQGC76VX.jpg) | [`clean_focus_product_B0BQGC76VX.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0BQGC76VX.jpg) | [Amazon](https://www.amazon.com/dp/B0BQGC76VX) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0BQGC76VX.html) |
| 11 | `B0CJ4Q4PZQ` | Pink Striped Glass Mushroom Lamp | $34.99 | [`raw_B0CJ4Q4PZQ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0CJ4Q4PZQ.jpg) | [`clean_focus_product_B0CJ4Q4PZQ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0CJ4Q4PZQ.jpg) | [Amazon](https://www.amazon.com/dp/B0CJ4Q4PZQ) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0CJ4Q4PZQ.html) |
| 12 | `B0CJC549C6` | Matte Black Thinker Statue Set | $19.99 | [`raw_B0CJC549C6.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0CJC549C6.jpg) | [`clean_focus_product_B0CJC549C6.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0CJC549C6.jpg) | [Amazon](https://www.amazon.com/dp/B0CJC549C6) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0CJC549C6.html) |
| 13 | `B0CX144DHK` | Glivpny Mid Century Mushroom Lamp | $93.90 | [`raw_B0CX144DHK.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0CX144DHK.jpg) | [`clean_focus_product_B0CX144DHK.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0CX144DHK.jpg) | [Amazon](https://www.amazon.com/dp/B0CX144DHK) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0CX144DHK.html) |
| 14 | `B0FGJ1S73D` | Ceramic Mushroom Bedside Lamp | $43.73 | [`raw_B0FGJ1S73D.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0FGJ1S73D.jpg) | [`clean_focus_product_B0FGJ1S73D.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0FGJ1S73D.jpg) | [Amazon](https://www.amazon.com/dp/B0FGJ1S73D) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0FGJ1S73D.html) |
| 15 | `B0FXLYXM32` | Wavy Full Length Floor Standing Mirror | $76.49 | [`raw_B0FXLYXM32.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0FXLYXM32.jpg) | [`clean_focus_product_B0FXLYXM32.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0FXLYXM32.jpg) | [Amazon](https://www.amazon.com/dp/B0FXLYXM32) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html) |
| 16 | `B0C2YLN3H4` | Modern Ceramic Donut Vase Set of 2 | $19.99 | [`raw_B0C2YLN3H4.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0C2YLN3H4.jpg) | [`clean_focus_product_B0C2YLN3H4.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0C2YLN3H4.jpg) | [Amazon](https://www.amazon.com/dp/B0C2YLN3H4) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html) |
| 17 | `B07HP22QTZ` | Hanging Crystal Suncatcher Prism | $14.99 | [`raw_B07HP22QTZ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B07HP22QTZ.jpg) | [`clean_focus_product_B07HP22QTZ.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B07HP22QTZ.jpg) | [Amazon](https://www.amazon.com/dp/B07HP22QTZ) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B07HP22QTZ.html) |
| 18 | `B0BZXNSW5K` | Touch Control Dimmable Bedside Lamp | $19.99 | [`raw_B0BZXNSW5K.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0BZXNSW5K.jpg) | [`clean_focus_product_B0BZXNSW5K.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0BZXNSW5K.jpg) | [Amazon](https://www.amazon.com/dp/B0BZXNSW5K) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html) |
| 19 | `B0DXKGL1T2` | Lily of the Valley Flower Desk Lamp | $38.57 | [`raw_B0DXKGL1T2.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0DXKGL1T2.jpg) | [`clean_focus_product_B0DXKGL1T2.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0DXKGL1T2.jpg) | [Amazon](https://www.amazon.com/dp/B0DXKGL1T2) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0DXKGL1T2.html) |
| 20 | `B0D1FRDFFX` | Handmade Glass Mushroom Ambient Lamp | $41.34 | [`raw_B0D1FRDFFX.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0D1FRDFFX.jpg) | [`clean_focus_product_B0D1FRDFFX.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0D1FRDFFX.jpg) | [Amazon](https://www.amazon.com/dp/B0D1FRDFFX) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0D1FRDFFX.html) |
| 21 | `B0D8P8CSYP` | Cute Bird Touch Control Nightstand Lamp | $9.98 | [`raw_B0D8P8CSYP.jpg`](file:///G:/CLI/pinterest-auto-affiliate/raw_images/raw_B0D8P8CSYP.jpg) | [`clean_focus_product_B0D8P8CSYP.jpg`](file:///G:/CLI/pinterest-auto-affiliate/flux_clean_images/clean_focus_product_B0D8P8CSYP.jpg) | [Amazon](https://www.amazon.com/dp/B0D8P8CSYP) | [Bridge](https://adityasnalawade742-design.github.io/bridge_B0D8P8CSYP.html) |

---

## 🛠️ Verification & Maintenance Workflows

1. **Verify Codebase Quality & Fixes**:
   ```bash
   python check_fixes.py
   ```
2. **Run Zero-Drift Daily Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
3. **Delete a Product**:
   ```bash
   python delete_product.py <ASIN>
   ```
4. **Re-render Graphic Badges from Clean AI Images**:
   ```bash
   python scratch/rebuild_all_badges_from_flux.py
   ```
5. **Run Web Console Server (Port 5000)**:
   ```bash
   python web_console_server.py
   ```
