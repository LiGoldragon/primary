# Task for generalist

Fresh read-only follow-up lane: nix-jj-local-git-input. The first experiment proved path: overrides are broad, but it did not establish that a remote push is necessary. In a disposable setup representative of the colocated Jujutsu/Git skills repository, test whether a committed but unpushed JJ revision can be consumed through a pinned local Git flake input such as git+file (using an exact Git commit), whether the resulting source excludes .jj and ignored/untracked noise, and whether Nix can then transfer that narrow store input to a native remote builder without the revision existing on a remote Git server. Do not perform an expensive build; use tiny derivations/evaluation and inspect source contents/sizes. Also identify any JJ export/HEAD synchronization traps and whether pure non-colocated JJ has a safe equivalent. Return a concise answer to: must agents push every intermediate revision, or can a committed local Git revision provide narrow remote-build input? Include evidence and limitations. No shared edits, commits, or pushes.

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