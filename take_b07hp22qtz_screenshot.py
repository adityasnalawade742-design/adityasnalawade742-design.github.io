import asyncio
import json
import sys
from pathlib import Path
from playwright.async_api import async_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
art_dir = Path(r"C:\Users\adity\.gemini\antigravity-cli\brain\ee05c394-54f8-4d2d-a754-b7f6bfd8e22e")

async def main():
    url = "https://www.amazon.com/dp/B07HP22QTZ"
    print(f"🌐 Navigating to {url}...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1400, "height": 900}
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=15000)
            await page.wait_for_timeout(4000)

            # Take screenshot of page
            screenshot_path = art_dir / "amazon_b07hp22qtz_page.png"
            await page.screenshot(path=str(screenshot_path), full_page=False)
            print(f"📸 Saved page screenshot to {screenshot_path}")

            # Get main image element
            main_img_el = await page.query_selector("#landingImage, #imgBlkFront, #main-image")
            main_img_src = ""
            if main_img_el:
                main_img_src = await main_img_el.get_attribute("src") or await main_img_el.get_attribute("data-old-hires") or ""
            
            print(f"📷 Main Landing Image SRC: {main_img_src}")

            # Download the main image directly
            if main_img_src:
                import urllib.request
                import re
                clean_src = re.sub(r'\._[A-Z0-9_,]+_\.', '.', main_img_src)
                req = urllib.request.Request(clean_src, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as resp, open(art_dir / "b07hp22qtz_actual_main.jpg", "wb") as out_f:
                    out_f.write(resp.read())
                print(f"✅ Saved main image to {art_dir / 'b07hp22qtz_actual_main.jpg'}")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
