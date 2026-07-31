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

usd_prices = {
    "B0DZD1X83N": "$20.00",
    "B0GYDXHF4G": "$35.00",
    "B0FXLYXM32": "$76.49",
    "B0C2YLN3H4": "$18.30",
    "B07HP22QTZ": "$7.99",
    "B0BZXNSW5K": "$19.99",
    "B0DXKGL1T2": "$38.57",
    "B0D1FRDFFX": "$35.98",
    "B0D8P8CSYP": "$16.00"
}

registry = json.loads(registry_file.read_text(encoding="utf-8"))

for asin, price_usd in usd_prices.items():
    if asin in registry:
        registry[asin]["current_price"] = price_usd
        if "regional_prices" not in registry[asin]:
            registry[asin]["regional_prices"] = {}
        registry[asin]["regional_prices"]["US"] = price_usd

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ Updated product_price_registry.json with exact clean USD retail prices.")

# Now sync index.html
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin in usd_prices:
        usd_str = usd_prices[asin]
        usd_num = usd_str.replace("$", "")
        card["data-base-usd"] = usd_num
        card["data-price-us"] = usd_str
        
        # update inner tag
        pt = card.find("div", class_="card-price-tag")
        if pt:
            pt.string = usd_str

index_file.write_text(str(soup), encoding="utf-8")
print("✅ Successfully updated index.html with exact clean USD retail prices!")
