# 🌸 Pinterest Auto-Affiliate Automation Pipeline

A fully autonomous, multi-currency Amazon Associate affiliate marketing platform built for **Pinterest & Aesthetic Home Decor**.

🌐 **Live Storefront**: [https://adityasnalawade742-design.github.io](https://adityasnalawade742-design.github.io)

---

## 📌 Architecture & Features

1. **4-Layer Quality Photo Selection Engine (`modules/amazon_extractor.py`)**:
   - Inspects border pixels to filter out plain white cutouts.
   - Detects and discards seller text callouts, infographics, and dimension arrows.
   - Filters out human hands, arms, legs, and models (`skin_ratio > 0.03`).
   - Detects 2-grid and 4-grid split collages (`v_seam > 0.15`, `h_seam > 0.15`).
   - Ranks clean photos by Cozy Vibe Aesthetics (1.0 to 10.0) to select the #1 winner photo.

2. **Strict Replicate FLUX-Dev Engine (`modules/image_generator.py`)**:
   - Uses `black-forest-labs/flux-dev` Img2Img (`prompt_strength = 0.28 – 0.60`) to enhance room lighting while locking physical product structure.
   - Enforces strict Replicate execution with zero low-quality fallbacks.

3. **High-Converting Graphic Overlay Renderer (`modules/html_overlay_engine.py`)**:
   - Headless Playwright Chromium renders 1200x1600 3:4 vertical graphics with price pills, badges, 4 feature highlights, and **blank subtitles (`""`) per Rule 7**.

4. **Global Multi-Currency Engine (160+ Currencies)**:
   - Auto IP Geolocation (`ipapi.co/json`) converts prices into local currencies (`₹ INR`, `£ GBP`, `€ EUR`, `CA$ CAD`, `A$ AUD`, `¥ JPY`, etc.).
   - Live Exchange Rates API (`https://open.er-api.com/v6/latest/USD`).
   - Top-bar interactive currency selector dropdown.

5. **International Smart Geo-IP Location Router (`bridge_*.html`)**:
   - 3-way regional routing matrix: India (`Amazon.in`), UK & Europe (`Amazon.co.uk`), US & Rest of World (`Amazon.com`).

---

## 🛠️ CLI Commands & Maintenance

- **Delete Product Campaign**:
  ```powershell
  python delete_product.py <ASIN>
  ```
- **Daily Price Synchronization**:
  ```powershell
  python daily_price_updater.py
  ```

---

## 📄 License & Attribution
- Built with Python, Playwright, Replicate FLUX-Dev, Google GenAI, and Vanilla HTML5/CSS3.
- Affiliate Associate Tag: `smartdeal0358-21`
