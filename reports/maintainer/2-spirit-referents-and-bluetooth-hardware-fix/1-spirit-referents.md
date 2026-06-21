# Spirit referent repair and enforcement

## Summary

Spirit's live public active set was repaired before this pass, then enforcement was landed and deployed through the Home profile.

- Live active public records before repair: 615 total, 6 without referents, 0 non-kebab referents.
- Forced owner-side repair: `meta-spirit` imported six changes from `/tmp/spirit-referent-repair-import.nota`.
- Live active public records after repair and after deployment: 615 total, 615 with referents, 0 without referents, 0 non-kebab referents.
- Deployed Spirit now reports `VersionReported 0.16.0`.
- A non-Zero `Record` with empty referents now rejects as `(Rejected EmptyReferents)` before persistence.

## What changed

### `signal-spirit`

Commits:

- `cc5ec45ffda3` — `signal-spirit: require referents on active entries`
- `7ae038ef1af5` — `signal-spirit: bump to 0.8.0 for referent validation`

Changes:

- Added `ValidationError::EmptyReferents` to the generated contract schema.
- `Entry::validate` rejects empty referents when certainty is not `Zero`.
- Added validation tests for three cases:
  - active/non-Zero entry with empty referents rejects;
  - Zero-certainty entry may still have empty referents;
  - active entry with non-empty referents accepts.

Validation:

- `SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test`
- `cargo test`

### `spirit`

Commit:

- `b196c08ec6df` — `spirit: bump to 0.16.0 for referent enforcement`

Changes:

- Repinned `signal-spirit` 0.8.0 and refreshed stale schema-generated dependencies.
- Updated tests for generated newtype comparisons from the fresh schema emitter.
- Updated record fixtures so active records carry kebab referents.
- Updated the `State` fallback classification path to assign the `state` referent rather than creating non-Zero referent-less records.
- Updated production migration fallback records to carry `migrated-record` so old-store migration does not reintroduce active referent-less records.
- Preserved the explicit meta Import behavior: import remains owner-side migration authority, but it still rejects non-kebab referents and upserts existing identifiers. The previously-used repair path is therefore documented as privileged repair, not ordinary admission.

Validation:

- `cargo test` in `spirit` passed after the repin and fixture updates.
- Import tests still prove:
  - non-kebab import referents are refused;
  - new kebab import referents are auto-registered;
  - importing an existing record upserts in place.

### `CriomOS-home`

Commit:

- `631acec63e4e` — `home: repin spirit 0.16.0 referent enforcement`

Validation and deployment:

- `nix build --refresh --no-link --print-build-logs github:LiGoldragon/CriomOS-home/main#checks.x86_64-linux.spirit-deployment` passed.
- `lojix-run (HomeOnly ... Activate ...)` completed with status 0 in run directory `/home/li/.local/state/lojix-runs/20260621123223-spirit-referent-homeonly-ouranos`.
- Live `spirit Version` returned `0.16.0`.
- Empty-referent active write probe returned `(Rejected EmptyReferents)`.
- Post-probe public active dump remained 615 records, all with kebab referents.

## Remaining risks

- The privileged meta Import path is still a bypass of ordinary guardian/admission semantics by design. It is appropriate for owner-side repair and migration, but it must stay owner-only.
- The deployment updated the user Spirit daemon through Home activation. It did not change the current system boot generation.
- The record count stayed stable through the rejection probe, which proves the validation path did not persist the invalid test record.
