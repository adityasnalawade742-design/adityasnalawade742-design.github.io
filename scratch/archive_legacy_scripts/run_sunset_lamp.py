import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import NICHE, OUTPUT_DIR, BASE_BRIDGE_URL
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image, add_hook_text_overlay
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

def process_sunset_lamp():
    sunset_product = {
        "id": "B093S4S6XG",
        "title": "Aesthetic Sunset Projection Lamp for Room Decor & Ambient Vibe",
        "category": "Ambient Lighting & Lamps",
        "price": "$18.50",
        "rating": "4.8",
        "reviews_count": 1280,
        "affiliate_url": "https://www.amazon.com/dp/B093S4S6XG?tag=smartdeal0358-21",
        "original_image_url": "https://images.unsplash.com/photo-1540932239986-30128078f3c5?w=600",
        "features": "180 degree rotation sunset projection, warm golden orange sunset ambiance, perfect for cozy room photography backdrop."
    }



    print("=" * 65)
    print(f"🚀 Processing Unique Focus Product: Sunset Projection Lamp")
    print(f"📌 Niche: {NICHE}")
    print(f"🛍️ Target Product: {sunset_product['title']}")
    print(f"💰 Price: {sunset_product['price']} | ⭐ Rating: {sunset_product['rating']}")
    print("=" * 65)

    # Step 1: Vision Prompt Generator
    print("\n🎨 [Step 1] Generating Clean Vision Prompt for Sunset Lamp...")
    cozy_prompt = generate_cozy_image_prompt(
        product_title=sunset_product['title'],
        category=sunset_product['category'],
        key_features=sunset_product['features']
    )
    print(f" -> Generated Prompt: {cozy_prompt}")

    # Step 2: Generate Cozy Vertical AI Image
    print("\n🖼️ [Step 2] Generating Vertical 3:4 AI Image...")
    raw_image_path = generate_cozy_image(
        prompt=cozy_prompt,
        filename_prefix=f"focus_product_{sunset_product['id']}"
    )

    # Step 3: SEO Title & Description
    print("\n✍️ [Step 3] Writing Pinterest SEO Title & Description...")
    seo_data = generate_pin_seo_data(
        product_title=sunset_product['title'],
        price=sunset_product['price'],
        category=sunset_product['category']
    )
    print(f" -> Title: {seo_data['pin_title']}")
    print(f" -> Hook Text: {seo_data['image_hook']}")
    print(f" -> Description: {seo_data['description']}")

    # Step 4: Overlay Hook Text
    print("\n🎯 [Step 4] Overlaying Hook Text on Image...")
    final_image_path = add_hook_text_overlay(
        image_path=raw_image_path,
        hook_text=seo_data['image_hook']
    )

    # Step 5: Create Bridge Page
    print("\n🌉 [Step 5] Creating Amazon <-> Pinterest Bridge Landing Page...")
    bridge_page_path = generate_bridge_page(
        product=sunset_product,
        seo=seo_data,
        image_path=final_image_path
    )

    # Live destination URLs
    bridge_filename = Path(bridge_page_path).name
    image_filename = Path(final_image_path).name
    
    if BASE_BRIDGE_URL and "your-app.vercel.app" not in BASE_BRIDGE_URL:
        live_destination_url = f"{BASE_BRIDGE_URL.rstrip('/')}/bridge_pages/{bridge_filename}"
        live_image_url = f"{BASE_BRIDGE_URL.rstrip('/')}/images/{image_filename}"
    else:
        live_destination_url = f"file:///{bridge_page_path}"
        live_image_url = f"file:///{final_image_path}"

    # Step 6: Prepare Pinterest Payload
    print("\n📌 [Step 6] Preparing Pinterest Pin Payload...")
    pin_result = publish_pin_to_pinterest(
        image_path=final_image_path,
        title=seo_data['pin_title'],
        description=seo_data['description'],
        destination_url=live_destination_url,
        image_url=live_image_url,
        board_id=seo_data.get('suggested_board')
    )

    result = {
        "product": sunset_product,
        "seo": seo_data,
        "final_image_path": final_image_path,
        "bridge_page_path": bridge_page_path,
        "live_destination_url": live_destination_url,
        "pinterest_pin": pin_result
    }

    summary_path = OUTPUT_DIR / "sunset_lamp_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\n" + "=" * 65)
    print(f"🎉 Sunset Lamp Pipeline Execution Complete!")
    print(f"🖼️ Pin Graphic: {final_image_path}")
    print(f"🌐 Live Bridge Page: {live_destination_url}")
    print("=" * 65)
    return result

if __name__ == "__main__":
    process_sunset_lamp()
