import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

# We use the EXACT restored user background image
target_img = "focus_product_B0D8P8CSYP_hook.jpg"

print(f"Applying matching Cute Bird Lamp text overlay onto the EXACT background image: {target_img}")

render_html_overlay(
    image_path=target_img,
    headline="Cute Bird Touch Lamp",
    subtitle="SOFT BEDSIDE NIGHT LIGHT",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path=target_img
)

print("Done stamping matching text overlay onto exact user image!")
