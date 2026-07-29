import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

clean_base_img = "raw_images/birds_cute.jpg"
output_img = "focus_product_B0D8P8CSYP_hook.jpg"

print(f"Reading CLEAN base image: {clean_base_img}")
print(f"Rendering high-res Playwright graphic overlay -> {output_img}")

render_html_overlay(
    image_path=clean_base_img,
    headline="Cute Bird Touch Lamp",
    subtitle="SOFT BEDSIDE NIGHT LIGHT",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path=output_img
)

print("SUCCESS: Rendered clean graphic from raw_images/birds_cute.jpg!")
