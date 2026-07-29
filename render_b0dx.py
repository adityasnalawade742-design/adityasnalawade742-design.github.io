import shutil
from pathlib import Path
from modules.html_overlay_engine import render_html_overlay

clean_image = "G:/CLI/pinterest-auto-affiliate/generated image.jpg"
output_image = "G:/CLI/pinterest-auto-affiliate/focus_product_B0DXKGL1T2_hook.jpg"

# Render Playwright 3:4 Pinterest Overlay with exact price $36.38
render_html_overlay(
    image_path=clean_image,
    headline="Lily of the Valley Flower Lamp",
    subtitle="VINTAGE FLORAL GLOW",
    badge_text="✨ VIRAL ROOM FIND",
    price_str="$36.38",
    features=["3 COLOR MODES", "WARM BEDSIDE GLOW", "VINTAGE FLORAL DESIGN", "PERFECT GIFT IDEA"],
    output_path=output_image,
    theme="bottom_glass_card"
)

shutil.copy(output_image, "G:/CLI/pinterest-auto-affiliate/output/images/focus_product_B0DXKGL1T2_hook.jpg")
print("✅ Successfully rendered clean overlay onto generated image.jpg with exact price $36.38!")
