import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "https://adityasnalawade742-design.github.io/bridge_B0DZD1X83N.html"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    res = page.goto(url)
    title = page.title()
    price = page.locator(".price, .tag").first.inner_text()
    cta = page.locator("#buyBtnText").inner_text()

    print("==================================================")
    print("🌐 LIVE PLAYWRIGHT VERIFICATION FOR bridge_B0DZD1X83N.html")
    print("==================================================")
    print(f" • HTTP Status Code: {res.status}")
    print(f" • Page Title:       '{title}'")
    print(f" • Hero Price Tag:   '{price}'")
    print(f" • CTA Button Text:  '{cta}'")
    browser.close()
