# Task for reviewer

Final narrow read-only verification of the last Spirit judge source blocker and successor pins. You are the only active worker; do not spawn subagents. Do not edit, run Nix, build broadly, deploy, start services, call providers, access secrets/records/backups, or mutate coordination.

Previously approved code revisions remain unchanged except the spirit-judge documentation successor. Verify immutable source only:
- spirit-judge `6af6ed7c8ddea9719da1dd119b53997225dddd79`
- CriomOS-home `0005123af63e410cba3114701b2b12f54f5e24e1`
- deployment `229d9e4520620ccf46c672f92c7b29544c7fe731`
- unchanged judge `dfba388b9fbf55468c6ae7f6b3b3520b6bebaad4`
- unchanged signal-spirit-judge `7c25b71a34858c0d912dff8fd0b4f4ac213d7cd1`
- unchanged Spirit `f9f5266abec8a0bcf43b8bcc93cf066aa9f97ea2`

Gate only:
1. `spirit-judge/ARCHITECTURE.md` now truthfully states generic `judge` owns bounded single-attempt provider mechanics and `spirit-judge` owns any safe domain-specific retry policy, aligned with judge README and signal architecture.
2. The spirit-judge successor differs only as intended and Home/deployment pins/locks consume it exactly without regressing the already-approved judge/signal/Spirit revisions.
3. Reconstruct the final immutable pin chain from revision blobs.

Return `SOURCE APPROVE` or `SOURCE BLOCK` with exact witnesses. List remaining live gates separately. Do not reject for intentionally pending live deployment/account witnesses; the psyche already authorized the ambient Codex login for that later phase.

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