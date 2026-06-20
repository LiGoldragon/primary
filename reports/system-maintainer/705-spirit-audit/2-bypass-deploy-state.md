# Bypass deploy — prepared state and blockers

## What's done and proven

- **Trim plan**: 1323 → 591 active records, partition-perfect, kebab referents
  on all 591, archived. `raw/plan2.json`, `raw/proposals2.json`,
  `raw/render3.py` (Import-batches + nominate list).
- **Bypass code** (spirit): `import_record` auto-registers the referents an
  imported entry carries (owner-trusted, guardian-free); new referents are
  enforced lowercase kebab-case (`register_referent_record` +
  `validate_kebab_referent`, `StoreError::NonKebabReferent`); existing names
  grandfathered. 2 tests pass (`tests/import_auto_register_referents.rs`), no
  regression. Version bumped 0.14.0 → 0.15.0.
- **Branch** `spirit-import-bypass` pushed, rebased onto spirit `main`
  (`e126e5aa`, parent `2f3f6449`). Builds via nix → `lfl7f1fy…-spirit`.
- **Migration proven safe**: `spirit-migrate-store` on a copy of the live
  store migrates `e95828f` → the 0.15.0 digest with all 1322/1324 records
  intact; the 0.15.0 daemon serves the migrated copy cleanly.

## Corrections to earlier assumptions

- "A concurrent lane is fixing spirit's build" — **inference, not fact.** No
  orchestrate lock claims spirit. The build is *already fixed on main*: the
  `2f3f6449` repin (schema-rust-next `90d853c3`) makes main build; only the
  older `ba018269` base fails (`signal-spirit` stale schema artifacts). So
  the right base is **main**, not `ba018269`.
- Cargo cannot reproduce the store's schema digest (nix applies local schema
  patches cargo doesn't); only the nix build matches.

## Deploy blockers (why I stopped before activating)

1. **CriomOS-home is claimed by `system-designer`** ("fix-it-all… deep
   build"). Pinning spirit there to my branch would collide. Workaround:
   lojix `--override-input spirit` at activation (mechanism confirmed:
   `FlakeInputOverride` / `override_input_options`), avoiding any CriomOS-home
   edit — but the exact `lojix-run` request shape for a home deploy with an
   override is not yet pinned down.
2. **Home activation taxes the live desktop.** Precedent:
   `reports/pi-operator/8-ouranos-desktop-survivability-2026-06-05.md` — a
   `lojix-run` home activation caused Niri lag, PipeWire underruns, memory
   pressure (cold-cache heavy fetch). Warm cache now should be lighter, but
   it's a real workstation operation.
3. **One-way migration**: once the store is migrated to 0.15.0, the old
   0.14.0 daemon can't open it — so a compatible daemon must persist
   (declarative pin), which is what blocker 1 complicates.
4. **Moving-target store**: active count drifted 1322 → 1324 during the
   session (concurrent intent writes). Re-snapshot immediately before execute.

## Reference: lojix home activation shape

From `reports/cloud-designer/63-browser-extension-real-session.md`:
`lojix-run "(Home goldragon ouranos li <datom.nota> github:LiGoldragon/CriomOS-home/main Activate None None)"`
Modes seen: `Eval` / `Build` / `Profile` / `Activate` — `Build` lets the
closure be built (with overrides) without activating, a safe dry run.

## Two clean paths forward

- **A — ship trim via the paid guardian path now**: `plan2` over the working
  socket (Supersede/ChangeCertainty) against the stable running 0.14.0 daemon.
  No deploy, no migration, no collision. Delivers the count reduction
  (1323→~591) reliably; referents-on-everything is reject-prone via the paid
  referent-guardian (concept referents). ~$2–5 DeepSeek, background.
- **B — land the bypass via lojix home activation with a spirit override**:
  Build-mode dry run first, then Activate; migrate the store; execute the trim
  free via meta `Import`. Delivers the full goal incl. referents-on-everything
  + persistent kebab enforcement. Heavier/workstation-risk; needs the exact
  lojix override request.
