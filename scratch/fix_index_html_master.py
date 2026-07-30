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
print("🛠️ POLISHING & REBUILDING INDEX.HTML HOMEPAGE GRID")
print("==================================================")

timestamp = int(time.time())

grid_html = f'''    <!-- Product Grid Gallery -->
    <main class="grid" id="productGrid">

        <!-- Card B0DZD1X83N (Minimalist Wood Base Lamp) -->
        <div class="card-wrapper" id="card-B0DZD1X83N" data-base-usd="12.99" data-category="lighting">
            <a class="card" href="./bridge_B0DZD1X83N.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$12.99</div>
                    <div class="card-rating">★ 4.6</div>
                    <img src="./focus_product_B0DZD1X83N_hook.jpg?v={timestamp}" alt="Minimalist Wood Base Bedside Table Lamp">
                </div>
                <div class="card-content">
                    <h2>Minimalist Wood Base Bedside Table Lamp</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0DZD1X83N', 'card-B0DZD1X83N')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0GYDXHF4G (Flame Diffuser) -->
        <div class="card-wrapper" id="card-B0GYDXHF4G" data-base-usd="35.00" data-category="lighting decor">
            <a class="card" href="./bridge_B0GYDXHF4G.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$35.00</div>
                    <div class="card-rating">★ 4.9</div>
                    <img src="./focus_product_B0GYDXHF4G_hook.jpg?v={timestamp}" alt="Flame Aroma Essential Oil Diffuser">
                </div>
                <div class="card-content">
                    <h2>Flame Aroma Essential Oil Diffuser</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0GYDXHF4G', 'card-B0GYDXHF4G')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0FXLYXM32 (Wavy Mirror) -->
        <div class="card-wrapper" id="card-B0FXLYXM32" data-base-usd="76.49" data-category="mirror mirrors decor">
            <a class="card" href="./bridge_B0FXLYXM32.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$76.49</div>
                    <div class="card-rating">★ 4.8</div>
                    <img src="./focus_product_B0FXLYXM32_hook.jpg?v={timestamp}" alt="White Wavy Wall Vanity Mirror">
                </div>
                <div class="card-content">
                    <h2>White Wavy Wall Vanity Mirror</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0FXLYXM32', 'card-B0FXLYXM32')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0C2YLN3H4 (Donut Vases) -->
        <div class="card-wrapper" id="card-B0C2YLN3H4" data-base-usd="14.99" data-category="vases decor">
            <a class="card" href="./bridge_B0C2YLN3H4.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$14.99</div>
                    <div class="card-rating">★ 4.9</div>
                    <img src="./focus_product_B0C2YLN3H4_exact2vases_hook.jpg?v={timestamp}" alt="White Ceramic Donut Vase Set of 2">
                </div>
                <div class="card-content">
                    <h2>White Ceramic Donut Vase Set of 2</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0C2YLN3H4', 'card-B0C2YLN3H4')">🗑️ Delete Product</button>
        </div>

        <!-- Card B07HP22QTZ (Crystal Suncatcher) -->
        <div class="card-wrapper" id="card-B07HP22QTZ" data-base-usd="9.99" data-category="decor">
            <a class="card" href="./bridge_B07HP22QTZ.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$9.99</div>
                    <div class="card-rating">★ 4.9</div>
                    <img src="./focus_product_B07HP22QTZ_hook.jpg?v={timestamp}" alt="Crystal Prism Window Suncatcher">
                </div>
                <div class="card-content">
                    <h2>Crystal Prism Window Suncatcher</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B07HP22QTZ', 'card-B07HP22QTZ')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0BZXNSW5K (Bedside Touch Lamp) -->
        <div class="card-wrapper" id="card-B0BZXNSW5K" data-base-usd="19.99" data-category="lighting">
            <a class="card" href="./bridge_B0BZXNSW5K.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$19.99</div>
                    <div class="card-rating">★ 4.5</div>
                    <img src="./focus_product_B0BZXNSW5K_hook.jpg?v={timestamp}" alt="Fenmzee Touch Bedside Table Lamp">
                </div>
                <div class="card-content">
                    <h2>Fenmzee Touch Bedside Table Lamp</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0BZXNSW5K', 'card-B0BZXNSW5K')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0DXKGL1T2 (Lily of the Valley Lamp) -->
        <div class="card-wrapper" id="card-B0DXKGL1T2" data-base-usd="38.57" data-category="lighting">
            <a class="card" href="./bridge_B0DXKGL1T2.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$38.57</div>
                    <div class="card-rating">★ 4.8</div>
                    <img src="./focus_product_B0DXKGL1T2_hook.jpg?v={timestamp}" alt="Lily of the Valley Flower Table Lamp">
                </div>
                <div class="card-content">
                    <h2>Lily of the Valley Flower Table Lamp</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0DXKGL1T2', 'card-B0DXKGL1T2')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0D1FRDFFX (Glass Mushroom Lamp) -->
        <div class="card-wrapper" id="card-B0D1FRDFFX" data-base-usd="35.98" data-category="lighting">
            <a class="card" href="./bridge_B0D1FRDFFX.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$35.98</div>
                    <div class="card-rating">★ 4.8</div>
                    <img src="./focus_product_B0D1FRDFFX_hook.jpg?v={timestamp}" alt="Glass Mushroom Table Lamp">
                </div>
                <div class="card-content">
                    <h2>Glass Mushroom Table Lamp</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0D1FRDFFX', 'card-B0D1FRDFFX')">🗑️ Delete Product</button>
        </div>

        <!-- Card B0D8P8CSYP (Cute Bird Lamp) -->
        <div class="card-wrapper" id="card-B0D8P8CSYP" data-base-usd="20.56" data-category="lighting">
            <a class="card" href="./bridge_B0D8P8CSYP.html">
                <div class="card-img-container">
                    <div class="card-price-tag">$20.56</div>
                    <div class="card-rating">★ 4.8</div>
                    <img src="./focus_product_B0D8P8CSYP_hook.jpg?v={timestamp}" alt="Cute Bird Dimmable Touch Night Lamp">
                </div>
                <div class="card-content">
                    <h2>Cute Bird Dimmable Touch Night Lamp</h2>
                    <div class="card-cta">
                        <span>View Details</span>
                        <span class="arrow">→</span>
                    </div>
                </div>
            </a>
            <button class="delete-btn" onclick="deleteCard('B0D8P8CSYP', 'card-B0D8P8CSYP')">🗑️ Delete Product</button>
        </div>

    </main>'''

content = index_path.read_text(encoding="utf-8")
new_content = re.sub(r'<!-- Product Grid Gallery -->[\s\S]*?</main>', grid_html, content)
index_path.write_text(new_content, encoding="utf-8")

print(" ✅ Rebuilt main product grid on index.html!")

# Update category chips on index.html to match categories
chips_html = '''        <div class="category-chips">
            <div class="chip active" onclick="setCategory('all', this)">✨ All Finds</div>
            <div class="chip" onclick="setCategory('lighting', this)">🕯️ Lamps & Lighting</div>
            <div class="chip" onclick="setCategory('mirror', this)">🪞 Mirrors & Wall</div>
            <div class="chip" onclick="setCategory('vases', this)">🏺 Vases</div>
            <div class="chip" onclick="setCategory('decor', this)">🌿 Home Decor</div>
        </div>'''

new_content = re.sub(r'<div class="category-chips">[\s\S]*?</div>\s*</section>', f'{chips_html}\n    </section>', new_content)
index_path.write_text(new_content, encoding="utf-8")

print(" ✅ Updated category filter chips on index.html!")

# Push live to GitHub Pages
print("\n🚀 Pushing fixed index.html live to GitHub Pages...")
try:
    subprocess.run(["git", "add", "index.html"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "commit", "-m", f"fix index.html category filters, missing ratings, title sync & delete button visibility ({timestamp})"], cwd=str(repo_dir), check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_dir), check=True)
    print(" ✅ Git Commit & Push 100% Successful!")
except Exception as e:
    print(f" ⚠️ Git push warning: {e}")

print("\n🎉 INDEX.HTML HOMEPAGE POLISHED & DEPLOYED LIVE!")
