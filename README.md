# Star Office UI

🌐 Language: **English** | [中文](./README.zh.md) | [日本語](./README.ja.md)

![Star Office UI Cover](docs/screenshots/readme-cover-2.jpg)

**A pixel-art AI office dashboard** — Visualizes the working status of AI assistants in real-time, letting you intuitively see "who is doing what, what was done yesterday, and whether they are online now".

Supports multi-Agent collaboration, Tri-lingual (CN/EN/JP), AI-generated interior design, and Desktop Pet mode.
Provides the best experience when deeply integrated with [OpenClaw](https://github.com/openclaw/openclaw), but can also be deployed independently as a status dashboard.

> This project was co-created by **[Ring Hyacinth](https://x.com/ring_hyacinth)** and **[Simon Lee](https://x.com/simonxxoo)**, and is continuously maintained and co-built with community developers ([@Zhaohan-Wang](https://github.com/Zhaohan-Wang), [@Jah-yee](https://github.com/Jah-yee), [@liaoandi](https://github.com/liaoandi)).
> We welcome Issues and PRs, and thank every contributor for their support.

---

## ✨ Quick Experience

### Method 1: Let your Lobster deploy it for you (Recommended for OpenClaw users)

If you are using [OpenClaw](https://github.com/openclaw/openclaw), simply send the following sentence to your Lobster:

```text
Please follow this SKILL.md to help me deploy Star Office UI:
https://github.com/ringhyacinth/Star-Office-UI/blob/master/SKILL.md
```

Your Lobster will automatically clone, install dependencies, start the backend, configure status synchronization, and send you the access URL.

### Method 2: 30-Second Manual Deployment

> **Environment Requirements: Python 3.10+** (The code uses the `X | Y` union type syntax, not supported in 3.9 and below)

```bash
# 1) Clone the repository
git clone https://github.com/ringhyacinth/Star-Office-UI.git
cd Star-Office-UI

# 2) Install dependencies (Requires Python 3.10+)
python3 -m pip install -r backend/requirements.txt

# 3) Prepare the state file (First time)
cp state.sample.json state.json

# 4) Start the backend
cd backend
python3 app.py
```

Open **http://127.0.0.1:19000** and try switching states:

```bash
python3 set_state.py writing "Organizing documents"
python3 set_state.py error "Issue found, investigating"
python3 set_state.py idle "Standing by"
```

### Method 3: Container Deployment (Podman / Docker)

For users on Fedora or those preferring containers, you can deploy using Podman (or Docker).

```bash
# 1) Clone the repository
git clone https://github.com/alexzaak/pixel-homebase.git
cd pixel-homebase

# 2) Prepare the state file (First time)
cp state.sample.json state.json

# 3) Start the container
podman compose up -d
# OR with Docker: docker compose up -d
```

Open **http://127.0.0.1:19000** to view your office. The directory is mounted with the `:Z` flag to ensure compatibility with SELinux on Fedora.

![Star Office UI Preview](docs/screenshots/readme-cover-1.jpg)

---

## 🤔 Who is this for?

### Users with OpenClaw / AI Agents
This is the **complete experience**. The Agent automatically switches states while working, and the pixel character in the office will walk to the corresponding area in real-time — you just need to open the web page to see what the AI is currently doing.

### Users without OpenClaw
You can also easily deploy it. You can:
- Manually / use scripts to push status via `set_state.py` or API
- Treat it as a pixel-art personal status page / remote work dashboard
- Integrate any system capable of sending HTTP requests to drive the status

---

## 📋 Features Overview

1. **Status Visualization** — 6 states (`idle` / `writing` / `researching` / `executing` / `syncing` / `error`) automatically map to different areas of the office, displayed in real-time with animations + speech bubbles
2. **Yesterday's Memo** — Automatically reads the recent work log from `memory/*.md`, sanitizes it, and displays it as a "Yesterday's Memo" card
3. **Multi-Agent Collaboration** — Invite other Agents to join your office via a join key to see multi-person status in real-time
4. **Tri-lingual Support** — One-click switch between CN / EN / JP, UI text, speech bubbles, and loading prompts all sync together
5. **Custom Art Assets** — Sidebar to manage characters / scenes / decor assets, supports dynamic frame synchronization to avoid flickering
6. **AI Interior Design** — Integrates Gemini API to change the office background using AI; core features work normally even without the API
7. **Mobile Adaptation** — Can be viewed directly on mobile phones, perfect for a quick glance while outdoors
8. **Security Enhancements** — Sidebar password protection, weak password blocking in production, Session Cookie hardening
9. **Flexible Public Access** — Cloudflare Tunnel recommended for one-click public access, custom domains / reverse proxies also supported
10. **Desktop Pet Mode** — Optional Electron desktop wrapper that turns the office into a transparent desktop pet widget (see details below)

---

## 🚀 Detailed Deployment Guide

### 1) Install Dependencies

```bash
cd Star-Office-UI
python3 -m pip install -r backend/requirements.txt
```

### 2) Initialize State File

```bash
cp state.sample.json state.json
```

### 3) Start Backend

```bash
cd backend
python3 app.py
```

Open `http://127.0.0.1:19000`

> ✅ You can keep default settings for the first deployment; for production environments, please copy `.env.example` to `.env` and set a strong random `FLASK_SECRET_KEY` and `ASSET_DRAWER_PASS` to prevent weak passwords and session leaks.

### 4) Switch States

```bash
python3 set_state.py writing "Organizing documents"
python3 set_state.py syncing "Syncing progress"
python3 set_state.py error "Issue found, investigating"
python3 set_state.py idle "Standing by"
```

### 5) Public Access (Optional)

```bash
cloudflared tunnel --url http://127.0.0.1:19000
```

Take the `https://xxx.trycloudflare.com` link to share it.

### 6) Verify Installation (Optional)

```bash
python3 scripts/smoke_test.py --base-url http://127.0.0.1:19000
```

If all checks return `OK`, the deployment is successful.

---

## 🦞 OpenClaw Deep Integration

> The following content is for [OpenClaw](https://github.com/openclaw/openclaw) users. If you do not use OpenClaw, you can skip this section.

### Automatic Status Synchronization

Add the following rules to your `SOUL.md` (or Agent rule file) so the Agent automatically maintains its status:

```markdown
## Star Office Status Synchronization Rules
- Upon receiving a task: Execute `python3 set_state.py <state> "<description>"` before starting work
- Upon completing a task: Execute `python3 set_state.py idle "Standing by"` before replying
```

**Mapping 6 states → 3 areas:**

| State | Office Area | Trigger Scenario |
|------|-----------|---------|
| `idle` | 🛋 Break Area (Sofa) | Standing by / Task complete |
| `writing` | 💻 Workspace (Desk) | Writing code / Writing docs |
| `researching` | 💻 Workspace | Searching / Researching |
| `executing` | 💻 Workspace | Executing commands / Running tasks |
| `syncing` | 💻 Workspace | Syncing data / Pushing |
| `error` | 🐛 Bug Area | Error / Exception investigation |

### Invite Other Agents to Join the Office

**Step 1: Prepare the join key**

When starting the backend for the first time, if `join-keys.json` does not exist in the current directory, the service will automatically generate a runtime `join-keys.json` based on `join-keys.sample.json` (containing example keys, e.g. `ocj_example_team_01`). You can manually add, modify, or delete keys in the generated `join-keys.json`. Each key supports a maximum of 3 concurrent online users by default.

**Step 2: Have the Guest Agent Run the Push Script**

The guest only needs to download `office-agent-push.py` and fill in 3 variables:

```python
JOIN_KEY = "ocj_starteam02"          # Your assigned key
AGENT_NAME = "Little Ming's Lobster" # Display name
OFFICE_URL = "https://office.hyacinth.im"  # Your office URL
```

```bash
python3 office-agent-push.py
```

The script will automatically join the office and push the state every 15 seconds. The guest will appear on the dashboard and automatically walk to the corresponding area based on their state.

**Step 3 (Optional): Guest Installs Skill**

The guest can also use `frontend/join-office-skill.md` as a Skill, and the Agent will automatically complete the configuration and pushing.

> Detailed instructions for guest access can be found in [`frontend/join-office-skill.md`](./frontend/join-office-skill.md)

---

## 📡 Common APIs

| Endpoint | Description |
|------|------|
| `GET /health` | Health Check |
| `GET /status` | Get Primary Agent Status |
| `POST /set_state` | Set Primary Agent Status |
| `GET /agents` | Get Multi-Agent List |
| `POST /join-agent` | Guest Joins Office |
| `POST /agent-push` | Guest Pushes Status |
| `POST /leave-agent` | Guest Leaves |
| `GET /yesterday-memo` | Get Yesterday's Memo |
| `GET /config/gemini` | Get Gemini API Configuration |
| `POST /config/gemini` | Set Gemini API Configuration |
| `GET /assets/generate-rpg-background/poll` | Poll Image Generation Progress |

---

## 🖥 Desktop Pet Mode (Optional)

The `desktop-pet/` directory provides an **Electron**-based desktop wrapper version that can turn the pixel office into a transparent desktop pet window.

```bash
cd desktop-pet
npm install
npm run dev
```

- Automatically launches the Python backend on startup
- The window points to `http://127.0.0.1:19000/?desktop=1` by default
- Supports customizing the project path and Python path via environment variables

> ⚠️ This is an **optional experimental feature**, currently primarily developed and tested on macOS. For details, see [`desktop-pet/README.md`](./desktop-pet/README.md).
>
> 🙏 The Desktop Pet mode was independently developed by [@Zhaohan-Wang](https://github.com/Zhaohan-Wang). Thank you for his contribution!

---

## 🎨 Art Assets and Open Source Licenses

### Asset Sources

The guest character animations use free assets from **LimeZu**:
- [Animated Mini Characters 2 (Platformer) [FREE]](https://limezu.itch.io/animated-mini-characters-2-platform-free)

Please retain the source attribution when redistributing / demonstrating, and adhere to the original author's licensing terms.

### Licensing Agreement

- **Code / Logic: MIT** (See [`LICENSE`](./LICENSE))
- **Art Assets: Commercial Use Prohibited** (For learning / demonstration / communication purposes only)

> If you need commercial use, please replace all art assets with your own original materials.

---

## 📝 Changelog

| Date | Summary | Details |
|------|------|------|
| 2026-03-06 | 🔌 Default Port Adjustment — Adjusted default backend port from 18791 to 19000 to avoid conflicts with OpenClaw Browser Control port; synced scripts, desktop shell, and doc defaults | [`docs/CHANGELOG_2026-03.md`](./docs/CHANGELOG_2026-03.md) |
| 2026-03-05 | 📱 Stability Fixes — Fixed CDN caching, async image generation, optimized mobile sidebar, Join Key expiration and concurrency control | [`docs/UPDATE_REPORT_2026-03-05.md`](./docs/UPDATE_REPORT_2026-03-05.md) |
| 2026-03-04 | 🔒 P0/P1 Security Hardening — Blocked weak passwords, separated backend modules, auto-idle for stale status, optimized first-screen skeleton loading | [`docs/UPDATE_REPORT_2026-03-04_P0_P1.md`](./docs/UPDATE_REPORT_2026-03-04_P0_P1.md) |
| 2026-03-03 | 📋 Completed open-source release checklist | [`docs/OPEN_SOURCE_RELEASE_CHECKLIST.md`](./docs/OPEN_SOURCE_RELEASE_CHECKLIST.md) |
| 2026-03-01 | 🎉 **v2 Remaster Release** — Added Tri-lingual support, asset management system, AI interior design, comprehensive replacement of art assets | [`docs/FEATURES_NEW_2026-03-01.md`](./docs/FEATURES_NEW_2026-03-01.md) |

---

## 📁 Project Structure

```text
Star-Office-UI/
├── backend/            # Flask Backend
│   ├── app.py
│   ├── requirements.txt
│   └── run.sh
├── frontend/           # Frontend Pages and Assets
│   ├── index.html
│   ├── join.html
│   ├── invite.html
│   └── layout.js
├── desktop-pet/        # Electron Desktop Pet Version (Optional)
├── docs/               # Docs and Screenshots
│   └── screenshots/
├── office-agent-push.py  # Guest Push Script
├── set_state.py          # State Switch Script
├── state.sample.json     # State File Template
├── join-keys.sample.json # Join Key Template (Generates join-keys.json on start)
├── SKILL.md              # OpenClaw Skill
└── LICENSE               # MIT License
```

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/image?repos=ringhyacinth/Star-Office-UI&type=date&legend=top-left)](https://www.star-history.com/?repos=ringhyacinth%2FStar-Office-UI&type=date&legend=top-left)
