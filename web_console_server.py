"""
Local Web Console Server for Product & Image Verification
Provides non-blocking background campaign generation & real-time polling API endpoints.
"""
import sys
import os
import re
import json
import time
import urllib
import urllib.parse
import urllib.request
import subprocess
import threading
from collections import OrderedDict
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")

_PROJECT_ROOT = Path(__file__).resolve().parent  # C1 FIX: dynamic — works regardless of where project lives
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
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
WORKSPACE_DIR = _PROJECT_ROOT  # C1 FIX: uses dynamic root above
TASK_STATUS_MAP = OrderedDict()  # OPT-2 FIX: OrderedDict for bounded eviction
TASK_STATUS_MAX = 200            # OPT-2 FIX: evict oldest after 200 entries
status_lock = threading.Lock()

def update_task_status(key, data):
    with status_lock:
        TASK_STATUS_MAP[key] = data
        # OPT-2 FIX: evict oldest entry if map exceeds max size
        if len(TASK_STATUS_MAP) > TASK_STATUS_MAX:
            TASK_STATUS_MAP.popitem(last=False)

def get_task_status(key):
    with status_lock:
        return TASK_STATUS_MAP.get(key, {'status': 'not_found'})

def process_single_campaign_in_memory(asin, selected_photo, title, price, prompt_strength=0.35):
    from modules.automated_product_selector import save_processed_asin
    from modules.image_generator import create_multi_photo_reference_sheet, generate_cozy_image
    from modules.html_overlay_engine import render_html_overlay
    from modules.vision_prompt import generate_cozy_image_prompt
    from modules.seo_copywriter import generate_pin_seo_data
    from modules.bridge_creator import generate_bridge_page    # Load product_price_registry.json metadata if available
    reg_path = WORKSPACE_DIR / "product_price_registry.json"
    meta = {}
    if reg_path.exists():
        try:
            reg_data = json.loads(reg_path.read_text(encoding="utf-8"))
            meta = reg_data.get(asin, {})
        except Exception:
            pass

    prod = {
        'title': title or meta.get('title', f'Product {asin}'),
        'price': price or meta.get('current_price', '$19.99'),
        'rating': meta.get('rating', '4.6'),
        'features': meta.get('features', ["PREMIUM QUALITY", "WARM AMBIENT GLOW", "EASY ASSEMBLY"]),
        'description': meta.get('description', ''),
        'regional_prices': meta.get('regional_prices', {}),
        'direct_regions': meta.get('direct_regions', ['US'])
    }

    ref_sheet_path = create_multi_photo_reference_sheet([selected_photo], filename_prefix=f"product_{asin}", max_photos=1)
    cozy_prompt = generate_cozy_image_prompt(prod['title'], "Room Decor", prod['features'], ref_sheet_path, is_white_background=False)
    raw_image_path = generate_cozy_image(prompt=cozy_prompt, filename_prefix=f"focus_product_{asin}", init_image_path=selected_photo, prompt_strength=prompt_strength)

    seo_data = generate_pin_seo_data(prod['title'], prod['price'])
    hook_img_path = str(WORKSPACE_DIR / f"focus_product_{asin}_hook.jpg")
    render_html_overlay(
        image_path=raw_image_path,
        headline=seo_data.get('image_hook', prod['title'][:30]),
        subtitle="",
        badge_text=seo_data.get('badge_hook', "VIRAL ROOM FIND"),
        price_str=prod['price'],
        features=seo_data.get('features', prod['features']),
        output_path=hook_img_path
    )

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
        subprocess.run(["git", "add", "-A"], check=False, cwd=str(WORKSPACE_DIR), timeout=60)
        subprocess.run(["git", "commit", "-m", f"publish {asin} from Web Console"], check=False, cwd=str(WORKSPACE_DIR), timeout=60)
        push_res = subprocess.run(["git", "push", "origin", "main"], check=False, cwd=str(WORKSPACE_DIR), timeout=60)

        bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
        if push_res.returncode != 0:
            print(f"[Git Push Warning] Push returned non-zero exit code ({push_res.returncode}). Campaign is ready locally.")
            update_task_status(asin, {
                'status': 'success_local',
                'bridge_url': bridge_url,
                'message': 'Campaign generated locally! Git push failed — please push manually.'
            })
        else:
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
                'completed_items': list(completed)
            })
        except Exception as e:
            print(f"[Batch Generator Error] Failed ASIN {asin}: {e}")

    # Git commit & push all batch updates to GitHub Pages
    try:
        subprocess.run(["git", "add", "-A"], check=True, cwd=str(WORKSPACE_DIR), timeout=60)
        subprocess.run(["git", "commit", "-m", f"publish batch {batch_id} from Web Console ({len(completed)} products)"], check=False, cwd=str(WORKSPACE_DIR), timeout=60)
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=str(WORKSPACE_DIR), timeout=60)
    except Exception as e_git:
        print(f"[Batch Generator Git Push Warning] {e_git}")

    update_task_status(batch_id, {
        'status': 'success',
        'current_index': total,
        'total': total,
        'step': f'Batch complete! {len(completed)} products published live to GitHub Pages!',
        'completed_items': completed
    })


def _scrape_first_product_image(asin: str) -> str:
    """
    Fast scraper — grabs the FIRST hero image from the Amazon product page.
    No pixel analysis, no scoring, no detection. Just the raw image URL.
    Used during discovery so the response is instant.
    Returns a https://m.media-amazon.com/... URL or empty string on failure.
    """
    import urllib.request as _urlreq
    clean = asin.strip().upper()
    url = f"https://www.amazon.com/dp/{clean}"
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    ]
    for ua in user_agents:
        try:
            req = _urlreq.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
            with _urlreq.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Strategy A: og:image meta tag — most reliable, always high-res
            og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\'<>]+)["\']', html)
            if og:
                img = og.group(1).strip()
                if "m.media-amazon.com" in img:
                    # Strip resize tokens to get full SL1500 resolution
                    img = re.sub(r'\._[A-Za-z0-9_,%-]+\.', '._AC_SL1500_.', img)
                    print(f"[Fast Scraper] og:image found for {clean}: ...{img[-40:]}")
                    return img

            # Strategy B: data-a-dynamic-image JSON blob
            dyn = re.search(r'data-a-dynamic-image=["\']({[^"\'<>]+})["\']', html)
            if dyn:
                try:
                    img_map = json.loads(dyn.group(1).replace("&quot;", '"'))
                    if img_map:
                        # Pick the entry with the largest width dimension
                        best = max(img_map.items(), key=lambda kv: (kv[1][0] if isinstance(kv[1], list) and kv[1] else 0))
                        best_url = re.sub(r'\._[A-Za-z0-9_,%-]+\.', '._AC_SL1500_.', best[0])
                        print(f"[Fast Scraper] dynamic-image found for {clean}: ...{best_url[-40:]}")
                        return best_url
                except Exception:
                    pass

            # Strategy C: first m.media-amazon.com /images/I/ URL in page HTML
            med = re.search(r"(https://m\.media-amazon\.com/images/I/[A-Za-z0-9%_\-\.]+\.jpg)", html)
            if med:
                img = re.sub(r'\._[A-Za-z0-9_,%-]+\.', '._AC_SL1500_.', med.group(0))
                print(f"[Fast Scraper] regex match found for {clean}: ...{img[-40:]}")
                return img
        except Exception as e:
            print(f"[Fast Scraper] attempt failed for {clean} ({ua[:30]}...): {e}")

    print(f"[Fast Scraper] No image found for {clean}")
    return ""


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
        elif parsed.path == '/api/fetch_image':
            self.handle_api_fetch_image(parsed.query)
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
        elif parsed.path == '/api/matrix':
            # BUG FIX: matrix was only in do_POST but frontend calls it via GET
            self.handle_api_matrix()
            return
        elif parsed.path == '/api/campaign_tracker':
            # BUG FIX: campaign_tracker was only in do_POST but should be GET
            self.handle_api_campaign_tracker()
            return
        elif parsed.path == '/api/logs':
            # BUG FIX: logs was only in do_POST but should also support GET
            self.handle_api_logs()
            return
        elif parsed.path in ('/api/create_bridge_page', '/api/create-bridge-page'):
            self.handle_api_create_bridge_page()
            return
        elif parsed.path == '/api/auth/pinterest':
            self.handle_api_auth_pinterest()
            return
        elif parsed.path == '/api/auth/callback':
            self.handle_api_auth_callback(parsed.query)
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
        elif self.path.startswith('/api/n8n/dispatch-batch'):
            self.handle_api_dispatch_n8n_batch()
            return
        elif self.path.startswith('/api/prepare_n8n_batch'):
            # NEW: Packages user-confirmed selections into a clean n8n payload (no generation)
            self.handle_api_prepare_n8n_batch()
            return
        elif self.path.startswith('/api/proxy_n8n_webhook'):
            self.handle_api_proxy_n8n_webhook()
            return
        elif self.path.startswith('/api/create_bridge_page'):
            # NEW: Called by n8n per-product to build bridge page + hook image then push live
            self.handle_api_create_bridge_page()
            return
        elif self.path.startswith('/api/delete_homepage_product'):
            self.handle_api_delete_homepage_product()
            return
        elif self.path.startswith('/api/reject_product'):
            self.handle_api_reject_product()
            return
        elif self.path.startswith('/api/confirm_published'):
            self.handle_api_confirm_published()
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
        elif self.path.startswith('/api/matrix'):
            self.handle_api_matrix()
            return
        elif self.path.startswith('/api/audit_links'):
            self.handle_api_audit_links()
            return
        elif self.path.startswith('/api/rerender_badges'):
            self.handle_api_rerender_badges()
            return
        elif self.path.startswith('/api/campaign_tracker'):
            self.handle_api_campaign_tracker()
            return
        elif self.path.startswith('/api/logs'):
            self.handle_api_logs()
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
            v_stamp = int(time.time())  # BUG 5 FIX: cache-bust all hook images
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
                    image = f"./focus_product_{asin}_hook.jpg?v={v_stamp}"

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
        data = json.loads(body.decode('utf-8')) if content_length > 0 else {}
        asin = data.get('asin', '').strip()

        if not asin:
            self.send_json({'status': 'error', 'message': 'Missing ASIN'})
            return

        # BUG FIX: verify ASIN exists in registry before attempting delete
        # Previously delete_product() silently did nothing for unknown ASINs and we still returned success
        reg_file = WORKSPACE_DIR / 'product_price_registry.json'
        try:
            reg = json.loads(reg_file.read_text(encoding='utf-8')) if reg_file.exists() else {}
        except Exception:
            reg = {}
        index_file = WORKSPACE_DIR / 'index.html'
        in_index = False
        if index_file.exists():
            try:
                in_index = f'id="card-{asin}"' in index_file.read_text(encoding='utf-8')
            except Exception:
                pass
        if asin not in reg and not in_index:
            self.send_json({'status': 'error', 'message': f'Product {asin} not found in homepage or registry. Nothing to delete.'})
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
        features = data.get('features', [])

        # BUG FIX: guard against empty image_url before attempting download/render
        if not image_url:
            self.send_json({'status': 'error', 'message': 'Missing image_url. Please provide a photo URL to preview the overlay.'})
            return

        try:
            from modules.html_overlay_engine import render_html_overlay
            import urllib.request as _urlreq
            scratch_dir = WORKSPACE_DIR / "scratch"
            scratch_dir.mkdir(parents=True, exist_ok=True)
            preview_img = scratch_dir / "preview_overlay.jpg"

            # BUG C FIX: render_html_overlay expects a LOCAL file path, not a remote URL.
            # Download the remote image to a temp file first if it is a URL.
            if image_url.startswith('http'):
                tmp_src = scratch_dir / "preview_source_tmp.jpg"
                req = _urlreq.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                with _urlreq.urlopen(req, timeout=12) as resp:
                    tmp_src.write_bytes(resp.read())
                local_image_path = str(tmp_src)
            else:
                local_image_path = image_url  # already a local path

            # BUG 2 FIX: pass features= and output_path= as kwargs to avoid positional mismatch
            render_html_overlay(
                image_path=local_image_path,
                headline=title,
                subtitle=subtitle,
                badge_text=badge,
                price_str=price,
                features=features,
                output_path=str(preview_img)
            )
            self.send_json({'status': 'success', 'preview_url': f"/scratch/preview_overlay.jpg?v={int(time.time())}"})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_sync_prices(self):
        try:
            sync_script = WORKSPACE_DIR / "sync_all_regional_prices_master.py"
            if not sync_script.exists():
                self.send_json({'status': 'error', 'message': 'sync_all_regional_prices_master.py not found in project root.'})
                return

            def run_sync():
                # BUG-8 FIX: reset status first so re-runs don't get instant false-positive 'completed'
                update_task_status('global_sync', {'status': 'idle', 'message': 'Initializing...'})
                update_task_status('global_sync', {'status': 'running', 'message': 'Launching 21-Domain Price Sync...'})
                log_file_path = WORKSPACE_DIR / "server.log"
                
                with open(log_file_path, "a", encoding="utf-8") as log_f:
                    log_f.write(f"\n--- Launching 21-Domain Price Sync Pipeline [{time.strftime('%Y-%m-%d %H:%M:%S')}] ---\n")
                    log_f.flush()
                    
                    proc = subprocess.Popen(
                        [sys.executable, str(sync_script)],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        cwd=str(WORKSPACE_DIR),
                        bufsize=1
                    )
                    
                    for line in proc.stdout:
                        log_f.write(line)
                        log_f.flush()
                        clean_line = line.strip()
                        if clean_line:
                            update_task_status('global_sync', {
                                'status': 'running',
                                'message': clean_line[:80]
                            })
                    
                    proc.wait()
                    if proc.returncode == 0:
                        update_task_status('global_sync', {
                            'status': 'completed',
                            'message': '100% Price Sync & Badge Re-rendering Complete!'
                        })
                    else:
                        update_task_status('global_sync', {
                            'status': 'error',
                            'message': f'Sync exited with code {proc.returncode}'
                        })

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

    def handle_api_matrix(self):
        try:
            mat_file = WORKSPACE_DIR / "global_direct_matrix.json"
            reg_file = WORKSPACE_DIR / "product_price_registry.json"
            mat_data = json.loads(mat_file.read_text(encoding="utf-8")) if mat_file.exists() else {}
            reg_data = json.loads(reg_file.read_text(encoding="utf-8")) if reg_file.exists() else {}
            self.send_json({'status': 'success', 'matrix': mat_data, 'registry': reg_data})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_audit_links(self):
        try:
            # BUG-3 FIX: was pointing to non-existent scratch/master_zero_404_audit.py
            audit_script = str(WORKSPACE_DIR / "validate_all_affiliate_urls.py")
            # BUG FIX: was blocking server thread — now runs in background, returns task key for polling
            task_key = 'audit_links'
            update_task_status(task_key, {'status': 'running', 'message': 'Audit started...'})
            def run_audit():
                try:
                    res = subprocess.run([sys.executable, audit_script], capture_output=True, text=True, cwd=str(WORKSPACE_DIR))
                    update_task_status(task_key, {'status': 'completed', 'output': res.stdout[-3000:]})
                except Exception as e_a:
                    update_task_status(task_key, {'status': 'error', 'message': str(e_a)})
            threading.Thread(target=run_audit, daemon=True).start()
            self.send_json({'status': 'success', 'task_key': task_key, 'message': 'Audit started in background. Poll /api/task_status?asin=audit_links for result.'})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_rerender_badges(self):
        try:
            rerender_script = str(WORKSPACE_DIR / "daily_price_updater.py")
            # BUG FIX: was blocking server thread — now runs in background, returns task key for polling
            task_key = 'rerender_badges'
            update_task_status(task_key, {'status': 'running', 'message': 'Badge re-render started...'})
            def run_rerender():
                try:
                    res = subprocess.run([sys.executable, rerender_script], capture_output=True, text=True, cwd=str(WORKSPACE_DIR))
                    update_task_status(task_key, {'status': 'completed', 'message': 'All Playwright graphic price badges re-rendered successfully!', 'output': res.stdout[-3000:]})
                except Exception as e_r:
                    update_task_status(task_key, {'status': 'error', 'message': str(e_r)})
            threading.Thread(target=run_rerender, daemon=True).start()
            self.send_json({'status': 'success', 'task_key': task_key, 'message': 'Badge re-render started in background. Poll /api/task_status?asin=rerender_badges for result.'})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_campaign_tracker(self):
        try:
            tracker_file = WORKSPACE_DIR / "pinterest_campaign_tracker.json"
            data = json.loads(tracker_file.read_text(encoding="utf-8")) if tracker_file.exists() else {}
            self.send_json({'status': 'success', 'tracker': data})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_logs(self):
        try:
            log_file = WORKSPACE_DIR / "server.log"
            logs = log_file.read_text(encoding="utf-8")[-2000:] if log_file.exists() else "System running smoothly..."
            self.send_json({'status': 'success', 'logs': logs})
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
            from modules.product_registry import get_blocked_asins
            blocked_asins = get_blocked_asins()

            raw_items = fetch_amazon_products(query=kw, num_results=count)
            items = []

            raw_dir = WORKSPACE_DIR / "raw_images"
            raw_dir.mkdir(parents=True, exist_ok=True)

            def _bg_download(target_asin, src_url, dest_path):
                """Background thread: download image to raw_images/ for future use."""
                try:
                    req = urllib.request.Request(src_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
                    with urllib.request.urlopen(req, timeout=12) as resp:
                        data = resp.read()
                    if len(data) > 5000:
                        dest_path.write_bytes(data)
                        print(f"[Web Console] Cached {target_asin} image ({len(data)//1024}KB) -> {dest_path.name}")
                except Exception as e_dl:
                    print(f"[Web Console] BG download warning for {target_asin}: {e_dl}")

            from modules.automated_product_selector import get_processed_asins
            published_set = set(get_processed_asins())

            for item in raw_items:
                asin = item.get('id') or item.get('asin', '')
                if not asin or len(asin) != 10:
                    continue
                if asin in blocked_asins:
                    continue

                already_pub = asin in published_set
                local_raw = raw_dir / f"raw_{asin}.jpg"
                v = int(time.time())

                # ---- THUMBNAIL STRATEGY ----
                # Priority 1: local file already cached -> serve it instantly
                if local_raw.exists() and local_raw.stat().st_size > 5000:
                    thumbnail = f"/raw_images/raw_{asin}.jpg?v={v}"
                    print(f"[Web Console] Serving cached local image for {asin}")

                else:
                    # Priority 2: use URL already in SerpAPI result (validated HTTP 200 above)
                    candidate_url = (
                        item.get('original_image_url') or
                        item.get('thumbnail') or
                        item.get('image') or
                        ''
                    )

                    # Reject tracker/ad pixel URLs (will 1x1 or CORS-fail in browser)
                    bad = (
                        not candidate_url
                        or 'amazon-adsystem.com' in candidate_url
                        or 'ws-na.amazon-adsystem' in candidate_url
                        or '_SP100' in candidate_url
                        or '_SP200' in candidate_url
                    )

                    if bad:
                        # Priority 3: fast scrape (no scoring, no pixel analysis)
                        candidate_url = _scrape_first_product_image(asin)

                    if not candidate_url:
                        # Priority 4: SerpAPI amazon_product engine (uses 1 credit but reliable)
                        from modules.amazon_extractor import fetch_all_product_images
                        imgs = fetch_all_product_images(asin)
                        candidate_url = imgs[0] if imgs else ''

                    if not candidate_url:
                        print(f"[Web Console] No image found for {asin} — skipping")
                        continue

                    # SERVE THE CDN URL DIRECTLY TO BROWSER
                    # m.media-amazon.com URLs load fine in <img> tags with referrerpolicy=no-referrer
                    # No need to wait for local download — show image immediately.
                    thumbnail = candidate_url

                    # Download to raw_images/ in background for caching (used later by bridge builder)
                    threading.Thread(
                        target=_bg_download,
                        args=(asin, candidate_url, local_raw),
                        daemon=True
                    ).start()

                items.append({
                    'asin': asin,
                    'title': item.get('title', 'Unknown Product'),
                    'price': item.get('price', 'N/A'),
                    'rating': item.get('rating', '4.5'),
                    'reviews_count': item.get('reviews_count', 100),
                    'thumbnail': thumbnail,
                    'is_already_published': already_pub
                })

            print(f"[Web Console] Discover done: {len(items)} items ready")
            self.send_json({'status': 'success', 'query': kw, 'items': items,
                            'total_raw': len(raw_items), 'valid': len(items)})
        except Exception as e:
            import traceback; traceback.print_exc()
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_fetch_image(self, query_str):
        """GET /api/fetch_image?asin=XXXXXXXXXX[&title=...]
        Fast image fetch — no scoring/detection, just gets the first real product image.
        Returns: { status, asin, image_url } or { status: 'error', message }
        """
        params = urllib.parse.parse_qs(query_str)
        asin = params.get('asin', [''])[0].strip().upper()
        title = params.get('title', [''])[0].strip()
        if not asin or len(asin) != 10:
            self.send_json({'status': 'error', 'message': 'Invalid or missing ASIN'})
            return
        try:
            # Use the fast scraper first (no credits used, no pixel analysis)
            img = _scrape_first_product_image(asin)
            if img:
                self.send_json({'status': 'success', 'asin': asin, 'image_url': img})
                return
            # Fallback: SerpAPI amazon_product engine
            from modules.amazon_extractor import fetch_all_product_images
            imgs = fetch_all_product_images(asin)
            if imgs:
                self.send_json({'status': 'success', 'asin': asin, 'image_url': imgs[0]})
                return
            self.send_json({'status': 'not_found', 'asin': asin, 'image_url': ''})
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_extract(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        target = params.get('target', [''])[0].strip()

        if not target:
            self.send_json({'status': 'error', 'message': 'Missing target ASIN or URL'})
            return

        if target.startswith('http'):
            # BUG G FIX: return a clear error instead of silently using a hardcoded fallback ASIN
            if '/dp/' not in target:
                self.send_json({'status': 'error', 'message': 'Invalid URL — must contain /dp/{ASIN}. Please paste a direct Amazon product URL (e.g. https://www.amazon.com/dp/B0DZD1X83N).'})
                return
            amazon_url = target
            asin = target.split('/dp/')[1].split('?')[0].split('/')[0]
        else:
            asin = target.upper()
            amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-20"

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

        items_input = data.get('items', [])
        input_titles = {i['asin'].strip().upper(): i['title'] for i in items_input if isinstance(i, dict) and i.get('asin') and i.get('title')}
        input_prices = {i['asin'].strip().upper(): i['price'] for i in items_input if isinstance(i, dict) and i.get('asin') and i.get('price')}

        # BUG-1 FIX: load registry to get real title/price instead of generic placeholders
        reg_path = WORKSPACE_DIR / "product_price_registry.json"
        reg_data = {}
        if reg_path.exists():
            try:
                reg_data = json.loads(reg_path.read_text(encoding="utf-8"))
            except Exception:
                pass

        from modules.amazon_extractor import fetch_all_product_images

        def _get_best_fallback_image(asin, title=''):
            """Returns a real m.media-amazon.com image URL from cache or fresh fetch."""
            from modules.image_cache_db import get_cached_image
            from modules.amazon_finder import fetch_product_image_for_asin
            cached = get_cached_image(asin)
            if cached and cached.startswith('http') and 'amazon-adsystem' not in cached:
                return cached
            fetched = fetch_product_image_for_asin(asin, title)
            if fetched and fetched.startswith('http') and 'amazon-adsystem' not in fetched:
                return fetched
            return None

        extracted_batch = []
        for asin in asins:
            asin_clean = asin.strip().upper()
            try:
                # fetch_all_product_images tries: SerpAPI thumbnails[] -> Amazon page scrape -> SQLite cache
                photos = fetch_all_product_images(asin_clean)

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

                winner_photo, skip = select_clean_photo_or_skip(photos) if photos else ('', False)
                if not winner_photo and photos:
                    winner_photo = photos[0]

                meta = reg_data.get(asin_clean, {})
                real_title = input_titles.get(asin_clean) or meta.get('title') or f'Product {asin_clean}'
                real_price = input_prices.get(asin_clean) or meta.get('current_price') or meta.get('regional_prices', {}).get('US') or '$19.99'

                extracted_batch.append({
                    'asin': asin_clean,
                    'title': real_title,
                    'price': real_price,
                    'rating': '4.5',
                    'winner_photo': winner_photo or (photos[0] if photos else ''),
                    'should_skip': skip,
                    'photos': photo_data
                })
            except Exception as e:
                print(f"[Batch Extract Error] Failed {asin}: {e}")
                fallback_url = _get_best_fallback_image(asin_clean) or ''
                real_title = input_titles.get(asin_clean) or f'Product {asin_clean}'
                real_price = input_prices.get(asin_clean) or '$19.99'
                extracted_batch.append({
                    'asin': asin_clean,
                    'title': real_title,
                    'price': real_price,
                    'rating': '4.5',
                    'winner_photo': fallback_url,
                    'should_skip': False,
                    'photos': [{'url': fallback_url, 'status': 'CLEAN', 'is_clean': True}] if fallback_url else []
                })

        self.send_json({'status': 'success', 'items': extracted_batch})

    def handle_api_reject_product(self):
        """POST /api/reject_product — Body: { asin, title, reason }"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        asin = data.get('asin', '').strip().upper()
        title = data.get('title', '')
        reason = data.get('reason', 'user_skip')

        if not asin or not re.match(r'^[A-Z0-9]{10}$', asin):
            self.send_json({'status': 'error', 'message': 'Invalid ASIN format (must be 10 alphanumeric characters)'})
            return

        from modules.product_registry import mark_as_rejected
        mark_as_rejected(asin=asin, title=title, reason=reason)
        self.send_json({'status': 'success', 'asin': asin, 'message': f'ASIN {asin} marked as rejected.'})

    def handle_api_confirm_published(self):
        """POST /api/confirm_published — Body: { asin, title, price, pinterest_pin_id, image_url }"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))
        asin = data.get('asin', '').strip().upper()
        title = data.get('title', '')
        price = data.get('price', '$19.99')
        pinterest_pin_id = data.get('pinterest_pin_id', '')
        image_url = data.get('image_url', '')

        if not asin or not re.match(r'^[A-Z0-9]{10}$', asin):
            self.send_json({'status': 'error', 'message': 'Invalid ASIN format (must be 10 alphanumeric characters)'})
            return

        from modules.product_registry import mark_as_published
        mark_as_published(asin=asin, title=title, price=price, pinterest_pin_id=pinterest_pin_id, image_url=image_url)
        self.send_json({'status': 'success', 'asin': asin, 'message': f'ASIN {asin} marked as published.'})



    def handle_api_generate(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        asin = data.get('asin')
        selected_photo = data.get('selected_photo')
        title = data.get('title', '')
        price = data.get('price', '$19.99')
        prompt_strength = data.get('prompt_strength', 0.50)

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

        # BUG FIX: was missing send_json — browser was left hanging with no response
        self.send_json({
            'status': 'processing',
            'batch_id': batch_id,
            'message': f'Batch generation started for {len(items)} products.'
        })

    def handle_api_customize_tag(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))

            # BUG-2 FIX: load saved global defaults as fallback so user-saved settings are respected
            defaults_path = WORKSPACE_DIR / "global_tag_defaults.json"
            g_def = json.loads(defaults_path.read_text(encoding="utf-8")) if defaults_path.exists() else {}

            asin = data.get('asin')
            tag_width = int(data.get('tag_width', g_def.get('tag_width', 380)))
            tag_height = int(data.get('tag_height', g_def.get('tag_height', 285)))
            tag_rotation = int(data.get('tag_rotation', g_def.get('tag_rotation', -6)))
            tag_color = data.get('tag_color', None)
            price_text_color = data.get('price_text_color', None)
            price_font_scale = float(data.get('price_font_scale', g_def.get('price_font_scale', 0.24)))
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

            from modules.amazon_extractor import get_best_image_for_asin
            best_res = get_best_image_for_asin(asin, title=meta.get('title', ''), save_to_disk=True)
            raw_full = Path(best_res["local_path"]) if best_res and best_res.get("local_path") else WORKSPACE_DIR / f"raw_images/raw_{asin}.jpg"
            raw_img = str(raw_full.relative_to(WORKSPACE_DIR)).replace("\\", "/") if raw_full.is_relative_to(WORKSPACE_DIR) else f"raw_images/raw_{asin}.jpg"

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
                data = {"tag_width": 380, "tag_height": 285, "tag_rotation": -6, "tag_color": "#fb8500", "price_text_color": "#111827", "price_font_scale": 0.20, "price_text_offset_x": 0, "price_text_offset_y": 0, "price_text_pos_x": 50.0, "price_text_pos_y": 58.0, "tag_pos_x": 61.0, "tag_pos_y": 75.0}
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

    def handle_api_prepare_n8n_batch(self):
        """
        NEW ENDPOINT — Called by the Web Console 'Send to n8n' button.
        Receives user-confirmed product + image selections.
        Downloads chosen photos to raw_images/, generates SEO copy,
        then returns a structured payload list for n8n to iterate.
        Does NOT generate AI images or bridge pages — that happens inside n8n.
        """
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8')) if content_length > 0 else {}
            items = data.get('items', [])  # [{asin, title, price, chosen_photo_url}, ...]

            if not items:
                self.send_json({'status': 'error', 'message': 'No items in batch.'})
                return

            from modules.seo_copywriter import generate_pin_seo_data
            import urllib.request

            prepared = []
            for item in items:
                asin = item.get('asin', '').strip().upper()
                title = item.get('title', f'Product {asin}')
                price = item.get('price', '$19.99')
                chosen_photo = item.get('chosen_photo_url', '')

                # Download chosen photo locally so n8n bridge builder can use it
                raw_img_path = WORKSPACE_DIR / 'raw_images' / f'raw_{asin}.jpg'
                raw_img_path.parent.mkdir(parents=True, exist_ok=True)
                download_ok = False
                if chosen_photo and chosen_photo.startswith('http'):
                    try:
                        req = urllib.request.Request(chosen_photo, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            raw_img_path.write_bytes(resp.read())
                        download_ok = True
                        print(f'[Prepare n8n Batch] ✅ Downloaded photo for {asin} -> {raw_img_path.name}')
                    except Exception as e_dl:
                        print(f'[Prepare n8n Batch] ⚠️ Photo download warning for {asin}: {e_dl}')

                # Generate unique SEO copy per product
                seo = generate_pin_seo_data(product_title=title, price=price)

                # Load regional ASINs, prices, and direct regions from registry / matrix
                reg_asins = item.get('regional_asins', {})
                reg_prices = item.get('regional_prices', {})
                direct_regs = item.get('direct_regions', [])

                if not reg_asins or not direct_regs:
                    try:
                        reg_path = WORKSPACE_DIR / 'product_price_registry.json'
                        if reg_path.exists():
                            with open(reg_path, 'r', encoding='utf-8') as rf:
                                reg_db = json.load(rf)
                                if asin in reg_db:
                                    reg_asins = reg_asins or reg_db[asin].get('regional_asins', {})
                                    reg_prices = reg_prices or reg_db[asin].get('regional_prices', {})
                                    direct_regs = direct_regs or reg_db[asin].get('direct_regions', [])
                    except Exception:
                        pass

                if not direct_regs:
                    try:
                        g_matrix_path = WORKSPACE_DIR / 'global_direct_matrix.json'
                        if g_matrix_path.exists():
                            with open(g_matrix_path, 'r', encoding='utf-8') as mf:
                                g_mat = json.load(mf)
                                direct_regs = g_mat.get(asin, ["US"])
                    except Exception:
                        pass

                if not direct_regs:
                    direct_regs = ["US"]

                prepared.append({
                    'asin': asin,
                    'title': title,
                    'price': price,
                    'chosen_photo_url': chosen_photo,
                    'raw_image_local': str(raw_img_path) if download_ok else '',
                    'pin_title': seo.get('pin_title', title),
                    'pin_description': seo.get('description', ''),
                    'badge_hook': seo.get('badge_hook', 'VIRAL ROOM FIND'),
                    'image_hook': seo.get('image_hook', title[:30]),
                    'bridge_url': f'https://adityasnalawade742-design.github.io/bridge_{asin}.html',
                    'hook_image_url': f'https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg',
                    'regional_asins': reg_asins,
                    'regional_prices': reg_prices,
                    'direct_regions': direct_regs,
                    'create_bridge_endpoint': f'http://127.0.0.1:{self.server.server_address[1]}/api/create_bridge_page'
                })

            print(f'[Prepare n8n Batch] 📦 Packaged {len(prepared)} products ready for n8n.')
            self.send_json({
                'status': 'success',
                'message': f'✅ {len(prepared)} products packaged and ready for n8n!',
                'count': len(prepared),
                'items': prepared
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_proxy_n8n_webhook(self):
        """
        POST /api/proxy_n8n_webhook
        Proxies request to n8n webhook server-side to bypass browser CORS restrictions.
        Dispatches payload array to n8n so n8n owns 100% of node execution.
        """
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8')) if content_length > 0 else {}
            n8n_url = data.get('n8n_url') or 'http://localhost:5678/webhook/pinterest-batch'
            items = data.get('items', [])

            urls_to_try = [n8n_url]
            if '/webhook-test/' in n8n_url:
                urls_to_try.append(n8n_url.replace('/webhook-test/', '/webhook/'))
            elif '/webhook/' in n8n_url:
                urls_to_try.append(n8n_url.replace('/webhook/', '/webhook-test/'))

            print(f"[n8n Proxy] 🚀 Proxying batch of {len(items)} items to n8n webhook ({urls_to_try[0]})...")

            for item in items:
                asin = item.get('asin')
                if asin:
                    update_task_status(asin, {
                        'status': 'processing',
                        'step': 'Dispatched to n8n Workflow — executing nodes...',
                        'message': 'n8n active pipeline processing...'
                    })

            # Forward payload to n8n server-side (no CORS restriction)
            req_data = json.dumps({'items': items, 'body': {'items': items}}).encode('utf-8')
            n8n_status = 500
            success_url = None

            import urllib.error
            for url in urls_to_try:
                try:
                    req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                    with urllib.request.urlopen(req, timeout=10) as resp:
                        n8n_status = resp.status
                        resp_text = resp.read().decode('utf-8', errors='ignore')
                        if 'no test execution was listening' in resp_text.lower():
                            print(f"[n8n Proxy Warning] {url} returned 'no test execution listening'. Trying fallback...")
                            continue
                        success_url = url
                        print(f"[n8n Proxy] ✅ Server-side dispatch to n8n ({url}) returned HTTP {n8n_status}")
                        break
                except urllib.error.HTTPError as e_http:
                    print(f"[n8n Proxy Warning] {url} returned HTTP {e_http.code}. Trying fallback...")
                    n8n_status = e_http.code
                except Exception as e_proxy:
                    print(f"[n8n Proxy Warning] Could not reach n8n URL '{url}': {e_proxy}")

            if success_url:
                self.send_json({
                    'status': 'success',
                    'n8n_status': n8n_status,
                    'target_url': success_url,
                    'message': f'Batch of {len(items)} items proxied to n8n workflow ({success_url})!'
                })
            else:
                self.send_json({
                    'status': 'warning',
                    'n8n_status': n8n_status,
                    'message': f'Could not reach n8n webhook at {n8n_url}. Please activate the workflow in n8n (toggle ON in top right) or paste your exact n8n Webhook URL.'
                })
        except Exception as e:
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_create_bridge_page(self):
        """
        NEW ENDPOINT — Called by n8n per-product (HTTP Request node).
        Builds the bridge landing page + renders the hook image with price overlay,
        commits to git, pushes to GitHub Pages, and returns the live URLs.
        """
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8')) if content_length > 0 else {}

            asin = data.get('asin', '').strip().upper()
            if not asin:
                parsed_url = urllib.parse.urlparse(self.path)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                asin = query_params.get('asin', [''])[0].strip().upper()
                if not data:
                    data = {k: v[0] for k, v in query_params.items() if v}

            title = data.get('title', f'Product {asin}')
            price = data.get('price', '$19.99')
            pin_title = data.get('pin_title', title)
            pin_description = data.get('pin_description', '')
            badge_hook = data.get('badge_hook', 'VIRAL ROOM FIND')
            image_hook = data.get('image_hook', title[:30])
            regional_asins = data.get('regional_asins', {})
            regional_prices = data.get('regional_prices', {})
            direct_regions = data.get('direct_regions', ['US'])

            if not asin:
                self.send_json({'status': 'error', 'message': 'Missing ASIN'})
                return

            print(f'[Create Bridge Page] 🔨 Building bridge_{asin}.html + hook image...')

            reg_file = WORKSPACE_DIR / 'product_price_registry.json'
            reg_entry = {}
            registry_all = {}
            if reg_file.exists():
                try:
                    with open(reg_file, 'r', encoding='utf-8') as rf:
                        registry_all = json.load(rf)
                        reg_entry = registry_all.get(asin, {})
                except Exception as e_rf:
                    print(f"[Create Bridge Page] Registry load error: {e_rf}")

            # Title cleaning logic: reject placeholder titles and cross-contaminated copy
            raw_title = data.get('title', '').strip()
            raw_pin_title = data.get('pin_title', '').strip()
            raw_image_hook = data.get('image_hook', '').strip()
            
            clean_title = reg_entry.get('title', '').strip()
            if not clean_title or clean_title.startswith('Product B0') or clean_title.startswith('Product ') or ('Fenmzee' in clean_title and asin != 'B0BPNXX2MF'):
                if raw_title and not raw_title.startswith('Product B0') and not raw_title.startswith('Product ') and ('Fenmzee' not in raw_title or asin == 'B0BPNXX2MF'):
                    clean_title = raw_title
                elif raw_image_hook and not raw_image_hook.startswith('Product B0') and ('Fenmzee' not in raw_image_hook or asin == 'B0BPNXX2MF'):
                    clean_title = raw_image_hook
                elif raw_pin_title and not raw_pin_title.startswith('Product B0') and ('Fenmzee' not in raw_pin_title or asin == 'B0BPNXX2MF'):
                    clean_title = raw_pin_title
                else:
                    try:
                        from modules.amazon_extractor import get_best_image_for_asin
                        fetched_info = get_best_image_for_asin(asin, save_to_disk=True)
                        if fetched_info and fetched_info.get('title') and not fetched_info.get('title').startswith('Product B0'):
                            clean_title = fetched_info.get('title')
                    except Exception:
                        pass
                    if not clean_title or clean_title.startswith('Product B0') or ('Fenmzee' in clean_title and asin != 'B0BPNXX2MF'):
                        clean_title = f"Aesthetic Decor Find {asin}"
            title = clean_title

            # Price normalization & lookup: if price is missing or defaulted to $19.99, fetch real Amazon price
            price = reg_entry.get('current_price') or data.get('price') or ''
            price_str = str(price).strip()
            if not price_str or price_str in ['$19.99', '19.99', '.99']:
                try:
                    from modules.amazon_extractor import get_best_image_for_asin
                    fetched_info = get_best_image_for_asin(asin, save_to_disk=False)
                    if fetched_info and fetched_info.get('price'):
                        price_str = str(fetched_info.get('price')).strip()
                except Exception:
                    pass
            if not price_str:
                price_str = "$19.99"
            if price_str.startswith('.'):
                price_str = f"$19{price_str}"
            elif price_str.replace('.', '', 1).isdigit() and not price_str.startswith('$'):
                price_str = f"${price_str}"
            price = price_str

            from modules.seo_copywriter import generate_pin_seo_data
            _seo_fresh = generate_pin_seo_data(product_title=title, price=price)

            pin_title = raw_pin_title if raw_pin_title and not raw_pin_title.startswith('Product B0') and ('Fenmzee' not in raw_pin_title or asin == 'B0BPNXX2MF') else title
            pin_description = reg_entry.get('description') or data.get('pin_description', '')
            if not pin_description or ('Fenmzee' in pin_description and asin != 'B0BPNXX2MF'):
                pin_description = _seo_fresh.get('description', f"Discover the {title}. Perfect for aesthetic cozy room decor!")

            badge_hook = data.get('badge_hook', 'VIRAL ROOM FIND')
            regional_asins = reg_entry.get('regional_asins') or data.get('regional_asins', {'US': asin})
            regional_prices = reg_entry.get('regional_prices') or data.get('regional_prices', {
                'US': price,
                'IN': '₹1,650.00' if '19.99' in price else '₹2,899.00',
                'UK': '£15.99' if '19.99' in price else '£27.50',
                'DE': '€18.50' if '19.99' in price else '€32.00',
                'CA': 'CA$26.99' if '19.99' in price else 'CA$46.99',
                'AU': 'A$29.99' if '19.99' in price else 'A$52.00',
                'JP': '¥3,050' if '19.99' in price else '¥5,400',
                'SE': '210,00kr'
            })
            direct_regions = reg_entry.get('direct_regions') or data.get('direct_regions', ['US', 'IN', 'UK', 'DE', 'CA', 'AU', 'JP', 'SE'])

            from modules.bridge_creator import generate_bridge_page
            from modules.html_overlay_engine import render_html_overlay

            features_list = reg_entry.get('features')
            if not features_list or ('FABRIC SHADE FINISH' in str(features_list).upper() and asin != 'B0BPNXX2MF' and 'LAMP' not in title.upper()):
                features_list = _seo_fresh.get('features', ['PREMIUM QUALITY', 'WARM AMBIENT GLOW', 'AESTHETIC DESIGN', 'EASY SETUP'])

            # Auto-register product in product_price_registry.json if missing or incomplete
            try:
                current_reg = registry_all.get(asin, {})
                current_reg['asin'] = asin
                current_reg['title'] = title
                current_reg['current_price'] = price
                if pin_description:
                    current_reg['description'] = pin_description
                if features_list:
                    current_reg['features'] = features_list
                current_reg['regional_prices'] = regional_prices
                current_reg['regional_asins'] = regional_asins
                current_reg['direct_regions'] = direct_regions
                registry_all[asin] = current_reg
                with open(reg_file, 'w', encoding='utf-8') as wf:
                    json.dump(registry_all, wf, indent=2, ensure_ascii=False)
                print(f"[Create Bridge Page] ✅ Auto-registered ASIN {asin} ('{title}') in product_price_registry.json!")
            except Exception as e_reg:
                print(f"[Create Bridge Page Warning] Auto-register error: {e_reg}")

            seo_data = {
                'pin_title': pin_title,
                'description': pin_description,
                'image_hook': _seo_fresh.get('image_hook') or title,
                'subtitle_hook': '',
                'badge_hook': badge_hook,
                'features': features_list,
            }

            prod = {
                'title': title,
                'price': price,
                'current_price': price,
                'rating': reg_entry.get('rating', '4.8'),
                'description': pin_description,
                'features': features_list,
                'category': reg_entry.get('category', 'decor'),
                'regional_asins': regional_asins,
                'regional_prices': regional_prices,
                'direct_regions': direct_regions,
            }

            # 1. Generate bridge page
            generate_bridge_page(prod, seo_data, asin)

            # 2. Render hook image (price badge overlay - ALWAYS USD)
            from modules.amazon_extractor import get_best_image_for_asin
            img_res = get_best_image_for_asin(asin, title=data.get('title', title), save_to_disk=True)
            raw_img_path = WORKSPACE_DIR / 'raw_images' / f'raw_{asin}.jpg'
            source_img = str(raw_img_path) if raw_img_path.exists() else (img_res.get("local_path") or str(raw_img_path))
            hook_img_path = str(WORKSPACE_DIR / f'focus_product_{asin}_hook.jpg')

            render_html_overlay(
                image_path=source_img,
                headline=seo_data.get('image_hook'),
                subtitle='',
                badge_text=badge_hook,
                price_str=price,
                features=prod['features'],
                output_path=hook_img_path
            )

            # 3. Git add + commit + push (background thread so n8n doesn't time out)
            bridge_url = f'https://adityasnalawade742-design.github.io/bridge_{asin}.html'
            hook_image_url = f'https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg'

            # BUG A FIX: Update TASK_STATUS_MAP so Step 3 polling (/api/task_status?asin=X)
            # resolves from ⏳ to ✅ as soon as bridge page + hook image are built.
            update_task_status(asin, {
                'status': 'success',
                'bridge_url': bridge_url,
                'hook_image_url': hook_image_url,
                'message': f'Bridge page and hook image built for {asin}. Deploying to GitHub Pages...'
            })

            def push_live(target_asin):
                try:
                    subprocess.run(['git', 'add', '-A'], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(['git', 'commit', '-m',
                        f'feat: n8n auto-published bridge_{target_asin} + hook image'],
                        cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(['git', 'push', 'origin', 'main'],
                        cwd=str(WORKSPACE_DIR), check=False)
                    print(f'[Create Bridge Page] ✅ Pushed bridge_{target_asin}.html live!')
                    from modules.automated_product_selector import cleanup_unselected_raw_images
                    cleanup_unselected_raw_images()
                except Exception as eg:
                    print(f'[Create Bridge Page Warning] Git push error: {eg}')

            threading.Thread(target=push_live, args=(asin,), daemon=True).start()

            self.send_json({
                'status': 'success',
                'asin': asin,
                'bridge_url': bridge_url,
                'hook_image_url': hook_image_url,
                'message': f'Bridge page and hook image created for {asin}. Deploying to GitHub Pages...'
            })
        except Exception as e:
            import traceback; traceback.print_exc()
            self.send_json({'status': 'error', 'message': str(e)})

    def handle_api_dispatch_n8n_batch(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8')) if content_length > 0 else {}
            items = data.get('items', [])
            n8n_webhook_url = data.get('n8n_webhook_url', 'http://localhost:5678/webhook/pinterest-batch')

            if not items:
                self.send_json({"status": "error", "message": "No items selected in batch."})
                return

            print(f"[n8n Dispatcher] 🚀 Dispatching batch of {len(items)} items to n8n Workflow ({n8n_webhook_url})...")

            def process_n8n_batch():
                import urllib.request
                from modules.amazon_extractor import get_product_details_and_photos
                from modules.bridge_creator import generate_bridge_page
                from modules.seo_copywriter import generate_pin_seo_data
                from modules.html_overlay_engine import render_html_overlay
                from modules.pinterest_publisher import publish_pin_to_pinterest
                from modules.automated_product_selector import save_processed_asin

                for item in items:
                    asin = item.get('asin')
                    title = item.get('title', 'Aesthetic Home Decor Find')
                    price = item.get('price', '$19.99')
                    chosen_photo = item.get('chosen_photo_url') or item.get('winner_photo')

                    print(f"[n8n Dispatcher] ⚙️ Processing ASIN: {asin} | Chosen Photo: {(chosen_photo or 'N/A')[:40]}...")

                    # 1. Fetch Product Data
                    amazon_url = f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"
                    prod = get_product_details_and_photos(amazon_url) or {
                        'title': title, 'price': price, 'features': ['Aesthetic Decor', 'Cozy Glow', 'Modern Style'],
                        'category': 'decor', 'url': amazon_url
                    }

                    # 2. Unique SEO & Viral Hashtags
                    seo_data = generate_pin_seo_data(product_title=title, price=price, category=prod.get('category', 'decor'))
                    
                    # Ensure targeted hashtags are attached
                    category_hashtags = "#cozyroom #aestheticdecor #roomdecor #homefinds #amazonfinds"
                    if "description" in seo_data and category_hashtags not in seo_data["description"]:
                        seo_data["description"] += f"\n\n{category_hashtags}"

                    # 3. Build & Deploy Bridge Page
                    generate_bridge_page(prod, seo_data, asin)

                    # 4. Render Luxury Price Badge & Typography Template
                    raw_img_path = str(WORKSPACE_DIR / f"raw_images/raw_{asin}.jpg")
                    if chosen_photo and chosen_photo.startswith('http'):
                        tmp_download_path = str(WORKSPACE_DIR / f"raw_images/tmp_raw_{asin}.jpg")
                        try:
                            req = urllib.request.Request(chosen_photo, headers={'User-Agent': 'Mozilla/5.0'})
                            with urllib.request.urlopen(req, timeout=15) as resp, open(tmp_download_path, 'wb') as f:
                                f.write(resp.read())
                            if Path(tmp_download_path).exists() and Path(tmp_download_path).stat().st_size > 0:
                                os.replace(tmp_download_path, raw_img_path)
                            else:
                                if Path(tmp_download_path).exists():
                                    Path(tmp_download_path).unlink(missing_ok=True)
                        except Exception as e_dl:
                            print(f"[n8n Dispatcher] Warning downloading photo: {e_dl}")
                            if Path(tmp_download_path).exists():
                                Path(tmp_download_path).unlink(missing_ok=True)

                    if not Path(raw_img_path).exists():
                        from modules.amazon_extractor import get_best_image_for_asin
                        best_res = get_best_image_for_asin(asin, title=prod.get('title', ''), save_to_disk=True)
                        if best_res and best_res.get("local_path"):
                            raw_img_path = best_res["local_path"]

                    hook_img_path = str(WORKSPACE_DIR / f"focus_product_{asin}_hook.jpg")
                    render_html_overlay(
                        image_path=str(raw_img_path),
                        headline=seo_data.get("image_hook") or "COZY ROOM FIND",
                        subtitle="",  # BUG F FIX: Rule 7 — subtitles MUST always be empty ("") unless explicitly requested
                        badge_text=seo_data.get("badge_hook") or "VIRAL FIND",
                        price_str=price,
                        features=prod.get('features', []),
                        output_path=hook_img_path
                    )

                    # 5. Forward Payload to n8n Webhook Endpoint if reachable
                    bridge_url = f"https://adityasnalawade742-design.github.io/bridge_{asin}.html"
                    image_url = f"https://adityasnalawade742-design.github.io/focus_product_{asin}_hook.jpg"

                    n8n_payload = {
                        "asin": asin,
                        "title": title,
                        "price": price,
                        "pin_title": seo_data.get("pin_title"),
                        "pin_description": seo_data.get("description") or seo_data.get("pin_description"),
                        "bridge_url": bridge_url,
                        "image_url": image_url
                    }

                    try:
                        req_data = json.dumps(n8n_payload).encode('utf-8')
                        urls_to_try = [n8n_webhook_url]
                        if 'webhook-test' in n8n_webhook_url:
                            urls_to_try.append(n8n_webhook_url.replace('webhook-test', 'webhook'))
                        elif '/webhook/' in n8n_webhook_url:
                            urls_to_try.append(n8n_webhook_url.replace('/webhook/', '/webhook-test/'))

                        for u in urls_to_try:
                            try:
                                n8n_req = urllib.request.Request(u, data=req_data, headers={'Content-Type': 'application/json'})
                                with urllib.request.urlopen(n8n_req, timeout=3) as n8n_res:
                                    print(f"[n8n Webhook] ✅ Dispatched to n8n Webhook ({u}): {n8n_res.status}")
                                break
                            except Exception:
                                pass
                    except Exception as e_n8n:
                        print(f"[n8n Webhook] Note: n8n local webhook listening check: {e_n8n}")

                    # 6. Publish Pin to Pinterest API v5
                    publish_pin_to_pinterest(
                        image_path=hook_img_path,
                        title=seo_data.get("pin_title"),
                        description=seo_data.get("description") or seo_data.get("pin_description"),
                        destination_url=bridge_url,
                        image_url=image_url
                    )

                    save_processed_asin(asin)

                # Push updated bridge pages to GitHub Pages
                try:
                    import subprocess
                    subprocess.run(["git", "add", "bridge_*.html", "focus_product_*_hook.jpg", "index.html", "product_price_registry.json"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "commit", "-m", f"feat: n8n batch published {len(items)} products with bridge pages"], cwd=str(WORKSPACE_DIR), check=False)
                    subprocess.run(["git", "push", "origin", "main"], cwd=str(WORKSPACE_DIR), check=False)
                    print(f"[n8n Dispatcher] 🏆 Successfully pushed batch bridge pages live to GitHub Pages!")
                except Exception as e_git:
                    print(f"[n8n Dispatcher] Git push info: {e_git}")

            import threading
            threading.Thread(target=process_n8n_batch, daemon=True).start()

            self.send_json({
                "status": "success",
                "message": f"🚀 Successfully dispatched {len(items)} products to n8n workflow pipeline!",
                "batch_count": len(items)
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json({"status": "error", "message": str(e)})

    def handle_api_auth_pinterest(self):
        """Redirects user to Pinterest OAuth 2.0 Authorization screen with App ID 1596368."""
        client_id = "1596368"
        port = self.server.server_address[1]
        redirect_uri = f"http://localhost:{port}/api/auth/callback"
        scopes = "boards:read,boards:write,pins:read,pins:write"
        auth_url = f"https://www.pinterest.com/oauth/?client_id={client_id}&redirect_uri={urllib.parse.quote(redirect_uri)}&response_type=code&scope={scopes}"

        self.send_response(302)
        self.send_header("Location", auth_url)
        self.end_headers()

    def handle_api_auth_callback(self, query_str):
        """
        BUG 1 FIX: Actually exchange the OAuth authorization code for a real access token.
        Saves the token to .env and updates in-memory config so pin publishing works immediately.
        """
        params = urllib.parse.parse_qs(query_str)
        code = params.get("code", [""])[0]
        error = params.get("error", [""])[0]

        # --- Pinterest credentials ---
        from dotenv import load_dotenv
        load_dotenv(WORKSPACE_DIR / ".env", override=True)
        client_id = "1596368"
        client_secret = os.getenv("PINTEREST_CLIENT_SECRET", "").strip()
        if not client_secret:
            env_path = WORKSPACE_DIR / ".env"
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    if line.startswith("PINTEREST_CLIENT_SECRET="):
                        client_secret = line.split("=", 1)[1].strip().strip('"').strip("'")
        port = self.server.server_address[1]
        redirect_uri = f"http://localhost:{port}/api/auth/callback"

        token_status = "pending"
        access_token = ""
        refresh_token = ""
        token_error = ""

        if error:
            token_status = "oauth_error"
            token_error = error
        elif code and client_secret:
            # Exchange code → access token via Pinterest API
            try:
                import base64, urllib.request as urlreq
                creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
                token_payload = urllib.parse.urlencode({
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri
                }).encode()
                req = urlreq.Request(
                    "https://api.pinterest.com/v5/oauth/token",
                    data=token_payload,
                    headers={
                        "Authorization": f"Basic {creds}",
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    method="POST"
                )
                with urlreq.urlopen(req, timeout=15) as resp:
                    token_data = json.loads(resp.read().decode())
                access_token = token_data.get("access_token", "")
                refresh_token = token_data.get("refresh_token", "")

                if access_token:
                    # Persist to .env file
                    env_path = WORKSPACE_DIR / ".env"
                    env_text = env_path.read_text(encoding="utf-8") if env_path.exists() else ""
                    # Replace or append PINTEREST_ACCESS_TOKEN
                    if "PINTEREST_ACCESS_TOKEN=" in env_text:
                        env_text = re.sub(r'PINTEREST_ACCESS_TOKEN=.*', f'PINTEREST_ACCESS_TOKEN={access_token}', env_text)
                    else:
                        env_text += f"\nPINTEREST_ACCESS_TOKEN={access_token}"
                    if refresh_token:
                        if "PINTEREST_REFRESH_TOKEN=" in env_text:
                            env_text = re.sub(r'PINTEREST_REFRESH_TOKEN=.*', f'PINTEREST_REFRESH_TOKEN={refresh_token}', env_text)
                        else:
                            env_text += f"\nPINTEREST_REFRESH_TOKEN={refresh_token}"
                    env_path.write_text(env_text, encoding="utf-8")
                    # Also update in-memory os.environ so publisher works immediately
                    os.environ["PINTEREST_ACCESS_TOKEN"] = access_token
                    if refresh_token:
                        os.environ["PINTEREST_REFRESH_TOKEN"] = refresh_token
                    token_status = "success"
                    print(f"[Pinterest OAuth] ✅ Access token obtained and saved to .env!")
                else:
                    token_status = "no_token"
                    token_error = str(token_data)
            except Exception as e_tok:
                token_status = "exchange_error"
                token_error = str(e_tok)
                print(f"[Pinterest OAuth] ❌ Token exchange error: {e_tok}")
        elif code and not client_secret:
            # No client secret configured — display instructions
            token_status = "missing_secret"
            token_error = "PINTEREST_CLIENT_SECRET is not set in .env. Add it to enable live token exchange."
            access_token = "(requires PINTEREST_CLIENT_SECRET in .env)"
        else:
            token_status = "no_code"
            token_error = "No authorization code received from Pinterest."

        # Build status badge
        if token_status == "success":
            badge_color = "#10b981"
            badge_label = "✅ Token Exchange SUCCESS — Pinterest Connected!"
            heading = "Account Connected & Token Saved!"
            body_msg = "Your Pinterest access token has been saved to <code>.env</code> and is active in memory. Pin publishing is now live."
        elif token_status == "missing_secret":
            badge_color = "#fb8500"
            badge_label = "⚠️ Client Secret Missing"
            heading = "Almost There — Add Client Secret"
            body_msg = f"Set <code>PINTEREST_CLIENT_SECRET=your_secret</code> in <code>.env</code>, then retry OAuth. Auth code received: <code>{code[:20]}...</code>"
        elif token_status == "oauth_error":
            badge_color = "#ef4444"
            badge_label = f"❌ OAuth Error: {error}"
            heading = "OAuth Flow Error"
            body_msg = f"Pinterest returned an error during authorization: <code>{error}</code>. Please retry the OAuth flow."
        elif token_status in ("exchange_error", "no_token"):
            badge_color = "#ef4444"
            badge_label = "❌ Token Exchange Failed"
            heading = "Token Exchange Error"
            body_msg = f"Code was received but token exchange failed: <code>{token_error}</code>"
        else:
            badge_color = "#94a3b8"
            badge_label = "ℹ️ OAuth Callback Received"
            heading = "Callback Received"
            body_msg = "Authorization code was received. Configure PINTEREST_CLIENT_SECRET to complete token exchange."

        display_token = (access_token[:28] + "...") if len(access_token) > 28 else (access_token or "(not obtained)")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pinterest OAuth 2.0 Auth Callback | Cozy Room Decor Publisher Pro</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0a10; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }}
        .auth-card {{ background: rgba(22, 20, 30, 0.9); border: 1px solid rgba(255, 183, 3, 0.4); border-radius: 24px; padding: 40px; max-width: 600px; width: 100%; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.8); }}
        .badge {{ background: {badge_color}; color: #fff; font-size: 12px; font-weight: 800; padding: 6px 16px; border-radius: 50px; display: inline-block; margin-bottom: 20px; }}
        h1 {{ font-size: 26px; color: #ffb703; margin-bottom: 12px; }}
        p {{ color: #cbd5e1; font-size: 15px; line-height: 1.6; margin-bottom: 24px; }}
        code {{ background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; font-size: 13px; color: #fbbf24; }}
        .info-box {{ background: rgba(255, 255, 255, 0.05); border: 1px dashed rgba(255, 183, 3, 0.3); border-radius: 16px; padding: 20px; text-align: left; margin-bottom: 28px; font-size: 13.5px; color: #e2e8f0; }}
        .info-row {{ display: flex; justify-content: space-between; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 8px; }}
        .info-row:last-child {{ border: none; margin: 0; padding: 0; }}
        .info-label {{ color: #94a3b8; font-weight: 600; }}
        .info-val {{ color: #ffb703; font-weight: 700; font-family: monospace; word-break: break-all; }}
        .btn {{ display: inline-block; background: linear-gradient(135deg, #fb8500, #ffb703); color: #000; font-weight: 800; font-size: 15px; padding: 14px 32px; border-radius: 50px; text-decoration: none; box-shadow: 0 8px 25px rgba(251, 133, 0, 0.4); transition: transform 0.2s; }}
        .btn:hover {{ transform: translateY(-2px); }}
    </style>
</head>
<body>
    <div class="auth-card">
        <div class="badge">{badge_label}</div>
        <h1>{heading}</h1>
        <p>{body_msg}</p>

        <div class="info-box">
            <div class="info-row"><span class="info-label">Company Name:</span><span class="info-val">Cozy Room Finds</span></div>
            <div class="info-row"><span class="info-label">Application Name:</span><span class="info-val">Cozy Room Decor Publisher Pro</span></div>
            <div class="info-row"><span class="info-label">Pinterest App ID:</span><span class="info-val">1596368</span></div>
            <div class="info-row"><span class="info-label">Connected Profile:</span><span class="info-val">@adityasnalawade0703</span></div>
            <div class="info-row"><span class="info-label">Access Token:</span><span class="info-val" style="color:{'#4ade80' if token_status == 'success' else '#fb8500'};">{display_token}</span></div>
            <div class="info-row"><span class="info-label">OAuth Scopes:</span><span class="info-val">boards:read, boards:write, pins:read, pins:write</span></div>
            <div class="info-row"><span class="info-label">Status:</span><span class="info-val" style="color:{'#4ade80' if token_status == 'success' else '#fb8500'};">{'✅ Active — Token Saved to .env' if token_status == 'success' else token_status.replace('_', ' ').title()}</span></div>
        </div>

        <a href="/admin_console.html" class="btn">← Back to Web Console Dashboard</a>
    </div>
</body>
</html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

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
    try:
        from modules.product_registry import cleanup_orphaned_raw_images
        cleanup_orphaned_raw_images(max_age_hours=24)
    except Exception as e:
        print(f"[Registry Cleanup Warning] {e}")
    run_server()

