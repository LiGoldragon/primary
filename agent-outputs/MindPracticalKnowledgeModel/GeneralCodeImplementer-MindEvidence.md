# Mind Accepted-Knowledge V1 Implementation Evidence

## Task And Scope

Implemented the Mind accepted-knowledge v1 daemon/store/admission/query vertical slice in `/git/github.com/LiGoldragon/mind`.

Inputs consulted:

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/IntentTranslator-ImplementationBrief.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-Evidence.md`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`
- existing Mind actor, store, table, graph, memory, text, and actor topology test paths

Coordination:

- Observed Orchestrate roles.
- Claimed `(Path /git/github.com/LiGoldragon/mind)` as `GeneralCodeImplementer`.

## Changed Files

- `/git/github.com/LiGoldragon/mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind/Cargo.lock`
- `/git/github.com/LiGoldragon/mind/src/lib.rs`
- `/git/github.com/LiGoldragon/mind/src/knowledge.rs`
- `/git/github.com/LiGoldragon/mind/src/tables.rs`
- `/git/github.com/LiGoldragon/mind/src/memory.rs`
- `/git/github.com/LiGoldragon/mind/src/text.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/root.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/dispatch.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/domain.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/view.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/mod.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/graph.rs`
- `/git/github.com/LiGoldragon/mind/src/actors/store/kernel.rs`
- `/git/github.com/LiGoldragon/mind/tests/actor_topology.rs`

## Local Contract Consumption

Mind now patches `signal-mind` through:

```toml
[patch."https://github.com/LiGoldragon/signal-mind.git"]
signal-mind = { path = "../signal-mind" }
```

`Cargo.lock` resolves `signal-mind v0.5.1` from `/git/github.com/LiGoldragon/signal-mind`, consuming the uncommitted contract worker output. This is buildable for local Cargo checks. It is not remote-addressable for Nix until `signal-mind` is committed/pushed or replaced by a portable flake/git revision.

## Behavior Implemented

- Added `KnowledgeJudge` trait and `FixtureKnowledgeJudge` implementation.
- Added `MindRootArguments::with_knowledge_judge` so tests can inject deterministic verdicts; the default judge is an empty fixture that rejects semantic submissions as unclear.
- Routed `SubmitKnowledge` through dispatch, domain, store supervisor, graph store, and store kernel.
- Routed `QueryKnowledge` through dispatch, view, store supervisor, graph store, and store kernel.
- Added `accepted_knowledge` as a `sema-engine` registered table family and bumped the Mind store schema to v11.
- Stored accepted entities, statements, relations, domains, and sources as one `AcceptedKnowledge` family.
- Deterministic preflight rejects relation candidates with missing endpoints or relation domain/range mismatches before the judge is called.
- Verdict application persists accepted draft records and relations only; semantic rejections persist nothing.
- Accepted admission replies/receipts are not stored.
- `KnowledgeSource` is stored only when the accepted draft includes a source record or source relation.
- Queries support identifier, stable key, kind, domain selector, relation selector, `CurrentOnly`, and `IncludeSuperseded`.
- Current accepted-knowledge queries hide records targeted by accepted `Supersedes` relations; historical queries include them.

## Tests Added

Added `accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries` in `tests/actor_topology.rs`.

The test covers the ten-step fixture sequence:

- component and contract domains are accepted;
- `component:mind` and `contract:signal-mind:ordinary` entities are accepted and classified;
- `repo:signal-mind` defines the signal-mind contract;
- semantic `NotKnowledge` rejection stores nothing;
- missing endpoint rejection is structural and does not call the judge;
- source-backed statement stores a source only because the draft includes it;
- supersession hides the older statement from current queries and preserves it historically;
- conflict rejection stores nothing.

## Checks Run

- `cargo check` before tests: passed.
- `cargo test --test actor_topology accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries -- --exact`: passed.
- `cargo test --test actor_topology`: passed, 35 tests.
- `cargo test`: passed, full Rust suite.
- `cargo clippy --all-targets -- -D warnings`: passed.
- `cargo check` after architecture update: passed.
- `nix build .#checks.x86_64-linux.test --no-link --no-update-lock-file`: failed because the sandboxed build cannot load the local path dependency `/build/signal-mind`; the current contract dependency is intentionally local and uncommitted.

## Blockers And Follow-Up

Nix validation is blocked by dependency mechanics, not by Rust test failures. To make Nix green, publish or otherwise remote-address the `signal-mind` 0.5.1 contract changes, then replace the local path patch with the repo's normal portable dependency reference and rerun the Nix checks.

No real corpus import or production AI prompt integration was added.
