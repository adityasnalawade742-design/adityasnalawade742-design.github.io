import os
import sys
import time
import base64
import json
import re
import requests
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except Exception as e_import:
    PLAYWRIGHT_AVAILABLE = False
    sync_playwright = None

from PIL import Image, ImageDraw, ImageFont

def analyze_tag_and_room_with_gemini(room_image_path: str, tag_image_path: str) -> dict:
    """
    Feeds BOTH the room photo AND the custom price tag PNG to Gemini 2.0 Flash Vision!
    Gemini inspects both images simultaneously and dynamically determines exact tag position,
    rotation degree, scale, price font family, font size, text color, and vertical offsets.
    """
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.startswith("AQ."):
        return None

    try:
        with open(room_image_path, "rb") as f:
            room_b64 = base64.b64encode(f.read()).decode("utf-8")
        with open(tag_image_path, "rb") as f:
            tag_b64 = base64.b64encode(f.read()).decode("utf-8")

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        prompt = """
        You are a World-Class Graphic Designer & Pinterest Art Director.
        You are given two images:
        - Image 1: A 3:4 room decor photo.
        - Image 2: A custom price tag graphic PNG.

        Analyze both images carefully. Recommend the exact positioning, rotation, scale, font family, font size, and text color to place the price tag and numbers onto the room photo so it looks 100% natural, premium, and professional.

        Return ONLY a raw JSON object with these exact keys:
        1. "tag_position": "bottom_meta" | "top_right" | "bottom_right" | "top_left"
        2. "rotation_degrees": Integer between -15 and 15 (e.g. -6, -8, 4, 0)
        3. "tag_scale": "240px" | "260px" | "280px" | "300px"
        4. "price_font": "Outfit" | "Cormorant Garamond" | "Playfair Display"
        5. "price_font_size": "44px" | "48px" | "52px"
        6. "price_text_color": Hex color code for best high contrast readability (e.g. "#111827", "#1a0f00", "#0f172a")
        7. "vertical_offset_px": Integer offset between -20 and 20
        """

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": room_b64}},
                    {"inline_data": {"mime_type": "image/png", "data": tag_b64}}
                ]
            }]
        }
        res = requests.post(url, json=payload, timeout=12)
        if res.status_code == 200:
            data = res.json()
            raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
            raw_text = re.sub(r"^```json\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
            parsed = json.loads(raw_text)
            print(f"[Gemini Dual-Image Art Director] 🎨 Recommendation: Position={parsed.get('tag_position')}, Rotation={parsed.get('rotation_degrees')}deg, Scale={parsed.get('tag_scale')}, Font={parsed.get('price_font')}, Color={parsed.get('price_text_color')}")
            return parsed
    except Exception as e:
        print(f"[Gemini Dual-Image Art Director] ⚠️ Fallback: {e}")
    return None


def detect_image_luminance(image_path: str) -> dict:
    """
    Calculates exact RGB luminance of top 25% and bottom 25% regions.
    If image is already dark/medium, applies ZERO dimming (0% opacity).
    If image region is blindingly bright, applies ultra-subtle 0.25 - 0.30 opacity at reduced height (18%).
    """
    try:
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        
        top_crop = img.crop((0, 0, w, int(h * 0.25)))
        bot_crop = img.crop((0, int(h * 0.75), w, h))
        
        def calc_lum(crop_img):
            stat = crop_img.resize((50, 50))
            pixels = list(stat.getdata())
            lums = [0.299 * r + 0.587 * g + 0.114 * b for r, g, b in pixels]
        top_lum = sum(top_crop.getdata()) / float(top_crop.size[0] * top_crop.size[1])
        bot_lum = sum(bot_crop.getdata()) / float(bot_crop.size[0] * bot_crop.size[1])
        
        # High-contrast dimming for bright glowing lamps & room lights
        top_scrim_opacity = 0.55 if top_lum > 70 else 0.35
        bot_scrim_opacity = 0.65 if bot_lum > 70 else 0.45
        
        print(f"[Smart Brightness Engine] ☀️ Luminance Analysis: Top={top_lum:.1f} (Opacity={top_scrim_opacity}), Bottom={bot_lum:.1f} (Opacity={bot_scrim_opacity})")
        return {
            "top_opacity": top_scrim_opacity,
            "bot_opacity": bot_scrim_opacity,
            "top_height": "38%",
            "bot_height": "28%"
        }
    except Exception as e:
        return {"top_opacity": 0.55, "bot_opacity": 0.65, "top_height": "38%", "bot_height": "28%"}

def render_pillow_fallback(image_path: str, headline: str, subtitle: str, badge_text: str, price_str: str, output_path: str) -> str:

    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize((1200, 1600), Image.Resampling.LANCZOS)
        
        scrim = Image.new("RGBA", (1200, 1600), (0, 0, 0, 0))
        draw_scrim = ImageDraw.Draw(scrim)
        for y in range(500):
            alpha = int(210 * ((500 - y) / 500) ** 1.5)
            draw_scrim.line([(0, y), (1200, y)], fill=(12, 10, 18, alpha))
        for y in range(1250, 1600):
            alpha = int(210 * ((y - 1250) / 350) ** 1.5)
            draw_scrim.line([(0, y), (1250, y)], fill=(12, 10, 18, alpha))
            
        img = Image.alpha_composite(img, scrim)
        draw = ImageDraw.Draw(img)

        try:
            font_headline = ImageFont.truetype("arial.ttf", 56)
            font_sub = ImageFont.truetype("arial.ttf", 30)
            font_badge = ImageFont.truetype("arialbd.ttf", 26)
            font_price = ImageFont.truetype("arialbd.ttf", 38)
        except Exception:
            font_headline = font_sub = font_badge = font_price = ImageFont.load_default()

        # Top Badge
        draw.rounded_rectangle([60, 60, 420, 116], radius=28, fill=(251, 133, 0, 220), outline=(255, 255, 255, 255), width=2)
        draw.text((80, 74), f"✨ {badge_text.upper()[:22]}", fill=(255, 255, 255), font=font_badge)

        # Price Pill Top Right
        draw.rounded_rectangle([940, 60, 1140, 124], radius=32, fill=(251, 133, 0, 240), outline=(255, 255, 255, 255), width=3)
        draw.text((965, 73), price_str, fill=(13, 12, 16), font=font_price)

        # Headline & Subtitle
        draw.text((60, 140), headline[:38], fill=(255, 255, 255), font=font_headline)
        draw.text((60, 215), subtitle[:45], fill=(255, 183, 3), font=font_sub)

        final_img = img.convert("RGB")
        final_img.save(output_path, "JPEG", quality=98)
        print(f"[Pillow Overlay Engine] Generated high-res graphic: {output_path}")
        return str(output_path)
    except Exception as e_pil:
        print(f"[Pillow Overlay Engine] Error generating fallback graphic: {e_pil}")
        return str(image_path)

def stamp_price_onto_tag_image(tag_path: str, price_str: str, tag_bg_hex: str = None, price_text_color: str = None, price_font_scale: float = 0.38, price_text_offset_x: int = 0, price_text_offset_y: int = 15) -> str:
    """
    Dynamically recolors tag 1.png to match the room photo's ambient accent color,
    and stamps price text at the exact visual position with custom offsets!
    """
    try:
        import PIL.ImageColor as ImageColor
        img = Image.open(tag_path).convert("RGBA")
        
        # Default dark obsidian text color
        text_color = (17, 24, 39, 255)
        
        # If tag_bg_hex is provided, recolor card body pixels!
        if tag_bg_hex and tag_bg_hex.startswith("#"):
            try:
                target_rgb = ImageColor.getrgb(tag_bg_hex)
                data = []
                for pixel in img.get_flattened_data() if hasattr(img, "get_flattened_data") else list(img.getdata()):
                    r, g, b, a = pixel
                    if a > 100 and (r + g + b > 40):
                        data.append((target_rgb[0], target_rgb[1], target_rgb[2], a))
                    else:
                        data.append((r, g, b, a))
                img.putdata(data)
                
                # Auto-select contrasting text color unless custom price_text_color is set
                lum = 0.299 * target_rgb[0] + 0.587 * target_rgb[1] + 0.114 * target_rgb[2]
                text_color = (255, 255, 255, 255) if lum < 140 else (17, 24, 39, 255)
            except Exception as e_color:
                print(f"[PIL Tag Recolorer] ⚠️ Color warning: {e_color}")
                
        if price_text_color and price_text_color.startswith("#"):
            try:
                tc_rgb = ImageColor.getrgb(price_text_color)
                text_color = (tc_rgb[0], tc_rgb[1], tc_rgb[2], 255)
            except Exception: pass

        draw = ImageDraw.Draw(img)
        w, h = img.size
        
        white_y = []
        white_x = []
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                p = img.getpixel((x, y))
                if p[3] > 100:
                    white_y.append(y)
                    white_x.append(x)
                    
        if white_x and white_y:
            center_x = (min(white_x) + max(white_x)) // 2
            center_y = (min(white_y) + max(white_y)) // 2
            card_width = max(white_x) - min(white_x)
        else:
            center_x = w // 2
            center_y = h // 2
            card_width = w
            
        font_size = int(card_width * float(price_font_scale or 0.38) * 0.25)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()
            
        # Draw contrasting price text using exact 1:1 CSS percentage coordinate mapping
        target_x_pct = (50.0 + float(price_text_offset_x) * 0.30) / 100.0
        target_y_pct = (58.0 + float(price_text_offset_y) * 0.30) / 100.0

        text_x = int(w * target_x_pct)
        text_y = int(h * target_y_pct)

        if price_str and price_str.strip():
            draw.text((text_x, text_y), price_str, fill=text_color, font=font, anchor="mm")
        
        stamped_path = Path(tag_path).parent / "stamped_ambient_tag.png"
        img.save(stamped_path, format="PNG")
        return str(stamped_path)
    except Exception as e:
        print(f"[PIL Tag Stamper] ⚠️ Stamping error: {e}")
        return tag_path





def render_html_overlay(
    image_path: str,
    headline: str,
    subtitle: str = "",
    badge_text: str = "VIRAL FIND",
    price_str: str = "$19.99",
    features: list = None,
    output_path: str = None,
    theme: str = "floating_luxury",
    enable_ai_designer: bool = False,
    tag_width_px: int = 380,
    tag_height_px: int = 285,
    tag_rotation_deg: int = -6,
    tag_pos_x: float = 61.0,
    tag_pos_y: float = 75.0,
    tag_bg_hex: str = None,
    price_text_color: str = None,
    price_font_scale: float = 0.38,
    headline_pos_y: float = None,
    headline_color: str = None,
    headline_size_px: int = None,
    price_text_offset_x: int = 0,
    price_text_offset_y: int = 15
) -> str:
    """
    Renders Canva-quality Pinterest graphic using Playwright & dynamic HTML/CSS templates.
    Supports Gemini Multimodal AI Art Director for automatic spatial text placement, font sizing,
    glow styles, and color matching.
    """
    ai_recommendation = None
    if enable_ai_designer:
        try:
            from modules.ai_art_director import analyze_product_image_for_overlay
            ai_recommendation = analyze_product_image_for_overlay(image_path)
        except Exception as e_ai:
            print(f"[HTML Overlay Engine] ⚠️ AI Director fallback: {e_ai}")

    if ai_recommendation:
        theme = ai_recommendation.get("theme_style", theme)

    if features is None:
        features = ["PREMIUM MATERIALS", "WARM AMBIENT GLOW", "STYLISH DECOR", "PERFECT GIFT"]


    # Download image if remote URL
    if str(image_path).startswith("http://") or str(image_path).startswith("https://"):
        try:
            local_tmp_path = WORKSPACE_DIR / f"tmp_remote_{int(time.time())}.jpg" if 'WORKSPACE_DIR' in globals() else Path("G:/CLI/pinterest-auto-affiliate") / f"tmp_remote_{int(time.time())}.jpg"
            r_img = requests.get(image_path, timeout=15)
            local_tmp_path.write_bytes(r_img.content)
            image_path = str(local_tmp_path)
        except Exception as e_dl:
            print(f"[HTML Overlay Engine] ⚠️ Failed to download remote image: {e_dl}")

    if output_path is None:
        output_path = image_path

    # Absolutize background image path for local file URL
    abs_img_path = Path(image_path).resolve().as_uri()

    headline_clean = headline.strip().title()
    badge_clean = badge_text.strip().upper()
    subtitle_clean = subtitle.strip().upper()
    
    price_clean = str(price_str).strip()
    if not price_clean.startswith("$") and not price_clean.startswith("£") and not price_clean.startswith("€"):
        price_clean = f"${price_clean}"


    # Dynamic Font Sizing to PREVENT TEXT OVERLAP
    hlen = len(headline_clean)
    if hlen <= 18:
        dynamic_headline_size = "76px"
    elif hlen <= 28:
        dynamic_headline_size = "58px"
    elif hlen <= 38:
        dynamic_headline_size = "48px"
    else:
        dynamic_headline_size = "40px"

    # Build features HTML
    feat_items = "".join([f'<div class="feat-card"><span>{f}</span></div>' for f in features[:4]])

    # Smart Luminance Inspection Engine (0% dimming if dark/medium, ultra-light 0.20 opacity if bright)
    scrim = detect_image_luminance(image_path)
    top_h = scrim["top_height"]
    bot_h = scrim["bot_height"]
    top_op = scrim["top_opacity"]
    bot_op = scrim["bot_opacity"]



    tag_accent_hex = tag_bg_hex if tag_bg_hex else (ai_recommendation.get("accent_color", "#ff9900") if ai_recommendation else "#ff9900")
    custom_tag_path = Path("G:/CLI/pinterest-auto-affiliate/price tags/tag 1.png")
        # Recolored tag PNG without text bitmap stamping
        stamped_tag_file = stamp_price_onto_tag_image(str(custom_tag_path), price_clean="", tag_bg_hex=tag_accent_hex, price_text_color=price_text_color, price_font_scale=price_font_scale)
        tag_abs_url = Path(stamped_tag_file).resolve().as_uri()
        
        posX = tag_pos_x if tag_pos_x is not None else 61.0
        posY = tag_pos_y if tag_pos_y is not None else 75.0
        pos_style = f"position: absolute; left: {posX}%; top: {posY}%; z-index: 20;"

        calc_height_px = int(tag_width_px * (406.0 / 300.0))
        
        # Calculate HTML CSS text properties matching admin_console.html 1:1
        f_scale = float(price_font_scale or 0.20)
        calc_font_px = max(10, int(tag_width_px * f_scale * 0.45))
        shift_y_pct = 50.0 + (float(price_text_offset_y) * 0.40)
        shift_x_pct = 50.0 + (float(price_text_offset_x) * 0.40)
        p_color = price_text_color if price_text_color else "#111827"

        price_pill_html = f"""
        <div class="custom-price-container" style="{pos_style} width: {tag_width_px}px; height: {calc_height_px}px; transform: rotate({tag_rotation_deg}deg); filter: drop-shadow(0 18px 36px rgba(0, 0, 0, 0.75));">
            <img src="{tag_abs_url}" style="width: 100%; height: 100%; display: block; object-fit: contain;" />
            <div class="price-text-html" style="position: absolute; top: {shift_y_pct}%; left: {shift_x_pct}%; transform: translate(-50%, -50%); font-family: 'Outfit', sans-serif; font-size: {calc_font_px}px; font-weight: 900; color: {p_color}; white-space: nowrap; pointer-events: none; text-shadow: 0 1px 2px rgba(255,255,255,0.6);">
                {price_clean}
            </div>
        </div>
        """
    else:
        price_pill_html = f'<div class="price-pill">{price_clean}</div>'





    price_pill_css = """
    .price-pill {
        background: linear-gradient(135deg, #ff9900, #ffb703);
        border: 2.5px solid #ffffff; backdrop-filter: blur(20px);
        padding: 10px 45px; border-radius: 50px;
        font-family: 'Outfit', sans-serif; font-size: 44px; font-weight: 900;
        color: #0a0810; letter-spacing: 1px;
        box-shadow: 0 14px 35px rgba(255, 153, 0, 0.55), 0 6px 15px rgba(0, 0, 0, 0.4);
    }
    """



    if theme == "bottom_glass_card" or "lamp" in headline_clean.lower():
        # Soft Bedside Warm Pearl & Glass Card Theme (Tailored for Lamps & Nightstand Decor)
        top_container_pos_css = f"position: absolute; top: {headline_pos_y}%; left: 0; right: 0; z-index: 15;" if headline_pos_y is not None else ""
        headline_color_css = f"color: {headline_color} !important;" if headline_color else ""
        headline_size_css = f"font-size: {headline_size_px}px !important;" if headline_size_px else f"font-size: {dynamic_headline_size};"

        theme_css = f"""
        .scrim-top {{
            position: absolute; top: 0; left: 0; width: 100%; height: {top_h};
            background: linear-gradient(180deg, rgba(12, 10, 16, {top_op}) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }}
        .scrim-bottom {{
            position: absolute; bottom: 0; left: 0; width: 100%; height: {bot_h};
            background: linear-gradient(0deg, rgba(12, 10, 16, {bot_op}) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }}
        .top-container {{
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%; gap: 10px; {top_container_pos_css}
        }}
        .badge {{
            background: rgba(255, 255, 255, 0.22);
            border: 1.5px solid rgba(255, 255, 255, 0.65); backdrop-filter: blur(16px);
            color: #ffffff; font-size: 16px; font-weight: 800;
            padding: 8px 30px; border-radius: 50px; letter-spacing: 3.5px; text-transform: uppercase;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
        }}
        .headline {{
            font-family: 'Caveat', 'Playfair Display', 'Cormorant Garamond', cursive, serif; {headline_size_css} font-weight: 700;
            line-height: 1.12; {headline_color_css or 'color: #ffffff;'} text-shadow: 0 4px 24px rgba(0,0,0,0.95);
            max-width: 1000px; padding: 0 20px;
        }}

        .divider-line {{ background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.8), transparent); width: 130px; height: 2px; }}
        .divider-star {{ color: #ffd700; font-size: 20px; }}
        .subtitle {{ display: none; }}
        {price_pill_css}

        .feat-card {{
            background: rgba(255, 255, 255, 0.16); border: 1px solid rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(14px); border-radius: 16px; padding: 12px 8px; text-align: center;
        }}
        .feat-card span {{ color: #ffffff; font-size: 13px; font-weight: 700; letter-spacing: 1.2px; }}
        """

        # Prismatic Sunlight Crystal Glass Theme (For Suncatchers & Window Decor)


        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 38%;
            background: linear-gradient(180deg, rgba(20, 15, 30, 0.72) 0%, rgba(20, 15, 30, 0.2) 65%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 22%;
            background: linear-gradient(0deg, rgba(20, 15, 30, 0.75) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-container {
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%;
        }
        .badge {
            background: linear-gradient(135deg, rgba(255, 215, 0, 0.35), rgba(255, 105, 180, 0.35));
            border: 2px solid rgba(255, 255, 255, 0.95); backdrop-filter: blur(16px);
            color: #ffffff; font-size: 19px; font-weight: 800;
            padding: 10px 34px; border-radius: 50px; letter-spacing: 3.5px; text-transform: uppercase;
            margin-bottom: 18px; box-shadow: 0 8px 30px rgba(255, 182, 193, 0.4);
        }
        .headline {
            font-family: 'Cormorant Garamond', serif; font-size: 80px; font-weight: 700;
            line-height: 1.06; color: #ffffff; text-shadow: 0 4px 30px rgba(0,0,0,0.9);
            margin-bottom: 14px; max-width: 1050px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.95), transparent); width: 150px; height: 2px; }
        .divider-star { color: #ffd700; font-size: 24px; }
        .subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 18px; font-weight: 700; letter-spacing: 5px; color: #ffe699;
            text-transform: uppercase; text-shadow: 0 2px 12px rgba(0,0,0,0.9); margin-bottom: 22px;
        }
        .price-pill {
            background: linear-gradient(135deg, #ffd700, #ff8c00);
            border: 2px solid #ffffff; backdrop-filter: blur(20px);
            padding: 12px 52px; border-radius: 50px;
            font-family: 'Cormorant Garamond', serif; font-size: 54px; font-weight: 700;
            color: #0f0b18; box-shadow: 0 16px 45px rgba(255, 140, 0, 0.55);
        }
        .feat-card {
            background: rgba(255, 255, 255, 0.22); border: 1px solid rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(14px); border-radius: 16px; padding: 14px 10px; text-align: center;
        }
        .feat-card span { color: #ffffff; font-size: 13px; font-weight: 800; letter-spacing: 1.5px; }
        """
    elif theme == "dark_obsidian_neon":
        # Dark Obsidian Translucent Glass & Cyber Coral Glow Theme (For Diffusers & LED Boards)
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 36%;
            background: linear-gradient(180deg, rgba(8, 6, 14, 0.85) 0%, rgba(8, 6, 14, 0.3) 65%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 22%;
            background: linear-gradient(0deg, rgba(8, 6, 14, 0.85) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-container {
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%;
        }
        .badge {
            background: linear-gradient(135deg, #ff0055, #ff5000);
            border: 2px solid #ffffff; color: #ffffff; font-size: 19px; font-weight: 800;
            padding: 10px 32px; border-radius: 50px; letter-spacing: 3.5px; text-transform: uppercase;
            margin-bottom: 18px; box-shadow: 0 8px 30px rgba(255, 0, 85, 0.5);
        }
        .headline {
            font-family: 'Outfit', sans-serif; font-size: 74px; font-weight: 800;
            line-height: 1.08; color: #ffffff; text-shadow: 0 4px 28px rgba(0,0,0,0.95);
            margin-bottom: 14px; max-width: 1000px; letter-spacing: -1px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, #ff0055, transparent); width: 140px; height: 3px; }
        .divider-star { color: #ff5000; font-size: 22px; }
        .subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 18px; font-weight: 700; letter-spacing: 5px; color: #ff80a0;
            text-transform: uppercase; text-shadow: 0 2px 12px rgba(0,0,0,0.9); margin-bottom: 22px;
        }
        .price-pill {
            background: linear-gradient(135deg, #ff0055, #7a00ff);
            border: 2px solid #ffffff; backdrop-filter: blur(20px);
            padding: 12px 50px; border-radius: 50px;
            font-family: 'Outfit', sans-serif; font-size: 52px; font-weight: 800;
            color: #ffffff; box-shadow: 0 16px 45px rgba(255, 0, 85, 0.6);
        }
        .feat-card {
            background: rgba(18, 14, 28, 0.85); border: 1px solid rgba(255, 0, 85, 0.4);
            backdrop-filter: blur(14px); border-radius: 16px; padding: 14px 10px; text-align: center;
        }
        .feat-card span { color: #ffffff; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; }
        """
    elif theme == "floating_cream":
        # Floating Pearl & High-Fashion Aesthetic Cream Theme
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 36%;
            background: linear-gradient(180deg, rgba(15, 12, 18, 0.75) 0%, rgba(15, 12, 18, 0.25) 65%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 22%;
            background: linear-gradient(0deg, rgba(15, 12, 18, 0.75) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-container {
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%;
        }
        .badge {
            background: rgba(255, 251, 245, 0.92); border: 2px solid #ffffff;
            color: #1a1622; font-size: 19px; font-weight: 800;
            padding: 10px 32px; border-radius: 50px; letter-spacing: 3.5px; text-transform: uppercase;
            margin-bottom: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.35);
        }
        .headline {
            font-family: 'Cormorant Garamond', 'Playfair Display', serif; font-size: 78px; font-weight: 700;
            line-height: 1.08; color: #ffffff; text-shadow: 0 4px 28px rgba(0,0,0,0.9), 0 2px 8px rgba(0,0,0,0.95);
            margin-bottom: 14px; max-width: 1050px; font-style: italic;
        }
        .divider-line { background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.9), transparent); width: 140px; height: 2px; }
        .divider-star { color: #fdfbf7; font-size: 22px; }
        .subtitle {
            font-family: 'Outfit', sans-serif;
            font-size: 18px; font-weight: 700; letter-spacing: 5px; color: #f4efe6;
            text-transform: uppercase; text-shadow: 0 2px 12px rgba(0,0,0,0.9); margin-bottom: 22px;
        }
        .price-pill {
            background: linear-gradient(135deg, #ffffff, #fdfaf5);
            border: 2px solid rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 12px 50px;
            border-radius: 50px;
            font-family: 'Cormorant Garamond', serif;
            font-size: 54px;
            font-weight: 700;
            color: #120f18;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.5), inset 0 2px 4px rgba(255, 255, 255, 1);
            text-shadow: none;
        }
        .feat-card {
            background: rgba(255, 255, 255, 0.18); border: 1px solid rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(14px); border-radius: 16px; padding: 14px 10px; text-align: center;
        }
        .feat-card span { color: #ffffff; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; text-shadow: 0 2px 6px rgba(0,0,0,0.7); }
        """
    else:
        # 'floating_luxury' (Default Floating Amber Studio — Zero Boxes Blocking Product)
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 35%;
            background: linear-gradient(180deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.2) 65%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 22%;
            background: linear-gradient(0deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-container {
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%;
        }
        .badge {
            background: rgba(255, 183, 3, 0.22); border: 1px solid rgba(255, 183, 3, 0.7);
            backdrop-filter: blur(12px); color: #ffb703; font-size: 19px; font-weight: 700;
            padding: 8px 28px; border-radius: 50px; letter-spacing: 2.5px; text-transform: uppercase;
            margin-bottom: 16px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 72px; font-weight: 700;
            line-height: 1.12; color: #ffffff; text-shadow: 0 4px 24px rgba(0,0,0,0.85), 0 2px 6px rgba(0,0,0,0.9);
            margin-bottom: 16px; max-width: 1000px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, rgba(255, 210, 120, 0.9), transparent); width: 120px; height: 2px; }
        .divider-star { color: #ffb703; font-size: 22px; }
        .subtitle {
            font-size: 19px; font-weight: 600; letter-spacing: 5px; color: #ffd166;
            text-transform: uppercase; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 22px;
        }
        .price-pill {
            background: linear-gradient(135deg, #fb8500, #ffb703);
            border: 2px solid #ffffff;
            backdrop-filter: blur(20px);
            padding: 10px 46px;
            border-radius: 50px;
            font-family: 'Playfair Display', serif;
            font-size: 50px;
            font-weight: 700;
            color: #0d0c10;
            box-shadow: 0 14px 40px rgba(251, 133, 0, 0.6), inset 0 2px 4px rgba(255, 255, 255, 0.7);
            text-shadow: none;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        .feat-card {
            background: rgba(255, 255, 255, 0.14); border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(12px); border-radius: 16px; padding: 14px 10px; text-align: center;
        }
        .feat-card span { color: #f8f9fa; font-size: 13px; font-weight: 700; letter-spacing: 1.5px; text-shadow: 0 2px 6px rgba(0,0,0,0.7); }
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Outfit:wght@300;400;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;1,600;1,700&display=swap" rel="stylesheet">

    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            width: 1200px;
            height: 1600px;
            margin: 0;
            overflow: hidden;
            font-family: 'Outfit', sans-serif;
            background: #0f0e13 url('{abs_img_path}') center/cover no-repeat;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 50px 45px;
            color: #fff;
        }}

        {theme_css}

        .divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            width: 100%;
            margin-top: 8px;
        }}

        .bottom-container {{
            position: absolute;
            bottom: 40px;
            left: 45px;
            right: 45px;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 14px;
        }}

        .bottom-meta {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            padding: 0 10px;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            width: 100%;
        }}
    </style>
</head>
<body>
    <div class="scrim-top"></div>
    <div class="scrim-bottom"></div>

    <div class="top-container">
        <div class="badge">✨ {badge_clean}</div>
        <div class="headline">{headline_clean}</div>
        <div class="divider">
            <div class="divider-line"></div>
            <div class="divider-star">✦</div>
            <div class="divider-line"></div>
        </div>
    </div>

    {price_pill_html}

    <div class="bottom-container">
        <div class="features-grid">
            {feat_items}
        </div>
    </div>

</body>
</html>
"""


    temp_html = Path(image_path).parent / "temp_pin_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    if not PLAYWRIGHT_AVAILABLE:
        print("[HTML Overlay Engine] Playwright is unavailable, falling back to Pillow overlay engine...")
        return render_pillow_fallback(image_path, headline_clean, subtitle_clean, badge_clean, price_clean, output_path)

    print(f"[HTML Overlay Engine] Rendering 100% Product Clear Playwright 1200x1600 graphic to {output_path}...")

    rendered = False
    for attempt in range(3):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=[
                    "--no-sandbox",
                    "--disable-gpu",
                    "--force-color-profile=srgb",
                    "--disable-color-correct-rendering"
                ])
                context = browser.new_context(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
                page = context.new_page()

                page.goto(temp_html.resolve().as_uri())
                page.wait_for_timeout(1000)
                page.screenshot(path=str(output_path), type="jpeg", quality=98)
                browser.close()
                rendered = True
                break
        except Exception as e_p:
            time.sleep(1)
            if attempt == 2:
                print(f"[HTML Overlay Engine] Playwright error: {e_p}")

    if not rendered:
        print("[HTML Overlay Engine] Falling back to Pillow overlay engine after Playwright attempts...")
        render_pillow_fallback(image_path, headline_clean, subtitle_clean, badge_clean, price_clean, output_path)

    if temp_html.exists():
        temp_html.unlink()

    print(f"[HTML Overlay Engine] Saved high-res floating pin graphic (100% Product Clear): {output_path}")
    return str(output_path)
