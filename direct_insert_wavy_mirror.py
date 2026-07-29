import json
import shutil
import requests
from pathlib import Path
from modules.html_overlay_engine import render_html_overlay

project_root = Path("G:/CLI/pinterest-auto-affiliate")
raw_dir = project_root / "raw_images"
raw_dir.mkdir(exist_ok=True)

asin = "B0FXLYXM32"
winner_photo_url = "https://m.media-amazon.com/images/I/81A-bdsnQtL._AC_SL1500_.jpg"

registry_file = project_root / "product_price_registry.json"
with open(registry_file, "r", encoding="utf-8") as f:
    reg = json.load(f)

pdata = reg[asin]
print("Directly downloading winner photo...")

# 1. Direct photo download (Zero AI modifications)
res = requests.get(winner_photo_url, timeout=30)
raw_target = raw_dir / f"raw_{asin}.jpg"
raw_target.write_bytes(res.content)
reg[asin]["raw_image"] = f"raw_images/raw_{asin}.jpg"
print(f"Saved exact winner photo to {raw_target.name}")

# 2. Render Playwright text template overlay directly onto exact winner photo
hook_path = project_root / f"focus_product_{asin}_hook.jpg"
render_html_overlay(
    image_path=str(raw_target),
    headline=pdata["headline"],
    subtitle=pdata["subtitle"],
    badge_text=pdata["badge"],
    price_str=pdata["current_price"],
    features=pdata["features"],
    output_path=str(hook_path),
    theme="bottom_glass_card"
)
shutil.copy(hook_path, project_root / "output" / "images" / hook_path.name)
print(f"Rendered Playwright text template overlay to {hook_path.name}")

# 3. Save registry
with open(registry_file, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2)

print("Direct insertion complete!")
