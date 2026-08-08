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
cand_dir = repo_dir / "scratch" / "B0GYDXHF4G_true_candidates"
cand_dir.mkdir(parents=True, exist_ok=True)

artifact_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0")
artifact_cand_dir = artifact_dir / "scratch" / "B0GYDXHF4G_true_candidates"
artifact_cand_dir.mkdir(parents=True, exist_ok=True)

asin = "B0GYDXHF4G"
url = f"https://www.amazon.com/dp/{asin}"

print(f"🔍 Scraping authentic Amazon listing for ASIN [{asin}] via Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    try:
        page.goto(url, timeout=20000, wait_until="domcontentloaded")
        time.sleep(2)

        title_elem = page.query_selector("#productTitle")
        title = title_elem.inner_text().strip() if title_elem else "Unknown Product"
        print(f"📌 Authentic Product Title on Amazon: '{title}'")

        # Extract images from thumbnail gallery
        img_elements = page.query_selector_all("#altImages ul li img, .imgTagWrapper img, #landingImage")
        found_urls = []
        for img in img_elements:
            src = img.get_attribute("src") or ""
            dynamic = img.get_attribute("data-a-dynamic-image") or ""
            if dynamic:
                try:
                    d_map = json.loads(dynamic)
                    sorted_d = sorted(d_map.keys(), key=lambda u: d_map[u][0] * d_map[u][1], reverse=True)
                    if sorted_d:
                        found_urls.append(sorted_d[0])
                except Exception:
                    pass
            if src and "http" in src and not any(x in src for x in ["icon", "sprite", "pixel", "video", "play"]):
                high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', src)
                if high_res not in found_urls:
                    found_urls.append(high_res)

        print(f"Retrieved {len(found_urls)} authentic images from Amazon:")
        headers = {"User-Agent": "Mozilla/5.0"}
        saved_count = 0

        for idx, u in enumerate(found_urls, 1):
            try:
                high_res = re.sub(r'\._[A-Z0-9_]+_\.', '._AC_SL1500_.', u)
                req = urllib.request.Request(high_res, headers=headers)
                data = urllib.request.urlopen(req, timeout=12).read()
                if len(data) > 5000:
                    saved_count += 1
                    f_repo = cand_dir / f"true_option_{saved_count}.jpg"
                    f_art = artifact_cand_dir / f"true_option_{saved_count}.jpg"
                    f_repo.write_bytes(data)
                    f_art.write_bytes(data)
                    print(f"  Option {saved_count}: Saved {f_repo.name} ({len(data)/1024:.1f} KB) - {high_res}")
                    if saved_count >= 8:
                        break
            except Exception as e:
                print(f"  Option {idx}: Error downloading {u}: {e}")

    except Exception as e:
        print(f"⚠️ Playwright error: {e}")

    browser.close()

print("==================================================")
