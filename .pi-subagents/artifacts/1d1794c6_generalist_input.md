# Task for generalist

You are reviving a previous subagent conversation.

Original run: 82e96f44
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
Independent source review is SOURCE APPROVE with no blockers. Proceed to the authorized live cutover as the sole worker in the same held lane. Do not spawn subagents.

Psyche authority: the current ambient Codex CLI login is explicitly authorized as the intended account for the bounded Luna/Terra tests and production. Validate only through the approved non-secret `codex login status` interface; do not inspect, copy, identify, or expose auth material.

Resource guardrails:
- One Nix evaluation/build/activation operation at a time, foreground-owned to completion.
- Do not overlap unrelated active Nix work. Wait or return blocked.
- Use `--max-jobs 1 --cores 1` or supported equivalent; no parallel retries or broad redundant flake checks.
- Keep rollback generation available.

Use the approved immutable deployment revision `229d9e4520620ccf46c672f92c7b29544c7fe731` and follow its cutover runbook exactly.

Required live sequence:
1. Confirm both production services are inactive and candidate pin chain matches the approved immutable revisions.
2. Validate the authorized ambient Codex session via non-secret status only.
3. Create and verify the normal private byte-preserving production database backup, record only size/hash metadata, and capture the logical marker without inspecting records.
4. Run at most one bounded authenticated `gpt-5.6-luna` Medium component witness before production activation. Retain only timestamp, model, effort, executable/source revision, exit status, and parsed verdict class; no prompts, output text, credentials, diagnostics, or record content.
5. Activate immutable deployment through the existing safe Lojix path with serialized Nix. Verify the new generation is Current and exact closure/pin chain is active.
6. Verify live argv/service/socket/dependency/restart behavior uses `spirit-judge` over `signal-spirit-judge`, `openai-codex`, `gpt-5.6-terra`, Medium, 180000 ms, `codex-login`, packaged setsid/Codex, and no legacy fallback.
7. Run at most one bounded authenticated Terra Medium witness, retaining only the same privacy-safe fields. Do not create a Spirit intent record.
8. Verify fail-closed unavailable/malformed/timeout/provider-error behavior using isolated component/process or private database-copy probes. On the live production database use only service compatibility, read-only marker, and rejection/no-mutation evidence; do not submit an accepted live record or inspect content.
9. Recompare logical marker and file size/hash metadata. Stable marker is corpus evidence; byte differences after daemon reopen are not by themselves failure. Retain backup through acceptance.
10. If any gate fails, stop Spirit fail-closed and use documented rollback where safe; report exact state.

Keep claims/worktrees/branches until manager-supplied independent live review. Return LIVE READY with sanitized Luna/Terra witnesses, generation/current status, exact live argv/pins, service health, fail-closed evidence, backup/marker evidence, rollback state, resource serialization evidence, and any blocker. Do not perform final cleanup yet.

## Acceptance Contract
Acceptance level: attested
Completion is not accepted from prose alone. End with a structured acceptance report.

Criteria:
- criterion-1: Return concrete findings with file paths and severity when applicable

Required evidence: review-findings, residual-risks

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