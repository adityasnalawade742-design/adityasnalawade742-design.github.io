import sys
import io
import json
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.automated_product_selector import get_next_automated_product, save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page

def main():
    print("🤖 === AUTOMATED PRODUCT SELECTION & PIPELINE RUNNER ===")
    
    # Step 1: Automatically select next product
    item = get_next_automated_product()
    if not item:
        print("✅ All queued viral products have been processed!")
        return

    asin = item["id"]
    amazon_url = item["url"]
    print(f"\n📦 Selected Product: {asin} - {item['title']}")

    # Step 2: Extract Amazon product details & HD photos
    print("\n🚀 [Step 1] Extracting Amazon details & listing photos...")
    prod = get_product_details_and_photos(amazon_url)
    if not prod:
        print("❌ Error extracting Amazon details. Aborting.")
        return

    # Ensure clean price string
    if not prod.get("price") or prod["price"] == "$14.99":
        prod["price"] = item["target_price"]

    print(f"🛍️ Title: {prod['title']}")
    print(f"💰 Price: {prod['price']} | ⭐ Rating: {prod['rating']}")
    photos = prod.get("all_photos", [])
    print(f"📸 Extracted {len(photos)} Amazon listing photos.")

    # Step 3: Create 6-photo multi-angle composite reference sheet
    print("\n📸 [Step 2] Creating Multi-Angle Composite Reference Sheet...")
    ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{asin}", max_photos=6)

    # Step 4: Generate Vision prompt
    print("\n👁️ [Step 3] Generating Vision Master Commercial Prompt...")
    cozy_prompt = generate_cozy_image_prompt(
        product_title=prod['title'],
        category=prod['category'],
        key_features=prod['features'],
        ref_sheet_path=ref_sheet_path
    )

    # Step 5: Replicate FLUX-Dev Img2Img Paid AI Render (Seed 591928, FP16 32-step)
    print("\n🖼️ [Step 4] Paid Replicate FLUX-Dev Img2Img Rendering Lifestyle Graphic...")
    init_photo = photos[0] if photos else ""
    raw_image_path = generate_cozy_image(
        prompt=cozy_prompt,
        filename_prefix=f"focus_product_{asin}",
        init_image_path=init_photo
    )

    # Save clean raw image (with NO text) for future daily automated price updates
    import shutil
    raw_images_dir = Path("G:/CLI/pinterest-auto-affiliate/raw_images")
    raw_images_dir.mkdir(parents=True, exist_ok=True)
    clean_raw_path = raw_images_dir / f"raw_{asin}.jpg"
    shutil.copy(raw_image_path, clean_raw_path)
    print(f" 💾 Saved clean raw image (no text) to: {clean_raw_path}")

    # Use item title if extractor returned generic fallback
    if prod['title'] == "Aesthetic Bedside Decor Find":
        prod['title'] = item['title']

    # Step 6: SEO Copywriter & Headlines
    print("\n✍️ [Step 5] Writing SEO Title & Viral Hook Headline...")
    seo_data = generate_pin_seo_data(
        product_title=prod['title'],
        price=prod['price'],
        category=prod['category']
    )
    
    headline = seo_data.get("image_hook") or "Cozy Room Find"
    print(f" -> Headline: '{headline}'")

    # Step 7: Playwright HTML/CSS Graphic Overlay (100% Product Clear + Glowing Price Tag)
    print("\n🎨 [Step 6] Playwright HTML/CSS Rendering Graphic Overlay...")
    hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{asin}_hook.jpg"
    render_html_overlay(
        image_path=str(clean_raw_path),
        headline=headline,
        subtitle="ELEGANCE THAT SHINES",
        badge_text="VIRAL ROOM FIND",
        price_str=prod['price'],
        output_path=hook_img_path
    )

    # Step 8: Generate Vogue-Style Mobile Bridge Page & Auto-Sync Homepage Grid
    print("\n🌐 [Step 7] Generating Luxury Bridge Page & Syncing Homepage Gallery...")
    generate_bridge_page(prod, seo_data, asin)

    # Register in Daily Price Sync Registry
    from daily_price_updater import load_registry, save_registry
    registry = load_registry()
    registry[asin] = {
        "title": prod['title'],
        "url": amazon_url,
        "current_price": prod['price'],
        "headline": headline,
        "subtitle": "ELEGANCE THAT SHINES",
        "badge": "✨ VIRAL ROOM FIND",
        "features": ["PREMIUM MATERIALS", "WARM AMBIENT GLOW", "STYLISH DECOR", "PERFECT GIFT"],
        "raw_image": f"raw_images/raw_{asin}.jpg",
        "hook_image": f"focus_product_{asin}_hook.jpg",
        "bridge_page": f"bridge_{asin}.html"
    }
    save_registry(registry)

    # Step 9: Save ASIN to processed history
    save_processed_asin(asin)
    print(f"\n🎉 SUCCESS! Automatically processed, registered & deployed product: {asin}")

if __name__ == "__main__":
    main()
