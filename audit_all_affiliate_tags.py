import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path(__file__).resolve().parent  # FIX: dynamic path, not hardcoded
index_file = repo / "index.html"

print("🔍 AUDITING ALL PRODUCTS ON HOMEPAGE & LANDING PAGES FOR AFFILIATE TAG 'smartdeal0358-21'...\n")

if not index_file.exists():
    print("❌ index.html not found!")
    sys.exit(1)

html_content = index_file.read_text(encoding="utf-8")
soup = BeautifulSoup(html_content, "html.parser")

cards = soup.find_all("div", class_="card-wrapper")
print(f"📊 Found {len(cards)} active product cards on index.html:\n")

audit_summary = []

for i, card in enumerate(cards, 1):
    card_id = card.get("id", "")
    asin = card_id.replace("card-", "")
    
    link = card.find("a", class_="card")
    href = link.get("href", "") if link else ""
    title_el = card.find("h2")
    title = title_el.text.strip() if title_el else f"Product {asin}"
    
    bridge_path = repo / href.lstrip("./")
    
    has_tag_in_html = False
    has_tag_in_js = False
    buy_href_static = ""
    
    if bridge_path.exists():
        b_content = bridge_path.read_text(encoding="utf-8")
        b_soup = BeautifulSoup(b_content, "html.parser")
        
        buy_btn = b_soup.find(id="buyBtn")
        if buy_btn:
            buy_href_static = buy_btn.get("href", "")
            
        # Check for tag in static HTML
        if "smartdeal0358-21" in b_content:
            has_tag_in_html = True
            
        # Check for tag in JavaScript geo-redirect function
        if "tag=smartdeal0358-21" in b_content:
            has_tag_in_js = True
            
    print(f"[{i}] ASIN: {asin} ({title[:35]}...)")
    print(f"    Landing Page: {href}")
    print(f"    Static Button URL: {buy_href_static[:70]}...")
    print(f"    Tag Present in HTML/JS: {'✅ YES (smartdeal0358-21)' if has_tag_in_html or has_tag_in_js else '❌ MISSING'}\n")
    
    audit_summary.append({
        "asin": asin,
        "title": title,
        "href": href,
        "static_url": buy_href_static,
        "tagged": has_tag_in_html or has_tag_in_js
    })

print("==================================================")
print("🏆 HOMEPAGE & LANDING PAGES AFFILIATE TAG AUDIT RESULT:")
print("==================================================")
all_tagged = all(item["tagged"] for item in audit_summary)
if all_tagged:
    print("✅ 100% OF ALL PRODUCTS ON THE HOMEPAGE CONTAIN YOUR AFFILIATE TAG (smartdeal0358-21)!")
else:
    print("❌ SOME PRODUCTS ARE MISSING YOUR AFFILIATE TAG!")
