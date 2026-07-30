import sys
import time
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_mushroom_lamp_availability():
    asin = "B0D1FRDFFX"
    title = "Handblown Striped Glass Mushroom Table Lamp"

    countries = [
        ("US", "United States", "amazon.com"),
        ("UK", "United Kingdom", "amazon.co.uk"),
        ("IN", "India", "amazon.in"),
        ("DE", "Germany", "amazon.de"),
        ("CA", "Canada", "amazon.ca"),
        ("AU", "Australia", "amazon.com.au"),
        ("JP", "Japan", "amazon.co.jp"),
        ("SE", "Sweden", "amazon.se"),
        ("BR", "Brazil", "amazon.com.br"),
        ("AE", "UAE", "amazon.ae"),
        ("SG", "Singapore", "amazon.sg"),
        ("MX", "Mexico", "amazon.com.mx"),
        ("FR", "France", "amazon.fr"),
        ("IT", "Italy", "amazon.it"),
        ("ES", "Spain", "amazon.es")
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("==================================================")
        print(f"📦 PRODUCT AVAILABILITY AUDIT FOR {asin}: {title}")
        print("   Landing Page: https://adityasnalawade742-design.github.io/bridge_B0D1FRDFFX.html")
        print("==================================================")

        results = []

        for cc, country_name, domain in countries:
            url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={cc}"
            page.goto(url)
            time.sleep(0.2)

            hero_price_tag = page.locator(".price, .tag").first.inner_text()
            cta_button_text = page.locator("#buyBtnText").inner_text()
            cta_link_href = page.locator("#buyBtn").get_attribute("href")
            geo_box_visible = page.locator("#geoNoticeBox").is_visible()

            is_available = "NOT AVAILABLE" not in hero_price_tag.upper() and "Not Available" not in hero_price_tag

            status_symbol = "✅ AVAILABLE" if is_available else "🔴 NOT AVAILABLE IN LOCAL CATALOG"

            results.append({
                "code": cc,
                "country": country_name,
                "status": status_symbol,
                "price_tag": hero_price_tag,
                "cta_text": cta_button_text,
                "cta_link": cta_link_href,
                "geo_notice": geo_box_visible
            })

            print(f"\n🌍 {country_name} [{cc}] ({domain}):")
            print(f"   • Status:                 {status_symbol}")
            print(f"   • Price Tag Displayed:    '{hero_price_tag}'")
            print(f"   • CTA Button Action:     '{cta_button_text}'")
            print(f"   • CTA Destination Link:   '{cta_link_href}'")
            print(f"   • Notice Box Displayed:  {geo_box_visible}")

        browser.close()

        print("\n==================================================")
        print("📊 SUMMARY TABLE FOR B0D1FRDFFX (Mushroom Lamp)")
        print("==================================================")
        for r in results:
            print(f"{r['country']:15s} | {r['code']:2s} | {r['status']:30s} | {r['price_tag']}")

if __name__ == "__main__":
    check_mushroom_lamp_availability()
