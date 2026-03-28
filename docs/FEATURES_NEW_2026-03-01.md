# Star Office UI — New Features (This Phase)

## 1. Multi-Lobster Guest System
- Supports multiple remote OpenClaws joining the same office simultaneously.
- Guests support independent avatars, names, states, areas, and speech bubbles.
- Supports dynamic online/offline status and real-time refreshing.

## 2. Join Key Mechanism Upgrade
- Upgraded from "one-time key" to "fixed reusable key".
- Default keys: `ocj_starteam01` ~ `ocj_starteam08`.
- Preserved security controls: `maxConcurrent` concurrency limit per key (default 3).

## 3. Concurrency Control (Race Condition Fixed)
- Fixed race condition issue during concurrent joins.
- The 4th concurrent join for the same key is correctly rejected (HTTP 429).

## 4. Guest State Mapping and Area Rendering
- `idle -> breakroom`
- `writing/researching/executing/syncing -> writing`
- `error -> error`
- Guest speech bubble text is synchronized with state, preventing misalignment.

## 5. Guest Animation and Resource Optimization
- Guests upgraded from static images to animated sprites (pixel-art).
- WebP versions provided for `guest_anim_1~6`, reducing payload size.

## 6. Name and Bubble Display Optimization
- Names and bubble positions for non-demo guests shifted upward to avoid obscuring the character.
- Bubble anchoring is now based on name positioning, ensuring "bubble is above the name".

## 7. Mobile Display
- The page can be directly accessed and displayed on mobile phones.
- Basic mobile layout adaptations added for demonstration scenarios.

## 8. Remote Push Script Integration Improvements
- Supports reading state from state file and pushing to office.
- Added state source diagnostic logs (helps diagnose "why is it always idle").
- Fixed `AGENT_NAME` environment variable override timing issue.
