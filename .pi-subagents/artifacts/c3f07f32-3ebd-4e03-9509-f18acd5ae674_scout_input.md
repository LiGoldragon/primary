# Task for scout

Read-only doctrine audit requested by the psyche: local `cargo test` is invalid; all tests must run through Nix so they execute on remote builders. We will discuss amendments before editing.

Do not edit any file, run tests, invoke Cargo/Nix builds/evaluations, mutate generated surfaces, or dispatch subagents. Inspect authoritative skill/role source in the LiGoldragon/skills repository and compare generated runtime projections only to understand reach.

Map every relevant instruction that currently permits, recommends, or accepts bare local language test execution—especially `cargo test`—including at least:
- testing
- nix-usage / nix-discipline
- code-implementation
- Rust implementation/audit skills
- repository closeout/version-control/feature workflows if they mention checks
- project role packets for generalist, general-code-implementer, rust-auditor, nix-auditor, reviewer, and operating-system-implementer
- any generator/template source that owns repeated verification wording.

Return:
1. exact authoritative source files and quoted/line-located passages that conflict with or weaken the rule;
2. how generated `.agents`/`.pi` surfaces inherit those passages, without proposing edits to generated files;
3. a minimal coherent amendment set in owning source, avoiding repetitive patches;
4. proposed normative wording that clearly says bare local `cargo test` is invalid evidence and must not be run for testing, and that test suites must be exposed/executed as Nix checks or named Nix test outputs on remote builders;
5. how agents should verify that a remote builder—not local fallback—actually executed the test derivation, using existing workspace interfaces/doctrine;
6. scope questions for psyche discussion: whether the ban applies only to test execution or also `cargo check`, clippy, rustdoc/doctests, benchmarks, and formatting; how stateful tests/named outputs fit; what to do when remote builders are unavailable;
7. migration risks for repos whose tests are not yet exposed through Nix, and a transitional behavior that does not silently fall back to Cargo.

Separate observations from recommendations. Keep output concise enough for a doctrine decision. Do not write a report unless needed for fresh-context handoff; chat output is preferred.

## Acceptance Contract
Acceptance level: reviewed
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Implement the requested change without widening scope
- criterion-2: Return evidence sufficient for an independent acceptance review

Required evidence: changed-files, tests-added, commands-run, validation-output, residual-risks, no-staged-files

Review gate: optional by reviewer.

Finish with a fenced JSON block tagged `acceptance-report` in this shape:
Use empty arrays when no items apply; array fields contain strings unless object entries are shown.
```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "specific proof"
    }
  ],
  "changedFiles": [
    "src/file.ts"
  ],
  "testsAddedOrUpdated": [
    "test/file.test.ts"
  ],
  "commandsRun": [
    {
      "command": "command",
      "result": "passed",
      "summary": "short result"
    }
  ],
  "validationOutput": [
    "validation output or concise summary"
  ],
  "residualRisks": [
    "none"
  ],
  "noStagedFiles": true,
  "diffSummary": "short description of the diff",
  "reviewFindings": [
    "blocker: file.ts:12 - issue found, or no blockers"
  ],
  "manualNotes": "anything else the parent should know"
}
```