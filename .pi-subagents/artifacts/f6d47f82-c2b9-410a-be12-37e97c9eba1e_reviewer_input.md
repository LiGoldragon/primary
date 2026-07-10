# Task for reviewer

Perform the independent SOURCE review gate for the Spirit judge remediation. You are the only active worker; do not spawn subagents. Read-only: do not edit, deploy, start services, call Luna/Terra, access auth/secret values, inspect Spirit record content, mutate coordination, or alter the production backup.

Resource safety:
- Run at most one Nix operation at a time, foreground-owned to completion.
- If any build is necessary, use `--max-jobs 1 --cores 1` or repository equivalent.
- Prefer inspection and existing evidence; avoid broad redundant flake evaluations.

Candidate revisions:
- signal-spirit-judge: `8f24ff2198a861eeb13ac54087447cf651de18b3`
- judge: `3e0457b5166539ac9f7b5ec719d22bfe00380f89`
- spirit-judge: `33ca69b6c5d9e781f38ba3d62467606f98f45894`
- spirit: `28a909bc7d89a8165d42e1c4ea906cc055edd962`
- CriomOS-home: `9427e25aedd544021da2d9d8373f069ff1005fa6`
- deployment: `042ef622e990d91246b53887823e4434e4b70739`
Reported machine pin chain: signal contract → spirit-judge/spirit → Home → deployment.

Review closure of all prior blockers:
1. Codex accepts only consumed typed `ExternalSession(codex-login)`, rejects other auth variants, and truthfully describes an authorized ambient CLI session rather than account selection.
2. Provider timeout isolates, terminates, and reaps the entire process group/tree; descendant-sentinel test proves no leak. Typed/redacted unavailable, timeout, exit, empty, non-UTF8, malformed paths are covered, including nonexistent executable.
3. Luna and Terra Medium fake argv tests exercise runtime selection; declarative policy is distinguished from operative Home argv.
4. Signal contract all-features passes and the exact fixed revision is consumed by both adapter and Spirit across Cargo/lock/flake/vendoring surfaces.
5. Nix/Home/deployment exact pins, real package CLI-contract assertion, service fail-closed ordering, timeout/auth/model/effort argv, and fake-rendering-check labeling are truthful.
6. Judge README retry/ownership claims, signal architecture runtime wording, validation guidance, cutover preflight/pin chain, database marker semantics, rollback, and privacy-safe witness docs are correct.
7. Production services are expected stopped; no live call/deployment evidence should be claimed yet.

Use actual diffs/revisions and narrowly meaningful checks. Return `SOURCE APPROVE` or `SOURCE BLOCK` with severity-ranked findings, exact witnesses/checks, resource-concurrency evidence, and remaining post-authorization live gates. Include any refined docs/skills suggestions separately. Do not fail merely because authenticated/live gates intentionally await source approval.

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