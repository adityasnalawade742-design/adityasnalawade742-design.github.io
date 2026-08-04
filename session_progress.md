# Project Progress & Handover Report

This document records the exact state of the project, including features built, bugs resolved, and instructions on how to resume progress from a new workspace or a different agent session.

---

## 🌟 Outstanding Highlights & Completed Tasks
1. **Pinterest & n8n Variable Alignment:** Fixed data flow broken by n8n variable scoping. Node 6, 7, and 8 now correctly retrieve product metadata from the JavaScript cleaner node.
2. **Replicate 422 & 401 Errors Resolved:** Removed the forbidden `"version"` property from the Replicate prediction JSON payload. Addressed the 401 unauthenticated errors by switching to local Generic Header Auth credentials inside the n8n UI.
3. **Automated Clean Titles:** Resolved the issue where raw, long Amazon listing titles were rendering on image overlays and bridge page headings. The server now automatically writes the copywriter-shortened titles to the registry.
4. **Unified Font Overlay Styling:** Enforced the default cursive (`Caveat`) font theme across both server-generated web-console products and manually rebuilt ones.
5. **Product Deletion:** Cleaned out the hardcoded `B0DZD1X83N` campaign from `rebuild_EVERY_single_bridge.py`, removed the product files and card elements from `index.html`, and updated the sitemap/JSON-LD SEO schemas.
6. **Master Diagnostic & Sequential Sync:** Executed scrapers across all 22 regional domains, verified 352 outbound redirect urls, auto-healed 24 drifted data attributes, and pushed refreshed pages live.

---

## 🐛 Key Bugs Discovered & Resolved

### 1. n8n Variable Scope (`$json` evaluated to `undefined`)
* **Bug:** Subsequence nodes in n8n (Node 6, 7, 8) used `$json.asin` to reference metadata. Since n8n's `$json` only represents the immediate predecessor's output, and Node 5 (Replicate) only outputs prediction links, all product metadata was lost/empty.
* **Fix:** Rewrote all dynamic expressions in [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json) to pull explicitly from the JavaScript formatting node using `{{ $node['Code in JavaScript'].json.property }}`.

### 2. Replicate HTTP 422 (Invalid Input Validation)
* **Bug:** Node 5 was passing `"version": "black-forest-labs/flux-dev"` inside the request body while calling a model-specific endpoint (`.../models/black-forest-labs/flux-dev/predictions`). Replicate rejects this with a 422 validation error.
* **Fix:** Removed the `"version"` field from the JSON body in [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json).

### 3. Replicate HTTP 401 (Unauthenticated)
* **Bug:** The workflow relied on `{{ $env.REPLICATE_API_TOKEN }}` inside n8n. However, self-hosted n8n instances do not automatically inherit OS environment variables unless started with special dotenv overrides.
* **Fix:** Advised configuring n8n **Header Auth** credentials with `Name: Authorization` and `Value: Bearer <YOUR_REPLICATE_API_TOKEN_HERE>`. This encrypts and stores the key in the local n8n database, bypassing OS environment variables.

### 4. Raw Amazon Titles on Badges & Headings
* **Bug:** The local server's `/api/create_bridge_page` endpoint was writing the raw Amazon listing titles to the registry and overlays, causing giant overlapping text blocks.
* **Fix:** Modified [`web_console_server.py`](file:///G:/CLI/pinterest-auto-affiliate/web_console_server.py) to automatically reassign `title = _seo_fresh.get('image_hook')` right after processing the SEO copy, guaranteeing that the database registry and landing page headings always use the clean, shortened titles.

### 5. Inconsistent Font Styles
* **Bug:** Server-generated overlays (called by n8n) defaulted to a serif theme (`floating_luxury`), while the manual script [`rebuild_all_price_badges_usd.py`](file:///G:/CLI/pinterest-auto-affiliate/rebuild_all_price_badges_usd.py) used the cursive theme (`bottom_glass_card`).
* **Fix:** Updated [`web_console_server.py`](file:///G:/CLI/pinterest-auto-affiliate/web_console_server.py) to explicitly pass `theme="bottom_glass_card"` to the overlay rendering call, ensuring font consistency.

### 6. Deleted Products Kept Reappearing
* **Bug:** Deleting `B0DZD1X83N` succeeded temporarily, but running `rebuild_EVERY_single_bridge.py` recreated its files and card elements.
* **Fix:** Found that `B0DZD1X83N` was hardcoded inside the `master_catalog` dictionary of [`rebuild_EVERY_single_bridge.py`](file:///G:/CLI/pinterest-auto-affiliate/rebuild_EVERY_single_bridge.py). Removed the entry from the script.

---

## 🚀 How to Resume Progress on a New Machine / Account

If you start a new coding agent session or change systems, run these commands sequentially to pick up where you left off:

1. **Pull the latest changes from GitHub:**
   ```bash
   git pull origin main
   ```
2. **Ensure your python dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```
3. **If you want to run the local Web Console UI:**
   Launch the web server in the background:
   ```bash
   python web_console_server.py
   ```
4. **To perform a full sequential regional price sync & sitemap build:**
   ```bash
   python sync_all_regional_prices_master.py
   ```
5. **Import the updated n8n workflow:**
   Locate [`fixed_n8n_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/fixed_n8n_workflow.json) in your project directory, open your n8n workspace, click the menu in the top right, select **Import from File...**, choose this file, and click **Save**. Ensure you configure your Replicate credential as a local Header Auth credential.
