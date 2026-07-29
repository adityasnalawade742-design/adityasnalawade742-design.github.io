import sys
import shutil
import requests
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.html_overlay_engine import render_html_overlay

asin = "B0D8P8CSYP"
raw_photo_url = "https://m.media-amazon.com/images/I/71tqnj0QnXL._AC_SL1500_.jpg"
raw_local_path = Path(f"G:/CLI/pinterest-auto-affiliate/raw_{asin}_console.jpg")
hook_filename = f"focus_product_{asin}_hook_v2.jpg"
hook_img_path = Path(f"G:/CLI/pinterest-auto-affiliate/{hook_filename}")

print(f"📥 Downloading selected product photo for {asin}...")
res = requests.get(raw_photo_url, timeout=10)
raw_local_path.write_bytes(res.content)

print(f"🎨 Rendering 1200x1600 Playwright Visual Overlay on selected photo...")
title_hook = "Cute Bird Dimmable Touch Night Lamp"
price_str = "$20.56"
badge_hook = "VIRAL ROOM FIND"
features = ["SUNSET PROJECTION GLOW", "360 DEGREE ROTATION", "USB POWERED", "PHOTO BACKGROUND LIGHT"]

render_html_overlay(
    str(raw_local_path),
    title_hook,
    "",
    badge_hook,
    price_str,
    features,
    str(hook_img_path)
)
print(f"✅ Saved updated overlay image: {hook_img_path} ({hook_img_path.stat().st_size / 1024:.1f} KB)")

# Overwrite default focus_product_B0D8P8CSYP_hook.jpg as well
shutil.copyfile(hook_img_path, Path(f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"))

# Update bridge page HTML with new filename
bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
if bridge_file.exists():
    content = bridge_file.read_text(encoding="utf-8")
    import re
    content = re.sub(rf'focus_product_{asin}_hook[^\'"]*\.jpg(?:\?v=[^\'"]+)?', hook_filename, content)
    bridge_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated bridge_{asin}.html to load {hook_filename}")

# Update index.html HTML with new filename
index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
if index_file.exists():
    content = index_file.read_text(encoding="utf-8")
    import re
    content = re.sub(rf'focus_product_{asin}_hook[^\'"]*\.jpg(?:\?v=[^\'"]+)?', hook_filename, content)
    index_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated index.html to load {hook_filename}")

# Commit & Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"publish {asin} from Web Console with new image {hook_filename}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("🚀 Successfully pushed updated Sunset Projection Lamp image live to GitHub Pages!")
