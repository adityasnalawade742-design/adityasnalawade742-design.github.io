# 📌 Pinterest API Standard Access Demo Video Guide & Action Plan

---

## 🎯 Executive Summary of Resolved Rejection Points

Pinterest reviewer Nana listed **4 specific reasons** for the initial rejection of App ID `1594896`:

1. **Company & App Name Mismatch**: Now 100% matched across [index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html), [privacy-policy.html](file:///G:/CLI/pinterest-auto-affiliate/privacy-policy.html), [terms-of-service.html](file:///G:/CLI/pinterest-auto-affiliate/terms-of-service.html), and all landing pages (`Cozy Room Finds` — Developer of `Cozy Room Decor Publisher Pro`).
2. **Missing Contact Email**: Added explicit developer email (`aditya.s.nalawade742@gmail.com`) to Privacy Policy, Terms of Service, and site footers in a high-visibility gold badge box.
3. **Missing OAuth Connection Flow in Video**: Resolved by expanding the OAuth 2.0 demonstration to **45–60 seconds**, showing explicit user authorization.
4. **Complete Authentication Flow in Video**: Resolved by showing the full sequence: **Connect Pinterest ➔ OAuth Authorization ➔ Connected Successfully ➔ Publish Pin ➔ Live Pin & Destination Verification**.

---

## 🎬 Master 3-Minute Demo Video Script (UX & Compliance Focused)

Record your desktop screen using **Loom** or **OBS Studio**. Set Loom permissions to **"Anyone with the link can view"**.

> **💡 Key Guideline**: Focus on **User Experience and Policy Compliance**. Avoid technical jargon like "201 Created", "POST /v5/pins", or "JSON payloads". Show clearly that the user explicitly authorizes access before any Pin is published.

---

### ⏱️ Minute-by-Minute Recording Workflow:

#### **Part 1 — Introduce the App [0:00 – 0:20]**
- **Screen**: Open Pinterest Developer Dashboard (`developers.pinterest.com/apps/`).
- **Action**: Hover cursor over **App Name** (`Cozy Room Decor Publisher Pro`), **Company Name** (`Cozy Room Finds`), and **Standard Access Request**.
- **🎙️ Script**:
  > *"Hello Pinterest Review Team. My name is Aditya. This is my application, Cozy Room Decor Publisher Pro, developed by Cozy Room Finds. This application helps users publish product Pins to Pinterest using Pinterest's official API after authenticating with their Pinterest account."*

---

#### **Part 2 — Show Your Website [0:20 – 0:40]**
- **Screen**: Open homepage ([https://adityasnalawade742-design.github.io/index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html)).
- **Action**: Scroll slowly down the page. Point out:
  - Company Name (`Cozy Room Finds`)
  - App Name (`Cozy Room Decor Publisher Pro`)
  - Privacy Policy Link
  - Terms of Service Link
  - Contact Email (`aditya.s.nalawade742@gmail.com`)
- **🎙️ Script**:
  > *"This is the official website for the application. It includes our company information, privacy policy, terms of service, and contact email."*

---

#### **Part 3 — OAuth Authentication (MOST IMPORTANT PART) [0:40 – 1:30]**
- **Screen**: Open your application (n8n or Web Console dashboard).
- **Action**: Ensure you are **NOT** already logged in.
- **Action**: Click **Connect Pinterest**.
- **Action**: Browser opens `https://www.pinterest.com/oauth/`.
- **Action**: **Pause for 5 seconds** on the permissions page. Let the reviewer clearly see the requested permissions:
  - **Boards** (`boards:read`, `boards:write`)
  - **Pins** (`pins:read`, `pins:write`)
- **Action**: Click **Allow**.
- **Action**: Show the app screen updating to **"Connected Successfully"** or **"Pinterest Account Connected"**.
- **🎙️ Script**:
  > *"Here we demonstrate our account connection process. When the user clicks Connect Pinterest, they are redirected to Pinterest's official authorization page. The user clearly sees the requested permissions for boards and pins, and clicks Allow. The app then confirms that the account is connected successfully."*

---

#### **Part 4 — Show Connected Account [1:30 – 1:40]**
- **Screen**: Zoom in / highlight the connected account status in the app.
- **Action**: Point mouse cursor to **Connected Account: @adityasnalawade0703**.
- **🎙️ Script**:
  > *"As you can see, our account adityasnalawade0703 is now securely connected."*

---

#### **Part 5 — Publish a Pin [1:40 – 2:20]**
- **Screen**: Application workflow canvas / dashboard.
- **Action**: Click **Publish Pin** or **Run Workflow**.
- **Action**: Show status indicator changing to **Creating Pin...** then **Success**.
- **Action**: Briefly display the confirmation message and Pin ID.
- **🎙️ Script**:
  > *"Now we can trigger the publishing process. The app formats our visual content and publishes the Pin to our connected Pinterest board. The process is complete and returns a success confirmation."*

---

#### **Part 6 — Verify on Pinterest [2:20 – 2:50]**
- **Screen**: Go to Pinterest profile `@adityasnalawade0703` on board **Cozy Room & Desk Decor**.
- **Action**: Refresh the board.
- **Action**: Click open the newly created Pin.
- **Action**: Point out:
  - **Title**
  - **Description**
  - **Destination URL**
- **🎙️ Script**:
  > *"Switching to Pinterest and refreshing our board, we can see the newly published Pin. Clicking into the Pin shows our high-quality visual, clean title, helpful description, and direct destination link."*

---

#### **Part 7 — Open the Landing Page [2:50 – 3:20]**
- **Screen**: Click the destination link on the Pin.
- **Action**: The destination landing page opens ([`bridge_B0FXLYXM32.html`](file:///G:/CLI/pinterest-auto-affiliate/bridge_B0FXLYXM32.html)).
- **Action**: Scroll down slowly. Point out:
  - Company Name (`Cozy Room Finds`)
  - App Name (`Cozy Room Decor Publisher Pro`)
  - Privacy Policy & Terms Links
  - Developer Email (`aditya.s.nalawade742@gmail.com`)
  - Amazon Associate FTC Affiliate Disclosure
- **🎙️ Script**:
  > *"Clicking the Pin takes the user directly to our compliant landing page. Here you can see our company name, app name, privacy policy, contact email, and Amazon Associate affiliate disclosures."*

---

#### **Finish [3:20]**
- **🎙️ Script**:
  > *"Thank you for reviewing my application. This app uses Pinterest's official OAuth flow, publishes Pins only after explicit user authorization, and complies with Pinterest's Developer Policies. Thank you for your time."*

---

## 📝 Copy-Paste Form Answers for Developer Portal Re-Submission

### Question 1: Describe the primary use case of your application.
> **Answer**:
> Our application, "Cozy Room Decor Publisher Pro", developed by "Cozy Room Finds", automates the curation and distribution of high-quality home decor and desk aesthetic ideas. It processes product specifications, generates vertical 3:4 lifestyle visuals, creates helpful SEO titles and descriptions, and publishes pins to designated Pinterest boards via the official Pinterest API v5 (`POST /v5/pins`). Every pin directs users to a compliant, responsive landing page featuring product information, clear affiliate disclosure badges, and privacy policy links.

### Question 2: How does your application ensure compliance with Pinterest Developer Terms & Spam Policies?
> **Answer**:
> We adhere strictly to Pinterest Developer Terms:
> 1. Official OAuth 2.0 Authentication: All requests use official OAuth 2.0 user authorization where the user explicitly grants board and pin permissions (`boards:read`, `boards:write`, `pins:read`, `pins:write`).
> 2. Explicit User Consent: Pins are published only after an account has been authorized by the user.
> 3. Rate Limiting: Workflows are strictly throttled (1 pin per scheduled run) to avoid high-frequency posting.
> 4. Original & High-Quality Content: Every pin features customized vertical photography and bespoke titles/descriptions tailored to specific home decor aesthetics.
> 5. Transparent Links: All destination URLs point exclusively to our verified domain (`adityasnalawade742-design.github.io`), which hosts compliant landing pages with explicit FTC affiliate disclaimers and privacy policy links containing direct developer email contact (aditya.s.nalawade742@gmail.com).

### Question 3: Provide the URL to your Privacy Policy and Contact Information.
> **Answer**:
> - **Privacy Policy URL**: `https://adityasnalawade742-design.github.io/privacy-policy.html`
> - **Terms of Service URL**: `https://adityasnalawade742-design.github.io/terms-of-service.html`
> - **Website Domain**: `https://adityasnalawade742-design.github.io`
> - **Contact Email**: `aditya.s.nalawade742@gmail.com`
> - **Company Name**: Cozy Room Finds
> - **App Name**: Cozy Room Decor Publisher Pro
