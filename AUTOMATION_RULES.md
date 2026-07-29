# 🛡️ Pinterest Affiliate Automation Pipeline - Core System Rules & Guidelines

## 1. 📷 4-Layer Photo Selection Engine (`modules/amazon_extractor.py`)

Every Amazon listing photo suite (5–9 photos) MUST undergo the following 4-layer inspection pipeline:

1. **Text & Infographic Scanner**:
   - `top_contrast > 0.035` or `full_contrast > 0.035`
   - Discards seller text callouts, dimension arrows, and badges.
   - Allows natural organic flora (pampas grass fronds, pine needles) to pass 100% cleanly.

2. **Grid Collage Scanner**:
   - `v_seam > 0.20` and `h_seam > 0.20`
   - Discards 2-grid, 3-grid, and 4-grid split collages.
   - Guarantees 1 single 1-scene full-bleed room photo.

3. **Human / Model Scanner**:
   - `skin_ratio > 0.10`
   - Discards human models, hands holding products, or people sitting in the room.
   - Guarantees pure product + room decor focus.

4. **Cozy Vibe Aesthetics Scorer**:
   - Evaluates warm amber/gold color temperature ($R > G > B$) vs cold grey studio lighting.
   - Ranks all remaining 100% clean 1-scene photos and selects the **#1 highest cozy score (1.0 to 10.0)**.

---

## 2. 🎨 Dynamic Img2Img Prompt Strength Engine (`n8n_local_bridge.py`)

- **Prompt 1 (Existing Lifestyle Room Photos - Capped at MAX 0.55)**:
  - **`prompt_strength = 0.28`**: Automatically assigned to **Item Sets, Multi-Packs, or Intricate Items** (e.g. 2-piece vase sets, crystal suncatchers) to guarantee **100% exact item count and zero hallucinated props**.
  - **`prompt_strength = 0.48 – 0.55`**: Automatically assigned to **Single Solid Items** (e.g. 1 wall mirror, 1 bedside lamp) for maximum room enhancement while **STRICTLY CAPPED AT MAX 0.55**.

- **Prompt 2 (Plain White Studio Cutouts)**:
  - **`prompt_strength = 0.75 – 0.80`**: Reserved exclusively for white studio cutouts with zero background to synthesize a brand-new 3:4 room background from scratch while locking physical product shape via the 6-photo Multi-Angle Reference Sheet.

---

## 3. 🚀 Cache-Busting Guidelines

- Always append version/timestamp query parameters (`?v=exact_v2`) or generate unique filenames (`focus_product_{asin}_exact2vases_hook.jpg`) when updating media files on GitHub Pages to bypass aggressive browser image caching.

---

## 4. 📌 Pinterest API v5 Integration

- **App ID**: `1594896` (Trial Access Active)
- **Authenticated Account**: `@adityasnalawade0703` (Business Account)
- **Target Board ID**: `1092545259543920271` (*Cozy Room & Desk Decor*)
- **Required Scopes**: `boards:read`, `boards:write`, `pins:read`, `pins:write`
- **Privacy Policy**: [https://adityasnalawade742-design.github.io/privacy-policy.html](https://adityasnalawade742-design.github.io/privacy-policy.html)

---

## 5. 🏷️ Strict Price Synchronization Rule

- **100% Exact Amazon Price Sync**: Whenever creating or processing any new product, the price text rendered inside:
  1. The graphic price tag (`focus_product_{asin}_hook.jpg`),
  2. The mobile bridge landing page (`bridge_{asin}.html`),
  3. The homepage gallery card (`index.html`),
  MUST automatically match the exact live price extracted directly from the Amazon product listing page.

- **Daily Automated Price Synchronization Engine (`daily_price_updater.py`)**:
  - **Raw Image Archiving**: Clean, text-free AI generated room photos are preserved in `raw_images/raw_{asin}.jpg`.
  - **Product Registry (`product_price_registry.json`)**: Tracks ASIN, Amazon URL, current price, headline, raw image path, hook image path, and bridge landing page URL.
  - **Automated Price Check**: Runs daily scraping live Amazon prices. If a price change is detected:
    1. Re-renders the Playwright graphic overlay onto `raw_images/raw_{asin}.jpg` with the new price tag.
    2. Updates `<div class="price">` in `bridge_{asin}.html`.
    3. Updates `<div class="card-price-tag">` in `index.html`.
    4. Automatically commits and pushes live updates to GitHub Pages with cache-busting query params (`?v={timestamp}`).

---

## 6. 🔒 Cloud Hosting Security & Admin Authentication Requirement

- **Secure Remote Deletion**: When deploying to cloud hosting (AWS EC2 / Lambda / n8n), all remote administrative endpoints (product deletion, manual overrides) MUST be protected by a private `ADMIN_SECRET_KEY` saved in `.env` to prevent unauthorized public execution.



