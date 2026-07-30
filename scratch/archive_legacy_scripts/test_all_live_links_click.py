import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

live_products = [
    "B0DZD1X83N", "B0BZXNSW5K", "B0D1FRDFFX", "B0C2YLN3H4",
    "B0GYDXHF4G", "B0FXLYXM32", "B07HP22QTZ", "B0D8P8CSYP",
    "B0DLN5S5K9", "B0DXKGL1T2"
]

base_live = "https://adityasnalawade742-design.github.io/bridge_"

print("🌐 Simulating Real User Clicks Across ALL 10 Live Landing Pages on GitHub Pages...\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for asin in live_products:
        url = f"{base_live}{asin}.html"
        print(f"📦 Product: bridge_{asin}.html")
        page.goto(url)
        page.wait_for_timeout(500)
        
        buy_href = page.get_attribute("#buyBtn", "href")
        buy_text = page.inner_text("#buyBtnText").strip()
        notice_disp = page.eval_on_selector("#geoNoticeBox", "el => getComputedStyle(el).display")
        
        print(f"   Button Link:   {buy_href}")
        print(f"   Button Text:   {buy_text}")
        print(f"   Notice Display:{notice_disp}\n")
        
    browser.close()

print("🏁 Audit Completed Successfully!")
