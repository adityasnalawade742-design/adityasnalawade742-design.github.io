import sys
import json
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from modules.html_overlay_engine import render_html_overlay

# Fix price in registry
reg_path = repo_dir / "product_price_registry.json"
reg = json.load(open(reg_path, encoding="utf-8"))
reg["B07HP22QTZ"]["current_price"] = "$14.99"
if "regional_prices" in reg["B07HP22QTZ"]:
    reg["B07HP22QTZ"]["regional_prices"]["US"] = "$14.99"

with open(reg_path, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2)

print("✅ Fixed B07HP22QTZ price to $14.99 in product_price_registry.json")

# Re-render overlay badge for B07HP22QTZ
clean_img = repo_dir / "flux_clean_images" / "clean_focus_product_B07HP22QTZ.jpg"
output_path = repo_dir / "focus_product_B07HP22QTZ_hook.jpg"

render_html_overlay(
    image_path=str(clean_img),
    headline="Hanging Crystal Suncatcher Prism",
    subtitle="COZY HOME & LUXURY ROOM FIND",
    badge_text="✨ VIRAL ROOM FIND",
    price_str="$14.99",
    features=["CRYSTAL PRISM CLUSTER", "RAINBOW LIGHT REFLECTION", "WINDOW SUNCATCHER"],
    output_path=str(output_path),
    theme="bottom_glass_card"
)

out_img = repo_dir / "output" / "images" / "focus_product_B07HP22QTZ_hook.jpg"
shutil.copy(output_path, out_img)
print(f"✅ Saved updated price badge with $14.99: {output_path.name}")
