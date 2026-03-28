# Star Office UI — Open Source Release Checklist (Preparation Only, Do Not Upload)

## 0. Current Goal
- This document is for "pre-release preparation", do not perform actual uploads.
- All push actions require explicit final approval from Hyacinth.

## 1. Privacy and Security Review Results (Current Repository)

### Identified High-Risk Files (Must be excluded)
- Runtime Logs:
  - `cloudflared.out`
  - `cloudflared-named.out`
  - `cloudflared-quick.out`
  - `healthcheck.log`
  - `backend.log`
  - `backend/backend.out`
- Runtime State:
  - `state.json`
  - `agents-state.json`
  - `backend/backend.pid`
- Backup/Historical Files:
  - `index.html.backup.*`
  - `index.html.original`
  - `*.backup*` directories and files
- Local Virtual Envs and Caches:
  - `.venv/`
  - `__pycache__/`

### Identified Potentially Sensitive Content
- Absolute paths in code `/root/...` (Recommend changing to relative paths or environment variables)
- Private domains in docs and scripts like `office.example.com` (Can be kept as an example, but suggest using placeholder domains)

## 2. Required Modifications (Before Commit)

### A. .gitignore (Should be updated)
Suggested additions:
```
*.log
*.out
*.pid
state.json
agents-state.json
join-keys.json
*.backup*
*.original
__pycache__/
.venv/
venv/
```

### B. README Copyright Notice (Must be added)
Add an "Art Asset Copyright and Usage Restrictions" section:
- Code follows open-source license (e.g., MIT)
- Art assets belong to original authors/studios
- Assets are for learning/demonstration purposes only, **commercial use is prohibited**

### C. Slimming Down Release Directory
- Clean up runtime logs, state files, and backups
- Only keep "minimum runnable set + necessary assets + docs"

## 3. Suggested Structure for Release Package in Preparation
```
star-office-ui/
  backend/
    app.py
    requirements.txt
    run.sh
  frontend/
    index.html
    game.js (If still needed)
    layout.js
    assets/* (Publicly releasable assets only)
  office-agent-push.py
  set_state.py
  state.sample.json
  README.md
  LICENSE
  SKILL.md
  docs/
```

## 4. Final Pre-Release Check (For Hyacinth's Confirmation)
- [ ] Keep private domain example (`office.example.com`)?
- [ ] Which art resources are allowed to be public (confirm item-by-item)?
- [ ] Does the README "non-commercial" disclaimer wording meet expectations?
- [ ] Should the "Arwen Lobster Integration Script" be placed in an `examples` directory separately?

## 5. Current Status
- ✅ Documentation preparation completed (summary, feature explanation, Skill v2, release checklist)
- ⏳ Waiting for Hyacinth to confirm "public asset scope + disclaimer copy + whether to execute packaging and cleanup script"
- ⛔ Has not been uploaded to GitHub
