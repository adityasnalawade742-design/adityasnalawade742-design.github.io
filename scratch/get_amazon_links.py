import sys
from pathlib import Path

repo_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_dir))

from modules.amazon_finder import fetch_amazon_products
prods = fetch_amazon_products("Lily of the Valley Flower Table Lamp", num_results=5)

print("==================================================")
for idx, p in enumerate(prods, 1):
    title = p.get("title", "")
    asin = p.get("asin", "")
    link = p.get("url") or p.get("product_url") or f"https://www.amazon.com/dp/{asin}"
    img = p.get("original_image_url") or p.get("image")
    print(f"Option {idx}:")
    print(f"  Title: {title}")
    print(f"  ASIN:  {asin}")
    print(f"  Link:  {link}")
    print(f"  Image: {img}\n")
print("==================================================")
