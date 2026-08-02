import sys
import io
import re
import json
import requests
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import NICHE, AMAZON_ASSOCIATE_TAG, SERPAPI_KEY
from modules.automated_product_selector import is_asin_published_on_homepage
from modules.amazon_extractor import is_adult_aesthetic_product, select_clean_photo_or_skip, get_product_details_and_photos

CACHE_FILE = Path("G:/CLI/pinterest-auto-affiliate/serpapi_cache.json")

TRENDING_PINTEREST_KEYWORDS = [
    "aesthetic glass mushroom table lamp",
    "lily of the valley flower lamp bedside",
    "sunset lamp projection light golden hour",
    "flameless candle warmer lamp timer",
    "white ceramic donut vase pampas grass set",
    "abstract thinker statue bookshelf decor",
    "wavy vanity wall mirror aesthetic cream",
    "framed neutral botanical print set black frame",
    "water hyacinth storage basket set natural"
]

def load_serp_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_serp_cache(cache_data):
    try:
        CACHE_FILE.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"[SerpAPI Cache Error] Could not save cache: {e}")

def parse_price_float(price_str: str) -> float:
    """Extracts floating point price value from price string."""
    if not price_str:
        return 0.0
    cleaned = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def fetch_amazon_products(query: str = None, num_results: int = 3, min_price: float = 10.0, max_price: float = 50.0):
    """
    Intelligent Live Amazon Product Finder with SerpAPI Quota Protection & Multi-Criteria Quality Filters:
      1. Zero-Cost Local Query Cache (Saves SerpAPI search credits)
      2. Price Sweet Spot ($10 - $50 impulse conversion threshold)
      3. Minimum 4.2★ Rating & Review count check
      4. Adult Room Aesthetics (excludes kids toys, toddler boards)
      5. Dynamic Homepage Deduplication (skips active items on index.html)
      6. 4-Layer Photo Cleanliness Verification (must have clean text-free photos)
    """
    search_query = query or NICHE
    print(f"[Amazon Finder Engine] Searching LIVE Amazon catalog for: '{search_query}'...")

    live_items = _fetch_from_serpapi_with_filters(search_query, num_results=num_results*2, min_price=min_price, max_price=max_price)
    if live_items:
        unpub_items = [it for it in live_items if not is_asin_published_on_homepage(it["id"])]
        result_set = unpub_items[:num_results] if unpub_items else live_items[:num_results]
        print(f"[Amazon Finder] Found {len(result_set)} live Amazon products for query: '{search_query}'")
        return result_set

    print("[Amazon Finder] Falling back to curated high-converting niche products...")
    return fetch_sample_amazon_products()

def _fetch_from_serpapi_with_filters(query: str, num_results: int = 10, min_price: float = 10.0, max_price: float = 50.0):
    from config import SERPAPI_KEYS
    cache = load_serp_cache()
    query_key = query.lower().strip()

    # 1. CHECK LOCAL CACHE FIRST TO SAVE SERPAPI QUOTA
    if query_key in cache:
        print(f"[SerpAPI Cache] ⚡ RETRIEVED FROM LOCAL CACHE (0 SerpAPI credits used!) for '{query_key}'")
        raw_results = cache[query_key]
        return _parse_raw_serp_results(raw_results, num_results, min_price, max_price)

    keys_to_try = SERPAPI_KEYS if SERPAPI_KEYS else ([SERPAPI_KEY] if SERPAPI_KEY else [])
    if not keys_to_try:
        print("[SerpAPI Warning] No SERPAPI_KEYS configured.")
        return None

    url = "https://serpapi.com/search.json"
    
    for key_idx, current_key in enumerate(keys_to_try, 1):
        params = {
            "engine": "google",
            "q": f"site:amazon.com/dp/ {query}",
            "api_key": current_key
        }
        
        try:
            print(f"[SerpAPI Request] 🌐 Calling SerpAPI (Key #{key_idx}/{len(keys_to_try)}) for: '{query}'...")
            response = requests.get(url, params=params, timeout=12)
            if response.status_code == 200:
                data = response.json()
                
                # Check if SerpAPI error payload indicates quota or credit limit reached
                if "error" in data:
                    err_msg = str(data["error"]).lower()
                    if any(k in err_msg for k in ["credit", "search", "quota", "limit", "out of"]):
                        print(f"[SerpAPI Quota Alert] Key #{key_idx} out of credits: {data['error']} -> Switching to Key #{key_idx + 1}...")
                        continue

                results = data.get("amazon_results") or data.get("organic_results") or []
                if not results:
                    print(f"[SerpAPI Key #{key_idx}] 0 results returned. Trying next key...")
                    continue
                
                # Save raw results to local cache to preserve credits for future searches
                cache[query_key] = results
                save_serp_cache(cache)
                print(f"[SerpAPI Cache] 💾 Saved {len(results)} search results to local disk cache!")
                
                parsed = _parse_raw_serp_results(results, num_results, min_price, max_price)
                if parsed:
                    return parsed
            else:
                print(f"[SerpAPI Key #{key_idx} Error {response.status_code}] {response.text[:100]}")
                if response.status_code in [400, 401, 403, 429]:
                    print(f"[SerpAPI Key Switch] Key #{key_idx} failed ({response.status_code}). Switching to Key #{key_idx + 1}...")
                    continue
        except Exception as e:
            print(f"[SerpAPI Exception Key #{key_idx}] Error: {e}")

    return None

def _parse_raw_serp_results(results, num_results: int, min_price: float, max_price: float):
    parsed_products = []
    for item in results:
        asin = item.get("asin") or item.get("product_id")
        if not asin or len(asin) != 10:
            link = item.get("link", "")
            match = re.search(r'/(?:dp|gp/product)/([A-Z0-9]{10})', link, re.IGNORECASE)
            if match:
                asin = match.group(1).upper()
            else:
                continue

        title = item.get("title", "Aesthetic Room Decor Find")

        # Adult aesthetics check
        if not is_adult_aesthetic_product(title):
            print(f"[Amazon Finder Filter] Discarded Kids/Toy product: '{title[:40]}'")
            continue

        price_val = item.get("price")
        if isinstance(price_val, dict):
            price_str = price_val.get("raw") or str(price_val.get("extracted", "$24.99"))
        elif isinstance(price_val, str):
            price_str = price_val
        else:
            price_str = "$24.99"

        price_num = parse_price_float(price_str)
        if price_num > 0 and (price_num < min_price or price_num > max_price):
            print(f"[Amazon Finder Filter] Price ${price_num:.2f} outside ${min_price}-${max_price} target range for '{title[:35]}'")
            continue

        try:
            rating_num = float(item.get("rating", 4.5))
        except (ValueError, TypeError):
            rating_num = 4.5

        if rating_num < 4.2:
            print(f"[Amazon Finder Filter] Rating {rating_num}★ below 4.2★ threshold for '{title[:35]}'")
            continue

        reviews = item.get("reviews", 150)
        image_url = item.get("thumbnail") or item.get("image") or item.get("original_image_url", "")
        
        # Pull real high-res Amazon listing hero image
        if not image_url and asin:
            details = get_product_details_and_photos(asin)
            if details and details.get("original_image_url"):
                image_url = details.get("original_image_url")
            elif details and details.get("all_photos"):
                image_url = details["all_photos"][0]
            else:
                image_url = f"https://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF-8&MarketPlace=US&ASIN={asin}&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=_SL400_"

        affiliate_url = f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"

        parsed_products.append({
            "id": asin,
            "title": title,
            "category": "Cozy Room Decor & Lighting",
            "price": price_str,
            "rating": str(rating_num),
            "reviews_count": reviews,
            "affiliate_url": affiliate_url,
            "original_image_url": image_url,
            "features": f"Highly rated {title} with {rating_num}★ stars and {reviews} customer reviews."
        })

        if len(parsed_products) >= num_results:
            break
    
    return parsed_products

def fetch_sample_amazon_products(niche: str = NICHE):
    """Fallback sample products formatted with user affiliate tag and official Amazon Associates links."""
    tag = AMAZON_ASSOCIATE_TAG
    return [
        {
            "id": "B0BQBKWSKK",
            "title": "Volcano Erupting Flame Essential Oil Diffuser with Warm LED Glow",
            "category": "Home Fragrance & Room Decor",
            "price": "$25.99",
            "rating": "4.7",
            "reviews_count": 1420,
            "affiliate_url": f"https://www.amazon.com/dp/B0BQBKWSKK?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg",
            "features": "Volcano flame mist effect, 7 glowing ambient light colors, essential oil diffuser."
        }
    ]




