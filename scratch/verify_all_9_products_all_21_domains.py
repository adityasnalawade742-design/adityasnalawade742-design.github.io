import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def verify_all_9_products_all_21_domains():
    asins = [
        ("B0BZXNSW5K", "Touch Bedside Lamp"),
        ("B0C2YLN3H4", "White Donut Vases"),
        ("B07HP22QTZ", "Crystal Suncatcher"),
        ("B0D8P8CSYP", "Cute Bird Touch Lamp"),
        ("B0D1FRDFFX", "Glass Mushroom Lamp"),
        ("B0GYDXHF4G", "Flame Aroma Diffuser"),
        ("B0DXKGL1T2", "Lily of Valley Lamp"),
        ("B0DZD1X83N", "Minimalist Wood Lamp"),
        ("B0FXLYXM32", "White Wavy Mirror")
    ]

    domains_to_test = [
        ("US", "amazon.com"),
        ("CA", "amazon.ca"),
        ("MX", "amazon.com.mx"),
        ("BR", "amazon.com.br"),
        ("UK", "amazon.co.uk"),
        ("DE", "amazon.de"),
        ("FR", "amazon.fr"),
        ("IT", "amazon.it"),
        ("ES", "amazon.es"),
        ("NL", "amazon.nl"),
        ("SE", "amazon.se"),
        ("PL", "amazon.pl"),
        ("BE", "amazon.com.be"),
        ("TR", "amazon.com.tr"),
        ("AE", "amazon.ae"),
        ("SA", "amazon.sa"),
        ("EG", "amazon.eg"),
        ("IN", "amazon.in"),
        ("JP", "amazon.co.jp"),
        ("AU", "amazon.com.au"),
        ("SG", "amazon.sg")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print("🌍 AUDITING ALL 9 PRODUCTS ACROSS ALL 21 AMAZON DOMAINS (189 TOTAL CHECKS)")
        print("==================================================")

        total_checks = 0
        passed_checks = 0

        for asin, title in asins:
            print(f"\n📦 [{asin}] {title}:")
            for cc, domain in domains_to_test:
                total_checks += 1
                url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
                page.goto(url)
                time.sleep(0.15)

                cta_link = page.locator("#buyBtn").get_attribute("href")

                assert domain in cta_link, f"Domain mismatch for {asin} [{cc}]: expected {domain} in {cta_link}"
                assert "tag=smartdeal0358-21" in cta_link, f"Missing affiliate tag for {asin} [{cc}]"

                passed_checks += 1
                print(f"   • Country {cc:2s} ({domain:14s}) -> ✅ {cta_link[:65]}...")

        browser.close()

        print("\n==================================================")
        print(f"🎉 100% PASS: All {passed_checks}/{total_checks} checks verified across ALL 9 products & 21 Amazon domains!")
        print("==================================================")

if __name__ == "__main__":
    verify_all_9_products_all_21_domains()
