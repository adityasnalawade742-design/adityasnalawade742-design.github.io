import sys
import time
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.html_overlay_engine import render_html_overlay

asin = "B0BZXNSW5K"
raw_img_path = Path("G:/CLI/pinterest-auto-affiliate/b9e65w6bf9rn80cznt1tap5v28.jpg")
overlay_filename = "b9e65w6bf9rn80cznt1tap5v28_dimmed_v2.jpg"
overlay_img_path = Path(f"G:/CLI/pinterest-auto-affiliate/{overlay_filename}")

title_hook = "Bedside Table Touch Lamp"
price_str = "$19.99"
badge_hook = "VIRAL ROOM FIND"

print(f"🎨 Rendering 1200x1600 Premium Floating Visual Overlay onto user photo...")
render_html_overlay(
    str(raw_img_path),
    title_hook,
    "",
    badge_hook,
    price_str,
    ["DIMMABLE TOUCH", "USB A+C CHARGING", "AC OUTLET", "LED BULB INCLUDED"],
    str(overlay_img_path)
)
print(f"Created overlay image: {overlay_img_path} ({overlay_img_path.stat().st_size / 1024:.1f} KB)")

# Update bridge page HTML with new overlay filename
bridge_file = Path(f"G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html")
content = bridge_file.read_text(encoding="utf-8")
import re
content = re.sub(r'b9e65w6bf9rn80cznt1tap5v28[^\'"]*\.jpg', overlay_filename, content)
bridge_file.write_text(content, encoding="utf-8")
print(f"✅ Updated bridge_{asin}.html to load {overlay_filename}")

# Update index.html HTML with new overlay filename
index_file = Path("G:/CLI/pinterest-auto-affiliate/index.html")
content = index_file.read_text(encoding="utf-8")
content = re.sub(r'b9e65w6bf9rn80cznt1tap5v28[^\'"]*\.jpg', overlay_filename, content)
index_file.write_text(content, encoding="utf-8")
print(f"✅ Updated index.html to load {overlay_filename}")

# Commit & Push Live
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"apply premium Playwright overlay template {overlay_filename} for {asin}"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("🚀 Successfully pushed premium template overlay live to GitHub Pages!")
