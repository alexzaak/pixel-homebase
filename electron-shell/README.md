# Star Desktop Pet (Electron Shell)

This directory contains the Electron version of the desktop shell, existing alongside the current Tauri version to facilitate gradual migration.

## Integrated Capabilities

- Reuses existing frontend: `http://127.0.0.1:19000/?desktop=1`
- Reuses mini page: `desktop-pet/src/minimized.html`
- Automatically starts Python backend on boot (if not already running)
- Toggle between Main Window / Mini Window
- Resident tray (menu bar) menu
- Injects a `window.__TAURI__` compatibility layer via preload, minimizing required changes to existing frontend logic

## Launch Method

```bash
cd "/Users/wangzhaohan/Documents/GitHub/Star-Office-UI/electron-shell"
npm install
npm run dev
```

## Optional Environment Variables

- `STAR_PROJECT_ROOT`: Project root directory (auto-detected by default)
- `STAR_BACKEND_PYTHON`: Backend Python executable path
- `STAR_BACKEND_HOST`: Backend host (defaults to `127.0.0.1`)
- `STAR_BACKEND_PORT`: Backend port (defaults to `19000`)

## Notes

- This is currently a "runnable migration skeleton", aiming to replace the desktop container layer first.
- The existing Tauri directory remains unaffected, and can be rolled back to or compared in parallel at any time.
