# 📌 Pinterest Auto Affiliate System — Project State & Resume Guide

**Project Directory:** `G:\CLI\pinterest-auto-affiliate`  
**Current Niche:** Cozy Room & Desk Setup Decor  
**Target Market:** International / US Audience (High purchasing power)  

---

## 🚦 API Integration Status

### ✅ Configured & Active Systems (`.env`)
1. **Amazon Associate Tag:** `AMAZON_ASSOCIATE_TAG=smartdeal0358-21`
   - *Role:* Attaches your affiliate ID to all Amazon links on generated bridge pages and mobile deep-links.
2. **SerpAPI Key:** `SERPAPI_KEY`
   - *Role:* Scrapes live, trending Amazon products matching any search query.
3. **Pollinations FLUX API:** `100% FREE` (No key required)
   - *Role:* Generates 3:4 vertical FLUX AI photorealistic cozy room scenes with zero cost.
4. **Google Fonts Typography:** Installed in `fonts/` (`PlayfairDisplay-Bold.ttf` & `Outfit-Bold.ttf`)
   - *Role:* Renders top amber pill badges ("✨ PINTEREST COZY FIND") and frosted-glass lower third headline cards.
5. **Vercel 1-Click Hosting Configuration:** [`vercel.json`](file:///G:/CLI/pinterest-auto-affiliate/vercel.json)
   - *Role:* Serves generated bridge landing pages & pin images live on the web.

---

## 🔑 Steps to Activate Direct Pinterest Posting & Live Hosting

1. **Add Pinterest API Credentials in [`.env`](file:///G:/CLI/pinterest-auto-affiliate/.env)**:
   ```env
   PINTEREST_ACCESS_TOKEN="your_pinterest_access_token_here"
   PINTEREST_BOARD_ID="your_target_board_id_here"
   ```
   *To get these:* Go to [developers.pinterest.com](https://developers.pinterest.com/), register an app, and generate an Access Token with `pins:write` and `boards:read` permissions.

2. **Set Live Web Bridge Domain in [`.env`](file:///G:/CLI/pinterest-auto-affiliate/.env)**:
   ```env
   BASE_BRIDGE_URL="https://your-pinterest-bridge.vercel.app"
   ```

3. **Deploy Bridge Pages & Images to Vercel**:
   ```powershell
   npx vercel --prod
   ```

4. **Update Gemini API Key** (optional):
   Replace `GEMINI_API_KEY` in `.env` if you'd like to use a specific new Gemini billing key, or let the built-in multi-model fallback chain handle generations automatically.

---

## 🏃 How to Run the Pipeline

```powershell
cd G:\CLI\pinterest-auto-affiliate
python main.py
```

All generated output graphics and bridge pages are saved to:
- **Images:** [`output/images/`](file:///G:/CLI/pinterest-auto-affiliate/output/images/)
- **Bridge Pages:** [`output/bridge_pages/`](file:///G:/CLI/pinterest-auto-affiliate/output/bridge_pages/)
- **Campaign Summary:** [`output/campaign_summary.json`](file:///G:/CLI/pinterest-auto-affiliate/output/campaign_summary.json)
