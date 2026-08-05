import asyncio
import json
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
    print(f"🌐 Fetching Amazon product images for [{asin}] from {url}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9"}
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)
            
            # Extract main image & thumbnails
            img_urls = []
            
            # Extract hiRes / landing images from script tags or DOM
            script_content = await page.content()
            
            # Try finding hiRes images in JSON data inside scripts
            import re
            matches = re.findall(r'"hiRes"\s*:\s*"(https://m\.media-amazon\.com/images/I/[^"]+\.jpg)"', script_content)
            if matches:
                img_urls.extend(matches)
                
            # Try large image URLs
            large_matches = re.findall(r'"large"\s*:\s*"(https://m\.media-amazon\.com/images/I/[^"]+\.jpg)"', script_content)
            if large_matches:
                img_urls.extend(large_matches)

            # Fallback: query landing image element
            main_img = await page.query_selector("#landingImage, #imgBlkFront")
            if main_img:
                src = await main_img.get_attribute("src")
                if src:
                    img_urls.append(src)

            # Deduplicate preserving order
            unique_urls = []
            seen = set()
            for u in img_urls:
                # Clean thumbnail params to get max res
                clean_u = re.sub(r'\._[A-Z0-9_,]+_\.', '.', u)
                if clean_u not in seen:
                    seen.add(clean_u)
                    unique_urls.append(clean_u)

            print(f"📷 Found {len(unique_urls)} product candidate images!")

            # Download candidate images locally
            downloaded = []
            import urllib.request
            for idx, img_url in enumerate(unique_urls[:6], 1):
                save_path = output_dir / f"candidate_{idx}.jpg"
                try:
                    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as resp, open(save_path, 'wb') as out_f:
                        out_f.write(resp.read())
                    downloaded.append((idx, img_url, str(save_path)))
                    print(f"  • Candidate {idx}: {save_path.name} ({img_url})")
                except Exception as e_dl:
                    print(f"  ⚠️ Error downloading candidate {idx}: {e_dl}")

        except Exception as e:
            print(f"❌ Error fetching page: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
