import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

from modules.html_overlay_engine import render_html_overlay

raw_path = repo_dir / "raw_images" / "raw_B0D8P8CSYP.jpg"
output_path = repo_dir / "focus_product_B0D8P8CSYP_hook.jpg"

registry_file = repo_dir / "product_price_registry.json"
usd_price = "$18.99"
if registry_file.exists():
    with open(registry_file, "r", encoding="utf-8") as f:
        reg = json.load(f)
        usd_price = reg.get("B0D8P8CSYP", {}).get("current_price") or reg.get("B0D8P8CSYP", {}).get("regional_prices", {}).get("US", "$18.99")

print("==================================================")
print(f"🐦 RE-RENDERING GRAPHIC PIN FOR CUTE BIRD LAMP [{raw_path.name}]")
print(f"   • Raw Image Path: {raw_path}")
print(f"   • USD Price:      {usd_price}")
print(f"   • Output Pin:     {output_path.name}")
print("==================================================")

render_html_overlay(
    image_path=str(raw_path),
    headline="Cute Bird Touch Dimmable Night Lamp",
    subtitle="",
    badge_text="🐦 CUTE BEDSIDE PICK",
    price_str=usd_price,
    output_path=str(output_path),
    theme="bottom_glass_card"
)

print("\n✅ Graphic pin for Cute Bird Lamp re-rendered successfully!")
