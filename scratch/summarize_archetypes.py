import json
from pathlib import Path

catalog_path = Path("scratch/catalog_41_extracted.json")
catalog = json.loads(catalog_path.read_text(encoding="utf-8"))

print(f"Total Extracted Catalog Items: {len(catalog)}\n")

categories = {}
prices = []

for item in catalog:
    title = item.get("title", "")
    price_str = item.get("price", "$0")
    
    # Clean price
    import re
    p_num = 0.0
    try:
        p_num = float(re.sub(r'[^\d.]', '', price_str))
    except Exception:
        pass
    if p_num > 0:
        prices.append(p_num)
        
    t_lower = title.lower()
    
    cat = "Other Decor & Accessories"
    if any(k in t_lower for k in ["lamp", "light", "chandelier", "sconce"]):
        cat = "Aesthetic & Ambient Lighting"
    elif any(k in t_lower for k in ["vase", "pottery"]):
        cat = "Ceramic & Stoneware Vases"
    elif any(k in t_lower for k in ["mirror"]):
        cat = "Mirrors & Vanity Wall Decor"
    elif any(k in t_lower for k in ["blanket", "throw", "pillow", "cushion"]):
        cat = "Cozy Textiles & Throw Blankets"
    elif any(k in t_lower for k in ["chair", "armchair", "table", "ottoman", "storage"]):
        cat = "Accent Furniture & Tables"
    elif any(k in t_lower for k in ["sculpture", "statue", "candle", "tray", "basket"]):
        cat = "Tabletop Styling & Sculptural Objects"
    elif any(k in t_lower for k in ["painting", "art", "frame"]):
        cat = "Wall Art & Gallery Frames"

    categories.setdefault(cat, []).append({"title": title[:65], "price": price_str})

for c, items in categories.items():
    print(f"=== Category: {c} ({len(items)} items) ===")
    for it in items[:6]:
        print(f"  • {it['price']} - {it['title']}")
    print()

if prices:
    print(f"Price Range: ${min(prices):.2f} - ${max(prices):.2f} (Avg: ${sum(prices)/len(prices):.2f})")
