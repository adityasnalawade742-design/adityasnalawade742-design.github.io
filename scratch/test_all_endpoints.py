"""
Comprehensive Audit & Test for ALL Real Endpoints in Web Console Server
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("AUDITING ALL WEB CONSOLE ENDPOINTS")
print("=" * 70)

passed = 0
failed = 0

def run_test(name, method, path, params=None, body=None):
    global passed, failed
    url = f"{BASE_URL}{path}"
    print(f"\n[TEST] {name} -> {method} {path}")
    try:
        if method == "GET":
            resp = requests.get(url, params=params, timeout=10)
        else:
            resp = requests.post(url, params=params, json=body, timeout=10)

        print(f"       HTTP Code : {resp.status_code}")
        if resp.status_code == 200:
            try:
                data = resp.json()
                st = data.get('status', 'OK')
                print(f"       Status    : {st}")
                print(f"       Sample    : {str(data)[:100]}...")
                passed += 1
            except Exception:
                print(f"       Text      : {resp.text[:100]}...")
                passed += 1
        else:
            print(f"  [!] FAIL ({resp.status_code}): {resp.text[:150]}")
            failed += 1
    except Exception as e:
        print(f"  [!] EXCEPTION: {e}")
        failed += 1

# GET Endpoints
run_test("Console UI", "GET", "/admin_console.html")
run_test("Homepage Products", "GET", "/api/homepage_products")
run_test("Discover Products", "GET", "/api/discover", params={"query": "mushroom lamp", "count": 2})
run_test("Fetch Image", "GET", "/api/fetch_image", params={"asin": "B0CLV5M9TF"})
run_test("Task Status", "GET", "/api/task_status")
run_test("Batch Status", "GET", "/api/batch_status")
run_test("Global Tag Defaults", "GET", "/api/global_tag_defaults")
run_test("Matrix Data", "GET", "/api/matrix")
run_test("Campaign Tracker", "GET", "/api/campaign_tracker")
run_test("Console Logs", "GET", "/api/logs")

# POST Endpoints
run_test("Prepare n8n Batch", "POST", "/api/prepare_n8n_batch", body={"products": [{"asin": "B0TEST1234", "title": "Test"}]})
run_test("Reject Product", "POST", "/api/reject_product", body={"asin": "B0TEST1234", "title": "Test Product"})

print("\n" + "=" * 70)
print(f"AUDIT COMPLETE: Passed {passed} / {passed+failed} endpoints")
print("=" * 70)
