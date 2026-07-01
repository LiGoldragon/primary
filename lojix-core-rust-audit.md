# Lojix Core Nonlegacy Rust Audit

Task: read-only audit of the public Lojix core nonlegacy implementation in `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, and `/git/github.com/LiGoldragon/lojix`. Private repos were not inspected. Approved intent used for judgment: no legacy support in live core contracts/runtime; accepted live vocabulary is `CompleteHost`, `BaseHost`, `UserEnvironment`, `DeployAccepted`, and `DeployHandle`; no aliases/parsers for `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, or `AcceptedDeploy`; no wrapper behavior.

Spirit evidence: public `PublicTextSearch` found record `10pz`, which supports replaceable design rather than compatibility preservation.

Verdict: **FAIL** for closeout from the current worktrees. The live legacy vocabulary removal is mostly successful, and path-overridden tests pass, but normal downstream Cargo builds still fail against stale locked git dependencies, and there are correctness/storage gaps in source revision and activation-slot handling.

## Findings

### Blocker: downstream repos do not build without local path overrides

Paths:
- `/git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock:404-406`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock:411-413`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock:769-771`

Risk: the downstream locks still point at pushed `signal-lojix` / `meta-signal-lojix` commits carrying `0.1.0` schema metadata. Normal `cargo check --features nota-text` fails because the generated downstream schemas import new nonlegacy types (`HostComposition`, `GenerationArtifact`) from dependencies that Cargo resolves to old git commits. This means the current core repos are only valid under local `paths` overrides and are not closeout-ready as repo states.

Evidence:
- `meta-signal-lojix` no-override check failed with `ImportedTypeNotFound { crate_name: "signal-lojix", module: "lib", type_name: "HostComposition" }`.
- `lojix` no-override check failed with `ImportedTypeNotFound { crate_name: "signal-lojix", module: "lib", type_name: "GenerationArtifact" }`.

Expected correction: close out in dependency order and refresh downstream locks after each upstream push: push/lock `signal-lojix` first, then update and validate `meta-signal-lojix` without `paths`, then update and validate `lojix` without `paths`. Do not close while downstream tests require local path overrides.

### Major: `ResolveAndRecord` does not durably record resolved source revision information

Paths:
- `/git/github.com/LiGoldragon/lojix/schema/sema.schema:67`
- `/git/github.com/LiGoldragon/lojix/schema/sema.schema:105`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:2363-2370`

Risk: the policy is named `ResolveAndRecord`, but the implementation only mutates the in-memory pipeline flake before eval. The durable SEMA deploy submission/job shapes do not include the requested ref, resolved flake/ref, resolved revision, or policy, and events do not capture them. After a restart or from typed event/status queries, operators cannot prove what exact source was accepted and built. This is a storage/wire safety gap and leaves the exact-ref behavior under-observable.

Expected correction: add versioned durable schema fields/events for requested ref, resolved ref/revision, and `SourceRevisionPolicy`; regenerate generated Rust; use the resolved durable value for eval/resume; add an end-to-end boundary test showing `ResolveAndRecord` records and builds from the resolved reference.

### Major: `RequireImmutable` uses a hand-rolled substring heuristic for structured flake references

Path: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:916-922`

Risk: `is_immutable` accepts any string containing `rev=` or `narHash=`. Flake references are structured input, and workspace Rust Parsing Storage And Wire discipline requires a real parser or established parser library for structured input. The current heuristic can accept malformed or misleading refs and does not verify that a revision is actually an immutable commit identity.

Expected correction: validate immutability through a real flake-reference parser or Nix metadata/lock resolution, and reject malformed or non-commit refs with a typed deploy rejection. Add negative tests for malformed refs that merely contain `rev=` / `narHash=`.

### Major: activation success records always commit `Current`, discarding computed activation slot

Paths:
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1154-1160`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:3025-3040`

Risk: `run_activate_generation` computes the correct slot from `ActivationEffect` and returns it in `ActivatedGeneration`, but the later `activation_commit` hard-codes `GenerationSlot::Current`. `SetBootProfile` / `ScheduleBootOnce` should land as `BootPending`, and `TestActivation` should land as `Recent`; currently successful activation commits can be persisted and queried under the wrong slot. This is runtime/storage correctness drift introduced around the renamed activation vocabulary.

Expected correction: propagate the `ActivatedGeneration.generation_slot` (or derive from `pipeline.activation_effect`) into `ActivationCommit`, persist the correct slot, and add tests that a boot-profile, boot-once, and test activation query back with the expected slot.

### Minor: one architecture witness is source-text search, not a live contract witness

Path: `/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs:23-28`

Risk: `base_host_materialization_excludes_home_and_broad_firmware` asserts a string exists in `src/schema_runtime.rs`. Per architectural truth tests, positive source search is not proof that the generated schema/runtime path uses the value. A shortcut or dead code could satisfy the test.

Expected correction: replace with a runtime or artifact witness that constructs the public/generated `MaterializationShape::BaseHost` path and observes the materialized override contents, or a generated schema/object witness that cannot be counterfeited by dead source text.

## Non-findings and residual risks

- No residual old live deploy vocabulary was found by targeted grep in the three public core repos outside `Cargo.lock`/`target`: no `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, `AcceptedDeploy`, `DeploymentKind`, `HomeMode`, or `SystemAction` matches.
- No hidden `lojix-run`/wrapper support terms were found in live core source/tests/docs checked with targeted grep. The only unrelated `wrapper` matches were NixOS `/run/wrappers/bin` PATH entries, not Lojix wrapper behavior.
- Generated Rust appears consistent with source schemas under the local dependency override path; the schema build checks run during `cargo test` passed.
- Ignored real Nix/network/daemon tests were not run. This leaves operational deployment behavior unverified.
- Current dependency order remains a closeout risk until downstream locks are refreshed against pushed upstream commits and validation passes without `paths` overrides.

## Commands run

- `spirit "(PublicTextSearch [lojix legacy support core contracts runtime vocabulary CompleteHost BaseHost UserEnvironment DeployAccepted DeployHandle])"` — passed; found public record `10pz` supporting replace-over-compatibility intent.
- `orchestrate "(Observe Roles)"` and `orchestrate "(Claim (RustAuditor [(Path /home/li/primary/lojix-core-rust-audit.md)] [write audit output]))"` — observed roles and claimed the report path.
- `jj status --no-pager` in all three repos — passed; confirmed only the implementation files are dirty.
- `cargo test --features nota-text` in `signal-lojix` — passed; 8 tests passed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix"]'` in `meta-signal-lojix` — passed; 8 tests passed.
- `cargo test --features nota-text --config 'paths=["/git/github.com/LiGoldragon/signal-lojix","/git/github.com/LiGoldragon/meta-signal-lojix"]'` in `lojix` — passed; 96 tests passed, 10 ignored.
- `cargo check --features nota-text` in `meta-signal-lojix` without local paths override — failed with missing imported `HostComposition` from old locked `signal-lojix`.
- `cargo check --features nota-text` in `lojix` without local paths override — failed with missing imported `GenerationArtifact` from old locked `signal-lojix`.
- `cargo fmt --check` in all three repos — passed.
- Targeted legacy-vocabulary grep in all three repos excluding `target/**` and `Cargo.lock` — passed with no matches.
- Targeted wrapper/support phrase grep in live source/tests/docs/AGENTS — passed with no relevant matches.

## Closeout judgment

Closeout for the core repos **must not proceed from the current worktrees**. At minimum, fix the no-override dependency/lock failure. I also recommend resolving the source-revision durability/parser issues and activation-slot persistence before declaring the core nonlegacy implementation complete.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include blocker/major/minor severity, file paths, risks, and expected corrections; residual risks are listed separately."
    }
  ],
  "changedFiles": [
    "/home/li/primary/lojix-core-rust-audit.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "spirit \"(PublicTextSearch [lojix legacy support core contracts runtime vocabulary CompleteHost BaseHost UserEnvironment DeployAccepted DeployHandle])\"",
      "result": "passed",
      "summary": "Found public intent record 10pz supporting replacement over compatibility preservation."
    },
    {
      "command": "jj status --no-pager in signal-lojix, meta-signal-lojix, lojix",
      "result": "passed",
      "summary": "Confirmed implementation worktree changes and no auditor edits in repos."
    },
    {
      "command": "cargo test --features nota-text (signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\"]' (meta-signal-lojix)",
      "result": "passed",
      "summary": "8 tests passed with local dependency override."
    },
    {
      "command": "cargo test --features nota-text --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\",\"/git/github.com/LiGoldragon/meta-signal-lojix\"]' (lojix)",
      "result": "passed",
      "summary": "96 tests passed, 10 ignored."
    },
    {
      "command": "cargo check --features nota-text (meta-signal-lojix, no paths override)",
      "result": "failed",
      "summary": "Build script failed: ImportedTypeNotFound HostComposition from old locked signal-lojix."
    },
    {
      "command": "cargo check --features nota-text (lojix, no paths override)",
      "result": "failed",
      "summary": "Build script failed: ImportedTypeNotFound GenerationArtifact from old locked signal-lojix."
    },
    {
      "command": "cargo fmt --check in all three repos",
      "result": "passed",
      "summary": "Formatting checks passed."
    },
    {
      "command": "rg old deploy vocabulary in signal-lojix, meta-signal-lojix, lojix excluding target/Cargo.lock",
      "result": "passed",
      "summary": "No matches for FullOs, OsOnly, HomeOnly, Deployed, AcceptedDeploy, DeploymentKind, HomeMode, or SystemAction."
    },
    {
      "command": "rg disallowed wrapper/support phrases in live core source/tests/docs/AGENTS",
      "result": "passed",
      "summary": "No relevant matches for lojix-run, lojix-cli, root fallback, postcheck, niri, pi symlink, local jj ref, or compatibility alias/decoder/translator."
    }
  ],
  "validationOutput": [
    "signal-lojix path-independent tests passed: 8 passed.",
    "meta-signal-lojix tests passed only with local signal-lojix path override: 8 passed.",
    "lojix tests passed only with local signal/meta path overrides: 96 passed, 10 ignored.",
    "meta-signal-lojix no-override cargo check failed on ImportedTypeNotFound HostComposition.",
    "lojix no-override cargo check failed on ImportedTypeNotFound GenerationArtifact.",
    "Legacy vocabulary grep found no live old names outside excluded target/Cargo.lock."
  ],
  "residualRisks": [
    "Ignored real Nix/network/daemon tests were not run.",
    "Downstream dependency locks must be refreshed after upstream pushes before no-override validation can pass.",
    "Source revision recording and activation slot persistence need behavior tests after correction."
  ],
  "noStagedFiles": true,
  "diffSummary": "Auditor did not edit core repos; wrote audit report only.",
  "reviewFindings": [
    "blocker: /git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock and /git/github.com/LiGoldragon/lojix/Cargo.lock - normal downstream builds fail without local path overrides because locks still point at old 0.1.0 signal/meta git commits.",
    "major: /git/github.com/LiGoldragon/lojix/schema/sema.schema and /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs - ResolveAndRecord only mutates in-memory flake state and does not durably record requested/resolved refs, revision, or policy.",
    "major: /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:916 - RequireImmutable is implemented by substring checks over a structured flake reference, violating parser discipline and risking false acceptance.",
    "major: /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1159 - activation commits hard-code GenerationSlot::Current and discard the computed activation slot.",
    "minor: /git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs:23 - BaseHost materialization test is source-text search, not a live architecture witness."
  ],
  "manualNotes": "Pass/fail: FAIL. Closeout may not proceed from the current worktrees; fix no-override dependency locks and the major runtime/storage findings first."
}
```
