import requests
from config import NICHE, AMAZON_ASSOCIATE_TAG, SERPAPI_KEY, RAINFOREST_API_KEY

def fetch_amazon_products(query: str = None, num_results: int = 3):
    """
    Fetches live products from Amazon via SerpAPI if SERPAPI_KEY is available.
    Otherwise falls back to curated niche products.
    """
    if SERPAPI_KEY:
        print(f"[Amazon Finder] Fetching LIVE Amazon products via SerpAPI for: '{query or NICHE}'...")
        live_items = _fetch_from_serpapi(query or NICHE, num_results=num_results)
        if live_items:
            return live_items

    print("[Amazon Finder] Using curated high-converting niche products...")
    return fetch_sample_amazon_products()

def _fetch_from_serpapi(query: str, num_results: int = 3):
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
            for item in results[:num_results]:
                asin = item.get("asin") or item.get("product_id") or f"sp_{len(parsed_products)+1}"
                title = item.get("title", "Aesthetic Room Decor Find")
                
                price_val = item.get("price")
                if isinstance(price_val, dict):
                    price_str = price_val.get("raw") or str(price_val.get("extracted", "$24.99"))
                elif isinstance(price_val, str):
                    price_str = price_val
                else:
                    price_str = "$24.99"
                
                rating = str(item.get("rating", "4.5"))
                reviews = item.get("reviews", 150)
                image_url = item.get("thumbnail") or item.get("image", "")
                
                # Construct Amazon Affiliate Link with user's Store ID
                affiliate_url = f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
                
                parsed_products.append({
                    "id": asin,
                    "title": title,
                    "category": "Cozy Decor & Lighting",
                    "price": price_str,
                    "rating": rating,
                    "reviews_count": reviews,
                    "affiliate_url": affiliate_url,
                    "original_image_url": image_url,
                    "features": f"Highly rated {title} with {rating} stars and {reviews} customer reviews."
                })
            
            print(f"[Amazon Finder] Successfully fetched {len(parsed_products)} live Amazon items!")
            return parsed_products
        else:
            print(f"[Amazon Finder] SerpAPI HTTP Error {response.status_code}: {response.text[:100]}")
    except Exception as e:
        print(f"[Amazon Finder] Exception querying SerpAPI: {e}")
        
    return None

def fetch_sample_amazon_products(niche: str = NICHE):
    """Fallback sample products formatted with user affiliate tag and official Amazon Associates links."""
    tag = AMAZON_ASSOCIATE_TAG
    return [
        {
            "id": "B08B896T2W",
            "title": "VOBAGA Coffee Mug Warmer for Desk with Auto Shut Off",
            "category": "Desk Accessories & Heating",
            "price": "$21.99",
            "rating": "4.7",
            "reviews_count": 8420,
            "affiliate_url": f"https://www.amazon.com/gp/product/B08B896T2W?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg",
            "features": "3 temperature settings, auto shut-off after 4 hours, splash-proof electric heating plate."
        },
        {
            "id": "B07NKWJCVH",
            "title": "COSORI Premium Stainless Steel Coffee Mug Warmer for Desk",
            "category": "Desk Accessories & Heating",
            "price": "$29.99",
            "rating": "4.8",
            "reviews_count": 12510,
            "affiliate_url": f"https://www.amazon.com/gp/product/B07NKWJCVH?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/61SsDfH706L._AC_SL1254_.jpg",
            "features": "Digital LED temperature display, brushed stainless steel body, high temperature heating pad."
        },
        {
            "id": "B093S4S6XG",
            "title": "Aesthetic Sunset Projection Lamp for Room Decor & Vibe",
            "category": "Ambient Lighting & Lamps",
            "price": "$18.50",
            "rating": "4.8",
            "reviews_count": 1280,
            "affiliate_url": f"https://www.amazon.com/gp/product/B093S4S6XG?tag={tag}",
            "original_image_url": "https://m.media-amazon.com/images/I/618IaAUvESL._AC_SL1254_.jpg",
            "features": "180 degree rotation sunset projection, warm golden orange sunset ambiance, perfect for cozy room photo backdrop."
        }
    ]



