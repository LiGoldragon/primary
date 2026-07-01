# Lojix Core Nonlegacy Implementation Continue

Task: continue and finish the approved non-legacy Lojix core/schema/runtime implementation from the actual public core repo state. Scope was public `signal-lojix`, `meta-signal-lojix`, and `lojix`; `private-repos/` was not inspected. No commit or push was performed.

## Intent and local context read

- Read `/home/li/primary/lojix-nonlegacy-redesign-plan.md`.
- Read `/home/li/primary/lojix-run-deletion-migration-map.md`.
- Read `/home/li/primary/AGENTS.md` and repo-local `AGENTS.md` files.
- Attempted repo-local canonical `~/primary/repos/lore/AGENTS.md`; it is missing on this checkout.
- Spirit public text search class: `PublicTextSearch`; relevant record `10pz` supports replaceable design over compatibility preservation.

## Coordination

- Observed Orchestrate roles.
- Initial claim as `assistant` was rejected because the repos were already held by `general-code-implementer` from the prior timed-out worker.
- Claimed `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, and `/git/github.com/LiGoldragon/lojix` as `general-code-implementer` and continued from the dirty working-copy state.

## Changed files

### `/git/github.com/LiGoldragon/signal-lojix`

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `build.rs`
- `schema/lib.schema`
- `src/schema/lib.rs`
- `tests/dependency_boundary.rs`
- `tests/frame.rs`
- `tests/round_trip.rs`

### `/git/github.com/LiGoldragon/meta-signal-lojix`

- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `build.rs`
- `schema/lib.schema`
- `src/schema/lib.rs`
- `tests/dependency_boundary.rs`
- `tests/frame.rs`
- `tests/round_trip.rs`

### `/git/github.com/LiGoldragon/lojix`

- `AGENTS.md`
- `ARCHITECTURE.md`
- `Cargo.lock`
- `Cargo.toml`
- `README.md`
- `build.rs`
- `schema/nexus.schema`
- `schema/sema.schema`
- `skills.md`
- `src/bin/meta-lojix.rs`
- `src/daemon.rs`
- `src/schema/nexus.rs`
- `src/schema/sema.rs`
- `src/schema_runtime.rs`
- `tests/build_smoke.rs`
- `tests/client_nota.rs`
- `tests/deploy_job_survival.rs`
- `tests/durable_resume.rs`
- `tests/engine_routing.rs`
- `tests/horizon_materialization_contract.rs`

## Implementation summary

- Completed prior partial rename work across public contracts and runtime:
  - `DeploymentKind` / `FullOs` / `OsOnly` / `HomeOnly` replaced by `GenerationArtifact`, `HostComposition`, `CompleteHost`, `BaseHost`, and `UserEnvironment`.
  - `SystemAction` and `HomeMode` replaced by `HostDeployAction` and `UserEnvironmentAction`.
  - `ActivationKind` replaced by `ActivationEffect`.
  - Meta admission is now `DeployAccepted DeployHandle` instead of `Deployed AcceptedDeploy`.
  - Meta deploy requests are now `Host HostDeployment` and `UserEnvironment UserEnvironmentDeployment` with required `SourceRevisionPolicy`.
- Finished Lojix runtime alignment:
  - host/user-environment submission lowering uses the renamed contract types;
  - runtime materialization maps `CompleteHost`, `BaseHost`, and `UserEnvironment` through Nexus;
  - `ResolveAndRecord` replaces the pipeline flake with the resolved reference before eval;
  - `RequireImmutable` rejects mutable flake references;
  - event-log query routing uses `ReadEventLog` and returns typed `DeploymentEventsQueried EventLogPage`.
- Updated docs/comments/tests for direct nonlegacy vocabulary and admission semantics.
- Bumped versions for the breaking contract/runtime change:
  - `signal-lojix` `0.1.0` -> `0.2.0`;
  - `meta-signal-lojix` `0.1.0` -> `0.2.0`;
  - `lojix` `0.3.10` -> `0.4.0`;
  - schema build version expectations updated accordingly.

## Validation

Commands run and results:

- `spirit '(PublicTextSearch [legacy compatibility wrapper lojix replace additive])'` — passed; found public record `10pz` supporting replacement over compatibility preservation.
- `jj status --no-pager` and `jj diff --stat --no-pager` in the three repos — passed; confirmed prior dirty state and final changed-file set.
- `cargo test --features nota-text` in `signal-lojix` — passed; 8 tests passed, 0 failed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix"]'` in `meta-signal-lojix` — passed; 8 tests passed, 0 failed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix","/git/github.com/LiGoldragon/meta-signal-lojix"]'` in `lojix` — passed; 96 tests passed, 0 failed, 10 ignored by design for real Nix/network/daemon smoke coverage.
- `cargo fmt` in `lojix` — passed.
- Grep old vocabulary in all three repos:
  - `rg -n --hidden --glob '!target/**' --glob '!Cargo.lock' 'FullOs|OsOnly|HomeOnly|\(Deployed|\bDeployed\b|AcceptedDeploy|DeploymentKind|HomeMode|SystemAction'` — passed with no matches.
- Grep disallowed support/wrapper terms in live source/tests/docs/AGENTS:
  - `rg -n --hidden --glob '!target/**' --glob '!Cargo.lock' 'root fallback|postcheck|niri|pi symlink|local jj ref|compatibility decoder|compatibility translator|compatibility alias|lojix-cli' ARCHITECTURE.md README.md skills.md schema src tests AGENTS.md` — passed with no matches.

Notable failed exploratory commands:

- Running `meta-signal-lojix` tests without local path override failed because downstream git dependencies still point at pushed `signal-lojix` `main`, which does not yet contain the uncommitted `0.2.0` contract.
- `cargo update -p signal-lojix` attempts were not usable in this unpushed multi-repo state; final validation used Cargo `paths` overrides and left no path-source lock entries.

## Final worktree status

- No commit or push performed by request.
- No staged files: true. These are JJ working copies; no staging operation exists and none was performed.
- Final status shows only the implementation files listed above in the three public core repos.
- `private-repos/` was not inspected.

## Residual risks and remaining work

- Downstream validation currently requires Cargo `paths` overrides until the three repos are committed/pushed in dependency order and downstream locks are refreshed against remote refs.
- Real Nix/network/daemon smoke tests remain ignored by default and were not run: `build_smoke` ignored tests, `engine_routing::production_eval_materializes_horizon_inputs_and_returns_deploy_accepted`, and three ignored `test_op` live/hermetic Nix tests.
- Closeout should commit and push in dependency order (`signal-lojix`, then `meta-signal-lojix`, then `lojix`) and then rerun downstream tests without local `paths` overrides.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Implemented the accepted nonlegacy vocabulary in signal-lojix, meta-signal-lojix, and lojix only; did not inspect private-repos and did not touch CriomOS-home/CriomOS/skills docs."
    },
    {
      "id": "criterion-2",
      "status": "satisfied",
      "evidence": "Report includes changed files, commands, passing cargo tests, grep validation with no old vocabulary matches, residual risks, and no-staged-files status."
    }
  ],
  "changedFiles": [
    "/git/github.com/LiGoldragon/signal-lojix/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/signal-lojix/Cargo.lock",
    "/git/github.com/LiGoldragon/signal-lojix/Cargo.toml",
    "/git/github.com/LiGoldragon/signal-lojix/README.md",
    "/git/github.com/LiGoldragon/signal-lojix/build.rs",
    "/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema",
    "/git/github.com/LiGoldragon/signal-lojix/src/schema/lib.rs",
    "/git/github.com/LiGoldragon/signal-lojix/tests/dependency_boundary.rs",
    "/git/github.com/LiGoldragon/signal-lojix/tests/frame.rs",
    "/git/github.com/LiGoldragon/signal-lojix/tests/round_trip.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock",
    "/git/github.com/LiGoldragon/meta-signal-lojix/Cargo.toml",
    "/git/github.com/LiGoldragon/meta-signal-lojix/build.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema",
    "/git/github.com/LiGoldragon/meta-signal-lojix/src/schema/lib.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/dependency_boundary.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/frame.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/round_trip.rs",
    "/git/github.com/LiGoldragon/lojix/AGENTS.md",
    "/git/github.com/LiGoldragon/lojix/ARCHITECTURE.md",
    "/git/github.com/LiGoldragon/lojix/Cargo.lock",
    "/git/github.com/LiGoldragon/lojix/Cargo.toml",
    "/git/github.com/LiGoldragon/lojix/README.md",
    "/git/github.com/LiGoldragon/lojix/build.rs",
    "/git/github.com/LiGoldragon/lojix/schema/nexus.schema",
    "/git/github.com/LiGoldragon/lojix/schema/sema.schema",
    "/git/github.com/LiGoldragon/lojix/skills.md",
    "/git/github.com/LiGoldragon/lojix/src/bin/meta-lojix.rs",
    "/git/github.com/LiGoldragon/lojix/src/daemon.rs",
    "/git/github.com/LiGoldragon/lojix/src/schema/nexus.rs",
    "/git/github.com/LiGoldragon/lojix/src/schema/sema.rs",
    "/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs",
    "/git/github.com/LiGoldragon/lojix/tests/build_smoke.rs",
    "/git/github.com/LiGoldragon/lojix/tests/client_nota.rs",
    "/git/github.com/LiGoldragon/lojix/tests/deploy_job_survival.rs",
    "/git/github.com/LiGoldragon/lojix/tests/durable_resume.rs",
    "/git/github.com/LiGoldragon/lojix/tests/engine_routing.rs",
    "/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs"
  ],
  "testsAddedOrUpdated": [
    "/git/github.com/LiGoldragon/signal-lojix/tests/dependency_boundary.rs",
    "/git/github.com/LiGoldragon/signal-lojix/tests/frame.rs",
    "/git/github.com/LiGoldragon/signal-lojix/tests/round_trip.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/dependency_boundary.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/frame.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/tests/round_trip.rs",
    "/git/github.com/LiGoldragon/lojix/tests/build_smoke.rs",
    "/git/github.com/LiGoldragon/lojix/tests/client_nota.rs",
    "/git/github.com/LiGoldragon/lojix/tests/deploy_job_survival.rs",
    "/git/github.com/LiGoldragon/lojix/tests/durable_resume.rs",
    "/git/github.com/LiGoldragon/lojix/tests/engine_routing.rs",
    "/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs"
  ],
  "commandsRun": [
    {
      "command": "spirit '(PublicTextSearch [legacy compatibility wrapper lojix replace additive])'",
      "result": "passed",
      "summary": "Found public Spirit record 10pz supporting replacement over compatibility preservation."
    },
    {
      "command": "cargo test --features nota-text (signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed; schema generation/check ran through build.rs."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\"]' (meta-signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed against local uncommitted signal-lojix 0.2.0."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\",\"/git/github.com/LiGoldragon/meta-signal-lojix\"]' (lojix)",
      "result": "passed",
      "summary": "96 tests passed, 10 ignored by existing real Nix/network/daemon gates."
    },
    {
      "command": "cargo fmt (lojix)",
      "result": "passed",
      "summary": "Formatted Rust after internal activation helper renames."
    },
    {
      "command": "rg old deploy vocabulary in signal-lojix, meta-signal-lojix, lojix",
      "result": "passed",
      "summary": "No matches for FullOs, OsOnly, HomeOnly, Deployed, AcceptedDeploy, DeploymentKind, HomeMode, or SystemAction outside excluded Cargo.lock/target."
    },
    {
      "command": "rg disallowed support/wrapper phrases in live core source/tests/docs/AGENTS",
      "result": "passed",
      "summary": "No matches for root fallback, postcheck, niri, pi symlink, local jj ref rewriting, compatibility decoder/translator/alias, or lojix-cli."
    },
    {
      "command": "jj status --no-pager in all three repos",
      "result": "passed",
      "summary": "Confirmed uncommitted working-copy changes only; no commit or push performed."
    }
  ],
  "validationOutput": [
    "signal-lojix cargo test: ok, 8 passed, 0 failed.",
    "meta-signal-lojix cargo test with local paths override: ok, 8 passed, 0 failed.",
    "lojix cargo test with local paths override: ok, 96 passed, 0 failed, 10 ignored.",
    "Old vocabulary grep: no matches in signal-lojix, meta-signal-lojix, or lojix outside target/Cargo.lock exclusions.",
    "Disallowed support/wrapper grep: no matches in live core source/tests/docs/AGENTS."
  ],
  "residualRisks": [
    "Downstream tests require local Cargo paths overrides until repos are committed/pushed in dependency order and remote locks are refreshed.",
    "Ignored real Nix/network/daemon smoke tests were not run in this pass."
  ],
  "noStagedFiles": true,
  "diffSummary": "Replaced legacy deploy vocabulary in ordinary/meta schemas, generated Rust, Lojix internal schemas/runtime/tests/docs, added typed event-log query output, source revision policy handling, admission rename, and version bumps.",
  "reviewFindings": [
    "no blockers"
  ],
  "manualNotes": "No commit/push by request. private-repos was not inspected. Closeout should push signal-lojix first, then meta-signal-lojix, then lojix and rerun downstream tests without local paths overrides."
}
```
