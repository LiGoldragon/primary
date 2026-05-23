# 11 — MVP sandbox repo audit and small fixes

*Kind: Implementation audit · Topic: lean lojix/horizon MVP + sandbox readiness · 2026-05-23*

## Scope

Input frame: `reports/system-designer/34-mvp-and-sandbox-audit/0-frame-and-method.md`.

I audited the lean-stack repos that `/34` points at and fixed only small, obvious, low-risk drift. I did not touch dirty worktrees owned by other lanes.

## Reconciliation with `/34` slice reports

The system-designer slice reports `reports/system-designer/34-mvp-and-sandbox-audit/1-mvp-code-state-fresh-audit.md` through `4-cutover-to-main-deployment-requirements.md` appeared in the primary working tree while this audit was underway. I read them after my repo pass and checked their claims against local code.

Material corrections from local verification:

- `lojix` is **green but stale**, not broken as-pinned. `/34/3` says the crate is broken at the lock boundary because `signal-lojix/horizon-leaner-shape` moved to operation roots. The branch-head compatibility risk is real, but current `lojix/Cargo.lock` still pins `signal-lojix` to `df49dae1`, so the current locked tree compiles and its daemon/CLI tests pass. It will break only when the `signal-lojix` lock refresh lands unless `lojix` migrates in the same pass.
- The dual `nota-codec` pin is **not resolved** in the current `lojix` lock. `/34/1` says it is resolved, but `Cargo.lock` still contains `nota-codec` at `2618adbf` via `?branch=main` and at `97c1f496` via the unbranched Git source. This remains cleanup work.
- `/34/1` records `lojix/horizon-leaner-shape` at `be12741e`; after the small fix in this audit the branch tip is `60b93000`.

Convergences:

- `/34/2` agrees the current sandbox infrastructure is real but old-stack-oriented.
- `/34/4` agrees cutover needs separate `lojix` package outputs, a `CriomOS` NixOS module for `lojix-daemon`, and a `criomos-horizon-config` bridge.
- All reports agree that `CriomOS-lib/lib/predicates.nix` and the `CriomOS` `behavesAs` sweep are required before the horizon role-merge becomes buildable downstream.

## Small fixes landed

### `lojix`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape`

Commit pushed to `horizon-leaner-shape`: `60b93000` — `lojix: refresh lean-branch guidance`.

Changes:

- `AGENTS.md`: renamed stale `horizon-re-engineering` status to `horizon-leaner-shape`.
- `skills.md`: removed a horizontal-rule separator line forbidden by workspace markdown discipline.

Verification:

- `rg -n "horizon-re-engineering|^---$" AGENTS.md skills.md ARCHITECTURE.md README.md` returned no matches.
- `nix build --no-link .#checks.x86_64-linux.daemon-cli-integration .#checks.x86_64-linux.test-build-pipeline .#checks.x86_64-linux.test-event-log .#checks.x86_64-linux.test-socket --option warn-dirty false -L` passed.

### `CriomOS-lib`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-lib/horizon-leaner-shape`

Commit pushed to `horizon-leaner-shape`: `3143a175` — `criomos-lib: clarify transitional lan constants`.

Change:

- `lib/default.nix`: replaced a stale comment saying LAN subnet/gateway constants had moved to horizon with an honest note that transitional IPv4 LAN constants are not here yet, and the lean cutover intends CriomOS-side operational defaults to live in this shared library.

Verification:

- `nix flake show --all-systems --no-write-lock-file` passed.
- `nix eval --no-write-lock-file .#lib.constants.network.lan.lease.defaultTtlSeconds` returned `4000`.

## Repo state audit

### `lojix`

The daemon/CLI MVP is real and substantially tested.

Current branch tip after my fix: `horizon-leaner-shape` at `60b93000`.

What is present:

- One crate with `lojix-daemon` plus thin `lojix` CLI.
- Typed daemon/CLI `nota-config` configuration boundary.
- CLI-only-to-daemon invariant has tests.
- Socket runtime, streaming observations, stalled-client isolation.
- Build-only deployment actor slice.
- Criome authorization gate before Nix/SSH/rsync/GC-root effects.
- Sema-backed deployment identifiers, observations, subscriptions, and built generations.

What is still not cutover-ready:

- `Cargo.lock` still carries two `nota-codec` pins.
- `Cargo.lock` pins `signal-lojix` to `df49dae1`, behind both `signal-lojix/horizon-leaner-shape` at `a007e8b6` and the in-progress `signal-lojix` working copy at `ef98dc0a`.
- `Cargo.lock` pins `horizon-rs` to `189bfd04`, behind `horizon-rs/horizon-leaner-shape` at `7a3072c7` and far behind the role-merge design surface.
- Lojix still compiles against old `signal-lojix` public names such as `DeploymentSubmission`, `CacheRetentionRequest`, and subscription records. It has not consumed the contract-local verb split.

Conclusion: `lojix` is the strongest implementation slice today, but it is ready for MVP only after the `signal-lojix` and `horizon-rs` pins are advanced through a controlled compatibility pass.

### `CriomOS-test-cluster`

Repo: `/git/github.com/LiGoldragon/CriomOS-test-cluster`

Current `main`: `dae757ff` — `add missing super-node horizon fixture`.

Existing sandbox surface:

- `checks.*`: projection checks, invalid cluster rejection checks, full module contracts, source constraints.
- `packages.*.dune-toplevel`: synthetic system toplevel build.
- `packages.*.dune-nspawn-toplevel`: nspawn container-aware synthetic toplevel.
- `apps.*.run-on-prometheus`: remote `nix flake check` under transient `systemd-run --user` sandbox.
- `apps.*.build-dune-on-prometheus`: remote toplevel build under the same sandbox shape.
- `apps.*.nspawn-dune-on-prometheus`: remote nspawn create/start/verify/teardown through deployed `criomos-nspawn`.

Verification I ran:

- `nix build --no-link .#checks.x86_64-linux.source-constraints .#checks.x86_64-linux.projections-match-fieldlab .#packages.x86_64-linux.nspawn-dune-on-prometheus --option warn-dirty false -L` passed.

Important limitation:

- I did **not** run `nix run .#nspawn-dune-on-prometheus`. That command pushes `main`, SSHes to Prometheus, creates a transient nspawn machine, starts it, and tears it down. It is the right live witness, but should be run intentionally as a cutover gate, not casually during a small-fix audit.

Branch issue:

- This repo has `horizon-re-engineering`, not `horizon-leaner-shape`, as its feature bookmark. The name mismatch is not fatal, but it is a coordination hazard because `/34` and the active repo map use `horizon-leaner-shape`.

Lean-stack gap:

- `flake.nix` still drives `horizon-cli` with flags from `horizon-rs` and compares checked-in JSON fixtures. It proves the legacy projection path, not yet the new `lojix-daemon` path.

MVP test implication:

- The sandbox runner exists and builds. The missing MVP test is a new lean-stack smoke that starts `lojix-daemon`, submits a build-only deployment for the synthetic fixture, and then promotes that into the Prometheus nspawn witness once activation exists.

### `horizon-rs`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape`

State:

- Working copy is dirty with `ARCHITECTURE.md` and `INTENT.md` edits from another lane. I did not touch it.
- `main` has `ae8754d3` — `horizon-rs: refresh main NOTA codec consumers`.
- `horizon-leaner-shape` bookmark is at `7a3072c7` — `horizon-rs: migrate NOTA fixtures to bracket strings`.
- Working copy commit `2ade8957` describes the role-merge destination in docs.

Critical gap:

- Code is still pre-role-merge. It still has `NodeSpecies`, `NodeService`, `NodeServices`, `Contained`, view-side `behavesAs`, and old service modules. The role-merged `Role` vector, `Pod` placement, and Nix-side predicate migration are not in code yet.

Risk:

- `ARCHITECTURE.md` now describes a destination that code has not reached. That is acceptable as a target document only if operators know it is not current implementation truth. Otherwise it will mislead the next implementation pass.

### `signal-lojix`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape`

State:

- Working copy is dirty with a large described change `ef98dc0a`: contract-local operation roots (`Deploy`, `Pin`, `Unpin`, `Retire`, `Query`, `WatchDeployments`, etc.) and renamed records (`DeploymentRequest` replacing `DeploymentSubmission`).
- `horizon-leaner-shape` bookmark is at `a007e8b6`.
- `main` is at `ae8b3525`.

Critical gap:

- `lojix` is not yet pinned to this new contract shape. Updating the pin now would be an ABI break until `lojix` migrates request matching, tests, and docs to the new operation names.

MVP implication:

- The next implementation pass should treat `signal-lojix` + `lojix` as one compatibility cut: finalize and push the contract branch, then migrate `lojix` to that exact named reference in the same pass.

### `CriomOS`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS/horizon-leaner-shape`

State:

- Worktree is clean at `325de8a7` — `criomos: consume service variant vector`.
- `main` has advanced to `39cca733` — `criomos: gate all-firmware deployment policy`.

Critical gap:

- Modules still consume `horizon.node.behavesAs` widely: router, network, metal, nspawn, users, liveiso, llm, normalize, and others.
- `docs/GUIDELINES.md` still names `horizon.node.behavesAs.*`.
- There is no visible `criomosLib.predicates.*` consumer cutover in this branch.

MVP implication:

- Horizon role-merge cannot land alone. `CriomOS-lib/lib/predicates.nix` and the CriomOS module sweep have to land with it, or the lean branch breaks immediately.

### `CriomOS-lib`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-lib/horizon-leaner-shape`

State after my fix:

- Branch tip `3143a175`.
- Still intentionally small: `lib/default.nix` with `constants`, `importJSON`, and `mkJsonMerge`; no `predicates.nix` yet.

Critical gap:

- The destination requires a new predicate surface that derives `isCenter`, `isEdge`, `isRouter`, `isRemoteNixBuilder`, cache role, large-AI role, container-host facts, and related booleans from `node.roles + node.placement + node.pubKeys`.

MVP implication:

- This is the natural first repo for the horizon role-merge cutover, because CriomOS consumers need the new predicate functions before horizon drops `behavesAs`.

### `goldragon`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/goldragon/horizon-leaner-shape`

State:

- Working copy has an added `INTENT.md` from another lane. I did not touch it.
- `horizon-leaner-shape` bookmark is at `5b55de84` — `goldragon: use lean service variants`.

MVP implication:

- Goldragon cluster data still needs to follow whatever horizon finalizes: either service variants remain until the role merge lands, or datom migrates to the role vector in the same cutover wave.

### `CriomOS-home`

Repo/worktree: `/home/li/wt/github.com/LiGoldragon/CriomOS-home/horizon-leaner-shape`

State:

- Worktree is clean at `e1206533` — `home: enrich AI providers from CriomOS-lib catalog`.
- Canonical `/git/.../CriomOS-home` remains locked by `pi-operator`, so I did not audit or edit home-profile deployment surfaces beyond checking status.

## Cutover blockers

1. **Horizon docs are ahead of code.** `horizon-rs` architecture describes role-merge; implementation still uses old species/service/Contained/behavesAs model.
2. **`signal-lojix` contract-local verb branch is not consumed by `lojix`.** `lojix` is green on the old branch pin; new contract shape requires a compatibility pass.
3. **`CriomOS-lib` lacks predicates.** CriomOS still consumes `behavesAs`; horizon cannot drop it until shared Nix predicates exist.
4. **Sandbox runner proves old projection path.** `CriomOS-test-cluster` has good Prometheus/nspawn infrastructure, but no lean-stack `lojix-daemon` smoke yet.
5. **Feature branch naming is inconsistent.** Most repos use `horizon-leaner-shape`; `CriomOS-test-cluster` still has `horizon-re-engineering`.

## Recommended next implementation order

1. Finalize and push the `signal-lojix` contract-local operation branch.
2. Migrate `lojix` to that exact `signal-lojix` named branch tip; update tests from old request names to new operation roots.
3. Add `CriomOS-lib/lib/predicates.nix` and tests for role/placement-derived predicates.
4. Migrate `CriomOS` consumers from `horizon.node.behavesAs` to `criomosLib.predicates.*`.
5. Land `horizon-rs` role-merge in code and update fixtures.
6. Add `lojix-daemon` build-only smoke to `CriomOS-test-cluster`.
7. Run the live `nspawn-dune-on-prometheus` gate after the build-only smoke is green.

## Questions for psyche

1. Should `CriomOS-test-cluster` rename or recreate its feature bookmark as `horizon-leaner-shape`, matching the rest of the lean arc, or should it remain `horizon-re-engineering` because it is a separate historical branch?
2. For the first MVP sandbox gate, is a `lojix-daemon` build-only deploy against the synthetic `dune` fixture sufficient, or must the first lean-stack gate include activation inside the nspawn machine?
3. Should `horizon-rs/ARCHITECTURE.md` be marked explicitly as "destination, not implementation" until role-merge code lands, or should operators immediately bring code up to the document instead?
