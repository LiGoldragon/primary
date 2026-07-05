# General Code Implementer Evidence

## Task and Scope

Implemented tracker bead `primary-xi6z.1`: first read-only vertical slice for deterministic SEMA schema evolution. Scope was a deterministic old/new SEMA schema diff awareness library entry point that reports schema facts and classifies changes without mutating live stores, daemon state, selectors, or compatibility shims. The implementation avoids mirror-as-noun framing.

## Repositories and Files Consulted

- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/protocols/active-repositories.md`
- `/git/github.com/LiGoldragon/upgrade/AGENTS.md`
- `/git/github.com/LiGoldragon/upgrade/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/upgrade/skills.md`
- `/git/github.com/LiGoldragon/signal-upgrade/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/meta-signal-upgrade/ARCHITECTURE.md`
- Spirit query: public text search for SEMA schema evolution/upgrade; relevant conclusion was that deterministic derivable classification belongs in code/schema machinery rather than agent judgment (`w312`).

## Changed Files

In `/git/github.com/LiGoldragon/upgrade`:

- `src/schema_diff.rs` — added typed read-only schema-diff model and report engine:
  - `SemaSchemaSnapshot` as old/new input model;
  - family, storage, key, hash, field, and type identity domain objects;
  - deterministic `SchemaDifferenceReport::stable_text()`;
  - detection for added/removed/likely-renamed families;
  - detection for added/removed/likely-renamed fields;
  - detection for type changes;
  - detection for key identity changes, storage identity changes, and family hash changes;
  - classifications: `AutoSafe`, `NeedsExplicitUpgradeRule`, `Unsupported`;
  - schema facts explaining each classification;
  - deterministic rename heuristics documented in emitted facts.
- `src/lib.rs` — exported the schema-diff API.
- `tests/schema_diff.rs` — added fixture coverage for every required detection/classification category.

## Classification Shape

- Added family and added field: `auto-safe`.
- Removed family and storage identity change: `unsupported`.
- Likely rename, removed field, type change, key identity change, and family hash change: `needs explicit upgrade rule`.

Likely rename detection is intentionally heuristic and deterministic:

- family rename: same storage plus same key identity, or at least two same-name fields with identical types;
- field rename: removed/added field pair within the same family with identical type text.

The report includes `HeuristicLimit` facts so downstream upgrade planning knows these are awareness signals, not implicit migration rules.

## Tracker Update

- `bd close primary-xi6z.1 --reason "Implemented in upgrade commit d4724bc5a20a on drop-next: deterministic read-only SEMA schema diff awareness API with tests."`
- Result: bead `primary-xi6z.1` closed. The tracker also reported parent `primary-xi6z` closed as all steps complete.

## Verification

Commands run in `/git/github.com/LiGoldragon/upgrade`:

- `cargo fmt` — passed.
- `cargo test schema_difference_report_is_deterministic_and_classified` — passed.
- `cargo test` — passed: 26 tests passed including the new schema diff test.
- `nix flake show --all-systems --no-update-lock-file` — passed/evaluated outputs.
- `nix build --no-update-lock-file .#checks.x86_64-linux.test` — first run failed because new files were untracked and not included in the clean Nix source; after staging/tracking the new files, rerun passed.
- `nix build --no-update-lock-file .#checks.x86_64-linux.clippy` — passed.
- `nix build --no-update-lock-file .#checks.x86_64-linux.fmt` — passed.

## Commit and Push

Committed and pushed in `/git/github.com/LiGoldragon/upgrade`:

- Branch/bookmark: `drop-next`
- Commit: `d4724bc5a20a`
- Message: `upgrade: add deterministic sema schema diff awareness (Codex GPT-5)`
- Push result: `drop-next@origin` matches local `drop-next`.

Primary workspace already had unrelated uncommitted files before this task. This output file was written under the required agent output path; no unrelated primary changes were reverted.

## Unmet Acceptance Criteria or Blockers

No acceptance criteria are intentionally unmet for this read-only slice. The library accepts typed schema snapshots rather than parsing authored `.schema` files directly; that is the smallest coherent slice in the `upgrade` runtime and keeps this work awareness-only. A future slice can adapt authoritative schema AST emission into `SemaSchemaSnapshot` once the schema source type exposes all family storage/key/hash facts at the desired boundary.
