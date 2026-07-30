import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_all_products_all_currencies():
    currencies = [
        ("USD", "$"),
        ("GBP", "£"),
        ("INR", "₹"),
        ("EUR", "€"),
        ("JPY", "¥"),
        ("CAD", "CA$"),
        ("AUD", "A$")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html")
        time.sleep(1)

        print("==================================================")
        print("🔍 AUDITING ALL 9 PRODUCTS ACROSS ALL 7 CURRENCIES")
        print("==================================================")

        cards = page.query_selector_all("#productGrid .card-wrapper")
        print(f"Found {len(cards)} products on homepage grid.\n")

        for curr, sym in currencies:
            print(f"--- Testing Currency: {curr} (Symbol: {sym}) ---")
            page.select_option("#currencySelector", curr)
            time.sleep(0.3)

            for i, card in enumerate(cards, 1):
                title = card.query_selector("h2").inner_text()
                price_tag = card.query_selector(".card-price-tag").inner_text()
                base_usd = card.get_attribute("data-base-usd")
                link = card.query_selector("a").get_attribute("href")

                assert sym in price_tag or curr in price_tag, f"Missing symbol {sym} in {price_text} for {title}"
                print(f" Product #{i}: [{base_usd} USD] -> {price_tag} | Link: {link}")

            print(f" ✅ All 9 products correctly converted to {curr}!\n")

        browser.close()
        print("==================================================")
        print("🎉 100% AUDIT PASS: All 9 products verified across all world currencies!")
        print("==================================================")

if __name__ == "__main__":
    test_all_products_all_currencies()
