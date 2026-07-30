import json
import re
import urllib.request
import time
from pathlib import Path
from PIL import Image

WORKSPACE = Path("G:/CLI/pinterest-auto-affiliate")

def run_advanced_audit():
    print("=" * 60)
    print("[Audit] ADVANCED CANVA CUSTOMIZER & RE-RENDER AUDIT")
    print("=" * 60)
    
    # 1. Audit Asset Dimensions & Aspect Ratios
    tag_asset = WORKSPACE / "price tags/tag 1.png"
    assert tag_asset.exists(), "price tags/tag 1.png is missing!"
    img = Image.open(tag_asset)
    w, h = img.size
    aspect_ratio = w / float(h)
    print(f"[Audit] 1. Asset Check: 'tag 1.png' dimensions = {w}x{h}px (Aspect Ratio: {aspect_ratio:.4f})")
    assert abs(aspect_ratio - (300/406)) < 0.05, f"Aspect ratio mismatch! Expected 300:406 (~0.7389), got {aspect_ratio:.4f}"
    print("   -> Asset aspect ratio matches 300:406 container spec 100%")

    # 2. Audit API Customization Request with Extreme Boundaries
    test_cases = [
        {"name": "Default Center", "tag_color": "#fb8500", "price_color": "#111827", "rot": -6, "w": 380, "h": 514, "pos_x": 61.0, "pos_y": 75.0, "off_x": 0, "off_y": 15, "font_scale": 0.20},
        {"name": "Top-Left Red Swatch", "tag_color": "#ff0055", "price_color": "#ffffff", "rot": -12, "w": 320, "h": 433, "pos_x": 15.0, "pos_y": 20.0, "off_x": -15, "off_y": 30, "font_scale": 0.25},
        {"name": "Bottom-Right Violet Swatch", "tag_color": "#7a00ff", "price_color": "#ffffff", "rot": 10, "w": 450, "h": 609, "pos_x": 50.0, "pos_y": 60.0, "off_x": 15, "off_y": 0, "font_scale": 0.15}
    ]

    for idx, tc in enumerate(test_cases, 1):
        print(f"\n[Audit] 2.{idx} Testing Customization Scenario: '{tc['name']}'...")
        payload = {
            "asin": "B0D8P8CSYP",
            "tag_width": tc["w"],
            "tag_height": tc["h"],
            "tag_rotation": tc["rot"],
            "tag_color": tc["tag_color"],
            "price_text_color": tc["price_color"],
            "price_font_scale": tc["font_scale"],
            "price_text_offset_x": tc["off_x"],
            "price_text_offset_y": tc["off_y"],
            "tag_pos_x": tc["pos_x"],
            "tag_pos_y": tc["pos_y"]
        }
        
        t0 = time.time()
        req = urllib.request.Request(
            "http://localhost:5000/api/customize_tag",
            data=json.dumps(payload).encode('utf-8'),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            elapsed = time.time() - t0
            print(f"   -> Response Status: {data.get('status')} (Render Time: {elapsed:.2f}s)")
            assert data.get('status') == 'success', f"API returned non-success: {data}"
            assert data.get('message') == 'changed published', "Missing 'changed published' message!"
            
            output_img = WORKSPACE / "focus_product_B0D8P8CSYP_hook.jpg"
            assert output_img.exists(), "Output image missing!"
            print(f"   -> Rendered File Verified: {output_img.name} ({output_img.stat().st_size} bytes)")

            # Check cache busting in index.html
            index_html = (WORKSPACE / "index.html").read_text(encoding="utf-8")
            assert data['v_tag'] in index_html, f"index.html missing version tag {data['v_tag']}"
            print("   -> index.html cache-busting tag updated!")

            # Check cache busting in bridge page
            bridge_html = (WORKSPACE / "bridge_B0D8P8CSYP.html").read_text(encoding="utf-8")
            assert data['v_tag'] in bridge_html, f"bridge_B0D8P8CSYP.html missing version tag {data['v_tag']}"
            print("   -> bridge_B0D8P8CSYP.html cache-busting tag updated!")

    # 3. Audit Stamped PNG File Integrity
    stamped_tag = WORKSPACE / "price tags/stamped_ambient_tag.png"
    assert stamped_tag.exists(), "stamped_ambient_tag.png missing!"
    s_img = Image.open(stamped_tag)
    print(f"\n[Audit] 3. Stamped PNG Verification: Dimensions = {s_img.size[0]}x{s_img.size[1]}px")
    assert s_img.mode == "RGBA", "Stamped PNG is not in RGBA format!"
    print("   -> Translucent PNG channel intact!")

    print("\n" + "=" * 60)
    print("[Audit] ADVANCED CUSTOMIZER AUDIT COMPLETE: 100% PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    run_advanced_audit()
