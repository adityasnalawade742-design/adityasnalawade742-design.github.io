import sys
import time
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.html_overlay_engine import render_html_overlay

asin = "B0BZXNSW5K"
custom_img_path = Path("G:/CLI/pinterest-auto-affiliate/b9e65w6bf9rn80cznt1tap5v28.jpg")
hook_img_path = Path(f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg")

if not custom_img_path.exists():
    print(f"❌ Custom image file not found: {custom_img_path}")
    sys.exit(1)

print(f"🖼️ Found user custom image: {custom_img_path} ({custom_img_path.stat().st_size / 1024:.1f} KB)")

# Render Playwright 1200x1600 Pinterest visual overlay
title_hook = "Bedside Table Touch Lamp"
price_str = "$19.99"
badge_hook = "VIRAL ROOM FIND"

print(f"🎨 Rendering Playwright 1200x1600 visual overlay onto user image...")
render_html_overlay(str(custom_img_path), title_hook, "", badge_hook, price_str, str(hook_img_path))
print(f"✅ Saved overlay image: {hook_img_path}")

# Update cache buster query parameter on bridge page and index.html
ts = int(time.time())
cache_buster = f"v={ts}"

bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
if bridge_file.exists():
    content = bridge_file.read_text(encoding="utf-8")
    # Replace any existing ?v=... parameter for focus_product_B0BZXNSW5K_hook.jpg
    import re
    content = re.sub(r'focus_product_B0BZXNSW5K_hook\.jpg(?:\?v=[^\'"]+)?', f'focus_product_B0BZXNSW5K_hook.jpg?{cache_buster}', content)
    bridge_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated bridge_{asin}.html with cache buster ?{cache_buster}")

index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
if index_file.exists():
    content = index_file.read_text(encoding="utf-8")
    import re
    content = re.sub(r'focus_product_B0BZXNSW5K_hook\.jpg(?:\?v=[^\'"]+)?', f'focus_product_B0BZXNSW5K_hook.jpg?{cache_buster}', content)
    index_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated index.html with cache buster ?{cache_buster}")

# Commit and Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"apply user generated image b9e65w6bf9rn80cznt1tap5v28 for B0BZXNSW5K ({cache_buster})"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\n🚀 SUCCESS! User custom image applied and deployed live to GitHub Pages!")
