import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_currencies_on_all_landing_pages():
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

    currencies = [
        ("US", "USD", "$"),
        ("UK", "GBP", "£"),
        ("IN", "INR", "₹"),
        ("DE", "EUR", "€"),
        ("CA", "CAD", "CA$"),
        ("AU", "AUD", "A$"),
        ("JP", "JPY", "¥"),
        ("SE", "SEK", "kr"),
        ("BR", "BRL", "R$"),
        ("AE", "AED", "AED"),
        ("KR", "KRW", "₩")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🌐 VERIFYING ALL 9 LANDING PAGES ACROSS 11 WORLD CURRENCIES")
        print("==================================================")

        total_checks = 0
        passed_checks = 0

        for asin, title in asins:
            print(f"\n📦 [{asin}] {title}:")
            for cc, curr_code, expected_sym in currencies:
                total_checks += 1
                url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
                page.goto(url)
                time.sleep(0.2)

                hero_price_tag = page.locator(".price, .tag").first.inner_text()
                cta_link = page.locator("#buyBtn").get_attribute("href")

                print(f"   • Country {cc:2s} ({curr_code:3s}): '{hero_price_tag}'")
                tag_upper = hero_price_tag.upper()
                assert expected_sym.upper() in tag_upper or "NOT AVAILABLE" in tag_upper or curr_code.upper() in tag_upper or "NOT AVAILABLE" in tag_upper, f"Price format error for {asin} [{cc}]: '{hero_price_tag}'"
                passed_checks += 1

        browser.close()

        print("\n==================================================")
        print(f"🎉 100% PASS: All {passed_checks}/{total_checks} currency checks verified across 9 landing pages!")
        print("==================================================")

if __name__ == "__main__":
    verify_all_currencies_on_all_landing_pages()
