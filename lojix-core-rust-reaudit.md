# Lojix Core Rust Re-audit

Task and scope: read-only re-audit of the public Lojix core worktrees after audit fixes. Repositories inspected: `/git/github.com/LiGoldragon/signal-lojix`, `/git/github.com/LiGoldragon/meta-signal-lojix`, and `/git/github.com/LiGoldragon/lojix`. I did not inspect `private-repos`, and I did not edit, commit, or push any core repository files.

Intent evidence: `spirit PublicTextSearch` for the new fix terms found no matching record. `spirit Lookup 10pz` confirmed the public replace-over-compatibility principle relevant to removing old live vocabulary.

Verdict: **PASS for the prior Rust audit blocker fixes under local path overrides**. The source-revision durability, activation-slot persistence, `RequireImmutable` substring removal, and materialization witness blocker set is materially fixed. **Closeout remains on hold** until dependency-order push/lock refresh makes downstream no-override Cargo checks pass.

## Findings

### Closeout blocker: no-override downstream builds still resolve stale git dependency locks

Paths:
- `/git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock:404-406`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock:411-413`
- `/git/github.com/LiGoldragon/lojix/Cargo.lock:769-771`

Risk: normal downstream builds still resolve pushed `signal-lojix` / `meta-signal-lojix` commits with old `0.1.0` contracts. `meta-signal-lojix` fails without `paths` because old `signal-lojix` lacks `HostComposition`; `lojix` fails without `paths` because old `signal-lojix` lacks `SourceRevisionPolicy`. This is the expected unpushed dependency-order/lock issue, not a new implementation regression, but it blocks final repository closeout.

Expected correction: commit and push in dependency order, then refresh downstream locks and validate without path overrides: `signal-lojix` first, then `meta-signal-lojix`, then `lojix`.

### Minor: `RequireImmutable` no longer uses substring matching, but the local query parser remains narrow review debt

Path: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:935-1008`

Risk: the previous blocker was fixed for the stated malformed `rev=` / `narHash=` cases: the code now parses query parameters and validates `rev` as 40 hex characters, and the tests at `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:4993-5019` reject malformed strings that only contain `rev=` or `narHash=` text. However, this is still a hand-rolled query parser over structured flake references (`split_once('?')`, `split('&')`, `split_once('=')`), and `NarHashText::is_sri_hash` accepts any non-empty `sha256-` suffix. Under the workspace Rust Parsing Storage And Wire rule, this remains parser debt if the accepted flake-reference grammar broadens.

Expected correction: not required for the fixed blocker set, but a future hardening pass should use an established URL/flake-reference parser or Nix metadata validation for the `narHash` form and add a negative test for prefixed but invalid SRI values such as `?narHash=sha256-deadbeef` if full SRI validation is intended.

## Verified prior blockers

- Source revision policy/evidence is now durable in ordinary schema and generated Rust: `SourceRevisionPolicy` / `SourceRevisionRecord` at `/git/github.com/LiGoldragon/signal-lojix/schema/lib.schema:68-69`, `Generation.source_revision` at lines 86-95, and `DeploymentPhaseEvent.source_revision` at lines 149-157.
- SEMA records now carry source revision evidence: `ActivationCommit` at `/git/github.com/LiGoldragon/lojix/schema/sema.schema:71`, `LiveGeneration` at line 88, and `DeployJob` requested/resolved fields at lines 104-109.
- Nexus command/result boundaries now carry source revision evidence: `FlakeAuthRequest`, `ResolvedFlake`, and `NixEvalCommand` at `/git/github.com/LiGoldragon/lojix/schema/nexus.schema:80-88`.
- Runtime carries the resolved record through the pipeline: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:2538-2548` stores resolved source revision; lines 1217-1224 put it on `NixEvalCommand`; lines 1319-1333 put it on events; lines 1308-1316 require it for activation commits; lines 1366-1384 persist it into deploy jobs.
- Activation commit now persists the computed slot: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:1308-1316` uses `self.activation_slot?`; `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:2497-2501` stores the slot returned by the activation effect. Tests cover boot profile, boot once, and test activation at `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:4910-4965`.
- Materialization witness is no longer only source-text search for the BaseHost/CompleteHost distinction: `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5637-5657` exercises `DeploymentInput::from_shape` with generated `MaterializationShape::CompleteHost`, `BaseHost`, and `UserEnvironment`.
- Old live deploy vocabulary was not found in the checked core repos outside `target/**` and `Cargo.lock`: no matches for `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, `AcceptedDeploy`, `DeploymentKind`, `HomeMode`, or `SystemAction`.

## Residual risks

- Final no-override validation is still blocked by unpushed dependency-order/lock state, as described in the closeout blocker.
- Ignored real Nix/network/daemon tests were not run.
- The `RequireImmutable` parser is improved enough for the fixed blocker but remains intentionally narrow and hand-rolled.
- Existing source-text architecture checks remain for broad horizon-materialization presence in `/git/github.com/LiGoldragon/lojix/tests/horizon_materialization_contract.rs`; the specific BaseHost/CompleteHost materialization claim now has a runtime unit witness, but a fuller production-boundary artifact witness would be stronger.

## Commands run

- `spirit "(PublicTextSearch [Lojix core deploy immutable source revision activation materialization])"` — returned `(Error [no matching record])`; negative evidence only.
- `spirit "(Lookup 10pz)"` — passed; record supports replaceable design rather than compatibility preservation.
- `jj status --no-pager` and `jj diff --stat --no-pager` in all three repos — passed; confirmed dirty implementation worktrees and no auditor edits to core repos.
- `CARGO_TARGET_DIR=/tmp/lojix-reaudit-signal-target cargo test --features nota-text --locked` in `signal-lojix` — passed; 8 tests passed.
- `CARGO_TARGET_DIR=/tmp/lojix-reaudit-meta-target cargo test --features nota-text --locked --config 'paths=["/git/github.com/LiGoldragon/signal-lojix"]'` in `meta-signal-lojix` — passed; 8 tests passed.
- `CARGO_TARGET_DIR=/tmp/lojix-reaudit-lojix-target cargo test --features nota-text --locked --config 'paths=["/git/github.com/LiGoldragon/signal-lojix","/git/github.com/LiGoldragon/meta-signal-lojix"]'` in `lojix` — passed; 108 tests passed, 10 ignored.
- `CARGO_TARGET_DIR=/tmp/lojix-reaudit-meta-nooverride-target cargo check --features nota-text --locked` in `meta-signal-lojix` — failed as expected with `ImportedTypeNotFound { crate_name: "signal-lojix", module: "lib", type_name: "HostComposition" }` from locked old `signal-lojix`.
- `CARGO_TARGET_DIR=/tmp/lojix-reaudit-lojix-nooverride-target cargo check --features nota-text --locked` in `lojix` — failed as expected with `ImportedTypeNotFound { crate_name: "signal-lojix", module: "lib", type_name: "SourceRevisionPolicy" }` from locked old `signal-lojix`.
- `cargo fmt --check` in all three repos — passed.
- `rg -n "\b(FullOs|OsOnly|HomeOnly|Deployed|AcceptedDeploy|DeploymentKind|HomeMode|SystemAction)\b" . --glob '!target/**' --glob '!Cargo.lock'` in all three repos — passed; no matches.
- Targeted support/wrapper phrase grep across live source/tests/docs — no old deploy support path found; only unrelated documentation terms and NixOS `/run/wrappers/bin` PATH strings.
- Final `jj status --no-pager` in all three repos — unchanged from initial implementation dirty state.

## Closeout recommendation

Proceed with dependency-order closeout only: commit/push `signal-lojix`, refresh and validate `meta-signal-lojix` without path overrides, commit/push `meta-signal-lojix`, then refresh and validate `lojix` without path overrides. Do not declare the core repos closed while no-override downstream checks still require local `paths` overrides.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Findings include a closeout blocker with Cargo.lock paths and a minor parser-debt finding with schema_runtime.rs paths; residual risks are listed separately."
    }
  ],
  "changedFiles": [
    "/home/li/primary/lojix-core-rust-reaudit.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "spirit \"(PublicTextSearch [Lojix core deploy immutable source revision activation materialization])\"",
      "result": "passed",
      "summary": "Returned no matching record; treated as negative evidence."
    },
    {
      "command": "spirit \"(Lookup 10pz)\"",
      "result": "passed",
      "summary": "Confirmed public replace-over-compatibility principle relevant to no legacy support."
    },
    {
      "command": "jj status --no-pager and jj diff --stat --no-pager in signal-lojix, meta-signal-lojix, lojix",
      "result": "passed",
      "summary": "Confirmed dirty implementation worktrees and reviewed diff scope."
    },
    {
      "command": "CARGO_TARGET_DIR=/tmp/lojix-reaudit-signal-target cargo test --features nota-text --locked",
      "result": "passed",
      "summary": "signal-lojix: 8 tests passed."
    },
    {
      "command": "CARGO_TARGET_DIR=/tmp/lojix-reaudit-meta-target cargo test --features nota-text --locked --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\"]'",
      "result": "passed",
      "summary": "meta-signal-lojix: 8 tests passed with local signal path override."
    },
    {
      "command": "CARGO_TARGET_DIR=/tmp/lojix-reaudit-lojix-target cargo test --features nota-text --locked --config 'paths=[\"/git/github.com/LiGoldragon/signal-lojix\",\"/git/github.com/LiGoldragon/meta-signal-lojix\"]'",
      "result": "passed",
      "summary": "lojix: 108 tests passed, 10 ignored, with local signal/meta path overrides."
    },
    {
      "command": "CARGO_TARGET_DIR=/tmp/lojix-reaudit-meta-nooverride-target cargo check --features nota-text --locked",
      "result": "failed",
      "summary": "Expected closeout failure: locked pushed signal-lojix lacks HostComposition."
    },
    {
      "command": "CARGO_TARGET_DIR=/tmp/lojix-reaudit-lojix-nooverride-target cargo check --features nota-text --locked",
      "result": "failed",
      "summary": "Expected closeout failure: locked pushed signal-lojix lacks SourceRevisionPolicy."
    },
    {
      "command": "cargo fmt --check in all three repos",
      "result": "passed",
      "summary": "Formatting checks passed."
    },
    {
      "command": "rg old deploy vocabulary in all three repos excluding target/** and Cargo.lock",
      "result": "passed",
      "summary": "No matches for FullOs, OsOnly, HomeOnly, Deployed, AcceptedDeploy, DeploymentKind, HomeMode, or SystemAction."
    },
    {
      "command": "targeted support/wrapper phrase grep across live source/tests/docs",
      "result": "passed",
      "summary": "No old deploy support path found; only unrelated docs terms and /run/wrappers/bin PATH strings."
    }
  ],
  "validationOutput": [
    "Path-overridden signal-lojix cargo test passed: 8 passed.",
    "Path-overridden meta-signal-lojix cargo test passed: 8 passed.",
    "Path-overridden lojix cargo test passed: 108 passed, 10 ignored.",
    "No-override meta-signal-lojix cargo check failed only because Cargo.lock resolves old signal-lojix without HostComposition.",
    "No-override lojix cargo check failed only because Cargo.lock resolves old signal-lojix without SourceRevisionPolicy.",
    "Old live deploy vocabulary grep found no matches outside target/Cargo.lock exclusions."
  ],
  "residualRisks": [
    "Final closeout still requires dependency-order push and downstream Cargo.lock refresh before no-override builds pass.",
    "Ignored real Nix/network/daemon tests were not run.",
    "RequireImmutable uses a narrow hand-rolled query parser; adequate for the fixed substring blocker, but still parser debt if broader flake-reference validation is required.",
    "Broad horizon-materialization presence tests remain source-text based, though the BaseHost/CompleteHost mapping now has a runtime unit witness."
  ],
  "noStagedFiles": true,
  "diffSummary": "Auditor did not modify core repos. Current worktrees add typed source revision records through ordinary/SEMA/Nexus/runtime paths, persist activation slots from effect results, replace substring immutability checks with structured query validation, update tests, and remove old live deploy vocabulary.",
  "reviewFindings": [
    "no implementation blockers in the prior Rust audit blocker fix set under local path overrides",
    "closeout blocker: /git/github.com/LiGoldragon/meta-signal-lojix/Cargo.lock:404 and /git/github.com/LiGoldragon/lojix/Cargo.lock:411,769 still resolve stale pushed signal/meta dependencies, so normal no-override downstream Cargo checks fail until dependency-order push/lock refresh",
    "minor: /git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:935-1008 still hand-rolls flake query parsing and accepts any non-empty sha256- narHash suffix; not a blocker for the stated substring-heuristic fix, but parser debt under Rust Parsing Storage And Wire"
  ],
  "manualNotes": "Pass/fail: PASS for re-audit of the fixed blockers with local path overrides; HOLD/FAIL for final closeout until signal-lojix, then meta-signal-lojix, then lojix are validated without path overrides after dependency-order push and lock refresh."
}
```
