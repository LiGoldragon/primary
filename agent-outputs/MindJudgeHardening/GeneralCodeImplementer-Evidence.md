# Mind Judge Hardening Evidence

## Task And Scope

Implementation worker for the approved Mind judge-hardening lane. Scope was limited to Mind accepted-knowledge judge prompt/training and deterministic tests for the first approved rejection batch:

- duplicates;
- contradictions to accepted knowledge;
- non-knowledge tasks, instructions, imperatives, and requests;
- vague or unstable claims with no stable subject;
- submissions that do not agree with their declared subject/domain.

Mind accepts non-Spirit knowledge; Spirit remains the intent store. The accepted-knowledge surface stayed simplified: `Submit`, `Accepted`, `Get`, `Found`, `NotFound`, `Rejected`. `KnowledgeJudgeVerdict::Accept` remains payload-free.

## Files Consulted

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`

## Changed Files

Mind repo commit: `8c6c0b42aff9` (`general-code-implementer(gpt-5): harden accepted-knowledge judge prompt`), pushed to `main@origin`.

- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`

## Prompt And Training Changes

`KnowledgeJudgePrompt::system_prompt` now explicitly trains the judge to:

- accept stable, non-private, non-intent knowledge that matches the declared subject/domain;
- treat Mind accepted knowledge as separate from Spirit psyche intent;
- reject exact or semantic duplicates using `SemanticDuplicate(neighbor_identity)`;
- reject contradictions or conflicts using `ConflictsAcceptedKnowledge([neighbor_identity ...])`;
- reject imperatives, tasks, instructions, requests, logs, receipts, admission receipts, and process chatter as `NotKnowledge`;
- reject vague, unstable, time-sensitive, or no-stable-subject claims as `NeedsMoreSpecificShape`;
- reject subject/domain mismatch as `WrongSubject(expected_subject)`;
- keep deterministic code responsible for identity minting, storage, lookup, and verdict application.

`KnowledgeJudgePrompt::user_prompt` now states that relevant neighbors are accepted records with identities, and that those identities must be cited for duplicate/conflict rejections.

## Scenario Mapping Implemented

- Duplicate: fake agent returns `Reject(SemanticDuplicate(accepted_identity))`; Mind replies `Rejected(SemanticDuplicate(accepted_identity))`.
- Contradiction: fake agent returns `Reject(ConflictsAcceptedKnowledge([accepted_identity]))`; Mind replies `Rejected(ConflictsAcceptedKnowledge([accepted_identity]))`.
- Task/instruction non-knowledge: fake agent returns `Reject(NotKnowledge)`; Mind replies `Rejected(NotKnowledge)`.
- Vague/unstable/no stable subject: mapped to `NeedsMoreSpecificShape`; fake agent returns `Reject(NeedsMoreSpecificShape)` and Mind replies `Rejected(NeedsMoreSpecificShape)`.
- Subject/domain mismatch: fake agent returns `Reject(WrongSubject(Component))`; Mind replies `Rejected(WrongSubject(Component))`.

The new test also proves accepted neighbors render in the prompt with both the generated identity and accepted statement available to the model.

## Checks Run

- `cargo fmt` passed.
- `cargo test agent_knowledge_judge_prompt_and_verdicts_cover_first_rejection_batch --test actor_topology` passed: 1 passed.
- `cargo test knowledge --test actor_topology` passed: 5 passed.
- `nix build .#checks.x86_64-linux.test --no-write-lock-file` passed.
- `nix build .#checks.x86_64-linux.fmt --no-write-lock-file` passed.
- `nix build .#checks.x86_64-linux.clippy --no-write-lock-file` passed.

## Residuals And Follow-Up

No live AI smoke test was added. The current live provider path remains opt-in through daemon configuration and the local `agent` socket; default checks remain deterministic and do not make external provider calls.

