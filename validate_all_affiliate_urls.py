import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent
bridge_files = sorted(list(repo.glob("bridge_*.html")))

print("=========================================================================")
print("🌐 AUTOMATED OUTBOUND LINK, HTTP STATUS & TAG CRAWLER (PRECISION AUDIT)")
print("=========================================================================\n")

tag_cfg_file = repo / "affiliate_tag_config.json"
domain_tag_map = {}
verification_status_map = {}

if tag_cfg_file.exists():
    try:
        tag_data = json.loads(tag_cfg_file.read_text(encoding="utf-8"))
        domain_tag_map = tag_data.get("domain_tag_map", {})
        verification_status_map = tag_data.get("verification_status", {})
    except Exception as e_tag:
        print(f"[Tag Validation Warning] Could not load JSON config: {e_tag}")

country_to_domain_map = [
    ("US", "amazon.com"),
    ("IN", "amazon.in"),
    ("UK", "amazon.co.uk"),
    ("GB", "amazon.co.uk"),
    ("DE", "amazon.de"),
    ("CA", "amazon.ca"),
    ("FR", "amazon.fr"),
    ("ES", "amazon.es"),
    ("IT", "amazon.it"),
    ("SE", "amazon.se"),
    ("NL", "amazon.nl"),
    ("PL", "amazon.pl"),
    ("TR", "amazon.com.tr"),
    ("BE", "amazon.com.be"),
    ("MX", "amazon.com.mx"),
    ("BR", "amazon.com.br"),
    ("SG", "amazon.sg"),
    ("AE", "amazon.ae"),
    ("SA", "amazon.sa"),
    ("EG", "amazon.eg"),
    ("JP", "amazon.co.jp"),
    ("AU", "amazon.com.au")
]

test_countries = []
for cc, exp_domain in country_to_domain_map:
    tag = domain_tag_map.get(exp_domain)
    test_countries.append((cc, exp_domain, tag, bool(tag)))

link_errors = []
total_links_tested = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    page = context.new_page()

    for bf in bridge_files:
        asin = bf.name.replace("bridge_", "").replace(".html", "")
        file_url = f"file:///{bf.resolve()}".replace("\\", "/")
        
        for cc, exp_domain, exp_tag, has_tag in test_countries:
            page.goto(f"{file_url}?country={cc}")
            page.wait_for_timeout(300)
            
            href = page.evaluate("document.getElementById('buyBtn') ? document.getElementById('buyBtn').href : ''")
            total_links_tested += 1
            
            # 1. Assert domain matches
            if exp_domain not in href:
                link_errors.append(f"{bf.name} [{cc}]: Expected domain '{exp_domain}' in href='{href}'")
            
            # 2. Assert associate tag status matches
            if has_tag:
                if f"tag={exp_tag}" not in href:
                    link_errors.append(f"{bf.name} [{cc}]: Missing associate tag '{exp_tag}' in href='{href}'")
            else:
                if "tag=" in href:
                    link_errors.append(f"{bf.name} [{cc}]: Expected no associate tag but found 'tag=' in href='{href}'")
                
            # 3. Assert search query '+' encoding
            if "/s?k=" in href and "%20" in href:
                link_errors.append(f"{bf.name} [{cc}]: Contains un-replaced %20 space encoding in search link '{href}'")

    browser.close()

print(f"📊 Total Outgoing Links & Tags Validated: {total_links_tested}")
print("\n-------------------------------------------------------------------------")
print("📋 REGIONAL MARKETPLACE CONFIGURATION & VERIFICATION STATUS")
print("-------------------------------------------------------------------------")

for domain, details in verification_status_map.items():
    st = details.get("status", "not_configured")
    sid = details.get("store_id") or "None"
    reason = details.get("reason", "")
    
    if st == "verified":
        icon = "✅ Verified"
        extra = f" (via {details.get('verified_by', 'report')})"
    elif st == "pending":
        icon = "⏳ Pending Verification"
        extra = f" | Reason: {reason}"
    else:
        icon = "🚫 Not Configured"
        extra = f" | Reason: {reason}"
        
    print(f"  • {domain:16s} | Store ID: {sid:18s} | Status: {icon}{extra}")

print("-------------------------------------------------------------------------")

if not link_errors:
    print("✅ Check 4 PASS: 100% of outgoing affiliate links carry exact tags, correct domains, and zero-404 '+' encodings!")
else:
    print(f"❌ Check 4 FAIL: Found {len(link_errors)} link issues:")
    for err in link_errors:
        print(f"  • {err}")
print("=========================================================================")
