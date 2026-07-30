import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_landing_page_prices():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🎯 VERIFYING DYNAMIC LANDING PAGE REGIONAL PRICES")
        print("==================================================")

        # 1. Fenmzee Touch Lamp B0BZXNSW5K in India
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/bridge_B0BZXNSW5K.html?country=IN")
        time.sleep(1)
        tag_text_lamp = page.inner_text(".tag")
        print(f"1. Touch Lamp (B0BZXNSW5K) India Badge Tag: '{tag_text_lamp}'")
        assert "₹475.00" in tag_text_lamp, f"Expected ₹475.00, got {tag_text_lamp}"

        # 2. Donut Vases B0C2YLN3H4 in India
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/bridge_B0C2YLN3H4.html?country=IN")
        time.sleep(1)
        tag_text_vases = page.inner_text(".tag")
        print(f"2. Donut Vases (B0C2YLN3H4) India Badge Tag: '{tag_text_vases}'")
        assert "₹599.00" in tag_text_vases, f"Expected ₹599.00, got {tag_text_vases}"

        # 3. Flame Diffuser B0GYDXHF4G in India (Out of Stock)
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/bridge_B0GYDXHF4G.html?country=IN")
        time.sleep(1)
        tag_text_diffuser = page.inner_text(".tag")
        print(f"3. Flame Diffuser (B0GYDXHF4G) India Badge Tag: '{tag_text_diffuser}'")
        assert "NOT AVAILABLE IN YOUR REGION" in tag_text_diffuser, f"Expected NOT AVAILABLE IN YOUR REGION, got {tag_text_diffuser}"

        browser.close()
        print("\n==================================================")
        print("🎉 100% PASS: All landing pages render exact dynamic regional price tags!")
        print("==================================================")

if __name__ == "__main__":
    test_landing_page_prices()
