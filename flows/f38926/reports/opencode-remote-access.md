# OpenCode Remote Access — Architecture Report

Read on 2026-09-19. Upstream repository `anomalyco/opencode` (the GitHub
org `sst/opencode` redirects there; homepage `opencode.ai`), latest release
**v1.18.31**, published 2026-09-14. Every statement below is tagged
**[W]** witnessed (read in docs or code on that date) or **[I]** inferred.

Illustrator note: each named box below is a box; each numbered arrow is an
arrow with a label (what travels) and a protocol.

---

## Components

**Box 1 — Phone (Android).** A handset on the tailnet. Holds no API keys
for models. [W]

**Box 2 — OpenCode Mobile.** Third-party Android client, package
`cc.agentlabs.opencode`, v0.4.7, MIT, React Native / Expo, by Agent Labs
(`dzianisv/opencode-mobile`). Its README states plainly: *"Not affiliated
with opencode."* Distributed on Google Play, a self-hosted F-Droid repo,
and a signed APK. It is a **thin client** that "speaks the opencode HTTP +
SSE API." No official first-party mobile app exists in opencode's own docs
navigation. [W]

**Box 3 — OpenCode Server.** The process started by `opencode serve`: a
headless HTTP server exposing an OpenAPI 3.1 surface. Default bind
`127.0.0.1`, default port `4096`. Flags: `--port`, `--hostname`, `--mdns`,
`--mdns-domain`, `--cors <origin>` (repeatable). One server holds many
sessions and accepts many concurrent clients. [W]

**Box 4 — TUI / Web client.** Plain `opencode` starts a TUI *and* a server
in one process; `opencode web` starts the server plus a browser UI on
`127.0.0.1` at a random free port. Both are peers of Box 2 against the same
API. `packages/app` is that web UI, a SolidJS app whose e2e harness expects
a backend at `localhost:4096`. [W]

**Box 5 — Session Store.** On-disk state under `~/.local/share/opencode/`:
session data, logs in `log/`, credentials in `auth.json`, and a SQLite
database `opencode.db` (seen in `packages/core/drizzle.config.ts`). Config
lives separately at `~/.config/opencode/opencode.jsonc`. [W]

**Box 6 — Event Bus.** Internal pub/sub inside the server, bridged to SSE.
The SSE handler filters events by instance directory and workspace ID
before emitting. [W]

**Box 7 — Model Provider.** The external LLM API (Anthropic, OpenAI,
Ollama, …). Reached over the AI SDK with Models.dev metadata; 75+
providers. [W]

**Box 8 — Share Service.** `opncd.ai/s/<share-id>`, opt-in, syncs full
conversation history to upstream servers; `"share": "disabled"` turns it
off; enterprise self-hosting is offered. [W]

**Box 9 — Repository / Workspace.** The checkout the server edits: the
tools' actual target. [W]

---

## Data flow: phone → server → model

1. **Connect** — Box 2 → Box 3. A base URL plus a password, entered once
   per connection and held in the Android Keystore via `expo-secure-store`.
   Auth is HTTP Basic: password from `OPENCODE_SERVER_PASSWORD`, username
   `opencode` unless `OPENCODE_SERVER_USERNAME` overrides. Protocol: HTTP(S).
   If the password variable is unset the server is unauthenticated. [W]
2. **Discover** — Box 2 → Box 3. `GET /config`, `GET /config/providers`
   (providers and default models), `GET /sessions`. Carries: session list,
   model catalogue. HTTP/JSON. [W]
3. **Subscribe** — Box 2 → Box 3 → Box 6. An SSE stream. The server docs
   name `GET /event`; the v1 SDK page names `GET /events` — treat the exact
   path as version-dependent. First frame is `server.connected`, then bus
   events, each `{id, type, properties}`. `server.instance.disposed` and
   `global.disposed` are witnessed type names; the message-part, tool-call
   and permission event names were **not** witnessed. Protocol:
   `text/event-stream`, one long-lived GET. [W for shape, unknown for the
   full type list]
4. **Open session** — Box 2 → Box 3. `POST /sessions` (or reuse from the
   list). Carries a new session ID. HTTP/JSON. [W]
5. **Prompt** — Box 2 → Box 3. `POST /sessions/{id}/prompt`. Carries the
   user's text and optional structured-output request. HTTP/JSON. [W]
6. **Inference** — Box 3 → Box 7. The *server* holds the credentials from
   `auth.json` and calls the provider directly; the app "never touches"
   the keys and nothing is proxied through the app vendor's infrastructure.
   Carries: the assembled conversation and tool schemas. HTTPS. [W from the
   mobile README and the auth-storage location; the provider docs do not
   state it in those words — the direct-call claim is **[I]** from where
   credentials live]
7. **Stream back** — Box 7 → Box 3 → Box 6 → arrow 3 → Box 2. Token
   deltas, tool-call records and file diffs ride the already-open SSE
   stream. The phone renders token-by-token streaming and inline diffs. [W]
8. **Permission ask** — Box 3 → Box 2 over SSE; answer returns as
   `POST /sessions/{id}/permissions/{permissionId}`. Carries: the pending
   tool call, then approve/reject. The app exposes this as "tool call
   approval," gated behind biometric unlock. [W]
9. **Act** — Box 3 → Box 9. Tool execution: file reads/writes, shell.
   Server-side endpoints exist for `GET /file/read`, `GET /file/status`,
   `GET /find/text|files|symbols`, and `POST /sessions/{id}/shell`. [W]
10. **Persist** — Box 3 → Box 5. Messages and session metadata written to
    `~/.local/share/opencode/`. Readable again via
    `GET /sessions/{id}/messages`. [W]
11. **Share (optional)** — Box 3 → Box 8. `POST /sessions/{id}/share`
    ( `/share` command) uploads the conversation and returns a public URL;
    `/unshare` revokes. [W]
12. **Drive the TUI (optional)** — any client → Box 3 → Box 4. A whole
    `/tui/*` group: `prompt/append`, `prompt/submit`, `command/execute`,
    `toast/show`, `sessions/open`, `models/open`. A remote client can steer
    a human's terminal UI, not only its own session. [W]

Other endpoint groups witnessed: `GET /health`, `POST /app/log`,
`GET /app/agents`, `GET /projects`, `GET /project/current`, `GET /path`,
`POST /auth/{id}`, and session verbs `children`, `init`, `abort`,
`summarize`, `command`, `revert`, `unrevert`, `PATCH`, `DELETE`. Handler
files in `packages/opencode/src/server/routes/instance/httpapi/handlers/`
additionally name `mcp`, `pty`, `question`, `workspace`, `sync`,
`control-plane`, `experimental`. [W]

---

## Cluster mapping

**Packaging is already half-done, and this was witnessed, not assumed.**
nixpkgs carries `opencode` at version **1.18.16**
(`pkgs/by-name/op/opencode/package.nix`, fetching `anomalyco/opencode`),
alongside `opencode-desktop` and `opencode-claude-auth`. CriomOS already
has `modules/nixos/testing/opencode.nix` defining
`criomos.testing.opencode.enable`, which installs `pkgs.opencode`, and
`checks/opencode-testing-policy/` asserts it is **off by default**.
CriomOS-home pins a flake input `agent-intercom-opencode-src`
(`dataforxyz/agent-intercom-opencode`) and installs it as an OpenCode
plugin. So the decision to run OpenCode is a flag flip plus a service, not
a packaging project. [W, via CriomOS and CriomOS-home working trees]

**Where the server runs.** Prometheus (`prometheus.goldragon.criome`, the
NixBuilder) is the natural host: always-on, holds the checkouts, already
the heavy node. Zeus is the alternative when the work must touch the
workstation's own tree. One `opencode serve` per host per working
directory; the server is directory-scoped (the SSE handler filters by
`instance.directory`). [I]

**How the phone reaches it.** The Criome cluster *is* the tailnet — the
trusted network, with trust carried by the cluster's own trust values.
Bind with `--hostname` to the host's tailnet address (not `0.0.0.0`, and
not `127.0.0.1`), so the listener exists only on the trusted interface.
The phone joins the tailnet and uses `http://<tailnet-ip>:4096`, which is
one of OpenCode Mobile's four documented connection types and needs no
Cloudflare Tunnel or ngrok. `OPENCODE_SERVER_PASSWORD` stays set regardless
— the tailnet is the perimeter, the password is the second lock. [W for the
app's Tailscale support and the bind flags; [I] for the binding choice]

**How it reaches providers.** Arrow 6 leaves Prometheus directly for the
provider API. Credentials land in `~/.local/share/opencode/auth.json` via
`opencode auth login -p <provider>`. Per the `secrets` skill that file is a
persistent import the consumer's contract requires; the GoPass producer
pipes into the login's own stdin prompt, never through argv or the
environment. A local provider (Ollama, llama.cpp) configured with a
`baseURL` would keep arrow 6 inside the cluster entirely. [W for mechanism,
[I] for the GoPass composition]

---

## Flow / Message integration — **PROPOSAL, does not exist**

Nothing below is built or witnessed. It is a shape, offered for the living
to accept or reject.

Today a flow is prompted by injection: Hacky Messenger resolves a live
target and prompts it through Herdr into a terminal pane. An OpenCode
session is a different kind of endpoint — it has a *real API*. The proposal:

- **Box 10 — OpenCode flow endpoint (proposed).** A session ID on a named
  host, registered in Flow Nexus as a resolvable flow identity, exactly as
  a Herdr pane is today.
- **Arrow A (proposed).** Message Nexus / Hacky Messenger → Box 3:
  `POST /sessions/{id}/prompt` carrying the message datom. This replaces
  Herdr injection for this endpoint kind — no keystrokes, no Escape-count
  differences per harness, no composer race.
- **Arrow B (proposed).** Box 3 → Message Nexus over SSE: the stream gives
  what injection never gave — a real *presented* signal when the prompt is
  accepted, and a real *completed* signal when the session goes idle. Per
  the `messaging` skill these stay distinct grades; the HTTP 2xx on arrow A
  is **submitted**, nothing more.
- **Arrow C (proposed).** Permission asks (arrow 8) routed outward as
  HardAbrupt-priority messages to the living, answered back through
  `POST /sessions/{id}/permissions/{permissionId}`.

This also satisfies "observation by subscription" from `Vision/nexus.md`:
SSE is a subscription, not a poll. The tension to surface: OpenCode's event
stream is JSON over HTTP, and a Nexus speaks pure binary signal — an
OpenCode endpoint would be an adapter at the edge of the graph, not a
Nexus. [all I]

---

## Proof-of-concept steps — **do not execute from this report**

1. **Enable the package.** Set `criomos.testing.opencode.enable = true` for
   Prometheus and rebuild. *Witnessed:* `opencode --version` on the host,
   and the `opencode-testing-policy` check still passing for hosts that
   left it off.
2. **Authenticate one provider.** `opencode auth login -p anthropic`,
   feeding the key from GoPass into the prompt's stdin with
   `set -o pipefail`, output suppressed. *Witnessed:* `opencode auth list`
   naming the provider; `opencode models` returning a non-empty catalogue.
   The key itself is never seen by the flow.
3. **First local round trip.** `opencode run -m <provider/model> "say ok"`
   in a scratch directory. *Witnessed:* a model reply, and a new entry
   under `~/.local/share/opencode/`.
4. **Bring up the server.** A systemd **user** service on Prometheus:
   `opencode serve --hostname <tailnet-ip> --port 4096`, with
   `OPENCODE_SERVER_PASSWORD` supplied by `LoadCredential` rather than an
   `Environment=` line. A Herdr pane is the cheaper first shot but does not
   survive a workspace reap — use it only for step 5. *Witnessed:*
   `systemctl --user status`, and `ss -ltnp` showing the listener on the
   tailnet address and **not** on the LAN address.
5. **Probe the API from Zeus.** `curl -u opencode:<pw>
   http://<tailnet-ip>:4096/health`, then `/config/providers`, then hold
   the SSE stream open. *Witnessed:* a health JSON body, a provider list,
   and a `server.connected` first frame. Also confirm an unauthenticated
   `curl` is rejected.
6. **Pair the phone.** Install `cc.agentlabs.opencode` from the F-Droid
   self-hosted repo (preferred over Play; APK is signed and reproducible
   from source). Add a connection of type Tailscale:
   `http://<tailnet-ip>:4096` plus the password. *Witnessed:* the app's
   session list is non-empty and matches step 5's `/sessions`.
7. **First witnessed remote round trip.** From the phone, create a session
   in a throwaway directory and prompt it to write one file with a unique
   marker. *Witnessed, and each separately:* the prompt appears in
   `GET /sessions/{id}/messages` on Prometheus (transported); tokens stream
   in the app (presented); the marker file exists on disk (completed).
8. **Exercise the permission gate.** Prompt something requiring a shell
   tool. *Witnessed:* the approval card on the phone, a reject, and the
   absence of the side effect on disk.
9. **Disable sharing.** Set `"share": "disabled"` in
   `~/.config/opencode/opencode.jsonc` before any real repository is
   touched. *Witnessed:* `/share` refusing.

---

## Unknowns

- The full SSE event-type vocabulary. Only `server.connected`,
  `server.instance.disposed` and `global.disposed` were read. The names for
  message parts, tool-call lifecycle, permission asks and session-status
  transitions were not found in the time available. Not inferred here.
- Whether the canonical stream path is `/event` (server doc) or `/events`
  (SDK doc) at v1.18.31, and whether session paths are `/sessions/…` or
  `/session/…`. The docs disagree; the repo has a v1 and a v2 SDK side by
  side and a `V1_API_MIGRATION.md`.
- The docs site banners "OpenCode v2" while releases read v1.18.31; what v2
  names is unresolved.
- Whether mDNS (`--mdns`) is usable for pairing across a tailnet, or only
  on a broadcast LAN. Almost certainly LAN-only, but unwitnessed.
- Whether nixpkgs 1.18.16 and upstream 1.18.31 differ in the API surface.
- Whether `opencode serve` will serve more than one working directory, or
  needs one process per checkout. The directory filter in the SSE handler
  suggests per-directory instances; not confirmed.
- What the `agent-intercom-opencode` plugin already wires up — it was found
  as a flake input, not read.
- No claim is made that any of this has been run on the cluster. Nothing in
  Part 3 was executed.

---

## Sources

Read 2026-09-19.

Primary, upstream:
- https://opencode.ai/docs/server/ — serve, port 4096, hostname 127.0.0.1, flags, `OPENCODE_SERVER_PASSWORD`, `/doc` OpenAPI 3.1, `GET /event`
- https://opencode.ai/docs/ — docs navigation (no mobile page)
- https://opencode.ai/docs/cli/ — command and flag list
- https://opencode.ai/docs/sdk/ — endpoint↔method map
- https://opencode.ai/docs/providers/ — `auth.json`, `opencode.json`, baseURL, 75+ providers
- https://opencode.ai/docs/share/ — `opncd.ai/s/<id>`, share modes
- https://opencode.ai/docs/web/ — `opencode web`
- https://opencode.ai/docs/network/ — proxy/CA only; no remote-access content
- https://github.com/anomalyco/opencode — release v1.18.31 (2026-09-14), pushed 2026-09-19; files read: `packages/opencode/src/server/routes/instance/httpapi/handlers/` (listing), `.../handlers/event.ts`, `packages/schema/src/server-event.ts`, `packages/core/drizzle.config.ts`, `packages/app/README.md`, `packages/web/src/content/docs/troubleshooting.mdx`

Android client (third party):
- https://github.com/dzianisv/opencode-mobile — README, MIT, v0.4.7, pushed 2026-08-20
- https://play.google.com/store/apps/details?id=cc.agentlabs.opencode
- https://dzianisv.github.io/opencode-mobile/fdroid/repo
- https://github.com/giuliastro/harness-remote — a separate multi-harness control plane, formerly `opencode-remote-android`; not evaluated

Local paths read:
- /home/li/primary/flows/b81560/vision/operational-openCodeAndroidApp.md
- /home/li/primary/flows/b81560/vision/operational-openSourceRemoteAccess.md
- /home/li/primary/flows/b81560/vision/operational-remoteControlResearchReport.md
- /home/li/primary/flows/b81560/vision/operational-messagingSimpleSystem.md
- /home/li/primary/flows/c8d79f/vision/operational-criomeClusterIsTheTailnet.md
- /home/li/primary/Vision/messaging.md, Vision/flowNexus.md, Vision/nexus.md
- /home/li/primary/SKILL_VARIABLES.md
- skills as loaded: spirit, behavior, vocabulary, flow-evidence, messaging, psyche, herdr, secrets
- /git/github.com/LiGoldragon/CriomOS: modules/nixos/testing/opencode.nix, modules/nixos/criomos.nix, flake.nix, checks/opencode-testing-policy/default.nix
- /git/github.com/LiGoldragon/CriomOS-home: flake.nix, packages/agent-intercom/default.nix, packages/pi/default.nix
- /nix/store/31w94yhfpllma9jnlgavjkzsfs548ijx-source/pkgs/by-name/op/opencode/package.nix — version 1.18.16

## Corrections from Mind Astra 0ab019 source review, 2026-09-19

- Upstream v1.18.16 (the nixpkgs version) supports `opencode auth login --provider openai --method "ChatGPT Pro/Plus (browser)"`. The OAuth callback is `localhost:1455/auth/callback`, so the living runs the login on Zeus with Zeus's browser.
- Plural session paths were assumed above; the tagged source uses `/session` and the SSE stream is `/event`. The live `/doc` on the installed server defines the paths the tests use.
- The permission-gate test (step 8) needs an explicit ask rule configured so the tool call is actually held for approval.
- Installed help is verified by Field on Zeus before the install-ready handoff; nothing above is that handoff.
