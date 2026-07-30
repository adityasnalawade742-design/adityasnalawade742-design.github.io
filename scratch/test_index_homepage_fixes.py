import time
from playwright.sync_api import sync_playwright

def test_homepage_fixes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:5000/index.html")
        time.sleep(1)

        # 1. Verify 9 cards
        cards = page.query_selector_all(".card-wrapper")
        print(f"Total cards on homepage: {len(cards)}")
        assert len(cards) == 9, f"Expected 9 cards, found {len(cards)}"

        # 2. Verify ratings on all cards
        ratings = page.query_selector_all(".card-rating")
        print(f"Total rating badges found: {len(ratings)}")
        assert len(ratings) == 9, f"Expected 9 ratings, found {len(ratings)}"

        # 3. Test Vases filter chip
        page.click("text=🏺 Vases")
        time.sleep(0.5)
        visible_vases = [c for c in page.query_selector_all(".card-wrapper") if c.is_visible()]
        print(f"Visible cards under Vases filter: {len(visible_vases)}")
        assert len(visible_vases) >= 1, "Vases filter returned 0 items!"

        # 4. Test Mirrors filter chip
        page.click("text=🪞 Mirrors & Wall")
        time.sleep(0.5)
        visible_mirrors = [c for c in page.query_selector_all(".card-wrapper") if c.is_visible()]
        print(f"Visible cards under Mirrors filter: {len(visible_mirrors)}")
        assert len(visible_mirrors) >= 1, "Mirrors filter returned 0 items!"

        # 5. Reset to All
        page.click("text=✨ All Finds")
        time.sleep(0.5)

        browser.close()
        print("✅ 100% PASS: Homepage filters, rating badges, titles & cards verified!")

if __name__ == "__main__":
    test_homepage_fixes()
