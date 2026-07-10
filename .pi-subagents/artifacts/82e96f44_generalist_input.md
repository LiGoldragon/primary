# Task for generalist

You are reviving a previous subagent conversation.

Original run: 636eb66e
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Final source review found one remaining documentation blocker; all code, process-tree timeout, auth, tests, pins, and Nix/source behavior otherwise passed.

Continue as the sole worker in the same held lane. Keep production stopped; no authenticated calls/deployment/backup changes. Do not spawn subagents. Serialize any Nix lock operations and do not overlap unrelated Nix work.

Required correction: in `spirit-judge/ARCHITECTURE.md:23-26`, replace the contradictory claim that retries belong in generic `judge`. State truthfully that `judge` owns bounded single-attempt provider mechanics, while `spirit-judge` owns any safe domain-specific retry policy. Align exactly with `judge/README.md` and `signal-spirit-judge/ARCHITECTURE.md` without expanding scope.

Commit/push the spirit-judge documentation correction. Because the immutable source revision changes, update and push every required Home/deployment pin/lock to the new spirit-judge revision in producer-before-consumer order, using one foreground Nix update at a time. Machine-check the resulting pin chain. Run only narrow formatting/docs/source checks needed; no broad rebuild unless required. Keep claims held for a final read-only doc/pin verification.

Reviewer artifact: `/home/li/primary/.pi-subagents/artifacts/95201a88-e425-4319-90f9-a884536eff3b_reviewer_output.md`.

Return exact successor revisions and pin evidence. Do not alter already-approved code.

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