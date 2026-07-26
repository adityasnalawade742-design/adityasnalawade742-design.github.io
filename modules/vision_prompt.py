import time
from pathlib import Path
from google import genai
from config import GEMINI_API_KEY, NICHE

def generate_cozy_image_prompt(
    product_title: str,
    category: str = "",
    key_features: str = "",
    ref_sheet_path: str = ""
) -> str:
    """
    Uses Gemini Vision API to analyze all angles from the 3-in-1 multi-photo reference sheet (if provided)
    and output a high-precision, distortion-free FLUX AI room scene prompt.
    """
    from PIL import Image
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an elite commercial product photographer and AI vision engineer. "
        "Your goal is to inspect the product (and its multi-angle photos if provided) "
        "and output a precise, distortion-free AI image prompt (under 45 words) for FLUX AI.\n\n"
        "RULES:\n"
        "1. Identify the exact physical object, shape, materials (wood grain, frosted glass, matte ceramic), colors, buttons, and finish.\n"
        "2. DO NOT include technical specs, watts, model numbers, or promotional junk words.\n"
        "3. Describe the exact item sitting naturally inside a cozy ambient room or desk setup.\n"
        "4. Enforce visual terms: '35mm photograph, sharp product focus, realistic materials, warm ambient lighting, cozy room aesthetic, soft bokeh background'.\n"
        "5. Output ONLY the raw prompt string (no commentary, under 45 words)."
    )

    contents = []

    # If 3-in-1 multi-angle reference sheet exists, feed image directly into Gemini Vision
    if ref_sheet_path and Path(ref_sheet_path).exists():
        try:
            print(f"[Vision Prompt] Inspecting 3-in-1 multi-angle reference sheet with Gemini Vision: {ref_sheet_path}")
            ref_img = Image.open(ref_sheet_path)
            contents.append(ref_img)
        except Exception as e:
            print(f"[Vision Prompt] Multi-angle image loading error: {e}")

    prompt_input = f"""
    Product Title: {product_title}
    Category: {category}
    Key Features: {key_features}

    Analyze the physical object from all angles and write a high-precision FLUX AI image prompt.
    """
    contents.append(prompt_input)

    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-2.0-flash-lite"
    ]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config={"system_instruction": system_instruction}
            )
            time.sleep(1)
            result = response.text.strip().replace('"', '').replace("'", "")
            if len(result) > 10:
                print(f"[Vision Prompt] Generated prompt ({model_name}): {result[:70]}...")
                return result
        except Exception:
            time.sleep(1)
            continue

    clean_title = product_title.split("-")[0].split(",")[0].strip()
    return (
        f"A sharp 35mm lifestyle photo of a clean, minimalist {clean_title} on a cozy wooden desk, "
        "warm ambient lighting, soft bokeh background, 8k resolution, crisp focus."
    )

