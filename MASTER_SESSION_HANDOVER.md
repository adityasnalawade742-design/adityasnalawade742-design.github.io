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

1. **Marketplace-Aware Seller Verification & Rendered-Page ASIN Identity Fix**:
   - Upgraded [`modules/price_registry_manager.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/price_registry_manager.py) with `verify_seller()` (distinguishes Amazon seller, 3rd party + Amazon fulfillment, and 3rd party) and `extract_page_asin()` (extracts ASIN from `input#ASIN`, `#dp[data-asin]`, canonical tag, and page URL).
   - Enforced that `STATUS_FRESH_VERIFIED` strictly requires `is_direct == True`, `identity_verified == True`, AND `seller_verified == True`.
   - Updated scrapers (`scrape_us.py`, `scrape_in.py`, `scrape_uk.py`, `scrape_extended_domains.py`).
   - Added Rule 7 Tests 1–7 to [`test_price_scraper_integrity.py`](file:///G:/CLI/pinterest-auto-affiliate/test_price_scraper_integrity.py) (16/16 PASS).

2. **Read-Only Takeover Audit**:
   - Completed 12-point project state takeover audit (Verdict: 🟢 **TAKEOVER CONSISTENT**).

3. **Automated Test Suite Verification (100% PASS)**:
   - `python test_price_scraper_integrity.py` (16/16 PASS)
   - `python check_fixes.py` (20/20 PASS)
   - `python test_affiliate_routing.py` (8/8 PASS)
   - `python audit_all_affiliate_tags.py` (23/23 PASS)
   - `python validate_all_affiliate_urls.py` (23/23 PASS)
   - `python test_bridge_geo_routing.py` (8/8 PASS)

---

## 📌 Instructions for Resuming in a New Session / Account

1. All code, templates, and documentation are committed and pushed to `main`.
2. To verify system status in a new AGY account or session:
   ```powershell
   python test_price_scraper_integrity.py
   python check_fixes.py
   ```
3. To post all 23 pins live to production boards once Pinterest grants Standard Access:
   ```powershell
   python publish_all_homepage_pins.py prod
   ```
