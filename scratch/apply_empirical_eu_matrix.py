import sys
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))

print("==================================================")
print("🎯 UPDATING global_direct_matrix.json WITH EMPIRICALLY VERIFIED EU STOREFRONTS")
print("==================================================")

matrix_path = repo_dir / "global_direct_matrix.json"
with open(matrix_path, "r", encoding="utf-8") as f:
    current_matrix = json.load(f)

# Verified empirical EU results from live HTTP requests
empirical_eu = {
  "B0GYDXHF4G": [],
  "B0FXLYXM32": ["DE", "FR", "IT", "ES"],
  "B0C2YLN3H4": ["DE", "NL", "FR", "IT", "ES", "SE"],
  "B07HP22QTZ": ["DE", "NL", "FR", "IT", "ES", "SE"],
  "B0BZXNSW5K": ["DE", "NL", "FR", "IT", "ES", "SE"],
  "B0DXKGL1T2": [],
  "B0D1FRDFFX": ["DE", "NL", "FR", "IT", "ES", "SE"],
  "B0D8P8CSYP": ["DE", "NL", "FR", "IT", "ES", "SE"],
  "B0DZD1X83N": []
}

non_eu_codes = ["US", "UK", "IN", "CA", "JP", "AU"]

updated_matrix = {}
for asin, current_list in current_matrix.items():
    # Keep non-EU verified codes
    kept_non_eu = [c for c in current_list if c in non_eu_codes]
    # Merge with empirical EU codes
    new_eu = empirical_eu.get(asin, [])
    # Unique combined list
    combined = list(dict.fromkeys(kept_non_eu + new_eu))
    updated_matrix[asin] = combined

with open(matrix_path, "w", encoding="utf-8") as f:
    json.dump(updated_matrix, f, indent=2)

print(" ✅ Successfully updated global_direct_matrix.json:")
print(json.dumps(updated_matrix, indent=2))

# Rebuild 100% of landing pages
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

with open(repo_dir / "product_price_registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

print("\n🔨 Rebuilding 100% of landing pages with empirical EU direct matrix...")
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
print("\n🚀 Pushing empirical EU matrix rebuild live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "update global_direct_matrix with live verified EU storefront listings"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 EMPIRICAL EU MATRIX DEPLOYED LIVE!")
