# ChatGPT desktop missing-image investigation

Captured read-only on 2026-09-08, before any restart or update action in
this flow. The supplied screenshot is a direct user observation: four image
slots in a regular ChatGPT conversation have their rounded light-gray frames
but no pixels. It establishes a rendering/resource-display failure in that
conversation. It does not establish whether the image URLs, their HTTP
responses, the renderer, or an accessibility/display preference caused it.

## Current process and release witness

The running main process is PID 297785, launched as the Nix-packaged
`chatgpt-unwrapped-26.901.31953` Electron application with
`--ozone-platform=wayland`. Its network service (PID 297852) has active TLS
connections while the app is running. The active profile resolves
`chatgpt` to `chatgpt-26.901.31953`; its bundled Chromium reports
`ver=152.0.7977.64` to Crashpad. The associated active `codex` CLI is
`codex-cli 0.153.3`, and `codex-remote-control.service` is active (PID 2217).

Thus the user-facing name is **ChatGPT desktop app**. It contains Codex and
regular-chat surfaces, but the symptom reported here is from its regular-chat
surface; it is not evidence of a separate “Codex desktop” application.

## Failure boundary witnessed today

The current desktop log identifies this instance as
`codex-desktop-75dffa24-...-297785-t0-i1-142833-0.log` and provides the
following relevant observations, without reading conversation contents:

- At 14:35, 14:36, 14:37, and 14:48 UTC, explicit conversation refetches
  completed with `asyncStatus=null`, `currentNodeApplied=true`, and
  `statusAfter=idle`. This confirms that at least the application-side
  conversation fetch/reconciliation completed for those sessions.
- At 15:15 UTC, `thread/start` returned with `errorCode=null`; the `codex_app`
  MCP server later reached `status=ready`. The prior malformed
  `mcp_servers.codex_app` new-thread failure is therefore not present in this
  observed current start.
- A targeted scan of today's two desktop logs found no
  `ERR_*`, `failed to load`, image/media fetch, renderer, GPU, or network
  error that can be connected to the blank image slots. The log does not
  record renderer subresource requests, so that absence does not clear an
  image URL, CDN, content filter, or renderer problem.
- The only current non-conversation desktop error is a bundled-plugin
  marketplace staging write/cleanup failure (`EACCES`) at 15:15. It concerns
  `/home/li/.codex/.tmp/bundled-marketplaces/...`, after the successful thread
  start. No evidence connects it to regular-chat image display.
- Crashpad has historical browser crash records dated 2026-09-02/03, but none
  from today's launch. They show only `ptype=browser`, with no failure reason.
  They do not witness this problem.

The available evidence therefore locates the visible failure after a
conversation can be fetched and rendered far enough to create image frames.
The cause remains unknown. Plausible but unproven causes include failed image
resource delivery (including a blocked `*.oaistatic.com` or
`*.oaiusercontent.com` request), a desktop renderer regression, and stale
app/site state.

## Recalled desktop flows, depth 1

Remembered: `cf0ed9` — depth 1. Its report records the former new-chat
`invalid transport` failure in `mcp_servers.codex_app`; it is a different
boundary from the present regular-chat display symptom. The current log's
successful `thread/start` is a light re-witness that the old failure does not
explain the reported image frames.

Remembered: `ea1e56` — depth 1. It documented the declarative ChatGPT/Codex
integration and a then-active version `26.831.21537`; today's running release
is later (`26.901.31953`). Its report cautioned that private-ASAR wiring and
stale Electron processes can make historical desktop findings non-current.

Remembered: `01a0338f` and `01a03e39` — depth 1. They identify the desktop
surface and Wayland launch override. Current process arguments re-witness the
Wayland override. The psyche record in `01a0338f` says the living was no
longer interested in heavily modifying these applications; this investigation
therefore makes no private-bundle or runtime change.

The `transcript` utility specified by the transcript-search skill was absent
on this host (`command not found`), so reports and flow logs were the
available retained records. No private conversation database, cookies, or
renderer cache was read.

## Official OpenAI guidance

The official OpenAI Help Center says a desktop reload/restart, status check,
and—if the issue persists—browser-console/HAR diagnostics with timestamps are
the supported next diagnostic sequence for missing/blank ChatGPT content. Its
network guidance lists `*.oaistatic.com` and `*.oaiusercontent.com` among
domains that must not be blocked, and recommends upgrading the desktop app
before deeper debugging. These are recommendations, not a diagnosis of this
instance.

## Supplementary runtime and package boundary

The finished `desktop_evidence` subflow witnessed these additional read-only
facts and supplied them to this report:

- The running application exposes no debug listener. A request to
  `localhost:9222/json/version` was refused, and no NetLog, `chrome_debug`,
  DevTools, or renderer diagnostic files were present under the inspected
  application state and cache trees. There is therefore no retained
  per-request renderer trace from which this flow can recover the failed or
  missing image request.
- The desktop logs remained fresh through 17:25 CEST for the main process and
  17:15 CEST for its companion. They contained Electron main-process and app
  server events, but no per-image-resource requests.
- The package uses the vendor's official Debian artifact. Its Nix packaging
  unpacks that artifact, applies the exact ASAR guard
  `isLinux() && process.report` to a single string, supplies launch
  library/path and Wayland wrappers, and fixes Qt shim RPATHs. The inspected
  packaging contains no `webRequest` or protocol interception, URL rewriting,
  or resource filtering.
- The vendor bundle contains `webRequest` and `did-fail-load` code in browser
  or sandbox navigation and renderer-recovery contexts. The subflow did not
  witness interception of regular-chat image resources in those contexts.

These probes narrow the local packaging boundary but do not identify the
cause. The observed blank image frames may still result from resource
delivery, vendor application behavior, renderer state, or another condition
that the available main-process logs do not record.

## Sources

- Supplied screenshot: `/tmp/codex-clipboard-dfIZhx.png` (user observation)
- Current desktop log: `/home/li/.local/state/codex/logs/2026/09/08/codex-desktop-75dffa24-6abb-46f8-94fe-49802693baf3-297785-t0-i1-142833-0.log`
- Companion current desktop log: `/home/li/.local/state/codex/logs/2026/09/08/codex-desktop-75dffa24-6abb-46f8-94fe-49802693baf3-297785-t1-i1-142838-0.log`
- Prior diagnostic: `/home/li/primary/flows/cf0ed9/reports/live-diagnosis.md`
- Prior deployment/state witness: `/home/li/primary/flows/ea1e56/witnesses/current-desktop-codex-state.md`
- Prior deployment audit: `/home/li/primary/flows/ea1e56/reports/desktop-persistent-codex-audit.md`
- Desktop/Wayland history: `/home/li/primary/flows/01a0338f/log.md`; `/home/li/primary/flows/01a03e39/witnesses/chatgptWaylandOverride.md`
- Psyche records searched: `/home/li/primary/flows/01a0338f/vision/tuiAndDesktopVersions.md`; `/home/li/primary/flows/ea1e56/vision/desktopCodexIntegration.md`; `/home/li/primary/flows/01a05d17/vision/fullAccessPermission.md`
- `desktop_evidence` subflow: live debug-endpoint, state/cache, current-log,
  Nix-package, unpacked vendor-ASAR, and interception-context inspection
  (read-only findings relayed to this report)
- Official OpenAI documentation: [Troubleshooting ChatGPT Error Messages](https://help.openai.com/en/articles/7996703); [Network recommendations for ChatGPT errors on web and apps](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
