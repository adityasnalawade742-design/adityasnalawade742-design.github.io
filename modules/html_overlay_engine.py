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
    theme: str = "luxury_glass"
) -> str:
    """
    Renders Canva-quality Pinterest graphic using Playwright & modern HTML/CSS.
    Uses flexbox layout, CSS glassmorphism, Google Fonts, and automatic high-res viewport capture.
    """
    if features is None:
        features = ["PREMIUM MATERIALS", "WARM AMBIENT GLOW", "STYLISH DECOR", "PERFECT GIFT"]

    if output_path is None:
        output_path = image_path

    # Absolutize background image path for local file URL
    abs_img_path = Path(image_path).resolve().as_uri()

    # Clean headline & format
    headline_clean = headline.strip().title()
    badge_clean = badge_text.strip().upper()
    subtitle_clean = subtitle.strip().upper()
    
    # Ensure currency symbol
    price_clean = str(price_str).strip()
    if price_clean and not any(price_clean.startswith(c) for c in ["$", "£", "€"]):
        price_clean = f"${price_clean}"

    # Build features HTML
    feat_items = "".join([f'<div class="feat-card"><span>{f}</span></div>' for f in features[:4]])

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
            padding: 80px 60px;
            color: #fff;
        }}

        /* Subtle top & bottom dark ambient gradients for legibility */
        .scrim-top {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 45%;
            background: linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,0,0,0.3) 60%, rgba(0,0,0,0) 100%);
            pointer-events: none;
            z-index: 1;
        }}
        .scrim-bottom {{
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 30%;
            background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, rgba(0,0,0,0) 100%);
            pointer-events: none;
            z-index: 1;
        }}

        .top-container {{
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            width: 100%;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 183, 3, 0.18);
            border: 1px solid rgba(255, 183, 3, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            color: #ffb703;
            font-size: 20px;
            font-weight: 700;
            padding: 10px 28px;
            border-radius: 50px;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}

        .headline {{
            font-family: 'Playfair Display', serif;
            font-size: 72px;
            font-weight: 700;
            line-height: 1.15;
            color: #ffffff;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8), 0 2px 4px rgba(0, 0, 0, 0.9);
            margin-bottom: 20px;
            max-width: 1000px;
        }}

        .divider {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            width: 100%;
            margin-bottom: 20px;
        }}
        .divider-line {{
            width: 120px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255, 210, 120, 0.8), transparent);
        }}
        .divider-star {{
            color: #ffb703;
            font-size: 22px;
        }}

        .subtitle {{
            font-size: 22px;
            font-weight: 600;
            letter-spacing: 5px;
            color: #ffd166;
            text-transform: uppercase;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
            margin-bottom: 28px;
        }}

        .price-pill {{
            background: rgba(26, 24, 33, 0.75);
            border: 2px solid rgba(255, 183, 3, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            padding: 14px 44px;
            border-radius: 50px;
            font-family: 'Playfair Display', serif;
            font-size: 48px;
            font-weight: 700;
            color: #ffb703;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(255, 183, 3, 0.2);
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        }}

        /* Bottom Feature Bar */
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

        .feat-card {{
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.25);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            padding: 16px 12px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }}

        .feat-card span {{
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #f8f9fa;
            text-transform: uppercase;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
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

    print(f"[HTML Overlay Engine] Rendering Playwright 1200x1600 HTML/CSS template to {output_path}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1200, "height": 1600}, device_scale_factor=2)
        page.goto(temp_html.resolve().as_uri())
        
        # Wait for web fonts & background image to render
        page.wait_for_timeout(800)
        
        page.screenshot(path=str(output_path), type="jpeg", quality=98)
        browser.close()

    if temp_html.exists():
        temp_html.unlink()

    print(f"[HTML Overlay Engine] Saved high-res HTML/CSS rendered pin graphic: {output_path}")
    return str(output_path)
