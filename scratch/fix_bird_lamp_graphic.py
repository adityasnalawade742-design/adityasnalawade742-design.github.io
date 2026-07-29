import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

# Check raw image source for Cute Bird Lamp
raw_src = "raw_B0D8P8CSYP_console.jpg"
if not Path(raw_src).exists():
    raw_src = "raw_images/raw_B0D8P8CSYP.jpg"

output_img = "focus_product_B0D8P8CSYP_hook.jpg"

print(f"Rendering clean graphic overlay on raw image: {raw_src} -> {output_img}")

render_html_overlay(
    image_path=raw_src,
    headline="Cute Bird Touch Lamp",
    subtitle="SOFT BEDSIDE NIGHT LIGHT",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "WARM SOFT GLOW"],
    output_path=output_img
)

print("✅ Cute Bird Lamp graphic successfully fixed with exact matching title & text!")
