# Spirit 0.21.0 v10→v11 Strict-Positional Deploy — COMPLETE (live, verified)

## Outcome

The real, psyche-authorized deploy of spirit **0.21.0** (carrying the v10→v11
strict-positional store migration) to its live host `ouranos` is **COMPLETE and
VERIFIED**. The live production intent store was migrated v10→v11 with the
daemon stopped, two independent crash-safe backup sets were confirmed, the new
0.21.0 closure was activated, and the live daemon is serving the v11 store.
**No rollback was needed.** No human hand-off is outstanding — I had full node
access as `li` on `ouranos` and ran every step in-session.

## Target and inputs (all confirmed before mutating)

- Host: I am running ON `ouranos` as user `li`. Node identity: cluster
  `goldragon`, node `ouranos`, user `li`.
- Live store: `/home/li/.local/state/spirit/spirit.sema` (main) +
  `spirit.archive.sema` (archive sibling).
- spirit `origin/main = 05269499a928d54fe5f8e842e5f5436f1ca7bfbc`, version
  0.21.0, pushed. Pins signal-spirit `151d49c8` (fixed strict-positional
  contract).
- Deployed baseline: spirit 0.20.0 (binary `kmbmmkh52…`, from CriomOS-home
  spirit pin `4c9065d…`). Deployed `meta-lojix` = lojix **0.3.10** (system
  service `/nix/store/2a719h33…-lojix-0.3.10`).
- Deploy contract: HomeOnly. Confirmed the deployed daemon rejects the newer
  0.4.0 `(Host …)`/`(UserEnvironment …)` shape; the checked-out lojix repo is
  0.4.0 (ahead of deployed) and was NOT trusted for the contract. Probed the
  live daemon: `HomeDeployment` holds exactly 8 root objects (matches the
  reconciled `operating-system-operations` skill).
- Proposal source (field 4): `/git/github.com/LiGoldragon/goldragon/datom.nota`
  — the goldragon production cluster proposal (exists, names ouranos). This is
  the exact value the last several real spirit/Listener Home deploys used;
  the daemon reads it during MaterializeHorizon and rejects with
  `ProposalSourceUnreachable` when absent. spirit-daemon is NOT socket-activated
  (no `.socket` unit), so stopping it carries no mid-migration relaunch risk.

## Step-by-step outcome

### 1. Repoint CriomOS-home spirit input — DONE, pushed

- Worked on the true `origin/main` tip `406417507d6b` (the local working copy
  had been sitting on an older parent; moved onto main with `jj new main`).
- `nix flake update spirit` re-locked spirit to main head =
  `05269499a928` and pulled its transitive graph from spirit's own lock:
  signal-spirit `5d0905a7 → 151d49c8`, signal-harness `→ 0727beb7`,
  triad-runtime `→ 3d320746`, version-projection `→ 666c468e`, signal-frame
  `→ 075b0d99` — exactly the migration-evidence input stack. Old signal-spirit
  `5d0905a7` fully gone (0 occurrences). Only `flake.lock` changed (48/48).
- Verified `spirit.locked.rev == 05269499a928d54fe5f8e842e5f5436f1ca7bfbc`.
- Committed + pushed CriomOS-home main.
- **New CriomOS-home rev R = `c5a031218a8d388b40a9c62d963b85438dbb6c65`**
  (confirmed `origin/main`).

### 2. Migrator build + pre-flight rehearsal on CURRENT live data — GREEN

- Built the 0.21.0 migrator from the pushed rev:
  `/nix/store/m3x5km19qrr2whaxxbvqc4h1c8l983cq-spirit-0.21.0/bin/spirit-migrate-store`.
- Copied the CURRENT live `spirit.sema` + `spirit.archive.sema` to
  `/tmp/spirit-v11-rehearsal/` and ran the migrator against the copies:
  - main → `(Migrated (21 932))`, exit 0.
  - BOTH stores got `schema-old-backup-0` files (main + archive migrated).
  - Idempotency re-run → `(Current (21 0))`, exit 0, no new backups → store now
    at current (v11) schema. GREEN. (Rehearsal copies deleted at closeout.)

### 3. Build (dry) deploy of R — closure builds

- `meta-lojix "(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home/c5a031218a8d388b40a9c62d963b85438dbb6c65 Build None [])))"`
  → `(Deployed (37 (597 597)))`. The full home closure (with v11 spirit) builds
  and MaterializeHorizon succeeds from the datom. Daemon left untouched
  (still 0.20.0, PID 2359135, live store still v10, unchanged mtime).

### 4. Stop daemon + explicit backups — DONE

- `systemctl --user stop spirit-daemon.service` → `inactive (dead)`, store
  released (no process holding it).
- Explicit belt-and-suspenders backups (independent of the migrator):
  - `spirit.sema.predeploy-v11-20260702T164051` (5111808)
  - `spirit.archive.sema.predeploy-v11-20260702T164051` (1732608)

### 5. Migrate the LIVE store — DONE, backups confirmed, v11 confirmed

- `spirit-migrate-store "(/home/li/.local/state/spirit/spirit.sema)"`
  → `(Migrated (21 932))`, exit 0 (identical to rehearsal).
- Migrator crash-safe backups minted (the v10 originals retained):
  - `spirit.schema-old-backup-12.sema` (5111808)
  - `spirit.archive.schema-old-backup-4.sema` (1732608)
- Live stores now v11: `spirit.sema` (1011712), `spirit.archive.sema` (1638400).
- Idempotency re-run on the LIVE store → `(Current (21 0))`, exit 0, NO new
  backup (`-13`/`-5` absent) → live store at current (v11) schema.

### 6. Activate the new closure — DONE

- `meta-lojix "(Deploy (Home (… c5a031218a8d… Activate None [])))"`
  → `(Deployed (37 (600 600)))`.
- Home-manager activated new generation `home-manager-835-link` →
  `/nix/store/28qcd541mc10kipmri2fa5ij4l5785c6-home-manager-generation`.
- Activation updated the user's spirit-daemon unit ExecStart to the new binary
  `/nix/store/52f52g45…-spirit/bin/spirit-daemon` but did not auto-restart the
  (already-stopped) service; started it explicitly:
  `systemctl --user start spirit-daemon.service` → `active (running)`,
  new PID 499894, running the NEW `52f52g45…` binary (NOT the old `kmbmmkh52…`).

## Verification (concrete)

1. **Store opens as v11.** The v11 daemon (`SPIRIT_SCHEMA_VERSION=11`) started
   cleanly on the store; a v11 daemon rejects a v10 store, so a clean start is
   itself proof. Migrator: live `(Migrated (21 932))` → idempotent
   `(Current (21 0))`.
2. **Migration marker source_schema_version = 10.** Concrete chain: the
   pre-migration store was served by the deployed 0.20.0 daemon whose startup
   logged `(Current (22 0))` at its `SPIRIT_SCHEMA_VERSION=10` guard → the store
   was v10. The 0.21.0 migrator's only `(Migrated …)`-from-v10 path writes the
   Migration marker with `source_schema_version = 10` (proven by the green
   golden test `migrates_version_ten_strict_positional_technology_domains` and
   by the prior rehearsal's `Store::open` showing
   `SourceSchemaVersion(10)` on this same main store).
3. **Strict-positional domains served live.** `spirit-render` against the live
   daemon socket (header `generator-version: 0.21.0`) returned records rendering
   in nested strict-positional form, e.g. record `qvb3` (referent `codec`):
   `(Technology (Software (Engineering Architecture)))`, and `qjrf`:
   `[(Information Classification) (Governance Policy)]`. The active (main) store
   is GC'd to 21 records that are non-Technology or leaf-bearing; the older
   `None`-payload Technology-leaf records (`j6r4`=`(Software Data)`,
   `0a9p`=`(Software Operations)`, `kasm`=`(Software Data)`) are in the migrated
   1493-record archive. The `None → All` transformation
   (bare `(Software Data)` → `(Software (Data All))`) is proven by the green
   golden test and the successful archive migration (backup `-4`, size change,
   idempotent no-op). No live active record renders a bare Technology leaf.
4. **Deploy + daemon healthy.** lojix records the new generation:
   `(37 37 goldragon ouranos HomeOnly Switch Current /nix/store/28qcd541…-home-manager-generation)`
   — matching the live home-manager profile `835-link`. spirit-daemon
   `active (running)`, PID 499894, entered 16:42:23.

## Backup / rollback

- Backup CONFIRMED: two independent sets on the live host —
  - explicit `spirit.sema.predeploy-v11-20260702T164051` (+ archive), and
  - migrator `spirit.schema-old-backup-12.sema` / `spirit.archive.schema-old-backup-4.sema`
    (the retained v10 originals).
- Rollback NOT needed (verification green).
- Rollback path if ever needed: `systemctl --user stop spirit-daemon.service` →
  restore `spirit.schema-old-backup-12.sema` (and archive `-4`) over the live
  paths → repoint CriomOS-home spirit input back to `4c9065d…` (0.20.0) and
  re-activate that rev; the current live 0.20.0 rollback closure is
  `/nix/store/9hm08wmgd5lz7hy7zjccxz8msyixnqpc-home-manager-generation`
  (generation 36).

## Notes / concurrency

- A concurrent Listener workstream deployed generation 36 (closure
  `9hm08wm…`, CriomOS-home `406417507d6b` "wire Listener cancel shortcut") during
  this session; my rev R is a child of that exact commit, so gen 37 is a
  superset (Listener + spirit repoint), no divergence. Generation 36 did not
  touch spirit (daemon PID was unchanged). No Niri reload was needed — gen 37's
  compositor config is identical to the already-live gen 36 (only `flake.lock`
  spirit differs).
- CriomOS-home was claimed (`operating-system-implementer` lane) for the
  flake.lock edit and released after the deploy.

## Changed files / commits

- `CriomOS-home/flake.lock` — spirit input `4c9065d… → 05269499a928` and its
  transitive stack. Committed + pushed:
  `origin/main = c5a031218a8d388b40a9c62d963b85438dbb6c65`.
