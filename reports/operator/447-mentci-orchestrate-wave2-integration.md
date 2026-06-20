# 447 — Mentci and orchestrate wave-2 integration

## Scope

The psyche relayed the designer wave-2 checkpoint and operator handoffs:

- merge the re-founded Mentci shared-model branches;
- remove prototype local path patches;
- adopt the shared criome verdict mapping where convenient;
- integrate the orchestrate worktree-registry triad and fix the codegen pin
  skew surfaced by the prototype.

## Mentci integration

Landed to main:

- `signal-mentci` `58dd5a26` — public readers on
  `ProjectedInterfaceState`, needed by the shared observation model.
- `mentci-lib` `0731c374` — re-founded shared model on live contracts, with
  the local `signal-mentci` prototype patch removed.
- `mentci-egui` `8c8b426e` — consumes `mentci-lib::ObservationModel` and
  `RenderNota` from main, with local `mentci-lib` and `signal-mentci` patches
  removed.
- `mentci` `ada04788` — daemon bridge uses
  `mentci_lib::CriomeVerdict` for the closed Mentci decision to criome
  authorization decision mapping.

Retired merged feature bookmarks:

- `re-found-on-live-contracts` in `signal-mentci`.
- `re-found-on-live-contracts` in `mentci-lib`.
- `re-found-on-live-contracts` in `mentci-egui`.

Verification:

- `signal-mentci`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `mentci-lib`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `mentci-egui`: `cargo test --all-targets`;
  `cargo clippy --all-targets -- -D warnings`. The live-daemon observe test
  passed.
- `mentci`: `cargo test --all-targets`;
  `cargo clippy --all-targets -- -D warnings`.

## Orchestrate integration

Landed to main:

- `signal-orchestrate` `a785cc77` — worktree registry contract surface.
- `meta-signal-orchestrate` `135c2e7a` — worktree register/refresh meta
  orders, then a portability fix removing the prototype local path patch and
  resolving `signal-orchestrate` from main.
- `orchestrate` `0cd09045` — daemon-owned worktree registry state, scanner,
  projection, handlers, and tests, then a portability fix removing the local
  contract path patches.

Retired merged feature bookmarks:

- `signal-orchestrate-worktree-registry`.
- `meta-signal-orchestrate-worktree-registry`.
- `orchestrate-worktree-registry`.

The codegen skew flagged by designer is resolved in the landed stack: the
contract and daemon lockfiles now resolve `schema-next` main `4b7e830a` and
`schema-rust-next` main `90d853c3`, rather than the stale intermediate pins
that could not parse the current contracts.

Verification:

- `signal-orchestrate`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `meta-signal-orchestrate`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.
- `orchestrate`: `cargo test --all-targets --features nota-text`;
  `cargo clippy --all-targets --features nota-text -- -D warnings`.

## Current state

All touched code checkouts are clean and aligned with origin main:

- `signal-mentci`
- `mentci-lib`
- `mentci-egui`
- `mentci`
- `signal-orchestrate`
- `meta-signal-orchestrate`
- `orchestrate`

The designer lock still advertises the old `mentci-lib` feature worktree, but
the remote branch has been integrated and deleted. That lock should be released
by the designer lane.

Next operator-safe Mentci slice: CLI read+answer roster, then the egui approval
card, then the criome+mentci VM proof.
