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

print("=== 🛠️ PERFECTING ALL REGIONAL PRICE ATTRIBUTES FOR WORLD COUNTRIES ===")

# Base USD Prices & Authentic Regional Overrides
base_usd_prices = {
    "B0DZD1X83N": 20.00,
    "B0GYDXHF4G": 35.00,
    "B0FXLYXM32": 76.49,
    "B0C2YLN3H4": 18.30,
    "B07HP22QTZ": 7.99,
    "B0BZXNSW5K": 19.99,
    "B0DXKGL1T2": 38.57,
    "B0D1FRDFFX": 35.98,
    "B0D8P8CSYP": 16.00
}

# Special regional price overrides for items with direct local listings
local_price_overrides = {
    "B0C2YLN3H4": {"IN": "₹599.00"},
    "B0BZXNSW5K": {"IN": "₹475.00"},
    "B0GYDXHF4G": {"IN": "Not Available", "UK": "Not Available", "DE": "Not Available", "CA": "Not Available", "AU": "Not Available", "JP": "Not Available"}
}

rates = {
    "US": 1.0,
    "UK": 0.78,
    "DE": 0.92,
    "CA": 1.36,
    "AU": 1.52,
    "IN": 83.50,
    "JP": 155.0
}

symbols = {
    "US": "$",
    "UK": "£",
    "DE": "€",
    "CA": "CA$",
    "AU": "A$",
    "IN": "₹",
    "JP": "¥"
}

registry = json.loads(registry_file.read_text(encoding="utf-8"))

for asin, base_usd in base_usd_prices.items():
    if asin not in registry:
        continue
    
    item = registry[asin]
    item["current_price"] = f"${base_usd:.2f}"
    
    if "regional_prices" not in item:
        item["regional_prices"] = {}
        
    for reg, rate in rates.items():
        # Check override first
        if asin in local_price_overrides and reg in local_price_overrides[asin]:
            item["regional_prices"][reg] = local_price_overrides[asin][reg]
        else:
            sym = symbols[reg]
            converted = base_usd * rate
            if reg == "JP":
                item["regional_prices"][reg] = f"{sym}{int(round(converted)):,}"
            else:
                item["regional_prices"][reg] = f"{sym}{converted:.2f}"

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ Updated product_price_registry.json with 100% clean regional prices.")

# Now update index.html card attributes
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin in registry:
        reg_p = registry[asin]["regional_prices"]
        card["data-base-usd"] = f"{base_usd_prices[asin]:.2f}"
        card["data-price-us"] = reg_p.get("US", f"${base_usd_prices[asin]:.2f}")
        card["data-price-uk"] = reg_p.get("UK", "Not Available")
        card["data-price-in"] = reg_p.get("IN", "Not Available")
        card["data-price-de"] = reg_p.get("DE", "Not Available")
        card["data-price-ca"] = reg_p.get("CA", "Not Available")
        card["data-price-jp"] = reg_p.get("JP", "Not Available")
        card["data-price-au"] = reg_p.get("AU", "Not Available")
        
        pt = card.find("div", class_="card-price-tag")
        if pt:
            pt.string = reg_p.get("US", f"${base_usd_prices[asin]:.2f}")

index_file.write_text(str(soup), encoding="utf-8")
print("✅ Successfully updated index.html with clean regional price attributes ($, £, €, ₹, CA$, A$, ¥)!")
