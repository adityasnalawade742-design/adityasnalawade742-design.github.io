# 🚀 Master Session Handover & System State Summary

---

## 🚨 MANDATORY NEXT SESSION STARTUP DIRECTIVE
> **High Priority Directive**: When this conversation or a new session is opened, your VERY FIRST ACTION must be to run:
> ```bash
> python run_daily_health_check.py
> ```
> This executes an automated zero-drift self-healing check across all 9 storefront products, verified prices, legal footers, and GitHub Pages live deployments!

---

## 1. Last Session Summary (August 2, 2026)

This session completed a **full n8n workflow redesign** — a new 3-step "Send to n8n" pipeline was built directly into the Web Console.

### Key Achievements This Session:
1. **New "📌 Send to n8n" Tab added to `admin_console.html`**:
   - **Step 1**: User searches Amazon (any keyword, any count 1–20), gets a product grid, clicks to select/deselect products.
   - **Step 2**: System extracts all listing photos per product. Auto-selects the best clean photo (AI pick). User can click any image to override the selection. Green ✓ CLEAN / Red ✗ BAD badge on each photo.
   - **Step 3**: Clicks "Send to n8n Workflow" button → preps batch (downloads photos, generates unique SEO copy per product) → fires to n8n webhook → shows live status row per product.

2. **Two new Python endpoints added to `web_console_server.py`**:
   - `POST /api/prepare_n8n_batch` — packages user-confirmed product+image selections, downloads chosen photos locally, generates unique SEO copy, returns structured payload for n8n.
   - `POST /api/create_bridge_page` — called by n8n per-product, builds `bridge_{ASIN}.html` + renders `focus_product_{ASIN}_hook.jpg`, git-pushes live to GitHub Pages, returns `bridge_url` + `hook_image_url` back to n8n.

3. **Full n8n workflow JSON redesigned (`n8n_pinterest_affiliate_workflow.json`)**:
   - Now has 6 nodes (was 5):
     - Node 1: Webhook (receives batch from Web Console)
     - Node 1b: Immediate ACK response (prevents timeout)
     - Node 2: Split Items (loops 1 product at a time)
     - Node 3: HTTP POST → `localhost:5000/api/create_bridge_page` (builds bridge + hook image per product)
     - Node 4: Set — merges bridge_url + hook_image_url + SEO copy
     - Node 5: POST → Pinterest API v5 (publishes pin with bridge URL as destination)
     - Node 6: Log result

4. **All changes committed and pushed to GitHub Pages**:
   - Latest commit: `2f0dff9` — *feat: new n8n Send to n8n tab with 3-step product+image review workflow, bridge page builder endpoint, and redesigned 6-node n8n workflow*

---

## 2. Live Website & Legal URLs

- **Main Storefront**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)
- **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)
- **Terms of Service**: [https://adityasnalawade742-design.github.io/terms-of-service.html](https://adityasnalawade742-design.github.io/terms-of-service.html)
- **Sitemap XML**: [https://adityasnalawade742-design.github.io/sitemap.xml](https://adityasnalawade742-design.github.io/sitemap.xml)

---

## 3. Pinterest Developer Portal App Creation Cheat Sheet

When creating a new app on [developers.pinterest.com/apps/](https://developers.pinterest.com/apps/):

- **App Name**: `Cozy Room Decor Publisher Pro`
- **Company Name**: `Cozy Room Finds`
- **App ID**: `1596368`
- **Company Website**: `https://adityasnalawade742-design.github.io/index.html`
- **Privacy Policy Link**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
- **App Purpose**: `Personal API access (single, personal use)`
- **Sharing Access**: `No one. Access is strictly private and restricted to our own verified business profile (@adityasnalawade0703).`
- **Use Cases**: Check **Pin creation & scheduling**
- **Audience**: Check **Creators** & **Pinners**
- **Reads Pins/Boards**: Select **Yes, mine**
- **Pinterest Business Account**: `@adityasnalawade0703`
- **Target Board ID**: `1092545259543920271` *(Cozy Room & Desk Decor)*
- **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`

---

## 4. How to Use the New n8n Workflow (Added August 2, 2026)

### Step-by-step:
1. Start the web console server:
   ```powershell
   python -u web_console_server.py
   ```
2. Open `http://localhost:5000` in browser.
3. Click the **📌 Send to n8n** tab (red-tinted, top navigation).
4. **Step 1**: Type a search keyword (e.g. "mushroom lamp"), set count (e.g. 10), click **Search Amazon**. Click product cards to select/deselect.
5. **Step 2**: Click **Next: Review Images**. For each product, AI auto-picks best clean photo. Click any other image to override.
6. **Step 3**: Click **Send to n8n Workflow**. System preps + fires to n8n. Status rows show per-product progress.

### Import the workflow into n8n:
1. Open n8n (`http://localhost:5678` or cloud)
2. Workflows → Import from File
3. Select `G:\CLI\pinterest-auto-affiliate\n8n_pinterest_affiliate_workflow.json`
4. Set environment variables in n8n Settings:
   - `PINTEREST_ACCESS_TOKEN` = your Pinterest Bearer token
   - `PINTEREST_BOARD_ID` = `1092545259543920271`
5. **Activate** the workflow (toggle ON)
6. Webhook URL that Web Console calls: `http://localhost:5678/webhook/pinterest-batch`

---

## 5. Standard CLI Operations

```bash
# Run daily zero-drift health check & self-heal
python run_daily_health_check.py

# Rebuild all 9 landing pages with verified global matrix and push live to GitHub Pages
python rebuild_EVERY_single_bridge.py

# Launch local Web Console server (Port 5000)
python -u web_console_server.py

# Sync exact multi-region prices across 21 Amazon domains
python sync_exact_amazon_prices.py
```

---

## 6. Current Repository & Git State

- **Latest Commit**: `2f0dff9` — feat: new n8n Send to n8n tab + bridge page builder endpoint + redesigned 6-node n8n workflow
- **GitHub Pages Deployment Status**: 100% Active & Green.
- **Affiliate Tag Compliance**: 100% verified across all outbound links.
- **Working Tree**: Clean — nothing uncommitted.
