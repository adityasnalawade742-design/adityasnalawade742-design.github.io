import json
from pathlib import Path

cache_file = Path('serpapi_cache.json')
if cache_file.exists():
    data = json.load(open(cache_file, encoding='utf-8'))
    for k, v in data.items():
        if 'lily' in k.lower() or 'flower' in k.lower():
            for idx, item in enumerate(v[:5], 1):
                print(f"Option {idx}:")
                print("  Title:", item.get("title"))
                print("  Link: ", item.get("link") or item.get("product_link") or item.get("url"))
                print("  ASIN: ", item.get("asin"))
