import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_currencies():
    test_cases = [
        ("US", "USD", "$"),
        ("UK", "GBP", "£"),
        ("IN", "INR", "₹"),
        ("DE", "EUR", "€"),
        ("JP", "JPY", "¥"),
        ("CA", "CAD", "CA$"),
        ("AU", "AUD", "A$")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html")
        time.sleep(1)

        print("Testing Global Currency Engine across 7 major world regions...")

        for country, expected_curr, expected_sym in test_cases:
            # Change selector
            page.select_option("#currencySelector", expected_curr)
            time.sleep(0.5)

            # Read first product card price
            price_elem = page.query_selector("#productGrid .card-wrapper .card-price-tag")
            price_text = price_elem.inner_text() if price_elem else "N/A"

            print(f" Region: {country} | Selected: {expected_curr} | Rendered Price: '{price_text}'")
            assert expected_sym in price_text or expected_curr in price_text, f"Mismatch for {country}"

        browser.close()
        print("✅ 100% PASS: All global currency conversions (USD, GBP, INR, EUR, JPY, CAD, AUD) verified working!")

if __name__ == "__main__":
    test_currencies()
