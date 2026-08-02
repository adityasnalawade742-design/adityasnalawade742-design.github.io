import sys, json, requests
sys.path.insert(0, '.')
from modules.amazon_finder import fetch_amazon_products

print("Testing product discovery for mushroom lamp...")
items = fetch_amazon_products(query="aesthetic glass mushroom table lamp", num_results=3)
print(f"\nGot {len(items)} items:\n")

for it in items:
    asin = it.get("id", "")
    img  = it.get("original_image_url", "")
    thumb = it.get("thumbnail", "")
    print(f"  ASIN : {asin}")
    print(f"  Title: {it.get('title','')[:55]}")
    print(f"  original_image_url : {img[:80] if img else 'EMPTY'}")
    print(f"  thumbnail          : {thumb[:80] if thumb else 'EMPTY'}")

    # Check if the URL actually loads
    if img and img.startswith("http"):
        try:
            r = requests.head(img, headers={"User-Agent": "Mozilla/5.0"}, timeout=5, allow_redirects=True)
            size = r.headers.get("Content-Length", "?")
            print(f"  HTTP HEAD status   : {r.status_code} | Content-Length: {size}")
        except Exception as e:
            print(f"  HTTP HEAD error    : {e}")
    else:
        print(f"  -> NO VALID URL to load!")
    print()
