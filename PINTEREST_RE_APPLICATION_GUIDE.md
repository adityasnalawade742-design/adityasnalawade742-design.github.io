# 📌 Pinterest API Standard Access Master Demo Video Guide (n8n Workflow Edition)

---

## 🎯 Executive Summary & App Details

- **App Name**: `Cozy Room Decor Publisher Pro`
- **Company Name**: `Cozy Room Finds`
- **App ID**: `1596368` (Trial Access Pending)
- **Developer Contact Email**: `aditya.s.nalawade742@gmail.com`
- **Website Domain**: `https://adityasnalawade742-design.github.io`
- **Privacy Policy**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
- **Terms of Service**: `https://adityasnalawade742-design.github.io/terms-of-service.html`
- **n8n Workflow File**: [`n8n_pinterest_affiliate_workflow.json`](file:///G:/CLI/pinterest-auto-affiliate/n8n_pinterest_affiliate_workflow.json)

---

## 🎬 Master 10-Step Video Recording Script (n8n + Loom / OBS Recording)

Record your desktop screen using **Loom** or **OBS Studio**. Set Loom link permissions to **"Anyone with the link can view"**. **Do not crop the browser address bar!**

---

### ⏱️ The 10-Step Recording Sequence in n8n:

#### **Step 1 — Show App Overview in Pinterest Developer Portal [0:00 – 0:20]**
- **Screen**: Pinterest Developer Dashboard (`developers.pinterest.com/apps/1596368`).
- **Action**: Hover cursor over **App Name** (`Cozy Room Decor Publisher Pro`), **App ID** (`1596368`), and **Company Name** (`Cozy Room Finds`).
- **🎙️ Script**:
  > *"Hello Pinterest Review Team. My name is Aditya. This is my application, Cozy Room Decor Publisher Pro, App ID 1596368, developed by Cozy Room Finds. We use n8n to manage and publish curated room decor Pins to our connected Pinterest account."*

---

#### **Step 2 — Show Website & Legal Pages [0:20 – 0:40]**
- **Screen**: Open homepage (`https://adityasnalawade742-design.github.io/index.html`).
- **Action**: Scroll down slowly. Highlight:
  - Company Name (`Cozy Room Finds`)
  - App Name (`Cozy Room Decor Publisher Pro`)
  - Privacy Policy Link & Terms of Service Link
  - Direct Contact Email (`aditya.s.nalawade742@gmail.com`)
- **🎙️ Script**:
  > *"This is our official website hosting our product showcase, privacy policy, terms of service, and direct developer contact email."*

---

#### **Step 3 — Show n8n Workflow Canvas [0:40 – 0:50]**
- **Screen**: Open n8n Canvas (`n8n_pinterest_affiliate_workflow.json`).
- **Action**: Point mouse across the nodes:
  `1. Webhook / Item Trigger` ➔ `2. Format Product Data` ➔ `3. AI Visual Generator` ➔ `4. SEO Metadata` ➔ `5. Publish to Pinterest API v5`.
- **🎙️ Script**:
  > *"Here is our n8n visual workflow canvas showing every step of the content preparation and publishing process."*

---

#### **Step 4 — Show n8n OAuth 2.0 Account Connection [0:50 – 1:30]**
- **Screen**: Click on the **5. Publish to Pinterest API v5** HTTP Request Node in n8n.
- **Action 1**: Under Credentials, click **Connect Account** (or **OAuth 2.0 Connection**).
- **Action 2**: The browser opens `https://www.pinterest.com/oauth/?client_id=1596368...`. Ensure the address bar is fully visible!
- **Action 3**: **Hold on the permissions screen for 8 to 10 seconds**. Hover cursor over requested scopes:
  - `boards:read`, `boards:write`
  - `pins:read`, `pins:write`
- **Action 4**: Click **Allow**.
- **Action 5**: Show browser redirect back to n8n with green badge **"Account Connected Successfully"**.
- **🎙️ Script**:
  > *"Clicking Connect Account opens Pinterest's official OAuth authorization page. The user sees the requested permissions for boards and pins and clicks Allow. n8n completes the redirect and confirms the account connection."*

---

#### **Step 5 — Verify "Connected Account" Status in n8n [1:30 – 1:40]**
- **Screen**: n8n Credential Window.
- **Action**: Point cursor to the connected credential showing **Pinterest API v5 (Connected Account: @adityasnalawade0703)**.
- **🎙️ Script**:
  > *"n8n shows our verified account adityasnalawade0703 is now securely connected."*

---

#### **Step 6 — User Triggers Single Item Execution [1:40 – 2:00]**
- **Screen**: n8n Workflow Canvas.
- **Action**: Click **Test Step** or **Execute Node** on the Pinterest API Node.
- **🎙️ Script**:
  > *"We now trigger the node to publish the curated item to our connected account."*

---

#### **Step 7 — Show n8n Green Execution Output [2:00 – 2:15]**
- **Screen**: n8n Execution Output Panel.
- **Action**: Show green success badge on the node and returned Pin ID.
- **🎙️ Script**:
  > *"n8n prepares the Pin and posts it via Pinterest API v5, returning a success response."*

---

#### **Step 8 — Refresh Pinterest Board & Open Live Pin [2:15 – 2:40]**
- **Screen**: Go to Pinterest profile `@adityasnalawade0703` on board **Cozy Room & Desk Decor**.
- **Action**: **Click Refresh in the browser on camera**. Click open the newly created Pin.
- **🎙️ Script**:
  > *"Refreshing our Pinterest board on camera, the new Pin appears immediately. Opening the Pin shows our title, description, and destination link."*

---

#### **Step 9 — Open Destination Landing Page [2:40 – 3:05]**
- **Screen**: Click destination link on the Pin (`bridge_*.html`).
- **Action**: Scroll down landing page. Highlight:
  - Company Name (`Cozy Room Finds`) & App Name (`Cozy Room Decor Publisher Pro`)
  - Amazon Affiliate FTC Disclosure Badge
  - Contact Email (`aditya.s.nalawade742@gmail.com`)
- **🎙️ Script**:
  > *"Clicking the Pin takes the user directly to our landing page, which features clear product information, affiliate disclosures, and developer contact details."*

---

#### **Step 10 — Closing Statement [3:05 – 3:15]**
- **🎙️ Script**:
  > *"Thank you for reviewing our application for Standard Access. We appreciate your time!"*

---

## 📝 Copy-Paste Answers for Pinterest Developer Portal Re-Submission

### Question 1: Describe the primary use case of your application.
> Our application, "Cozy Room Decor Publisher Pro" (App ID: 1596368, developed by "Cozy Room Finds"), utilizes n8n workflow automation to review, curate, and publish home decor recommendations. The workflow formats product specifications, generates visual previews, creates SEO titles and descriptions, and publishes Pins to designated boards via official Pinterest API v5 (`POST /v5/pins`) after OAuth 2.0 user authorization. Every Pin directs users to a compliant, responsive landing page featuring product information, FTC affiliate disclosures, and privacy policy links containing direct developer contact (aditya.s.nalawade742@gmail.com).

### Question 2: How does your application ensure compliance with Pinterest Developer Terms & Spam Policies?
> We adhere strictly to Pinterest Developer Terms:
> 1. Official OAuth 2.0 User Consent: All API requests use official OAuth 2.0 authorization where the user explicitly grants board and pin permissions (`boards:read`, `boards:write`, `pins:read`, `pins:write`).
> 2. User-Initiated Actions: Pins are published only after an account has been authorized by the user and the action is explicitly initiated. We do not perform non-consensual profile modifications or automated spamming.
> 3. Rate Limiting: Requests are strictly throttled (1 Pin per manual execution) to ensure high-quality, authentic posting.
> 4. Transparent Links: All destination URLs point exclusively to our verified GitHub Pages domain (`adityasnalawade742-design.github.io`), which hosts compliant landing pages with explicit FTC affiliate disclaimers and developer contact email (`aditya.s.nalawade742@gmail.com`).
> 5. Credential Security: OAuth credentials and access tokens are managed securely within n8n environment variables for authentication, and no user profile data is sold, traded, or cached.
