# 🏛️ Pinterest Auto Affiliate Platform: Complete System Architecture & Reference Guide

> **Primary Master Documentation**: This file serves as the single source of truth for the entire automated Pinterest affiliate marketing ecosystem, multi-region landing page engines, dynamic currency conversion systems, and empirical Amazon geo-redirect matrix.

---

## 📌 Executive Summary & Core Purpose

This platform is a high-converting, fully automated affiliate marketing system designed to:
1. Convert Pinterest traffic into high-yield Amazon Affiliate commissions.
2. Provide **100% Zero 404 Error** landing pages for global visitors across **21 international Amazon domains**.
3. Dynamically adapt pricing, currency symbols, and Call-to-Action (CTA) routing based on visitor IP or country parameters.
4. Protect **100% of outgoing revenue links** with tag `smartdeal0358-21`.

---

## ⚙️ Key System Features & Architectural Subsystems

### 1. 🌐 Universal Multi-Region Geo-Redirector Engine (`bridge_creator.py`)
* **Dynamic Location Detection**: Detects visitor country code (`cc`) via URL parameter (`?country=XX`) or IP geo-location APIs (`ipapi.co`).
* **Empirical Matrix Routing (`global_direct_matrix.json`)**:
  * **Direct ASIN Page (`/dp/{asin}`)**: Used ONLY when the exact ASIN has been empirically verified to exist live in that country's local Amazon catalog (*e.g., US, UK, DE, IN, CA, JP, AU*).
  * **Targeted Category Search Fallback (`/s?k={keywords}`)**: Used when the exact ASIN code is not directly listed in that country (*e.g., Netherlands VPN, Brazil, UAE, Mexico*). Buyers land on live relevant local product search results carrying tag `smartdeal0358-21`.
  * **Zero 404 Guarantee**: Eliminates Amazon's internal *"Looking for something? We're sorry"* 404 page across 100% of global visits.

### 2. 💱 Global Multi-Currency Price Engine (160+ World Currencies)
* **Real Scraped Prices**: Uses daily scraped prices for primary markets (`USD`, `EUR`, `GBP`, `CAD`, `AUD`, `INR`, `JPY`).
* **Native Exchange Rate Conversions**: Converts USD base price to 160+ world currencies for international markets (*e.g., Sweden `kr`, Brazil `R$`, UAE `AED`, Mexico `Mex$`, Poland `PLN`, South Korea `₩`*).
* **Strike-Through List Prices & Savings Badges**: Displays glowing **`🔥 SAVE 20% OFF`** to **`🔥 SAVE 33% OFF`** discount badges and original list prices to maximize click-through conversion.

### 3. 🚨 Out-of-Stock & Regional Availability Engine
* **Regional Out-of-Stock**: When an item is explicitly marked out of stock in a scraped market (*e.g., Flame Diffuser in India*):
  * **Top Badge**: Renders soft glowing red 🔴 **`⚠️ NOT AVAILABLE IN YOUR REGION`**.
  * **Hero Price Tag**: Displays **`Not Available`**.
  * **CTA Button Action**: Switches to targeted category search fallback (*`SEARCH LOCAL DEALS ON AMAZON INDIA (₹)`*).

### 4. 🛒 Storefront Homepage (`index.html`) Features
* **Live Instant Search**: Filter cards dynamically by title or keyword.
* **1-Click Search Clear (`✕`)**: Instantly resets search input and restores all 9 product cards.
* **Category Chips**: Filter by `✨ All Finds`, `💡 Aesthetic Lighting`, `🌿 Room Decor`, `🏺 Ceramic Vases`, `🪞 Vanity Mirrors`.
* **Global Currency Selector**: Dropdown to switch all homepage card prices to any world currency.
* **Scoped Admin Mode (`?admin=true`)**: Public visitors see 0 delete buttons. Reveals admin controls ONLY when `?admin=true` is present.

### 5. 🔍 SEO & Crawler Optimization (`sitemap.xml` & `robots.txt`)
* **Indexable Sitemap**: Includes all 9 bridge landing pages and index page for Googlebot & Pinterestbot.
* **Crawler Rules**: Clean `robots.txt` allowing full indexing of static assets and landing pages.

---

## 📦 Master Product Catalog (9 Active ASINs)

| ASIN | Product Title | Primary Category | Verified Direct ASIN Regions | Search Fallback Regions |
| :--- | :--- | :--- | :--- | :--- |
| **`B0BZXNSW5K`** | Touch Bedside Lamp | Lighting | `UK`, `IN`, `DE`, `NL`, `FR`, `IT`, `ES`, `SE` | `US`, `CA`, `MX`, `BR`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `JP`, `AU`, `SG` |
| **`B0C2YLN3H4`** | White Donut Vases | Home Decor | `IN`, `AU`, `JP`, `DE`, `NL`, `FR`, `IT`, `ES`, `SE` | `US`, `CA`, `MX`, `BR`, `UK`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `SG` |
| **`B07HP22QTZ`** | Crystal Suncatcher | Home Decor | `UK`, `IN`, `AU`, `JP`, `DE`, `NL`, `FR`, `IT`, `ES`, `SE` | `US`, `CA`, `MX`, `BR`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `SG` |
| **`B0D8P8CSYP`** | Cute Bird Touch Lamp | Lighting | `UK`, `IN`, `AU`, `JP`, `DE`, `NL`, `FR`, `IT`, `ES`, `SE` | `US`, `CA`, `MX`, `BR`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `SG` |
| **`B0D1FRDFFX`** | Glass Mushroom Lamp | Lighting | `UK`, `IN`, `AU`, `DE`, `NL`, `FR`, `IT`, `ES`, `SE` | `US`, `CA`, `MX`, `BR`, `JP`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `SG` |
| **`B0GYDXHF4G`** | Flame Aroma Diffuser | Home Decor | *(Search Fallback Active Across All Regions)* | All 21 Amazon Domains |
| **`B0DXKGL1T2`** | Lily of Valley Lamp | Lighting | `UK` | All Other 20 Amazon Domains |
| **`B0DZD1X83N`** | Minimalist Wood Lamp | Lighting | `US` | All Other 20 Amazon Domains |
| **`B0FXLYXM32`** | White Wavy Mirror | Home Decor | `UK`, `IN`, `AU`, `JP`, `DE`, `FR`, `IT`, `ES` | `US`, `CA`, `MX`, `BR`, `NL`, `SE`, `PL`, `BE`, `TR`, `AE`, `SA`, `EG`, `SG` |

---

## 🛠️ Essential Core Scripts & CLI Commands

### Rebuild 100% of All Landing Pages & Push Live:
```bash
python rebuild_EVERY_single_bridge.py
```

### Daily Multi-Region Price Sync:
```bash
python sync_exact_amazon_prices.py
```

### Run Master 189-Point Zero 404 Audit:
```bash
python scratch/master_zero_404_audit.py
```

### Run 360-Degree Full Feature Audit:
```bash
python scratch/master_360_feature_audit.py
```

---

## 🔒 Security & Revenue Rules
1. **Affiliate Tag Guard**: `smartdeal0358-21` MUST remain attached to 100% of outgoing CTA links.
2. **Empirical Direct Matrix**: NEVER add a country code to `global_direct_matrix.json` without verifying live HTTP 200 product page existence via Playwright / Requests.
3. **No Breaking Lints or 404s**: Always test rebuilt bridge pages using Playwright before deployment.
