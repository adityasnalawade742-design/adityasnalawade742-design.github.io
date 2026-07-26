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
    Uses Gemini Vision API to analyze all angles from the multi-photo reference sheet (if provided)
    and output a high-precision, commercial luxury FLUX AI prompt.
    """
    from PIL import Image
    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an elite commercial product photographer and AI vision engineer. "
        "Inspect the product and output a detailed physical description of the product "
        "(exact physical object, shape, materials like wood grain, frosted glass, matte ceramic, colors, finish, and key features) in under 30 words."
    )

    contents = []

    if ref_sheet_path and Path(ref_sheet_path).exists():
        try:
            print(f"[Vision Prompt] Inspecting reference sheet with Gemini Vision: {ref_sheet_path}")
            ref_img = Image.open(ref_sheet_path)
            contents.append(ref_img)
        except Exception as e:
            print(f"[Vision Prompt] Multi-angle image loading error: {e}")

    prompt_input = f"""
    Product Title: {product_title}
    Category: {category}
    Key Features: {key_features}

    Analyze the physical object and write a 25-word exact description of its visual appearance, materials, and colors.
    """
    contents.append(prompt_input)

    models_to_try = [
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash",
        "gemini-2.0-flash-lite"
    ]

    prod_desc = ""
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
                prod_desc = result
                print(f"[Vision Prompt] Extracted Product Vision Specs ({model_name}): {prod_desc[:70]}...")
                break
        except Exception:
            time.sleep(1)
            continue

    if not prod_desc:
        clean_title = product_title.split("-")[0].split(",")[0].strip()
        prod_desc = f"{clean_title} featuring realistic materials, authentic textures, and clean physical geometry"

    master_commercial_prompt = (
        f"Transform the uploaded product image into a premium luxury commercial advertisement while preserving the original product. "
        f"Product details: {prod_desc}. "
        "The uploaded product is the main subject and must remain visually consistent with the reference image. "
        "Preserve its overall design, proportions, colors, materials, texture, branding, and recognizable features. "
        "Improve realism without redesigning the product. "
        "Replace the plain background with a beautiful lifestyle environment that naturally matches the product category. "
        "Create a clean, elegant, high-end scene using premium materials, sophisticated interior styling, realistic props, natural composition, and tasteful decoration that complements the product without distracting from it. "
        "Use warm cinematic lighting, soft shadows, realistic reflections, global illumination, high dynamic range, subtle depth of field, premium color grading, and magazine-quality commercial photography. "
        "Compose the image like a luxury advertising campaign with the product as the hero object. "
        "Leave generous clean negative space for headline, logo, pricing, or promotional text."
    )

    return master_commercial_prompt


