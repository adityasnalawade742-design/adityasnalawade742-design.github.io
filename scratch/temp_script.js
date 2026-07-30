
        let discoveredItems = [];
        let selectedAsins = new Set();
        let extractedBatchDetails = [];
        let batchSelectedPhotos = {};
        let batchCustomData = {}; // asin -> {title, badge, price}
        let currentBatchId = null;

        function escapeHTML(str) {
            if (!str) return '';
            return String(str).replace(/[&<>"']/g, function(m) {
                return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m];
            });
        }

        window.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeOverlayModal();
            }
        });

        function showToast(msg, icon = '✨') {
            const toast = document.getElementById('toast');
            document.getElementById('toastMsg').innerText = msg;
            document.getElementById('toastIcon').innerText = icon;
            toast.style.display = 'flex';
            setTimeout(() => { toast.style.display = 'none'; }, 4000);
        }

        function switchMode(mode) {
            document.getElementById('modeBatch').style.display = mode === 'batch' ? 'block' : 'none';
            document.getElementById('modeHomepage').style.display = mode === 'homepage' ? 'block' : 'none';
            document.getElementById('modeSingle').style.display = mode === 'single' ? 'block' : 'none';

            document.getElementById('tabBatch').classList.toggle('active', mode === 'batch');
            document.getElementById('tabHomepage').classList.toggle('active', mode === 'homepage');
            document.getElementById('tabSingle').classList.toggle('active', mode === 'single');

            if (mode === 'homepage') {
                loadHomepageProducts();
            }
        }

        function onTrendCategoryChange(val) {
            document.getElementById('customSearchInput').value = '';
        }

        function discoverProducts() {
            const customKw = document.getElementById('customSearchInput').value.trim();
            const categoryKw = document.getElementById('trendCategorySelect').value;
            const query = customKw || categoryKw;

            document.getElementById('discoverSpinner').style.display = 'inline-block';

            fetch(`/api/discover?query=${encodeURIComponent(query)}&count=10`)
                .then(r => r.json())
                .then(data => {
                    document.getElementById('discoverSpinner').style.display = 'none';
                    if (data.status === 'error') { alert("Error discovering products: " + data.message); return; }
                    discoveredItems = data.items || [];
                    renderDiscoverGrid(discoveredItems);
                    showToast(`Discovered ${discoveredItems.length} candidate products!`, "🔍");
                })
                .catch(err => {
                    document.getElementById('discoverSpinner').style.display = 'none';
                    alert("Error connecting to server backend.");
                });
        }

        function renderDiscoverGrid(items) {
            const grid = document.getElementById('discoverGrid');
            grid.innerHTML = '';
            selectedAsins.clear();

            items.forEach((item) => {
                const isPub = item.is_already_published;
                const card = document.createElement('div');
                card.className = `discover-card ${isPub ? 'published' : 'selected'}`;

                if (!isPub) selectedAsins.add(item.asin);

                card.innerHTML = `
                    ${isPub ? '<div class="pub-badge">ALREADY ON HOMEPAGE</div>' : ''}
                    <input type="checkbox" class="select-cb" ${!isPub ? 'checked' : ''} onchange="toggleProductSelection('${item.asin}', this.checked, this.parentNode)">
                    <img class="discover-thumb" src="${item.thumbnail || ''}" alt="${item.title}">
                    <div class="discover-body">
                        <div class="discover-title">${item.title}</div>
                        <div class="discover-meta">
                            <span class="discover-price">${item.price}</span>
                            <span class="discover-rating">★ ${item.rating}</span>
                        </div>
                    </div>
                `;
                grid.appendChild(card);
            });
            updateCounter();
        }

        function toggleProductSelection(asin, isChecked, cardElement) {
            if (isChecked) { selectedAsins.add(asin); cardElement.classList.add('selected'); }
            else { selectedAsins.delete(asin); cardElement.classList.remove('selected'); }
            updateCounter();
        }

        function updateCounter() {
            document.getElementById('selectionCounter').innerText = `${selectedAsins.size} Products Selected`;
        }

        function proceedToStep2PhotoVerification() {
            if (selectedAsins.size === 0) { alert("Please select at least 1 product."); return; }

            document.getElementById('panelStep1').style.display = 'none';
            document.getElementById('panelStep2').style.display = 'flex';
            document.getElementById('stepIndicator1').classList.remove('active');
            document.getElementById('stepIndicator2').classList.add('active');

            const asinsArray = Array.from(selectedAsins);
            showToast(`Extracting photo suites for ${asinsArray.length} products...`, "📸");

            fetch('/api/batch_extract', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ asins: asinsArray })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    extractedBatchDetails = data.items || [];
                    renderBatchPhotoBoards(extractedBatchDetails);
                } else { alert("Error extracting batch photos: " + data.message); }
            });
        }

        function renderBatchPhotoBoards(items) {
            const container = document.getElementById('batchPhotoBoards');
            container.innerHTML = '';
            batchSelectedPhotos = {};
            batchCustomData = {};

            items.forEach((item, pIdx) => {
                const systemWinner = item.winner_photo || (item.photos[0] ? item.photos[0].url : '');
                batchSelectedPhotos[item.asin] = systemWinner;
                batchCustomData[item.asin] = {
                    title: item.title,
                    price: item.price,
                    badge: "VIRAL ROOM FIND"
                };

                const box = document.createElement('div');
                box.className = 'batch-product-box';

                let photosHtml = '';
                item.photos.forEach((p, idx) => {
                    const isWinner = p.url === systemWinner;
                    let badgeClass = isWinner ? 'winner' : (p.status && p.status.includes('DISCARDED') ? 'discarded' : 'clean');
                    let badgeText = isWinner ? '🏆 #1 AI Winner' : (p.status || 'Clean Photo');

                    photosHtml += `
                        <div class="photo-pill-card ${isWinner ? 'selected' : ''}" id="pill-${item.asin}-${idx}" onclick="selectBatchPhoto('${item.asin}', '${p.url}', ${idx}, this.parentNode)">
                            <div class="photo-pill-badge ${badgeClass}">${badgeText}</div>
                            <img class="photo-pill-img" src="${p.url}" />
                        </div>
                    `;
                });

                box.innerHTML = `
                    <div class="batch-prod-header">
                        <div class="batch-prod-title">[Product #${pIdx+1}] ${item.title.substring(0, 65)}...</div>
                        <div style="font-weight: 800; color: var(--gold-primary);">${item.price}</div>
                    </div>
                    <div class="photos-row">${photosHtml}</div>
                    <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 12px; margin-top: 8px;">
                        <input type="text" class="input-field" style="padding: 10px 16px; font-size: 13px;" value="${item.title}" onchange="updateCustomData('${item.asin}', 'title', this.value)" placeholder="Custom Title / Image Hook">
                        <select class="select-field" style="padding: 10px; font-size: 13px;" onchange="updateCustomData('${item.asin}', 'badge', this.value)">
                            <option value="VIRAL ROOM FIND">✨ VIRAL ROOM FIND</option>
                            <option value="HOT DECOR FIND">🔥 HOT DECOR FIND</option>
                            <option value="BESTSELLER">🏆 BESTSELLER</option>
                            <option value="MUST HAVE">⭐ MUST HAVE</option>
                        </select>
                        <button class="btn-action" style="padding: 10px 16px; font-size: 13px; background: rgba(255,255,255,0.1);" onclick="previewOverlayLive('${item.asin}')">
                            👁️ Preview Overlay
                        </button>
                    </div>
                `;
                container.appendChild(box);
            });
        }

        function updateCustomData(asin, key, value) {
            if (!batchCustomData[asin]) batchCustomData[asin] = {};
            batchCustomData[asin][key] = value;
        }

        function previewOverlayLive(asin) {
            const photo = batchSelectedPhotos[asin];
            const custom = batchCustomData[asin] || {};

            showToast("Rendering 1200x1600 Graphic Overlay Preview...", "🎨");
            fetch('/api/preview_overlay', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    image_url: photo,
                    title: custom.title || "VIRAL ROOM FIND",
                    badge: custom.badge || "VIRAL ROOM FIND",
                    price: custom.price || "$19.99"
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('overlayModalImg').src = data.preview_url;
                    document.getElementById('overlayModal').style.display = 'flex';
                } else { alert("Overlay preview error: " + data.message); }
            });
        }

        function closeOverlayModal() {
            document.getElementById('overlayModal').style.display = 'none';
        }

        function selectBatchPhoto(asin, photoUrl, cardIdx, rowContainer) {
            batchSelectedPhotos[asin] = photoUrl;
            rowContainer.querySelectorAll('.photo-pill-card').forEach(c => c.classList.remove('selected'));
            const selectedCard = rowContainer.children[cardIdx];
            if (selectedCard) selectedCard.classList.add('selected');
            showToast(`Selected photo for ASIN ${asin}`, "🖼️");
        }

        function backToStep1() {
            document.getElementById('panelStep2').style.display = 'none';
            document.getElementById('panelStep1').style.display = 'flex';
            document.getElementById('stepIndicator2').classList.remove('active');
            document.getElementById('stepIndicator1').classList.add('active');
        }

        function launchBatchGeneration() {
            const itemsToRun = extractedBatchDetails.map(item => ({
                asin: item.asin,
                title: batchCustomData[item.asin]?.title || item.title,
                price: batchCustomData[item.asin]?.price || item.price,
                selected_photo: batchSelectedPhotos[item.asin] || item.winner_photo,
                prompt_strength: 0.35
            }));

            if (itemsToRun.length === 0) return;

            document.getElementById('batchLaunchSpinner').style.display = 'inline-block';
            document.getElementById('panelStep2').style.display = 'none';
            document.getElementById('panelStep3').style.display = 'flex';
            document.getElementById('stepIndicator2').classList.remove('active');
            document.getElementById('stepIndicator3').classList.add('active');

            fetch('/api/batch_generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ items: itemsToRun })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'processing') {
                    currentBatchId = data.batch_id;
                    showToast("Batch generation launched in background!", "⏳");
                    pollBatchStatus(currentBatchId);
                } else { alert("Error: " + data.message); }
            });
        }

        function pollBatchStatus(batchId) {
            const interval = setInterval(() => {
                fetch(`/api/batch_status?batch_id=${encodeURIComponent(batchId)}`)
                    .then(r => r.json())
                    .then(data => {
                        if (data.status === 'processing') {
                            document.getElementById('batchProgressBadge').innerText = `Processing ${data.current_index} of ${data.total}...`;
                            document.getElementById('batchStatusText').innerText = data.step || "Processing batch products...";
                            if (data.completed_items) renderBatchPreviews(data.completed_items);
                        } else if (data.status === 'success') {
                            clearInterval(interval);
                            document.getElementById('batchProgressBadge').innerText = `✅ Batch Complete (${data.completed_items ? data.completed_items.length : 0} Products Published)`;
                            document.getElementById('batchStatusText').innerText = data.step || "Batch run completed!";
                            showToast("All selected products published live to GitHub Pages!", "🚀");
                            if (data.completed_items) renderBatchPreviews(data.completed_items);
                        }
                    });
            }, 3000);
        }

        function renderBatchPreviews(completedItems) {
            const grid = document.getElementById('previewGrid');
            grid.innerHTML = '';
            completedItems.forEach(item => {
                const card = document.createElement('div');
                card.className = 'preview-card';
                card.innerHTML = `
                    <div style="font-weight: 800; font-size: 15px;">${item.title}</div>
                    <img class="preview-img" src="${item.hook_image}?v=${Date.now()}" alt="${item.title}" />
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; color: var(--gold-primary); font-size: 16px;">${item.price}</span>
                        <a href="${item.bridge_url}" target="_blank" class="btn-action" style="padding: 8px 16px; font-size: 12px; text-decoration: none;">
                            🔗 View Live Landing Page
                        </a>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        // =========================================================================
        // MODE C: HOMEPAGE SHOWCASE MANAGER & 1-CLICK DELETE
        // =========================================================================
        function loadHomepageProducts() {
            showToast("Loading active homepage products...", "🏠");
            fetch('/api/homepage_products')
                .then(r => r.json())
                .then(data => {
                    if (data.status === 'success') {
                        renderHomepageGrid(data.products || []);
                        showToast(`Loaded ${data.count || 0} homepage products!`, "✨");
                    } else {
                        alert("Error loading homepage products: " + (data.message || "Unknown error"));
                    }
                })
                .catch(err => alert("Error communicating with local server backend."));
        }

        function renderHomepageGrid(products) {
            const grid = document.getElementById('homepageProductsGrid');
            grid.innerHTML = '';

            if (products.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1/-1; padding: 40px; text-align: center; color: var(--text-sub); background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px dashed rgba(255,255,255,0.15);">📦 No products currently published on your homepage.<br><br>Use <b>Step 1 & Step 2</b> above to discover winning products and publish them live!</div>';
                return;
            }

            products.forEach(p => {
                const card = document.createElement('div');
                card.className = 'preview-card';
                card.id = `hp-card-${p.asin}`;
                card.innerHTML = `
                    <div style="font-weight: 800; font-size: 14px;">${escapeHTML(p.title)}</div>
                    <img class="preview-img" id="hp-img-${p.asin}" src="${p.image}" alt="${escapeHTML(p.title)}" />
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; color: var(--gold-primary);">${p.price}</span>
                        <a href="${p.bridge_url}" target="_blank" style="color: var(--gold-primary); font-size: 12px; text-decoration: none;">🔗 Open Page</a>
                    </div>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn-action" style="padding: 8px; font-size: 12px; flex: 1;" onclick="openTagEditorModal('${p.asin}')">
                            🏷️ Edit Price Tag Size
                        </button>
                        <button class="btn-action btn-danger" style="padding: 8px; font-size: 12px; width: 42px;" onclick="deleteHomepageProduct('${p.asin}')">
                            🗑️
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function deleteHomepageProduct(asin) {
            if (!confirm(`Are you sure you want to delete Product ASIN ${asin} from your homepage showcase?`)) return;

            showToast(`Deleting product ${asin} from homepage...`, "🗑️");
            fetch('/api/delete_homepage_product', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ asin: asin })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    const card = document.getElementById(`hp-card-${asin}`);
                    if (card) card.remove();
                    showToast(`Product ${asin} deleted and unblocked successfully!`, "✅");
                } else { alert("Delete error: " + data.message); }
            });
        }

        function runPriceSync() {
            document.getElementById('syncSpinner').style.display = 'inline-block';
            fetch('/api/sync_prices', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    document.getElementById('syncSpinner').style.display = 'none';
                    showToast("Daily prices synchronized live across 9 storefronts!", "🔄");
                    loadHomepageProducts();
                });
        }

        // =========================================================================
        // MODE A SINGLE ASIN EXTRACTION
        // =========================================================================
        function fetchSingleProductSuite() {
            const input = document.getElementById('targetInput').value.trim();
            if (!input) return;
            document.getElementById('extractSpinner').style.display = 'inline-block';

            fetch(`/api/extract?target=${encodeURIComponent(input)}`)
                .then(r => r.json())
                .then(data => {
                    document.getElementById('extractSpinner').style.display = 'none';
                    if (data.status === 'error') { alert(data.message); return; }
                    document.getElementById('metaTitle').innerText = data.title;
                    document.getElementById('metaAsin').innerText = `ASIN: ${data.asin}`;
                    document.getElementById('metaPrice').innerText = data.price;
                    document.getElementById('metaRating').innerText = `★ ${data.rating}`;
                    document.getElementById('productMetaPanel').style.display = 'grid';
                    showToast("Extracted single product photos!", "📸");
                });
        }

        let activeTagAsin = null;
        let currentTagPosX = null; // percentage left 0-100
        let currentTagPosY = null; // percentage top 0-100
        let isDraggingTag = false;
        let dragStartX, dragStartY, initialTagLeft, initialTagTop;

        let selectedTagColor = '#fb8500';
        let selectedPriceTextColor = '#111827';
        let selectedHeadlineColor = '#ffffff';
        let currentHeadlinePosY = null; // percentage top 0-100
        let isDraggingHeadline = false;
        let hlDragStartY, hlInitialTop;

        function setTagColor(hex) {
            selectedTagColor = hex;
            document.getElementById('tagCustomColorInput').value = hex;
            
            const tagOverlay = document.getElementById('liveTagOverlay');
            if (tagOverlay) {
                tagOverlay.style.borderColor = hex;
            }

            const liveTagImg = document.getElementById('liveTagImg');
            if (liveTagImg) {
                // Apply instant live CSS visual tint filter to price tag badge preview
                if (hex === '#fb8500') liveTagImg.style.filter = 'hue-rotate(0deg) saturate(1)';
                else if (hex === '#ff0055') liveTagImg.style.filter = 'hue-rotate(-35deg) saturate(2.5)';
                else if (hex === '#7a00ff') liveTagImg.style.filter = 'hue-rotate(85deg) saturate(2.5)';
                else if (hex === '#10b981') liveTagImg.style.filter = 'hue-rotate(140deg) saturate(2.5)';
                else if (hex === '#ffffff') liveTagImg.style.filter = 'brightness(1.6) contrast(1.2)';
                else if (hex === '#111827') liveTagImg.style.filter = 'brightness(0.15) contrast(1.5)';
                else liveTagImg.style.filter = 'sepia(0.5) saturate(2)';
            }
            showToast(`Tag color set to ${hex}`, "🎨");
        }

        function setPriceTextColor(hex) {
            selectedPriceTextColor = hex;
            document.getElementById('priceTextColorInput').value = hex;
            const priceEl = document.getElementById('liveTagPriceText');
            if (priceEl) priceEl.style.color = hex;
            showToast(`Price text color set to ${hex}`, "🎨");
        }

        function updateLiveTagPreview() {
            const scaleEl = document.getElementById('tagScaleSelect');
            if (!scaleEl) return;
            const scaleVal = scaleEl.value; // e.g. 380x285
            const [w, h] = scaleVal.split('x').map(Number);
            const rot = parseInt(document.getElementById('tagRotationRange')?.value || '-6');
            const fontScale = parseFloat(document.getElementById('priceTextScaleRange')?.value || '38') / 100.0;
            const offsetY = parseInt(document.getElementById('priceTextOffsetYRange')?.value || '15');
            const offsetX = parseInt(document.getElementById('priceTextOffsetXRange')?.value || '0');

            if (document.getElementById('tagRotationVal')) document.getElementById('tagRotationVal').innerText = `${rot}°`;
            if (document.getElementById('priceTextScaleVal')) document.getElementById('priceTextScaleVal').innerText = `${Math.round(fontScale * 100)}%`;
            if (document.getElementById('priceTextOffsetYVal')) document.getElementById('priceTextOffsetYVal').innerText = `${offsetY >= 0 ? '+' : ''}${offsetY}px`;
            if (document.getElementById('priceTextOffsetXVal')) document.getElementById('priceTextOffsetXVal').innerText = `${offsetX >= 0 ? '+' : ''}${offsetX}px`;

            // Calculate width percentage relative to 1200px master canvas
            const widthPct = (w / 1200) * 100;
            const liveTag = document.getElementById('liveTagOverlay');
            if (liveTag) {
                liveTag.style.width = `${widthPct}%`;
                liveTag.style.transform = `rotate(${rot}deg)`;
            }

            const priceEl = document.getElementById('liveTagPriceText');
            if (priceEl) {
                const liveTag = document.getElementById('liveTagOverlay');
                const tagPx = liveTag ? (liveTag.offsetWidth || 130) : 130;
                const calculatedPx = Math.round(tagPx * fontScale * 0.45);
                priceEl.style.fontSize = `${calculatedPx}px`;
                priceEl.style.color = selectedPriceTextColor;
                
                // Real-time visual position shift inside the tag badge
                const shiftYPercent = 58 + offsetY * 0.30;
                const shiftXPercent = 50 + offsetX * 0.30;
                priceEl.style.top = `${shiftYPercent}%`;
                priceEl.style.left = `${shiftXPercent}%`;
            }
        }

        function initDragAndDrop() {
            const tag = document.getElementById('liveTagOverlay');
            const container = document.getElementById('previewCanvasContainer');
            if (!tag || !container) return;

            function startDrag(e) {
                e.preventDefault();
                e.stopPropagation();
                isDraggingTag = true;
                tag.style.cursor = 'grabbing';
                tag.style.transition = 'none';

                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;

                dragStartX = clientX;
                dragStartY = clientY;

                const cRect = container.getBoundingClientRect();
                const tRect = tag.getBoundingClientRect();

                initialTagLeft = ((tRect.left - cRect.left) / cRect.width) * 100;
                initialTagTop = ((tRect.top - cRect.top) / cRect.height) * 100;
            }

            function moveDrag(e) {
                if (!isDraggingTag) return;
                e.preventDefault();
                const clientX = e.touches ? e.touches[0].clientX : e.clientX;
                const clientY = e.touches ? e.touches[0].clientY : e.clientY;

                const cRect = container.getBoundingClientRect();
                const deltaX = ((clientX - dragStartX) / cRect.width) * 100;
                const deltaY = ((clientY - dragStartY) / cRect.height) * 100;

                let newLeft = Math.max(0, Math.min(75, initialTagLeft + deltaX));
                let newTop = Math.max(0, Math.min(85, initialTagTop + deltaY));

                currentTagPosX = parseFloat(newLeft.toFixed(1));
                currentTagPosY = parseFloat(newTop.toFixed(1));

                tag.style.left = `${currentTagPosX}%`;
                tag.style.top = `${currentTagPosY}%`;
                tag.style.right = 'auto';
                tag.style.bottom = 'auto';

                if (document.getElementById('dragPosBadge')) {
                    document.getElementById('dragPosBadge').innerText = `📍 Position: X=${currentTagPosX}%, Y=${currentTagPosY}%`;
                }
            }

            function endDrag(e) {
                if (isDraggingTag) {
                    isDraggingTag = false;
                    tag.style.cursor = 'grab';
                    showToast(`Placed tag at X=${currentTagPosX}%, Y=${currentTagPosY}%`, "📍");
                }
            }

            tag.removeEventListener('mousedown', startDrag);
            tag.removeEventListener('touchstart', startDrag);

            tag.addEventListener('mousedown', startDrag, false);
            tag.addEventListener('touchstart', startDrag, { passive: false });

            document.removeEventListener('mousemove', moveDrag);
            document.removeEventListener('touchmove', moveDrag);
            document.removeEventListener('mouseup', endDrag);
            document.removeEventListener('touchend', endDrag);

            document.addEventListener('mousemove', moveDrag, { passive: false });
            document.addEventListener('touchmove', moveDrag, { passive: false });
            document.addEventListener('mouseup', endDrag, false);
            document.addEventListener('touchend', endDrag, false);
        function resetTagControlsToDefault() {
            fetch('/api/global_tag_defaults')
                .then(r => r.json())
                .then(d => {
                    if (d.status === 'success' && d.defaults) {
                        const g = d.defaults;
                        if (document.getElementById('tagScaleSelect')) document.getElementById('tagScaleSelect').value = `${g.tag_width}x${g.tag_height}`;
                        if (document.getElementById('tagRotationRange')) document.getElementById('tagRotationRange').value = g.tag_rotation;
                        if (document.getElementById('priceTextScaleRange')) document.getElementById('priceTextScaleRange').value = Math.round(g.price_font_scale * 100);
                        if (document.getElementById('priceTextOffsetYRange')) document.getElementById('priceTextOffsetYRange').value = g.price_text_offset_y;
                        if (document.getElementById('priceTextOffsetXRange')) document.getElementById('priceTextOffsetXRange').value = g.price_text_offset_x;
                        selectedTagColor = g.tag_color || '#fb8500';
                        selectedPriceTextColor = g.price_text_color || '#111827';
                        currentTagPosX = g.tag_pos_x || 61.0;
                        currentTagPosY = g.tag_pos_y || 75.0;
                    }
                    updateLiveTagPreview();
                    showToast("Reset price tag to saved system defaults", "🔄");
                })
                .catch(() => {
                    updateLiveTagPreview();
                });
        }

        function saveAsGlobalSystemDefault() {
            const scaleVal = document.getElementById('tagScaleSelect').value;
            const [w, h] = scaleVal.split('x').map(Number);
            const rot = parseInt(document.getElementById('tagRotationRange')?.value || '-6');
            const fontScale = parseFloat(document.getElementById('priceTextScaleRange')?.value || '20') / 100.0;
            const offsetY = parseInt(document.getElementById('priceTextOffsetYRange')?.value || '0');
            const offsetX = parseInt(document.getElementById('priceTextOffsetXRange')?.value || '0');
            const textPosY = 58.0 + (offsetY * 0.30);
            const textPosX = 50.0 + (offsetX * 0.30);

            showToast("Saving layout as system default for all future products...", "⭐");

            fetch('/api/save_global_defaults', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tag_width: w,
                    tag_height: h,
                    tag_rotation: rot,
                    tag_color: selectedTagColor,
                    price_text_color: selectedPriceTextColor,
                    price_font_scale: fontScale,
                    price_text_offset_x: offsetX,
                    price_text_offset_y: offsetY,
                    price_text_pos_x: textPosX,
                    price_text_pos_y: textPosY,
                    tag_pos_x: currentTagPosX,
                    tag_pos_y: currentTagPosY
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.status === 'success') {
                    showToast("⭐ Saved! All future products will use this default layout.", "✨");
                } else {
                    alert("Error saving global defaults: " + data.message);
                }
            })
            .catch(e => {
                console.error("[Save Global Defaults Error]", e);
                alert("Error saving defaults: " + e.message);
            });
        }

        function openTagEditorModal(asin, title, price) {
            activeTagAsin = asin;
            currentTagPosX = 61.0;
            currentTagPosY = 75.0;
            if (document.getElementById('dragPosBadge')) {
                document.getElementById('dragPosBadge').innerText = "📍 Tag: Default (X=61%, Y=75%)";
            }

            const tag = document.getElementById('liveTagOverlay');
            if (tag) {
                tag.style.left = 'auto';
                tag.style.top = 'auto';
                tag.style.right = '5%';
                tag.style.bottom = '8%';
            }

            const pTxt = document.getElementById('liveTagPriceText');
            if (pTxt && price) pTxt.innerText = price;

            document.getElementById('overlayModalImg').src = `./focus_product_${asin}_hook.jpg?t=${Date.now()}`;
            document.getElementById('overlayModal').style.display = 'flex';
            updateLiveTagPreview();
            setTimeout(initDragAndDrop, 100);
            
            // Set save button inside modal action box
            let saveBtn = document.getElementById('saveTagBtn');
            const actionBox = document.getElementById('modalSaveActionBox') || document.querySelector('#overlayModal .modal-content');
            if (!saveBtn) {
                saveBtn = document.createElement('button');
                saveBtn.id = 'saveTagBtn';
                saveBtn.className = 'btn-action btn-success';
                saveBtn.style.width = '100%';
                saveBtn.style.padding = '12px 20px';
                saveBtn.style.fontSize = '14px';
                saveBtn.innerHTML = '<div class="spinner" id="tagSaveSpinner"></div><span>🚀 Re-Render & Save Graphic Live</span>';
                saveBtn.onclick = saveTagCustomization;
                actionBox.appendChild(saveBtn);
            }
        }

        function saveTagCustomization() {
            if (!activeTagAsin) return;
            const scaleVal = document.getElementById('tagScaleSelect').value; // e.g. 380x285
            const [w, h] = scaleVal.split('x').map(Number);
            const rot = parseInt(document.getElementById('tagRotationRange')?.value || '-6');
            const fontScale = parseFloat(document.getElementById('priceTextScaleRange')?.value || '38') / 100.0;
            const offsetY = parseInt(document.getElementById('priceTextOffsetYRange')?.value || '15');
            const offsetX = parseInt(document.getElementById('priceTextOffsetXRange')?.value || '0');

            const saveSpinner = document.getElementById('tagSaveSpinner');
            if (saveSpinner) saveSpinner.style.display = 'inline-block';
            showToast(`Rendering Canva graphic via Playwright (${w}x${h}px, ${rot}°, ${selectedTagColor})...`, "🎨");

            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 45000);

            const textPosY = 58.0 + (offsetY * 0.30);
            const textPosX = 50.0 + (offsetX * 0.30);

            fetch('/api/customize_tag', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                signal: controller.signal,
                body: JSON.stringify({
                    asin: activeTagAsin,
                    tag_width: w,
                    tag_height: h,
                    tag_rotation: rot,
                    tag_color: selectedTagColor,
                    price_text_color: selectedPriceTextColor,
                    price_font_scale: fontScale,
                    price_text_offset_x: offsetX,
                    price_text_offset_y: offsetY,
                    price_text_pos_x: textPosX,
                    price_text_pos_y: textPosY,
                    tag_pos_x: currentTagPosX,
                    tag_pos_y: currentTagPosY
                })
            })
            .then(r => {
                clearTimeout(timeoutId);
                if (!r.ok) throw new Error(`HTTP ${r.status}: ${r.statusText}`);
                return r.json();
            })
            .then(data => {
                if (saveSpinner) saveSpinner.style.display = 'none';
                if (data.status === 'success') {
                    const newSrc = `${data.image}&t=${Date.now()}`;
                    document.getElementById('overlayModalImg').src = newSrc;
                    
                    // Dynamically update all matching card images on page
                    document.querySelectorAll('img').forEach(img => {
                        if (img.src.includes(activeTagAsin) || (img.id && img.id.includes(activeTagAsin))) {
                            img.src = newSrc;
                        }
                    });
                    
                    showToast("changed published", "✨");

                    // Insert prominent success banner inside modal
                    const actionBox = document.getElementById('modalSaveActionBox') || document.querySelector('#overlayModal .modal-content');
                    let pubBanner = document.getElementById('publishedNoticeBanner');
                    if (!pubBanner) {
                        pubBanner = document.createElement('div');
                        pubBanner.id = 'publishedNoticeBanner';
                        actionBox.appendChild(pubBanner);
                    }
                    pubBanner.style.cssText = "margin-top: 12px; padding: 14px; background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; border-radius: 12px; text-align: center; color: #10b981; font-weight: 800; font-size: 13.5px;";
                    const ghUrl = data.github_url || `https://adityasnalawade742-design.github.io/bridge_${activeTagAsin}.html?t=${Date.now()}`;
                    pubBanner.innerHTML = `
                        <div>✨ changed published</div>
                        <div style="font-size: 11.5px; color: #a7f3d0; margin-top: 4px; font-weight: 600;">Deploying automatically to GitHub Pages live!</div>
                        <div style="display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 10px;">
                            <a href="./bridge_${activeTagAsin}.html?t=${Date.now()}" target="_blank" style="padding: 8px 12px; background: #10b981; color: #000; font-weight: 800; border-radius: 8px; text-decoration: none; font-size: 12px;">🏠 Local Bridge Page</a>
                            <a href="${ghUrl}" target="_blank" style="padding: 8px 12px; background: #3b82f6; color: #fff; font-weight: 800; border-radius: 8px; text-decoration: none; font-size: 12px;">🚀 GitHub Pages Live →</a>
                        </div>
                    `;
                } else {
                    alert("Error customizing tag: " + data.message);
                }
            })
            .catch(e => {
                clearTimeout(timeoutId);
                if (saveSpinner) saveSpinner.style.display = 'none';
                console.error("[Customize Tag Error]", e);
                alert("Error communicating with server: " + e.message);
            });
        }

        window.onload = function() {
            discoverProducts();
        };
    