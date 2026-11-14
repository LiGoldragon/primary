# Independent per-address declaration delta gate

Nonauthor `/root/review_protos_slice`, native01a1adff-cafa-77a1-aa73-aa98b4dd4794, sequential review23:19:46–23:22:31UTC. Proposal `052-address-declaration-delta.md` SHA09015ce4efbd19ee8f088d8a01f3a7ff6e578a58adbeb96088d2a2e0cfd8c6fe unchanged before/after. Source bases Flow916b545/treef5f01e, meta281f5aa/tree907f3b, signalce083f/tree191072. Read-only, no effects. Parent lands reader's findings.

**Verdict GAP. Declaration-delta bodies remain held.**

## Exact missing-declaration behavior

- `waking.rs:1471–1492` silently falls back from absent declaration to predecessor LaunchProfile. After Remove, future wake/refresh can reuse removed configuration. Remove this fallback; no shadow declaration.
- `launching.rs:227–238` conflates absent declaration with root_option=None and supplies runtime source_root. Missing declaration can use existing `StartRejected(Undeclared)` as `sending.rs:542–550`; source-root projection remains only for present declaration.
- `store/successor.rs:170–177` conflates absence with OnDemand; explicit refresh consumes that at `waking.rs:1713–1728`. Missing declaration should use existing `RefreshRejected(Undeclared)` already at1764–1765, not present-but-both-continuities-unset `Response::Refused(Refusal::NotConfigured)`.
- Ordinary wake missing declaration should use existing `WakeRefusal::StartRejected(StartRejection::Undeclared)`/RetryCause rather than Unplaceable, whose496–524 mapping falsely yields HerdrRefused. Present-but-unresolved continuity can use existing `StartRejection::CompositionRefused(Unconfigured)` unless Core explicitly requires general NotConfigured on this internal path.

These are minimal existing-vocabulary proposals, not an author/self-granted design change. Primary/Core must bind exact branches.

## Omitted current producer and fixture obligations

- `flow-meta/src/main.rs:311–319` reconstructs whole-family Configure.Metaflows from snapshot.
- `capsule/flow-capsule.clj:1130–1148` configure-line, broken-metaflows and restore-configuration! depend on a single family line.
- Rust constructors: flow-nexus tests/ending.rs110; refresh_and_compaction.rs113; refreshing.rs60; send_admission.rs368; waking.rs120,4033,5456; src/lib.rs4365,4394,5649. Each requires per-address semantics, not mere compilation repair. Existing rehearsing/secondary/store/capsule ledger rows remain.

## Direct and transitive persisted reachability

Generated meta ConfigurationChange/Query/Response derive rkyv wire archives; no Flow EngineRecord embeds these enums. Store references to them are parameters/matches. Sole persisted shared payload is `StoredMetaMetaflowConfiguration { ConfigureMetaflow }` in store/metaflow_declaration.rs29–47. Optional Continuity therefore uses exactly the already-frozen V5→V6 CONFIG migration. Snapshot is wire-archived; Flow ConfiguredFamilies is not stored. No additional Memory family/version is evidenced by new operation variants.

Required wire tests remain meta datom+rkyv roundtrips for both new Query operations and unchanged snapshot Response. Persisted byte/readback proof remains an implementation gate, not claimed executed.
