# Mind Accepted-Knowledge Identity Correction Evidence

Task: correct the Mind-family accepted-knowledge usability surface after the psyche rejected caller-supplied identity choices. Scope was `signal-mind` and `mind`; Spirit record vocabulary was not changed.

## Consulted Surfaces

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/signal-mind/AGENTS.md`
- `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`
- Spirit identity mint reference: `/git/github.com/LiGoldragon/spirit/src/store/record_identifier.rs`

## Before Examples

Captured from the pre-change `signal-mind` canonical `to_nota()` encoder:

```nota
(SubmitKnowledge ((Entity (Keyed ((Component mind) Mind [[accepted knowledge substrate]] [Component]))) FixtureOnly ([[fixture accepted entity]])))
(QueryKnowledge (GetByIdentity (Component mind)))
(KnowledgeAccepted (([(Entity ((kn-component-mind (Keyed (Component mind)) operator 1790000000000000100) Mind [[accepted knowledge substrate]] [Component]))])))
(KnowledgeList ([(Entity ((kn-component-mind (Keyed (Component mind)) operator 1790000000000000100) Mind [[accepted knowledge substrate]] [Component]))] False))
(KnowledgeRejected (NotKnowledge ([not durable knowledge]) (Some ([submit a declarative statement]))))
```

## After Examples

Captured from the corrected `signal-mind` canonical `to_nota()` encoder:

```nota
(Submit (Component [Mind stores accepted knowledge.]))
(Get k9x8)
(Accepted (k9x8))
(Found ((k9x8 Component [Mind stores accepted knowledge.] operator 1790000000000000100)))
(NotFound (none))
(Rejected NotKnowledge)
```

## Changes

`signal-mind`:

- Replaced structured caller-supplied `KnowledgeIdentity`, `KnowledgeIdentitySlot`, `Keyed`, `Unkeyed`, `KnowledgeCandidate`, relation/domain/source candidate shapes, `GetByIdentity`, `KnowledgeAccepted`, `KnowledgeRejected`, and `KnowledgeList`.
- Added generated short `KnowledgeIdentity(String)`, `KnowledgeSubmission(subject, statement)`, flat `AcceptedKnowledge(identity, subject, statement, accepted_by, accepted_at)`, `KnowledgeJudgePacket(subject, statement, relevant_neighbors)`, `KnowledgeJudgeVerdict::Accept | Reject(KnowledgeRejectionReason)`, and replies `Accepted`, `Rejected`, `Found`, `NotFound`.
- Updated schema, architecture, and round-trip/schema-drift tests. Tests now reject old keyed/unkeyed/get-by-identity/substitute-accept text.

`mind`:

- Updated the pinned `signal-mind` dependency to commit `095925c84fe349962d821e900efecaa7ca3ea077`.
- Reworked accepted-knowledge admission to accept only subject and statement.
- Mind now mints identity after `KnowledgeJudgeVerdict::Accept`, persists the submitted subject/statement under that identity, and returns `Accepted(identity)`.
- `Get(identity)` reads the accepted-knowledge table and returns `Found(record)` or `NotFound(identity)`.
- Rejected semantic verdicts, malformed agent verdicts, and old substitute accept payloads return `Rejected(MeaningUnclear)` or the judge-provided rejection reason and do not populate `relevant_neighbors` for the next admission.
- Updated actor routing, storage keying, CLI text fallback handling, architecture, dependency lock, and actor topology tests.

## Identity Generation

Mind now mirrors Spirit's short identifier minting pattern: it collects existing accepted-knowledge identities, tries random base36 codes from 4 to 7 characters using `getrandom`, and falls back to the first unused code in that length range if random attempts collide. The identity is generated only inside Mind after acceptance; the submit request has no identity field and no keyed/unkeyed branch.

## Commits

- `/git/github.com/LiGoldragon/signal-mind`: `095925c84fe349962d821e900efecaa7ca3ea077` — `general-code-implementer(gpt-5): simplify Mind accepted knowledge contract`
- `/git/github.com/LiGoldragon/signal-mind`: `b8c5da96d8ead413287eb407cd7fda55919f5fd5` — `general-code-implementer(gpt-5): format accepted knowledge tests`
- `/git/github.com/LiGoldragon/mind`: `4b3b28c2f828198625e658bca496a3aeb7c31c51` — `general-code-implementer(gpt-5): mint Mind knowledge identities on accept`

All three commits were pushed; final source working copies were clean.

## Verification

- `cargo test` in `signal-mind`: passed, 70 tests/doc-tests total across the crate.
- `cargo test --test round_trip knowledge -- --nocapture` in `signal-mind`: passed, 4 focused knowledge tests.
- `cargo test --test round_trip old_keyed -- --nocapture` in `signal-mind`: passed, proving old keyed/unkeyed/get-by-identity/substitute verdict text no longer parses.
- `cargo check --lib` in `mind`: passed.
- `cargo test --test actor_topology accepted_knowledge -- --nocapture` in `mind`: passed.
- `cargo test --test actor_topology knowledge_judge -- --nocapture` in `mind`: passed.
- `cargo test --test actor_topology semantic_rejection -- --nocapture` in `mind`: passed.
- `cargo test` in `mind`: passed, all Rust unit, integration, and doc tests.
- `nix flake show --no-update-lock-file` in `mind`: passed, exposed `checks.x86_64-linux.default` and named check derivations.
- `nix flake check --no-update-lock-file` in `mind`: passed all x86_64-linux checks. Nix omitted incompatible systems `aarch64-darwin`, `aarch64-linux`, and `x86_64-darwin`.

## Follow-Up

- No blocker remains for this Mind-family correction.
- Future cross-component vocabulary cleanup may rename Spirit `Record` vocabulary, but this worker intentionally did not touch Spirit.
