"""Simulate exactly what the server's handle_api_discover does and print the thumbnail values."""
import sys, json
sys.path.insert(0, '.')

from modules.amazon_finder import fetch_amazon_products
from modules.automated_product_selector import is_asin_published_on_homepage
from pathlib import Path

raw_dir = Path("raw_images")
raw_dir.mkdir(exist_ok=True)

query = "aesthetic mushroom lamp"
print(f"Simulating /api/discover?query={query}\n")
raw_items = fetch_amazon_products(query=query, num_results=5)

print(f"\nRaw items from fetch_amazon_products: {len(raw_items)}\n")
for item in raw_items:
    asin = item.get('id') or item.get('asin', '')
    candidate_url = (
        item.get('original_image_url') or
        item.get('thumbnail') or
        item.get('image') or
        ''
    )
    bad = (
        not candidate_url
        or 'amazon-adsystem.com' in candidate_url
        or 'ws-na.amazon-adsystem' in candidate_url
        or '_SP100' in candidate_url
        or '_SP200' in candidate_url
    )
    print(f"  ASIN    : {asin}")
    print(f"  title   : {item.get('title','')[:50]}")
    print(f"  original_image_url : {item.get('original_image_url','EMPTY')[:70]}")
    print(f"  thumbnail field    : {item.get('thumbnail','EMPTY')[:70]}")
    print(f"  candidate_url      : {candidate_url[:70] if candidate_url else 'EMPTY'}")
    print(f"  bad url?           : {bad}")
    print(f"  -> thumbnail sent to browser: {candidate_url[:70] if not bad else 'WILL SCRAPE'}")
    print()
