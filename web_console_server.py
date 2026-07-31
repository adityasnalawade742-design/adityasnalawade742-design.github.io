"""
Local Web Console Server for Product & Image Verification
Provides non-blocking background campaign generation & real-time polling API endpoints.
"""
import sys
import os
import re
import json
import time
import urllib.parse
import subprocess
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")

sys.path.append("G:/CLI/pinterest-auto-affiliate")
from modules.amazon_extractor import (
    get_product_details_and_photos,
    select_clean_photo_or_skip,
    has_text_annotation,
    is_grid_collage,
    has_human_presence
)
from modules.amazon_finder import fetch_amazon_products, TRENDING_PINTEREST_KEYWORDS
from modules.automated_product_selector import is_asin_published_on_homepage, save_processed_asin

PORT = 5000
WORKSPACE_DIR = Path("G:/CLI/pinterest-auto-affiliate")
TASK_STATUS_MAP = {}
status_lock = threading.Lock()

def update_task_status(key, data):
    with status_lock:
        TASK_STATUS_MAP[key] = data

def get_task_status(key):
    with status_lock:
        return TASK_STATUS_MAP.get(key, {'status': 'not_found'})

def process_single_campaign_in_memory(asin, selected_photo, title, price, prompt_strength=0.35):
    from modules.automated_product_selector import save_processed_asin
    from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
    from modules.html_overlay_engine import render_html_overlay
    from modules.vision_prompt import generate_cozy_image_prompt
    from modules.seo_copywriter import generate_pin_seo_data
    from modules.bridge_creator import generate_bridge_page

    prod = {
        'title': title,
        'price': price,
        'rating': "4.6",
        'features': ["PREMIUM QUALITY", "WARM AMBIENT GLOW", "EASY ASSEMBLY"]
    }

    ref_sheet_path = create_multi_photo_reference_sheet([selected_photo], filename_prefix=f"product_{asin}", max_photos=1)
    cozy_prompt = generate_cozy_image_prompt(prod['title'], "Room Decor", prod['features'], ref_sheet_path, is_white_background=False)
    raw_image_path = generate_cozy_image(prompt=cozy_prompt, filename_prefix=f"focus_product_{asin}", init_image_path=selected_photo, prompt_strength=prompt_strength)

    seo_data = generate_pin_seo_data(prod['title'], prod['price'])
    hook_img_path = str(WORKSPACE_DIR / f"focus_product_{asin}_hook.jpg")
    render_html_overlay(raw_image_path, seo_data.get('image_hook', prod['title'][:30]), "", seo_data.get('badge_hook', "VIRAL ROOM FIND"), prod['price'], hook_img_path)
    generate_bridge_page(prod, seo_data, asin)
    save_processed_asin(asin)

def run_async_generation(asin, selected_photo, title_clean, price_clean, prompt_strength):
    update_task_status(asin, {
        'status': 'processing',
        'step': 'Rendering 8K FLUX AI Image (Replicate API)...',
        'message': 'Calling FLUX-Dev model...'
    })

    try:
        process_single_campaign_in_memory(asin, selected_photo, title_clean, price_clean, prompt_strength)
        
        # Git commit & push update
        subprocess.run(["git", "add", "-A"], check=True, cwd=str(WORKSPACE_DIR))
        subprocess.run(["git", "commit", "-m", f"publish {asin} from Web Console"], check=False, cwd=str(WORKSPACE_DIR))
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(WORKSPACE_DIR))

        bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
        update_task_status(asin, {
            'status': 'success',
            'bridge_url': bridge_url,
            'message': 'Campaign generated and deployed live to GitHub Pages!'
        })
    except Exception as e:
        update_task_status(asin, {
            'status': 'error',
            'message': str(e)
        })

def run_async_batch_generation(batch_id, items):
    total = len(items)
    completed = []
    
    update_task_status(batch_id, {
        'status': 'processing',
        'current_index': 0,
        'total': total,
        'step': f'Starting batch generation for {total} selected products...',
        'completed_items': []
    })
    
    for idx, item in enumerate(items, 1):
        asin = item.get('asin')
        selected_photo = item.get('selected_photo')
        title = item.get('title', f'Product {asin}')
        price = item.get('price', '$19.99')
        prompt_strength = item.get('prompt_strength', 0.35)
        
        update_task_status(batch_id, {
            'status': 'processing',
            'current_index': idx,
            'total': total,
            'current_asin': asin,
            'step': f"[{idx}/{total}] Processing ASIN {asin} - '{title[:35]}...'",
            'completed_items': completed
        })
        
        try:
            process_single_campaign_in_memory(asin, selected_photo, title, price, prompt_strength)
            completed.append({
                'asin': asin,
                'title': title,
                'price': price,
                'hook_image': f"./focus_product_{asin}_hook.jpg",
                'bridge_url': f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
            })
            update_task_status(batch_id, {
                'status': 'processing',
                'current_index': idx,
                'total': total,
                'current_asin': asin,
                'step': f"[{idx}/{total}] Completed ASIN {asin}",
                'completed_items': completed
            })
        except Exception as e:
            print(f"[Batch Generator Error] Failed ASIN {asin}: {e}")

    # Git commit & push all batch updates to GitHub Pages
    try:
        subprocess.run(["git", "add", "-A"], check=True, cwd=str(WORKSPACE_DIR))
        subprocess.run(["git", "commit", "-m", f"publish batch {batch_id} from Web Console ({len(completed)} products)"], check=False, cwd=str(WORKSPACE_DIR))
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(WORKSPACE_DIR))
    except Exception as e_git:
        print(f"[Batch Generator Git Push Warning] {e_git}")

    update_task_status(batch_id, {
        'status': 'success',
        'current_index': total,
        'total': total,
        'step': f'Batch complete! {len(completed)} products published live.',
        'completed_items': completed
    })

    TASK_STATUS_MAP[batch_id]['status'] = 'success'
    TASK_STATUS_MAP[batch_id]['step'] = f"Successfully generated and published {len(completed)} products live to GitHub Pages!"


class WebConsoleHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WORKSPACE_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == '/' or parsed.path == '/console':
            self.path = '/admin_console.html'
            return super().do_GET()
        elif parsed.path == '/api/homepage_products':
            self.handle_api_homepage_products()
            return
        elif parsed.path == '/api/extract':
            self.handle_api_extract(parsed.query)
            return
        elif parsed.path == '/api/discover':
            self.handle_api_discover(parsed.query)
            return
        elif parsed.path == '/api/task_status':
            self.handle_api_status(parsed.query)
            return
        elif parsed.path == '/api/batch_status':
            self.handle_api_batch_status(parsed.query)
            return
        elif parsed.path == '/api/global_tag_defaults':
            self.handle_api_get_global_defaults()
            return
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/generate'):
            self.handle_api_generate()
            return
        elif self.path.startswith('/api/batch_extract'):
            self.handle_api_batch_extract()
            return
        elif self.path.startswith('/api/batch_generate'):
            self.handle_api_batch_generate()
            return
        elif self.path.startswith('/api/delete_homepage_product'):
            self.handle_api_delete_homepage_product()
            return
        elif self.path.startswith('/api/preview_overlay'):
            self.handle_api_preview_overlay()
            return
        elif self.path.startswith('/api/sync_prices'):
            self.handle_api_sync_prices()
            return
        elif self.path.startswith('/api/customize_tag'):
            self.handle_api_customize_tag()
            return
        elif self.path.startswith('/api/save_global_defaults'):
            self.handle_api_save_global_defaults()
            return
        else:
            self.send_error(404, "Endpoint not found")

    def handle_api_homepage_products(self):
        try:
            index_path = WORKSPACE_DIR / "index.html"
            reg_path = WORKSPACE_DIR / "product_price_registry.json"
            
            reg_data = {}
            if reg_path.exists():
                try: reg_data = json.loads(reg_path.read_text(encoding="utf-8"))
                except Exception: pass

            products = []
            seen = set()
            if index_path.exists():
                html = index_path.read_text(encoding="utf-8")
                card_matches = re.findall(r'id="card-([A-Za-z0-9_]{5,15})"', html)
                for asin in card_matches:
                    if asin in seen:
                        continue
                    seen.add(asin)
                    meta = reg_data.get(asin, {})
                    
                    title = meta.get('title') or f"Product {asin}"
                    price = meta.get('current_price') or meta.get('price') or "$19.99"
                    image = f"./focus_product_{asin}_hook.jpg"

                    products.append({
                        'asin': asin,
                        'title': title,
                        'price': price,
                        'image': image,
                        'bridge_url': f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
                    })

            self.send_json({'status': 'success', 'count': len(products), 'products': products})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_delete_homepage_product(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        asin = data.get('asin', '').strip()

        if not asin:
            self.send_json({'status': 'error', 'message': 'Missing ASIN'})
            return

        try:
            from delete_product import delete_product
            delete_product(asin)
            self.send_json({'status': 'success', 'message': f'Product {asin} deleted and updated live on homepage!'})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_preview_overlay(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        image_url = data.get('image_url', '')
        title = data.get('title', 'VIRAL ROOM FIND')
        subtitle = data.get('subtitle', '')
        badge = data.get('badge', 'VIRAL ROOM FIND')
        price = data.get('price', '$19.99')

        try:
            from modules.html_overlay_engine import render_html_overlay
            scratch_dir = WORKSPACE_DIR / "scratch"
            scratch_dir.mkdir(parents=True, exist_ok=True)
            preview_img = scratch_dir / "preview_overlay.jpg"
            
            # Render temporary preview
            render_html_overlay(image_url, title, subtitle, badge, price, str(preview_img))
            self.send_json({'status': 'success', 'preview_url': f"/scratch/preview_overlay.jpg?v={int(time.time())}"})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_sync_prices(self):
        try:
            # Execute master regional scraper suite across all 21 Amazon domains
            def run_sync():
                update_task_status('global_sync', {'status': 'running', 'message': 'Scraping 21 Amazon domains and re-rendering badges...'})
                sync_script = str(WORKSPACE_DIR / "sync_all_regional_prices_master.py")
                res = subprocess.run([sys.executable, sync_script], capture_output=True, text=True, cwd=str(WORKSPACE_DIR))
                if res.returncode == 0:
                    update_task_status('global_sync', {'status': 'completed', 'message': '100% Price Sync & Badge Re-rendering Complete!'})
                else:
                    update_task_status('global_sync', {'status': 'error', 'message': res.stderr[:200]})

            update_task_status('global_sync', {'status': 'running', 'message': 'Launching 21-Domain Price Sync Pipeline...'})
            t = threading.Thread(target=run_sync)
            t.daemon = True
            t.start()
            
            self.send_json({
                'status': 'success', 
                'task_key': 'global_sync',
                'message': 'Master 21-Domain Regional Price Sync Pipeline Launched! Scraping all regional storefronts and deploying live...'
            })
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_status(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        asin = params.get('asin', [''])[0].strip()
        status_info = get_task_status(asin)
        self.send_json(status_info)

    def handle_api_batch_status(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        batch_id = params.get('batch_id', [''])[0].strip()
        status_info = get_task_status(batch_id)
        self.send_json(status_info)

    def handle_api_discover(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        kw = params.get('query', [''])[0].strip() or "aesthetic room decor lamp"
        count = int(params.get('count', [10])[0])

        print(f"[Web Console] Discovering live items for query: '{kw}'...")
        try:
            raw_items = fetch_amazon_products(query=kw, num_results=count)
            items = []
            for item in raw_items:
                asin = item.get('id')
                already_pub = is_asin_published_on_homepage(asin)
                items.append({
                    'asin': asin,
                    'title': item.get('title'),
                    'price': item.get('price'),
                    'rating': item.get('rating'),
                    'reviews_count': item.get('reviews_count', 100),
                    'thumbnail': item.get('original_image_url'),
                    'is_already_published': already_pub
                })
            self.send_json({'status': 'success', 'query': kw, 'items': items})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

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

            already_published = is_asin_published_on_homepage(asin)

            response = {
                'status': 'success',
                'asin': asin,
                'title': prod.get('title', f'Amazon Product {asin}'),
                'price': prod.get('price', '$19.99'),
                'rating': prod.get('rating', '4.5'),
                'winner_photo': winner_photo or (photos[0] if photos else ''),
                'should_skip': skip,
                'is_already_published': already_published,
                'photos': photo_data
            }
            self.send_json(response)
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_batch_extract(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        asins = data.get('asins', [])

        extracted_batch = []
        for asin in asins:
            amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"
            try:
                prod = get_product_details_and_photos(amazon_url)
                if not prod:
                    continue
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

                extracted_batch.append({
                    'asin': asin,
                    'title': prod.get('title'),
                    'price': prod.get('price', '$19.99'),
                    'rating': prod.get('rating', '4.5'),
                    'winner_photo': winner_photo or (photos[0] if photos else ''),
                    'should_skip': skip,
                    'photos': photo_data
                })
            except Exception as e:
                print(f"[Batch Extract Error] Failed {asin}: {e}")

        self.send_json({'status': 'success', 'items': extracted_batch})

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

        t = threading.Thread(
            target=run_async_generation,
            args=(asin, selected_photo, title_clean, price_clean, prompt_strength),
            daemon=True
        )
        t.start()

        self.send_json({
            'status': 'processing',
            'asin': asin,
            'message': 'Campaign generation started in background process.'
        })

    def handle_api_batch_generate(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        items = data.get('items', [])

        batch_id = f"batch_{int(time.time())}"

        t = threading.Thread(
            target=run_async_batch_generation,
            args=(batch_id, items),
            daemon=True
        )
        t.start()

    def handle_api_customize_tag(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            asin = data.get('asin')
            tag_width = int(data.get('tag_width', 380))
            tag_height = int(data.get('tag_height', 285))
            tag_rotation = int(data.get('tag_rotation', -6))
            tag_color = data.get('tag_color', None)
            price_text_color = data.get('price_text_color', None)
            price_font_scale = float(data.get('price_font_scale', 0.38))
            price_text_offset_x = int(data.get('price_text_offset_x', 0))
            price_text_offset_y = int(data.get('price_text_offset_y', 15))
            tag_pos_x = float(data['tag_pos_x']) if 'tag_pos_x' in data and data['tag_pos_x'] is not None else None
            tag_pos_y = float(data['tag_pos_y']) if 'tag_pos_y' in data and data['tag_pos_y'] is not None else None
            price_text_pos_x = float(data['price_text_pos_x']) if 'price_text_pos_x' in data and data['price_text_pos_x'] is not None else None
            price_text_pos_y = float(data['price_text_pos_y']) if 'price_text_pos_y' in data and data['price_text_pos_y'] is not None else None
            headline_pos_y = float(data['headline_pos_y']) if 'headline_pos_y' in data and data['headline_pos_y'] is not None else None
            headline_color = data.get('headline_color', None)
            headline_size_px = int(data['headline_size_px']) if 'headline_size_px' in data and data['headline_size_px'] is not None else None

            reg_path = WORKSPACE_DIR / "product_price_registry.json"
            reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
            meta = reg.get(asin, {})

            raw_img = meta.get('raw_image') or f"raw_images/raw_{asin}.jpg"
            raw_full = WORKSPACE_DIR / raw_img
            if not raw_full.exists():
                raw_img = "raw_images/birds_cute.jpg" if asin == "B0D8P8CSYP" else "raw_images/raw_B0BZXNSW5K.jpg"

            output_img = meta.get('hook_image') or f"focus_product_{asin}_hook.jpg"

            from modules.html_overlay_engine import render_html_overlay
            render_html_overlay(
                image_path=str(WORKSPACE_DIR / raw_img),
                headline=meta.get('headline', meta.get('title', 'Luxury Room Product')),
                subtitle="",
                badge_text=meta.get('badge', 'VIRAL FIND'),
                price_str=meta.get('current_price', '$19.99'),
                features=meta.get('features', []),
                output_path=str(WORKSPACE_DIR / output_img),
                tag_width_px=tag_width,
                tag_height_px=tag_height,
                tag_rotation_deg=tag_rotation,
                tag_pos_x=tag_pos_x,
                tag_pos_y=tag_pos_y,
                tag_bg_hex=tag_color,
                price_text_color=price_text_color,
                price_font_scale=price_font_scale,
                headline_pos_y=headline_pos_y,
                headline_color=headline_color,
                headline_size_px=headline_size_px,
                price_text_offset_x=price_text_offset_x,
                price_text_offset_y=price_text_offset_y,
                price_text_pos_x=price_text_pos_x,
                price_text_pos_y=price_text_pos_y
            )

            # Update cache-busted v param in bridge page and index.html
            v_tag = f"v={int(time.time())}"
            bridge_file = WORKSPACE_DIR / f"bridge_{asin}.html"
            if bridge_file.exists():
                txt = bridge_file.read_text(encoding="utf-8")
                txt = re.sub(r"src=\"\./focus_product_" + asin + r"_hook\.jpg(\?v=[^\"]*)?\"", f'src="./focus_product_{asin}_hook.jpg?{v_tag}"', txt)
                bridge_file.write_text(txt, encoding="utf-8")

            index_file = WORKSPACE_DIR / "index.html"
            if index_file.exists():
                txt = index_file.read_text(encoding="utf-8")
                txt = re.sub(r"src=\"\./focus_product_" + asin + r"_hook\.jpg(\?v=[^\"]*)?\"", f'src="./focus_product_{asin}_hook.jpg?{v_tag}"', txt)
                index_file.write_text(txt, encoding="utf-8")

            # Auto-push updated image and HTML files to GitHub Pages live in background thread
            def push_to_github_pages(target_asin, target_output):
                try:
                    import subprocess
                    print(f"[Auto Git Deploy] 🚀 Deploying re-rendered graphic {target_output} to GitHub Pages...")
                    subprocess.run(["git", "add", target_output, "index.html", f"bridge_{target_asin}.html", "price tags/stamped_ambient_tag.png"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "commit", "-m", f"auto: publish re-rendered graphic for {target_asin} to GitHub Pages"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "push", "origin", "main"], cwd=str(WORKSPACE_DIR), check=False)
                    print(f"[Auto Git Deploy] ✅ Published live to GitHub Pages: https://adityasnalawade742-design.github.io/bridge_{target_asin}.html")
                except Exception as e_git:
                    print(f"[Auto Git Deploy] ⚠️ Git push warning: {e_git}")

            import threading
            threading.Thread(target=push_to_github_pages, args=(asin, output_img), daemon=True).start()

            self.send_json({'status': 'success', 'asin': asin, 'v_tag': v_tag, 'image': f"./{output_img}?{v_tag}", 'github_url': f"https://adityasnalawade742-design.github.io/bridge_{asin}.html?{v_tag}", 'message': 'changed published'})
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[Customize Tag Error] {e}")
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_get_global_defaults(self):
        try:
            defaults_path = WORKSPACE_DIR / "global_tag_defaults.json"
            if defaults_path.exists():
                data = json.loads(defaults_path.read_text(encoding="utf-8"))
            else:
                data = {"tag_width": 380, "tag_height": 514, "tag_rotation": -6, "tag_color": "#fb8500", "price_text_color": "#111827", "price_font_scale": 0.20, "price_text_offset_x": 0, "price_text_offset_y": 0, "price_text_pos_x": 50.0, "price_text_pos_y": 58.0, "tag_pos_x": 61.0, "tag_pos_y": 75.0}
            self.send_json({"status": "success", "defaults": data})
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)})

    def handle_api_save_global_defaults(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            defaults_path = WORKSPACE_DIR / "global_tag_defaults.json"
            defaults_path.write_text(json.dumps(data, indent=4), encoding="utf-8")
            print("[Global Defaults] ⭐ Saved new system-wide price tag default settings!")

            # Auto-commit and push updated global_tag_defaults.json
            def push_defaults():
                try:
                    import subprocess
                    subprocess.run(["git", "add", "global_tag_defaults.json"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "commit", "-m", "feat: save new system-wide price tag layout defaults"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "push", "origin", "main"], cwd=str(WORKSPACE_DIR), check=False)
                except Exception: pass
            import threading
            threading.Thread(target=push_defaults, daemon=True).start()

            self.send_json({"status": "success", "message": "Saved as default for all future products!"})
        except Exception as e:
            self.send_json({"status": "error", "message": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_json(self, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

from socketserver import ThreadingMixIn

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

def run_server():
    candidate_ports = [5000, 5001, 8080, 8081]
    server = None
    active_port = PORT
    for p in candidate_ports:
        try:
            server = ThreadedHTTPServer(('localhost', p), WebConsoleHandler)
            active_port = p
            break
        except OSError:
            continue

    if not server:
        server = ThreadedHTTPServer(('localhost', 0), WebConsoleHandler)
        active_port = server.server_address[1]

    print(f"[Web Console] Threaded Server running on http://localhost:{active_port}")
    print(f"[Web Console] Open http://localhost:{active_port} in your browser to verify products & images!")
    server.serve_forever()

if __name__ == '__main__':
    run_server()

