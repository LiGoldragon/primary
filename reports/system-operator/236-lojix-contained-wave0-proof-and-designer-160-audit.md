# Lojix contained wave-0 proof and designer 160 audit

System-operator delta audit of system-designer report `reports/system-designer/160-writing-a-criome-spirit-router-cluster-test-the-comfortable-authoring-layer-2026-06-21.md` and the updated `schema-rust-next` branch `system-operator-contained-test-poc`, commit `e5f33eed` (`Prove lojix contained target split on current schema toolchain`).

## Bottom line

Designer report 160 fixes the main open contract question from operator audit 235. `CheckContained` should dissolve: status is `Query (ByTestRun ...)`, body execution is `VerifyContained`, and the public write/execution triple is `DeployContained / VerifyContained / Release`. That is the right grammar and it removes the status/store-peek ambiguity.

The wave-0 blocker is now discharged on my side. The prior POC only compiled by pinning `schema-next` to an old parser revision. I replaced that with the current `schema-next` `main` dependency and pushed a current-toolchain proof in `schema-rust-next`:

- ordinary `signal-lojix` owns `ContainedTarget` and `DeployContainedRequest`;
- meta `meta-signal-lojix` owns `ProductionNode` and `DeployRequest`;
- daemon `lojix:nexus` imports both target types directly and emits separate `ContainedPipelineCommand` / `ProductionPipelineCommand`;
- generated Rust contains no synthesized shared target supertype such as `ContainedOrProduction`, `ProductionOrContained`, or `DeployTarget`.

Verification run on the branch:

- `cargo test --test lojix_contained_wave0`
- `cargo test`
- `cargo fmt --check`

## Designer 160 review

Report 160's strongest correction is NOTA discipline. The comfortable authoring layer uses sibling variants for shorthand and a vector of option variants for optional settings, instead of pretending NOTA has named optional fields. That matters because the public testing surface should be easy without becoming a second, informal schema language.

The verb section is also a real convergence point. `CheckContained` was carrying two meanings in my POC: "what is the run status?" and "execute a check." Designer splits those cleanly:

- status read: `Query (ByTestRun ...)`;
- executable verification: `VerifyContained` carrying `VerificationBody`;
- lifecycle cleanup: `Release`.

That should be the shape before downstream `signal-lojix` and `lojix` are hardened.

The designer's `source` position is correct. `DeployContainedRequest.source` should be authoritative when present. Removing it would make the daemon-only default simpler, but it would make per-call proposal-source selection impossible and would hide a real input to `NodeProfile` closure resolution. My earlier audit found the actual bug: the runtime lowering ignored the request field.

The report is honest about router feasibility. `RouterFanOut` is allowed to be an honest stub until router builds against the current schema stack; the test system must not fake a green router path.

## Operator self-audit

The old weakness in my branch was the parser pin. That is fixed in `schema-rust-next` commit `e5f33eed`. The work was larger than adding a single fixture because moving to current `schema-next` required migrating stale fixture syntax and regenerating snapshots:

- retired `*` struct-field markers removed;
- scalar fields expressed as `field.Type`;
- PascalCase collection fields expressed as structural field wrappers, producing crate-local wrapper newtypes;
- family field syntax restored to keyed pairs such as `record Entry table entries key Domain`.

The broad fixture churn is not conceptual churn in lojix; it is the cost of proving the POC against the live schema parser rather than dodging it.

The downstream POC branches are now behind the design:

- `signal-lojix` still has `CheckContained`;
- `lojix` still has direct store checks for `CheckContained` / `Release`;
- `DeployContainedRequest.source` is still not authoritative in runtime lowering;
- internal nouns still say `TestRun*`, which is tolerable for a sketch but bad as a final public model.

## Greatest insights

1. The type-safety thesis survives the current toolchain. Current codegen can route ordinary and meta deployment into one daemon-facing nexus without inventing a shared target sum type.

2. The status verb was the conceptual bug. Once status returns to `Query`, `VerifyContained` can mean one thing: run a typed verification body.

3. `source` is not a convenience field. It is part of the closure-selection authority for a contained deployment request.

4. The comfortable authoring API should be a lowering layer over schema roots, not a parallel DSL. Short forms must be typed variants that lower to the full contract.

5. Fixture migration exposed a useful warning: stale parser pins can make a POC look healthier than the live toolchain allows. Wave-0 tests belong at the schema/codegen layer before daemon integration.

## Questions

1. Should `VerifyContained` return only a verdict, or should it also append a structured run event that `Query (ByTestRun ...)` observes?

2. Should `Release` be rejected until a successful `VerifyContained`, or should it always be legal and idempotent as cleanup?

3. Should `source` be required on every `DeployContainedRequest`, or optional with daemon defaults? I lean optional with authoritative override, because tests need convenience but per-call provenance must work.

4. Should `TestRun*` storage names be renamed now to `ContainedRun*`, before the live `VmHostGuest` path lands?

5. Should designer's `RunContainedCluster` authoring layer live in `signal-lojix` as a public ordinary shorthand, or in a thin lojix client/helper crate that emits ordinary roots?

## Next operator work

The next code step is downstream convergence:

1. Update `signal-lojix` POC from `CheckContained` to `VerifyContained` plus status through `Query`.
2. Make request `source` authoritative in `lojix` lowering.
3. Route `VerifyContained` and `Release` through nexus/sema effects rather than direct redb reads.
4. Rehome live deployment testing as `ContainedTarget::VmHostGuest`, not `TestMode::Live`.
5. Add the comfortable cluster test helper only after the lower contract no longer lies about status, source, or release lifecycle.
