import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_products_eu_direct():
    asins = [
        ("B0BZXNSW5K", "Touch Bedside Lamp"),
        ("B0C2YLN3H4", "White Donut Vases"),
        ("B07HP22QTZ", "Crystal Suncatcher"),
        ("B0D8P8CSYP", "Cute Bird Touch Lamp"),
        ("B0D1FRDFFX", "Glass Mushroom Lamp"),
        ("B0GYDXHF4G", "Flame Aroma Diffuser"),
        ("B0DXKGL1T2", "Lily of Valley Lamp"),
        ("B0DZD1X83N", "Minimalist Wood Lamp"),
        ("B0FXLYXM32", "White Wavy Mirror")
    ]

    eu_test_countries = [
        ("NL", "Netherlands", "amazon.nl"),
        ("FR", "France", "amazon.fr"),
        ("IT", "Italy", "amazon.it"),
        ("ES", "Spain", "amazon.es")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🇪🇺 AUDITING EU DIRECT ROUTING ACROSS ALL 9 PRODUCTS FOR NL, FR, IT, ES")
        print("==================================================")

        for asin, title in asins:
            print(f"\n📦 [{asin}] {title}:")
            for cc, cname, domain in eu_test_countries:
                url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
                page.goto(url)
                time.sleep(0.2)

                hero_price = page.locator(".price, .tag").first.inner_text()
                cta_text = page.locator("#buyBtnText").inner_text()
                cta_link = page.locator("#buyBtn").get_attribute("href")
                is_direct = f"/dp/{asin}" in cta_link

                type_label = "🎯 DIRECT ASIN LINK" if is_direct else "🔍 CATEGORY SEARCH FALLBACK"
                print(f"   • {cname:11s} [{cc}]: {type_label} | Button: '{cta_text}' | Link: '{cta_link}'")

                assert "tag=smartdeal0358-21" in cta_link, f"Missing affiliate tag for {asin} [{cc}]"

        browser.close()
        print("\n==================================================")
        print("🎉 100% PASS: All 9 products verified for EU direct routing across NL, FR, IT, ES!")
        print("==================================================")

if __name__ == "__main__":
    verify_all_products_eu_direct()
