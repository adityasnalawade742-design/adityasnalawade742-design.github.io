# 🏆 MASTER SESSION HANDOVER & STATE RECOVERY GUIDE

> **PROJECT**: Pinterest Auto Affiliate & Multi-Region Storefront Machine  
> **APP NAME**: Cozy Room Decor Publisher Pro (App ID: `1596368`)  
> **COMPANY / BRAND**: Cozy Room Finds / Cozy Room Decor  
> **DATE**: August 8, 2026  
> **STATUS**: 100% Operational | Full Codebase Audited | n8n Node 7 Hardened | Dual-Branch Synced (`main` + `gh-pages`)  

---

## 📌 Executive Summary & Account Resume Guide

If you start a **new AGY agent session**, switch accounts, or move to a new workspace, this file contains **100% of the state, instructions, credentials context, and commands** required to continue immediately without losing any progress!

---

## 🚀 Quick Restart Commands (Copy & Paste to Resume)

```powershell
# 1. Pull latest code & sync local branches
git checkout main
git pull origin main

# 2. Start Web Console & n8n Bridge Server (Port 5000)
python web_console_server.py

# 3. Launch n8n local instance (if needed)
n8n start

# 4. Verify catalog & zero-drift health check
python run_daily_health_check.py
```

---

## 🔑 Master App Branding & Configuration Reference

- **App Name**: `Cozy Room Decor Publisher Pro`
- **App ID**: `1596368`
- **Company Name**: `Cozy Room Finds`
- **Developer Contact**: `aditya.s.nalawade742@gmail.com`
- **Sandbox Board ID**: `1092545259543959836` (*Cozy Decor Sandbox Board*)
- **Credentials Location**: Saved locally in `.env` file (`PINTEREST_ACCESS_TOKEN`, `REPLICATE_API_TOKEN`)
- **SerpAPI Pool**: 5 Active Keys (969 total searches remaining)

---

## 🛠️ Summary of Key Features Built & Errors Fixed

### 1. 🔌 Pinterest API v5 OAuth 2.0 Integration & Demo Video Readiness
- **Consent Screen Brand Alignment**: Aligned App Name (`Cozy Room Decor Publisher Pro`), App ID (`1596368`), Company (`Cozy Room Finds`), and developer email across `index.html`, `privacy-policy.html`, `admin_console.html`, and bridge template modules.
- **Video Recording Script**: Created a complete 7-scene Loom/OBS recording script in [`PINTEREST_RE_APPLICATION_GUIDE.md`](file:///G:/CLI/pinterest-auto-affiliate/PINTEREST_RE_APPLICATION_GUIDE.md) satisfying reviewer Nana's rejection criteria.

### 2. ⚙️ n8n Workflow Hardening & 400 Bad Request Fixes
- **Recommended Workflow File**: [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json).
- **Node 3 Classifier Fix**: Updated expression to `Boolean($json.is_white_bg || ($json.chosen_photo_url && $json.chosen_photo_url.includes('cutout')))` so Amazon room photos are not falsely routed to Prompt A.
- **Node 5 Flux AI Fix**: Added `Bearer ` prefix to Replicate Authorization header.
- **Node 6 Auto-Publish Fix**: Updated line 1525 of `web_console_server.py` to push to **both `main` and `main:gh-pages`** simultaneously.
- **Node 7 Image Fetch Error Fix**: Updated `media_source` `url` in Node 7 to use `$node['Code in JavaScript'].json.chosen_photo_url` directly or raw GitHub links, bypassing GitHub Pages CDN propagation 404s.
- **Node 7 Expression & Syntax Hardening**: Resolved n8n Expression Engine syntax crashes (`invalid syntax at Expression.renderExpression`) by removing ES6 backticks inside `={{ ... }}`, cleaning variable spaces (`. pin_title`, `. json`), fixing missing `{` bracket syntax, and updating [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json) with clean standard string concatenation.

### 3. 🌐 Storefront Catalog & Branch Sync
- **Catalog Count**: 18 Curated Products active on [`index.html`](https://adityasnalawade742-design.github.io/index.html).
- **Subdirectory Alignment**: All bridge pages are synced in root (`bridge_{ASIN}.html`) AND subfolder (`bridge_pages/bridge_{ASIN}.html`).
- **Clean Cleanup**: Purged test products (`B0CT274BX5`, `B0CGZS5129`, `B0BWJDGJMM`) from registry, workspace, and git branches.

---

## 📊 Core Architecture Index

- [`index.html`](file:///G:/CLI/pinterest-auto-affiliate/index.html): Main storefront homepage with 18 product card wrappers & JS filter chips.
- [`product_price_registry.json`](file:///G:/CLI/pinterest-auto-affiliate/product_price_registry.json): Master product database & regional price matrix.
- [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json): Primary 8-node n8n workflow file.
- [`web_console_server.py`](file:///G:/CLI/pinterest-auto-affiliate/web_console_server.py): Flask Web Console & n8n Bridge Server (Port 5000).
- [`run_daily_health_check.py`](file:///G:/CLI/pinterest-auto-affiliate/run_daily_health_check.py): Zero-drift automated self-healing script.
- [`PINTEREST_RE_APPLICATION_GUIDE.md`](file:///G:/CLI/pinterest-auto-affiliate/PINTEREST_RE_APPLICATION_GUIDE.md): Master 10-step video recording guide & Pinterest submission template.
