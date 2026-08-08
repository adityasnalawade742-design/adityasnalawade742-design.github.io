---
name: playwright-overlay-designer
description: >-
  Design specifications, layout standards, and troubleshooting procedures for Playwright floating graphic
  pin overlays (modules/html_overlay_engine.py). Use when updating pin graphics, tweaking price badges,
  configuring Gemini bounding box detection, or fixing overlay typography and contrast rendering bugs.
---

# 🎨 Playwright Graphic Overlay Designer Skill

This skill defines the visual design system, rendering specifications, and code rules for creating high-res 1200x1600 floating price pin graphics via `modules/html_overlay_engine.py`.

---

## 📐 Visual Design System & Layout Specifications

1. **Canvas Resolution**: Fixed 1200 x 1600 pixels (standard 3:4 vertical Pinterest pin aspect ratio).
2. **Backdrop Card Styling**:
   - Background: `rgba(15, 14, 19, 0.72)` (dark glassmorphism).
   - Border: 1.5px subtle amber border (`rgba(255, 183, 3, 0.55)`).
   - Blur: `backdrop-filter: blur(12px)`.
3. **Typography**:
   - Primary Header: `Outfit`, `Plus Jakarta Sans`, sans-serif.
   - Font Weight: `800` (extra bold uppercase).
   - Font Color: Pure White (`#FFFFFF`) with subtle text shadow.
4. **Bottom Feature Bar Grid**:
   - Layout: Equal-width 4-column side-by-side grid (`grid-template-columns: repeat(4, 1fr)`).
   - Card Text: 13.5px uppercase bold with single-line ellipsis truncation.
   - Accents: `✨` sparkle icons and glowing amber price tags (`#ffb703` / `#fb8500`).

---

## 🚫 Mandatory Design Rules

1. **Empty Subtitle Policy**:
   - Subtitles MUST be left empty (`subtitle=""`) unless explicitly requested by the user.
   - **NEVER** add generic marketing fluff subtitles like `"ELEVATE YOUR VANITY SPACE"`, `"VINTAGE FLORAL GLOW"`, or arbitrary taglines.

2. **Gemini Vision Bounding Box Detection**:
   - `analyze_tag_and_room_with_gemini()` analyzes raw room photos to determine the optimal $[ymin, xmin, ymax, xmax]$ bounding box where the overlay badge will not obscure key product details.

3. **Pillow Graphic Fallback**:
   - If Playwright headless browser rendering fails or is unavailable, `render_pillow_fallback()` and `stamp_price_onto_tag_image()` execute Pillow-based image manipulation to stamp clean price tags onto the image.

---

## 🛠️ Re-Rendering & Debug Commands

### Re-render Price Overlay for Specific ASIN
Execute single-script badge re-renders via python:
```python
from modules.html_overlay_engine import render_html_overlay

render_html_overlay(
    image_path="raw_images/raw_B0D8P8CSYP.jpg",
    headline="Cute Bird Touch Table Lamp",
    subtitle="",
    badge_text="🐦 CUTE BEDSIDE PICK",
    price_str="$20.56",
    features=["RECHARGEABLE BATTERY", "TOUCH DIMMING", "WOODGRAIN FINISH", "PORTABLE LIGHT"],
    output_path="focus_product_B0D8P8CSYP_hook.jpg",
    theme="bottom_glass_card"
)
```

### Run Badge Re-Render Suite for All Catalog USD Prices
```bash
python scratch/rebuild_all_price_badges_usd.py
```

---

## 📋 Overlay Quality Audit Checklist
- [ ] Graphic output dimensions are exactly 1200 x 1600.
- [ ] Bottom feature bar is rendered cleanly in a 4-column glassmorphic grid.
- [ ] Price text matches exact live Amazon price tag.
- [ ] Subtitle string is empty (`""`) without fluff text.
- [ ] Copy saved to both root directory and `output/images/`.
