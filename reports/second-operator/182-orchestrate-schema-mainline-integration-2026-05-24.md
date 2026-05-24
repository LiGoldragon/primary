# 182 — Orchestrate schema mainline integration

*Kind: Implementation Report · Topic: orchestrate-schema-upgrade · Date: 2026-05-24 · Lane: second-operator*

## Outcome

Implemented the operator/mainline part of the orchestrate schema upgrade after intent record 517 clarified the branch topology: designers work in `~/wt` feature branches; operators maintain and rebase `main`.

Pushed commits:

- `/git/github.com/LiGoldragon/orchestrate` — `59669e30` — `orchestrate: add schema upgrade witness`
- `/git/github.com/LiGoldragon/signal-orchestrate` — `2e1a832e` — `signal-orchestrate: mark schema-engine upgrade`
- `/git/github.com/LiGoldragon/signal-orchestrate` — `df605591` — `signal-orchestrate: validate concept schema`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate` — `37bbf4da` — `owner-signal-orchestrate: validate concept schema`

## What Changed

`orchestrate` now has real parser-backed schema files:

- `schema/orchestrate-types-v0-1.schema`
- `schema/orchestrate-storage-v0-1.schema`
- `schema/orchestrate-v0-1.schema`
- `schema/orchestrate-v0-1-1.schema`
- `schema/orchestrate.concept.schema`

The runtime repo now depends on `schema` for tests, includes `schema/` in the Nix source filter, and has `tests/schema_contract.rs` proving:

- local `./` schema imports resolve;
- ordinary and owner route legs lower into `AssembledSchema`;
- short-header lookup finds ordinary and owner routes;
- v0.1.1 plans an additive no-downtime upgrade from v0.1 using `BranchTopology`;
- the concept schema is not marker-only text anymore.

`signal-orchestrate` and `owner-signal-orchestrate` now also have parser-backed concept schema tests. Their old marker-only `(Version 0 1)` / `(Status Concept)` feature vectors were replaced with schema-reader-compatible declarations.

## Verification

Passed:

- `/git/github.com/LiGoldragon/orchestrate`: `cargo test`
- `/git/github.com/LiGoldragon/orchestrate`: `cargo clippy --all-targets -- -D warnings`
- `/git/github.com/LiGoldragon/orchestrate`: `nix flake check --option max-jobs 0`
- `/git/github.com/LiGoldragon/signal-orchestrate`: `cargo fmt && cargo test && cargo clippy --all-targets -- -D warnings`
- `/git/github.com/LiGoldragon/signal-orchestrate`: `nix flake check --option max-jobs 0`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate`: `cargo fmt && cargo test && cargo clippy --all-targets -- -D warnings`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate`: `nix flake check --option max-jobs 0`

## Remaining Gaps

1. Runtime code is still hand-written. This slice proves schema text can parse, import, lower, and plan an upgrade; it does not yet replace `signal_channel!`, `signal_cli!`, or `OperationLowering`.
2. Engine/Sema-effect annotations are still outside parsed `.schema` files. Current `OperationLowering` tests remain the authority for `Assert` / `Mutate` / `Retract` / `Match` / `Subscribe`.
3. The schema reader currently requires explicit imports for names referenced by features. `ImportAll` works for type expressions, but feature validation does not treat unresolved wildcard imports as enough.
4. Current schema version is still filename/catalogue convention (`orchestrate-v0-1.schema`), not a settled in-file field.

## Best Next Slice

After the Spirit macro pilot lands, wire generated schema outputs into orchestrate in this order:

1. generated short-header table checked against `tests/schema_contract.rs`;
2. generated ordinary/owner request enums checked against current contract route names;
3. generated lowering/engine annotations replacing the hand-written `OperationLowering` map;
4. generated storage descriptors checked against `OrchestrateTables`.
