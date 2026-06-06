---
title: 543 — triad_main! implementation + ordered landing handoff
role: designer
variant: Decision
date: 2026-06-06
topics: [triad-main, component-triad, schema-rust-next, triad-runtime, spirit, daemon, code-emission, streaming, handoff]
description: |
  triad_main! (the emitted daemon module, design 542 / Spirit lnhj) is
  implemented thoroughly across triad-runtime + schema-rust-next + spirit and
  verified GREEN end-to-end (option-B streaming proven against the emitted
  daemon by process_boundary). Pushed as three clean branches
  designer-daemon-emit-2026-06-06. This report is the operator handoff: the
  ordered cross-repo landing plan (git branch=main deps require it).
---

# 543 — triad_main! implementation + landing handoff

## Status: implemented thoroughly, verified green end-to-end

Built across three worktrees, cross-`[patch]`-wired for end-to-end
verification, then the dev `[patch]` stripped and pushed as three clean
branches **`designer-daemon-emit-2026-06-06`**:

- **triad-runtime** (`4454952f`): the `DaemonConfiguration` trait (the config
  accessors the emitter reads) + `ExitReport::from_result` (the
  component-agnostic exit helper — a method on a data-bearing noun, the
  discipline-faithful form of "run_to_exit_code"). 44 tests green.
- **schema-rust-next** (`304d52e7`): the **daemon emitter** (`daemon_emit.rs`,
  `ModuleEmission::daemon_module`). Off by default; emits source-visible,
  freshness-guarded `src/schema/daemon.rs` only when the schema declares a
  `NexusDaemonShape`. Emits the `ComponentDaemon` hook trait, `DaemonCommand`,
  the `GeneratedDaemonRuntime` decode→execute→encode spine, Single/Multi
  listener selection, `DaemonError`, and `DaemonEntry::run_to_exit_code`.
  **Option B**: when `Schema::streams()` yields a stream it emits
  `EmittedSubscriptions` (the `SubscriptionRegistry` + `SubscriptionEventPublisher`
  + register/publish/deliver) — the daemon-side streaming plumbing, generated.
  61 tests green (incl. daemon-emission goldens). *(The agent fixed three real
  emitter bugs to get spirit compiling: missing rkyv bounds on the emitted
  `StreamEvent` assoc type, a `MutexGuard` borrow-split in the emitted
  `publish`, + regression tests.)*
- **spirit** (`ad122e3e`): the pilot. `impl ComponentDaemon for SpiritDaemon`
  (only `build_runtime` + the escape hatches); `Configuration` implements
  `DaemonConfiguration`; `NexusDaemonShape` declared in `build.rs` (working
  `signal` tier + owner-only `0o600` meta tier); the emitted `src/schema/daemon.rs`
  generated + freshness-guarded; the bin is a true one-liner
  (`SpiritDaemon::run_to_exit_code()`); the hand-written
  `DaemonCommand`/`Daemon`/`SpiritDaemonRuntime` **and** the entire
  `SubscriptionHub` are **deleted** (streaming now emitted). `cargo test
  --all-features` 77 passed / 9 nix-ignored, clippy `-D` clean, freshness
  guard passes.

**End-to-end proof:** spirit's `process_boundary` suite (8/8) passes against
the **emitted** daemon binary over a real Unix socket — including
`cli_subscription_receives_matching_intent_events_without_blocking_daemon`
(the streaming/subscription test) and the trace test. Three adversarial
verifiers independently re-ran all builds/tests; trees left clean.

## Ordered landing plan (operator) — required by git `branch=main` deps

The chain must land in dependency order, regenerating each lockfile against the
freshly-landed upstream main (the pushed branches' lockfiles are stale from the
dev `[patch]` and should be regenerated):

1. **triad-runtime** → integrate `designer-daemon-emit-2026-06-06` to main, push.
2. **schema-rust-next** → integrate the branch; `cargo update -p triad-runtime`
   (pull the just-landed triad main); `cargo build`/`test`/`clippy -D` verify;
   push main.
3. **spirit** → integrate the branch; `cargo update -p triad-runtime -p
   schema-rust-next`; verify `cargo test --all-features` (especially
   `process_boundary`) + the freshness guard; push main.

The branches are clean (dev `[patch]` removed); each repo is additive +
independently green once its upstreams are landed.

## Notes / judgment calls (confirmed sound)

- **`fn main` is the bin one-liner**, not emitted — the emitted module provides
  `DaemonEntry::run_to_exit_code`; the 4-line `fn main` stays hand-written and
  calls it. (Matches the design's intent; the entry *logic* is generated.)
- **`public_surface.rs` guard narrowed** to still forbid flattening the four
  generated *plane* modules (`signal/nexus/sema/meta_signal`) while exempting
  `schema::daemon` (so the bin can `use spirit::{DaemonEntry, SpiritDaemon}`).
  Verified sound — preserves the guard's stated intent.
- **Follow-on** (design 542 §forks 5/6): generalize to cloud's multi-listener
  (retiring its hand-written `schema_daemon.rs` into emitted output), then
  domain-criome; update `skills/component-triad.md` to say triad_main! is an
  *emitted module* (not a literal macro) and re-anchor off the dead `1419`/`1486`
  to live `1488`.

Per psyche 2026-06-06 ("gap 3: let's design the main macro" → "go with B. implement thoroughly").
