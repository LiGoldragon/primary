# 180 — schema v13 model and upgrade implementation

*Kind: Implementation Report · Topic: schema-v13-model-upgrade · Date: 2026-05-24*

## Summary

Implemented the current `/326-v13` + operator `/174-v5` schema-language shape in `/git/github.com/LiGoldragon/schema`.

The crate now models the fixed six-position authored `.schema` form:

1. imports map
2. ordinary signal header
3. owner signal header
4. sema header
5. namespace map
6. features vector

The old flexible section-vector surface has been replaced with `Schema` / `Document` over explicit imports, three headers, namespace, and features.

## Landed

- Added import model:
  - `Imports`
  - `ImportDirective::Import`
  - `ImportDirective::ImportAll`
  - `ImportResolution`
  - collision diagnostics for import-import and import-local collisions
- Added uniform v13 route headers:
  - every `HeaderRoot` carries a non-empty `Vec<Name>` sub-variant vector
  - no scalar `(Root Payload)` model exists in the Rust API
  - every lowered `Route` has an endpoint slot, including one-sub-variant roots
- Added `AssembledSchema`:
  - import bindings
  - explicit route table
  - local/imported type entries
  - feature metadata
- Added route/body validation:
  - route endpoints resolve through namespace body declarations
  - route-root namespace keys are reserved by the route body declaration
  - extra route-body variants not listed in the header are rejected
  - unit endpoints lower to explicit `RouteBody::Unit`
- Added MVP feature model:
  - `Reply`
  - `Event`
  - `Observable`
  - `Upgrade`
- Added upgrade model:
  - `UpgradeAnnotation::{Migrate, RenamedFrom, Drop, Custom, Untranslatable}`
  - `AssembledSchema::plan_upgrade_from`
  - inferred identity projection
  - inferred additive enum-variant projection
  - explicit annotations required for changed records
  - `Drop` / `Untranslatable` required for removed types
- Updated repo docs:
  - `README.md`
  - `INTENT.md`
  - `ARCHITECTURE.md`
  - `AGENTS.md`

## Tests

Validated in `/git/github.com/LiGoldragon/schema`:

- `cargo fmt -- --check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --option max-jobs 0`

The Nix check ran on the remote builder and passed.

## Important Design Edge

Operator `/174-v5` correctly identifies that `/326-v13`'s rich example cannot reuse `State` as both an ordinary data type and a route-body declaration in the same flat namespace.

The implementation follows the operator recommendation: flat namespace keys are unique, so route-root body declarations reserve their key. A schema wanting both ideas must rename the ordinary data type, such as `PresenceSnapshot`, or later introduce a separate route-body section if psyche changes the architecture.

## What This Does Not Do Yet

- No NOTA text parser yet.
- No Rust type/code generator yet.
- No short-header table emission yet.
- No live Spirit database migration yet.
- No repo-wide boilerplate schema file sweep yet.
- No sandbox copy of the production Spirit database yet.

## Best Next Slice

Use this crate as the typed target for `primary-ezqx.1`: parse the Spirit v0.1 `.schema` into `Schema`, assemble it, and emit the first short-header route table from `AssembledSchema`.

For the repo-wide boilerplate sweep from designer `/327`, avoid doing it from this implementation lane unless explicitly assigned; it is broad cross-repo prep and will conflict with the designer-dispatched marking sweep if run concurrently.
