
import sys
from modules.automated_product_selector import save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page

asin = "B0BZXNSW5K"
prod = {
    'title': "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet | 3-Way Dimmable, LED Bulb Included, Fabric Lampshade, Wood-Grain Metal Base, 14\" Small Nightstand Lamp for Desk, Living Room",
    'price': "$19.99",
    'rating': "4.5",
    'features': ["PREMIUM QUALITY", "WARM AMBIENT GLOW", "EASY ASSEMBLY"]
}

ref_sheet_path = create_multi_photo_reference_sheet(["https://m.media-amazon.com/images/I/71zreHoOzVL._AC_SL1500_.jpg"], filename_prefix=f"product_{asin}", max_photos=1)
cozy_prompt = generate_cozy_image_prompt(prod['title'], "Room Lighting", prod['features'], ref_sheet_path, is_white_background=False)
raw_image_path = generate_cozy_image(prompt=cozy_prompt, filename_prefix=f"focus_product_{asin}", init_image_path="https://m.media-amazon.com/images/I/71zreHoOzVL._AC_SL1500_.jpg", prompt_strength=0.45)

seo_data = {
    "pin_title": prod['title'],
    "image_hook": prod['title'][:30],
    "subtitle_hook": "",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Transform your space with this viral room upgrade find.",
    "suggested_board": "Cozy Room Decor",
    "keywords": ["room decor", "lighting"]
}

hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
render_html_overlay(raw_image_path, seo_data['image_hook'], "", seo_data['badge_hook'], prod['price'], hook_img_path)
generate_bridge_page(prod, seo_data, asin)
save_processed_asin(asin)

import subprocess
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"publish {asin} from Web Console"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("SUCCESS")
