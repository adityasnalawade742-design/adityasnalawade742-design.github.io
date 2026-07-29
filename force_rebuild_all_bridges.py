import sys
import subprocess
from pathlib import Path

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from modules.bridge_creator import generate_bridge_page

products = [
    {
        "asin": "B0DZD1X83N",
        "prod": {
            "title": "Minimalist Wood Base Cream Shade Bedside Table Lamp",
            "price": "$12.99",
            "rating": "4.6",
            "features": [
                "MINIMALIST WOOD BASE",
                "CREAM FABRIC LAMPSHADE",
                "WARM AMBIENT GLOW",
                "INLINE CONTROL SWITCH"
            ],
            "category": "Bedside & Nightstand Ambient Decor"
        },
        "seo": {
            "pin_title": "Minimalist Wood Base Bedside Table Lamp for Bedroom Decor",
            "image_hook": "Minimalist Wood Bedside Lamp",
            "subtitle_hook": "",
            "badge_hook": "VIRAL ROOM FIND",
            "description": "Transform your nightstand setup with this aesthetic minimalist wood base table lamp. Warm ambient glow perfect for cozy reading and bedroom decor."
        }
    },
    {
        "asin": "B0BZXNSW5K",
        "prod": {
            "title": "Bedside Table Lamp for Bedroom - Dimmable Touch, USB A+C, AC Outlet",
            "price": "$19.99",
            "rating": "4.5",
            "features": [
                "DIMMABLE TOUCH CONTROL",
                "DUAL USB A+C CHARGING PORTS",
                "BUILT-IN AC OUTLET",
                "LED BULB INCLUDED"
            ],
            "category": "Bedside & Nightstand Ambient Decor"
        },
        "seo": {
            "pin_title": "Bedside Table Touch Lamp with USB A+C Ports & AC Outlet",
            "image_hook": "Bedside Table Touch Lamp",
            "subtitle_hook": "",
            "badge_hook": "VIRAL ROOM FIND",
            "description": "Upgrade your nightstand setup with this 3-way dimmable touch control bedside lamp featuring USB A+C charging ports and AC outlet."
        }
    },
    {
        "asin": "B0D1FRDFFX",
        "prod": {
            "title": "Glass Mushroom Lamp Ambient Table Nightstand Light",
            "price": "$35.98",
            "rating": "4.8",
            "features": [
                "HAND-BLOWN STRIPED GLASS",
                "WARM AMBIENT GLOW",
                "VINTAGE MUSHROOM DESIGN",
                "EASY ON/OFF SWITCH"
            ],
            "category": "Bedside & Nightstand Ambient Decor"
        },
        "seo": {
            "pin_title": "Glass Mushroom Lamp Aesthetic Nightstand Light",
            "image_hook": "Glass Mushroom Lamp",
            "subtitle_hook": "",
            "badge_hook": "VIRAL ROOM FIND",
            "description": "Add a cozy retro aesthetic to your space with this hand-blown striped glass mushroom lamp. Soft ambient glow for nightstands, desks, and shelves."
        }
    }
]

print("[Rebuild Engine] Re-generating ALL 3 luxury landing pages with Multi-Region Geo-Redirector...")

for item in products:
    asin = item["asin"]
    print(f" -> Regenerating bridge_{asin}.html...")
    generate_bridge_page(item["prod"], item["seo"], asin)

# Git add, commit, push
try:
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", "force rebuild all 3 bridge landing pages with universal multi-region geo-redirector"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print(" ✅ All bridge pages committed and pushed live successfully!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")
