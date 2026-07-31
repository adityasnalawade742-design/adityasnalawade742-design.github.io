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

print("=== 🔄 SYNCHRONIZING index.html PRICE ATTRIBUTES FROM REGISTRY ===")

registry = json.loads(registry_file.read_text(encoding="utf-8"))
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

cards = soup.find_all("div", class_="card-wrapper")
print(f"Found {len(cards)} card wrappers in index.html.")

updated_count = 0

for card in cards:
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if not asin or asin not in registry:
        continue
    
    item = registry[asin]
    reg_prices = item.get("regional_prices", {})
    
    # Calculate base USD price
    us_price_str = reg_prices.get("US", item.get("current_price", "$19.99"))
    usd_val_match = re.search(r'([0-9]+\.[0-9]{2})', us_price_str)
    base_usd = usd_val_match.group(1) if usd_val_match else "19.99"
    
    card["data-base-usd"] = base_usd
    card["data-price-us"] = reg_prices.get("US", f"${base_usd}")
    card["data-price-uk"] = reg_prices.get("UK", "Not Available")
    card["data-price-in"] = reg_prices.get("IN", "Not Available")
    card["data-price-de"] = reg_prices.get("DE", "Not Available")
    card["data-price-ca"] = reg_prices.get("CA", "Not Available")
    card["data-price-jp"] = reg_prices.get("JP", "Not Available")
    card["data-price-au"] = reg_prices.get("AU", "Not Available")
    
    # Update inner price tag
    price_tag = card.find("div", class_="card-price-tag")
    if price_tag:
        price_tag.string = reg_prices.get("US", f"${base_usd}")
        
    updated_count += 1
    print(f"  • Updated [{asin}] {item.get('headline', '')[:30]}: Base USD = ${base_usd}")

index_file.write_text(str(soup), encoding="utf-8")
print(f"\n✅ Successfully updated {updated_count} cards in index.html from product_price_registry.json!")
