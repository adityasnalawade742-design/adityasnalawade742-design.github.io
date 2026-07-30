import sys, io
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.amazon_extractor import get_product_details_and_photos, select_clean_photo_or_skip, is_lifestyle_photo

test_asins = [
    "B0C2YLN3H4",  # White Ceramic Donut Vase
    "B0GT5GWK4B",  # Candle Warmer Lamp
    "B0FXLYXM32",  # Wavy Wall Mirror
    "B0D4537YMT",  # Ribbed Ceramic Vase
    "B07HP22QTZ"   # Crystal Suncatcher
]

print("🔍 RUNNING TEXT DETECTION SUITE ACROSS CANDIDATE PRODUCTS...\n")

for asin in test_asins:
    print(f"==================================================")
    print(f"📦 ASIN: {asin}")
    prod = get_product_details_and_photos(f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21")
    if not prod:
        print("❌ Could not extract details")
        continue
    
    title = prod['title'][:55]
    photos = prod.get("all_photos", [])
    print(f"Title: '{title}...' ({len(photos)} photos extracted)\n")
    
    clean_photo, should_skip = select_clean_photo_or_skip(photos)
    if should_skip:
        print(f"🛑 FINAL DECISION: ⚠️ SKIPPED product {asin} because ALL photos contain text overlays.")
    else:
        is_lifestyle = is_lifestyle_photo(clean_photo)
        bg_type = "✅ Room Lifestyle Background (Prompt 1)" if is_lifestyle else "❌ Plain White Studio Cutout (Prompt 2)"
        print(f"✅ FINAL DECISION: PASSED text-free policy!")
        print(f"   Selected Clean Photo: {clean_photo}")
        print(f"   Photo Type: {bg_type}")
    print("\n")
