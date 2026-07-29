# 🛡️ Pinterest Auto-Affiliate Automation Pipeline - Comprehensive Master Architecture & System Documentation

> **IMPORTANT**: This document is the authoritative, self-contained Master Knowledge Base for the entire Pinterest Auto-Affiliate Automation Pipeline. Any new AI agent, system instance, or developer account reading this document will understand 100% of the project history, core architecture, decision rationale, 4-layer selection filters, AI prompt strategies, security rules, and active product campaigns.

---

## 📌 1. Executive Summary & Core Infrastructure Settings

- **Storefront & Showcase Domain**: [https://adityasnalawade742-design.github.io](https://adityasnalawade742-design.github.io)
- **GitHub Repository**: `adityasnalawade742-design/adityasnalawade742-design.github.io` (`main` branch)
- **Primary Amazon Associates Tag**: `smartdeal0358-21` (Configured across US `.com`, UK `.co.uk`, and India `.in`)
- **Pinterest Integration**: OAuth 2.0 API Sandbox (`pina_...`) & Production API (`https://api.pinterest.com/v5/pins`). Target Board: `1092545259543920271` (*Cozy Room & Desk Decor*)
- **Primary AI Image Generation Engine**: Replicate FLUX-Dev (`black-forest-labs/flux-dev`) with `aspect_ratio="3:4"`, `num_inference_steps=32`, `guidance_scale=3.5`, `seed=591928`, `output_format="jpg"`.
- **Vision Prompt Engine**: Google GenAI SDK (`gemini-2.0-flash`) in `modules/vision_prompt.py`.
- **Graphic Overlay Renderer**: Headless Playwright Chromium (`modules/html_overlay_engine.py`) rendering 1200x1600 3:4 vertical graphics with glassmorphism cards, price tags, top badges, and 4 feature highlights.

---

## 🔄 2. Complete 6-Step End-to-End Campaign Processing Workflow

Every product campaign follows a strict 6-step deterministic pipeline:

```
[Amazon Listing URL] 
       │
       ▼
1. Amazon Suite Extraction (`modules/amazon_extractor.py`)
       │
       ▼
2. 4-Layer Photo Selection & Quality Engine (`select_clean_photo_or_skip`)
       │ ──► [Filter out Seller Text, Collages, Human Hands/Models]
       │ ──► [Score remaining clean photos by Cozy Vibe Aesthetics (1.0 to 10.0)]
       │ ──► [Select Winner #1 Photo]
       ▼
3. Master Dual-Prompt Assignment (`modules/vision_prompt.py`)
       │ ──► [Prompt 1: Lifestyle Room Enhancement (is_white_background=False)]
       │ ──► [Prompt 2: Background Synthesis from Scratch (is_white_background=True)]
       ▼
4. Replicate FLUX-Dev Img2Img Generation (`modules/image_generator.py`)
       │ ──► [Attach Winner Photo as input payload & apply prompt_strength]
       │ ──► [Save 8K clean AI room image to raw_images/raw_{asin}.jpg]
       ▼
5. Playwright Graphic Overlay Rendering (`modules/html_overlay_engine.py`)
       │ ──► [Stamp Price Tag, Top Badge, 4 Feature Cards & Blank Subtitle ("") per Rule 7]
       │ ──► [Save graphic to focus_product_{asin}_hook.jpg]
       ▼
6. Global Publishing & Geo-IP Router (`index.html` & `bridge_{asin}.html`)
       │ ──► [Deploy 160+ World Currency Converter on index.html]
       │ ──► [Deploy 3-Way Geo-IP Router (IN -> Amazon.in, UK/EU -> Amazon.co.uk, US/ROW -> Amazon.com)]
       ▼
[Git Commit & Live Deployment to GitHub Pages]
```

---

## 🔍 3. Meticulous Breakdown of Step 2: 4-Layer Photo Selection Engine

Located in `modules/amazon_extractor.py` (`select_clean_photo_or_skip`):

1. **Layer 1: Border Pixel Cutout Inspection (`is_lifestyle_photo`)**:
   - Inspects the outer 15-pixel border channels of the image using Pillow (`PIL.Image`).
   - If border pixels are pure white (`#FFFFFF`), flags image as a **White Studio Cutout**.
   - If border pixels contain room textures, walls, or furniture, flags image as a **Lifestyle Room Photo**.

2. **Layer 2: Seller Text & Infographic Scanner (`has_text_annotation`)**:
   - Evaluates high-frequency edge density contrast (`top_contrast > 0.035` or `full_contrast > 0.035`).
   - Automatically discards seller marketing text (e.g. *"50% OFF"*, dimensions, callout arrows, badges).

3. **Layer 3: Human / Model Scanner (`has_human_presence`)**:
   - Evaluates RGB skin tone color spectrum ratio (`r > 140 and g > 90 and b > 60 and (r > g + 15)`).
   - **Threshold**: **`skin_ratio > 0.03` (3%)**.
   - Discards photos showing human faces, arms, hands holding products, or models sitting in the room so the focus remains 100% on the product decor item.

4. **Layer 4: Grid Collage Scanner (`is_grid_collage`)**:
   - Resizes image to 200x200 edge map and evaluates central vertical/horizontal seam line density at $x=100$ and $y=100$ (`edge_pixel > 60`).
   - **Threshold**: **`v_seam > 0.15` and `h_seam > 0.15`**.
   - Discards 2-grid, 3-grid, and 4-grid split collages (e.g. `71pk86fAeHL._AC_SL1500_.jpg`), guaranteeing a single 1-scene full-bleed room photo.

5. **Layer 5: Cozy Vibe Aesthetics Scorer (`calculate_cozy_vibe_score`)**:
   - Evaluates warm amber/gold color temperature ratios ($R > G > B$), detail contrast, and luminance.
   - Ranks all remaining clean 1-scene photos from **1.0 to 10.0** and selects the **#1 Winner Photo**.

---

## 🎨 4. Master Prompt Strength Rules Engine

Located in `AUTOMATION_RULES.md` and `modules/image_generator.py`:

- **Option A: For Products WITH Existing Lifestyle Room Photos (`is_white_background=False`)**:
  - **`prompt_strength = 0.28 – 0.35`**: Assigned to **Item Sets, Multi-Packs, or Intricate Items** (e.g. 2-piece donut vase set `B0C2YLN3H4`, crystal suncatchers) to guarantee **100% exact item count and zero hallucinated props**.
  - **`prompt_strength = 0.40 – 0.60`**: Assigned to **Single Solid Items** (e.g. 1 wall mirror `B0FXLYXM32`, 1 flame diffuser `B0GYDXHF4G`, 1 bedside lamp) for maximum room lighting enhancement while preserving physical product geometry.

- **Option B: For Plain White Studio Cutouts (`is_white_background=True`)**:
  - **`prompt_strength = 0.75 – 0.80`**: Reserved exclusively for white studio cutouts to synthesize a brand-new 3:4 photorealistic room background from scratch.

---

## 🛡️ 5. Master System Automation Rules

1. **Rule 1 (100% Home Decor Niche)**: Products must fall into room lighting, wall accents, nightstand decor, or cozy room transformation ($15 – $45 impulse price range).
2. **Rule 2 (No Kids / Adult Exclusion - `is_adult_aesthetic_product`)**: Automatically excludes items with keywords `kids`, `children`, `toy`, `drawing board for kids`.
3. **Rule 3 (No Plain Cutouts)**: Products MUST have authentic room lifestyle photos or undergo full 3:4 room background synthesis.
4. **Rule 4 (No Automatic Unapproved Execution)**: ALWAYS present product title, price, affiliate link, and selected winner photo to the user first, and wait for explicit user approval before running generation scripts.
5. **Rule 5 (100% Exact Amazon Price Sync)**: The price rendered in the graphic price tag (`focus_product_{asin}_hook.jpg`), landing page (`bridge_{asin}.html`), and homepage card (`index.html`) MUST 100% match the live Amazon price extracted directly from the product page.
6. **Rule 6 (Cloud Hosting Admin Security)**: Remote admin actions (deletions / manual triggers) on AWS or n8n cloud hosting MUST be secured behind an `ADMIN_SECRET_KEY` authentication layer saved in `.env`.
7. **Rule 7 (No Fluff Subtitles Policy)**: Subtitles in Playwright graphic overlays MUST be blank (`""`) by default. NEVER add generic marketing fluff taglines like `"ELEVATE YOUR VANITY SPACE"` or `"VINTAGE FLORAL GLOW"`.

---

## 🌐 6. Global Multi-Currency & Smart Geo-IP Location Router

- **Global Currency Engine (`index.html`)**:
  - Automatically detects visitor's country via IP API (`ipapi.co/json`) and formats prices in local currency (`₹ INR`, `£ GBP`, `€ EUR`, `CA$ CAD`, `A$ AUD`, `¥ JPY`, etc.).
  - Fetches live daily exchange rates from `https://open.er-api.com/v6/latest/USD`.
  - Top-bar dropdown allows manual currency switching across 160+ world currencies.
  - Card wrappers track `data-base-usd="{price}"` for instant dynamic conversion.

- **3-Way Smart Geo-IP Location Router (`bridge_*.html`)**:
  - **India (`IN`)** ➔ `Amazon.in` (`smartdeal0358-21`) with badge `⚡ Delivered via Amazon India`.
  - **UK & Europe (`GB`, `UK`, `NL`, `DE`, `FR`, `IT`, `ES`, etc.)** ➔ `Amazon.co.uk` (`smartdeal0358-21`) with badge `⚡ Delivered via Amazon UK & Europe`.
  - **US & Rest of World** ➔ `Amazon.com` (`smartdeal0358-21`) with badge `✈️ Ships Internationally via Amazon Global`.
  - **Testing Override Parameter**: Append `?geo=uk`, `?geo=in`, or `?geo=us` to any bridge URL to force regional routing without a VPN.

---

## 🛠️ 7. Product Deletion & Daily Maintenance Workflows

### Permanent Product Deletion (`delete_product.py`):
```powershell
python delete_product.py <ASIN>
```
*Actions Executed*:
1. Unlinks `bridge_{asin}.html` and `focus_product_{asin}_hook.jpg`.
2. Strips `<div class="card-wrapper" id="card-{asin}"...>` from `index.html`.
3. Removes ASIN entry from `product_price_registry.json` and `processed_asins.json`.
4. Runs `git add -A`, commits, and pushes live to GitHub Pages.

### Master Daily Price Synchronization (`daily_price_updater.py`):
```powershell
python daily_price_updater.py
```
*Actions Executed*:
1. Scrapes live Amazon prices for all active homepage ASINs.
2. If price changes, re-stamps Playwright text overlay directly onto `raw_images/raw_{asin}.jpg`.
3. Updates `bridge_{asin}.html` and `index.html` data attributes.
4. Auto-commits and pushes live to GitHub Pages.

---

## 📋 8. Active Homepage Product Campaigns Registry

| ASIN | Product Title | Price (USD) | Category | Raw Background Source | Subtitle Policy | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `B0GYDXHF4G` | Flame Aroma Essential Oil Diffuser | `$35.00` | Lighting/Decor | FLUX Img2Img (`strength=0.60`) | Blank (`""`) | Live |
| `B0FXLYXM32` | White Wavy Wall Vanity Mirror | `$76.49` | Mirror | FLUX Img2Img (`strength=0.40`) | Blank (`""`) | Live |
| `B0C2YLN3H4` | White Ceramic Donut Vase Set of 2 | `$14.99` | Decor | User FLUX Img2Img (`flux.jpg`) | Blank (`""`) | Live |
| `B07HP22QTZ` | Crystal Prism Window Suncatcher | `$9.99` | Decor | FLUX Img2Img (`strength=0.40`) | Blank (`""`) | Live |
| `B0BZXNSW5K` | Fenmzee Bedside Table Touch Lamp | `$19.99` | Lighting | FLUX Img2Img (`strength=0.40`) | Blank (`""`) | Live |
| `B0DXKGL1T2` | Lily of the Valley Flower Lamp | `$38.57` | Lighting | Custom Clean Lifestyle Photo | Blank (`""`) | Live (Exempt) |
| `B0D1FRDFFX` | Dawnwake Mushroom Touch Table Lamp | `$35.98` | Lighting | FLUX Img2Img (`strength=0.40`) | Blank (`""`) | Live |
| `B0D8P8CSYP` | Cute Bird Dimmable Touch Night Lamp | `$20.56` | Lighting | FLUX Img2Img (`strength=0.40`) | Blank (`""`) | Live |
| `B0DLN5S5K9` | WLHBF Vintage Flower Table Lamp | `$24.99` | Lighting | Custom Clean Lifestyle Photo | Blank (`""`) | Live (Exempt) |

---

## 🚀 9. Remaining Candidate Queue for Processing

1. **Crystal Prism Window Suncatcher** (`B07HP22QTZ`) — `$9.99`
2. **Fenmzee Bedside Table Touch Lamp** (`B0BZXNSW5K`) — `$19.99`
3. **Dawnwake Glass Mushroom Lamp** (`B0D1FRDFFX`) — `$35.98`
4. **Cute Bird Dimmable Touch Lamp** (`B0D8P8CSYP`) — `$20.56`
