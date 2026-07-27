import json
import time
from google import genai
from config import GEMINI_API_KEY, NICHE

def generate_pin_seo_data(product_title: str, price: str = "", category: str = "") -> dict:
    """
    Uses Gemini API to generate Pinterest SEO titles, descriptions, image hooks,
    and board recommendations tailored for maximum search visibility and CTR.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an elite Pinterest SEO Copywriter. "
        "Return ONLY a valid JSON object matching the requested fields, with no markdown codeblocks or extra text."
    )

    prompt = f"""
    Target Niche: {NICHE}
    Amazon Product Title: {product_title}
    Price: {price}
    Category: {category}

    Generate Pinterest SEO metadata for this product. Return JSON with the following keys:
    - "pin_title": A catchy, high-CTR Pinterest title (under 80 chars, with relevant emoji).
    - "image_hook": A 2-4 word short punchy headline for the image overlay (e.g. "White Wavy Vanity Mirror", "Cozy Touch Bird Light").
    - "subtitle_hook": A 3-5 word uppercase tagline customized specifically for this product's unique vibe (e.g. "ELEVATE YOUR VANITY SPACE", "FLAMELESS CANDLE LUXURY", "AESTHETIC BEDROOM GLOW").
    - "badge_hook": A 2-3 word badge customized for this product category (e.g. "VANITY GOALS", "COZY NIGHT VIBES", "ATMOSPHERE FIND").
    - "theme_style": Choose the best matching visual theme from: "floating_cream" (for mirrors, vanity decor, cream/white aesthetic items) or "floating_luxury" (for glowing lamps, candle warmers, diffusers).
    - "description": A 200-300 character SEO-rich Pinterest description with high-volume search phrases naturally included.
    - "suggested_board": Recommended Pinterest Board Name.
    - "keywords": A list of 5 key search terms.
    """

    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-2.0-flash-lite",
        "gemini-flash-latest",
        "gemini-1.5-flash"
    ]


    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "response_mime_type": "application/json"
                }
            )
            time.sleep(1)
            data = json.loads(response.text.strip())
            import re
            for k in ["image_hook", "subtitle_hook", "badge_hook"]:
                if k in data and isinstance(data[k], str):
                    data[k] = re.sub(r'[^\x00-\x7F]+', '', data[k]).strip()
                    # Clean trailing prepositions
                    words = data[k].split()
                    while words and words[-1].lower() in ["for", "with", "and", "in", "on", "of", "by", "the", "a", "an"]:
                        words.pop()
                    data[k] = " ".join(words)

            if data.get("image_hook") and 2 <= len(data["image_hook"].split()) <= 5:
                return data
        except Exception:
            time.sleep(1)
            continue

    # Smart Keyword-based Short Punchy Viral Headline Fallback (2-4 Words)
    title_lower = product_title.lower()
    if "mushroom" in title_lower:
        image_hook = "Aesthetic Mushroom Lamp"
    elif "bird" in title_lower:
        image_hook = "Cute Bird Touch Lamp"
    elif "flower" in title_lower or "lily" in title_lower:
        image_hook = "Lily Of The Valley Glow"
    elif "warmer" in title_lower or "mug" in title_lower:
        image_hook = "Aesthetic Coffee Warmer"
    elif "lamp" in title_lower or "light" in title_lower:
        image_hook = "Cozy Bedside Touch Lamp"
    else:
        words = [w for w in product_title.split() if w.lower() not in ["for", "with", "and", "in", "on", "of", "by", "the", "a", "an", "-", "|"]]
        image_hook = " ".join(words[:3]).title()

    clean_name = image_hook

    return {
        "pin_title": f"Cozy {clean_name} 🕯️",
        "image_hook": clean_name,
        "subtitle_hook": "ELEGANCE THAT SHINES",
        "badge_hook": "AMAZON HOME FIND",
        "description": f"Check out the best lamps for rooms and cozy desk decor. Find {clean_name} for the ultimate aesthetic room setup!",
        "suggested_board": "Cozy Room Decor Ideas",
        "keywords": ["cozy room decor", "aesthetic desk setup", "best lamps for rooms", "room upgrade", "budget decor"]
    }


