# 240 — signal-frame: collapse Operation, drop Request::check()

*Two follow-up cleanups in `signal-frame` after the macro
migration landed in operator report `/138`. Removes the
vestigial `Operation<Payload>` wrapper and the dead
`Request::check()` API. Wire shape unchanged; in-memory
layer simplified. Both psyche-confirmed 2026-05-19T20:50Z
("I concur"). Commit `4bdf1e1e` on signal-frame `main`.*

## 0 · TL;DR

What collapsed:

- `Operation<Payload>` — gone. The whole module `src/operation.rs`
  removed. With `SignalVerb` already retired by the macro
  migration, `Operation` was a transparent `{ payload }`
  wrapper carrying no semantic content.
- `Request<Payload>.operations: NonEmpty<Operation<Payload>>`
  → `Request<Payload>.payloads: NonEmpty<Payload>`. Renames
  follow: `from_operations(..)` → `from_payloads(..)`,
  `operations()` → `payloads()`.
- `Request::check()`, `Request::into_checked()`,
  `CheckedRequest<Payload>` — gone. With the universal
  verb-shaped rules retired, `check()` always returned
  `Ok(())`. Channel-specific validation lives in daemon
  executors and payload constructors, not in a kernel
  function pretending to do work.
- `RequestBuilder<Payload>` now operates on `Vec<Payload>`
  directly; constructor / `with(..)` / `push(..)` / `build()`
  signatures unchanged from the caller's view.

What stayed:

- **Wire shape is identical.** A length-1 `Request` encodes
  as the payload's record head directly; a length-N request
  encodes as `[(Verb …) (Verb …)]`. The collapse was a pure
  in-memory simplification.
- **`RequestRejectionReason::Internal` kept** — verified
  it's not produced by the removed `check()` but consumed via
  `Reply::Rejected { reason: Internal }` as a legitimate
  daemon-level pre-execution rejection. The doc comment
  already framed it this way.
- **Macro emitter untouched.** The macro generates the
  contract's payload enum (`MessageOperation` for a `Message`
  channel) and passes that enum as the `Payload` type to
  `Request<Payload>` / `RequestBuilder<Payload>`. The
  collapse fell out automatically because nothing in the
  emitter referenced `Operation<Payload>` directly. Doc
  comments in `macros/src/lib.rs` and `macros/README.md`
  updated to drop the wrapper mention.

## 1 · Verification

All checks green:

- `cargo build --locked`
- `cargo test --locked` — 22 tests across 4 binaries (6
  macro witnesses, 5 compile-fail witnesses, 15 frame
  witnesses, 1 doc test)
- `cargo clippy --all-targets --locked -- -D warnings`
- `nix flake check --option substituters ''` (remote builder)

## 2 · Tests touched

- `tests/frame.rs` — dropped `Operation` import; dropped
  `check_passes_on_well_formed_request` and
  `into_checked_returns_checked_request_on_success`; renamed
  `request_from_payload_wraps_single_operation` to
  `…wraps_single_payload`; multi-op round-trip rewritten
  using `Request::from_payloads(NonEmpty<Payload>)` directly.
- `tests/channel_macro.rs` — dropped `Operation` import;
  switched to `Request::from_payloads(..)`.
- Compile-fail witnesses unchanged — none depended on
  `Operation`.

## 3 · Docs touched

- `ARCHITECTURE.md` — §"Owns", §"Invariants", §"Migration
  history" (records this cleanup), §"Code Map".
- `skills.md`.
- `macros/README.md` and `macros/src/lib.rs` doc-comment.

## 4 · Cross-crate consequences

**`signal-sema` — no impact.** Verified: no `signal-frame`
references in `Cargo.toml`, `src/`, `tests/`, or
`examples/`. It owns its own `SemaOperation` type
independent of the former `signal-frame::Operation`. No
follow-up needed.

**`signal-repository-ledger` — invisible through the
macro.** It depends on `signal-frame` only for the
`signal_channel!` macro and `RequestPayload` marker trait.
The macro emits a `Message`-style payload enum, and
`Request<MessageOperation>` is what the consumer sees —
they never touched `Operation<Payload>` directly. If the
daemon code reaches into `Request.operations()` to iterate
ops, that becomes `Request.payloads()` — a single-method
rename caught by the compiler. Not blocking.

**Other legacy consumers** (`persona-*`, `sema-engine`,
`repository-ledger`, etc.) still depend on `signal-core`,
not `signal-frame`. Their migration is the broader work
item (per `/239` Phase 3); this slice doesn't touch them.
The new names land before any consumer has built on the
old `operations()`-shaped surface in signal-frame.

## 5 · An interesting structural finding

The macro emitter required **zero changes** for the
collapse. The reason: the emitter generates the contract's
payload enum (e.g. `MessageOperation` for `channel
Message`) and uses that enum as the `Payload` type
parameter when wrapping with `Request<Payload>`. Nothing
about the emitter knew or cared about `Operation<Payload>`.

This is a small validation of the architectural direction:
the kernel types and the macro-generated contract types
sit at orthogonal layers, and a kernel-side simplification
that removes a transparent wrapper is invisible to the
macro. The contract-local-verbs migration shape is
holding up.

## 6 · References

- `reports/operator/138-signal-frame-macro-migration-work.md`
  — the macro migration this builds on; the two design
  smells were flagged in §"What remains".
- `reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
  — broader architecture.
- `reports/designer/239-signal-architecture-migration-plan.md`
  — migration plan.
- `intent/component-shape.nota` 2026-05-19T20:50Z — psyche
  authorization for the two-smell-fix.
- `signal-frame` commit `4bdf1e1e` on `main` — landing.
