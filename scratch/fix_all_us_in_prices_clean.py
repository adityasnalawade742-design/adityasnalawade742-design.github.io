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

print("=== 📌 CLEANING ALL US & IN REGIONAL PRICES IN REGISTRY AND HOMEPAGE ===")

clean_prices = {
    "B07HP22QTZ": {"US": "$7.99", "IN": "₹2,760.15", "UK": "£14.99", "DE": "€8.75", "CA": "CA$19.99", "AU": "A$30.57", "JP": "¥3,651"},
    "B0BZXNSW5K": {"US": "$19.99", "IN": "₹475.00", "UK": "£15.59", "DE": "€18.39", "CA": "CA$29.99", "AU": "A$30.38", "JP": "¥3,098"},
    "B0C2YLN3H4": {"US": "$18.30", "IN": "₹599.00", "UK": "£14.27", "DE": "€16.84", "CA": "CA$42.26", "AU": "A$26.88", "JP": "¥4,664"},
    "B0D1FRDFFX": {"US": "$35.98", "IN": "₹11,299.51", "UK": "£28.06", "DE": "€33.10", "CA": "CA$48.93", "AU": "A$54.69", "JP": "¥5,577"},
    "B0D8P8CSYP": {"US": "$16.00", "IN": "₹3,843.00", "UK": "£12.48", "DE": "€14.72", "CA": "CA$21.76", "AU": "A$24.32", "JP": "¥2,480"},
    "B0FXLYXM32": {"US": "$76.49", "IN": "₹6,386.91", "UK": "£59.66", "DE": "€70.37", "CA": "CA$216.34", "AU": "A$116.26", "JP": "¥20,390"},
    "B0DZD1X83N": {"US": "$20.00", "IN": "₹1,670.00", "UK": "£15.60", "DE": "€18.40", "CA": "CA$27.20", "AU": "A$30.40", "JP": "¥3,100"},
    "B0DXKGL1T2": {"US": "$38.57", "IN": "₹3,220.59", "UK": "£30.08", "DE": "€35.48", "CA": "CA$52.46", "AU": "A$58.63", "JP": "¥5,978"},
    "B0GYDXHF4G": {"US": "$35.00", "IN": "Not Available", "UK": "Not Available", "DE": "Not Available", "CA": "Not Available", "AU": "Not Available", "JP": "Not Available"}
}

registry = json.loads(registry_file.read_text(encoding="utf-8"))

for asin, rp in clean_prices.items():
    if asin in registry:
        registry[asin]["current_price"] = rp["US"]
        registry[asin]["regional_prices"] = rp

registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("✅ product_price_registry.json cleaned of raw INR US entries.")

# Clean index.html
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin in clean_prices:
        rp = clean_prices[asin]
        card["data-base-usd"] = rp["US"].replace("$", "")
        card["data-price-us"] = rp["US"]
        card["data-price-in"] = rp["IN"]
        card["data-price-uk"] = rp["UK"]
        card["data-price-de"] = rp["DE"]
        card["data-price-ca"] = rp["CA"]
        card["data-price-au"] = rp["AU"]
        card["data-price-jp"] = rp["JP"]
        
        pt = card.find("div", class_="card-price-tag")
        if pt:
            pt.string = rp["US"]

index_file.write_text(str(soup), encoding="utf-8")
print("✅ index.html price attributes cleaned (B0BZXNSW5K US = $19.99, IN = ₹475.00)!")
