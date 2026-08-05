import sys
import shutil
import json
import re
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo = Path('.').resolve()
sys.path.append(str(repo))

console_src = repo / 'raw_B0D1FRDFFX_console.jpg'
raw_dst1 = repo / 'raw_images' / 'raw_B0D1FRDFFX.jpg'
raw_dst2 = repo / 'output' / 'images' / 'raw_B0D1FRDFFX.jpg'

raw_dst1.parent.mkdir(exist_ok=True)
raw_dst2.parent.mkdir(exist_ok=True)

if console_src.exists():
    shutil.copy(console_src, raw_dst1)
    shutil.copy(console_src, raw_dst2)
    print(f'Saved correct clean image from {console_src.name} to {raw_dst1} ({raw_dst1.stat().st_size} bytes)')
else:
    print(f'Warning: {console_src} not found!')

# Re-render Playwright graphic overlay badge
from modules.html_overlay_engine import render_html_overlay

hook_output = repo / 'focus_product_B0D1FRDFFX_hook.jpg'

render_html_overlay(
    image_path=str(raw_dst1),
    headline='Handmade Glass Mushroom Ambient Lamp',
    subtitle='',
    badge_text='✨ VIRAL ROOM FIND',
    price_str='$35.98',
    output_path=str(hook_output),
    theme='bottom_glass_card'
)
print(f'Re-rendered hook image badge: {hook_output} ({hook_output.stat().st_size} bytes)')

# Rebuild bridge pages
from rebuild_EVERY_single_bridge import master_catalog
# Re-run bridge creator script
from modules.bridge_creator import generate_bridge_page

reg_file = repo / 'product_price_registry.json'
registry = json.loads(reg_file.read_text(encoding='utf-8'))
item_meta = registry.get('B0D1FRDFFX', {})

generate_bridge_page(
    product_id='B0D1FRDFFX',
    title='Handmade Glass Mushroom Ambient Lamp',
    price='$35.98',
    rating='4.8',
    features=['HAND-BLOWN STRIPED GLASS', 'WARM AMBIENT GLOW', 'VINTAGE MUSHROOM DESIGN', 'EASY ON/OFF SWITCH'],
    hook_image='focus_product_B0D1FRDFFX_hook.jpg',
    category='lighting',
    description='Add a cozy retro aesthetic to your space with this hand-blown striped glass mushroom lamp. Soft ambient glow for nightstands, desks, and shelves.',
    direct_regions=['US', 'IN', 'UK', 'DE', 'SE', 'SG', 'CA', 'AU', 'JP'],
    regional_prices=item_meta.get('regional_prices', {}),
    regional_asins=item_meta.get('regional_asins', {}),
    output_filename='bridge_B0D1FRDFFX.html'
)
print('Rebuilt bridge_B0D1FRDFFX.html successfully!')
