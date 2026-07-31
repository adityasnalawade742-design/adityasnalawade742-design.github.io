import re
import io
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter
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
            border_pixels.append(img.getpixel((w - 1, y)))
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
        
        has_txt = (top_contrast > 0.035) or (full_contrast > 0.035)
        if has_txt:
            print(f"[Text Detector] DISCARDING Text/Glyphs Detected in image (...{image_url[-30:]}) [top={top_contrast:.4f}, full={full_contrast:.4f}]")
        else:
            print(f"[Text Detector] CLEAN PHOTO (NO TEXT) (...{image_url[-30:]}) [top={top_contrast:.4f}, full={full_contrast:.4f}]")
        return has_txt
    except Exception:
        return False

def is_grid_collage(image_url: str) -> bool:
    """
    Detects multi-panel split grid collage photos (2-grid, 4-grid collages).
    Scans central horizontal/vertical coordinate bands for seam lines and white dividers.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        raw = requests.get(image_url, headers=headers, timeout=10).content
        img = Image.open(io.BytesIO(raw)).convert('RGB').resize((200, 200))
        gray = img.convert('L')
        edges = gray.filter(ImageFilter.FIND_EDGES)
        
        max_v_white = max((sum(1 for y in range(200) if gray.getpixel((x, y)) > 240) / 200 for x in range(90, 110)), default=0)
        max_h_white = max((sum(1 for x in range(200) if gray.getpixel((x, y)) > 240) / 200 for y in range(90, 110)), default=0)
        
        max_v_edge = max((sum(1 for y in range(200) if edges.getpixel((x, y)) > 40) / 200 for x in range(90, 110)), default=0)
        max_h_edge = max((sum(1 for x in range(200) if edges.getpixel((x, y)) > 40) / 200 for y in range(90, 110)), default=0)
        
        is_collage = (max_v_white > 0.60 or max_v_edge > 0.60) and (max_h_white > 0.60 or max_h_edge > 0.60)
        if is_collage:
            print(f"[Grid Collage Scanner] DISCARDING Multi-Panel Collage (...{image_url[-30:]}) [v_w={max_v_white:.2f}, h_w={max_h_white:.2f}]")
        return is_collage
    except Exception as e:
        print(f"[is_grid_collage Error] {e}")
        return False

def has_human_presence(image_url: str) -> bool:
    """
    Detects photos containing human models, hands, or people.
    Evaluates skin tone color spectrum ratio.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        raw = requests.get(image_url, headers=headers, timeout=10).content
        img = Image.open(io.BytesIO(raw)).convert('RGB').resize((100, 100))
        w, h = img.size
        
        skin_pixels = 0
        total = w * h
        
        for x in range(w):
            for y in range(h):
                r, g, b = img.getpixel((x, y))
                if r > 140 and g > 90 and b > 60 and (r > g + 15) and (g > b + 10):
                    skin_pixels += 1
        
        skin_ratio = skin_pixels / total
        has_human = skin_ratio > 0.18
        if has_human:
            print(f"[Human/Model Scanner] DISCARDING Human Model/Hand Detected (...{image_url[-30:]}) [skin_ratio={skin_ratio:.3f}]")
        return has_human
    except Exception:
        return False

def calculate_cozy_vibe_score(image_url: str) -> float:
    """
    Evaluates cozy room aesthetic score (1.0 to 10.0) based on:
      1. Warmth ratio (amber/gold/wood warm hues vs cold white/grey)
      2. Soft contrast & ambient lighting depth
      3. Background richness
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        raw = requests.get(image_url, headers=headers, timeout=10).content
        img = Image.open(io.BytesIO(raw)).convert('RGB').resize((100, 100))
        w, h = img.size
        
        warm_pixels = 0
        pure_white_pixels = 0
        total = w * h
        
        for x in range(w):
            for y in range(h):
                r, g, b = img.getpixel((x, y))
                if r > 235 and g > 235 and b > 235:
                    pure_white_pixels += 1
                elif r > g + 8 and g >= b and r > 70:
                    warm_pixels += 1
        
        white_ratio = pure_white_pixels / total
        warm_ratio = warm_pixels / total
        
        score = 4.0 + (warm_ratio * 14.0)
        if white_ratio > 0.35:
            score -= (white_ratio * 6.0)
            
        return max(1.0, min(10.0, round(score, 2)))
    except Exception as e:
        print(f"[Cozy Vibe Scorer Error] {e}")
        return 5.0

def select_clean_photo_or_skip(photos: list) -> tuple[str, bool]:
    """
    Iterates through Amazon listing photos:
      1. Filters out photos containing seller text overlays/infographics.
      2. Scores remaining clean photos by Cozy Vibe Aesthetics (warmth, lighting, depth).
      3. Selects the #1 highest scoring cozy photo!
      4. If ALL photos contain text overlays, returns ("", True) to SKIP the product!
    """
    if not photos:
        return ("", True)
    
    clean_photos = []
    for u in photos:
        if u and u.startswith("http"):
            if not has_text_annotation(u) and not is_grid_collage(u) and not has_human_presence(u):
                clean_photos.append(u)
    
    if clean_photos:
        # Score each clean photo for cozy room vibes
        scored_photos = []
        for u in clean_photos:
            vibe_score = calculate_cozy_vibe_score(u)
            scored_photos.append((vibe_score, u))
            print(f"[Cozy Vibe Scorer] Photo ...{u[-30:]} | Score: {vibe_score:.1f}/10")
        
        # Sort descending by Cozy Vibe Score
        scored_photos.sort(key=lambda x: x[0], reverse=True)
        best_vibe_score, best_photo = scored_photos[0]
        print(f"[Cozy Vibe Scorer] SELECTED BEST PHOTO: ...{best_photo[-30:]} (Score: {best_vibe_score:.1f}/10)")
        return (best_photo, False)
    
    print("[Amazon Extractor] [WARNING] ALL listing photos contain seller text/infographics! Product will be SKIPPED per text-free policy.")
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
