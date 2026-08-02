import sys
sys.path.insert(0, '.')
from modules.amazon_finder import fetch_amazon_products

print("End-to-end test with Amazon engine...\n")
items = fetch_amazon_products(query="candle warmer lamp timer", num_results=5)
print(f"\nResults: {len(items)} products\n")
ok = 0
missing = 0
for it in items:
    asin = it.get("id", "")
    img  = it.get("original_image_url", "") or it.get("thumbnail", "")
    status = "✅ HAS IMAGE" if img and img.startswith("http") else "❌ NO IMAGE"
    if img and img.startswith("http"):
        ok += 1
    else:
        missing += 1
    print(f"  {status} | {asin} | {it.get('title','')[:45]}")
    if img:
        print(f"           {img[:75]}")
    print()

print(f"Summary: {ok}/{len(items)} have images, {missing} missing")
