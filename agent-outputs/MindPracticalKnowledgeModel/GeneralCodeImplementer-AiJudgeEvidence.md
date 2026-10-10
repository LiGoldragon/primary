# Mind AI-Backed Knowledge Judge Evidence

## Task And Scope

Implemented a real AI-backed `KnowledgeJudge` path for Mind accepted-knowledge v1 in `/git/github.com/LiGoldragon/mind`.

The implementation keeps the existing deterministic fixture judge for tests and safe default daemon behavior. It does not edit `/git/github.com/LiGoldragon/signal-mind` or Spirit. No commit or push was performed.

## Context Consulted

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/IntentTranslator-ImplementationBrief.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-MindEvidence.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-Validation.md`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/agent/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/agent/src/client.rs`
- `/git/github.com/LiGoldragon/agent/src/config.rs`
- `/git/github.com/LiGoldragon/agent/tests/fixture_round_trip.rs`
- `/git/github.com/LiGoldragon/spirit/src/guardian.rs`
- `/git/github.com/LiGoldragon/spirit/src/guardian_prompt.rs`
- `/git/github.com/LiGoldragon/signal-agent/src/lib.rs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`

`/home/li/primary/lore/AGENTS.md` was requested by the repo instructions but was absent.

## Coordination

- Observed Orchestrate roles.
- Claimed `(Path /git/github.com/LiGoldragon/mind)` as `GeneralCodeImplementer`.
- Did not revert or normalize the existing uncommitted accepted-knowledge work from earlier workers.

## Changed Files For This Task

- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind/Cargo.lock`
- `/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs`
- `/git/github.com/LiGoldragon/mind/src/configuration.rs`
- `/git/github.com/LiGoldragon/mind/src/daemon.rs`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/lib.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`

The working copy also still shows pre-existing uncommitted changes from the prior Mind accepted-knowledge implementation in actor/store/text/table files.

## Implementation Summary

Added `AgentKnowledgeJudge`, which implements `KnowledgeJudge` by calling the existing local `agent` daemon over `signal-agent::Input::Call`. This reuses the same model-call path Spirit Guardian uses: Unix socket, length-prefixed Signal frame, `signal_agent::Prompt`, and strict parse of one model completion.

The prompt is built from `KnowledgeJudgePacket` and asks for exactly one `KnowledgeJudgeVerdict` NOTA value. It makes Mind's rules explicit:

- accept only knowledge that belongs in Mind;
- reject tasks, logs, receipts, private/unauthorized material, vague prose, unsupported or false content, wrong-domain content, duplicates, conflicts, and bad supersessions;
- do not require source/provenance unless the candidate itself makes source part of the knowledge;
- return only typed NOTA grammar parseable as `KnowledgeJudgeVerdict`.

Malformed model output, socket failure, frame failure, or non-completed agent output fails closed to `KnowledgeJudgeVerdict::Reject` with `KnowledgeRejectionReason::MeaningUnclear`; no accepted draft is applied and no accepted knowledge is stored.

The daemon configuration now has a judge selector:

- `MindKnowledgeJudgeConfiguration::Fixture` is the default and preserves safe fixture/default behavior.
- `MindKnowledgeJudgeConfiguration::Agent(MindKnowledgeJudgeAgentConfiguration)` explicitly enables the AI judge.

The `mind-write-configuration` helper remains backward-compatible with the old four-path request and accepts an optional `(AgentKnowledgeJudge <agent-socket> <provider> <model> <timeout-ms> <max-output-tokens>)` field.

The crate version was bumped to `0.7.2` because the daemon startup configuration surface changed.

## Model Call Path And Model Name

Reused path: `mind-daemon` -> `AgentKnowledgeJudge` -> `signal-agent::Input::Call(Prompt)` -> local `agent-daemon` -> configured OpenAI-compatible provider.

No direct DeepSeek HTTP client was added to Mind.

Exact DeepSeek Flash selection used for tests/demo:

- provider: `deepseek`
- endpoint owned by `agent-daemon` provider seed: `https://api.deepseek.com/v1`
- model: `deepseek-v4-flash`
- secret source owned by `agent-daemon`: `Gopass platform.deepseek.com/api-key`

Mind's `MindKnowledgeJudgeAgentConfiguration::deepseek_flash` helper uses provider `deepseek`, model `deepseek-v4-flash`, timeout `180000` ms, and maximum output tokens `2048`.

## Tests Added

Added actor-boundary tests in `tests/actor_topology.rs`:

- `agent_knowledge_judge_accepts_strict_verdict_and_prompts_with_packet`
- `agent_knowledge_judge_malformed_verdict_rejects_and_stores_nothing`

These use a fake `signal-agent` socket, verify the prompt uses provider `deepseek`, model `deepseek-v4-flash`, and max output tokens `2048`, then prove strict verdict acceptance and malformed-output fail-closed behavior through the real Mind actor/store path.

The existing fixture vertical slice still passes.

## Checks Run

- `cargo fmt` - passed.
- `cargo test --test actor_topology accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries -- --exact` - passed.
- `cargo test --test actor_topology agent_knowledge_judge` - passed, 2 tests.
- `cargo check` - passed.
- `mind-write-configuration` old fixture request - passed; wrote a temp configuration.
- `mind-write-configuration` new `(AgentKnowledgeJudge ... deepseek deepseek-v4-flash 180000 2048)` request - passed; wrote a temp configuration.
- `cargo test` - passed. Covered 12 lib tests, 37 actor topology tests, 6 CLI tests, 13 daemon-wire tests, 7 memory tests, 3 orchestrate-caller tests, 17 weird actor truth tests, and doc tests.
- `cargo clippy --all-targets -- -D warnings` - passed.

## Live AI Probe

The DeepSeek gopass key handle was available, so I ran a temp live probe:

1. Started `agent-daemon` with `live-provider` and provider seed `(deepseek https://api.deepseek.com/v1 deepseek-v4-flash (Gopass platform.deepseek.com/api-key))`.
2. Started `mind-daemon` with `AgentKnowledgeJudge` targeting that agent socket.
3. Submitted one CLI request:
   `(SubmitKnowledge ((Domain (domain:component Component None)) FixtureOnly (None)))`
4. Queried:
   `(QueryKnowledge (ListByKind (Domain IncludeSuperseded)))`

Result: passed. The submit returned `KnowledgeAccepted` for `domain:component`, and the query returned the persisted `KnowledgeDomain`.

## Nix Check

- `nix build .#checks.x86_64-linux.test --no-link --no-update-lock-file` - failed.

Failure reason is still the known local dependency portability blocker: the Nix sandbox cannot load the uncommitted local path patch for `signal-mind` and tries to read `/build/signal-mind/Cargo.toml`, which does not exist. This is separate from the AI judge implementation; Cargo checks and tests pass locally with the existing path patch.

## Follow-Up

Publish or otherwise remote-address the `signal-mind 0.5.1` contract changes and replace the local `../signal-mind` path patch before expecting Nix checks to pass.
