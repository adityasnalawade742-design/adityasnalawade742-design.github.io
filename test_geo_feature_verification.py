import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

file_path = "file:///G:/CLI/pinterest-auto-affiliate/bridge_B0DZD1X83N.html"

test_cases = [
    {"name": "India (IN)", "url": file_path + "?country=IN", "expected_btn": "SEARCH LOCAL DEALS ON AMAZON INDIA (₹)", "expected_domain": "amazon.in"},
    {"name": "Sweden (SE)", "url": file_path + "?country=SE", "expected_btn": "SEARCH LOCAL DEALS ON AMAZON SWEDEN (kr)", "expected_domain": "amazon.se"},
    {"name": "Germany (DE)", "url": file_path + "?country=DE", "expected_btn": "SEARCH LOCAL DEALS ON AMAZON GERMANY (€)", "expected_domain": "amazon.de"},
    {"name": "United Kingdom (UK)", "url": file_path + "?country=UK", "expected_btn": "SEARCH LOCAL DEALS ON AMAZON UK (£)", "expected_domain": "amazon.co.uk"},
    {"name": "United States (US)", "url": file_path + "?country=US", "expected_btn": "CHECK DEAL ON AMAZON", "expected_domain": "amazon.com"}
]

print("🧪 Running Playwright Headless Verification Test for Geo-Redirector Feature...\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    all_passed = True
    for tc in test_cases:
        print(f"Testing Region: {tc['name']} -> {tc['url']}")
        page.goto(tc['url'])
        page.wait_for_timeout(500)
        
        buy_href = page.get_attribute("#buyBtn", "href")
        buy_text = page.inner_text("#buyBtnText").strip()
        geo_box_display = page.eval_on_selector("#geoNoticeBox", "el => getComputedStyle(el).display")
        
        print(f"   Button Link: {buy_href}")
        print(f"   Button Text: {buy_text}")
        print(f"   Notice Box Display: {geo_box_display}")
        
        domain_match = tc['expected_domain'] in buy_href
        text_match = tc['expected_btn'] in buy_text
        
        if domain_match and text_match:
            print("   ✅ PASSED!\n")
        else:
            print(f"   ❌ FAILED! Expected domain '{tc['expected_domain']}' and text '{tc['expected_btn']}'\n")
            all_passed = False
            
    browser.close()

if all_passed:
    print("🎉 ALL TEST CASES PASSED! Universal Multi-Region Geo-Redirector feature is 100% verified working!")
else:
    print("⚠️ Some test cases failed verification.")
