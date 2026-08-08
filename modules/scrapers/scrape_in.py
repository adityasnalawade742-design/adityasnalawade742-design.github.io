import sys
import json
import time
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent.parent.parent  # C6 FIX: dynamic path
registry_file = repo / "product_price_registry.json"

from modules.price_registry_manager import create_price_record, extract_price_string, normalize_registry_record, STATUS_NOT_MAPPED, get_now_iso

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
            normalize_registry_record(item)
            mapped_asin = item.get("regional_asins", {}).get("IN")
            
            # ELIMINATE US-ASIN FALLBACK SCRAPER POLLUTION
            if not mapped_asin:
                item["regional_prices"]["IN"] = {
                    "price": "Not Available",
                    "asin": None,
                    "country_code": "IN",
                    "is_direct": False,
                    "identity_verified": False,
                    "seller_verified": False,
                    "seller": None,
                    "ships_from": None,
                    "source_url": None,
                    "scraped_at": get_now_iso(),
                    "status": STATUS_NOT_MAPPED
                }
                print(f"  • [{asin}] India Price: Not Mapped (US ASIN Fallback Prohibited)")
                continue

            target_asin = mapped_asin
            url = f"https://www.amazon.in/dp/{target_asin}"
            price_str = None
            seller_name = None

            try:
                page.goto(url, timeout=12000, wait_until="domcontentloaded")
                time.sleep(0.5)

                merchant_el = page.query_selector("#merchant-info, #sellerProfileTriggerId, #bylineInfo")
                if merchant_el:
                    seller_name = merchant_el.inner_text().strip()

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
            except Exception as e:
                print(f"  ⚠️ India scrape error for {asin}: {e}")

            record = create_price_record(
                price_str=price_str,
                asin=target_asin,
                country_code="IN",
                is_direct=True,
                seller=seller_name,
                source_url=url,
                existing_record=item["regional_prices"].get("IN")
            )

            item["regional_prices"]["IN"] = record
            final_p = extract_price_string(record)
            if price_str:
                print(f"  • [{asin}] India Price: {final_p}")
            else:
                print(f"  • [{asin}] India Price (Preserved): {final_p}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("✅ Amazon India Scraping Complete.\n")

if __name__ == "__main__":
    scrape_in_prices()
