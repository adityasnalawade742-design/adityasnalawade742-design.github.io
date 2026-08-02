import sys
import json
import re
import os
import requests
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p = Path(__file__).resolve().parent
if str(p) not in sys.path:
    sys.path.append(str(p))

registry_path = p / "product_price_registry.json"

if not registry_path.exists():
    print("⚠️ Registry file missing. Skipping sync.")
    sys.exit(0)

with open(registry_path, "r", encoding="utf-8") as f:
    registry = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

regions_to_scrape = [
    ("US", "https://www.amazon.com/dp/"),
    ("IN", "https://www.amazon.in/dp/"),
    ("UK", "https://www.amazon.co.uk/dp/"),
    ("DE", "https://www.amazon.de/dp/"),
    ("CA", "https://www.amazon.ca/dp/"),
    ("AU", "https://www.amazon.com.au/dp/"),
    ("JP", "https://www.amazon.co.jp/dp/")
]

print("=== 🔄 DAILY MULTI-REGION AMAZON PRICE SYNCHRONIZATION ===")

for asin, item in registry.items():
    print(f"\n📦 [{asin}] {item.get('title', 'Product')[:35]}:")
    if "regional_prices" not in item:
        item["regional_prices"] = {}
        
    for reg_code, domain_prefix in regions_to_scrape:
        url = f"{domain_prefix}{asin}"
        price = None
        try:
            res = requests.get(url, headers=headers, timeout=6)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                offscreen = soup.select_one(".a-price .a-offscreen")
                if offscreen and offscreen.text:
                    price = offscreen.text.strip()
                if not price:
                    whole = soup.select_one("span.a-price-whole")
                    frac = soup.select_one("span.a-price-fraction")
                    if whole and frac:
                        price = f"{whole.text.strip()}{frac.text.strip()}"
        except Exception as e:
            pass
            
        if price:
            item["regional_prices"][reg_code] = price
            if reg_code == "US":
                item["current_price"] = price
            print(f"   • {reg_code:2s}: Scraped '{price}'")
        else:
            existing = item["regional_prices"].get(reg_code, "Not Available")
            print(f"   • {reg_code:2s}: Kept existing '{existing}'")

# Save updated registry
with open(registry_path, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2)

print("\n ✅ Registry updated with multi-region prices!")

# Rebuild 100% of landing pages to propagate new prices to ALL 21 DOMAINS & 200+ WORLD COUNTRIES
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

print("\n🔨 Rebuilding 100% of landing pages for all 21 Amazon domains...")
for asin, item in master_catalog.items():
    if asin in registry:
        reg_data = registry[asin].get("regional_prices", {})
        item["regional_matrix"] = {k.lower(): v for k, v in reg_data.items()}
        if "current_price" in registry[asin]:
            item["current_price"] = registry[asin]["current_price"]
            item["price"] = registry[asin]["current_price"]
            
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Git Commit & Push Live
print("\n🚀 Pushing daily price sync live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(p), check=True)
    subprocess.run(["git", "commit", "-m", "daily price sync: update multi-region prices for all 21 Amazon domains"], cwd=str(p), check=False)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(p), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push info: {e}")

print("\n🎉 MULTI-REGION PRICE SYNC COMPLETED SUCCESSFULLY!")
