import sys
import json
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:5000"

print(f"🔍 Testing All Web Console API Endpoints at {BASE_URL}...\n")

# 1. Test Console UI HTML
try:
    r1 = requests.get(f"{BASE_URL}/")
    print(f"1. GET / (Admin Console UI): HTTP {r1.status_code} | Length: {len(r1.text)} bytes")
except Exception as e:
    print(f"1. GET / Error: {e}")

# 2. Test Discover API
try:
    r2 = requests.get(f"{BASE_URL}/api/discover?query=white+ceramic+donut+vase&count=3")
    data2 = r2.json()
    items = data2.get("items", [])
    print(f"2. GET /api/discover: HTTP {r2.status_code} | Discovered {len(items)} items")
    if items:
        test_asin = items[0]["asin"]
        print(f"   -> Top Discovered ASIN: {test_asin} ('{items[0]['title'][:40]}...')")
except Exception as e:
    print(f"2. GET /api/discover Error: {e}")

# 3. Test Extract Single API
try:
    r3 = requests.get(f"{BASE_URL}/api/extract?target=B0DZD1X83N")
    data3 = r3.json()
    print(f"3. GET /api/extract (Single ASIN): HTTP {r3.status_code} | Winner Photo: {data3.get('winner_photo')[:45]}...")
except Exception as e:
    print(f"3. GET /api/extract Error: {e}")

# 4. Test Batch Extract API
try:
    r4 = requests.post(f"{BASE_URL}/api/batch_extract", json={"asins": ["B0DZD1X83N", "B0BWFJNBYQ"]})
    data4 = r4.json()
    batch_items = data4.get("items", [])
    print(f"4. POST /api/batch_extract: HTTP {r4.status_code} | Extracted {len(batch_items)} photo suites")
except Exception as e:
    print(f"4. POST /api/batch_extract Error: {e}")

# 5. Test Batch Status API
try:
    r5 = requests.get(f"{BASE_URL}/api/batch_status?batch_id=test_batch")
    data5 = r5.json()
    print(f"5. GET /api/batch_status: HTTP {r5.status_code} | Response: {data5}")
except Exception as e:
    print(f"5. GET /api/batch_status Error: {e}")

print("\n🎉 Web Console Full Suite Test Finished!")
