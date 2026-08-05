import sys
import json
import urllib.request
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent
registry_file = repo_dir / "product_price_registry.json"
matrix_file = repo_dir / "global_direct_matrix.json"

with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

domain_map = {
    "US": "amazon.com",
    "IN": "amazon.in",
    "UK": "amazon.co.uk",
    "DE": "amazon.de",
    "CA": "amazon.ca",
    "AU": "amazon.com.au",
    "JP": "amazon.co.jp",
    "SE": "amazon.se"
}

print("==================================================")
print("🔍 TESTING REAL DIRECT LISTING HTTP STATUS CODES FOR ALL PRODUCTS")
print("==================================================")

clean_matrix = {}

for asin, item in registry.items():
    print(f"\n📦 Testing ASIN [{asin}] - {item.get('title', '')[:35]}...")
    valid_direct_regions = ["US"]  # US is master source
    regional_asins = item.get("regional_asins", {})
    
    for cc, domain in domain_map.items():
        if cc == "US":
            continue
        
        target_asin = regional_asins.get(cc) or asin
        url = f"https://www.{domain}/dp/{target_asin}"
        
        # Test HTTP response code
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            resp = urllib.request.urlopen(req, timeout=5)
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Check for Amazon 404 indicators
            if "The Web address you entered is not a functioning page" in html or "Looking for something?" in html or resp.status != 200:
                print(f"   ❌ {cc} ({domain}/dp/{target_asin}): 404 Not Found")
            else:
                valid_direct_regions.append(cc)
                print(f"   ✅ {cc} ({domain}/dp/{target_asin}): 200 OK Direct Listing")
        except Exception as e:
            print(f"   ❌ {cc} ({domain}/dp/{target_asin}): Error / 404 ({e})")

    clean_matrix[asin] = valid_direct_regions
    item["direct_regions"] = valid_direct_regions
    print(f"   🎯 Verified Direct Regions for [{asin}]: {valid_direct_regions}")

# Save updated global_direct_matrix.json & product_price_registry.json
matrix_file.write_text(json.dumps(clean_matrix, indent=2, ensure_ascii=False), encoding="utf-8")
registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

print("\n==================================================")
print("🏆 DIRECT MATRIX AUDIT COMPLETE! UPDATED global_direct_matrix.json")
print("==================================================")
