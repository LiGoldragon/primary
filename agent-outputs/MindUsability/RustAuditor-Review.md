# Rust Auditor Review

Task: independent audit of Carson's Mind-family accepted-knowledge identity
correction.

Scope:

- `signal-mind` commit `095925c84fe349962d821e900efecaa7ca3ea077`
  plus follow-up `b8c5da96d8ead413287eb407cd7fda55919f5fd5`.
- `mind` commit `4b3b28c2f828198625e658bca496a3aeb7c31c51`.
- `primary` evidence commit `3e517695c1f88e0bc0460019bef8bed6c60e843f`,
  report `agent-outputs/MindUsability/GeneralCodeImplementer-Evidence.md`.
- Intended correction: remove caller-supplied accepted-knowledge identity from
  submit/write paths; remove user-facing `Keyed`, `Unkeyed`, `Candidate`, and
  `GetByIdentity`; mint a short Mind identity only after acceptance; return the
  identity in `Accepted`; allow `Get(identity)` to retrieve the record; store
  nothing for rejected or malformed verdicts; keep the change in the Mind family
  and avoid custom NOTA parsing/projection as the solution.

Intent grounding:

- Spirit query: `PublicTextSearch [Mind accepted knowledge identity]`.
- Result: `(Error [no matching record])`, treated as negative evidence rather
  than a tool failure. This audit uses the supplied correction brief as the
  authority.

## Findings

No defects found in the audited implementation.

The public `signal-mind` contract removes caller-supplied identity from the
write path. `signal-mind/src/knowledge.rs:56` defines
`KnowledgeSubmission` as only `subject` and `statement`, and
`signal-mind/src/lib.rs:1275` wires public `Submit(KnowledgeSubmission)`.
`KnowledgeIdentity` remains a typed value in `signal-mind/src/knowledge.rs:18`,
but the only public request root using it is `Get(KnowledgeIdentity)` at
`signal-mind/src/lib.rs:1276`.

The old user-facing surfaces are gone from the live public schema and source.
`signal-mind/schema/signal-mind.concept.schema:37` declares
`(Submit KnowledgeSubmission)` and `:38` declares `(Get KnowledgeIdentity)`.
The accepted-knowledge schema records at `:157-166` contain
`KnowledgeIdentity`, `KnowledgeSubmission`, `AcceptedKnowledge`,
`KnowledgeJudgePacket`, `KnowledgeJudgeVerdict`, `KnowledgeAccepted`,
`KnowledgeFound`, `KnowledgeNotFound`, and `KnowledgeRejectionReason`; they do
not retain `Keyed`, `Unkeyed`, `KnowledgeCandidate`,
`KnowledgeIdentitySlot`, or `GetByIdentity`. A source/schema search found no
`Candidate` token in the live `signal-mind` source/schema or `mind` source.
The remaining `SubmitKnowledge` and `QueryKnowledge` names are internal actor
message types in `mind`, not the public contract.

Mind mints identity only after acceptance. The runtime submit branch accepts
only `MindRequest::Submit(submission)` at `mind/src/knowledge.rs:300-307`.
It builds a judge packet from the submitted subject and statement at
`mind/src/knowledge.rs:345-350`. Only `KnowledgeJudgeVerdict::Accept` reaches
`apply_acceptance()` at `mind/src/knowledge.rs:352-354`. Acceptance then reads
existing records, generates a short base36 identity, builds
`AcceptedKnowledge`, persists it, and returns `MindReply::Accepted` with that
identity at `mind/src/knowledge.rs:387-406` and `:358-367`.

`Get` retrieves by minted identity. The query branch handles only
`MindRequest::Get(identity)` at `mind/src/knowledge.rs:312-318`, and
`KnowledgeQueryEngine::reply` returns `Found(record)` or `NotFound(identity)` at
`mind/src/knowledge.rs:526-532`. Storage keys are the accepted record identity:
`StoredAcceptedKnowledge` implements `EngineRecord` with
`RecordKey::new(self.identifier().as_str())` at `mind/src/tables.rs:434-437`,
and accepted records are inserted/read through the accepted-knowledge table at
`mind/src/tables.rs:916-934`.

Rejected and malformed verdicts store nothing. Semantic rejection returns
`MindReply::Rejected(reason)` directly at `mind/src/knowledge.rs:352-355`, before
any acceptance application. Agent output is parsed with the canonical
`NotaSource::parse::<KnowledgeJudgeVerdict>()` path at
`mind/src/knowledge.rs:160-163`; malformed output maps to
`Reject(MeaningUnclear)` at `mind/src/knowledge.rs:166-190`. The tests cover
semantic rejection leaving no relevant neighbor before the next admission at
`mind/tests/actor_topology.rs:515-558`, old substitute accept payload rejection
at `:593-629`, and malformed verdict rejection at `:632-665`.

The CLI does not reintroduce a second accepted-knowledge command language.
`mind/src/command.rs:159-167` first tries the existing work-graph
`MindTextRequest`, then falls through to canonical
`NotaSource::parse::<MindRequest>()` for full contract requests. Replies follow
the same pattern: `mind/src/command.rs:113-118` prints
`CommandReply::to_nota()`, whose fallback prints the full contract `MindReply`
with canonical `to_nota()` when no work-graph text projection exists.

No custom accepted-knowledge NOTA parser/projection was added as the solution.
The accepted-knowledge contract types derive `NotaEncode`/`NotaDecode` in
`signal-mind/src/knowledge.rs:30-120`, judge completions parse through
`NotaSource`, and the CLI fallback parses and prints the contract types.

Architecture and test adequacy are sufficient for this correction. Contract
round-trip tests cover `Submit`, `Get`, `Accepted`, `Found`, `NotFound`,
`Rejected`, and verdict parsing at
`signal-mind/tests/round_trip.rs:1394-1424`. The negative old-surface test at
`signal-mind/tests/round_trip.rs:1427-1446` proves old keyed/unkeyed/get-by-
identity and old substitute-accept text no longer parse. The actor topology
test at `mind/tests/actor_topology.rs:470-513` proves submit mints a short
base36 identity, returns it, and `Get` finds the stored record.

## Residual Risks

- The identity mint has no deterministic collision-injection unit test for the
  fallback path after random attempts. The main behavior is covered by actor
  tests and the code checks existing records before minting, so this is a
  hardening follow-up rather than a defect.
- `mind` still has a broad existing custom text projection for older work-graph
  shorthand in `mind/src/text.rs`. Accepted-knowledge requests bypass it and use
  contract parsing, so it does not violate this correction, but future CLI
  simplification should keep accepted knowledge on the contract path.
- I did not rerun the full `cargo test` or Nix flake check that Carson reported;
  focused checks matched the audit claims.

## Checked Evidence

Files and surfaces consulted:

- `/home/li/primary/AGENTS.md`
- `/home/li/primary/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/MindUsability/GeneralCodeImplementer-Evidence.md`
- `/git/github.com/LiGoldragon/signal-mind/AGENTS.md`
- `/git/github.com/LiGoldragon/signal-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-mind/schema/signal-mind.concept.schema`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/lib.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/round_trip.rs`
- `/git/github.com/LiGoldragon/signal-mind/tests/schema_drift.rs`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/src/command.rs`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/dispatch.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/domain.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/graph.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/kernel.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/mod.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`

Repository state:

- `jj status` in `/git/github.com/LiGoldragon/signal-mind`: clean working copy;
  parent commit `b8c5da96d8ead413287eb407cd7fda55919f5fd5` on `main`.
- `jj status` in `/git/github.com/LiGoldragon/mind`: clean working copy; parent
  commit `4b3b28c2f828198625e658bca496a3aeb7c31c51` on `main`.
- `jj log` in `/home/li/primary` shows evidence commit
  `3e517695c1f88e0bc0460019bef8bed6c60e843f`.

Focused commands run:

- `/git/github.com/LiGoldragon/signal-mind`:
  `cargo test --test round_trip knowledge -- --nocapture`
  - Result: passed, 4 tests.
- `/git/github.com/LiGoldragon/signal-mind`:
  `cargo test --test schema_drift accepted_knowledge -- --nocapture`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/signal-mind`:
  `cargo test --test round_trip old_keyed -- --nocapture`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/mind`:
  `cargo test --test actor_topology accepted_knowledge -- --nocapture`
  - Result: passed, 1 test.
- `/git/github.com/LiGoldragon/mind`:
  `cargo test --test actor_topology knowledge_judge -- --nocapture`
  - Result: passed, 3 tests.
- `/git/github.com/LiGoldragon/mind`:
  `cargo test --test actor_topology semantic_rejection -- --nocapture`
  - Result: passed, 1 test.
