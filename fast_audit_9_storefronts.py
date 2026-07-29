import sys
import json
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def check_single(args):
    asin, sf = args
    code = sf["code"]
    domain = sf["domain"]
    url = f"https://www.{domain}/dp/{asin}"
    
    try:
        r = requests.get(url, headers=headers, timeout=8)
        # Foolproof check: An active listing MUST have the productTitle element in HTML
        has_title = ("productTitle" in r.text) or ("title" in r.text and "dp-title" in r.text)
        has_404 = ("Looking for something" in r.text) or ("not a functioning page" in r.text) or ("Page Not Found" in r.text) or ("Dogs of Amazon" in r.text)
        is_active = (r.status_code == 200) and has_title and not has_404
    except Exception:
        is_active = False
        
    return asin, code, is_active

tasks = []
for item in asins:
    for sf in storefronts:
        tasks.append((item["asin"], sf))

print("⚡ Running Parallel Multi-Threaded Audit of ALL 9 Global Amazon Storefronts...\n")

with ThreadPoolExecutor(max_workers=15) as executor:
    results = list(executor.map(check_single, tasks))

matrix = {item["asin"]: [] for item in asins}
for asin, code, is_active in results:
    if is_active:
        matrix[asin].append(code)

print("==================================================")
print("🏆 EMPIRICAL 9-STOREFRONT DIRECT REGIONS MATRIX:")
print("==================================================")
print(json.dumps(matrix, indent=2))

with open("global_direct_matrix.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, indent=2)

print("\nSaved global_direct_matrix.json!")
