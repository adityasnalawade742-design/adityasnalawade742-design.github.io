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

def rebuild_all_price_badges():
    print("==================================================")
    print("🎨 REBUILDING GRAPHIC PRICE BADGES ACCORDING TO SYNCED PRICES")
    print("==================================================")

    for asin, meta in registry.items():
        raw_path = repo_dir / "raw_images" / f"raw_{asin}.jpg"
        if not raw_path.exists():
            if (repo_dir / f"raw_{asin}_console.jpg").exists():
                raw_path = repo_dir / f"raw_{asin}_console.jpg"
            elif (repo_dir / f"focus_product_{asin}_hook.jpg").exists():
                raw_path = repo_dir / f"focus_product_{asin}_hook.jpg"
            else:
                print(f" ⚠️ Skipping [{asin}]: raw image not found.")
                continue

        usd_price = meta.get("current_price") or meta.get("regional_prices", {}).get("US", "$19.99")
        if "INR" in str(usd_price):
            usd_price = "$19.99"

        output_path = repo_dir / f"focus_product_{asin}_hook.jpg"
        title = meta.get("title", f"Product {asin}")
        badge = meta.get("badge", "✨ VIRAL ROOM FIND")

        print(f"\n🖼️ Re-rendering graphic overlay for [{asin}]...")
        print(f"   • Raw Image:  {raw_path.name}")
        print(f"   • Synced Price: {usd_price}")
        print(f"   • Output Pin: {output_path.name}")

        render_html_overlay(
            image_path=str(raw_path),
            headline=title,
            subtitle="",
            badge_text=badge,
            price_str=usd_price,
            features=meta.get("features"),
            output_path=str(output_path),
            theme="bottom_glass_card"
        )

    print("\n==================================================")
    print(" 🎉 ALL GRAPHIC PRICE BADGES REBUILT ACCORDING TO SYNCED PRICES!")
    print("==================================================")

if __name__ == "__main__":
    rebuild_all_price_badges()
