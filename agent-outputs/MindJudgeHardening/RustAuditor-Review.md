# Rust Auditor Review

## Task And Scope

Independent audit of Tesla's Mind judge-hardening work in `/git/github.com/LiGoldragon/mind`, reported as commit `8c6c0b42aff9f7331ff8265ac925a79e9998361f` on `main@origin`.

Scope reviewed:

- judge prompt and training for accepted-knowledge admissions;
- deterministic fake-agent coverage for the first rejection batch;
- accepted-neighbor rendering for duplicate/conflict decisions;
- payload-free `Accept` and fail-closed malformed/substitute verdict behavior;
- schema/contract, NOTA parser/projection, storage/wire, and default-test provider boundaries.

Spirit query evidence: public text search for Mind accepted knowledge / Spirit intent returned records including `qjrf` and `gni3`, which distinguish psyche intent from information/belief and warn that agent-authored content is not psyche-authorized intent. I used that as audit grounding for the Mind-vs-Spirit boundary.

## Findings

No defects found.

The implementation matches the requested policy at the Rust and prompt-boundary level:

- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:234) makes the judge explicitly evaluate Mind accepted knowledge while saying "Mind accepts non-Spirit knowledge here; Spirit remains for psyche intent." This keeps Mind's accepted-knowledge store distinct from Spirit's intent authority instead of collapsing information into psyche intent.
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:247) trains the declared subject/domain rule and names the required rejection shapes for `WrongSubject(expected_subject)`, `SemanticDuplicate(neighbor_identity)`, `ConflictsAcceptedKnowledge([neighbor_identity ...])`, `NotKnowledge`, and `NeedsMoreSpecificShape`.
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:257) requires exactly one `KnowledgeJudgeVerdict` NOTA value, and the examples are generated from typed contract values rather than hand-written verdict strings.
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:156) parses verdicts through `NotaSource::parse::<KnowledgeJudgeVerdict>()`; I did not find custom NOTA parsing or keyword/regex semantic rejection in the implementation.
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:165) fails closed to `Reject(MeaningUnclear)` when the agent path is unavailable, rejects non-completed agent output, or returns malformed NOTA.
- [src/knowledge.rs](/git/github.com/LiGoldragon/mind/src/knowledge.rs:384) passes accepted records from storage into `KnowledgeJudgePacket.relevant_neighbors` before calling the judge, and acceptance still stores the submitted record exactly as supplied under a Mind-generated identity.

The tests cover the requested deterministic scenarios:

- [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:711) drives the real `AgentKnowledgeJudge` over a fake Unix-socket Signal agent, so the test exercises Signal framing, prompt construction, agent response decoding, typed NOTA verdict parsing, and the Mind actor/store reply path.
- [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:752) covers all five requested rejection classes: `NotKnowledge`, `NeedsMoreSpecificShape`, `WrongSubject(Component)`, `SemanticDuplicate(accepted_identity)`, and `ConflictsAcceptedKnowledge([accepted_identity])`.
- [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:793) checks that accepted-neighbor identity and statement text appear in subsequent prompts, which is the meaningful context needed for duplicate/conflict judgments.
- [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:813) checks for the prompt-training phrases that carry the requested policy.
- Existing focused tests at [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:636) and [tests/actor_topology.rs](/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:675) verify old substitute `Accept` payloads and malformed verdicts fail closed and do not store records.

Schema/contract review found no regression in this commit:

- `jj show --summary -r 8c6c0b42aff9` reports only `src/knowledge.rs` and `tests/actor_topology.rs` changed.
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs` still defines `KnowledgeJudgeVerdict::Accept` as payload-free and `Reject(KnowledgeRejectionReason)` as the typed reject form.
- Default daemon configuration remains `MindKnowledgeJudgeConfiguration::Fixture`, and live agent use remains opt-in through `MindKnowledgeJudgeConfiguration::Agent`.

## Residual Risks

The tests are not live semantic evals. They prove the prompt contains the requested training, accepted neighbors are available, verdict parsing is typed, and Mind applies the judge's typed verdicts correctly. They do not prove a live model will classify the five scenario statements correctly under realistic temperature/model/provider conditions.

The fake agent returns predetermined verdicts in the same order as the test scenarios. That is appropriate for deterministic Rust boundary coverage, but richer evals or a live AI smoke test are still needed before treating prompt quality as empirically validated.

The Rust boundary currently trusts any well-formed `Reject` payload from the judge. For example, a valid `SemanticDuplicate` identity not present in `relevant_neighbors` would be surfaced as the judge's reason rather than fail-closed. I am not classifying that as a defect because the brief kept semantic rejection at the AI/prompt level and only required fail-closed behavior for malformed/substitute verdicts, but it is a useful future hardening point if Mind wants deterministic validation of cited neighbor identities.

## Evidence Checked

Files and surfaces consulted:

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/MindJudgeHardening/GeneralCodeImplementer-Evidence.md`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- `/git/github.com/LiGoldragon/mind/src/configuration.rs`
- `/git/github.com/LiGoldragon/mind/src/daemon.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`

Commands run:

- `spirit "(PublicTextSearch [Mind accepted knowledge Spirit intent judge prompt])"`: returned relevant public intent records including `qjrf` and `gni3`; no blocker.
- `orchestrate "(Observe Roles)"`: no conflicting claim on the Mind checkout.
- `jj status`: clean working copy; parent commit is reported `8c6c0b42` on `main`.
- `jj show --summary -r 8c6c0b42aff9`: only `src/knowledge.rs` and `tests/actor_topology.rs` changed.
- `jj show --stat -r 8c6c0b42aff9`: 2 files changed, 221 insertions, 13 deletions.
- `jj diff -r 8c6c0b42aff9 -- src/knowledge.rs tests/actor_topology.rs`: prompt/test-only Rust changes inspected.
- `rg -n "regex|contains\\(|split\\(|starts_with\\(|ends_with\\(|NotKnowledge|WrongSubject|SemanticDuplicate|ConflictsAcceptedKnowledge" src/knowledge.rs src tests/actor_topology.rs`: no Rust regex/keyword semantic rejection found in `src/knowledge.rs`; test `contains` checks are prompt witnesses.
- `cargo fmt --check`: passed.
- `cargo test agent_knowledge_judge_prompt_and_verdicts_cover_first_rejection_batch --test actor_topology`: passed, 1 test.
- `cargo test knowledge --test actor_topology`: passed, 5 tests.

I did not rerun the full Nix check set from Tesla's evidence because the audit only needed focused confirmation after inspecting the changed files and the reported full-check evidence.

