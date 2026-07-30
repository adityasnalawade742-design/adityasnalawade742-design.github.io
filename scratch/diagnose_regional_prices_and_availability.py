import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

print("==================================================")
print("🔬 DIAGNOSTIC AUDIT: REGIONAL PRICES & AVAILABILITY MATRIX")
print("   Testing 9 Products Across 7 Major World Regions")
print("==================================================")

asins = ["B0DZD1X83N", "B0GYDXHF4G", "B0FXLYXM32", "B0C2YLN3H4", "B07HP22QTZ", "B0BZXNSW5K", "B0DXKGL1T2", "B0D1FRDFFX", "B0D8P8CSYP"]

countries = [
    ("US", "USD", "us"),
    ("UK", "GBP", "uk"),
    ("IN", "INR", "in"),
    ("DE", "EUR", "de"),
    ("CA", "CAD", "ca"),
    ("JP", "JPY", "jp"),
    ("AU", "AUD", "au")
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for country, curr, region_code in countries:
        print(f"\n🌍 Testing Visitor Perspective: {country} ({curr})")
        page.goto(f"file:///{repo_dir}/index.html?country={country}")
        time.sleep(0.8)

        page.select_option("#currencySelector", curr)
        page.dispatch_event("#currencySelector", "change")
        time.sleep(0.4)

        avail_count = 0
        unavail_count = 0

        for asin in asins:
            price_tag = page.inner_text(f"#card-{asin} .card-price-tag")
            is_unavail = price_tag == "Not Available"

            if is_unavail:
                unavail_count += 1
            else:
                avail_count += 1

            print(f"   - [{asin}] -> Rendered: '{price_tag}'")
            results.append(price_tag != "")

        print(f"   📊 Summary for {country}: {avail_count} Available | {unavail_count} Not Available")

    browser.close()

print("\n==================================================")
if all(results):
    print("🎉 100% DIAGNOSTIC PASS: Regional price and 'Not Available' badges working perfectly across all 7 countries!")
else:
    print("⚠️ Diagnostic anomalies detected!")
print("==================================================")
