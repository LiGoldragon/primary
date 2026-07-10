# Task for generalist

You are reviving a previous subagent conversation.

Original run: b3d32420-15dd-4174-8e5a-f51272334792
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Independent source review returned three focused blockers. Continue the same Recovery lane/claims as the sole worker; do not spawn subagents. Keep production services stopped, no authenticated calls/deployment, backup untouched, and serialize all Nix work with one foreground operation and `--max-jobs 1 --cores 1` where applicable.

Fix exactly:
1. `judge` timeout teardown must terminate/reap the entire process group even when the leader exits after SIGTERM. Do not return merely because the leader exited. After the grace interval, detect remaining group members and SIGKILL the group as needed, then reap safely. Add a fake descendant that explicitly ignores SIGTERM and prove no live descendant/sentinel survives escalation. Preserve typed/redacted errors and method doctrine.
2. The architecture correction exists at `signal-spirit-judge` revision `7c25b71` (or a verified successor). Inspect and land/use the actual correction, then repin every real consumer and lock/flake/vendoring/Home/deployment surface from `8f24ff21` to that exact published revision. Machine-check and build/test the integrated chain; do not pin documentation-only stale commits accidentally.
3. Run formatting on `spirit-judge` and ensure `cargo fmt --check` passes, especially `src/main.rs:113-117`.
4. Update timeout validation guidance to require the TERM-ignoring descendant witness if not already truthful.

Reviewer artifact: `/home/li/primary/.pi-subagents/artifacts/f6d47f82-c2b9-410a-be12-37e97c9eba1e_reviewer_output.md`.

Validate narrowly, commit/push producers before consumers, update full pin chain, and return SOURCE READY with exact revisions/checks/resource evidence. Keep claims held for one more independent source review. The psyche has already authorized the current ambient Codex login for the later bounded Luna/Terra calls; do not ask again and do not use it in this source-only turn.

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