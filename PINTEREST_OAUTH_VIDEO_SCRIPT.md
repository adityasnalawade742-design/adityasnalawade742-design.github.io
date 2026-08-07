# 🎬 Master Pinterest API Standard Access Approval Video Script (OAuth Centric)

> **Target Video Length**: 1:45 – 2:15 minutes  
> **Key Objective**: Satisfy Pinterest reviewer requirements by proving the complete OAuth 2.0 connection flow, API v5 Pin publishing (`201 Created`), non-spam content quality, and compliant mobile landing page with FTC disclaimers.

---

## 📌 Pre-Recording Security & Setup Checklist

Before pressing record, make sure to verify:
- [ ] **Incognito / Fresh Browser Profile**: Open an incognito browser window to showcase the clean OAuth consent screen without pre-saved sessions.
- [ ] **App Name Alignment**: Ensure application name (`Cozy Room Decor Publisher Pro`) matches across Developer Dashboard, OAuth Consent Screen, and Website.
- [ ] **Security Masking**: Hide or mask Client Secret, Bearer Tokens, Refresh Tokens, and API Keys.
- [ ] **Forbidden Words**: Do **NOT** mention scraping, SerpAPI, HSV color filters, FLUX/AI generation details, 0ms redirect tricks, or affiliate commission models. Focus 100% on high-quality home decor marketing & Pinterest API compliance.

---

## 🎬 Step-by-Step Video Recording Timeline & Script

---

### Scene 1 — Developer Dashboard (0:00 – 0:12)
* **Screen**: Pinterest Developer Portal (`developers.pinterest.com/apps/`).
* **Visual Focus**: Hover cursor over **App Name** (`Cozy Room Decor Publisher Pro`), **App ID** (`1596368`), **Website URL**, and **Privacy Policy URL**.
* **Narration**:
  > *"Hello Pinterest Review Team. This is a demonstration of my application, Cozy Room Decor Publisher Pro. In this video, I'll show the complete Pinterest OAuth connection flow and how the application uses the Pinterest API v5 to publish original home décor Pins."*

---

### Scene 2 — Application / Workflow Dashboard (0:12 – 0:22)
* **Screen**: Your web application or n8n visual workflow interface.
* **Visual Focus**: Overview of the workflow dashboard. *Do not click Publish yet.*
* **Narration**:
  > *"This application creates original Pinterest content from selected home décor products and publishes it through the Pinterest API."*

---

### Scene 3 — OAuth Authorization Flow (0:22 – 0:50) ⭐ [MOST CRITICAL STEP]
* **Screen**: 
  1. Click **"Connect Pinterest"** button.
  2. The official Pinterest OAuth authorization page loads (`https://www.pinterest.com/oauth/...`).
  3. Show requested scopes (`boards:read`, `boards:write`, `pins:read`, `pins:write`).
  4. Click **"Authorize"**.
  5. Page redirects back to your application showing **"Connected Successfully"**.
  6. Pause and leave the success screen visible for 3–5 seconds.
* **Narration**:
  > *"The user connects their Pinterest account through Pinterest's official OAuth 2.0 authorization flow. After authorization, the application receives an access token and can publish Pins on behalf of the connected Pinterest account."*

> [!CAUTION]
> Ensure your Client Secret and Access Tokens are masked or kept hidden during this step.

---

### Scene 4 — Content Preparation (0:50 – 1:10)
* **Screen**: Display one curated product card.
* **Visual Focus**: Highlight the prepared original marketing image, Pin title, Pin description, and destination landing page URL.
* **Narration**:
  > *"The application prepares an original marketing image, Pinterest title, description, and landing page before publishing."*

---

### Scene 5 — HTTP Request & 201 Created API Response (1:10 – 1:30)
* **Screen**: Open the HTTP Request node / API execution window.
* **Visual Focus**:
  - Endpoint: `POST https://api.pinterest.com/v5/pins`
  - Header: `Authorization: Bearer ********` (Masked token)
  - JSON Body payload: `board_id`, `title`, `description`, `link`, `media_source`
  - Execute request.
  - Show response: `201 Created` and Pin ID (e.g. `"id": "1092545259543920271"`).
* **Narration**:
  > *"The application sends a POST request to Pinterest API v5. Pinterest returns a successful 201 Created response together with the new Pin ID."*

---

### Scene 6 — Live Pinterest Board Verification (1:30 – 1:50)
* **Screen**: Open Pinterest in your browser.
* **Visual Focus**:
  - Refresh your Pinterest Board.
  - Click on the newly published Pin.
  - Let the reviewer clearly inspect the Pin title, image, description, and target board.
* **Narration**:
  > *"Here is the published Pin live on our Pinterest board, complete with high-resolution visual layout, description, and target board placement."*

---

### Scene 7 — Compliant Landing Page & FTC Disclosure (1:50 – 2:10)
* **Screen**: Click the destination link on the Pin.
* **Visual Focus**:
  - Landing page opens (`adityasnalawade742-design.github.io`).
  - Scroll down slowly.
  - Show product details, **FTC Affiliate Disclaimer**, and **Contact / Privacy Policy** link.
* **Narration**:
  > *"Clicking the Pin opens our mobile-optimized landing page, which features clear product specifications, full FTC disclosure compliance, contact information, and privacy policy links."*

---

### Ending — Closing Statement (2:10 – 2:15)
* **Screen**: Return to application dashboard or stay on landing page.
* **Narration**:
  > *"The Pin has been successfully published using Pinterest API v5 and links to our landing page. Thank you for reviewing our application."*
* **Action**: Stop recording.

---

## 🛠️ Summary Checklist

| Scene | Timestamp | Key Action | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **Scene 1** | `0:00 - 0:12` | Developer Dashboard | Show App ID, Website & Privacy Policy |
| **Scene 2** | `0:12 - 0:22` | App Dashboard | Introduce system scope |
| **Scene 3** | `0:22 - 0:50` | OAuth Flow | Prove full OAuth 2.0 authorization |
| **Scene 4** | `0:50 - 1:10` | Content Prep | Show original image & SEO metadata |
| **Scene 5** | `1:10 - 1:30` | API Execution | Show `POST /v5/pins` & `201 Created` |
| **Scene 6** | `1:30 - 1:50` | Pinterest Board | Verify Pin live on board |
| **Scene 7** | `1:50 - 2:10` | Landing Page | Show FTC disclaimer & Privacy link |
| **Ending** | `2:10 - 2:15` | Closing Statement | Thank reviewer & stop recording |
