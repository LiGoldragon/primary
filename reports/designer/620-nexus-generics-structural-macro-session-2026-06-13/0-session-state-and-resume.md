# Session state & resume anchor (2026-06-13)

Context dump before a smaller-context restart. This directory captures every
design and open problem from a long system-designer session with psyche `li`.
Read this file first; the others go deep on each thread.

## What this session was about

Started as a Spirit guardian corpus-health investigation (reports 615-617),
moved into the **Nexus runtime flaw** (reports 618-619), then deep into
**schema-level generics** and the **NOTA structural-macro machinery**, and
ended mid-flight on a **referent-guardian fix + deploy**. Ultracode was on.

## Companion files in this directory

- `1-nexus-frame-and-ideal-generated-code.md` — the flaw, the ideal generated
  code (engine-bound `reaction::Plane`, no ZST, no alias), what changed since
  reports 618/619.
- `2-schema-generics-and-structural-macros.md` — the two new schema syntax
  forms, the `reaction.schema` file kind, the structural-macro-machinery
  verdict (what it can/can't do), and SD's TypeReference question (D5-1 /
  primary-xzzf).
- `3-referent-guardian-fix-and-deploy.md` — the referent admission flaw, the
  prompt fix, the built binary, and the exact resumable deploy state.

## Prior reports this builds on (already on main)

- `617-spirit-guardian-corpus-health-and-referent-activation` — guardian bundle
  = whole corpus (O(n²)); scoped-retrieval fix; referent activation; caching.
- `618-nexus-runtime-naming-and-driver-fork-flaw` — three flaws: (1) universal
  reaction frame re-authored per component [central], (2) `Nexus*` prefix
  (C-CRATE-PREFIX), (3) spirit hand-writes `execute_to_reply` driver fork.
- `619-ideal-nexus-plane-generated-code` — the target: `reaction::Plane` frame
  shared once; per-component output collapses ~2577 lines → payload enums + one
  binding. NOTE 619 still shows the engine-bound `impl Plane for Nexus` shape;
  §2 here records the further evolution to direct-application syntax.

## Intent captured this session (Spirit)

- `sarw` (Principle Medium): [Generated and schema-emitted Rust avoids
  transparent type aliases as a binding or naming mechanism; prefer real
  data-bearing types and trait or associated-type bindings over a pub type
  alias.] — from "I dont like type aliases".
- `n6fz` (Principle High): [The Signal, Nexus, and SEMA reaction-frame types
  Work, Action, and the canonical five-variant action set are
  workspace-universal and must be declared once and applied or bound per
  component, never hand-re-authored in each component schema; re-authoring
  universal types per component is a design failure.] — from "if theyre
  rewritten for every component, something has been badly designed".
  **`n6fz` was recorded with an EMPTY referent vector** because the
  referent-guardian rejected `triad-runtime` (the flaw being fixed). After the
  referent-guardian fix deploys, RE-SUBMIT this principle WITH referent
  `[triad-runtime]` and REMOVE `n6fz`. (Task #406.)

Already-existing intent that ALREADY covers what the psyche re-voiced (do NOT
duplicate): `xai7` (structural macro node = shape-decoded NOTA enum, type-
directed, first-match-wins, recursive, bidirectional, a derive; "the part of
NOTA original design that was never implemented"); `v0n6` (everything reading
NOTA must go through typed structural macro nodes; if a shape can't be
expressed that signals the design wasn't implemented properly — surface it);
`6grf`, `tace`, `er9w`, `jr65`, `b05y` (schema as specification language;
shape-driven node-type matching; the Rust subset).

## Todo list (live tasks)

- **#406 (in_progress)** — finish referent-guardian fix: deploy main, re-submit
  the universal-frame principle with `[triad-runtime]`, remove `n6fz`.
- **#407** — implement schema generics + convert TypeReference to a structural
  macro (the main psyche-directed task).
- **#408** — compile-prototype the `reaction::Plane` generic frame (may be
  superseded by the direct-generics shape; see §2).
- **#409** — drop `Nexus*` prefix + manifest intent into per-repo INTENT.md +
  re-absorb spirit's driver fork.
- (#402, pre-existing) replayable guardian decision journal — operator bead.

## Key revs / locations (verify before acting — may have moved)

- spirit repo `/git/github.com/LiGoldragon/spirit`: local `main` = `92dc509`
  (== origin/main), version **0.12.1**. Deployed daemon = **0.12.0** at pinned
  rev `a4cc858` (CriomOS-home flake.lock). Delta deployed→main = `c1952d1`
  (scope guardian retrieval bundle — the primary-tqe3 fix) + `92dc509` (import
  ordinary signal contract — deletes signal.rs/domain.rs ~11k lines, touches
  nexus/sema schemas).
- Built daemon (main + referent fix): `/nix/store/64n5pj7rrm1d6r992fpx7dm7jalild2d-spirit-0.12.1/bin/spirit-daemon`.
- `.sema` intent store: `~/.local/state/spirit/` (backed up this session before any restart).
- nota-next `/git/github.com/LiGoldragon/nota-next`: `derive/src/lib.rs` (the
  `StructuralMacroNode` / `ln` derive), `tests/macro_nodes.rs` (the capability
  spec), `src/macros.rs` / `parser.rs`.
- schema-next `/git/github.com/LiGoldragon/schema-next`: `identity.rs`
  (`TypeReference` enum — Vector/Optional variants), `resolution.rs`
  (ImportResolver), `raw.rs`.
- schema-rust-next `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs`:
  `PlaneEnvelopeTokens` (~2887, the `Nexus<Root>` generic-emit precedent),
  `NewtypeInherentImplTokens` (~1827, the per-item emit precedent),
  `NexusRunnerNextStepProjectionTokens` (~2017, the `into_next_step` shim to
  delete).

## Beads

- `primary-tqe3` (the guardian retrieval scoping fix) — operator IMPLEMENTED it
  as spirit `c1952d1` on main; awaiting deploy (folded into the main deploy in
  task #406). Verify bead status.
