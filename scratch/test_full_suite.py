import json
import re
import urllib.request
from pathlib import Path

WORKSPACE = Path("G:/CLI/pinterest-auto-affiliate")

def run_test():
    print("[Suite Test] Testing /api/customize_tag endpoint live on http://localhost:5000 ...")
    
    payload = {
        "asin": "B0D8P8CSYP",
        "tag_width": 380,
        "tag_height": 285,
        "tag_rotation": -10,
        "tag_color": "#ff0055",
        "price_text_color": "#ffffff",
        "price_font_scale": 0.45,
        "price_text_offset_x": 10,
        "price_text_offset_y": 0,
        "tag_pos_x": 25.0,
        "tag_pos_y": 35.0
    }
    
    req = urllib.request.Request(
        "http://localhost:5000/api/customize_tag",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print("[Suite Test] Response:", data)
            assert data.get('status') == 'success', f"API returned non-success status: {data}"
            assert 'message' in data and data['message'] == 'changed published', "Missing 'changed published' message!"
            
            output_img = WORKSPACE / "focus_product_B0D8P8CSYP_hook.jpg"
            assert output_img.exists(), "Rendered output image focus_product_B0D8P8CSYP_hook.jpg does not exist!"
            print(f"[Suite Test] Output image file exists on disk: {output_img} ({output_img.stat().st_size} bytes)")
            
            # Check bridge_B0D8P8CSYP.html file
            bridge_file = WORKSPACE / "bridge_B0D8P8CSYP.html"
            bridge_txt = bridge_file.read_text(encoding="utf-8")
            assert "focus_product_B0D8P8CSYP_hook.jpg?v=" in bridge_txt, "Bridge page missing cache-busted image tag!"
            print("[Suite Test] bridge_B0D8P8CSYP.html contains updated cache-busted image URL!")

            # Check index.html file
            index_file = WORKSPACE / "index.html"
            index_txt = index_file.read_text(encoding="utf-8")
            assert "focus_product_B0D8P8CSYP_hook.jpg?v=" in index_txt, "index.html missing cache-busted image tag!"
            print("[Suite Test] index.html contains updated cache-busted image URL!")

            print("[Suite Test] ALL END-TO-END TESTS PASSED CLEANLY!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

if __name__ == '__main__':
    run_test()
