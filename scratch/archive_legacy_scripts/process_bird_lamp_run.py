import json
import sys
import io
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import OUTPUT_DIR, BASE_BRIDGE_URL
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image, add_hook_text_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page
from modules.pinterest_publisher import publish_pin_to_pinterest

amazon_url = "https://www.amazon.com/Control-Bird-Cordless-Dimmable-Rechargeable/dp/B0D8P8CSYP"
print("🚀 [Step 1] Extracting Product Details & Multi-Photos for ASIN B0D8P8CSYP...")

prod = get_product_details_and_photos(amazon_url)
if not prod:
    print("❌ Error: Could not extract product details from Amazon.")
    sys.exit(1)

print(f"🛍️ Title: {prod['title']}")
print(f"💰 Price: {prod['price']} | ⭐ Rating: {prod['rating']}")
photos = prod.get("all_photos", [])
print(f"📸 Found {len(photos)} Amazon listing photos.")

# Step 2: Create 6-photo multi-angle reference sheet
print("\n📸 [Step 2] Creating Multi-Angle Composite Reference Sheet...")
ref_sheet_path = create_multi_photo_reference_sheet(photos, filename_prefix=f"product_{prod['id']}", max_photos=6)
print(f" -> Multi-Angle Reference Sheet: {ref_sheet_path}")

# Step 3: Gemini Vision Prompt
print("\n👁️ [Step 3] Gemini Vision Inspecting Multi-Angle Reference Sheet...")
cozy_prompt = generate_cozy_image_prompt(
    product_title=prod['title'],
    category=prod['category'],
    key_features=prod['features'],
    ref_sheet_path=ref_sheet_path
)
print(f" -> Generated Vision Prompt: {cozy_prompt}")

# Step 4: Replicate FLUX Img2Img & Depth Control Product Render
print("\n🖼️ [Step 4] Paid Replicate FLUX Img2Img & Depth Control Rendering 8K 3:4 Lifestyle Room Graphic...")
init_photo = "pinterest reference user/amazon.jpg" if Path("pinterest reference user/amazon.jpg").exists() else (photos[0] if photos else "")
raw_image_path = generate_cozy_image(
    prompt=cozy_prompt,
    filename_prefix=f"focus_product_{prod['id']}",
    init_image_path=init_photo
)
print(f" -> FLUX Product Control Render: {raw_image_path}")

# Step 5: SEO Data Generator
print("\n✍️ [Step 5] Writing Pinterest SEO Title & Description...")
seo_data = generate_pin_seo_data(
    product_title=prod['title'],
    price=prod['price'],
    category=prod['category']
)
print(f" -> SEO Title: {seo_data['pin_title']}")
print(f" -> Image Hook: {seo_data['image_hook']}")

# Step 6: Ultra-Aesthetic Typography Overlay
print("\n✨ [Step 6] Overlaying Ultra-Aesthetic Backlit Typography (matching reference pin)...")
final_image_path = add_hook_text_overlay(
    image_path=raw_image_path,
    hook_text=seo_data['image_hook'],
    subtitle=seo_data.get('subtitle_hook', 'CORDLESS BEDSIDE LIGHT'),
    badge_text=seo_data.get('badge_hook', 'AMAZON TOP FIND'),
    price_str=prod['price'],
    style="glowing_neon"
)
print(f" -> Final Pin Graphic: {final_image_path}")

# Step 7: Mobile Bridge Landing Page
print("\n🌉 [Step 7] Generating Amazon <-> Pinterest Mobile Bridge Landing Page...")
bridge_page_path = generate_bridge_page(
    product=prod,
    seo=seo_data,
    image_path=final_image_path
)
print(f" -> Saved Bridge Page: {bridge_page_path}")

bridge_filename = Path(bridge_page_path).name
image_filename = Path(final_image_path).name
live_destination_url = f"{BASE_BRIDGE_URL.rstrip('/')}/bridge_pages/{bridge_filename}"
live_image_url = f"{BASE_BRIDGE_URL.rstrip('/')}/images/{image_filename}"

# Step 8: Pinterest Pin Payload
print("\n📌 [Step 8] Preparing Pinterest Pin Payload...")
pin_result = publish_pin_to_pinterest(
    image_path=final_image_path,
    title=seo_data['pin_title'],
    description=seo_data['description'],
    destination_url=live_destination_url,
    image_url=live_image_url,
    board_id=seo_data.get('suggested_board')
)

result = {
    "product": prod,
    "seo": seo_data,
    "ref_sheet_path": ref_sheet_path,
    "final_image_path": final_image_path,
    "bridge_page_path": bridge_page_path,
    "live_destination_url": live_destination_url,
    "pinterest_pin": pin_result
}

summary_path = OUTPUT_DIR / "bird_lamp_B0D8P8CSYP_summary.json"
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("\n" + "=" * 65)
print("🎉 CAMPAIGN PROCESSING COMPLETE FOR B0D8P8CSYP!")
print(f"📸 Reference Sheet: {ref_sheet_path}")
print(f"🖼️ Pin Graphic: {final_image_path}")
print(f"🌐 Live Bridge Landing Page: {live_destination_url}")
print("=" * 65)
