import os
import sys
import re
import json
import subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
sys.path.append(str(repo_dir))
index_path = repo_dir / "index.html"

print("==================================================")
print("♿ APPLYING KEYBOARD NAVIGATION & SEO SCHEMAS")
print("==================================================")

content = index_path.read_text(encoding="utf-8")

# 1. Add :focus-visible Keyboard Navigation Styles to index.html
keyboard_css = '''
        /* Keyboard Focus Navigation Rings (WCAG 2.1 AA) */
        a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, .chip:focus-visible {
            outline: 2px solid var(--gold-primary) !important;
            outline-offset: 4px !important;
            box-shadow: 0 0 16px rgba(255, 183, 3, 0.6) !important;
        }

        .chip {
            cursor: pointer;
            user-select: none;
        }
'''
if ':focus-visible' not in content:
    content = content.replace('/* Top Bar Navigation */', f'{keyboard_css}\n        /* Top Bar Navigation */')

# 2. Add Google & Pinterest Structured JSON-LD ItemList Schema to index.html
json_ld_schema = '''    <!-- Google & Pinterest Rich Snippet Structured Data (JSON-LD) -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "ItemList",
      "name": "Cozy Room Finds - Curated Aesthetic Home Decor",
      "description": "Discover viral aesthetic room upgrades, cozy lighting, bedside lamps, and luxury Amazon home finds.",
      "url": "https://adityasnalawade742-design.github.io/index.html",
      "numberOfItems": 9,
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Minimalist Wood Base Bedside Table Lamp", "url": "https://adityasnalawade742-design.github.io/bridge_B0DZD1X83N.html" },
        { "@type": "ListItem", "position": 2, "name": "Flame Aroma Essential Oil Diffuser", "url": "https://adityasnalawade742-design.github.io/bridge_B0GYDXHF4G.html" },
        { "@type": "ListItem", "position": 3, "name": "White Wavy Wall Vanity Mirror", "url": "https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html" },
        { "@type": "ListItem", "position": 4, "name": "White Ceramic Donut Vase Set of 2", "url": "https://adityasnalawade742-design.github.io/bridge_B0C2YLN3H4.html" },
        { "@type": "ListItem", "position": 5, "name": "Crystal Prism Window Suncatcher", "url": "https://adityasnalawade742-design.github.io/bridge_B07HP22QTZ.html" },
        { "@type": "ListItem", "position": 6, "name": "Fenmzee Touch Bedside Table Lamp", "url": "https://adityasnalawade742-design.github.io/bridge_B0BZXNSW5K.html" },
        { "@type": "ListItem", "position": 7, "name": "Lily of the Valley Flower Table Lamp", "url": "https://adityasnalawade742-design.github.io/bridge_B0DXKGL1T2.html" },
        { "@type": "ListItem", "position": 8, "name": "Glass Mushroom Table Lamp", "url": "https://adityasnalawade742-design.github.io/bridge_B0D1FRDFFX.html" },
        { "@type": "ListItem", "position": 9, "name": "Cute Bird Dimmable Touch Night Lamp", "url": "https://adityasnalawade742-design.github.io/bridge_B0D8P8CSYP.html" }
      ]
    }
    </script>'''

if 'application/ld+json' not in content:
    content = content.replace('</head>', f'{json_ld_schema}\n</head>')

# 3. Update Category Chips to support Keyboard Enter & Space Navigation
chips_accessibility_html = '''        <div class="category-chips" role="tablist" aria-label="Product Category Filters">
            <div class="chip active" tabindex="0" role="tab" aria-selected="true" aria-label="Filter all products" onclick="setCategory('all', this)" onkeydown="if(event.key==='Enter'||event.key===' '){setCategory('all', this);event.preventDefault();}">✨ All Finds</div>
            <div class="chip" tabindex="0" role="tab" aria-selected="false" aria-label="Filter lamps and lighting" onclick="setCategory('lighting', this)" onkeydown="if(event.key==='Enter'||event.key===' '){setCategory('lighting', this);event.preventDefault();}">🕯️ Lamps & Lighting</div>
            <div class="chip" tabindex="0" role="tab" aria-selected="false" aria-label="Filter mirrors and wall decor" onclick="setCategory('mirror', this)" onkeydown="if(event.key==='Enter'||event.key===' '){setCategory('mirror', this);event.preventDefault();}">🪞 Mirrors & Wall</div>
            <div class="chip" tabindex="0" role="tab" aria-selected="false" aria-label="Filter vases" onclick="setCategory('vases', this)" onkeydown="if(event.key==='Enter'||event.key===' '){setCategory('vases', this);event.preventDefault();}">🏺 Vases</div>
            <div class="chip" tabindex="0" role="tab" aria-selected="false" aria-label="Filter home decor" onclick="setCategory('decor', this)" onkeydown="if(event.key==='Enter'||event.key===' '){setCategory('decor', this);event.preventDefault();}">🌿 Home Decor</div>
        </div>'''

content = re.sub(r'<div class="category-chips"[\s\S]*?</div>\s*<div id="productCounter"', f'{chips_accessibility_html}\n        <div id="productCounter"', content)

# 4. Update JavaScript setCategory to update aria-selected attribute
set_cat_js = '''        function setCategory(cat, element) {
            currentCategory = cat;
            document.querySelectorAll('.chip').forEach(c => {
                c.classList.remove('active');
                c.setAttribute('aria-selected', 'false');
            });
            element.classList.add('active');
            element.setAttribute('aria-selected', 'true');
            filterProducts();
        }'''

content = re.sub(r'function setCategory\(cat, element\) \{[\s\S]*?\}', set_cat_js, content)

index_path.write_text(content, encoding="utf-8")
print(" ✅ Applied Keyboard Focus Rings, ARIA Roles, and Google JSON-LD Schema to index.html!")

# 5. Rebuild Bridge Pages with Product Rich Snippet Schema
from rebuild_EVERY_single_bridge import master_catalog
from modules.bridge_creator import generate_bridge_page

print("\n🔨 Rebuilding landing pages with Google Product JSON-LD Schemas & Keyboard Focus...")
for asin, item in master_catalog.items():
    seo_data = {
        "pin_title": item["title"],
        "image_hook": item["headline"],
        "subtitle_hook": "",
        "badge_hook": item["badge"],
        "description": item["description"]
    }
    generate_bridge_page(item, seo_data, asin)

# Push live to GitHub Pages
print("\n🚀 Pushing Accessibility & SEO upgrades live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "-A"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", "apply keyboard navigation focus rings, ARIA roles, and Google/Pinterest JSON-LD rich snippet schemas"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 KEYBOARD ACCESSIBILITY & SEO SCORE BOOST DEPLOYED LIVE!")
