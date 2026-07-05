# Rust Auditor Review

Task: audit completed implementation for tracker bead `primary-xi6z.1` in `/git/github.com/LiGoldragon/upgrade` at commit `d4724bc5a20a`, without source edits, tracker mutation, Spirit mutation, commit, or push.

## Verdict

Conditionally acceptable as a read-only deterministic awareness core, but I would not treat the slice as fully accepted until the added-field classification is made more conservative or explicitly backed by schema facts such as optional/default/new-table-only semantics.

## Blocking issues

1. `src/schema_diff.rs:671-679` classifies every added field in an existing family as `AutoSafe` using only `FieldPresentOnlyInNew` as evidence. The snapshot model has no required/optional/default/backfill fact, so this is not conservative enough for durable SEMA evolution: an old record loaded under the new schema may lack the new field. Expected correction: classify added fields as `NeedsExplicitUpgradeRule` unless the schema input carries an explicit fact that the field is optional, defaulted, derived, or otherwise safe for all legacy records.

## Non-blocking follow-ups

- `src/schema_diff.rs:8-15` and `src/schema_diff.rs:45-62` silently overwrite duplicate family or field identities. If actual schema-emitted inputs already guarantee uniqueness this is acceptable, but the public constructor currently has no typed error path or duplicate fact. A future boundary should either accept only validated schema-emitted snapshots or return a typed construction error for duplicate identities.
- The API is a useful typed in-memory core, but it is still hand-fed by local snapshot structs and string-backed domain values. The next slice should add the adapter from the schema-emitted SEMA/schema source so the awareness path is anchored in the declared schema pipeline rather than a parallel caller-assembled model.
- Tests cover all claimed categories in one integrated fixture, but mostly via substring assertions over `stable_text`. Add exact typed-change assertions or a golden full report to pin ordering and prevent accidental extra/missing changes.

## Evidence

- Tracker read: `bd show primary-xi6z.1` confirmed acceptance criteria: stable deterministic report; detect added/removed/likely-renamed families, added/removed/likely-renamed fields, type changes, key/storage identity changes, family hash changes; classify as `AutoSafe`, `NeedsExplicitUpgradeRule`, or `Unsupported`; explain facts; tests/fixtures cover every category; read-only path; no mirror noun.
- Intent query: public Spirit text search for upgrade/schema/diff/evolution surfaced record `w312`, supporting deterministic mechanism for derivable classification work.
- Changed implementation inspected:
  - `src/schema_diff.rs`
  - `src/lib.rs`
  - `tests/schema_diff.rs`
  - `ARCHITECTURE.md`
  - `Cargo.toml`
- Read-only behavior: `schema_diff.rs` contains no `redb`, daemon, selector, store, or mirror references. It only compares in-memory snapshots and returns a report.
- Determinism: implementation uses `BTreeMap`/`BTreeSet` for identity ordering and sorts final changes by stable text. Rename heuristics are deterministic, including tie choice by ordered identity.
- Typed/component-neutral shape: public API exposes domain newtypes (`FamilyIdentity`, `FieldIdentity`, `StorageIdentity`, `KeyIdentity`, `FamilySchemaHash`, `FieldType`) and typed enums for changes/facts/classifications. No component-specific or mirror-as-noun assumption found.
- Claimed category coverage in `tests/schema_diff.rs`: integrated fixture covers added/removed/likely-renamed families, added/removed/likely-renamed fields, type change, key identity change, storage identity change, family hash change, and all three classifications.
- Commit/push claim verified: repository HEAD is `d4724bc5a20a7081adf2f2b5bc44bccadd446090`; `origin/drop-next` resolves to the same commit; `HEAD` is an ancestor of `origin/drop-next`.

## Verification commands/results

- `bd show primary-xi6z.1` from `/home/li/primary`: succeeded; bead is closed with the acceptance criteria above.
- `git -C /git/github.com/LiGoldragon/upgrade status --short --branch`: clean detached HEAD at `d4724bc`.
- `git -C /git/github.com/LiGoldragon/upgrade log -1 --oneline --decorate`: `d4724bc (HEAD, origin/drop-next, drop-next) upgrade: add deterministic sema schema diff awareness (Codex GPT-5)`.
- `cd /git/github.com/LiGoldragon/upgrade && CARGO_TARGET_DIR=/tmp/upgrade-audit-target cargo test --test schema_diff`: passed, 1 test.
- `cd /git/github.com/LiGoldragon/upgrade && cargo fmt --check`: passed.
- `cd /git/github.com/LiGoldragon/upgrade && CARGO_TARGET_DIR=/tmp/upgrade-audit-target cargo clippy --all-targets --all-features -- -D warnings`: passed.
- `cd /git/github.com/LiGoldragon/upgrade && nix build --no-link .#checks.x86_64-linux.test`: passed.
- Final `git -C /git/github.com/LiGoldragon/upgrade status --short --branch`: clean; no source edits made.
