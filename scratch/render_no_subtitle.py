import sys
from pathlib import Path
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

# 1. Cute Bird Lamp (B0D8P8CSYP)
render_html_overlay(
    image_path="raw_images/birds_cute.jpg",
    headline="Cute Bird Touch Lamp",
    subtitle="",
    badge_text="CUTE ROOM FIND",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path="focus_product_B0D8P8CSYP_hook.jpg"
)

# 2. Bedside Touch Lamp (B0BZXNSW5K)
render_html_overlay(
    image_path="raw_images/raw_B0BZXNSW5K.jpg",
    headline="Bedside Touch Lamp",
    subtitle="",
    badge_text="VIRAL ROOM FIND",
    price_str="$19.99",
    features=["TOUCH DIMMABLE", "DUAL USB PORTS", "AC POWER OUTLET", "LED INCLUDED"],
    output_path="focus_product_B0BZXNSW5K_hook.jpg"
)

print("SUCCESS: Re-rendered default price-pill tags!")
