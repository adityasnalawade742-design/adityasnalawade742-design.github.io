import io
import requests
from PIL import Image

def is_lifestyle_photo(image_url: str) -> bool:
    """
    Analyzes an Amazon image URL to detect if it has a real lifestyle background
    (room decor, ambient lighting, wood surfaces) or is a plain white studio cutout.
    Returns True if it's a lifestyle photo, False if it's a plain white cutout.
    """
    if not image_url:
        return False
    
    try:
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
        if res.status_code != 200:
            return False
        
        img = Image.open(io.BytesIO(res.content)).convert('RGB')
        width, height = img.size
        
        # Sample border pixels (top, bottom, left, right edges)
        border_pixels = []
        
        # Top & Bottom edges
        for x in range(0, width, max(1, width // 20)):
            border_pixels.append(img.getpixel((x, 0)))
            border_pixels.append(img.getpixel((x, height - 1)))
            
        # Left & Right edges
        for y in range(0, height, max(1, height // 20)):
            border_pixels.append(img.getpixel((0, y)))
            border_pixels.append(img.getpixel((width - 1, y)))
            
        # Count white/near-white border pixels (R>240, G>240, B>240)
        white_count = sum(1 for r, g, b in border_pixels if r > 240 and g > 240 and b > 240)
        white_ratio = white_count / len(border_pixels)
        
        # If > 60% of the border is pure white, it's a studio cutout (NOT a lifestyle photo)
        is_lifestyle = white_ratio < 0.60
        return is_lifestyle, white_ratio
    except Exception as e:
        print(f"[Image Filter Error] Could not analyze image {image_url[:40]}: {e}")
        return True, 0.0

test_photos = [
    ("https://m.media-amazon.com/images/I/71zjJtLCl5L._AC_SL1500_.jpg", "Sunset Lamp Room Scene"),
    ("https://m.media-amazon.com/images/I/51uN6sj8Q6L._AC_SL1500_.jpg", "Crystal Suncatcher Sunlight Scene"),
    ("https://m.media-amazon.com/images/I/71qCnqRyWHL._AC_SL1500_.jpg", "Mug Warmer Cutout")
]

print("=== TESTING AUTOMATED LIFESTYLE BACKGROUND DETECTOR ===")
for url, label in test_photos:
    is_lifestyle, ratio = is_lifestyle_photo(url)
    status = "LIFESTYLE BACKGROUND DETECTED" if is_lifestyle else "PLAIN WHITE CUTOUT (SKIPPED)"
    print(f"Photo '{label}' -> White Ratio: {ratio:.1%} | Result: {status}")

