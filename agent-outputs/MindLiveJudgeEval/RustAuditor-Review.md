# Rust Auditor Review

Task: independent audit of the research-driven Mind accepted-knowledge judge hardening pass. Scope included Mind commit `67d41168096e`, primary evidence commit `ec159d152d88`, the prompt file, the Rust live-eval harness, evidence report, and archived output directories `rust-prompt-v3-stateful` and `rust-prompt-v3-isolated`. No live provider calls were run.

## Findings

1. Medium: conflict identity checks allow overbroad identity sets to pass.

File: `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1981`

Risk: `ReplyEvaluation::check_identity` marks `ConflictsAcceptedKnowledge` identity correctness as passed when the returned identity list contains the expected identity anywhere. The prompt and researcher recommendation require the minimal directly conflicting neighbor set. A model can return the right identity plus unrelated topical identities and still pass the identity-bearing metric. This inflates `identity_bearing_pass_rate` and hides exactly the over-citation behavior the hardening pass is meant to measure.

Expected correction: represent expected conflict identities as a set and compare the returned set exactly, or add an explicit `minimal_conflict_identity_passed` check that fails on missing or extra identities. Keep semantic duplicate as single-identity equality.

2. Medium: the storage absence witness is not a direct storage witness.

File: `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1215` and `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:2028`

Risk: `StorageAbsenceWitness` checks only the runner's in-memory `accepted_records` ledger and its count before/after a rejected submit. That ledger is populated only after the runner observes `Accepted` and then `Get` returns `Found`. It does not query Mind storage by subject/statement after a rejected reply. If the daemon incorrectly stored a rejected candidate while returning `Rejected`, this witness would still pass. The JSON kind is honest enough (`runner_accepted_record_ledger_absence`), but the evidence report's "direct storage witness" wording overclaims it.

Expected correction: either rename/report it as a runner-ledger absence witness, or add a real storage witness through a diagnostic test-only query, storage reader over the isolated test store, or daemon-side search by subject/statement. Until then, do not use the `95/95` or `158/158` numbers as proof of durable storage absence.

3. Low: `safety_rejection_rate` omits temporal/unstable safety cases.

File: `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1581`

Risk: the metric covers only `private_secret_trap` and `task_or_instruction`. The recommendation report's promotion gates treat private/secret, task/instruction, and temporal/unstable as safety categories that should stay at 100%. Both v3 runs scored temporal/unstable at only `8/10`, but the summary still reports safety as `15/16` and `16/16`. This does not change the non-promotion result, but it can mislead future gate reviews.

Expected correction: rename the current metric to `private_task_rejection_rate`, or add temporal/unstable to the safety gate and report separate submetrics so source/temporal failures remain visible.

## Verified Evidence

Spirit query: `PublicTextSearch [Mind knowledge judge]` returned no matching public record, so this audit uses the supplied brief and local lane artifacts as authority.

Prompt rewrite: `/git/github.com/LiGoldragon/mind/src/knowledge-judge-prompts/accepted-knowledge.md` follows the researcher recommendations: ordered decision procedure, neighbor proposition comparison, declared-subject `WrongSubject` payload direction, source-vs-false fork, accept-positive guidance, safety reminders, and contrastive examples. I found no hard-coded parseable NOTA verdict examples in the markdown. Runtime verdict examples are still generated from Rust in `/git/github.com/LiGoldragon/mind/src/knowledge.rs:264`.

Metric recomputation from `results.jsonl` matches the evidence report and user summary:

- Stateful: raw/scored `227/132`; setup `0`; submit/judge `227/205`; exact prefilter hits `22`; verdict class `112/132`; identity-bearing `27/52`; accepted-positive `22/27`; private/task safety `15/16`; runner-ledger storage witness `95/95`; paraphrase duplicate `2/14`; false/unsupported `1/6`; conflict `7/14`.
- Isolated: raw/setup/scored `485/252/132`; setup passed `195/252`; submit/judge `485/463`; exact prefilter hits `22`; verdict class `108/132`; identity-bearing `27/52`; accepted-positive `17/27`; private/task safety `16/16`; runner-ledger storage witness `158/158`; paraphrase duplicate `2/14`; false/unsupported `1/6`; conflict `6/14`; valid seed `11/18`.

Secret hygiene: artifacts contain full eval statements and typed secret-source references such as the configured provider secret source path, plus synthetic fake secret placeholders. I found no resolved provider key, decrypted credential value, provider HTTP dump, or diagnostic packet text directory in the v3 output directories.

Checks inspected: implementer reported `cargo check --bin mind-live-knowledge-judge-eval`, targeted actor-topology tests, full `actor_topology`, and build of relevant binaries as passing. I did not rerun Cargo because this audit was constrained to read-only inspection and local parsing; Cargo would write build artifacts.

## Interpretation

The v3 failures are not primarily a prompt-coverage problem. The prompt implements the requested research advice and the added examples are reasonable. The harness now separates setup, primary, and probe rows and the recomputed counts are consistent.

The remaining failures are mostly model capability and architecture pressure:

- Flash accepts most paraphrase duplicates as new facts in both modes.
- Flash overuses `WrongSubject` for source/false/conflict/valid-positive cases.
- Flash rejects too many stable positives, especially in isolated setup.
- Identity-bearing correctness remains `27/52` even after explicit identity rules.

There are some harness issues above, but they do not explain the poor aggregate results. DeepSeek Flash is not suitable as the final accepting authority for Mind accepted knowledge on this evidence.

## Recommended Next Action

Do not spend another broad prompt-only pass on Flash. The next useful step is an architecture change: deterministic or retrieval-assisted neighbor handling plus Pro/equivalent confirmation for accepts and identity-bearing rejects. Keep Flash only as cheap telemetry or a reject-only/draft screen until a stronger model clears the same gate suite. Use deterministic isolated fixture seeding for prompt-quality diagnostics before any further live model comparison.
