import asyncio
import json
import re
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
output_dir = repo / "b07hp22qtz_candidates"
output_dir.mkdir(exist_ok=True)

async def main():
    asin = "B07HP22QTZ"
    url = f"https://www.amazon.com/dp/{asin}"
    print(f"🌐 Fetching Amazon product images for [{asin}] via Playwright...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1400, "height": 900},
            extra_http_headers={
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            }
        )
        page = await context.new_page()
        
        try:
            resp = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(3000)
            content = await page.content()
            print(f"Page loaded! Content length: {len(content)} bytes")

            # Extract image URLs
            matches = re.findall(r'https://m\.media-amazon\.com/images/I/([A-Za-z0-9_\-]+)\.(?:jpg|png)', content)
            
            clean_ids = []
            seen = set()
            for m in matches:
                clean_id = m.split('.')[0]
                if len(clean_id) >= 8 and clean_id not in seen and not any(x in clean_id.lower() for x in ['sprite', 'icon', 'logo', 'play', 'badge', 'pxpe', 'ss40']):
                    seen.add(clean_id)
                    clean_ids.append(clean_id)

            print(f"📷 Found {len(clean_ids)} candidate image IDs!")

            import urllib.request
            headers = {"User-Agent": "Mozilla/5.0"}

            for idx, img_id in enumerate(clean_ids[:6], 1):
                img_url = f"https://m.media-amazon.com/images/I/{img_id}.jpg"
                save_path = output_dir / f"candidate_{idx}.jpg"
                try:
                    req = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_f:
                        out_f.write(response.read())
                    print(f"  • Option {idx}: {img_url}")
                except Exception as e_dl:
                    print(f"  ⚠️ Error downloading Option {idx}: {e_dl}")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
