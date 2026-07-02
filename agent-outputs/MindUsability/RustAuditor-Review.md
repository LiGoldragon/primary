# Rust Auditor Review

Task: independent audit of Carver's completed Mind usability implementation across `signal-mind` and `mind`.

Scope:

- `signal-mind` commit `12c9e94edd1d42566bbda9806c8820ee75045c3d`
- `mind` commit `54142da6fe84de754f90f7b4d63f4be5d0831f37`
- Intended behavior: Mind stores accepted non-intent knowledge; Spirit remains for psyche intent; AI judges semantic acceptance; deterministic Rust owns typed structure, routing, verdict parsing/application, storage, and query; `Accept` carries no substitute accepted record; accepted submissions materialize the submitted `KnowledgeCandidate`; old substitute accepted-draft payloads and malformed verdicts store nothing.

Intent grounding:

- Spirit `PublicTextSearch [Mind knowledge Spirit intent accepted knowledge]` observed records `qjrf`, `gni3`, and `izsf`.
- Relevant conclusion: information/belief is not Spirit intent, and agent-authored material is not psyche-authorized intent. That supports the reviewed boundary: accepted knowledge belongs in Mind, while Spirit remains the psyche-intent layer.

Files consulted:

- `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-mind/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/schema_drift.rs`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/dispatch.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/domain.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/view.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/graph.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/kernel.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- `/git/github.com/LiGoldragon/nota-next/src/codec.rs`

## Findings

No defects found in the audited implementation.

The specific prior bug is addressed at the contract and application boundaries:

- `signal-mind/src/knowledge.rs:468` defines `KnowledgeJudgeVerdict` as `Accept` or `Reject(KnowledgeRejection)`, so `Accept` no longer carries replacement records.
- `signal-mind/schema/signal-mind.concept.schema:190` mirrors the same schema-first verdict shape: `KnowledgeJudgeVerdict [Accept (Reject KnowledgeRejection)]`.
- `mind/src/knowledge.rs:403` applies `KnowledgeJudgeVerdict::Accept` by calling `apply_acceptance()` over `self.candidate`; there is no path that reads an accepted draft payload from the judge.
- `mind/src/knowledge.rs:490` materializes the submitted `KnowledgeCandidate` into `AcceptedKnowledge`, and `mind/src/knowledge.rs:522` persists only those materialized records through `MindTables::assert_accepted_knowledge`.
- `mind/src/knowledge.rs:165` parses the AI completion as `KnowledgeJudgeVerdict`; malformed or old accepted-draft payloads become a `Reject(MeaningUnclear)` via `unavailable_verdict()` at `mind/src/knowledge.rs:174`.
- `nota-next/src/codec.rs:170` requires exactly one NOTA root before decode, so an AI reply with extra root records/prose around a verdict does not silently decode as a valid verdict.

The tested regression coverage is adequate for the requested audit:

- Submitted accepted knowledge is materialized from the submitted candidate: `mind/tests/actor_topology.rs:971` accepts a fake-agent strict `Accept` and verifies the returned record is the submitted statement body and identity, not a prompt example.
- The fixture storage path also queries persisted accepted knowledge after accepted submissions: `mind/tests/actor_topology.rs:645` exercises accepted domains, entities, statements, sources, relations, query by identifier, query by identity, domain queries, relation queries, semantic rejection, structural preflight rejection, and current/superseded views.
- Old substitute accepted-draft payloads reject and store nothing: `mind/tests/actor_topology.rs:1009` sends the old `(Accept ((...)))` shape, verifies `KnowledgeRejected(MeaningUnclear)`, and verifies zero stored `Statement` and zero stored `Domain` records.
- Malformed verdicts reject and store nothing: `mind/tests/actor_topology.rs:1055` sends `not a verdict`, verifies `KnowledgeRejected(MeaningUnclear)` with a malformed-verdict summary, and verifies zero stored `Domain` records.
- Prompt discipline is covered by `mind/tests/actor_topology.rs:996`, including a negative assertion that the generated AI prompt does not contain `domain:component`.
- Contract drift coverage exists in `signal-mind/tests/round_trip.rs:1466`, `signal-mind/tests/round_trip.rs:1502`, `signal-mind/tests/round_trip.rs:1660`, and `signal-mind/tests/schema_drift.rs:96`.

Architecture and discipline observations:

- The accepted-knowledge public contract uses typed records and typed identities rather than colon pseudo-identifiers in schema and round-trip witnesses.
- The Mind implementation keeps semantic judgment behind `KnowledgeJudge`, while deterministic code owns relation endpoint preflight, domain/range validation, verdict parsing, materialization, persistence, and query.
- The store boundary persists only `AcceptedKnowledge` through the registered `accepted_knowledge` Sema family in `mind/src/tables.rs:514` and `mind/src/tables.rs:921`.
- `mind/Cargo.toml:50` pins `signal-mind` to the audited contract commit `12c9e94edd1d42566bbda9806c8820ee75045c3d`.
- I did not find architecture drift that should block acceptance.

## Residual Risks

- A live AI smoke test is still recommended before declaring the configured agent path operational in production. The fake-agent tests prove the frame, prompt, parser, malformed-output rejection, and store behavior, but they do not prove the real configured model reliably emits strict single-root `KnowledgeJudgeVerdict` NOTA.
- The strict fake-agent accept test verifies the returned accepted record, while the broader fixture test verifies persisted query behavior. A future hardening test could query the exact accepted statement by identity after the fake-agent `Accept` to fuse those witnesses in one test, but the current implementation path persists before returning `KnowledgeAccepted`, so this is not a defect.
- Existing actor trace labels for knowledge write/query still reuse thought-oriented trace nodes in adjacent code (`THOUGHT_COMMIT`, `THOUGHT_QUERY`). This does not affect the reviewed behavior, but a future architecture-test pass could add knowledge-specific path witnesses if accepted-knowledge tracing becomes a public invariant.

## Checked Evidence

Repository state:

- `jj status` in `/git/github.com/LiGoldragon/signal-mind`: clean working copy; parent commit `12c9e94e` on `main`.
- `jj status` in `/git/github.com/LiGoldragon/mind`: clean working copy; parent commit `54142da6` on `main`.

Commands run:

- `/git/github.com/LiGoldragon/signal-mind`: `cargo test knowledge_ --tests`
  - Result: passed. Covered 8 accepted-knowledge round-trip tests plus `concept_schema_declares_accepted_knowledge_roots`.
- `/git/github.com/LiGoldragon/signal-mind`: `cargo test concept_schema_declares_accepted_knowledge_roots --test schema_drift`
  - Result: passed.
- `/git/github.com/LiGoldragon/signal-mind`: `cargo test knowledge_verdicts_and_replies_round_trip --test round_trip`
  - Result: passed.
- `/git/github.com/LiGoldragon/mind`: `cargo test agent_knowledge_judge_ --test actor_topology`
  - Result: passed. Covered strict accept, old substitute accept payload rejection, and malformed verdict rejection.
- `/git/github.com/LiGoldragon/mind`: `cargo test accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries --test actor_topology`
  - Result: passed.

One redundant attempted command, `cargo test concept_schema_declares_accepted_knowledge_roots knowledge_verdicts_and_replies_round_trip knowledge_submit_and_query_requests_round_trip --tests`, failed because Cargo accepts only one positional test filter. The covered tests were run through the valid commands above.
