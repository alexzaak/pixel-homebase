# Desktop Pet State Integration Guide (for openclaw)

The desktop pet retrieves its current state by reading **state.json** and updates its appearance (overhead icon/emoji, speech bubbles, character animation, pathfinding target). openclaw needs to **write or update** this file to drive the desktop pet.

---

## 1. File Location

- **Path**: The `state.json` under the desktop pet's working directory (upon startup, it resolves to the project root directory, which contains `state.json` and the `layers/` directory).
- **Format**: UTF-8 JSON.

---

## 2. state.json Structure

```json
{
  "state": "idle",
  "detail": "Optional, state description, currently used only for display/debugging",
  "progress": 0.0,
  "updated_at": "2025-02-27T12:00:00Z"
}
```

| Field        | Type    | Required | Description |
|--------------|---------|----------|-------------|
| `state`      | string  | Yes      | Current state, see table below. The desktop pet polls this every ~2s. |
| `detail`     | string  | No       | Optional description, can be extended later for speech bubbles or debugging. |
| `progress`   | number  | No       | 0~1, optional progress, can be extended later. |
| `updated_at` | string  | No       | ISO8601 time, optional. |

**Only the `state` field affects the desktop pet's behavior**; other fields can be left empty or omitted.

---

## 3. State Values (The `state` openclaw should write)

The desktop pet only recognizes the following **standard state names** (lowercase). Writing other values will treat it as `idle` or resolve via alias mapping.

| state Value      | Meaning           | Desktop Pet Behavior Overview |
|------------------|-------------------|-------------------------------|
| `idle`           | Slacking/No task  | 💤 Breathing animation, random wandering |
| `writing`        | Writing/Notes     | Word icon, walks to writing POI |
| `receiving`      | Receiving message | Hangouts icon, walks to receiving POI |
| `replying`       | Replying to msg   | Glovo icon, walks to replying POI |
| `researching`    | Researching       | Google icon, walks to researching POI |
| `executing`      | Executing/Running | ⚡️ emoji, walks to executing POI |
| `syncing`        | Syncing/Backup    | ☁️ emoji, walks to syncing POI |
| `error`          | Error             | ❗️ emoji, walks to error POI |

POIs are configured in `layers/map.json` under `pois`; when the state changes, the desktop pet will pathfind to the corresponding tile.

---

## 4. Alias Mapping (Optional)

If different names are used on the openclaw side, the desktop pet frontend will first perform an **alias → standard state** mapping, then display the behavior according to the table above:

| openclaw writable state | Mapped to |
|-------------------------|-----------|
| `working`               | `writing` |
| `run`                   | `executing` |
| `running`               | `executing` |
| `sync`                  | `syncing` |
| `research`              | `researching` |

Any `state` not in the above lists will be treated as `idle`.

---

## 5. What openclaw needs to do

- **Write state.json**: Create or overwrite `state.json` in the agreed directory, ensuring `state` is one of the 8 standard states (or 5 aliases) above.
- **When to write**: Write once when the state changes; the desktop pet polling interval is about 2 seconds, no need for high-frequency writing.
- **Examples**
  - Starts writing doc: `{ "state": "writing" }`
  - Received message: `{ "state": "receiving" }`
  - Replying: `{ "state": "replying" }`
  - Researching: `{ "state": "researching" }`
  - Executing task: `{ "state": "executing" }`
  - Syncing: `{ "state": "syncing" }`
  - Error: `{ "state": "error" }`
  - Slacking/No task: `{ "state": "idle" }`

By updating `state.json` in this manner, it will sync consistently with the current desktop pet behavior and POIs.
