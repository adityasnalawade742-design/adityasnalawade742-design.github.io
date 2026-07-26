from pathlib import Path
from jinja2 import Template
from config import BRIDGE_DIR, IMAGES_DIR

BRIDGE_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ seo.pin_title }} | Cozy Room Finds</title>
    <meta name="description" content="{{ seo.description }}">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Playfair+Display:ital,wght@0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f0e13;
            --card-bg: rgba(26, 24, 33, 0.85);
            --accent-warm: #ffb703;
            --accent-glow: #fb8500;
            --text-main: #f8f9fa;
            --text-muted: #adb5bd;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-image: radial-gradient(circle at 50% 10%, rgba(251, 133, 0, 0.12), transparent 60%);
        }

        .container {
            max-width: 480px;
            width: 100%;
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 24px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            text-align: center;
        }

        .tag {
            display: inline-block;
            background: rgba(255, 183, 3, 0.15);
            color: var(--accent-warm);
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 50px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }

        .hero-img {
            width: 100%;
            border-radius: 16px;
            aspect-ratio: 3/4;
            object-fit: cover;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 24px;
            margin-bottom: 12px;
            color: #fff;
            line-height: 1.3;
        }

        .price {
            font-size: 28px;
            font-weight: 700;
            color: var(--accent-warm);
            margin-bottom: 16px;
        }

        p.description {
            font-size: 14px;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 24px;
        }

        .features {
            background: rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 24px;
            text-align: left;
        }

        .features h3 {
            font-size: 13px;
            color: var(--accent-warm);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .features p {
            font-size: 13px;
            color: var(--text-main);
        }

        .btn-amazon {
            display: block;
            width: 100%;
            background: linear-gradient(135deg, var(--accent-warm), var(--accent-glow));
            color: #000;
            font-weight: 700;
            font-size: 16px;
            padding: 18px;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 8px 25px rgba(251, 133, 0, 0.4);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn-amazon:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(251, 133, 0, 0.6);
        }

        .footer-note {
            margin-top: 16px;
            font-size: 11px;
            color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <span class="tag">✨ Pinterest Cozy Pick</span>
        <img class="hero-img" src="{{ relative_image_path }}" alt="{{ product.title }}">
        <h1>{{ seo.pin_title }}</h1>
        <div class="price">{{ product.price }}</div>
        <p class="description">{{ seo.description }}</p>

        <div class="features">
            <h3>Key Aesthetic Highlights</h3>
            <p>{{ product.features }}</p>
        </div>

        <a id="amazon-btn" class="btn-amazon" href="{{ product.affiliate_url }}" target="_blank" rel="noopener">
            🛒 Check Price & Availability on Amazon ➔
        </a>

        <p class="footer-note">As an Amazon Associate, we earn from qualifying purchases.</p>
    </div>

    <script>
        // Direct Amazon Product Page Redirection
        document.getElementById('amazon-btn').addEventListener('click', function(e) {
            e.preventDefault();
            const directProductUrl = "{{ product.affiliate_url }}";
            window.open(directProductUrl, '_blank', 'noopener,noreferrer');
        });
    </script>
</body>

</html>
"""


import shutil

def generate_bridge_page(product: dict, seo: dict, image_path: str) -> str:
    """
    Generates an aesthetic micro landing page (Bridge Page) for the product.
    Returns the path to the created HTML file.
    """
    template = Template(BRIDGE_PAGE_TEMPLATE)
    
    import time
    image_name = Path(image_path).name
    relative_image_path = f"{image_name}?v={int(time.time())}"

    rendered_html = template.render(
        product=product,
        seo=seo,
        relative_image_path=relative_image_path
    )

    page_file = BRIDGE_DIR / f"bridge_{product['id']}.html"
    with open(page_file, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    # Save directly to project root for 100% reliable GitHub Pages routing
    project_root = Path(__file__).resolve().parent.parent
    root_page_file = project_root / f"bridge_{product['id']}.html"
    root_image_file = project_root / image_name

    with open(root_page_file, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    if Path(image_path).exists():
        shutil.copy(image_path, root_image_file)

    # Automatically update root index.html showcase gallery
    update_showcase_index_page(product, image_name)

    print(f"[Bridge Creator] Created aesthetic bridge page: {page_file} (Synced to root bridge_{product['id']}.html & index.html)")
    return str(page_file)


def update_showcase_index_page(product: dict, image_name: str):
    """Dynamically updates root index.html showcase gallery with the latest product card."""
    project_root = Path(__file__).resolve().parent.parent
    index_file = project_root / "index.html"
    
    if not index_file.exists():
        return

    try:
        with open(index_file, "r", encoding="utf-8") as f:
            html = f.read()

        card_href = f"./bridge_{product['id']}.html"
        if card_href in html:
            return  # Already present in index.html

        new_card = f"""        <div class="card-wrapper" id="card-{product['id']}">
            <a class="card" href="./bridge_{product['id']}.html">
                <img src="./{image_name}?v=2" alt="{product.get('title', 'Product')}">
                <h2>{product.get('title', 'Cozy Room Find')[:45]}...</h2>
                <div class="price">{product.get('price', '')}</div>
            </a>
            <button class="delete-btn" onclick="deleteCard('{product['id']}', 'card-{product['id']}')">🗑️ Delete Product</button>
        </div>"""

        grid_marker = '<div class="grid" id="productGrid">'
        if grid_marker not in html:
            grid_marker = '<div class="grid">'

        if grid_marker in html:
            html = html.replace(grid_marker, f"{grid_marker}\n{new_card}\n")
            with open(index_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[Bridge Creator] Updated index.html showcase with card for {product['id']}")
    except Exception as e:
        print(f"[Bridge Creator] Error updating index.html: {e}")

