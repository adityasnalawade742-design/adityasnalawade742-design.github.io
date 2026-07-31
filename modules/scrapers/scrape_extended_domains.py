import sys
import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
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
                if "regional_prices" not in item:
                    item["regional_prices"] = {}

                target_asin = item.get("regional_asins", {}).get(cc) or asin
                url = f"{base_url}{target_asin}"
                price_str = None

                try:
                    page.goto(url, timeout=8000, wait_until="domcontentloaded")
                    time.sleep(0.3)

                    offscreen = page.query_selector(".a-price .a-offscreen")
                    if offscreen:
                        txt = offscreen.inner_text().strip()
                        if symbol in txt or any(char.isdigit() for char in txt):
                            price_str = txt

                    if not price_str:
                        whole = page.query_selector("span.a-price-whole")
                        if whole:
                            w = whole.inner_text().strip().replace("\n", "")
                            price_str = f"{symbol} {w}" if symbol not in w else w
                except Exception:
                    pass

                if price_str:
                    item["regional_prices"][cc] = price_str
                    print(f"  • [{asin}] {cc} Price: {price_str}")
                else:
                    existing = item["regional_prices"].get(cc, "Not Available")
                    item["regional_prices"][cc] = existing

        browser.close()

    registry_file.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n✅ All 14 Extended Global Amazon Domains Scraping Complete.\n")

if __name__ == "__main__":
    scrape_extended_domains()
