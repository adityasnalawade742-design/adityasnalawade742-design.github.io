import sys
sys.path.append("G:/CLI/pinterest-auto-affiliate")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import requests
from config import SERPAPI_KEYS

print(f"Total Configured SerpAPI Keys: {len(SERPAPI_KEYS)}\n")

for idx, key in enumerate(SERPAPI_KEYS, 1):
    print(f"--- Testing Key #{idx}: {key[:8]}...{key[-8:]} ---")
    url = f"https://serpapi.com/account.json?api_key={key}"
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            searches_left = data.get("total_searches_left") or data.get("searches_per_month")
            plan = data.get("plan_name", "Free")
            print(f"   ✅ Key #{idx} is WORKING! Plan: {plan} | Searches Left: {searches_left}")
        else:
            print(f"   ❌ Key #{idx} API Error HTTP {r.status_code}: {r.text[:100]}")
    except Exception as e:
        print(f"   ⚠️ Key #{idx} Exception: {e}")
