import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

live_products = [
    {"asin": "B0DZD1X83N", "name": "Minimalist Lamp"},
    {"asin": "B0BZXNSW5K", "name": "Bedside Touch Lamp"},
    {"asin": "B0D1FRDFFX", "name": "Glass Mushroom Lamp"}
]

base_live = "https://adityasnalawade742-design.github.io/bridge_"

print("🌐 Testing LIVE GitHub Pages URLs for all 3 products...\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for item in live_products:
        asin = item["asin"]
        url_in = f"{base_live}{asin}.html?country=IN"
        print(f"Testing Live India URL: {url_in}")
        page.goto(url_in)
        page.wait_for_timeout(1000)
        
        btn_href = page.get_attribute("#buyBtn", "href")
        btn_text = page.inner_text("#buyBtnText").strip()
        box_disp = page.eval_on_selector("#geoNoticeBox", "el => getComputedStyle(el).display")
        
        print(f"   -> Live Link:   {btn_href}")
        print(f"   -> Live Text:   {btn_text}")
        print(f"   -> Live Notice: display={box_disp}\n")
        
    browser.close()
