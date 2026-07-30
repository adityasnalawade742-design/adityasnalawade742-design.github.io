import sys
import io
import requests
import numpy as np
from PIL import Image
import easyocr

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def has_text_annotation(image_url: str, reader=None) -> bool:
    if not image_url or not image_url.startswith("http"):
        return True
    try:
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if res.status_code != 200 or len(res.content) < 3000:
            return True

        img = Image.open(io.BytesIO(res.content)).convert("RGB")
        img_np = np.array(img)

        if reader is None:
            reader = easyocr.Reader(['en'], gpu=False)
            
        results = reader.readtext(img_np, detail=0)
        detected_words = [w.strip() for w in results if len(w.strip()) > 1 and any(c.isalnum() for c in w)]

        if detected_words:
            print(f"[EasyOCR Engine] ❌ Text Detected in image (...{image_url[-30:]}): {detected_words[:5]}")
            return True
        else:
            print(f"[EasyOCR Engine] ✅ 100% CLEAN PHOTO (NO TEXT) (...{image_url[-30:]})")
            return False
    except Exception as e:
        print(f"[EasyOCR Warning] Error running OCR check: {e}")
        return False

# Listing photos for B0GGHJ1J4L
sample_photos = [
    "https://m.media-amazon.com/images/I/81E5p8uvtWL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71MfShfsWyL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/710HFWtubIL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/817JiwgvYTL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81n5zERXHSL._AC_SL1500_.jpg"
]

print("🔍 Testing EasyOCR Engine on B0GGHJ1J4L Listing Photos...\n")
reader = easyocr.Reader(['en'], gpu=False)
clean_photos = []
for idx, url in enumerate(sample_photos, 1):
    has_txt = has_text_annotation(url, reader=reader)
    if not has_txt:
        clean_photos.append(url)

print(f"\n📊 Summary: Found {len(clean_photos)} clean text-free photos out of {len(sample_photos)} total photos.")
