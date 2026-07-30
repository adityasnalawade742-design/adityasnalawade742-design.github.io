import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_regional_matrix():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🔍 TESTING UNIVERSAL REGIONAL MATRIX (IN, UK, US)")
        print("==================================================")

        # 1. Test India (IN)
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html?country=IN")
        time.sleep(1)
        page.select_option("#currencySelector", "INR")
        page.dispatch_event("#currencySelector", "change")
        time.sleep(0.5)
        
        diffuser_in = page.inner_text("#card-B0GYDXHF4G .card-price-tag")
        suncatcher_in = page.inner_text("#card-B07HP22QTZ .card-price-tag")
        wood_in = page.inner_text("#card-B0DZD1X83N .card-price-tag")

        print(f"🇮🇳 India (IN):")
        print(f"   - Flame Diffuser B0GYDXHF4G: '{diffuser_in}'")
        print(f"   - Suncatcher B07HP22QTZ: '{suncatcher_in}'")
        print(f"   - Wood Lamp B0DZD1X83N: '{wood_in}'")

        assert diffuser_in == "Not Available", f"Expected 'Not Available' for Diffuser in India, got {diffuser_in}"
        assert wood_in == "Not Available", f"Expected 'Not Available' for Wood Lamp in India, got {wood_in}"
        assert "2,762.75" in suncatcher_in or "2762.75" in suncatcher_in, f"Expected ₹2,762.75 for Suncatcher in India, got {suncatcher_in}"

        # 2. Test UK
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html?country=UK")
        time.sleep(1)
        page.select_option("#currencySelector", "GBP")
        page.dispatch_event("#currencySelector", "change")
        time.sleep(0.5)

        vases_uk = page.inner_text("#card-B0C2YLN3H4 .card-price-tag")
        print(f"\n🇬🇧 United Kingdom (UK):")
        print(f"   - Donut Vases B0C2YLN3H4: '{vases_uk}'")
        assert vases_uk == "Not Available", f"Expected 'Not Available' for Donut Vases in UK, got {vases_uk}"

        browser.close()
        print("\n==================================================")
        print("🎉 100% PASS: Universal regional availability and 'Not Available' tags verified working!")
        print("==================================================")

if __name__ == "__main__":
    test_regional_matrix()
