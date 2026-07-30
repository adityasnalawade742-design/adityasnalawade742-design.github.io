import sys
import requests
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def test_b0dzd1x83n_cta_links():
    asin = "B0DZD1X83N"
    countries = ["US", "UK", "IN", "DE", "CA", "AU", "JP"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🔍 TESTING ALL CTA LINKS FOR B0DZD1X83N ON LIVE AMAZON STOREFRONTS")
        print("==================================================")

        for cc in countries:
            url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
            page.goto(url)
            cta_link = page.locator("#buyBtn").get_attribute("href")
            cta_text = page.locator("#buyBtnText").inner_text()

            # Test HTTP status of destination Amazon URL
            try:
                res = requests.head(cta_link, headers=headers, timeout=5, allow_redirects=True)
                status = res.status_code
            except Exception:
                status = "Error"

            print(f" • Country [{cc:2s}]: CTA Text: '{cta_text:38s}'")
            print(f"               Destination Link: {cta_link}")
            print(f"               HTTP Response:   {status}\n")

        browser.close()

if __name__ == "__main__":
    test_b0dzd1x83n_cta_links()
