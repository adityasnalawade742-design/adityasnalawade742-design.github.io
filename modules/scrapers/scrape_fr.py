import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"

def scrape_fr_prices():
    print("🇫🇷 SCRAPING AMAZON FRANCE (Amazon.fr)...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)", locale="fr-FR")
        page = context.new_page()

        for asin, item in registry.items():
            if "regional_prices" not in item: item["regional_prices"] = {}
            target_asin = item.get("regional_asins", {}).get("FR") or asin
            url = f"https://www.amazon.fr/dp/{target_asin}"
            price_str = None

            try:
                page.goto(url, timeout=10000, wait_until="domcontentloaded")
                time.sleep(0.3)
                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen and "€" in offscreen.inner_text(): price_str = offscreen.inner_text().strip()
            except Exception: pass

            if price_str:
                item["regional_prices"]["FR"] = price_str
                print(f"  • [{asin}] France Price: {price_str}")
            else:
                existing = item["regional_prices"].get("FR", "Not Available")
                item["regional_prices"]["FR"] = existing
                print(f"  • [{asin}] France Price (Preserved): {existing}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon France Scraping Complete.\n")

if __name__ == "__main__": scrape_fr_prices()
