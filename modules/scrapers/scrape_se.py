import sys, json, time, re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
repo = Path(__file__).resolve().parent.parent.parent  # C6 FIX: dynamic path
registry_file = repo / "product_price_registry.json"

def scrape_se_prices():
    print("🇸🇪 SCRAPING AMAZON SWEDEN (Amazon.se)...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0", locale="sv-SE")
        page = context.new_page()

        for asin, item in registry.items():
            if "regional_prices" not in item: item["regional_prices"] = {}
            target_asin = item.get("regional_asins", {}).get("SE") or asin
            url = f"https://www.amazon.se/dp/{target_asin}"
            price_str = None

            try:
                page.goto(url, timeout=10000, wait_until="domcontentloaded")
                time.sleep(0.3)
                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen:
                    txt = offscreen.inner_text().strip()
                    m = re.search(r"(\d{1,3}(?:\s*\d{3})*(?:,\d{2})?)\s*kr", txt)
                    if m:
                        raw_num = m.group(1).replace(" ", "").replace(",", ".")
                        val = float(raw_num)
                        base_usd = float(str(item.get("current_price", "$20.00")).replace("$", "").replace(",", "") or 20.0)
                        if val <= (base_usd * 25.0):
                            price_str = f"{val:.2f}kr".replace(".", ",")
            except Exception: pass

            if price_str:
                item["regional_prices"]["SE"] = price_str
                print(f"  • [{asin}] Sweden Price: {price_str}")
            else:
                item["regional_prices"]["SE"] = item["regional_prices"].get("SE", "Not Available")

        browser.close()
    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon Sweden Scraping Complete.\n")

if __name__ == "__main__": scrape_se_prices()
