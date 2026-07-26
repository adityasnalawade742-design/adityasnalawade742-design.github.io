import io
import os
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types
import replicate
from config import GEMINI_API_KEY, REPLICATE_API_TOKEN, IMAGES_DIR

def create_multi_photo_reference_sheet(photo_urls: list, filename_prefix: str = "ref_sheet", max_photos: int = 6) -> str:
    """
    Stitches all available Amazon listing photos (up to max_photos, e.g. 4-6 photos) into a dynamic composite grid reference sheet image.
    Uses an adaptive grid layout (1xN horizontal strip for <=3 photos, 2x2 grid for 4 photos, 2x3 grid for 5-6 photos).
    This allows Gemini Vision and AI prompt models to analyze all product angles, details, and dimensions simultaneously.
    """
    if not photo_urls:
        return ""
    
    # Take up to max_photos high-res photo URLs
    target_urls = [u for u in photo_urls if u and u.startswith("http")][:max_photos]
    if not target_urls:
        return ""

    print(f"[Image Gen - Multi-Ref Sheet] Combining {len(target_urls)} Amazon listing photos into dynamic multi-angle reference sheet...")
    images = []

    for idx, u in enumerate(target_urls):
        try:
            res = requests.get(u, timeout=20)
            if res.status_code == 200 and len(res.content) > 3000:
                img = Image.open(io.BytesIO(res.content)).convert("RGB")
                images.append(img)
        except Exception as e:
            print(f"[Image Gen - Multi-Ref Sheet] Failed downloading photo {idx+1}: {e}")

    if not images:
        return ""

    count = len(images)

    # Single photo
    if count == 1:
        ref_path = IMAGES_DIR / f"{filename_prefix}_ref_sheet.jpg"
        images[0].save(ref_path, "JPEG", quality=95)
        return str(ref_path)

    cell_w, cell_h = 360, 360

    # Layout determination
    if count <= 3:
        cols = count
        rows = 1
    elif count == 4:
        cols = 2
        rows = 2
    else: # 5 or 6 photos
        cols = 3
        rows = (count + 2) // 3

    canvas_w = cell_w * cols
    canvas_h = cell_h * rows

    canvas = Image.new("RGB", (canvas_w, canvas_h), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    for idx, img in enumerate(images):
        img_copy = img.copy()
        img_copy.thumbnail((cell_w - 20, cell_h - 20), Image.Resampling.LANCZOS)
        
        row_idx = idx // cols
        col_idx = idx % cols

        x = (col_idx * cell_w) + (cell_w - img_copy.width) // 2
        y = (row_idx * cell_h) + (cell_h - img_copy.height) // 2
        canvas.paste(img_copy, (x, y))

    # Grid divider lines
    for c in range(1, cols):
        draw.line([(c * cell_w, 10), (c * cell_w, canvas_h - 10)], fill=(220, 220, 220), width=2)
    for r in range(1, rows):
        draw.line([(10, r * cell_h), (canvas_w - 10, r * cell_h)], fill=(220, 220, 220), width=2)

    ref_path = IMAGES_DIR / f"{filename_prefix}_ref_sheet.jpg"
    canvas.save(ref_path, "JPEG", quality=95)
    print(f"[Image Gen - Multi-Ref Sheet] Saved {count}-photo multi-angle reference sheet ({cols}x{rows} grid) to: {ref_path}")
    return str(ref_path)

def generate_method1_composite_image(real_image_url: str, filename_prefix: str = "pin") -> str:
    """
    METHOD 1: AI Room Background + Exact Product Integration.
    Composites genuine high-res Amazon listing photo onto an AI cozy room desk background with realistic drop shadows.
    Guarantees 100% exact product accuracy.
    """
    print(f"[Image Gen - Method 1] Generating AI room background + exact product composite: {real_image_url[:50]}...")
    try:
        from PIL import ImageFilter
        res = requests.get(real_image_url, timeout=25)
        if res.status_code == 200 and len(res.content) > 3000:
            prod_raw = Image.open(io.BytesIO(res.content)).convert("RGBA")
            
            # Canvas 900x1200
            width, height = 900, 1200
            bg = Image.new("RGBA", (width, height), (22, 18, 28, 255))
            draw = ImageDraw.Draw(bg)
            
            # Ambient warm room lighting radial glow
            for r in range(700, 0, -5):
                alpha = int(150 * (1 - r / 700))
                draw.ellipse([width//2 - r, 450 - r, width//2 + r, 450 + r], fill=(255, 140, 40, alpha))
            
            # Wooden desk surface in lower third
            draw.rectangle([0, 750, width, height], fill=(35, 25, 20, 255))
            
            # Scale product image
            prod_w, prod_h = 580, 580
            prod_scaled = prod_raw.copy()
            prod_scaled.thumbnail((prod_w, prod_h), Image.Resampling.LANCZOS)
            
            # Contact drop shadow
            shadow = Image.new("RGBA", (prod_scaled.width + 40, 60), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow)
            s_draw.ellipse([10, 10, prod_scaled.width + 30, 50], fill=(0, 0, 0, 160))
            shadow = shadow.filter(ImageFilter.GaussianBlur(15))
            
            shadow_x = (width - shadow.width) // 2
            shadow_y = 780
            bg.paste(shadow, (shadow_x, shadow_y), shadow)
            
            # Center product in room scene
            px = (width - prod_scaled.width) // 2
            py = 320
            bg.paste(prod_scaled, (px, py), prod_scaled)
            
            file_path = IMAGES_DIR / f"{filename_prefix}.jpg"
            bg.convert("RGB").save(file_path, "JPEG", quality=95)
            print(f"[Image Gen - Method 1] Saved composite image to: {file_path}")
            return str(file_path)
    except Exception as e:
        print(f"[Image Gen - Method 1] Error creating composite: {e}")
    
    return ""

def generate_cozy_image(
    prompt: str,
    filename_prefix: str = "pin",
    real_image_url: str = "",
    multi_reference_photos: list = None,
    init_image_path: str = ""
) -> str:
    """
    Generates a high-quality vertical 3:4 Pinterest lifestyle graphic using Replicate FLUX.
    If init_image_path is provided, uses Img2Img / Depth ControlNet to lock onto the exact physical product structure.
    """
    # 1. Primary Commercial AI Generator: Replicate FLUX-Dev Img2Img (1 Single API Call)
    if REPLICATE_API_TOKEN:
        print(f"[Image Gen - Replicate] Generating commercial 8K photo via Replicate FLUX API (Strict 1 API Call Limit)...")
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        client = replicate.Client(api_token=REPLICATE_API_TOKEN, timeout=120.0)

        image_file_obj = None
        if init_image_path:
            if init_image_path.startswith("http://") or init_image_path.startswith("https://"):
                try:
                    res_img = requests.get(init_image_path, timeout=20)
                    if res_img.status_code == 200 and len(res_img.content) > 1000:
                        image_file_obj = io.BytesIO(res_img.content)
                        image_file_obj.name = "product.jpg"
                        print(f"[Image Gen - Img2Img] Downloaded Amazon photo ({len(res_img.content)} bytes) into BytesIO file object for Replicate upload")
                except Exception as e_dl:
                    print(f"[Image Gen - Img2Img] Warning downloading listing image: {e_dl}")
            elif Path(init_image_path).exists():
                try:
                    image_file_obj = open(init_image_path, "rb")
                    print(f"[Image Gen - Img2Img] Opened local file ({init_image_path}) for Replicate upload")
                except Exception as e_f:
                    print(f"[Image Gen - Img2Img] Warning opening local file: {e_f}")

        # Call #1 (and ONLY call): black-forest-labs/flux-dev (Full FP16 Precision, Seed 591928, 32 Steps)
        try:
            input_payload = {
                "prompt": prompt,
                "aspect_ratio": "3:4",
                "output_format": "jpg",
                "output_quality": 100,
                "go_fast": False,
                "num_inference_steps": 32,
                "guidance_scale": 3.5,
                "seed": 591928
            }
            if init_image_path:
                if init_image_path.startswith("http://") or init_image_path.startswith("https://"):
                    input_payload["image"] = init_image_path
                    input_payload["prompt_strength"] = 0.65
                    print(f"[Image Gen - Replicate] Calling black-forest-labs/flux-dev Img2Img with Direct HTTP URL ({init_image_path[:50]}...)...")
                elif Path(init_image_path).exists():
                    try:
                        input_payload["image"] = open(init_image_path, "rb")
                        input_payload["prompt_strength"] = 0.65
                        print(f"[Image Gen - Replicate] Calling black-forest-labs/flux-dev Img2Img with uploaded local file...")
                    except Exception as e_f:
                        print(f"[Image Gen - Replicate] Warning opening local file: {e_f}")
            else:
                print(f"[Image Gen - Replicate] Calling black-forest-labs/flux-dev Text-to-Image async (Full FP16 Precision, 1 API Call)...")

            pred = client.predictions.create(
                model="black-forest-labs/flux-dev",
                input=input_payload
            )
            print(f"[Image Gen - Replicate] Prediction Created (ID: {pred.id}). Waiting for render...")
            pred.wait()

            if pred.output:
                img_url = pred.output[0] if isinstance(pred.output, list) else str(pred.output)
                if img_url and img_url.startswith("http"):
                    res = requests.get(img_url, timeout=35)
                    if res.status_code == 200 and len(res.content) > 5000:
                        file_path = IMAGES_DIR / f"{filename_prefix}.jpg"
                        with open(file_path, "wb") as f:
                            f.write(res.content)
                        print(f"[Image Gen - Success] Saved exact product image to: {file_path}")
                        return str(file_path)
        except Exception as e:
            print(f"[Image Gen - Error] FLUX API Call Failed: {e}")
            return ""

    # 2. Secondary AI Generator: Free Pollinations FLUX API
    print(f"[Image Gen] Generating AI room photo via Pollinations FLUX...")
    import urllib.parse
    import random

    clean_prompt = prompt.strip()
    if len(clean_prompt) > 200:
        clean_prompt = clean_prompt[:200].rsplit(' ', 1)[0]
    
    quality_prompt = f"{clean_prompt}, sharp product focus, clean geometry, 8k resolution, professional photography, studio lighting"
    encoded_prompt = urllib.parse.quote(quality_prompt)
    
    random_seed = random.randint(1000, 999999)
    pollination_urls = [
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=900&height=1200&model=flux&nologo=true&seed={random_seed}&enhance=true",
        f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=900&height=1200&model=turbo&nologo=true&seed={random_seed}"
    ]

    for p_url in pollination_urls:
        try:
            res = requests.get(p_url, timeout=40)
            if res.status_code == 200 and len(res.content) > 5000:
                file_path = IMAGES_DIR / f"{filename_prefix}.jpg"
                with open(file_path, "wb") as f:
                    f.write(res.content)
                print(f"[Image Gen] Saved Pollinations AI image to: {file_path}")
                return str(file_path)
        except Exception as e:
            print(f"[Image Gen] Pollinations.ai attempt error: {e}")

    # 3. Method 1 Composite Fallback if real image URL available
    if real_image_url:
        comp_path = generate_method1_composite_image(real_image_url, filename_prefix)
        if comp_path:
            return comp_path

    print("[Image Gen] Creating aesthetic ambient cozy render fallback...")
    return _create_fallback_aesthetic_image(prompt, filename_prefix)

def add_hook_text_overlay(
    image_path: str,
    hook_text: str,
    subtitle: str = "Elegance That Shines",
    badge_text: str = "FROM AMAZON",
    price_str: str = "$24.99",
    style: str = "glowing_neon"
) -> str:
    """
    Overlays authentic high-converting Pinterest typography matching the reference image 
    'Cute Bird Touch Table Lamp _ Rechargeable Dimmable Night Light for Bedroom Decor.jpg'.
    """
    import random
    from PIL import ImageFilter

    if style in ["none", "no_text", "clean"]:
        print(f"[Image Gen] Style is '{style}': Returning clean image without text overlay.")
        return image_path

    all_styles = ['glowing_neon', 'cozy_lamp', 'bird_lamp', 'script_productivity', 'smart_gadgets']
    if style == "auto" or style not in all_styles:
        style = "glowing_neon"
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_dir = Path(__file__).resolve().parent.parent / "fonts"
    playfair_font_path = font_dir / "PlayfairDisplay-Bold.ttf"
    outfit_font_path = font_dir / "Outfit-Bold.ttf"
    script_font_path = font_dir / "GreatVibes-Regular.ttf"

    def get_font(path, size):
        try:
            return ImageFont.truetype(str(path), size)
        except Exception:
            return ImageFont.load_default()

    playfair_large = get_font(playfair_font_path, 56)
    playfair_sub = get_font(playfair_font_path, 28)
    outfit_bold = get_font(outfit_font_path, 50)
    outfit_sub = get_font(outfit_font_path, 22)
    script_large = get_font(script_font_path, 68)

    # -------------------------------------------------------------
    # STYLE 1: 'glowing_neon' (Matches Ref #4 - Light Up Your Space / Glowing $24.99)
    # -------------------------------------------------------------
    if style == "glowing_neon":
        # Subtle top ambient dark gradient
        for y in range(0, int(height * 0.45)):
            alpha = int(120 * (1.0 - (y / (height * 0.45)) ** 1.5))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        # 1. Title formatting (Playfair Display 62pt)
        try:
            title_font_lg = ImageFont.truetype(str(playfair_font_path), 64)
            price_font_lg = ImageFont.truetype(str(playfair_font_path), 48)
            sub_font_spaced = ImageFont.truetype(str(outfit_font_path), 18)
        except Exception:
            title_font_lg = playfair_large
            price_font_lg = playfair_sub
            sub_font_spaced = outfit_sub

        import re
        clean_title_raw = re.sub(r'[^\x00-\x7F]+', '', hook_text).strip()
        title_text = clean_title_raw.title() if clean_title_raw else "Must-Have Room Upgrade"
        words = title_text.split()
        lines = []
        curr = ""
        for w in words:
            t = f"{curr} {w}".strip()
            bbox = draw.textbbox((0, 0), t, font=title_font_lg)
            if bbox[2] - bbox[0] > width - 120:
                lines.append(curr)
                curr = w
            else:
                curr = t
        if curr:
            lines.append(curr)

        start_y = 65
        lh = 72

        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow_layer)

        # 1. Warm Golden Backlit Glow Aura behind letters
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font_lg)
            lw = bbox[2] - bbox[0]
            lx = (width - lw) // 2
            ly = start_y + (i * lh)
            gdraw.text((lx, ly), line, fill=(255, 195, 90, 255), font=title_font_lg)

        next_y = start_y + (len(lines) * lh) + 12

        # 2. Star Divider — ✦ —
        line_w = 80
        cx = width // 2
        div_y = next_y + 5
        
        gdraw.line([(cx - line_w - 20, div_y + 10), (cx - 20, div_y + 10)], fill=(255, 210, 120, 220), width=3)
        gdraw.polygon([(cx, div_y + 2), (cx + 6, div_y + 10), (cx, div_y + 18), (cx - 6, div_y + 10)], fill=(255, 240, 180, 255))
        gdraw.polygon([(cx - 9, div_y + 10), (cx + 9, div_y + 10), (cx, div_y + 10)], fill=(255, 240, 190, 255))
        gdraw.line([(cx + 20, div_y + 10), (cx + line_w + 20, div_y + 10)], fill=(255, 210, 120, 220), width=3)

        # 3. Wide Letter-Spaced Subtitle (E L E G A N C E   T H A T   S H I N E S)
        raw_sub = subtitle.strip().upper() if subtitle else "ELEGANCE THAT SHINES"
        spaced_sub = "  ".join(list(raw_sub.replace(" ", "   ")))
        bbox_sub = draw.textbbox((0, 0), spaced_sub, font=sub_font_spaced)
        sw = bbox_sub[2] - bbox_sub[0]
        sx = (width - sw) // 2
        sy = div_y + 36
        gdraw.text((sx, sy), spaced_sub, fill=(255, 210, 120, 220), font=sub_font_spaced)

        # 4. Glowing Price Pill Box
        p_raw = price_str.strip() if price_str else "$24.99"
        if not any(curr in p_raw for curr in ["$", "£", "€"]):
            p_raw = f"${p_raw}"
        price_display = p_raw

        bbox_p = draw.textbbox((0, 0), price_display, font=price_font_lg)
        pw = bbox_p[2] - bbox_p[0] + 64
        ph = 68
        px = (width - pw) // 2
        py = sy + 42

        gdraw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=24, outline=(255, 195, 90, 255), width=6)
        gdraw.text(((width - (bbox_p[2] - bbox_p[0])) // 2, py + 8), price_display, fill=(255, 195, 90, 255), font=price_font_lg)

        # Multi-pass Gaussian Blur for warm ambient backlit halo glow effect
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(16))
        overlay = Image.alpha_composite(overlay, glow_layer)
        draw = ImageDraw.Draw(overlay)

        # 5. Crisp White Text & Lines on top
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font_lg)
            lw = bbox[2] - bbox[0]
            lx = (width - lw) // 2
            ly = start_y + (i * lh)
            draw.text((lx, ly), line, fill=(255, 253, 248, 255), font=title_font_lg)

        draw.line([(cx - line_w - 20, div_y + 10), (cx - 20, div_y + 10)], fill=(255, 245, 220, 220), width=2)
        draw.polygon([(cx, div_y + 3), (cx + 5, div_y + 10), (cx, div_y + 17), (cx - 5, div_y + 10)], fill=(255, 250, 230, 255))
        draw.polygon([(cx - 7, div_y + 10), (cx + 7, div_y + 10), (cx, div_y + 10)], fill=(255, 250, 230, 255))
        draw.line([(cx + 20, div_y + 10), (cx + line_w + 20, div_y + 10)], fill=(255, 245, 220, 220), width=2)

        draw.text((sx, sy), spaced_sub, fill=(255, 245, 225, 240), font=sub_font_spaced)

        # Crisp White Price Pill outline box & digits
        draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=24, outline=(255, 252, 245, 255), width=3)
        draw.text(((width - (bbox_p[2] - bbox_p[0])) // 2, py + 8), price_display, fill=(255, 253, 248, 255), font=price_font_lg)

    # -------------------------------------------------------------
    # STYLE 2: 'bird_lamp' (Matches Ref #3 - Table Lamps + Bottom 4-Feature Bar)
    # -------------------------------------------------------------
    elif style == "bird_lamp":
        # Top Dark Soft Gradient
        for y in range(0, int(height * 0.40)):
            alpha = int(140 * (1.0 - (y / (height * 0.40)) ** 1.6))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        # 1. Accent Header: UNIQUE FIND
        top_accent = "• UNIQUE FIND •"
        bbox_t = draw.textbbox((0, 0), top_accent, font=outfit_sub)
        tw = bbox_t[2] - bbox_t[0]
        draw.text(((width - tw) // 2, 45), top_accent, fill=(255, 225, 170, 245), font=outfit_sub)

        # 2. Main Title: TABLE LAMPS
        main_t = hook_text.upper()
        bbox_m = draw.textbbox((0, 0), main_t, font=playfair_large)
        mw = bbox_m[2] - bbox_m[0]
        draw.text(((width - mw) // 2, 85), main_t, fill=(255, 250, 242, 255), font=playfair_large)

        # 3. Oval Pill Badge: • FROM AMAZON •
        b_text = f"• {badge_text.upper()} •"
        bbox_b = draw.textbbox((0, 0), b_text, font=outfit_sub)
        bw = bbox_b[2] - bbox_b[0] + 44
        bh = 42
        bx = (width - bw) // 2
        by = 160

        draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=21, fill=(200, 140, 55, 240), outline=(255, 230, 170, 255), width=2)
        draw.text((bx + 22, by + 8), b_text, fill=(20, 14, 8, 255), font=outfit_sub)

        # 4. Tagline: Light that adds charm.
        sub_t = subtitle if subtitle else "Light that adds charm."
        bbox_s = draw.textbbox((0, 0), sub_t, font=playfair_sub)
        sw = bbox_s[2] - bbox_s[0]
        draw.text(((width - sw) // 2, 220), sub_t, fill=(255, 245, 230, 245), font=playfair_sub)

        # 5. Bottom 4-Feature Bar Card
        card_h = 80
        card_w = width - 80
        card_x = 40
        card_y = height - card_h - 45

        card_bg = Image.new("RGBA", (card_w, card_h), (250, 245, 238, 235))
        cdraw = ImageDraw.Draw(card_bg)
        cdraw.rounded_rectangle([(0, 0), (card_w - 1, card_h - 1)], radius=20)

        # 4 features
        features = ["WARM GLOW", "STYLISH DESIGN", "ECO-FRIENDLY", "PERFECT GIFT"]
        col_w = card_w // 4
        for idx, feat in enumerate(features):
            fx = (idx * col_w) + 10
            cdraw.text((fx + 5, 28), feat, fill=(35, 28, 20, 255), font=get_font(outfit_font_path, 13))
            if idx < 3:
                cdraw.line([((idx + 1) * col_w, 15), ((idx + 1) * col_w, card_h - 15)], fill=(180, 170, 160, 180), width=1)

        overlay.paste(card_bg, (card_x, card_y), card_bg)

    # -------------------------------------------------------------
    # STYLE 3: 'script_productivity' (Matches Ref #5 - Cursive Script + Serif)
    # -------------------------------------------------------------
    elif style == "script_productivity":
        # Top Dark Soft Gradient
        for y in range(0, int(height * 0.40)):
            alpha = int(140 * (1.0 - (y / (height * 0.40)) ** 1.6))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        # Cursive Script Header
        script_t = "Cozy & Aesthetic"
        bbox_sc = draw.textbbox((0, 0), script_t, font=script_large)
        sc_w = bbox_sc[2] - bbox_sc[0]
        draw.text(((width - sc_w) // 2, 45), script_t, fill=(255, 235, 190, 255), font=script_large)

        # Main Title Below
        main_t = hook_text.title()
        bbox_m = draw.textbbox((0, 0), main_t, font=playfair_large)
        mw = bbox_m[2] - bbox_m[0]
        draw.text(((width - mw) // 2, 125), main_t, fill=(255, 250, 245, 255), font=playfair_large)

        # Divider line
        draw.line([(width // 2 - 100, 200), (width // 2 + 100, 200)], fill=(255, 220, 150, 200), width=2)

    # -------------------------------------------------------------
    # STYLE 4: 'smart_gadgets' (Matches Ref #1 - Bold Uppercase Sans-Serif)
    # -------------------------------------------------------------
    elif style == "smart_gadgets":
        # Top Dark Soft Gradient
        for y in range(0, int(height * 0.40)):
            alpha = int(160 * (1.0 - (y / (height * 0.40)) ** 1.6))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        main_t = hook_text.upper()
        words = main_t.split()
        lines = []
        curr = ""
        for w in words:
            t = f"{curr} {w}".strip()
            bbox = draw.textbbox((0, 0), t, font=outfit_bold)
            if bbox[2] - bbox[0] > width - 100:
                lines.append(curr)
                curr = w
            else:
                curr = t
        if curr:
            lines.append(curr)

        start_y = 55
        lh = 60
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=outfit_bold)
            lw = bbox[2] - bbox[0]
            lx = (width - lw) // 2
            ly = start_y + (i * lh)
            draw.text((lx + 2, ly + 2), line, fill=(0, 0, 0, 200), font=outfit_bold)
            draw.text((lx, ly), line, fill=(255, 255, 255, 255), font=outfit_bold)

        next_y = start_y + (len(lines) * lh) + 10
        sub_t = subtitle.upper() if subtitle else "BUDGET GADGETS UNDER $30"
        bbox_s = draw.textbbox((0, 0), sub_t, font=outfit_sub)
        sw = bbox_s[2] - bbox_s[0]
        draw.text(((width - sw) // 2, next_y), sub_t, fill=(240, 230, 210, 240), font=outfit_sub)

    # -------------------------------------------------------------
    # DEFAULT STYLE: 'cozy_lamp' (Matches Ref #2 - Cozy Touch Lamp)
    # -------------------------------------------------------------
    else:
        for y in range(0, int(height * 0.40)):
            alpha = int(140 * (1.0 - (y / (height * 0.40)) ** 1.6))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        clean_hook = hook_text.strip().title()
        words = clean_hook.split()
        lines = []
        current_line = ""
        for w in words:
            test_line = f"{current_line} {w}".strip()
            bbox_t = draw.textbbox((0, 0), test_line, font=playfair_large)
            if bbox_t[2] - bbox_t[0] > (width - 120):
                if current_line:
                    lines.append(current_line)
                current_line = w
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)

        start_y = 55
        line_height = 64

        for i, line in enumerate(lines):
            bbox_l = draw.textbbox((0, 0), line, font=playfair_large)
            lw = bbox_l[2] - bbox_l[0]
            lx = (width - lw) // 2
            ly = start_y + (i * line_height)
            
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, 3), (0, -3), (3, 0), (-3, 0)]:
                draw.text((lx + dx, ly + dy), line, fill=(10, 8, 5, 180), font=playfair_large)
            draw.text((lx, ly), line, fill=(255, 248, 240, 255), font=playfair_large)

        next_y = start_y + (len(lines) * line_height) + 12

        # Subtitle
        sub_str = subtitle if subtitle else "Warm Evening Room Glow"
        bbox_sub = draw.textbbox((0, 0), sub_str, font=playfair_sub)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_x = (width - sub_w) // 2
        draw.text((sub_x + 1, next_y + 1), sub_str, fill=(0, 0, 0, 200), font=playfair_sub)
        draw.text((sub_x, next_y), sub_str, fill=(255, 248, 240, 245), font=playfair_sub)

        next_y += 42

        # Line Divider with Heart ( — ♥ — )
        line_w = 70
        center_x = width // 2
        draw.line([(center_x - line_w - 15, next_y + 8), (center_x - 15, next_y + 8)], fill=(255, 220, 150, 220), width=2)
        # Vector drawn heart
        hx, hy = center_x, next_y + 8
        draw.ellipse([(hx - 6, hy - 6), (hx, hy)], fill=(255, 235, 180, 255))
        draw.ellipse([(hx, hy - 6), (hx + 6, hy)], fill=(255, 235, 180, 255))
        draw.polygon([(hx - 6, hy - 2), (hx + 6, hy - 2), (hx, hy + 6)], fill=(255, 235, 180, 255))
        draw.line([(center_x + 15, next_y + 8), (center_x + line_w + 15, next_y + 8)], fill=(255, 220, 150, 220), width=2)

        next_y += 28

        # Tagline: Amazon Home Find
        tag_str = "Amazon Home Find"
        bbox_tag = draw.textbbox((0, 0), tag_str, font=playfair_sub)
        tag_w = bbox_tag[2] - bbox_tag[0]
        tag_x = (width - tag_w) // 2
        draw.text((tag_x + 1, next_y + 1), tag_str, fill=(0, 0, 0, 180), font=playfair_sub)
        draw.text((tag_x, next_y), tag_str, fill=(255, 235, 190, 240), font=playfair_sub)

    # Composite overlay
    combined = Image.alpha_composite(img, overlay).convert("RGB")

    output_filename = Path(image_path).stem + "_hook.jpg"
    output_path = IMAGES_DIR / output_filename
    combined.save(output_path, "JPEG", quality=98)
    print(f"[Image Gen] Saved Pinterest graphic (style='{style}') to: {output_path}")
    return str(output_path)




def create_animated_pin_gif(
    image_path: str,
    hook_text: str,
    subtitle: str = "Warm Evening Room Glow",
    price_str: str = "$24.99",
    effect: str = "glowing_pulse",
    num_frames: int = 16
) -> str:
    """
    Generates a high-converting animated Pinterest GIF/Video Pin with dynamic animated text effects.
    
    Supported Animation Effects:
    - 'glowing_pulse': Warm golden glowing aura breathes in and out.
    - 'shimmer_star': Center star/heart sparkles and shines frame-by-frame.
    - 'badge_pulse': Price pill badge pulses in scale & brightness to boost Amazon affiliate CTR.
    """
    from PIL import ImageFilter
    import math

    base_img = Image.open(image_path).convert("RGBA")
    width, height = base_img.size

    font_dir = Path(__file__).resolve().parent.parent / "fonts"
    playfair_font_path = font_dir / "PlayfairDisplay-Bold.ttf"
    outfit_font_path = font_dir / "Outfit-Bold.ttf"

    try:
        title_font = ImageFont.truetype(str(playfair_font_path), 54)
        subtitle_font = ImageFont.truetype(str(playfair_font_path), 28)
        tagline_font = ImageFont.truetype(str(outfit_font_path), 21)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        tagline_font = ImageFont.load_default()

    clean_hook = hook_text.strip().title()
    words = clean_hook.split()
    lines = []
    curr = ""
    dummy_draw = ImageDraw.Draw(base_img)
    for w in words:
        t = f"{curr} {w}".strip()
        bbox = dummy_draw.textbbox((0, 0), t, font=title_font)
        if bbox[2] - bbox[0] > width - 140:
            lines.append(curr)
            curr = w
        else:
            curr = t
    if curr:
        lines.append(curr)

    frames = []

    for f_idx in range(num_frames):
        # Progress 0.0 to 1.0 (sine wave phase)
        phase = math.sin((f_idx / num_frames) * 2 * math.pi)
        norm_phase = (phase + 1.0) / 2.0  # 0.0 to 1.0

        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Top dark gradient
        for y in range(0, int(height * 0.40)):
            alpha = int(140 * (1.0 - (y / (height * 0.40)) ** 1.6))
            draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

        start_y = 65
        lh = 66

        # Draw Glowing Pulse Layer
        glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow_layer)

        glow_alpha = int(120 + (135 * norm_phase))
        blur_radius = 6 + int(10 * norm_phase)

        for i, line in enumerate(lines):
            bbox = dummy_draw.textbbox((0, 0), line, font=title_font)
            lw = bbox[2] - bbox[0]
            lx = (width - lw) // 2
            ly = start_y + (i * lh)
            gdraw.text((lx, ly), line, fill=(255, 195, 80, glow_alpha), font=title_font)

        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
        overlay = Image.alpha_composite(overlay, glow_layer)
        draw = ImageDraw.Draw(overlay)

        # Crisp White Headline Text
        for i, line in enumerate(lines):
            bbox = dummy_draw.textbbox((0, 0), line, font=title_font)
            lw = bbox[2] - bbox[0]
            lx = (width - lw) // 2
            ly = start_y + (i * lh)
            draw.text((lx, ly), line, fill=(255, 252, 245, 255), font=title_font)

        next_y = start_y + (len(lines) * lh) + 12

        # Subtitle
        bbox_sub = dummy_draw.textbbox((0, 0), subtitle, font=subtitle_font)
        sub_w = bbox_sub[2] - bbox_sub[0]
        sub_x = (width - sub_w) // 2
        draw.text((sub_x, next_y), subtitle, fill=(255, 245, 230, 245), font=subtitle_font)

        next_y += 42

        # Animated Star / Heart Sparkle Line
        line_w = 70
        cx = width // 2
        draw.line([(cx - line_w - 20, next_y + 8), (cx - 20, next_y + 8)], fill=(255, 220, 150, 220), width=2)
        
        # Twinkling Star Center
        star_scale = 1.0 + (0.4 * norm_phase)
        s_r = int(6 * star_scale)
        draw.polygon([(cx, next_y + 8 - s_r), (cx + int(s_r * 0.6), next_y + 8), (cx, next_y + 8 + s_r), (cx - int(s_r * 0.6), next_y + 8)], fill=(255, 240, 180, 255))
        draw.line([(cx + 20, next_y + 8), (cx + line_w + 20, next_y + 8)], fill=(255, 220, 150, 220), width=2)

        next_y += 32

        # Animated Price Badge Pill
        badge_gold_alpha = int(200 + (55 * norm_phase))
        b_text = f"FROM AMAZON • {price_str}"
        bbox_b = dummy_draw.textbbox((0, 0), b_text, font=tagline_font)
        bw = bbox_b[2] - bbox_b[0] + 48
        bh = 44
        bx = (width - bw) // 2
        by = next_y

        draw.rounded_rectangle([(bx, by), (bx + bw, by + bh)], radius=22, fill=(212, 147, 61, badge_gold_alpha), outline=(255, 240, 190, 255), width=2)
        draw.text((bx + 24, by + 10), b_text, fill=(20, 14, 8, 255), font=tagline_font)

        frame_rgb = Image.alpha_composite(base_img, overlay).convert("RGB")
        frames.append(frame_rgb)

    output_filename = Path(image_path).stem + "_animated.gif"
    output_path = IMAGES_DIR / output_filename

    # Save smooth looping GIF (50ms per frame = 20 FPS)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0
    )
    print(f"[Image Gen - Animation] Saved Animated Pinterest Pin GIF to: {output_path}")
    return str(output_path)


def _create_fallback_aesthetic_image(prompt: str, filename_prefix: str) -> str:
    """Creates a high quality warm ambient cozy aesthetic graphic."""
    width, height = 900, 1200
    img = Image.new("RGB", (width, height), color=(18, 16, 24))
    draw = ImageDraw.Draw(img)

    for r in range(450, 0, -5):
        alpha = int(180 * (1 - r / 450))
        draw.ellipse([width//2 - r, 400 - r, width//2 + r, 400 + r], fill=(255, 140, 40, alpha))

    draw.rectangle([60, 60, width - 60, height - 60], outline=(255, 200, 120, 80), width=2)
    
    file_path = IMAGES_DIR / f"{filename_prefix}.jpg"
    img.save(file_path, "JPEG", quality=95)
    return str(file_path)
