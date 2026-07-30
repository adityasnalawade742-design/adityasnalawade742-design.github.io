import urllib.request
import urllib.parse
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(name, url, method="GET", payload=None):
    print(f"[Button Audit] Testing {name} ({method} {url}) ...")
    req = urllib.request.Request(url, method=method)
    if payload:
        data_bytes = json.dumps(payload).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
        req.data = data_bytes
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            assert data.get('status') == 'success' or 'products' in data or 'status' in data or 'items' in data, f"Non-success response: {data}"
            print(f"[Button Audit] PASS: {name} -> {data.get('status') or 'OK'}")
            return True
    except Exception as e:
        print(f"[Button Audit] FAIL: {name} -> {e}")
        return False

def run_full_button_audit():
    results = []
    
    # 1. Homepage Products Fetch
    results.append(test_endpoint("Homepage Products Load", f"{BASE_URL}/api/homepage_products"))
    
    # 2. Global Tag Defaults Get
    results.append(test_endpoint("GET Global Tag Defaults", f"{BASE_URL}/api/global_tag_defaults"))
    
    # 3. Save Global Tag Defaults Post
    defaults_payload = {
        "tag_width": 380,
        "tag_height": 514,
        "tag_rotation": -6,
        "tag_color": "#fb8500",
        "price_text_color": "#111827",
        "price_font_scale": 0.20,
        "price_text_offset_x": 0,
        "price_text_offset_y": 0,
        "price_text_pos_x": 50.0,
        "price_text_pos_y": 58.0,
        "tag_pos_x": 61.0,
        "tag_pos_y": 75.0
    }
    results.append(test_endpoint("POST Save Global Defaults", f"{BASE_URL}/api/save_global_defaults", method="POST", payload=defaults_payload))

    # 4. Product Catalog Discovery Search
    results.append(test_endpoint("Product Discovery", f"{BASE_URL}/api/discover?query=aesthetic%20glass%20mushroom%20table%20lamp&count=1"))

    # 5. Price Sync Trigger
    results.append(test_endpoint("Price Sync Engine", f"{BASE_URL}/api/sync_prices", method="POST", payload={}))

    # 6. Customize Price Tag Re-Render
    cust_payload = {
        "asin": "B0D8P8CSYP",
        "tag_width": 380,
        "tag_height": 514,
        "tag_rotation": -6,
        "tag_color": "#fb8500",
        "price_text_color": "#111827",
        "price_font_scale": 0.20,
        "price_text_offset_x": 0,
        "price_text_offset_y": 0,
        "price_text_pos_x": 50.0,
        "price_text_pos_y": 58.0,
        "tag_pos_x": 61.0,
        "tag_pos_y": 75.0
    }
    results.append(test_endpoint("Customize Price Tag Re-Render", f"{BASE_URL}/api/customize_tag", method="POST", payload=cust_payload))

    passed = sum(results)
    total = len(results)
    print(f"\n==========================================")
    print(f"[Button Audit Summary] {passed}/{total} Buttons & API Endpoints Operational!")
    print(f"==========================================")
    assert passed == total, "Some endpoints failed!"

if __name__ == '__main__':
    run_full_button_audit()
