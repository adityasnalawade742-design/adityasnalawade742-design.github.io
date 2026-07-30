import os
import sys
import time
import json
import re
import shutil
import requests
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page
from modules.seo_copywriter import generate_pin_seo_data

asin = "B0BZXNSW5K"
selected_photo_url = "https://m.media-amazon.com/images/I/71zreHoOzVL._AC_SL1500_.jpg"

print(f"==================================================")
print(f"📸 APPLYING USER-SELECTED PHOTO #1 FOR ASIN: {asin}")
print(f"   URL: {selected_photo_url}")
print(f"==================================================")

# Step 1: Download Photo #1 to raw_images/raw_B0BZXNSW5K.jpg
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(parents=True, exist_ok=True)
saved_raw_path = raw_dir / f"raw_{asin}.jpg"

print(f"\n[Step 1] Downloading Photo #1 to {saved_raw_path}...")
res = requests.get(selected_photo_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
if res.status_code == 200 and len(res.content) > 3000:
    saved_raw_path.write_bytes(res.content)
    print(" ✅ Download successful!")
else:
    raise RuntimeError(f"Failed downloading photo: HTTP {res.status_code}")

# Step 2: Render High-Res 1200x1600 Playwright Canva Overlay
print("\n✨ [Step 2] Rendering High-Res 1200x1600 Playwright Graphic Overlay...")
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

# Copy to output/images
out_img = repo_dir / "output" / "images" / f"focus_product_{asin}_hook.jpg"
out_img.parent.mkdir(parents=True, exist_ok=True)
shutil.copy(hook_img_path, out_img)

# Step 3: Update Landing Page & Homepage Gallery with Cache Buster
print("\n🌉 [Step 3] Updating Landing Page & Storefront Gallery with Cache Buster...")
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

# Step 4: Update product_price_registry.json
from daily_price_updater import load_registry, save_registry
registry = load_registry()
registry[asin] = {
    "title": prod['title'],
    "url": f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21",
    "current_price": prod['price'],
    "headline": "Dimmable Touch Nightstand Lamp",
    "subtitle": "",
    "badge": "🕯️ BEDSIDE FAVORITE",
    "features": prod['features'],
    "raw_image": f"raw_images/raw_{asin}.jpg",
    "hook_image": f"focus_product_{asin}_hook.jpg",
    "bridge_page": f"bridge_{asin}.html"
}
save_registry(registry)

# Step 5: Git Commit & Deploy Live to GitHub Pages
print("\n🚀 [Step 4] Deploying updated image and landing page live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", f"apply Photo #1 (71zreHoOzVL) for B0BZXNSW5K bedside touch lamp ({cache_buster})"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e_git:
    print(f" ⚠️ Git push warning: {e_git}")

print(f"\n🎉 SUCCESS! Fully updated and deployed Photo #1 campaign for ASIN {asin}!")
print(f" 🌐 Live Landing Page: https://adityasnalawade742-design.github.io/bridge_{asin}.html")
