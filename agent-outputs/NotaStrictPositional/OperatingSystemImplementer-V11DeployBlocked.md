# Spirit v10→v11 Strict-Positional Deploy — BLOCKED (live system untouched)

## Task and scope

Deploy the prepared `spirit` v10→v11 strict-positional store migration
(`spirit-strict-positional-v11 @ b3f19a6c`) to its live host, following the
runbook `agent-outputs/NotaStrictPositional/GeneralCodeImplementer-V11StoreMigration.md`:
land → stop daemon → migrate live store → deploy new closure → verify, with
rollback available. Plus an independent tail: record one psyche-authorized
Spirit intent record.

Outcome: **the deploy is BLOCKED before any live-mutating step.** Multiple
independent blockers, the decisive one found by a zero-impact dress rehearsal on
a throwaway copy of the production store. **No live-system state was changed by
the deploy attempt** (no daemon stopped, no live store migrated, no branch
landed, no deploy submitted). Rollback was NOT needed. The intent tail
succeeded.

## Live-system ground truth (host `ouranos`)

- Spirit daemon runs as user service `spirit-daemon.service` (active, running),
  binary `/nix/store/kmbmmkh52wak5c7qhvls1jgr5shwmgfm-spirit/bin/spirit-daemon`.
- Live store: `/home/li/.local/state/spirit/spirit.sema` (main) +
  `/home/li/.local/state/spirit/spirit.archive.sema` (archive sibling). These
  are the psyche's production intent store on this machine.
- The daemon unit's `ExecStartPre` already runs `spirit-migrate-store
  "($database_path)"` on start — the migration runs automatically at service
  activation inside the closure; it is not a purely out-of-band step.
- Existing store backups run through `spirit.schema-old-backup-11.sema` (next
  mint would be `-12`); archive backups through `-3` (next `-4`).
- Live domains render with bare leaves, e.g. `(Technology (Software Quality))`
  and `(Technology (Software (Engineering Architecture)))` — the OLD (v10,
  `Option<Leaf>` = None) rendering. The live store is pre-migration schema v10.

## BLOCKER A (decisive, empirically proven) — migrator fails on the live archive sibling

Method: built the migrator from the working copy —
`nix build .#store-migration` → `/nix/store/z4xapwcmf66q5fdsk3mnn4ydq50z8dhz-spirit-0.19.0/bin/spirit-migrate-store`
— and ran it against a COPY of the live store + archive (never the live files).

Full-set rehearsal (main + archive sibling) result:

```
spirit-migrate-store: layout-3 spirit store: engine storage layout 5 does not match this build's layout 3; the store was written under an older engine layout and must be rebuilt through checkpoint import or versioned replay
MIGRATOR_EXIT=1
```

Isolation:
- **Main store alone migrates cleanly**: `(Migrated (21 932))`. Verified the
  migrated main store with a throwaway `Store::open` reader:
  `store_schema_version = 11`; marker =
  `Migration { source_schema_version: SourceSchemaVersion(10), migrated_record_count: 21, migrated_referent_count: 932 }`.
  So the main-store migration path is fully correct (v11, marker source=10).
- **Archive sibling fails**: in the real path it errors on the layout-3 engine
  rejecting a layout-5 store; forced through the main path it additionally hits
  `referent name is not lowercase kebab-case: CriomOS` (a test artifact of that
  forcing — the real archive path folds only records, not referents).

Root cause (code, `src/production_migration.rs`): `migrate_archive_sibling`
(≈L2818) tries, in order, `SpiritStoreV10LegacyFamilyCurrentArchiveDatabase`,
`SpiritStoreV9CurrentArchiveDatabase`, `SpiritStoreV9Layout3ArchiveDatabase`,
then falls through to `SpiritStoreV10Layout3ArchiveDatabase::open(...)?`
(layout-3). The archive reader set (defs at L225–L298) has **no
`SpiritStoreV10CurrentArchiveDatabase`** (current-family, engine layout 5),
whereas the main-store path DOES have the parallel
`SpiritStoreV10CurrentLiveDatabase` (L273). The live archive `spirit.archive.sema`
is current-family / engine layout 5 / schema 10 — the same generation as the
main store — so every archive reader misses and the code falls through to the
layout-3 reader, which hard-rejects layout 5. The prepared migration was tested
only against seeded v10 stores that do not reproduce the live archive's
current-family layout-5 shape.

Data-safety note (good news): the migration ordering is
`migrate_archive_sibling` (L2794) BEFORE the main store backup-hard-link + rename
(L2802–L2804), and the archive error occurs during a READ (opening the
layout-3 reader), before any archive write. So even running this against the
LIVE store would leave BOTH the live main store and the live archive UNCHANGED
at v10 (it would only drop an orphan `*.schema-10-migrating-*.sema` temp).
It fails crash-safely — but it cannot succeed, so I did not run it live.

## BLOCKER B (premise error) — the deployed spirit is 0.20.0 (main line), not the runbook's 0.19.0 baseline

The runbook states the deployed baseline is `criome-authorization-push @
202a6e24` (0.19.0, pinning old signal-spirit). Independently verified this is
WRONG:
- CriomOS-home's committed `flake.lock` pins `spirit.locked.rev =
  4c9065d254e921fc143af0c1e16d1f4c7e7cf377`; `spirit.url =
  github:LiGoldragon/spirit` (no `ref` → tracks `main`).
- That rev's `Cargo.toml` version = **0.20.0**, and `4c9065d` **is** an ancestor
  of `main`.
- The running binary `/nix/store/kmbmmkh52...-spirit` derives from
  `w6ddxnfgfpfq4yfhmlkyfnvs9gvvzx7l-spirit.drv` (spirit 0.20.0).
- The prepared branch `b3f19a6c` = **0.19.0**, and is **NOT** an ancestor of
  `main` (it is on the divergent `criome-authorization-push` line, child of
  `202a6e24`).

Consequence: deploying `b3f19a6c` would be a cross-branch move that REGRESSES
spirit 0.20.0 → 0.19.0, dropping the 0.20.0 work (runtime-overridable guardian
prompt, strict-bar role, guardian-prompt re-home, meta-signal-spirit 0.5.0
relock). The v11 migration is branched off the wrong (non-deployed) baseline.

## BLOCKER C (interface drift) — deployed meta-lojix contract differs from the loaded doctrine

The installed `meta-lojix` is lojix 0.3.10. The `operating-system-operations`
skill documents the newer 0.4.0 contract (`(Deploy (Host ...))`,
`CompleteHost`/`BaseHost`, `RequireImmutable`). The running daemon REJECTS that
shape — probe: `meta-lojix "(Deploy (Host ()))"` → `unknown DeployRequest
variant Host`. The deployed 0.3.10 contract is `DeployRequest [(System
SystemDeployment) (Home HomeDeployment)]`; the spirit daemon is a home-manager
user service, so it is a `(Deploy (Home ...))` HomeOnly deploy (8 positional
fields, `HomeMode = Activate`, no `RequireImmutable`).

## BLOCKER D (deploy chain) — meta-lojix takes no spirit ref directly

`meta-lojix` builds Home deploys from CriomOS-home's
`homeConfigurations.<user>.activationPackage`; the daemon overrides only
horizon/system/secrets inputs, never `spirit`. So the deployed spirit rev is
fixed by CriomOS-home's committed `flake.lock`. To land any spirit change one
must: push the spirit rev; repoint CriomOS-home's `spirit` input to it and push
CriomOS-home (a plain `nix flake update spirit` would resolve `main`, not the
divergent `b3f19a6c` — the rev must be pinned explicitly); then
`meta-lojix "(Deploy (Home (goldragon ouranos li <proposal-path>
github:LiGoldragon/CriomOS-home/<new-rev> Activate None [])))"`; then verify via
`lojix "(Query (ByNode (goldragon ouranos None)))"`.

Node identity confirmed: cluster `goldragon`, node `ouranos`, user `li`.
`lojix "(Query (ByNode (goldragon ouranos None)))"` returns generations; current
home generation observed as HomeOnly / Switch / Current.

## What a human / follow-up must do (and the proof for each)

1. **Fix the archive-sibling migration (Blocker A).** Add a current-family
   layout-5 v10 archive reader (`SpiritStoreV10CurrentArchiveDatabase`, the
   archive analogue of `SpiritStoreV10CurrentLiveDatabase`) and use it in
   `migrate_archive_sibling` before the layout-3 fallback. Add a regression test
   seeding a current-family layout-5 v10 archive. Proof: rehearse the migrator on
   a fresh COPY of the live `spirit.sema` + `spirit.archive.sema` and get
   `(Migrated ...)` with no error, then a throwaway `Store::open` reader showing
   both stores at schema 11 with marker `source_schema_version = 10`.
   (Reusable rehearsal recipe: `cp` both live `.sema` files into a temp dir
   preserving the `spirit.sema` / `spirit.archive.sema` names, run
   `spirit-migrate-store "(<tmp>/spirit.sema)"`.)
2. **Resolve the baseline/version conflict (Blocker B).** Rebase the v11
   strict-positional work onto the deployed `main` line (spirit 0.20.0, rev
   `4c9065d`/current `main` 11452d6d) instead of the divergent 0.19.0
   `criome-authorization-push` line, bump the version forward (>= 0.20.0), and
   re-run `nix flake check`. Confirm with the psyche whether a 0.20.0→0.19.0
   regression is intended (it almost certainly is not).
3. **Use the deployed 0.3.10 deploy contract (Blocker C/D)**, not the skill's
   0.4.0 shape: push spirit → repoint+push CriomOS-home `spirit` input (pin the
   exact rev) → `(Deploy (Home (goldragon ouranos li <proposal-path>
   github:LiGoldragon/CriomOS-home/<new-rev> Activate None [])))`. Proof: new
   HomeOnly generation `Current` in the lojix node query, `spirit-daemon.service`
   restarted onto the new closure, its `ExecStartPre` migrator logging
   `(Migrated ...)` then the daemon serving v11 domain queries (bare
   `(Software Quality)` becomes `(Software (Quality All))`).
4. **The operating-system-operations skill is stale** for this host (documents
   0.4.0; deployed daemon is 0.3.10). Recommend reconciling the skill with the
   deployed lojix contract, or upgrading lojix on ouranos. (Provisional
   recommendation — not applied here.)

## Verification against the runbook's step 5 (partial, on the rehearsal copy)

- Store opens as v11: YES for the main store (`store_schema_version = 11`).
- Marker `source_schema_version = 10`: YES for the main store (confirmed above).
- Domain strict-positional on the LIVE daemon: NOT possible until Blocker A is
  fixed and the closure deployed (the v11 daemon cannot come up while the archive
  fails to migrate). The migration remap logic itself is proven green by the
  landed golden test `migrates_version_ten_strict_positional_technology_domains`.

## Rollback

Not needed. Nothing on the live system was changed by the deploy attempt: the
daemon was never stopped, the live `spirit.sema` / `spirit.archive.sema` were
never migrated (all migration runs were on throwaway `/tmp` copies, since
deleted), no branch was landed, and no deploy was submitted. `flake check` was
green on `b3f19a6c` content, and the migrator built cleanly.

## Intent tail (independent of deploy outcome) — DONE

Recorded via the deployed Spirit CLI:
`(Constraint)` domain `(Technology (Software (Engineering Architecture)))`,
certainty High, importance High, privacy Zero, referents `[codec typed-codec
wire-format]`; testimony verbatim. First attempt was ReferentGuardian-rejected
for referent `serialization` ("abstract concept, not a nameable particular");
resubmitted with valid referents.

- Statement: "Structured data must be encoded and decoded through the canonical
  shared codec for its format; hand-rolled or special-cased per-type encoding or
  decoding logic is forbidden."
- Result: `(RecordAccepted qvb3)` → record identifier **`qvb3`**.

## Files / commands consulted

- Runbook: `agent-outputs/NotaStrictPositional/GeneralCodeImplementer-V11StoreMigration.md`
- Spirit repo `/git/github.com/LiGoldragon/spirit`: `flake.nix`,
  `src/production_migration.rs`, `src/bin/spirit-migrate-store.rs`,
  `src/store/mod.rs`, `src/schema/sema.rs`, `src/render.rs`.
- `nix build .#store-migration`; `nix flake check -L` (green on b3f19a6c);
  migrator dress rehearsal on throwaway copies; throwaway `Store::open` verifier
  (added + removed; working copy left clean).
- `systemctl --user cat/status spirit-daemon.service`; daemon open-fd probe;
  `lojix "(Query (ByNode (goldragon ouranos None)))"`.
- CriomOS-home `flake.lock` (spirit pin), spirit `Cargo.toml` at revs
  `4c9065d` (0.20.0) and `b3f19a6c` (0.19.0); jj ancestry checks.
- Deploy-mechanics investigation (read-only subagent) for the lojix 0.3.10
  contract and CriomOS-home wiring.
