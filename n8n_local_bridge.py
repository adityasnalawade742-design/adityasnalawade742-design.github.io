"""
n8n Local Bridge HTTP Endpoint / CLI Wrapper
Exposes an n8n-compatible interface for triggering the Pinterest Auto Affiliate Pipeline.
"""
import sys
import io
import json
import argparse
from pathlib import Path

# UTF-8 encoding fix
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.amazon_extractor import get_product_details_and_photos
from modules.automated_product_selector import get_next_automated_product, save_processed_asin
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

def run_n8n_triggered_pipeline(asin=None, amazon_url=None):
    print("🤖 === N8N TRIGGERED PINTEREST AFFILIATE PIPELINE ===")
    
    if asin and not amazon_url:
        amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"
    
    if not amazon_url:
        item = get_next_automated_product()
        if not item:
            print(json.dumps({"status": "error", "message": "No un-processed products in queue"}))
            return
        asin = item["id"]
        amazon_url = item["url"]

    print(f"📦 Target Product ASIN: {asin}")
    print(f"🔗 Amazon Link: {amazon_url}")

    # Extract Amazon Data
    prod = get_product_details_and_photos(amazon_url)
    if not prod:
        print(json.dumps({"status": "error", "message": f"Could not extract details for ASIN {asin}"}))
        return

    photos = prod.get("all_photos", [])
    ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{asin}", max_photos=6)

    # Prompt & AI Image
    cozy_prompt = generate_cozy_image_prompt(
        product_title=prod['title'],
        category=prod['category'],
        key_features=prod['features'],
        ref_sheet_path=ref_sheet_path
    )
    
    init_photo = photos[0] if photos else ""
    raw_image_path = generate_cozy_image(
        prompt=cozy_prompt,
        filename_prefix=f"focus_product_{asin}",
        init_image_path=init_photo
    )

    # SEO Copywriting
    seo_data = generate_pin_seo_data(
        product_title=prod['title'],
        price=prod['price'],
        category=prod['category']
    )
    headline = seo_data.get("image_hook") or "Cozy Room Find"

    # Playwright Overlay with Dynamic Vibe & Theme Matching
    hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
    render_html_overlay(
        image_path=raw_image_path,
        headline=headline,
        subtitle=seo_data.get("subtitle_hook") or "ELEVATE YOUR VANITY SPACE",
        badge_text=seo_data.get("badge_hook") or "VANITY GOALS",
        price_str=prod['price'],
        output_path=hook_img_path,
        theme=seo_data.get("theme_style") or "floating_cream"
    )

    # Bridge Page Generation
    generate_bridge_page(prod, seo_data, asin)

    # Pinterest Pin Payload Output
    bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
    image_url = f"https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg"
    
    pin_result = publish_pin_to_pinterest(
        image_path=hook_img_path,
        title=seo_data['pin_title'],
        description=seo_data['description'],
        destination_url=bridge_url,
        image_url=image_url
    )

    save_processed_asin(asin)

    n8n_output = {
        "status": "success",
        "asin": asin,
        "product_title": prod['title'],
        "price": prod['price'],
        "pin_title": seo_data['pin_title'],
        "pin_description": seo_data['description'],
        "bridge_url": bridge_url,
        "image_url": image_url,
        "pinterest_api_result": pin_result
    }
    
    # Print JSON output for n8n to capture
    print(json.dumps(n8n_output, indent=2))
    return n8n_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="n8n Local Bridge for Pinterest Auto Affiliate")
    parser.add_argument("--asin", help="Amazon ASIN code")
    parser.add_argument("--url", help="Amazon product URL")
    args = parser.parse_args()
    
    run_n8n_triggered_pipeline(asin=args.asin, amazon_url=args.url)
