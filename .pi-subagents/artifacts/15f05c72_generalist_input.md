# Task for generalist

You are reviving a previous subagent conversation.

Original run: 82e96f44
Original agent: generalist
Original session file: /home/li/.pi/agent/sessions/--home-li-primary--/2026-07-10T16-12-43-460Z_019f4ccd-7e44-7200-864a-ab25009b65e7/9c351f1f/run-0/session.jsonl

Use the stored session context as background. Answer the orchestrator's follow-up below. Do not assume the original child process is still alive.

Follow-up:
The live attempt stopped safely before Luna/deployment/Terra. Read-only diagnosis found the failure is not transient: ad-hoc `/tmp/spirit-luna-witness` had no lockfile and resolved incompatible `nota@7dc0ab7e` / `schema-language@6aae825d`, producing 49 compile errors. Backup and logical marker were captured; services remain inactive; no model call or activation occurred. Lojix Current is now generation 81 at unrelated CriomOS revision `43d9234f`, so never deploy the older candidate over current without proper integration.

Resume as the sole worker in the held Recovery lane. Do not spawn subagents. Keep production stopped; no authenticated provider calls or deployment this turn. Serialize all Nix/build work, avoid overlapping unrelated Nix, and use one-job limits.

Required source remediation:
1. Delete/retire the task-created unlocked `/tmp/spirit-luna-witness` only after confirming it is the failed task artifact; do not reuse it.
2. Provide a first-class reproducible, privacy-safe component witness surface owned by the appropriate repository (prefer an existing locked crate/example/test binary if one fits; otherwise add the smallest repo-owned witness executable/example following Rust crate-layout doctrine). It must use the repository’s exact Cargo.lock/flake dependency graph, send a synthetic non-database Spirit judge request over the real typed socket/component path, and emit only a parsed verdict class plus non-sensitive model/effort/revision/exit metadata. It must not print prompt/provider output, diagnostics, credentials, or records.
3. Add fake-provider coverage for the witness and a reproducible Nix/package or locked invocation so no ad-hoc dependency resolution occurs. Document the exact Luna/Terra witness command in the cutover runbook.
4. Reconcile all relevant repository mains and current deployment source first. Current Lojix generation 81 reflects unrelated advancement; integrate/rebase the approved changes onto current main per doctrine, preserving all unrelated commits and work. Update producer→consumer pins through Home/deployment and prove the final candidate is a descendant/integration of current source, not a rollback to `229d9e45`.
5. Run narrow serialized checks, commit/push producers before consumers, machine-check the complete pin chain and clean task state. Do not activate.
6. Preserve the existing production backup and marker evidence; because services remain stopped, do not retake or touch them during source work.

Return SOURCE READY for another independent review with exact revisions, witness design/command, tests, integrated current-main ancestry/pin evidence, temp-artifact cleanup, and remaining live gates. Keep claims held and task branches/worktrees intact.

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