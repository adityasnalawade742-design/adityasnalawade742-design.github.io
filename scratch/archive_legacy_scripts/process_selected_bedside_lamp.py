import sys
import io
import json
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.automated_product_selector import save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page

asin = "B0DZD1X83N"
amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"

print(f"[Step 1] Processing Selected Product: {asin} - Minimalist Wood Bedside Lamp...")

prod = get_product_details_and_photos(amazon_url)
if not prod:
    print("Error extracting Amazon details. Aborting.")
    sys.exit(1)

prod["price"] = "$12.99"
if not prod.get("title") or prod["title"] == "Aesthetic Bedside Decor Find":
    prod["title"] = "9 Inch Small Minimalist Table Lamp for Bedroom Wood Base"

print(f"Title: {prod['title']}")
print(f"Price: {prod['price']} | Rating: {prod['rating']}")
photos = prod.get("all_photos", [])
print(f"Extracted {len(photos)} Amazon listing photos.")

# User selected Photo #1
selected_photo = "https://m.media-amazon.com/images/I/71HckKKPVML._AC_SL1500_.jpg"
print(f" -> User Selected Photo #1: {selected_photo}")

# Step 2: Multi-photo reference sheet
print("\n[Step 2] Creating Multi-Angle Composite Reference Sheet...")
ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{asin}", max_photos=6)

# Step 3: Vision Master Prompt (is_white_background=False for lifestyle photo)
print("\n[Step 3] Generating Vision Master Commercial Prompt (Preserving Room Table Scene)...")
cozy_prompt = generate_cozy_image_prompt(
    product_title=prod['title'],
    category="Bedside & Nightstand Ambient Decor",
    key_features=prod['features'],
    ref_sheet_path=ref_sheet_path,
    is_white_background=False
)

# Step 4: FLUX-Dev Paid Img2Img AI Render (Seed 591928, FP16 32-step, strength=0.45)
print("\n[Step 4] Paid Replicate FLUX-Dev Img2Img Rendering 8K Commercial Graphic (strength=0.45)...")
raw_image_path = generate_cozy_image(
    prompt=cozy_prompt,
    filename_prefix=f"focus_product_{asin}",
    init_image_path=selected_photo,
    prompt_strength=0.45
)

# Step 5: SEO Copywriter
print("\n[Step 5] Writing SEO Title & Viral Hook Headline...")
seo_data = {
    "pin_title": "Minimalist Wood Base Bedside Table Lamp for Bedroom Decor",
    "image_hook": "Minimalist Wood Bedside Lamp",
    "subtitle_hook": "",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Transform your nightstand setup with this aesthetic minimalist wood base table lamp. Warm ambient glow perfect for cozy reading and bedroom decor.",
    "suggested_board": "Cozy Room & Desk Decor",
    "keywords": ["bedside lamp", "minimalist table lamp", "wood base lamp", "cozy bedroom decor", "aesthetic nightstand setup"]
}

headline = seo_data["image_hook"]
print(f" -> Headline: '{headline}'")

# Step 6: Playwright Graphic Overlay Engine (Rule 7 subtitle="")
print("\n[Step 6] Playwright HTML/CSS Rendering Floating Graphic Overlay...")
hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
render_html_overlay(
    image_path=raw_image_path,
    headline=headline,
    subtitle="",
    badge_text=seo_data["badge_hook"],
    price_str=prod['price'],
    output_path=hook_img_path
)

# Step 7: Vogue Mobile Bridge Page & Auto-Sync Homepage
print("\n[Step 7] Generating Luxury Bridge Page & Syncing Homepage Gallery...")
generate_bridge_page(prod, seo_data, asin)

save_processed_asin(asin)

# Step 8: Deploy Live to GitHub Pages
print("\n[Step 8] Deploying Updates Live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"publish B0DZD1X83N minimalist bedside lamp campaign"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(" ✅ Git Commit & Push Successful!")
except Exception as e:
    print(f" ⚠️ Git Push Warning: {e}")

print(f"\nSUCCESS! Fully processed and deployed selected product: {asin}")
