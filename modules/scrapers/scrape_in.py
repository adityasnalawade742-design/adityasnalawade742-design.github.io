import sys
import json
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"

def scrape_in_prices():
    print("🇮🇳 [2/7] SCRAPING AMAZON INDIA (Amazon.in)...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-IN"
        )
        page = context.new_page()

        for asin, item in registry.items():
            if "regional_prices" not in item:
                item["regional_prices"] = {}

            target_asin = item.get("regional_asins", {}).get("IN") or asin
            url = f"https://www.amazon.in/dp/{target_asin}"
            price_str = None

            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)

                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen:
                    txt = offscreen.inner_text().strip()
                    m = re.search(r"[₹\s]*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", txt)
                    if m:
                        val = float(m.group(1).replace(",", ""))
                        base_usd = float(str(item.get("current_price", "$20.00")).replace("$", "").replace(",", "") or 20.0)
                        if val <= (base_usd * 150.0):
                            price_str = f"₹{val:,.2f}"

                if not price_str:
                    whole = page.query_selector("span.a-price-whole")
                    if whole:
                        w_raw = whole.inner_text().strip().replace("\n", "").replace(".", "").replace(",", "")
                        if w_raw.isdigit():
                            val = float(w_raw)
                            base_usd = float(str(item.get("current_price", "$20.00")).replace("$", "").replace(",", "") or 20.0)
                            if val <= (base_usd * 150.0):
                                price_str = f"₹{val:,.2f}"
            except Exception:
                pass

            if price_str:
                item["regional_prices"]["IN"] = price_str
                print(f"  • [{asin}] India Price: {price_str}")
            else:
                existing = item["regional_prices"].get("IN", "Not Available")
                item["regional_prices"]["IN"] = existing
                print(f"  • [{asin}] India Price (Preserved): {existing}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon India Scraping Complete.\n")

if __name__ == "__main__":
    scrape_in_prices()
