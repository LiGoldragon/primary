# 140 — phase 3 actor + supervision audit (2026-05-16)

Role: operator-assistant
Branches: `main` only (phase-3 fanout discipline)
Scope: workspace-wide actor/supervision discipline audit + consolidation
pass after phase-1 (component gap-closes) and earlier phase-3 slices
(/135, /136, /137, /138, /139) landed. AUDIT not REIMPLEMENT —
reconciled ARCH/skills.md where stale, added missing architectural-
truth witnesses where /138's kameo gap and /91's user-settled
subscription lifecycle hadn't yet reached.

## TL;DR

Twelve commits across eight repos. Two workspace skills carry the
load-bearing /138 kameo gap finding (`spawn_in_thread` releases
`wait_for_shutdown` before `Self::drop()` runs) so every state-bearing
component that wants Template 2 sees the gap before adopting it.
One per-repo ARCH reconciled (persona-system §1.5, drops the "Path A
reply-side only" overcorrection that pre-dates /91). Nine per-repo
witness tests (`no-zst-actor` and `no-shared-locks` source scans)
landed in the repos that didn't already carry both — persona,
persona-router, persona-harness, persona-terminal, persona-introspect,
persona-system, persona-message, terminal-cell, criome.
persona-mind already carries the source-scan equivalents in
`tests/weird_actor_truth.rs` (per /138 + earlier).

Two designer-facing escalations surfaced during the audit; both
documented inline in the relevant repo's witness file and in §"Designer
escalations" below.

| # | Repo | Commit subject |
|---|---|---|
| 1 | primary | skills/kameo: warn that supervised spawn_in_thread leaks file locks past wait_for_shutdown |
| 2 | primary | skills/actor-systems: surface supervised spawn_in_thread gotcha and parallel multi_thread restart hang |
| 3 | persona-system | ARCH: reconcile focus subscription close with user-settled lifecycle (request + reply ack) |
| 4 | criome | tests: witness no-zst actors and no-shared-locks across actor source |
| 5 | persona-introspect | tests: witness no-zst actors and no-shared-locks across actor source |
| 6 | terminal-cell | tests: witness no-zst TerminalCell and no-shared-locks in library source |
| 7 | persona-system | tests: witness no-zst actors and no-shared-locks across actor source |
| 8 | persona-message | tests: witness no-zst actors and no-shared-locks across actor source |
| 9 | persona-harness | tests: witness no-zst actors and no-shared-locks between actors |
| 10 | persona-router | tests: witness no shared locks between actors via source scan |
| 11 | persona-terminal | tests: witness no-zst public actor nouns |
| 12 | persona | tests: witness no-zst actors and no-shared-locks across actor source |

All commits pushed to `origin/main` per the `jj`-canonical flow.

---

## 1. What I audited

For each in-scope component repo, I audited the ARCH and the skills.md
against the actor-discipline rules from /90 §1/§2/§9 (designer-
assistant's critique), /91 (user-settled subscription lifecycle +
daemons-no-env-var + persona-system paused + signal-core stable
reference), /134 (manager phase-1), /131 (router phase-1), /137 (phase-3
event-sourcing + restart witnesses), /135 (phase-3 push subscription
chains), /136 (phase-3 terminal control/data plane), and /138 (mind
phase-1 + the kameo gap discovery).

Per-repo audit rubric:

1. Are all named actors data-bearing (no ZST actors)?
2. Is supervision tree explicit in ARCH (parent/child + restart policy
   + restart_limit)?
3. Are blocking-plane templates documented (Template 1/2/3 selection
   per `~/primary/skills/kameo.md`)?
4. Are `*Phase` carve-out actors named correctly (NOT `*Supervisor`
   if they don't supervise children)?
5. Are restart-from-Args reconstruction semantics described per
   state-bearing actor?
6. Is the child-exit observation path documented (per Erlang link
   pattern, per /134's manager implementation)?
7. Are there architectural-truth witnesses for: topology manifest,
   trace-pattern, forbidden-edge, no-blocking-handler, no-zst-actor,
   actor-count, no-shared-locks?

| Repo | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| persona | ✓ | ✓ | (Template 1 in router; manager uses unsupervised `spawn_in_thread`) | ✓ | ✓ ARCH §1.7 manager restore | ✓ ARCH §1.7 watcher-task-per-child | ✓ + added /140 |
| persona-mind | ✓ | ✓ | ✓ destination Template 2 / current spawn (per /138) | ✓ `ReplyShaper` not `ReplySupervisor` | ✓ | n/a (mind has no children to launch) | ✓ already (weird_actor_truth.rs) |
| persona-router | ✓ | ✓ | ✓ Template 1 on `HarnessDelivery`; `spawn_in_thread` on non-supervised path | ✓ | partial — `MindAdjudicationOutbox` in-memory transitional | n/a | size_of ✓; no-shared-locks added /140 |
| persona-harness | ✓ | ✓ | n/a | ✓ `SupervisionPhase` | ✓ | n/a | ✓ added /140 (with sink carve-out) |
| persona-terminal | ✓ | ✓ | n/a | ✓ `SupervisionPhase` | ✓ | n/a | size_of ✓ /140; no-shared-locks ✓ already (actor_runtime_truth.rs) |
| terminal-cell | ✓ (one actor: TerminalCell) | partial (daemon binary still owns shared Arc<Mutex> — see escalation #1) | n/a | n/a | ✓ | ✓ child-exit watcher | ✓ added /140 (library scope) |
| persona-introspect | ✓ | ✓ | n/a | ✓ `SupervisionPhase` | ✓ | n/a | ✓ added /140 |
| persona-system | ✓ (paused) | ✓ | n/a | ✓ `SupervisionPhase` | ✓ | n/a | ✓ added /140 |
| persona-message | ✓ | ✓ (stateless) | n/a | ✓ `SupervisionPhase` | n/a (stateless daemon) | n/a | ✓ added /140 |
| criome | ✓ | ✓ | ✓ Template 1/2 named for BLS sign/verify | n/a | ✓ | n/a | ✓ added /140 |

---

## 2. Workspace skills update (load-bearing /138 finding)

The mind continuation /138 discovered a Kameo 0.20 shutdown-ordering
gap: when a supervised state-bearing actor (`StoreKernel`) spawns via
`.spawn_in_thread()`, the parent's `wait_for_shutdown` returns the
moment `notify_links` drops `mailbox_rx`, **before** the actor's
`Self` value (which owns the redb `Database` and the file lock) is
dropped. The next daemon's `bind()` races the still-held lock and
fails with `Io(UnexpectedEof)` or hangs.

This is load-bearing because Template 2 — dedicated OS thread for
frequent sync work — is the **destination** shape for every redb-
backed store in the workspace (mind's `StoreKernel`, persona's
`ManagerStore`, router's `ChannelAuthority` once it persists, every
future state-bearing daemon). Until upstream Kameo grows a hook that
fires after `Self` is dropped, every state-bearing actor with a
supervisor stays on `.spawn()`.

Two skill commits land the finding at the right level:

### 2.1 · `skills/kameo.md` (commit 1)

Added a §"Blocking-plane templates" Template 2 warning naming the
exact failure mode, citing the live `persona-mind/src/actors/store/mod.rs:295-307`
comment block and the /138 report. The narrow carve-out is preserved:
the non-supervised `Self::spawn_in_thread(self)` shape (call after
building `Self`, no parent supervisor) is fine for processes that
exit on their own clock; the trap is `supervise(&parent, …).spawn_in_thread().await`.

Added two anti-patterns to §"Anti-patterns and gotchas":

- **Supervised `spawn_in_thread` releases `wait_for_shutdown` before
  `Self::drop()` runs.** Cross-references Template 2.
- **`#[tokio::test(flavor = "multi_thread")]` + parallel restart
  tests.** Even with `.spawn()`, multi-thread + parallel-runner
  combination hangs restart tests. Single-thread `#[tokio::test]`
  (default) passes the same tests in parallel. Surfaced by /138
  §"Found by accident".

### 2.2 · `skills/actor-systems.md` (commit 2)

Added §"Supervision gotcha — Template 2 on a supervised state-bearing
actor" inside §"Blocking is a design bug" to surface the gap at the
architectural-discipline level. Cross-references kameo.md for
mechanics and /138 for the failure trace.

Added §"Anti-pattern — `flavor = "multi_thread"` on parallel daemon-
restart tests" inside §"Test actor density".

---

## 3. ARCH reconciliation — persona-system §1.5 (commit 3)

`persona-system/ARCHITECTURE.md` §1.5 ("Paused-state skeleton") still
carried the /195 overcorrection:

> Path A discipline applies when unpausing. Focus subscription close
> is a reply-side `SystemReply::SubscriptionRetracted { subscription_id,
> reason }` event, not a request-side `FocusUnsubscription`.
> [...] Today's `FocusUnsubscription` variant is treated as a deferred
> decoded-and-unimplemented shape; the contract change to a reply-side
> retraction lands together with the live event-stream wiring.

This is doubly stale:

1. The `signal-persona-system` contract already has the user-settled
   lifecycle landed at `src/lib.rs:303-330` —
   `Retract FocusSubscriptionRetraction(FocusSubscriptionToken)` is a
   first-class request variant, `SubscriptionRetracted(SubscriptionRetracted)`
   is a first-class reply variant, and the `signal_channel!` `stream`
   block's `close FocusSubscriptionRetraction` line emits the typed
   `closed_stream()` discriminant. The contract change has shipped.
2. Per /91 §2, retraction is **BOTH** request + final reply ack —
   not reply-side only. The /195 overcorrection /91 settled.

Replaced with the canonical five-state FSM citation
(`~/primary/skills/subscription-lifecycle.md`) and named the kernel
grammar enforcement point. Renamed the variant reference in the §1.5
bullet list from `focus subscription, focus unsubscription, focus
snapshot` to `FocusSubscription, FocusSubscriptionRetraction,
FocusSnapshot` to match contract spelling.

---

## 4. Witness additions (commits 4–12)

Workspace-level discipline says every state-bearing actor noun must
carry data (no public ZST actor markers) and no `Arc<Mutex<T>>` /
`Arc<RwLock<T>>` shared-lock state between actors. Per phase-1 /
phase-3 inventory:

- **`mem::size_of::<MyActor>() > 0` (no-zst-actor):** persona-router
  has this in `actor_runtime_truth.rs::public_control_records_cannot_be_zero_sized`.
  persona has it for `EngineManager` only (in `manager.rs`).
  persona-mind has the source-scan equivalent
  (`actor_adapter_markers_cannot_be_public_zst_nouns`).
- **No-shared-locks source scan:** persona-mind has
  `actor_source_cannot_hide_shared_locks_or_polling_waits` covering
  `Arc<Mutex`, `Arc < Mutex`, `RwLock`, blocking sleeps, polling
  intervals. persona-terminal has
  `terminal_signal_control_state_is_owned_by_a_kameo_actor` covering
  `Arc<Mutex` and `std::sync::Mutex`.

Every other in-scope repo was missing at least one of the two. Added
the missing witness(es) per repo as one logical commit each. The
canonical witness shape:

```rust
#[test]
fn public_actor_nouns_carry_data() {
    assert!(std::mem::size_of::<MyActor>() > 0);
    // ... per declared actor
}

#[test]
fn actor_source_does_not_share_locks_between_actors() {
    // scan src/**, skip // comment lines, look for Arc<Mutex / Arc < Mutex / RwLock,
    // optionally skip narrow documented carve-outs
}
```

Carve-outs surfaced during the audit:

- **persona-harness `TranscriptSubscriptionSink`** (`src/subscription.rs:74`)
  uses `Arc<Mutex<TranscriptSubscriptionSinkInner>>` as a per-consumer
  back-pressure primitive. Its source doc comment explicitly names it
  as test/prototype scaffolding to be replaced by a real socket-writer
  actor in production daemons (per /135 §"Daemon-socket streaming
  layer (router → harness subscription)"). The witness skips that
  specific line; the destination shape doesn't yet ship.
- **persona `DirectProcessLauncher::StopHandoff`** (`src/direct_process.rs:128-129`)
  uses `Arc<Mutex<Option<oneshot::Sender<StopComponentReceipt>>>>` as
  a single-actor coordination handoff between the launcher's mailbox
  and the watcher task. The doc comment immediately above explicitly
  names the constraint it satisfies ("not Arc-Mutex-as-ownership
  between two actors"). The witness skips that specific type
  declaration line.
- **terminal-cell-daemon binary**
  (`src/bin/terminal-cell-daemon.rs:196`) uses
  `Arc<Mutex<TerminalSignalControlState>>` for prompt-pattern registry
  sharing across socket-accept-loop tasks. This is **real drift** from
  the destination shape (the persona-terminal ARCH §1.5 names
  `TerminalSignalControl` as a Kameo actor in `persona-terminal`,
  not a shared lock in the terminal-cell daemon binary). The witness
  scopes to `src/**` excluding `src/bin/`; the drift is surfaced as
  designer escalation #1 below.

---

## 5. Designer escalations

### 5.1 · terminal-cell-daemon shared-lock drift

`terminal-cell/src/bin/terminal-cell-daemon.rs` carries an
`Arc<Mutex<TerminalSignalControlState>>` (lines 123, 196, 205, 318,
398, 407) that the daemon's control-plane accept loop locks on every
signal-control request. This pre-dates the persona-terminal ARCH
§1.5 destination shape (control-plane lives in `persona-terminal`
behind the `TerminalSignalControl` Kameo actor) and the operator/136
phase-3 terminal control/data plane split.

Two resolution paths:

1. Move `TerminalSignalControlState` into a Kameo actor inside
   `terminal-cell` (parallel to the existing `TerminalCell` actor),
   with the accept loop sending typed requests. Then `persona-terminal`
   forwards control-plane Signal frames to that actor's mailbox.
2. Retire terminal-cell's signal-control surface entirely — let
   `persona-terminal`'s supervisor own all control state and let
   terminal-cell speak only the byte-tag CLI protocol. Per /136 §"two-
   plane split", the data plane on `data.sock` is already
   terminal-cell-owned and stays.

Either is operator-design territory. The witness in
`terminal-cell/tests/actor_discipline_truth.rs` scopes to library
source only; the day the daemon binary's drift is fixed, the scope
widens to cover it.

### 5.2 · persona-message uncommitted ARCH edits

A parallel agent left edits to `persona-message/ARCHITECTURE.md` in
the working copy when I started the audit (around line 91-93 adding
prose about `geteuid()`-based stamper constructor as test-only +
standalone-launch affordance, plus §2 typed-configuration-via-argv
prose, plus a new constraint about no env-var reading). Those edits
align with the current code and look correct to land. I used a
`jj commit <test_path>` partial commit to add my witness without
bundling the unrelated ARCH change. The ARCH edits remain in the
working copy for whoever made them; they didn't conflict with my
witness.

### 5.3 · persona uncommitted direct_process.rs edits

A parallel agent left WIP edits to `persona/src/direct_process.rs`
adding a `write_terminal_daemon_configuration_file` method against a
`signal_persona_terminal::TerminalDaemonConfiguration` type that doesn't
exist on the current `signal-persona-terminal` git pin. The edits
don't compile. I used a `jj commit <test_path>` partial commit and a
`jj new @-` switch to land my witness on top of `main` (not on top of
the broken WIP), then squashed an import-path fix. The parallel
agent's WIP is preserved in a sibling commit
(`pqltszmw 4d0420a5` at the time of audit) under their own change-ID
for whoever owns it.

---

## 6. What I deliberately did NOT touch

Per the prompt's scope (AUDIT + CONSOLIDATION, not REIMPLEMENT):

- **P1 choreography handlers** (per /138 §P1) — deferred; designer call
  needed on `ChoreographyPolicy` storage shape, authorization model,
  grant→router data flow, retract-vs-in-flight semantics.
- **P2 Template-2 StoreKernel migration** (per /138 §P2) — deferred;
  Kameo upstream needs a `pre_notify_links` hook (or an actor-owned
  close-then-confirm protocol) before supervised state-bearing actors
  can move to `.spawn_in_thread()`. My skill updates document the
  deferral at the right level so future agents see the gap.
- **MindAdjudicationOutbox redb persistence** (per /131 §6.1) —
  gated on `RouterDaemonConfiguration` typed config landing.
- **ChannelTriple typed migration** (per /131 §6.2) — coordinated
  schema-bump cascade exceeding this audit's blast radius.
- **Reply-side subscription contract narrative in `signal-persona-system`**
  — the contract code is correct per /91, but the doc comment on
  `SubscriptionRetracted` (line 277-279 of `src/lib.rs`) still says
  "This is the Path A reply variant per /181; retraction is a closed
  reply event signaling the stream is over, not a request-only fire-
  and-forget op." That's stale per /91 (it's BOTH request and reply).
  `signal-persona-system` is not in this audit's target list; I left
  the doc comment alone. Designer should reconcile on a future
  contract-side sweep.
- **persona-mind `ChoreographyAdjudicator` skeleton** — deferred per
  /138 §P1.
- **Subscription push delivery 3-actor split in persona-mind** —
  deferred per /138 §P5; gated on P1.

---

## 7. Witness file inventory after this audit

| Repo | Tests file added/extended | Witnesses |
|---|---|---|
| persona | `tests/actor_discipline_truth.rs` (new) | `public_actor_nouns_carry_data` (7 actors), `actor_source_does_not_share_locks_between_actors` (skips `StopHandoff` carve-out) |
| persona-mind | already covered (`tests/weird_actor_truth.rs`) | `actor_adapter_markers_cannot_be_public_zst_nouns`, `actor_source_cannot_hide_shared_locks_or_polling_waits` |
| persona-router | `tests/no_shared_locks_truth.rs` (new); `tests/actor_runtime_truth.rs` already had `public_control_records_cannot_be_zero_sized` | size_of (10 actors+records), no-shared-locks (source scan) |
| persona-harness | `tests/actor_discipline_truth.rs` (new) | `public_actor_nouns_carry_data` (5 actors), `actor_source_does_not_share_locks_between_actors` (skips `TranscriptSubscriptionSinkInner` carve-out) |
| persona-terminal | `tests/actor_size_truth.rs` (new); `tests/actor_runtime_truth.rs` already had `terminal_signal_control_state_is_owned_by_a_kameo_actor` | size_of (3 actors), no-shared-locks (source scan, already there) |
| terminal-cell | `tests/actor_discipline_truth.rs` (new) | size_of (TerminalCell), no-shared-locks (library scope; binary scope deferred per escalation #1) |
| persona-introspect | `tests/actor_discipline_truth.rs` (new) | size_of (9 actors), no-shared-locks |
| persona-system | `tests/actor_discipline_truth.rs` (new) | size_of (3 actors), no-shared-locks |
| persona-message | `tests/actor_discipline_truth.rs` (new) | size_of (2 actors), no-shared-locks |
| criome | `tests/actor_discipline_truth.rs` (new) | size_of (6 actors), no-shared-locks |

Topology-manifest discipline (each component's ARCH §"Supervision
tree" lists exactly the actors that exist at runtime): persona-mind
has `ActorManifest` (a runtime test fixture exposing the live actor
tree). Every other component's ARCH names its actor tree in prose +
mermaid (see persona-router §1, persona-harness §1.5/1.6,
persona-terminal §1.5/2, terminal-cell §1.4/2, persona-introspect §3,
persona §1.7). I did not add a manifest-style runtime probe to every
repo — that's a larger discipline lift than this audit warranted.
Surface for designer: the workspace might benefit from a canonical
`ActorManifest` shape that every component daemon exposes through its
supervision contract.

---

## 8. See also

- `~/primary/reports/designer-assistant/90-critique-designer-184-200-deep-architecture-scan.md`
  §1 manager, §2 mind, §9 kernel — authoritative critique substance.
- `~/primary/reports/designer-assistant/91-user-decisions-after-designer-184-200-critique.md`
  — load-bearing decisions this audit enforces.
- `~/primary/reports/operator-assistant/134-persona-manager-gap-close-2026-05-16.md`
  — phase-1 manager work this audit consolidates around.
- `~/primary/reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
  — kameo gap discovery; canonical source for the skill updates.
- `~/primary/reports/operator-assistant/131-persona-router-gap-close-2026-05-16.md`
  — phase-1 router work this audit consolidates around.
- `~/primary/reports/operator-assistant/135-phase3-push-subscription-chains-2026-05-16.md`
  — three-actor subscription pattern; harness sink scaffolding noted.
- `~/primary/reports/operator-assistant/136-phase3-terminal-control-data-plane-2026-05-16.md`
  — terminal control/data plane split context.
- `~/primary/reports/operator-assistant/137-phase3-event-sourcing-snapshots-2026-05-16.md`
  — event-log/snapshot/orphan witness shape.
- `~/primary/skills/kameo.md` §"Blocking-plane templates" Template 2
  and §"Anti-patterns and gotchas" — where the kameo gap finding lives
  permanently.
- `~/primary/skills/actor-systems.md` §"Supervision gotcha — Template 2
  on a supervised state-bearing actor" and §"Anti-pattern — `flavor =
  "multi_thread"` on parallel daemon-restart tests" — where the
  architectural-discipline framing lives permanently.
- `~/primary/skills/subscription-lifecycle.md` — canonical five-state
  FSM the persona-system ARCH now cites.
- `~/primary/skills/architectural-truth-tests.md` §"Actor-density tests"
  — the witness discipline this audit applies.
