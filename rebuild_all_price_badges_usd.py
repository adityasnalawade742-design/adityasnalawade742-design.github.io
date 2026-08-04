import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path(__file__).resolve().parent  # FIX: dynamic path, not hardcoded
sys.path.append(str(repo_dir))

from modules.html_overlay_engine import render_html_overlay

registry_file = repo_dir / "product_price_registry.json"
with open(registry_file, "r", encoding="utf-8") as f:
    registry = json.load(f)

# Master catalog metadata mapping for graphic pin overlays
items_to_rebuild = [
    {
        "asin": "B0DZD1X83N",
        "title": "Minimalist Wood Base Table Lamp",
        "raw": "raw_images/raw_B0DZD1X83N.jpg",
        "hook": "focus_product_B0DZD1X83N_hook.jpg",
        "badge": "✨ VIRAL ROOM FIND"
    },
    {
        "asin": "B0BZXNSW5K",
        "title": "Touch Control Dimmable Bedside Lamp",
        "raw": "raw_images/raw_B0BZXNSW5K.jpg",
        "hook": "focus_product_B0BZXNSW5K_hook.jpg",
        "badge": "🕯️ BEDSIDE FAVORITE"
    },
    {
        "asin": "B0D1FRDFFX",
        "title": "Glass Mushroom Ambient Lamp",
        "raw": "raw_images/raw_B0D1FRDFFX.jpg",
        "hook": "focus_product_B0D1FRDFFX_hook.jpg",
        "badge": "🍄 VIRAL MUSHROOM LAMP"
    },
    {
        "asin": "B0C2YLN3H4",
        "title": "White Ceramic Donut Vase Set",
        "raw": "raw_images/raw_B0C2YLN3H4.jpg",
        "hook": "focus_product_B0C2YLN3H4_hook.jpg",
        "badge": "🌿 BOHO DECOR PICK"
    },
    {
        "asin": "B0GYDXHF4G",
        "title": "Flame Aroma Essential Oil Diffuser",
        "raw": "raw_images/raw_B0GYDXHF4G.jpg",
        "hook": "focus_product_B0GYDXHF4G_hook.jpg",
        "badge": "✨ VIRAL ROOM FIND"
    },
    {
        "asin": "B0FXLYXM32",
        "title": "White Wavy Wall Vanity Mirror",
        "raw": "raw_images/raw_B0FXLYXM32.jpg",
        "hook": "focus_product_B0FXLYXM32_hook.jpg",
        "badge": "✨ VANITY GOALS"
    },
    {
        "asin": "B07HP22QTZ",
        "title": "Crystal Prism Window Suncatcher",
        "raw": "raw_images/raw_B07HP22QTZ.jpg",
        "hook": "focus_product_B07HP22QTZ_hook.jpg",
        "badge": "🌈 SUNLIGHT MAGIC"
    },
    {
        "asin": "B0D8P8CSYP",
        "title": "Cute Bird Dimmable Touch Lamp",
        "raw": "raw_images/raw_B0D8P8CSYP.jpg",
        "hook": "focus_product_B0D8P8CSYP_hook.jpg",
        "badge": "🐦 CUTE BEDSIDE PICK"
    },
    {
        "asin": "B0DXKGL1T2",
        "title": "Lily of Valley Flower Lamp",
        "raw": "raw_images/raw_B0DXKGL1T2.jpg",
        "hook": "focus_product_B0DXKGL1T2_hook.jpg",
        "badge": "✨ VIRAL ROOM FIND"
    },
    {
        "asin": "B0FGJ1S73D",
        "title": "Ceramic Mushroom Bedside Lamp",
        "raw": "raw_images/raw_B0FGJ1S73D.jpg",
        "hook": "focus_product_B0FGJ1S73D_hook.jpg",
        "badge": "🍄 MUSHROOM LAMP FIND"
    },
    {
        "asin": "B0CJC549C6",
        "title": "Matte Black Thinker Statue Set",
        "raw": "raw_images/raw_B0CJC549C6.jpg",
        "hook": "focus_product_B0CJC549C6_hook.jpg",
        "badge": "✨ VIRAL DECOR FIND"
    },
    {
        "asin": "B0CJ4Q4PZQ",
        "title": "Pink Striped Glass Mushroom Lamp",
        "raw": "raw_images/raw_B0CJ4Q4PZQ.jpg",
        "hook": "focus_product_B0CJ4Q4PZQ_hook.jpg",
        "badge": "🍄 COZY BEDSIDE GLOW"
    }
]

def rebuild_all_price_badges():
    print("==================================================")
    print("🎨 REBUILDING GRAPHIC PRICE BADGES ACCORDING TO SYNCED PRICES")
    print("==================================================")

    for item in items_to_rebuild:
        asin = item["asin"]
        raw_path = repo_dir / item["raw"]
        if not raw_path.exists():
            print(f" ⚠️ Skipping [{asin}]: raw image {raw_path} not found.")
            continue

        usd_price = registry.get(asin, {}).get("current_price") or registry.get(asin, {}).get("regional_prices", {}).get("US", "$19.99")
        output_path = repo_dir / item["hook"]

        print(f"\n🖼️ Re-rendering graphic overlay for [{asin}]...")
        print(f"   • Raw Image:  {raw_path.name}")
        print(f"   • Synced Price: {usd_price}")
        print(f"   • Output Pin: {output_path.name}")

        render_html_overlay(
            image_path=str(raw_path),
            headline=item["title"],
            subtitle="",
            badge_text=item["badge"],
            price_str=usd_price,
            output_path=str(output_path),
            theme="bottom_glass_card"
        )

    print("\n==================================================")
    print(" 🎉 ALL GRAPHIC PRICE BADGES REBUILT ACCORDING TO SYNCED PRICES!")
    print("==================================================")

if __name__ == "__main__":
    rebuild_all_price_badges()
