import os
import sys
import re
import io
import json
import time
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup

# Ensure UTF-8 stdout
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = BASE_DIR / "product_price_registry.json"
RAW_IMAGES_DIR = BASE_DIR / "raw_images"
RAW_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Imports from existing modules
from modules.html_overlay_engine import render_html_overlay
from modules.amazon_extractor import get_product_details_and_photos

from modules.affiliate_manager import build_affiliate_url

# Master Active Product Registry Seed
DEFAULT_REGISTRY = {
    "B0GYDXHF4G": {
        "title": "Flame Aroma Essential Oil Diffuser Dark Crackle",
        "url": build_affiliate_url("B0GYDXHF4G"),
        "current_price": "$35.00",
        "headline": "Flame Aroma Essential Oil Diffuser",
        "subtitle": "REALISTIC FLAME ATMOSPHERE",
        "badge": "✨ VIRAL ROOM FIND",
        "features": ["VOLCANO FLAME MIST", "WARM AMBER GLOW", "AUTO SHUT OFF", "ESSENTIAL OIL READY"],
        "raw_image": "raw_images/raw_B0GYDXHF4G.jpg",
        "hook_image": "focus_product_B0GYDXHF4G_hook.jpg",
        "bridge_page": "bridge_B0GYDXHF4G.html"
    },
    "B0FXLYXM32": {
        "title": "Pocetry 22\"x30\" White Wavy Wall Mirror for Vanity",
        "url": build_affiliate_url("B0FXLYXM32"),
        "current_price": "$76.49",
        "headline": "White Wavy Wall Vanity Mirror",
        "subtitle": "ELEVATE YOUR VANITY SPACE",
        "badge": "✨ VANITY GOALS",
        "features": ["CREAM WAVY FRAME", "HIGH CLARITY GLASS", "CUTE SQUIGGLE DESIGN", "WALL & VANITY MOUNT"],
        "raw_image": "raw_images/raw_B0FXLYXM32.jpg",
        "hook_image": "focus_product_B0FXLYXM32_hook.jpg",
        "bridge_page": "bridge_B0FXLYXM32.html"
    },
    "B0C2YLN3H4": {
        "title": "White Ceramic Donut Vase Set of 2",
        "url": build_affiliate_url("B0C2YLN3H4"),
        "current_price": "$13.49",
        "headline": "White Ceramic Donut Vase Set",
        "subtitle": "MODERN MINIMALIST VASE",
        "badge": "🌿 BOHO DECOR PICK",
        "features": ["SET OF 2 VASES", "MATTE CERAMIC", "HOLLOW DONUT DESIGN", "PAMPAS GRASS READY"],
        "raw_image": "raw_images/raw_B0C2YLN3H4.jpg",
        "hook_image": "focus_product_B0C2YLN3H4_exact2vases_hook.jpg",
        "bridge_page": "bridge_B0C2YLN3H4.html"
    },
    "B07HP22QTZ": {
        "title": "Suncatcher Crystal Ball Prism Window Rainbow Maker",
        "url": build_affiliate_url("B07HP22QTZ"),
        "current_price": "$9.99",
        "headline": "Crystal Prism Window Suncatcher",
        "subtitle": "RAINBOW SPECTRUM MAKER",
        "badge": "🌈 SUNLIGHT MAGIC",
        "features": ["K9 OPTICAL CRYSTAL", "RAINBOW MAKER", "EASY WINDOW HANGING", "DURABLE CHAIN"],
        "raw_image": "raw_images/raw_B07HP22QTZ.jpg",
        "hook_image": "focus_product_B07HP22QTZ_hook.jpg",
        "bridge_page": "bridge_B07HP22QTZ.html"
    },
    "B0BZXNSW5K": {
        "title": "Fenmzee Bedside Table Touch Lamp",
        "url": build_affiliate_url("B0BZXNSW5K"),
        "current_price": "$19.99",
        "headline": "Dimmable Touch Nightstand Lamp",
        "subtitle": "WARM BEDTIME GLOW",
        "badge": "🕯️ BEDSIDE FAVORITE",
        "features": ["TOUCH SENSOR CONTROL", "3 BRIGHTNESS LEVELS", "WARM AMBER LIGHT", "USB CHARGING PORT"],
        "raw_image": "raw_images/raw_B0BZXNSW5K.jpg",
        "hook_image": "focus_product_B0BZXNSW5K_hook.jpg",
        "bridge_page": "bridge_B0BZXNSW5K.html"
    },
    "B0DXKGL1T2": {
        "title": "Lily of the Valley Flower Table Lamp",
        "url": build_affiliate_url("B0DXKGL1T2"),
        "current_price": "$36.38",
        "headline": "Lily of the Valley Flower Lamp",
        "subtitle": "VINTAGE FLORAL GLOW",
        "badge": "✨ VIRAL ROOM FIND",
        "features": ["3 COLOR MODES", "WARM BEDSIDE GLOW", "VINTAGE FLORAL DESIGN", "PERFECT GIFT IDEA"],
        "raw_image": "generated image.jpg",
        "hook_image": "focus_product_B0DXKGL1T2_hook.jpg",
        "bridge_page": "bridge_B0DXKGL1T2.html"
    },
    "B0D1FRDFFX": {
        "title": "Dawnwake Mushroom Touch Table Lamp",
        "url": build_affiliate_url("B0D1FRDFFX"),
        "current_price": "$39.98",
        "headline": "Glass Mushroom Touch Accent Lamp",
        "subtitle": "COZY AMBIENT GLOW",
        "badge": "🍄 VIRAL MUSHROOM LAMP",
        "features": ["BLOWN GLASS DOME", "TOUCH DIMMABLE", "WARM NIGHT LIGHT", "MINIMALIST DESIGN"],
        "raw_image": "raw_images/raw_B0D1FRDFFX.jpg",
        "hook_image": "focus_product_B0D1FRDFFX_hook.jpg",
        "bridge_page": "bridge_B0D1FRDFFX.html"
    },
    "B0D8P8CSYP": {
        "title": "Cute Bird Dimmable Touch Night Lamp",
        "url": build_affiliate_url("B0D8P8CSYP"),
        "current_price": "$20.56",
        "headline": "Cute Bird Dimmable Touch Lamp",
        "subtitle": "SOFT NIGHTSTAND LIGHT",
        "badge": "🐦 CUTE BEDSIDE PICK",
        "features": ["RECHARGEABLE BATTERY", "TOUCH DIMMING", "WOODGRAIN FINISH", "PORTABLE NIGHT LIGHT"],
        "raw_image": "raw_images/raw_B0D8P8CSYP.jpg",
        "hook_image": "focus_product_B0D8P8CSYP_hook.jpg",
        "bridge_page": "bridge_B0D8P8CSYP.html"
    }
}

def load_registry() -> dict:
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Price Updater Critical] Error loading registry JSON: {e}")
            return {}
    save_registry(DEFAULT_REGISTRY)
    return DEFAULT_REGISTRY

def save_registry(registry_data: dict):
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry_data, f, indent=2)

def extract_live_amazon_price(amazon_url: str) -> str:
    """
    Extracts the precise live price from Amazon URL using HTTP scraping + extractor fallback.
    Returns price string (e.g. '$36.38') or None if unparseable.
    """
    try:
        req = urllib.request.Request(amazon_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Priority 1: Target DOM .a-price .a-offscreen element
        offscreen = soup.select_one('.a-price .a-offscreen')
        if offscreen:
            txt = offscreen.text.strip()
            if "INR" not in txt and "₹" not in txt:
                m = re.search(r'(\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', txt)
                if m:
                    return m.group(1)

        # Priority 2: DOM whole + fraction
        whole = soup.find('span', {'class': 'a-price-whole'})
        fraction = soup.find('span', {'class': 'a-price-fraction'})
        symbol = soup.find('span', {'class': 'a-price-symbol'})
        if whole:
            sym = symbol.text.strip() if symbol else "$"
            wh = re.sub(r'[^\d]', '', whole.text)
            fr = fraction.text.strip() if fraction else "00"
            if wh.isdigit() and len(wh) <= 6:
                return f"{sym}{wh}.{fr}"
            
        # Priority 3: Regex fallback
        m = re.search(r'(\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', html)
        if m:
            return m.group(1)
    except Exception as e:
        print(f"[Price Scraper Warning] HTTP Direct error: {e}")

    # Fallback to amazon_extractor module
    try:
        prod = get_product_details_and_photos(amazon_url)
        if prod and prod.get("price"):
            p = prod["price"]
            if not p.startswith("$") and not p.startswith("£") and not p.startswith("€"):
                p = f"${p}"
            return p
    except Exception as e2:
        print(f"[Price Extractor Warning] Extractor fallback error: {e2}")

    return None

def update_landing_page_price(bridge_filename: str, old_price: str, new_price: str):
    """Precisely updates the price inside bridge html file."""
    filepath = BASE_DIR / bridge_filename
    if not filepath.exists():
        return
    content = filepath.read_text(encoding="utf-8")
    updated = re.sub(
        r'<div class="price">[^<]+</div>',
        f'<div class="price">{new_price}</div>',
        content
    )
    filepath.write_text(updated, encoding="utf-8")
    print(f"  └─ Updated Landing Page ({bridge_filename}): {new_price}")

def update_homepage_price(asin: str, new_price: str, timestamp: str):
    """Precisely updates the price tag in index.html for card-ASIN."""
    filepath = BASE_DIR / "index.html"
    if not filepath.exists():
        return
    content = filepath.read_text(encoding="utf-8")
    
    # Pattern targeting card-ASIN wrapper
    pattern = rf'(<div class="card-wrapper" id="card-{asin}">[\s\S]*?<div class="card-price-tag">)([^<]+)(</div>)'
    updated = re.sub(pattern, rf'\g<1>{new_price}\g<3>', content)
    
    filepath.write_text(updated, encoding="utf-8")
    print(f"  └─ Updated Homepage (index.html) card-{asin}: {new_price}")

def regenerate_clean_graphic_with_new_price(asin: str, item_data: dict, new_price: str, timestamp: str):
    """
    Re-renders Playwright graphic overlay using the clean raw image with NO text,
    stamping the new exact price into the price tag!
    """
    # Priority 1: Check flux_clean_images folder for clean AI Flux Dev image
    flux_clean_dir = BASE_DIR / "flux_clean_images"
    flux_candidates = [
        flux_clean_dir / f"clean_focus_product_{asin}.jpg",
        flux_clean_dir / f"clean_{asin}.jpg",
        flux_clean_dir / f"focus_product_{asin}.jpg",
        flux_clean_dir / f"focus_product_{asin}_ai.jpg",
        flux_clean_dir / f"flux_{asin}.jpg"
    ]
    
    raw_img = None
    for cand in flux_candidates:
        if cand.exists():
            raw_img = cand
            break
            
    if not raw_img or not raw_img.exists():
        raw_img = BASE_DIR / item_data["raw_image"]
    
    # Fallback to generated image.jpg or current hook image if raw image file missing
    if not raw_img.exists():
        if (BASE_DIR / "generated image.jpg").exists():
            raw_img = BASE_DIR / "generated image.jpg"
        elif (BASE_DIR / item_data["hook_image"]).exists():
            raw_img = BASE_DIR / item_data["hook_image"]
        else:
            print(f"  ⚠️ Warning: No raw image found for {asin}. Skipping graphic re-render.")
            return

    output_path = BASE_DIR / item_data["hook_image"]
    
    print(f"  └─ Re-rendering graphic overlay from clean raw image: {raw_img.name}")
    render_html_overlay(
        image_path=str(raw_img),
        headline=item_data["headline"],
        subtitle=item_data.get("subtitle", "ELEGANCE THAT SHINES"),
        badge_text=item_data.get("badge", "✨ VIRAL ROOM FIND"),
        price_str=new_price,
        features=item_data.get("features"),
        output_path=str(output_path),
        theme="bottom_glass_card"
    )
    
    # Copy to output/images directory
    out_img = BASE_DIR / "output" / "images" / item_data["hook_image"]
    out_img.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(output_path, out_img)

def run_daily_price_update_check(auto_git_push: bool = True):
    print("=" * 70)
    print(f"🔄 === DAILY AUTOMATED PRICE SYNCHRONIZER ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    print("=" * 70)
    
    registry = load_registry()
    updated_asins = []
    timestamp = str(int(time.time()))

    for asin, data in registry.items():
        title = data.get("title", asin)
        old_price = data.get("current_price", "$0.00")
        url = data.get("url", "")
        if not url:
            print(f"\n🔍 Skipping ASIN: {asin} (No URL configured)")
            continue
        
        print(f"\n🔍 Checking ASIN: {asin} - '{title[:45]}...'")
        print(f"   Registered Price: {old_price}")
        
        extracted_price = extract_live_amazon_price(url)
        if not extracted_price:
            print(f"   ⚠️ Could not extract live price for {asin}. Keeping registered price: {old_price}")
            continue
            
        print(f"   Extracted Amazon Price: {extracted_price}")
        
        # Check if price has changed
        if extracted_price != old_price:
            print(f"   🚨 PRICE CHANGE DETECTED! {old_price} ➔ {extracted_price}")
            
            # 1. Re-render graphic overlay using clean raw image
            regenerate_clean_graphic_with_new_price(asin, data, extracted_price, timestamp)
            
            # 2. Update Landing Page
            update_landing_page_price(data.get("bridge_page", f"bridge_{asin}.html"), old_price, extracted_price)
            
            # 3. Update Homepage
            update_homepage_price(asin, extracted_price, timestamp)
            
            # 4. Update Registry
            data["current_price"] = extracted_price
            data["last_updated"] = datetime.now().isoformat()
            updated_asins.append((asin, old_price, extracted_price))
        else:
            print("   ✅ Price is 100% synchronized and up to date.")
            
    # Save updated registry
    save_registry(registry)

    # Trigger full master sequential regional price sync suite
    print("\n🌐 Executing Master Multi-Region Regional Price Sync Suite...")
    import subprocess
    master_script = BASE_DIR / "sync_all_regional_prices_master.py"
    subprocess.run([sys.executable, str(master_script)], cwd=str(BASE_DIR))

if __name__ == "__main__":
    run_daily_price_update_check()
