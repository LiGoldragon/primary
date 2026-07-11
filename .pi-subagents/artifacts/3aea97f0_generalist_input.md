# Task for generalist

You are reviving a previous subagent conversation.

Original run: 5618eed5
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Resume the same held Recovery lane and staged deployment integration; my prior guidance arrived after your clean stop. You are the sole implementation worker and must not spawn subagents.

Mandatory psyche rule now applies: all testing/acceptance validation runs through Nix on authorized remote builders. Do not run bare Cargo tests/checks or local test binaries. For test derivations disable local build slots with `--option max-jobs 0`, use an uncached/rebuild path where needed, print/retain builder attribution, and stop blocked rather than falling back locally. Run one foreground Nix operation at a time and do not overlap retries.

Complete source integration:
1. Load/follow the repository’s documented Lojix materialization/deployment check interface and relevant operating-system/Nix usage doctrine. Do not rerun generic root `nix flake check` against the intentional default-system stub.
2. Correct the Nix pin assertion to traverse/assert the actual generated lock graph or exported package metadata. Do not assume a nonexistent top-level `signal-spirit-judge` node, hand-edit locks, or weaken the end-to-end signal→witness/Spirit→Home→deployment proof.
3. Validate the staged deployment through the correct named/materialized Nix surfaces on a remote builder, including the Nix-packaged witness and exact provider/model/effort/auth/timeout pins. Distinguish evaluation from remote test execution.
4. If the authoritative Lojix materialized check surface is absent, identify the smallest source-owned Nix check/output needed, add it, and validate remotely; otherwise return the exact blocker.
5. Commit/push the current-main deployment integration only after valid Nix evidence. Machine-check ancestry and the full pin chain. Keep production inactive; no provider call, database/backup touch, or activation.

Return SOURCE READY with exact revisions, commands/surfaces (not long logs), remote-builder attribution, pin/ancestry evidence, and remaining live gates. Keep claims/resources held for independent source review.

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