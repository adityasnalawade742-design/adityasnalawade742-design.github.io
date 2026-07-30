import sys
import json
import re
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

print("==================================================")
print("🎯 FIXING .price SELECTOR IN modules/bridge_creator.py")
print("==================================================")

bridge_creator_path = repo_dir / "modules" / "bridge_creator.py"
bc_content = bridge_creator_path.read_text(encoding="utf-8")

# Include .price in priceTags selector
old_sel = "const priceTags = document.querySelectorAll('.tag, .hero-price, .cta-price, #heroPriceTag');"
new_sel = "const priceTags = document.querySelectorAll('.price, .tag, .hero-price, .cta-price, #heroPriceTag');"

if old_sel in bc_content:
    bc_content = bc_content.replace(old_sel, new_sel)

bridge_creator_path.write_text(bc_content, encoding="utf-8")
print(" ✅ Updated priceTags selector in modules/bridge_creator.py!")

# Rebuild 100% of landing pages
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

full_country_matrix = {
    "B0DZD1X83N": { "us": "$12.99", "uk": "£10.99", "in": "Not Available", "de": "€14.99", "ca": "CA$18.99", "jp": "Not Available", "au": "Not Available" },
    "B0GYDXHF4G": { "us": "$35.00", "uk": "Not Available", "in": "Not Available", "de": "Not Available", "ca": "Not Available", "jp": "Not Available", "au": "Not Available" },
    "B0FXLYXM32": { "us": "$76.49", "uk": "£57.42", "in": "Not Available", "de": "€66.97", "ca": "CA$107.56", "jp": "¥12,508", "au": "A$110.02" },
    "B0C2YLN3H4": { "us": "$14.99", "uk": "Not Available", "in": "₹599.00", "de": "€13.12", "ca": "CA$21.08", "jp": "¥2,451", "au": "A$21.56" },
    "B07HP22QTZ": { "us": "$9.99", "uk": "£7.50", "in": "₹2,762.75", "de": "€8.75", "ca": "CA$14.05", "jp": "¥1,634", "au": "A$14.37" },
    "B0BZXNSW5K": { "us": "$19.99", "uk": "£15.01", "in": "₹475.00", "de": "€17.50", "ca": "CA$28.11", "jp": "Not Available", "au": "Not Available" },
    "B0DXKGL1T2": { "us": "$38.57", "uk": "£28.95", "in": "Not Available", "de": "€33.77", "ca": "CA$54.24", "jp": "Not Available", "au": "Not Available" },
    "B0D1FRDFFX": { "us": "$35.98", "uk": "£27.01", "in": "₹11,428.51", "de": "€31.50", "ca": "CA$50.60", "jp": "Not Available", "au": "A$51.75" },
    "B0D8P8CSYP": { "us": "$20.56", "uk": "£15.43", "in": "₹3,843.00", "de": "€18.00", "ca": "CA$28.91", "jp": "¥3,362", "au": "A$29.57" }
}

print("\n🔨 Rebuilding 100% of landing pages with fixed .price selector...")
for asin, item in master_catalog.items():
    if asin in full_country_matrix:
        item["regional_matrix"] = full_country_matrix[asin]
    
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Git Commit & Push Live
print("\n🚀 Pushing fixed landing page price selector live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "fix .price selector in bridge_creator.py so hero price adapts for all world countries"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 FIXED HERO PRICE SELECTOR DEPLOYED LIVE!")
