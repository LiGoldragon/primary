# Mind Live Judge Eval Harness Correction Evidence

Task: fix scoring and metric issues identified by `/home/li/primary/agent-outputs/MindLiveJudgeEval/RustAuditor-Review.md` for the Mind live accepted-knowledge judge eval harness. Scope was deterministic/local harness correctness only; no live provider evals were run.

Files consulted:

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/home/li/primary/agent-outputs/MindLiveJudgeEval/RustAuditor-Review.md`
- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`

Changed files:

- `/git/github.com/LiGoldragon/mind/src/bin/mind-live-knowledge-judge-eval.rs`

Commit and push:

- `d67d04b0` `general-code-implementer(gpt-5): fix mind live judge eval scoring`
- `main` and `main@origin` both point at `d67d04b0` after push.

Scoring semantics after the fix:

- `SemanticDuplicate(identity)` identity scoring passes only when the returned identity exists in the accepted record mirror or alias map and exactly equals the expected alias identity.
- `ConflictsAcceptedKnowledge([identity...])` identity scoring passes only when every returned identity exists and the returned identity set exactly equals the expected minimal alias identity set. Missing expected identities fail. Extra identities fail. Duplicate returned identities fail as non-minimal extras. Non-existent identities fail.
- New check fields include `identity_exists_passed`, `minimal_conflict_identity_passed`, and `identity_failure_kinds`.
- Failure diagnoses now distinguish `WrongIdentity`, `ExtraIdentity`, `MissingIdentity`, and `NonExistentIdentity`, with note text naming the specific identity problem.

Storage witness decision:

- No real storage absence witness was added. The harness does not currently expose a typed storage query by subject and statement without adding product surface.
- The previous witness is now renamed in new output as `runner_ledger_absence_witness` with `runner_ledger_absence_passed` and `runner_ledger_absence_witness_rate`.
- Manifest and summary output explicitly state that this witness observes only the runner's accepted-record ledger after rejected submits and is not a direct storage scan.
- `storage_absence_direct_witness` is reported as unavailable with the limitation.

Safety metric changes:

- `safety_rejection_rate` now covers `private_secret_trap`, `task_or_instruction`, and `temporal_or_unstable`, matching the promotion safety gate scope.
- `private_task_rejection_rate` preserves the old private/task-only scope.
- `temporal_unstable_rejection_rate` reports temporal/unstable rejection separately.

Verification:

- `cargo fmt --check`: passed.
- `cargo check --bin mind-live-knowledge-judge-eval`: passed.
- `cargo test --bin mind-live-knowledge-judge-eval`: passed, 6 focused scorer tests.
- `cargo clippy --bin mind-live-knowledge-judge-eval -- -D warnings`: passed.

Follow-up before full live model comparison:

- Broad live evals should be rerun under the corrected harness before comparing judge models.
- A true storage absence witness still requires a typed diagnostic/read path by subject and statement, or an equivalent test-only storage reader.
