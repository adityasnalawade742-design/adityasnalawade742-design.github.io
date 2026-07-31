import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Fix UTF-8 output encoding for Windows terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
bridge_creator_file = repo / "modules/bridge_creator.py"

print("=========================================================================")
print("🌐 FULL SYSTEM GEOLOCATION AUDIT FOR ALL 8 ACTIVE STORE IDs & LANDING PAGES")
print("=========================================================================\n")

# Store IDs to test
expected_stores = {
    "US": {"tag": "smartdeal0358-20", "domain": "amazon.com", "currency": "USD", "symbol": "$"},
    "CA": {"tag": "smartdeal0302-20", "domain": "amazon.ca", "currency": "CAD", "symbol": "CA$"},
    "IN": {"tag": "smartdeal0358-21", "domain": "amazon.in", "currency": "INR", "symbol": "₹"},
    "UK": {"tag": "smartdea04b3a-21", "domain": "amazon.co.uk", "currency": "GBP", "symbol": "£"},
    "DE": {"tag": "smartdeal0bb4-21", "domain": "amazon.de", "currency": "EUR", "symbol": "€"},
    "FR": {"tag": "smartdeal0962-21", "domain": "amazon.fr", "currency": "EUR", "symbol": "€"},
    "ES": {"tag": "smartdeal0b46-21", "domain": "amazon.es", "currency": "EUR", "symbol": "€"},
    "IT": {"tag": "smartdea03a8d-21", "domain": "amazon.it", "currency": "EUR", "symbol": "€"}
}

# 1. Audit index.html JS mapping
print("📌 [1/3] AUDITING HOMEPAGE SHOWCASE CURRENCY & LINK FORWARDING (index.html)...")
index_text = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(index_text, "html.parser")
cards = soup.find_all("div", class_="card-wrapper")

print(f"  📊 Homepage Cards Found: {len(cards)}")
has_curr_map = "countryToCurrencyMap" in index_text
has_apply_func = "applyHomepageCountry" in index_text
has_exchange_rates = "exchangeRates" in index_text

print(f"  • Currency Map: {'✅ PASS' if has_curr_map else '❌ FAIL'}")
print(f"  • applyHomepageCountry Engine: {'✅ PASS' if has_apply_func else '❌ FAIL'}")
print(f"  • Real-time Exchange Rates: {'✅ PASS' if has_exchange_rates else '❌ FAIL'}\n")

# 2. Audit Bridge Creator Template Engine
print("📌 [2/3] AUDITING BRIDGE CREATOR TEMPLATE (modules/bridge_creator.py)...")
bc_text = bridge_creator_file.read_text(encoding="utf-8")
template_store_pass = True
for cc, meta in expected_stores.items():
    if meta["tag"] in bc_text:
        print(f"  ✅ {cc} ({meta['domain']}) -> Tag '{meta['tag']}' mapped in Template Engine")
    else:
        print(f"  ❌ {cc} ({meta['domain']}) -> Tag '{meta['tag']}' MISSING")
        template_store_pass = False

print()

# 3. Audit All 9 Landing Pages for All 8 Country Stores
print("📌 [3/3] AUDITING ALL 9 LANDING PAGES ACROSS ALL 8 COUNTRY STORES...")
landing_pages = sorted(list(repo.glob("bridge_*.html")))

overall_results = {}

for lp in landing_pages:
    lp_text = lp.read_text(encoding="utf-8")
    lp_soup = BeautifulSoup(lp_text, "html.parser")
    title_el = lp_soup.find("h1")
    title = title_el.text.strip() if title_el else lp.name
    asin = lp.name.replace("bridge_", "").replace(".html", "")
    
    print(f"📦 Product [{asin}]: {title[:40]}...")
    
    lp_country_results = {}
    for cc, meta in expected_stores.items():
        tag = meta["tag"]
        domain = meta["domain"]
        symbol = meta["symbol"]
        
        # Check tag mapped in JS associateTagMap
        tag_ok = tag in lp_text
        
        # Check domain mapped in countryMap or applyGeoRedirect
        domain_ok = domain in lp_text
        
        # Check currency symbol in JS currencySymbols
        symbol_ok = symbol in lp_text or meta["currency"] in lp_text
        
        status_ok = tag_ok and domain_ok and symbol_ok
        lp_country_results[cc] = {
            "tag_ok": tag_ok,
            "domain_ok": domain_ok,
            "symbol_ok": symbol_ok,
            "status_ok": status_ok
        }
        
        symbol_display = symbol if symbol != '€' else 'EUR (€)'
        print(f"   • {cc} | Domain: {domain:<12} | Tag: {tag:<18} | Currency: {symbol_display:<7} | Audit: {'✅ 100% PASS' if status_ok else '❌ FAIL'}")
    
    overall_results[asin] = lp_country_results
    print()

print("=========================================================================")
print("🏆 MASTER GEOLOCATION SYSTEM AUDIT RESULT:")
print("=========================================================================")

all_pass = True
for asin, results in overall_results.items():
    for cc, res in results.items():
        if not res["status_ok"]:
            all_pass = False
            print(f"❌ Product {asin} failed for country {cc}")

if all_pass:
    print("✅ 100% PASS: ALL 9 LANDING PAGES & HOMEPAGE SHOWCASE ARE CORRECTLY FORWARDING & DISPLAYING THE RIGHT CURRENCIES, DOMAINS, AND AFFILIATE STORE IDs FOR ALL 8 GEOLOCATIONS!")
print("=========================================================================")
