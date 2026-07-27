import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.automated_product_selector import save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.bridge_creator import generate_bridge_page

asin = "B0GYDXHF4G"
amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"

print(f"[Step 1] Processing Selected Product: {asin} - Flame Aroma Diffuser Dark Crackle Design...")

prod = get_product_details_and_photos(amazon_url)
if not prod:
    print("Error extracting Amazon details. Aborting.")
    sys.exit(1)

prod["price"] = "$35.00"
if not prod.get("title") or prod["title"] == "Aesthetic Bedside Decor Find":
    prod["title"] = "Flame Aroma Essential Oil Diffuser - Dark Crackle Design with Warm LED Glow"

print(f"Title: {prod['title']}")
print(f"Price: {prod['price']} | Rating: {prod['rating']}")
photos = prod.get("all_photos", [])
print(f"Extracted {len(photos)} Amazon listing photos.")

# Step 2: Multi-photo reference sheet
print("\n[Step 2] Creating Multi-Angle Composite Reference Sheet...")
ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{asin}", max_photos=6)

# Step 3: Vision Master Prompt
print("\n[Step 3] Generating Vision Master Commercial Prompt...")
cozy_prompt = generate_cozy_image_prompt(
    product_title=prod['title'],
    category="Home Fragrance & Ambient Room Atmosphere",
    key_features=prod['features'],
    ref_sheet_path=ref_sheet_path
)

# Step 4: FLUX-Dev Paid Img2Img AI Render (Seed 591928, FP16 32-step)
print("\n[Step 4] Paid Replicate FLUX-Dev Img2Img Rendering 8K Commercial Graphic...")
init_photo = photos[0] if photos else ""
raw_image_path = generate_cozy_image(
    prompt=cozy_prompt,
    filename_prefix=f"focus_product_{asin}",
    init_image_path=init_photo
)

# Step 5: SEO Copywriter
print("\n[Step 5] Writing SEO Title & Viral Hook Headline...")
seo_data = {
    "pin_title": "Flame Aroma Essential Oil Diffuser for Cozy Bedroom",
    "image_hook": "Flame Aroma Diffuser",
    "subtitle_hook": "WARM AMBIENT GLOW",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Create a cozy bedroom sanctuary with this dark crackle ceramic flame essential oil diffuser. Projects realistic warm mist flame rings for ambient evening relaxation.",
    "suggested_board": "Cozy Fragrance & Ambient Decor",
    "keywords": ["flame diffuser", "essential oil diffuser", "ambient room glow", "cozy bedroom decor", "dark ceramic diffuser"]
}

headline = seo_data["image_hook"]
print(f" -> Headline: '{headline}'")

# Step 6: Playwright Graphic Overlay Engine
print("\n[Step 6] Playwright HTML/CSS Rendering Floating Graphic Overlay...")
hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
render_html_overlay(
    image_path=raw_image_path,
    headline=headline,
    subtitle=seo_data["subtitle_hook"],
    badge_text=seo_data["badge_hook"],
    price_str=prod['price'],
    output_path=hook_img_path
)

# Step 7: Vogue Mobile Bridge Page & Auto-Sync Homepage
print("\n[Step 7] Generating Luxury Bridge Page & Syncing Homepage Gallery...")
generate_bridge_page(prod, seo_data, asin)

save_processed_asin(asin)
print(f"\nSUCCESS! Fully processed and deployed selected product: {asin}")
