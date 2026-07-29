from pathlib import Path
from jinja2 import Template
from config import BRIDGE_DIR, IMAGES_DIR

BRIDGE_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ seo.pin_title }} | Cozy Room Finds</title>
    <meta name="description" content="{{ seo.description }}">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #09080c;
            --card-bg: rgba(20, 18, 26, 0.85);
            --accent-gold: #ffb703;
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
            padding: 24px 16px;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(251, 133, 0, 0.2), transparent 60%),
                radial-gradient(circle at 90% 80%, rgba(255, 183, 3, 0.08), transparent 50%);
            background-attachment: fixed;
        }

        .container {
            max-width: 480px;
            width: 100%;
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border-radius: 28px;
            padding: 24px;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6);
            text-align: center;
            position: relative;
        }

        /* Top Back Link */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }

        .back-link {
            color: var(--text-muted);
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: color 0.2s;
        }

        .back-link:hover {
            color: var(--accent-gold);
        }

        .tag {
            background: linear-gradient(135deg, rgba(251, 133, 0, 0.2), rgba(255, 183, 3, 0.2));
            border: 1px solid rgba(255, 183, 3, 0.5);
            color: var(--accent-gold);
            font-size: 11px;
            font-weight: 700;
            padding: 5px 14px;
            border-radius: 50px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        /* Hero Image Container */
        .img-container {
            position: relative;
            width: 100%;
            border-radius: 20px;
            overflow: hidden;
            aspect-ratio: 3/4;
            margin-bottom: 20px;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .hero-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s ease;
        }

        /* Image Switcher Tabs */
        .img-tabs {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }

        .img-tab-btn {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #d1d5db;
            font-size: 12px;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .img-tab-btn.active {
            background: linear-gradient(135deg, var(--accent-glow), var(--accent-gold));
            color: #0d0c10;
            border-color: #ffffff;
            font-weight: 700;
            box-shadow: 0 4px 16px rgba(251, 133, 0, 0.35);
        }

        /* Ratings */
        .rating-box {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 12px;
            color: var(--accent-gold);
            font-size: 14px;
            font-weight: 700;
        }

        .rating-stars {
            letter-spacing: 2px;
        }

        .rating-count {
            color: var(--text-muted);
            font-size: 12px;
            font-weight: 500;
        }

        h1 {
            font-family: 'Playfair Display', serif;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 10px;
            color: #ffffff;
            line-height: 1.28;
        }

        .price-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 18px;
        }

        .price {
            font-family: 'Playfair Display', serif;
            font-size: 34px;
            font-weight: 700;
            color: var(--accent-gold);
        }

        .prime-badge {
            background: rgba(0, 168, 225, 0.15);
            border: 1px solid rgba(0, 168, 225, 0.4);
            color: #00a8e1;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }

        p.description {
            font-size: 14.5px;
            color: var(--text-muted);
            line-height: 1.6;
            margin-bottom: 22px;
        }

        /* Features Box */
        .features-box {
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 24px;
            text-align: left;
        }

        .features-box h3 {
            font-size: 12px;
            color: var(--accent-gold);
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
        }

        .features-list {
            list-style: none;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }

        .features-list li {
            font-size: 12.5px;
            color: #e5e7eb;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Geo Shipping Notice Box */
        .geo-notice-box {
            display: none;
            background: rgba(251, 133, 0, 0.12);
            border: 1px solid rgba(251, 133, 0, 0.4);
            border-radius: 16px;
            padding: 14px 18px;
            margin-bottom: 20px;
            text-align: left;
            align-items: flex-start;
            gap: 12px;
            font-size: 12.5px;
            color: #f8f9fa;
        }

        .geo-notice-box .geo-icon { font-size: 18px; }
        .geo-notice-box strong { color: var(--accent-gold); display: block; margin-bottom: 2px; }

        /* High-Converting CTA Button */
        .btn-amazon {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            background: linear-gradient(135deg, var(--accent-glow), var(--accent-gold));
            border: 2px solid #ffffff;
            color: #0d0c10;
            font-weight: 800;
            font-size: 17px;
            padding: 16px;
            border-radius: 50px;
            text-decoration: none;
            box-shadow: 0 12px 35px rgba(251, 133, 0, 0.5);
            transition: all 0.3s ease;
            animation: pulse-glow 2.5s infinite;
            margin-bottom: 16px;
        }

        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(251, 133, 0, 0.6); }
            70% { box-shadow: 0 0 0 16px rgba(251, 133, 0, 0); }
            100% { box-shadow: 0 0 0 0 rgba(251, 133, 0, 0); }
        }

        .btn-amazon:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 16px 45px rgba(251, 133, 0, 0.7);
        }

        .guarantee {
            font-size: 12px;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
        }

        .guarantee span {
            display: flex;
            align-items: center;
            gap: 4px;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="top-bar">
            <a href="./index.html" class="back-link">← Back to Showcase</a>
            <div class="tag">✨ VIRAL FIND</div>
        </div>

        <!-- Rating Box -->
        <div class="rating-box">
            <span class="rating-stars">★★★★★</span>
            <span>{{ product.rating or '4.9' }}</span>
            <span class="rating-count">(1,240+ Verified Reviews)</span>
        </div>

        <h1>{{ product.title }}</h1>

        <div class="price-container">
            <div class="price">{{ product.price }}</div>
            <div class="prime-badge">⚡ Prime 2-Day Free Shipping</div>
        </div>

        <!-- Hero Image -->
        <div class="img-container">
            <img id="mainImage" class="hero-img" src="{{ hook_image_rel }}" alt="{{ product.title }}">
        </div>

        <!-- Image View Switcher -->
        <div class="img-tabs">
            <button class="img-tab-btn active" onclick="switchImage('{{ hook_image_rel }}', this)">✨ Commercial View</button>
            {% for raw_img in raw_images %}
            <button class="img-tab-btn" onclick="switchImage('{{ raw_img }}', this)">📷 Angle {{ loop.index }}</button>
            {% endfor %}
        </div>

        <p class="description">{{ seo.description }}</p>

        <!-- Feature Highlights Box -->
        <div class="features-box">
            <h3>✦ Highlights & Features</h3>
            <ul class="features-list">
                <li>✨ Premium Aesthetic</li>
                <li>💡 Warm Ambient Glow</li>
                <li>🌿 High Quality Build</li>
                <li>🎁 Perfect Gift Choice</li>
            </ul>
        </div>

        <!-- Geo Shipping Notice Box for Non-US Visitors -->
        <div id="geoNoticeBox" class="geo-notice-box">
            <span class="geo-icon">📍</span>
            <div>
                <strong id="geoNoticeTitle">Direct US Shipping Unavailable to Your Location</strong>
                <span id="geoNoticeDesc">This item ships from Amazon US. We've automatically linked equivalent local options on Amazon for fast regional delivery.</span>
            </div>
        </div>

        <!-- High-Converting CTA -->
        <a id="buyBtn" href="{{ affiliate_url }}" class="btn-amazon" target="_blank" rel="nofollow noopener">
            <span id="buyBtnText">CHECK DEAL ON AMAZON</span>
            <span>➔</span>
        </a>

        <div class="guarantee">
            <span>🔒 Official Amazon Store</span>
            <span>⚡ Free 30-Day Returns</span>
        </div>
    </div>

    <script>
        function switchImage(src, btn) {
            document.getElementById('mainImage').src = src;
            document.querySelectorAll('.img-tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        // Bulletproof Multi-Fallback Global Amazon Geo-Redirector
        (function() {
            const countryMap = {
                "IN": { domain: "amazon.in", label: "AMAZON INDIA (₹)" },
                "GB": { domain: "amazon.co.uk", label: "AMAZON UK (£)" },
                "UK": { domain: "amazon.co.uk", label: "AMAZON UK (£)" },
                "CA": { domain: "amazon.ca", label: "AMAZON CANADA (CA$)" },
                "AU": { domain: "amazon.com.au", label: "AMAZON AUSTRALIA (A$)" },
                "DE": { domain: "amazon.de", label: "AMAZON GERMANY (€)" },
                "FR": { domain: "amazon.fr", label: "AMAZON FRANCE (€)" },
                "ES": { domain: "amazon.es", label: "AMAZON SPAIN (€)" },
                "IT": { domain: "amazon.it", label: "AMAZON ITALY (€)" },
                "JP": { domain: "amazon.co.jp", label: "AMAZON JAPAN (¥)" },
                "MX": { domain: "amazon.com.mx", label: "AMAZON MEXICO (Mex$)" },
                "BR": { domain: "amazon.com.br", label: "AMAZON BRAZIL (R$)" },
                "NL": { domain: "amazon.nl", label: "AMAZON NETHERLANDS (€)" },
                "SE": { domain: "amazon.se", label: "AMAZON SWEDEN (kr)" }
            };

            const asin = "{{ asin }}";
            const prodKeywords = encodeURIComponent("{{ product.title[:40] }}");

            function applyGeoRedirect(cc) {
                if (!cc || !countryMap[cc] || cc === 'US') return;
                const target = countryMap[cc];
                const buyBtn = document.getElementById('buyBtn');
                const buyBtnText = document.getElementById('buyBtnText');
                const geoBox = document.getElementById('geoNoticeBox');
                
                // Route to valid local search deals on regional Amazon store (prevents 404 errors)
                if (buyBtn) buyBtn.href = `https://www.${target.domain}/s?k=${prodKeywords}`;
                if (buyBtnText) buyBtnText.innerText = `SEARCH LOCAL DEALS ON ${target.label}`;
                
                if (geoBox) {
                    const titleEl = document.getElementById('geoNoticeTitle');
                    const descEl = document.getElementById('geoNoticeDesc');
                    if (titleEl) titleEl.innerText = `Item Ships from Amazon US (Not Directly Listed on ${target.domain})`;
                    if (descEl) descEl.innerText = `This specific US model code is not directly listed in your region. We've automatically linked equivalent local deals on ${target.domain} for fast delivery.`;
                    geoBox.style.display = 'flex';
                }
            }

            // Method 1: Try api.country.is (Open CORS, Fast)
            fetch('https://api.country.is')
                .then(r => r.json())
                .then(d => {
                    if (d && d.country) applyGeoRedirect(d.country);
                    else throw new Error("No country");
                })
                .catch(err => {
                    // Method 2: Try ipapi.co
                    fetch('https://ipapi.co/json/')
                        .then(r => r.json())
                        .then(d => {
                            if (d && d.country_code) applyGeoRedirect(d.country_code);
                            else throw new Error("No country code");
                        })
                        .catch(err2 => {
                            // Method 3: Browser Timezone Fallback
                            try {
                                const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
                                if (tz.includes('Stockholm')) applyGeoRedirect('SE');
                                else if (tz.includes('Kolkata') || tz.includes('Calcutta')) applyGeoRedirect('IN');
                                else if (tz.includes('London')) applyGeoRedirect('GB');
                                else if (tz.includes('Berlin') || tz.includes('Paris')) applyGeoRedirect('DE');
                                else if (tz.includes('Tokyo')) applyGeoRedirect('JP');
                            } catch(e) {}
                        });
                });
        })();
    </script>

</body>
</html>
"""

def generate_bridge_page(product_data: dict, seo_data: dict, asin: str) -> str:
    """
    Generates a mobile-first, high-converting Pinterest affiliate bridge page.
    Saves file to root repository directory as bridge_{asin}.html.
    """
    output_filename = f"bridge_{asin}.html"
    
    # Absolute file path for writing
    output_filepath = Path("G:/CLI/pinterest-auto-affiliate") / output_filename
    
    # Form relative image paths for HTML display
    hook_img_rel = f"./focus_product_{asin}_hook.jpg?v=3"
    
    raw_images_rel = []
    if "images" in product_data and product_data["images"]:
        for i, img_path in enumerate(product_data["images"][:3]):
            raw_images_rel.append(f"./output/images/raw_amazon_{asin}_{i}.jpg")
    
    # Template rendering
    aff_url = product_data.get("affiliate_url") or f"https://www.amazon.com/dp/{asin}?tag=smartdeal0358-21"
    template = Template(BRIDGE_PAGE_TEMPLATE)
    rendered_html = template.render(
        product=product_data,
        seo=seo_data,
        asin=asin,
        affiliate_url=aff_url,
        hook_image_rel=hook_img_rel,
        raw_images=raw_images_rel
    )
    
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    print(f"[Bridge Creator] Generated high-converting luxury bridge page: {output_filepath}")
    
    # Auto-update showcase index page
    try:
        update_showcase_index_page(product_data, asin)
    except Exception as e:
        print(f"[Bridge Creator] Warning updating index showcase: {e}")

    return str(output_filepath)


def update_showcase_index_page(product_data: dict, asin: str):
    """
    Ensures newly processed products automatically appear on index.html grid.
    """
    index_path = Path("G:/CLI/pinterest-auto-affiliate/index.html")
    if not index_path.exists():
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    card_id = f"card-{asin}"
    if card_id in html:
        return  # Card already exists

    card_html = f'''
        <!-- Card {asin} -->
        <div class="card-wrapper" id="{card_id}">
            <a class="card" href="./bridge_{asin}.html">
                <div class="card-img-container">
                    <div class="card-price-tag">{product_data.get('price', '$19.99')}</div>
                    <div class="card-rating">★ 4.5</div>
                    <img src="./focus_product_{asin}_hook.jpg?v=3" alt="{product_data.get('title', 'Product')}">
                </div>
                <div class="card-content">
                    <h2>{product_data.get('title', 'Cozy Room Find')[:50]}...</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('{asin}', '{card_id}')">🗑️ Delete Product</button>
        </div>
'''
    for grid_tag in ['<main class="grid" id="productGrid">', '<div class="grid" id="productGrid">']:
        if grid_tag in html:
            new_html = html.replace(grid_tag, grid_tag + card_html)
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(new_html)
            print(f"[Bridge Creator] Automatically inserted new card {asin} into index.html showcase.")
            break
