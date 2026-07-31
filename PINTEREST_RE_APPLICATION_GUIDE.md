# 📌 Pinterest API Standard Access Re-Submission Guide (n8n Workflow)

---

## 🎯 Executive Summary of Resolved Rejection Points

Pinterest reviewer Nana listed **4 specific reasons** for the initial rejection of App ID `1594896`:

1. **Company & App Name Mismatch**: Now 100% matched across [index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html), [privacy-policy.html](file:///G:/CLI/pinterest-auto-affiliate/privacy-policy.html), and all landing pages (`Cozy Room Finds` — Developer of `Cozy Room Decor Auto Publisher`, App ID: `1594896`).
2. **Missing Contact Email**: Added explicit developer email (`adityasnalawade742@gmail.com`) to Privacy Policy and site footers.
3. **Missing OAuth Connection Flow in Video**: Resolved by recording the live **n8n Pinterest OAuth Credential Connect / Auth Authorization** screen in n8n.
4. **Complete Authentication & 201 Created Response in Video**: Resolved by demonstrating the full n8n OAuth authorization flow through to the live `201 Created` API response.

---

## 🎬 Step-by-Step n8n Screen Recording Script (60–90 Seconds)

Record your desktop screen using **Loom** or **OBS Studio**. Set Loom permissions to **"Anyone with the link can view"**.

### ⏱️ Minute-by-Minute n8n Recording Workflow:

#### **1. [0:00 – 0:15] Developer Portal Verification**
- **Screen**: Open browser tab at `developers.pinterest.com/apps/1594896`.
- **Action**: Hover cursor over **App Name**: `Cozy Room Decor Auto Publisher` and **App ID**: `1594896`.
- **Script**:
  > *"Hello Pinterest API Review Team. This is a demonstration of our n8n automation workflow for our app Cozy Room Decor Auto Publisher, App ID 1594896, developed by Cozy Room Finds."*

#### **2. [0:15 – 0:35] n8n OAuth 2.0 Account Connection Flow**
- **Screen**: Switch to **n8n Desktop / Cloud**. Open your imported workflow (`n8n_pinterest_affiliate_workflow.json`).
- **Action**: Double-click Node 5 (**Publish to Pinterest API v5**) or open Credentials → **Pinterest OAuth2 API**.
- **Action**: Click **Connect Account** / **OAuth Authorization**.
- **Result**: The browser opens `https://www.pinterest.com/oauth/` showing permissions requested (`boards:read`, `boards:write`, `pins:read`, `pins:write`). Click **Allow**. n8n displays *"Connection Successful"*.
- **Script**:
  > *"Here in n8n, we trigger the official Pinterest OAuth 2.0 connection. Clicking authorize prompts the user permission screen for boards and pins scopes, returning a valid OAuth token to n8n."*

#### **3. [0:35 – 0:55] Execute Node & Verify `201 Created` Response**
- **Screen**: In n8n, click **Execute Node** on Node 5 (**Publish to Pinterest API v5**).
- **Result**: Zoom into the output panel on the right side of n8n showing:
  - `Status Code: 201 Created`
  - `"id": "1092545..."`
  - `"board_id": "1092545259543920271"`
- **Script**:
  > *"Executing the node sends the JSON payload containing the vertical graphic, title, description, and link directly to POST https://api.pinterest.com/v5/pins. The Pinterest API returns a successful 201 Created response with the new Pin ID."*

#### **4. [0:55 – 1:25] Live Pin & Landing Page Verification**
- **Screen**: Open Pinterest, navigate to profile `@adityasnalawade0703`, and refresh board **Cozy Room & Desk Decor**.
- **Action**: Click the newly generated Pin.
- **Action**: Click the outbound destination link on the Pin (`https://adityasnalawade742-design.github.io/bridge_B0FXLYXM32.html`).
- **Result**: Show that the destination page loads instantly, displaying FTC affiliate disclaimers, privacy policy link, and contact email (`adityasnalawade742@gmail.com`).
- **Script**:
  > *"The pin is live on Pinterest. Clicking the pin leads directly to our mobile-optimized landing page featuring product details, FTC affiliate disclaimers, privacy policy, and developer contact information. Thank you for reviewing our application!"*

---

## 📝 Copy-Paste Answers for Pinterest Developer Portal Re-Submission

When re-submitting in the **Pinterest Developer Portal**, paste these exact policy-compliant answers:

### Question 1: Describe the primary use case of your application.
> **Answer**:
> Our application, "Cozy Room Decor Auto Publisher" (App ID: 1594896), developed by "Cozy Room Finds", integrates with n8n workflows to automate the curation and distribution of high-quality home decor and desk aesthetic ideas. It processes product specifications, generates vertical 3:4 lifestyle visuals, creates helpful SEO titles and descriptions, and publishes pins to designated Pinterest boards via the official Pinterest API v5 (`POST /v5/pins`). Every pin directs users to a compliant, responsive landing page featuring product information, clear affiliate disclosure badges, and privacy policy links.

### Question 2: How does your application ensure compliance with Pinterest Developer Terms & Spam Policies?
> **Answer**:
> We adhere strictly to Pinterest Developer Terms:
> 1. Official OAuth 2.0 Authentication: All requests use official OAuth 2.0 user authorization in n8n with explicit scopes (`boards:read`, `boards:write`, `pins:read`, `pins:write`).
> 2. Rate Limiting: Workflows are strictly throttled (1 pin per scheduled run) to avoid high-frequency posting.
> 3. Original & High-Quality Content: Every pin features customized vertical photography and bespoke titles/descriptions tailored to specific home decor aesthetics.
> 4. Transparent Links: All destination URLs point exclusively to our verified domain (`adityasnalawade742-design.github.io`), which hosts compliant landing pages with explicit FTC affiliate disclaimers and privacy policy links containing direct developer email contact (adityasnalawade742@gmail.com).

### Question 3: Provide the URL to your Privacy Policy and Contact Information.
> **Answer**:
> - **Privacy Policy URL**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
> - **Website Domain**: `https://adityasnalawade742-design.github.io`
> - **Contact Email**: `adityasnalawade742@gmail.com`
> - **Company Name**: Cozy Room Finds
> - **App Name**: Cozy Room Decor Auto Publisher (App ID: 1594896)

---

## 🚀 Re-Submission Checklist

- [x] Website & Privacy Policy updated with matching Company (`Cozy Room Finds`), App (`Cozy Room Decor Auto Publisher`), and App ID (`1594896`).
- [x] Developer contact email (`adityasnalawade742@gmail.com`) included on Privacy Policy and website footers.
- [x] `n8n_pinterest_affiliate_workflow.json` node 5 configured for Pinterest API v5 POST endpoint.
- [ ] Record 60–90s Loom video in n8n following the script above.
- [ ] Set Loom video permissions to "Anyone with the link can view".
- [ ] Re-submit application in Pinterest Developer Portal.
