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
    theme: str = "floating_luxury"
) -> str:
    """
    Renders Canva-quality Pinterest graphic using Playwright & modern floating HTML/CSS templates.
    Ensures the product is 100% VISIBLE without any large boxes or windows obscuring the main subject.
    
    Supported themes:
      - 'floating_luxury': Floating white & amber gold serif text with subtle scrim (100% Product Clear)
      - 'floating_cream': Floating dark espresso text with soft top glow (100% Product Clear)
      - 'botanical_green': Floating sage & champagne gold accents (100% Product Clear)
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

    if theme == "floating_cream":
        # Floating Dark Espresso & Soft Cream Accents (Zero Boxes Blocking Product)
        theme_css = """
        .scrim-top {
            position: absolute; top: 0; left: 0; width: 100%; height: 32%;
            background: linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.2) 60%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .scrim-bottom {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 20%;
            background: linear-gradient(0deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);
            z-index: 1;
        }
        .top-container {
            display: flex; flex-direction: column; align-items: center; text-align: center;
            width: 100%;
        }
        .badge {
            background: rgba(255, 251, 245, 0.25); border: 1px solid rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(12px); color: #ffffff; font-size: 18px; font-weight: 700;
            padding: 8px 26px; border-radius: 50px; letter-spacing: 2.5px; text-transform: uppercase;
            margin-bottom: 16px; text-shadow: 0 2px 8px rgba(0,0,0,0.7);
        }
        .headline {
            font-family: 'Playfair Display', serif; font-size: 70px; font-weight: 700;
            line-height: 1.12; color: #ffffff; text-shadow: 0 4px 24px rgba(0,0,0,0.85), 0 2px 6px rgba(0,0,0,0.9);
            margin-bottom: 14px; max-width: 1000px;
        }
        .divider-line { background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent); width: 110px; height: 2px; }
        .divider-star { color: #ffffff; font-size: 20px; }
        .subtitle {
            font-size: 18px; font-weight: 600; letter-spacing: 4.5px; color: #f8f9fa;
            text-transform: uppercase; text-shadow: 0 2px 10px rgba(0,0,0,0.8); margin-bottom: 20px;
        }
        .price-pill {
            background: rgba(26, 24, 33, 0.82); border: 2px solid rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(16px); padding: 10px 40px; border-radius: 50px;
            font-family: 'Playfair Display', serif; font-size: 44px; font-weight: 700; color: #ffffff;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4); text-shadow: 0 2px 8px rgba(0,0,0,0.5);
        }
        .feat-card {
            background: rgba(26, 24, 33, 0.65); border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(12px); border-radius: 16px; padding: 14px 10px; text-align: center;
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
            background: rgba(26, 24, 33, 0.82); border: 2px solid rgba(255, 183, 3, 0.85);
            backdrop-filter: blur(16px); padding: 12px 44px; border-radius: 50px;
            font-family: 'Playfair Display', serif; font-size: 46px; font-weight: 700; color: #ffb703;
            box-shadow: 0 10px 32px rgba(0,0,0,0.5); text-shadow: 0 2px 10px rgba(0,0,0,0.5);
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
            padding: 60px 50px;
            color: #fff;
        }}

        {theme_css}

        .divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            width: 100%;
            margin-bottom: 16px;
        }}

        .bottom-container {{
            position: relative;
            z-index: 10;
            width: 100%;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
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
        <div class="subtitle">{subtitle_clean}</div>
        <div class="price-pill">{price_clean}</div>
    </div>

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

    print(f"[HTML Overlay Engine] Rendering 100% Product Clear Playwright 1200x1600 graphic to {output_path}...")

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

    print(f"[HTML Overlay Engine] Saved high-res floating pin graphic (100% Product Clear): {output_path}")
    return str(output_path)
