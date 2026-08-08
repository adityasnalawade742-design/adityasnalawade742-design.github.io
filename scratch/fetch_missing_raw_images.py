import sys
import json
import time
import urllib.request
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent.parent
raw_dir = repo_dir / "raw_images"
raw_dir.mkdir(exist_ok=True)

targets = [
    ("B0GYDXHF4G", "https://www.amazon.ca/dp/B0GYDXHF4G"),
    ("B07HP22QTZ", "https://www.amazon.co.uk/dp/B07HP22QTZ"),
    ("B0DXKGL1T2", "https://www.amazon.co.uk/dp/B0DXKGL1T2")
]

print("==================================================")
print("📥 FETCHING MISSING 3 RAW CLEAN IMAGES")
print("==================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for asin, url in targets:
        raw_target = raw_dir / f"raw_{asin}.jpg"
        print(f"\n🔍 Processing ASIN [{asin}] via {url}...")
        img_url = None

        try:
            page.goto(url, timeout=20000, wait_until="domcontentloaded")
            time.sleep(2)

            img_elem = page.query_selector("#landingImage") or page.query_selector("#imgBlkFront") or page.query_selector("#main-image") or page.query_selector(".imgTagWrapper img")
            if img_elem:
                dynamic_data = img_elem.get_attribute("data-a-dynamic-image")
                if dynamic_data:
                    try:
                        parsed_urls = json.loads(dynamic_data)
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
                img_url = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', img_url)
                print(f"   • Downloading high-res image: {img_url}")
                req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                img_data = urllib.request.urlopen(req, timeout=15).read()
                raw_target.write_bytes(img_data)
                print(f"   ✅ Saved clean raw image: {raw_target.name}")
            else:
                print(f"   ⚠️ Could not locate image element for [{asin}]")

        except Exception as e:
            print(f"   ⚠️ Error fetching image for [{asin}]: {e}")

    browser.close()

print("==================================================")
