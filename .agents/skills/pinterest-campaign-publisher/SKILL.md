---
name: pinterest-campaign-publisher
description: >-
  Step-by-step workflow for discovering a new Amazon product and executing an end-to-end
  Pinterest automated affiliate campaign. Use when discovering new products, running main.py,
  creating composite 3-in-1 reference sheets, generating Flux Dev/Imagen 3 AI vision prompts,
  rendering Playwright graphic price overlays, generating Jinja2 bridge landing pages,
  and publishing pin payloads to Pinterest API v5.
---

# 📌 Pinterest Campaign Publisher Skill

This skill defines the complete end-to-end automation workflow for discovering Amazon products, generating AI lifestyle images, creating Playwright price overlays, building mobile bridge landing pages, and publishing pin payloads directly to Pinterest API v5.

---

## ⚙️ Workflow Execution Pipeline

### Step 1: Discover Live Amazon Products
Fetch candidate Amazon products using `modules/amazon_finder.py` or `main.py`:
```bash
python main.py
```
- Uses SerpAPI search queries (*e.g., "aesthetic coffee mug warmer cozy desk"*).
- Caches search responses in `serpapi_cache.json` to minimize API quota usage.
- Evaluates aesthetic suitability using `is_pinterest_aesthetic_gemini()`.

---

### Step 2: 4-Layer Photo Selection Pipeline (`modules/amazon_extractor.py`)
Filter candidate listing photos using the 4-layer inspection engine:
1. **Text & Infographic Scanner**: `top_contrast > 0.035` or `full_contrast > 0.035` (discards seller callouts, dimensions, badges).
2. **Grid Collage Scanner**: `v_seam > 0.20` and `h_seam > 0.20` (discards split grid collages).
3. **Human / Model Scanner**: `skin_ratio > 0.10` (discards human models/hands; keeps pure room focus).
4. **Cozy Vibe Aesthetics Scorer**: Ranks remaining clean images based on warm color temperature ($R > G > B$) on a 1.0 to 10.0 scale.

---

### Step 3: Multi-Angle Reference Sheet & AI Vision Prompting
1. Build a 3-in-1 multi-angle reference collage:
   ```python
   from modules.image_generator import create_multi_photo_reference_sheet
   ref_sheet = create_multi_photo_reference_sheet(photo_urls, filename_prefix=f"product_{asin}")
   ```
2. Generate structured vision prompts via `modules/vision_prompt.py`:
   ```python
   from modules.vision_prompt import generate_cozy_image_prompt
   prompt = generate_cozy_image_prompt(product_title, category, key_features, ref_sheet_path=ref_sheet)
   ```

---

### Step 4: AI Image Generation & Img2Img Prompt Strength Rules
Generate high-res 3:4 aspect ratio lifestyle room photos via Replicate Flux Dev / Imagen 3:
- **Existing Lifestyle Room Photos**: Set `prompt_strength` between **`0.28` and `0.55`** to prevent hallucinating extra props.
  - Set `0.28` for **Item Sets / Multi-Packs** (*e.g., 2-piece donut vase set*).
  - Set `0.48 – 0.55` for **Single Solid Items** (*e.g., 1 wall mirror*).
- **Plain White Studio Cutouts**: Set `prompt_strength` between **`0.75` and `0.80`** to synthesize a full aesthetic background from scratch.

---

### Step 5: SEO Copywriting & Tag Generation
Generate Pinterest SEO metadata via `modules/seo_copywriter.py`:
```python
from modules.seo_copywriter import generate_pin_seo_data
seo_data = generate_pin_seo_data(product_title=title, price=price, category=category)
```
- Output fields: `pin_title` (max 100 chars), `image_hook`, `description` (max 500 chars), `suggested_board`.

---

### Step 6: Render Playwright Floating Graphic Overlay
Overlay price tag badges onto the generated image via `modules/html_overlay_engine.py`:
- Calculates dynamic bounding box using Gemini vision analysis (`analyze_tag_and_room_with_gemini`).
- Renders 1200x1600 Playwright dark glassmorphism card (`background: rgba(15, 14, 19, 0.72)`).
- Enforces **Empty Subtitle Policy** (`subtitle=""`).

---

### Step 7: Build Bridge Landing Page & Publish Pin
1. Generate bridge landing page:
   ```python
   from modules.bridge_creator import generate_bridge_page
   bridge_path = generate_bridge_page(product=product_dict, seo=seo_data, image_path=final_image_path)
   ```
2. Publish pin payload to Pinterest API v5:
   ```python
   from modules.pinterest_publisher import publish_pin_to_pinterest
   pin_result = publish_pin_to_pinterest(
       image_path=final_image_path,
       title=seo_data['pin_title'],
       description=seo_data['description'],
       destination_url=live_destination_url,
       image_url=live_image_url,
       board_id="1092545259543920271"
   )
   ```

---

## 🔒 Mandatory Verification Checklist
- [ ] Product price in graphic overlay matches exact live Amazon listing price.
- [ ] Bridge landing page (`bridge_{asin}.html`) contains 0ms geo-redirector script.
- [ ] Outgoing CTA link carries official associate tag `smartdeal0358-21`.
- [ ] `product_price_registry.json` updated with new ASIN metadata.
- [ ] `campaign_summary.json` saved in `output/`.
