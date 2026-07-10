# Task for generalist

You are reviving a previous subagent conversation.

Original run: 15f05c72
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Correction from the psyche: because the router Nix/Cargo processes ended when the worker ended, treat them as worker-owned/attached rather than unrelated. The prior classification and wait were wrong. Resume the same held lane and preserved rebase state as the sole worker; do not spawn subagents.

First confirm no prior Nix/Cargo process remains. Then run the exact required lock regeneration and `.#witness` package validation yourself as foreground-owned operations, one at a time, with `--max-jobs 1 --cores 1`. Keep the worker turn/session alive until each operation completes; do not background it, misclassify its child/remote-build processes as unrelated, or stop merely because status activity is quiet. On a real command failure, capture full output and return; do not overlap retries.

Complete the current-main integration from the preserved state: regenerate only declared input locks through owning interfaces, validate the locked witness, commit/push producer-before-consumer, and machine-check the final pin chain/ancestry. Keep production services stopped, backup/marker untouched, and make no authenticated provider call or activation. Return SOURCE READY for review, with exact revisions and resource-process evidence. Claims remain held; no cleanup yet.

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