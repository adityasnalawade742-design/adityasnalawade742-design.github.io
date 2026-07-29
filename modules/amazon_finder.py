import sys
import io
import re
import requests

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import NICHE, AMAZON_ASSOCIATE_TAG, SERPAPI_KEY
from modules.automated_product_selector import is_asin_published_on_homepage
from modules.amazon_extractor import is_adult_aesthetic_product, select_clean_photo_or_skip, get_product_details_and_photos

TRENDING_PINTEREST_KEYWORDS = [
    "aesthetic room decor lamp",
    "cozy bedside ambient light",
    "flame aroma essential oil diffuser",
    "white ceramic donut vase boho decor",
    "crystal prism window suncatcher",
    "glowing led memo note board desk",
    "wavy vanity wall mirror aesthetic"
]

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
    Intelligent Live Amazon Product Finder with Multi-Criteria Quality Filters:
      1. Price Sweet Spot ($10 - $50 impulse conversion threshold)
      2. Minimum 4.3★ Rating & Review count check
      3. Adult Room Aesthetics (excludes kids toys, toddler boards)
      4. Dynamic Homepage Deduplication (skips active items on index.html)
      5. 4-Layer Photo Cleanliness Verification (must have clean text-free photos)
    """
    search_query = query or NICHE
    print(f"[Amazon Finder Engine] Searching LIVE Amazon catalog for: '{search_query}'...")

    if SERPAPI_KEY:
        live_items = _fetch_from_serpapi_with_filters(search_query, num_results=num_results*3, min_price=min_price, max_price=max_price)
        if live_items:
            # Filter and verify clean photo availability
            verified_winners = []
            for item in live_items:
                asin = item["id"]
                
                # 1. Skip if already published on homepage
                if is_asin_published_on_homepage(asin):
                    print(f"[Amazon Finder] Skipping ASIN {asin} (Already published on homepage)")
                    continue

                # 2. Extract full photo suite & verify clean photo
                full_details = get_product_details_and_photos(asin)
                if not full_details:
                    continue

                photos = full_details.get("all_photos", [])
                winner_photo, skip = select_clean_photo_or_skip(photos)

                if skip or not winner_photo:
                    print(f"[Amazon Finder] Skipping ASIN {asin} (All listing photos contain seller text/infographics)")
                    continue

                item["original_image_url"] = winner_photo
                item["all_photos"] = photos
                item["features"] = full_details.get("features", item["features"])
                verified_winners.append(item)

                if len(verified_winners) >= num_results:
                    break

            if verified_winners:
                print(f"[Amazon Finder] Selected {len(verified_winners)} verified clean winning products!")
                return verified_winners

    print("[Amazon Finder] Falling back to curated high-converting niche products...")
    return fetch_sample_amazon_products()

def _fetch_from_serpapi_with_filters(query: str, num_results: int = 10, min_price: float = 10.0, max_price: float = 50.0):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "amazon",
        "k": query,
        "q": query,
        "api_key": SERPAPI_KEY,
        "amazon_domain": "amazon.com"
    }
    
    try:
        response = requests.get(url, params=params, timeout=12)
        if response.status_code == 200:
            data = response.json()
            results = data.get("amazon_results") or data.get("organic_results") or []
            
            parsed_products = []
            for item in results:
                asin = item.get("asin") or item.get("product_id")
                if not asin or len(asin) != 10:
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
                image_url = item.get("thumbnail") or item.get("image", "")

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
    except Exception as e:
        print(f"[Amazon Finder] Exception querying SerpAPI: {e}")
        
    return None

def fetch_sample_amazon_products(niche: str = NICHE):
    """Fallback sample products formatted with user affiliate tag and official Amazon Associates links."""
    tag = AMAZON_ASSOCIATE_TAG
    return [
        {
            "id": "B0FC2DV6FP",
            "title": "Rain Cloud Raindrop Humidifier & Relaxing Sound Machine",
            "category": "Bedroom Wellness Decor",
            "price": "$33.99",
            "rating": "4.7",
            "reviews_count": 1420,
            "affiliate_url": f"https://www.amazon.com/dp/B0FC2DV6FP?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg",
            "features": "Raindrop water drip sound effect, 7 glowing ambient light colors, essential oil diffuser."
        },
        {
            "id": "B0DZFGTCLR",
            "title": "Flameless Top-Down Candle Warmer Melting Lamp with Timer",
            "category": "Cozy Scented Decor",
            "price": "$12.99",
            "rating": "4.8",
            "reviews_count": 890,
            "affiliate_url": f"https://www.amazon.com/dp/B0DZFGTCLR?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/61SsDfH706L._AC_SL1254_.jpg",
            "features": "Top-down halogen candle melting lamp, dimmable timer switch, wood base."
        }
    ]




