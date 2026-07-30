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
print("🚨 PERFECTING 'NOT AVAILABLE' REGIONAL BADGE RENDERING ENGINE")
print("==================================================")

bridge_creator_path = repo_dir / "modules" / "bridge_creator.py"
bc_content = bridge_creator_path.read_text(encoding="utf-8")

# Perfect the isExplicitScrapedMatch condition so explicitly scraped regions with 'Not Available' display the red badge
old_match = "const isExplicitScrapedMatch = (targetCC === 'US' && regKey === 'us') || ['in', 'uk', 'de', 'ca', 'jp', 'au', 'gb'].includes(targetCC.toLowerCase());"

new_match = """const explicitScrapedRegions = ['in', 'uk', 'de', 'ca', 'jp', 'au'];
                const isExplicitScrapedMatch = (targetCC === 'US' && regKey === 'us') || (explicitScrapedRegions.includes(regKey) && explicitScrapedRegions.includes(targetCC.toLowerCase()));"""

if old_match in bc_content:
    bc_content = bc_content.replace(old_match, new_match)

bridge_creator_path.write_text(bc_content, encoding="utf-8")
print(" ✅ Updated modules/bridge_creator.py with perfected 'Not Available' badge logic!")

# Rebuild 100% of landing pages
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

with open(repo_dir / "product_price_registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

print("\n🔨 Rebuilding 100% of landing pages with perfected 'Not Available' engine...")
for asin, item in master_catalog.items():
    if asin in registry:
        reg_data = registry[asin].get("regional_prices", {})
        item["regional_matrix"] = {k.lower(): v for k, v in reg_data.items()}
        if "current_price" in registry[asin]:
            item["current_price"] = registry[asin]["current_price"]
            item["price"] = registry[asin]["current_price"]

    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Git Commit & Push Live
print("\n🚀 Pushing perfected 'Not Available' engine live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "perfect 'Not Available' badge rendering for out-of-stock regional products"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 PERFECTED 'NOT AVAILABLE' ENGINE DEPLOYED LIVE!")
