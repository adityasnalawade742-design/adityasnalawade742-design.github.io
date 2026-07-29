import sys
import io
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.automated_product_selector import save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page

asin = "B0D1FRDFFX"
flux_image_path = "G:/CLI/pinterest-auto-affiliate/flux.jpg"

print(f"[Step 1] Publishing Campaign for ASIN {asin} (Mushroom Lamp) using flux.jpg...")

# Copy flux.jpg to raw_images/raw_B0D1FRDFFX.jpg
raw_dir = Path("G:/CLI/pinterest-auto-affiliate/raw_images")
raw_dir.mkdir(parents=True, exist_ok=True)
clean_raw_path = raw_dir / f"raw_{asin}.jpg"
shutil.copy(flux_image_path, clean_raw_path)
print(f" 💾 Saved raw image to: {clean_raw_path}")

prod = {
    "title": "Mushroom Lamp Glass Table Lamp for Bedroom & Nightstand Decor",
    "price": "$35.98",
    "rating": "4.8",
    "features": [
        "AESTHETIC MUSHROOM DESIGN",
        "WARM AMBIENT GLOW",
        "BLOWN GLASS LAMPSHADE",
        "PERFECT BEDSIDE DECOR"
    ],
    "category": "Bedside & Nightstand Ambient Decor"
}

seo_data = {
    "pin_title": "Aesthetic Glass Mushroom Table Lamp for Bedroom Decor",
    "image_hook": "Glass Mushroom Table Lamp",
    "subtitle_hook": "",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Upgrade your nightstand aesthetic with this cozy glass mushroom table lamp. Emits a warm ambient glow perfect for bedroom and desk setups.",
    "suggested_board": "Cozy Room & Desk Decor",
    "keywords": ["mushroom lamp", "glass table lamp", "aesthetic room decor", "cozy bedside lamp", "nightstand light"]
}

# Step 2: Playwright 1200x1600 Graphic Overlay Render (Rule 7 subtitle="")
print("\n[Step 2] Playwright HTML/CSS Rendering Floating Graphic Overlay...")
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
print("\n[Step 3] Generating Luxury Bridge Page & Syncing Homepage Gallery...")
generate_bridge_page(prod, seo_data, asin)
save_processed_asin(asin)

# Step 4: Register in Daily Price Sync Registry
from daily_price_updater import load_registry, save_registry
registry = load_registry()
registry[asin] = {
    "title": prod['title'],
    "url": f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21",
    "current_price": prod['price'],
    "headline": seo_data["image_hook"],
    "subtitle": "",
    "badge": "VIRAL ROOM FIND",
    "features": prod['features'],
    "raw_image": f"raw_images/raw_{asin}.jpg",
    "hook_image": f"focus_product_{asin}_hook.jpg",
    "bridge_page": f"bridge_{asin}.html"
}
save_registry(registry)

# Step 5: Git Commit & Deploy Live to GitHub Pages
print("\n[Step 4] Deploying Live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", f"publish B0D1FRDFFX glass mushroom lamp campaign using flux.jpg"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(" ✅ Git Commit & Push Successful!")
except Exception as e:
    print(f" ⚠️ Git Push Warning: {e}")

print(f"\n🎉 SUCCESS! Fully updated and deployed campaign for ASIN {asin} using flux.jpg!")
