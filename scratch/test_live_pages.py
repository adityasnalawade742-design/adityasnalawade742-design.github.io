from playwright.sync_api import sync_playwright

def run_live_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        test_countries = ['NL', 'PL', 'SE', 'UK', 'IN']
        
        print("\n=========================================================================")
        print("LIVE GITHUB PAGES CDN VERIFICATION REPORT FOR ONELINK ROUTING")
        print("=========================================================================\n")
        
        for cc in test_countries:
            url = f"https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html?country={cc}"
            page.goto(url)
            page.wait_for_timeout(600)
            
            href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
            badge = page.evaluate("document.querySelector('.prime-badge') ? document.querySelector('.prime-badge').innerText : ''")
            price = page.evaluate("document.querySelector('.price') ? document.querySelector('.price').innerText : ''")
            tag = page.evaluate("document.querySelector('.tag') ? document.querySelector('.tag').innerText : ''")
            
            badge_clean = badge.encode('ascii', 'ignore').decode('ascii')
            tag_clean = tag.encode('ascii', 'ignore').decode('ascii')
            price_clean = price.encode('ascii', 'ignore').decode('ascii')
            
            print(f"Country: {cc:<4} | Href: {href}")
            print(f"       | Shipping Badge: {badge_clean}")
            print(f"       | Display Price: {price_clean} ({tag_clean})\n")
            
        browser.close()

if __name__ == "__main__":
    run_live_verification()
