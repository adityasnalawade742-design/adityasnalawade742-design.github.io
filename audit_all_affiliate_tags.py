import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent  # FIX: dynamic path, not hardcoded
index_file = repo / "index.html"

from modules.affiliate_manager import get_canonical_tag, load_affiliate_config

print("🔍 AUDITING ALL PRODUCTS ON HOMEPAGE & LANDING PAGES FOR ONELINK & FALLBACK TAG COMPLIANCE...\n")

if not index_file.exists():
    print("❌ index.html not found!")
    sys.exit(1)

html_content = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(html_content, "html.parser")

cards = soup.find_all("div", class_="card-wrapper")
print(f"📊 Found {len(cards)} active product cards on index.html:\n")

audit_summary = []
invalid_tag_conflicts = []

for i, card in enumerate(cards, 1):
    card_id = card.get("id", "")
    asin = card_id.replace("card-", "")
    
    link = card.find("a", class_="card")
    href = link.get("href", "") if link else ""
    title_el = card.find("h2")
    title = title_el.text.strip() if title_el else f"Product {asin}"
    
    bridge_path = repo / href.lstrip("./")
    
    has_canonical_tag = False
    has_india_tag = False
    has_tag_conflict = False
    buy_href_static = ""
    
    if bridge_path.exists():
        b_content = bridge_path.read_text(encoding="utf-8")
        b_soup = BeautifulSoup(b_content, "html.parser")
        
        buy_btn = b_soup.find(id="buyBtn")
        if buy_btn:
            buy_href_static = buy_btn.get("href", "")
            
        # Check for canonical tag (smartdeal0358-20)
        if "smartdeal0358-20" in b_content:
            has_canonical_tag = True
            
        # Check for India tag (smartdeal0358-21)
        if "smartdeal0358-21" in b_content:
            has_india_tag = True
            
        # Flag error if India tag smartdeal0358-21 is incorrectly used on amazon.com
        if "amazon.com/dp/" in b_content and "amazon.com/dp/" in buy_href_static and "tag=smartdeal0358-21" in buy_href_static:
            has_tag_conflict = True
            invalid_tag_conflicts.append(f"ASIN {asin}: India tag smartdeal0358-21 used on amazon.com URL!")
            
    print(f"[{i}] ASIN: {asin} ({title[:35]}...)")
    print(f"    Landing Page: {href}")
    print(f"    Static Button URL: {buy_href_static[:70]}...")
    print(f"    Canonical OneLink Tag (smartdeal0358-20): {'✅ YES' if has_canonical_tag else '❌ MISSING'}")
    print(f"    India Fallback Tag (smartdeal0358-21):    {'✅ YES' if has_india_tag else 'ℹ️ N/A'}\n")
    
    audit_summary.append({
        "asin": asin,
        "title": title,
        "href": href,
        "static_url": buy_href_static,
        "tagged": has_canonical_tag and not has_tag_conflict
    })

print("==================================================")
print("🏆 HOMEPAGE & LANDING PAGES ONELINK TAG AUDIT RESULT:")
print("==================================================")
all_tagged = all(item["tagged"] for item in audit_summary)
if invalid_tag_conflicts:
    print(f"❌ INVALID TAG CONFLICTS FOUND ({len(invalid_tag_conflicts)}):")
    for conflict in invalid_tag_conflicts:
        print(f"   • {conflict}")
elif all_tagged:
    print("✅ 100% OF ALL LANDING PAGES USE CANONICAL ONELINK TAG (smartdeal0358-20) & VERIFIED FALLBACKS!")
else:
    print("❌ SOME LANDING PAGES ARE MISSING CANONICAL ONELINK TAGS!")
