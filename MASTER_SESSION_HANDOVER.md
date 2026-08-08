# 🏛️ MASTER SESSION HANDOVER & STATE PRESERVATION RECORD

> **RESTART SAFE HANDOVER**: This file preserves the exact project status, recent bug fixes, operational credentials, and step-by-step instructions so that any AGY instance, new session, or account switch can resume work seamlessly without context loss.

---

## 📌 Executive Summary

* **Project Name**: Pinterest Auto Affiliate System (`pinterest-auto-affiliate`)
* **Local Path**: `G:\CLI\pinterest-auto-affiliate`
* **GitHub Repository**: `https://github.com/adityasnalawade742-design/adityasnalawade742-design.github.io.git`
* **Live Site**: `https://adityasnalawade742-design.github.io/`
* **Active Products**: **23 Verified Products** (100% compiled & deployed to GitHub Pages)
* **Canonical US Tag (OneLink)**: `smartdeal0358-20`
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

## 🚀 Major Milestones Completed in Current Session

1. **Authoritative Network-First Geo-Engine**:
   - Reverted client-side JS in [`modules/bridge_creator.py`](file:///G:/CLI/pinterest-auto-affiliate/modules/bridge_creator.py) to Network-First priority (Cloudflare trace + cascading IP APIs).
   - Added 1.5s fallback deadline timer and single-resolution guard (`commitResolution`) preventing race conditions.

2. **Amazon OneLink & Associate Tag Isolation**:
   - OneLink Countries (`US`, `CA`, `GB/UK`, `DE`, `FR`, `IT`, `ES`): Canonical URL `https://www.amazon.com/dp/{ASIN}?tag=smartdeal0358-20` on `#buyBtn.href`.
   - India (`IN`): Direct ASIN listing (`amazon.in/dp/{IN_ASIN}?tag=smartdeal0358-21`) or search fallback (`amazon.in/s?k=...`).
   - Tag Isolation: 100% verified across all 23 bridge pages and homepage cards.

3. **Verified vs Unverified Price Labeling**:
   - Enforced `isDirectListing === true` requirement for `✨ VERIFIED DEAL` label.
   - Unlisted reseller import prices labeled `⚠️ UNLISTED IN REGION • Approx. [price]`.
   - Real-time exchange rate conversions prefixed with `Approx.`.

4. **Geo-Aware Shipping Badges**:
   - `⚡ Prime 2-Day Free Shipping` for US.
   - `📦 Amazon OneLink International Delivery` for OneLink countries.
   - `📦 Amazon India Delivery Available` for direct India listings.
   - `📦 US Import • Search Amazon.in Deals` for search fallbacks.
   - `📦 Amazon Global Delivery` for unknown countries.

5. **Master System Guide Version 3.1**:
   - Updated [`SYSTEM_SETUP_AND_GLOBAL_LINKING_GUIDE.txt`](file:///G:/CLI/pinterest-auto-affiliate/SYSTEM_SETUP_AND_GLOBAL_LINKING_GUIDE.txt) with accurate 404 detection terminology, OneLink verification caveats, and 21-country catalog classification.

6. **Pinterest Sandbox Batch Execution (100% PASS)**:
   - Built batch publisher script [`publish_all_homepage_pins.py`](file:///G:/CLI/pinterest-auto-affiliate/publish_all_homepage_pins.py).
   - Exported complete JSON payload [`sandbox_pins_payload.json`](file:///G:/CLI/pinterest-auto-affiliate/sandbox_pins_payload.json).
   - **Result**: **23 / 23 SUCCESSFUL (100% PASS)** posted to Sandbox Board `1092545259543959836` with valid Pin IDs returned. Logged in [`pinterest_campaign_tracker.json`](file:///G:/CLI/pinterest-auto-affiliate/pinterest_campaign_tracker.json).

---

## 🧪 Automated Verification Commands

```powershell
python check_fixes.py
python test_affiliate_routing.py
python audit_all_affiliate_tags.py
python validate_all_affiliate_urls.py
python test_bridge_geo_routing.py
```

---

## 📌 Instructions for Resuming in a New Session / Account

1. All code, templates, and documentation are committed and pushed to `main`.
2. Web Console server is bound to `http://127.0.0.1:5000/`.
3. To post all 23 pins live to production boards once Pinterest grants Standard Access:
   ```powershell
   python publish_all_homepage_pins.py prod
   ```
