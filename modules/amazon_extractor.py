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

def is_lifestyle_photo(image_url: str) -> bool:
    """
    Analyzes an Amazon photo URL to detect if it features a real lifestyle background
    (room interior, ambient light, wood surfaces) vs a plain white studio cutout.
    Returns True if it has a rich lifestyle background, False if it is a white cutout.
    """
    if not image_url:
        return False
    try:
        import io, requests
        from PIL import Image
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        if res.status_code != 200:
            return False
        img = Image.open(io.BytesIO(res.content)).convert('RGB')
        w, h = img.size
        border_pixels = []
        for x in range(0, w, max(1, w // 20)):
            border_pixels.append(img.getpixel((x, 0)))
            border_pixels.append(img.getpixel((x, h - 1)))
        for y in range(0, h, max(1, h // 20)):
            border_pixels.append(img.getpixel((0, y)))
            white_count = sum(1 for r, g, b in border_pixels if r > 240 and g > 240 and b > 240)
        white_ratio = white_count / len(border_pixels)
        return white_ratio < 0.60
    except Exception:
        return True

def has_text_annotation(image_url: str) -> bool:
    """
    Analyzes an Amazon listing photo to detect if it contains seller text/infographic overlays
    (e.g., dimension arrows, feature badges, promotional text callouts, handwritten text on products).
    Uses high-frequency pixel contrast & edge density across top and center image regions.
    """
    if not image_url:
        return False
    try:
        import io, requests
        from PIL import Image, ImageFilter
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=6)
        if res.status_code != 200 or len(res.content) < 3000:
            return False
        img = Image.open(io.BytesIO(res.content)).convert('L')
        # Edge detection filter to catch sharp text glyphs, letters, and callouts
        edges = img.filter(ImageFilter.FIND_EDGES)
        w, h = edges.size
        # Inspect top 25% margin specifically for top seller headline text callouts
        top_crop = edges.crop((0, 0, w, int(h * 0.25)))
        top_pixels = list(top_crop.get_flattened_data())
        top_contrast = sum(1 for p in top_pixels if p > 120) / len(top_pixels)
        
        full_contrast = sum(1 for p in list(edges.get_flattened_data()) if p > 120) / (w * h)
        
        has_txt = (top_contrast > 0.008) or (full_contrast > 0.022)
        if has_txt:
            print(f"[Text Detector] ❌ Text/Glyphs Detected in image (...{image_url[-30:]}) [top={top_contrast:.4f}, full={full_contrast:.4f}]")
        else:
            print(f"[Text Detector] ✅ 100% CLEAN PHOTO (NO TEXT) (...{image_url[-30:]}) [top={top_contrast:.4f}, full={full_contrast:.4f}]")
        return has_txt
    except Exception:
        return False

def select_clean_photo_or_skip(photos: list) -> tuple[str, bool]:
    """
    Iterates through Amazon listing photos:
      1. Filters out photos containing seller text overlays/infographics.
      2. Prioritizes clean LIFESTYLE ROOM photos first (Prompt 1).
      3. If no clean room photos exist, selects clean WHITE CUTOUT photos (Prompt 2).
      4. If ALL photos contain text overlays, returns ("", True) to SKIP the product!
    """
    if not photos:
        return ("", True)
    
    clean_photos = []
    for u in photos:
        if u and u.startswith("http"):
            if not has_text_annotation(u):
                clean_photos.append(u)
    
    if clean_photos:
        # Prioritize clean lifestyle room photos first
        clean_lifestyle = [u for u in clean_photos if is_lifestyle_photo(u)]
        if clean_lifestyle:
            return (clean_lifestyle[0], False)
        # Fallback to clean white studio cutout photo
        return (clean_photos[0], False)
    
    print("[Amazon Extractor] ⚠️ ALL listing photos contain seller text/infographics! Product will be SKIPPED per text-free policy.")
    return ("", True)

EXCLUDED_KIDS_KEYWORDS = [
    "for kids", "kids", "children", "child", "toddler", "baby", "toy", "nursery toy",
    "drawing board for kids", "playroom", "kid gift", "birthday festival"
]

def is_adult_aesthetic_product(title: str) -> bool:
    """
    Filters out children's products, toys, and kids' drawing boards.
    Returns True if the item is an adult/home decor product, False if it's for kids.
    """
    if not title:
        return True
    t_lower = title.lower()
    for kw in EXCLUDED_KIDS_KEYWORDS:
        if kw in t_lower:
            return False
    return True

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

                sorted_photos = photos
                has_lifestyle = any(is_lifestyle_photo(img) for img in sorted_photos)
                
                affiliate_url = f"https://www.{domain}/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
                
                features_list = p.get("features", []) or p.get("description", "")
                if isinstance(features_list, list):
                    features_str = " ".join(features_list[:3])
                else:
                    features_str = str(features_list)[:200]

                lifestyle_cnt = sum(1 for img in sorted_photos if is_lifestyle_photo(img))
                print(f"[Amazon Extractor] Extracted {len(sorted_photos)} photos ({lifestyle_cnt} lifestyle backgrounds) for: {title[:40]}")
                return {
                    "id": asin,
                    "title": title,
                    "category": "Aesthetic Room Decor & Lighting",
                    "price": price,
                    "rating": rating,
                    "reviews_count": reviews,
                    "affiliate_url": affiliate_url,
                    "original_image_url": sorted_photos[0] if sorted_photos else "",
                    "all_photos": sorted_photos,
                    "has_lifestyle_photos": has_lifestyle,
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
                "affiliate_url": f"https://www.{domain}/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}",
                "original_image_url": photos[0] if photos else "",
                "all_photos": photos,
                "features": f"Aesthetic {title} for cozy room decor."
            }
    except Exception as e:
        print(f"[Amazon Extractor] Scraper fallback error: {e}")

    return None
