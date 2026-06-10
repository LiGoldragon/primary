---
title: 87 — triad_main landed on main + cloud multi-listener pilot complete
role: system-designer
variant: Contextualization
date: 2026-06-06
topics: [triad-main, component-migration, schema-rust-next, daemon, scoreboard, cloud-pilot, message, terminal-control, emitter-grammar, bare-name-vs-pair, working-socket-mode, ug6i]
description: |
  Merge of reports 80 + 81 (same day, same arc). triad_main — the EMITTED
  daemon module (src/schema/daemon.rs) — landed on main across schema-rust-next,
  triad-runtime, and spirit, with spirit + message migrated and cloud the
  multi-listener pilot. Carries: the intent-record reframe table, the migration
  scoreboard (as of 2026-06-06; current fleet state now lives in reports 85/86),
  the corrected per-component recipe (the durable form is in
  skills/component-triad.md), how reports 74-79 stand, the COMPLETE cloud port,
  and two cross-fleet emitter findings (working-socket mode is not
  emitter-configurable; the bare-name→pair enum grammar shift makes ug6i
  staleness fleet-wide).
---

# 87 — triad_main landed; cloud pilot complete

> Merge of reports 80 (triad_main scoreboard) and 81 (cloud pilot findings),
> both 2026-06-06, one arc. The *current* fleet migration state (criome the
> last daemon, five contracts still hand-written) lives in reports **85**
> (`85.4` execution log) and **86** (handover); this report is the 2026-06-06
> landing snapshot and the design rationale behind it. The durable per-component
> recipe lives in `skills/component-triad.md`.

## The central fact — triad_main integrated to main

`triad_main` — the EMITTED, source-visible `src/schema/daemon.rs` (NOT a literal
macro, per `lnhj` / report 542) — landed on main, resolving the prior session's
central uncertainty (it had been green on `designer-daemon-emit-2026-06-06`
branches but not on main, and a stray codec fix had forked schema-rust-next
main). Both are resolved:

- **schema-rust-next main** — `33337d74` (token-based daemon emitter) +
  `b75c7f50` (deliver disambiguation) + `6685e7b3` (ConnectionContext into
  `handle_working_input`). The stray codec fix `799f6787` (emit the basic frame
  codec for wire-facing targets incl WireContract) is in the ancestor chain on
  main — integrated cleanly, no divergence.
- **triad-runtime main** — `33b9531a` ConnectionContext; + `DaemonConfiguration`
  trait, `ExitReport`, `BoundedWorkers` (`k6w1`).
- **spirit main** — `d406d198` (land triad_main pilot — emitted daemon) +
  `bd04eac7` (thread ConnectionContext). Spirit is the proven pilot per report
  542: one-line bin (`SpiritDaemon::run_to_exit_code()`); `src/daemon.rs` is
  ONLY the `impl ComponentDaemon for SpiritDaemon` escape hatch (209 lines);
  `src/schema/daemon.rs` is emitted.

## Intent refresh — the records that reframe the work

| Record | Kind | What it settles |
|---|---|---|
| **ocu7** | Decision | THE migration directive: mind, message, orchestrate, router, terminal-control, spirit (pilot done), persona migrate onto triad_main + the Signal/Nexus/SEMA engine traits. triad_main audited + obvious flaws fixed as migration proceeds. |
| **lnhj** | Decision | Captures report 542: triad_main! is an EMITTED source-visible `src/schema/daemon.rs`, not a literal macro. Streaming is Option B (emitter generates pub/sub wiring from declared `Schema::streams()`). |
| **g3ax** | Decision | The emitted spine threads per-connection `ConnectionContext` (SO_PEERCRED via `UnixStream::peer_cred`) into `handle_working_input`, so message/router/persona mint origin tags from peer credentials. The spine had regressed message origin to a constant Owner tag; now fixed (landed on main). |
| **1g8y** | Clarification | Corrects report 79: terminal-control maps to the EXISTING `terminal` repo — migrate `terminal`. No separate terminal-control component to create. |
| **k6w1** | Principle | Daemon connection-concurrency (bounded thread-per-connection worker) belongs in triad-runtime, reused by every daemon. Realized: `triad-runtime/src/workers.rs` `BoundedWorkers`; lojix already consumes it. |
| **2alg** | Decision | lojix serves connections concurrently; per-request in-flight state; durable Store is the brief-locked shared point; long nix effects hold no global lock; bounded by a permit cap. |
| **ug6i** | Principle | Contract Rust is ALWAYS regenerated from schema; stale artifacts are a failure; `write_or_check` freshness gate must run fleet-wide. |
| **3nqt / 8bea / tdsu** | Correction/Principle | Auto-retry transient errors (529, connection-close, the subagent-no-StructuredOutput hiccup) — main agent AND dispatched work. |
| **3pfh** | Decision | spirit archive (meta-signal Configure ArchiveTarget) is redirect-forward-only — re-points future writes/reads; prior records stay put. |
| **own9** | Correction | The entire at-binder surface is abandoned in nota-next; authored surface is the positional bracket/brace form. |

## The migration scoreboard (snapshot 2026-06-06; current state in 85/86)

| Component | State (2026-06-06) | Detail |
|---|---|---|
| schema-rust-next | ✅ emitter landed | token-based daemon emitter on main; codec fix integrated; ConnectionContext hook |
| triad-runtime | ✅ shells landed | `BoundedWorkers` (k6w1), `DaemonConfiguration`, `ExitReport`, `ConnectionContext`, listener shells, `Runner::drive` |
| spirit | ✅ migrated (pilot) | single-listener; emitted daemon + `impl ComponentDaemon`; one-line bin; streaming Option-B emitted |
| message | ✅ migrated | single-listener (`NexusDaemonShape::new(message-daemon, signal)`); peer-cred origin via g3ax. BUT stateless — `alom` existence-log NOT built |
| lojix | ◑ partial | consumes `BoundedWorkers` (k6w1); still hand-written `triad-port/src/daemon.rs` |
| cloud | ✅ COMPLETE (see below) | was WRONG-SHAPE on 06-06 morning; full multi-listener triad_main port landed `4a378d37` |
| orchestrate | ✗ todo | hand-written `src/daemon.rs` (ocu7 / `82 §5`) |
| domain-criome | ✗ todo→done | hand-written daemon then; emitted by the time of 85 |
| router | ✗ todo | g3ax names it a peer-cred origin minter |
| mind | ✗ todo | INTENT only then |
| terminal (=terminal-control, 1g8y) | ✗ todo | INTENT only then |
| persona | ✗ todo | concept schema only then |

**Current state supersedes this table:** per report 85 (`85.4` schema-emission
section) every component daemon is emitted EXCEPT criome (now done in the 85
session), and per report 86 five hand-written contracts remain
(`signal-{system,introspect,spirit,mind,harness}`).

## The corrected per-component recipe (durable form: skills/component-triad.md)

The pre-triad_main recipe (report 77 — hand-write a ~190-line daemon shell) is
SUPERSEDED. What spirit and message actually did:

1. **Declare a `NexusDaemonShape` in `build.rs`** — process name + listener
   tier(s). Single-listener:
   `NexusDaemonShape::new("x-daemon", WorkingListenerTier::new("signal"))`.
   Multi-listener (cloud): add the meta/owner tier.
2. **Turn on the daemon emitter** — `src/schema/daemon.rs` is generated +
   freshness-checked by the same `write_or_check` gate guarding signal/nexus/sema.
3. **Hand-write only `impl ComponentDaemon`** — the record-1488 escape hatches:
   `type Configuration/Engine/Error`, `PROCESS_NAME`, required `build_runtime`
   (open the Store/Engine), `handle_working_input` (one Input → one Output,
   taking `&ConnectionContext` per g3ax), optional owner/meta hatch + stream
   filter/event policy.
4. **Bin is a one-liner** — `XDaemon::run_to_exit_code()`.
5. **Delete** the hand-written `DaemonCommand`/`Daemon`/`*DaemonRuntime`/generic
   `DaemonError`/hand-rolled SubscriptionHub — all emitted now.

The only real per-component decision is single-vs-multi listener and what
`build_runtime` opens.

## How reports 74-79 stand

- **74 (engine-forward exploration)** — the SAFE-NOW port set and critical-path
  framing; the runner spine it sequences has since landed (this report). Port
  maps remain useful design context.
- **75 (message/router/orchestrate production roadmap)** — the three port maps +
  the 37-rule rulebook + the meta-signal rename prerequisite. Still the design of
  record for those three ports.
- **76 (message↔router overlap)** — holds. message is the SO_PEERCRED trust
  boundary; g3ax confirms it operationally. Keep separate. ✓
- **77 (port recipe + per-component plans)** — recipe section SUPERSEDED by the
  corrected recipe above; per-component roadmap subsumed by the scoreboard +
  reports 85/86.
- **78 (terminal raw-data-plane carve-out)** — DISSOLVED (self-banner'd);
  terminal-cell is a library/binary, not a daemon (confirmed in 85's component
  list).
- **79 (terminal-layer decomposition → terminal-control)** — refined by 1g8y
  (terminal-control is the EXISTING `terminal` repo, no new component) but the
  systemd+sema reattach decomposition (Spirit `ckhx`/`5fd6`/`bcca`) STANDS as
  adopted design — kept.

## The cloud multi-listener pilot — COMPLETE

**STATUS: COMPLETE (2026-06-06, psyche chose "grind the full port now").** The
full cloud port landed on main, green end-to-end (build all-targets + clippy -D
+ all tests, incl. live `schema_daemon` socket tests driving both tiers over
real Unix sockets through the emitted daemon). Landed commits:

- schema-rust-next `98fbb369` (dependency-contract working tier) + `2c3c162d`
  (gate emitted `try_clone_stream` behind `emits_stream` — no dead code in
  non-streaming multi-listener daemons).
- signal-cloud `27d7056e` (regen) + `0ff53ff2` (Observation → pair form,
  restoring the tuple wire contract the bare-name regen had silently broken).
- meta-signal-cloud `abce145f` (regen; unaffected — body enums already unit/root).
- cloud `4a378d37` — schema pair-form migration (nexus + sema), `schema_role.rs`
  deleted (role impls now emitted), triad-runtime bumped,
  `SchemaRuntime::reply_to_signal` (per-request execute on the engine noun),
  `schema_daemon.rs` rewritten to `impl ComponentDaemon for CloudDaemon` + a thin
  `SchemaDaemon` wrapper. Legacy `daemon.rs` (Cloudflare-IO) + the `cloud-daemon`
  bin unchanged (the live-IO effect-plane port is separate).

### What landed (independently valuable)

1. **Daemon emitter supports dependency-crate working contracts**
   (schema-rust-next `98fbb369`). `WorkingListenerTier::dependency(path)` emits
   `use signal_cloud::schema::lib::{Input, Output, SignalFrameError}` instead of
   crate-local-only. Local case byte-identical (6 daemon goldens + full suite +
   clippy -D green). cloud now emits a correct two-tier `src/schema/daemon.rs`
   (dependency import, working+meta bind, ComponentDaemon trait, DaemonEntry
   one-liner entry).
2. **signal-cloud regenerated** against the current emitter — was stale (ug6i).
3. **meta-signal-cloud regenerated** against current emitter + fresh signal-cloud
   — was stale (ug6i).

### The emitter shift the cloud regen exposed (the real story)

Regenerating cloud against the current emitter + fresh contracts exposed 34
errors that have nothing to do with the daemon — a broad emitter shift cloud's
stale artifacts had hidden:

1. **Enum declaration grammar changed: bare name = unit variant** (the root of
   ~25 errors).

   | Schema declaration | Old emission | New emission |
   |---|---|---|
   | `ReadInput [Observe ObservePlan Validate]` (bare names) | tuple variants `Observe(Observation)` | **unit variants** `Observe` + `pub type Observe = Observation` |
   | `ReadInput [(Observe Observe) (Lookup Lookup)]` (pairs) | tuple variants | tuple variants `Observe(Observe)` |

   cloud's `sema.schema`/`nexus.schema` use the bare-name form, so every
   payload-carrying variant regenerated as a UNIT variant — and cloud's
   hand-written engine (`schema_runtime.rs`, 491 lines) constructs/matches them
   as tuples, so it no longer compiles. spirit (the canonical pilot) uses the
   PAIR form and compiles. **The pair form is the current grammar; bare-name
   schemas must migrate.**
2. **NexusEngine trait surface changed** (4 × E0407) — `apply_sema_write` /
   `observe_sema_read` / `run_effect` / `budget_exhausted_reply` are no longer
   members of the emitted `nexus::NexusEngine`; stale impls must reconcile.
3. **Role-marker impls now emitted** (5 × E0119) — the emitter emits
   `impl triad_runtime::NexusWork for NexusWork {}` etc. inline; cloud's
   `schema_role.rs` (the report-77 SOFT bridge) now duplicates — delete it.
4. **triad_runtime pin too old** (3 × E0432/E0425) — the emitted daemon.rs
   imports `ConnectionContext`/`DaemonConfiguration`/`ExitReport`; bump to main.

The remaining cloud port was therefore a real multi-file engine port (migrate
bare-name→pair enums, regenerate, delete `schema_role.rs`, bump triad_runtime,
reconcile `schema_runtime.rs`, retire `schema_daemon.rs` → thin
`impl ComponentDaemon` + one-line bin with the per-request execute helper moved
onto `SchemaRuntime`) — all of which landed in `4a378d37`.

## Two cross-fleet findings beyond cloud (open follow-ups)

- **Working-socket mode is not emitter-configurable.** The emitted
  multi-listener bind applies the *meta* socket mode (owner-only) but binds the
  *working* socket at default umask mode — no knob. Report 76's security
  partition (message.sock = 0660 external door vs router.sock = 0600 owner-only)
  is a real distinction; message migrated onto the emitted daemon, so its
  working socket is now default-mode unless handled elsewhere. Candidate fix: a
  `WorkingListenerTier` socket mode + a `working_socket_mode()` on the
  `DaemonConfiguration` trait, symmetric with the meta tier. **(Belongs in
  schema-rust-next / triad-runtime emitter design — migrate-flagged.)**
- **ug6i staleness is fleet-wide, not cloud-local.** The bare-name→unit grammar
  shift and the role-marker-impl emission mean EVERY component carrying
  hand-written engine code or schemas in the old grammar breaks on regeneration
  the same way cloud did. The `write_or_check` freshness gate catches stale
  *output* but not stale *grammar*; a fleet regeneration sweep is the real ug6i
  closure. **(This is the through-line into the NOTA-free / schema-emission arc
  that reports 85/86 carry forward.)**

## Lane note

ocu7's ports land on main in code repos (operator-owned per 6xzu); spirit +
message were operator work. cloud's multi-listener retirement was the designer
pilot (542 names it), proving multi-listener emission the way spirit proved
single.
