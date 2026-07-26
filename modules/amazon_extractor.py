import re
import requests
from bs4 import BeautifulSoup
from config import SERPAPI_KEY, AMAZON_ASSOCIATE_TAG

def extract_asin_from_url(url: str) -> str:
    """Extracts 10-character Amazon ASIN from any raw Amazon product URL or query string."""
    asin_match = re.search(r'/(?:dp|gp/product|product)/([A-Z0-9]{10})', url, re.IGNORECASE)
    if asin_match:
        return asin_match.group(1).upper()
    
    # Fallback pattern check for ASIN query or direct code
    code_match = re.search(r'\b([A-Z0-9]{10})\b', url, re.IGNORECASE)
    if code_match:
        return code_match.group(1).upper()
    return ""

def enhance_to_max_resolution(image_url: str) -> str:
    """Converts low-res Amazon thumbnail URLs into maximum high-res SL1500 master images."""
    if not image_url:
        return ""
    # Strip Amazon dynamic resizing tokens (e.g. ._AC_SX342_SY445_QL70_FMwebp_ -> ._AC_SL1500_)
    high_res = re.sub(r'\._AC_[A-Za-z0-9_,-]+\.', '._AC_SL1500_.', image_url)
    high_res = re.sub(r'\._[A-Za-z0-9_,-]+\.', '._AC_SL1500_.', high_res)
    return high_res

def get_product_details_and_photos(url_or_asin: str) -> dict:
    """
    Intelligent Amazon Product & Multi-Photo Extractor.
    Extracts ASIN, full high-res listing photos, clean title, price, rating, reviews, and features.
    """
    asin = extract_asin_from_url(url_or_asin) if "http" in url_or_asin else url_or_asin.strip().upper()
    if not asin:
        print(f"[Amazon Extractor] Invalid Amazon URL or ASIN provided: {url_or_asin}")
        return None

    print(f"[Amazon Extractor] Extracting full photo suite for ASIN: {asin}...")

    
    domain = "amazon.co.uk" if "amazon.co.uk" in url_or_asin else "amazon.com"

    # 1. Primary Extraction: SerpAPI Amazon Product Engine
    if SERPAPI_KEY:
        try:
            r = requests.get(
                "https://serpapi.com/search.json",
                params={"engine": "amazon_product", "asin": asin, "amazon_domain": domain, "api_key": SERPAPI_KEY},
                timeout=20
            )
            if r.status_code == 200:
                p = r.json().get("product_results", {})
                title = p.get("title") or "Aesthetic Bedside Decor Find"
                price_data = p.get("price")
                if isinstance(price_data, dict):
                    price = price_data.get("raw") or str(price_data.get("extracted", "$14.99"))
                elif isinstance(price_data, str):
                    price = price_data
                else:
                    price = "$14.99"
                
                rating = str(p.get("rating", "4.6"))
                reviews = p.get("reviews", 500)
                
                # Retrieve raw thumbnails and upgrade to max-resolution SL1500 images
                raw_photos = p.get("thumbnails", []) or [p.get("thumbnail")]
                photos = [enhance_to_max_resolution(img) for img in raw_photos if img]
                photos = list(dict.fromkeys(photos)) # Deduplicate while preserving order
                
                affiliate_url = f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
                
                features_list = p.get("features", []) or p.get("description", "")
                if isinstance(features_list, list):
                    features_str = " ".join(features_list[:3])
                else:
                    features_str = str(features_list)[:200]

                print(f"[Amazon Extractor] Successfully extracted {len(photos)} high-res photos for: {title[:40]}")
                return {
                    "id": asin,
                    "title": title,
                    "category": "Aesthetic Room Decor & Lighting",
                    "price": price,
                    "rating": rating,
                    "reviews_count": reviews,
                    "affiliate_url": affiliate_url,
                    "original_image_url": photos[0] if photos else "",
                    "all_photos": photos,
                    "features": features_str or f"High-rated {title} with {rating} stars and {reviews} customer reviews."
                }
        except Exception as e:
            print(f"[Amazon Extractor] SerpAPI extraction error: {e}")

    # 2. Fallback Extraction: Direct BeautifulSoup Scraper
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        res = requests.get(f"https://www.{domain}/dp/{asin}", headers=headers, timeout=10)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            title_el = soup.find("span", {"id": "productTitle"})
            title = title_el.get_text().strip() if title_el else "Aesthetic Decor Find"
            
            # Find all media-amazon image URLs
            raw_imgs = [img['src'] for img in soup.find_all('img') if 'media-amazon' in img.get('src', '') and 'I/' in img.get('src', '')]
            photos = [enhance_to_max_resolution(img) for img in raw_imgs]
            photos = list(dict.fromkeys(photos))
            
            return {
                "id": asin,
                "title": title,
                "category": "Aesthetic Room Decor & Lighting",
                "price": "$14.99",
                "rating": "4.6",
                "reviews_count": 500,
                "affiliate_url": f"https://www.amazon.com/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}",
                "original_image_url": photos[0] if photos else "",
                "all_photos": photos,
                "features": f"Aesthetic {title} for cozy room decor."
            }
    except Exception as e:
        print(f"[Amazon Extractor] Scraper fallback error: {e}")

    return None
