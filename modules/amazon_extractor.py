import re
import io
import json
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
    if not image_url or "SL1500" in image_url:
        return image_url or ""
    # Strip Amazon dynamic resizing tokens (e.g. ._AC_SX342_SY445_QL70_FMwebp_ -> ._AC_SL1500_)
    return re.sub(r'\._(?:AC_)?[A-Za-z0-9_,-]+\.', '._AC_SL1500_.', image_url)

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
        top_pixels = list(top_crop.getdata())
        top_contrast = sum(1 for p in top_pixels if p > 120) / len(top_pixels)
        
        full_pixels = list(edges.getdata())
        full_contrast = sum(1 for p in full_pixels if p > 120) / (w * h)
        
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
        # White studio cutouts are single products, never split collages
        if not is_lifestyle_photo(image_url):
            return False

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        raw = requests.get(image_url, headers=headers, timeout=6).content
        img = Image.open(io.BytesIO(raw)).convert('RGB').resize((200, 200))
        w, h = img.size
        
        def scan_band(pixels_list, threshold=240, seam_ratio=0.85):
            white_count = sum(1 for r, g, b in pixels_list if r > threshold and g > threshold and b > threshold)
            return (white_count / len(pixels_list)) > seam_ratio if pixels_list else False
        
        # Check horizontal center band (y = h//2)
        h_band = [img.getpixel((x, h // 2)) for x in range(w)]
        # Check vertical center band (x = w//2)
        v_band = [img.getpixel((w // 2, y)) for y in range(h)]
        
        is_h_seam = scan_band(h_band)
        is_v_seam = scan_band(v_band)
        
        return is_h_seam and is_v_seam
    except Exception as e:
        return False

def has_human_presence(image_url: str) -> bool:
    """
    Detects human skin tones in image using color histogram on flesh-tone HSV range.
    Returns True if a significant human presence (hand, face, body) is detected.
    """
    if not image_url:
        return False
    try:
        res = requests.get(image_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
        if res.status_code != 200:
            return False
        img = Image.open(io.BytesIO(res.content)).convert('RGB').resize((100, 100))
        skin_pixels = 0
        total = 100 * 100
        for x in range(100):
            for y in range(100):
                r, g, b = img.getpixel((x, y))
                # Tightened flesh-tone range:
                # (r-g) < 40 excludes orange/amber product tones (candles, lamps, terracotta)
                # (r-b) > 30 requires stronger red bias (real skin, not warm wood/amber)
                # r must dominate both channels significantly
                if (r > 80 and g > 40 and b > 20
                        and r > g and r > b
                        and (r - b) > 30
                        and (r - g) < 40
                        and g > b):
                    skin_pixels += 1
        # Raise threshold to 15% to avoid false positives from warm-lit room shots
        return (skin_pixels / total) > 0.15
    except Exception:
        return False

def calculate_cozy_vibe_score(image_url: str) -> float:
    """
    Scores an Amazon product photo on a 1-10 Cozy Vibe Aesthetics scale based on:
      1. Warm color tones (amber, gold, terracotta)
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

def score_product_photo(image_url: str, title: str = "") -> dict:
    """
    Scores an Amazon product photo on a 0-100 Quality Scale & pre-computes optimal prompt strength:
      - 90-100: Pure white studio cutout (Prompt strength = 0.82 for scratch synthesis)
      - 75-89: Clean single-item lifestyle photo (Prompt strength = 0.48 for room enhancement)
      - 60-74: Clean multi-pack / set / delicate item (Prompt strength = 0.28 to preserve item count)
      - 25-59: Usable photo with minor edge callout (Prompt strength = 0.20 for safe touch-up)
      - 0: Unusable (split grid collage or heavy human face/body presence)
    """
    if not image_url or not image_url.startswith("http"):
        return {"score": 0, "prompt_strength": 0.48, "is_white_bg": False, "reason": "invalid_url"}

    # 1. Hard Disqualifiers
    if is_grid_collage(image_url):
        return {"score": 0, "prompt_strength": 0.48, "is_white_bg": False, "reason": "grid_collage"}
    
    try:
        has_human = has_human_presence(image_url)
    except Exception:
        has_human = False

    if has_human:
        return {"score": 0, "prompt_strength": 0.48, "is_white_bg": False, "reason": "human_presence"}

    try:
        has_text = has_text_annotation(image_url)
        is_lifestyle = is_lifestyle_photo(image_url)
    except Exception:
        # Network error — assume usable with neutral score
        return {"score": 50, "prompt_strength": 0.48, "is_white_bg": False, "reason": "network_error_assume_ok"}
    is_white_bg = not is_lifestyle

    title_lwr = (title or "").lower()
    is_set_or_multi = any(kw in title_lwr for kw in ["set of", "pack of", " 2 ", " 3 ", " 4 ", "pcs", "pair", "crystal", "prism", "vases"])

    if not has_text:
        if is_white_bg:
            return {"score": 95, "prompt_strength": 0.82, "is_white_bg": True, "reason": "clean_white_cutout"}
        elif is_set_or_multi:
            return {"score": 75, "prompt_strength": 0.28, "is_white_bg": False, "reason": "clean_lifestyle_multipack"}
        else:
            vibe = calculate_cozy_vibe_score(image_url)
            score = max(70, min(90, int(60 + (vibe * 3.0))))
            return {"score": score, "prompt_strength": 0.48, "is_white_bg": False, "reason": "clean_lifestyle_single"}
    else:
        # Minor overlay present — still usable at low transformation strength instead of binary discard
        return {"score": 35, "prompt_strength": 0.20, "is_white_bg": is_white_bg, "reason": "minor_text_overlay"}


def select_clean_photo_or_skip(photos: list, title: str = "") -> tuple:
    """
    Evaluates listing photos with 0-100 quality scoring.
    Returns (best_photo_url, should_skip).
    Only skips if zero photos have score > 0.
    """
    if not photos:
        return ("", True)
    
    scored_candidates = []
    for u in photos:
        if u and u.startswith("http"):
            res = score_product_photo(u, title=title)
            if res["score"] > 0:
                scored_candidates.append((res["score"], u, res))
                print(f"[Photo Quality Scorer] ...{u[-30:]} | Score: {res['score']}/100 ({res['reason']})")

    if scored_candidates:
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        best_score, best_photo, best_meta = scored_candidates[0]
        print(f"[Photo Quality Scorer] SELECTED BEST PHOTO: ...{best_photo[-30:]} (Score: {best_score}/100)")
        return (best_photo, False)

    print("[Amazon Extractor] [WARNING] No usable photos found (all collages/models). Product flagged for fallback.")
    return ("", True)


def get_best_image_for_asin(asin: str, title: str = "", photos: list = None, save_to_disk: bool = True) -> dict:
    """
    UNIFIED IMAGE EXTRACTION ENGINE
    Single authoritative contract used by Discovery, Batch Extract, Web Console, and n8n.
      1. Checks local raw_images/raw_{ASIN}.jpg
      2. Checks SQLite image_cache.db
      3. Scrapes/Scores Amazon listing photos (0-100 scale)
      4. CDN Fallback (never cross-contaminates with another product's photo)
      5. Downloads to raw_images/ and saves to SQLite cache
    """
    from pathlib import Path
    import requests
    
    clean_asin = (asin or "").strip().upper()
    if not clean_asin:
        return {"asin": "", "image_url": "", "local_path": "", "quality_score": 0, "prompt_strength": 0.48, "is_white_bg": False, "source": "none"}

    repo_dir = Path(__file__).resolve().parent.parent
    raw_dir = repo_dir / "raw_images"
    raw_dir.mkdir(parents=True, exist_ok=True)
    target_raw_file = raw_dir / f"raw_{clean_asin}.jpg"

    # 1. Local Disk Check
    if target_raw_file.exists() and target_raw_file.stat().st_size > 5000:
        from modules.image_cache_db import get_cached_image
        cached_url = get_cached_image(clean_asin) or f"https://ws-na.amazon-adsystem.com/widgets/q?_encoding=UTF-8&ServiceVersion=20070822&MarketPlace=US&ID=AsinImage&WS=1&Format=_SL1500_&ASIN={clean_asin}"
        score_res = score_product_photo(cached_url, title=title) if cached_url.startswith("http") else {"prompt_strength": 0.48, "is_white_bg": False}
        return {
            "asin": clean_asin,
            "image_url": cached_url,
            "local_path": str(target_raw_file),
            "quality_score": 90,
            "prompt_strength": score_res.get("prompt_strength", 0.48),
            "is_white_bg": score_res.get("is_white_bg", False),
            "source": "local_disk"
        }

    # 2. SQLite Cache Check
    from modules.image_cache_db import get_cached_image, set_cached_image
    cached_url = get_cached_image(clean_asin)
    winning_url = ""
    winning_source = "cache"
    best_meta = {"score": 50, "prompt_strength": 0.48, "is_white_bg": False}

    if cached_url and cached_url.startswith("http") and "amazon-adsystem" not in cached_url:
        winning_url = cached_url
        best_meta = score_product_photo(winning_url, title=title)
    else:
        # 3. Listing Photos Scrape & Quality Scoring
        candidate_photos = photos or fetch_all_product_images(clean_asin)
        # Filter out tracking sprites (_SP\d+), ad widgets, and non-media-amazon CDN URLs
        candidate_photos = [
            u for u in candidate_photos
            if u and u.startswith("http")
            and "amazon-adsystem" not in u
            and "ws-na." not in u
            and not any(f"_SP{n}" in u for n in ["100", "200", "300"])
        ]
        scored = []
        for p_url in candidate_photos:
            if p_url and p_url.startswith("http"):
                res = score_product_photo(p_url, title=title)
                if res["score"] > 0:
                    scored.append((res["score"], p_url, res))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            best_score, winning_url, best_meta = scored[0]
            winning_source = "scraped_listing"
        elif candidate_photos:
            # Fallback to main listing photo if quality filter rejected all candidates
            winning_url = candidate_photos[0]
            winning_source = "main_listing_fallback"
            best_meta = {"score": 30, "prompt_strength": 0.48, "is_white_bg": True}
        else:
            # Product-Specific Constructable Fallback
            winning_url = f"https://m.media-amazon.com/images/P/{clean_asin}.01.LZZZZZZZ.jpg"
            winning_source = "constructable_fallback"
            best_meta = {"score": 30, "prompt_strength": 0.48, "is_white_bg": True}

    # Save to SQLite Cache
    set_cached_image(clean_asin, winning_url, source=winning_source)

    # 5. Stream download to raw_images/raw_{ASIN}.jpg
    MIN_IMAGE_BYTES = 5000  # anything smaller is a broken/placeholder image
    if save_to_disk and winning_url.startswith("http"):
        downloaded_ok = False
        urls_to_try = [winning_url]
        # If using constructable fallback, also try alternative known formats
        if winning_source == "constructable_fallback":
            urls_to_try += [
                f"https://m.media-amazon.com/images/I/{clean_asin}._SL1500_.jpg",  # direct ASIN format
                f"https://images-na.ssl-images-amazon.com/images/P/{clean_asin}.01.LZZZZZZZ.jpg",
            ]
        for try_url in urls_to_try:
            try:
                resp = requests.get(try_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, stream=True, timeout=15)
                if resp.status_code == 200:
                    with open(target_raw_file, "wb") as f_out:
                        for chunk in resp.iter_content(chunk_size=16384):
                            f_out.write(chunk)
                    if target_raw_file.stat().st_size >= MIN_IMAGE_BYTES:
                        print(f"[Unified Extractor] Downloaded raw image for {clean_asin} -> {target_raw_file.name} ({target_raw_file.stat().st_size//1024}KB)")
                        downloaded_ok = True
                        break
                    else:
                        print(f"[Unified Extractor] Tiny file ({target_raw_file.stat().st_size}B) from {try_url[:60]} — trying next URL")
                        target_raw_file.unlink(missing_ok=True)  # delete bad file
            except Exception as e_dl:
                print(f"[Unified Extractor Warning] Download failed for {clean_asin} ({try_url[:50]}): {e_dl}")
        if not downloaded_ok:
            print(f"[Unified Extractor] All download attempts failed for {clean_asin} — will serve CDN URL")

    return {
        "asin": clean_asin,
        "image_url": winning_url,
        "local_path": str(target_raw_file) if target_raw_file.exists() else "",
        "quality_score": best_meta.get("score", 50),
        "prompt_strength": best_meta.get("prompt_strength", 0.48),
        "is_white_bg": best_meta.get("is_white_bg", False),
        "source": winning_source
    }

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
                photos = list(dict.fromkeys(photos))  # Deduplicate while preserving order

                sorted_photos = photos
                lifestyle_flags = [is_lifestyle_photo(img) for img in sorted_photos]
                has_lifestyle = any(lifestyle_flags)
                
                affiliate_url = f"https://www.{domain}/dp/{asin}?tag={AMAZON_ASSOCIATE_TAG}"
                
                features_list = p.get("features", []) or p.get("description", "")
                if isinstance(features_list, list):
                    features_str = " ".join(features_list[:3])
                else:
                    features_str = str(features_list)[:200]

                lifestyle_cnt = sum(1 for f in lifestyle_flags if f)
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


def fetch_all_product_images(asin: str) -> list:
    """
    Multi-strategy fetcher that returns ALL gallery images for a given ASIN.

    Strategy order:
      1. SerpAPI amazon_product engine (thumbnails[] key) - with key rotation
      2. Direct Amazon page scrape - extracts colorImages JSON block embedded in page
      3. Single cached image from image_cache_db as last resort

    Returns a list of high-res m.media-amazon.com image URLs.
    """
    asin = asin.strip().upper()

    # ── Strategy 1: SerpAPI amazon_product engine (gives full gallery) ──
    try:
        from config import SERPAPI_KEYS, SERPAPI_KEY as _SERPAPI_KEY
        keys = list(SERPAPI_KEYS) if SERPAPI_KEYS else ([_SERPAPI_KEY] if _SERPAPI_KEY else [])
        for key in keys:
            if not key:
                continue
            try:
                r = requests.get(
                    "https://serpapi.com/search.json",
                    params={"engine": "amazon_product", "asin": asin,
                            "amazon_domain": "amazon.com", "api_key": key},
                    timeout=8
                )
                if r.status_code == 200:
                    data = r.json()
                    thumbs = data.get("product_results", {}).get("thumbnails", [])
                    if thumbs:
                        images = [enhance_to_max_resolution(t) for t in thumbs if t]
                        images = list(dict.fromkeys(images))
                        images = [img for img in images if img and "amazon-adsystem" not in img]
                        if images:
                            print(f"[fetch_all_product_images] SerpAPI returned {len(images)} images for {asin}")
                            return images
            except Exception as e:
                print(f"[fetch_all_product_images] SerpAPI key failed: {e}")
                continue
    except Exception as e:
        print(f"[fetch_all_product_images] SerpAPI block error: {e}")

    # ── Strategy 2: Scrape Amazon page for embedded colorImages JSON ──
    try:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        ]
        for ua in user_agents:
            try:
                res = requests.get(
                    f"https://www.amazon.com/dp/{asin}",
                    headers={"User-Agent": ua,
                             "Accept-Language": "en-US,en;q=0.9",
                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"},
                    timeout=10
                )
                if res.status_code != 200:
                    continue

                html = res.text
                all_images = []

                # Amazon embeds all product images in a JS variable 'colorImages'
                color_match = re.search(r"'colorImages'\s*:\s*\{[^}]*'initial'\s*:\s*(\[.*?\])\s*\}", html, re.DOTALL)
                if not color_match:
                    color_match = re.search(r'"colorImages"\s*:\s*\{\s*"initial"\s*:\s*(\[.*?\])\s*\}', html, re.DOTALL)

                if color_match:
                    try:
                        img_entries = json.loads(color_match.group(1))
                        for entry in img_entries:
                            for res_key in ("hiRes", "large", "main"):
                                url = entry.get(res_key)
                                if url and "m.media-amazon.com" in url:
                                    all_images.append(enhance_to_max_resolution(url))
                                    break
                    except Exception:
                        pass

                if not all_images:
                    # Fallback: regex scan all media-amazon /I/ image URLs in the page
                    found = re.findall(r'https://m\.media-amazon\.com/images/I/[A-Za-z0-9+_%.-]+\.(?:jpg|jpeg|png|webp)', html, re.IGNORECASE)
                    all_images = [enhance_to_max_resolution(u) for u in found]

                # Deduplicate, strip ad URLs, filter out tiny icon sprites
                all_images = list(dict.fromkeys(all_images))
                all_images = [u for u in all_images if u and "amazon-adsystem" not in u]

                def _is_product_img(url):
                    if not url: return False
                    lower = url.lower()
                    if any(lower.endswith(ext) for ext in ['.js', '.css', '.html', '.htm', '.json']):
                        return False
                    if '._rc' in lower or ('._png' in lower and not lower.endswith('.png')):
                        return False
                    m = re.search(r'/images/I/([A-Za-z0-9+%-]+)\.', url)
                    return bool(m and len(m.group(1)) > 10)

                all_images = [u for u in all_images if _is_product_img(u)]

                if all_images:
                    print(f"[fetch_all_product_images] Page scrape returned {len(all_images)} images for {asin}")
                    return all_images[:12]

            except Exception as e:
                print(f"[fetch_all_product_images] Page scrape UA failed: {e}")
                continue
    except Exception as e:
        print(f"[fetch_all_product_images] Page scrape block error: {e}")

    # ── Strategy 3: Single cached image as last resort ──
    try:
        from modules.image_cache_db import get_cached_image
        from modules.amazon_finder import fetch_product_image_for_asin
        cached = get_cached_image(asin)
        if cached and cached.startswith("http") and "amazon-adsystem" not in cached:
            print(f"[fetch_all_product_images] Using single cached image for {asin}")
            return [cached]
        fetched = fetch_product_image_for_asin(asin)
        if fetched and fetched.startswith("http") and "amazon-adsystem" not in fetched:
            return [fetched]
    except Exception as e:
        print(f"[fetch_all_product_images] Cache fallback error: {e}")

    print(f"[fetch_all_product_images] No images found for {asin}")
    return []
