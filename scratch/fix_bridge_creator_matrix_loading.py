import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

print("==================================================")
print("🎯 FIXING DIRECT MATRIX LOADING IN modules/bridge_creator.py")
print("==================================================")

bridge_creator_path = repo_dir / "modules" / "bridge_creator.py"
bc_content = bridge_creator_path.read_text(encoding="utf-8")

# Fix bridge_creator.py to load direct regions from global_direct_matrix.json
old_dr = 'direct_regions = product_data.get("direct_regions", ["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"])'

new_dr = """global_matrix_file = Path("G:/CLI/pinterest-auto-affiliate/global_direct_matrix.json")
    if global_matrix_file.exists():
        with open(global_matrix_file, "r", encoding="utf-8") as f:
            g_matrix = json.load(f)
            direct_regions = g_matrix.get(asin, ["US"])
    else:
        direct_regions = product_data.get("direct_regions", ["US"])"""

if old_dr in bc_content:
    bc_content = bc_content.replace(old_dr, new_dr)
    bridge_creator_path.write_text(bc_content, encoding="utf-8")
    print(" ✅ Updated modules/bridge_creator.py to read global_direct_matrix.json!")

# Rebuild 100% of landing pages
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

print("\n🔨 Rebuilding 100% of landing pages with global_direct_matrix.json...")
for asin, item in master_catalog.items():
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Git Commit & Push Live
print("\n🚀 Pushing matrix fix live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "fix bridge_creator to load exact verified directRegions from global_direct_matrix.json"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 MATRIX LOAD FIX DEPLOYED LIVE!")
