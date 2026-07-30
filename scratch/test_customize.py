import json
from pathlib import Path
from modules.html_overlay_engine import render_html_overlay

try:
    asin = "B0D8P8CSYP"
    res = render_html_overlay(
        image_path="G:/CLI/pinterest-auto-affiliate/raw_images/birds_cute.jpg",
        headline="Cute Bird Touch Lamp",
        subtitle="",
        badge_text="VIRAL FIND",
        price_str="$20.56",
        output_path="G:/CLI/pinterest-auto-affiliate/focus_product_B0D8P8CSYP_hook.jpg",
        tag_width_px=380,
        tag_height_px=285,
        tag_rotation_deg=-6,
        tag_pos_x=45.0,
        tag_pos_y=60.0,
        tag_bg_hex="#fb8500",
        price_text_color="#111827",
        price_font_scale=0.38,
        price_text_offset_x=0,
        price_text_offset_y=15
    )
    print("SUCCESS:", res)
except Exception as e:
    import traceback
    traceback.print_exc()
