# PROJECT STATE & CONTINUATION GUIDE: PINTEREST AUTO AFFILIATE MACHINE

## 🎯 Priority Goal for Next Session
- **Pinterest API Standard Access Approval**: Record and submit the 60-second video demo showing our clean 5-node n8n workflow execution (`Status 201 Created`) in the Pinterest Developer Portal to unlock production Standard Access (`https://api.pinterest.com/v5/pins`).

---

## 📌 Master Configuration Settings
- **Amazon Affiliate Store ID**: `smartdeal0358-21` *(100% configured across config.py, .env, and all bridge templates)*
- **GitHub Pages Domain**: `https://adityasnalawade742-design.github.io`
## 📌 Master Project State: Pinterest Auto-Affiliate Automation Pipeline

## 1. System Overview & Core Architecture
- **Primary Affiliate Tag**: `smartdeal0358-21` (Amazon Associates US, UK & India)
- **Pinterest Integration**: OAuth 2.0 API Sandbox (`pina_...`) & Production API (`https://api.pinterest.com/v5/pins`)
- **Master Price Synchronization Engine (`daily_price_updater.py`)**: Daily automated scraping of live Amazon prices. Automatically re-stamps prices onto clean raw room photos (`raw_images/raw_{asin}.jpg`), updates `bridge_{asin}.html` and `index.html`, and auto-pushes live to GitHub Pages.
- **Graphic Overlay Engine (`modules/html_overlay_engine.py`)**: Headless Playwright Chromium 1200x1600 3:4 vertical graphic renderer with glassmorphism cards, price tags, top badges, and 4 feature highlights.
- **Live Deployment**:
  - **URL**: [https://adityasnalawade742-design.github.io](https://adityasnalawade742-design.github.io)
  - **Repo**: `adityasnalawade742-design/adityasnalawade742-design.github.io` (`main` branch)

---

## 2. Homepage Design & Layout Architecture (`index.html`)
- **Dark Mode Glassmorphism**: Obsidian dark background (`#07060a`) with warm gold radial glows (`#ffb703` ➔ `#fb8500`).
- **Responsive Card Grid**: Card width capped at `290px` (`grid-template-columns: repeat(auto-fill, minmax(250px, 290px))` with `justify-content: center`).
- **Image Container**: `aspect-ratio: 3/4`, `object-fit: contain` on `#0b0a0f` container to ensure zero cropping/zoom on vertical Pinterest pin graphics.
- **Interactive Controls**: Real-time search bar + 5 category filter chips (`✨ All Finds`, `🕯️ Lamps & Lighting`, `🪞 Mirrors & Wall`, `🏺 Vases & Decor`, `✨ Desk Accessories`).
- **Public Security**: Delete buttons (`.delete-btn`) are hidden by default for public visitors.

---

## 3. Global Multi-Currency Engine (160+ World Currencies)
- **Auto Geolocation**: IP API (`ipapi.co/json`) detects visitor's country and maps it to official currency (e.g. India ➔ `INR ₹`, UK ➔ `GBP £`, Eurozone ➔ `EUR €`, Canada ➔ `CAD CA$`, Australia ➔ `AUD A$`, Japan ➔ `JPY ¥`).
- **Live Rates API**: Fetches daily exchange rates from `https://open.er-api.com/v6/latest/USD`.
- **Top Bar Selector**: Dropdown menu allows manual currency switching across 160+ world currencies.
- **Card Data Attribute**: Each card wrapper tracks `data-base-usd="{price}"` for instant dynamic conversion.

---

## 4. International Smart Geo-IP Location Router (`bridge_*.html`)
- **3-Way Routing Matrix**:
  - **India (`IN`)**: Routes button to `Amazon.in` with affiliate tag `smartdeal0358-21` (Badge: `⚡ Delivered via Amazon India`).
  - **UK & Europe (`GB`, `UK`, `NL`, `DE`, `FR`, `IT`, `ES`, etc.)**: Routes button to `Amazon.co.uk` (Badge: `⚡ Delivered via Amazon UK & Europe`).
  - **US & Rest of World**: Routes button to `Amazon.com` (Badge: `✈️ Ships Internationally via Amazon Global`).
- **Testing Override Parameter**: Append `?geo=uk`, `?geo=in`, or `?geo=us` to any landing page URL to force regional routing without a VPN.

---

## 5. Master Dual-Prompt AI Vision Strategy (`modules/vision_prompt.py`)
- **Prompt 1 (`is_white_background=False`)**: For listing photos with existing room backgrounds. Commercial room enhancement while preserving physical product geometry (Img2Img `prompt_strength = 0.40 max`).
- **Prompt 2 (`is_white_background=True`)**: For white studio cutouts with no background. Photorealistic 3:4 room background synthesis from scratch (Img2Img `prompt_strength = 0.78`) tailored to product category (Vases, Diffusers, Lamps, Mirrors, Suncatchers).
- **Photo Selection Engine (`select_clean_photo_or_skip`)**: 4-layer quality filter evaluating border pixels, edge density, luminance, and color richness (`Cozy Vibe Score`).

---

## 6. Permanent Product Deletion Workflow (`delete_product.py`)
To permanently remove any product campaign from local files, registries, and GitHub Pages:
```powershell
python delete_product.py <ASIN>
```
*Actions Executed*:
1. Unlinks `bridge_{asin}.html` and `focus_product_{asin}_hook.jpg`.
2. Strips `<div class="card-wrapper" id="card-{asin}"...>` from `index.html`.
3. Removes ASIN entry from `product_price_registry.json` and `processed_asins.json`.
4. Runs `git add -A`, commits, and pushes live to GitHub Pages.

---

## 7. Active Homepage Products Registry
1. `B0GYDXHF4G` - Flame Aroma Essential Oil Diffuser ($35.00)
2. `B0FXLYXM32` - White Wavy Wall Vanity Mirror ($76.49)
3. `B0C2YLN3H4` - White Ceramic Donut Vase Set of 2 ($14.99)
4. `B07HP22QTZ` - Crystal Prism Window Suncatcher ($9.99)
5. `B0BZXNSW5K` - Fenmzee Bedside Table Touch Lamp ($19.99)
6. `B0DXKGL1T2` - Lily of the Valley Flower Lamp ($38.57) *(Exempt from bulk regen)*
7. `B0D1FRDFFX` - Dawnwake Mushroom Touch Table Lamp ($35.98)
8. `B0D8P8CSYP` - Cute Bird Dimmable Touch Night Lamp ($20.56)
9. `B0DLN5S5K9` - WLHBF Vintage Flower Table Lamp ($24.99) *(Exempt from bulk regen)*

---

## 🛍️ Currently Live Homepage Products (10 Items Total)

### ✅ POSTED TO PINTEREST (5 Pins Published):
1. **`B0GYDXHF4G`**: Flame Aroma Essential Oil Diffuser Dark Crackle ($35.00) — Pin ID `1092545190892598928`
2. **`B0FXLYXM32`**: Pocetry 22"x30" White Wavy Wall & Vanity Mirror ($76.49) — Pin ID `1092545190892598932`
3. **`B0C2YLN3H4`**: White Ceramic Donut Vase Set of 2 ($13.49) — Pin ID `1092545190892598936`
4. **`B07HP22QTZ`**: Suncatcher Crystal Ball Prism Window Rainbow Maker ($9.99) — Pin ID `1092545190892598942`
5. **`B0BDRSG2BT`**: Tsrarey Sunset Projection Lamp Light ($16.99) — Pin ID `1092545190892598946`

### ⏳ UNPOSTED HOMEPAGE PRODUCTS (5 Items Queued):
6. **`B0GGHJ1J4L`**: LED Acrylic Glowing Desktop Note Board ($18.99) — Status: `UNPOSTED`
7. **`B0BZXNSW5K`**: Fenmzee Bedside Table Touch Lamp ($19.99) — Status: `UNPOSTED`
8. **`B0DXKGL1T2`**: Lily of the Valley Flower Table Lamp (£36.38) — Status: `UNPOSTED`
9. **`B0D1FRDFFX`**: Dawnwake Mushroom Touch Table Lamp ($39.98) — Status: `UNPOSTED`
10. **`B0D8P8CSYP`**: Cute Bird Dimmable Touch Night Lamp ($20.56) — Status: `UNPOSTED`

---

## 📋 Verified Candidate Queue for Next Generation Session
1. **`B0GT5GWK4B`**: Dreamholder Top-Down Candle Warmer Lamp with Timer ($14.99)
   - *Link*: `https://www.amazon.com/dp/B0GT5GWK4B?tag=smartdeal0358-21`
2. **`B0CXSRT211`**: IOWER Boho Macrame Woven Wall Hanging Tapestry ($31.50)
   - *Link*: `https://www.amazon.com/dp/B0CXSRT211?tag=smartdeal0358-21`
