import sys
sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.html_overlay_engine import render_html_overlay

# Re-render B0BZXNSW5K pin graphic
img_b0b = "raw_images/raw_B0BZXNSW5K.jpg"
if not __import__("pathlib").Path(img_b0b).exists():
    img_b0b = "focus_product_B0BZXNSW5K_hook.jpg"

render_html_overlay(
    image_path=img_b0b,
    headline="Bedside Touch Lamp",
    subtitle="DUAL USB A+C CHARGING",
    badge_text="VIRAL ROOM FIND",
    price_str="$19.99",
    features=["TOUCH DIMMABLE", "DUAL USB PORTS", "AC POWER OUTLET", "LED INCLUDED"],
    output_path="focus_product_B0BZXNSW5K_hook.jpg"
)

# Re-render B0D8P8CSYP pin graphic
img_bird = "raw_images/raw_B0D8P8CSYP.jpg"
if not __import__("pathlib").Path(img_bird).exists():
    img_bird = "focus_product_B0D8P8CSYP_hook.jpg"

render_html_overlay(
    image_path=img_bird,
    headline="Cute Bird Touch Lamp",
    subtitle="SOFT NIGHTSTAND LIGHT",
    badge_text="MUST HAVE DECOR",
    price_str="$20.56",
    features=["TOUCH DIMMING", "RECHARGEABLE", "WOODGRAIN BASE", "PORTABLE LIGHT"],
    output_path="focus_product_B0D8P8CSYP_hook.jpg"
)

print("Successfully re-rendered high-res 1200x1600 Pinterest pin graphics!")
