import sys
import json
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asins = [
    {"asin": "B0DZD1X83N", "name": "Minimalist Wood Base Bedside Lamp"},
    {"asin": "B0BZXNSW5K", "name": "Bedside Table Touch Lamp"},
    {"asin": "B0D1FRDFFX", "name": "Glass Mushroom Lamp"},
    {"asin": "B0C2YLN3H4", "name": "White Ceramic Donut Vase Set"},
    {"asin": "B0GYDXHF4G", "name": "Flame Aroma Essential Oil Diffuser"},
    {"asin": "B0FXLYXM32", "name": "White Wavy Wall Vanity Mirror"},
    {"asin": "B07HP22QTZ", "name": "Suncatcher Crystal Prism Window"},
    {"asin": "B0D8P8CSYP", "name": "Sunset Lamp Projection Light"},
    {"asin": "B0DLN5S5K9", "name": "Minimalist Ceramic Table Lamp"},
    {"asin": "B0DXKGL1T2", "name": "Lily of the Valley Flower Lamp"}
]

storefronts = [
    {"code": "US", "domain": "amazon.com"},
    {"code": "IN", "domain": "amazon.in"},
    {"code": "UK", "domain": "amazon.co.uk"},
    {"code": "DE", "domain": "amazon.de"},
    {"code": "SE", "domain": "amazon.se"},
    {"code": "SG", "domain": "amazon.sg"},
    {"code": "CA", "domain": "amazon.ca"},
    {"code": "AU", "domain": "amazon.com.au"},
    {"code": "JP", "domain": "amazon.co.jp"}
]

print("🌐 AUDITING ALL 10 PRODUCTS ACROSS ALL 9 GLOBAL AMAZON STOREFRONTS...\n")

global_direct_matrix = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for item in asins:
        asin = item["asin"]
        name = item["name"]
        print(f"==================================================")
        print(f"📦 ASIN {asin} ({name}):")
        print(f"==================================================")
        
        active_regions = []
        for sf in storefronts:
            code = sf["code"]
            domain = sf["domain"]
            url = f"https://www.{domain}/dp/{asin}"
            
            try:
                page.goto(url, timeout=7000)
                page.wait_for_timeout(500)
                content = page.content()
                title = page.title()
                is_404 = ("Looking for something?" in content or "Page Not Found" in title or "404" in title or "Robot Check" in title)
            except Exception:
                is_404 = True
                
            status = "❌ 404 UNLISTED" if is_404 else "✅ ACTIVE DIRECT PAGE"
            if not is_404:
                active_regions.append(code)
                
            print(f"   [{code}] {domain:<15}: {status}")
            
        global_direct_matrix[asin] = active_regions
        print(f"   -> Verified Direct Regions: {active_regions}\n")
        
    browser.close()

print("==================================================")
print("🏆 GLOBAL MULTI-REGION MATRIX RESULTS SUMMARY:")
print("==================================================")
print(json.dumps(global_direct_matrix, indent=2))

# Save to disk as global_direct_matrix.json
with open("global_direct_matrix.json", "w", encoding="utf-8") as f:
    json.dump(global_direct_matrix, f, indent=2)

print("\nSaved global_direct_matrix.json successfully!")
