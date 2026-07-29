import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

asin = "B0D8P8CSYP"
base_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"

test_countries = [
    ("US", "United States", "amazon.com/dp/B0D8P8CSYP?tag=smartdeal0358-21"),
    ("IN", "India", "amazon.in/dp/B0D8P8CSYP?tag=smartdeal0358-21"),
    ("GB", "United Kingdom", "amazon.co.uk/s?k=Cute%20Bird%20Dimmable%20Touch%20Night%20Lamp&tag=smartdeal0358-21"),
    ("DE", "Germany", "amazon.de/s?k=Cute%20Bird%20Dimmable%20Touch%20Night%20Lamp&tag=smartdeal0358-21"),
    ("CA", "Canada", "amazon.ca/s?k=Cute%20Bird%20Dimmable%20Touch%20Night%20Lamp&tag=smartdeal0358-21"),
    ("JP", "Japan", "amazon.co.jp/s?k=Cute%20Bird%20Dimmable%20Touch%20Night%20Lamp&tag=smartdeal0358-21"),
]

print("🧪 TESTING MULTI-COUNTRY GEO-REDIRECTOR ON LIVE GITHUB PAGES LANDING PAGE...\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for cc, name, expected_url_snippet in test_countries:
        target_url = f"{base_url}?country={cc}"
        page.goto(target_url, wait_until="networkidle")
        
        buy_btn = page.query_selector("#buyBtn")
        href = buy_btn.get_attribute("href") if buy_btn else ""
        btn_text = buy_btn.inner_text() if buy_btn else ""
        
        has_tag = "tag=smartdeal0358-21" in href
        print(f"🌍 Country: {cc} ({name})")
        print(f"   Target URL Tested: {target_url}")
        print(f"   Button Href:       {href}")
        print(f"   Button Text:       {btn_text.strip()}")
        print(f"   Affiliate Tag:     {'✅ YES (smartdeal0358-21)' if has_tag else '❌ MISSING'}\n")

    browser.close()

print("==================================================")
print("🏆 PLAYWRIGHT MULTI-COUNTRY REDIRECT TEST COMPLETE!")
print("==================================================")
