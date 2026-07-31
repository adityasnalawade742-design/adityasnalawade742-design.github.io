import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

eu_countries = [
    ("NL", "Amazon Netherlands", "amazon.nl"),
    ("DE", "Amazon Germany", "amazon.de"),
    ("FR", "Amazon France", "amazon.fr"),
    ("IT", "Amazon Italy", "amazon.it"),
    ("ES", "Amazon Spain", "amazon.es"),
    ("SE", "Amazon Sweden", "amazon.se")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("==================================================")
    print("🇪🇺 LIVE DESTINATION LINKS FOR CUTE BIRD LAMP (B0D8P8CSYP)")
    print("==================================================")

    for code, name, domain in eu_countries:
        url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_B0D8P8CSYP.html?country={code}"
        page.goto(url)
        
        price = page.locator(".price, .tag").first.inner_text()
        cta_text = page.locator("#buyBtnText").inner_text()
        cta_link = page.locator("#buyBtn").get_attribute("href")

        print(f"\n📍 Country: {name} ({code})")
        print(f"   • Price Tag:       '{price}'")
        print(f"   • CTA Button Text: '{cta_text}'")
        print(f"   • Destination Link: {cta_link}")

    browser.close()
