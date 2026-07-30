import sys
import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

asins = [
    "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4", "B07HP22QTZ",
    "B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP", "B0DZD1X83N"
]

domains = [
    ("US", "https://www.amazon.com/dp/"),
    ("UK", "https://www.amazon.co.uk/dp/"),
    ("IN", "https://www.amazon.in/dp/"),
    ("DE", "https://www.amazon.de/dp/"),
    ("CA", "https://www.amazon.ca/dp/"),
    ("AU", "https://www.amazon.com.au/dp/"),
    ("JP", "https://www.amazon.co.jp/dp/")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

verified_matrix = {}

print("==================================================")
print("🔍 VERIFYING EXACT AMAZON DIRECT /DP/ LISTING EXISTENCE ACROSS ALL REGIONS")
print("==================================================")

for asin in asins:
    verified_matrix[asin] = []
    print(f"\n📦 ASIN [{asin}]:")
    for code, prefix in domains:
        url = f"{prefix}{asin}"
        is_live_listing = False
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200:
                # Check if it's a real product page vs Amazon 404 "Looking for something?" page
                if "a-price" in r.text or "add-to-cart-button" in r.text or "dp-container" in r.text or "productTitle" in r.text:
                    is_live_listing = True
        except Exception:
            pass

        if is_live_listing:
            verified_matrix[asin].append(code)
            print(f"   • {code:2s} ({prefix}): ✅ DIRECT ASIN PAGE LIVE")
        else:
            print(f"   • {code:2s} ({prefix}): 🔴 NOT DIRECT (WILL USE SEARCH FALLBACK)")

# Save verified matrix to global_direct_matrix.json
matrix_file = repo_dir / "global_direct_matrix.json"
with open(matrix_file, "w", encoding="utf-8") as f:
    json.dump(verified_matrix, f, indent=2)

print("\n==================================================")
print(" ✅ Updated global_direct_matrix.json with 100% empirically verified live Amazon direct listings!")
print("==================================================")
