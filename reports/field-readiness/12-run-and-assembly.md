# Field Readiness — RUN & ASSEMBLY Recon (2026-07-02)

Recon worker map for the sustained Fable 5 build/assemble/run/test session.
Scope: can the minimal runnable whole come up and exchange real mail, and where
is the unfinished surface a continuous testing session will hit. Method: read
the persona-system-audit reports (20/21/22), then witnessed bring-up locally
with the repos' own binaries and config tools. All daemons started for this
recon were killed and the sandbox removed. No source was modified.

WITNESSED = observed command output this session. INFERRED = reasoned from
source or prior audit. Repos live at `/git/github.com/LiGoldragon/<repo>`.

## VERDICT

YES — the minimal runnable whole (router + 2×message + harness + persona
supervisor) comes up and exchanges real mail today, but ONLY after rebuilding
every repo's binaries against its own committed lock; the first attempt with
the on-disk binaries failed with a silent typed wire-decode error, which is
exactly the failure class a continuous testing session will hit first.

## ASSEMBLY MAP

### The minimal interactive whole (chat loop) — 4-6 processes

| # | Process | Binds | Speaks | Config authored by |
|---|---------|-------|--------|--------------------|
| 1 | `router-daemon` | `router.sock`, `router-meta.sock` (supervision rides meta) | signal-message ingress, signal-router observation; delivers via fresh `UnixStream` per endpoint | `router-write-configuration` + `router-write-bootstrap` (NOTA → rkyv) |
| 2 | `message-daemon` ×2 (agent A, B) | `<actor>-message.sock`, `<actor>-message-meta.sock` | CLI ingress; stamps SO_PEERCRED origin; forwards signal-message frames to `router.sock` | `message-write-configuration` |
| 3 | `harness-daemon` | `harness.sock`, `harness-supervision.sock` | receives `HarnessRequest::MessageDelivery`; delivers to terminal socket (signal-terminal frame) or spawns `pi --mode rpc` subprocess | NO writer binary — only the harness crate API (see kink K3) |
| 4 | terminal endpoint | `terminal.sock` per agent | signal-terminal `TerminalInputRoot` | e2e uses in-test fixture listeners; the real `terminal-cell` daemon exists but is not built locally |
| 5 | `pi` (external) | stdio JSONL | pi RPC (prompt/steer/follow_up) | in PATH: `/home/li/.nix-profile/bin/pi` (WITNESSED) |

Wiring: message CLI `(Send b [text])` → message-daemon (origin stamp) →
router (adjudicate against bootstrap-granted channel tables, persist to
`router.sema`) → deliver to recipient endpoint → harness → pi. The reply is
NEW mail (async mail objects), never a synchronous return. Channel grants can
ONLY be authored via the bootstrap document — the meta grant vocabulary cannot
grant arbitrary actor channels (`router/src/bin/router_write_bootstrap.rs:102-108`
doc comment, FACT).

### The supervisor plane

`persona-daemon` = manager socket + env-gated `EngineSupervisor`. Bare launch =
manager only. With `PERSONA_PROTOTYPE_STACK_EXECUTABLE` (one binary for all
components) or per-component `PERSONA_<COMP>_EXECUTABLE`, it spawns the
8-component FullPrototype topology [Mind, Router, System, Harness, Terminal,
Message, Introspect, Spirit], creating per component: domain socket,
supervision socket, envelope, `.env`, `<comp>-daemon.rkyv` under
`run/<engine>/`, plus `state/<engine>/` (WITNESSED, see below). Env knobs:
`PERSONA_ENGINE_TOPOLOGY` (default FullPrototype), `PERSONA_MANAGER_ENGINE_ID`
(default "default"), `PERSONA_STATE_ROOT`/`PERSONA_RUN_ROOT` (default beside
manager socket) — `persona/src/transport.rs:468-523`,
`persona/src/launch/configuration.rs:92-134`.

### What already runs on this host (WITNESSED via ps, untouched)

Production (nix): `spirit-daemon`, `agent-daemon`, `lojix-daemon`,
`listener-daemon`, `repository-ledger-daemon`, `orchestrate-daemon`,
`chroma-daemon`. Live spirit answered a read-only `(PublicTextSearch persona)`
with a typed RecordsObserved reply (WITNESSED). The chat-loop components
(router/message/harness/terminal/persona) are NOT deployed — matches audit
24-deploy-path.

Leftover debug daemons from prior demo sessions still running (NOT started by
this recon, left untouched): `criome-daemon` + `mentci-daemon` in
`/tmp/mentci-egui-sandbox` and `/tmp/criome-mentci-spirit-demo-20260701-150210`,
`introspect-daemon` + `mentci-daemon` in `/tmp/mentci-introspect-live-systemd-HUr6mJ`
— the introspect one's own `target/` directory no longer exists on disk.

### Build state of the fabric (WITNESSED)

Built binaries present: message, router, harness, persona, mind, criome,
mirror, spirit, agent. NO target dir: **terminal-cell, system, introspect,
upgrade** (orchestrate: repo target empty; deployed binary in nix profile). A
real-daemon 8-component persona topology therefore cannot start today without
first building terminal-cell/system/introspect.

## BRING-UP WITNESS

### 1. e2e first run: FAILED — silent wire skew from stale binaries

```
cd harness && MESSAGE_CLI_BINARY=… MESSAGE_DAEMON_BINARY=… ROUTER_DAEMON_BINARY=… \
  cargo test --offline --test message_router_harness_e2e
→ router-daemon[working]: daemon signal frame error: rkyv archive deserialization failed
→ panicked: expected SubmissionAccepted, got Error("router socket unreachable; message not forwarded")
```

On-disk binaries were mixed-vintage: message-daemon built Jun 29,
router-daemon linked Jul 1 14:48 from a mid-demo dependency state. The router
could not decode the message-daemon's frame; it dropped the connection without
reply; message mapped EOF to its typed `Unreachable`. The CLI symptom ("router
socket unreachable") misattributes the cause.

### 2. Rebuild against committed locks → e2e PASSES

`cargo build --offline` in message and router re-linked all three binaries to
artifacts matching the current committed locks (message-daemon/message mtime
moved to this session; router-daemon re-linked to a Jun 30 14:03 cache
artifact — i.e. the Jul 1 binary was from a divergent dep state). Rerun:

```
test message_cli_round_trips_between_two_agents_through_one_harness_daemon ... ok  (0.14s)
```

Full loop proven: A `Send` → SubmissionAccepted(1) → routed to B's terminal
fixture → B's reply CLI → slot 2 → delivered back to A. Same binaries
fail-then-pass ⇒ the failure was binary vintage, not code.

### 3. Manual native bring-up: real mail across 4 processes (no cargo test)

Configs authored with each repo's own writer tools (NOTA → rkyv), sandbox
`/tmp/claude-1001/ra` (removed after):

```
router-write-bootstrap "(BootstrapWriteRequest …/bootstrap.rkyv [] [(agent-a 1 None None) (agent-b 1 None None)] [(agent-a agent-b) (agent-b agent-a)])"
router-write-configuration "(ConfigurationWriteRequest …/router.sock …/router-meta.sock …/router-sup.sock …/router.sema (Some …/bootstrap.rkyv) 1001 None local-router None …/router.rkyv)"
message-write-configuration "(ConfigurationWriteRequest …/a-message.sock …/a-message-meta.sock …/router.sock …/a-message.db li 1001 …/a-message.rkyv)"   # and b-…
router-daemon …/router.rkyv &   message-daemon …/a-message.rkyv &   message-daemon …/b-message.rkyv &

MESSAGE_SOCKET=…/a-message.sock message "(Send agent-b [hello from recon])"
→ (SubmissionAccepted 1)
MESSAGE_SOCKET=…/b-message.sock message "(Inbox agent-b)"
→ (InboxListing [(1 li [hello from recon])])
# second send → slot 2; inbox listed both, origin-stamped "li"
```

Real mail end-to-end through the router's sema store, typed replies at every
hop, clean daemon logs. First attempt failed with
`daemon listener error: async listener IO error: path must be shorter than SUN_LEN`
when the sandbox lived under the deep session scratchpad path (kink K5).

Note: the message CLI inbox verb is `(Inbox <recipient>)`; bare `(Inbox)`
returns a typed arity error (`expected Input::Inbox to hold 2 root objects`).

### 4. Persona supervisor: 8-component topology up under fixtures

```
persona-write-configuration "(ConfigurationWriteRequest …/persona.sock …/persona.sema …/persona.rkyv)"
PERSONA_PROTOTYPE_STACK_EXECUTABLE=…/persona-component-fixture persona-daemon …/persona.rkyv &
→ 8 persona-component-fixture children spawned (mind, router, system, harness,
  terminal, message, introspect, spirit), each with domain socket + supervision
  socket + envelope + .env + <comp>-daemon.rkyv under run/default/ and state/default/

PERSONA_SOCKET=…/persona.sock persona
→ (EngineStatusReport (0 Starting [(mind Mind Running Starting) (persona-router Router Running Starting) … 8 entries]))
```

Manager answers over the wire. All 8 components report `Running`; engine and
component readiness stayed `Starting` after ~10s of settling (WITNESSED; cause
not established — fixture handshake depth vs supervision wiring, see K4).
CLI request surface is status/start/stop only; contract-level
`Launch`/`Retire`/`Tap` remain hardcoded rejections
(`persona/src/manager.rs:181-202`, FACT).

### 5. Harness → pi leg

```
HARNESS_LIVE_PI_RPC=1 cargo test --offline --test pi_rpc_live
→ test live_pi_rpc_accepts_prompt_on_low_quant_gemma_moe ... ok  (0.72s)
```

Harness spawned the real `pi` binary in RPC mode and got the delivery receipt
(`harness-1`). CAVEAT: the receipt is prompt ACCEPTANCE, not a model reply; no
local LLM server is running (no llama/ollama/vllm process, nothing on the
usual ports — WITNESSED), so the model-backed reply-as-new-mail leg remains
unwitnessed end to end (K7).

### 6. Cross-repo lock skew is live but currently benign (INFERRED + measured)

Lock diff across harness/message/router: `signal-frame` and `signal-message`
identical everywhere; `signal-router` diverges (harness `277bd153` vs router
`289c7de4`, both `branch=main`) and `signal-harness` diverges (harness
`959b62bd` vs router `0727beb7`). The intervening signal-router commit
`d212ea8` APPENDS a wire field (`attestation_issued_at` on
`RouterPeerAttestation`). Today's e2e passes because the specific types the
harness world writes for the router (config, bootstrap) didn't change between
those revs — the system is one field-append away from cross-world breakage
with the same invisible symptom as §1.

## NOTBUILTYET / STUB SURFACE

Operations returning typed unfinished replies (`NotBuiltYet`,
`NotInPrototypeScope`, `NotImplemented`) — the holes a continuous testing
session will hit. 22 operation-level entries; all path-cited, verified in
source this session.

### Working plane (functional holes)

1. mind `AdjudicationRequest` → `MindRequestUnimplemented{NotInPrototypeScope}` — `mind/src/actors/dispatch.rs:143-145,367-375`. THE channel-adjudication hole.
2. mind `ChannelList` → same — `mind/src/actors/dispatch.rs:143-145`.
3. mind subscription/graph/knowledge fallback arms → `NotInPrototypeScope` — `mind/src/actors/subscription.rs:296-299`, `mind/src/graph.rs:401-404`, `mind/src/knowledge.rs:366-370`.
4. system: every `SystemRequest` except `QueryStatus` → `NotBuiltYet` — `system/src/supervisor.rs:147-155`; CLI mirror `system/src/command.rs:91-97`. Health/readiness hardcoded (`supervisor.rs:175,181`, per audit 22). Focus observation (system's purpose) unbuilt; niri backend exists unwired.
5. harness: every op other than `MessageDelivery`/`WatchHarnessTranscript`/`UnwatchHarnessTranscript` → `NotBuiltYet` — `harness/src/daemon.rs:1105-1111,1146-1149`.
6. harness: cross-harness watch and unknown unwatch token → `NotBuiltYet` events — `harness/src/daemon.rs:841-857`.
7. upgrade: ENTIRE ordinary Input handler → `not_built_yet_output()` — `upgrade/src/execution.rs:183`; sema writes `ReadyToHandover, HandoverCompleted, Mirror, Divergence, RecoverFromFailure, Register, Allow, Block, ForceFlip, Rollback, Quarantine` → `:201-212`; sema reads `AskHandoverMarker, Query` → `:223-230`; placeholders `upgrade/src/placeholder.rs:16,22`. Only `AttemptUpgrade` + `Inspect`/`Report` are real.
8. orchestrate: sema observe_read fallback → `ReadMissReason::NotBuiltYet` — `orchestrate/src/execution.rs:255`; reason enums `orchestrate/src/schema/sema.rs:105,174`; meta round-trip `execution.rs:3225-3241`.
9. agent: `StreamCall`/`CancelStream` → `NotInPrototypeScope` — `agent/src/engine.rs:110-118`. (Real provider also behind default-off `live-provider` feature, per audit 22.)
10. router: raw (unstamped) `Submit` over router socket → `NotInPrototypeScope` — `router/src/router.rs:1830-1832` (scope guard: only daemon-stamped submissions).
11. router: `SubmitStamped` with kind ≠ `Send` → `NotInPrototypeScope` — `router/src/router.rs:2041-2044,2062-2069`.
12. message: public `SubmitStamped` → `NotInPrototypeScope` — `message/src/engine.rs:151-156` (scope guard: stamping is daemon-only).
13. router supervision `Query` → `NotInPrototypeScope` — `router/src/supervision.rs:135-139` (Health/Stop are real).
14. version-projection: `Error::DirectionNotImplemented` — `version-projection/src/projection.rs:46`.
15. persona manager: `Launch` → `LaunchRejected`, `Retire` → `RetireRejected`, `Tap`/`Untap` → `ActionRejected(ComponentNotManaged)` — hardcoded, `persona/src/manager.rs:181-202`.

### Meta/owner plane (reconfiguration unbuilt fabric-wide)

16. message meta `Configure` → `RequestUnimplemented{NotBuiltYet}` — `message/src/meta.rs:146`.
17. harness meta: ALL ops → `NotBuiltYet` — `harness/src/daemon.rs:220-228`.
18. introspect meta: ALL ops → `NotBuiltYet` — `introspect/src/daemon.rs:248-251`.
19. mind meta → `NotBuiltYet` — `mind/src/meta.rs:132-135`.
20. terminal meta `CreateSession`/`RetireSession` → `NotBuiltYet` — `terminal/src/supervisor.rs:616-627`.
21. listener meta CLI → `Error::NotImplemented{"meta-listener CLI"}` — `listener/src/meta.rs:30`.
22. listener: operational errors conflated into `UnimplementedReason::NotBuiltYet` — `listener/src/runtime.rs:312-320` (smell: failure ≠ unfinished).

Net: no daemon in the federation can be live-reconfigured over its meta
socket; system and upgrade are near-total skeletons behind healthy sockets;
mind cannot adjudicate channels. Supervision readiness passes while function
is absent — a testing session must probe OPERATIONS, not socket liveness.

## KINK LEDGER

### K1 — Stale-binary wire skew fails silently at the frame

- What: mixed-vintage `target/debug` binaries across repos produce rkyv
  decode failures at the socket; symptom surfaces as a MISLEADING typed error
  (`router socket unreachable`) on the sender and one stderr line on the
  receiver; nothing crashes.
- Where: any cross-daemon socket; witnessed message→router.
- Blast radius: the WHOLE fabric — any bring-up using prebuilt binaries;
  first thing a testing session hits (it was the first thing this recon hit).
- Likelihood: HIGH (happened on attempt #1; demo work on Jul 1 left a
  divergent router binary on disk).
- Proposed fix: (a) cheap: a bring-up preflight script that runs
  `cargo build` per participating repo before spawning anything;
  (b) bead: a wire-schema fingerprint in the signal-frame hello/envelope so a
  vintage mismatch is a TYPED, named rejection instead of ArchiveDeserialize.
- Class: (a) cheap-safe; (b) needs-a-bead.
- Evidence: §Bring-up witness 1-2; binary mtimes; fail→relink→pass on
  identical sources.

### K2 — Cross-repo Cargo.lock drift on shared wire contracts

- What: same `branch=main` contract pinned at different commits across
  consumers (`signal-router` 277bd153 vs 289c7de4; `signal-harness` 959b62bd
  vs 0727beb7). Commit `d212ea8` shows wire fields DO get appended.
- Where: `harness/Cargo.lock` vs `router/Cargo.lock` (measured); audit 20
  found the same pattern fabric-wide plus mind's ssh-pinned revs.
- Blast radius: any cross-world-authored artifact (configs, bootstraps,
  frames); breakage mode is K1's silent decode failure.
- Likelihood: MEDIUM today (current types compatible — e2e passes), HIGH over
  a multi-day session as contracts move.
- Proposed fix: lock-sync sweep (`cargo update -p <contract>` in every
  consumer, commit) + a CI-ish check script that diffs LiGoldragon rev pins
  across repo locks (the diff took one awk line this session).
- Class: check script cheap-safe; the sweep needs-a-bead (commits across many
  repos, must land producers before consumers).
- Evidence: §Bring-up witness 6; lock diffs in this session.

### K3 — Channel adjudication loop is bootstrap-only

- What: dynamic channel admission does not exist: router parks unknown
  channels in an unwired in-memory pull-only outbox, mind answers
  `NotInPrototypeScope`, and the deployable bootstrap is the ONLY authoring
  path for actor-to-actor grants (its own doc comment says so).
- Where: `mind/src/actors/dispatch.rs:143-145`, `router/src/adjudication.rs`
  (audit 22), `router/src/bin/router_write_bootstrap.rs:102-108`.
- Blast radius: every conversation topology must be fully pre-declared in the
  bootstrap rkyv before router start; no runtime channel changes; violates
  push-not-pull.
- Likelihood: CERTAIN for any test beyond the pre-granted pair.
- Proposed fix: bead — build mind `AdjudicationRequest` handling + a router
  push (or mind pull drain) + `ApplyMindChannelGrant` return path; interim
  cheap mitigation: testing sessions generate bootstrap grants exhaustively
  for their planned actor set.
- Class: needs-a-bead (interim mitigation cheap-safe).
- Evidence: audit 22 (source-cited) + bootstrap writer doc comment verified
  this session; my manual bring-up worked only because grants were
  pre-declared.

### K4 — Persona readiness never leaves Starting under bare fixture launch

- What: all 8 supervised fixture components report `Running` health but
  component and engine readiness stayed `Starting` (~10s observation window).
  Either the fixture doesn't complete the readiness handshake or the
  supervision readiness path needs something a bare launch doesn't provide.
- Where: `persona-daemon` + `persona-component-fixture`; status via persona
  CLI (`(EngineStatusReport (0 Starting …))`).
- Blast radius: a testing session gating on Ready will wait forever; also
  means "supervision green" is not yet a usable health gate.
- Likelihood: HIGH for anyone using the fixture stack as scaffolding.
- Proposed fix: cheap first: read `persona/tests/engine.rs` to learn what
  drives Ready and whether bare launch is expected to converge; bead if a
  real handshake gap emerges.
- Class: investigation cheap-safe; fix unknown until diagnosed.
- Evidence: §Bring-up witness 4 (WITNESSED status output; cause INFERRED
  unknown).

### K5 — SUN_LEN: deep runtime roots break every daemon

- What: Unix socket paths >~104 bytes fail bind with
  `path must be shorter than SUN_LEN`. The session scratchpad path is already
  too deep; any tempdir-per-test nesting can cross the limit.
- Where: all daemons (triad-runtime async listener); witnessed on router and
  message.
- Blast radius: test harnesses and sandboxes with generated deep paths;
  confusing first-contact failure.
- Proposed fix: cheap: document the short-run-root convention (e.g.
  `/tmp/<lane>/`) in the testing session's brief; bead (optional):
  triad-runtime could bind relative to a dirfd/chdir to lift the limit.
- Class: convention cheap-safe; runtime change needs-a-bead.
- Evidence: §Bring-up witness 3 (exact error observed).

### K6 — Chat-loop components lack deployment surface AND (harness) a config writer

- What: no NixOS/home modules for persona/mind/message/harness/terminal/
  system/introspect (audit 24, unchanged); additionally `harness` has NO
  `harness-write-configuration` binary target at all (Cargo.toml [[bin]] list:
  harness, meta-harness, harness-daemon, harness-claude-artifact-observer-test)
  — its config can only be authored from Rust via the harness crate, so even a
  hand-rolled module or script cannot configure it today. message/router/
  persona/mind/criome/mirror/spirit/agent all have writer binaries.
- Blast radius: no systemd/persona-supervised deployment of the interactive
  loop; manual bring-up of harness requires writing rkyv from a Rust program
  (in practice: only `cargo test` fixtures).
- Proposed fix: bead: add `harness-write-configuration` (mirror the message
  writer, ~150 lines by pattern); then the persona-supervised or systemd
  deployment beads from audit 02 become executable.
- Class: needs-a-bead.
- Evidence: bin list read this session; audit 24 for the module absence.

### K7 — Model-backed reply leg unwitnessed (no LLM backend up)

- What: harness→pi RPC handshake is real (receipt witnessed) but no local
  LLM server is running, and the full loop "delivered prompt → model reply →
  reply enters as new mail via B's message CLI" is not exercised by any
  committed test with real daemons.
- Where: `pi` provider `criomos-local` (default in `harness/tests/pi_rpc_live.rs`);
  CriomOS has an `llm.nix` module (audit 20) but nothing listening here.
- Blast radius: the demo goal ("agent B (model) replies") — last leg of the
  minimal whole.
- Proposed fix: bead: bring up the llm service (or point pi at a reachable
  provider), then run the harness e2e with `HarnessKind::Pi` +
  `pi_rpc_adapter` configured instead of terminal fixtures.
- Class: needs-a-bead (environment + a real-daemon full-loop witness).
- Evidence: §Bring-up witness 5; process/port scan.

### K8 — Missing built binaries for three topology members

- What: terminal-cell, system, introspect (and upgrade) have no target dir;
  the real 8-component persona topology cannot start; system/introspect are
  skeletons anyway (see stub list), terminal-cell is real code but unbuilt.
- Proposed fix: cheap-safe: `cargo build` in terminal-cell (real, needed for
  real PTY delivery); building system/introspect is cheap but yields
  status-only skeletons.
- Class: cheap-safe (build); the function gaps behind them are separate beads
  (stub list #4, #18).
- Evidence: target-dir scan this session.

### K9 — Field hygiene: orphan demo daemons from prior sessions

- What: criome/mentci/introspect debug daemons from Jun 30-Jul 1 demos still
  running against /tmp sandboxes; one binary's target dir no longer exists.
  Not cleaned by this recon (not mine; may hold state someone wants).
- Blast radius: socket-path and state collisions for a new testing session;
  confusing `ps` output.
- Proposed fix: cheap-safe after psyche confirmation: inventory + kill +
  remove sandboxes; testing session should own sandbox lifecycles (pids file,
  trap cleanup) as this recon did.
- Evidence: ps scan (§Assembly map).

## UNKNOWNS / NOT CHECKED

- Why persona readiness stays `Starting` (K4) — persona/tests/engine.rs not
  read this session.
- Whether the e2e passes with a REAL terminal-cell daemon instead of fixture
  listeners (terminal-cell unbuilt locally).
- The pi→model reply leg (K7) and harness `HarnessKind` behavior with a real
  `pi_rpc_adapter` config.
- mind/orchestrate/upgrade daemons were not brought up live; their stub
  citations are source-verified only.
- The identity of the one fixture child spawned without a config argument
  (pid pattern suggests mind); not traced.
- Production daemons (spirit etc.) were only touched with one read-only query.
