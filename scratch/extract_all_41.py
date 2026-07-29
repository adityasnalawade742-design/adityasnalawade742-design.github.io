import sys
import json
import time
import requests
from pathlib import Path

sys.path.append("G:/CLI/pinterest-auto-affiliate")

from modules.amazon_extractor import get_product_details_and_photos

links_file = Path("amazon_products_links.txt")
lines = [l.strip() for l in links_file.read_text(encoding="utf-8").splitlines() if l.strip()]

from modules.amazon_extractor import extract_asin_from_url

asins = []
for url in lines:
    a = extract_asin_from_url(url)
    if a and a not in asins:
        asins.append(a)

print(f"Total Unique ASINs: {len(asins)}")

fetched_catalog = []

for idx, asin in enumerate(asins, 1):
    print(f"[{idx}/{len(asins)}] Fetching ASIN {asin}...")
    try:
        data = get_product_details_and_photos(asin)
        if data:
            fetched_catalog.append(data)
            print(f"   -> Found: {data.get('title')[:60]}... | Price: {data.get('price')}")
        else:
            print(f"   -> Could not fetch {asin}")
    except Exception as e:
        print(f"   -> Error fetching {asin}: {e}")
    time.sleep(0.5)

scratch_dir = Path("G:/CLI/pinterest-auto-affiliate/scratch")
scratch_dir.mkdir(parents=True, exist_ok=True)
with open(scratch_dir / "catalog_41_extracted.json", "w", encoding="utf-8") as f:
    json.dump(fetched_catalog, f, indent=2)

print(f"\nSaved {len(fetched_catalog)} extracted products to catalog_41_extracted.json!")
