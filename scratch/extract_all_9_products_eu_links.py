import sys
import json
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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

eu_countries = [
    ("NL", "Netherlands", "amazon.nl"),
    ("DE", "Germany", "amazon.de"),
    ("FR", "France", "amazon.fr"),
    ("IT", "Italy", "amazon.it"),
    ("ES", "Spain", "amazon.es"),
    ("SE", "Sweden", "amazon.se")
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print("==================================================")
    print("🇪🇺 EXTRACTING LIVE DESTINATION LINKS FOR ALL 9 PRODUCTS ACROSS EU STOREFRONTS")
    print("==================================================")

    for asin, title in asins:
        results[asin] = {"title": title, "links": {}}
        print(f"\n📦 ASIN [{asin}] {title}:")
        for code, country_name, domain in eu_countries:
            url = f"file:///G:/CLI/pinterest-auto-affiliate/bridge_{asin}.html?country={code}"
            page.goto(url)
            
            price = page.locator(".price, .tag").first.inner_text()
            cta_text = page.locator("#buyBtnText").inner_text()
            cta_link = page.locator("#buyBtn").get_attribute("href")

            is_direct = "/dp/" in cta_link
            link_type = "DIRECT /DP/" if is_direct else "SEARCH FALLBACK"

            results[asin]["links"][code] = {
                "country": country_name,
                "domain": domain,
                "price": price,
                "cta_text": cta_text,
                "cta_link": cta_link,
                "type": link_type
            }

            print(f"   • {code:2s} ({domain:12s}) -> {link_type:15s} | {cta_link}")

    browser.close()

with open("scratch/all_products_eu_links_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n==================================================")
print(" ✅ Successfully extracted all 9 product links across EU storefronts!")
print("==================================================")
