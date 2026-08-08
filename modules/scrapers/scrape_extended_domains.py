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

extended_domains = [
    ("FR", "Amazon.fr", "https://www.amazon.fr/dp/", "€"),
    ("ES", "Amazon.es", "https://www.amazon.es/dp/", "€"),
    ("IT", "Amazon.it", "https://www.amazon.it/dp/", "€"),
    ("SE", "Amazon.se", "https://www.amazon.se/dp/", "kr"),
    ("NL", "Amazon.nl", "https://www.amazon.nl/dp/", "€"),
    ("PL", "Amazon.pl", "https://www.amazon.pl/dp/", "zł"),
    ("TR", "Amazon.com.tr", "https://www.amazon.com.tr/dp/", "₺"),
    ("BE", "Amazon.com.be", "https://www.amazon.com.be/dp/", "€"),
    ("MX", "Amazon.com.mx", "https://www.amazon.com.mx/dp/", "Mex$"),
    ("BR", "Amazon.com.br", "https://www.amazon.com.br/dp/", "R$"),
    ("SG", "Amazon.sg", "https://www.amazon.sg/dp/", "S$"),
    ("AE", "Amazon.ae", "https://www.amazon.ae/dp/", "AED"),
    ("SA", "Amazon.sa", "https://www.amazon.sa/dp/", "SAR"),
    ("EG", "Amazon.eg", "https://www.amazon.eg/dp/", "E£")
]

from modules.price_registry_manager import create_price_record, extract_price_string, normalize_registry_record, STATUS_NOT_MAPPED, get_now_iso

def scrape_extended_domains():
    print("🌍 SCRAPING ALL 14 EXTENDED GLOBAL AMAZON DOMAINS...")
    registry = json.loads(registry_file.read_text(encoding="utf-8"))

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for cc, name, base_url, symbol in extended_domains:
            print(f"\n📌 Processing Domain: {name} [{cc}]...")
            for asin, item in registry.items():
                normalize_registry_record(item)
                mapped_asin = item.get("regional_asins", {}).get(cc)

                # ELIMINATE US-ASIN FALLBACK SCRAPER POLLUTION
                if not mapped_asin:
                    item["regional_prices"][cc] = {
                        "price": "Not Available",
                        "asin": None,
                        "country_code": cc,
                        "is_direct": False,
                        "identity_verified": False,
                        "seller_verified": False,
                        "seller": None,
                        "ships_from": None,
                        "source_url": None,
                        "scraped_at": get_now_iso(),
                        "status": STATUS_NOT_MAPPED
                    }
                    continue

                target_asin = mapped_asin
                url = f"{base_url}{target_asin}"
                price_str = None
                seller_name = None

                try:
                    page.goto(url, timeout=8000, wait_until="domcontentloaded")
                    time.sleep(0.3)

                    merchant_el = page.query_selector("#merchant-info, #sellerProfileTriggerId, #bylineInfo")
                    if merchant_el:
                        seller_name = merchant_el.inner_text().strip()

                    offscreen = page.query_selector(".a-price .a-offscreen")
                    if offscreen:
                        txt = offscreen.inner_text().strip()
                        if "INR" not in txt and "₹" not in txt:
                            m = re.search(r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)", txt)
                            if m:
                                raw_num = m.group(1).replace(" ", "")
                                if "," in raw_num and "." in raw_num:
                                    if raw_num.find(",") < raw_num.find("."):
                                        raw_num = raw_num.replace(",", "")
                                    else:
                                        raw_num = raw_num.replace(".", "").replace(",", ".")
                                elif "," in raw_num:
                                    raw_num = raw_num.replace(",", ".")
                                
                                try:
                                    val = float(raw_num)
                                    base_usd = float(str(item.get("current_price", "$20.00")).replace("$", "").replace(",", "") or 20.0)
                                    if 1.0 <= val <= (base_usd * 4.0 * 100.0):
                                        price_str = re.sub(r"\s+", " ", txt).strip()
                                except ValueError:
                                    pass

                    if not price_str:
                        whole = page.query_selector("span.a-price-whole")
                        if whole:
                            w = whole.inner_text().strip().replace("\n", "").replace(".", "").replace(",", "")
                            if w.isdigit():
                                price_str = f"{symbol}{w}"
                except Exception as e:
                    print(f"  ⚠️ {cc} scrape error for {asin}: {e}")

                record = create_price_record(
                    price_str=price_str,
                    asin=target_asin,
                    country_code=cc,
                    is_direct=True,
                    seller=seller_name,
                    source_url=url,
                    existing_record=item["regional_prices"].get(cc)
                )

                item["regional_prices"][cc] = record
                final_p = extract_price_string(record)
                if price_str:
                    print(f"  • [{asin}] {cc} Price: {final_p}")
                else:
                    print(f"  • [{asin}] {cc} Price (Preserved): {final_p}")

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n✅ All 14 Extended Global Amazon Domains Scraping Complete.\n")

if __name__ == "__main__":
    scrape_extended_domains()
