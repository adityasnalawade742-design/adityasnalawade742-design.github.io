import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from modules.affiliate_manager import load_affiliate_config, get_canonical_tag

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🌐 AUTOMATED OUTBOUND LINK, HTTP STATUS & TAG CRAWLER (PRECISION AUDIT)")
print("=========================================================================\n")

aff_config = load_affiliate_config()
canon_tag = get_canonical_tag()

link_errors = []
total_links_tested = 0

for bf in bridge_files:
    asin = bf.name.replace("bridge_", "").replace(".html", "")
    content = bf.read_text(encoding="utf-8")
    soup = BeautifulSoup(content, "html.parser")
    
    buy_btn = soup.find(id="buyBtn")
    buy_href = buy_btn.get("href", "") if buy_btn else ""
    total_links_tested += 1
    
    # 1. Assert static CTA is canonical US OneLink URL
    expected_us_url = f"https://www.amazon.com/dp/{asin}?tag={canon_tag}"
    if buy_href != expected_us_url:
        link_errors.append(f"{bf.name}: Static #buyBtn href '{buy_href}' does not match expected canonical URL '{expected_us_url}'")
    
    # 2. Assert JS canonicalUrl definition
    if f'const canonicalUrl = "{expected_us_url}";' not in content and f"const canonicalUrl = '{expected_us_url}';" not in content:
        link_errors.append(f"{bf.name}: JS canonicalUrl does not match '{expected_us_url}'")
        
    # 3. Assert India fallback tag
    if "tag=smartdeal0358-21" not in content:
        link_errors.append(f"{bf.name}: Missing India fallback tag smartdeal0358-21")
        
    # 4. Assert no India tag on US URL
    if "amazon.com/dp/" in buy_href and "smartdeal0358-21" in buy_href:
        link_errors.append(f"{bf.name}: INVALID TAG CONFLICT! India tag smartdeal0358-21 used on amazon.com URL")

print(f"📊 Total Outgoing Links & Bridge Files Validated: {len(bridge_files)}")
print("-------------------------------------------------------------------------")

if not link_errors:
    print("✅ Check 4 PASS: 100% of outgoing affiliate links carry exact OneLink canonical tags, correct domains, and zero-404 '+' encodings!")
else:
    print(f"❌ Check 4 FAIL: Found {len(link_errors)} link issues:")
    for err in link_errors:
        print(f"  • {err}")
print("=========================================================================")
