# Reconciling cpip and report 156 with the reframe — testing IS lojix's ordinary contract

*System-designer study · 2026-06-20 · report 157 (supersedes the separate-crucible design of report 156)*

The psyche's reframe: testing and deployment are the SAME function in ONE
component (lojix). Both build an OS/cluster closure and bring it up on a
target; they differ ONLY in containment. So lojix does both, split across
the triad's two faces — ORDINARY signal = safe contained testing
(throwaway/ephemeral targets, no production authority), META signal =
privileged production deployment to real nodes. The ordinary-vs-meta split
IS the safety boundary, enforced by TYPED contained-vs-production targets, a
type/authority property and NOT a runtime flag. There is NO crucible
component; `cpip`'s "one easily-reusable interface for testing" IS lojix's
ordinary contract; deployment is lojix's meta contract.

This report does NOT relitigate whether to do it. It answers HOW: (1) the
three `cpip` substrates become `ContainedTarget` variants on the ORDINARY
contract; (2) where per-test customization lives now; (3) what of report
156 survives vs dissolves; and it produces the relocated ordinary-contract
test-operation shape.

## The decisive finding: the reframe is already half-built, on the wrong face

The current lojix triad already carries a `Test` op and already encodes the
containment axis — but it placed both on the wrong sides under the reframe.
Verified against the live contracts:

- `meta-signal-lojix/schema/lib.schema:60` — the meta request root is
  `[Deploy Pin Unpin Retire Test]`. **`Test` lives on the privileged meta
  face**, declared "strictly more privileged than Deploy" (`:80-82`).
- `signal-lojix/schema/lib.schema:74` — `TestMode [Hermetic Live]` already
  exists, and its own comment (`:69-73`) names the containment distinction
  exactly: Hermetic is a "sandboxed VM, no host effect"; Live drives the
  "host-untouched cycle". This IS the reframe's containment axis, already
  typed — it was just never used as the ordinary/meta sorting key.
- The daemon already drives both (`lojix/src/schema_runtime.rs:1455-1468`):
  Hermetic → `HermeticCheck` effect; Live → `BringUpTestVm`, with Live
  honestly gated `LiveNotYetEnabled` at submit (`:1681`).

So the reframe is not a green-field add. It is a **face-correction plus a
generalization**: move `Test` from meta to ordinary, and widen its single
containment knob (`TestMode [Hermetic Live]`) into the full
`ContainedTarget` spectrum that `cpip` and report 156 already worked out.
What stays on meta is exactly `Deploy`/`Pin`/`Unpin`/`Retire` — the
production-mutating verbs. This is the cleanest possible landing for the
reframe: it deletes a contract leg's worth of report-156 scaffolding and
*subtracts* a verb from meta rather than adding a component.

This also resolves report 156 open question 3 ("do lojix's
`TestMode`/`TestRunRecord` stay in signal-lojix or migrate to crucible?")
by dissolving it: they stay in signal-lojix because lojix IS the testing
component; there is no crucible to migrate to.

## (3 first) What survives the reframe and what dissolves

| Report-156 artifact | Disposition under the reframe |
|---|---|
| Separate `crucible` daemon | **DISSOLVES.** No new component. lojix already is the multi-substrate engine; it already shells `nix flake check` (Hermetic), drives the live VM bring-up, and is the deploy driver. The carve-out-3 multi-peer concern (the entire reason 156 forced a daemon into wave-1) evaporates: lojix is the deploy/build driver itself, not a client of one. |
| `signal-crucible` working contract | **DISSOLVES into signal-lojix.** The `TestDescriptor` vocabulary lands as the ordinary `Test` op's request payload on the EXISTING `signal-lojix` contract — no new repo, no cross-imports-to-self. |
| `meta-signal-crucible` + policy tables + ledger | **DISSOLVES.** 156 already deferred these behind a "need for owned state" trigger; the reframe removes the owner entirely. Provisioning ceilings stay in cloud's `Policy`; defaults in lojix's existing `TestDefaults`. |
| `TestDescriptor` knob set (`SubstrateWeight`, `Topology`, `Networking`, `Persistence`, `MaximumDuration`) | **SURVIVES, relocated** as fields of the ordinary `Test` request (see §2). `SubstrateWeight` is renamed `ContainedTarget` to name the safety property, not the mass. |
| `GateAssertionSpec` body (authorized-head / threshold-short / unconfigured / quorum-threshold) | **SURVIVES verbatim** as the typed `PropagationBody`. It is the `cpip` propagation test; the spirit precedent is real (`spirit/tests/criome_gate_1of1.rs:297-432` carries exactly the three cases). Carried `xhwa` 1-of-1 → `jk1w` quorum unchanged. |
| Three distinct case newtypes (`AuthorizedHeadCase` etc.) | **SURVIVES** with 156's permutation-safety rationale intact. |
| `ArtifactKind` / `RunRecord` / typed `TestOutcome`/`FailureStage` observation surface | **SURVIVES, already largely present.** signal-lojix already has `TestRunRecord`/`TestRunPhase`/`TestOutcome`/`FailureStage` (`:112-125`) observed via `(Query (ByTestRun …))`. Report 156's `Collect`/`ArtifactKind` is the one genuine ADD to the ordinary read surface. |
| The intent-fidelity map | **SURVIVES wholesale** — every record (`cpip g7yd 77ic 7let se72 y1v5 cncj qkvx 0a9p lt44 component-triad one-argument-daemon`) maps the same way, now onto lojix's two faces instead of crucible's. Updated table in §4. |
| `Validate` dry-run (pre-flight capability resolution) | **SURVIVES** as an ordinary verb — cheap projection read, surfaces `NoCapableHost`/cost before spending provider quota. |
| 156's data-level-vs-execution-identity honesty about the propagation body | **SURVIVES verbatim** — same three engines, same path to a single lojix-owned assertion interpreter. |

The net: report 156's TYPED CONTENT survives almost completely; its
STRUCTURAL premise (a separate component triad) is what the reframe deletes.
156's own adversarial critique pushed toward "the honest minimal answer is
not a new component" — the reframe is the psyche arriving at the same place
from intent, and it is stronger than 156's compromise.

## (1) The three cpip substrates become ContainedTarget variants

`cpip` fixes three substrates of escalating fidelity. Under the reframe each
is a variant of a single ordinary-contract `ContainedTarget` enum — the
typed value that makes "this run targets only throwaway resources" a
*type* property, not a flag. Every variant is contained by construction; a
broken ordinary run kills only the named throwaway target.

```
ContainedTarget [
  (Hermetic   HermeticProfile)   ;; cpip substrate 1 — host-untouched runNixOSTest
  (DurableVm  DurableVmProfile)  ;; cpip substrate 2 — on-demand VmHost guest (77ic)
  (CloudDroplet CloudDropletProfile) ;; cpip substrate 3 — ephemeral DO droplet, provisioned+reaped
]
```

Mapping, and why each is contained (the reframe's whole point):

- **`Hermetic`** ← `cpip`'s default hermetic runNixOSTest cluster (`7let`
  posture). Guests boot on separate kernels inside the nix sandbox; the host
  is never reconfigured. Containment = the nix build sandbox + throwaway
  VMs. This is the EXISTING `TestMode::Hermetic`, widened with a profile.
- **`DurableVm`** ← `cpip`'s opt-in durable on-demand microvm node (`77ic`).
  The guest is a throwaway target homed on a `VmHost`-capability node
  (`g7yd`); a broken deploy kills only the guest, host untouched (`7let`).
  This is the EXISTING `TestMode::Live`, narrowed to its contained meaning
  and given a profile. (Its host-untouched + BootOnce safety is what made it
  contained in the first place — `7let`/`77ic`.)
- **`CloudDroplet`** ← `cpip`'s opt-in DigitalOcean on-demand droplets for
  real cross-machine validation. Containment = the droplets are provisioned
  by lojix-as-cloud-client and **reaped under a mandatory teardown**; they
  are ephemeral by construction and never a standing production node. This is
  NEW to lojix's surface (today lojix has no cloud-droplet test path), and
  it is the one place lojix becomes a `meta-signal-cloud` client.

The key reframe insight made concrete: **the ordinary `Test` op accepts
ONLY `ContainedTarget` values; it has no variant that names a production
node.** Targeting a real live node to switch/promote a generation is
*unrepresentable* on the ordinary request — that operation is `Deploy` on
meta. The type system enforces the safety boundary; there is no
`--contained=false` runtime escape.

## (2) Where per-test customization lives now

In report 156 the per-test knobs were fields of a free-standing
`TestDescriptor` carried on `signal-crucible`. Under the reframe they are
**fields of the ordinary `Test` request payload on signal-lojix** — the
lightweight-sandbox ↔ full-KVM weight, topology, networking, and
persistence axes live inside each `ContainedTarget` profile (substrate-local
knobs) plus a few run-level fields (substrate-independent knobs).

Substrate-local (inside the profile — what varies node realization):

- `HermeticProfile { NetworkIsolation MaximumGuests }` — the `lt44`
  lightweight tier; `NetworkIsolation [SharedHost TapLayer3 CrossMachine]`
  (tap/L3 intra-host; vsock deferred per `lt44`). This is the
  lightweight-sandbox end of the weight axis.
- `DurableVmProfile { HostRequirement Activation MachineSizing }` —
  `HostRequirement` is a CAPABILITY requirement (`RequiresVmHost`), never a
  host-role field (`g7yd`, 156's accepted critique fix). `Activation
  [BootOnce]` single-variant by design (`77ic`). `MachineSizing` is the
  full-KVM-weight end (CPU/memory/disk newtypes).
- `CloudDropletProfile { Provider DropletCount RegionName CloudBringUp
  CostCeilingCents }` — `CloudBringUp [StockImage NixosAnywhere]`;
  `CostCeilingCents` + a daemon-side droplet cap bound cost; reaping is
  mandatory.

Run-level (substrate-independent — identical across substrates, the `cpip`
"one identical test"):

- `Topology { (Vec NodeSpec) (Vec NetworkLink) }`;
  `NodeSpec { NodeRole (Optional MachineSizing) }` — the cluster shape.
- `Networking` — the inter-node link policy.
- `PropagationBody` — the typed `cpip` test body, byte-identical across
  substrates (data-level identity in wave-1, per 156's honest statement).
- `Persistence [Ephemeral KeepForDebug]` — the debug-hold knob.
- `(Optional MaximumDuration)` — the cost/runaway bound.

The substrate-weight axis `cpip` names ("lightweight networked sandboxes
and/or full KVM, customized per test") is therefore expressed as: pick the
`ContainedTarget` variant for the substrate, and set its profile's weight
knobs (`MachineSizing` for full KVM, `MaximumGuests`/`NetworkIsolation` for
the lightweight tier). ONLY the `ContainedTarget` field varies node
realization; everything in the run-level set stays identical — that is the
`cpip` invariant, preserved.

## The relocated ordinary-contract test-operation shape

signal-lojix's ordinary request root gains the `Test` op (moved off meta)
and a `Collect`/`Validate` pair; the read surface (`Query`, the two
`Watch`es, `Unwatch`, `CheckHostKeyMaterial`) stays. Positional NOTA, bare
atoms unless delimited, never quotation marks (`qkvx`, NOTA discipline).

Ordinary request root (was `[Query WatchDeployments WatchCacheRetention
Unwatch CheckHostKeyMaterial]`):

```
[Test ObserveRun Collect Validate Query WatchDeployments WatchCacheRetention Unwatch CheckHostKeyMaterial]
```

| Verb | Reply | Meaning |
|---|---|---|
| `(Test TestRun)` | `(TestAccepted TestRunIdentifier DatabaseMarker)` | mint a contained run; daemon owns the lifecycle. Replaces the meta `Test`. |
| `(ObserveRun (ByRun TestRunIdentifier))` / `(ByCluster ClusterName)` | `(RunObserved TestRunListing)` | reuses the EXISTING `TestRunRecord`, generalized by a `ContainedTarget` column instead of the `TestMode` column. |
| `(Collect (FromRun TestRunIdentifier ArtifactKind))` | `(ArtifactsCollected (Vec ArtifactHandle))` | `ArtifactKind [SerialConsole DaemonJournal AssertionLog ClosurePath ProviderEvent]` — the one genuine ADD to the ordinary read surface. |
| `(Validate TestRun)` | `(Validated TargetResolution)` | dry-run capability resolution; returns the host/provider that WOULD be selected, or `NoCapableHost`, before spending provider quota. |

The `Test` request payload (the relocated `TestDescriptor`):

```
TestRun {
  ClusterName *
  ContainedTarget *      ;; the substrate spectrum — ONLY production-free variants
  Topology *
  Networking *
  PropagationBody *
  Persistence *
  duration (Optional MaximumDuration)
}

ContainedTarget [
  (Hermetic   HermeticProfile)
  (DurableVm  DurableVmProfile)
  (CloudDroplet CloudDropletProfile)
]
HermeticProfile   { NetworkIsolation * MaximumGuests * }
DurableVmProfile  { HostRequirement * Activation * sizing (Optional MachineSizing) }
CloudDropletProfile { Provider * DropletCount * RegionName * CloudBringUp * CostCeilingCents * }

NetworkIsolation [SharedHost TapLayer3 CrossMachine]
HostRequirement  [RequiresVmHost]
Activation       [BootOnce]
CloudBringUp     [StockImage NixosAnywhere]
Persistence      [Ephemeral KeepForDebug]

Topology    { nodes (Vec NodeSpec) links (Vec NetworkLink) }
NodeSpec    { NodeRole * sizing (Optional MachineSizing) }
MachineSizing { VirtualCpuCount * MemoryMebibytes * DiskGibibytes * }

PropagationBody [
  (FlakeCheck FlakeAttribute)
  (GateAssertion GateAssertionSpec)
  (Steps (Vec TestStep))
]
GateAssertionSpec {
  AuthorizedHeadCase *
  ThresholdShortCase *
  UnconfiguredCase *
  QuorumThreshold *
}
```

What changes on the META contract: `Test`, `TestRequest`, `TestRun`,
`QuickCheck`, `NodeSelection`, `AcceptedTest`, `RejectedTest`,
`TestRejectionReason` all **leave meta-signal-lojix**. Meta's request root
shrinks to `[Deploy Pin Unpin Retire]` — the production-mutating verbs only.
`TestMode` and `HostSelection` (today defined in signal-lojix `:74`/`:79`
and cross-imported by meta `:57-58`) stay in signal-lojix, now consumed by
the ordinary `Test` op directly; meta no longer imports them. The
`vudl`/`cgd8` authority records ("Test is owner-only, lives in meta") are
the records the reframe SUPERSEDES — flag for a psyche-confirmed
`Supersede`/`Clarify` edit (see Spirit gate below).

Honest gating carried forward: the daemon already handles Hermetic for real
and gates Live as `LiveNotYetEnabled` (`:1681`). Under the relocation,
`DurableVm` keeps that honest gate, `CloudDroplet` is unbuilt and returns a
typed `SubstrateUnavailable`/`NoCapableHost`, never a faked pass (`dqg3`).

## (4) Intent-fidelity map (relocated onto lojix's two faces)

| Record | How honored under the reframe |
|---|---|
| THE NEW DECISION (this turn) | The spine. Ordinary `Test` = safe contained testing; meta `Deploy` = privileged production. `ContainedTarget` is the typed safety boundary; no production-node variant is representable on the ordinary request. No crucible. |
| `cpip` | The ordinary `Test` op + the thin lojix CLI = the one reusable interface; `GateAssertionSpec` carried across substrates = the one propagation test; `ContainedTarget` = substrate-by-typed-parameter; the three substrates map exactly; `QuorumThreshold` carries `xhwa`→`jk1w`. Now a refinement of `cpip` (the interface IS lojix-ordinary), not a sibling. |
| `tvbn` | Direct: lojix is the traditional component receiving the full triad-engine; folding testing onto its ordinary face finishes the lean shape and avoids spawning a parallel component to retire later. |
| `g7yd` | `DurableVm` resolved by `NodeService::VmHost` capability via the projection, never the agent's host; `HostRequirement` is a capability requirement; `NoCapableHost` honest reply. |
| `77ic` | `DurableVm` IS the durable on-demand TestVm on a `VmHost` node; `Activation=BootOnce`; not booted by default; host untouched. The existing `TestMode::Live` path. |
| `7let`/`se72` | Containment IS the testing safety property the reframe generalizes from `7let`: deploy a full OS into a throwaway target, host untouched. `Hermetic` is the CI proof; `DurableVm`/`CloudDroplet` go all-the-way. |
| `qkvx` | Every knob a closed enum or typed newtype; `PropagationBody` a typed variant, never a command string; `ContainedTarget` a real enum (real horizon `NodeService::VmHost`), not a string-keyed hack. |
| `0a9p` | `DurableVm`/`Hermetic` deploy via lojix build-on-target so model closures realize in the target store; heavy work stays on prometheus/AI node. |
| `lt44` | `HermeticProfile.NetworkIsolation [SharedHost TapLayer3 CrossMachine]`; vsock deferred. The lightweight-sandbox end of the weight axis. |
| `88eq` | Hermetic builds from a committed revision (commit-first); the runner snapshots off `@` rather than draining the shared working copy (156's accepted fix). |
| `2f04` | The ordinary signal root is a >1-variant interface enum; `ContainedTarget` and `PropagationBody` are nested payload enums — real interface depth, not a single-op newtype. |
| `component-triad` / one-argument-daemon | No new triad; lojix's existing triad gains the ordinary `Test` op. CLI takes one NOTA arg → lojix-daemon only; daemon takes one rkyv startup msg, no flags. The `CloudDroplet` substrate makes lojix a `meta-signal-cloud` client (the only multi-peer reach), legitimate for a daemon. |
| `y1v5`/`cncj`/`8f8e` | GPU/display is a FOURTH `ContainedTarget` variant, design-deferred until `horizon-rs` `NodeService` gains a typed VFIO/display capability (`qkvx` — no string hack now). |

## Spirit gate for this study

THE NEW DECISION was captured this turn (referents lojix signal-lojix
meta-signal-lojix). This report is its design elaboration — no sibling
Record. Two edits the psyche should confirm, because the reframe SUPERSEDES
prior intent rather than extending it:

1. `cpip` reads as REFINED by the reframe (the "one reusable interface for
   testing" IS lojix's ordinary contract). Candidate: a `Clarify` on `cpip`
   stating the interface is lojix-ordinary, deployment is lojix-meta — NOT a
   new Record. Confirm before editing.
2. `vudl` (and `cgd8`) currently say "Test is owner-only, lives in
   meta-signal-lojix." The reframe moves `Test` to ordinary. Candidate: a
   `Supersede`/`Clarify` on `vudl` narrowing the meta authority split to
   `Deploy`/`Pin`/`Unpin`/`Retire` and placing `Test` on ordinary. This is a
   genuine intent conflict — flag, do not silently override.

## Open questions for the psyche

1. Confirm the `cpip` Clarify and the `vudl` Supersede/Clarify above before
   any Spirit edit (refine-vs-supersede is the psyche's call).
2. Verb naming: `Test`/`ObserveRun`/`Collect`/`Validate` on the ordinary
   root — or fold `ObserveRun` into the existing `Query (ByTestRun …)`
   selection (it already exists at signal-lojix `:103`)? Reusing `Query`
   avoids a redundant verb; a distinct `ObserveRun` reads cleaner. I lean
   reuse `Query`.
3. `ContainedTarget` vs keeping the existing name `TestMode` widened? The
   reframe's safety-property framing argues for `ContainedTarget` (it names
   WHY it is ordinary); the existing `TestMode` is entrenched in the daemon.
4. Does the production `Deploy` (meta) also deserve a contained-vs-production
   TYPE marker for symmetry, or is "meta = production" sufficient because the
   socket authority already carries it? The reframe says the split itself is
   the boundary, suggesting no extra marker is needed.
