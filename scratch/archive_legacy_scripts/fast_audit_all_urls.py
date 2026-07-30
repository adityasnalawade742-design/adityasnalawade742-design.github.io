import sys
import requests
from concurrent.futures import ThreadPoolExecutor

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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def check_asin(item):
    asin = item["asin"]
    name = item["name"]
    
    # Check US
    url_us = f"https://www.amazon.com/dp/{asin}"
    try:
        r_us = requests.get(url_us, headers=headers, timeout=5)
        us_active = (r_us.status_code == 200 and "Looking for something?" not in r_us.text and "Page Not Found" not in r_us.text)
    except Exception:
        us_active = False
        
    # Check India
    url_in = f"https://www.amazon.in/dp/{asin}"
    try:
        r_in = requests.get(url_in, headers=headers, timeout=5)
        in_active = (r_in.status_code == 200 and "Looking for something?" not in r_in.text and "Page Not Found" not in r_in.text)
    except Exception:
        in_active = False
        
    return asin, name, us_active, in_active

print("🔍 Auditing ALL 10 Products for Direct Amazon US & Amazon India Page Status...\n")

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(check_asin, asins))

direct_map = {}
for asin, name, us_active, in_active in results:
    regions = []
    if us_active: regions.append("US")
    if in_active: regions.append("IN")
    direct_map[asin] = regions
    print(f"📦 {asin} ({name[:30]}...):")
    print(f"   🇺🇸 Amazon US:    {'✅ ACTIVE DIRECT PAGE' if us_active else '❌ 404 UNLISTED (Uses US Search Fallback)'}")
    print(f"   🇮🇳 Amazon India: {'✅ ACTIVE DIRECT PAGE' if in_active else '❌ 404 UNLISTED (Uses IN Search Fallback)'}\n")

print("==================================================")
print("📊 FINAL VERIFIED DIRECT REGIONS MAP:")
print("==================================================")
for asin, regions in direct_map.items():
    print(f'"{asin}": direct_regions = {regions}')
