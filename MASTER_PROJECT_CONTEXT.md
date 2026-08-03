# 🚀 MASTER PROJECT BLUEPRINT & SYSTEM ARCHITECTURE
> **Project Name**: Production Pinterest Auto-Affiliate System  
> **Repository**: `pinterest-auto-affiliate` (`adityasnalawade742-design.github.io`)  
> **Last Verified & Updated**: August 3, 2026  
> **System Status**: 100% Operational • Zero Drift • 45 Currencies • 21 Amazon Storefront Domains • n8n Webhook Workflow Integrated

---

## 📌 1. EXECUTIVE SUMMARY & SYSTEM OVERVIEW

This repository houses an automated, high-converting **Pinterest Auto-Affiliate Engine** designed to monetize global viral traffic. It features:
* A dynamic luxury storefront ([`index.html`](file:///G:/CLI/pinterest-auto-affiliate/index.html)).
* High-converting luxury bridge landing pages ([`bridge_*.html`](file:///G:/CLI/pinterest-auto-affiliate/bridge_B0FGJ1S73D.html)).
* A central empirical JSON registry ([`product_price_registry.json`](file:///G:/CLI/pinterest-auto-affiliate/product_price_registry.json)).
* A web console proxy & bridge server ([`web_console_server.py`](file:///G:/CLI/pinterest-auto-affiliate/web_console_server.py)).
* n8n Workflow Integration (Nodes 1-7 pipeline orchestrating product scraping, AI copywriting, bridge creation, graphic overlay rendering, and status tracking).
* 0ms Instant Synchronous Geo-Redirector Engine ([`modules/bridge_creator.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/bridge_creator.py)).
* High-res Playwright Pin Graphic Engine ([`modules/html_overlay_engine.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/html_overlay_engine.py)).
* Master portfolio rebuilder ([`rebuild_EVERY_single_bridge.py`](file:///G:/CLI/pinterest-auto-affiliate/rebuild_EVERY_single_bridge.py)).

---

## 🛡️ 2. THE 8 PRECISION CORE SUBSYSTEMS

### 1. ⚡ 0ms Instant Synchronous Geo-Redirector Engine (`modules/bridge_creator.py`)
* **Purpose**: Detects visitor country instantly (0ms) using browser timezone (`Asia/Kolkata`, `Europe/London`, `Asia/Tokyo`) and language signals (`en-IN`, `hi`).
* **Adblocker Proof**: Works synchronously before network requests fire, ensuring visitors from India (`amazon.in`), UK (`amazon.co.uk`), DE, JP, CA, AU never see raw `.com` links even if privacy extensions block external IP lookup services.
* **Search Fallback Engine**: If a product model code is only directly listed in the US, non-US visitors get an automatic notice box + direct search CTA (`https://www.amazon.in/s?k=...`) preserving affiliate tags (`smartdeal0358-21`).

### 2. 🤖 n8n Workflow & Web Console Proxy Bridge (`web_console_server.py`)
* **Purpose**: Serves local Web Console UI and proxies requests between local python engines and n8n webhook workflows.
* **Key Endpoints**:
  * `/api/create_bridge_page`: Called by n8n Node 6/7 to compile luxury Jinja2 bridge pages and invoke Playwright overlay engine.
  * `/api/batch_extract`: Scrapes Amazon US details, extracts lifestyle images, and formats full payloads.
  * `/api/proxy_n8n`: Forwards requests directly to n8n webhook (`http://localhost:5678/webhook/...`) and tracks task execution status.

### 3. 🖼️ Playwright Floating Pin Graphic Engine (`modules/html_overlay_engine.py`)
* **Purpose**: Generates high-res 1200x1600 Pinterest pin graphics with floating product callouts.
* **Design Specifications**:
  * **4-Column Grid Alignment**: Equal-width side-by-side feature cards across the bottom (`grid-template-columns: repeat(4, 1fr)`).
  * **Dark Glassmorphic Backdrop**: `background: rgba(15, 14, 19, 0.72)` + backdrop blur + 1.5px subtle border for 100% text contrast.
  * **Bold White Typography**: 13.5px bold white uppercase text (`font-weight: 800`) with clean `✨` sparkle icons and single-line ellipsis truncation.

### 4. 🔨 Dynamic Master Rebuilder (`rebuild_EVERY_single_bridge.py`)
* **Purpose**: Automatically merges static catalog entries with empirical data from `product_price_registry.json` and `global_direct_matrix.json`.
* **Sitemap Generator**: Auto-generates `sitemap.xml` with 100% of portfolio landing page URLs.
* **GitHub Pages Auto-Deploy**: Runs `git add`, `git commit`, and `git push origin main` after rebuilding.

### 5. 🛡️ Automated "Zero-Drift" Self-Healing Bot (`run_daily_health_check.py`)
* **Purpose**: Compares 100% of price values between `product_price_registry.json`, `index.html`, and all `bridge_*.html` landing pages after every price update.
* **Guarantee**: Automatically heals and corrects any 1-penny/rupee discrepancy.

### 6. 🗺️ Regional ASIN Variant Mapper (Direct `/dp/` Upgrader)
* **Purpose**: Maps local model ASIN codes when a product is sold under different ASINs in different countries (e.g. US `B0DZD1X83N` vs European `B0F946YHSZ`).

### 7. 🏦 Official Native Financial Formatting Engine
* **Purpose**: Formats numbers and currency symbols according to native banking standards:
  * **🇺🇸/🇮🇳/🇬🇧/🇨🇦/🇦🇺**: Period decimal (`$32.99`, `₹2,754.67`, `£15.59`).
  * **🇪🇺 Europe**: Comma decimal & space thousands (`18,40 €`).
  * **🇯🇵 Japan**: Pure integer formatting (`¥3,100`).

### 8. 🌍 45-Currency Real-Time Exchange Rate Sync Engine
* **Purpose**: Fetches live exchange rates from `https://open.er-api.com/v6/latest/USD` on both `index.html` and `bridge_*.html` pages.

---

## 🔑 3. OFFICIAL AMAZON ASSOCIATE STORE IDs

| Region | Storefront Domain | Official Store ID | Status |
| :--- | :--- | :--- | :--- |
| 🇺🇸 **United States** | `Amazon.com` | `smartdeal0358-20` | **Primary Geo** |
| 🇨🇦 **Canada** | `Amazon.ca` | `smartdeal0302-20` | Native |
| 🇮🇳 **India** | `Amazon.in` | `smartdeal0358-21` | Native |
| 🇬🇧 **United Kingdom** | `Amazon.co.uk` | `smartdea04b3a-21` | Native |
| 🇩🇪 **Germany** | `Amazon.de` | `smartdeal0bb4-21` | Native |
| 🇫🇷 **France** | `Amazon.fr` | `smartdeal0962-21` | Native |
| 🇪🇸 **Spain** | `Amazon.es` | `smartdeal0b46-21` | Native |
| 🇮🇹 **Italy** | `Amazon.it` | `smartdea03a8d-21` | Native |
| 🇸🇪 **Sweden** | `Amazon.se` | `smartdeal0bb4-21` | OneLink ➔ DE |
| 🇳🇱 **Netherlands** | `Amazon.nl` | `smartdeal0bb4-21` | OneLink ➔ DE |
| 🇵🇱 **Poland** | `Amazon.pl` | `smartdeal0bb4-21` | OneLink ➔ DE |
| 🇹🇷 **Turkey** | `Amazon.com.tr` | `smartdeal0bb4-21` | OneLink ➔ DE |
| 🇧🇪 **Belgium** | `Amazon.com.be` | `smartdeal0962-21` | OneLink ➔ FR |
| 🇲🇽 **Mexico** | `Amazon.com.mx` | `smartdeal0358-20` | OneLink ➔ US |
| 🇧🇷 **Brazil** | `Amazon.com.br` | `smartdeal0358-20` | OneLink ➔ US |
| 🇸🇬 **Singapore** | `Amazon.sg` | `smartdeal0358-20` | OneLink ➔ US |
| 🇦🇪 **UAE** | `Amazon.ae` | `smartdeal0358-20` | OneLink ➔ US |
| 🇸🇦 **Saudi Arabia** | `Amazon.sa` | `smartdeal0358-20` | OneLink ➔ US |
| 🇪🇬 **Egypt** | `Amazon.eg` | `smartdeal0358-20` | OneLink ➔ US |
| 🇯🇵 **Japan** | `Amazon.co.jp` | `smartdeal0358-20` | OneLink ➔ US |
| 🇦🇺 **Australia** | `Amazon.com.au` | `smartdeal0358-20` | OneLink ➔ US |

---

## 📁 4. REPOSITORY STRUCTURE & KEY SCRIPTS

```text
G:\CLI\pinterest-auto-affiliate\
├── index.html                               # Dynamic Luxury Storefront Showcase
├── product_price_registry.json              # Master Empirical Product Data Registry
├── web_console_server.py                    # Web Console UI & n8n Webhook Proxy Server
├── rebuild_EVERY_single_bridge.py           # Dynamic Portfolio Rebuilder & Deployer
├── run_daily_health_check.py                # Automated Zero-Drift Self-Healing Bot
├── validate_all_affiliate_urls.py           # Outbound Link & Store ID Crawler
├── bridge_B0FGJ1S73D.html                   # Landing Page: Ceramic Mushroom Bedside Lamp
├── focus_product_B0FGJ1S73D_hook.jpg        # High-Res 1200x1600 Floating Pin Graphic
├── modules/
│   ├── bridge_creator.py                    # Jinja2 Bridge Page Generator & Geo-Redirector JS
│   ├── html_overlay_engine.py               # Playwright 1200x1600 Graphic Pin Renderer
│   ├── amazon_extractor.py                  # Scrapes Product Details, Prices & Photos
│   └── scrapers/                            # Playwright Scraper Suite (21 Amazon Domains)
```

---

## 🛠️ 5. QUICK RECOVERY & DEPLOYMENT COMMANDS

If switching machines, AGY CLI instances, or fresh clones:

1. **Start Local Web Console Server**:
   ```bash
   python web_console_server.py
   ```
2. **Rebuild 100% of Landing Pages & Deploy Live to GitHub Pages**:
   ```bash
   python rebuild_EVERY_single_bridge.py
   ```
3. **Run Zero-Drift Health Check**:
   ```bash
   python run_daily_health_check.py
   ```
4. **Scrape Real Product Details for ASIN**:
   ```bash
   python -c "from modules.amazon_extractor import get_product_details_and_photos; print(get_product_details_and_photos('ASIN_HERE'))"
   ```
