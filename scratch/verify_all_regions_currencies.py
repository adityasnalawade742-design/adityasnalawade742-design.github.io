import os
import sys
import glob
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_audit():
    print("=========================================================================")
    print("🌐 AUDITING GEO-REDIRECT, PRICES & CURRENCIES ACROSS ALL REGIONS")
    print("=========================================================================\n")

    bridge_files = glob.glob("bridge_*.html")
    if not bridge_files:
        print("❌ No bridge files found!")
        return

    test_countries = [
        "US", "IN", "GB", "DE", "CA", "AU", "JP", "FR", "ES", "IT", 
        "SE", "NL", "PL", "TR", "BE", "MX", "BR", "SG", "AE", "SA", 
        "EG", "KR", "CH", "NO", "DK"
    ]

    expected_tags = {
        "US": "smartdeal0358-20",
        "CA": "smartdeal0302-20",
        "IN": "smartdeal0358-21",
        "GB": "smartdea04b3a-21",
        "UK": "smartdea04b3a-21",
        "IE": "smartdea04b3a-21",
        "DE": "smartdeal0bb4-21",
        "FR": "smartdeal0962-21",
        "ES": "smartdeal0b46-21",
        "IT": "smartdea03a8d-21",
        "SE": "smartdeal0bb4-21",
        "NL": "smartdeal0bb4-21",
        "PL": "smartdeal0bb4-21",
        "TR": "smartdeal0bb4-21",
        "CH": "smartdeal0bb4-21",
        "NO": "smartdeal0bb4-21",
        "DK": "smartdeal0bb4-21",
        "CZ": "smartdeal0bb4-21",
        "AT": "smartdeal0bb4-21",
        "BE": "smartdeal0962-21",
        "MX": "smartdeal0358-20",
        "BR": "smartdeal0358-20",
        "SG": "smartdeal0358-20",
        "AE": "smartdeal0358-20",
        "SA": "smartdeal0358-20",
        "EG": "smartdeal0358-20",
        "JP": "smartdeal0358-20",
        "AU": "smartdeal0358-20",
        "KR": "smartdeal0358-21",
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        total_checks = 0
        total_passed = 0

        # Sample test key bridge files
        sample_bridges = [bridge_files[0], bridge_files[min(3, len(bridge_files)-1)]]

        for bfile in sample_bridges:
            page = browser.new_page()
            file_url = f"file:///{os.path.abspath(bfile).replace('\\', '/')}"
            page.goto(file_url)
            page.wait_for_load_state("domcontentloaded")

            print(f"📄 Testing Bridge Page: {bfile}")

            for cc in test_countries:
                total_checks += 1
                # Execute applyGeoRedirect(cc) in page context
                page.evaluate(f"window.applyGeoRedirect('{cc}')")
                
                # Retrieve price text, button link, and select value
                price_text = page.inner_text(".price").strip()
                buy_href = page.get_attribute("#buyBtn", "href") or ""
                buy_btn_text = page.inner_text("#buyBtnText").strip()
                select_val = page.eval_on_selector("#bridgeRegionSelect", "el => el.value") if page.query_selector("#bridgeRegionSelect") else ""

                # Check tag attachment
                expected_tag = expected_tags.get(cc, "smartdeal0358-20")
                has_tag = f"tag={expected_tag}" in buy_href

                # Validate price is not empty and has a symbol / number
                has_price = len(price_text) > 0 and price_text != "$0.00"

                if has_price and has_tag:
                    total_passed += 1
                    print(f"   [PASS] {cc:2s} ➔ Price: {price_text:15s} | CTA: {buy_btn_text[:30]:30s} | Tag: {expected_tag}")
                else:
                    print(f"   [FAIL] {cc:2s} ➔ Price: {price_text} | Href: {buy_href}")

            page.close()
            print("")

        browser.close()

    print("=========================================================================")
    print(f"🏆 AUDIT COMPLETE: Passed {total_passed} / {total_checks} regional price & tag checks!")
    print("=========================================================================")

if __name__ == "__main__":
    run_audit()
