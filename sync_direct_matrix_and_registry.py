import sys
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
registry_file = repo / "product_price_registry.json"
matrix_file = repo / "global_direct_matrix.json"
index_file = repo / "index.html"

registry = json.loads(registry_file.read_text(encoding="utf-8"))
matrix = {}
if matrix_file.exists():
    matrix = json.loads(matrix_file.read_text(encoding="utf-8"))

for asin, data in registry.items():
    regional_asins = data.get("regional_asins", {})
    
    # Direct regions are US plus any region with a verified regional_asin entry
    direct_regs = ["US"]
    for cc, reg_asin in regional_asins.items():
        if cc != "US" and reg_asin:
            direct_regs.append(cc)
    
    # Save back to matrix & registry
    matrix[asin] = direct_regs
    data["direct_regions"] = direct_regs
    data["image_path"] = f"raw_images/raw_{asin}.jpg"

# Save updated JSON files
matrix_file.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")
registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ Synchronized global_direct_matrix.json and product_price_registry.json for all 16 ASINs!")

# Update index.html visibleCount to 16
raw_html = index_file.read_text(encoding="utf-8")
raw_html = re.sub(r'id="visibleCount">\d+</span>', 'id="visibleCount">16</span>', raw_html)

# Update JSON-LD schema to 16 items
item_list_entries = []
for idx, (asin, item) in enumerate(registry.items(), 1):
    title = item.get("title", f"Product {asin}").replace('"', '\\"')
    entry = {
        "@type": "ListItem",
        "position": idx,
        "name": title,
        "url": f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
    }
    item_list_entries.append(entry)

json_ld = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "numberOfItems": len(registry),
    "itemListElement": item_list_entries
}

# Replace JSON-LD schema block
json_ld_str = json.dumps(json_ld, indent=2)
raw_html = re.sub(r'<script type="application/ld\+json">\s*\{[\s\S]*?\}\s*</script>', f'<script type="application/ld+json">\n{json_ld_str}\n</script>', raw_html, count=1)

index_file.write_text(raw_html, encoding="utf-8")
print("✅ Updated index.html visibleCount to 16 and updated JSON-LD schema with all 16 products!")
