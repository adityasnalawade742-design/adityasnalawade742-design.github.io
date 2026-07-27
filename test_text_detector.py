import sys
import io
import requests
from PIL import Image
from google import genai
from config import GEMINI_API_KEY

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from google import genai
import os

os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

def photo_has_seller_text(image_url: str) -> bool:
    """
    Uses Gemini Vision to check if an Amazon listing photo contains seller marketing text,
    infographics, dimension labels, promotional badges, or written callouts.
    Returns True if text/infographics are detected, False if the image is 100% clean photo.
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
            "Analyze this e-commerce product image carefully. "
            "Does this image contain ANY seller marketing text, promotional overlays, "
            "infographic badges, dimension labels, numbers, or written text callouts? "
            "Respond ONLY with 'YES' if text/infographics exist, or 'NO' if the image is a 100% clean photo with zero text."
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[img, prompt]
        )
        answer = response.text.strip().upper()
        return "YES" in answer
    except Exception as e:
        print(f"[Text Detector Warning] Error checking image text: {e}")
        return False

# Test on candidate photos for B0GGHJ1J4L
sample_photos = [
    "https://m.media-amazon.com/images/I/81E5p8uvtWL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/71MfShfsWyL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/710HFWtubIL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/817JiwgvYTL._AC_SL1500_.jpg",
    "https://m.media-amazon.com/images/I/81n5zERXHSL._AC_SL1500_.jpg"
]

print("🔍 Testing Gemini Vision Text Detection on Amazon Listing Photos...")
clean_photos = []
for idx, url in enumerate(sample_photos, 1):
    has_text = photo_has_seller_text(url)
    status = "❌ HAS SELLER TEXT / INFOGRAPHICS" if has_text else "✅ 100% CLEAN PHOTO (NO TEXT)"
    print(f"Photo {idx}: {status} -> {url[:60]}...")
    if not has_text:
        clean_photos.append(url)

print(f"\n📊 Summary: Found {len(clean_photos)} clean text-free photos out of {len(sample_photos)} total photos.")
