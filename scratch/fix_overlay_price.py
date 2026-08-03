import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from modules.html_overlay_engine import render_html_overlay

asin = 'B0FGJ1S73D'
raw_img = Path(f'raw_images/raw_{asin}.jpg')
out_img = Path(f'focus_product_{asin}_hook.jpg')

if raw_img.exists():
    render_html_overlay(
        image_path=str(raw_img),
        headline='Ceramic Mushroom Lamp',
        subtitle='Cozy Bedroom Glow',
        badge_text='VIRAL ROOM FIND',
        price_str='$32.99',
        features=['3-WAY TOUCH', 'GLASS SHADE', 'CERAMIC BASE', 'WARM GLOW'],
        output_path=str(out_img)
    )
    print('Re-rendered graphic overlay with real Amazon price $32.99!')
else:
    print('raw image not found:', raw_img)
