import json
import re
from pathlib import Path
from config import AMAZON_ASSOCIATE_TAG
from modules.affiliate_manager import build_affiliate_url

PROJECT_ROOT = Path(__file__).resolve().parent.parent  # C4 FIX: dynamic path
PROCESSED_FILE = PROJECT_ROOT / "processed_asins.json"
INDEX_FILE = PROJECT_ROOT / "index.html"
REGISTRY_FILE = PROJECT_ROOT / "product_price_registry.json"

# Curated High-Converting Home Decor Product Pipeline ($15-$45 Impulse Price, 4.4★+ Rating)
VIRAL_HOME_DECOR_QUEUE = [
    {
        "id": "B0BQBKWSKK",
        "url": build_affiliate_url("B0BQBKWSKK"),
        "niche": "Home Fragrance & Room Decor",
        "title": "Volcano Erupting Flame Essential Oil Diffuser with Warm LED Glow",
        "target_price": "$25.99"
    },
    {
        "id": "B0FRS84KT9",
        "url": build_affiliate_url("B0FRS84KT9"),
        "niche": "Nightstand & Desk Decor",
        "title": "Acrylic Illuminated Glowing LED Note Memo Board with Wood Base",
        "target_price": "$29.99"
    },
    {
        "id": "B08HJ2M49T",
        "url": build_affiliate_url("B08HJ2M49T"),
        "niche": "Sunlight Window Decor",
        "title": "Crystal Suncatcher Prism Window Hanging Rainbow Decor",
        "target_price": "$14.99"
    },
    {
        "id": "B0B8Z7X5M1",
        "url": build_affiliate_url("B0B8Z7X5M1"),
        "niche": "Bedroom & Vanity Mirror Decor",
        "title": "Minimalist Asymmetric Wavy Body Mirror for Vanity & Bedroom",
        "target_price": "$34.99"
    }
]

def get_active_homepage_asins() -> set:
    """Scans index.html and product_price_registry.json for currently active/published ASINs on the homepage."""
    active_asins = set()
    
    # 1. Check index.html for card-wrapper IDs and bridge hrefs
    if INDEX_FILE.exists():
        try:
            html = INDEX_FILE.read_text(encoding="utf-8")
            card_matches = re.findall(r'id="card-([A-Z0-9]{10})"', html)
            bridge_matches = re.findall(r'href="\./bridge_([A-Z0-9]{10})\.html"', html)
            active_asins.update(card_matches)
            active_asins.update(bridge_matches)
        except Exception as e:
            print(f"[Automated Selector Warning] Could not parse index.html: {e}")
            
    # 2. Check product_price_registry.json
    if REGISTRY_FILE.exists():
        try:
            with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
                reg = json.load(f)
                active_asins.update(reg.keys())
        except Exception:
            pass
            
    return active_asins

def get_processed_asins() -> list:
    """
    Loads list of ASINs that are currently considered published/processed.
    Combines processed_asins.json AND dynamic active index.html cards.
    If a product was deleted from index.html and removed from processed_asins.json, it will NOT be in this list.
    """
    processed_set = set()
    
    # Load from processed_asins.json
    if PROCESSED_FILE.exists():
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    processed_set.update([str(a).upper().strip() for a in data if a])
        except Exception:
            pass
            
    # Combine with currently active homepage ASINs
    homepage_asins = get_active_homepage_asins()
    processed_set.update([str(a).upper().strip() for a in homepage_asins if a])
    
    return sorted(list(processed_set))

def is_asin_published_on_homepage(asin: str) -> bool:
    """Returns True if the ASIN is currently published on index.html or in active registry."""
    if not asin:
        return False
    active = get_processed_asins()
    return asin.upper().strip() in active

def save_processed_asin(asin: str):
    """Saves a newly processed ASIN to processed_asins.json safely using atomic replacement."""
    if not asin:
        return
    asin_clean = asin.upper().strip()
    processed = set(get_processed_asins())
    processed.add(asin_clean)
    
    tmp_file = PROCESSED_FILE.parent / f"tmp_{PROCESSED_FILE.name}"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(sorted(list(processed)), f, indent=2)
    import os
    os.replace(tmp_file, PROCESSED_FILE)
    print(f"[Automated Selector] Saved ASIN {asin_clean} to processed history.")

def remove_processed_asin(asin: str):
    """Removes ASIN from processed_asins.json when deleted from the homepage."""
    if not asin:
        return
    asin_clean = asin.upper().strip()
    if PROCESSED_FILE.exists():
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                data = [str(a).upper().strip() for a in data]
                if asin_clean in data:
                    data.remove(asin_clean)
                    tmp_file = PROCESSED_FILE.parent / f"tmp_{PROCESSED_FILE.name}"
                    with open(tmp_file, "w", encoding="utf-8") as f:
                        json.dump(sorted(data), f, indent=2)
                    import os
                    os.replace(tmp_file, PROCESSED_FILE)
                    print(f"[Automated Selector] Removed ASIN {asin_clean} from processed history.")
        except Exception as e:
            print(f"[Automated Selector Error] Failed removing ASIN {asin_clean}: {e}")

def get_next_automated_product() -> dict:
    """
    Selects the next un-processed Home Decor product that is NOT currently published on the homepage.
    """
    processed = set(get_processed_asins())
    for item in VIRAL_HOME_DECOR_QUEUE:
        if item["id"] not in processed:
            print(f"[Automated Selector] Selected next Home Decor product: {item['id']} - '{item['title']}' ({item['niche']})")
            return item
    
    print("[Automated Selector] All queued Home Decor products are currently published on the homepage!")
    return None


def cleanup_unselected_raw_images() -> int:
    """
    Deletes any raw_images/raw_{ASIN}.jpg files that belong to unchosen search results 
    (ASINs not currently published on index.html or in product_price_registry.json).
    Returns the count of cleaned up files.
    """
    active_asins = get_active_homepage_asins()
    raw_dir = PROJECT_ROOT / "raw_images"
    if not raw_dir.exists():
        return 0

    cleaned_count = 0
    for file_path in raw_dir.glob("raw_*.jpg"):
        m = re.search(r"raw_([A-Z0-9]{10})\.jpg", file_path.name, re.IGNORECASE)
        if m:
            asin = m.group(1).upper()
            if asin not in active_asins:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    print(f"[Cleanup] Purged unchosen raw image: {file_path.name}")
                except Exception as e:
                    print(f"[Cleanup Error] Could not delete {file_path.name}: {e}")

    if cleaned_count > 0:
        print(f"[Cleanup] Successfully purged {cleaned_count} unchosen raw image files from disk!")
    return cleaned_count


