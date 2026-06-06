---
title: 542 — triad_main! design — the emitted daemon entry point
role: designer
variant: Decision
date: 2026-06-06
topics: [triad-main, component-triad, schema-rust-next, daemon, code-emission, runner, escape-hatch, spirit]
description: |
  Design for triad_main! (Gap 3 of study 327). Key reframe: it is NOT a
  literal macro — schema-rust-next emits source-visible items, so triad_main!
  is an emitted per-component `daemon` module. The emitter writes the uniform
  daemon skeleton (main + DaemonCommand + the decode→execute→encode runtime +
  listener selection); the component hand-writes only a small ComponentDaemon
  hook impl + a schema daemon-shape declaration. Six forks for the psyche,
  with leans. Re-anchors to live record 1488 (1419/1486 are dead refs).
---

# 542 — triad_main! design

## The reframe: emission, not a literal macro

The intent calls it `triad_main!` (with the bang), but the right form is **not
a `macro_rules!`**. Both INTENT files settle this:

- `triad-runtime/INTENT.md`: *"triad-runtime neither owns nor emits
  triad_main!; when that emission lands it will be a schema-rust-next emitter
  responsibility, with triad-runtime continuing to own only the generic runner
  the emitted entry point drives."*
- `schema-rust-next/INTENT.md`: Rust emission is source-visible into
  `src/schema/`, freshness-checked, **never hidden in OUT_DIR or a compiler
  macro** — so generated interfaces stay reviewable.

So `triad_main!` is a **new schema-rust-next emitter** that writes a
per-component, source-visible **`src/schema/daemon.rs`** — exactly like the
already-shipped `NexusEngine::execute` glue. The trailing `!` is intent
shorthand for "the emitted entry point," not a literal macro. (The skill
`component-triad.md` should be updated to say this; and it currently cites the
**dead** records `1419`/`1486` — the live anchor is **`1488`**.)

## The shape — generate the skeleton, hand-write only the escape hatches

This is `1488` made concrete (*schema carries the engine baseline; per-component
variation uses explicit escape hatches, not hand-written daemon plumbing*) and
the readability thesis applied to the daemon (*generate the plumbing; hand-write
only the real algorithm*).

**Emitted into `src/schema/daemon.rs` (uniform skeleton):**
- `fn main()` — the one-line `exit(Daemon::from_environment().run_to_exit_code())`
  shell that is hand-written *identically* today in spirit, cloud, and
  domain-criome bins.
- `DaemonCommand` — argv parse → `signal_file_argument` → `Configuration::from_binary_path`
  (reject inline/file NOTA), generic in `triad-runtime`'s `ComponentCommand`.
- The generic `DaemonError` plumbing (Argument/Configuration/Listener/ActorStart/
  ActorStop + the `From<{Single,Multi}ListenerDaemonError>` conversions).
- The `{Single,Multi}ListenerDaemon` selection + bind + `run`, chosen from the
  schema-declared listener tiers (not hand-toggled).
- The generated `ListenerRuntime` struct + its `handle_stream` **decode→execute→
  encode spine** (read length-prefixed body → `Input::decode_signal_frame` →
  `NexusEngine::execute` [→ `Runner::drive`] → `Output::encode_signal_frame` →
  write). Per-tier dispatch for the multi-listener case.

**Hand-written by the component (the only daemon code left):**
- `impl ComponentDaemon for SpiritDaemon` — declares the escape hatches:
  `type Configuration / Engine / Error`, `PROCESS_NAME`, and
  `fn build_runtime(&Configuration) -> Result<Engine, Error>` (**REQUIRED** —
  the macro can't know how to open your Store; this is the canonical `1488`
  escape hatch), plus an **optional** `fn after_reply(&self, input, output,
  writer)` defaulting to no-op (spirit overrides it for `SubscriptionHub`
  register/publish).
- The engine trait impls (`NexusEngine`/`SignalEngine`/`SemaEngine`) — already
  the established emitted seam; `triad_main!` inherits them, effects ride
  `run_effect` for free.
- A schema-side **`NexusDaemonShape`** declaration (process name, listener
  tiers, socket modes, contract-per-tier) — a sibling to the existing
  `NexusRunnerShape` — so the emitter knows single-vs-multi and which `Input`
  to decode where.

## Where it lives — hybrid (settled by intent, not a fork)

schema-rust-next **emits** the per-component `daemon.rs`; triad-runtime keeps
owning only the **component-agnostic** shells (`Single/MultiListenerDaemon`,
the `MultiListenerRuntime` trait, `Runner::drive`, and a tiny
`run_to_exit_code(result)` helper with zero component knowledge). A literal
`macro_rules!` in triad-runtime would contradict the source-visible discipline
*and* force triad-runtime to carry component knowledge it explicitly disclaims.

## Migration — spirit pilots, no regression, 4 steps

0. Keep spirit's hand-written `daemon.rs` as the reference; build the emitter to
   reproduce its semantics exactly (decode→handle→write→register→publish).
1. Extract spirit's two real differences into `impl ComponentDaemon for
   SpiritDaemon` — `build_runtime` (lift `runtime()`, trace cfg and all) +
   `after_reply` (lift register_subscription + publish_output). Still compiles.
2. Add the schema `NexusDaemonShape` declaration; turn on the emitter so
   `src/schema/daemon.rs` is generated + freshness-checked by the same
   `write_or_check` gate guarding signal/nexus/sema.
3. Flip the bin to the emitted entry; **delete** the hand-written
   `DaemonCommand`/`Daemon`/`SpiritDaemonRuntime`/generic-`DaemonError`,
   leaving only the component-specific error variants + the `ComponentDaemon`
   impl. Each step independently shippable.

## The forks (with leans) — for the psyche

1. **Generate the runtime struct, or require a component trait impl?** (the
   core call) — Generating it means the emitter owns the decode/execute/encode
   spine and the component only fills hooks (maximal generation, the
   readability thesis). **Strong lean: generate it** — the spine is the
   plumbing `1488` wants emitted.
2. **Listener tiers: inferred from contract shape, or an explicit
   `NexusDaemonShape`?** **Lean: explicit** — socket *mode* and process name
   aren't derivable from the contract.
3. **`Configuration`: a small `triad-runtime` `DaemonConfiguration` trait the
   component implements (uniform surface the emitter reads socket paths/modes
   from), or a per-component type the emitter only names?** **Lean: the trait**
   — the emitter needs a uniform way to read socket_path/meta_socket_path/
   database_path/trace_socket_path.
4. **`after_reply` as a single post-reply hook, or model streaming
   first-class?** The emitter already emits streaming frame support from
   `Schema::streams()`; extending it to emit the daemon-side publish/subscribe
   wiring would shrink spirit's escape hatch from "hand-write the whole hub" to
   "declare the stream." **Lean: start with the hook, grow toward first-class
   streaming emission** (bigger emitter scope; do it after the spine lands).
5. **Thin `run_to_exit_code` in triad-runtime, or emit it per-component?**
   **Lean: the thin helper** (it's genuinely component-agnostic; avoids
   re-emitting the same 4 lines everywhere).
6. **Pilot order.** **Lean: spirit first** (single-listener, smallest delta,
   proves the spine + `build_runtime` + `after_reply`), then cloud's
   multi-listener (retiring its hand-written `schema_daemon.rs` into emitted
   output), then domain-criome.

Per psyche 2026-06-06 ("gap 3: let's design the main macro").
