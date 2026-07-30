import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_21_amazon_domains():
    asin = "B0D1FRDFFX"
    title = "Handblown Striped Glass Mushroom Table Lamp"

    domains_to_test = [
        ("US", "United States", "amazon.com"),
        ("CA", "Canada", "amazon.ca"),
        ("MX", "Mexico", "amazon.com.mx"),
        ("BR", "Brazil", "amazon.com.br"),
        ("UK", "United Kingdom", "amazon.co.uk"),
        ("DE", "Germany", "amazon.de"),
        ("FR", "France", "amazon.fr"),
        ("IT", "Italy", "amazon.it"),
        ("ES", "Spain", "amazon.es"),
        ("NL", "Netherlands", "amazon.nl"),
        ("SE", "Sweden", "amazon.se"),
        ("PL", "Poland", "amazon.pl"),
        ("BE", "Belgium", "amazon.com.be"),
        ("TR", "Turkey", "amazon.com.tr"),
        ("AE", "UAE", "amazon.ae"),
        ("SA", "Saudi Arabia", "amazon.sa"),
        ("EG", "Egypt", "amazon.eg"),
        ("IN", "India", "amazon.in"),
        ("JP", "Japan", "amazon.co.jp"),
        ("AU", "Australia", "amazon.com.au"),
        ("SG", "Singapore", "amazon.sg")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🌐 AUDITING SYSTEM PERFORMANCE ACROSS ALL 21 GLOBAL AMAZON DOMAINS")
        print(f"   Product ASIN: [{asin}] {title}")
        print("==================================================")

        passed_count = 0

        for cc, country_name, domain in domains_to_test:
            url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
            page.goto(url)
            time.sleep(0.2)

            hero_price = page.locator(".price, .tag").first.inner_text()
            cta_text = page.locator("#buyBtnText").inner_text()
            cta_link = page.locator("#buyBtn").get_attribute("href")

            assert domain in cta_link, f"Domain mismatch for {cc}: expected {domain} in {cta_link}"
            assert "tag=smartdeal0358-21" in cta_link, f"Missing affiliate tag for {cc}"

            passed_count += 1
            print(f" {passed_count:2d}. ✅ [{cc:2s}] {country_name:15s} ({domain:14s}) -> Button: '{cta_text:35s}' | Price: '{hero_price}'")

        browser.close()

        print("\n==================================================")
        print(f"🎉 100% PASS: System verified fully operational across ALL {passed_count}/21 Amazon domains!")
        print("==================================================")

if __name__ == "__main__":
    verify_all_21_amazon_domains()
