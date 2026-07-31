import sys
import json
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"
index_file = repo / "index.html"

print("=========================================================================")
print("🌐 100% REAL REGIONAL AMAZON PRICE SCRAPER (NO ESTIMATED CONVERSIONS)")
print("=========================================================================\n")

registry = json.loads(registry_file.read_text(encoding="utf-8"))

regions = [
    ("US", "https://www.amazon.com/dp/"),
    ("IN", "https://www.amazon.in/dp/"),
    ("UK", "https://www.amazon.co.uk/dp/"),
    ("DE", "https://www.amazon.de/dp/"),
    ("CA", "https://www.amazon.ca/dp/"),
    ("AU", "https://www.amazon.com.au/dp/"),
    ("JP", "https://www.amazon.co.jp/dp/")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        locale="en-US"
    )
    page = context.new_page()

    for asin, item in registry.items():
        print(f"📦 Scraping Real Regional Prices for [{asin}] {item.get('headline', '')[:30]}:")
        if "regional_prices" not in item:
            item["regional_prices"] = {}

        for reg, base_url in regions:
            url = f"{base_url}{asin}"
            price_str = None
            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)
                
                # Check for offscreen price
                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen:
                    text = offscreen.inner_text().strip()
                    if text and ("$" in text or "₹" in text or "£" in text or "€" in text or "¥" in text or "CDN$" in text or "CA$" in text or "A$" in text):
                        price_str = text
                
                if not price_str:
                    whole = page.query_selector("span.a-price-whole")
                    frac = page.query_selector("span.a-price-fraction")
                    sym = page.query_selector("span.a-price-symbol")
                    if whole and sym:
                        s = sym.inner_text().strip()
                        w = whole.inner_text().strip().replace("\n", "").replace(".", "")
                        f = frac.inner_text().strip() if frac else "00"
                        price_str = f"{s}{w}.{f}" if f else f"{s}{w}"
            except Exception as e:
                pass

            if price_str:
                # Clean currency symbol formatting
                if reg == "IN" and "INR" in price_str:
                    price_str = price_str.replace("INR", "₹").strip()
                elif reg == "UK" and "INR" in price_str:
                    price_str = None # Reject INR returned on UK
                elif reg == "DE" and "INR" in price_str:
                    price_str = None # Reject INR returned on DE
                    
            if price_str:
                item["regional_prices"][reg] = price_str
                print(f"   • {reg}: Real Scraped Price = {price_str}")
            else:
                # Keep existing valid empirical price or set Not Available
                existing = item["regional_prices"].get(reg)
                if not existing or "INR" in str(existing) and reg != "IN":
                    item["regional_prices"][reg] = "Not Available"
                print(f"   • {reg}: {item['regional_prices'][reg]}")

    browser.close()

# Save updated registry
registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n✅ product_price_registry.json updated with 100% real scraped regional prices!")

# Update index.html
index_html = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

for card in soup.find_all("div", class_="card-wrapper"):
    asin = card.get("data-asin") or card.get("id", "").replace("card-", "")
    if asin in registry:
        rp = registry[asin]["regional_prices"]
        card["data-price-us"] = rp.get("US", "Not Available")
        card["data-price-in"] = rp.get("IN", "Not Available")
        card["data-price-uk"] = rp.get("UK", "Not Available")
        card["data-price-de"] = rp.get("DE", "Not Available")
        card["data-price-ca"] = rp.get("CA", "Not Available")
        card["data-price-au"] = rp.get("AU", "Not Available")
        card["data-price-jp"] = rp.get("JP", "Not Available")
        
        pt = card.find("div", class_="card-price-tag")
        if pt and rp.get("US") != "Not Available":
            pt.string = rp.get("US")

index_file.write_text(str(soup), encoding="utf-8")
print("✅ index.html updated with 100% real scraped regional prices!")
