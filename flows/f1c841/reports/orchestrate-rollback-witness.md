# Orchestrate rollback witness: 0.37.0 and the live 0.35.0 on one store

Subflow of f1c841, 2026-10-03. Target: orchestrate-test main, landed as
`b8e2b971d9cb5a1a600663408bb2d283f512a9d7` (parent `4aeec4c5`). Nothing was
deployed. The live Nexus, its sockets and its store were never touched; every
run used a fresh store in the Nix build sandbox (`/build/tmp.*`).

## Answer

- Rollback (a 0.37.0 store, then 0.35.0): 0.35.0 **resumes** the store. It
  becomes ready with empty stderr, holds the Lock, refuses the Lock's path,
  numbers the next Lock 2, keeps ordinary Configure shut, and serves the meta
  socket the store names.
- Forward from the live shape (a 0.35.0 store saved with
  `meta-orchestrate.sock`, then 0.37.0): 0.37.0 resumes it, holds the Lock,
  numbers the next Lock 2, and the meta Configure through
  `meta-orchestrate.sock` answers `Configured.{ { … } True }`.
- The existing `orchestrate-old-meta-name` scenario did **not** already cover
  this. Its store is written by the release under test (0.37.0), not by 0.35.0,
  and it holds no Lock. So the reverse scenario `orchestrate-live-orchestrate`
  was added.

## Inputs

| input | release | commit |
| --- | --- | --- |
| `orchestrate` | 0.37.0 | `c7c44cb39934b0727d724a6aa03a36a2a94cacf9` (unchanged) |
| `orchestrate-previous` | 0.36.1 | `bc5cd36e81df395ed1f84e2e3e98d5a6ee90bf8c` (unchanged) |
| `orchestrate-live` | 0.35.0 | `9070cbb8717813b127e448dd5a43a2095daf7d1b` (added) |

How the live commit was found. These are three independent lines of evidence:

1. The running service (pid 1944, `orchestrate-nexus.service`, up since
   2026-09-26) executes
   `/nix/store/6ynfv0hywpwg8gpapyfh7zn0yqzdg52z-orchestrate-0.35.0/bin/orchestrate-nexus`.
2. In orchestrate history, `9070cbb8` ("Identify the store by its file, and give
   a carried one a declared way back") is the commit that sets version 0.35.0.
   The next commit, `d80a617f`, is docs-only (README, UPGRADES). After that,
   `b56f2644` is 0.36.0. CriomOS-home `flake.lock` pins orchestrate to
   `9070cbb8`.
3. The live derivation's filtered build source
   (`/nix/store/6f72ys10…-source`) is byte-identical in `Cargo.toml`,
   `Cargo.lock`, `rust-toolchain.toml` and `crates/` to the `9070cbb8` source.
   `github:LiGoldragon/orchestrate/9070cbb8…` built with orchestrate-test's
   nixpkgs produces exactly `/nix/store/6ynfv0hy…-orchestrate-0.35.0`. That is
   the live store path itself.

## Method

- A new component step, `attempt` in `lib/components/orchestrate.nix`, starts a
  Nexus and waits a bounded time on its own `orchestrate-nexus ready` line or
  on its exit. It sets `orchestrateNexusOutcome` to `ready` or
  `exited <code>` and keeps the Nexus's stderr. With this, a refusal by
  0.35.0 could have been asserted exactly rather than failing the start.
- `checks/orchestrate-rollback.nix` (the name the brief gave; the drive-order
  name would be `orchestrate-orchestrate-live`):
  1. 0.37.0 `start`.
  2. meta Configure with the default paths.
  3. Lock `Held`.
  4. TERM.
  5. 0.35.0 `attempt` on the same `XDG_RUNTIME_DIR` and `XDG_STATE_HOME`.
  6. Outcome `ready`.
  7. Using the 0.35.0 clients (old wire): Observe.Locks, overlapping Lock,
     a free Lock, ordinary Configure, and meta Configure.
- `checks/orchestrate-live-orchestrate.nix`:
  1. 0.35.0 `start`.
  2. meta Configure to `meta-orchestrate.sock`.
  3. Lock `Held`.
  4. TERM.
  5. Export `ORCHESTRATE_META_SOCKET` as the legacy path.
  6. 0.37.0 `attempt`.
  7. Outcome `ready`.
  8. Using the 0.37.0 clients: Observe.Locks, a free Lock, and meta Configure
     through `meta-orchestrate.sock`.
- Oracle. Every expected reply is built from the inputs the scenario itself
  typed (the Lock's name, flow, path and reason; the socket paths the scenario
  chose). Its shape comes from the reply grammar in the existing scenarios and
  from the 0.35.0 source's own tests (`ordinary_lock_contract.rs` PathOverlap,
  `configuration_authority.rs` MetaConfigureOccurred). None of it is computed
  through the code under test.
- Fail-once:
  - `orchestrate-rollback` failed on a wrong allocator id
    (`expected Locked.{ 3 Next … }`, got `Locked.{ 2 Next … }`).
  - It failed again on a wrong outcome (`outcome: expected exited 1`, got
    `ready`).
  - `orchestrate-live-orchestrate` failed on a wrong Lock id in
    `Observed.Locks` (`expected { 2 Held … }`, got `{ 1 Held … }`).
  - Each was corrected and then passed.
- Gate:
  - `nix flake check --no-build --option allow-import-from-derivation false`
    passed.
  - `nix flake check` passed locally, with all seven checks green: lint,
    orchestrate, orchestrate-populated-store, orchestrate-old-meta-name,
    orchestrate-previous-orchestrate, orchestrate-rollback and
    orchestrate-live-orchestrate.
  - After the push, `nix flake check --refresh github:LiGoldragon/orchestrate-test`
    at `b8e2b971` printed `all checks passed!` (exit 0).
- An attempt to probe outside the sandbox was abandoned and is not evidence.
  The scratchpad paths exceeded SUN_LEN.

## Replies witnessed (green runs; `R` = `/build/tmp.4DW487FHdv`, `S` = `/build/tmp.mxqgTLMNYJ`)

`orchestrate-rollback`:

    configure: Configured.{ { R/runtime/orchestrate-nexus/orchestrate.sock R/runtime/orchestrate-nexus/orchestrate-meta.sock } True } (exit 0)
    lock: Locked.{ 1 Held f1c841 [ R/work/held ] «under test» } (exit 0)
    Nexus under test stopped with TERM; starting the live release on its store
    orchestrate-nexus outcome: ready
    orchestrate-nexus stderr: «»
    live-locks: Observed.Locks.[ { 1 Held f1c841 [ R/work/held ] «under test» } ] (exit 0)
    live-overlap: LockRejected.PathOverlap.{ R/work/held { 1 Held f1c841 [ R/work/held ] «under test» } } (exit 0)
    live-allocator: Locked.{ 2 Next f1c841 [ R/work/free ] «free path» } (exit 0)
    live-ordinary-configure-shut: ConfigurationRefused.{ MetaConfigureOccurred } (exit 0)
    live-meta: Configured.{ { R/runtime/orchestrate-nexus/orchestrate.sock R/runtime/orchestrate-nexus/orchestrate-meta.sock } True } (exit 0)

`orchestrate-live-orchestrate`:

    live-configure-legacy: Configured.{ { S/runtime/orchestrate-nexus/orchestrate.sock S/runtime/orchestrate-nexus/meta-orchestrate.sock } True } (exit 0)
    live-lock: Locked.{ 1 Held f1c841 [ S/work/held ] «live generation» } (exit 0)
    live release stopped with TERM; starting the Nexus under test on its store
    orchestrate-nexus outcome: ready
    orchestrate-nexus stderr: «»
    resumed-locks: Observed.Locks.[ { 1 Held f1c841 [ S/work/held ] «live generation» } ] (exit 0)
    resumed-allocator: Locked.{ 2 Next f1c841 [ S/work/free ] «free path» } (exit 0)
    resumed-meta-at-legacy: Configured.{ { S/runtime/orchestrate-nexus/orchestrate.sock S/runtime/orchestrate-nexus/meta-orchestrate.sock } True } (exit 0)

## Evidence grades

- 0.35.0 resumes a 0.37.0 store (Lock, overlap, allocator, Configure shut, meta
  socket): **witnessed**, in a pure Nix check that is green locally and on the
  remote flake.
- 0.37.0 resumes a 0.35.0 store saved with `meta-orchestrate.sock`, and the
  meta Configure there answers Configured: **witnessed**, by the same gate.
- `orchestrate-live` is the live binary's build: **witnessed** as an exact
  store-path identity (`6ynfv0hy…-orchestrate-0.35.0`). The source is also
  byte-identical, and the CriomOS-home pin agrees.
- The `attempt` refusal branch (`exited <code>` plus stderr) is **built but not
  exercised by a real refusal**. Only its `ready` branch ran, together with the
  deliberately wrong `exited 1` expectation, which it correctly failed.

## Gaps

- The fixture stores are fresh and tiny: one Lock, one Configure. The live store
  was first written before 0.34.0, has been resumed by 0.35.0 since
  2026-09-26, and holds an unknown number of Locks. Neither its history nor its
  size is reproduced. A copy of the live store was not used, because the brief
  forbids touching it and the Nexus refuses a carried store.
- Rollback was tested only from a 0.37.0 store that had one Configure and one
  Lock. It was not tested from a store 0.37.0 resumed from 0.35.0 (live, then
  0.37.0, then 0.35.0). That three-step path, the real morning sequence, is
  unwitnessed.
- Releases are not exercised across generations; Release on a resumed Lock is
  not asserted in either scenario.
- Only TERM stops were exercised; a crash (SIGKILL) mid-write before rollback is
  not.
- The installed wrappers (`orchestrate`, `orchestrate-meta`, which set the
  sockets from `XDG_RUNTIME_DIR`) are not in the sandbox; the direct binaries
  were driven with explicit `ORCHESTRATE_SOCKET` / `ORCHESTRATE_META_SOCKET`.

## Sources

- orchestrate-test `b8e2b971d9cb5a1a600663408bb2d283f512a9d7`:
  `checks/orchestrate-rollback.nix`, `checks/orchestrate-live-orchestrate.nix`,
  `lib/components/orchestrate.nix` (`attempt`), `lib/default.nix`, `flake.nix`,
  `flake.lock`, `README.md`.
- Build logs: `nix log /nix/store/f9b9jiypvlk5gb1k68mr3na0xvjc2vj9-orchestrate-rollback`,
  `nix log /nix/store/0hxyxcg1jpr064sb3grr6dqnrf1qf5wf-orchestrate-live-orchestrate`.
- Live service: `systemctl --user status orchestrate-nexus` (pid 1944);
  derivation `/nix/store/8q0qwf3wv0sk20xswflhqsvjb8bj2ij7-orchestrate-0.35.0.drv`,
  nexus derivation `f88xawg6…-orchestrate-nexus-0.35.0.drv` with src
  `6f72ys10…-source`.
- orchestrate history: `9070cbb8` (0.35.0), `d80a617f` (docs), `b56f2644` (0.36.0),
  `bc5cd36e` (0.36.1), `c7c44cb3` (0.37.0); CriomOS-home `flake.lock` node
  `orchestrate`.
- 0.35.0 source tests: `crates/orchestrate-nexus/tests/ordinary_lock_contract.rs`,
  `configuration_authority.rs`, `live_nexus.rs`.
