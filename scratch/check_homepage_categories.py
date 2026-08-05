import re
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path('.').resolve()
reg_file = repo / 'product_price_registry.json'
idx_file = repo / 'index.html'

registry = json.loads(reg_file.read_text(encoding='utf-8'))
idx_html = idx_file.read_text(encoding='utf-8')

card_pattern = re.compile(r'<div\b[^>]*?\bid=["\']card-([^"\']+)["\'][^>]*?>', re.IGNORECASE)
cards = card_pattern.findall(idx_html)

print("=========================================================================")
print("🌐 HOMEPAGE (index.html) vs REGISTRY CATEGORY ALIGNMENT AUDIT")
print("=========================================================================\n")

mismatches = []
by_category = {"vases": [], "lighting": [], "mirror": [], "decor": []}

for asin in cards:
    title = registry.get(asin, {}).get('title', asin)
    reg_cat = registry.get(asin, {}).get('category', 'decor')
    
    # Extract data-category attribute from index.html card tag
    tag_match = re.search(rf'(<div\b[^>]*?\bid=["\']card-{asin}["\'][^>]*?>)', idx_html, re.IGNORECASE)
    tag_str = tag_match.group(1) if tag_match else ''
    cat_match = re.search(r'data-category="([^"]*)"', tag_str)
    html_cat = cat_match.group(1) if cat_match else 'MISSING'
    
    by_category.setdefault(reg_cat, []).append((asin, title))
    
    if reg_cat != html_cat:
        mismatches.append({
            'asin': asin,
            'title': title,
            'registry_cat': reg_cat,
            'html_cat': html_cat
        })

print("1. 📊 CATEGORY DISTRIBUTION ON HOMEPAGE:")
for cat, items in by_category.items():
    print(f"   • {cat.upper():8s} ({len(items)} items):")
    for asin, title in items:
        print(f"       - [{asin}] {title[:45]}...")

print(f"\n2. 🔍 ALIGNMENT CHECK:")
if mismatches:
    print(f"   ⚠️ Found {len(mismatches)} data-category mismatch(es) between registry and index.html:")
    for m in mismatches:
        print(f"      • [{m['asin']}] Registry: '{m['registry_cat']}' vs index.html: '{m['html_cat']}'")
else:
    print("   ✅ 100% PERFECT ALIGNMENT! Every index.html card matches registry category 1:1.")

print("\n=========================================================================")
