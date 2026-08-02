"""
Master Full-System End-to-End Diagnostic Tool
Tests Configuration, Database/Registry, SerpAPI Multi-Key Rotation, Scraper/Extractor,
Bridge Generator, Server Process, and Web API Endpoints.
"""
import os
import sys
import json
import time
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

print("=" * 80)
print("MASTER FULL-SYSTEM END-TO-END DIAGNOSTIC RUNNER")
print("=" * 80)

passed = 0
failed = 0

def check(name, fn):
    global passed, failed
    print(f"\n[CHECK] {name}...")
    try:
        res = fn()
        if res is not False:
            print(f"        ✅ PASSED: {res if isinstance(res, str) else 'OK'}")
            passed += 1
        else:
            print(f"        ❌ FAILED")
            failed += 1
    except Exception as e:
        print(f"        ❌ EXCEPTION: {e}")
        failed += 1

# 1. Environment & Config Verification
def check_config():
    from config import SERPAPI_KEYS, AMAZON_ASSOCIATE_TAG, BASE_BRIDGE_URL, NICHE
    if not SERPAPI_KEYS:
        return False
    return f"{len(SERPAPI_KEYS)} SerpAPI keys configured | Tag: {AMAZON_ASSOCIATE_TAG} | Niche: '{NICHE}'"

check("Config & Environment (.env)", check_config)

# 2. Registry & Database Check
def check_registry():
    from modules.product_registry import init_registry_db, get_blocked_asins
    init_registry_db()
    blocked = get_blocked_asins()
    return f"Registry SQLite initialized | {len(blocked)} blocked/rejected ASINs"

check("Product Registry & Excel Sync", check_registry)

# 3. SQLite Image Cache Check
def check_sqlite_cache():
    from modules.image_cache_db import init_image_db, get_cached_image
    init_image_db()
    img = get_cached_image("B0CLV5M9TF")
    return f"SQLite DB initialized | Test lookup for B0CLV5M9TF: {img[:45] if img else 'None'}"

check("SQLite Image Cache DB", check_sqlite_cache)

# 4. Product Search & SerpAPI Multi-Key Rotation
def check_finder():
    from modules.amazon_finder import fetch_amazon_products
    items = fetch_amazon_products(query="cozy mushroom table lamp", num_results=2)
    if not items:
        return False
    return f"Found {len(items)} products | Item 1: {items[0]['id']} ({items[0]['title'][:35]})"

check("Amazon Product Finder Engine", check_finder)

# 5. Scraper & Fast Photo Extractor
def check_extractor():
    from modules.amazon_extractor import fetch_all_product_images
    imgs = fetch_all_product_images("B0CLV5M9TF")
    if not imgs:
        return False
    return f"Extracted {len(imgs)} gallery images | Hero: {imgs[0][:50]}"

check("Amazon Scraper & Photo Extractor", check_extractor)

# 6. HTML Overlay & Bridge Creator
def check_bridge_creator():
    from modules.bridge_creator import generate_bridge_page
    product_data = {
        "id": "TESTASIN12",
        "title": "Aesthetic Cozy Mushroom Lamp Test",
        "price": "$24.99",
        "rating": "4.8",
        "reviews_count": 500,
        "affiliate_url": "https://www.amazon.com/dp/TESTASIN12?tag=smartdeal0358-21",
        "original_image_url": "https://m.media-amazon.com/images/I/61bYfBM7KRL._AC_SL1500_.jpg",
        "features": ["4.8 Star Rating", "500 Reviews", "Soft Ambient Glow"]
    }
    seo_data = {
        "pin_title": "Aesthetic Cozy Mushroom Lamp Test",
        "description": "Discover cozy room decor lamp options.",
        "hashtags": "#roomdecor #homedecor"
    }
    bridge_path = generate_bridge_page(product_data, seo_data, "TESTASIN12")
    if not bridge_path or not Path(bridge_path).exists():
        return False
    return f"Generated Bridge HTML -> {Path(bridge_path).name}"

check("Bridge Creator Engine", check_bridge_creator)

# 7. Live Server & Endpoint Health
def check_server():
    r = requests.get("http://localhost:5000/api/homepage_products", timeout=5)
    if r.status_code == 200:
        data = r.json()
        return f"Server running on port 5000 | {data.get('count', 0)} active homepage items"
    return False

check("Web Console Server (http://localhost:5000)", check_server)

print("\n" + "=" * 80)
print(f"MASTER DIAGNOSTIC RESULT: Passed {passed} / {passed+failed} core system checks")
print("=" * 80)
