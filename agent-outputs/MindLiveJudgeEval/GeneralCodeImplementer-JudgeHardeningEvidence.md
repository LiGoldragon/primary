# Mind Judge Hardening Evidence

Task: implement the approved Mind accepted-knowledge judge hardening lane. Scope included the default judge training prompt, the Rust live evaluation harness, expanded contrast-set eval data, local checks, live DeepSeek Flash stateful and isolated evaluations, and closeout evidence. No prompt or harness change promotes DeepSeek Flash defaults.

## Source Changes

Repository: `/git/github.com/LiGoldragon/mind`

Commit: `67d41168096e` (`general-code-implementer(gpt-5): harden mind knowledge judge eval`)

Changed files:

- `src/knowledge-judge-prompts/accepted-knowledge.md`
- `src/bin/mind-live-knowledge-judge-eval.rs`

Prompt changes by research category:

- Decision procedure: rewrote the prompt around an ordered procedure: task/private checks, neighbor proposition comparison, duplicate, conflict, wrong subject, vague, source-required, false/unsupported, then accept.
- Neighbor comparison: added proposition-normalization instructions, identity selection rules, minimal conflict identity selection, and warnings that accepted neighbors are comparison data, not policy text.
- Wrong-subject payload: added explicit payload direction: `WrongSubject` carries the declared subject from the packet; contrast covers Contract-vs-Storage and same statement under right subject.
- SourceRequired vs FalseOrUnsupported: added a fork between claims needing external benchmark/deployment/account/latest/future evidence and fabricated or unsupported technical claims.
- Accept-positive guidance: added stable technical fact acceptance guidance and examples for broad but durable internal facts.
- Safety/task reminders: compact reminders preserve strong private/secret and task/instruction behavior; secret-source references are allowed as references only, not resolved values.
- Contrastive examples: added examples for paraphrase duplicate, related-but-new fact, conflict with distractors, wrong-subject direction, source-vs-false, valid positive, vague-vs-stable, and quoted instruction text as data.
- Verdict grammar: did not add NOTA verdict examples to markdown. Parseable verdict examples remain generated from Rust in `knowledge.rs`.

Harness and eval-data changes:

- Added short default work roots (`/tmp/mj-<hash>`) and Unix socket path-length preflight.
- Added raw/setup/scored row separation and kept rejection resubmission probes as diagnostic rows instead of scored primary rows.
- Added row fields for exact prefilter hits, semantic judge attempts, storage absence witness, row kind, and failure diagnosis.
- Added direct runner-ledger storage absence witness for rejected candidates; resubmission probes remain separate rejection-stability diagnostics.
- Added summary metrics for raw rows, setup rows/pass counts, scored rows, alias-missing count, exact prefilter hit count, semantic judge attempts, identity-bearing pass rate, verdict-class pass rate, reason pass rate, accepted-positive rate, safety rejection rate, storage absence witness rate, setup results, and invalid/retry telemetry availability.
- Added failure diagnosis labels: `ModelVerdictFailure`, `SetupAliasMissing`, `RuntimeUnavailable`, `StorageWitnessFailure`; setup model failures are labeled separately as `SetupModelFailure` when applicable.
- Added contrast-set cases for valid-vs-paraphrase, paraphrase-vs-related-new, false/source-required without accepted neighbors in isolated mode, wrong subject vs same statement under right subject, source-required benchmark vs source-location fact, and quoted instruction text vs actual instruction.

## Checks

Local checks run in `/git/github.com/LiGoldragon/mind`:

- `cargo check --bin mind-live-knowledge-judge-eval`: passed.
- `cargo test exact_accepted_knowledge_duplicate_rejects_before_judge_and_stores_nothing_new --test actor_topology`: passed.
- `cargo test agent_knowledge_judge_accepts_strict_verdict_and_prompts_with_packet --test actor_topology`: passed.
- `cargo test --test actor_topology`: passed, 42 tests.
- `cargo build --bin mind-live-knowledge-judge-eval --bin mind --bin mind-daemon --bin mind-write-configuration`: passed.

## Live Evaluation Commands

Stateful:

```sh
target/debug/mind-live-knowledge-judge-eval --mode stateful --probe-rejections --eval-id rust-prompt-v3-stateful-20260703T083929Z --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-stateful --work-directory /tmp/mjv2stateful
```

Isolated categories:

```sh
target/debug/mind-live-knowledge-judge-eval --mode isolated-categories --probe-rejections --eval-id rust-prompt-v3-isolated-20260703T084400Z --output-directory /home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-isolated --work-directory /tmp/mjv2iso
```

Both runs used default hash-only diagnostics. No redacted packet text mode was requested.

## Live Results

Stateful summary path: `/home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-stateful/summary.json`

- Exit code: 2, completed with failures.
- Raw rows: 227.
- Scored rows: 132.
- Setup rows: 0.
- Submit calls: 227.
- Exact prefilter hits: 22.
- Semantic judge attempts: 205.
- Alias-missing count: 9.
- Verdict-class pass rate: 112/132, 84.85%.
- Identity-bearing pass rate: 27/52, 51.92%.
- Accepted-positive rate: 22/27, 81.48%.
- Safety rejection rate: 15/16, 93.75%.
- Storage absence witness: 95/95, 100%.
- Failure diagnoses: 37 `ModelVerdictFailure`, 9 `SetupAliasMissing`.
- Category highlights: private/secret 8/8; source-needed 5/6; task/instruction 7/8; paraphrase duplicate 2/14; false/unsupported 1/6; conflict 7/14; valid seed 15/18.

Isolated summary path: `/home/li/primary/agent-outputs/MindLiveJudgeEval/rust-prompt-v3-isolated/summary.json`

- Exit code: 2, completed with failures.
- Raw rows: 485.
- Setup rows: 252, with 195 passed.
- Scored rows: 132.
- Submit calls: 485.
- Exact prefilter hits: 22.
- Semantic judge attempts: 463.
- Alias-missing count: 8.
- Verdict-class pass rate: 108/132, 81.82%.
- Identity-bearing pass rate: 27/52, 51.92%.
- Accepted-positive rate: 17/27, 62.96%.
- Safety rejection rate: 16/16, 100%.
- Storage absence witness: 158/158, 100%.
- Failure diagnoses: 40 `ModelVerdictFailure`, 8 `SetupAliasMissing`.
- Category highlights: private/secret 8/8; task/instruction 8/8; unsupported-no-neighbor 3/3; source-needed 5/6; paraphrase duplicate 2/14; false/unsupported 1/6; conflict 6/14; valid seed 11/18.

## Promotion Decision

Promotion gates were not met.

The prompt improved diagnostics and preserved strong safety categories, but DeepSeek Flash remains weak on paraphrase duplicate detection, conflict reason/identity selection, false/unsupported taxonomy under neighbor context, wrong-subject overuse, and acceptance of valid stable technical facts. Stateful and isolated primary pass rates remain far below a promotable threshold, and identity-bearing pass rate is only 51.92% in both modes.

## Secret Safety

The live runs used the configured typed secret-source reference only. The runner did not write resolved provider secret values, credential files, decrypted secret-store values, provider HTTP dumps, or redacted packet text. Synthetic secret cases contain fake placeholder strings only. Secret-source references are present only as references in manifest evidence.

## Remaining Blockers And Follow-Ups

- Deterministic isolated fixture seeding is not available through the current daemon/config surface; isolated mode still uses live model setup and reports setup failures separately. A future harness-only fixture seeding path would make prompt-quality diagnostics cleaner.
- The judge still needs better paraphrase-equivalence behavior. Current prompt training alone is insufficient for this model.
- The model overuses `WrongSubject` for valid Contract/Architecture/Source facts and for false/unsupported claims. More prompt text may not solve this; consider a stronger judge model or provider-side structured/schema enforcement before promotion.
- Setup seed acceptance is too unstable for broad isolated diagnostics, especially valid seed cases. Consider splitting seed acceptance into a deterministic harness fixture or narrowing seed statements to model-robust forms.
- Invalid/retry telemetry remains unavailable because agent-daemon validate-and-retry details are not exposed to the harness.
