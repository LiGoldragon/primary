# Mind Live Judge Eval Correction Audit

Task and scope: independent Rust audit of Mind commit `f9f6e0f8e5ab4c12fb4b98bfbda64b91cea6eace` (`general-code-implementer(gpt-5): correct mind live judge eval harness`) on `/git/github.com/LiGoldragon/mind`. Scope covered exact structural duplicate prefiltering, judge semantic boundary, typed NOTA parsing in the live eval harness, isolated mode separation, evidence naming, smoke evidence, and secret hygiene. Spirit public intent query surfaced `w312`: deterministic mechanism belongs in code while agent judgment is reserved for non-mechanical cognition.

## Findings

No defects found.

## Audited Behavior

- Exact duplicate prefilter: [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:546) loads accepted records, checks `ExactKnowledgeDuplicate` before constructing `KnowledgeJudgePacket`, and returns `MindReply::Rejected(KnowledgeRejectionReason::SemanticDuplicate(identity))` on exact `(subject, statement)` match. The comparison at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:600) is structural equality on `KnowledgeSubject` and `TextBody`.
- Judge boundary: no Rust paraphrase, keyword, regex, contradiction, or source-requirement logic was found in the admission path. Non-exact decisions remain behind `KnowledgeJudge::judge` at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:564).
- Regression coverage: [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:571) accepts an initial record, resubmits the same subject/statement, asserts `SemanticDuplicate(accepted_identity)`, checks the fake agent saw only one prompt, then submits a distinct statement and checks only two total judge prompts. This is an adequate path witness for "exact duplicate does not call judge and does not store a second accepted neighbor."
- Rust live harness parser: [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1162) parses CLI stdout with `nota_next::NotaSource::parse::<signal_mind::MindReply>()`. The supported Python entrypoint [scripts/live-knowledge-judge-eval.py](/git/github.com/LiGoldragon/mind/scripts/live-knowledge-judge-eval.py:18) is only an `execvp` launcher for the Rust binary or `cargo run`; no regex NOTA parser remains in the supported path.
- Isolated mode: `EvalMode::IsolatedCategories` is accepted at [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:216). The runner stops daemons, clears aliases and accepted-record mirrors, starts daemons under each category work directory, and reruns category-local seed/setup cases at [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:988). This is meaningfully separate from the single-daemon `stateful` path at [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:981).
- Evidence naming: manifest and summary emit `submit_calls`, `judge_attempts`, and `provider_call_count_unavailable: true` at [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1298) and [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1344). Markdown says provider HTTP call count is unavailable rather than exact at [src/bin/mind-live-knowledge-judge-eval.rs](/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs:1893).
- Diagnostics: the daemon writes only `packet_sha256`, `prompt_sha256`, and `training_sha256` by default at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:372). Redacted packet structure is opt-in through `MIND_JUDGE_DIAGNOSTIC_TEXT=redacted` at [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:410).
- Architecture docs match the implementation boundary: [ARCHITECTURE.md](/git/github.com/LiGoldragon/mind/ARCHITECTURE.md:659) assigns exact structural duplicate rejection to deterministic code and keeps paraphrase/conflict/truth/source decisions out of Rust mechanism.

## Smoke Evidence

Inspected `/home/li/primary/agent-outputs/MindLiveJudgeEval/rust-smoke-20260703/`:

- `manifest.json`: 2 cases, mode `stateful`, parser label `nota_next::NotaSource::<signal_mind::MindReply>`, provider telemetry unavailable, provider HTTP dumps false, secret source recorded as reference only.
- `summary.json`: `submit_calls: 2`, `judge_attempts: 2`, `provider_call_count_unavailable: true`, `failure_count: 0`.
- `summary.md`: provider HTTP call count explicitly unavailable.
- `results.jsonl`: 2 accepted seed cases passed with successful `Get` probes.

Secret hygiene check over the smoke directory found provider/model names, endpoint URL, and the secret-source reference `Gopass:platform.deepseek.com/api-key`, but no resolved secret bytes, API key values, bearer tokens, authorization headers, HTTP dumps, or decrypted secret-store output. The temporary work directory from the smoke run was no longer present, so this audit could not inspect daemon stdout/stderr or `judge-diagnostics.jsonl` from that run.

## Checks Run

- `jj status` in `/git/github.com/LiGoldragon/mind`: clean working copy; `main` parent is `f9f6e0f8`.
- `jj show f9f6e0f8 --stat`: confirmed the reported changed files and dependency changes.
- `cargo test exact_accepted_knowledge_duplicate_rejects_before_judge_and_stores_nothing_new --test actor_topology`: passed, 1 test run.
- `cargo check --bin mind-live-knowledge-judge-eval`: passed.
- Source searches with `rg` for regex/parser/provider-call/secret surfaces across the changed files and smoke artifacts.

## Residual Risks

- Smoke evidence is only a 2-case stateful seed run; it proves harness plumbing, not Flash quality across rejection categories, paraphrases, conflicts, wrong-subject cases, or isolated-category behavior.
- The harness estimates `judge_attempts` by exact-duplicate precheck against its local accepted-record mirror. This is correctly labeled as a harness attempt count, not provider HTTP count, but it should not be treated as provider telemetry.
- Durable smoke artifacts did not include daemon diagnostic files. Hash-only diagnostic behavior is verified from source, not from the reported smoke run's temporary work directory.

## Recommended Next Step

Run the full DeepSeek Flash eval through the Rust harness in both `--mode stateful` and `--mode isolated-categories`, with the default hash-only diagnostics and no `--include-redacted-packet-text`, then archive the output directories under `/home/li/primary/agent-outputs/MindLiveJudgeEval/`. Use the resulting `summary.json` values for `submit_calls`, `judge_attempts`, and `provider_call_count_unavailable`; do not report exact provider HTTP calls unless agent-daemon adds telemetry.
