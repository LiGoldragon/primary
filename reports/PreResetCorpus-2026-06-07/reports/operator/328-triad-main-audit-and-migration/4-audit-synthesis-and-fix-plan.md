---
title: 328 — triad_main audit synthesis + land-and-fix plan
role: operator
variant: Psyche
date: 2026-06-06
topics: [triad-main, daemon-emit, audit-synthesis, token-emission, landing-plan]
description: |
  Synthesis of the three-reviewer audit of the implemented triad_main (emitted
  daemon module). The emitted product is sound and triad-conformant; the
  emitter MECHANISM violates 4np2 (fully string-based). Consolidated flaw
  ledger + the dependency-ordered land-and-fix plan.
---

# 328 — Audit Synthesis & Land-and-Fix Plan

## One-line verdict

The **emitted daemon module is clean and triad-conformant**; the **emitter that
produces it is a 807-line string generator** that violates `4np2`. Fix = port
the emitter to tokens (after merging onto post-Gap-1 main); the emitted product
needs only small touch-ups. Landing is low-risk (test-merged clean).

## Flaw ledger

| ID | Severity | Flaw | Fix |
|---|---|---|---|
| **B1** | BLOCKER (`4np2`) | `daemon_emit.rs` fully string-based: 807 lines, ~404 `self.line()` + 6 `format!`, **0 `quote!`/`ToTokens`**; `DaemonModuleWriter` god-struct (only field `output: String`) | Port the 14 `emit_*` methods to per-section `…Tokens` `ToTokens` nouns routed through `RustModuleRenderer::emit_item_tokens` → `prettyplease` (the Gap-1 seam) |
| **M1** | MAJOR (`de8i`) | the 14 section emitters hang off the `DaemonModuleWriter` god-struct, owning no domain data | dissolves under the B1 port (each section becomes its own data-bearing `ToTokens` noun) |
| **M2** | MAJOR | emitter never parse-validates its output (no `syn::parse2` gate like `lib.rs:2917`) — the reason 543's 3 emitter bugs reached consumer `cargo build` | the token port routes through `syn::parse2` + `prettyplease`, giving emission-time validation for free |
| **M3** | MAJOR | `DaemonStreamShape.event_type` (`daemon_emit.rs:128`) + its 18-line `reference_type_name` recursion is **dead code** — computed then discarded (`let _ = event` :377, `let _event` :527); only "stream declared?" is used | delete the struct, replace with `emits_stream: bool` |
| m1 | MINOR | emitted `DaemonError::Component` uses bare `#[error("{0}")]`, asymmetric with the 3 self-describing arms | make it self-describing |
| m2 | MINOR | emitted `EmittedSubscriptions::deliver` is a 3-arg associated fn | make it `&mut self` on `SubscriptionState` |
| m3 | MINOR (DEFER) | emitted `EmittedSubscriptions::publish` delivers synchronously inline — a wedged subscriber stalls the publishing request thread (NOT the daemon; **no regression** vs the `SubscriptionHub` it replaces) | follow-up: non-blocking writers / publisher actor — not this pass |
| m4 | MINOR | `ComponentDaemon::ConfigurationError` bounded only by `Display`, not `std::error::Error` (loses `source()` chaining) | tighten the bound |
| n1 | NIT | load-bearing borrow-split `//` comment is dropped by prettyplease on regen | promote to a doc comment so it survives |
| n2 | NIT | stale `RustWriter` doc reference `daemon_emit.rs:194` | remove (vanishes under the port) |

## Sound — preserve as-is

All three reviewers confirm the **emitted output** is clean, idiomatic, and
triad-faithful: `ComponentDaemon` hook surface (`build_runtime` + escape
hatches), the decode→execute→encode spine, the single-argument rule (argv
rejects inline/file NOTA, accepts only the rkyv `SignalFile`), rkyv-signal-frame-only
wire (no NOTA between components), `3d5z` separation (no plane bleed; meta path
never re-enters the SEMA log write), typed `DaemonError`, `DaemonConfiguration`,
`ExitReport::from_result` (a method on a data-bearing noun — 543's
discipline-faithful claim verified), Single/Multi listener selection, no ZST
namespaces. The three prior emitter bugs (rkyv `StreamEvent` bound, `MutexGuard`
borrow-split) are genuinely fixed, proven by `process_boundary`.

**The discipline problem is the production mechanism, not the product.**

## Land-and-fix plan (dependency-ordered)

R3 *test-merged* the schema-rust-next branch onto post-Gap-1 main: **zero
conflicts**, `RustModuleRenderer` kept, `RustWriter` correctly gone, daemon
module retained, `cargo check` + daemon-emission tests pass after `cargo update
-p triad-runtime`. So:

1. **triad-runtime** — integrate the branch (`DaemonConfiguration` + `ExitReport`
   + `process.rs`/`lib.rs`/ARCH additions) onto main; reconcile the ARCHITECTURE.md
   overlap with the earlier doc commit; verify; push.
2. **schema-rust-next** — merge the branch onto main (clean), `cargo update -p
   triad-runtime`. **Then apply B1+M1+M2+M3+m1+m2+m4+n1+n2** (the token rewrite +
   dead-code removal + emitted touch-ups). Verify `cargo check`/`test`/`clippy -D`
   incl. the daemon-emission goldens (whitespace/comma-insensitive, so the
   reformat won't break them). Push.
3. **spirit** — integrate the branch (clean descendant); `cargo update -p
   triad-runtime -p schema-rust-next`; verify `cargo test --all-features`
   (especially `process_boundary` against the emitted daemon) + the freshness
   guard. Push.

Then the runtime is landed clean and component migration begins.
