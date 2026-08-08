import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent.parent.parent  # C6 FIX: dynamic path
registry_file = repo / "product_price_registry.json"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

from modules.price_registry_manager import create_price_record, extract_price_string, normalize_registry_record, extract_page_asin

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
            normalize_registry_record(item)
            target_asin = item.get("regional_asins", {}).get("US") or asin
            url = f"https://www.amazon.com/dp/{target_asin}"
            price_str = None
            seller_name = None
            detected_asin = None
            identity_verified = False

            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)

                # Extract actual page ASIN and verify identity
                detected_asin = extract_page_asin(page)
                identity_verified = bool(detected_asin and target_asin and detected_asin.upper() == target_asin.upper())

                # Extract seller / merchant info if available
                merchant_el = page.query_selector("#merchant-info, #sellerProfileTriggerId, #bylineInfo")
                if merchant_el:
                    seller_name = merchant_el.inner_text().strip()

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
                        if w.isdigit() and len(w) <= 6:
                            price_str = f"${w}.{f}"
            except Exception as e:
                print(f"  ⚠️ Scrape page error for {asin}: {e}")

            # Sanity ceiling check
            if price_str:
                num_val = float(re.sub(r"[^\d.]", "", price_str) or 0)
                if num_val > 10000:
                    price_str = None

            record = create_price_record(
                price_str=price_str,
                asin=target_asin,
                country_code="US",
                is_direct=True,
                seller=seller_name,
                source_url=url,
                existing_record=item["regional_prices"].get("US"),
                detected_asin=detected_asin,
                identity_verified=identity_verified
            )

            item["regional_prices"]["US"] = record
            final_p = extract_price_string(record)
            if price_str:
                item["current_price"] = final_p
                print(f"  • [{asin}] US Price: {final_p}")
            else:
                print(f"  • [{asin}] US Price (Preserved): {final_p}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon US Scraping Complete.\n")

if __name__ == "__main__":
    scrape_us_prices()
