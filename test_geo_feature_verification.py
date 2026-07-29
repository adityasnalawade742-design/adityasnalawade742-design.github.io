import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

products = ["B0DZD1X83N", "B0BZXNSW5K", "B0D1FRDFFX"]
base_url = "file:///G:/CLI/pinterest-auto-affiliate/bridge_"

regions = [
    {"code": "IN", "name": "India", "expected_domain": "amazon.in", "expected_text": "SEARCH LOCAL DEALS ON AMAZON INDIA (₹)", "box": "flex"},
    {"code": "SE", "name": "Sweden", "expected_domain": "amazon.se", "expected_text": "SEARCH LOCAL DEALS ON AMAZON SWEDEN (kr)", "box": "flex"},
    {"code": "DE", "name": "Germany", "expected_domain": "amazon.de", "expected_text": "SEARCH LOCAL DEALS ON AMAZON GERMANY (€)", "box": "flex"},
    {"code": "UK", "name": "United Kingdom", "expected_domain": "amazon.co.uk", "expected_text": "SEARCH LOCAL DEALS ON AMAZON UK (£)", "box": "flex"},
    {"code": "US", "name": "United States", "expected_domain": "amazon.com", "expected_text": "CHECK DEAL ON AMAZON", "box": "none"}
]

print("🧪 Running Comprehensive Playwright Verification Across ALL Product Landing Pages...\n")

total_tests = 0
passed_tests = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for asin in products:
        print(f"==================================================")
        print(f"📦 TESTING PRODUCT ASIN: {asin}")
        print(f"==================================================")
        
        for r in regions:
            total_tests += 1
            url = f"{base_url}{asin}.html?country={r['code']}"
            page.goto(url)
            page.wait_for_timeout(400)
            
            buy_href = page.get_attribute("#buyBtn", "href")
            buy_text = page.inner_text("#buyBtnText").strip()
            geo_box_display = page.eval_on_selector("#geoNoticeBox", "el => getComputedStyle(el).display")
            
            domain_ok = r['expected_domain'] in buy_href
            text_ok = r['expected_text'] in buy_text
            box_ok = (geo_box_display == r['box'])
            
            status = "✅ PASSED" if (domain_ok and text_ok and box_ok) else "❌ FAILED"
            if domain_ok and text_ok and box_ok:
                passed_tests += 1
                
            print(f"  Region [{r['code']}] {r['name']}: {status}")
            print(f"     -> Link:   {buy_href}")
            print(f"     -> Label:  {buy_text}")
            print(f"     -> Notice: display={geo_box_display}\n")
            
    browser.close()

print(f"==================================================")
print(f"🏆 VERIFICATION SUMMARY: {passed_tests} / {total_tests} Tests Passed!")
if passed_tests == total_tests:
    print("🎉 PERFECT SCORE! Every single product page passed all multi-region tests with 100% precision!")
else:
    print("⚠️ Some tests failed.")
