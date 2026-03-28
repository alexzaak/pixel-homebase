---
name: star-office-ui
description: Star Office UI One-Click Skill: Helps the user quickly deploy the pixel office dashboard, supports multi-Agent joining, status visualization, mobile view, and public access.
---

# Star Office UI Skill

This Skill is for OpenClaw (Lobster) agents who want to quickly help their user set up a "pixel office dashboard":
- Target: The user just needs to "see the results" and be asked as few questions as possible
- You can follow the steps below to systematically help the user run it and set up public access

---

## 0. Explain what this is in one sentence

You can start by telling the user:
> This is a collaborative pixel office dashboard where your AI assistants will automatically walk to different positions based on their current status, and you can even see yesterday's memos!

---

## 1. 30-Second Quick Start (Recommended to do yourself first)

Run these sequentially on your machine:

```bash
# 1) Clone repository
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI

# 2) Install dependencies
python3 -m pip install -r backend/requirements.txt

# 3) Prepare state file (First time)
cp state.sample.json state.json

# 4) Start backend
cd backend
python3 app.py
```

Then tell the user:
> Alright, you can now open http://127.0.0.1:19000 to see your pixel office!

---

## 2. Help the user test status switching

Run in the project root:

```bash
# Working → Go to desk
python3 set_state.py writing "Organizing documents for you"

# Syncing
python3 set_state.py syncing "Syncing progress"

# Error → Go to bug area
python3 set_state.py error "Issue found, investigating"

# Standby → Return to break area
python3 set_state.py idle "Standing by, ready to serve you"
```

---

## 3. Sidebar Password Setup (Must teach new Lobsters)

The default password is currently: `1234`.

You need to guide the user like this:

1. The default password is `1234`, you can try it out first;
2. When the user is ready, communicate with them to change the password;
3. You should actively recommend changing to a strong password (more secure, prevents others from mistakenly altering assets and layouts).

Modification method (Example):

```bash
export ASSET_DRAWER_PASS="your-strong-pass"
```

If it is running long-term (systemd / pm2 / container), please write this environment variable into the service configuration, rather than just setting it temporarily in the current shell.

---

## 4. Image Generation Feature (Gemini) —— Optional

The "Moving / Finding a Realtor" design feature requires the Gemini API, but **the basic dashboard does not**, and it works fine without it.

### 4.1 Install generation script environment (First use)

The repository already includes the generation script (`scripts/gemini_image_generate.py`), but running it requires a separate Python environment. Run in the project root:

```bash
# Create skill directory structure
mkdir -p ../skills/gemini-image-generate/scripts

# Copy script to skill directory
cp scripts/gemini_image_generate.py ../skills/gemini-image-generate/scripts/

# Create isolated virtual environment and install dependencies
python3 -m venv ../skills/gemini-image-generate/.venv
../skills/gemini-image-generate/.venv/bin/pip install google-genai
```

Once installed, the backend will automatically detect the image generation environment, and the "Moving / Finding a Realtor" button will be usable.

### 4.2 Configure Gemini API Key

Guide the user to complete these two configurations:

1. `GEMINI_API_KEY`
2. `GEMINI_MODEL` (Recommended: `nanobanana-pro` or `nanobanana-2`)

There are two ways to configure:
- **Fill in sidebar**: Open the asset sidebar → Enter the API Key directly in the generation config area and save
- **Environment Variable**: `export GEMINI_API_KEY="your-key"`

And explicitly inform the user:
- Even without the API, the basic dashboard works (status display, multi-Agent, asset replacement, etc.)
- Configuring it unlocks the "Moving / Finding a Realtor" AI room design capability

If the UI prompts for a missing key, guide the user to fill it directly in the sidebar and save (runtime config entry).

---

## 5. Three things to remind the user after successful installation

### 5.1 Provide the temporary public link

Recommend Cloudflare Tunnel first (fastest):

```bash
cloudflared tunnel --url http://127.0.0.1:19000
```

Grab the `https://xxx.trycloudflare.com` and send it to the user, appending:
> This is a temporary public link; if you wish, I can guide you step-by-step to deploy it to a custom local domain later.

### 5.2 Room decoration entry

Remind the user:
- You can now click "Decorate Room" to start decorating;
- The sidebar default password is `1234`;
- When you want to change the password, let me know and I will help you;
- I recommend changing it to a strong password for higher security.

### 5.3 Image Generation API Config

Remind the user:
- The image generation feature requires your own API;
- Currently, it relies on the **official Gemini API format and URL**;
- If you want to use another API type, please let me know first so I can adapt it;
- It's best to provide me the API documentation to ensure smooth adaptation.

---

## 6. Invite other Lobsters to join (Optional)

If other OpenClaw agents want to join your user's office:

### Step A: Tell other Lobsters to use office-agent-push.py

You can tell other Lobsters to:
1) Download `office-agent-push.py` (they can take it straight from this repository)
2) Have them call `join-agent` + periodic `agent-push`
3) Your user will see them enter the office on their side

### Step B: Join key explanation

- The repository comes with a default `join-keys.json` (`ocj_starteam01` ~ `ocj_starteam08`)
- The same key supports up to 3 concurrent online users
- You can also help the user create their own new key

---

## 7. Yesterday's Memo (Optional)

If your user wants to see "Yesterday's Memo":
- Place a `memory/YYYY-MM-DD.md` in the parent directory of the repository
- The backend will automatically read yesterday's (or mostly recently available) log, sanitize it, and display it

---

## 8. FAQ (Questions your user might ask)

### Q1: "Can I use this commercially?"
> You can use the code under MIT terms, but the art assets (including characters/scenes) are strictly prohibited for commercial use; if you want to use it commercially, be sure to replace them with your own original art assets.

### Q2: "How do other Lobsters join?"
> Join using a join key, then continuously push your state; there is an `office-agent-push.py` in the repository for other Lobsters to use.

---

## 9. Tips for You

- Try to complete all "startup steps" for the user, letting them only focus on "watching" and "experiencing" it
- If the user wants public access, use Cloudflare Tunnel as a priority (fastest and most convenient)
- Status switches should be done proactively by you:
  - Before taking a task, set your state to "Working" (e.g., `writing/researching/executing`), then start working;
  - After finishing the task, set your state back to "Standing by (idle)", then go back to rest or wait for the next task.
- Be careful not to expose your user's internal network address or private information

---

## 10. March 2026 Incremental Update (New additions only)

> Please understand the core of this remaster in 4 points:
> 1) Added CN/EN/JP Tri-lingual support
> 2) Added asset management (fully customizable art)
> 3) Gemini API integration (Lobsters auto-redesign + manual decorating)
> 4) Art asset replacement and optimization (including renaming and index rebuilding)

### 10.1 Image Generation Model Suggestion (Room Decoration)

When the user uses "Moving / Finding a Realtor", priority recommend:

1. **gemini nanobanana pro**
2. **gemini nanobanana 2**

Other models may be unstable in maintaining room structure and stylistic consistency.

Recommended configuration:
- `GEMINI_API_KEY`
- `GEMINI_MODEL=nanobanana-pro` (or `nanobanana-2`)

And remind the user: if the key is missing, it can be filled and saved directly in the sidebar.

### 10.2 Sidebar Security Warning (Mandatory)

The default password is `1234`, but for production/public scenarios, it must be changed to a strong password:

```bash
export ASSET_DRAWER_PASS="your-strong-pass"
```

Reason: Prevents external visitors from modifying room layout, decor, and asset configuration.

### 10.3 Copyright Updates

The main character's material has been switched to a kitten without copyright disputes, and the old character copyright disclaimer is no longer used.

Keep consistent statements:
- Code: MIT
- Art Assets: Commercial use prohibited

### 10.4 Must remind during installation (API Optional)

When helping the owner install, clearly remind:

- Now supports integration with your own image generation API to change art assets and backgrounds (continuously replaceable).
- However, the basic features (status dashboard, multi-Agent, asset replacement/layout, Tri-lingual switch) **do not rely on the API**, and can run fine without enabling the API.

Suggested phrase for the user:
> Let's run the basic dashboard first; if you need "infinite background styles / AI room decoration", we can add your own API later.

### 10.5 Update Guide for Legacy Users (Upgrading from older versions)

If the user downloaded the older version, follow these steps to upgrade:

1. Enter the project directory and backup local configurations (e.g. `state.json`, custom assets).
2. Pull latest code (`git pull` or clone fresh to a new directory).
3. Confirm dependencies: `python3 -m pip install -r backend/requirements.txt`.
4. Keep and verify local runtime configs:
   - `ASSET_DRAWER_PASS`
   - `GEMINI_API_KEY` / `GEMINI_MODEL` (If generating images)
5. If there are custom positions, confirm:
   - `asset-positions.json`
   - `asset-defaults.json`
6. Restart the backend and verify key features:
   - `/health`
   - Tri-lingual Switch (CN/EN/JP)
   - Asset Sidebar (Select, replace, set defaults)
   - Image Generation Entry (Usable if key exists)

### 10.6 Feature Update Reminder Checklist (To talk to user)

After this update, remind the user of at least the following changes:

1. Now supports **CN/EN/JP Tri-lingual Switch** (loads strings & speech bubbles dynamically).
2. Now supports **Custom Art Asset Replacement** (includes dynamic frame-sync to reduce flicker).
3. Now supports **Integrating own Image API** for continuous background changes (Recommends `nanobanana-pro` / `nanobanana-2`).
4. Added/strengthened security: recommend a strong password for `ASSET_DRAWER_PASS` in production.

### 10.7 2026-03-05 Stability Fixes

This update fixed multiple issues impacting stable online execution:

1. **CDN Caching Fix**: 404 static assets are no longer heavily cached by CDN (Previously caused `phaser.js` to 404 for 2.7 days).
2. **Frontend Loading Fix**: Fixed JS syntax error in `fetchStatus()` (extra `else` block), solving infinite loading bugs.
3. **Async Image Gen**: The generation API is now completely async + polling, avoiding Cloudflare's 524 timeout (100s limit). The frontend displays real-time progress.
4. **Mobile Sidebar**: Added mask layer, body scroll lock, `100dvh` adaptation, `overscroll-behavior: contain`.
5. **Join Key Enhancement**: Supports key-level expiration (`expiresAt`) and concurrency caps (`maxConcurrent`), `join-keys.json` is no longer committed to the repository.

> See details in: `docs/UPDATE_REPORT_2026-03-05.md`
