import sys
import io
import json
import time

# Ensure UTF-8 output encoding for Windows PowerShell/CMD
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from pathlib import Path
from config import NICHE, OUTPUT_DIR, BASE_BRIDGE_URL
from modules.amazon_finder import fetch_amazon_products
from modules.vision_prompt import generate_cozy_image_prompt
from modules.image_generator import generate_cozy_image, add_hook_text_overlay, create_multi_photo_reference_sheet
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

def run_pipeline():
    print("=" * 65)
    print(f"🚀 Starting Pinterest Automated Affiliate Pipeline")
    print(f"📌 Niche: {NICHE}")
    print(f"🌐 Base Bridge Web URL: {BASE_BRIDGE_URL}")
    print("=" * 65)

    # Step 1: Discover Live Amazon Products via SerpAPI
    products = fetch_amazon_products(query="aesthetic coffee mug warmer cozy desk", num_results=3)
    print(f"\n[Step 1] Retrieved {len(products)} Amazon products for processing.")

    results = []

    for idx, product in enumerate(products, 1):
        print(f"\n--- Processing Product {idx}/{len(products)}: {product['title']} ---")

        # Step 2: Create 3-in-1 Multi-Angle Reference Sheet & Vision Prompt
        print("\n📸 [Step 2] Creating 3-in-1 Multi-Angle Reference Sheet & Vision Prompt...")
        ref_sheet_path = ""
        photos = product.get("all_photos", []) or ([product.get("original_image_url")] if product.get("original_image_url") else [])
        if photos:
            ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{product['id']}")

        cozy_prompt = generate_cozy_image_prompt(
            product_title=product['title'],
            category=product['category'],
            key_features=product['features'],
            ref_sheet_path=ref_sheet_path
        )
        print(f" -> Generated Prompt: {cozy_prompt}")

        # Step 3: Generate Cozy AI Image (via Imagen 3 / Gemini)
        print("\n🖼️ [Step 3] Generating Vertical AI Image (Imagen 3)...")
        raw_image_path = generate_cozy_image(
            prompt=cozy_prompt,
            filename_prefix=f"product_{product['id']}"
        )

        # Step 4: SEO Title, Description & Hook Text Generator
        print("\n✍️ [Step 4] Writing Pinterest SEO Title & Description...")
        seo_data = generate_pin_seo_data(
            product_title=product['title'],
            price=product['price'],
            category=product['category']
        )
        print(f" -> Title: {seo_data['pin_title']}")
        print(f" -> Hook Text: {seo_data['image_hook']}")
        print(f" -> Description: {seo_data['description']}")

        # Step 5: Overlay Hook Text on Generated Image
        print("\n🎯 [Step 5] Overlaying Hook Text on Image...")
        final_image_path = add_hook_text_overlay(
            image_path=raw_image_path,
            hook_text=product['title'],
            subtitle=seo_data.get('subtitle_hook', ''),
            price_str=product.get('price', '$24.99'),
            style="glowing_neon"
        )



        # Step 6: Create Bridge Landing Page
        print("\n🌉 [Step 6] Creating Amazon <-> Pinterest Bridge Page...")
        bridge_page_path = generate_bridge_page(
            product=product,
            seo=seo_data,
            image_path=final_image_path
        )

        # Construct live web URL vs local file URL for Pinterest payload
        bridge_filename = Path(bridge_page_path).name
        image_filename = Path(final_image_path).name
        
        if BASE_BRIDGE_URL and "your-app.vercel.app" not in BASE_BRIDGE_URL:
            live_destination_url = f"{BASE_BRIDGE_URL.rstrip('/')}/bridge_pages/{bridge_filename}"
            live_image_url = f"{BASE_BRIDGE_URL.rstrip('/')}/images/{image_filename}"
        else:
            live_destination_url = f"file:///{bridge_page_path}"
            live_image_url = f"file:///{final_image_path}"

        # Step 7: Prepare / Publish to Pinterest
        print("\n📌 [Step 7] Preparing Pinterest Pin Payload...")
        pin_result = publish_pin_to_pinterest(
            image_path=final_image_path,
            title=seo_data['pin_title'],
            description=seo_data['description'],
            destination_url=live_destination_url,
            image_url=live_image_url,
            board_id=seo_data.get('suggested_board')
        )


        item_result = {
            "product_id": product['id'],
            "product_title": product['title'],
            "seo": seo_data,
            "final_image_path": final_image_path,
            "bridge_page_path": bridge_page_path,
            "pinterest_pin": pin_result
        }
        results.append(item_result)

    # Save summary report
    summary_path = OUTPUT_DIR / "campaign_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 65)
    print(f"🎉 Pipeline Execution Complete!")
    print(f"📁 Campaign Summary saved to: {summary_path}")
    print("=" * 65)

if __name__ == "__main__":
    run_pipeline()
