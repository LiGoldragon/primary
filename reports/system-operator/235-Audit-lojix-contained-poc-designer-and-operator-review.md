# Audit: lojix contained POC, designer work, and operator self-review

System-operator audit of system-designer report `reports/system-designer/158-lojix-unified-deploy-test-poc-contracts-and-verification-2026-06-21.md`, the live `lojix` branch `live-deploy-test-chain`, and my POC branches:

- `schema-rust-next` branch `system-operator-contained-test-poc`, commit `2d34bcf3` (`Pin schema-next parser for lojix POC codegen`)
- `signal-lojix` branch `system-operator-contained-test-poc`, commits through `7a48193f` (`Use pinned schema rust branch for ordinary POC`)
- `meta-signal-lojix` branch `system-operator-contained-test-poc`, commit `0bb3ca4e` (`Remove meta test surface for contained POC`)
- `lojix` branch `system-operator-contained-test-poc`, commit `38868f1f` (`Implement ordinary contained deploy test POC`)

## Bottom line

Designer's reframe still holds: lojix should be the unified deploy/test component, contained testing belongs on ordinary `signal-lojix`, and production deployment belongs on privileged `meta-signal-lojix`. My POC proves the basic face-correction can compile and pass tests: ordinary now has `DeployContained` / `CheckContained` / `Release`; meta has only `Deploy` / `Pin` / `Unpin` / `Retire`; production targets are represented by a meta-only `ProductionNode`.

The important self-review correction is that my POC is a useful implementation sketch, not the designer's wave-0 proof. I bypassed the current schema toolchain by pinning `schema-rust-next` back to a specific `schema-next` parser revision. That made the contract reshape buildable, but it did not prove current `schema-rust-next` can route ordinary and meta deploys into one shared pipeline without synthesizing a shared target supertype. Designer was right to call that a make-or-break gate, and my implementation has not discharged it.

## Designer Work Review

### 1. Strong: the architecture is correctly re-centered on the two faces

Report 158's central move is sound. It dissolves the separate `crucible` component and places the reusable test interface on lojix's ordinary signal while keeping production mutation on the meta signal. The report also accepts the correction from my prior audit: the boundary is not "ordinary can never mention a cluster node." The better invariant is "ordinary can describe a node profile to build, but it cannot name a production node as the live mutation or generation-promotion target."

My POC follows that corrected shape:

- `signal-lojix/schema/lib.schema:79` defines `NodeProfile { ClusterName * NodeName * kind (Optional DeploymentKind) }`.
- `signal-lojix/schema/lib.schema:90` defines `ContainedTarget [HermeticVm (VmHostGuest VmHostGuestTarget) (EphemeralDroplet EphemeralDropletTarget)]`.
- `meta-signal-lojix/schema/lib.schema:78` defines `ProductionNode { ClusterName * NodeName * }`.
- `meta-signal-lojix/schema/lib.schema:88-111` makes `ProductionNode` the target for deploy, pin, unpin, and retire.

This is the right type split. `NodeProfile` means "configuration to instantiate under containment." `ProductionNode` means "declared live node whose generation may be mutated." Those should remain separate nouns.

### 2. Strong: designer's honesty about HermeticVm prevents a false victory

Report 158 says the hermetic wave proves the face-correction, not the full shared bring-up pipeline. That is exactly right. My tests prove an ordinary `DeployContained(HermeticVm)` records and observes a contained run, but `HermeticVm` is still the degenerate `nix build .#checks...` path. It does not bring a closure up on a running endpoint.

So the truthful claim is:

- proved: contained hermetic run can be initiated and observed from ordinary signal, with no meta `Test` verb;
- not proved: one shared deploy pipeline brings closures up across production and contained live targets;
- not proved: the daemon executes a typed propagation body over criome/spirit/router.

That matters because the public story should not accidentally sell a hermetic check as the full deployment/test unification.

### 3. Strong: the live branch has a clear rehome path

The designer/live branch `/home/li/wt/github.com/LiGoldragon/lojix/live-deploy-test-chain` is clean and contains the real live bracket:

- `BringUpTestVm`
- `DeployIntoTestVm`
- `AssertTestVm`
- `TearDownTestVm`

It is still expressed through `TestMode [Hermetic Live]`, which is the old shape. The branch should not be merged as a mode flag. It should be rehomed as the `VmHostGuest` variant under ordinary `ContainedTarget`, with a test proving the ordinary path cannot resolve or mutate a real `ProductionNode`.

Designer's wave 1.5 migration invariant is therefore correct and operationally specific: every live call site is either contained-guest work, which goes to ordinary `VmHostGuest`, or production-switch work, which goes to meta `Deploy`.

## Operator POC Review

### 1. Critical: I did not prove the codegen gate

Report 158 says wave 0 must prove that schema/codegen can route ordinary `DeployContained` and meta `Deploy` into one pipeline without forcing the contained and production targets into a shared supertype. My implementation does not do that.

The evidence:

- `schema-rust-next/Cargo.toml:19` pins `schema-next` to revision `abae95f9`.
- `signal-lojix/Cargo.toml:26` points build-dependency `schema-rust-next` at my POC branch.
- `meta-signal-lojix/Cargo.toml:27` does the same.

This was a tactical escape hatch after the current parser rejected older schema syntax. It proves the reshaped contracts and daemon path can build with a pinned parser. It does not prove the current toolchain can carry the final shape. Before this becomes the integration path, wave 0 still needs the throwaway fixture designer specified.

### 2. High: the public type split is good, but the internal nouns still say "test"

The public schemas moved in the right direction, but daemon internals still carry old vocabulary:

- `TestDefaults`
- `TestJobs`
- `TestPipeline`
- `TestRunIdentifier`
- `TestRunRecord`
- `TestOutcome`

Some of that may survive as historical storage names, but it is a smell if it leaks into the final public interface. The component is no longer "test mode"; it is contained deployment plus optional verification and release. The likely final nouns are closer to:

- `ContainedDefaults` or `ContainedPolicy`
- `ContainedJobs`
- `ContainedRunIdentifier`
- `ContainedRunRecord`
- `ContainedOutcome` or `ContainedVerdict`

This rename is not cosmetic. It prevents future agents from rediscovering a `TestMode` worldview after the contract removed it.

### 3. High: `DeployContainedRequest.source` is ignored by the runtime lowering path

The ordinary request includes `source ProposalSource` at `signal-lojix/schema/lib.schema:95`, and tests construct it in `lojix/tests/test_op.rs:66` and `:83`. But the runtime lowering path in `lojix/src/schema_runtime.rs:103-118` consumes the profile, contained target, and flake; it does not use `request.source`.

Validation instead reads configured `TestDefaults.proposal_source` through `TestDefaults::projection` at `schema_runtime.rs:144-149`. That creates a split-brain contract:

- the ordinary caller appears to choose the proposal source;
- the daemon actually validates against its configured source;
- a caller reading the schema cannot know whether the field is authoritative.

There are two clean shapes. Either remove `source` from `DeployContainedRequest` and make daemon policy explicitly own the projection, or use the request's `source` consistently for validation. Leaving both is a latent bug.

### 4. High: `CheckContained` and `Release` are ordinary roots but not real SEMA-shaped operations yet

`Query(ByTestRun ...)` already routes through `SemaRead` at `lojix/src/schema_runtime.rs:1474-1485`. My new `CheckContained` and `Release` do not. They inspect the store directly:

- `check_contained_run` calls `self.store.test_runs()` at `schema_runtime.rs:1518-1524`.
- `release_contained_run` calls `self.store.test_runs()` at `schema_runtime.rs:1545-1551`.

For the user's stated "all in signal/nexus/sema schema interfaces" bar, this is not good enough. `CheckContained` should probably be a thin ordinary shorthand that lowers to a SEMA read. `Release` should become a SEMA write that marks a contained handle released and, for non-hermetic targets, drives a reaper command. The POC's direct store reads are acceptable as a temporary sketch; they should not land as the production pattern.

### 5. Medium: `Release` acknowledges, but does not reap

The POC's `Release` returns `Released { released: true }` for any known run (`schema_runtime.rs:1552-1557`). It does not mark the run released in durable state and does not drive teardown. That is fine for `HermeticVm`, which has no live endpoint, but it is the core safety requirement for `VmHostGuest` and `EphemeralDroplet`.

Before either live contained target becomes runnable, release must be a durable lifecycle transition:

- write released/reaping/reaped state to SEMA;
- drive teardown through nexus effects;
- reconcile on daemon restart;
- reject or idempotently acknowledge duplicate release.

Designer's "provisioner must be reaper" point is correct; my POC does not implement it.

### 6. Medium: I implemented `CheckContained`, while designer converged on `VerifyContained`

My branch uses roots `DeployContained CheckContained Release` (`signal-lojix/schema/lib.schema:24`). Report 158 initially sketched `AssertAgainst`, then accepted my earlier correction that `Assert` is a SEMA-class word and suggested `VerifyContained`.

`CheckContained` is safe from the SEMA naming collision, but it is ambiguous: it can mean "query the handle" rather than "run a verification body." In the POC, it is exactly a status check. If the next wave needs a typed propagation body, there should be a separate verb, probably `VerifyContained`, for body execution. I would keep `CheckContained` only as a status shorthand.

### 7. Medium: the test interface is promising but still only a witness

The compact interface in `lojix/tests/test_op.rs:180-186` is the right ergonomic direction:

```rust
let inputs =
    ContainedClusterTest::new("goldragon", "github:LiGoldragon/CriomOS-test-cluster/main")
        .hermetic("criome")
        .hermetic("spirit")
        .hermetic("router")
        .deploy_inputs();
```

This shows the user-facing test shape we want: name a cluster fixture, name nodes, choose a substrate, and get schema-native ordinary inputs. But it is still just a test-local helper returning raw `ordinary::Input`. The public API should become a lojix helper layer with typed shorthands and policy query/setting primitives, not a pattern copied between tests.

The next iteration should let a test express:

- cluster fixture source;
- contained substrate per node or default substrate for all nodes;
- lease/cost/machine-size options;
- deployment kind and flake/build attribute;
- verification body;
- release policy.

It should also expose daemon policy query/set explicitly, so the caller can discover defaults rather than guessing from schema fields.

## Integration Risks

### 1. Current POC branches and designer live branch will conflict

The live branch depends on `TestMode` and the old meta `Test` plumbing. My POC deletes the meta `Test` surface and generalizes records onto `ContainedTarget`. Integration should happen in this order:

1. Land the wave-0 schema/codegen fixture.
2. Land the ordinary/meta contract split.
3. Rebase the live branch by translating `TestMode::Live` into `ContainedTarget::VmHostGuest`.
4. Add the no-production-resolution negative test.

Trying to merge the live branch first will preserve the old mode flag and make the later type boundary harder to enforce.

### 2. The POC has broad deletion in `tests/test_op.rs`

The `lojix` POC commit changed `tests/test_op.rs` heavily: 846 lines removed and 521 inserted across the repo. The simplification was useful for making the POC legible, but review should check whether any old live or daemon-integration coverage disappeared rather than being translated.

I would not merge the POC as-is without an explicit test coverage migration list.

### 3. The cloud tier is accepted by intent but not yet safe by mechanism

The psyche accepted bounded cloud spend on ordinary, but the actual safety mechanism is still future work. The final `EphemeralDroplet` runnable path needs daemon policy and restart reconciliation before it stops returning `SubstrateUnavailable`. That is not optional hardening; it is the authority boundary for real money.

## Questions

1. Should the public ordinary verification root be split into `CheckContained` for status and `VerifyContained` for executing a typed body? My POC currently uses `CheckContained` only for status; designer's design needs a body-execution verb.

2. Should `DeployContainedRequest.source` be removed in favor of daemon-owned projection policy, or should the request source become authoritative? The current POC schema exposes a source field that runtime lowering ignores.

3. Should final contained-run storage rename away from `TestRun*`, or do we accept old storage nouns internally while keeping the public wire clean? I recommend renaming before this pattern spreads.

4. Should `EphemeralDroplet` require a caller-presented typed quota or lease credential in addition to daemon caps? The user accepted bounded ordinary spend, but a credential would make the delegated cloud authority visible on the ordinary request.

5. Should the live branch be rebased onto the POC split, or should the POC split be re-authored on top of the live branch? I recommend landing the split first, then translating live work into `VmHostGuest`, because the split is the safety boundary.

## Recommendations

1. Treat report 158 as the canonical design frame, with one correction: "ordinary cannot name a production node" should always be phrased as "ordinary cannot use a production node as a mutation target." `NodeProfile` is allowed on ordinary; `ProductionNode` is not.

2. Run the real wave-0 codegen fixture before any merge of these branches. My POC branch pin is a useful escape hatch, not proof.

3. Promote `CheckContained`/`Release` into explicit SEMA read/write paths before landing. Direct store inspection is the wrong final pattern.

4. Build the public test helper API deliberately. The `ContainedClusterTest` helper demonstrates the desired ease of use, but the real API should expose schema shorthands, contained substrate options, leases/cost caps, and daemon policy query/set.

5. Rehome the live branch as `VmHostGuest` only after the ordinary/meta split is stable, with an explicit negative test that ordinary cannot resolve a real `ProductionNode`.
