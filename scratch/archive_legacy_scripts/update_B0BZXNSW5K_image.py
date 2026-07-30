import sys
import time
import requests
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page

asin = "B0BZXNSW5K"
raw_photo_url = "https://m.media-amazon.com/images/I/61PqF3ZxdwL._AC_SL1500_.jpg"
raw_local_path = f"G:/CLI/pinterest-auto-affiliate/raw_{asin}_console.jpg"
hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"

print(f"📥 Downloading selected product photo for {asin}...")
res = requests.get(raw_photo_url, timeout=10)
with open(raw_local_path, "wb") as f:
    f.write(res.content)

print(f"🎨 Rendering 1200x1600 Playwright Visual Overlay on selected photo...")
title_hook = "Bedside Table Touch Lamp"
price_str = "$19.99"
badge_hook = "VIRAL ROOM FIND"

render_html_overlay(raw_local_path, title_hook, "", badge_hook, price_str, hook_img_path)
print(f"✅ Saved updated overlay image: {hook_img_path}")

# Update bridge page HTML with cache buster
ts = int(time.time())
bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
if bridge_file.exists():
    content = bridge_file.read_text(encoding="utf-8")
    content = content.replace(f"focus_product_{asin}_hook.jpg?v=3", f"focus_product_{asin}_hook.jpg?v={ts}")
    content = content.replace(f"focus_product_{asin}_hook.jpg?v=master_vision_v6", f"focus_product_{asin}_hook.jpg?v={ts}")
    bridge_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated cache buster in bridge_{asin}.html to ?v={ts}")

# Update index.html HTML with cache buster
index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
if index_file.exists():
    content = index_file.read_text(encoding="utf-8")
    content = content.replace(f"focus_product_{asin}_hook.jpg?v=master_vision_v6", f"focus_product_{asin}_hook.jpg?v={ts}")
    content = content.replace(f"focus_product_{asin}_hook.jpg?v=3", f"focus_product_{asin}_hook.jpg?v={ts}")
    index_file.write_text(content, encoding="utf-8")
    print(f"✅ Updated cache buster in index.html to ?v={ts}")

# Commit & Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"update image for {asin} with fresh Playwright overlay v={ts}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("🚀 Successfully pushed updated image live to GitHub Pages!")
