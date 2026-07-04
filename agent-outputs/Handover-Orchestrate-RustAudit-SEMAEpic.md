# Handover — Orchestrate Rust audit and SEMA store-compatibility epic

## Focus
Fresh context should continue only these follow-ups:
- Rust audit of the new Orchestrate runtime path/default/config-writer behavior.
- Create or prepare the systemic epic for SEMA/redb store compatibility policy across components.

## Settled intent and constraints
- Orchestrate runtime state and socket files do not belong in the repo/workspace.
- Orchestrate local state is disposable; starting from a fresh database was explicitly approved.
- Future Orchestrate runtime paths should be XDG-style non-repo paths: state/config under `~/.local/state/orchestrate`, sockets under `$XDG_RUNTIME_DIR/orchestrate`.
- Public Spirit record `10pz` is relevant to the systemic design: replace broken older shapes deliberately rather than preserving legacy compatibility paths when legacy manufactures bad shape.

## Completed Orchestrate recovery
- Orchestrate recovery is complete and audited pass for the Nix/OS surface.
- Pushed commits:
  - `LiGoldragon/orchestrate`: `62a7682e578863d372fc2b655331029a550a1cdc`
  - `LiGoldragon/CriomOS-home`: `3356ff07346b5bc010269cb76bdc777c29fb73cb`
- Changed Orchestrate files reported by the recovery worker:
  - `Cargo.toml`
  - `src/bin/orchestrate.rs`
  - `src/bin/meta_orchestrate.rs`
  - `src/bin/orchestrate_write_configuration.rs`
- Changed CriomOS-home files reported by the recovery worker:
  - `flake.nix`
  - `flake.lock`
  - `modules/home/profiles/min/orchestrate.nix`
- Current runtime paths reported and audited:
  - state/config: `~/.local/state/orchestrate/orchestrate.sema`
  - signal/config: `~/.local/state/orchestrate/orchestrate-daemon.signal`
  - sockets: `$XDG_RUNTIME_DIR/orchestrate/orchestrate.sock`, `orchestrate-owner.sock`, `orchestrate-upgrade.sock`
- Stale repo-local runtime files were quarantined under `~/.local/state/orchestrate/repo-local-quarantine-20260704133654`.

## Verification already reported
- Recovery worker reported:
  - `nix build .#checks.x86_64-linux.test-daemon-cli --no-link --print-build-logs` passed.
  - `nix build .#packages.x86_64-linux.default --no-link --print-build-logs` passed.
  - Home activation completed directly.
  - `systemctl --user is-active orchestrate-daemon.service` returned `active`.
  - `orchestrate "(Observe Lanes)"` returned `(LanesObserved [])`.
  - No `.sock`, `.signal`, `.redb*`, `.log`, or `.lock` files remained under `/home/li/primary/orchestrate`.
- Nix auditor confirmed:
  - `orchestrate` repo at `62a7682e578863d372fc2b655331029a550a1cdc` and clean.
  - `CriomOS-home` repo at `3356ff07346b5bc010269cb76bdc777c29fb73cb` and clean.
  - Current materialized unit has `RuntimeDirectory=orchestrate`, `RuntimeDirectoryMode=0700`, `ExecStartPre=orchestrate-write-configuration ... %t/orchestrate/...`, and `ExecStart=orchestrate-daemon ~/.local/state/orchestrate/orchestrate-daemon.signal`.
  - Sockets listen only under `$XDG_RUNTIME_DIR/orchestrate`.
  - Daemon has state fd under `~/.local/state/orchestrate/orchestrate.sema`.
  - Repo-local runtime check found no `.sock`, `.signal`, `.redb*`, `.log`, `.lock`, or `.sema` recreated.

## Rust audit focus
The Nix/OS audit passed but explicitly did not perform a deep Rust audit of the new CLI/default-path code or binary configuration writer.

Audit the Rust behavior around:
- CLI defaults for runtime state and socket paths.
- `orchestrate-write-configuration` output shape and error behavior.
- `orchestrate` and `meta_orchestrate` socket/path handling.
- Whether default behavior can recreate repo-local state when run from `/home/li/primary` or a repo checkout.
- Whether path normalization, XDG fallback behavior, and diagnostic errors are safe and clear.
- Codec/error-path behavior around daemon configuration and signal files.

Relevant source files begin in `LiGoldragon/orchestrate`:
- `src/bin/orchestrate.rs`
- `src/bin/meta_orchestrate.rs`
- `src/bin/orchestrate_write_configuration.rs`
- any shared library/config modules those binaries call.

## Systemic SEMA/redb root-cause design already returned
Root-cause worker conclusion:
- High confidence for Orchestrate and mirror, medium for lojix as the same class.
- The pattern is missing storage-evolution policy across SEMA/redb-backed daemons.
- SEMA/redb rejects stores whose on-disk schema/table family no longer matches the running binary, but components generally lack an explicit next step: migration, deliberate reset/quarantine for disposable state, or durable rebuild path for durable state.
- Path/version mixing amplified the failures: repo-local Orchestrate state, mirror `/var/lib/mirror/mirror.sema`, lojix CLI/daemon contract skew, and in-place service restart during deploy.
- Wire/protocol mismatch and unsupervised activation are secondary amplifiers, not the primary redb cause.

## Component evidence to preserve
Orchestrate:
- `LiGoldragon/orchestrate/src/tables.rs` hard-bumped `ORCHESTRATE_SCHEMA_VERSION` to `3` and comments that live store migration needs a sema-upgrade migration and should not migrate the live store from a prototype branch.
- Prior failure was on-disk v2 while binary expected v3.
- Old log showed redb table type mismatch for `roles`, consistent with older sema-engine keyed-table representation meeting current table representation.
- Conclusion: disposable coordination state was treated as durable without a reset policy.

Mirror:
- `agent-outputs/LojixDeployAuthMap/Scout-H945-NoPermissionDiagnosis.md` records live `mirror.service` failure: `store-heads` registered as old `HeadFamily@52af…`, current binary declares `HeadFamily@df02…`.
- `LiGoldragon/mirror/src/store.rs` opens `SchemaVersion::new(1)` and registers generated `RecordFamily` descriptors, but has no migration/reset path.
- `LiGoldragon/mirror/ARCHITECTURE.md` states mirror state loss is unacceptable and schema changes need strict hard migration.
- Conclusion: mirror needs migration/rebuild, not blind reset.

Lojix:
- `LiGoldragon/lojix/src/lib.rs` hard-codes `LOJIX_SCHEMA_VERSION = 1`, persistent live generation tables, and comments that future bumps are deliberate hard migration.
- `agent-outputs/LojixDeployAuthMap/Deploy-H945-LandingEvidence.md` records 0.3.10 to 0.4.1 in-place restart before the old daemon committed the activation record; new daemon came up with marker `(0 0)`.
- Same evidence notes contract vocabulary changed and old CLI/profile skew remained.
- Conclusion: lojix incident is mostly upgrade/handover and wire-version skew, not proven redb schema mismatch.

## Proposed systemic epic shape
Candidate epic name: `SEMA store compatibility policy across components`.

Candidate scope:
- Add typed open-failure classification in `sema-engine` or a companion crate for schema-version mismatch, engine layout mismatch, family/hash mismatch, redb table key/value signature mismatch, and rkyv format mismatch.
- Require each component to declare a store-open policy:
  - `DisposableReset`: atomically quarantine old store and create fresh.
  - `DurableMigrate`: run named migration only.
  - `DurableRebuildFromLog`: rebuild materialized tables from versioned log/checkpoint.
  - `FailClosed`: stop with explicit diagnostic and bounded restart behavior.
- Never silently retro-stamp or read old bytes as new types.
- Prefer generated schema family hashes over ad hoc labels.
- Component policies:
  - Orchestrate: `DisposableReset`, seed roles from workspace/config, claims void after outage.
  - Mirror: `DurableMigrate` or `DurableRebuildFromLog`; keep disabled until migration is implemented and tested; do not discard `/var/lib/mirror/mirror.sema` by default.
  - Lojix: `DurableMigrate` plus upgrade handover/version handshake and reconcile/import for already-running system generation.
- Tests/checks:
  - old-store fixtures for schema mismatch, family-hash mismatch, and redb key-type mismatch.
  - Orchestrate test: old store quarantines and daemon starts.
  - Mirror test: old `HeadFamily` fixture migrates/rebuilds without losing entries.
  - Lojix VM test: self-upgrade while deploy is active still yields a queryable generation.
  - Nix checks: generated daemon config matches pinned writer schema; CLI/daemon contract versions align.

## Immediate follow-up questions
- Whether to create the systemic epic now in the active tracker, or first have a tracker-weaver inspect existing beads to avoid duplicates.
- Whether the Rust audit should include implementation of small fixes if defects are found, or report-only.
- Whether mirror’s old ledger can be rebuilt entirely from versioned entries on the live host.
- Exact desired lojix reconcile authority: automatic from `/run/current-system` or explicit owner/meta operation.

## Related open issue outside this focus
- `meta-lojix` home deploy admission failed with `CliRejected [signal frame error: frame IO error: failed to fill whole buffer]`; direct Home Manager activation was used for Orchestrate recovery. This likely belongs under lojix/deploy follow-up and may overlap the systemic epic, but it is not the Rust audit itself.

## Artifact pointers
- Recovery worker output: `/tmp/pi-subagents-1001/home-li-primary/019f2cc8-521e-78f8-93e3-c370492593a9/tasks/e376d633-884c-43f.output`
- Root-cause design worker output: `/tmp/pi-subagents-1001/home-li-primary/019f2cc8-521e-78f8-93e3-c370492593a9/tasks/7ba2f039-b81e-461.output`
- Nix/OS auditor output: `/tmp/pi-subagents-1001/home-li-primary/019f2cc8-521e-78f8-93e3-c370492593a9/tasks/d2c4e904-66e3-4ce.output`
- Prior handover: `agent-outputs/Handover-OrchestrateDaemon-Fix-and-RootCause.md`
