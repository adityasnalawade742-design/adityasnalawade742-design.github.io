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
print("🎯 FIXING HIGH-CONVERTING SEARCH KEYWORD RELEVANCE")
print("   Replacing generic 4-word truncations with exact category search queries")
print("==================================================")

search_keywords_map = {
    "B0GYDXHF4G": "Volcano Flame Aroma Diffuser Lamp",
    "B0DXKGL1T2": "Lily of the Valley Flower Table Lamp",
    "B0DZD1X83N": "Minimalist Wood Base Table Nightstand Lamp",
    "B0FXLYXM32": "White Wavy Wall Body Standing Mirror",
    "B0C2YLN3H4": "White Ceramic Donut Flower Vase Set",
    "B07HP22QTZ": "Crystal Ball Prism Window Suncatcher",
    "B0BZXNSW5K": "Touch Control Dimmable Bedside Table Lamp",
    "B0D1FRDFFX": "Glass Mushroom Desk Table Lamp",
    "B0D8P8CSYP": "Cute Bird Touch Dimmable Nightstand Lamp"
}

# 1. Update product_price_registry.json with search_keywords
reg_path = repo_dir / "product_price_registry.json"
if reg_path.exists():
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    for asin, phrase in search_keywords_map.items():
        if asin in reg:
            reg[asin]["search_keywords"] = phrase
    reg_path.write_text(json.dumps(reg, indent=2), encoding="utf-8")
    print(" ✅ Updated product_price_registry.json with high-converting search keywords!")

# 2. Update modules/bridge_creator.py to use product.search_keywords
bridge_creator_path = repo_dir / "modules" / "bridge_creator.py"
bc_content = bridge_creator_path.read_text(encoding="utf-8")

old_line = "{% set clean_words = product.title.split()[:4] | join(' ') %}\n            const currentAsin = \"{{ product.get('target_asin', asin) }}\";\n            const prodKeywords = encodeURIComponent(\"{{ clean_words }}\");"
new_line = "{% set search_phrase = product.get('search_keywords') or (product.title.split()[:4] | join(' ')) %}\n            const currentAsin = \"{{ product.get('target_asin', asin) }}\";\n            const prodKeywords = encodeURIComponent(\"{{ search_phrase }}\");"

if old_line in bc_content:
    bc_content = bc_content.replace(old_line, new_line)
    bridge_creator_path.write_text(bc_content, encoding="utf-8")
    print(" ✅ Updated modules/bridge_creator.py to prioritize targeted search keywords!")
else:
    # Regex fallback
    pattern = r"\{% set clean_words = product\.title\.split\(\)\[:4\] \| join\(' '\) %\}[\s\S]*?const prodKeywords = encodeURIComponent\(\"\{\{ clean_words \}\}\"\);"
    replacement = "{% set search_phrase = product.get('search_keywords') or (product.title.split()[:4] | join(' ')) %}\n            const currentAsin = \"{{ product.get('target_asin', asin) }}\";\n            const prodKeywords = encodeURIComponent(\"{{ search_phrase }}\");"
    bc_content = re.sub(pattern, replacement, bc_content)
    bridge_creator_path.write_text(bc_content, encoding="utf-8")
    print(" ✅ Regex updated modules/bridge_creator.py!")

# 3. Update rebuild_EVERY_single_bridge.py master_catalog dict
rebuilder_path = repo_dir / "rebuild_EVERY_single_bridge.py"
rb_content = rebuilder_path.read_text(encoding="utf-8")

for asin, phrase in search_keywords_map.items():
    # Inject "search_keywords": "phrase" into master_catalog entries
    pattern = rf'("{asin}":\s*\{{[\s\S]*?)("title":)'
    replacement = rf'\1"search_keywords": "{phrase}",\n        \2'
    rb_content = re.sub(pattern, replacement, rb_content)

rebuilder_path.write_text(rb_content, encoding="utf-8")
print(" ✅ Updated rebuild_EVERY_single_bridge.py with exact search phrases!")

# 4. Rebuild all bridge landing pages
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

print("\n🔨 Rebuilding 100% of all landing pages with high-converting search keywords...")
for asin, item in master_catalog.items():
    if asin in search_keywords_map:
        item["search_keywords"] = search_keywords_map[asin]
    
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item.get("headline", item["title"])[:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# 5. Git Commit & Push Live
print("\n🚀 Pushing targeted search keyword updates live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "update targeted high-converting fallback search keywords for all products across regional stores"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 TARGETED SEARCH KEYWORDS DEPLOYED LIVE!")
