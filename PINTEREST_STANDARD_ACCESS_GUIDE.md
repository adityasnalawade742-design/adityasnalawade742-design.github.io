# 📘 Comprehensive Step-by-Step Guide: Pinterest API Standard Access Approval

---

## 📑 Executive Overview

To unlock **Production Standard Access** (`https://api.pinterest.com/v5/pins`), Pinterest requires developers to submit a functional application and a **60–90 second Loom screen recording** proving:
1. The app uses legitimate OAuth authentication with proper scopes.
2. Content generated is high quality, non-spammy, and relevant to the selected board.
3. Destination links lead to compliant, mobile-optimized landing pages containing clear affiliate disclaimers and privacy policies.

---

## 🔑 Phase 1: Generating the Correct Pinterest OAuth Token

Currently, Pinterest tokens generated without explicit write permissions will fail with `401 Unauthorized` (`Missing: ['boards:write', 'pins:write']`).

### Step-by-Step Instructions:

1. Open the [Pinterest Developer Portal Apps Dashboard](https://developers.pinterest.com/apps/).
2. Click on your application: **`Cozy Room Decor Publisher Pro`** (App ID: `1596368`).
3. In the left navigation menu, click **"Generate access token"** (or **"OAuth Tokens"**).
4. Under **Select Scopes**, check the following 4 boxes:
   - `boards:read`
   - `boards:write`
   - `pins:read`
   - `pins:write`
5. Click **Generate Token**.
6. Copy the resulting access token (string starting with `pina_...`).
7. Open your local `.env` file at `G:\CLI\pinterest-auto-affiliate\.env` and update the value:
   ```env
   PINTEREST_ACCESS_TOKEN="pina_YOUR_NEW_TOKEN_HERE"
   ```

---

## 🛠️ Phase 2: Choosing Your Video Recording Method

You can record the video demo using either **Method A (n8n Visual Builder - Recommended)** or **Method B (Terminal / Python Bridge Script)**.

---

### Method A: Using n8n (Visual Workflow Builder - Preferred by Reviewers)

1. Open **n8n** (Cloud or Local Desktop).
2. Click **Workflows** → **Import from File**.
3. Select `G:\CLI\pinterest-auto-affiliate\n8n_pinterest_affiliate_workflow.json`.
4. Double-click the **Publish to Pinterest API v5** HTTP Request node.
5. Under **Headers**, set:
   - `Authorization`: `Bearer pina_YOUR_NEW_TOKEN_HERE`
6. Under **Body Parameters**, verify payload:
   - `board_id`: `1092545259543920271`
   - `title`: `{{ $json.pin_title }}`
   - `description`: `{{ $json.description }}`
   - `link`: `{{ $json.bridge_url }}`
   - `media_source`: `{"source_type": "image_url", "url": "{{ $json.image_url }}"}`

---

### Method B: Using Local Terminal (Python Bridge Script)

If you don't use n8n, you can run the exact automated bridge command in PowerShell:

```powershell
cd G:\CLI\pinterest-auto-affiliate
python n8n_local_bridge.py --asin B0GGHJ1J4L
```

---

## 🎬 Phase 3: Exact 60–90 Second Screen Recording Script

Record using **Loom**, **OBS Studio**, or **Windows Game Bar** (`Win + Alt + R`). Make sure your mic is active or add clear captions.

---

### ⏱️ Minute-by-Minute Recording Workflow:

#### **[0:00 – 0:15] Developer Portal Setup**
- **Action**: Display browser tab showing `developers.pinterest.com/apps/1596368`. Point your cursor to **App ID: 1596368** and **App Name: Cozy Room Decor Publisher Pro**.
- **Voiceover / Script**:
  > *"Hello Pinterest API Review Team. This is a live demonstration of our automated content publishing integration for our app Cozy Room Decor Publisher Pro, App ID 1596368."*

#### **[0:15 – 0:45] Workflow & API Request Execution**
- **Action**: Switch to n8n (or PowerShell terminal). Click on the **Publish Pin to Pinterest API v5** node (or run the python command). Click **Execute Node**.
- **Voiceover / Script**:
  > *"Our system curates top home decor items, generates vertical high-resolution aesthetic visuals, builds dedicated responsive landing pages, and posts the formatted payload directly to the Pinterest v5 Pins endpoint."*

#### **[0:45 – 1:00] Verify API Response `201 Created`**
- **Action**: Zoom in / highlight the HTTP JSON response body showing:
  - `Status: 201 Created`
  - `"id": "1092545..."`
- **Voiceover / Script**:
  > *"As seen here, the Pinterest API v5 endpoint returns a successful 201 Created status along with the unique Pin ID."*

#### **[1:00 – 1:30] Live Pin & Landing Page Verification**
- **Action**: Open Pinterest in your browser, go to your business profile (`@adityasnalawade0703`), and refresh the board **Cozy Room & Desk Decor**.
- **Action**: Click the newly created Pin. Point out the title, description, and high-quality image.
- **Action**: Click the outbound destination link on the Pin. Show that it opens `https://adityasnalawade742-design.github.io/bridge_B0GGHJ1J4L.html`.
- **Voiceover / Script**:
  > *"The pin is live on our verified board. Clicking the pin leads directly to our mobile landing page, complete with privacy policy, Amazon affiliate disclaimers, and direct purchasing options. Thank you for reviewing our application for Standard Access!"*

---

## 📝 Phase 4: Standard Access Application Form Copy-Paste Answers

When filling out the application in the **Pinterest Developer Portal**, copy and paste the following pre-written, policy-compliant responses:

---

### Question 1: Describe the primary use case of your application.
> **Answer**:
> Our application, "Cozy Room Decor Publisher Pro", automates the curation and distribution of high-quality home decor and desk aesthetic ideas. It processes curated product specifications, generates vertical 3:4 lifestyle photography, writes helpful SEO-optimized titles and descriptions, and publishes pins to designated Pinterest boards. Every pin directs users to a compliant, responsive landing page featuring product information, clear affiliate disclosure badges, and privacy policy links.

---

### Question 2: How does your application ensure compliance with Pinterest Developer Terms & Spam Policies?
> **Answer**:
> We adhere strictly to Pinterest Developer Terms:
> 1. Rate Limiting: Requests are strictly throttled (1 pin per batch run) to avoid high frequency posting.
> 2. Original & Relevant Content: Every pin features customized vertical photography and bespoke titles/descriptions tailored to specific home decor aesthetics.
> 3. Transparent Links: All destination URLs point exclusively to our verified GitHub Pages domain (`adityasnalawade742-design.github.io`), which hosts compliant landing pages with explicit FTC affiliate disclaimers.
> 4. No Redirect Chains: Links load directly without intermediate cloaking or deceptive redirects.

---

### Question 3: Provide the URL to your Privacy Policy and Terms of Service.
> **Answer**:
> - **Privacy Policy URL**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
> - **Website Domain**: `https://adityasnalawade742-design.github.io`

---

### Question 4: Video Demo URL
> **Answer**:
> Insert your recorded Loom / YouTube video link here.

---

## 🚀 Checklist Before Clicking Submit

- [ ] New Access Token with `pins:write` scope saved to `.env`.
- [ ] Test Pin successfully executed with `Status 201 Created`.
- [ ] Video link recorded (60–90s) and permissions set to "Anyone with the link can view".
- [ ] Application form filled out in Developer Portal.
