# Lojix Core Audit Fixes

Task and scope: fixed the public Lojix core Rust audit blockers in `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, and `/git/github.com/LiGoldragon/lojix`. No commit or push was performed. `private-repos/` was not inspected.

## Implementation summary

Changed source revision recording from an in-memory-only flake mutation to typed durable evidence:

- moved `SourceRevisionPolicy` into `signal-lojix` so ordinary events/state can carry it without depending on the meta contract;
- added `SourceRevisionRecord { policy, requested_ref, resolved_ref, resolved_revision }` to ordinary schema;
- added source revision evidence to ordinary `Generation` and `DeploymentPhaseEvent`;
- added source revision evidence to Lojix SEMA `ActivationCommit`, `LiveGeneration`, and durable `DeployJob` rows;
- added source revision evidence to Nexus `FlakeAuthRequest`, `ResolvedFlake`, and `NixEvalCommand`;
- updated runtime so `ResolveAndRecord` stores requested and resolved refs/revision in the active pipeline, deploy job row, event log, eval command, activation commit, and generation state.

Fixed `RequireImmutable` validation:

- replaced the old substring heuristic with a structured query parser that validates `rev` as a full 40-hex commit and `narHash` as an SRI-style `sha256-...` value;
- added negative tests for malformed refs that merely contain `rev=` or `narHash=` text.

Fixed activation slot persistence:

- carried the `ActivatedGeneration.generation_slot` returned by the activation effect into the activation commit;
- removed the hard-coded `GenerationSlot::Current` from activation commit construction;
- added tests for boot profile, boot-once, and test activation slot persistence.

Improved the materialization witness:

- removed the BaseHost source-text-only assertion from `tests/horizon_materialization_contract.rs`;
- added a runtime unit witness for `DeploymentInput::from_shape` proving `CompleteHost` emits home/all-firmware and `BaseHost` excludes both.

## Files changed in this pass

- `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema`
- `/git/github.com/LiGoldragon/signal-lojix/src/schema/lib.rs`
- `/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema`
- `/git/github.com/LiGoldragon/meta-signal-lojix/src/schema/lib.rs`
- `/git/github.com/LiGoldragon/lojix/schema/nexus.schema`
- `/git/github.com/LiGoldragon/lojix/schema/sema.schema`
- `/git/github.com/LiGoldragon/lojix/src/schema/nexus.rs`
- `/git/github.com/LiGoldragon/lojix/src/schema/sema.rs`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`
- `/git/github.com/LiGoldragon/lojix/tests/deploy_job_survival.rs`
- `/git/github.com/LiGoldragon/lojix/tests/durable_resume.rs`
- `/git/github.com/LiGoldragon/lojix/tests/engine_routing.rs`
- `/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs`

The worktrees also retain earlier nonlegacy implementation changes from the prior pass; no attempt was made to separate or revert them.

## Validation

Passed:

- `cargo test --features nota-text` in `signal-lojix`: 8 passed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix"]'` in `meta-signal-lojix`: 8 passed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix","/git/github.com/LiGoldragon/meta-signal-lojix"]'` in `lojix`: 108 passed, 10 ignored.
- `cargo fmt --check` in all three repos: passed.
- Targeted old-vocabulary grep excluding `target/**` and `Cargo.lock`: no matches for `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, `AcceptedDeploy`, `DeploymentKind`, `HomeMode`, or `SystemAction`.

Expected failures:

- `cargo check --features nota-text` in `meta-signal-lojix` without local paths failed because `Cargo.lock` still resolves old pushed `signal-lojix`, missing `HostComposition`.
- `cargo check --features nota-text` in `lojix` without local paths failed because locked upstream `signal-lojix` is stale and lacks `SourceRevisionPolicy`.

Conclusion: no-override Cargo checks are still expected to fail only because upstream commits are unpushed and downstream locks are stale. The code is ready for re-audit under local path overrides; closeout still needs dependency-order commit/push and downstream lock refresh.

## Residual risks

- Real Nix/network/daemon tests remain ignored and were not run.
- The structured immutable-ref validator is intentionally narrow: it accepts full `rev` query commits and SRI-style `narHash` query identities, not every possible Nix flake grammar form.
- No-override downstream validation remains blocked until the unpushed cross-repo state is closed out in dependency order.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings and residual risks include file paths and severity where applicable; audit blockers were fixed with schema/runtime/test changes and path-overridden validation passed."
    }
  ],
  "changedFiles": [
    "/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema",
    "/git/github.com/LiGoldragon/signal-lojix/src/schema/lib.rs",
    "/git/github.com/LiGoldragon/meta-signal-lojix/schema/lib.schema",
    "/git/github.com/LiGoldragon/meta-signal-lojix/src/schema/lib.rs",
    "/git/github.com/LiGoldragon/lojix/schema/nexus.schema",
    "/git/github.com/LiGoldragon/lojix/schema/sema.schema",
    "/git/github.com/LiGoldragon/lojix/src/schema/nexus.rs",
    "/git/github.com/LiGoldragon/lojix/src/schema/sema.rs",
    "/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs",
    "/git/github.com/LiGoldragon/lojix/tests/deploy_job_survival.rs",
    "/git/github.com/LiGoldragon/lojix/tests/durable_resume.rs",
    "/git/github.com/LiGoldragon/lojix/tests/engine_routing.rs",
    "/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs"
  ],
  "testsAddedOrUpdated": [
    "/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs: source revision event/state tests, immutable-ref negative tests, activation-slot tests, materialization unit witness",
    "/git/github.com/LiGoldragon/lojix/tests/deploy_job_survival.rs: DeployJob source revision fields",
    "/git/github.com/LiGoldragon/lojix/tests/durable_resume.rs: LiveGeneration source revision field",
    "/git/github.com/LiGoldragon/lojix/tests/engine_routing.rs: DeploymentPhaseEvent source revision field",
    "/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs: removed source-text-only BaseHost witness"
  ],
  "commandsRun": [
    {
      "command": "orchestrate \"(Observe Roles)\" and orchestrate claim for exact edited paths",
      "result": "passed",
      "summary": "Observed roles and claimed signal/meta/lojix schema/runtime/test paths plus the output report path before editing."
    },
    {
      "command": "SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text (signal-lojix)",
      "result": "passed",
      "summary": "Regenerated and checked signal schema artifacts."
    },
    {
      "command": "META_SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\"]' (meta-signal-lojix)",
      "result": "passed",
      "summary": "Regenerated and checked meta schema artifacts against local signal."
    },
    {
      "command": "LOJIX_UPDATE_SCHEMA_ARTIFACTS=1 cargo check --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\",\"/git/github.com/LiGoldragon/meta-signal-lojix\"]' (lojix)",
      "result": "passed",
      "summary": "Regenerated Lojix Nexus/SEMA artifacts and checked after runtime updates."
    },
    {
      "command": "cargo test --features nota-text (signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\"]' (meta-signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\",\"/git/github.com/LiGoldragon/meta-signal-lojix\"]' (lojix)",
      "result": "passed",
      "summary": "108 tests passed, 10 ignored."
    },
    {
      "command": "cargo fmt --check in signal-lojix, meta-signal-lojix, lojix",
      "result": "passed",
      "summary": "Formatting checks passed after running cargo fmt."
    },
    {
      "command": "rg old deploy vocabulary in signal-lojix, meta-signal-lojix, lojix excluding target/Cargo.lock",
      "result": "passed",
      "summary": "No matches for FullOs, OsOnly, HomeOnly, Deployed, AcceptedDeploy, DeploymentKind, HomeMode, or SystemAction."
    },
    {
      "command": "cargo check --features nota-text (meta-signal-lojix, no paths override)",
      "result": "failed",
      "summary": "Expected stale-lock failure: locked pushed signal-lojix lacks HostComposition."
    },
    {
      "command": "cargo check --features nota-text (lojix, no paths override)",
      "result": "failed",
      "summary": "Expected stale-lock failure: locked pushed signal-lojix lacks SourceRevisionPolicy."
    },
    {
      "command": "jj status --no-pager and jj diff --stat --no-pager in all three repos",
      "result": "passed",
      "summary": "Confirmed dirty JJ working copies and no commit/push performed."
    }
  ],
  "validationOutput": [
    "signal-lojix cargo test: ok, 8 passed.",
    "meta-signal-lojix cargo test with local signal path override: ok, 8 passed.",
    "lojix cargo test with local signal/meta path overrides: ok, 108 passed, 10 ignored.",
    "Old vocabulary grep: no live matches outside target/Cargo.lock exclusions.",
    "No-override meta/lojix cargo checks still fail from stale locked upstream commits, as expected until closeout."
  ],
  "residualRisks": [
    "major: /git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock and /git/github.com/LiGoldragon/lojix/Cargo.lock - no-override checks fail until signal/meta are pushed and downstream locks refreshed.",
    "minor: /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs - immutable flake validation is structured and no longer substring-based, but intentionally accepts only full rev query commits and SRI-style narHash identities.",
    "minor: ignored real Nix/network/daemon tests were not run."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added typed source revision records to ordinary/meta/SEMA/Nexus/generated/runtime paths, persisted activation slots from effect results, replaced substring immutability checks with structured query validation, updated tests, and replaced the BaseHost source-text witness with a runtime unit witness.",
  "reviewFindings": [
    "no blockers in the fixed audit blocker set under local path overrides",
    "blocker for closeout only: /git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock and /git/github.com/LiGoldragon/lojix/Cargo.lock still resolve stale unpushed upstream contract commits for no-override Cargo checks"
  ],
  "manualNotes": "No commit or push by request. Core is ready for re-audit with local path overrides; final closeout must push signal-lojix, then meta-signal-lojix, then refresh/test lojix without path overrides."
}
```
