# 🏆 MASTER SESSION HANDOVER & STATE RECOVERY GUIDE

> **PROJECT**: Pinterest Auto Affiliate & Multi-Region Storefront Machine
> **DATE**: August 5, 2026
> **STATUS**: 100% Operational | Zero Drift | 4-Board Category Mapped | n8n Hardened

---

## 📌 Executive Summary & Account Resume Guide

If you start a **new agent session**, switch AGY accounts, or move to a different workspace, this single file contains **everything required** to pick up immediately without losing state or context.

---

## 🚀 Quick Restart Commands (Copy & Paste)

```bash
# 1. Pull latest code from GitHub Pages main branch
git pull origin main

# 2. Run automated zero-drift self-healing health check
python run_daily_health_check.py

# 3. Launch local Web Console & n8n Bridge Server (Port 5000)
python web_console_server.py

# 4. Verify category board alignment on index.html
python scratch/check_homepage_categories.py
```

---

## 🛠️ Summary of Completed Features & Resolved Issues

### 1. 🪴 Pinterest 4-Category Board System Mapped & Live
All 16 products are published across their respective category boards on Pinterest account **`Nesteraliving`**:
* 🪴 **Boho Vases & Desk Decor** (`1092545259543956197`) — 4 Products
* 💡 **Aesthetic Lighting & Lamps** (`1092545259543956233`) — 7 Products
* 🪞 **Vanity Mirrors & Wall Decor** (`1092545259543956238`) — 2 Products
* 🛋️ **Cozy Room & Home Decor** (`1092545259543956242`) — 3 Products
* **Mapping Config**: Stored in `pinterest_board_mapping.json` & `modules/pinterest_publisher.py`.

### 2. ⚡ Product Selection Upgrades 1–4 Implemented
* **Auto Category Classifier** (`modules/amazon_extractor.py` -> `classify_product_category`): Automatically maps any new product to one of the 4 Pinterest categories.
* **Multi-Region Pre-Flight Check** (`modules/amazon_extractor.py` -> `preflight_regional_check`): Fast HTTP check across US, UK, DE, IN prior to selection.
* **Impulse Price Guardrails** (`modules/amazon_finder.py`): Enforces `$15.00 – $49.99` price sweet spot & `4.3★+` rating threshold.
* **2026 Expanded Pinterest Keywords**: Loaded 12 high-intent 2026 viral decor queries.

### 3. 🌐 Storefront Category Alignment & Vanity Mirrors Fix
* **Category Auto-Healing**: Updated `run_daily_health_check.py` to auto-heal `data-category` attributes on `index.html`.
* **Vanity Mirrors Chip Fix**: Resolved singular/plural mismatch (`mirrors` vs `mirror`) on `index.html`. Enhanced JS `filterProducts()` matcher to handle singular/plural variations (`mirror`/`mirrors`, `vase`/`vases`).
* **Category Audit**: 100% PASS across all 5 tabs (`all`: 16, `lighting`: 7, `decor`: 3, `vases`: 4, `mirror`: 2).

### 4. ⚙️ n8n Workflow Hardening & Fixes
* **Recommended Workflow File**: **`fixed_n8n_workflow.json`**.
* **Title Length Sanitizer**: Enforced 35-character cap on overlay titles in `modules/html_overlay_engine.py`, `modules/seo_copywriter.py`, and `web_console_server.py` to eliminate giant text overlays.
* **Env Access Error Fix**: Removed `$env` references in Node 7 to bypass n8n's `N8N_BLOCK_ENV_ACCESS_IN_NODE` error.
* **Header Auth Credentials**: Node 5 (Replicate) & Node 7 (Pinterest) configured to use n8n's `genericCredentialType` (`httpHeaderAuth`).
* **Dynamic Board Routing**: Node 7 uses `board_id: $json.board_id` returned by `/api/create_bridge_page`.
* **Transparent Error Reporting**: Removed `onError: continueRegularOutput` on Node 7 so errors are reported clearly.

### 5. 🛠️ Product Page Repair (`bridge_B0D5YNHXQ7.html`)
* Rebuilt `bridge_B0D5YNHXQ7.html` with clean title (**`Glivpny Vintage Ceramic Mushroom Lamp`**), category `lighting`, clean 35-char hook image overlay (`focus_product_B0D5YNHXQ7_hook.jpg`), and verified multi-region India routing (`?country=IN`).

---

## 🔑 Key Credential Setup in n8n UI

When importing `fixed_n8n_workflow.json` into n8n (`http://localhost:5678`):
1. **Node 5 (Replicate API)**:
   * **Authentication**: Generic Credential Type -> Header Auth
   * **Name**: `Authorization`
   * **Value**: `Bearer r8_YOUR_REPLICATE_TOKEN`
2. **Node 7 (Pinterest API)**:
   * **Authentication**: Generic Credential Type -> Header Auth
   * **Name**: `Authorization`
   * **Value**: `Bearer pina_YOUR_TRIAL_TOKEN`
   * **URL**: `https://api-sandbox.pinterest.com/v5/pins`

---

## 📊 File Architecture Index

* `index.html`: Storefront homepage with 16 card wrappers & JS filter chips
* `product_price_registry.json`: Master product database & regional price matrix
* `fixed_n8n_workflow.json`: Primary 8-node n8n workflow file
* `web_console_server.py`: Local Web Console & n8n Bridge Server (Port 5000)
* `run_daily_health_check.py`: Automated zero-drift self-healing script
* `pinterest_board_mapping.json`: Category -> Board ID mapping matrix
* `modules/amazon_extractor.py`: Category classifier & pre-flight checker
* `modules/amazon_finder.py`: Impulse price guardrails & 2026 keyword finder
* `modules/html_overlay_engine.py`: Playwright 1200x1600 image overlay renderer
* `modules/pinterest_publisher.py`: Direct Pinterest API publisher module
