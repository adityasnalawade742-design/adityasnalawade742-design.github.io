# 🎥 Pinterest API Standard Access Approval & n8n Automation Guide

> [!IMPORTANT]
> Pinterest requires a **1 to 2 minute Loom / Screen Recording video demo** demonstrating a functional, compliant workflow to approve your **Standard Access API (v5)** application.

---

## ⚡ 1. The n8n Solution Overview

Yes! **n8n is the ideal tool** for this video demo. Pinterest reviewers love visual workflow builders (like n8n or Make) because they can clearly see every node:
1. **Input Data**: Amazon product URL / ASIN.
2. **AI Image & SEO Copy Engine**: Generating vertical lifestyle photos & Pinterest titles.
3. **Bridge Page Generator**: Deploying the mobile landing page link.
4. **Pinterest API v5 HTTP Node**: Firing `POST https://api.pinterest.com/v5/pins` with `Authorization: Bearer <TOKEN>`.

---

## 📂 2. Included Files in Your Repository

We have created two ready-to-use n8n integration files in your project directory:

1. **[n8n_pinterest_affiliate_workflow.json](file:///G:/CLI/pinterest-auto-affiliate/n8n_pinterest_affiliate_workflow.json)**
   - Import directly into n8n (Cloud, Desktop, or Docker).
   - Visual nodes: Webhook Trigger → Product Extractor → FLUX AI Generator → Pinterest SEO Writer → Pinterest API v5 HTTP POST Node.

2. **[n8n_local_bridge.py](file:///G:/CLI/pinterest-auto-affiliate/n8n_local_bridge.py)**
   - CLI script allowing n8n's **Execute Command Node** to trigger our Python engine (Playwright typography + bridge page deployment) with a single command:
     ```powershell
     python G:\CLI\pinterest-auto-affiliate\n8n_local_bridge.py --asin B0FXLYXM32
     ```

---

## 🎬 3. Video Demo Script for Pinterest Reviewers (Step-by-Step)

Record a **60–90 second screen video** using Loom, OBS, or Windows Game Bar (`Win + Alt + R`).

### ⏱️ Timeline & Action Checklist:

#### **[0:00 - 0:15] Pinterest Developer Portal**
- **Action**: Open [developers.pinterest.com](https://developers.pinterest.com/apps/) and display your **App Overview & App ID**.
- **Voiceover / Caption**: *"Hi Pinterest API Review team! This is a demo of our automated Pinterest affiliate & room decor content system using Pinterest v5 API for creating pins."*

#### **[0:15 - 0:45] The n8n Workflow Execution**
- **Action**: Open n8n. Click on the **Pinterest API Node** (`POST https://api.pinterest.com/v5/pins`) to show headers and payload formatting.
- **Action**: Click **Execute Node** or trigger the workflow.
- **Voiceover / Caption**: *"Our workflow extracts product metadata, generates photorealistic cozy room lifestyle visuals, creates mobile landing pages, and formats the Pin payload according to Pinterest Guidelines."*

#### **[0:45 - 1:10] API Response 201 Created**
- **Action**: Zoom in on the n8n response window showing `Status: 201` and the returned `id` (e.g. `"id": "109823485723948"`).
- **Voiceover / Caption**: *"As you can see, Pinterest v5 API returns a 201 Created response with the new Pin ID."*

#### **[1:10 - 1:30] Live Verification on Pinterest & Bridge Page**
- **Action**: Open Pinterest in your browser and refresh your Pinterest Board (`Cozy Room Decor`).
- **Action**: Click the newly created Pin. Show the high-res graphic, SEO title, description, and destination link.
- **Action**: Click the link to prove it opens your clean, mobile-optimized landing page (`adityasnalawade742-design.github.io`).
- **Voiceover / Caption**: *"The pin is now live on our board, linking seamlessly to our mobile landing page. Thank you for reviewing our application!"*

---

## 🚀 4. Quick How-To: Import n8n Workflow

1. Open **n8n** (Cloud or Local).
2. Click **Workflows** → **Import from File**.
3. Select `G:\CLI\pinterest-auto-affiliate\n8n_pinterest_affiliate_workflow.json`.
4. Double click the **Publish to Pinterest API v5** node and set your **Bearer Token** and **Board ID**.
5. Test execute the node and record your video!
