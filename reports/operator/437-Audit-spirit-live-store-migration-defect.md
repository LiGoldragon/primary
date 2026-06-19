---
variant: Audit
topic: spirit
title: live store migration defect
---

# Spirit Live Store Migration Defect

## Headline

Spirit was defective in production for two related reasons: the installed user
service was trying to start a Spirit build that did not match the live
`spirit.sema` store, and current Spirit source still missed one schema-10
family-identity half-step from the live database. The service symptom is fixed
now; the source-side migration gap is fixed on Spirit main in commit
`f1bc797c` (`spirit: recognize live v10 store family migration`).

## What Failed

The first live checks reproduced a real production outage:

- `spirit Version` failed with `transport IO error: No such file or directory`.
- `systemctl --user status spirit-daemon.service` showed `failed
  (start-limit-hit)`.
- The journal showed startup failing in `spirit-migrate-store` with
  `unrecognized spirit store schema version: 10`.
- The installed CLI also rejected the documented shorthand
  `(PublicTextSearch spirit)` with `unknown Input variant PublicTextSearch`,
  proving the user profile had an older CLI than the active Spirit docs and
  source.

After the live service moved forward, the installed CLI and daemon became
healthy again:

- `spirit Version` now returns `(VersionReported 0.14.0)`.
- `spirit "(PublicTextSearch spirit)"` returns direct `RecordsObserved`
  results.
- `spirit-daemon.service` is active and its startup reports `(Current (1321
  0))`.

## Source Bug

Current Spirit source could still not migrate a copy of the live store before
the fix. Running the current migrator against a copied
`~/.local/state/spirit/spirit.sema` failed because the live store was schema
version 10 but its registered family identities were an intermediate pair:

- `RecordsFamily@e95828fbcaa5f39eb2cedb9ad97a1280239c7db38578545f7e7d22a986467f6e`
- `ReferentsFamily@3b1fd977c03300e7b8e21bd8f39bb90eb5d910ae9c356991ae6b58138c55a229`

Those identities were neither the current generated schema-10 family pair nor
the already-known v10 legacy pair. That meant the next source/current package
could hit the same failure again when deployed against the real store.

## Fix

Spirit commit `f1bc797c` adds that observed v10 live family pair to
`src/production_migration.rs` for both the live store and its default archive
sibling. It also keeps the schema-10 probe from discarding the more precise
legacy-family probe when current-family open fails.

The new regression test
`migrates_version_ten_live_june19_family_to_current_family` seeds a schema-10
store with the exact observed family pair, runs the migration, checks the
record and referent survive, checks the migration marker is recorded, and then
checks the second migration run reports `Current`.

## Verification

I verified the fix at four levels:

- Real copied live store: current fixed `spirit-migrate-store` migrated a copy
  of the production database with `(Migrated (1321 60))`.
- Migration and process tests:
  `cargo test --features production-migration,nota-text` passed.
- Propagation regression:
  `cargo test --features mirror-shipper --test criome_gate_1of1` passed.
- Lint and package:
  `cargo clippy --features production-migration,nota-text --all-targets -- -D warnings`
  passed, and
  `nix build --builders '' --no-link --print-out-paths --log-format bar-with-logs .#default`
  passed with output `/nix/store/si3lzq8pi7liclbsg0f863cw6i0rrjlk-spirit`.

## What Went Wrong

The migration surface was chasing schema version numbers but not every
family-identity half-step that production had actually written. Schema version
10 was not one shape on disk; the live store had a schema-10 header with an
intermediate `RecordsFamily` / `ReferentsFamily` catalog. The migration code
already knew about two schema-10 half-steps, but not this third live one.

The second failure was deployment skew. The user profile initially had a Spirit
CLI/service old enough to lack `PublicTextSearch` and to reject schema version
10 outright. Source tests were green, but the deployed package and the live
database had diverged.

The practical lesson is that every production Spirit store half-step needs a
named migration fixture before code is treated as deployable. A copy of the
live store is the right witness for this class of issue; a synthetic v9/v10
fixture alone was not enough.

## Remaining Coordination

The live service is currently healthy, but `CriomOS-home` was actively claimed
and dirty under the system-maintainer lane while this fix landed, so I did not
edit or repin that deployment repo. The durable deployment follow-through is:
pin `CriomOS-home` to Spirit `f1bc797c` or newer, deploy the user profile, and
confirm the profile's `spirit`, `spirit-daemon`, and `spirit-migrate-store`
all come from that revision or a descendant.
