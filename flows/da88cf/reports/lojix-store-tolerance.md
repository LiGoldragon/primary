# Lojix store tolerance: rows that no longer decode are quarantined

A subflow of da88cf did this on 2026-09-25. It worked in the jj workspace `~/wt/github.com/LiGoldragon/lojix/store-tolerance-da88cf`, created from a67f5773 in the canonical lojix repo, under Orchestrate lock 6966, which covered that workspace path only. The canonical checkout stays under the integrator's lock 6832.

## Revision

- Bookmark `lojix-store-tolerance-da88cf` = `1c9b43ac35ed36179fe544150442cc436b5c5f89`, one commit on a67f5773. `git ls-remote origin refs/heads/lojix-store-tolerance-da88cf` printed that revision. Main was not touched.
- lojix main (`c4bba4fa`) is behind a67f5773. a67f5773 sits on the 00f95a bookmark `lojix-horizon-datom31-00f95a`, and the integrator lands it on main.
- **Version:** all five packages are at **8.0.0** in this commit. The repo's convention is one bump per release with one UPGRADES entry, so this commit opens `# 7.0.0 to 8.0.0`. The repin commit extends that entry and does not bump again.

## What changed

- **`src/quarantine.rs` (new).**
  - When the store opens, every row of all 11 families is read by itself as raw redb bytes. This goes through the engine's read-only `storage_reader()`, the same exception Flow 0.12.1 took, and it is noted at the site.
  - A row that decodes stays where it is.
  - Any other row is moved into the new `quarantined-row` family (`QuarantinedRowFamily`, hash `[13;32]`) as `QuarantinedRow { table, key, quarantine_number, archive, decode_error }`. The move and the row's retraction are one atomic commit. The retraction goes through a zero-size `UnreadRow` view of the same table.
  - This is the quarantine half only. No earlier layout is carried forward.
- **The quarantine runs before anything reads a family whole.** In `open_unchecked` it comes first, before `ensure_nexus_configuration` and before the identifier allocation and startup validation steps. Undecodable rows therefore no longer produce `StoreStartupCompatibility`.
- **Logging.** The real open logs one line per row on stderr: `lojix-nexus: RowQuarantined.{ <table> <key> «<decode error>» }`. The disposable startup probe logs nothing. `Store::opening()` (trait `OpenedStore`) records what that open did.
- **Configuration row: my decision.** It is rebuilt, but not from the archive. The Nexus reads no startup archive: the `lojix-write-configuration` archive is written and read only by the `lojix-reset-store` unit (CriomOS `modules/nixos/lojix.nix`). The one source the Nexus has is its built-in configuration, the same value a fresh store is seeded with and the one CriomOS restates.
  - When a quarantined `nexus-configuration` row exists and the table is empty, the Nexus reseeds the row from that built-in configuration and logs `NexusConfigurationRebuilt.{ nexus-configuration BuiltIn }`.
  - Because the check reads the persisted quarantine, a crash between the move and the reseed is completed at the next open.
  - A layer added by an ordinary or meta `Configure` is lost with the row. Its bytes stay in quarantine, and ordinary Configure is open again.
- **`lojix-inspect-store`.**
  - It now covers all 11 families plus `quarantined-row`.
  - A family with undecodable rows reports `decode-failed undecodable_row_count=<n> row_count=<m> [first error]`.
  - The report ends with `Quarantine quarantined_row_count=<n> undecodable_row_count=<m>`: the rows already set aside and the rows the next open will set aside.
- **Also updated:** the reconstruction catalog's recognised families (so a reset still recognises the store), ARCHITECTURE §4, and UPGRADES.

## Tests

- **`tests/store_startup_gate.rs`.**
  - The old refusal test became `a_malformed_live_set_row_is_quarantined_not_refused`.
  - New: `undecodable_deploy_job_and_configuration_rows_are_quarantined_and_the_store_serves`. The store holds one live generation, plus `deploy-job 19` and `nexus-configuration desired` overwritten with undecodable bytes. The inspector counts 2 undecodable rows before the open. The open quarantines exactly those two, keeping the original bytes. The configuration equals `built_in()`, `deploy_jobs()` is empty, and the live-generation query answers 1. A reopen sets nothing aside, and the inspector then reports `quarantined_row_count=2 undecodable_row_count=0`.
  - Also new: a second quarantine under the same key is numbered 2 and kept beside the first, and the log line has the exact form above.
- **`nexus/tests/daemon_configuration.rs`: `nexus_over_undecodable_rows_quarantines_them_and_answers_a_query`.** This runs the real `lojix-nexus` binary over such a store.
  - It announces readiness on the built-in sockets, which shows the rebuilt configuration is in use.
  - It answers an ordinary `Query` with `Queried`.
  - Its stderr holds each of the three lines exactly once.
- **`tests/horizon_layout_fixture.rs` and `tests/fixtures/lojix-v5-horizon-0.12-deploy-job.sema`.** The fixture is a v5 store written once at horizon `ee8d6f8`. It holds an admitted, in-flight Horizon-mode `Deploy.Host` row under key `1`. At this commit the row reads and nothing is quarantined.
- **Local runs (ouranos):** before committing I ran the targeted suites locally to iterate: `store_startup_gate` 5/5, `store_inspection` 5/5, `lojix-nexus` 4/4, `horizon_layout_fixture` 1/1. `cargo clippy --workspace --all-targets` gave 0 warnings, and `cargo fmt --check` and both law scripts were clean.
- **Full suite:** it ran only through the offloaded flake checks below.

## Offload evidence

OFFLOAD_RESULT_PLACEHOLDER

## What the train's repin commit must still do

- **Flip the fixture test.** Change `tests/horizon_layout_fixture.rs` to the other side of the bump: the same fixture store opens, `opening().quarantined_rows` is exactly `deploy-job 1`, and the store serves. This answers B3's "starts or is refused": it starts.
  - Check that the row fails to decode rather than decoding into garbage. rkyv bytecheck can in principle accept a layout it was not written in.
  - If it decodes, the test fails. Stop and report that; do not paper over it.
- **Do not regenerate the fixture.**
- **Extend the UPGRADES `7.0.0 to 8.0.0` entry** with the horizon, signal and meta pins and the wire break. Do not bump the version again.
- **Keep what B3 already required:** the repin itself and `Cargo.lock` holding one horizon-lib, one signal-lojix and one meta-signal-lojix.

## Operational notes for B6

- **Inspect first.** Run `lojix-inspect-store` from `<L8>` on a copy of `/var/lib/lojix/lojix.sema`. It now covers `nexus-configuration` and gives counts, so the operator knows beforehand what will be quarantined and whether the configuration row will be rebuilt.
- **The rebuilt row carries `daemon_host` `localhost`.** If the live row carried a Configured `daemon_host`, the rebuild resets it to `localhost`. The self-switch guard uses that value, so re-send `Configure` after the restart.
- **Never ActivateNow the Nexus host.** The advice stands, but a leftover row is no longer fatal.

## Sources

- lojix a67f5773: `src/lib.rs` (`validate_startup_compatibility`, `open_unchecked`, `ensure_nexus_configuration`), `src/inspection.rs`, `src/reconstruction.rs`, `src/daemon.rs` (`Daemon::from_environment`)
- sema-engine `27e814a`: `src/engine.rs` (`retract`, `StorageReader`), `src/atomic.rs`
- flow `fe709c7`: `crates/flow-nexus/src/store.rs` (`settle_launch_attempts`); `flows/38de5b/receipts/flow-0.12.1-store.md`
- CriomOS `modules/nixos/lojix.nix` (the Nexus reads no archive; the reset unit owns it)
- `flows/da88cf/reports/repin-train.md` §4 and B3
