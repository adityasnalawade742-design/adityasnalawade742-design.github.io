import sys
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.html_overlay_engine import render_html_overlay

asin = "B0D8P8CSYP"
custom_img_path = Path("G:/CLI/pinterest-auto-affiliate/acjw3wxaadrny0czntsb5vbt8c.jpg")
hook_filename = "acjw3wxaadrny0czntsb5vbt8c.jpg"
hook_img_path = Path(f"G:/CLI/pinterest-auto-affiliate/{hook_filename}")

if not custom_img_path.exists():
    print(f"❌ Custom image file not found: {custom_img_path}")
    sys.exit(1)

print(f"🖼️ Found user custom image: {custom_img_path} ({custom_img_path.stat().st_size / 1024:.1f} KB)")

# Render Playwright 1200x1600 Pinterest visual overlay
title_hook = "Aesthetic Sunset Lamp Light"
price_str = "$18.99"
badge_hook = "VIRAL ROOM FIND"
features = ["SUNSET PROJECTION GLOW", "360 DEGREE ROTATION", "USB POWERED", "PHOTO BACKGROUND LIGHT"]

print(f"🎨 Rendering Playwright 1200x1600 visual overlay onto user image...")
render_html_overlay(
    str(custom_img_path),
    title_hook,
    "",
    badge_hook,
    price_str,
    features,
    str(hook_img_path)
)
print(f"✅ Saved overlay image: {hook_img_path} ({hook_img_path.stat().st_size / 1024:.1f} KB)")

# Also update focus_product_B0D8P8CSYP_hook.jpg
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

# Commit and Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"apply user generated image acjw3wxaadrny0czntsb5vbt8c for {asin}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\n🚀 SUCCESS! User custom image applied and deployed live to GitHub Pages!")
