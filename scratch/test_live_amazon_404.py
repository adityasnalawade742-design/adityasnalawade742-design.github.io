import sys
import json
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
matrix_file = repo_dir / "global_direct_matrix.json"
registry_file = repo_dir / "product_price_registry.json"

asins = [
    "B0DZD1X83N", "B0BZXNSW5K", "B0D1FRDFFX", "B0C2YLN3H4",
    "B0GYDXHF4G", "B0FXLYXM32", "B07HP22QTZ", "B0D8P8CSYP", "B0DXKGL1T2"
]

domains = [
    ("US", "https://www.amazon.com/dp/"),
    ("CA", "https://www.amazon.ca/dp/"),
    ("UK", "https://www.amazon.co.uk/dp/"),
    ("DE", "https://www.amazon.de/dp/"),
    ("FR", "https://www.amazon.fr/dp/"),
    ("IT", "https://www.amazon.it/dp/"),
    ("ES", "https://www.amazon.es/dp/"),
    ("NL", "https://www.amazon.nl/dp/"),
    ("SE", "https://www.amazon.se/dp/"),
    ("IN", "https://www.amazon.in/dp/"),
    ("JP", "https://www.amazon.co.jp/dp/"),
    ("AU", "https://www.amazon.com.au/dp/")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

live_matrix = {}

print("==================================================")
print("🔍 AUDITING LIVE AMAZON DIRECT LISTINGS FOR 404 ERRORS")
print("==================================================")

for asin in asins:
    live_matrix[asin] = []
    print(f"\n📦 ASIN [{asin}]:")
    for cc, prefix in domains:
        url = f"{prefix}{asin}"
        is_live = False
        try:
            r = requests.get(url, headers=headers, timeout=5)
            # Check for Amazon 404 text
            if r.status_code == 200 and "Looking for something?" not in r.text and "looking for something else" not in r.text.lower():
                if "dp-container" in r.text or "productTitle" in r.text or "a-price" in r.text or "add-to-cart-button" in r.text:
                    is_live = True
        except Exception:
            pass

        if is_live:
            live_matrix[asin].append(cc)
            print(f"   • {cc:2s}: ✅ LIVE DIRECT LISTING ({url})")
        else:
            print(f"   • {cc:2s}: 🔴 404 / UNLISTED (Uses Search Fallback)")

# Save true empirical matrix
with open(matrix_file, "w", encoding="utf-8") as f:
    json.dump(live_matrix, f, indent=2)

print("\n==================================================")
print(" ✅ Empirical global_direct_matrix.json updated!")
print("==================================================")
