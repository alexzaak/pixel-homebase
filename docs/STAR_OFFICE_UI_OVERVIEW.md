# Star Office UI — Features Overview

Star Office UI is a "pixel office" visualization interface, used to render the state of AI assistants/multiple OpenClaw guests into a small office scene viewable on web pages (including mobile phones).

## What you can see
- Pixel office background (top-down view)
- Characters (Star + Guests) will move to different areas based on their state
- Names and speech bubbles display current status/thoughts (customizable mapping)
- Can also be displayed when opened on mobile phones (suitable for portfolio showcases/livestreams/external demonstrations)

## Core Capabilities

### 1) Single Agent (Local Star) State Rendering
- Backend reads `state.json` to provide `GET /status`
- Frontend polls `/status`, rendering Star's area based on `state`
- Provides `set_state.py` to quickly switch states

### 2) Multi-Guest (Multi-Lobster) Joining Office
- Guests join via `POST /join-agent`, securing an `agentId`
- Guests continuously push their state via `POST /agent-push`
- Frontend fetches guest list via `GET /agents` and renders

### 3) Join Key Mechanism
- Supports fixed reusable join keys (e.g., `ocj_starteam01~08`)
- Supports maximum concurrent online limit per key (default 3)
- Makes it easier to control "who can enter the office" and "how many lobsters can enter simultaneously on the same key"

### 4) State → Area Mapping (Unified Logic)
- idle → breakroom
- writing / researching / executing / syncing → writing (workspace)
- error → error (bug area)

### 5) Guest Animation and Performance Optimization
- Guest characters use animated sprites
- Better WebP resources support (smaller size, faster loading)

### 6) Non-Obstructive Name/Bubble Layout
- Separation logic for real guests and demo guests
- Non-demo guest names and bubbles are shifted upwards globally
- Bubbles are anchored above the name, avoiding overlapping the name

### 7) Demo Mode (Optional)
- Demo guests only displayed when `?demo=1` is provided (hidden by default)
- Demo and real guests do not conflict

## Main APIs (Backend)
- `GET /`: Frontend Page
- `GET /status`: Single agent status (backward compatibility)
- `GET /agents`: Multi-agent list (used for guest rendering)
- `POST /join-agent`: Guest joins
- `POST /agent-push`: Guest pushes status
- `POST /leave-agent`: Guest leaves
- `GET /health`: Health check

## Security and Privacy Notes
- Do not write private information into `detail` (because it becomes rendered/fetchable)
- Must clean up before open sourcing: logs, runtime state files, join keys, tunnel outputs, etc.

## Art Asset Usage Notice (Mandatory)
- Code can be open-sourced, but art assets (backgrounds, characters, animations, etc.) copyrights belong to the original authors/studios.
- Art assets are for learning and demonstration purposes only, **commercial use is prohibited**.
