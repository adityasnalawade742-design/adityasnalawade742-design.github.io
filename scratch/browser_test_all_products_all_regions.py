import sys
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path("G:/CLI/pinterest-auto-affiliate")
bridge_files = sorted(list(repo.glob("bridge_*.html")))

test_regions = [
    ("US", "amazon.com", "smartdeal0358-20"),
    ("IN", "amazon.in", "smartdeal0358-21"),
    ("UK", "amazon.co.uk", "smartdea04b3a-21"),
    ("DE", "amazon.de", "smartdeal0bb4-21"),
    ("CA", "amazon.ca", "smartdeal0302-20"),
    ("AU", "amazon.com.au", "smartdeal0358-20"),
    ("JP", "amazon.co.jp", "smartdeal0358-20"),
    ("CH", "amazon.de", "smartdeal0bb4-21"),
    ("SE", "amazon.se", "smartdeal0bb4-21")
]

print("=========================================================================")
print("🌐 BROWSER-LEVEL DOM AUTOMATION AUDIT: 100% PRODUCTS & ALL REGIONS")
print("=========================================================================\n")

failures = []
passed_tests = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    for bridge_path in bridge_files:
        asin = bridge_path.name.replace("bridge_", "").replace(".html", "")
        file_url = f"file:///{bridge_path.resolve()}".replace("\\", "/")
        print(f"📦 Auditing Product [{asin}]: {bridge_path.name}")
        
        for cc, exp_domain, exp_tag in test_regions:
            target_url = f"{file_url}?country={cc}"
            page.goto(target_url)
            page.wait_for_timeout(100) # Give 100ms for script execution
            
            href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
            btn_text = page.evaluate("document.getElementById('buyBtnText') ? document.getElementById('buyBtnText').innerText : ''")
            hero_price = page.evaluate("document.querySelector('.hero-price') ? document.querySelector('.hero-price').innerText : ''")
            
            # Validations
            has_domain = exp_domain in href
            has_tag = f"tag={exp_tag}" in href
            has_valid_href = href.startswith("https://")
            
            if not (has_domain and has_tag and has_valid_href):
                err = f"❌ [{asin} | {cc}] Bad Link: href='{href}' (Expected domain '{exp_domain}', tag '{exp_tag}')"
                failures.append(err)
                print(f"   • {cc}: {err}")
            else:
                passed_tests += 1
                print(f"   • {cc} ➔ Domain: {exp_domain} | Tag: {exp_tag} | Price: {hero_price[:12]} | CTA: '{btn_text}' | ✅ PASS")
                
    browser.close()

print("\n=========================================================================")
print("🏆 PLAYWRIGHT BROWSER DOM AUDIT RESULTS:")
print("=========================================================================")
if not failures:
    print(f"✅ 100% PASS: ALL {len(bridge_files)} LANDING PAGES ACROSS ALL {len(test_regions)} REGIONS PASSED BROWSER-LEVEL DOM EXECUTION!")
    print(f"✅ Total Assertions Verified: {passed_tests}")
else:
    print(f"❌ FAIL: Found {len(failures)} DOM failures:")
    for f in failures:
        print(f"  {f}")
print("=========================================================================")
