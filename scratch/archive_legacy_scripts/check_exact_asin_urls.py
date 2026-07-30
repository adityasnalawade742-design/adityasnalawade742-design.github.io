import sys
import requests

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asin = "B0C2YLN3H4"
stores = [
    ("US", "amazon.com"),
    ("IN", "amazon.in"),
    ("UK", "amazon.co.uk"),
    ("DE", "amazon.de"),
    ("SE", "amazon.se"),
    ("SG", "amazon.sg"),
    ("CA", "amazon.ca"),
    ("AU", "amazon.com.au"),
    ("JP", "amazon.co.jp"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"🔍 AUDITING EXACT ASIN HTTP STATUS FOR B0C2YLN3H4 ACROSS ALL 9 AMAZON STORES...\n")

working_regions = []

for code, domain in stores:
    url = f"https://www.{domain}/dp/{asin}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        is_live = (r.status_code == 200) and ("Looking for something" not in r.text) and ("Page Not Found" not in r.text)
        print(f"  [{code}] {domain:15s} -> Status: {r.status_code} | Live Listing: {'✅ YES' if is_live else '❌ 404 NOT LISTED'}")
        if is_live:
            working_regions.append(code)
    except Exception as e:
        print(f"  [{code}] {domain:15s} -> Error: {e}")

print("\n==================================================")
print(f"🏆 EXACT DIRECT REGIONS LIST FOR B0C2YLN3H4:")
print(f"   {working_regions}")
print("==================================================")
