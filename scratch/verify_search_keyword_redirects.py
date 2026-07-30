import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_search_keywords():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🎯 VERIFYING TARGETED REGIONAL SEARCH FALLBACK URLS")
        print("==================================================")

        # 1. Flame Diffuser B0GYDXHF4G
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/bridge_B0GYDXHF4G.html?country=IN")
        time.sleep(1)
        buy_btn_diffuser = page.query_selector("#buyBtn").get_attribute("href")
        print(f"1. Flame Diffuser (B0GYDXHF4G) Search URL:")
        print(f"   {buy_btn_diffuser}\n")
        assert "Volcano%20Flame%20Aroma%20Diffuser%20Lamp" in buy_btn_diffuser, f"Expected Volcano Flame Aroma Diffuser Lamp, got {buy_btn_diffuser}"

        # 2. Lily of the Valley Lamp B0DXKGL1T2
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/bridge_B0DXKGL1T2.html?country=IN")
        time.sleep(1)
        buy_btn_lily = page.query_selector("#buyBtn").get_attribute("href")
        print(f"2. Lily Lamp (B0DXKGL1T2) Search URL:")
        print(f"   {buy_btn_lily}\n")
        assert "Lily%20of%20the%20Valley%20Flower%20Table%20Lamp" in buy_btn_lily, f"Expected Lily of the Valley Flower Table Lamp, got {buy_btn_lily}"

        browser.close()
        print("==================================================")
        print("🎉 100% PASS: All fallback search URLs are 100% relevant and category-accurate!")
        print("==================================================")

if __name__ == "__main__":
    test_search_keywords()
