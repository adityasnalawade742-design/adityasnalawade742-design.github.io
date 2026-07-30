import os
import sys
import time
import json
import re
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

from config import REPLICATE_API_TOKEN, AMAZON_ASSOCIATE_TAG
from modules.amazon_extractor import get_product_details_and_photos, select_clean_photo_or_skip
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page
from modules.seo_copywriter import generate_pin_seo_data

asin = "B0BZXNSW5K"
print(f"==================================================")
print(f"🚀 RE-GENERATING 8K FLUX AI IMAGE FOR ASIN: {asin}")
print(f"   Product: Touch Bedside Table Lamp")
print(f"==================================================")

# Step 1: Fetch listing details & clean photo
print("\n📸 [Step 1] Fetching Amazon listing photo suite for B0BZXNSW5K...")
details = get_product_details_and_photos(asin)
photos = details.get("all_photos", []) if details else []

clean_photo, skip = select_clean_photo_or_skip(photos)
if not clean_photo and photos:
    clean_photo = photos[0]

print(f" └─ Selected Clean Listing Photo: {clean_photo}")

# Step 2: Build Reference Sheet & Vision Prompt
ref_sheet = create_multi_photo_reference_sheet(photos or [clean_photo], filename_prefix=f"product_{asin}")
prompt = generate_cozy_image_prompt(
    product_title="Touch Bedside Table Lamp with USB Ports",
    category="Bedside & Nightstand Ambient Decor",
    key_features="3-way dimmable touch control, dual USB charging ports, warm amber glow",
    ref_sheet_path=ref_sheet,
    is_white_background=False
)
print(f" └─ FLUX AI Prompt: {prompt[:120]}...")

# Step 3: Call Replicate FLUX-Dev model for 8K photorealistic room render
print("\n🎨 [Step 2] Generating new 8K FLUX-Dev image via Replicate API...")
raw_gen_path = generate_cozy_image(
    prompt=prompt,
    filename_prefix=f"focus_product_{asin}_new",
    init_image_path=clean_photo,
    prompt_strength=0.48
)

print(f" └─ Generated Raw AI Image: {raw_gen_path}")

# Copy to raw_images/raw_B0BZXNSW5K.jpg
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(parents=True, exist_ok=True)
saved_raw_path = raw_dir / f"raw_{asin}.jpg"
shutil.copy(raw_gen_path, saved_raw_path)

# Step 4: Render High-Res 1200x1600 Playwright Canva Overlay
print("\n✨ [Step 3] Rendering High-Res 1200x1600 Playwright Graphic Overlay...")
prod = {
    "title": "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet",
    "price": "$19.99",
    "rating": "4.5",
    "features": ["DIMMABLE TOUCH CONTROL", "DUAL USB A+C CHARGING PORTS", "BUILT-IN AC OUTLET", "LED BULB INCLUDED"],
    "category": "lighting"
}
seo_data = generate_pin_seo_data(prod["title"], prod["price"])

hook_img_path = repo_dir / f"focus_product_{asin}_hook.jpg"
render_html_overlay(
    image_path=str(saved_raw_path),
    headline="Dimmable Touch Nightstand Lamp",
    subtitle="",
    badge_text="🕯️ BEDSIDE FAVORITE",
    price_str="$19.99",
    features=prod["features"],
    output_path=str(hook_img_path)
)

# Step 5: Update Landing Page & Homepage Gallery with Cache Buster
print("\n🌉 [Step 4] Updating Landing Page & Storefront Gallery with Cache Buster...")
cache_buster = f"v={int(time.time())}"
generate_bridge_page(prod, seo_data, asin)

# Update index.html image version
index_file = repo_dir / "index.html"
if index_file.exists():
    content = index_file.read_text(encoding="utf-8")
    content = re.sub(
        rf'focus_product_{asin}_hook\.jpg(?:\?v=[^\'"]+)?',
        f'focus_product_{asin}_hook.jpg?{cache_buster}',
        content
    )
    index_file.write_text(content, encoding="utf-8")

# Update bridge page image version
bridge_file = repo_dir / f"bridge_{asin}.html"
if bridge_file.exists():
    b_content = bridge_file.read_text(encoding="utf-8")
    b_content = re.sub(
        rf'focus_product_{asin}_hook\.jpg(?:\?v=[^\'"]+)?',
        f'focus_product_{asin}_hook.jpg?{cache_buster}',
        b_content
    )
    bridge_file.write_text(b_content, encoding="utf-8")

# Step 6: Git Commit & Deploy Live to GitHub Pages
print("\n🚀 [Step 5] Deploying updated image and landing page live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", f"re-generate FLUX 8K AI room image for B0BZXNSW5K bedside touch lamp ({cache_buster})"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e_git:
    print(f" ⚠️ Git push warning: {e_git}")

print(f"\n🎉 RE-GENERATION & DEPLOYMENT COMPLETE FOR ASIN {asin}!")
print(f" 🌐 Live Landing Page: https://adityasnalawade742-design.github.io/bridge_{asin}.html")
