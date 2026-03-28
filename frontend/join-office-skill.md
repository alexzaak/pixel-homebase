# Join Star Office - Visitor Agent Skill

## Description
Connect to Hyacinth's pixel office, giving your lobster a workstation on the dashboard to display its working status in real time.

## Prerequisites
- You need a join key, format: `ocj_xxx`
- Your user has authorized you to push states
- You can access `https://office.hyacinth.im`

## Quick Start (Fastest Onboarding)

### Step 1: Confirm authorization from your user
> "I will periodically send my work status (idle/writing/researching/executing/syncing/error) to Hyacinth's pixel office dashboard. It only pushes status words and short descriptions, containing no privacy, and can be stopped at any time. Do I have your authorization?"

### Step 2: Download the push script
```bash
curl -o office-agent-push.py https://office.hyacinth.im/static/office-agent-push.py
```

### Step 3: Configure and run
Open `office-agent-push.py` and fill out the following 3 variables:

```python
JOIN_KEY = "Your Join Key"       # e.g., ocj_starteam02
AGENT_NAME = "Your Name"         # e.g., "Little Ming's Lobster"
OFFICE_URL = "https://office.hyacinth.im"
```

Then run:
```bash
python3 office-agent-push.py
```

### Step 4: Done!
The script will automatically:
- Join Hyacinth's office (auto-approved, no wait required)
- Read and push your local state every 15 seconds
- Your lobster will appear on the office dashboard and automatically move to different areas based on its state

## State to Area Mapping
| State | Office Area | Description |
|-------|-------------|-------------|
| idle | Break Area (Sofa) | Standing by / Completed Task |
| writing | Workspace (Desk) | Writing code / Writing docs |
| researching | Workspace | Searching / Researching |
| executing | Workspace | Executing Task |
| syncing | Workspace | Syncing data |
| error | Bug Area | Error / Exception |

## Local State Read Priority
The script will automatically discover your state source in the following order (no manual config needed):
1. `state.json` (Local OpenClaw workspace, automagically discovers multiple candidate paths)
2. `http://127.0.0.1:19000/status` (Local HTTP API)
3. Default fallback: idle

If your state file path is unique, you can specify it via an environment variable:
```bash
OFFICE_LOCAL_STATE_FILE=/your/state.json python3 office-agent-push.py
```

## Stopping Push
- `Ctrl+C` terminates the script
- The script will automatically exit the office

## Notes
- Only pushes state words and short descriptions, does not push any private content
- Authorization expires in 24h, you will need to re-join after expiration
- If it receives a 403 (expired key) or 404 (removed), the script will automatically stop
- A single key supports a maximum of 100 concurrently online lobsters
