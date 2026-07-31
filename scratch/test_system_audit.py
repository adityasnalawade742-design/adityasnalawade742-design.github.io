import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

root = Path("G:/CLI/pinterest-auto-affiliate")

print("=== 1. Checking index.html Cards & Scripts ===")
index_html = (root / "index.html").read_text(encoding="utf-8")
card_matches = re.findall(r'id="card-([A-Za-z0-9_]+)"', index_html)
print(f"Found {len(card_matches)} cards in index.html: {card_matches}")

reg = json.loads((root / "product_price_registry.json").read_text(encoding="utf-8"))
reg_asins = list(reg.keys())
print(f"Found {len(reg_asins)} items in registry: {reg_asins}")

missing_in_html = [a for a in reg_asins if a not in card_matches]
missing_in_reg = [a for a in card_matches if a not in reg_asins]

if missing_in_html:
    print(f"  [BUG] ASINs in registry but missing on index.html: {missing_in_html}")
else:
    print("  [OK] All registry ASINs are present on index.html!")

if missing_in_reg:
    print(f"  [BUG] ASINs on index.html missing in registry: {missing_in_reg}")
else:
    print("  [OK] All index.html ASINs exist in registry!")

print("\n=== 2. Checking JavaScript Handlers in index.html ===")
if "deleteCard" in index_html and "function deleteCard" not in index_html and "deleteCard =" not in index_html:
    print("  [BUG] 'deleteCard' is called in HTML onclick but NO 'function deleteCard' definition exists in index.html!")
else:
    print("  [OK] deleteCard function check passed!")

print("\n=== 3. Checking Images & Landing Pages ===")
for asin in reg_asins:
    hook_img = root / f"focus_product_{asin}_hook.jpg"
    raw_img = root / "raw_images" / f"raw_{asin}.jpg"
    bridge = root / f"bridge_{asin}.html"
    
    if not hook_img.exists():
        print(f"  [MISSING HOOK IMAGE] {hook_img.name}")
    if not raw_img.exists():
        print(f"  [MISSING RAW IMAGE] {raw_img.name}")
    if not bridge.exists():
        print(f"  [MISSING BRIDGE] bridge_{asin}.html")

print("\n=== 4. Checking delete_product.py ===")
delete_script = (root / "delete_product.py").read_text(encoding="utf-8")
if "delete_product" in delete_script:
    print("  [OK] delete_product.py present.")

print("\n=== Audit Complete ===")
