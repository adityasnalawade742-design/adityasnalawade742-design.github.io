import sys
import json
import time
import urllib.request
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent
registry_file = repo_dir / "product_price_registry.json"
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)

with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

print("==================================================")
print("📥 FETCHING CLEAN RAW (TEXT-FREE) PRODUCT IMAGES FOR ALL ASINs")
print("==================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for asin, meta in registry.items():
        raw_target = raw_dir / f"raw_{asin}.jpg"
        print(f"\n🔍 Processing ASIN [{asin}] - {meta.get('title', '')[:40]}...")
        
        img_url = None
        url = f"https://www.amazon.com/dp/{asin}"
        
        try:
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            time.sleep(1)
            
            # Find main product image
            img_elem = page.query_selector("#landingImage") or page.query_selector("#imgBlkFront") or page.query_selector("#main-image") or page.query_selector(".imgTagWrapper img")
            if img_elem:
                # Get dynamic hires image or src attribute
                dynamic_data = img_elem.get_attribute("data-a-dynamic-image")
                if dynamic_data:
                    try:
                        parsed_urls = json.loads(dynamic_data)
                        # Pick highest resolution URL (largest dimensions)
                        sorted_urls = sorted(parsed_urls.keys(), key=lambda u: parsed_urls[u][0] * parsed_urls[u][1], reverse=True)
                        if sorted_urls:
                            img_url = sorted_urls[0]
                    except Exception:
                        pass
                
                if not img_url:
                    hires = img_elem.get_attribute("data-old-hires")
                    if hires and hires.startswith("http"):
                        img_url = hires
                    else:
                        img_url = img_elem.get_attribute("src")

            if img_url:
                # Upgrade image quality to max resolution (SL1500)
                img_url = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', img_url)
                print(f"   • Downloading high-res image: {img_url}")
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=15).read()
                raw_target.write_bytes(img_data)
                print(f"   ✅ Saved clean raw image: {raw_target.name}")
            else:
                print(f"   ⚠️ Could not locate image element for [{asin}]")

        except Exception as e:
            print(f"   ⚠️ Scrape image error for [{asin}]: {e}")

    browser.close()

print("\n==================================================")
print("🎉 ALL CLEAN RAW PRODUCT IMAGES DOWNLOADED & SAVED TO raw_images/")
print("==================================================")
