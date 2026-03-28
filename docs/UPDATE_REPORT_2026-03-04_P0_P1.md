# Star Office UI Update Document (P0 / P1)

Update Date: 2026-03-04
Branch: `feat/office-art-rebuild`

---

## 1. Update Goals

The goals of this update round are divided into two levels:

- **P0: Security and Releasability** (Prevent leaks, prevent weak configs, self-testable before launch)
- **P1: Structure and Stability Optimization** (No feature reduction, improve state sync and loading experience)

Simultaneously addressed critical online issues:

- Occasional 502 from service (Unstable process/service startup)
- Character state inconsistent with real working state (especially "still at desk after concluding reply")

---

## 2. Completed P0 Items

### 2.1 Backend Security Baseline Hardening

- Added production mode security validation (blocks startup on weak secrets/passwords)
- Session Cookie security parameter hardening (HttpOnly / SameSite / Secure)
- Automatically attempts to tighten file permissions (`600`) after writing `runtime-config.json`

### 2.2 Sensitive Files Governance

- Supplemented runtime and high-risk files in `.gitignore`
- Introduced sample files to replace runtime files:
  - `join-keys.sample.json`
  - `.env.example`
- `join-keys.json` is now initialized at runtime, no longer a fixed config in the repository

### 2.3 Pre-launch Security Self-test Capability

- Added `scripts/security_check.py`
- Can check:
  - Weak secret / weak password
  - Whether risk files are tracked by git
  - Common sensitive token patterns

---

## 3. Completed P1 Items (No business capability changes)

### 3.1 Backend Structural Split

Without changing existing API behavior, split out `backend/app.py`:

- `backend/security_utils.py`
- `backend/memo_utils.py`
- `backend/store_utils.py`

Benefits:
- Reduced single-file complexity
- Lowered regression risk during later feature changes
- Improved readability and maintenance efficiency

### 3.2 State Sync Fixes (Core)

- Fixed state source path priority (avoiding reading wrong state files)
- Added automatic fallback to `idle` for stale states (avoiding fake "working" states)
- Frontend state polling changed to a faster rhythm with forced visual alignment to avoid animations getting stuck on old states

### 3.3 Image Generation Model Strategy Convergence

Converged to two user model semantics as required:

- `nanobanana-pro`
- `nanobanana-2`

And supplemented provider mapping and error detail surfacing to improve diagnosability.

### 3.4 First Screen Performance and Feel Optimization

- Homepage HTML caching (Backend in-process cache)
- Delayed non-critical initialization (Show screen first)
- Added canvas skeleton screen to reduce the "black screen + long loading" feel
- Sped up loading overlay fade-out

---

## 4. Online Stability Fixes (Focus of this round)

### 4.1 502 Root Cause

Cloudflare is normal, but the `18888` origin process was unstable/inconsistently started, causing occasional connection refused.

### 4.2 Handled

- Fixed and unified `star-office-ui.service` startup method (systemd resident)
- Cleaned up port hogging caused by manual temporary starts
- Restarted and verified:
  - `star-office-ui.service` running normally
  - `star-office-push.service` running normally

---

## 5. Current Known Risks / To Be Followed Up

1. **State Strategy still needs full Eventualization**
   - Misjudgments have been vastly reduced, but it is advised to make a single state controller later (explicit events priority, completely disable implicit inference)

2. **Process Model is still Flask Development Server**
   - Currently usable but not ideal; recommend migrating to production process models like gunicorn/uvicorn later

3. **Animation State Sync still advised to add an end-to-end regression script**
   - Especially the switching link between writing / syncing / error / idle

---

## 6. Acceptance Suggestions (Manual)

Acceptance Address: `https://simonoffice.hyacinth.im/`

Advised to at least cover:

1. Homepage entry speed and skeleton screen experience
2. State switching (writing / syncing / error / idle)
3. Whether it returns to the break area after concluding a reply
4. Both image generation entries (Moving / Finding Realtor)
5. Whether it auto-recovers after network disconnect or service fluctuation

---

## 7. Commit Scope (Summary)

This round mainly covered:

- Security and config: P0
- Backend refactoring: P1
- State sync and animation consistency fixes
- Image generation model strategy and error diagnosis
- Load performance and experience optimization
- systemd resident and stability fixes

If PR attachments are needed, this document can be directly used as "Update Notes / Release Notes".
