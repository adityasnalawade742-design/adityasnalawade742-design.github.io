import sys, io
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from modules.amazon_extractor import get_product_details_and_photos, select_clean_photo_or_skip, is_lifestyle_photo

new_asins = [
    "B08N5N4C74",  # Flame Essential Oil Diffuser
    "B08HGVDBX3",  # Sunset Lamp Projection Light
    "B09FLK9F5V",  # Ceramic Book Vase for Flowers
    "B07T43J94V",  # Macrame Hanging Wall Decor
    "B09W2J3R9B"   # Minimalist Ceramic Candle Holder
]

print("🔍 RUNNING TEXT DETECTION ON 5 BRAND NEW CANDIDATE PRODUCTS...\n")

for asin in new_asins:
    print(f"==================================================")
    print(f"📦 ASIN: {asin}")
    prod = get_product_details_and_photos(f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21")
    if not prod:
        print(f"❌ Could not extract details for ASIN {asin}")
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
