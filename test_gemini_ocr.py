import sys
import io
import os
import requests
from PIL import Image
from google import genai
from config import GEMINI_API_KEY

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

def has_text_annotation(image_url: str) -> bool:
    """
    Uses Gemini 2.0 Vision AI to inspect an Amazon listing photo for ANY written text,
    letters, numbers, seller badges, dimension labels, or infographic overlays.
    Returns True if text exists, False if the photo is 100% clean.
    """
    if not image_url or not image_url.startswith("http"):
        return True
    try:
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if res.status_code != 200 or len(res.content) < 3000:
            return True

        img = Image.open(io.BytesIO(res.content)).convert("RGB")
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = (
            "Inspect this e-commerce product image carefully. "
            "Does this image contain ANY written text, letters, numbers, seller badges, dimension arrows, or infographic text overlays? "
            "Answer ONLY with 'YES' if text exists anywhere, or 'NO' if the image is a 100% clean photo with zero text."
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[img, prompt]
        )
        ans = response.text.strip().upper()
        has_txt = "YES" in ans
        print(f"[Gemini Vision OCR] Image ...{image_url[-30:]}: {'❌ Text Detected' if has_txt else '✅ 100% Clean'}")
        return has_txt
    except Exception as e:
        print(f"[Gemini Vision OCR Warning] Error checking image text: {e}")
        return False

# Listing photos for B0GGHJ1J4L
sample_photos = [
    "https://m.media-amazon.com/images/I/81E5p8uvtWL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71MfShfsWyL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/710HFWtubIL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/817JiwgvYTL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81n5zERXHSL._AC_SL1500_.jpg"
]

print("🔍 Testing Gemini 2.0 Vision OCR on B0GGHJ1J4L Listing Photos...\n")
clean_photos = []
for idx, url in enumerate(sample_photos, 1):
    has_txt = has_text_annotation(url)
    if not has_txt:
        clean_photos.append(url)

print(f"\n📊 Summary: Found {len(clean_photos)} clean text-free photos out of {len(sample_photos)} total photos.")
