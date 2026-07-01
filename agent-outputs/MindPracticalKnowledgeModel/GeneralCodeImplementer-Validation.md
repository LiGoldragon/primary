# Mind Accepted-Knowledge V1 Validation

## Task And Scope

Validated the current Mind accepted-knowledge v1 implementation in `/git/github.com/LiGoldragon/mind` using the local uncommitted `signal-mind 0.5.1` path patch. No source edits were made, and nothing was committed or pushed.

Context consulted:

- `/home/li/primary/AGENTS.md`
- `/git/github.com/LiGoldragon/mind/AGENTS.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-Evidence.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/GeneralCodeImplementer-MindEvidence.md`
- `/home/li/primary/agent-outputs/MindPracticalKnowledgeModel/IntentTranslator-ImplementationBrief.md`
- `src/knowledge.rs`
- `src/actors/root.rs`
- `src/daemon.rs`
- `src/command.rs`
- `tests/actor_topology.rs`
- `tests/cli.rs`
- `tests/daemon_wire.rs`
- `/git/github.com/LiGoldragon/signal-mind/src/knowledge.rs`

The Mind repo also instructs agents to read `/home/li/primary/lore/AGENTS.md`; that file was absent, so validation continued with the available primary and repo instructions.

## What Was Tested

The concrete accepted-knowledge path is testable now through the fixture actor test:

- accepted domain/entity/relation/statement/source draft application;
- semantic `NotKnowledge` and conflict rejections storing nothing;
- relation missing-endpoint structural preflight returning `StructuralPreflightFailed`;
- structural preflight bypassing the judge, verified through fixture judge call count;
- source records being absent until the accepted draft explicitly includes a source;
- current queries hiding superseded statements while historical queries include them;
- identifier, stable-key, domain, relation, and kind queries retrieving accepted fixture data.

The daemon/CLI path is also partially testable now:

- full `signal_mind::MindRequest` NOTA fallback parsing accepts `QueryKnowledge` and `SubmitKnowledge`;
- a real `mind-daemon` process served a temp socket and store;
- the `mind` CLI sent requests over the daemon socket;
- default daemon admission rejected semantic submissions as `MeaningUnclear`;
- semantic rejection stored no accepted knowledge;
- missing endpoint structural rejection worked through the daemon/CLI path.

Accepted data cannot be created through the current process daemon or ordinary CLI because `MindEngine` starts `MindRootArguments::new(...)`, whose default knowledge judge is `FixtureKnowledgeJudge::empty()`. The fixture judge injection that can accept drafts is currently test-only via `MindRootArguments::with_knowledge_judge`.

## Exact Commands And Results

- `cargo test --test actor_topology accepted_knowledge_fixture_slice_admits_queries_and_preserves_rejection_boundaries -- --exact`  
  Result: passed, 1 test.

- `cargo check`  
  Result: passed.

- `cargo test`  
  Result: passed. Covered 12 lib tests, 35 `actor_topology` tests, 6 CLI tests, 13 daemon-wire tests, 7 memory tests, 3 orchestrate-caller tests, 17 architecture/constraint tests, and doc tests.

- `cargo clippy --all-targets -- -D warnings`  
  Result: passed.

- `cargo run --quiet --bin mind-write-configuration -- '(ConfigurationWriteRequest /tmp/mind-knowledge-cli.7GjyNx/mind.sock /tmp/mind-knowledge-cli.7GjyNx/mind.meta.sock /tmp/mind-knowledge-cli.7GjyNx/mind.sema /tmp/mind-knowledge-cli.7GjyNx/mind.config)'`  
  Result: passed, wrote daemon configuration.

- `cargo run --quiet --bin mind-daemon -- /tmp/mind-knowledge-cli.7GjyNx/mind.config`  
  Result: daemon started and served the temp socket until stopped after the probe.

- `MIND_SOCKET=/tmp/mind-knowledge-cli.7GjyNx/mind.sock MIND_ACTOR=operator cargo run --quiet --bin mind -- '(QueryKnowledge (ListByKind (Domain IncludeSuperseded)))'`  
  Result: passed with `(KnowledgeList ([] False))`.

- `MIND_SOCKET=/tmp/mind-knowledge-cli.7GjyNx/mind.sock MIND_ACTOR=operator cargo run --quiet --bin mind -- '(SubmitKnowledge ((Domain (domain:component Component None)) FixtureOnly (None)))'`  
  Result: passed with `(KnowledgeRejected (MeaningUnclear ([fixture judge has no verdict]) (Some ([submit a more specific accepted-knowledge candidate]))))`.

- `MIND_SOCKET=/tmp/mind-knowledge-cli.7GjyNx/mind.sock MIND_ACTOR=operator cargo run --quiet --bin mind -- '(QueryKnowledge (ListByKind (Domain IncludeSuperseded)))'`  
  Result: passed with `(KnowledgeList ([] False))`, confirming semantic rejection stored no domain.

- `MIND_SOCKET=/tmp/mind-knowledge-cli.7GjyNx/mind.sock MIND_ACTOR=operator cargo run --quiet --bin mind -- '(SubmitKnowledge ((Relation (DependsOn (StableKey component:mind) (StableKey component:missing) None)) FixtureOnly (None)))'`  
  Result: passed with `(KnowledgeRejected ((StructuralPreflightFailed ((MissingEndpoint (StableKey component:mind)))) ([relation DependsOn]) None))`.

- `MIND_SOCKET=/tmp/mind-knowledge-cli.7GjyNx/mind.sock MIND_ACTOR=operator cargo run --quiet --bin mind -- '(QueryKnowledge (ListByDomain (Any IncludeSuperseded)))'`  
  Result: passed with `(KnowledgeList ([] False))`.

- `nix build .#checks.x86_64-linux.test --no-link --no-update-lock-file`  
  Result: failed as expected. The sandboxed build could not load the local path dependency for `signal-mind`; Cargo in the Nix build tried to read `/build/signal-mind/Cargo.toml`, which was absent. This is dependency portability failure, not a Rust test failure.

## Direct Answers

Mind can be tested in action now through the fixture actor path and through a daemon/CLI rejection/query probe.

The full accepted-data vertical slice is not yet operator-visible through the daemon/CLI because the only accepting judge is injectable through test construction. The process daemon uses the default empty fixture judge, so every semantic submission is rejected as unclear.

Semantic rejection stores nothing: confirmed by the fixture test and by daemon/CLI query returning an empty domain list after `MeaningUnclear`.

Structural rejection bypasses the judge: confirmed by fixture judge call count in the vertical slice test; the daemon/CLI path also returns structural missing-endpoint rejection before any semantic verdict is needed.

Queries can retrieve accepted fixture data: confirmed in the vertical slice test by identifier, stable key, domain, relation, kind, current, and historical queries.

## Recommended Next Step

The smallest step for an operator-visible accepted-knowledge demo is to add a non-production demo judge configuration path for `mind-daemon`, for example a configuration field or test/demo binary that supplies a deterministic fixture verdict queue to `MindRootArguments::with_knowledge_judge`. After that, the existing CLI full-contract NOTA path can submit accepting `SubmitKnowledge` requests and query the accepted records through the real socket.

Before Nix can validate this implementation, publish or otherwise remote-address `signal-mind 0.5.1` and replace the local `../signal-mind` path patch with a portable dependency reference.
