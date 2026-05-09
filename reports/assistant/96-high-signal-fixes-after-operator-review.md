# 96 - High-signal fixes after operator review

Status: completed assistant implementation pass after
`reports/assistant/95-operator-work-review-after-designer-93.md`.

Author: Codex (assistant)

Date: 2026-05-09

---

## Summary

I fixed the high-signal issues surfaced in `reports/assistant/95` and folded
in the matching designer critique about contract-owned boundary validation.

The substantive code change landed in `signal-persona-orchestrate`: boundary
newtypes now enforce their own invariants before frames are built. The rest of
the work corrected architectural truth in documentation so the docs match the
current Sema library direction: state-bearing components own their own Sema
databases, while `persona-sema` owns schema/table conventions rather than a
central store actor.

## Commits Pushed

| Repo | Commit | Message |
|---|---:|---|
| `/git/github.com/LiGoldragon/signal-persona-orchestrate` | `7282c352` | `feat: validate orchestrate boundary strings` |
| `/git/github.com/LiGoldragon/signal-persona-system` | `1f9b2154` | `docs: correct system contract upgrade truth` |
| `/git/github.com/LiGoldragon/persona-orchestrate` | `7f0bf022` | `docs: clarify orchestrate state ownership` |
| `/git/github.com/LiGoldragon/persona-message` | `3046a46e` | `docs: clarify component-owned sema state` |
| `/git/github.com/LiGoldragon/persona-sema` | `8954770a` | `docs: clarify component actor ownership` |

Remote `main` was verified after each push.

## `signal-persona-orchestrate`

Files changed:

- `/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-persona-orchestrate/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-persona-orchestrate/README.md`
- `/git/github.com/LiGoldragon/signal-persona-orchestrate/ARCHITECTURE.md`

What changed:

- Added a public `Error` enum and `Result<T>` alias for boundary
  construction failures.
- Replaced unchecked `new` constructors with:
  - `WirePath::from_absolute_path`
  - `TaskToken::from_wire_token`
  - `ScopeReason::from_text`
- Added `TryFrom<String>` and `TryFrom<&str>` for each boundary newtype.
- Made `WirePath` reject relative paths, empty paths, and `..` components.
- Made `WirePath` normalize slash-separated absolute paths by collapsing
  empty path components and `.` components.
- Made `TaskToken` reject empty tokens, bracketed tokens, and whitespace.
- Made `ScopeReason` reject blank and multiline text.
- Updated round-trip tests and docs to use the fallible constructors.

Why it matters:

`WirePath`, `TaskToken`, and `ScopeReason` are contract types. If the type name
claims an invariant, the constructor should enforce it at the contract boundary
rather than leaving each downstream consumer to rediscover the rule.

## `signal-persona-system`

Files changed:

- `/git/github.com/LiGoldragon/signal-persona-system/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-persona-system/ARCHITECTURE.md`

What changed:

- Corrected the `SystemTarget` comment: adding future backend variants is a
  coordinated schema upgrade because the enum is closed and unknown variants
  are rejected.
- Corrected `ARCHITECTURE.md` from "15 round-trip tests" to the real current
  surface: 14 tests covering all 6 request variants, all 5 event variants,
  every `InputBufferState`, both `SubscriptionKind` values, and representative
  `From` impl witnesses.

Why it matters:

The old comment taught the closed-enum lesson backwards. Closed enums are good
because consumers fail loudly on unknown variants; that makes extension a
coordinated contract change, not a free compatible addition.

## Sema Ownership Wording

Files changed:

- `/git/github.com/LiGoldragon/persona-orchestrate/README.md`
- `/git/github.com/LiGoldragon/persona-message/README.md`
- `/git/github.com/LiGoldragon/persona-sema/README.md`

What changed:

- Removed retired references to `persona-store` and a central store actor.
- Reworded the docs around the current target architecture:
  state-bearing Persona components own their own Sema databases through
  `persona-sema`, and each component actor sequences its own writes.
- Left `persona-sema` framed as the typed schema/open/table-convention layer
  over the Sema redb/rkyv kernel.

Why it matters:

This keeps the public README layer aligned with
`reports/designer/92-sema-as-database-library-architecture-revamp.md` and the
current Sema-as-library direction. There is no shared store actor boundary to
teach future implementers.

## Verification

Passed:

- `nix flake check` in `/git/github.com/LiGoldragon/signal-persona-orchestrate`
- `nix flake check` in `/git/github.com/LiGoldragon/signal-persona-system`
- `nix flake check` in `/git/github.com/LiGoldragon/persona-orchestrate`
- `nix flake check` in `/git/github.com/LiGoldragon/persona-message`
- `nix flake check` in `/git/github.com/LiGoldragon/persona-sema`
- `nix develop --command cargo test` in
  `/git/github.com/LiGoldragon/signal-persona-orchestrate`:
  23 tests passed.
- `nix develop --command cargo test` in
  `/git/github.com/LiGoldragon/signal-persona-system`: 14 tests passed.

Notes:

- Some Nix invocations emitted transient eval-cache "database is busy" lines;
  the builds/tests still completed successfully.
- `persona-message` still emits flake app `meta` warnings and reports
  `running 0 flake checks`; that pre-existing flake-shape hygiene was not part
  of this fix pass.

## Current State

The findings from `reports/assistant/95` are now fixed.

The next live implementation gap remains `primary-9iv`: implement
`persona-orchestrate` against `signal-persona-orchestrate`, using
component-owned Sema state and the backward-compatible lock-file projection
described by the orchestration protocol.
