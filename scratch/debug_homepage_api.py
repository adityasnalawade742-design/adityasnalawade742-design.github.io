import re
import json
from pathlib import Path

index_path = Path("index.html")
reg_path = Path("product_price_registry.json")

reg_data = {}
if reg_path.exists():
    try: reg_data = json.loads(reg_path.read_text(encoding="utf-8"))
    except Exception as e: print("Registry load error:", e)

print(f"Registry Items ({len(reg_data)}):", list(reg_data.keys()))

products = []
if index_path.exists():
    html = index_path.read_text(encoding="utf-8")
    card_matches = re.findall(r'id="card-([A-Za-z0-9_]{5,15})"', html)
    print("Found Card Matches in index.html:", card_matches)
    
    for asin in card_matches:
        meta = reg_data.get(asin, {})
        title = meta.get('title') or f"Product {asin}"
        price = meta.get('price') or "$19.99"
        image = f"./focus_product_{asin}_hook.jpg"

        products.append({
            'asin': asin,
            'title': title,
            'price': price,
            'image': image,
            'bridge_url': f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
        })

print(f"\nExtracted {len(products)} homepage products cleanly!")
print(json.dumps(products[:3], indent=2))
