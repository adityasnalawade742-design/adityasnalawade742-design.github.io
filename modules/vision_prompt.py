import time
from pathlib import Path
from google import genai
from config import GEMINI_API_KEY, NICHE

def generate_cozy_image_prompt(
    product_title: str = "",
    category: str = "",
    key_features: str = "",
    ref_sheet_path: str = "",
    is_white_background: bool = False
) -> str:
    """
    Master Luxury Commercial Advertisement Prompt for FLUX AI Image Generation.
    """
    clean_title = product_title.split("-")[0].split(",")[0].strip() if product_title else "Cozy Home Decor Find"
    return (
        f"Transform the uploaded product image into a premium luxury commercial advertisement while preserving the original product. "
        f"Product details: {clean_title} featuring realistic materials, authentic textures, and clean physical geometry. "
        "The uploaded product is the main subject and must remain visually consistent with the reference image. "
        "Preserve its overall design, proportions, colors, materials, texture, branding, and recognizable features. "
        "Enhance the surrounding room background with warm cinematic lighting, soft shadows, realistic reflections, subtle depth of field, and magazine-quality commercial photography. "
        "Leave generous clean negative space for headline, logo, pricing, or promotional text."
    )





