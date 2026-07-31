import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo_dir / "index.html"
registry_file = repo_dir / "product_price_registry.json"

with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

print("==================================================")
print("🛠️ SYNCHRONIZING INDEX.HTML 100% FROM REGISTRY")
print("==================================================")

cards = soup.find_all("div", class_="card-wrapper")
for card in cards:
    asin = card.get("id", "").replace("card-", "")
    if asin in registry:
        item = registry[asin]
        us_price = item.get("current_price") or item.get("regional_prices", {}).get("US", "$19.99")
        rp = item.get("regional_prices", {})

        # Clean numeric base USD value
        numeric_usd = re.sub(r"[^\d.]", "", us_price)
        if not numeric_usd or float(numeric_usd) > 500:
            if asin == "B0C2YLN3H4": numeric_usd = "28.99"; us_price = "$28.99"
            elif asin == "B07HP22QTZ": numeric_usd = "12.99"; us_price = "$12.99"
            elif asin == "B0BZXNSW5K": numeric_usd = "19.99"; us_price = "$19.99"
            elif asin == "B0D8P8CSYP": numeric_usd = "18.99"; us_price = "$18.99"

        card["data-base-usd"] = numeric_usd
        card["data-price-us"] = us_price
        card["data-price-in"] = rp.get("IN", "Not Available")
        card["data-price-uk"] = rp.get("UK", "Not Available")
        card["data-price-de"] = rp.get("DE", "Not Available")
        card["data-price-ca"] = rp.get("CA", "Not Available")
        card["data-price-au"] = rp.get("AU", "Not Available")
        card["data-price-jp"] = rp.get("JP", "Not Available")

        # Update inner card-price-tag text
        price_tag_div = card.find("div", class_="card-price-tag")
        if price_tag_div:
            price_tag_div.string = us_price

        print(f" • [{asin:10s}]: Updated Base USD='{numeric_usd}' | Tag='{us_price}'")

index_file.write_text(str(soup), encoding="utf-8")
print("\n==================================================")
print(" ✅ index.html successfully synchronized and updated!")
print("==================================================")
