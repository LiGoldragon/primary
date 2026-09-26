# Horizon 0.13.0 repin train: run

Subflow of da88cf, 2026-09-25. Steps 1–3 of `reports/repin-train.md` ran, followed by the deploy-gate inspection. The producer is horizon-rs 0.13.0 `a3ddaf8685b920093a2328b85ba350a04e11477a`. `git ls-remote` showed it on horizon-rs `main` and on `tailnet-repair-da88cf`.

Nothing was deployed or restarted. The live Nexus store was only read with `cp`, and its hash was unchanged afterwards.

## Revisions

| Repo | Base (before) | main before | After (`horizon-0.13-da88cf` = main) | Version |
|---|---|---|---|---|
| signal-lojix | `f7866bf013499503d21491bcdaadaf88ea6c810c` | `ff02394` (abandoned b45d6ad line) | `cd164896311af9849e2ddf1cdbdd35b5feedcdd1` | 5.0.0 → 6.0.0 |
| meta-signal-lojix | `b500561f0ce813917366997581412b7a79aebc99` | `631d832` (abandoned line) | `c0f883c5cc428ce94ffa109fa20a5a28f7902481` | 6.0.0 → 7.0.0 |
| lojix | `lojix-store-tolerance-da88cf` = `1c9b43ac35ed36179fe544150442cc436b5c5f89` (on a67f5773, already 8.0.0) | `c4bba4f` | `f090da079f71b75a5d8c5dc45bffab6298b7d2a3` | 8.0.0 (not bumped again) |

After each push, `git ls-remote` showed `refs/heads/main` and `refs/heads/horizon-0.13-da88cf` both at the "After" revision.

- Both signal mains moved sideways, using `--allow-backwards`.
- lojix main moved forward from `c4bba4f`.
- The `lojix-store-tolerance-da88cf` bookmark still sat at `1c9b43a` when lojix was pushed.

## Changes

**signal-lojix `cd16489`**
- `Cargo.toml`: horizon-lib rev set to `a3ddaf86`, version set to 6.0.0.
- `Cargo.lock`: updated with `cargo update -p horizon-lib` only. It has one horizon-lib, at 0.13.0.
- UPGRADES: new "5.0.0 to 6.0.0" entry covering the rkyv break.
- `gold_horizon_definition` fixture extended with:
  - Router
  - `RouterInterfaces` with `country_code: MX`
  - TailnetController (CA plus TLS certificate and key references)
  - TailnetClient (SecretReference)
  - UsbDownlink (`10.47.0.1/24`)
- `cargo fmt` rewrapped some existing lines in `tests/generated_contract.rs`. The `fmt` check had already failed on that file's existing code before this change, with the same diff locally and on Prometheus.
- ethos-zero `4bf73ca` and datom-codec `09e2a9d` are unchanged. `src/generated/signal.rs` is untouched, and `build.rs` asserts it on every build.

**meta-signal-lojix `c0f883c`**
- horizon-lib `a3ddaf86` and signal-lojix `cd16489` in `Cargo.toml` and `Cargo.lock` (`cargo update -p horizon-lib -p signal-lojix`).
- Version 7.0.0, plus an UPGRADES "6.0.0 to 7.0.0" entry.
- The same fixture extension on `minimal_horizon_definition`, which the decimal-location fixture reuses.
- The same pre-existing `cargo fmt` rewrap.

**lojix `f090da0`**, stacked on `1c9b43a`
- horizon `a3ddaf86`, signal `cd16489` and meta `c0f883c` are set in:
  - the root `Cargo.toml`
  - `nexus/Cargo.toml` (signal, meta)
  - `clients/ordinary/Cargo.toml` (signal)
  - `clients/meta/Cargo.toml` (horizon, signal, meta)
  - `tools/Cargo.toml` (horizon, signal)
  - `Cargo.lock` (`cargo update -p` of the three)
  - the `flake.nix` `horizon.url`
  - the `flake.lock` `horizon` node (`nix flake update horizon`)
- `Cargo.lock` has exactly one horizon-lib (0.13.0), one signal-lojix (6.0.0) and one meta-signal-lojix (7.0.0).
- ethos-zero and datom-codec were not repinned. The lock still carries the duplicate datom-codec 0.26.3/0.31.0 and ethos-zero 8.0.1/10.0.0 entries it already had at the base.
- The lock also re-resolved three windows-sys dependency lines, from 0.61.2 to 0.52.0 (Windows-only).
- The UPGRADES "7.0.0 to 8.0.0" entry gained a "Horizon 0.13.0 repin and its wire break" section.
- `tests/horizon_layout_fixture.rs` now expects the other side of the bump, and the fixture store was not regenerated. The Horizon 0.12 `deploy-job 1` row:
  - is counted undecodable by the inspector before the open,
  - is quarantined by the first open (table `deploy-job`, key `1`, archive kept, decode error non-empty, configuration not rebuilt),
  - is not served by `deploy_jobs()`,
  - and a second open sets nothing aside.

  The test passes, so the 0.12 row does **not** decode under 0.13.0, and a v5 store holding it **starts**, with the row quarantined.

## Checks

The Nix builds ran on ouranos with `--builders @/etc/nix/machines --option max-jobs 0 --option fallback false`, one check at a time, against `git+file:///git/github.com/LiGoldragon/<repo>?rev=<after>`.

Run logs are in the scratchpad at `…/scratchpad/repin-train-run/{signal,meta,lojix}/`.

**signal-lojix `cd16489`**
- All 10 checks exit 0: fmt, test-generated-contract, test-datom-contract, test, clippy, build, doc, test-doc, no-free-functions, no-inherent-methods.
- test-datom-contract: 7 passed; test-generated-contract: 3 passed.
- Offload evidence: `building '/nix/store/62xxjnnh…-signal-lojix-test-6.0.0.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`, and the same for fmt, clippy, build, doc and the no-* checks.
- The first run, at `33c7f43`, failed only on `fmt`, because of the pre-existing formatting. That was fixed and the commit amended to `cd16489`.

**meta-signal-lojix `c0f883c`**
- The same 10 checks, all exit 0.
- test-datom-contract: 8 passed.
- Every log carries `on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` lines.

**lojix `f090da0`**
- All 14 flake checks exit 0: fmt, test, clippy, build, nexus-binary, no-free-functions, no-inherent-methods, bootstrap-rejects-flags, nexus-startup-rejects-arguments, fresh-daemon-startup, deploy-honesty, failure-evidence, retained-transient-semantics, same-host-test-activation.
- test: 145 passed and 0 failed across 18 test binaries, including `a_horizon_0_12_deploy_job_row_is_quarantined_under_the_horizon_0_13_layout ... ok`.
- Offload evidence: `building '/nix/store/1fkif3rp…-lojix-8.0.0.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`. The same-host-test-activation log has 25 such lines and the test log 15.
- `nexus-binary` and `retained-transient-semantics` built nothing new, because their outputs were already realised by the earlier checks.
- `cargo check --workspace --all-targets` was not run separately. Clippy (`--all-targets`), build and test cover it.

## Deploy gate: store inspection

- The inspector is `lojix-inspect-store` from `f090da0#offline-tools`, at `/nix/store/l5zbllf6jhaxyffbv70swc3f06ljkmz6-lojix-8.0.0`.
- At 2026-09-25T23:27-06:00, `/var/lib/lojix/lojix.sema` was copied with `cp` into the scratchpad. Its mtime is 22:45:11. Live and copy have the same sha256, `fb5de909…2b29b`.

**Finding: the inspector cannot read a hot copy.** On the raw copy, the inspector reports `Database open-failed [Database repair aborted.]`. redb marks a file that a writer holds open as needing repair, and `redb::ReadOnlyDatabase` refuses to repair. So mitigation (a) as written in the map will not work while the Nexus 7 runs.

Workaround used here, on a second copy only:
- A 12-line scratch tool (`…/repin-train-run/redb-repair`, redb =4.1.0, built with cargo on ouranos) opened the copy writable once, which repairs it to the last committed transaction, and then closed it cleanly.
- The inspector then read that copy.

Result on the repaired copy, under 8.0.0:

- `Schema matches version=5`, 11 registered tables.
- **`deploy-job` empty, row_count=0.** `test-run` and `container-lifecycle` are also empty.
- **`Quarantine quarantined_row_count=0 undecodable_row_count=0`.** No row in any family fails to decode under 8.0.0.
- `nexus-configuration` is readable, with row_count=1. **The configuration row would not be rebuilt**, so no `Configure` re-send is needed in the deploy window as of this snapshot.
- The other tables: live-set 6, gc-roots 6, event-log 111, deployment-record 32, deployment-outbox 111, pending-transition-intent 111, identifier-allocation 1. `quarantined-row` is missing, and is created on the first 8.0.0 open.

## Blockers and notes

- **The gate has to be run again at the window.** This snapshot is from 22:45. Any deploy after it can leave a deploy-job row.
- The gate needs either:
  - the Nexus stopped, so that the file is clean for `ReadOnlyDatabase`, or
  - a repaired copy, as above.

  A read-only inspector that repairs into a temporary copy would make (a) usable. That would be a lojix change and is not made here.
- Even if a 7.0.0 Horizon-mode deploy-job row does survive, it no longer crash-loops Nexus 8. It is quarantined. The Nexus-self-deploy row would still be lost as an in-flight job, so hazard (b), never self-ActivateNow the Nexus host, still stands.
- The 8.0.0 clients and the Nexus must be deployed together with signal 6.0.0 and meta 7.0.0. A 7.0.0 client cannot talk to an 8.0.0 Nexus.
- No Orchestrate lock was refused. Locks 6987, 6988 and 6997 were taken and released.

## Sources

- `flows/da88cf/reports/repin-train.md` (map, briefs B1–B3)
- Workspaces: `/home/li/wt/github.com/LiGoldragon/{signal-lojix,meta-signal-lojix,lojix}/repin-train-da88cf`
- Check logs and results: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/repin-train-run/{signal,meta,lojix}/`, plus `offline-tools.log`, `inspect.out` (raw copy) and `inspect-repaired.out`
- `git ls-remote` of horizon-rs, signal-lojix, meta-signal-lojix and lojix after each push
