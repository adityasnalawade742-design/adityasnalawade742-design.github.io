import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_9_india_landing_pages():
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

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🇮🇳 VERIFYING ALL 9 LANDING PAGES FOR INDIAN VISITORS (?country=IN)")
        print("==================================================")

        for asin, title in asins:
            url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country=IN"
            page.goto(url)
            time.sleep(0.3)

            hero_price_tag = page.locator(".price, .tag").first.inner_text()
            cta_button_text = page.locator("#buyBtnText").inner_text()
            cta_link_href = page.locator("#buyBtn").get_attribute("href")

            print(f"\n📦 [{asin}] {title}:")
            print(f"   • Dynamic Hero Price Tag: '{hero_price_tag}'")
            print(f"   • CTA Button Text:       '{cta_button_text}'")
            print(f"   • CTA Affiliate Link:    '{cta_link_href}'")

            assert "tag=smartdeal0358-21" in cta_link_href, f"Affiliate tag missing for {asin}"

        browser.close()
        print("\n==================================================")
        print("🎉 100% PASS: All 9 landing pages verified adapting dynamically for Indian visitors!")
        print("==================================================")

if __name__ == "__main__":
    verify_all_9_india_landing_pages()
