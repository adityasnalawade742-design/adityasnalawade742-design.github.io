import time
from playwright.sync_api import sync_playwright

def test_modal_prices():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:5000/admin_console.html")
        page.click("#tabHomepage")
        time.sleep(1)

        # Check products in homepage grid
        cards = page.query_selector_all("#homepageProductsGrid .preview-card")
        print(f"Testing price binding for {len(cards)} homepage products...")

        results = []
        for card in cards:
            card_id = card.get_attribute("id") # hp-card-ASIN
            asin = card_id.replace("hp-card-", "")
            
            # Click edit tag button for this card
            btn = card.query_selector("button:has-text('Edit Price Tag')")
            btn.click()
            time.sleep(0.5)

            # Check modal price text
            modal_price = page.inner_text("#liveTagPriceText")
            card_price = card.query_selector("span").inner_text()

            print(f"ASIN {asin}: Card Price='{card_price}', Modal Price='{modal_price}'")
            results.append(card_price == modal_price)

            # Close modal
            page.click("button:has-text('✕ Close Window')")
            time.sleep(0.3)

        browser.close()
        assert all(results), "Mismatch in modal prices!"
        print("✅ 100% PASS: Every product modal dynamically displays its exact matching price!")

if __name__ == "__main__":
    test_modal_prices()
