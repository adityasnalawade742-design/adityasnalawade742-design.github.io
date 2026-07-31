import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"

registry = json.loads(registry_file.read_text(encoding="utf-8"))
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

print("=== 🔬 COMPREHENSIVE PRICE DISCREPANCY DETECTOR ===")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin not in registry:
        print(f"⚠️ ASIN {asin} missing in registry!")
        continue
    
    item = registry[asin]
    reg_p = item.get("regional_prices", {})
    base_usd = card.get("data-base-usd")
    price_us = card.get("data-price-us")
    price_in = card.get("data-price-in")
    price_uk = card.get("data-price-uk")
    price_de = card.get("data-price-de")
    price_ca = card.get("data-price-ca")
    
    print(f"\n📦 ASIN [{asin}] - {item.get('headline', '')[:30]}:")
    print(f"  • Registry current_price: '{item.get('current_price')}'")
    print(f"  • Homepage base_usd: '{base_usd}' | price_us: '{price_us}'")
    print(f"  • Homepage price_in: '{price_in}' | Registry IN: '{reg_p.get('IN')}'")
    print(f"  • Homepage price_uk: '{price_uk}' | Registry UK: '{reg_p.get('UK')}'")
    print(f"  • Homepage price_de: '{price_de}' | Registry DE: '{reg_p.get('DE')}'")
    print(f"  • Homepage price_ca: '{price_ca}' | Registry CA: '{reg_p.get('CA')}'")

print("\n=== Audit Finished ===")
