import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

clean_base_img = "raw_images/birds_cute.jpg"
output_img = "focus_product_B0D8P8CSYP_hook.jpg"

print(f"Rendering Extra Large Price Tag (450px x 337px) on clean base image: {clean_base_img}")

render_html_overlay(
    image_path=clean_base_img,
    headline="Cute Bird Touch Lamp",
    subtitle="",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path=output_img,
    tag_width_px=450,
    tag_height_px=337,
    tag_rotation_deg=-6
)

print("SUCCESS: Rendered Extra Large (450px x 337px) price tag graphic for B0D8P8CSYP!")
