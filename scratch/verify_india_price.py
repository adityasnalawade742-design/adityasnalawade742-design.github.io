import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_india_price():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Test index.html?country=IN
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html?country=IN")
        time.sleep(1)

        # Trigger INR
        page.select_option("#currencySelector", "INR")
        time.sleep(0.5)

        suncatcher_price = page.inner_text("#card-B07HP22QTZ .card-price-tag")
        print(f"1. Homepage Suncatcher Card Price (INR): '{suncatcher_price}'")
        assert "2,762.75" in suncatcher_price or "2762.75" in suncatcher_price, f"Expected ₹2,762.75, got {suncatcher_price}"

        browser.close()
        print("✅ 100% PASS: Exact Amazon India local price (₹2,762.75 INR) verified working!")

if __name__ == "__main__":
    test_india_price()
