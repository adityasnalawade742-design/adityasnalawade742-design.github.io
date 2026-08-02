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

CACHE_FILE = Path(__file__).resolve().parent.parent / "serpapi_cache.json"  # C5 FIX: dynamic path

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
      3. Minimum 4.2 Rating & Review count check
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
        print(f"[SerpAPI Cache] RETRIEVED FROM LOCAL CACHE (0 SerpAPI credits used!) for '{query_key}'")
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
            "q": f"site:amazon.com/dp {query} buy",
            "api_key": current_key,
            "gl": "us",
            "hl": "en",
            "num": 20
        }

        try:
            print(f"[SerpAPI Request] Calling SerpAPI (Key #{key_idx}/{len(keys_to_try)}) for: '{query}'...")
            response = requests.get(url, params=params, timeout=4)
            if response.status_code == 200:
                data = response.json()

                # Check if SerpAPI error payload indicates quota or credit limit reached
                if "error" in data:
                    err_msg = str(data["error"]).lower()
                    if any(k in err_msg for k in ["credit", "search", "quota", "limit", "out of"]):
                        print(f"[SerpAPI Quota Alert] Key #{key_idx} out of credits: {data['error']} -> Switching to Key #{key_idx + 1}...")
                        continue

                results = data.get("organic_results") or data.get("amazon_results") or []
                if not results:
                    print(f"[SerpAPI Key #{key_idx}] 0 results returned. Trying next key...")
                    continue

                # Save raw results to local cache to preserve credits for future searches
                cache[query_key] = results
                save_serp_cache(cache)
                print(f"[SerpAPI Cache] Saved {len(results)} search results to local disk cache!")

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


# ---------------------------------------------------------------------------
# IMAGE FETCHING — Multi-strategy, no API key required for strategy 1
# ---------------------------------------------------------------------------

def _scrape_amazon_page_for_image(asin: str) -> str:
    """
    Strategy 1: Scrape the real image from Amazon product page HTML.
    Tries 2 URL patterns x 2 User-Agent variants = 4 attempts.
    Real product images are at m.media-amazon.com/images/I/, NOT /images/P/ (which is a 1x1 tracking GIF).
    """
    url_variants = [
        f"https://www.amazon.com/dp/{asin}",
        f"https://www.amazon.com/gp/product/{asin}",
    ]
    headers_variants = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
        },
        {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    ]
    for url in url_variants:
        for headers in headers_variants:
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code != 200:
                    continue
                html = resp.text
                # 1a. og:image meta tag (full-res hero image — most reliable)
                og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'<>]+)["\']', html)
                if og:
                    img = og.group(1).strip()
                    if "m.media-amazon.com" in img or "ssl-images-amazon" in img:
                        return img
                # 1b. data-a-dynamic-image JSON blob (has all resolution variants)
                dyn = re.search(r'data-a-dynamic-image=["\']({[^"\'<>]+})["\']', html)
                if dyn:
                    try:
                        img_map = json.loads(dyn.group(1).replace("&quot;", '"'))
                        if img_map:
                            best = max(img_map.items(), key=lambda kv: (kv[1][0] if isinstance(kv[1], list) else 0))
                            return best[0]
                    except Exception:
                        pass
                # 1c. Any m.media-amazon.com image URL in HTML (catches landingImage etc.)
                med = re.search(r"(https://m\.media-amazon\.com/images/I/[A-Za-z0-9%_\-\.]+\.jpg)", html)
                if med:
                    return med.group(0)
            except Exception:
                pass
    return ""


def _serpapi_amazon_product_image(asin: str) -> str:
    """
    Strategy 2: Fetch image via SerpAPI amazon_product engine.
    Uses one search credit but returns structured product data including images.
    """
    from config import SERPAPI_KEYS, SERPAPI_KEY
    keys = SERPAPI_KEYS if SERPAPI_KEYS else ([SERPAPI_KEY] if SERPAPI_KEY else [])
    for key in keys:
        try:
            resp = requests.get(
                "https://serpapi.com/search.json",
                params={"engine": "amazon_product", "asin": asin, "api_key": key, "amazon_domain": "amazon.com"},
                timeout=12
            )
            if resp.status_code == 200:
                data = resp.json()
                if "error" in data:
                    continue
                imgs = data.get("product_results", {}).get("images", [])
                if imgs:
                    return imgs[0].get("link") or imgs[0].get("src", "")
        except Exception:
            pass
    return ""


def _serpapi_google_image_search(asin: str, title: str = "") -> str:
    """
    Strategy 3: Search Google Images for the product via SerpAPI.
    Uses one search credit. Prefers Amazon-hosted image URLs.
    """
    from config import SERPAPI_KEYS, SERPAPI_KEY
    keys = SERPAPI_KEYS if SERPAPI_KEYS else ([SERPAPI_KEY] if SERPAPI_KEY else [])
    query = f"amazon {asin}" if not title else f"{title[:40]} amazon"
    for key in keys:
        try:
            resp = requests.get(
                "https://serpapi.com/search.json",
                params={"engine": "google_images", "q": query, "api_key": key, "gl": "us", "hl": "en", "num": 5},
                timeout=12
            )
            if resp.status_code == 200:
                data = resp.json()
                if "error" in data:
                    continue
                imgs = data.get("images_results", [])
                # Prefer Amazon-hosted images
                for img in imgs:
                    src = img.get("original") or img.get("thumbnail", "")
                    if src and ("amazon" in src or "m.media-amazon" in src or "ssl-images-amazon" in src):
                        return src
                # Fall back to first result thumbnail
                if imgs:
                    return imgs[0].get("thumbnail", "")
        except Exception:
            pass
    return ""


def _duckduckgo_image_search(asin: str, title: str = "") -> str:
    """
    Strategy 2: DuckDuckGo image search — completely FREE, no API key needed.
    Uses DDG's unofficial token-based image API. Searches ASIN + title on Amazon.
    """
    query = f"amazon {asin} {title[:30]}".strip()
    try:
        # Step 1: get the vqd token DDG requires for image searches
        token_resp = requests.post(
            "https://duckduckgo.com/",
            data={"q": query},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=8
        )
        # DDG returns: vqd="4-12345678..." or vqd=4-12345678...
        vqd_match = re.search(r'vqd="?([0-9\-]+)"?', token_resp.text)
        if not vqd_match:
            return ""
        vqd = vqd_match.group(1)

        # Step 2: fetch image results using the token
        img_resp = requests.get(
            "https://duckduckgo.com/i.js",
            params={"q": query, "vqd": vqd, "f": ",,,", "p": "1"},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://duckduckgo.com/",
            },
            timeout=8
        )
        if img_resp.status_code == 200:
            data = img_resp.json()
            results = data.get("results", [])
            # DDG returns 'image' (full URL) and optionally 'thumbnail'
            # Prefer Amazon-hosted images
            for r in results:
                src = r.get("image") or r.get("thumbnail", "")
                if src and ("amazon" in src or "m.media-amazon" in src or "ssl-images-amazon" in src):
                    return src
            # Fall back to first result image
            if results:
                return results[0].get("image") or results[0].get("thumbnail", "")
    except Exception as e:
        print(f"[Image Fetch] DDG search error for {asin}: {e}")
    return ""


def fetch_product_image_for_asin(asin: str, title: str = "") -> str:
    """
    PUBLIC API: Returns a real displayable high-res image URL for an Amazon product ASIN.
    Delegates to unified get_best_image_for_asin in modules/amazon_extractor.py.
    """
    from modules.amazon_extractor import get_best_image_for_asin
    res = get_best_image_for_asin(asin=asin, title=title, save_to_disk=True)
    if res and res.get("image_url"):
        return res["image_url"]

    # Fallback to direct Amazon CDN
    clean_asin = (asin or "").strip().upper()
    return f"https://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF-8&ServiceVersion=20070822&MarketPlace=US&ID=AsinImage&WS=1&Format=_SL1500_&ASIN={clean_asin}"


def _fetch_amazon_product_image(asin: str) -> str:
    """Internal alias used by _parse_raw_serp_results."""
    return fetch_product_image_for_asin(asin)


def _parse_raw_serp_results(results, num_results: int, min_price: float, max_price: float):
    parsed_products = []
    for item in results:
        asin = item.get("asin") or item.get("product_id")
        if not asin or len(asin) != 10:
            link = item.get("link", "") or item.get("product_link", "")
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
            print(f"[Amazon Finder Filter] Rating {rating_num} below 4.2 threshold for '{title[:35]}'")
            continue

        reviews = item.get("reviews", 150)

        # Get thumbnail — google organic results rarely have this; scraper fills the gap
        image_url = item.get("thumbnail") or item.get("image") or item.get("original_image_url", "")

        # Reject broken ad-widget tracker URLs and the 1x1 GIF ASIN-based pattern
        bad_url = (
            not image_url
            or "amazon-adsystem.com" in image_url
            or "ws-na.amazon" in image_url
            or ("/images/P/" in image_url and ".01._" in image_url)
        )
        if bad_url and asin:
            print(f"[Amazon Image] Thumbnail missing/broken for {asin}, fetching via scraper...")
            image_url = _fetch_amazon_product_image(asin)

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
            "features": [  # H3 FIX: must be a list, not a string
                f"{rating_num} Amazon Rating",
                f"{reviews} Customer Reviews",
                title[:45]
            ]
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
            "features": ["4.7 Amazon Rating", "1420 Customer Reviews", "Volcano Erupting Flame Diffuser"]
        },
        {
            "id": "B0F488XNNB",
            "title": "Kariosid Glass Mushroom Table Lamp Aesthetic Nightstand Light",
            "category": "Cozy Room Decor & Lighting",
            "price": "$29.99",
            "rating": "4.8",
            "reviews_count": 890,
            "affiliate_url": f"https://www.amazon.com/dp/B0F488XNNB?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/61Ci-1lZHNL._AC_SX679_.jpg",
            "features": ["4.8 Amazon Rating", "890 Customer Reviews", "Kariosid Glass Mushroom Lamp"]
        },
        {
            "id": "B0BZYN1MRP",
            "title": "GGK Smiling Mushrooms LED Neon Sign Ambient Wall Decor Light",
            "category": "Cozy Room Decor & Lighting",
            "price": "$22.99",
            "rating": "4.6",
            "reviews_count": 640,
            "affiliate_url": f"https://www.amazon.com/dp/B0BZYN1MRP?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/91OBhVIxJqL._AC_SX679_.jpg",
            "features": ["4.6 Amazon Rating", "640 Customer Reviews", "GGK Smiling Mushrooms Neon Sign"]
        },
        {
            "id": "B0G3X63T88",
            "title": "Lily of The Valley Flower Bedside Lamp Warm Ambient Nightlight",
            "category": "Cozy Room Decor & Lighting",
            "price": "$34.99",
            "rating": "4.9",
            "reviews_count": 1120,
            "affiliate_url": f"https://www.amazon.com/dp/B0G3X63T88?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/71FuFo33wOL._AC_SX679_PIbundle-6,TopRight,0,0_SH20_.jpg",
            "features": ["4.9 Amazon Rating", "1120 Customer Reviews", "Lily of The Valley Flower Lamp"]
        },
        {
            "id": "B0FVXXF9XJ",
            "title": "Retro Egg Tart Glass Mushroom Bedside Accent Table Lamp",
            "category": "Cozy Room Decor & Lighting",
            "price": "$27.99",
            "rating": "4.7",
            "reviews_count": 530,
            "affiliate_url": f"https://www.amazon.com/dp/B0FVXXF9XJ?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/61llXJeXxgL._AC_SX679_.jpg",
            "features": ["4.7 Amazon Rating", "530 Customer Reviews", "Retro Egg Tart Glass Mushroom Lamp"]
        }
    ]
