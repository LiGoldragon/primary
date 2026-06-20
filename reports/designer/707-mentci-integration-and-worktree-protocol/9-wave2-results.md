# 707-9 — Wave 2 results (both builds green; safety resolved)

Both headline builds landed as designer prototypes on branches (operator
integrates main), independently verified on origin.

## mentci re-found on the live contracts (intent 7x5z / sub-report 5)

Three branches, all `re-found-on-live-contracts`, off operator's latest mains:
- **mentci-lib** `b94320bb` (off `360eb25c`) — the shared leg, re-founded. Deleted
  the dead skeleton (graph-signal transport, the never-built nexus dual-daemon
  model, the duplicate approval vocabulary, canvas/constructor/etc.). Kept +
  rebased onto the live contracts: MVU → `ObservationModel` (keyed by
  `ComponentSocketKind`), approval state machine + edits-as-proposals →
  `ApprovalModel` over signal-mentci's *real* types, NOTA renderer → `RenderNota`,
  and the closed-decision→criome-by-slot mapping → `CriomeVerdict` (per `t00s`).
  9/9 model tests, clippy clean.
- **signal-mentci** `58dd5a26` (off `c187a611`) — a genuine contract gap fixed:
  only `pub(crate)` constructors existed for the pending-questions readers, so no
  consumer could project them; added the public reader methods (additive). 5
  round-trip tests.
- **mentci-egui** `0239edd6` (off `075cbff4`) — the proving consumer: holds an
  `ObservationModel`, paints its `ObservationView`, renders via `RenderNota`, owns
  no approval logic of its own. Builds; live-daemon observe test passes.

Integration handoffs for operator: merge the signal-mentci public readers (the
prototype consumes them via a local-path `[patch]` that collapses to a plain dep);
the daemon's private `criome_bridge::map_decision` adopts `mentci-lib::CriomeVerdict`
when convenient. Collision risk low (only mentci-lib [orphaned] + additive
signal-mentci readers + the egui shell touched; the daemon untouched).

## Worktree registry (Spirit eh5a / sub-report 6)

Three branches `*-worktree-registry`, off each main; daemon `ba8866d2` (off
`b53f8efd`). Built across the triad: signal-orchestrate `a785cc77`
(`Worktree`/`WorktreeStatus`/`PushedState` + `RepositoryName`/`BranchName`/
`LaneName`/`PurposeText` newtypes + `Observe(Worktrees)`→`WorktreesObserved`),
meta-signal-orchestrate `6c077889` (`RegisterWorktree` + `RefreshWorktreeIndex`
orders + acks, mirroring `RepositoryIndexRefreshed`), orchestrate daemon
`ba8866d2` (`StoredWorktree` + `worktrees` redb table keyed `repository|branch`,
a `WorktreeRegistry` scanning `~/wt` and deriving `PushedState`/`last_activity`
via jj, a `WorktreeProjection` writing `orchestrate/worktrees.nota` beside the
`.lock` projections, full execution dispatch). All green against TEMP stores:
**signal 33 / meta 5 / daemon 38, 0 failures** (incl. a `worktree.rs` smoke:
register → observe → `worktrees.nota` written; + a refresh-scan test). The live
daemon (PID 653243) and store were untouched.

Integration concerns for operator/maintainer:
1. **Schema-version bump 2→3** (new `worktrees` table) — the live
   `orchestrate.redb` needs a sema-upgrade migration on integration.
2. **Pre-existing codegen skew surfaced** — the daemon main's `Cargo.lock` pins an
   *intermediate* schema-rust-next/schema-next that cannot parse the current
   contract `.schema` files at all (`ExpectedEvenMapEntries`), failing even on
   pristine main; the prototype unified all three repos to the newest codegen
   (`90d853c3`/`4b7e830a`). Operator should adopt a deliberate common codegen pin.
   (This ties to the schema-rust-next worktrees below — that lane's toolchain is
   mid-transition.)

Deferred: the `orchestrate worktree list/register/refresh` CLI adapter in primary
`orchestrate-cli` (spec in the agent report) — a follow-up once the contracts land
on main; richer scan→register lane reconciliation.

## Worktree upkeep / safety (sub-report 7, corrected by operator 445)

Both schema-rust-next worktrees are **must-not-lose** (operator corrected the
wave-1 false-positive on `structural-forms-integration`: it has unique unpushed
work, is green, and is not an ancestor of main — only *partly* superseded).
**Resolved:** operator pushed preservation bookmarks to origin —
`operator/preserve-schema-rust-next-reaction-expand` (`8b147fac`) and
`operator/preserve-schema-rust-next-structural-forms-integration` (`a0138ce1`);
the unique-unpushed-non-empty revset is now empty for both. The
catalog-vs-resolver design choice (reaction-expand) and the real
comparison/integration pass (both) are routed to the schema-toolchain owner
(nota-designer / system-designer); `reaction-expand`'s `Cargo.toml` `[patch]`
local-path pin needs repointing to a pushed branch before it builds elsewhere.

The destructive GC pass (dismantling the merged/archive worktree set + removing
the empty `nota-next/` + `upgrade/` parent dirs) stays gated on the registry's
`worktrees.nota` manifest landing on main + the GC contract's live re-verify.

## Next slices

- mentci: the CLI read+answer atom roster (grep-assertable, prints the shared
  `RenderNota`) and the criome+mentci `runNixOSTest` on Prometheus (recycle
  `criome-nixos-module-142`) — the readability/testing payoff.
- registry: the orchestrate-cli `worktree` adapter (after the contracts integrate).
- integration: operator merges the mentci + registry branches; handles the
  orchestrate live-redb migration + the codegen pin.
