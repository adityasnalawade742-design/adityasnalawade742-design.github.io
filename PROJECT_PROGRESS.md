# 🚀 Project Progress & Architecture State Guide

> **Last Updated**: August 2, 2026  
> **System Status**: Fully Operational (HTTP 200) on `http://localhost:5000`  
> **Main Purpose**: Pinterest Auto-Affiliate Automation System & Master Web Console 3.0

---

## 📌 Executive Summary of Progress & Completed Work

### 1. 🖼️ Product Discovery & Image Loading Architecture (Fixed & Optimized)
- **Problem**: Product discovery in Web Console failed to load product images or showed broken thumbnails because it was running heavy pixel-analysis algorithms (`has_text_annotation`, `is_grid_collage`, `has_human_presence`) synchronously during discovery, causing requests to time out or fall back to CORS-blocked URLs.
- **Solution Implemented**:
  - Rewrote `handle_api_discover` in `web_console_server.py` to fetch high-res `m.media-amazon.com` image URLs directly from memory during search.
  - Implemented async background image caching into `raw_images/raw_{ASIN}.jpg`.
  - Upgraded browser `<img>` rendering with `referrerpolicy="no-referrer"` to bypass Amazon CDN hotlink protection.
  - Added smart fallback image resolution via `/api/fetch_image`.

### 2. 🔑 SerpAPI Multi-Key Engine Upgrade (6 Active Keys)
- **Problem**: The Google SerpAPI search engine (`engine: google`) returned 0 thumbnails in organic search results and frequently ran out of API credits.
- **Solution Implemented**:
  - Switched primary SerpAPI engine to `engine: amazon` in `modules/amazon_finder.py`. The Amazon engine returns ASINs, thumbnails, prices, and ratings directly on every result.
  - Configured 6 active SerpAPI keys in `.env` (`SERPAPI_KEY` through `SERPAPI_KEY_6`) providing **1,100+ total monthly search credits**.
  - Added automatic key failover when quota is exhausted on any key.

### 3. 🔍 Photo Zoom Lightbox Feature (Step 2 Review & Override)
- **Feature Added**: Added full-resolution Lightbox photo preview in **Step 2 (Review & Override Images)** in `admin_console.html`.
- **Interactions**:
  - Hover over any candidate photo or the Chosen Photo to see a `🔍` zoom button overlay.
  - Double-click any photo or click `🔍` to open a glassmorphism fullscreen modal.
  - Select winner photos directly inside the Lightbox modal via **`✓ Pick This Photo`**.
  - Keyboard shortcut: `Escape` key closes the zoom view.

### 4. 🛠️ Complete Server & Import Debugging
- Fixed missing module imports (`import urllib.parse`, `import urllib.request`) in `web_console_server.py` and `modules/amazon_finder.py`.
- Fixed process hang / port conflicts on port 5000.
- Audited all 12 Web Console endpoints (`/api/discover`, `/api/fetch_image`, `/api/homepage_products`, `/api/matrix`, `/api/prepare_n8n_batch`, `/api/reject_product`, `/api/logs`, etc.) — all 12 pass with HTTP 200.

---

## 🛠️ System Components & Directory Map

```text
pinterest-auto-affiliate/
├── admin_console.html         # Master Web Console 3.0 UI Dashboard
├── web_console_server.py       # Multi-threaded Python Web Console Server (Port 5000)
├── config.py                  # Environment config & SerpAPI key rotation manager
├── .env                       # API keys, Associate Tag, Niche configuration
├── index.html                 # Live storefront showcase page
├── product_registry.xlsx      # Master Excel database of published & rejected ASINs
├── serpapi_cache.json         # Search result cache to conserve API credits
├── cache/
│   ├── image_cache.db         # SQLite permanent image URL cache
│   └── registry.db            # SQLite registry database
├── raw_images/                # Downloaded raw product images (raw_{ASIN}.jpg)
├── modules/
│   ├── amazon_finder.py       # Live product catalog search (SerpAPI Amazon engine)
│   ├── amazon_extractor.py    # Multi-photo suite extractor & photo quality scorer
│   ├── bridge_creator.py      # Standalone HTML bridge page & schema.org generator
│   ├── html_overlay_engine.py # Hook image overlay generator
│   ├── product_registry.py    # Registry state manager & Excel sync
│   └── automated_product_selector.py # Deduplication & index.html parser
└── scratch/                   # System diagnostic & test scripts
```

---

## 🔑 Environment Configuration (`.env`)

```env
GEMINI_API_KEY=AQ.Ab8...
AMAZON_ASSOCIATE_TAG=smartdeal0358-21
NICHE="Home Decor"
OUTPUT_DIR="./output"

SERPAPI_KEY=cc9f45c2d831...
SERPAPI_KEY_2=e84a6b288e36...
SERPAPI_KEY_3=52c4235f8674...
SERPAPI_KEY_4=f671351c109f...
SERPAPI_KEY_5=a004722a...
SERPAPI_KEY_6=789dea48...
```

---

## 🚀 How to Run & Maintain the System

1. **Start the Web Console Server**:
   ```bash
   python -u web_console_server.py
   ```
2. **Access Dashboard**:
   Open **`http://localhost:5000`** in any web browser.
3. **Run Full System Health Check**:
   ```bash
   python -u scratch/full_system_diagnostic.py
   ```

---

## 💡 Quick Tips for Future Conversations / AI Sessions

If starting a new session or switching accounts, simply refer to this document (`PROJECT_PROGRESS.md`). All features, API endpoints, key rotations, and server fixes are documented here for seamless continuation.
