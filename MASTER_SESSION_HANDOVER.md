# 🚀 Master Session Handover & System State Summary

---

## 🚨 MANDATORY NEXT SESSION STARTUP DIRECTIVE
> **High Priority Directive**: When this conversation or a new AGY session is opened, your VERY FIRST ACTION must be to run:
> ```bash
> python run_daily_health_check.py
> ```
> This executes an automated zero-drift self-healing check across all 9 storefront products, verified prices, legal footers, and GitHub Pages live deployments!

---

## 1. Executive Summary & Session Log (August 2, 2026)

This session focused on **debugging, optimizing, and completely rebuilding the Web Console and n8n Workflow integration** to create a seamless 3-step product curation and auto-posting machine.

### Key Accomplishments & Debug Fixes This Session:
1. **Complete Rebuild of Web Console (`admin_console.html`)**:
   - Streamlined into **2 primary tabs**:
     - **📌 Send to n8n Workflow**: Full 3-step curation pipeline (Step 1: Discover → Step 2: Review/Override Images → Step 3: Send to n8n).
     - **🏠 Homepage Manager**: Live storefront product cards + 21-Region Matrix Grid.
   - Removed legacy single-ASIN panels and duplicate header elements.
   - Products in Step 1 now start **unselected**, giving complete manual control over product selection.

2. **Full Product Discovery Engine Overhaul (`modules/amazon_finder.py`)**:
   - **SerpAPI Key Failover**: Added automatic key failover across `SERPAPI_KEYS` array (Keys #1, #2, #3). When Key #1 ran out of credits, the system automatically switched to active Keys #2 and #3 without failing.
   - **Real High-Res Amazon Hero Photos**: Resolved empty/transparent 43-byte CDN thumbnail issues by fetching real Amazon listing hero photos (`https://m.media-amazon.com/images/I/..._SL1500_.jpg`) directly via `get_product_details_and_photos(asin)`.
   - **Full 10-Product Batching**: Guaranteed 10 candidate Amazon products returned for every search query without premature fallback.

3. **Backend API Endpoints (`web_console_server.py`)**:
   - `POST /api/prepare_n8n_batch`: Packages user-confirmed product and image choices, downloads photos to `raw_images/`, generates unique SEO copy per item, and returns a clean payload list for n8n.
   - `POST /api/create_bridge_page`: Called by n8n per product to build `bridge_{ASIN}.html`, render `focus_product_{ASIN}_hook.jpg` via Playwright, and auto-push to GitHub Pages via Git in the background.

4. **Redesigned 6-Node n8n Workflow (`n8n_pinterest_affiliate_workflow.json`)**:
   - Node 1: Webhook receiver (`pinterest-batch`)
   - Node 1b: Immediate ACK response (prevents timeout)
   - Node 2: Split items (loops products 1-by-1)
   - Node 3: HTTP POST → `http://localhost:5000/api/create_bridge_page`
   - Node 4: Merge SEO copy, bridge URL, and hook image URL
   - Node 5: POST → Pinterest API v5 (`POST /v5/pins`)
   - Node 6: Log result

5. **Restored Original Storefront Portfolio**:
   - Restored `B0DZD1X83N` (Minimalist Wood Lamp) and `B0GYDXHF4G` (Flame Aroma Diffuser) to the live homepage.
   - 100% of the 9 portfolio products are active and verified.

---

## 2. Live Website & Legal URLs

- **Main Storefront**: [https://adityasnalawade742-design.github.io/index.html](https://adityasnalawade742-design.github.io/index.html)
- **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)
- **Terms of Service**: [https://adityasnalawade742-design.github.io/terms-of-service.html](https://adityasnalawade742-design.github.io/terms-of-service.html)
- **Sitemap XML**: [https://adityasnalawade742-design.github.io/sitemap.xml](https://adityasnalawade742-design.github.io/sitemap.xml)

---

## 3. Pinterest Developer Portal Credentials & Configuration

When connecting or configuring Pinterest API v5 on [developers.pinterest.com/apps/](https://developers.pinterest.com/apps/):

- **App Name**: `Cozy Room Decor Publisher Pro`
- **Company Name**: `Cozy Room Finds`
- **App ID**: `1596368`
- **Company Website**: `https://adityasnalawade742-design.github.io/index.html`
- **Privacy Policy**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
- **App Purpose**: `Personal API access (single, personal use)`
- **Pinterest Account**: `@adityasnalawade0703`
- **Target Board ID**: `1092545259543920271` *(Cozy Room & Desk Decor)*
- **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`

---

## 4. How to Operate the Web Console & n8n Pipeline

### Step-by-Step Instructions:

1. **Launch Local Web Console**:
   ```powershell
   python -u web_console_server.py
   ```
2. **Open Web Console**: Go to `http://localhost:5000` in browser (or `http://localhost:5000/console`).
3. **Run 3-Step n8n Workflow**:
   - **Step 1 (Select)**: Search Amazon or pick a category. Click product cards to select 1–15 items.
   - **Step 2 (Review Photos)**: Inspect all listing photos. AI auto-picks the best photo (gold highlight). Click any photo to override the selection if desired.
   - **Step 3 (Send to n8n)**: Click **📌 Send to n8n Workflow**. System packages choices and fires payload to n8n webhook (`http://localhost:5678/webhook/pinterest-batch`).
4. **n8n Automation**:
   - Import `n8n_pinterest_affiliate_workflow.json` into n8n.
   - Set environment variables `PINTEREST_ACCESS_TOKEN` and `PINTEREST_BOARD_ID`.
   - Toggle workflow to **Active**.

---

## 5. Master Portfolio Products Matrix (9 Active Items)

| # | ASIN | Product Title | Price | Landing Page |
| :-: | :--- | :--- | :--- | :--- |
| 1 | `B0DZD1X83N` | Minimalist Wood Base Bedside Table Lamp | $20.00 | [bridge_B0DZD1X83N.html](./bridge_B0DZD1X83N.html) |
| 2 | `B0GYDXHF4G` | Flame Aroma Essential Oil Diffuser | $35.00 | [bridge_B0GYDXHF4G.html](./bridge_B0GYDXHF4G.html) |
| 3 | `B0FXLYXM32` | White Wavy Wall Vanity Mirror | $76.49 | [bridge_B0FXLYXM32.html](./bridge_B0FXLYXM32.html) |
| 4 | `B0C2YLN3H4` | White Ceramic Donut Vase Set of 2 | $28.99 | [bridge_B0C2YLN3H4.html](./bridge_B0C2YLN3H4.html) |
| 5 | `B07HP22QTZ` | Crystal Prism Window Suncatcher | $12.99 | [bridge_B07HP22QTZ.html](./bridge_B07HP22QTZ.html) |
| 6 | `B0BZXNSW5K` | Touch Control Dimmable Bedside Lamp | $19.99 | [bridge_B0BZXNSW5K.html](./bridge_B0BZXNSW5K.html) |
| 7 | `B0DXKGL1T2` | Lily of the Valley Flower Desk Lamp | $38.57 | [bridge_B0DXKGL1T2.html](./bridge_B0DXKGL1T2.html) |
| 8 | `B0D1FRDFFX` | Handmade Glass Mushroom Ambient Lamp | $35.98 | [bridge_B0D1FRDFFX.html](./bridge_B0D1FRDFFX.html) |
| 9 | `B0D8P8CSYP` | Cute Bird Touch Control Nightstand Lamp | $18.99 | [bridge_B0D8P8CSYP.html](./bridge_B0D8P8CSYP.html) |

---

## 6. Standard CLI Operations & Scripts

```bash
# Run daily zero-drift health check & self-heal
python run_daily_health_check.py

# Rebuild all 9 landing pages with universal matrix & push live
python rebuild_EVERY_single_bridge.py

# Launch local Web Console server (Port 5000)
python -u web_console_server.py

# Delete a product campaign completely by ASIN
python delete_product.py <ASIN>
```

---

## 7. Current Repository & Git State

- **Branch**: `main` (Up to date with `origin/main`)
- **Latest Commits**:
  - `af081dd` — refactor: complete clean rebuild of Web Console (admin_console.html) with 2 streamlined tabs
  - `245d641` — fix: fetch real Amazon listing hero photos for all discovered products
  - `1ff582f` — fix: automatic SerpAPI key failover + 10 live Amazon products with images per search
  - `aea422c` — fix: generate direct Amazon CDN high-res product image URLs for all search candidates
  - `31167fe` — Revert "Delete product campaign B0DZD1X83N"
  - `c1165f1` — Revert "Delete product campaign B0GYDXHF4G"
- **GitHub Pages Live Status**: 100% Active & Green.
- **Working Tree**: Clean.
