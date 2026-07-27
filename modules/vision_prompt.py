import time
from pathlib import Path
from google import genai
from config import GEMINI_API_KEY, NICHE

def generate_cozy_image_prompt(
    product_title: str = "",
    category: str = "",
    key_features: str = "",
    ref_sheet_path: str = "",
    is_white_background: bool = True
) -> str:
    """
    DUAL-PROMPT STRATEGY:
      - Prompt 1 (is_white_background=False): For products WITH existing lifestyle room backgrounds.
        Enhances room lighting, depth of field, and atmosphere while keeping existing room scene.
      - Prompt 2 (is_white_background=True): For products WITH NO BACKGROUND (white cutouts / studio photos).
        Synthesizes a brand-new photorealistic 3:4 lifestyle room environment from scratch tailored to the product vibe!
    """
    clean_title = product_title.split("-")[0].split(",")[0].strip() if product_title else "Cozy Home Decor Find"
    title_lower = clean_title.lower()

    if is_white_background:
        # =========================================================================
        # PROMPT STRATEGY 2: Background Synthesis (For White Cutouts / No Background)
        # =========================================================================
        if "vase" in title_lower or "flower" in title_lower:
            room_scene = "a sunlit oak dining table with soft morning rays, dried pampas grass, and sheer linen window curtains"
        elif "board" in title_lower or "memo" in title_lower or "note" in title_lower or "acrylic" in title_lower:
            room_scene = "a cozy warm desk setup with ambient fairy lights, a ceramic coffee mug, aesthetic notebooks, and soft bokeh"
        elif "timer" in title_lower or "hourglass" in title_lower or "clock" in title_lower:
            room_scene = "a luxury dark walnut bookshelf in a cozy library setting with warm glowing reading lamps and vintage books"
        elif "diffuser" in title_lower or "flame" in title_lower or "aroma" in title_lower:
            room_scene = "a modern bedside nightstand in a moody dark-toned room with warm ambient mist glow and soft drop shadows"
        elif "lamp" in title_lower or "light" in title_lower:
            room_scene = "a cozy aesthetic bedside table in a warm bedroom setting with soft golden hour lighting and wall art"
        elif "mirror" in title_lower or "wavy" in title_lower:
            room_scene = "a chic cream vanity setup with delicate perfume bottles, warm sunlight reflections, and soft pastel room decor"
        else:
            room_scene = "a stylish, warm luxury living room side table featuring ambient interior lighting and elegant home styling props"

        return (
            f"The input photo is an isolated product cutout on a plain white studio background featuring '{clean_title}'. "
            f"Synthesize a brand-new, complete 8K photorealistic 3:4 lifestyle room background from scratch: place the product naturally onto {room_scene}. "
            "Integrate the isolated product seamlessly into this new room setting with realistic contact drop shadows, natural surface reflections, and matching ambient light bleeding. "
            "Preserve the main physical product shape, colors, and textures 100% accurately while rendering a high-end Architectural Digest room scene around it. "
            "Leave generous clean negative space at the top for headline text."
        )

    else:
        # =========================================================================
        # PROMPT STRATEGY 1: Lifestyle Room Enhancement (For Existing Room Photos)
        # =========================================================================
        return (
            f"Transform the uploaded product image into a premium luxury commercial advertisement while preserving the original product. "
            f"Product details: {clean_title} featuring realistic materials, authentic textures, and clean physical geometry. "
            "The uploaded product is the main subject and must remain visually consistent with the reference image. "
            "Preserve its overall design, proportions, colors, materials, texture, branding, and recognizable features. "
            "Enhance the surrounding room background with warm cinematic lighting, soft shadows, realistic reflections, subtle depth of field, and magazine-quality commercial photography. "
            "Leave generous clean negative space for headline, logo, pricing, or promotional text."
        )





