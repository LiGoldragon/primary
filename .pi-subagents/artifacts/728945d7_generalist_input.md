# Task for generalist

You are reviving a previous subagent conversation.

Original run: 3aea97f0
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Resume only to diagnose and remediate the mandatory remote scheduling blocker, following the supervisor guidance that arrived after your clean stop. Sole worker; no subagents. Production remains stopped; no provider/database/activation work.

Do not run the test again first. Use read-only Nix configuration and derivation metadata to compare the remotely successful `spiritJudgePinChain` derivation with Home’s `spirit-judge-cli-contract`: system, requiredSystemFeatures, preferLocalBuild/allowSubstitutes, builder protocol/capabilities, and whether `--rebuild` or cached validity affects scheduling. Follow nix-usage remote-builder probe doctrine and do not inspect credentials.

If the CLI-contract derivation is not remote-portable, make the smallest owning Nix source correction so the exact named check is eligible for the authorized Prometheus builder. Then run one foreground remote validation with local slots disabled (`--option max-jobs 0`), one-job limits where applicable, and capture builder attribution. Do not use bare Cargo, local Nix fallback, ad-hoc scripts, or repeated retries.

If source is already portable and the builder is unavailable/mismatched, return the exact system/feature/scheduler blocker and do not mutate unrelated source. If it passes, complete the staged deployment integration checks through Nix, commit/push producer-before-consumer, and return SOURCE READY with exact revisions, remote builder evidence, pin/ancestry proof, and remaining live gates. Keep claims held.

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