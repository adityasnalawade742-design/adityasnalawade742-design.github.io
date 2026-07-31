import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

def scrape_us_prices():
    import random
    import re
    print("🇺🇸 [1/7] SCRAPING AMAZON US (Amazon.com)...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            locale="en-US"
        )
        page = context.new_page()

        for asin, item in registry.items():
            if "regional_prices" not in item:
                item["regional_prices"] = {}
            if "regional_asins" not in item:
                item["regional_asins"] = {}

            target_asin = item.get("regional_asins", {}).get("US") or asin
            url = f"https://www.amazon.com/dp/{target_asin}"
            price_str = None

            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)

                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen:
                    txt = offscreen.inner_text().strip()
                    if "$" in txt and "INR" not in txt:
                        m = re.search(r"(\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", txt)
                        if m:
                            price_str = m.group(1)

                if not price_str:
                    whole = page.query_selector("span.a-price-whole")
                    frac = page.query_selector("span.a-price-fraction")
                    if whole:
                        w = whole.inner_text().strip().replace("\n", "").replace(".", "")
                        f = frac.inner_text().strip() if frac else "00"
                        if w.isdigit() and len(w) <= 3:
                            price_str = f"${w}.{f}"
            except Exception:
                pass

            # Sanity ceiling check
            if price_str:
                num_val = float(re.sub(r"[^\d.]", "", price_str) or 0)
                if num_val > 500:
                    price_str = None

            if price_str:
                item["regional_prices"]["US"] = price_str
                item["current_price"] = price_str
                print(f"  • [{asin}] US Price: {price_str}")
            else:
                existing = item["regional_prices"].get("US", item.get("current_price", "$19.99"))
                if "INR" in str(existing):
                    existing = "$19.99"
                item["regional_prices"]["US"] = existing
                print(f"  • [{asin}] US Price (Preserved): {existing}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon US Scraping Complete.\n")

if __name__ == "__main__":
    scrape_us_prices()
