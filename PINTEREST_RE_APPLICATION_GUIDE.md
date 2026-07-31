# 📌 Pinterest API Standard Access Master Demo Video Guide (10/10 Score Blueprint)

---

## 🎯 Executive Summary of Rejection Resolutions

Pinterest reviewer Nana listed **4 specific reasons** for the initial rejection of App ID `1594896`:

1. **Company & App Name Mismatch**: Now 100% matched across [index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html), [privacy-policy.html](file:///G:/CLI/pinterest-auto-affiliate/privacy-policy.html), [terms-of-service.html](file:///G:/CLI/pinterest-auto-affiliate/terms-of-service.html), and all landing pages (`Cozy Room Finds` — Developer of `Cozy Room Decor Publisher Pro`).
2. **Missing Contact Email**: Added high-visibility email badge box displaying **`aditya.s.nalawade742@gmail.com`** (100% matched with Pinterest Business Account `@adityasnalawade0703`).
3. **Missing OAuth Connection Flow in Video**: Resolved by expanding the OAuth 2.0 demonstration to **60+ seconds**, showing full uncropped browser URLs and permission grants.
4. **Complete Authentication & Live Pin Flow in Video**: Resolved by showing the full unedited sequence: **Connect Pinterest ➔ Address Bar OAuth ➔ Permission Hold (8-10s) ➔ Browser Redirect ➔ Connected Account Verification ➔ Live Publish Transition ➔ Live Board Refresh ➔ Destination Page Audit**.

---

## 🎬 10/10 Demo Video Script & Screen Recording Blueprint

Record your desktop screen using **Loom** or **OBS Studio**. Set Loom permissions to **"Anyone with the link can view"**. Do not crop the browser address bar!

---

### ⏱️ Minute-by-Minute Recording Workflow:

#### **Part 1 — Introduce the App [0:00 – 0:20]**
- **Screen**: Pinterest Developer Dashboard (`developers.pinterest.com/apps/`).
- **Action**: Hover cursor over **App Name** (`Cozy Room Decor Publisher Pro`), **Company Name** (`Cozy Room Finds`), and **Standard Access Request**.
- **🎙️ Script**:
  > *"Hello Pinterest Review Team. My name is Aditya. This is my application, Cozy Room Decor Publisher Pro, developed by Cozy Room Finds. This application helps users publish product Pins to Pinterest using Pinterest's official API after authenticating with their Pinterest account."*

---

#### **Part 2 — Show Your Website & Legal Compliance [0:20 – 0:40]**
- **Screen**: Open homepage ([https://adityasnalawade742-design.github.io/index.html](file:///G:/CLI/pinterest-auto-affiliate/index.html)).
- **Action**: Scroll slowly down the page. Point out:
  - Company Name (`Cozy Room Finds`)
  - App Name (`Cozy Room Decor Publisher Pro`)
  - Privacy Policy Link
  - Terms of Service Link
  - High-visibility Contact Email (`aditya.s.nalawade742@gmail.com`)
- **🎙️ Script**:
  > *"This is the official website for the application. It includes our company information, privacy policy, terms of service, and contact email."*

---

#### **Part 3 — Complete OAuth 2.0 Authentication Flow [0:40 – 1:35]**
- **Screen**: Open application dashboard (n8n or Web Console). Start **NOT logged in**.
- **Action 1**: Click **Connect Pinterest**.
- **Action 2**: The browser opens `https://www.pinterest.com/oauth/`. **Ensure the full browser address bar is clearly visible**.
- **Action 3**: **Hold on the permissions page for 8 to 10 seconds**. Move your mouse slowly over the requested scopes:
  - **Boards** (`boards:read`, `boards:write`)
  - **Pins** (`pins:read`, `pins:write`)
- **Action 4**: Click **Allow**.
- **Action 5**: **Show the live browser redirect** (`Redirecting...` ➔ `http://localhost:5000/api/auth/callback` or n8n OAuth return screen).
- **Action 6**: Show the app updating to **"Connected Successfully"** / **"Pinterest Account Connected"**.
- **🎙️ Script**:
  > *"Here we demonstrate our account connection process. When the user clicks Connect Pinterest, they are redirected to Pinterest's official authorization page at pinterest.com/oauth. The user clearly sees the requested permissions for boards and pins, and clicks Allow. The browser completes the redirect, and the app confirms that the account is connected successfully. The application only publishes Pins after the user explicitly authorizes access through Pinterest's official OAuth flow."*

---

#### **Part 4 — Show Connected Account [1:35 – 1:45]**
- **Screen**: App dashboard.
- **Action**: Hover cursor over the connected account status. **Leave visible for 3 to 5 seconds**:
  - `Connected Account: @adityasnalawade0703`
- **🎙️ Script**:
  > *"As you can see, our account adityasnalawade0703 is now securely connected."*

---

#### **Part 5 — Publish a Pin (Show Live Transition) [1:45 – 2:25]**
- **Screen**: Application workflow canvas / dashboard.
- **Action 1**: Click **Publish Pin** or **Run Workflow**.
- **Action 2**: Show the live status transition:
  - `Publishing...` ➔ `Success`
- **Action 3**: Display the confirmation message and Pin ID.
- **🎙️ Script**:
  > *"Now we can trigger the publishing process. As shown, the status changes from Publishing to Success, confirming the Pin has been sent to our connected Pinterest account."*

---

#### **Part 6 — Refresh & Verify on Pinterest [2:25 – 2:55]**
- **Screen**: Go to Pinterest profile `@adityasnalawade0703` on board **Cozy Room & Desk Decor**.
- **Action 1**: **Click Refresh in the browser on camera**.
- **Action 2**: Wait 2 seconds until the new Pin appears live.
- **Action 3**: Click open the newly created Pin. Point out:
  - **Title**
  - **Description**
  - **Destination Link**
- **🎙️ Script**:
  > *"Switching to Pinterest and refreshing our board on camera, we can see the newly published Pin appear immediately. Opening the Pin shows our visual, clean title, description, and destination link."*

---

#### **Part 7 — Open Destination Landing Page [2:55 – 3:25]**
- **Screen**: Click the destination link on the Pin.
- **Action**: The destination website opens ([`bridge_B0FXLYXM32.html`](file:///G:/CLI/pinterest-auto-affiliate/bridge_B0FXLYXM32.html)).
- **Action**: Scroll down slowly. Point out:
  - Company Name (`Cozy Room Finds`)
  - App Name (`Cozy Room Decor Publisher Pro`)
  - Privacy Policy & Terms Links
  - Contact Email (`aditya.s.nalawade742@gmail.com`)
  - Amazon Associate FTC Affiliate Disclosure
- **🎙️ Script**:
  > *"Clicking the Pin takes the user directly to our compliant landing page. Here you can see our company name, app name, privacy policy, contact email, and Amazon Associate affiliate disclosures."*

---

#### **Finish & Closing [3:25]**
- **🎙️ Script**:
  > *"Thank you for reviewing our application. This application uses Pinterest's official OAuth flow, requires explicit user authorization before publishing, and is intended for managing and publishing Pins for our own Pinterest account. We appreciate your time and consideration."*

---

## 📝 Copy-Paste Form Answers for Developer Portal Re-Submission

### Question 1: Describe the primary use case of your application.
> **Answer**:
> Our application, "Cozy Room Decor Publisher Pro", developed by "Cozy Room Finds", automates the curation and distribution of high-quality home decor and desk aesthetic ideas. It processes product specifications, generates vertical 3:4 lifestyle visuals, creates helpful SEO titles and descriptions, and publishes pins to designated Pinterest boards via the official Pinterest API v5 (`POST /v5/pins`). Every pin directs users to a compliant, responsive landing page featuring product information, clear affiliate disclosure badges, and privacy policy links.

### Question 2: How does your application ensure compliance with Pinterest Developer Terms & Spam Policies?
> **Answer**:
> We adhere strictly to Pinterest Developer Terms:
> 1. Official OAuth 2.0 Authentication: All requests use official OAuth 2.0 user authorization where the user explicitly grants board and pin permissions (`boards:read`, `boards:write`, `pins:read`, `pins:write`).
> 2. Explicit User Consent: Pins are published only after an account has been authorized by the user through Pinterest's official OAuth authorization endpoint.
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
