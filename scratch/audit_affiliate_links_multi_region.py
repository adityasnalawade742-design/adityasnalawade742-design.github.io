import sys
import time
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

print("==================================================")
print("🔑 DEEP AUDIT: AMAZON AFFILIATE TAG 'smartdeal0358-21'")
print("   Testing Multi-Region Geo-Redirects Across All 9 Products")
print("==================================================")

asins = ["B0DZD1X83N", "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4", "B07HP22QTZ", "B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP"]
test_regions = [
    ("US", "amazon.com"),
    ("UK", "amazon.co.uk"),
    ("IN", "amazon.in"),
    ("DE", "amazon.de"),
    ("CA", "amazon.ca"),
    ("JP", "amazon.co.jp"),
    ("AU", "amazon.com.au")
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for asin in asins:
        bridge_file = repo_dir / f"bridge_{asin}.html"
        assert bridge_file.exists(), f"Missing landing page for {asin}"

        print(f"\n📌 Auditing ASIN: {asin} ({bridge_file.name})")

        for country, expected_domain in test_regions:
            page.goto(f"file:///{bridge_file}?country={country}")
            time.sleep(0.3)

            # Get Buy button URL
            buy_btn = page.query_selector("a#buyBtn") or page.query_selector("a.btn-buy")
            buy_url = buy_btn.get_attribute("href") if buy_btn else "N/A"

            has_tag = "smartdeal0358-21" in buy_url
            has_domain = expected_domain in buy_url or "amazon.com" in buy_url

            status = "✅ PASS" if (has_tag and has_domain) else "❌ FAIL"
            print(f"   [{country}] Domain: {expected_domain} | Tag Present: {has_tag} | Status: {status}")
            print(f"        URL: {buy_url[:75]}...")

            results.append(has_tag and has_domain)

    browser.close()

print("\n==================================================")
if all(results):
    print("🎉 100% AUDIT PASS: Every product across every country contains tag 'smartdeal0358-21'!")
else:
    print("⚠️ Mismatches found during affiliate audit!")
print("==================================================")
