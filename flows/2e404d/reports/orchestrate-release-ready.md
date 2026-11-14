# Orchestrate on ethos-zero 28, with Fable's 5q8i rulings: ready for release

Everything is on branches named `ethos27-2e404d`, pushed, and each is a fast-forward of its main. Nothing was merged or deployed. No running service was touched, and I did not ssh to zeus. The evidence is in `/home/li/primary/flows/2e404d/orchestrate/release-ready/`.

## Heads, gates, fast-forward

Each gate ran `nix run github:Mic92/nix-fast-build -- --remote prometheus --no-nom --no-download --eval-workers 1 --flake 'git+file://<worktree>?rev=<commit>#checks.x86_64-linux'` on the committed head. Logs are in `release-ready/gates/<worktree>-<commit>.log`.

| repository | head (pushed) | main | fast-forward | gate |
|---|---|---|---|---|
| signal-orchestrate | `bf21c0c` (6.0.0) | `df564c6` | yes, 2 ahead | exit 0, 13 checks |
| meta-signal-orchestrate | `fff088f` (6.0.0) | `5e4986d` | yes, 2 ahead | exit 0, 13 checks |
| memory-engine | `ef24197` (0.20.0) | `27f256c` | yes, 2 ahead | exit 0, 10 checks |
| orchestrate | `9e65b55` (0.39.0) | `0f99614` | yes, 5 ahead | exit 0, 18 checks |
| orchestrate-test | `eadcd22` | `b8e2b97` | yes, 5 ahead | exit 0, 11 checks |
| nexus | `64a735d` (untouched) | `c495f2a` | yes, 1 ahead | earlier gate stands: exit 0, 3 checks |

- **ethos-zero:** every Orchestrate repository pins `970459d`, which is ethos-zero main (28.0.0).
- **`Problem::Payload`:** no Orchestrate repository matches on it, so nothing needed replacing.
- **build-base is untouched.** None of these repositories uses crate2nix; all build with crane. No Cargo.nix exists to regenerate, and no crate edge forced a build-base change.
- **The contract versions stay where they were.** Both contracts are still 6.0.0 and orchestrate is still 0.39.0, because none of them has reached main. Each UPGRADES entry is rewritten to describe the full change.

## What changed

1. **ethos-zero 28.** All three generated files were regenerated: both contracts, orchestrate's `memory.ethos`, and both client modules. The client modules came out byte-identical.
2. **Ruling 1: the held Lock is `Lock` again.** It sits beside the input `Lock.LockRequest`. `LockOverlap.held_lock` is `lock`, and `StoredLock.held_lock` is `lock`.
3. **`ConfigurationAccepted` is renamed `Configured`** in signal-orchestrate 6.0.0.
4. **Ruling 3: a store failure is an answer in the contract.**
   - Both contracts declare `Refused.Refusal` with `Refusal.[ Store.String ]`, placed after every other output, so no earlier archived tag moves. The meta contract imports the ordinary contract's `Refusal`.
   - `Answerer` runs each transition and maps a `StoreError` to `Refused.Store.«<error text>»`. `Unsent` is gone, and so is the failure the Answerer used to hold.
   - The core's replies are `Result<Output, Infallible>`, so they cannot fail.
   - An `Observe` whose opening state cannot be read is answered `Refused.Store`.
   - New in this change: if the state after a Lock or Release cannot be read back, the core announces `Unkept`, and every subscription ends `Lagged`. Before, that error closed the connection of whoever made the change, and subscribers got no update.
   - Tests:
     - `a_request_the_store_refuses_is_answered_refused_store` (ordinary_lock_contract).
     - `a_nul_lock_path_never_becomes_durable` (live_nexus), which now expects `Refused.Store` where it used to expect a dropped connection.
5. **Ruling 7: ethos-zero 28 accepts the head form.** `StoredMetadata.{ Configuration.ConfigurationState<OrchestrateNexusConfiguration> }` generates `pub struct Configuration(pub nexus::ConfigurationState<…>)` and the named field `configuration: Configuration`.
   - A head over one type declares a newtype, so the code reads it as `stored.configuration.0`.
   - The bytes are unchanged: `the_metadata_tree_archives_as_the_0_38_metadata_record` passes.
6. **The zeus-store answers, applied.**
   - **Upgrade line on every outcome.** The Nexus now prints `orchestrate-nexus upgraded <path> from the sema format to the memory format` whether or not the open then succeeds.
   - **memory-engine `ef24197`.** An open that converts the file and is then refused answers `Error::RefusedAfterSemaConversion { conversion, refusal }`, which `Error::sema_conversion()` reads. This covers the kernel's version guard and every later check. Two tests were added.
   - **orchestrate.** An `OrchestrateStore::open` refusal after the engine has converted the file carries the conversion as `StoreError::RefusedAfterSemaConversion`; `CarriedStore` is one such refusal. `main` prints the line from either the store or the refusal.
   - **No copy kept.** The engine keeps no copy of the converted file; ARCHITECTURE and UPGRADES now say the release keeps the rollback copy.
   - **New scenario.** orchestrate-test adds `orchestrate-sema-carried`:
     1. 0.37.0 writes a store, which is then copied to the memory name as a second file.
     2. The first open prints the upgrade line and is refused as carried.
     3. The second open prints nothing and is refused the same way.
     4. After `orchestrate-relocate`, the Lock 0.37.0 wrote is served.

## Proofs

### Before and after, against the live 0.38.0

`release-ready/proof/contract/`, script `contract.sh`.

**Setup.**
- Store: one read-only snapshot of the live store, sha256 `b2c383fa…`.
- Each run: a fresh copy in a bwrap namespace at the live store's path, with a scratch socket directory.
- Binaries: the live service's own 0.38.0 (`zlyxh0bq…`) and the branch package (`6zwm1a6y…`).

| run | result |
|---|---|
| A (live) and B (branch), the same 11 inputs as the 0.39.0 proof | identical except for one reply, `ConfigurationAccepted.{ … }` → `Configured.{ … }`. The binary path and the copy's inode also differ |
| C: 0.38.0 on the store B served; D: branch on the store A served | Observe matches the snapshot's first Observe (md5 `b5b7f7f4`) in A, B, C and D |
| E: branch Nexus with 0.38.0 clients | ordinary refused `ContractMismatch.5340723165906021863`, meta refused `ContractMismatch.-5802613112951910567` |
| F: 0.38.0 Nexus with branch clients | ordinary refused `ContractMismatch.8912638139974146909`, meta refused `ContractMismatch.-8743676413678169448` |
| G: `Lock` with path `relative/path` | 0.38.0: the connection drops, and the client prints `Unreachable.{ … «Signal frame: Signal frame I/O failed: failed to fill whole buffer» }` with exit 1. Branch: `Refused.Store.«lock path "relative/path" is not absolute»` with exit 0. In both, the following Observe still answers |

### Upgrade on open of both old-format stores

`release-ready/proof/upgrade/`, script `upgrade.sh`, the earlier `prove.sh` pointed at the same snapshot.

**The stores.**
- The zeus copy: `zeus-store/zeus-orchestrate-nexus.memory`, sha256 `46a99052…`.
- The ouranos older store: `orchestrate-nexus.memory.pre-memory`, sha256 `c67fb557…`.

**Results.**
- **The bytes as found, at the memory name (zeus and ouranos).**
  - The first open converts every table from `__sema_*` to `__memory_*` with the same row counts.
  - It now prints the upgrade line, and then exits 1 with `CarriedStore`. That line was missing in the earlier proof.
  - After `orchestrate-relocate`, the Nexus serves the store: Lock 1 on zeus, Lock 26134 on ouranos.
  - A reopen prints nothing extra.
- **The writer's reading compared with the branch.** Observe md5 is `c0432094` (zeus, 0 Locks) and `6b2bfed1` (ouranos, 148 Locks), the same for:
  - 0.37.0 as writer;
  - the branch's first open, which prints the upgrade line;
  - the branch's reopen, which prints nothing;
  - 0.38.0 afterwards (`05-live-0.38.0-after.txt`), so rollback stays open.
  These hashes match the earlier proof's.
- **The live store, already in the memory format.** 0.38.0 and the branch produce identical transcripts apart from the binary path, and neither prints an upgrade line.

## Kept as briefed

- **CLI text:** the CLIs accept the same text as before. The only reply that differs for the same input is `Configured`.
- **Store bytes:** unchanged for the new-format store. All five representation tests pass, and runs C and D show both directions.
- **Meta contract, changed by ruling 3.** A meta input whose commit fails needs an output, so `Refused.Store` was added. The meta digest therefore moves, and 0.38.0 and 0.39.0 meta clients no longer work with each other's Nexus (run E/F, and orchestrate-test's `orchestrate-previous-orchestrate`). Deploy the clients together with the Nexus.

## Open

1. **Lock paths the store rejects.** A relative, NUL, empty, parent-component or duplicate path now gets `Refused.Store.«…»` instead of a dropped connection. These are faults in the request, so Fable may want them under `LockRejection` instead of under Store.
2. **The relocate and preflight tools stay silent.** `orchestrate-relocate` and `orchestrate-upgrade-preflight` still upgrade a sema store through the same open without printing anything. Only the Nexus prints the line.
3. **Behaviour I added without a ruling.** `Announcement::Unkept`, which ends subscriptions `Lagged`, is my choice and has not been ruled on.
4. **A new public error variant in memory-engine.** `memory_engine::Error` gains `RefusedAfterSemaConversion`. 0.20.0 has not been released, and UPGRADES names the variant for consumers that match on errors.
5. **orchestrate-test evaluates only on prometheus.** Local evaluation fails: the 0.37.0 input's `sema` rev `51d7927c` is no longer on sema's main. The gate evaluates on prometheus, where the source is cached.
6. **ethos-zero 19.2 is still in the graph,** through `signal` `7afb68b`'s build-dependency.
7. **zeus at deploy.** The first login after the deploy runs the upgrade, so the release step must set the sema file aside first.

## Final fixes

Two last changes before the release, so the contract changes only once. Everything is on `ethos27-2e404d`, pushed, and each branch fast-forwards its main. Nothing was merged or deployed, and I did not ssh to zeus. The evidence is in `/home/li/primary/flows/2e404d/orchestrate/release-ready/final-fixes/`.

### Heads, gates, fast-forward

Each gate ran `nix run github:Mic92/nix-fast-build -- --remote prometheus --no-nom --no-download --eval-workers 1 --flake 'git+file://<worktree>?rev=<commit>#checks.x86_64-linux'` on the committed head. Logs are in `final-fixes/gates/`. The first gate, on the heads before the last commit in each repository, is kept in `gates/superseded/`: the envelope test still carried the old digest, and clippy refused the large error type.

| repository | head (pushed) | main | fast-forward | gate |
|---|---|---|---|---|
| signal-orchestrate | `e4fda9b` (6.0.0) | `df564c6` | yes, 4 ahead | exit 0, 13 checks |
| meta-signal-orchestrate | `27ac19c` (6.0.0) | `5e4986d` | yes, 4 ahead | exit 0, 13 checks |
| orchestrate | `ef4fe80` (0.39.0) | `0f99614` | yes, 7 ahead | exit 0, 18 checks |
| orchestrate-test | `cc2b197` | `b8e2b97` | yes, 7 ahead | exit 0, 12 checks |
| memory-engine | `ef24197` (untouched) | `27f256c` | yes, 2 ahead | earlier gate stands |
| nexus | `64a735d` (untouched) | `c495f2a` | yes, 1 ahead | earlier gate stands |

### 1. A bad Lock path is a Lock rejection

- **Contract.** `LockRejection` in signal-orchestrate gains five variants, placed after `DuplicateName` and `PathOverlap` so their archived tags stay the same:
  - `NoPath`
  - `RelativePath.LockPath`
  - `ParentComponent.LockPath`
  - `NulCharacter.LockPath`
  - `DuplicatePath.LockPath` (the normalized path that appears twice)

  Each path fault carries the path at fault. Datom text, for example: `LockRejected.RelativePath.relative/path`.
- **Digest.** The ordinary digest is now `-3784715512862853597`. The meta file imports nothing that changed, so its generated module and digest (`-5802613112951910567`) stay the same.
- **Nexus.** Lock path normalization returns `LockRejection`, and the Lock transition answers it as `LockRejected`. Five `StoreError` variants are gone (`RelativePath`, `EmptyPathSet`, `ParentPathComponent`, `NulPath`, `DuplicateNormalizedPath`). `Refused.Store` is now left to a store that fails.
- **Tests.**
  - signal-orchestrate: `a_path_fault_is_a_lock_rejection_of_the_contract` (wire round trip) and `a_path_fault_is_written_by_its_name` (Datom text).
  - orchestrate, one per fault through the core:
    - `a_lock_naming_no_path_is_rejected_no_path`
    - `a_relative_lock_path_is_rejected_relative_path`
    - `a_lock_path_with_a_parent_component_is_rejected_parent_component`
    - `a_lock_path_with_nul_is_rejected_nul_character`
    - `a_lock_path_repeated_once_normalized_is_rejected_duplicate_path`
  - Each of those checks that the core then still takes a sound Lock.
  - `a_nul_lock_path_never_becomes_durable` (live Nexus) now expects `LockRejected.NulCharacter`.
  - `a_request_the_store_refuses_is_answered_refused_store` now uses a real store failure: an allocator at `i64::MAX`, answered `Refused.Store.«the durable Lock ID allocator is exhausted»`.
  - orchestrate-test's `orchestrate` scenario sends through the client each fault a client can write (`NoPath`, `RelativePath`, `ParentComponent`, `DuplicatePath`) and expects every reply whole.
- **Clippy.** `LockRejection` is large because `DuplicateName` carries a whole Lock. The two normalization signatures therefore allow `clippy::result_large_err`, as `Answerer::attempt` already does.

### 2. The relocate and preflight tools print the upgrade line

- **One place makes the line.** `UpgradeLine` (in `orchestrate_nexus::store`) is its only source. `ReportsUpgrade::upgrade_line(path)` yields it for any opened value or refusal that carries a sema conversion, and for a `Result` of the two.
- **The Nexus, `orchestrate-relocate` and `orchestrate-upgrade-preflight`** each print `orchestrate-nexus upgraded <path> from the sema format to the memory format` when their open upgraded the store, whether or not they then succeed.
  - `StoreRelocation` and `LegacyStorePreflight` carry the conversion.
  - `RecoveryError` gains `RefusedAfterSemaConversion`, as `StoreError` has, so a refusal after the upgrade still reports it.
- **Test.** New orchestrate-test scenario `orchestrate-sema-tools`:
  1. 0.37.0 writes a store, and those bytes are copied to the memory name.
  2. The preflight prints the line and the count. A second preflight prints the count alone.
  3. On a fresh copy, `orchestrate-relocate` prints the line and declares the move.
  4. The Nexus then serves the Lock without printing an upgrade line of its own.

### Proofs

**Before and after, against the live 0.38.0.** `final-fixes/proof/contract/`, using the same `contract.sh`, the same snapshot (sha256 `b2c383fa…`), the live `zlyxh0bq…` 0.38.0 and the branch `75m14mfl…`.

| run | result |
|---|---|
| A (live) and B (branch), the same 11 inputs | identical except for one reply, `ConfigurationAccepted` → `Configured`. The binary path and the copy's inode also differ |
| C and D | Observe md5 `b5b7f7f4` in A, B, C and D, as before |
| E: branch Nexus with 0.38.0 clients | ordinary refused `ContractMismatch.-3784715512862853597` (the new digest), meta refused `-5802613112951910567` |
| F: 0.38.0 Nexus with branch clients | the same as before: `8912638139974146909` and `-8743676413678169448` |
| G: `Lock` with path `relative/path` | 0.38.0: the connection drops, `Unreachable.{ … failed to fill whole buffer }`, exit 1. Branch: `LockRejected.RelativePath.relative/path`, exit 0. In both, the next Observe answers |

**Upgrade on open of both old-format stores.** `final-fixes/proof/upgrade/`, `upgrade.sh`. This is the earlier script with one added line, run on the same zeus copy (`46a99052…`) and ouranos older store (`c67fb557…`).
- **Every earlier line is unchanged.** Every transcript matches the earlier proof's apart from store paths, inodes and an inspector thread id:
  - as found;
  - from the writer, with Observe `c0432094` (zeus) and `6b2bfed1` (ouranos) for 0.37.0, the branch's first open, the reopen, and 0.38.0 afterwards;
  - the live memory-format store.
- **The tools as first opener (new).** On each store, on fresh copies at the memory name:
  - `orchestrate-upgrade-preflight` prints the upgrade line, then `active legacy PathLock rows: 0`. A second run prints only the count.
  - `orchestrate-relocate` as first opener prints the upgrade line, then `declared: …`.
  - In both cases the Nexus then serves the store without printing an upgrade line: 0 Locks on zeus, the ouranos Locks on ouranos.

### Standing

- **Lagged subscriptions.** A change whose state the core cannot read back still announces `Unkept`, and every subscription ends `Lagged`. This is left as it is, as briefed, and has not been ruled on.
- **Earlier open items unchanged:** 4 (the memory-engine error variant), 5 (orchestrate-test evaluates only on prometheus), 6 (ethos-zero 19.2 is still in the graph) and 7 (at zeus deploy, set the sema file aside first).
