import sys
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

print("🔍 Auditing ALL 10 Products for Amazon US & Amazon India 404 Status...\n")

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for item in asins:
        asin = item["asin"]
        name = item["name"]
        print(f"📦 Checking ASIN {asin} ({name}):")
        
        # Check Amazon US
        url_us = f"https://www.amazon.com/dp/{asin}"
        try:
            page.goto(url_us, timeout=10000)
            page.wait_for_timeout(1000)
            content_us = page.content()
            title_us = page.title()
            is_404_us = ("Looking for something?" in content_us or "Page Not Found" in title_us or "404" in title_us)
        except Exception as e:
            is_404_us = True
            
        print(f"   🇺🇸 Amazon US:    {'❌ 404 PAGE NOT FOUND' if is_404_us else '✅ ACTIVE DIRECT PAGE'}")
        
        # Check Amazon India
        url_in = f"https://www.amazon.in/dp/{asin}"
        try:
            page.goto(url_in, timeout=10000)
            page.wait_for_timeout(1000)
            content_in = page.content()
            title_in = page.title()
            is_404_in = ("Looking for something?" in content_in or "Page Not Found" in title_in or "404" in title_in)
        except Exception as e:
            is_404_in = True
            
        print(f"   🇮🇳 Amazon India: {'❌ 404 PAGE NOT FOUND' if is_404_in else '✅ ACTIVE DIRECT PAGE'}\n")
        
        results[asin] = {
            "us_active": not is_404_us,
            "in_active": not is_404_in
        }
        
    browser.close()

print("==================================================")
print("📊 AUDIT RESULTS SUMMARY:")
print("==================================================")
for asin, res in results.items():
    direct = []
    if res["us_active"]: direct.append("US")
    if res["in_active"]: direct.append("IN")
    print(f"ASIN {asin}: direct_regions = {direct}")
