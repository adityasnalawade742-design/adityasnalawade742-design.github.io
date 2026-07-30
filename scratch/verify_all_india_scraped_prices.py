import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_all_in_prices():
    expected = {
        "card-B0C2YLN3H4": "₹599.00",
        "card-B07HP22QTZ": "₹2,762.75",
        "card-B0BZXNSW5K": "₹475.00",
        "card-B0D1FRDFFX": "₹11,428.51",
        "card-B0D8P8CSYP": "₹3,843.00",
        "card-B0FXLYXM32": "Not Available",
        "card-B0DZD1X83N": "Not Available",
        "card-B0GYDXHF4G": "Not Available",
        "card-B0DXKGL1T2": "Not Available"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html?country=IN")
        time.sleep(1)

        print("==================================================")
        print("🇮🇳 VERIFYING ALL 9 PRODUCTS ON AMAZON INDIA (amazon.in)")
        print("==================================================")

        for card_id, exp_val in expected.items():
            actual = page.inner_text(f"#{card_id} .card-price-tag")
            print(f" {card_id:20s} -> Rendered: '{actual}' | Expected: '{exp_val}'")
            assert exp_val in actual or actual == exp_val, f"Mismatch for {card_id}: expected {exp_val}, got {actual}"

        browser.close()
        print("\n==================================================")
        print("🎉 100% PASS: All 9 products matched exact Amazon India prices & out-of-stock badges!")
        print("==================================================")

if __name__ == "__main__":
    test_all_in_prices()
