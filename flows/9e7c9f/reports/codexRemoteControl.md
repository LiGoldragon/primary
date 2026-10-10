# Codex remote control on ouranos

Carried account for flow 9e7c9f. Subject: the persistent Codex server on
ouranos that lets the living remote-control Codex sessions from the phone
Codex app, and the symptom that new flows started from the phone today
(2026-09-12) are no longer listed in the app's remote-control view.

Every claim below is marked **witnessed** (this subflow ran the command and
read the output, at the stated time) or **relayed** (read out of a file
another flow or the living wrote). Nothing was restarted, stopped or
reconfigured; every observation is read-only.

Observation window: 2026-09-12 12:33–12:45 local (UTC-6) on ouranos.

---

## 1. Raw psyche records

Searched `flows/*/vision/`, `flows/*/notion/`, `vision-raw/`, `Vision/` and
`Intent/` under `/home/li/primary`. **Relayed** (files read).

**Distillation status: none of this is distilled.** No `Vision/` or
`Intent/` entry covers Codex remote control, the app-server, the ChatGPT
desktop connection, or `--remote` / `--remote-control`. Every record below
is raw.

The living's words are reproduced verbatim. Surrounding context lines are
the recording flow's, not the living's.

### 1.1 `flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`

Heading: `# remote control all the codex tui sessions I create`
Four dated entries. No `-- psyche` attribution line; the recording flow
frames each as "The living asked / clarified / approved / completed".
Raw.

> ## 2026-08-26T20:19:21+02:00
>
> The living asked for an investigation into a desired Codex interaction:
>
> > Find out if there is a way for me to allow me to remote control all the codex tui sessions I create. Right now, it doesnt allow me to connext to sessions that have an "active writer", but I am able to do it with claude code, by enabling remote control in that session, then my remote messages just appear in the terminal session. I would like to do the same with codex
>
> ## 2026-08-26T20:32:10+02:00
>
> The living clarified that remote control means the Codex app on the phone, not a generic local message-ingress mechanism:
>
> > No, I don't know if you understand what I'm saying. I'm trying to use the remote control feature in the Codex app on my phone, and right now I cannot connect to a session that is essentially running in a terminal somewhere. So I think you misunderstood what I want from your last comment.
>
> ## 2026-08-26T23:09:40+02:00
>
> After being shown the proposed Nix-owned anatomy—an always-running Home Manager app-server service using the single existing Codex derivation, with no standalone installer or updater, every terminal TUI connecting to it, and ChatGPT remaining independent while sharing the derivation—the living approved realization and expanded the deployment scope:
>
> > ok, lets do that. and then also deploy the updated criomos to zeus (in addition to ouranos and/or my profile), and make sure bird's profile is updated on zeus.
>
> ## 2026-08-27T09:36:13+02:00
>
> The living completed the phone-to-terminal proof on Ouranos. After pairing and
> launching a daemon-backed TUI, the sessions appeared on the phone after a short
> discovery delay, and a message sent from the phone arrived in this same live
> terminal conversation:
>
> > ok everything works! we got it!
>
> The living explicitly kept the remaining deployment in scope:
>
> > keep the zeus deploy going
>
> Zeus TestActivation and ActivateNow then completed successfully, including live
> verification of both `li` and Bird's independent services and sockets.

This is the founding record: the want, the client (the phone Codex app), the
approved anatomy, and the living's own confirmation that it worked
end to end on 2026-08-27. Note the living's own phrase there —
"the sessions appeared on the phone **after a short discovery delay**".

### 1.2 `flows/01a047d2/vision/remoteControl.md`

Heading: `# One server for everything`. No dates in text; file mtime
2026-08-28 09:04. Provenance `-- psyche, typed.` on all three entries. Raw.

> ## Both Claude and Codex
>
> > Keep working on the one server for everything solutions, both for Claude and codex
>
> -- psyche, typed.
>
> ## Rooted in primary
>
> > Yes, the code server should be rooted in primary.
>
> -- psyche, typed.
>
> ## The server running for Codex and Claude
>
> Context: clarification of "one server for everything"; this rules out the proposed Nexus/control-plane interpretation.
>
> > I dont want to start a nexus for this; we just need the server running for codex and claude, and the desktop apps using it locally.
>
> -- psyche, typed.

"Rooted in primary" is realized in the live unit as
`WorkingDirectory=/home/li/primary` (witnessed, §3.1).

### 1.3 `flows/01a04336/vision/remoteFlag.md`

Heading: `` # The `--remote` flag ``. Date `## 2026-08-27T14:37:41+02:00`.
Provenance: "this flow, living's message received immediately before this
entry." Raw.

> Context: The living identified `--remote` as the apparent trigger while the repair was being investigated.
>
> > seems to be the  --remote flag that starts it in ~/
> >
> > I want the remote flag to work, but not default me to ~/
> >
> > If it defaults anywhere, it should be ~/primary, but I dont want that hardwired in the OS or home code

### 1.4 `flows/01a04524/vision/claudeRemoteControl.md`

Heading: `# Claude remote control`. No dates in text; file mtime
2026-08-27 16:18. Provenance `-- psyche, typed.` on both. Raw.

> ## Session 01a03f49 has the right design
>
> On the target architecture for Claude remote control:
>
> > session 01a03f49 has the right design for how we want to do this on codex side. try to aim for the same design with claude (see if its possible)
>
> -- psyche, typed.
>
> ## The desktop app can access them
>
> On accepting the supported Claude client boundary:
>
> > but the desktop app can access them then? That would be acceptable.
>
> -- psyche, typed.

The living names 01a03f49 as the canonical design.

### 1.5 `flows/01a05487/notion/rollingCodexServices.md`

Heading: `# define two services`. No dates in text; file mtime
2026-08-31 06:17. Provenance `-- psyche, typed.` on both. Raw **notion** —
a brainstorm, binding nothing.

> > "Maybe we can define two services:
> > 1. One pointing to the old executable so that it doesn't restart
> > 2. The updated one
> >
> > We could use this to sort of roll through. I don't know, it's just a thought. You can see what you think about that."
>
> -- psyche, typed.
>
> > "Is it possible to run multiple servers on the same host? Like you say, just leave the old sessions connected to the former server. On my phone, I can have multiple remotes or multiple servers that I connect to, so I would just add the new one as yet another server. ... we probably will get to a point where there's always going to be a flow going, so we can never actually wait for the motive to finish. ... create this continual new remote server kind of situation where I would have an ever-growing number of servers on my remote clients. Is there a clean way to actually do this?"
>
> -- psyche, typed.

The living's own words here are load-bearing for hypothesis H2 in §3.11:
"On my phone, I can have multiple remotes or multiple servers that I connect
to". The live enrollment table holds **two** servers both named `ouranos`
(witnessed, §3.5).

### 1.6 `flows/01a05487/vision/flowMovesBetweenGenerations.md`

Heading: `# Flow can move to the new generation between turns`. No date in
text; file mtime 2026-08-31 06:59. No provenance line. Raw.

> > "You're saying the Flow can move to the new generation between turns. Is that even possible? If so, then yeah, I'm all for it."
>
> Context: conditional approval; whether Codex can preserve the Flow across a server-generation boundary must be established first.

### 1.7 `flows/01a052b6/vision/reportFeedback.md`

Heading `# Report feedback`, subsection
`## Mobile, accumulated comments returned to the originating flow`.
No date in text; file mtime 2026-08-31 08:07. Provenance
`-- psyche, typed.` Raw.

> Context: The living clarified the feedback contract sought from Codex visual reports by describing the established Claude workflow.
>
> > "I want to be able to put comments from my phone. Essentially, I'm remote accessing Codex, which is running on my machine here, and then Codex would create a visual report. There would be a link I could open on my phone where I could actually put in all the comments one by one. I would be able to put in comments without triggering the session every time I put a comment. I could potentially put multiple comments and then go back to the session and tell it that I commented on the report. It would be able to see all the comments and what they refer to. ... I'm describing the flow that I have developed with Claude, and that's the kind of flow I'm looking to get with Codex."

### 1.8 `flows/01a05d17/vision/fullAccessPermission.md`

Heading: `# full access permission`. No date in text; file mtime
2026-09-01 07:33. Provenance `-- psyche, typed.` Raw.

> Context: desired behavior for Bird's ChatGPT Desktop when it creates a Codex session.
>
> > her chatgpt desktop app doesnt start a new codex session with "full access" permission, as I want it to be

### 1.9 `flows/ea1e56/vision/desktopCodexIntegration.md`

Heading: `# I am no longer interested in heavily modifying those applications
to achieve better functionality`. Date `## 2026-09-02`. Provenance
`-- psyche, typed.` Raw.

> Context: The living asked the flow to inventory the local implementations and hacks used to connect the desktop application to the persistent Codex server so their removal can be considered.
>
> > I am no longer interested in heavily modifying those applications to achieve better functionality.

This is the record behind the later removal work (§2).

### 1.10 `flows/58a86d/vision/vscodium.md`

Heading: `# VSCodium`. Date
`## 2026-09-05 — obsolete; the Claude and ChatGPT desktop apps replace it`.
Provenance `-- psyche, typed.` Raw. Marginal to remote control; it fixes the
ChatGPT desktop app as a standing tool.

> Context: the flow had reported that the deployment's activation died on the VSCodium managed-extension hook and had asked the living, as steward, to authorize the reconciliation.
>
> > let's get rid of vscodium; we now use the claude and chatgpt desktop apps instead. vscodium is obsolete.

### 1.11 `flows/01a0437d/vision/codexAndClaude.md`

Heading: `# only codex and claude`. Dates
`## 2026-08-27T16:25:28+02:00`, `## 2026-08-27T17:53:41+02:00`. No
provenance line. Raw. Marginal — packaging ownership of the shared
derivation, which the 01a03f49 anatomy depends on.

> ## 2026-08-27T16:25:28+02:00
>
> Context: Asked whether the CriomOS-owned package collection should cover only Codex and Claude or replace `llm-agents` generally.
>
> > yes, only codex and claude.
>
> ## 2026-08-27T17:53:41+02:00
>
> Context: CriomOS-home was proposed as owner of the canonical Codex and Claude engine packages and the derived ChatGPT and Claude Desktop packages, including their source pins, update paths, single-stack adaptations, and contract checks; the direct `llm-agents` flake dependency would disappear after every consumer was migrated. Asked whether owning the desktop package expressions too was the intended boundary.
>
> > great. approved.

### 1.12 `flows/01a038be/vision/archive-x11.md`

Heading: `# take x11 out of the equation`. Date
`## 2026-08-26T13:54:46+02:00`. No provenance line. Raw. Marginal.

> Context: The official ChatGPT/Codex Linux app froze during use while running through X11 under a Wayland session, with contemporaneous Intel GPU hangs.
>
> > lets take x11 out of the equation first. we want to be able to take out x11 from criomos eventually

### 1.13 `flows/e71fa5/vision/private-data-separation.md`

Heading `# Private data separation`, subsection
`## Everything public for now, working toward a separation of private data`.
No date in text; file mtime 2026-09-09 16:35. Provenance `-- psyche, STT.`
Raw. Marginal — reached only because flow f7941a pushed a log carrying the
living's ChatGPT account id, the same account id that appears in the live
enrollment rows (§3.5).

> Context: asked whether the primary remote is public, after f7941a pushed a log carrying the living's ChatGPT account id.
>
> > "Yeah, we're just doing everything public for now. We're gonna work towards creating a separation of private data. And we've already touched on that"

### 1.14 Chronology of the raw records

| When | Record |
|---|---|
| 2026-08-26 13:54 | 1.12 take x11 out of the equation |
| 2026-08-26 20:19 → 08-27 09:36 | **1.1 remote control all the codex tui sessions I create** (want → design → working) |
| 2026-08-27 14:37 | 1.3 the `--remote` flag |
| 2026-08-27 16:25 / 17:53 | 1.11 only codex and claude |
| ~2026-08-27 16:18 | 1.4 Claude remote control (01a03f49 has the right design) |
| ~2026-08-28 09:04 | **1.2 One server for everything** (no Nexus; rooted in primary) |
| ~2026-08-31 06:17 | **1.5 rolling Codex services** (notion; multiple servers on the phone) |
| ~2026-08-31 06:59 | 1.6 Flow can move between generations |
| ~2026-08-31 08:07 | 1.7 report feedback from the phone |
| ~2026-09-01 07:33 | 1.8 full access permission |
| 2026-09-02 | **1.9 no longer interested in heavily modifying those applications** |
| 2026-09-05 | 1.10 VSCodium obsolete |
| ~2026-09-09 | 1.13 private data separation |

---

## 2. Flow accounts

All of §2 is **relayed** — read out of `log.md`, `reports/` and `witnesses/`
in `/home/li/primary/flows/`. Where a flow itself marked a claim as
witnessed (it ran a command and recorded the output), that is noted as
**[flow-W]**; where a flow relayed or planned, **[flow-R]** / **[flow-P]**.
A flow's witness is not this subflow's witness.

### 2.1 The design approved in 01a03f49

The blocking constraint that forced the shape —
`flows/01a03f49/log.md:16` **[flow-W** from installed Codex 0.149.1 source
and CLI help**]**:

> Settled from installed Codex 0.149.1 source and CLI help: an ordinary
> already-running TUI cannot be attached or converted because its embedded
> app-server holds the writer lock. The intended shared topology is to start
> the remote-control-enabled managed daemon first, pair it to the phone, and
> run the terminal TUI as a client of that daemon. The phone and TUI then
> share the daemon's single writer.

Restated in `flows/01a03f49/reports/codexPhoneRemoteControl.md:43-44`:

> A plain TUI launched before the daemon uses an embedded app-server. No
> attach, rebind, or conversion command exists. Starting Remote Control
> afterward makes another process try to load the thread, producing the
> intentional `already has an active writer` rejection.

The topology it recorded (`:7-11`):

```text
Codex phone ── OpenAI Remote Control relay ── managed app-server daemon ── thread
                                                   │
                                                   └── terminal TUI client
```

The approval — `flows/01a03f49/log.md:18`:

> The living approved a corrected Nix-native realization: Home Manager owns
> a direct `codex app-server --remote-control --listen unix://` user service
> using the one existing Codex derivation. The standalone installer, managed
> mutable path, and updater are excluded. Deployment scope includes Zeus and
> bird's Zeus profile in addition to the relevant Ouranos/li state.

Why the vendor's own recipe was refused —
`reports/codexPhoneRemoteControl.md:65`:

> Further source inspection established that `codex remote-control start` is
> not acceptable for this environment: it requires
> `$CODEX_HOME/packages/standalone/current/codex` and bootstraps an
> installer-owned updater.

The anatomy, as the flows record it:

| Element | Value |
|---|---|
| Unit | `codex-remote-control.service`, Home Manager per-user systemd user service, `Description=Codex Remote Control app-server` |
| Launch | `codex app-server --remote-control --listen unix://` |
| Policy | `Restart=always`, `RestartSec=2s`, `UMask=0077`, `WorkingDirectory=<home>/primary`, `WantedBy=default.target` |
| Socket | `~/.codex/app-server-control/app-server-control.sock`, mode `0600` |
| Owner | Home Manager, one per user, each with independent `CODEX_HOME`, socket, auth and pairing state |
| Purpose | one persistent thread owner shared by the phone (via OpenAI's relay) and by terminal TUIs attaching as thin clients |
| TUI routing, **as approved** | "The normal interactive Codex entrypoint routes fresh, resume, fork, and agents TUIs to `unix://`; noninteractive/admin commands, ChatGPT's `CODEX_CLI_PATH`, and named recovery commands retain the raw pinned executable." (`codexPhoneRemoteControl.md:71`) |

Nix module paths, as the flows cite them (CriomOS-home unless stated):

- `modules/home/profiles/min/agent-intercom.nix:153-169` — **declares the
  unit** (`flows/ea1e56/reports/source-inventory.md:29`;
  `flows/564f55/reports/codexLaunch.md:82` cites line 158) — the same module
  this subflow witnessed as the authoring source in §3.1
- `owned-agents/codex/tui.nix:55-140` — the TUI routing wrapper: "rejects
  non-`unix://` remotes, injects caller PWD plus full-access defaults,
  routes ordinary TUI/resume/fork to `--remote unix://`, permits only
  observational `app-server daemon version`, and blocks app-server
  lifecycle/`remote-control`"
- `owned-agents/codex/remote.nix` — declares `codex-remote` =
  `codex --remote unix:// "$@"` (`codexLaunch.md:85-91` **[flow-W]**)
- `owned-agents/codex/default.nix:37-85` + `hashes.json` — the one canonical
  Codex derivation
- `checks/codex-remote-control/default.nix:93-166` — unit shape and wrapper
  routing contract; `checks/codex-remote-control-vm/default.nix:36-85` — a
  NixOS VM proving service start, `0600` socket, restart, re-initialize
- CriomOS `modules/nixos/userHomes.nix:33-49` imports the Home module;
  CriomOS `checks/lojix-ownership/default.nix` asserts the generated unit's
  `WorkingDirectory`/`Restart`/`UMask`

Landing: CriomOS-home `ba0de9f84130c47a927a04723db2cb6f33b6b103`, CriomOS
`2fb323b0f2c7d0a06a28cc2c757c46799e4a9e0f`; Ouranos deployment **72**; Zeus
**73** Evaluate / **74** Realize / **75** TestActivation / **76** ActivateNow,
all Completed/Succeeded, independently for `li` and Bird. Codex 0.149.1.
**[flow-W]**

The live phone proof — `reports/codexPhoneRemoteControl.md:50-55`
(**[flow-W]** for the machine side; the phone-side observation is the
living's, relayed):

> The complete topology was live-tested on Ouranos with the living's phone.
> The Nix-owned service was active, the living paired the phone with
> `codex remote-control pair`, and a TUI launched with `codex --remote unix://`
> remained open in the terminal. After a short discovery delay, the phone
> showed the daemon-backed sessions. A message sent from the phone appeared
> in the same live terminal conversation.

With the caveat the flow attached (`:57`): "The path remains experimental in
Codex 0.149.1."

A chronology note: flow `01a038be` (2026-08-26, hours before 01a03f49)
already reports "the Codex remote-control and bridge services are active".
That is a **different, now-deleted lineage** — the unofficial
`ilysenko/codex-desktop-linux` "Computer Use / remote mobile control"
wiring, removed by Home commit `2fb9f089fafb` when the official signed
OpenAI ChatGPT Linux package was adopted, because "the official Linux
preview does not support it"
(`flows/01a038be/reports/officialChatgptCorrectionDeployment.md:9-13`;
`flows/ea1e56/reports/desktop-persistent-codex-audit.md:41-42`). The
vendor-native remote/mobile control was *lost* in that swap; 01a03f49's
Nix-owned owner is what refilled the gap.

### 2.2 What was later removed, and what was kept

**4ad49f (2026-09-02) — the ChatGPT Desktop stock-boundary rollback.**
Working instruction, `flows/4ad49f/log.md:3`:

> restore ChatGPT Desktop to a stock and supportable application boundary,
> retain the independent persistent Codex owner for terminal sessions and
> phone Remote Control, remove Desktop-specific attempts to force that
> owner, prove stock launch/new-chat/resume behavior, and deploy through the
> immutable CriomOS-home → CriomOS → Lojix boundary.

Why: the living's words, gathered in
`flows/ea1e56/reports/desktop-persistent-codex-audit.md:15-24` — the record
reproduced verbatim at 1.9 above, plus (from flow cf0ed9) "The defect is on
openai for lacking the feature I want". And the architectural verdict that
made the Desktop crossing unsalvageable,
`flows/01a047d2/log.md:68` **[flow-W** from the installed ASAR and Codex
0.150.1 source**]**:

> Therefore the observed Desktop build cannot both preserve its native
> dynamic app-tools behavior and attach to the existing process-global owner
> through a simple gate. Correct options are: allow Desktop its private
> native Core while retaining the shared owner for TUI/phone; accept a
> reduced Desktop without app tools; or design an authenticated
> per-connection/per-thread bridge that injects and isolates dynamic MCP
> configuration. This is now an explicit psyche architecture decision; do
> not widen the matcher without it.

4ad49f took the first option.

**Deleted** (`flows/4ad49f/witnesses/home-rollback-review.md:45-55`,
**[flow-W]** by immutable `jj` inspection of Home revision
`c025a681df31d55b9035364c01e2f6c8d7b59c1c` against baseline `90a12633cc60`):
the ASAR patcher `owned-agents/chatgpt/patch-asar.py` and its tracked
`__pycache__` bytecode; the four patch regions `COPY_PLUGINS_WRITABLE`,
`NO_APP_TOOLS_CONFIG_OVERRIDE`, `SHARED_APP_SERVER`
(`getConfigOverrides` → `()=>[]`), `SKIP_PROCESS_REPORT` (1 355 differing
bytes against the independently extracted vendor archive,
`witnesses/pristine-stock-boundary.md:85-87`); the env forcing
`CODEX_APP_SERVER_USE_LOCAL_DAEMON=1` and the unsets of `CODEX_CLI_PATH`,
`CODEX_APP_SERVER_FORCE_CLI`, `CODEX_APP_SERVER_CLI_COMMAND`,
`CODEX_APP_TOOLS_PIPE_PATH`; and the replacement of vendor
`resources/codex` with the canonical Nix Codex symlink. Earlier lineages
were already gone: the Agent Intercom `coi-shared-app-server.patch` /
`sharedAppServerSocket` / `programs.codexDesktopLinux` /
`agent-intercom-codex-bridge` set at `2fb9f089fafb`, and the
`owned-agents/codex/desktop-gate.nix` proxy gate at `64d4784969e8`.

**Kept** (`witnesses/home-rollback-review.md:81-91`, **[flow-W]** by SHA-256
source-byte comparison):

> `owned-agents/codex/tui.nix`, `owned-agents/codex/default.nix`,
> `modules/home/profiles/min/codex-permission-defaults.nix`,
> `modules/home/vscodium/vscodium/default.nix`, and
> `packages/agent-intercom/default.nix` have identical SHA-256 source bytes
> at baseline and c025.
> In `modules/home/profiles/min/agent-intercom.nix`, the functional regions
> beginning at the Agent Intercom package, MCP declaration, and
> `codex-remote-control` service are byte-identical; only the ChatGPT factory
> argument and adjacent explanatory comment changed. The service still uses
> the canonical Codex package, Unix app-server, `UMask=0077`, and restart
> policy.

The audit that scoped it classified the owner explicitly —
`flows/ea1e56/reports/desktop-persistent-codex-audit.md:47-51`:

> The user environment declares a per-user `codex-remote-control.service`
> running the canonical Codex package as a long-running app server on its
> private control socket, rooted in the primary workspace. Daemon-backed
> terminal sessions and phone Remote Control use it independently of ChatGPT
> Desktop.
> Classification: **independent foundation. Retain unless the living
> separately abandons persistent terminal/phone Remote Control.**

The continuity gate, and the strongest evidence in the corpus that the owner
survived — `flows/4ad49f/witnesses/live-stock-desktop.md:74-110,149-157`
**[flow-W]**:

> each `codex-remote-control.service` symlink resolves to exactly the same
> immutable unit file:
> `/nix/store/wz1lzdy0szhpwis2cjn68ak8dw4q7bhx-codex-remote-control.service/codex-remote-control.service`
> Candidate/current/active unit SHA-256 is
> `720c73a7a11b170e770374cd2580728e2af0adbebe44ef52769f47bc728c034e`. Both
> byte comparisons exited `0` … This exact unit identity is the safety gate:
> it rules out a unit-driven owner replacement or restart by this activation.
> After activation, `codex-remote-control.service` remained `active/running`;
> `MainPID` and `ExecMainPID` remained `1664375`, equal to the pre-activation
> PID. … No listener exists on TCP port 18080.

Deployment chain: CriomOS `663fefb70f9962c6751fd0d87b07f8cfef01ef9e` pinning
Home `c025a681df31…`; Lojix **146** Realize Succeeded, **147** rejected
`FlakeReferenceMalformed`, **148** ActivateNow Completed/Succeeded.

What 4ad49f did **not** prove (`log.md:9`):

> a fresh stock Electron process tree launched successfully for a bounded
> interval, but no safe installed Wayland/AT-SPI/Desktop-control surface can
> perform a new chat and same-thread resume without private UI traversal or
> input injection. Those two authenticated GUI actions remain unverified
> rather than inferred from launch or initialization.

**8a5caa (2026-09-05) — the second removal, and the one that matters most
for the present symptom.** The ordinary `codex` wrapper stopped attaching.
`flows/8a5caa/reports/codex-implementation.md:1-8` **[flow-W]**:

> The Home implementation changes normal `codex` back to the canonical
> pinned upstream package. `codex-remote` is a separately named launcher
> that executes the upstream CLI with only `--remote unix://` before its
> untouched arguments. It has no argument scanner, fallback route,
> working-directory injection, or permission flags. The persistent
> `codex-remote-control` service remains the owner of the app-server.
> The provider and its consumers remove `direct-codex` and `codex-raw`.

The living's word, `flows/8a5caa/log.md:17-21`, on a proposed
`codex-app-server-proxy`: "this isnt useful to me. implement the rest."

Landed: CriomOS-home `c40ff0cde736a4b092b7c713571afce40361a395`, CriomOS
`a66c93816c9a0bbd0660f979b26bb9c552b0e2b0`; Lojix **202** Realize and
**204** ActivateNow, both Succeeded, with the owner unchanged on PID
4096266. This is why the plain `codex` on PATH today carries no `--remote`
(witnessed, §3.7) — that is the deployed design, not a defect.

**db267d (2026-09-06) — the third removal: the Claude side, entirely.**
Psyche instruction, `flows/db267d/log.md:16`: "Take the cloud remote server
out of CriomOS. Reintroducing it is a later conversation."
`modules/home/profiles/min/claude-remote-control.nix`,
`checks/claude-remote-control/`, the module import, the flake check wiring
and the prose were deleted (CriomOS-home `1ae5da86`, CriomOS `a48f9cb8`).
And the explicit non-touch,
`flows/db267d/witnesses/claude-remote-control-removal.md:31-33` **[flow-W]**:

> `codex-remote-control` is a different module
> (`modules/home/profiles/min/agent-intercom.nix`) declaring a different unit
> from a different package. The two share no code. **Untouched.**

### 2.3 Chronology of unit / socket / version / wrapper

| Date | Flow | Change | Deployment |
|---|---|---|---|
| 2026-08-25 | 01a0338f | unofficial `codex-desktop-computer-use-ui-remote-mobile-control`; profile CLI 0.149.0 vs running app-server 0.148.0 (first skew warning) | — |
| 2026-08-26 | 01a038be | official signed ChatGPT `26.818.61809`; the unofficial remote/mobile-control wiring is removed | 61–63 |
| 2026-08-26/27 | **01a03f49** | **the approved unit lands**, Codex **0.149.1** | 72 (Ouranos), 73–76 (Zeus) |
| 2026-08-27 | 01a04336 | wrapper repair: remote mode sent no cwd so the app-server used its service cwd `/home/li`; wrapper now injects `--cd "$PWD"` — the realization of the living's 1.3 | 78 |
| 2026-08-28 | 674a4dab | audit finds `owned-agents/codex/desktop-gate.nix` was **agent-initiated, never asked for** | — |
| 2026-08-28 | 01a047d2 | Codex **0.150.1**; old PID needed `SIGKILL` after stop timeout | 83 failed at Eval, 84 |
| 2026-08-31 | 01a05833 | Codex **0.151.0** on Zeus; the literal `/home/li/primary` `WorkingDirectory` gave Bird `status 200/CHDIR`; repaired | 106–122 |
| 2026-09-01 | 01a05c80 | `resources/codex` restored for the vendor preflight; owner PID 4013983 unchanged; the living confirmed "chatgpt works now" | 123, 124 |
| 2026-09-02 | d30eb1 | Home activation stopped the 0.151.0 owner 18:06:47, `SIGKILL` 18:08:18, started **0.152.1** | — |
| 2026-09-02 | **4ad49f** | stock Desktop boundary; unit byte-identical `720c73a7…`; **PID 1664375 unchanged** | 146, 147 rejected, 148 |
| 2026-09-04 | 5d0c7b | live-update-without-interruption investigation — **rejected, self-declared invalid** | — |
| 2026-09-05 | 4a8046 | **drift witnessed**: unit loaded 0.153.3 while the live process still ran the 0.153.2 binary; Codex update then explicitly deferred by the living | 198–201 |
| 2026-09-05 | **8a5caa** | ordinary `codex` reverted to plain upstream; only `codex-remote` attaches; `direct-codex`/`codex-raw` removed | 202, 204 |
| 2026-09-06 | db267d | `claude-remote-control` deleted whole; Codex owner untouched | — |
| 2026-09-08 | 985ba2 | Codex **0.153.3 → 0.153.4**; old PID 2217 stopped 17:44:01, `SIGKILL`, new PID 326495 at 17:45:32 | 234, 235 |
| 2026-09-09 | 564f55 | owner re-witnessed at 0.153.4, PID 326495, socket `srw------- Sep 8 17:45` | — |
| 2026-09-09/10 | f7941a | `codex-desktop` launcher authored on top of `codex-remote` ("it does not create another app-server"); **deployment 240 failed** at `CopyClosure`/`BuilderUnreachable` — `codex-desktop` **remains absent from the live profile** | 239, 240 failed |
| 2026-09-11 | f6db8d | owner classed "Doing real work … live client, traffic through 19:31 today" | — |
| **2026-09-12** | **this flow** | witnessed: 0.153.4, PID 2087, up since 09-10 13:30 (see §3) | — |

Version line: 0.148.0 → 0.149.0 → **0.149.1** (unit created) → 0.150.1 →
0.151.0 → 0.152.1 → 0.153.2 → 0.153.3 → **0.153.4** (current). The socket
path and mode never changed. The wrapper was created in 01a03f49, gained
`--cd "$PWD"` in 01a04336, and was **retired in 8a5caa**.

### 2.4 Unresolved

**Replacing the owner kills attached work, and no accepted design exists.**
Witnessed twice with `SIGKILL` after the stop timeout: 2026-09-02
18:06:47→18:08:18 (`flows/d30eb1/log.md:15` — "restored conversation context
is not process continuity") and 2026-09-08 17:44:01→17:45:32
(`flows/985ba2/reports/application-updates.md:63-67` — "the flow's likely
cause of the conversation interruption at activation"). The living ruled out
the only architecture proposed — `flows/5d0c7b/log.md:18-23`:

> The living corrected the governing requirement: Codex flows are always
> running, so the architecture cannot rely on a global no-running-flow point.
> The proposed architecture therefore does not satisfy the requirement.

and that flow then disowned itself (`:37-43`): "This Flow is a catastrophic
behavioral failure. … Its technical findings must not be treated as an
accepted design or as authorization for implementation or deployment."

The design boundary that remains, `flows/01a05487/log.md:33-34` **[flow-W]**:

> after a clean turn and after the old server releases the thread-writer
> lock, a fresh server can `initialize` and cold `thread/resume` the same
> durable thread ID from its rollout. Under the defined vocabulary this is a
> successor Flow preserving thread continuity, not the same bounded
> Flow/process. Current clients disconnect fatally and do not migrate
> transparently.

and the living's open question (`:28-30`): "find the clean end-shape for
continually introducing new Codex server generations when some flows may
always remain active, without accumulating an ever-growing set of remote
entries on phone clients" — the same worry as the notion at 1.5.

**Phone invisibility has happened before and was never explained.**
`flows/01a047d2/log.md:18` **[flow-W** for the timestamps, cause
unknown**]**:

> The Codex service was explicitly stopped and started at 04:04:53–04:04:54,
> but the requester and its relationship to temporary phone invisibility
> remain unknown.

And `flows/01a047d2/log.md:5` records that 01a03f49 "did not establish …
phone enrollment surviving restart." That gap is still open.

**Pairing validity has never been re-witnessed.**
`flows/564f55/reports/codexLaunch.md:108-116,447-451`, which marks its own
boundary:

> **Not witnessed by me** — whether that enrollment is still valid today is
> unknown, and `remote control requires ChatGPT authentication; API key auth
> is not supported` is a string in the binary (witnessed).
> **Pairing is a human step.** If the ChatGPT-side enrollment has lapsed,
> the living runs `codex remote-control pair --json` and enters the code in
> the ChatGPT app. Whether it is currently enrolled was **not witnessed** —
> checking it means talking to the daemon.

Both delegated sweeps report **no phone-side or pairing witness anywhere in
the corpus after 2026-09-02**. This subflow adds the first since: the
enrollment rows of §3.5 and the `codex_chatgpt_android_remote` connection of
§3.9. Enrollment exists and the phone did connect today.

**Thread naming and root-thread identification were deferred by name.**
`flows/01a05826/log.md:19` **[flow-W** from Codex source reading, not a live
protocol trace**]**:

> phone remote control and local TUI converge in the shared Codex app-server
> at `thread/start` → `ThreadProcessor::thread_start` →
> `ThreadManager::start_thread`. The app-server can distinguish a root user
> session by `thread_source=user` with no `parent_thread_id`; subflows use
> `thread_source=subagent` and carry a parent. Codex core `SessionStart`
> hooks run before the first model request, but their output schema has no
> thread-name field and is not routed to `thread/name/set`, so an existing
> hook cannot perform the rename.

`:21`: "Deferred possible future work: automatically assign the unique
six-character flow-directory ID as the Codex root session name inside the
common app-server root-thread creation lifecycle. **This is not current
work.**" — This is the same `thread_source` / `name` machinery this subflow
read directly in §3.8, and it is why today's two threads carry
`name = NULL`.

**Standing warnings from the corpus**, all still in force:

1. **Never run `codex remote-control start` on this host** — it demands
   `$CODEX_HOME/packages/standalone/current/codex` and bootstraps an
   installer-owned updater that fights Nix
   (`01a03f49/reports/codexPhoneRemoteControl.md:58-61`, re-asserted
   `564f55/reports/codexLaunch.md:93-98`).
2. **A session must be `--remote` from its first invocation.**
   `564f55/reports/codexLaunch.md:100-106`: "the session **must be started
   with `--remote` from the very first invocation**. A plain `codex` in a
   ghostty window can never be made remote afterward."
3. **Do not restart or activate over the owner from a flow attached to it**
   (`01a047d2/log.md:41`; `flows/01a048a6/annotations.md:3`).
4. **`WorkingDirectory` must not be a hardwired `/home/li/primary` literal**
   — it broke Bird's unit with `status 200/CHDIR` (`01a05833/log.md:38`).
5. **Version equality does not prove no restart** — `4a8046/log.md:112`:
   "integration must compare candidate/current Codex unit bytes … version
   equality alone does not prove there will be no service restart."
6. **Config reaches the owner only at start** — `flows/be2534/log.md:7`: a
   model/config change needs an owner restart, which costs the attached
   sessions.
7. **Green Nix checks did not catch the real failures** —
   `ea1e56/reports/desktop-persistent-codex-audit.md:97`: the checks
   "exercised and reported passing package shapes and bare Codex behavior
   but did not exercise Desktop Composer's actual generated configuration,
   allowing green builds while the reported real new-chat path remained
   broken."
8. `CODEX_REMOTE_CONTROL_DAEMON_AUTOSTART_DISABLED=1` appears in agent
   shells but "is absent from the installed Codex source and binary. Codex
   itself does not recognize it"
   (`01a03f49/reports/codexPhoneRemoteControl.md:46`) — later established as
   a caller/harness setting absent from the service environment, so **not**
   evidence the service is disabled. This subflow confirms it: the live unit
   carries an empty `Environment=` (§3.4).

Adjacent and open: `codex-desktop` is not installed (deployment 240 failed);
ChatGPT Desktop's `SIGILL` window-then-exit is undiagnosed (bead `home-273`);
`checks/lojix-ownership` is deliberately red and "left for the psyche";
Lojix discards activation stderr (bead `primary-cod`); `cci` fails to start.

**Provenance caution carried forward.** One delegated sweep was flagged by
the harness as instruction-shaped because it quotes the literal CLI flag
string `--permission-mode bypassPermissions` out of
`flows/01a057e7/log.md` — the recorded `ExecStart` of the now-deleted
**Claude** owner unit. It is quoted evidence, not a directive, and was
treated as data.

---

## 3. Live state, witnessed now

All of §3 is **witnessed** on ouranos at 2026-09-12 12:33–12:45 local unless
marked otherwise.

### 3.1 The unit definition

`systemctl --user cat codex-remote-control.service`:

```
# /home/li/.config/systemd/user/codex-remote-control.service -> /nix/store/7c7hvcxhzkh7a08isr1i6hzvagivd6xs-codex-remote-control.service/codex-remote-control.service
[Install]
WantedBy=default.target

[Service]
ExecStart=/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex app-server --remote-control --listen unix://
Restart=always
RestartSec=2s
UMask=0077
WorkingDirectory=/home/li/primary

[Unit]
Description=Codex Remote Control app-server
```

It is a Nix-owned Home Manager user unit, symlinked from the store — the
anatomy the living approved in 1.1. `WorkingDirectory=/home/li/primary`
realizes 1.2 ("the code server should be rooted in primary").

**Relayed**, for the authoring source only: the module that generates this
unit is `modules/home/profiles/min/agent-intercom.nix` in CriomOS-home, e.g.
`/home/li/wt/github.com/LiGoldragon/CriomOS-home-wispr-overlay/modules/home/profiles/min/agent-intercom.nix`:

```nix
    systemd.user.services.codex-remote-control = {
      Unit.Description = "Codex Remote Control app-server";
      Service = {
        ExecStart = "${codexCliPackage}/bin/codex app-server --remote-control --listen unix://";
        UMask = "0077";
        Restart = "always";
        RestartSec = "2s";
      };
      Install.WantedBy = [ "default.target" ];
    };
```

with the comment above it:

```nix
    # Codex's app-server is the single owner of every normal terminal TUI
    # session.  Its default Unix socket is local to the user, while remote
    # control reaches the phone through Codex's authenticated relay.
```

That worktree copy has no `WorkingDirectory`, so it is **not** the revision
that produced the live store path. Treat the live unit text as authoritative
and the worktree text as the shape only.

### 3.2 Uptime, version, resources

`systemctl --user status`:

- `Active: active (running) since Thu 2026-09-10 13:30:08 CST; 1 day 23h ago`
- `Main PID: 2087`, `Tasks: 238`
- `Memory: 9.6G (peak: 18G, swap: 255.7M, swap peak: 1.3G)`, `CPU: 57min 42.926s`
- Invocation `60b0716d7afd42549ab3f5366d6d6449`

Codex version: the store path is `codex-0.153.4`, and `codex --version`
reports `codex-cli 0.153.4`. **The service has not restarted today.** The
unit lifecycle lines in the journal end at
`2026-09-10T13:30:08-06:00 ouranos systemd[2067]: Started Codex Remote Control app-server.`
The preceding stop was `2026-09-10T03:41:23-06:00 ... Stopped`.

Children of the unit (from the status cgroup listing): one
`codex-code-mode-host`, and seven pairs of
`agent-intercom-0.10.0/.../codex-server.mjs` + `chatgpt-unwrapped-26.901.31953/.../node_repl`
MCP servers, the newest started 12:23:36. These are MCP servers the
app-server spawned per thread, not separate app-servers.

### 3.3 Socket path

`ss -xlp` shows exactly one listening app-server socket:

```
u_str LISTEN 0 4096 /home/li/.codex/app-server-control/app-server-control.sock 22489 * 0 users:((".codex-wrapped",pid=2087,fd=28))
```

So `--listen unix://` with no path resolves to
`/home/li/.codex/app-server-control/app-server-control.sock` (mode `srw-------`,
created 2026-09-10 13:30). There is no second app-server socket on the
machine. `~/.codex/app-server-daemon/` holds only stale zero-byte lock files
from 2026-08-26/27, and `~/.codex/ipc/ipc.sock` is from 2026-09-08 — both
残 leftovers, not in use by pid 2087.

### 3.4 Journal for today

`journalctl --user -u codex-remote-control --since today` returns **74 lines,
all of them `ERROR` from the model's tool layer** — `apply_patch verification
failed`, `exec_command failed: CreateProcess ... Rejected`,
`collab spawn failed: agent thread limit reached`,
`failed to refresh available models: timeout waiting for child process to exit`,
and `rmcp ... fail to delete session`. There is **no** thread-creation,
pairing, disconnect, restart or remote-control line in the journal today, and
`grep -i 'wham\|remote/control\|enroll'` over the whole unit journal returns
nothing.

That absence is a **logging gap, not evidence**: `systemctl show -p Environment`
is empty (no `RUST_LOG`), `~/.codex/log/` is empty, and only `ERROR`-level
stderr reaches the journal. The remote-control events are recorded elsewhere
(§3.7).

Two journal lines are worth naming even though they are not list-related:

- `2026-09-12T15:11:02Z ERROR codex_core::tools::router: error=collab spawn failed: agent thread limit reached`
- `2026-09-12T01:31:35Z ERROR codex_core::session: failed to record rollout items: thread 01a091f8-ba98-7b41-bc80-b1cabc8740f6 not found`

The second is a thread the server could not find while writing its rollout —
the only witnessed instance of thread bookkeeping actually failing in this
process's life, and it is from yesterday's date-line, not today's threads.

### 3.5 Remote-control enrollment: two servers both named `ouranos`

`~/.codex/state_5.sqlite` carries a `remote_control_enrollments` table. Read
read-only via Python `sqlite3` (no `sqlite3` binary on this machine). Two
rows, both for websocket
`wss://chatgpt.com/backend-api/wham/remote/control/server`, both
`server_name = "ouranos"`, both `remote_control_enabled = 1`, both for
account `6717c197-e526-4f10-8cdf-48640cce4b43`:

| `app_server_client_name` | `server_id` | `environment_id` | `updated_at` |
|---|---|---|---|
| `""` (empty) | `srv_e_6a6a1cede72c8326bafecffd15108c6c` | `env_e_6a6a1cede71c8326a96f12cb2b467b06` | 1788366205 = 2026-09-02 10:23:25 |
| `Codex Desktop` | `srv_e_6a898486aa1c8326b45abb201a1cc6e4` | `env_e_6a898486aa0c8326979d131e35a65bda` | 1788877721 = 2026-09-08 08:28:41 |

**The phone therefore has two enrolled servers named `ouranos` to choose
between.** This is exactly the situation the living described in the notion
at 1.5 ("On my phone, I can have multiple remotes or multiple servers that
I connect to").

And **ChatGPT Desktop is not running**: `ps -eo pid,lstart,args | grep -i
chatgpt` returns only `chatgpt-unwrapped-26.901.31953/.../node_repl`
processes, all of which are children of pid 2087 (MCP servers configured in
`~/.codex/config.toml` under `[mcp_servers.node_repl]`). There is no
desktop-app process and no second app-server. The `Codex Desktop`
enrollment currently has nothing behind it.

The historical websocket log (§3.7) shows the environment identity
**switching** between these two: entries up to 2026-09-09 12:43 carry
`environment_id=Some("env_e_6a898486aa0c8326979d131e35a65bda")` (the
`Codex Desktop` row) and from 2026-09-10 01:29:42 onward carry
`env_e_6a6a1cede71c8326a96f12cb2b467b06` (the empty-name row).

### 3.6 Attached `codex --remote` TUI processes

Exactly **one**:

```
3181506 3181390 Sat Sep 12 09:04:21 2026  03:29:24  /nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex --remote unix://
```

- started 2026-09-12 09:04:21 local, running 3h29m at observation
- `cwd -> /home/li/primary`, stdin/stdout on `/dev/pts/7`
- parent chain: `pid 3181390 zsh` → `pid 4578 ghostty` → `systemd --user`

So it was typed by hand into a Ghostty shell, not launched by a wrapper.
`ss -xp` confirms its socket connection into the control socket
(`.codex-wrapped pid=3181506` ESTAB against pid 2087 fd 36).

No other `codex --remote` process exists. No other TUI has attached since
09:04.

### 3.7 How a TUI is normally launched here, and whether `--remote` is passed

- `codex` on PATH is `/home/li/.nix-profile/bin/codex` →
  `/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex`.
  Its content is the plain Nix wrapper: it prepends bubblewrap to `PATH` and
  `exec`s `.codex-wrapped "$@"`. **It is not agent-intercom and it does not
  pass `--remote`.** `zsh -lic 'whence -a codex; alias | grep -i codex'`
  shows no alias or function.
- The wrapper that *does* pass `--remote` is agent-intercom's `coi`, on PATH
  at `/run/current-system/sw/bin/coi`. In
  `/nix/store/id3rw3xlwdqb764pwqg6yamd0j60nx4d-agent-intercom-0.10.0/share/agent-intercom/codex/codex/coi.ts`:

  ```
  416:    ? ["resume", "--remote", remote, ...optionArgs, threadId, ...promptTail]
  417:    : ["--remote", remote, ...optionArgs, ...promptTail];
  722:  const remote = `unix://${socketPath}`;
  ```

  and its README: "Everything not recognized as a sidecar flag is passed
  through to `codex resume --remote`". `coi` also passes
  `--remote-auth-token-env`.
- The TUI running now was launched as bare `codex --remote unix://` — i.e.
  neither the plain default nor `coi`'s `resume --remote` form.

`codex --help` documents the two relevant surfaces:

```
      --remote <ADDR>
          Connect the TUI to a remote app server endpoint.
          Accepted forms: `ws://host:port`, `wss://host:port`, `unix://`, or `unix://PATH`.
```

and a subcommand `remote-control` — "[experimental] Manage the app-server
daemon with remote control enabled" — with `start`, `stop`, and **`pair`
(Create and print a short-lived manual pairing code)**. `codex app-server`
additionally offers `daemon` and `proxy` (Proxy stdio bytes to the running
app-server control socket).

### 3.8 Threads created today: where they live and who made them

This version does **not** store sessions only as rollout JSONL; it keeps
`~/.codex/thread_history_1.sqlite` (2.4 GB; tables `thread_items` 304 809,
`thread_turns` 4 509, `thread_history_projection_state` 2 391) and
`~/.codex/state_5.sqlite` (tables `threads` 3 249, `thread_spawn_edges`
2 279, `remote_control_enrollments` 2). Rollout JSONL is still written under
`~/.codex/sessions/YYYY/MM/DD/`.

`~/.codex/sessions/2026/09/12/` holds **12** rollout files. The `threads`
table has 12 rows created today: **3 root threads** (`thread_source='user'`)
and 9 subagents.

The three root threads:

| id | created (local) | tokens | `name` | in `session_index.jsonl`? |
|---|---|---|---|---|
| `01a09625-e9d0-7652-83d5-68014dc941bf` | 09:04:22 | 17 847 046 | `Audit 33a4d4 deployment` | yes (2 entries, last 15:05:28Z) |
| `01a096d4-3552-7f50-9ea0-5238325c1e96` | 12:14:44 | 1 599 945 | `NULL` | **no** |
| `01a096dc-545f-7323-974a-b734146763a0` | 12:23:37 | 842 408 | `NULL` | **no** |

All three: `archived=0`, `is_pinned=0`, `cwd=/home/li/primary`,
`history_mode=paginated`, `project_id=NULL`, `thread_section_id=NULL`,
`has_user_event=0` (that last is 0 for *every* user thread every day, so it
discriminates nothing).

`~/.codex/session_index.jsonl` was last written 09:05 local; its final entry
is `01a09625` / `"Audit 33a4d4 deployment"`. It has **no** entry for the two
later threads.

**The two later threads are the living's, typed from the phone.** Their
`first_user_message` in the `threads` table:

`01a096dc` (12:23:37, model `gpt-5.6-luna`):

> I use these standard skills manually loaded in both Claude and Codex harnesses. I'm on the road now, and on my phone, it's a bit difficult. I need you to collect and make it easy to copy separately:
> - the standard skills that I usually load with Claude
> - the standard skillset that I usually load in Codex
>
>
> with the right syntax for me to just paste them in a new session and start my session.

`01a096d4` (12:14:44, model `gpt-6-astra`):

> $main-flow $spirit $psyche $psyche-interraction $behavior $correction $vocabulary $edit-coordination
>
> I had a very extensive Claude Flow work overnight on a number of things, and I want you to:
> - Get a very good grasp of that.
> [… task list continues …]

Both ran: `01a096d4` spawned four subagents (12:15:07, 12:15:22, 12:15:43,
12:20:06) and `tokens_used` is 1.6 M; `01a096dc` reached 842 k. Both have
rows in `thread_history_projection_state` (`next_rollout_ordinal` 350 and
108) and `thread_items` (88 and 30). Their rollout files exist and were last
appended 12:22:48 and 12:25:26.

**So the living's belief is correct and now witnessed: two new flows were
started from the phone today and they did run.** Nothing was lost locally.

Provenance recorded *in* the rollouts is inconsistent with that, and this is
worth flagging: today's three root rollouts all carry
`"originator": "codex-tui", "source": "vscode"`. Historically the phone
stamped a distinct originator — a survey of every rollout since 2026-09-01
gives these `(originator, source)` pairs:

```
292 ('codex-tui', 'subagent')
 72 ('Codex Desktop', 'subagent')
 51 ('codex-tui', 'vscode')
 32 ('codex_exec', 'subagent')
 11 ('Codex Desktop', 'vscode')
 10 ('codex_exec', 'exec')
  5 ('codex_chatgpt_android_remote', 'subagent')
  1 ('codex_chatgpt_android_remote', 'vscode')
```

`codex_chatgpt_android_remote` roots appear on 2026-08-28 (`01a047d2`,
`01a048a0`, `01a048a6`, `01a04881`) and 2026-09-07 (`01a07b54`) — **and not
since**. Today's phone threads were stamped `codex-tui` instead.

### 3.9 The decisive log: the phone did drive this app-server today

`~/.codex/logs_2.sqlite` (954 MB, table `logs`, 275 538 rows spanning
2026-09-02 09:04:50 → 2026-09-12 12:37:42) is the app-server's structured
log. Process `pid:2087:7e574b7b-db4c-4f54-a2fa-ebd1f24cc3df` holds 13 918
rows from 09-10 13:34:11 to 09-12 12:37:42 — note the first row is **4
minutes after** the unit started at 13:30:08, so anything the process logged
in its first four minutes is not in this DB.

Today's `thread_processor` WARNs name the client outright:

```
09-12 12:23:37 WARN  app_server.request{otel.kind="server" otel.name="thread/resume"
  rpc.system="jsonrpc" rpc.method="thread/resume" rpc.transport="unix_socket"
  rpc.request_id=125 app_server.connection_id=38 app_server.api_version="v2"
  app_server.client_name="codex_chatgpt_android_remote" app_server.client_version="dev"}
  :resume_running_thread: thread/resume overrides ignored for loaded thread
  01a096dc-545f-7323-974a-b734146763a0: config overrides were provided and ignored while running
```

```
09-12 12:24:37 WARN  … app_server.connection_id=38 …
  app_server.client_name="codex_chatgpt_android_remote" app_server.client_version="dev"}
  :resume_running_thread: thread/resume overrides ignored for loaded thread
  01a09625-e9d0-7652-83d5-68014dc941bf: …
```

So: **connection 38 is the phone** (`codex_chatgpt_android_remote`, client
version `dev`, arriving as `rpc.transport="unix_socket"` because the relay
terminates inside the app-server and forwards the phone as a local
connection). Connection 32, at 09:03:59, carried
`app_server.client_name="codex-tui"` — the local terminal.

Connection 38 issued the whole phone session: `thread/queue/list`,
`thread/goal/get`, `turn/start`, `thread/resume`, `skills/list`,
`mcpServerStatus/list`, `plugin/list`, `thread/turns/list`,
`thread/items/list`, `gitDiffToRemote`, `config/read`,
`configRequirements/read`, `model/list` between 12:23:37 and 12:24:38.
And at 12:24:37 the phone resumed `01a09625` — the thread the *local
terminal* TUI had created at 09:04. That is the feature working exactly as
the living asked for it in 1.1.

Connections 37 and 39 are the backend's own notification channel:

```
09-12 12:09:33 DEBUG composing running thread resume response thread_id=01a09625-… request_id=ConnectionRequestId { connection_id: ConnectionId(37), request_id: String("__slingshot_backend_notification_thread_resume__:01a09625-…") }
09-12 12:10:06 DEBUG … thread_id=01a0919c-83d8-7113-9274-46633a4d40cf … ConnectionId(37) … __slingshot_backend_notification_thread_resume__:01a0919c-…
09-12 12:10:12 DEBUG … thread_id=01a0808b-adfe-7dd0-8c55-6338e9e77b05 … ConnectionId(37) … __slingshot_backend_notification_thread_resume__:01a0808b-…
09-12 12:14:45 DEBUG … thread_id=01a096d4-3552-7f50-9ea0-5238325c1e96 … ConnectionId(37) … __slingshot_backend_notification_thread_resume__:01a096d4-… active_turn_status=Some(InProgress)
09-12 12:23:37 TRACE app-server request: thread/resume connection_id=ConnectionId(39) request_id=String("__slingshot_backend_notification_thread_resume__:01a096dc-545f-7323-974a-b734146763a0")
09-12 12:25:26 TRACE app-server request: thread/unsubscribe connection_id=ConnectionId(39) request_id=String("__slingshot_backend_notification_thread_unsubscribe__:01a096dc-545f-7323-974a-b734146763a0")
```

**The backend did subscribe to both new threads.** `01a096d4` at 12:14:45,
`01a096dc` at 12:23:37 — so the relay announced them upward. `01a096dc` was
then unsubscribed at 12:25:26.

At 12:10 the backend subscribed to `01a09625`, `01a0919c` (created 09-11)
and `01a0808b` (created 09-08) — a set that looks like the phone list being
populated. Of note for the "missing name" theory: `01a0808b` also has
`name = NULL`, and it *was* subscribed. A missing name therefore does not by
itself keep a thread out of the backend's view.

Then, the last remote-control line in the entire DB:

```
09-12 12:27:56 INFO  codex_app_server_transport::transport::remote_control::client_tracker
  forwarding remote control connection closed transport event connection_id=ConnectionId(37)
```

**The remote-control connection closed at 12:27:56 and nothing
remote-control-related has been logged since.** The only rows after that
timestamp (through 12:37:42) are three identical `list_models` refresh
cycles at 12:28:41, 12:33:11 and 12:37:42.

### 3.10 The websocket-cycle silence, and what it does and does not mean

Grouping every `remote_control` log row (436 rows) by process:

```
pid:2468231  websocket n=76  client_tracker n=8   09-03 20:34 .. 09-04 04:36
pid:3103529  websocket n=9   client_tracker n=1   09-04 09:24 .. 09-04 09:34
pid:3137277  websocket n=9                        09-05 04:02
pid:213379   websocket n=8   enroll n=1  remote_control n=4   09-05 08:46
pid:4096266  websocket n=92  client_tracker n=10  09-06 02:25 .. 09-06 13:28
pid:1171756  websocket n=21  client_tracker n=2   09-06 06:07 .. 09-06 06:29
pid:2829     websocket n=33  enroll n=1  client_tracker n=2   09-06 17:07 .. 09-06 18:04
pid:29549    websocket n=62  client_tracker n=7   09-07 05:40 .. 09-07 10:37
pid:298129   websocket n=51  client_tracker n=5   09-09 09:45 .. 09-09 12:43
pid:2316     websocket n=8                        09-09 16:56 .. 09-09 16:57
pid:168251   websocket n=18  client_tracker n=3   09-10 01:29 .. 09-10 03:02
pid:2087     client_tracker n=1                   09-12 12:27:56
```

Every earlier app-server process logged `remote_control::websocket`
connection cycles — "connecting to app-server remote control websocket",
"connected to …", "remote control websocket status changed", "refreshing
remote control server token", "remote control websocket reader disconnected",
"pong timeout". **The process running now, pid 2087, has logged none of them
in two days.** Its only remote-control row is the single connection-closed
line.

Two readings, and the evidence does not separate them:

- the initial connect cycle happened in the 4-minute window before the log
  sink attached (13:30:08 → 13:34:11), and the socket then simply stayed up
  for two days with nothing to report; or
- the remote-control websocket cycle is not being logged by this build/level
  at all.

What can be said: on 2026-09-11 12:01–12:06 the process logged repeated
`codex_api::endpoint::responses_websocket` failures ("Network is
unreachable", "Temporary failure in name resolution") — a real network
outage — and logged **no** corresponding remote-control websocket
disconnect, where earlier processes did log such disconnects on comparable
events. Live TCP now: pid 2087 holds 10 ESTAB connections to `:443` on
`172.64.155.209` and `104.18.32.47` (Cloudflare fronting `chatgpt.com`),
four from `192.168.1.5` and two from `10.18.0.102`. Consistent with a live
relay socket; not proof of one.

### 3.11 Version: 0.153.4 running, 0.154.0 upstream stable

- running: `codex-cli 0.153.4` (store `codex-0.153.4`)
- `~/.codex/version.json`:
  `{"latest_version":"0.154.0","last_checked_at":"2026-09-12T15:04:01.738959517Z","dismissed_version":null}`
- `gh release view --repo openai/codex`: latest full release is
  `rust-v0.154.0`, published `2026-09-09T22:35:38Z`
- `gh release list`: prereleases run ahead to `0.155.0-alpha.3.10`
  (2026-09-11T15:52:58Z)

So the server is **one minor behind upstream stable**, and the release it is
behind landed on 2026-09-09 — after the last date the phone stamped
`codex_chatgpt_android_remote` on a rollout (2026-09-07). The phone client
identifies itself as `client_version="dev"` against `api_version="v2"`.

### 3.12 Possible causes, ranked by the evidence

These are hypotheses. None is asserted as the cause; none was witnessed
causing the symptom.

**H1 — The phone's remote-control client connection is closed and the list
the living is looking at is a stale client-side or backend view.**
*Ranked first: the strongest direct evidence.*
Witnessed: the one remote-control line in this process's two-day life is
`forwarding remote control connection closed transport event
connection_id=ConnectionId(37)` at 12:27:56, two minutes after the last
phone thread stopped writing, and nothing remote-control-related has been
logged in the 10 minutes since. Witnessed: both new threads *were*
announced upward (`__slingshot_backend_notification_thread_resume__` for
`01a096d4` at 12:14:45 and `01a096dc` at 12:23:37), so the relay did carry
them at the time.
*Decided by:* open the app now and re-read
`~/.codex/logs_2.sqlite` for rows after 12:37:42. If a new
`remote_control::client_tracker`/`websocket` line and a `thread/list`-shaped
request appear on a connection whose `app_server.client_name` is
`codex_chatgpt_android_remote`, the server is answering and the app is
filtering or rendering the answer wrongly. If no such row appears, the app
never reconnected to this server and the list is purely cached.

**H2 — The phone is pointed at the other enrolled `ouranos`.**
*Ranked second: two enrolled servers with the same display name, one of them
currently unbacked, is witnessed fact.*
Witnessed: `remote_control_enrollments` holds two rows, both
`server_name="ouranos"`, both enabled, for the same account — `""` /
`srv_e_6a6a1ce…` (updated 2026-09-02) and `Codex Desktop` /
`srv_e_6a898486…` (updated 2026-09-08). Witnessed: no ChatGPT Desktop
process is running and no second app-server socket exists, so the
`Codex Desktop` server has nothing serving it. Witnessed: the logged
`environment_id` switched from `env_e_6a898486…` to `env_e_6a6a1ce…` on
2026-09-10 01:29:42 — the machine's relay identity changed three days ago.
Relayed and corroborating: the living's own notion (1.5) describes holding
"multiple remotes or multiple servers" on the phone.
*Decided by:* on the phone, look at the server picker. If two `ouranos`
entries are listed, select the other one and see whether today's threads
appear there. A server whose threads are all older than 2026-09-10 is the
`Codex Desktop` one.

**H3 — The relay announced the threads but the backend's *list* never
learned them, only the per-thread subscription.**
*Ranked third: there is a concrete local index that stopped, but also direct
counter-evidence.*
Witnessed: `~/.codex/session_index.jsonl` was last appended at 09:05 local
with `01a09625`, and has no entry for either later thread; both later
threads also have `name = NULL` where `01a09625` got
`"Audit 33a4d4 deployment"`. Witnessed counter-evidence: `01a0808b`
(2026-09-08) likewise has `name = NULL` and the backend *did* subscribe to
it at 12:10:12; and `name = NULL` is common historically (5 of 12 user
threads on 09-05, 2 of 3 on 09-08). So a missing auto-title does not by
itself explain invisibility.
*Decided by:* from the phone, try to reach
`01a096dc-545f-7323-974a-b734146763a0` directly (by search, or by resuming
it from the list of a different client). If it opens but never appears in
the list, the list is a separately-maintained projection that is stale or
filtered. If it cannot be reached at all, it was never entered into the
backend's catalogue.

**H4 — Version skew between the 0.153.4 app-server and the phone client.**
*Ranked fourth: real skew, no evidence tying it to the symptom.*
Witnessed: server `0.153.4`; upstream stable `rust-v0.154.0` published
2026-09-09; `version.json` records `latest_version 0.154.0` checked today at
15:04:01Z; the phone announces itself as `client_version="dev"`,
`api_version="v2"`. Witnessed: the phone's `thread/resume` calls were
answered today, so the protocol is not wholly broken — the two WARNs are
only "config overrides were provided and ignored while running". Witnessed:
`codex_chatgpt_android_remote` last appeared as a rollout *originator* on
2026-09-07, and today's phone-created threads were stamped `codex-tui`
instead — an originator-attribution change somewhere between those dates
that could equally well shift how a thread is catalogued for the app.
*Decided by:* compare the `thread/list`-family response this 0.153.4
app-server returns against what the app expects, or upgrade the unit's
`codexCliPackage` to 0.154.0 in CriomOS-home and re-test from the phone.
That upgrade is a change outside this report's remit and needs the living's
word.

**H5 — The relay websocket dropped silently after 12:27:56.**
*Ranked fifth: only an absence of logs supports it, and the absence has an
innocent explanation.*
Witnessed: pid 2087 logged no `remote_control::websocket` cycle in two days,
where all eleven earlier app-server processes did; and it logged no
remote-control disconnect during the real network outage of 2026-09-11
12:01–12:06 that its `responses_websocket` target *did* record. Against:
the log sink attached 4 minutes after process start, so the initial connect
cycle is genuinely unobservable; and 10 live ESTAB `:443` connections to
Cloudflare/chatgpt.com exist right now.
*Decided by:* raise the unit's log level (`RUST_LOG=info`) at the next
restart and watch for the connection cycle — or, without restarting, force
a refresh from the phone and check whether a new
`remote_control::websocket` row appears at all. If the phone reaches the
server and *still* no websocket row is logged, the silence is a logging
change, not a dead socket.

**H6 — Ordering: the new threads sorted out of view.**
*Ranked last; the evidence argues against it.*
Witnessed: `recency_at` for the two new threads is 12:14:45 and 12:23:37,
newer than every other thread in the table, and both have `archived=0`,
`is_pinned=0`. A recency-ordered list would put them first.
*Decided by:* scroll the list. If they are present but buried, the ordering
key is not recency.

**H7 — The flow corpus's own leading candidate: a session started as plain
`codex` is invisible to the phone forever.**
*Named separately because it is the explanation the flow record points at,
and because this subflow's live evidence rules it out for these two threads
specifically — but not for anything else the living started today.*
Relayed: 8a5caa (deployment 204, 2026-09-05) reverted ordinary `codex` to
plain upstream, leaving `codex-remote` as the only attaching launcher (§2.2);
and 01a03f49 established that "A plain TUI launched before the daemon uses an
embedded app-server. No attach, rebind, or conversion command exists", with
`564f55/reports/codexLaunch.md:100-106` stating the rule outright: "the
session **must be started with `--remote` from the very first invocation**.
A plain `codex` in a ghostty window can never be made remote afterward."
Witnessed here: plain `codex` on PATH indeed passes no `--remote` (§3.7).
Witnessed counter-evidence for today: the one live TUI *was* launched
`codex --remote unix://` (§3.6), and both new threads were created *inside*
pid 2087 and driven by a connection the server labelled
`codex_chatgpt_android_remote` (§3.9) — so neither of the two missing flows
is an unattached embedded-app-server session.
*Decided by:* ask the living whether the flows they mean are these two
(`01a096d4`, `01a096dc`) or others. If others, look for a `codex` process
without `--remote` — such a session's threads would never reach the phone,
and the fix is launching with `codex-remote` (or `codex --remote unix://`)
from the first invocation.

**Precedent worth naming.** This has happened once before and was never
explained. `flows/01a047d2/log.md:18` (relayed, that flow's witness of the
timestamps only): "The Codex service was explicitly stopped and started at
04:04:53–04:04:54, but the requester and its relationship to **temporary
phone invisibility** remain unknown." And 01a03f49 "did not establish …
phone enrollment surviving restart" (`01a047d2/log.md:5`). The word
*temporary* in that record is the one encouraging note in the whole corpus:
the last occurrence resolved on its own.

**What this report deliberately does not claim.** No cause was witnessed.
The two things that *were* witnessed and that bound every hypothesis are:
(a) the threads exist, ran, and are intact locally, so nothing was lost; and
(b) the app-server's remote-control connection to the phone closed at
12:27:56 and has logged nothing since. Everything between those two facts —
what the backend's list holds, which `ouranos` the app is looking at, what
the app renders — is beyond this machine's evidence and needs one
observation from the phone.

### 3.13 Two further witnessed facts, flagged not diagnosed

- The app-server holds **9.6 GB resident, 18 GB peak, 238 tasks** after
  1d23h and one root thread reached **17.8 M tokens**. `collab spawn failed:
  agent thread limit reached` fired at 09:11:02 today and repeatedly on
  09-09 and 09-11. This is a standing pressure on the always-running-owner
  design (1.1) and on the rolling-restart question the living raised as a
  notion (1.5). Not a cause of list invisibility.
- The living's ChatGPT `account_id` `6717c197-e526-4f10-8cdf-48640cce4b43`
  sits in the enrollment rows, and this report names it. That is the same
  class of datum flow f7941a pushed and the living then addressed in 1.13
  ("we're just doing everything public for now"). Flagging it rather than
  deciding it.

Auth is not implicated: `~/.codex/auth.json` (`auth_mode`, tokens,
`last_refresh 2026-09-06T23:07:45Z`) carries an `access_token` with
`exp 2026-09-16T23:07:45Z` — valid for four more days. Its `id_token`
expired 2026-09-07T00:07:45Z, which is normal for an id token.

---

## Sources

### Method
§3 was observed directly by this subflow with read-only commands on ouranos
between 2026-09-12 12:33 and 12:45 local; nothing was started, stopped or
reconfigured, and every SQLite read used `mode=ro`. §1 and §2 were gathered
by two nested read-only subflows and are therefore **doubly relayed**: a
nested flow read the file and reported the text, and this report carries it.
The verbatim psyche blocks in §1 were required to be reproduced without
paraphrase and are presented as returned. §2's flow-internal witness marks
(`[flow-W]`) are those flows' own claims, not this subflow's observations.
This report is written but **not committed** — committing is left to the main
flow.

### Psyche records (relayed; files read this session)
- `/home/li/primary/flows/01a03f49/vision/remoteControlAllTheCodexTuiSessionsICreate.md`
- `/home/li/primary/flows/01a047d2/vision/remoteControl.md`
- `/home/li/primary/flows/01a04336/vision/remoteFlag.md`
- `/home/li/primary/flows/01a04524/vision/claudeRemoteControl.md`
- `/home/li/primary/flows/01a05487/notion/rollingCodexServices.md`
- `/home/li/primary/flows/01a05487/vision/flowMovesBetweenGenerations.md`
- `/home/li/primary/flows/01a052b6/vision/reportFeedback.md`
- `/home/li/primary/flows/01a05d17/vision/fullAccessPermission.md`
- `/home/li/primary/flows/ea1e56/vision/desktopCodexIntegration.md`
- `/home/li/primary/flows/58a86d/vision/vscodium.md`
- `/home/li/primary/flows/01a0437d/vision/codexAndClaude.md`
- `/home/li/primary/flows/01a038be/vision/archive-x11.md`
- `/home/li/primary/flows/e71fa5/vision/private-data-separation.md`
- Searched and found empty for this topic: `/home/li/primary/Vision/`, `/home/li/primary/Intent/`, `/home/li/primary/vision-raw/`

### Flow accounts (relayed; all paths under `/home/li/primary/flows/`)
- `01a03f49/log.md`; `01a03f49/reports/codexPhoneRemoteControl.md`
- `01a038be/log.md`; `01a038be/reports/officialChatgptCorrectionDeployment.md`; `01a038be/reports/rememberedUserDeployment.md`
- `01a0338f/witnesses/ouranosChatgpt.md`
- `01a04336/log.md`
- `01a047d2/log.md`
- `01a048a6/annotations.md`
- `01a04524/log.md`
- `01a05487/log.md`
- `01a05826/log.md`
- `01a05833/log.md`
- `01a057e7/log.md`
- `01a05c80/log.md`; `01a05e53/log.md`
- `4ad49f/log.md`; `4ad49f/reports/implementation.md`; `4ad49f/reports/system-integration.md`; `4ad49f/witnesses/{deployment-boundary,home-rollback-review,live-stock-desktop,pristine-stock-boundary,prechange-red-gate}.md`
- `ea1e56/reports/desktop-persistent-codex-audit.md`; `ea1e56/reports/source-inventory.md`; `ea1e56/witnesses/current-desktop-codex-state.md`
- `cf0ed9/reports/live-diagnosis.md`; `cf0ed9/reports/code-and-deployment-path.md`; `cf0ed9/reports/remaining-codex-app-producer.md`; `cf0ed9/witnesses/{chatgpt-restart,chatgpt-corrected-live}.md`
- `d30eb1/log.md`
- `d97d50/reports/declarative-state.md`; `d97d50/witnesses/runtime-crash.md`
- `5d0c7b/log.md`
- `4a8046/log.md`; `4a8046/witnesses/{activation-readiness,integration-deployment}.md`
- `8a5caa/log.md`; `8a5caa/reports/{codex-implementation,codex-integration}.md`
- `58a86d/log.md`
- `db267d/log.md`; `db267d/witnesses/claude-remote-control-removal.md`; `db267d/witnesses/zeus-claude-desktop-repair-deployment.md`
- `985ba2/log.md`; `985ba2/reports/application-updates.md`; `985ba2/reports/unused-app-removal.md`; `985ba2/reports/desktop-image-investigation.md`
- `564f55/reports/codexLaunch.md`
- `f7941a/reports/desktop-transport.md`
- `e71fa5/log.md`
- `f6db8d/reports/unused-survey.md`; `f6db8d/reports/landings-consumers.md`; `f6db8d/reports/terminal-migration.md`
- `7648a0/log.md`
- `674a4dab/reports/criomosStackAudit.md`
- `7b4d4c/reports/psyche-harnesses.md`
- `be2534/log.md`; `7fba5f/reports/codexReportLoop.md`
- `index.md` (flow-index row for 01a03f49)
- `9e7c9f/log.md` (this flow's own pre-delegation witness line)

### Live state (witnessed 2026-09-12 12:33–12:45 local, ouranos)
- `systemctl --user cat codex-remote-control.service`
- `systemctl --user status codex-remote-control.service --no-pager`
- `systemctl --user show codex-remote-control.service -p Environment -p EnvironmentFiles`
- `journalctl --user -u codex-remote-control --since today --no-pager`
- `journalctl --user -u codex-remote-control --no-pager` (full, grepped for `wham`, `remote`, `pair`, `thread`, lifecycle)
- `ss -xlp`, `ss -xap`, `ss -tnp`
- `ps -eo pid,ppid,lstart,etime,args`; `/proc/3181506/{cmdline,cwd,stat,fd}`; parent chain to `ghostty`
- `/home/li/.nix-profile/bin/codex` (wrapper text); `codex --version`; `codex --help`; `codex remote-control --help`; `codex app-server --help`
- `/nix/store/id3rw3xlwdqb764pwqg6yamd0j60nx4d-agent-intercom-0.10.0/share/agent-intercom/codex/codex/coi.ts`; `.../codex/README.md`; `/run/current-system/sw/bin/coi`
- `/home/li/.codex/` listing; `/home/li/.codex/app-server-control/`; `/home/li/.codex/app-server-daemon/`; `/home/li/.codex/ipc/`; `/home/li/.codex/log/` (empty)
- `/home/li/.codex/config.toml`; `/home/li/.codex/version.json`; `/home/li/.codex/session_index.jsonl`; `/home/li/.codex/auth.json` (JWT `exp`/`iat` only)
- `/home/li/.codex/sessions/2026/09/12/*.jsonl` (12 files, first-line metadata); originator/source survey over `/home/li/.codex/sessions/**` since 2026-09-01
- `/home/li/.codex/state_5.sqlite` read-only (`remote_control_enrollments`, `threads`, `projects`, `project_roots`, `thread_sections`, `backfill_state`, `rollout_migration_state`)
- `/home/li/.codex/thread_history_1.sqlite` read-only (`thread_history_projection_state`, `thread_items`)
- `/home/li/.codex/logs_2.sqlite` read-only (`logs`: remote-control rows, per-process spans, today's `thread_lifecycle`/`thread_processor`/`message_processor`/`thread_state` rows)
- `gh release list --repo openai/codex --limit 8`; `gh release view --repo openai/codex`
- `/home/li/wt/github.com/LiGoldragon/CriomOS-home-wispr-overlay/modules/home/profiles/min/agent-intercom.nix` (authoring source; **not** the revision that produced the live store path)
