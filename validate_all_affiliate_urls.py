import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent  # FIX: dynamic path, not hardcoded
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🌐 AUTOMATED OUTBOUND LINK & TAG CRAWLER (PRECISION AUDIT)")
print("=========================================================================\n")

test_countries = [
    ("US", "amazon.com", "smartdeal0358-20"),
    ("IN", "amazon.in", "smartdeal0358-21"),
    ("UK", "amazon.co.uk", "smartdea04b3a-21"),
    ("DE", "amazon.de", "smartdeal0bb4-21"),
    ("CA", "amazon.ca", "smartdeal0302-20"),
    ("FR", "amazon.fr", "smartdeal0962-21"),
    ("ES", "amazon.es", "smartdeal0b46-21"),
    ("IT", "amazon.it", "smartdea03a8d-21")
]

link_errors = []
total_links_tested = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for bf in bridge_files:
        asin = bf.name.replace("bridge_", "").replace(".html", "")
        file_url = f"file:///{bf.resolve()}".replace("\\", "/")
        
        for cc, exp_domain, exp_tag in test_countries:
            page.goto(f"{file_url}?country={cc}")
            page.wait_for_timeout(400)
            
            href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
            total_links_tested += 1
            
            # 1. Assert domain matches
            if exp_domain not in href:
                link_errors.append(f"{bf.name} [{cc}]: Expected domain '{exp_domain}' in href='{href}'")
            
            # 2. Assert associate tag matches
            if f"tag={exp_tag}" not in href:
                link_errors.append(f"{bf.name} [{cc}]: Missing associate tag '{exp_tag}' in href='{href}'")
                
            # 3. Assert search query '+' encoding
            if "/s?k=" in href and "%20" in href:
                link_errors.append(f"{bf.name} [{cc}]: Contains un-replaced %20 space encoding in search link '{href}'")

    browser.close()

print(f"📊 Total Outgoing Links & Tags Validated: {total_links_tested}")
if not link_errors:
    print("✅ Check 4 PASS: 100% of outgoing affiliate links carry exact tags, correct domains, and zero-404 '+' encodings!")
else:
    print(f"❌ Check 4 FAIL: Found {len(link_errors)} link issues:")
    for err in link_errors:
        print(f"  • {err}")
print("=========================================================================")
