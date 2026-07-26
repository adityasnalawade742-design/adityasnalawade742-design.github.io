import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import NICHE, OUTPUT_DIR, BASE_BRIDGE_URL, AMAZON_ASSOCIATE_TAG
from modules.amazon_extractor import get_product_details_and_photos
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image, add_hook_text_overlay
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

def process_ceramic_vase_campaign():
    target_url = "https://www.amazon.com/Ceramic-Vases-Decor-Modern-Farmhouse/dp/B0BKSV8176?tag=smartdeal0358-21"
    
    print("=" * 65)
    print(f"🚀 Processing Live Home Decor Product: Ceramic Mushroom Vase")
    print(f"📌 Niche: {NICHE}")
    print(f"🛍️ Link: {target_url}")
    print("=" * 65)

    # Step 1: Extract Amazon Product & Photo Suite
    print("\n🔍 [Step 1] Extracting Product Data & 1500px Photo Suite...")
    product = get_product_details_and_photos(target_url)
    if not product:
        tag = AMAZON_ASSOCIATE_TAG
        product = {
            "id": "B0BKSV8176",
            "title": "Aesthetic Ceramic Flower Vase for Modern Farmhouse Home Decor",
            "category": "Home Decor & Vases",
            "price": "$21.99",
            "rating": "4.8",
            "reviews_count": 1840,
            "affiliate_url": f"https://www.amazon.com/Ceramic-Vases-Decor-Modern-Farmhouse/dp/B0BKSV8176?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/712yfgNo9nL._AC_SL1500_.jpg",
            "features": "Handcrafted ribbed ceramic texture, aesthetic off-white finish, perfect for neutral living room shelves and dining table centerpieces."
        }

    print(f" -> ASIN: {product['id']}")
    print(f" -> Title: {product['title']}")
    print(f" -> Price: {product['price']} | Rating: {product['rating']}")

    # Step 2: Vision Prompt Generator
    print("\n🎨 [Step 2] Generating Vision Prompt for Ceramic Vase...")
    cozy_prompt = generate_cozy_image_prompt(
        product_title=product['title'],
        category=product['category'],
        key_features=product['features']
    )
    print(f" -> Prompt: {cozy_prompt}")

    # Step 3: Generate AI Vertical 3:4 Image via Replicate FLUX-Dev
    print("\n🖼️ [Step 3] Generating Commercial AI Image via Replicate FLUX-Dev...")
    raw_image_path = generate_cozy_image(
        prompt=cozy_prompt,
        filename_prefix=f"focus_product_{product['id']}"
    )

    # Step 4: SEO Title & Description
    print("\n✍️ [Step 4] Writing Pinterest SEO Copy...")
    seo_data = generate_pin_seo_data(
        product_title=product['title'],
        price=product['price'],
        category=product['category']
    )
    print(f" -> Title: {seo_data['pin_title']}")
    print(f" -> Hook Text: {seo_data['image_hook']}")

    # Step 5: Overlay Hook Text
    print("\n🎯 [Step 5] Overlaying Typography & Frosted Glass Card...")
    final_image_path = add_hook_text_overlay(
        image_path=raw_image_path,
        hook_text=seo_data['image_hook']
    )

    # Step 6: Create Bridge Landing Page
    print("\n🌉 [Step 6] Creating Amazon <-> Pinterest Bridge Page...")
    bridge_page_path = generate_bridge_page(
        product=product,
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

    # Step 7: Prepare Pinterest Payload
    print("\n📌 [Step 7] Preparing Pinterest Pin Payload...")
    pin_result = publish_pin_to_pinterest(
        image_path=final_image_path,
        title=seo_data['pin_title'],
        description=seo_data['description'],
        destination_url=live_destination_url,
        image_url=live_image_url,
        board_id=seo_data.get('suggested_board')
    )

    result = {
        "product": product,
        "seo": seo_data,
        "final_image_path": final_image_path,
        "bridge_page_path": bridge_page_path,
        "live_destination_url": live_destination_url,
        "pinterest_pin": pin_result
    }

    summary_path = OUTPUT_DIR / "ceramic_vase_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\n" + "=" * 65)
    print(f"🎉 Ceramic Vase Campaign Execution Complete!")
    print(f"🖼️ Pin Graphic: {final_image_path}")
    print(f"🌐 Live Bridge Page: {live_destination_url}")
    print("=" * 65)
    return result

if __name__ == "__main__":
    process_ceramic_vase_campaign()
