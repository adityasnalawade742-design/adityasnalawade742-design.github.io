import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def render_html_overlay(
    image_path: str,
    headline: str,
    subtitle: str = "ELEGANCE THAT SHINES",
    badge_text: str = "AMAZON HOME FIND",
    price_str: str = "$19.99",
    features: list = None,
    output_path: str = None,
    theme: str = "warm_cream"
) -> str:
    """
    Renders Canva-quality Pinterest graphic using Playwright & modern HTML/CSS templates.
    Supported themes:
      - 'warm_cream': Soft cream/linen frosted glass card with dark espresso serif (Cozy Bedroom Vibe)
      - 'botanical_sage': Earthy sage green accents with champagne gold borders (Nature/Botanical Vibe)
      - 'moody_boho': Sunset amber & terracotta warm ambient glow (Cozy Evening Vibe)
      - 'luxury_glass': Dark luxury translucent glassmorphism with glowing amber badge (Luxury Studio Vibe)
    """
    if features is None:
        features = ["PREMIUM MATERIALS", "WARM AMBIENT GLOW", "STYLISH DECOR", "PERFECT GIFT"]

    if output_path is None:
        output_path = image_path

    # Absolutize background image path for local file URL
    abs_img_path = Path(image_path).resolve().as_uri()

    headline_clean = headline.strip().title()
    badge_clean = badge_text.strip().upper()
    subtitle_clean = subtitle.strip().upper()
    
    price_clean = str(price_str).strip()
    if price_clean.startswith("$."):
        price_clean = f"${price_clean[2:]}"
    if price_clean and not any(price_clean.startswith(c) for c in ["$", "£", "€"]):
        price_clean = f"${price_clean}"

    # Build features HTML
    feat_items = "".join([f'<div class="feat-card"><span>{f}</span></div>' for f in features[:4]])

    # Define CSS styles per theme
    if theme == "warm_cream":
        # Soft Cream / Organic Linen Editorial Vibe (Light frosted glass card)
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 40%;
            background: linear-gradient(180deg, rgba(40,32,24,0.4) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 25%;
            background: linear-gradient(0deg, rgba(40,32,24,0.5) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-card {
            background: rgba(255, 251, 245, 0.88);
            border: 1px solid rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-radius: 36px;
            padding: 44px 48px;
            box-shadow: 0 20px 60px rgba(44, 36, 30, 0.25);
            display: flex; flex-direction: column; align-items: center; text-align: center;
            max-width: 1040px;
        }
        .badge {
            background: rgba(180, 130, 80, 0.12);
            border: 1px solid rgba(180, 130, 80, 0.35);
            color: #8c5a2b;
            font-size: 19px; font-weight: 700; padding: 8px 24px; border-radius: 50px;
            letter-spacing: 2px; text-transform: uppercase; margin-bottom: 18px;
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 68px; font-weight: 700;
            line-height: 1.15; color: #2c221e; margin-bottom: 16px;
        }
        .divider-line { background: rgba(140, 90, 40, 0.3); width: 100px; height: 1px; }
        .divider-star { color: #b8860b; font-size: 18px; }
        .subtitle {
            font-size: 18px; font-weight: 700; letter-spacing: 4px; color: #7a5c40;
            text-transform: uppercase; margin-bottom: 22px;
        }
        .price-pill {
            background: #2c221e; color: #fff5ea; border-radius: 50px;
            padding: 12px 40px; font-family: 'Playfair Display', serif; font-size: 46px; font-weight: 700;
            box-shadow: 0 10px 30px rgba(44, 34, 30, 0.3);
        }
        .feat-card {
            background: rgba(255, 251, 245, 0.82); border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(16px); border-radius: 18px; padding: 16px 12px; text-align: center;
        }
        .feat-card span { color: #3a2e26; font-size: 14px; font-weight: 700; letter-spacing: 1px; }
        """
        html_layout = f"""
        <div class="top-container">
            <div class="top-card">
                <div class="badge">✨ {badge_clean}</div>
                <div class="headline">{headline_clean}</div>
                <div class="divider">
                    <div class="divider-line"></div>
                    <div class="divider-star">✦</div>
                    <div class="divider-line"></div>
                </div>
                <div class="subtitle">{subtitle_clean}</div>
                <div class="price-pill">{price_clean}</div>
            </div>
        </div>
        """
    elif theme == "botanical_sage":
        # Botanical Sage Green & Gold Vibe
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 45%;
            background: linear-gradient(180deg, rgba(20,35,25,0.7) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 25%;
            background: linear-gradient(0deg, rgba(20,35,25,0.75) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .top-container { display: flex; flex-direction: column; align-items: center; text-align: center; }
        .badge {
            background: rgba(168, 195, 160, 0.22); border: 1px solid rgba(180, 215, 170, 0.7);
            backdrop-filter: blur(16px); color: #d4ebd0; font-size: 20px; font-weight: 700;
            padding: 10px 28px; border-radius: 50px; letter-spacing: 2px; margin-bottom: 22px;
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 74px; font-weight: 700;
            color: #f4fbf2; text-shadow: 0 4px 20px rgba(0,0,0,0.7); margin-bottom: 18px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, #a8c3a0, transparent); width: 120px; height: 2px; }
        .divider-star { color: #a8c3a0; font-size: 22px; }
        .subtitle { font-size: 20px; font-weight: 600; letter-spacing: 5px; color: #c3e2bb; margin-bottom: 24px; }
        .price-pill {
            background: rgba(30, 50, 38, 0.82); border: 2px solid #a8c3a0; backdrop-filter: blur(20px);
            padding: 12px 42px; border-radius: 50px; font-family: 'Playfair Display', serif;
            font-size: 46px; font-weight: 700; color: #e8f7e4; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
        .feat-card {
            background: rgba(30, 50, 38, 0.75); border: 1px solid rgba(168, 195, 160, 0.4);
            backdrop-filter: blur(16px); border-radius: 18px; padding: 16px 12px; text-align: center;
        }
        .feat-card span { color: #e8f7e4; font-size: 14px; font-weight: 700; letter-spacing: 1px; }
        """
        html_layout = f"""
        <div class="top-container">
            <div class="badge">🌿 {badge_clean}</div>
            <div class="headline">{headline_clean}</div>
            <div class="divider">
                <div class="divider-line"></div>
                <div class="divider-star">✦</div>
                <div class="divider-line"></div>
            </div>
            <div class="subtitle">{subtitle_clean}</div>
            <div class="price-pill">{price_clean}</div>
        </div>
        """
    elif theme == "moody_boho":
        # Terracotta & Sunset Amber Warm Ambient Vibe
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 45%;
            background: linear-gradient(180deg, rgba(45,20,10,0.7) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 25%;
            background: linear-gradient(0deg, rgba(45,20,10,0.8) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .top-container { display: flex; flex-direction: column; align-items: center; text-align: center; }
        .badge {
            background: rgba(230, 120, 60, 0.2); border: 1px solid rgba(255, 160, 100, 0.6);
            backdrop-filter: blur(16px); color: #ffb088; font-size: 20px; font-weight: 700;
            padding: 10px 28px; border-radius: 50px; letter-spacing: 2px; margin-bottom: 22px;
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 74px; font-weight: 700;
            color: #fff4ee; text-shadow: 0 4px 20px rgba(0,0,0,0.8); margin-bottom: 18px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, #ffaa80, transparent); width: 120px; height: 2px; }
        .divider-star { color: #ffaa80; font-size: 22px; }
        .subtitle { font-size: 20px; font-weight: 600; letter-spacing: 5px; color: #ffd0b8; margin-bottom: 24px; }
        .price-pill {
            background: rgba(55, 25, 15, 0.85); border: 2px solid #ffaa80; backdrop-filter: blur(20px);
            padding: 12px 42px; border-radius: 50px; font-family: 'Playfair Display', serif;
            font-size: 46px; font-weight: 700; color: #ffaa80; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .feat-card {
            background: rgba(55, 25, 15, 0.75); border: 1px solid rgba(255, 170, 128, 0.4);
            backdrop-filter: blur(16px); border-radius: 18px; padding: 16px 12px; text-align: center;
        }
        .feat-card span { color: #fff4ee; font-size: 14px; font-weight: 700; letter-spacing: 1px; }
        """
        html_layout = f"""
        <div class="top-container">
            <div class="badge">🌅 {badge_clean}</div>
            <div class="headline">{headline_clean}</div>
            <div class="divider">
                <div class="divider-line"></div>
                <div class="divider-star">✦</div>
                <div class="divider-line"></div>
            </div>
            <div class="subtitle">{subtitle_clean}</div>
            <div class="price-pill">{price_clean}</div>
        </div>
        """
    else:  # 'luxury_glass' (Default Amber Studio Glass)
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 45%;
            background: linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 30%;
            background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0) 100%); z-index: 1;
        }
        .top-container { display: flex; flex-direction: column; align-items: center; text-align: center; }
        .badge {
            background: rgba(255, 183, 3, 0.18); border: 1px solid rgba(255, 183, 3, 0.6);
            backdrop-filter: blur(16px); color: #ffb703; font-size: 20px; font-weight: 700;
            padding: 10px 28px; border-radius: 50px; letter-spacing: 2.5px; margin-bottom: 24px;
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 72px; font-weight: 700;
            color: #ffffff; text-shadow: 0 4px 20px rgba(0,0,0,0.8); margin-bottom: 20px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, rgba(255, 210, 120, 0.8), transparent); width: 120px; height: 2px; }
        .divider-star { color: #ffb703; font-size: 22px; }
        .subtitle { font-size: 22px; font-weight: 600; letter-spacing: 5px; color: #ffd166; margin-bottom: 28px; }
        .price-pill {
            background: rgba(26, 24, 33, 0.75); border: 2px solid rgba(255, 183, 3, 0.8);
            backdrop-filter: blur(20px); padding: 14px 44px; border-radius: 50px;
            font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 700; color: #ffb703;
        }
        .feat-card {
            background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px); border-radius: 16px; padding: 16px 12px; text-align: center;
        }
        .feat-card span { color: #f8f9fa; font-size: 14px; font-weight: 700; letter-spacing: 1.5px; }
        """
        html_layout = f"""
        <div class="top-container">
            <div class="badge">✨ {badge_clean}</div>
            <div class="headline">{headline_clean}</div>
            <div class="divider">
                <div class="divider-line"></div>
                <div class="divider-star">✦</div>
                <div class="divider-line"></div>
            </div>
            <div class="subtitle">{subtitle_clean}</div>
            <div class="price-pill">{price_clean}</div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
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
            padding: 80px 60px;
            color: #fff;
        }}

        {theme_css}

        .divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            width: 100%;
            margin-bottom: 20px;
        }}

        .bottom-container {{
            position: relative;
            z-index: 10;
            width: 100%;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 16px;
            width: 100%;
        }}
    </style>
</head>
<body>
    <div class="scrim-top"></div>
    <div class="scrim-bottom"></div>

    {html_layout}

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

    print(f"[HTML Overlay Engine] Rendering theme='{theme}' Playwright 1200x1600 graphic to {output_path}...")

    for attempt in range(3):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
                context = browser.new_context(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
                page = context.new_page()
                page.goto(temp_html.resolve().as_uri())
                page.wait_for_timeout(1000)
                page.screenshot(path=str(output_path), type="jpeg", quality=98)
                browser.close()
                break
        except Exception as e_p:
            time.sleep(1)
            if attempt == 2:
                print(f"[HTML Overlay Engine] Playwright error: {e_p}")

    if temp_html.exists():
        temp_html.unlink()

    print(f"[HTML Overlay Engine] Saved high-res '{theme}' pin graphic: {output_path}")
    return str(output_path)
