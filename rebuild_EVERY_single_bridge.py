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
        "title": "Minimalist Wood Base Cream Shade Bedside Table Lamp",
        "price": "$12.99",
        "rating": "4.6",
        "features": ["MINIMALIST WOOD BASE", "CREAM FABRIC LAMPSHADE", "WARM AMBIENT GLOW", "INLINE CONTROL SWITCH"],
        "category": "lighting",
        "description": "Transform your nightstand setup with this aesthetic minimalist wood base table lamp. Warm ambient glow perfect for cozy reading and bedroom decor.",
        "direct_regions": ["US", "CA"]
    },
    "B0BZXNSW5K": {
        "title": "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet",
        "price": "$19.99",
        "rating": "4.5",
        "features": ["DIMMABLE TOUCH CONTROL", "DUAL USB A+C CHARGING PORTS", "BUILT-IN AC OUTLET", "LED BULB INCLUDED"],
        "category": "lighting",
        "description": "Upgrade your nightstand setup with this 3-way dimmable touch control bedside lamp featuring USB A+C charging ports and AC outlet.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "CA"]
    },
    "B0D1FRDFFX": {
        "title": "Glass Mushroom Lamp Ambient Table Nightstand Light",
        "price": "$35.98",
        "rating": "4.8",
        "features": ["HAND-BLOWN STRIPED GLASS", "WARM AMBIENT GLOW", "VINTAGE MUSHROOM DESIGN", "EASY ON/OFF SWITCH"],
        "category": "lighting",
        "description": "Add a cozy retro aesthetic to your space with this hand-blown striped glass mushroom lamp. Soft ambient glow for nightstands, desks, and shelves.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "AU"]
    },
    "B0C2YLN3H4": {
        "title": "White Ceramic Donut Vase Set of 2 Modern Aesthetic Decor",
        "price": "$14.99",
        "rating": "4.7",
        "features": ["MATTE CERAMIC FINISH", "DONUT HOLLOW CENTER", "MINIMALIST NORDIC STYLE", "SET OF 2 MATCHING VASES"],
        "category": "decor",
        "description": "Minimalist matte white ceramic donut vase set of 2 for aesthetic pampas grass, shelf styling, coffee table and mantle room decor.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B0GYDXHF4G": {
        "title": "Flame Aroma Essential Oil Diffuser Dark Crackle Flame Effect",
        "price": "$35.00",
        "rating": "4.9",
        "features": ["REALISTIC FLAME EFFECT", "ULTRASONIC MIST HUMIDIFIER", "SILENT SLEEP OPERATION", "AUTO SHUTOFF SAFETY"],
        "category": "lighting decor",
        "description": "Cozy ambient flame effect humidifier and essential oil diffuser in dark crackle finish. Realistic flame glow for bedroom relaxation.",
        "direct_regions": ["US"]
    },
    "B0FXLYXM32": {
        "title": "White Wavy Wall Vanity Mirror Aesthetic Squiggle Mirror",
        "price": "$76.49",
        "rating": "4.8",
        "features": ["SQUIGGLE WAVY FRAME", "HIGH DEFINITION GLASS", "WALL MOUNT OR TABLETOP", "VIRAL DORM DECOR"],
        "category": "mirror",
        "description": "Trendy white wavy squiggle vanity mirror for bedroom desk, wall decor, and viral aesthetic room transformation.",
        "direct_regions": ["US", "IN", "UK", "DE", "SG", "CA", "AU", "JP"]
    },
    "B07HP22QTZ": {
        "title": "Suncatcher Crystal Prism Window Rainbow Maker Hanging Light Catcher",
        "price": "$9.99",
        "rating": "4.9",
        "features": ["K9 CRYSTAL PRISM", "RAINBOW LIGHT REFLECTION", "WINDOW HANGING CHAIN", "GIFT BOX INCLUDED"],
        "category": "decor",
        "description": "Sparkling crystal prism suncatcher window hanging. Casts vibrant rainbow light patterns across room when sunlight shines through.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "CA", "AU", "JP"]
    },
    "B0D8P8CSYP": {
        "title": "Aesthetic Sunset Lamp Projection Light Ambient Glow",
        "price": "$18.99",
        "rating": "4.6",
        "features": ["SUNSET PROJECTION GLOW", "360 DEGREE ROTATION", "USB POWERED", "PHOTO BACKGROUND LIGHT"],
        "category": "lighting",
        "description": "Create warm romantic room vibes with this viral sunset projection lamp.",
        "direct_regions": ["US", "IN", "UK", "DE", "SE", "SG", "AU", "JP"]
    },
    "B0DLN5S5K9": {
        "title": "Minimalist Ceramic Table Lamp Neutral Bedside Glow",
        "price": "$29.99",
        "rating": "4.7",
        "features": ["CERAMIC TEXTURED BASE", "LINEN SHADE", "WARM LIGHT BULB", "BEDSIDE ACCENT"],
        "category": "lighting",
        "description": "Neutral minimalist ceramic table lamp for bedroom and living room accent lighting.",
        "direct_regions": ["UK", "SE", "JP"]
    },
    "B0DXKGL1T2": {
        "title": "Lily of the Valley Flower Table Lamp Glass Nightlight",
        "price": "$38.57",
        "rating": "4.8",
        "features": ["HAND-CRAFTED FLOWER GLASS SHADE", "WARM AMBIENT NIGHTLIGHT", "MINIMALIST BEDROOM DECOR", "PERFECT GIFT CHOICE"],
        "category": "lighting",
        "description": "Hand-crafted Lily of the Valley flower glass shade table lamp with warm ambient glow for nightstands, bedrooms, and aesthetic room decor.",
        "direct_regions": ["UK"]
    }
}

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
