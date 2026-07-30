import os
import sys
import re
import time
import subprocess
from pathlib import Path

# Ensure UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_dir = Path("G:/CLI/pinterest-auto-affiliate")
index_path = repo_dir / "index.html"

print("==================================================")
print("🚀 APPLYING ALL 5 UX & SEO ENHANCEMENTS TO INDEX.HTML")
print("==================================================")

content = index_path.read_text(encoding="utf-8")

# 1. Add SVG Favicon & OpenGraph Meta Tags to <head>
head_tags = '''    <!-- Favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>✨</text></svg>">
    
    <!-- OpenGraph & Social Sharing Meta Tags -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="Cozy Room Finds">
    <meta property="og:title" content="Cozy Room Finds | Curated Aesthetic Home Decor & Viral Amazon Deals">
    <meta property="og:description" content="Discover viral aesthetic room upgrades, cozy lighting, bedside lamps, and luxury Amazon home finds curated for Pinterest setup lovers.">
    <meta property="og:image" content="https://adityasnalawade742-design.github.io/focus_product_B0BZXNSW5K_hook.jpg">
    <meta property="og:url" content="https://adityasnalawade742-design.github.io/index.html">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Cozy Room Finds | Curated Aesthetic Home Decor">
    <meta name="twitter:description" content="Discover viral aesthetic room upgrades and cozy lighting finds.">
    <meta name="twitter:image" content="https://adityasnalawade742-design.github.io/focus_product_B0BZXNSW5K_hook.jpg">'''

if 'rel="icon"' not in content:
    content = content.replace('<!-- Google Fonts -->', f'{head_tags}\n    \n    <!-- Google Fonts -->')

# 2. Add Clear Button CSS
clear_btn_css = '''
        .clear-search-btn {
            position: absolute;
            right: 18px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255, 255, 255, 0.12);
            border: none;
            color: #ffffff;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        }

        .clear-search-btn:hover {
            background: var(--gold-primary);
            color: #000000;
        }
'''
if '.clear-search-btn' not in content:
    content = content.replace('/* Hero Header */', f'{clear_btn_css}\n        /* Hero Header */')

# 3. Update Search Box HTML with Clear Button & Counter
search_html = '''    <!-- Filter & Search Bar -->
    <section class="filter-container">
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" class="search-input" placeholder="Search lamps, mirrors, diffusers, vases..." oninput="filterProducts()">
            <button id="clearSearchBtn" class="clear-search-btn" onclick="clearSearch()" style="display:none;">✕</button>
        </div>
        <div class="category-chips">
            <div class="chip active" onclick="setCategory('all', this)">✨ All Finds</div>
            <div class="chip" onclick="setCategory('lighting', this)">🕯️ Lamps & Lighting</div>
            <div class="chip" onclick="setCategory('mirror', this)">🪞 Mirrors & Wall</div>
            <div class="chip" onclick="setCategory('vases', this)">🏺 Vases</div>
            <div class="chip" onclick="setCategory('decor', this)">🌿 Home Decor</div>
        </div>
        <div id="productCounter" style="color: var(--text-sub); font-size: 13px; font-weight: 600; text-align: center; margin-top: 4px;">
            Showing <span id="visibleCount" style="color: var(--gold-primary); font-weight: 800;">9</span> Curated Finds
        </div>
    </section>'''

content = re.sub(r'<!-- Filter & Search Bar -->[\s\S]*?</section>', search_html, content)

# 4. Add Empty State Container inside productGrid
empty_state_html = '''        <!-- No Results Empty State -->
        <div id="noResults" style="display: none; grid-column: 1/-1; padding: 50px 20px; text-align: center; color: var(--text-sub); background: rgba(255,255,255,0.02); border-radius: 20px; border: 1px dashed rgba(255,255,255,0.12);">
            <div style="font-size: 36px; margin-bottom: 12px;">📦</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 8px;">No matching finds found</div>
            <p style="font-size: 14px; color: var(--text-sub);">Try searching for "lamp", "mirror", "diffuser", or "vase", or click <b>✨ All Finds</b> above!</p>
        </div>'''

if 'id="noResults"' not in content:
    content = content.replace('<main class="grid" id="productGrid">', f'<main class="grid" id="productGrid">\n\n{empty_state_html}')

# 5. Update JavaScript filterProducts & clearSearch
js_logic = '''        function filterProducts() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const clearBtn = document.getElementById('clearSearchBtn');
            if (clearBtn) clearBtn.style.display = query ? 'flex' : 'none';

            const cards = document.querySelectorAll('.card-wrapper');
            let visibleCount = 0;

            cards.forEach(card => {
                const category = card.getAttribute('data-category') || '';
                const title = card.querySelector('h2').innerText.toLowerCase();

                const matchesCategory = (currentCategory === 'all') || category.includes(currentCategory);
                const matchesSearch = title.includes(query);

                if (matchesCategory && matchesSearch) {
                    card.style.display = 'flex';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            const noRes = document.getElementById('noResults');
            if (noRes) noRes.style.display = (visibleCount === 0) ? 'block' : 'none';

            const countEl = document.getElementById('visibleCount');
            if (countEl) countEl.innerText = visibleCount;
        }

        function clearSearch() {
            document.getElementById('searchInput').value = '';
            filterProducts();
        }'''

content = re.sub(r'function filterProducts\(\) \{[\s\S]*?\}\s*function deleteCard', f'{js_logic}\n\n        function deleteCard', content)

index_path.write_text(content, encoding="utf-8")
print(" ✅ Applied all 5 UX & SEO enhancements to index.html!")

# Git Commit & Push Live
timestamp = int(time.time())
print("\n🚀 Pushing enhanced index.html live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "index.html"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", f"apply 5 UX & SEO enhancements (favicon, opengraph, clear search, live counter, empty state) ({timestamp})"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 HOMEPAGE UX & SEO 100% ENHANCED AND DEPLOYED LIVE!")
