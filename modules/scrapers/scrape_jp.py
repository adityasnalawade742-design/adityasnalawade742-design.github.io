import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
registry_file = repo / "product_price_registry.json"

def scrape_jp_prices():
    print("🇯🇵 [7/7] SCRAPING AMAZON JAPAN (Amazon.co.jp)...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="ja-JP"
        )
        page = context.new_page()

        for asin, item in registry.items():
            if "regional_prices" not in item:
                item["regional_prices"] = {}

            target_asin = item.get("regional_asins", {}).get("JP") or asin
            url = f"https://www.amazon.co.jp/dp/{target_asin}"
            price_str = None

            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)

                offscreen = page.query_selector(".a-price .a-offscreen")
                if offscreen:
                    txt = offscreen.inner_text().strip()
                    if "¥" in txt or "￥" in txt:
                        price_str = txt.replace("￥", "¥")

                if not price_str:
                    whole = page.query_selector("span.a-price-whole")
                    if whole:
                        w = whole.inner_text().strip().replace("\n", "").replace(".", "").replace(",", "")
                        price_str = f"¥{w}"
            except Exception:
                pass

            if price_str:
                item["regional_prices"]["JP"] = price_str
                print(f"  • [{asin}] Japan Price: {price_str}")
            else:
                existing = item["regional_prices"].get("JP", "Not Available")
                item["regional_prices"]["JP"] = existing
                print(f"  • [{asin}] Japan Price (Preserved): {existing}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon Japan Scraping Complete.\n")

if __name__ == "__main__":
    scrape_jp_prices()
