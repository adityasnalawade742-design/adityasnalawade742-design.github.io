import sys
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
index_file = repo / "index.html"
registry_file = repo / "product_price_registry.json"
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🧪 ULTIMATE END-TO-END FEATURE VERIFICATION SUITE")
print("=========================================================================\n")

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # ---------------------------------------------------------------------
    # TEST 1: Homepage Showcase & Currency Selector (index.html)
    # ---------------------------------------------------------------------
    print("📌 [1/5] Testing Homepage Showcase & Currency Selector...")
    index_url = f"file:///{index_file.resolve()}".replace("\\", "/")
    page.goto(index_url)
    page.wait_for_timeout(100)

    # Test switching currency to INR
    page.select_option("#currencySelector", "INR")
    page.wait_for_timeout(100)
    inr_price = page.evaluate("document.querySelector('#card-B0BZXNSW5K .card-price-tag').innerText")
    
    if inr_price == "₹475.00":
        results.append("✅ Homepage Currency Selector (INR -> ₹475.00): PASS")
    else:
        results.append(f"❌ Homepage Currency Selector FAIL: got '{inr_price}'")

    # ---------------------------------------------------------------------
    # TEST 2: Bridge Page Dynamic Geo-Redirector (?country=IN)
    # ---------------------------------------------------------------------
    print("📌 [2/5] Testing Bridge Page Dynamic Geo-Redirector (India ?country=IN)...")
    suncatcher_url = f"file:///{ (repo / 'bridge_B07HP22QTZ.html').resolve() }?country=IN".replace("\\", "/")
    page.goto(suncatcher_url)
    page.wait_for_timeout(100)

    hero_p = page.evaluate("(document.querySelector('.tag') || document.querySelector('.price') || {}).innerText || ''")
    btn_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
    btn_text = page.evaluate("document.getElementById('buyBtnText') ? document.getElementById('buyBtnText').innerText : ''")

    if "₹2,760.15" in hero_p and "tag=smartdeal0358-21" in btn_href and "amazon.in" in btn_href:
        results.append("✅ Suncatcher Bridge Page (India ?country=IN -> ₹2,760.15, smartdeal0358-21): PASS")
    else:
        results.append(f"❌ Suncatcher Bridge Page FAIL: hero_p='{hero_p}', href='{btn_href}'")

    # ---------------------------------------------------------------------
    # TEST 3: Glass Mushroom Lamp Bridge Page (?country=IN)
    # ---------------------------------------------------------------------
    print("📌 [3/5] Testing Glass Mushroom Lamp Bridge Page (?country=IN)...")
    mushroom_url = f"file:///{ (repo / 'bridge_B0D1FRDFFX.html').resolve() }?country=IN".replace("\\", "/")
    page.goto(mushroom_url)
    page.wait_for_timeout(100)

    mush_price = page.evaluate("(document.querySelector('.tag') || document.querySelector('.price') || {}).innerText || ''")
    mush_href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")

    if "₹11,299.51" in mush_price and "smartdeal0358-21" in mush_href:
        results.append("✅ Glass Mushroom Lamp (India ?country=IN -> ₹11,299.51, smartdeal0358-21): PASS")
    else:
        results.append(f"❌ Glass Mushroom Lamp FAIL: price='{mush_price}', href='{mush_href}'")

    # ---------------------------------------------------------------------
    # TEST 4: European Germany Geo-Redirector (?country=DE)
    # ---------------------------------------------------------------------
    print("📌 [4/5] Testing European Germany Geo-Redirector (?country=DE)...")
    de_url = f"file:///{ (repo / 'bridge_B0BZXNSW5K.html').resolve() }?country=DE".replace("\\", "/")
    page.goto(de_url)
    page.wait_for_timeout(100)

    de_href = page.evaluate("document.getElementById('buyBtn').href")
    
    if "amazon.de" in de_href and "tag=smartdeal0bb4-21" in de_href:
        results.append("✅ Touch Lamp Germany (?country=DE -> amazon.de, smartdeal0bb4-21): PASS")
    else:
        results.append(f"❌ Touch Lamp Germany FAIL: href='{de_href}'")

    # ---------------------------------------------------------------------
    # TEST 5: Two-Tier Out of Stock Badge (Flame Diffuser ?country=IN)
    # ---------------------------------------------------------------------
    print("📌 [5/5] Testing Out of Stock Badge (Flame Diffuser ?country=IN)...")
    flame_url = f"file:///{ (repo / 'bridge_B0GYDXHF4G.html').resolve() }?country=IN".replace("\\", "/")
    page.goto(flame_url)
    page.wait_for_timeout(100)

    flame_badge = page.evaluate("document.querySelector('.tag') ? document.querySelector('.tag').innerText : ''")
    
    if "OUT OF STOCK" in flame_badge or "UNLISTED" in flame_badge:
        results.append("✅ Flame Diffuser Status Badge (Out of Stock / Unlisted Badge): PASS")
    else:
        results.append(f"❌ Flame Diffuser Status Badge FAIL: badge='{flame_badge}'")

    browser.close()

print("\n=========================================================================")
print("🏆 END-TO-END FEATURE VERIFICATION SUMMARY:")
print("=========================================================================")
for res in results:
    print(f"  {res}")
print("=========================================================================")
