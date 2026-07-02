# Mind Judge Hardening Situational Map

## Task And Scope

Scout task for the approved Mind judge-hardening lane in `/home/li/primary`: inspect Mind's current AI judge surface, verdict schema, deterministic hooks, live-smoke affordances, and likely implementation edit scope. Read-only source inspection only; no tests with real models were run and no source files were edited.

The prompt context says Mind accepts non-Spirit knowledge, Spirit remains for psyche intent, and the Mind term should be `judge`, not `guardian`. Local source already mostly follows `judge`; remaining `guardian` mentions found in this scout are in Spirit/agent context or historical reports, not Mind's current accepted-knowledge type names.

## Commands And Files Consulted

- `spirit "(PublicTextSearch [Mind judge knowledge])"` from `/home/li/primary`: returned `(Error [no matching record])`; used as negative evidence only.
- `/home/li/primary/AGENTS.md` from the supplied task context.
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/protocols/active-repositories.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/configuration.rs`
- `/git/github.com/LiGoldragon/mind/src/daemon.rs`
- `/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/dispatch.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/kernel.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- `/git/github.com/LiGoldragon/mind/scripts/*`
- `/git/github.com/LiGoldragon/mind/flake.nix`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/agent/README.md`
- `/git/github.com/LiGoldragon/agent/src/bin/agent_write_configuration.rs`
- `/git/github.com/LiGoldragon/agent/tests/fixture_round_trip.rs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`
- Process/socket checks: `jj status` in Mind, `pgrep -af 'mind-daemon|agent-daemon'`, `ls -l /home/li/.local/state/agent/agent.sock ...`, and scoped `rg` searches. No `/nix/store` filesystem search was performed.

## Observed Facts

Mind and Signal contract location:

- Active repo inventory names `mind` at `/git/github.com/LiGoldragon/mind` and `signal-mind` at `/git/github.com/LiGoldragon/signal-mind` in `/home/li/primary/protocols/active-repositories.md`.
- Mind working copy was clean by `jj status`: working copy `krluququ cb6a3a63 (empty)`, parent `nywqxqvl 290a6328 main | general-code-implementer(gpt-5): consume simplified knowledge replies`.
- `/git/github.com/LiGoldragon/mind/AGENTS.md:1-9` asks agents to read `/home/li/primary/lore/AGENTS.md`; `test -e /home/li/primary/lore/AGENTS.md` returned nonzero, so that referenced file is absent in this workspace.

Accepted-knowledge public surface:

- `signal-mind` schema declares the current simplified accepted-knowledge contract at `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema:151-164`: `KnowledgeSubmission (KnowledgeSubject TextBody)`, `KnowledgeJudgePacket (KnowledgeSubject TextBody (Vec AcceptedKnowledge))`, `KnowledgeJudgeVerdict [Accept (Reject KnowledgeRejectionReason)]`, and rejection reasons.
- `signal-mind` request/reply enum includes `Submit(KnowledgeSubmission)`, `Get(KnowledgeIdentity)`, `Accepted(KnowledgeIdentity)`, `Rejected(KnowledgeRejectionReason)`, `Found(KnowledgeRecord)`, and `NotFound` at `/git/github.com/LiGoldragon/signal-mind/src/lib.rs:1275-1308`.
- `signal-mind` current round-trip tests assert examples matching the brief: `(Accepted k9x8)`, `(Found (k9x8 Component [Mind stores accepted knowledge.]))`, and `NotFound` at `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs:1388-1405`.
- Old accepted-knowledge surfaces are explicitly rejected by parse tests at `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs:1420-1440`.

Judge prompt and call path:

- The judge abstraction is `KnowledgeJudge` with `fn judge(&self, packet: KnowledgeJudgePacket) -> KnowledgeJudgeVerdict` in `/git/github.com/LiGoldragon/mind/src/knowledge.rs:28-32`.
- Deterministic fixture implementation is `FixtureKnowledgeJudge` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:34-76`; it returns queued verdicts and defaults to `Reject(MeaningUnclear)` when empty.
- Live AI implementation is `AgentKnowledgeJudge` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:79-192`; it sends `signal_agent::Input::Call(Prompt)` over a Unix socket and parses one completion as `KnowledgeJudgeVerdict`.
- Prompt assembly is in `KnowledgeJudgePrompt` methods at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:211-286`.
- Current system prompt text is built by `KnowledgeJudgePrompt::system_prompt` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:234-254`. It tells the model it is "Mind's accepted-knowledge judge", assigns semantic judgment for knowledge/truth/domain/private/duplicate/conflict/source, says deterministic code handles identity/storage/lookup, rejects tasks/logs/receipts/vague/wrong-subject/duplicates/conflicts, and requires exactly one `KnowledgeJudgeVerdict` NOTA value.
- Current user prompt is built by `KnowledgeJudgePrompt::user_prompt` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:256-264`; it includes the `KnowledgeJudgePacket` and says relevant neighbors are the only accepted records usable for duplicate/conflict decisions.
- Prompt options set temperature 0, `OutputMode::Nota`, low reasoning effort, and disabled thinking at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:266-277`.
- Failure to connect, frame, parse, or receive a completed output fails closed to `Reject(MeaningUnclear)` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:165-190`.

Admission and persistence:

- `AcceptedKnowledgeLedger::submit` handles only `MindRequest::Submit`, builds a judge packet, applies accept/reject, and `query` handles only `MindRequest::Get` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:299-320`.
- `KnowledgeAdmission::reply_from_judge` includes `subject`, `statement`, and all current accepted records as `relevant_neighbors`, then maps `Accept` to `apply_acceptance` and `Reject(reason)` to `MindReply::Rejected(reason)` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:344-354`.
- `KnowledgeAcceptanceApplication::accepted` mints the `KnowledgeIdentity` after accept, records actor and timestamp internally, stores `AcceptedKnowledge`, and returns only `Accepted(identity)` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:386-405`.
- `KnowledgeQueryEngine::reply` returns `Found(public_record)` or bare `NotFound` at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:516-532`.
- Storage table is `accepted_knowledge` at `/git/github.com/LiGoldragon/mind/src/tables.rs:45-56`; `StoredAcceptedKnowledge` wraps `AcceptedKnowledge` at `/git/github.com/LiGoldragon/mind/src/tables.rs:108-110`.
- Accepted rows are asserted and read through `assert_accepted_knowledge` and `accepted_knowledge_records` at `/git/github.com/LiGoldragon/mind/src/tables.rs:915-934`.
- Architecture confirms deterministic code owns identity minting, verdict application, persistence, and `Get`, while duplicate/contradiction/truth/source are not keyword/regex rules at `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md:659-663`.

Daemon configuration:

- `MindDaemonConfiguration` carries `knowledge_judge: MindKnowledgeJudgeConfiguration` at `/git/github.com/LiGoldragon/mind/src/configuration.rs:19-25`.
- `MindKnowledgeJudgeConfiguration` variants are exactly `Fixture` and `Agent(MindKnowledgeJudgeAgentConfiguration)` at `/git/github.com/LiGoldragon/mind/src/configuration.rs:93-106`.
- `MindKnowledgeJudgeAgentConfiguration::deepseek_flash` names provider `deepseek`, model `deepseek-v4-flash`, timeout `180000`, and max output tokens `2048` at `/git/github.com/LiGoldragon/mind/src/configuration.rs:108-138`.
- `MindProcessDaemon::build_runtime` selects `FixtureKnowledgeJudge::empty()` or `AgentKnowledgeJudge::new(configuration.clone())` at `/git/github.com/LiGoldragon/mind/src/daemon.rs:150-163`.
- `mind-write-configuration` accepts an optional fifth/sixth logical object for `(AgentKnowledgeJudge <agent-socket> <provider> <model> <timeout-ms> <max-output-tokens>)` at `/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs:146-182` and `/git/github.com/LiGoldragon/mind/src/bin/mind_write_configuration.rs:209-257`.

## Verdict Schema And Rejection Coverage

Exact schema/type names:

- `KnowledgeJudgePacket` fields: `subject: KnowledgeSubject`, `statement: TextBody`, `relevant_neighbors: Vec<AcceptedKnowledge>` at `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs:100-107`.
- `KnowledgeJudgeVerdict` variants: `Accept`, `Reject(KnowledgeRejectionReason)` at `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs:109-115`.
- `KnowledgeRejectionReason` variants at `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs:117-130`: `NotKnowledge`, `PrivateOrUnauthorized`, `MeaningUnclear`, `FalseOrUnsupported`, `SemanticDuplicate(KnowledgeIdentity)`, `ConflictsAcceptedKnowledge(Vec<KnowledgeIdentity>)`, `WrongSubject(KnowledgeSubject)`, `NeedsMoreSpecificShape`, `SourceRequired`, `PersistenceRejected`.

Coverage against the approved first rejection batch:

- Duplicates: expressible as `SemanticDuplicate(KnowledgeIdentity)`.
- Contradictions to accepted knowledge: expressible as `ConflictsAcceptedKnowledge(Vec<KnowledgeIdentity>)`.
- Non-knowledge task/instruction submissions: expressible as `NotKnowledge`.
- Vague/unstable claims with no stable subject: expressible, but not exactly named. Best current fit is `MeaningUnclear` or `NeedsMoreSpecificShape`; prompt says "vague prose" but not "unstable claim/no stable subject" explicitly.
- Submissions that do not agree with subject/domain: expressible, but not exactly named as domain mismatch. Best current fit is `WrongSubject(KnowledgeSubject)`. `FalseOrUnsupported` may overlap when the statement is unsupported rather than wrong-subject.

Interpretation: the current schema is sufficient for the first batch without contract changes unless the implementation worker wants more precise audit labels for `VagueOrUnstable` and `DomainMismatch`. Adding reason variants would be a `signal-mind` wire-contract change; prompt/tests can likely cover this batch with existing variants.

## Deterministic Tests And Mocks

Existing deterministic hooks:

- `FixtureKnowledgeJudge::new(vec![...])` provides queued verdicts and call counting at `/git/github.com/LiGoldragon/mind/src/knowledge.rs:34-76`.
- `ActorFixture::with_knowledge_judge` starts `MindRoot` with an injected `KnowledgeJudgePort` at `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:196-207`.
- `FakeKnowledgeAgent` is a local fake `signal-agent` socket that captures prompts and returns configured completion text at `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:290-399`. It verifies provider/model/max-token prompt options at lines 333-354.

Existing behavior tests:

- `accepted_knowledge_submit_mints_identity_and_get_finds_record` proves queued accept stores submitted subject/statement, mints a short base36 identity, `Get` returns the record, and missing identity returns `NotFound`: `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:468-511`.
- `semantic_rejection_stores_nothing_before_next_judgment` proves a semantic `Reject(NotKnowledge)` stores nothing and does not appear in the next prompt's neighbor list: `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:513-557`.
- `agent_knowledge_judge_accepts_strict_verdict_and_prompts_with_packet` proves the fake agent path accepts strict verdict text and the prompt includes key instruction phrases: `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:559-589`.
- `agent_knowledge_judge_old_substitute_accept_payload_rejects_and_stores_nothing` proves old payload-bearing accept text is malformed under the current schema and stores nothing: `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:591-628`.
- `agent_knowledge_judge_malformed_verdict_rejects_and_stores_nothing` proves arbitrary malformed output rejects as `MeaningUnclear` and stores nothing: `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs:630-660`.
- `signal-mind` contract tests cover request/reply/verdict round trips and old-surface rejection at `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs:1352-1440`.

Gaps in deterministic scenario coverage:

- No current test asserts `SemanticDuplicate`, `ConflictsAcceptedKnowledge`, `WrongSubject`, `NeedsMoreSpecificShape`, `FalseOrUnsupported`, `PrivateOrUnauthorized`, or `SourceRequired` handling through Mind's actor/store path. Search evidence: scoped `rg` found only `NotKnowledge` and `MeaningUnclear` in Mind tests.
- No current test feeds an accepted neighbor and verifies the prompt contains that neighbor in a way useful for duplicate/contradiction judgment, beyond checking rejected submissions are absent from neighbors.
- No current table-driven scenario set exists for the approved rejection batch.

## Live Smoke Path

Current local runtime state:

- `pgrep -af 'mind-daemon|agent-daemon'` found a running `agent-daemon` process.
- `/home/li/.local/state/agent/agent.sock` and `/home/li/.local/state/agent/agent-meta.sock` exist.
- `/home/li/.local/state/mind/mind.sock`, `/home/li/.local/state/mind/meta-mind.sock`, `/tmp/mind.sock`, `/tmp/meta-mind.sock`, `/tmp/agent.sock`, and `/tmp/meta-agent.sock` were absent during scouting.

Existing code/scripts:

- Mind has process smoke scripts in `/git/github.com/LiGoldragon/mind/scripts/`, but they use default fixture configuration. Example: `/git/github.com/LiGoldragon/mind/scripts/mind-store-survives-process-restart:16-19` writes `(ConfigurationWriteRequest $socket $meta_socket $store $configuration)` with no `AgentKnowledgeJudge`.
- Mind flake checks wire these scripts through `mindConstraintCheck` at `/git/github.com/LiGoldragon/mind/flake.nix:54-66` and list the script checks at `/git/github.com/LiGoldragon/mind/flake.nix:491-495`.
- No Mind-owned script was found that starts `agent-daemon`, writes Mind `AgentKnowledgeJudge` configuration, starts `mind-daemon`, and submits live accepted-knowledge cases.
- The `agent` repo has a gated real-network test `live_deepseek_flash_returns_valid_nota_with_gopass_key` at `/git/github.com/LiGoldragon/agent/tests/fixture_round_trip.rs:244-280`; it skips when the gopass key is unavailable and requires `--features live-provider`.
- `/git/github.com/LiGoldragon/agent/README.md:19-20` states live provider calls are behind `--features live-provider`.
- CriomOS-home's Spirit profile configures a user `agent-daemon` with provider `deepseek`, endpoint `https://api.deepseek.com/v1`, default model `deepseek-v4-flash`, and gopass handle `platform.deepseek.com/api-key` at `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:22-49`, then starts `agent-daemon` as a user service at lines 154-170.

How to exercise manually, not run by this scout:

1. Use the existing deployed agent socket `/home/li/.local/state/agent/agent.sock`, or start a temp `agent-daemon` from `/git/github.com/LiGoldragon/agent` using `agent-write-configuration` with a `ProviderSeed`.
2. In `/git/github.com/LiGoldragon/mind`, write a Mind config with:
   ```text
   (ConfigurationWriteRequest /tmp/<lane>/mind.sock /tmp/<lane>/mind-meta.sock /tmp/<lane>/mind.sema /tmp/<lane>/mind.config.rkyv (AgentKnowledgeJudge /home/li/.local/state/agent/agent.sock deepseek deepseek-v4-flash 180000 2048))
   ```
3. Start `mind-daemon <config>`, set `MIND_SOCKET`, and submit simplified examples such as:
   ```text
   (Submit (Component [Mind stores accepted knowledge.]))
   (Get <accepted-id>)
   ```

This is an external/model path, so it should remain opt-in and not part of ordinary deterministic checks.

## Likely Implementation Edit Scope

Primary Mind files:

- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`: strengthen `KnowledgeJudgePrompt::system_prompt` and `user_prompt`; possibly add scenario rendering helpers if prompt grows beyond inline strings; keep `AgentKnowledgeJudge` strict parse/fail-closed behavior.
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`: add deterministic scenario tests using `FakeKnowledgeAgent` and `FixtureKnowledgeJudge` for the first rejection batch, accepted-neighbor context, and prompt wording.
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`: update only if the prompt/training contract or scenario policy changes materially.

Likely contract files only if exact new reason names are required:

- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/schema_drift.rs`

Live smoke support, optional:

- `/git/github.com/LiGoldragon/mind/scripts/` and `/git/github.com/LiGoldragon/mind/flake.nix` if adding an opt-in smoke script. Do not make real model calls part of default `nix flake check`.

## Architecture Constraints, Risks, And Gaps

- Mind's architecture explicitly assigns semantic duplicate/contradiction/truth/source judgment to the judge, not Rust keyword rules: `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md:659-663`. The implementation worker should harden prompts and deterministic verdict plumbing, not implement semantic rejection by regex.
- The current simplified verdict `Accept` has no payload, which removes the old live-model failure where a model could copy an example accepted draft into storage. The remaining correctness risk is under-trained judgment: accepting bad knowledge or choosing coarse/wrong rejection reasons.
- The prompt currently says "vague prose" and "wrong-subject content" but does not explicitly teach the first approved batch in those words: duplicates, contradictions, task/instruction submissions, vague/unstable claims with no stable subject, and subject/domain mismatch.
- The judge packet gives all accepted records as `relevant_neighbors` through `accepted_knowledge_records().unwrap_or_default()` in `/git/github.com/LiGoldragon/mind/src/knowledge.rs:345-349`. That is acceptable for small stores but is a scaling/context-risk if the accepted corpus grows; there is no retrieval narrowing yet.
- `KnowledgeSubject` is a small enum: `Component`, `Contract`, `Repository`, `Architecture`, `Interface`, `Storage`, `Source` at `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs:43-51`. Domain mismatch scenarios must fit that enum unless the contract expands.
- `PrivateOrUnauthorized` exists but Mind has no deterministic privacy authority model for knowledge submissions in the inspected path; the judge prompt is the only guard in current accepted-knowledge admission.
- Mind process scripts currently exercise daemon/CLI storage but not `AgentKnowledgeJudge`; implementation should add deterministic tests first, and only add opt-in live smoke if useful.
- The repo entry instruction points to missing `/home/li/primary/lore/AGENTS.md`; this is a fresh-agent usability issue but not a judge-hardening blocker.

## Recommended Implementation Scope

Use the existing `KnowledgeRejectionReason` enum for the first hardening pass. Strengthen only Mind's judge prompt and add deterministic, table-shaped tests in `tests/actor_topology.rs` that cover:

- exact duplicate of an accepted neighbor -> `Reject(SemanticDuplicate(id))`;
- contradiction against an accepted neighbor -> `Reject(ConflictsAcceptedKnowledge(vec![id]))`;
- imperative task/instruction -> `Reject(NotKnowledge)`;
- vague/unstable/no stable subject -> `Reject(NeedsMoreSpecificShape)` or `Reject(MeaningUnclear)`, with the chosen mapping stated in test names;
- subject/domain mismatch -> `Reject(WrongSubject(expected_subject))`;
- useful positive controls for each `KnowledgeSubject` the scenario set relies on.

Keep the AI output contract as exactly one `KnowledgeJudgeVerdict` and keep accept payload-free. Add an opt-in live smoke script only after deterministic prompt/scenario tests land, and keep it outside default checks because it depends on a running `agent-daemon`, provider configuration, network, and gopass-backed secret availability.

## Not Checked

- I did not run `cargo test`, `nix flake check`, or live DeepSeek/model calls.
- I did not inspect generated schema emitter internals outside Mind's emitted/handwritten surfaces.
- I did not inspect `meta-signal-mind`; the accepted-knowledge judge path is on ordinary `signal-mind` plus Mind.
- I did not inspect any `/nix/store` paths.
