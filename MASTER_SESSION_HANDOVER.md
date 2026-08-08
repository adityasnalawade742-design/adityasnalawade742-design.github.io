# 🏛️ MASTER SESSION HANDOVER & STATE PRESERVATION RECORD

> **RESTART SAFE HANDOVER**: This file preserves the exact project status, recent bug fixes, operational credentials, and step-by-step instructions so that any AGY instance, new session, or account switch can resume work seamlessly without context loss.

---

## 📌 Executive Summary

* **Project Name**: Pinterest Auto Affiliate System (`pinterest-auto-affiliate`)
* **Local Path**: `G:\CLI\pinterest-auto-affiliate`
* **GitHub Repository**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`
* **Live Site**: `https://adityasnalawade742-design.github.io/`
* **Active Products**: **23 Verified Products** (100% compiled & deployed to GitHub Pages)
* **Canonical US Tag (OneLink)**: `smartdeal0358-20` (Active for 10 Marketplaces: US, CA, UK/GB, FR, DE, IT, ES, NL, PL, SE)
* **India Fallback Tag**: `smartdeal0358-21`
* **Pinterest Developer App**: Cozy Room Decor Publisher Pro (App ID: `1596368`)

---

## 🔑 Credentials & Environment Summary (`.env`)

* `PINTEREST_APP_ID`: `"1596368"`
* `PINTEREST_CLIENT_SECRET`: `"edb85c72428604586ec3bffaeaf7fd97e9c87782"`
* `PINTEREST_ACCESS_TOKEN`: Active production token (`pina_AEA...`)
* `PINTEREST_SANDBOX_ACCESS_TOKEN`: Active Sandbox token (`pina_AMA5...`)
* `PINTEREST_SANDBOX_BOARD_ID`: `"1092545259543959836"` (`Cozy Decor Sandbox Board`)
* `REPLICATE_API_TOKEN`: Active Flux Dev token (`r8_fK...`)
* `AMAZON_ASSOCIATE_TAG`: `smartdeal0358-20`
* `INDIA_ASSOCIATE_TAG`: `smartdeal0358-21`

---

## 🚀 Major Milestones Completed & Verified

1. **Verified 10-Marketplace OneLink Architecture**:
   - `US`, `CA`, `GB/UK`, `FR`, `DE`, `IT`, `ES`, `NL`, `PL`, `SE` configured for OneLink canonical URL routing (`amazon.com/dp/{ASIN}?tag=smartdeal0358-20`).
   - Rebuilt all 23 bridge pages via `rebuild_EVERY_single_bridge.py` and deployed live to GitHub Pages.

2. **Price Verification & OneLink Routing Independence**:
   - Verified that OneLink routing and Regional Price Verification are 100% separate concepts. Unlisted items in OneLink countries are tagged `⚠️ UNLISTED IN REGION • Approx. [price]` with red warning styling.

3. **India Tag & Direct Listing Isolation**:
   - Preserved `smartdeal0358-21` isolation for India (`amazon.in/dp/...` or `amazon.in/s?k=...`).

4. **Pinterest Batch Publishing (100% PASS)**:
   - Executed batch publishing of all 23 products to Pinterest API v5 Sandbox Board `1092545259543959836` with 100% success rate (`HTTP 201 Created`).

5. **Automated Test Suite Verification (100% PASS)**:
   - `python check_fixes.py` (PASS)
   - `python test_affiliate_routing.py` (8/8 PASS)
   - `python audit_all_affiliate_tags.py` (PASS)
   - `python validate_all_affiliate_urls.py` (23/23 PASS)
   - `python test_bridge_geo_routing.py` (8/8 PASS including NL, PL, SE)

---

## 📌 Instructions for Resuming in a New Session / Account

1. All code, templates, and documentation are committed and pushed to `main`.
2. To post all 23 pins live to production boards once Pinterest grants Standard Access:
   ```powershell
   python publish_all_homepage_pins.py prod
   ```
