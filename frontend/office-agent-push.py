#!/usr/bin/env python3
"""
Hyacinth Office - Agent State Active Push Script

Usage:
1. Fill in the JOIN_KEY below (your one-time join key from Hyacinth)
2. Fill in AGENT_NAME (the name you want to display in the office)
3. Run: python office-agent-push.py
4. The script will automatically join first (on first run), then push your current state to the Hyacinth Office every 30s
"""

import json
import os
import time
import sys
from datetime import datetime

# === Information you need to fill in ===
JOIN_KEY = ""   # Required: Your one-time join key
AGENT_NAME = "" # Required: Your name in the office
OFFICE_URL = "https://office.hyacinth.im"  # Hyacinth office URL (usually no need to change)

# === Push Configuration ===
PUSH_INTERVAL_SECONDS = 15  # Push interval in seconds (more real-time)
STATUS_ENDPOINT = "/status"
JOIN_ENDPOINT = "/join-agent"
PUSH_ENDPOINT = "/agent-push"

# Automatic state daemon: Automatically returns to idle when local state file doesn't exist or hasn't updated in a long time, to avoid "fake working"
STALE_STATE_TTL_SECONDS = int(os.environ.get("OFFICE_STALE_STATE_TTL", "600"))

# Local state storage (remembers the agentId obtained from the last join)
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "office-agent-state.json")

# Prioritize reading the state file of the local OpenClaw workspace (closer to AGENTS.md workflow)
# Supports auto-discovery to reduce manual configuration costs and avoid hardcoding absolute paths:
# - Prioritize environment variables OPENCLAW_HOME / OPENCLAW_WORKSPACE_DIR
# - Secondary: current user's HOME/.openclaw
# - Fallback: current working directory and script directory
OPENCLAW_HOME = os.environ.get("OPENCLAW_HOME") or os.path.join(os.path.expanduser("~"), ".openclaw")
OPENCLAW_WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE_DIR") or os.path.join(OPENCLAW_HOME, "workspace")

DEFAULT_STATE_CANDIDATES = [
    os.path.join(OPENCLAW_WORKSPACE_DIR, "star-office-ui", "state.json"),
    os.path.join(OPENCLAW_WORKSPACE_DIR, "state.json"),
    "/root/.openclaw/workspace/Star-Office-UI/state.json",  # Current repository (exact case)
    "/root/.openclaw/workspace/star-office-ui/state.json",  # Historical/compatible path
    "/root/.openclaw/workspace/state.json",
    os.path.join(os.getcwd(), "state.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json"),
]

# If the peer's local /status requires authentication, fill in the token here (or via env var OFFICE_LOCAL_STATUS_TOKEN)
LOCAL_STATUS_TOKEN = os.environ.get("OFFICE_LOCAL_STATUS_TOKEN", "")
LOCAL_STATUS_URL = os.environ.get("OFFICE_LOCAL_STATUS_URL", "http://127.0.0.1:19000/status")
# Optional: Directly specify the local state file path (simplest solution: bypasses /status authentication)
LOCAL_STATE_FILE = os.environ.get("OFFICE_LOCAL_STATE_FILE", "")
VERBOSE = os.environ.get("OFFICE_VERBOSE", "0") in {"1", "true", "TRUE", "yes", "YES"}


def load_local_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "agentId": None,
        "joined": False,
        "joinKey": JOIN_KEY,
        "agentName": AGENT_NAME
    }


def save_local_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_state(s):
    """Compatible with different local state words, mapped to office recognized states."""
    s = (s or "").strip().lower()
    if s in {"writing", "researching", "executing", "syncing", "error", "idle"}:
        return s
    if s in {"working", "busy", "write"}:
        return "writing"
    if s in {"run", "running", "execute", "exec"}:
        return "executing"
    if s in {"research", "search"}:
        return "researching"
    if s in {"sync"}:
        return "syncing"
    return "idle"


def map_detail_to_state(detail, fallback_state="idle"):
    """When there is only detail, infer state using keywords (closer to AGENTS.md office logic)."""
    d = (detail or "").lower()
    if any(k in d for k in ["error", "error", "bug", "exception", "alarm", "报错", "异常", "报警"]):
        return "error"
    if any(k in d for k in ["sync", "sync", "backup", "同步", "备份"]):
        return "syncing"
    if any(k in d for k in ["research", "research", "search", "lookup", "调研", "搜索", "查资料"]):
        return "researching"
    if any(k in d for k in ["execute", "run", "advance", "process task", "working", "writing", "执行", "推进", "处理任务", "工作中"]):
        return "writing"
    if any(k in d for k in ["standby", "rest", "idle", "complete", "done", "待命", "休息", "完成"]):
        return "idle"
    return fallback_state


def _state_age_seconds(data):
    try:
        ts = (data or {}).get("updated_at")
        if not ts:
            return None
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is not None:
            from datetime import timezone
            return (datetime.now(timezone.utc) - dt.astimezone(timezone.utc)).total_seconds()
        return (datetime.now() - dt).total_seconds()
    except Exception:
        return None


def fetch_local_status():
    """Read local status:
    1) Prioritize state.json (Complies with AGENTS.md: writing before task, idle after completion)
    2) Second priority: try local HTTP /status
    3) Finally: fallback idle

    Extra debounce: If local state update time exceeds STALE_STATE_TTL_SECONDS, automatically treated as idle.
    """
    # 1) Read local state.json (Prioritize explicitly specified path, auto-discover secondary)
    candidate_files = []
    if LOCAL_STATE_FILE:
        candidate_files.append(LOCAL_STATE_FILE)
    for fp in DEFAULT_STATE_CANDIDATES:
        if fp not in candidate_files:
            candidate_files.append(fp)

    for fp in candidate_files:
        try:
            if fp and os.path.exists(fp):
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    # Only accept "state file" structure; prevent mistakenly treating office-agent-state.json (only caches agentId) as source
                    if not isinstance(data, dict):
                        continue
                    has_state = "state" in data
                    has_detail = "detail" in data
                    if (not has_state) and (not has_detail):
                        continue

                    state = normalize_state(data.get("state", "idle"))
                    detail = data.get("detail", "") or ""
                    # detail fallback correction, ensuring "work/rest/alarm" falls into the correct area
                    state = map_detail_to_state(detail, fallback_state=state)

                    # Prevent long-unupdated state from being stuck in working state
                    age = _state_age_seconds(data)
                    if age is not None and age > STALE_STATE_TTL_SECONDS:
                        state = "idle"
                        detail = f"Local state unupdated for {STALE_STATE_TTL_SECONDS}s, auto-returned to standby"

                    if VERBOSE:
                        print(f"[status-source:file] path={fp} state={state} detail={detail[:60]}")
                    return {"state": state, "detail": detail}
        except Exception:
            pass

    # 2) Try local /status (may need authentication)
    try:
        import requests
        headers = {}
        if LOCAL_STATUS_TOKEN:
            headers["Authorization"] = f"Bearer {LOCAL_STATUS_TOKEN}"
        r = requests.get(LOCAL_STATUS_URL, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            state = normalize_state(data.get("state", "idle"))
            detail = data.get("detail", "") or ""
            state = map_detail_to_state(detail, fallback_state=state)

            age = _state_age_seconds(data)
            if age is not None and age > STALE_STATE_TTL_SECONDS:
                state = "idle"
                detail = f"Local /status unupdated for {STALE_STATE_TTL_SECONDS}s, auto-returned to standby"

            if VERBOSE:
                print(f"[status-source:http] url={LOCAL_STATUS_URL} state={state} detail={detail[:60]}")
            return {"state": state, "detail": detail}
        # If 401, means token is needed
        if r.status_code == 401:
            return {"state": "idle", "detail": "Local /status needs auth (401), set OFFICE_LOCAL_STATUS_TOKEN"}
    except Exception:
        pass

    # 3) Default fallback
    if VERBOSE:
        print("[status-source:fallback] state=idle detail=Standing by")
    return {"state": "idle", "detail": "Standing by"}


def do_join(local):
    import requests
    payload = {
        "name": local.get("agentName", AGENT_NAME),
        "joinKey": local.get("joinKey", JOIN_KEY),
        "state": "idle",
        "detail": "Just joined"
    }
    r = requests.post(f"{OFFICE_URL}{JOIN_ENDPOINT}", json=payload, timeout=10)
    if r.status_code in (200, 201):
        data = r.json()
        if data.get("ok"):
            local["joined"] = True
            local["agentId"] = data.get("agentId")
            save_local_state(local)
            print(f"✅ Successfully joined Hyacinth Office, agentId={local['agentId']}")
            return True
    print(f"❌ Join failed: {r.text}")
    return False


def do_push(local, status_data):
    import requests
    payload = {
        "agentId": local.get("agentId"),
        "joinKey": local.get("joinKey", JOIN_KEY),
        "state": status_data.get("state", "idle"),
        "detail": status_data.get("detail", ""),
        "name": local.get("agentName", AGENT_NAME)
    }
    r = requests.post(f"{OFFICE_URL}{PUSH_ENDPOINT}", json=payload, timeout=10)
    if r.status_code in (200, 201):
        data = r.json()
        if data.get("ok"):
            area = data.get("area", "breakroom")
            print(f"✅ Status synced, current area={area}")
            return True

    # 403/404: Refused/Removed → Stop pushing
    if r.status_code in (403, 404):
        msg = ""
        try:
            msg = (r.json() or {}).get("msg", "")
        except Exception:
            msg = r.text
        print(f"⚠️  Access denied or removed from room ({r.status_code}), stopping push: {msg}")
        local["joined"] = False
        local["agentId"] = None
        save_local_state(local)
        sys.exit(1)

    print(f"⚠️  Push failed: {r.text}")
    return False


def main():
    local = load_local_state()

    # Startup hint for state source and URL (helps with port/state issues, e.g. issue #31)
    if LOCAL_STATE_FILE:
        print(f"State file: {LOCAL_STATE_FILE}")
    else:
        first_existing = next((p for p in DEFAULT_STATE_CANDIDATES if p and os.path.exists(p)), None)
        if first_existing:
            print(f"State file (auto): {first_existing}")
        else:
            print("State file: auto-discover (set OFFICE_LOCAL_STATE_FILE if state not found)")
    print(f"Local status URL: {LOCAL_STATUS_URL} (set OFFICE_LOCAL_STATUS_URL if backend uses another port)")

    # Confirm config completeness first
    if not JOIN_KEY or not AGENT_NAME:
        print("❌ Please fill in JOIN_KEY and AGENT_NAME at the top of the script first")
        sys.exit(1)

    # If haven't joined before, join first
    if not local.get("joined") or not local.get("agentId"):
        ok = do_join(local)
        if not ok:
            sys.exit(1)

    # Continuous pushing
    print(f"🚀 Started continuous status push, interval={PUSH_INTERVAL_SECONDS} seconds")
    print("🧭 Status logic: Working -> Workspace; Standby/Done -> Breakroom; Error -> Bug Area")
    print("🔐 If local /status returns Unauthorized (401), set env vars: OFFICE_LOCAL_STATUS_TOKEN or OFFICE_LOCAL_STATUS_URL")
    try:
        while True:
            try:
                status_data = fetch_local_status()
                do_push(local, status_data)
            except Exception as e:
                print(f"⚠️  Push exception: {e}")
            time.sleep(PUSH_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n👋 Stopped push")
        sys.exit(0)


if __name__ == "__main__":
    main()
