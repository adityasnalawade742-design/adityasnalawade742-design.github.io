"""
Local Web Console Server for Product & Image Verification
Serves admin_console.html on http://localhost:5000
Provides API endpoints for extracting Amazon photos and launching campaign generation.
"""
import sys
import os
import json
import urllib.parse
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.amazon_extractor import (
    get_product_details_and_photos,
    select_clean_photo_or_skip,
    has_text_annotation,
    is_grid_collage,
    has_human_presence
)

PORT = 5000
WORKSPACE_DIR = Path("G:/CLI/pinterest-auto-affiliate")

class WebConsoleHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/' or parsed.path == '/console':
            self.path = '/admin_console.html'
            return super().do_GET()
        elif parsed.path == '/api/extract':
            self.handle_api_extract(parsed.query)
            return
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api/generate':
            self.handle_api_generate()
            return
        else:
            self.send_error(404, "Endpoint not found")

    def handle_api_extract(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        target = params.get('target', [''])[0].strip()

        if not target:
            self.send_json({'status': 'error', 'message': 'Missing target ASIN or URL'})
            return

        if target.startswith('http'):
            amazon_url = target
            asin = target.split('/dp/')[1].split('?')[0].split('/')[0] if '/dp/' in target else 'B0DZD1X83N'
        else:
            asin = target.upper()
            amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"

        try:
            prod = get_product_details_and_photos(amazon_url)
            if not prod:
                self.send_json({'status': 'error', 'message': f'Could not extract details for ASIN: {asin}'})
                return

            photos = prod.get('all_photos', [])
            winner_photo, skip = select_clean_photo_or_skip(photos)

            photo_data = []
            for p in photos:
                has_txt = has_text_annotation(p)
                has_grid = is_grid_collage(p)
                has_human = has_human_presence(p)

                status_list = []
                if has_txt: status_list.append("Text Overlay")
                if has_grid: status_list.append("Split Collage")
                if has_human: status_list.append("Human/Hand")

                status_str = f"DISCARDED ({', '.join(status_list)})" if status_list else "CLEAN"
                photo_data.append({
                    'url': p,
                    'status': status_str,
                    'is_clean': len(status_list) == 0
                })

            response = {
                'status': 'success',
                'asin': asin,
                'title': prod.get('title', f'Amazon Product {asin}'),
                'price': prod.get('price', '$19.99'),
                'rating': prod.get('rating', '4.5'),
                'winner_photo': winner_photo or (photos[0] if photos else ''),
                'should_skip': skip,
                'photos': photo_data
            }
            self.send_json(response)
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_generate(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        asin = data.get('asin')
        selected_photo = data.get('selected_photo')
        title = data.get('title', '')
        price = data.get('price', '$19.99')
        prompt_strength = data.get('prompt_strength', 0.30)

        title_clean = title.replace('"', '\\"').replace("'", "\\'")
        price_clean = price.replace('"', '\\"')

        # Run campaign generation script
        script_code = f"""
import sys
from modules.automated_product_selector import save_processed_asin
from modules.amazon_extractor import get_product_details_and_photos
from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
from modules.html_overlay_engine import render_html_overlay
from modules.vision_prompt import generate_cozy_image_prompt
from modules.seo_copywriter import generate_pin_seo_data
from modules.bridge_creator import generate_bridge_page

asin = "{asin}"
prod = {{
    'title': "{title_clean}",
    'price': "{price_clean}",
    'rating': "4.5",
    'features': ["PREMIUM QUALITY", "WARM AMBIENT GLOW", "EASY ASSEMBLY"]
}}

ref_sheet_path = create_multi_photo_reference_sheet(["{selected_photo}"], filename_prefix=f"product_{{asin}}", max_photos=1)
cozy_prompt = generate_cozy_image_prompt(prod['title'], "Room Lighting", prod['features'], ref_sheet_path, is_white_background=False)
raw_image_path = generate_cozy_image(prompt=cozy_prompt, filename_prefix=f"focus_product_{{asin}}", init_image_path="{selected_photo}", prompt_strength={prompt_strength})

seo_data = {{
    "pin_title": prod['title'],
    "image_hook": prod['title'][:30],
    "subtitle_hook": "",
    "badge_hook": "VIRAL ROOM FIND",
    "description": "Transform your space with this viral room upgrade find.",
    "suggested_board": "Cozy Room Decor",
    "keywords": ["room decor", "lighting"]
}}

hook_img_path = f"G:/CLI/pinterest-auto-affiliate/focus_product_{{asin}}_hook.jpg"
render_html_overlay(raw_image_path, seo_data['image_hook'], "", seo_data['badge_hook'], prod['price'], hook_img_path)
generate_bridge_page(prod, seo_data, asin)
save_processed_asin(asin)

import subprocess
subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"publish {{asin}} from Web Console"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)
print("SUCCESS")
"""
        temp_script = WORKSPACE_DIR / f"run_console_{asin}.py"
        with open(temp_script, "w", encoding="utf-8") as f:
            f.write(script_code)

        try:
            res = subprocess.run([sys.executable, str(temp_script)], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
            stdout_str = res.stdout or ""
            stderr_str = res.stderr or ""
            if res.returncode == 0 and "SUCCESS" in stdout_str:
                bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
                self.send_json({'status': 'success', 'bridge_url': bridge_url})
            else:
                self.send_json({'status': 'error', 'message': stderr_str or stdout_str or "Execution failed."})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})
        finally:
            if temp_script.exists():
                os.remove(temp_script)

    def send_json(self, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

def run_server():
    server = HTTPServer(('localhost', PORT), WebConsoleHandler)
    print(f"[Web Console] Server running on http://localhost:{PORT}")
    print(f"[Web Console] Open http://localhost:{PORT} in your browser to verify products & images!")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
