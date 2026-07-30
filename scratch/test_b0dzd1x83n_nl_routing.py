import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "file:///G:/CLI/pinterest-auto-affiliate/bridge_B0DZD1X83N.html?country=NL"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    
    price = page.locator(".price, .tag").first.inner_text()
    cta_text = page.locator("#buyBtnText").inner_text()
    cta_link = page.locator("#buyBtn").get_attribute("href")

    print("==================================================")
    print("🇳🇱 VERIFYING NETHERLANDS ROUTING FOR B0DZD1X83N")
    print("==================================================")
    print(f" • Price Tag:       '{price}'")
    print(f" • CTA Button Text: '{cta_text}'")
    print(f" • Destination Link: {cta_link}")

    browser.close()
