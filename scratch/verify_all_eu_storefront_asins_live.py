import sys
import json
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

asins = [
    "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4", "B07HP22QTZ",
    "B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP", "B0DZD1X83N"
]

eu_domains = [
    ("DE", "amazon.de"),
    ("NL", "amazon.nl"),
    ("FR", "amazon.fr"),
    ("IT", "amazon.it"),
    ("ES", "amazon.es"),
    ("SE", "amazon.se")
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

print("==================================================")
print("🔍 TESTING LIVE AMAZON EU STOREFRONTS FOR EVERY SINGLE ASIN")
print("==================================================")

verified_matrix = {}

for asin in asins:
    verified_matrix[asin] = []
    print(f"\n📦 ASIN [{asin}]:")
    for code, domain in eu_domains:
        url = f"https://www.{domain}/dp/{asin}"
        is_live = False
        try:
            r = requests.get(url, headers=headers, timeout=6)
            if r.status_code == 200:
                # Must be a real product page, not Amazon's 404 "Looking for something?" page
                if "a-price" in r.text or "add-to-cart-button" in r.text or "productTitle" in r.text or "dp-container" in r.text:
                    is_live = True
        except Exception:
            pass

        if is_live:
            verified_matrix[asin].append(code)
            print(f"   • {code:2s} ({domain:12s}): ✅ LIVE DIRECT PRODUCT PAGE")
        else:
            print(f"   • {code:2s} ({domain:12s}): 🔴 NOT DIRECT (SAFE SEARCH FALLBACK)")

print("\n==================================================")
print("📊 EMPIRICALLY VERIFIED EU DIRECT MATRIX RESULT:")
print(json.dumps(verified_matrix, indent=2))
print("==================================================")
