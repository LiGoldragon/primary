# 63 · Extension bridge — driving the psyche's REAL Chrome session with browser-use + local Gemma 4 (2026-06-19)

Builds directly on generation 799 (reports 61, 62): browser-use is packaged in
CriomOS-home, on PATH as `browser-use`/`bu`/`browser-use-local`/`browser-use-gemma`,
wired to the workspace-local Gemma 4 at `http://prometheus.goldragon.criome:11434/v1`
(`gemma-4-26b-a4b`, gopass token, no cloud provider). This report adds the
EXTENSION PATH so that browser-use can drive the psyche's **real, logged-in
Chrome profile** — honouring Spirit 5g4d (prefer the human's main Chrome
profile) and bypassing the Chrome 136+ rule that refuses the external
`--remote-debugging-port` on the default profile.

The mechanism is an in-browser bridge: a Chrome extension using the
`chrome.debugger` API (which attaches CDP to a tab FROM INSIDE the browser, on
the real profile) that relays to a local endpoint browser-use connects to via
`--cdp-url`. This was IMPLEMENTED, PACKAGED, and BUILT. It is staged on
CriomOS-home `main` for the same `lojix-run HomeOnly` home deploy gen 799 used.
The extension load is a deliberate **one-time manual step** (Chrome forbids
programmatic load of an arbitrary unpacked extension — which is also the right
consent gate for a capability that grants control of the logged-in browser).

## 1 · The chosen bridge + why + manual vs automatic load

### What the research ruled out (and why naive paths fail)

The deployed `browser-use` is **0.13.1** (cdp-use 1.4.5). Its CLI exposes
`--cdp-url CDP_URL` ("Connect to existing browser via CDP URL (http:// or
ws://)"), `--profile`, `--connect`, `--session`, `--mcp`. Reading the deployed
library's `browser/session.py` settles the contract:

- `--cdp-url http://…` → browser-use fetches `/json/version`, reads
  `webSocketDebuggerUrl`, connects to that.
- `--cdp-url ws://…` → connects to that WebSocket directly.
- On connect it immediately drives the **browser-LEVEL Target domain**:
  `Target.setAutoAttach`, `Target.getTargets`, `Target.attachToTarget`,
  `Target.createTarget` (`SessionManager.start_monitoring()` +
  `setAutoAttach(autoAttach=true, flatten=true)`).

That last point is the load-bearing constraint. Candidates evaluated:

| Option | Verdict |
|---|---|
| **(a) browser-use native real-browser** (`--profile Default`) | browser-use launches its OWN Chrome with `--remote-debugging-port` + `--user-data-dir` (its `local_browser_watchdog`). On Chrome 147 that is **refused on the Default profile** (the 136+ rule). browser-use has **no** chrome.debugger fallback. Does not drive the real session. |
| **(b) Playwright MCP `--extension` + the Playwright Extension** | The official Playwright Extension (Chrome Web Store / unpacked from `microsoft/playwright` `packages/extension`) DOES use `chrome.debugger` on the real default profile and DOES emulate the browser-level Target domain (`protocolHandlers.ts` answers `Target.setAutoAttach` "from a populated tab model"). BUT its relay speaks the Playwright/MCP transport; Playwright MCP `--extension` mode **does not expose a browser-level CDP url** to external tools (microsoft/playwright-mcp issue #1130 requested exactly this; it does not exist). So browser-use's `--cdp-url` cannot ride it. |
| **(c) chrome.debugger CDP relay** (OpenClaw Browser Relay / ClawHosters / nano-browser) | These DO attach to the real profile, but their relays expose a **tab-level** endpoint (`ws://127.0.0.1:18792/cdp`). browser-use/Playwright sending browser-level `Target.attachToBrowserTarget` get `{"code":-32000,"message":"Not allowed"}` (openclaw issue #30426, closed not-planned). Tab-level relays do **not** work with browser-use 0.13.x. |

The decisive finding: **no off-the-shelf component hands the deployed
browser-use a `--cdp-url` that drives the real profile.** The Playwright
Extension proves browser-level Target emulation over `chrome.debugger` is doable
(it does it internally); the failing relays prove that NOT doing it breaks
browser-use.

### The chosen bridge

A **purpose-built, dependency-light bridge packaged into CriomOS-home**
(`packages/chrome-cdp-bridge`), with two artifacts:

1. **An unpacked Chrome extension** (`extension/`, manifest v3, permissions
   `debugger`+`tabs`+`storage`, `<all_urls>`). Its service worker
   (`background.js`) attaches `chrome.debugger` to the tab the human **clicks**
   the toolbar icon on (the consent gesture), on the **real default profile**,
   and relays that tab's raw CDP over an outbound WebSocket to the local relay.
   Click again to detach; the badge shows `ON`.

2. **The relay** (`relay.mjs`, the `chrome-cdp-bridge-relay` binary, Node +
   `ws`). It (a) serves `http://127.0.0.1:9333/json/version` →
   `{webSocketDebuggerUrl: ws://127.0.0.1:9333/devtools/browser/…}` for
   browser-use's `--cdp-url`; (b) accepts the extension's outbound WS on
   `/extension`; (c) **synthesises the browser-level Target domain** over the
   single attached tab (`Target.setAutoAttach` / `getTargets` /
   `attachToTarget` / `createTarget` / `getBrowserContexts` /
   `Browser.getVersion` answered by the relay itself), and forwards only
   page-level CDP to the extension. This is exactly the part the OpenClaw-family
   relays omit — and the reason they fail with browser-use.

**Why this over reusing the Playwright Extension:** the Playwright Extension's
relay wire-protocol is Playwright-internal (its `relayConnection.ts` handshake),
so re-exposing a browser-use `--cdp-url` from it means reimplementing
Playwright's relay side anyway — more coupling, more version drift, for the same
result. A small standalone bridge whose ONLY job is "one consented tab → a
browser-level CDP url" is simpler, has one npm dep (`ws`), and is the right
scope for the supervised-scout model (exactly one tab, the one the human
clicked). It reuses the **same gopass token path the existing `playwright-cli`
package already seeds** (`chrome-browser/playwright-mcp-extension-token`).

### Manual or automatic load

**Manual, once.** Chrome forbids programmatic `--load-extension` of an arbitrary
unpacked extension into the real default profile (and the existing home Chrome
is the plain `google-chrome`, not a debug launch). This is FINE and is flagged
clearly: the package ships the unpacked extension into the nix store and prints
its path via `browser-use-attach --extension-path`; the psyche loads it once via
`chrome://extensions` → Developer mode → **Load unpacked**. That one-time step is
also the correct consent boundary for a capability that grants control of the
logged-in browser.

## 2 · The exact CriomOS-home changes

New package `packages/chrome-cdp-bridge/`:

| File | Purpose |
|---|---|
| `relay.mjs` | The CDP relay: `/json/version` + browser-level Target emulation + page-level forwarding to the extension. ~290 lines, no secrets. |
| `extension/manifest.json` | Manifest v3, `debugger`+`tabs`+`storage`, `<all_urls>`, action button. |
| `extension/background.js` | Service worker: click-to-attach `chrome.debugger`, proxy CDP frames to the relay, click-to-detach. |
| `package.json` / `package-lock.json` | Single dep `ws@8.18.0` (Node 24 has a WS client but no WS server). |
| `default.nix` | `buildNpmPackage` (like `packages/playwright-cli`): exposes `chrome-cdp-bridge-relay` + `chrome-cdp-bridge-extension-path`, ships the unpacked extension under `$out/share/chrome-cdp-bridge/extension`. `npmDepsHash = sha256-h4J3qVVazU9bLOp+JxFjyQ8gTtPwUh1xy/TyGQnskz4=`. |

Module `modules/home/profiles/max/browser-use.nix` (extended, gen-799 Gemma
wiring untouched): adds `chromeCdpBridge = callPackage … {}` and a new
`browser-use-attach` wrapper. The wrapper sources the bridge token from gopass
(`chrome-browser/playwright-mcp-extension-token`, never logged) and the Gemma
endpoint/token (the existing `gemmaEnvPreamble`), starts the relay on
`127.0.0.1:9333`, waits for `/json/version`, then runs ONE browser-use task with
the local Gemma 4 against the relay via the existing
`browser-use-local-driver.py`. The relay is stopped on exit. New on PATH:
`chrome-cdp-bridge-relay`, `chrome-cdp-bridge-extension-path`,
`browser-use-attach`. Everything from gen 799 stays exactly as-is.

Gated to the same **Large tier** as Chrome and the rest of browser-use.

## 3 · Deploy result + rollback

**Built, deployed, and live.** Same mechanism as gen 799: CriomOS-home `main`
committed + pushed to origin (rev `d969788443cb`), then `lojix-run HomeOnly …
Profile` (build-before-switch) and `Activate` (build + switch), which rebuild
from the pushed remote rev.

- **`Profile` (build-before-switch, reversible) ran first and passed clean:**
  `lojix_run=success`, `home_profile_matches_deploy=yes`, `failed_user_units=0`,
  `niri_reload=success`. The new module integrated into the full home build with
  no errors (gen 799's `Profile` caught three real errors; this one was clean).
- **`Activate` (build + switch): `lojix_run=success`.** The live home-manager
  generation moved **799 → 800**. The new binaries are on PATH:
  `browser-use-attach`, `chrome-cdp-bridge-relay`,
  `chrome-cdp-bridge-extension-path` (plus the gen-799 tools intact). The
  deployed relay serves `/json/version` with a browser-level
  `webSocketDebuggerUrl`. The existing profile was not broken (0 failed units,
  compositor reloaded).
- **Live generation: 800. Rollback target: 799** (`home-manager generations`,
  then activate the 799 link, or `lojix-run … Activate` against the prior main
  rev). Home-manager generations are reversible.
- Request shape used (decoded from `lojix-cli` `request.rs`):
  `(HomeOnly goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/main Profile|Activate None None)`
  — the `ProposalSource` is the goldragon cluster proposal `datom.nota`.

## 4 · Neutral real-session test (relay validated end to end)

The bridge was validated end to end **without touching the real profile**, using
a faithful stand-in for the extension: a mock that bridges the relay's
page-level CDP to a **real headless Chrome** (Chrome 147) on a throwaway
profile, exactly as the real `chrome.debugger` extension would. This isolates
and proves the relay's browser-level Target emulation against the **actual
deployed browser-use 0.13.1 + the local Gemma 4**:

- browser-use connected to the relay's `--cdp-url`, the relay answered
  `Target.setAutoAttach`/`getTargets`/`attachToTarget`, browser-use's
  `SessionManager` attached the page session and set the viewport
  (`Emulation.setDeviceMetricsOverride`) — i.e. the **browser-level connect
  succeeded with no `Target.attachToBrowserTarget: Not allowed`**, the failure
  that kills tab-level relays.
- Page-level CDP flowed both ways: the real Chrome navigated to **example.com**
  through the relay (confirmed `https://example.com/` live in the headless
  Chrome's target list), and **Gemma read the page through the relay and
  identified the heading** — the agent reported, mid-run: *"I am on
  https://example.com/. I have identified that 'Example Domain' is likely the H1
  heading."* That is the full loop: relay → real CDP backend → page snapshot →
  on-prem Gemma vision → answer.
- The drive was **neutral only** — example.com, the canonical neutral page. No
  account, no DigitalOcean, no logged-in tab, no consequential click, no
  reading of any private page. The throwaway profile has no logins.

The remaining wobble is **Gemma cold-start latency** (the first vision call can
exceed browser-use's 75 s per-step LLM timeout; browser-use retries up to 6×).
This is the gen-799 behaviour (report 62 saw the same self-recovery) and is a
model-warmup property, not a bridge fault — the CDP path itself is solid.

The final on-real-profile neutral test (load the extension on the psyche's
actual Chrome, click a neutral tab, `browser-use-attach` to read its H1) is the
psyche's one-time enable step (§5) — it cannot be done for them because the
manual Load-unpacked + click is the consent gate.

## 5 · Psyche: enable once, invoke, disable

**Enable (one time):**

1. Build/activate the home profile with this change (§3) so
   `chrome-cdp-bridge-extension-path` is on PATH.
2. Print the extension dir: `browser-use-attach --extension-path`.
3. In the psyche's normal Chrome (the real profile): `chrome://extensions` →
   enable **Developer mode** (top-right) → **Load unpacked** → select that dir.
4. (Recommended) seed a shared bridge token so only the consented extension can
   reach the loopback relay: put a random string in gopass
   `chrome-browser/playwright-mcp-extension-token`, and set the same value in the
   extension (open the extension's storage via its service-worker console, or a
   later settings UI; empty token = loopback-only is also acceptable on a
   single-user box). The token never enters logs or chat.

**Invoke (drive the real session):**

```sh
# 1. Click the "CriomOS CDP Bridge" toolbar icon on the ONE tab you consent to
#    expose (badge shows ON).
# 2. Drive it with the local Gemma 4:
browser-use-attach "Read the open page and report its main heading. Do not click or navigate."
```

`browser-use-attach` starts the relay, waits for the attached tab, runs ONE
task with the on-prem Gemma 4 over the relay's `--cdp-url`, and stops the relay
on exit. (The lower-level `browser-use-local <cdp-url> <task>` still drives a
plain CDP Chrome for the non-extension scout flow from report 61.)

**Disable / toggle (this grants real-browser control):**

- **Per session:** click the toolbar icon again to **detach** the tab (badge
  clears); or just don't run `browser-use-attach` (the relay only runs while a
  task runs).
- **Suspend the capability:** `chrome://extensions` → toggle the **CriomOS CDP
  Bridge** extension **off** (greys it out; chrome.debugger can no longer
  attach). Toggle on to re-enable.
- **Remove entirely:** **Remove** the extension on `chrome://extensions`, and/or
  drop it from `home.packages` (move the `chromeCdpBridge`/`attachDriver` lines
  out of `browser-use.nix`) and re-deploy. Reversible either way.

## 6 · Supervised-use discipline (governs USE)

This extension grants control of the psyche's logged-in browser; it is governed
by the same intent as gen 799:

- **7hmc (supervised scout):** the agent scans + reports the UI state and
  possible next steps step by step and **waits for human decisions before any
  consequential action**. `browser-use-attach` drives exactly the ONE tab the
  human clicked — the relay deliberately does not spawn new tabs or touch other
  tabs. Phrase tasks as scan-and-report; the human owns every consequential
  click.
- **s8lq (secrets / human-driven money):** the human does login, 2FA, payment,
  and funding in their own window; the agent never types credentials or reads
  password/card fields. Secrets are gopass-populated env vars, never echoed —
  the bridge token and the Gemma token are sourced at exec time and never enter
  logs, chat, or this report.
- **5g4d (real profile):** the whole point — drive the human's real, logged-in
  Chrome so familiar context + logged-in state are available, **when safe**.
  "When safe" is the supervised discipline above plus the privacy default
  (never read a logged-in page's content into a model or report unless the
  psyche asks for that specific page).
- **Privacy (u275/wvgh/8pgh):** the vision model is the **on-prem Gemma 4**, so
  the page screenshots browser-use feeds its model stay on-prem — never shipped
  to a cloud LLM. This is the reason the extension path is even acceptable on a
  logged-in profile.

## 7 · Still needs the psyche / flagged

1. **The one-time extension load is yours.** Chrome forbids programmatic load of
   an arbitrary unpacked extension on the real profile (§1), so steps §5.1–5.3
   are a human action — by design (the consent gate). I cannot load it on your
   real profile for you. The on-real-profile neutral test (load extension →
   click a neutral tab → `browser-use-attach`) is yours to run once.
2. **VCS boundary (same as gen 799, not blocking):** CriomOS-home `main` was
   committed + pushed to origin (rev `d969788443cb`) because `lojix-run` rebuilds
   from the pushed remote rev — a home deploy cannot reach the profile otherwise,
   and the psyche asked to deploy. This is the path prior home deploys used; it
   crosses the "operators own code-repo main" guideline — flagging so an operator
   can reconcile if a different integration flow is expected.
3. **No host/system authority needed or used** — entirely the user home profile
   (`HomeOnly`). No NixOS rebuild, no other host, no root.
4. **Gemma throughput** (§4): the vision call can exceed browser-use's 75 s step
   timeout under load (browser-use retries up to 6×, then a run can exhaust).
   This is a model-latency property (gen 799 saw the same), not a bridge fault —
   the CDP path is solid. Warming the model before `browser-use-attach` makes the
   first step prompt; worth tracking as a separate model-serving tuning item,
   independent of this bridge.

## Sources

- Deployed `browser-use --help` (0.13.1): `--cdp-url` (http/ws), `--profile`,
  `--connect`, `--mcp`; library `browser/session.py` `connect()` (json/version
  resolution + `Target.setAutoAttach`/`getTargets`/`createTarget`);
  `watchdogs/local_browser_watchdog.py` (`--profile` launches own Chrome with
  `--remote-debugging-port`).
- Chrome 136+ default-profile remote-debugging block:
  https://developer.chrome.com/blog/remote-debugging-port
- Playwright Extension (browser-level Target emulation over chrome.debugger):
  `microsoft/playwright` `packages/extension` `manifest.json`,
  `protocolHandlers.ts` (`Target.setAutoAttach` answered from a tab model),
  `relayConnection.ts`; README (Chrome Web Store / "leverage your default user
  profile").
- Playwright MCP `--extension` does not expose an external CDP url:
  microsoft/playwright-mcp issue #1130.
- Tab-level relays break browser-level Target ops:
  openclaw/openclaw issue #30426 (`Target.attachToBrowserTarget: Not allowed`),
  Yixn/clawhosters-relay (tab-level `ws://…/cdp`).
- Cross-references: reports 61 (supervised DO-token scout + Chrome-136
  constraint), 62 (home-profile browser-use packaging + Gemma wiring, gen 799),
  Spirit 5g4d / 7hmc / s8lq / u275 / wvgh / 8pgh.
```
