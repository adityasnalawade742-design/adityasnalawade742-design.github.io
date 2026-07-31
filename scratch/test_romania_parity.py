import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Test Homepage RO
    page.goto(f"file:///{ (repo / 'index.html').resolve() }?country=RO".replace("\\", "/"))
    page.wait_for_timeout(200)
    page.select_option("#currencySelector", "RON")
    page.wait_for_timeout(200)
    hp_price = page.evaluate("document.querySelector('#card-B0GYDXHF4G .card-price-tag').innerText")
    
    # Test Bridge RO
    page.goto(f"file:///{ (repo / 'bridge_B0GYDXHF4G.html').resolve() }?country=RO".replace("\\", "/"))
    page.wait_for_timeout(200)
    bridge_price = page.evaluate("(document.querySelector('.tag') || document.querySelector('.price') || {}).innerText || ''")
    
    print(f"🇷🇴 Romania Homepage Price: {hp_price}")
    print(f"🇷🇴 Romania Bridge Page Price: {bridge_price}")
    
    browser.close()
