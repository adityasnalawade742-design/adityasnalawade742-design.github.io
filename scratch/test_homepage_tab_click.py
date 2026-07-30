import sys
import time
from playwright.sync_api import sync_playwright

def test_click():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Browser PageError] {err}"))
        
        page.goto("http://localhost:5000/admin_console.html")
        print("Page loaded:", page.title())
        
        # Check initial visibility
        mode_batch_vis = page.is_visible("#modeBatch")
        mode_hp_vis = page.is_visible("#modeHomepage")
        print(f"Initial: modeBatch={mode_batch_vis}, modeHomepage={mode_hp_vis}")
        
        page.on("console", lambda msg: print(f"[Browser Console] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Browser PageError] {err}"))
        
        # Click Homepage Manager Tab
        print("Clicking #tabHomepage button via page.evaluate...")
        page.evaluate("switchMode('homepage')")
        time.sleep(1)
        
        mode_batch_vis2 = page.is_visible("#modeBatch")
        mode_hp_vis2 = page.is_visible("#modeHomepage")
        print(f"After Click: modeBatch={mode_batch_vis2}, modeHomepage={mode_hp_vis2}")
        
        cards = page.query_selector_all("#homepageProductsGrid .preview-card")
        print(f"Homepage Cards Rendered Count: {len(cards)}")
        
        for c in cards:
            text = c.inner_text()
            print(" - Card:", text.split('\n')[0])
            
        browser.close()

if __name__ == "__main__":
    test_click()
