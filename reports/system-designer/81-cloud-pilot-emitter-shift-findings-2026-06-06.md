---
title: 81 — cloud triad_main pilot — what the retirement actually surfaced
role: system-designer
variant: Findings
date: 2026-06-06
topics: [cloud, triad-main, schema-rust-next, emitter-shift, schema-grammar, fleet-staleness, ug6i, daemon, pair-form]
description: |
  The cloud multi-listener pilot (report 542 / ocu7 / psyche "yes") was scoped
  as "retire the hand-written schema_daemon.rs onto the emitted triad_main."
  Doing it proved the daemon retirement works (a small emitter enhancement,
  landed) but unblocked a much larger truth: cloud's whole schema engine
  predates a broad emitter shift. This report records what landed, what the
  shift is, and the decision the size of the remaining port warrants.
---

# 81 — cloud pilot: what the retirement surfaced

## STATUS: COMPLETE (2026-06-06, psyche chose "grind the full port now")

The full cloud port landed on main, green end-to-end (build all-targets +
clippy -D + all tests, incl. the live `schema_daemon` socket tests that drive
both tiers over real Unix sockets through the emitted daemon). Landed commits:

- schema-rust-next `98fbb369` (dependency-contract working tier) + `2c3c162d`
  (gate emitted `try_clone_stream` behind `emits_stream` — no dead code in
  non-streaming multi-listener daemons).
- signal-cloud `27d7056e` (regen) + `0ff53ff2` (Observation → pair form,
  restoring the tuple wire contract the bare-name regen had silently broken).
- meta-signal-cloud `abce145f` (regen; its body enums were already unit/root, so
  unaffected).
- cloud `4a378d37` — schema pair-form migration (nexus + sema), `schema_role.rs`
  deleted (role impls now emitted), triad-runtime bumped,
  `SchemaRuntime::reply_to_signal` (per-request execute on the engine noun),
  and `schema_daemon.rs` rewritten to `impl ComponentDaemon for CloudDaemon` +
  a thin `SchemaDaemon` wrapper. Legacy `daemon.rs` (Cloudflare-IO) + the
  `cloud-daemon` bin unchanged (the live-IO effect-plane port is separate).

The two findings below (working-socket mode; fleet-wide grammar staleness)
remain open follow-ups beyond cloud.

## What the retirement surfaced (kept for the record)

## Landed and pushed (independently valuable, all green)

1. **Daemon emitter supports dependency-crate working contracts**
   (schema-rust-next main `98fbb369`). `WorkingListenerTier::dependency(path)`
   emits `use signal_cloud::schema::lib::{Input, Output, SignalFrameError}`
   instead of crate-local-only. Local case byte-identical (6 daemon goldens +
   full suite + clippy -D green). This is the one genuinely-new emitter
   capability the cloud pilot required, and it works: cloud now emits a correct
   two-tier `src/schema/daemon.rs` (dependency import, working+meta bind,
   ComponentDaemon trait, DaemonEntry one-liner entry).
2. **signal-cloud regenerated** against the current emitter (main `27d7056e`) —
   was stale (ug6i).
3. **meta-signal-cloud regenerated** against current emitter + fresh signal-cloud
   (main `abce145f`) — was stale (ug6i).

## The daemon retirement itself is proven

My emitter enhancement + cloud's `build.rs` wiring (declare a two-tier
`NexusDaemonShape` with `WorkingListenerTier::dependency("signal_cloud::schema::lib")`
+ `with_meta_tier`, point the daemon module at the streamless local `nexus`
schema) makes the emitter generate exactly the daemon spine cloud hand-wrote in
`schema_daemon.rs` — `DaemonCommand`, the decode→execute→encode
`GeneratedDaemonRuntime`, `ListenerTier` Working/Meta dispatch, `DaemonError`,
`DaemonEntry::run_to_exit_code`. The hand-written `SchemaDaemon`/`CloudRuntime`/
`serve_*` is now redundant. So the SHAPE retirement is unblocked.

## But cloud can't compile — a broad emitter shift its stale artifacts hid

Regenerating cloud (against the current emitter + fresh contracts) exposed 34
errors that have nothing to do with the daemon. They are the same "broad emitter
shift" I noted last session, now unmissable post-regeneration:

### 1. Enum declaration grammar changed: bare name = unit variant

The root cause of ~25 errors. The emitter changed how it reads a NOTA enum
variant list:

| Schema declaration | Old emission | New emission |
|---|---|---|
| `ReadInput [Observe ObservePlan Validate]` (bare names) | tuple variants `Observe(Observation)` | **unit variants** `Observe` + `pub type Observe = Observation` |
| `ReadInput [(Observe Observe) (Lookup Lookup)]` (pairs) | tuple variants | tuple variants `Observe(Observe)` |

cloud's `sema.schema` / `nexus.schema` use the **bare-name** form
(`SemaReadInput [Observe ObservePlan Validate]`), so every payload-carrying
variant regenerated as a **unit** variant — and cloud's hand-written engine
(`schema_runtime.rs`, 491 lines) constructs and matches them as tuples
(`SemaReadInput::Observe(observation)`), so it no longer compiles. spirit (the
canonical pilot) uses the **pair** form (`ReadInput [(Observe Observe) ...]`)
and compiles. **The pair form is the current grammar; cloud's schema is in the
old bare-name style and must be migrated.**

### 2. NexusEngine trait surface changed (4 × E0407)

`apply_sema_write` / `observe_sema_read` / `run_effect` /
`budget_exhausted_reply` are no longer members of the emitted
`nexus::NexusEngine` — cloud's hand-written `impl NexusEngine` carries stale
method names and must be reconciled with the current trait.

### 3. Role-marker impls now emitted (5 × E0119)

The emitter now emits `impl triad_runtime::NexusWork for NexusWork {}` and
friends inline (in the regenerated nexus.rs/sema.rs). cloud's `schema_role.rs`
was the report-77 SOFT bridge hand-writing exactly these — now duplicates.
Delete `schema_role.rs`.

### 4. triad_runtime pin too old (3 × E0432/E0425)

The emitted daemon.rs imports `triad_runtime::{ConnectionContext,
DaemonConfiguration, ExitReport}` — cloud's pinned triad_runtime predates them.
Bump to current main.

## The remaining cloud port (now fully diagnosed, mechanical but broad)

1. Migrate cloud's `nexus.schema` + `sema.schema` enums from bare-name to pair
   form for every payload-carrying variant (the bulk — many enums).
2. Regenerate (emitter writes the new tuple-variant nexus.rs/sema.rs).
3. Delete `schema_role.rs` (now-emitted marker impls).
4. Bump `triad_runtime` to current main.
5. Reconcile `schema_runtime.rs` against the changed `NexusEngine` trait surface.
6. Retire `schema_daemon.rs` → thin `impl ComponentDaemon for CloudDaemon`
   (build_runtime over `Arc<SchemaStore>`, handle_working_input, handle_meta_stream),
   one-line bin; relocate the per-request execute helper onto `SchemaRuntime`
   (`reply_to_signal`) so it lives on a real noun, not the ZST daemon marker.

This is a real multi-file engine port, not a daemon swap. It is mechanical now
that the grammar shift is understood, but it is the size of a full component
migration, with several slow builds.

## Two findings worth the psyche's eye beyond cloud

- **Working-socket mode is not emitter-configurable.** The emitted multi-listener
  bind applies the *meta* socket mode (owner-only) but binds the *working* socket
  at default umask mode — no knob. Report 76's security partition (message.sock =
  0660 external door vs router.sock = 0600 owner-only) is a real distinction;
  message migrated onto the emitted daemon and so its working socket is now
  default-mode unless handled elsewhere. This affects the trust-boundary
  component (message), not just cloud. Candidate fix: a
  `WorkingListenerTier` socket mode + a `working_socket_mode()` on the
  `DaemonConfiguration` trait, symmetric with the meta tier.
- **ug6i staleness is fleet-wide, not cloud-local.** The bare-name→unit grammar
  shift and the role-marker-impl emission mean EVERY component carrying
  hand-written engine code or schemas in the old grammar will break on
  regeneration the same way cloud did. The `write_or_check` freshness gate
  catches stale *output* but not stale *grammar*; a fleet regeneration sweep is
  the real ug6i closure.
