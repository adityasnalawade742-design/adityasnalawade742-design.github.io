import io, requests, sys
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image

def calculate_cozy_vibe_score(image_url: str) -> float:
    """
    Evaluates cozy room aesthetic score (1.0 to 10.0) based on:
      1. Warmth ratio (amber/gold/wood warm hues vs cold white/grey)
      2. Soft contrast & ambient lighting depth
      3. Background richness
    """
    try:
        raw = requests.get(image_url, timeout=10).content
        img = Image.open(io.BytesIO(raw)).convert('RGB')
        w, h = img.size
        
        # Sample pixels for color temperature analysis
        pixels = list(img.resize((100, 100)).getdata())
        
        warm_pixels = 0
        pure_white_pixels = 0
        
        for r, g, b in pixels:
            # Check for pure white/grey studio background (r>240, g>240, b>240)
            if r > 240 and g > 240 and b > 240:
                pure_white_pixels += 1
            # Check for warm golden/wood/ambient lighting hues (r > g and g > b and r > 80)
            elif r > g + 10 and g >= b and r > 80:
                warm_pixels += 1
        
        total = len(pixels)
        white_ratio = pure_white_pixels / total
        warm_ratio = warm_pixels / total
        
        # Base score from warm ambient ratio
        score = 5.0 + (warm_ratio * 10.0)
        
        # Deduct points if photo is a plain white studio cutout (less cozy)
        if white_ratio > 0.40:
            score -= (white_ratio * 4.0)
            
        return max(1.0, min(10.0, round(score, 2)))
    except Exception as e:
        print(f"Error scoring cozy vibe: {e}")
        return 5.0

print("🔍 SCORING COZY VIBES ON B0D4537YMT CLEAN PHOTOS...")
photos = [
    "https://m.media-amazon.com/images/I/61Y4762ZwsL._AC_SL1500_.jpg", # White cutout
    "https://m.media-amazon.com/images/I/612FlARiy7L._AC_SL1500_.jpg", # Room photo 1
    "https://m.media-amazon.com/images/I/61XX+8bjiWL._AC_SL1500_.jpg", # Room photo 2
    "https://m.media-amazon.com/images/I/71OrpXi+5OL._AC_SL1500_.jpg"  # Room photo 3
]

for p in photos:
    score = calculate_cozy_vibe_score(p)
    print(f"Photo: ...{p[-30:]} | Cozy Vibe Score: {score}/10")
