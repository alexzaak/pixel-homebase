# Star Office Tauri Desktop Shell

This directory is used to package `Star-Office-UI` into a desktop application (transparent window), and automatically launch the backend process on startup.

## Development & Running

First, prepare the Python environment in the repository root directory:

```bash
cd /Users/wangzhaohan/Documents/GitHub/Star-Office-UI
uv venv .venv
uv pip install -r backend/requirements.txt --python .venv/bin/python
```

Then start Tauri:

```bash
cd /Users/wangzhaohan/Documents/GitHub/Star-Office-UI/desktop-pet
npm install
npm run dev
```

## Automatic Backend Launch Logic

- Priority: `../.venv/bin/python backend/app.py`
- Fallback 1: `python3 backend/app.py`
- Fallback 2: `python backend/app.py`

The window defaults to navigating to:

- `http://127.0.0.1:19000/?desktop=1`

## Optional Environment Variables

- `STAR_PROJECT_ROOT`: Project root directory (auto-detected by default)
- `STAR_BACKEND_PYTHON`: Custom Python executable path
- `STAR_BACKEND_URL`: Custom URL for the desktop window to open
