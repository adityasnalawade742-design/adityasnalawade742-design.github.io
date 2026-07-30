import sys
import io
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.automated_product_selector import save_processed_asin
from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page

asin = "B0DZD1X83N"
flux_image_path = "G:/CLI/pinterest-auto-affiliate/flux.jpg"

print(f"[Step 1] Updating Bridge Page for ASIN {asin} with Amazon India Geo-Redirector...")

raw_dir = Path("G:/CLI/pinterest-auto-affiliate/raw_images")
raw_dir.mkdir(parents=True, exist_ok=True)
clean_raw_path = raw_dir / f"raw_{asin}.jpg"
if Path(flux_image_path).exists():
    shutil.copy(flux_image_path, clean_raw_path)

prod = {
    "title": "Minimalist Wood Base Cream Shade Bedside Table Lamp",
    "price": "$12.99",
    "rating": "4.6",
    "features": [
        "MINIMALIST WOOD BASE",
        "CREAM FABRIC LAMPSHADE",
        "WARM AMBIENT GLOW",
        "INLINE CONTROL SWITCH"
    ],
    "category": "Bedside & Nightstand Ambient Decor"
}

seo_data = {
    "pin_title": "Minimalist Wood Base Bedside Table Lamp for Bedroom Decor",
    "image_hook": "Minimalist Wood Bedside Lamp",
    "subtitle_hook": "",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Transform your nightstand setup with this aesthetic minimalist wood base table lamp. Warm ambient glow perfect for cozy reading and bedroom decor.",
    "suggested_board": "Cozy Room & Desk Decor",
    "keywords": ["bedside lamp", "minimalist table lamp", "wood base lamp", "cozy bedroom decor", "aesthetic nightstand setup"]
}

# Step 2: Playwright 1200x1600 Graphic Overlay Render
hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
render_html_overlay(
    image_path=str(clean_raw_path),
    headline=seo_data["image_hook"],
    subtitle="",
    badge_text=seo_data["badge_hook"],
    price_str=prod['price'],
    output_path=hook_img_path
)

# Step 3: Generate Luxury Mobile Bridge Page & Update Homepage Gallery
generate_bridge_page(prod, seo_data, asin)
save_processed_asin(asin)

# Step 4: Git Commit & Deploy Live to GitHub Pages
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"update B0DZD1X83N with Amazon India Geo-Redirector"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(" ✅ Git Commit & Push Successful!")
except Exception as e:
    print(f" ⚠️ Git Push Warning: {e}")

print(f"\n🎉 SUCCESS! Fully updated bridge page for ASIN {asin} with Amazon India Geo-Redirector!")
