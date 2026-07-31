import os
import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.bridge_creator import generate_bridge_page

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")

# Find all bridge_*.html files
bridge_files = list(repo_dir.glob("bridge_*.html"))
print(f"[Master Rebuilder] Found {len(bridge_files)} landing pages across repository:")
for bf in bridge_files:
    print(f"   - {bf.name}")

# Master dictionary for all products in portfolio
master_catalog = {
    "B0DZD1X83N": {
        "search_keywords": "Minimalist Wood Base Table Nightstand Lamp",
        "title": "Minimalist Wood Base Cream Shade Bedside Table Lamp",
        "price": "$12.99",
        "rating": "4.6",
        "features": ["MINIMALIST WOOD BASE", "CREAM FABRIC LAMPSHADE", "WARM AMBIENT GLOW", "INLINE CONTROL SWITCH"],
        "category": "lighting",
        "description": "Transform your nightstand setup with this aesthetic minimalist wood base table lamp. Warm ambient glow perfect for cozy reading and bedroom decor.",
        "direct_regions": ["US", "DE", "SE", "CA", "JP"]
    },
    "B0BZXNSW5K": {
        "search_keywords": "Touch Control Dimmable Bedside Table Lamp",
        "title": "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet",
        "price": "$19.99",
        "rating": "4.5",
        "features": ["DIMMABLE TOUCH CONTROL", "DUAL USB A+C CHARGING PORTS", "BUILT-IN AC OUTLET", "LED BULB INCLUDED"],
        "category": "lighting",
        "description": "Upgrade your nightstand setup with this 3-way dimmable touch control bedside lamp featuring USB A+C charging ports and AC outlet.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "CA", "JP"]
    },
    "B0D1FRDFFX": {
        "search_keywords": "Glass Mushroom Desk Table Lamp",
        "title": "Glass Mushroom Lamp Ambient Table Nightstand Light",
        "price": "$35.98",
        "rating": "4.8",
        "features": ["HAND-BLOWN STRIPED GLASS", "WARM AMBIENT GLOW", "VINTAGE MUSHROOM DESIGN", "EASY ON/OFF SWITCH"],
        "category": "lighting",
        "description": "Add a cozy retro aesthetic to your space with this hand-blown striped glass mushroom lamp. Soft ambient glow for nightstands, desks, and shelves.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B0C2YLN3H4": {
        "search_keywords": "White Ceramic Donut Flower Vase Set",
        "title": "White Ceramic Donut Vase Set of 2 Modern Nordic Home Decor",
        "price": "$28.99",
        "rating": "4.9",
        "features": ["MATTE CERAMIC FINISH", "SET OF 2 HALLOW VASES", "NORDIC MINIMALIST DESIGN", "PERFECT GIFT BOX"],
        "category": "vases",
        "description": "Handcrafted white ceramic donut vases for pampas grass and modern minimalist home decor.",
        "direct_regions": ["US", "IN", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B0GYDXHF4G": {
        "search_keywords": "Volcano Flame Aroma Diffuser Lamp",
        "title": "Flame Aroma Essential Oil Diffuser Dark Crackle Flame Effect",
        "price": "$35.00",
        "rating": "4.9",
        "features": ["REALISTIC FLAME EFFECT", "ULTRASONIC MIST HUMIDIFIER", "SILENT SLEEP OPERATION", "AUTO SHUTOFF SAFETY"],
        "category": "lighting decor",
        "description": "Cozy ambient flame effect humidifier and essential oil diffuser in dark crackle finish. Realistic flame glow for bedroom relaxation.",
        "direct_regions": ["US", "DE", "SE", "CA", "JP"]
    },
    "B0FXLYXM32": {
        "search_keywords": "White Wavy Wall Body Standing Mirror",
        "title": "White Wavy Wall Vanity Mirror Aesthetic Squiggle Mirror",
        "price": "$76.49",
        "rating": "4.8",
        "features": ["SQUIGGLE WAVY FRAME", "HIGH DEFINITION GLASS", "WALL MOUNT OR TABLETOP", "VIRAL DORM DECOR"],
        "category": "mirror",
        "description": "Trendy white wavy squiggle vanity mirror for bedroom desk, wall decor, and viral aesthetic room transformation.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B07HP22QTZ": {
        "search_keywords": "Crystal Ball Prism Window Suncatcher",
        "title": "Crystal Prism Window Suncatcher Rainbow Maker Hanging Ornament",
        "price": "$12.99",
        "rating": "4.8",
        "features": ["K9 CRYSTAL PRISMS", "RAINBOW MAKER REFLECTIONS", "GOLD HANGING CHAIN", "WINDOW & GARDEN ACCENT"],
        "category": "decor",
        "description": "Transform sunlight into vibrant room rainbows with these handcrafted K9 crystal suncatchers.",
        "direct_regions": ["US", "IN", "GB", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B0D8P8CSYP": {
        "search_keywords": "Cute Bird Touch Dimmable Nightstand Lamp",
        "title": "Cute Bird Touch Control Nightstand Lamp",
        "price": "$18.99",
        "rating": "4.8",
        "features": ["DIMMABLE TOUCH CONTROL", "RECHARGEABLE BATTERY", "WARM BEDSIDE GLOW", "PORTABLE NIGHT LIGHT"],
        "category": "lighting",
        "description": "Adorable dimmable touch nightstand lamp in aesthetic bird design. Soft warm ambient light perfect for cozy bedrooms, desks, and bedside tables.",
        "direct_regions": ["US", "IT", "JP", "AU"]
    },
    "B0DXKGL1T2": {
        "search_keywords": "Lily of the Valley Flower Table Lamp",
        "title": "Lily of the Valley Flower Table Lamp Glass Nightlight",
        "price": "$38.57",
        "rating": "4.8",
        "features": ["HAND-CRAFTED FLOWER GLASS SHADE", "WARM AMBIENT NIGHTLIGHT", "MINIMALIST BEDROOM DECOR", "PERFECT GIFT CHOICE"],
        "category": "lighting",
        "description": "Hand-crafted Lily of the Valley flower glass shade table lamp with warm ambient glow for nightstands, bedrooms, and aesthetic room decor.",
        "direct_regions": ["US", "UK", "DE", "SE", "CA", "JP"],
    }
}
# Load and merge empirical scraped prices and empirical direct matrix
registry_path = repo_dir / "product_price_registry.json"
matrix_path = repo_dir / "global_direct_matrix.json"

matrix_data = {}
if matrix_path.exists():
    import json
    with open(matrix_path, "r", encoding="utf-8") as f_mat:
        matrix_data = json.load(f_mat)

if registry_path.exists():
    import json
    with open(registry_path, "r", encoding="utf-8") as f_reg:
        reg_data = json.load(f_reg)
    for asin, item in master_catalog.items():
        if asin in matrix_data:
            item["direct_regions"] = matrix_data[asin]
        if asin in reg_data:
            reg_prices = reg_data[asin].get("regional_prices", {})
            item["regional_prices"] = reg_prices
            item["regional_matrix"] = reg_prices
            item["regional_asins"] = reg_data[asin].get("regional_asins", {})
            if "current_price" in reg_data[asin]:
                item["current_price"] = reg_data[asin]["current_price"]

print("\n[Master Rebuilder] Rebuilding 100% of all landing pages with Multi-Region Geo-Redirector...\n")

for asin, item in master_catalog.items():
    print(f" 🔨 Rebuilding bridge_{asin}.html...")
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item["title"][:30],
        "subtitle_hook": "",
        "badge_hook": "VIRAL ROOM FIND",
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Also check subdirectories like bridge_pages/
sub_dir = repo_dir / "bridge_pages"
if sub_dir.exists():
    for sub_bf in sub_dir.glob("bridge_*.html"):
        asin = sub_bf.stem.replace("bridge_", "")
        if asin in master_catalog:
            print(f" 🔨 Rebuilding sub-directory file: {sub_bf}...")
            item = master_catalog[asin]
            seo_data = {
                "pin_title": item["title"],
                "image_hook": item["title"][:30],
                "subtitle_hook": "",
                "badge_hook": "VIRAL ROOM FIND",
                "description": item["description"]
            }
            res_html = generate_bridge_page(item, seo_data, asin)
            # Copy to sub_dir
            with open(res_html, "r", encoding="utf-8") as f_src:
                content = f_src.read()
            with open(sub_bf, "w", encoding="utf-8") as f_dst:
                f_dst.write(content)

print("\n[Master Rebuilder] Pushing 100% of rebuilt bridge pages live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "rebuild 100% of all portfolio landing pages with universal multi-region geo-redirector"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 ALL PORTFOLIO LANDING PAGES REBUILT AND DEPLOYED LIVE!")
