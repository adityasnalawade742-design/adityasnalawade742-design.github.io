from modules.html_overlay_engine import render_html_overlay
from modules.bridge_creator import generate_bridge_page
import json

asin = "B0BDRSG2BT"
raw_image_path = f"G:/CLI/pinterest-auto-affiliate/output/images/focus_product_{asin}.jpg"
hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"

print("[Fix Script] Fixing graphic overlay headline for Sunset Projection Light...")

# Correct Headline
render_html_overlay(
    image_path=raw_image_path,
    headline="Sunset Projection Light",
    subtitle="GOLDEN HOUR AMBIENCE",
    badge_text="VIRAL ROOM FIND",
    price_str="$16.99",
    output_path=hook_img_path
)

# Correct SEO Data & Bridge Page
prod_data = {
    "id": asin,
    "title": "Tsrarey Sunset Lamp Projection, 21 Colors Sunset Lights, Ambient Halo Projector",
    "category": "Ambient Lighting & Sunset Projection",
    "price": "$16.99",
    "rating": "4.4",
    "reviews_count": 840,
    "affiliate_url": f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21",
    "original_image_url": "https://m.media-amazon.com/images/I/71zjJtLCl5L._AC_SL1500_.jpg",
    "all_photos": ["https://m.media-amazon.com/images/I/71zjJtLCl5L._AC_SL1500_.jpg"],
    "features": "21 colors, 180-degree rotation, ambient golden hour projector light for bedroom decor."
}

seo_data = {
    "pin_title": "Golden Hour Sunset Projection Light for Room Decor",
    "image_hook": "Sunset Projection Light",
    "subtitle_hook": "GOLDEN HOUR AMBIENCE",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Transform your bedroom into a warm golden hour sanctuary with this 21-color sunset lamp projection light. Perfect ambient glow for cozy bedroom decor & aesthetic room photos.",
    "suggested_board": "Cozy Ambient Room Decor",
    "keywords": ["sunset lamp", "golden hour light", "room projector", "cozy ambient light", "bedroom decor"]
}

print("[Fix Script] Regenerating Vogue Bridge Page & updating Homepage card...")
generate_bridge_page(prod_data, seo_data, asin)

print("[Fix Script] SUCCESS! Corrected Sunset Lamp graphic & bridge page!")
