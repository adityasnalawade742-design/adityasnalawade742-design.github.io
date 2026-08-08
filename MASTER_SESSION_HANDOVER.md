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

1. **Price Scraper Integrity Remediation & Targeted Audit**:
   - Built [`modules/price_registry_manager.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/price_registry_manager.py) to manage structured price records, DOM seller info, status semantics (`FRESH_VERIFIED`, `FRESH_UNVERIFIED`, `STALE_VERIFIED`, `NOT_MAPPED`), and 7-day TTL stale price logic.
   - Prohibited US ASIN fallback scraper pollution across all regional domain scrapers (`scrape_in.py`, `scrape_uk.py`, `scrape_extended_domains.py`).
   - Created [`test_price_scraper_integrity.py`](file:///G:/CLI/pinterest-auto-affiliate/test_price_scraper_integrity.py) with 9/9 PASS.
   - Targeted read-only audit completed: Verified identity isolation on `B0BXP7YWHJ` (`NOT_MAPPED`) and `B0CX144DHK` (`FRESH_VERIFIED`).

2. **Verified 10-Marketplace OneLink Architecture**:
   - `US`, `CA`, `GB/UK`, `FR`, `DE`, `IT`, `ES`, `NL`, `PL`, `SE` configured for OneLink canonical URL routing (`amazon.com/dp/{ASIN}?tag=smartdeal0358-20`).

3. **India Tag & Direct Listing Isolation**:
   - Preserved `smartdeal0358-21` isolation for India (`amazon.in/dp/...` or `amazon.in/s?k=...`).

4. **Automated Test Suite Verification (100% PASS)**:
   - `python check_fixes.py` (PASS)
   - `python test_affiliate_routing.py` (8/8 PASS)
   - `python audit_all_affiliate_tags.py` (PASS)
   - `python validate_all_affiliate_urls.py` (23/23 PASS)
   - `python test_bridge_geo_routing.py` (8/8 PASS)
   - `python test_price_scraper_integrity.py` (9/9 PASS)

---

## 📌 Instructions for Resuming in a New Session / Account

1. All code, templates, and documentation are committed and pushed to `main`.
2. To post all 23 pins live to production boards once Pinterest grants Standard Access:
   ```powershell
   python publish_all_homepage_pins.py prod
   ```
