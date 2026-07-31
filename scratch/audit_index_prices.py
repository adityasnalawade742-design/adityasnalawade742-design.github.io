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

with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

print("==================================================")
print("🔍 HOMEPAGE (index.html) VS REGISTRY PRICE AUDIT")
print("==================================================")

cards = soup.find_all("div", class_="card-wrapper")
for card in cards:
    asin = card.get("id", "").replace("card-", "")
    card_price_tag = card.find("div", class_="card-price-tag")
    card_price_text = card_price_tag.text.strip() if card_price_tag else "Missing"
    data_price_us = card.get("data-price-us", "Missing")
    data_base_usd = card.get("data-base-usd", "Missing")
    
    reg_us_price = registry.get(asin, {}).get("current_price") or registry.get(asin, {}).get("regional_prices", {}).get("US", "Missing")
    
    match = (card_price_text == reg_us_price)
    status = "✅ MATCH" if match else "🔴 MISMATCH"
    print(f" • [{asin:10s}]: Card Tag='{card_price_text:10s}' | Data US='{data_price_us:10s}' | Registry US='{reg_us_price:10s}' -> {status}")
