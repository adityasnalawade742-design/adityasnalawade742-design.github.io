import time
from pathlib import Path
from google import genai
from config import GEMINI_API_KEY, NICHE

def generate_cozy_image_prompt(
    product_title: str = "",
    category: str = "",
    key_features: str = "",
    ref_sheet_path: str = ""
) -> str:
    """
    Returns the exact 100% unmodified master luxury commercial advertisement prompt provided by the user.
    """
    return (
        "Transform the uploaded product image into a premium luxury commercial advertisement while preserving the original product. "
        "The uploaded product is the main subject and must remain visually consistent with the reference image. "
        "Preserve its overall design, proportions, colors, materials, texture, branding, and recognizable features. "
        "Improve realism without redesigning the product. "
        "Replace the plain background with a beautiful lifestyle environment that naturally matches the product category. "
        "Create a clean, elegant, high-end scene using premium materials, sophisticated interior styling, realistic props, natural composition, and tasteful decoration that complements the product without distracting from it. "
        "Use warm cinematic lighting, soft shadows, realistic reflections, global illumination, high dynamic range, subtle depth of field, premium color grading, and magazine-quality commercial photography. "
        "Compose the image like a luxury advertising campaign with the product as the hero object. "
        "Leave generous clean negative space for headline, logo, pricing, or promotional text."
    )



