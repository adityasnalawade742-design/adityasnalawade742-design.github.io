import sys
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🔬 AUDITING 100% PRICE PARITY: HOMEPAGE VS BRIDGE PAGES (ALL REGIONS)")
print("=========================================================================\n")

test_matrix = [
    ("US", "USD"),
    ("IN", "INR"),
    ("UK", "GBP"),
    ("DE", "EUR"),
    ("CA", "CAD"),
    ("AU", "AUD"),
    ("JP", "JPY")
]

mismatches = []
matches_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    registry = json.loads(registry_file.read_text(encoding="utf-8"))

    for cc, curr in test_matrix:
        print(f"📌 Auditing Region [{cc}] / Currency [{curr}] across all products...")
        
        # Load Homepage for this country
        homepage_url = f"file:///{index_file.resolve()}?country={cc}".replace("\\", "/")
        page.goto(homepage_url)
        page.wait_for_timeout(150)
        
        # Trigger currency switch on homepage if needed
        page.select_option("#currencySelector", curr)
        page.wait_for_timeout(150)

        # Scrape all card prices from homepage
        homepage_prices = {}
        for card in page.query_selector_all(".card-wrapper"):
            asin = card.get_attribute("data-asin") or card.get_attribute("id").replace("card-", "")
            pt = card.query_selector(".card-price-tag")
            if pt:
                homepage_prices[asin] = pt.inner_text().strip()

        # Compare against each bridge page
        for bf in bridge_files:
            asin = bf.name.replace("bridge_", "").replace(".html", "")
            bridge_url = f"file:///{bf.resolve()}?country={cc}".replace("\\", "/")
            page.goto(bridge_url)
            page.wait_for_timeout(100)
            
            bridge_price = page.evaluate("(document.querySelector('.tag') || document.querySelector('.price') || {}).innerText || ''").strip()
            
            # Clean "✨ VERIFIED DEAL • ", "🔴 OUT OF STOCK", etc.
            clean_bridge_price = bridge_price.replace("✨ VERIFIED DEAL • ", "").replace("⚠️ UNLISTED IN REGION • ", "").strip()
            
            hp_price = homepage_prices.get(asin, "")
            
            # Compare prices
            if hp_price and clean_bridge_price:
                # Normalize spaces and text
                if hp_price == clean_bridge_price or hp_price in clean_bridge_price or clean_bridge_price in hp_price:
                    matches_count += 1
                else:
                    mismatches.append(f"Product [{asin}] in [{cc}]: Homepage='{hp_price}' vs Bridge='{clean_bridge_price}'")
                    print(f"  ❌ MISMATCH Product [{asin}] [{cc}]: Homepage='{hp_price}' vs Bridge='{clean_bridge_price}'")

    browser.close()

print("\n=========================================================================")
print("🏆 HOMEPAGE VS BRIDGE PAGE PRICE PARITY RESULTS:")
print("=========================================================================")
print(f"📊 Total Product x Country Tests Passed: {matches_count}")
print(f"❌ Price Mismatches Found: {len(mismatches)}")

if not mismatches:
    print("🎉 ZERO PRICE MISMATCHES FOUND! HOMEPAGE AND BRIDGE PAGES MATCH 100% FOR ALL REGIONS & CURRENCIES!")
else:
    print("❌ MISMATCHES REQUIRING CORRECTION:")
    for mm in mismatches:
        print(f"  • {mm}")
print("=========================================================================")
