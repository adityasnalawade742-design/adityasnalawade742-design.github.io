import sys
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_mobile():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile Viewport: iPhone 14 Pro
        page = browser.new_page()
        page.set_viewport_size({"width": 393, "height": 852})
        page.goto("file:///G:/CLI/pinterest-auto-affiliate/index.html")
        page.screenshot(path="scratch/mobile_viewport_before.png", full_page=False)

        top_nav_box = page.locator(".top-nav").bounding_box()
        search_box = page.locator(".search-box").bounding_box()
        card_box = page.locator(".card").first.bounding_box()

        print("==================================================")
        print("📱 MOBILE VIEWPORT BOUNDING BOX ANALYSIS (393px width)")
        print(f" Top Nav Height: {top_nav_box['height']}px | Width: {top_nav_box['width']}px")
        print(f" Search Box Height: {search_box['height']}px | Width: {search_box['width']}px")
        print(f" Card 1 Height: {card_box['height']}px | Width: {card_box['width']}px")
        print("==================================================")

        browser.close()

if __name__ == "__main__":
    check_mobile()
