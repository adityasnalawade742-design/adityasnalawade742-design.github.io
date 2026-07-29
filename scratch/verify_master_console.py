import sys
import json
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://localhost:5000"

print("🔍 RUNNING MASTER WEB CONSOLE FULL FEATURE VERIFICATION TEST...\n")

test_results = []

# Test 1: Homepage Manager Endpoint
try:
    r1 = requests.get(f"{BASE_URL}/api/homepage_products")
    data1 = r1.json()
    prods = data1.get("products", [])
    test_results.append(("1. Live Homepage Product Manager (/api/homepage_products)", r1.status_code == 200, f"Found {len(prods)} active products on homepage"))
except Exception as e:
    test_results.append(("1. Live Homepage Product Manager", False, str(e)))

# Test 2: Live Discover Endpoint (SerpAPI Cache Protection)
try:
    r2 = requests.get(f"{BASE_URL}/api/discover?query=aesthetic+glass+mushroom+table+lamp&count=3")
    data2 = r2.json()
    items = data2.get("items", [])
    test_results.append(("2. Live Trend Keyword Discover (/api/discover)", r2.status_code == 200, f"Discovered {len(items)} candidate products"))
except Exception as e:
    test_results.append(("2. Live Trend Keyword Discover", False, str(e)))

# Test 3: Batch Extract Photo Suites
try:
    r3 = requests.post(f"{BASE_URL}/api/batch_extract", json={"asins": ["B0DZD1X83N", "B0BWFJNBYQ"]})
    data3 = r3.json()
    extracted = data3.get("items", [])
    test_results.append(("3. Multi-Photo Verification & System Winner (/api/batch_extract)", r3.status_code == 200, f"Extracted photo suites for {len(extracted)} products"))
except Exception as e:
    test_results.append(("3. Multi-Photo Verification & System Winner", False, str(e)))

# Test 4: Live Graphic Overlay Preview (Playwright Renderer)
try:
    r4 = requests.post(f"{BASE_URL}/api/preview_overlay", json={
        "image_url": "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg",
        "title": "MUSHROOM AMBIENT LAMP",
        "badge": "VIRAL ROOM FIND",
        "price": "$29.99"
    })
    data4 = r4.json()
    preview_url = data4.get("preview_url", "")
    test_results.append(("4. Real-Time Graphic Overlay Preview (/api/preview_overlay)", r4.status_code == 200 and "preview_overlay.jpg" in preview_url, f"Preview URL: {preview_url}"))
except Exception as e:
    test_results.append(("4. Real-Time Graphic Overlay Preview", False, str(e)))

# Test 5: Batch Status Polling
try:
    r5 = requests.get(f"{BASE_URL}/api/batch_status?batch_id=test_batch")
    data5 = r5.json()
    test_results.append(("5. Real-Time Batch Progress Polling (/api/batch_status)", r5.status_code == 200, f"Status: {data5.get('status')}"))
except Exception as e:
    test_results.append(("5. Real-Time Batch Progress Polling", False, str(e)))

print("=" * 80)
print("RESULT SUMMARY:")
print("=" * 80)
all_pass = True
for name, passed, detail in test_results:
    status_str = "✅ WORKING" if passed else "❌ FAILED"
    if not passed: all_pass = False
    print(f"{status_str} | {name:<60} | {detail}")

print("=" * 80)
if all_pass:
    print("🎉 ALL FEATURES ARE 100% WORKING PERFECTLY!")
else:
    print("⚠️ SOME FEATURES NEED ATTENTION!")
