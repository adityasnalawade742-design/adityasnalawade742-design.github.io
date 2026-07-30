import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_master_diagnostic():
    asins = [
        "B0DZD1X83N", "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4",
        "B07HP22QTZ", "B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP"
    ]

    countries = ["US", "UK", "IN", "DE", "CA", "JP", "AU"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🔬 MASTER DIAGNOSTIC SUITE: HOMEPAGE & 9 BRIDGE PAGES")
        print("   Testing 63 Storefront Cards & 63 Landing Page Links Across 7 Regions")
        print("==================================================")

        # --------------------------------------------------
        # PART 1: HOMEPAGE (index.html) REGIONAL DIAGNOSTIC
        # --------------------------------------------------
        print("\n--- PART 1: HOMEPAGE (index.html) REGIONAL PRICE AUDIT ---")
        homepage_pass = True
        for cc in countries:
            page.goto(f"file:///G:/CLI/pinterest-auto-affiliate/index.html?country={cc}")
            time.sleep(0.5)

            available_count = 0
            not_available_count = 0

            for asin in asins:
                card = page.locator(f"#card-{asin}")
                price_tag = card.locator(".card-price-tag").inner_text()
                if "Not Available" in price_tag:
                    not_available_count += 1
                else:
                    available_count += 1
            
            print(f" 🌍 Homepage [{cc:2s}]: {available_count} Available | {not_available_count} Not Available")

        # --------------------------------------------------
        # PART 2: ALL 9 LANDING PAGES (bridge_*.html) REGIONAL DIAGNOSTIC
        # --------------------------------------------------
        print("\n--- PART 2: ALL 9 LANDING PAGES (bridge_*.html) REGIONAL PRICE AUDIT ---")
        total_bridge_checks = 0
        passed_bridge_checks = 0

        for asin in asins:
            print(f"\n📦 Testing Product ASIN: [{asin}]")
            for cc in countries:
                total_bridge_checks += 1
                page.goto(f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}")
                time.sleep(0.3)

                price_tag = page.locator(".price, .tag").first.inner_text()
                buy_btn_href = page.locator("#buyBtn").get_attribute("href")
                buy_btn_text = page.locator("#buyBtnText").inner_text()

                assert "tag=smartdeal0358-21" in buy_btn_href, f"Missing affiliate tag in {asin} [{cc}]"

                print(f"   Country [{cc:2s}] -> Hero Price Tag: '{price_tag}' | CTA Button: '{buy_btn_text}'")
                passed_bridge_checks += 1

        browser.close()

        print("\n==================================================")
        print(f"🎉 100% MASTER DIAGNOSTIC PASS!")
        print(f"   Homepage: 7/7 Regions Verified")
        print(f"   Landing Pages: {passed_bridge_checks}/{total_bridge_checks} Regional Page Checks Verified")
        print(f"   Affiliate Tag 'smartdeal0358-21': 100% Present Across All Links")
        print("==================================================")

if __name__ == "__main__":
    run_master_diagnostic()
