import os
import sys
import io
import time
import shutil
import requests
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from config import REPLICATE_API_TOKEN, OUTPUT_DIR, BASE_BRIDGE_URL
from modules.image_generator import add_hook_text_overlay
import replicate

asin = "B0DXKGL1T2"
amazon_photo_url = "https://m.media-amazon.com/images/I/71HlC2o1fmL._AC_SL1500_.jpg"

user_prompt = """Transform this ordinary ecommerce product photo into a premium luxury commercial advertisement.

Keep the product 100% identical to the reference image.

Do not alter the design.

Create a realistic environment that naturally fits the product.

Use expensive-looking interior styling, designer furniture, premium props, warm cinematic lighting, volumetric light, soft shadows, realistic reflections, tasteful composition, shallow depth of field, luxury lifestyle aesthetic, Apple-style product photography, Muji minimalism, Scandinavian interior design, high-end magazine quality.

Make it look like a professional product campaign photographed by an advertising agency.

Leave empty space for headline, logo and price.

Ultra realistic, photorealistic, 8K, HDR, commercial photography."""

print(f"🚀 Running Luxury Commercial Prompt on FLUX-Dev Img2Img for {asin} (Async 1 API Call)...")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

print(f"[1 API Call] Invoking black-forest-labs/flux-dev async prediction...")

pred = client.predictions.create(
    model="black-forest-labs/flux-dev",
    input={
        "prompt": user_prompt,
        "image": amazon_photo_url,
        "prompt_strength": 0.65,
        "aspect_ratio": "3:4",
        "output_format": "jpg",
        "output_quality": 98
    }
)

print(f"  ✓ Prediction Created (ID: {pred.id}). Waiting for completion...")
pred.wait()
print(f"  ✓ Prediction Status: {pred.status}")

if pred.output:
    img_url = pred.output[0] if isinstance(pred.output, list) else str(pred.output)
    print(f" -> Replicate Output URL: {img_url}")

    res_out = requests.get(img_url, timeout=35)
    raw_path = OUTPUT_DIR / "images" / f"focus_product_{asin}.jpg"
    with open(raw_path, "wb") as f:
        f.write(res_out.content)

    print(f" -> Saved Raw Luxury Render: {raw_path}")

    # Overlay aesthetic text
    final_path = add_hook_text_overlay(
        image_path=str(raw_path),
        hook_text="Lily Of The Valley Lamp",
        subtitle="VINTAGE AMBIANCE",
        badge_text="MUST-HAVE FIND",
        price_str="£36.38",
        style="glowing_neon"
    )
    print(f" -> Final Overlaid Graphic: {final_path}")

    # Sync to root
    shutil.copy(final_path, f"focus_product_{asin}_hook.jpg")
    shutil.copy(str(OUTPUT_DIR / "bridge_pages" / f"bridge_{asin}.html"), f"bridge_{asin}.html")

    print("\n" + "=" * 65)
    print(f"🎉 LUXURY COMMERCIAL CAMPAIGN RENDER COMPLETE FOR {asin}!")
    print(f"🖼️ Pin Graphic: {final_path}")
    print(f"🌐 Live Bridge Page: {BASE_BRIDGE_URL.rstrip('/')}/bridge_{asin}.html")
    print("=" * 65)
else:
    print(f"❌ Error: Prediction failed with status {pred.status} - {pred.error}")
