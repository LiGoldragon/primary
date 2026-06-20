# 707-1 — mentci CLI/GUI integration for criome/spirit/router observability + VM testing

Stream A of the 707 wave. Read-only review of operator's recent work plus a
concrete design for a better mentci CLI + GUI integration that turns mentci into
a unified observability / control / test-driving surface over the
criome / spirit / router full-host daemons, with nix-derived VM tests. Design
pass — propose, do not build.

## 1. What exists today (review of operator's work)

### 1.1 The mentci daemon triad is REAL, not aspirational

All three triad repos exist with live source and recent operator commits:

- `mentci` (daemon + thin CLI) — `/git/github.com/LiGoldragon/mentci`. Real
  Kameo-actor daemon: `src/daemon.rs:20-176` (a `StateOwner` actor wrapping
  `State`), `src/state.rs:14-321` (the full in-memory state machine over the
  signal-mentci vocabulary), `src/client.rs:34-191` (the one-argument thin CLI),
  `src/criome_bridge.rs:13-76` (the criome meta-socket bridge), three bins
  (`mentci-daemon`, `mentci-write-configuration`, `mentci-criome-pickup-witness-test`).
- `signal-mentci` — the working contract, `schema/lib.schema:68-378`. Six
  requests (`PresentQuestion`, `PushUpdate`, `ObserveInterfaceState`,
  `AnswerQuestion`, `ProposeEditedAnswer`, `RetractInterfaceObservation`),
  seven replies, a `MentciEvent` stream (`InterfaceStateChanged`) on
  `InterfaceStateStream` (`schema/lib.schema:373-377`).
- `meta-signal-mentci` — the meta contract, `schema/lib.schema:65-216`. One verb
  `Configure(MentciDaemonConfiguration)` carrying typed `ComponentSocket`s
  (`ComponentSocketKind` = `Mentci | MetaMentci | Criome | MetaCriome`,
  `schema/lib.schema:108-117`), a `PersonaIdentity`, and `NotificationClient`s.

The daemon boots from exactly one binary rkyv `Configure` file
(`src/configuration.rs:21-39`, `src/daemon.rs:50-75`); the CLI takes exactly one
argument — a `.rkyv` frame, a `.nota` file, inline NOTA, or a criome approval
atom (`src/client.rs:56-90`). Discipline holds.

ARCHITECTURE.md is honest about the gaps (`mentci/ARCHITECTURE.md:34-69`):
in-memory SEMA (not durable), no notification fan-out events beyond
request/reply, and observe-triggered parked-authorization pickup is a one-shot
poll, not a continuous push loop.

### 1.2 How mentci talks to criome today — over criome's META socket, by slot

The criome approval flow operator landed is end-to-end real and matches settled
intent (t00s / p43g):

- criome runs in `ClientApproval` mode and PARKS every submission instead of
  evaluating it (`criome` log `245f044`, witnessed by
  `criome/src/bin/criome-client-approval-witness-test.rs:144-160` —
  `EvaluateAuthorization → AuthorizationPending(slot)`).
- mentci lists + decides parked authorizations over criome's META socket using
  `meta-signal-criome`'s `ObserveParkedAuthorizations` /
  `SubmitAuthorizationApproval(request_slot, decision)`
  (`meta-signal-criome/schema/lib.schema:21-55`,
  `mentci/src/criome_bridge.rs:42-67`). It approves BY SLOT, never resubmitting
  the evaluation by value (ARCHITECTURE.md:55-58) — exactly t00s.
- The daemon folds parked criome requests INTO its own pending-question queue on
  `ObserveInterfaceState` (`mentci/src/daemon.rs:130-141`,
  `src/state.rs:92-104`, `into_question_proposal` at `src/state.rs:293-320`), so
  a connecting client sees criome-queued requests as mentci questions without a
  separate poll.

The CLI also speaks the bare criome approval atoms `criome:parked`,
`criome:approve:<slot>`, `criome:reject:<slot>`, `criome:defer:<slot>`
(`src/client.rs:139-191`) straight to criome's meta socket.

### 1.3 mentci-egui today — a daemon-connected NOTA transcript viewer

mentci-egui was rebuilt off the daemon (commits `7b6c379`, `9f7f9c4`,
`293a228`, `075cbff`). It is a thin client: one "observe" button issues
`ObserveInterfaceState(FullInterfaceState)` and renders the reply as collapsible
request/reply NOTA blocks (`mentci-egui/src/app.rs:42-141`,
`src/daemon_client.rs:68-86`). Socket displays carry channel labels `Mentci` /
`MetaMentci` (xen8 satisfied: `src/daemon_client.rs:177-184`, header at
`app.rs:75-101`). It connects over signal-mentci frames directly
(`src/daemon_client.rs:98-130`).

What it does NOT do yet: it is request/reply only (no live subscription /
`MentciEvent` consumption); "meta" mode is a placeholder string
(`src/daemon_client.rs:88-96`) because the daemon exposes no live meta socket;
it renders ONE socket (Mentci) — it does not connect to criome/spirit/router
sockets directly (xen8's multi-component case is unrealized); and it has no
verdict/approve UI — it cannot answer a question, only view it.

### 1.4 router — authorized-object projection is live and uses signal-standard

router exposes the criome authorized-object projection (commits `9471219`,
`4ce85c1`, `ce578f1`). `src/authorized_object_projection.rs:1-73` converts
`signal_criome::AuthorizedObjectReference` → `signal_standard` types via clean
`impl From` conversions. Notably **router already consumes `signal-standard`** —
the cross-import path that signal-mentci / meta-signal-mentci deferred is proven.

### 1.5 THE CENTRAL FINDING — mentci-lib is orphaned and stale (violates 7x5z)

Intent 7x5z: "mentci-lib is the shared application/state-machine library reused
by the daemon AND clients." Reality contradicts this on every edge:

- The daemon does NOT depend on mentci-lib. `mentci/Cargo.toml:11-20` pulls
  `signal-mentci`, `criome`, `meta-signal-*` — no `mentci-lib`. Its state machine
  is hand-written in `mentci/src/state.rs` over signal-mentci types.
- mentci-egui does NOT depend on mentci-lib. `mentci-egui/Cargo.toml:15-25`
  pulls `signal-mentci` / `signal-frame` / `nota-next` — no `mentci-lib`. Its
  client is hand-written in `src/daemon_client.rs`.
- mentci-lib depends on NEITHER signal-mentci nor any mentci repo. It imports a
  generic `signal::{Graph, Node, Slot, Frame, Handshake}` graph vocabulary
  (`grep` over `mentci-lib/src`: only `use signal::…`), and models a
  `DaemonRole::Criome | DaemonRole::Nexus` handshake connection
  (`src/connection/driver.rs:1-40`) that does not exist in the live
  signal-mentci/signal-frame contract.
- mentci-lib re-declares the entire approval vocabulary as hand-rolled plain
  Rust — `ApprovalQuestion`, `ApprovalSource`, `ApprovalPrompt`,
  `SuggestedAnswer`, `ApprovalExplanation` (`src/approval.rs:49-120`) — a second,
  divergent copy of signal-mentci's `ApprovalQuestion` / `ApprovalSource` /
  `PromptText` / `SuggestedAnswer`.

So the shared-state-machine leg of the triad is, today, a divergent skeleton on
a contract the daemon abandoned. The daemon and the GUI each independently
re-implement state + transport. This is the single biggest integration debt and
the lever for the whole readability/testing goal.

## 2. What readability + testing means here, concretely

Readability = a human (psyche) or an agent can point mentci at a running
criome/spirit/router daemon and SEE, in typed-then-NOTA form, what the daemon's
canonical state is, what it is asking, and what a verdict will do — over both the
working and meta channels, with every pane labeled by component + authority lane
(xen8). Testing = a nix-derived VM stands the real daemons up from their deploy
path and DRIVES them through mentci (CLI in-VM, or the egui client model headless)
to assert that the readable surface is also the correct surface, end-to-end.

The criome witness tests (`criome-client-approval-witness-test.rs`) are already
exactly the right SHAPE for this: a struct holding typed clients, each step a
method that sends a real frame and asserts the typed reply, exit 0/nonzero. The
design generalizes that shape into mentci and lifts it into nixosTest guests.

## 3. The design

### 3.1 Shared model — make mentci-lib the real shared leg (the keystone)

Re-found mentci-lib as the **observability + control model over the live
contracts**, deleting the orphaned graph-signal skeleton and the duplicate
approval types:

- Depend on `signal-mentci`, `meta-signal-mentci`, `signal-criome`,
  `meta-signal-criome`, and `signal-standard`. Re-export their typed nouns;
  never re-declare them (the `src/approval.rs` duplicates go).
- Own one `ObservationModel`: a typed projection of "what I am connected to and
  what each connection currently shows." Keyed by `ComponentSocketKind`
  (`Mentci | MetaMentci | Criome | MetaCriome`, extended to add
  `Spirit | MetaSpirit | Router | MetaRouter`), each entry carries the channel
  label (xen8), the last typed reply, and its NOTA rendering.
- Own the **NOTA-fallback renderer** as a single method (xlrk): typed reply →
  purpose-built view if one exists, else `value.to_nota()`. Both the CLI and the
  GUI call it; the GUI's current ad-hoc `to_nota()` in `daemon_client.rs:132-146`
  and the daemon's `format!("{:?}", …)` in `state.rs:296-317` collapse into it.
- Own the **approval-decision model**: the closed `ApprovalDecision`
  (signal-mentci) for daemon questions, mapped to criome's
  `AuthorizationApprovalDecision` exactly as `criome_bridge.rs:69-75` already
  does — that mapping belongs in mentci-lib, used by daemon, CLI, and GUI alike.

The daemon's `State` (`mentci/src/state.rs`) then becomes a thin owner of the
mentci-lib state machine rather than a private re-implementation; mentci-egui's
`daemon_client.rs` becomes a thin transport wrapper around mentci-lib's
connection model. This is what 7x5z actually asked for, and it is the precondition
that makes CLI and GUI improvements land once instead of twice.

### 3.2 CLI improvements (in the mentci daemon repo's thin client)

The CLI is the daemon's first client and the in-VM test driver. Concrete moves:

1. **A read-side verb roster, not just one frame in / one frame out.** Today the
   CLI is "send one request, print one reply." Add first-class atoms mirroring
   the criome ones already there (`client.rs:139-161`):
   `mentci:state` (ObserveInterfaceState FullInterfaceState),
   `mentci:questions` (PendingQuestions projection),
   `mentci:status`, `mentci:answer:<question>:<approve|reject|defer>`. Each prints
   the typed reply through the shared NOTA renderer (§3.1), so CLI output reads
   identically to what the GUI shows.
2. **Multi-component connect.** The CLI already reaches criome's meta socket
   (`client.rs:131-136`). Generalize to a `--`-free atom family
   `criome:state`, `spirit:state`, `router:objects` that opens the relevant
   component working/meta socket (typed by `ComponentSocketKind` from the daemon
   config, not env-var guesswork) and renders the typed reply. This is the CLI
   half of xen8: every line of output is prefixed with the component + channel it
   came from.
3. **A `--`-free `mentci:transcript` that drives a scripted sequence** from one
   NOTA file (a vector of requests), printing each labeled reply — the CLI form
   of a witness run, runnable in-VM and asserted by `grep` in a testScript.

### 3.3 GUI improvements (mentci-egui)

1. **Live subscription, not poll.** The contract already has the
   `MentciEvent::InterfaceStateChanged` stream (`signal-mentci/schema/lib.schema:373-377`);
   the daemon does not push it yet (ARCHITECTURE.md:66-69). Wire the daemon to
   publish stream events on `bump_revision()` (`state.rs:260-263`), and have the
   egui client hold the long-lived `ObserveInterfaceState` subscription and
   render `InterfaceStateChanged` frames as they arrive — the long-lived-events
   shape xlrk asks for, replacing the single "observe" button
   (`app.rs:85-92`).
2. **Multi-component panes (xen8 fully realized).** Render one labeled pane per
   `ComponentSocketKind` — Mentci, MetaMentci, Criome, MetaCriome, and (when their
   contracts are reachable) Spirit, Router. Each pane shows the typed→NOTA
   projection from mentci-lib's `ObservationModel`. The header already labels two
   sockets (`app.rs:75-101`); generalize the label loop over the model.
3. **The approval surface (t00s / gc0n made visible and actionable).** Render
   each pending `ApprovalQuestion` (the daemon already folds parked criome
   requests into these, `state.rs:92-104`) as a card: prompt, suggested answer,
   context entries, and three buttons — Approve / Reject / Defer — that send
   `AnswerQuestion(ApprovalVerdict)`. For criome-sourced questions
   (`ApprovalSource::CriomeEscalation`) the verdict routes through the daemon's
   `CriomeApprovalBridge` to the criome meta socket by slot. This is the
   EscalateToPsyche UI gc0n says is "inert until a psyche-facing UI exists" — this
   card IS that UI. Today the GUI cannot answer anything; this is the highest-value
   GUI gap.
4. **A live meta mode.** Replace the placeholder
   (`daemon_client.rs:88-96`) once the daemon binds its MetaMentci socket
   (§3.4) — meta mode shows the live `MentciDaemonConfiguration` and the
   configured component sockets.

### 3.4 Two daemon-side enablers (small, contract-shaped)

- **Bind the MetaMentci socket.** The daemon binds only `Mentci`
  (`daemon.rs:54-60`); the config already carries a `MetaMentci` endpoint
  (`meta-signal-mentci/schema/lib.schema:108-117`). Bind it and serve
  `Configure` so meta mode and reconfiguration become live (the egui placeholder
  goes away).
- **Continuous criome parked-authorization pickup.** Turn the one-shot
  observe-time poll (`daemon.rs:130-141`) into a background subscription loop that
  re-polls criome's meta socket and pushes new parked slots as
  `InterfaceStateChanged` events — closing ARCHITECTURE.md's stated gap and
  feeding §3.3.1.

### 3.5 Resolve the now-unblocked cross-imports (correctness + clarity)

Both signal-mentci (`schema/lib.schema:50-57`, `303-313`) and meta-signal-mentci
(`schema/lib.schema:34-47`, `98-145`) declare `StandardSocket` / `ComponentKind`
locally with a "cross-import DEFERRED — signal-standard not yet a crate" note.
**signal-standard now exists** (`/git/github.com/LiGoldragon/signal-standard`,
`schema/lib.schema` carries `StandardSocket [(UnixSocket SocketPath)
(NetworkSocket NetworkEndpoint)]`, `ComponentKind`, `AuthorizedObjectReference`),
and router already consumes it (§1.4). Collapse the local declarations into
`signal-standard:lib:` imports as both schemas pre-described. This unblocks the
eaf7 standard-socket type for mentci's multi-component connect and removes a
divergent `StandardSocket` shape (the local one is a struct with one `path`;
signal-standard's is the richer Unix/Network enum).

## 4. Nix-derived VM test approach

The foundation already exists in the `criome-nixos-module-142` worktree:
`nix/modules/criome.nix` (a systemd module that NOTA→rkyv-encodes the config in
`ExecStartPre` and runs `criome-daemon <config.rkyv>` with one arg, no flags)
and `nix/tests/criome-node.nix` (a `pkgs.testers.runNixOSTest` that boots it,
asserts the 0600 socket, deploy discipline, key custody, and self-resume). The
design extends this pattern, it does not invent it.

### 4.1 The shape

A nixosTest guest (`pkgs.testers.runNixOSTest`) with one machine running the
three daemons as systemd services, each from its own deploy module mirroring
`criome.nix`:

- `services.criome` — already exists (the module above), set to `ClientApproval`.
- `services.spirit`, `services.router` — siblings authored the same way (NOTA→rkyv
  ExecStartPre, one-arg daemon). router's deploy module sibling is referenced as
  `message-router.nix` in the criome module header; spirit needs one.
- `services.mentci` — the mentci-daemon, configured (via
  `mentci-write-configuration`, `mentci/src/bin/mentci-write-configuration.rs`)
  with typed `ComponentSocket`s pointing at the criome/spirit/router sockets in
  the guest.

The testScript drives the system **through mentci's CLI** (in-VM,
`mentci:state`, `criome:parked`, `criome:approve:<slot>`, etc. from §3.2) and
asserts on the rendered output — the witness-test assertion style
(`criome-client-approval-witness-test.rs`) lifted into the guest. Because the CLI
prints the shared NOTA renderer's output (§3.1), asserting in the testScript also
asserts the GUI's readability.

### 4.2 The motivating end-to-end scenario (the first VM test)

1. Boot guest; `wait_for_unit` for criome (ClientApproval), mentci.
2. Submit an authorization to criome's working socket (the
   `mentci-criome-pickup-witness-test` bin already does exactly this,
   `mentci/src/bin/mentci-criome-pickup-witness-test.rs:46-78`) → criome parks it.
3. `mentci mentci:questions` → assert the parked criome request appears as a
   mentci `ApprovalQuestion` with `source CriomeEscalation` and the slot in its
   context (proves the §1.2 fold and xen8 labeling, readably).
4. `mentci mentci:answer:<question>:approve` → mentci routes the verdict to
   criome's meta socket by slot.
5. `mentci criome:state` / criome `ObserveAuthorization` → assert
   `AuthorizationStatus::Granted` (the §5 half of the criome witness, now driven
   through mentci rather than a bespoke bin).

This single test proves the whole readability+control chain — criome park →
mentci question → psyche verdict → criome grant — end-to-end on a real booted
daemon, and the assertions ARE the readability contract.

### 4.3 Prometheus

`prometheus` is the workspace's smoke-build/VM host (active-repositories.md:134,
the horizon end-to-end smoke target). The nixosTest above needs `/dev/kvm`;
the driver builds/evaluates everywhere but the guest boots on a KVM host —
prometheus is that host. The flake `checks.<system>.mentci-node` runs in CI/eval;
the actual boot+assert run executes on prometheus.

## 5. Worktree recommendations for the build wave

Per kb4k / oust / eh5a, register every worktree in the orchestrate tool and
prefer recycle over new. Recommendations:

- **mentci / mentci-egui / mentci-lib: create fresh feature worktrees.** None
  exist under `~/wt` today — all mentci work was committed directly on the `/git`
  checkouts' main (each is on a detached HEAD at main:
  `git -C …/mentci branch` shows `* (no branch) … main`). New worktrees under
  `~/wt/github.com/LiGoldragon/<repo>/mentci-shared-model-707/` for the §3.1
  re-founding, the §3.2/§3.3 CLI/GUI work, and §3.4 daemon enablers.
- **criome: RECYCLE `criome-nixos-module-142`** (rebase on main) — it already
  carries the VM module + nixosTest the §4 design extends. This is the single
  most valuable existing worktree for this work. `criome-client-approval-witness`
  is also relevant but its content has landed on main (the witness bins are in
  the `/git` checkout); archive it after confirming nothing is unpushed.
- **router / spirit: new VM-module worktrees** (`router-nixos-module-707`,
  `spirit-nixos-module-707`) for the §4.1 deploy-module siblings, unless an
  operator already owns a router transport-test worktree to host it
  (`router/transport-two-kernel-e2e-138` is the closest existing nixosTest home).
- **signal-mentci / meta-signal-mentci: small worktrees** for the §3.5
  cross-import resolution now that signal-standard exists.

The detached-HEAD-on-main state of the mentci `/git` checkouts is itself worth
flagging to Stream B/C: mentci work bypassed the worktree protocol entirely,
which is precisely the gap eh5a closes.

## 6. The smallest first prototype slice

Do these three, in order, before anything else:

1. **Re-found mentci-lib on the live contracts (§3.1).** Delete the
   graph-signal skeleton + duplicate approval types; depend on signal-mentci /
   meta-signal-mentci / signal-criome / meta-signal-criome / signal-standard;
   ship the `ObservationModel` + the one NOTA-fallback renderer + the
   decision-mapping. Nothing else can land cleanly until the shared leg is real.
2. **CLI read+answer atoms (§3.2.1).** Add `mentci:state`, `mentci:questions`,
   `mentci:answer:<q>:<verdict>` to the thin client, printing through the shared
   renderer. This is the smallest thing that makes the criome→mentci→criome chain
   drivable from one command.
3. **The §4.2 nixosTest** (recycling `criome-nixos-module-142`): one guest,
   criome ClientApproval + mentci, the five-step park→question→approve→grant
   scenario, asserted through the CLI. This is the first proof that mentci is a
   readable, correct test-driving surface over a real criome daemon — and the
   template every later spirit/router pane reuses.

The egui live-subscription + approval-card work (§3.3) follows once the shared
model and the daemon stream-push (§3.4) are in; it consumes the same mentci-lib
model the CLI proves, so it lands as rendering, not re-implementation.
