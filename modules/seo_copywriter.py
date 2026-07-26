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
    - "image_hook": A 3-6 word short punchy phrase for image text overlay (e.g. "Best Desk Light Under $30 🌙").
    - "description": A 200-300 character SEO-rich Pinterest description with high-volume search phrases naturally included (e.g. "best lamps for rooms", "cozy desk setup", "aesthetic bedroom decor", "budget room finds").
    - "suggested_board": Recommended Pinterest Board Name (e.g. "Cozy Room Decor Ideas").
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
            time.sleep(2)
            data = json.loads(response.text.strip())
            import re
            if "image_hook" in data:
                data["image_hook"] = re.sub(r'[^\x00-\x7F]+', '', data["image_hook"]).strip()
            return data
        except Exception as e:
            time.sleep(2)
            continue

    return {
        "pin_title": f"Cozy {product_title[:50]} 🕯️",
        "image_hook": "Must-Have Room Upgrade 🌙",
        "description": f"Check out the best lamps for rooms and cozy desk decor. Find {product_title} for the ultimate aesthetic room setup!",
        "suggested_board": "Cozy Room Decor Ideas",
        "keywords": ["cozy room decor", "aesthetic desk setup", "best lamps for rooms", "room upgrade", "budget decor"]
    }
