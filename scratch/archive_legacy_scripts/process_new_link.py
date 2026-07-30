import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import NICHE, OUTPUT_DIR, BASE_BRIDGE_URL, AMAZON_ASSOCIATE_TAG
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import generate_cozy_image, add_hook_text_overlay
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

def process_selected_product_campaign():
    target_url = "https://www.amazon.com/dp/B0CCP46DK9"
    
    print("=" * 65)
    print(f"🚀 Processing Product: Wood Grain Coffee Mug & Candle Warmer")
    print(f"📌 Niche: {NICHE}")
    print(f"🛍️ Link: {target_url}")
    print("=" * 65)

    # Step 1: Extract Amazon Product Data & Photo Suite
    print("\n🔍 [Step 1] Extracting Product Data & 7 High-Res Photos...")
    product = get_product_details_and_photos(target_url)
    tag = AMAZON_ASSOCIATE_TAG
    product['affiliate_url'] = f"https://www.amazon.com/House-Gem-Mug-Warmer-Temperature/dp/B0CCP46DK9?tag={tag}"

    print(f" -> ASIN: {product['id']}")
    print(f" -> Title: {product['title']}")
    print(f" -> Price: {product['price']} | Rating: {product['rating']}")
    print(f" -> Master Reference Image: {product['original_image_url']}")

    # Step 2: Vision Prompt Generator
    print("\n🎨 [Step 2] Generating Vision Prompt for Wood Grain Mug Warmer...")
    cozy_prompt = f"A commercial 8k photograph of this exact wood grain coffee mug warmer heating pad and ceramic mug on an oak desk inside a cozy dimly lit aesthetic bedroom workspace at dusk, warm soft ambient glow, 35mm film photography, crisp focus, studio interior design"
    print(f" -> Prompt: {cozy_prompt}")

    # Step 3: Generate Commercial AI Image via Multi-Photo Reference Conditioning / ControlNet
    print("\n🖼️ [Step 3] Generating Graphic via Multi-Photo Reference Conditioning / ControlNet (FLUX-Dev)...")
    raw_image_path = generate_cozy_image(
        prompt=cozy_prompt,
        filename_prefix=f"focus_product_{product['id']}",
        real_image_url=product['original_image_url'],
        multi_reference_photos=product.get('all_photos', [])
    )

    # Step 4: SEO Copywriting
    print("\n✍️ [Step 4] Writing Pinterest SEO Copy...")
    seo_data = generate_pin_seo_data(
        product_title=product['title'],
        price=product['price'],
        category=product['category']
    )

    # Step 5: Overlay Typography & Glassmorphism Card
    print("\n🎯 [Step 5] Overlaying Playfair Bold Typography & Gold Pill Badges...")
    final_image_path = add_hook_text_overlay(
        image_path=raw_image_path,
        hook_text="Smart Wood Grain Mug Warmer ☕"
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

    summary_path = OUTPUT_DIR / "wood_warmer_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("\n" + "=" * 65)
    print(f"🎉 Wood Grain Mug Warmer Campaign Complete!")
    print(f"🖼️ Pin Graphic: {final_image_path}")
    print(f"🌐 Live Bridge Page: {live_destination_url}")
    print("=" * 65)
    return result

if __name__ == "__main__":
    process_selected_product_campaign()
