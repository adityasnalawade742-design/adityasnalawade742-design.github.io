import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

clean_raw = "raw_B0D8P8CSYP_console.jpg"
output_img = "focus_product_B0D8P8CSYP_hook.jpg"

print(f"Rendering clean single text layer on un-overlayed raw photo: {clean_raw} -> {output_img}")

render_html_overlay(
    image_path=clean_raw,
    headline="Cute Bird Touch Lamp",
    subtitle="SOFT BEDSIDE NIGHT LIGHT",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path=output_img
)

print("Single text layer render complete!")
