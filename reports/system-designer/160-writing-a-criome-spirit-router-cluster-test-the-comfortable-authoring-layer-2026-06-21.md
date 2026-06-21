# Writing a criome/spirit/router cluster test — the comfortable authoring layer over lojix's contained contract

*System-designer study · 2026-06-21 · report 160*

This delivers the thing the psyche asked to see: **how you write a criome/spirit/router cluster test**, in an easy public interface, in *correct* NOTA, lowering to the operator's actual contained contract. It folds in two psyche corrections from this turn.

## Two corrections folded in

**NOTA, done right (the important one).** `TestDescriptor`, `Steps`, `KeyMember`, `MaximumGuests` are **variants**, not labels. My earlier sketch sprinkled `(NetworkIsolation TapLayer3) (MaximumGuests 3) (Lease 900)` as if they were optional named fields — that is the `(key value)` shape NOTA forbids. The corrected discipline, taken from the deployed `signal-lojix` schema:

- **A shorthand is a terser sibling *variant* the daemon lowers** — the established idiom is `TestRequest [(Run TestRun) (Check QuickCheck)]`, where `Check` is the terse variant `TestDefaults::lower` expands. NOTA forbids tail-omission, so a shorter form is always its own variant, never an under-filled struct.
- **Option-setting is a `(Vec OptionEnum)` of option-variants** — `(MaximumGuests 3)` is a *variant* of an option enum collected in a vector: order-free, omittable (empty vector = all defaults), fully typed. Not a labeled field.
- **Struct bodies are positional and untagged** (`DatabaseMarker { CommitSequence * StateDigest * }` → value `(<seq> <digest>)`, no head); **enum variant values carry a head** (`(OnHost atlas)`); optionals are `None` / `(Some x)`; an enum-variant payload that is a struct nests in its own parens (`(Record (<entry> <justification>))`).

**Don't block on questions.** A directive to implement and show *is* the answer — act on the recommendation, deliver, make choices reversible. Captured as Spirit `ki6i`. This report is the delivery, not a question.

## Aligning with the operator's contract (already built)

The operator's `system-operator-contained-test-poc` branch already carries the corrected ordinary contract — I align to it rather than duplicate:

```
roots  [DeployContained CheckContained Release Query WatchDeployments WatchCacheRetention Unwatch CheckHostKeyMaterial]
NodeProfile     { ClusterName * NodeName * kind (Optional DeploymentKind) }   ;; the SAFE build profile — audit 234's split, implemented
ContainedTarget [HermeticVm (VmHostGuest VmHostGuestTarget) (EphemeralDroplet EphemeralDropletTarget)]
DeployContainedRequest { NodeProfile * ContainedTarget * source ProposalSource flake FlakeReference }
ContainedCheck   { TestRunIdentifier * }      ;; CheckContained — operator chose this over VerifyContained
ContainedRelease { TestRunIdentifier * }
```

Two facts that shape the authoring layer: (1) `DeployContained` is **per node** — one `NodeProfile`, one `ContainedTarget`; a cluster is N deploys + N checks + N releases. (2) `ContainedCheck` today takes only a run id — the daemon runs a fixed integrity check; a *typed verification body on the wire* is the later wave (report 158's wave-3). So the verification vocabulary below is the authoring target the daemon grows into; the lowering runs the standard gate until then.

## The criome/spirit/router cluster test — short common case

```nota
;; cluster-gate.nota   —   lojix cluster-gate.nota
(RunContainedCluster (fieldlab [(Member criome) (Member spirit) (Member router)] HermeticVm Gate []))
```

Every token is typed, positional, variant-headed: `RunContainedCluster` (request-root variant) carries one `ClusterRun` struct `(fieldlab [...] HermeticVm Gate [])` — `fieldlab` the `ClusterName`; a vector of `MemberProfile` variants; `HermeticVm` the bare `ContainedTarget` variant; `Gate` the bare `VerificationBody` shorthand (= the standard criome three-case gate); `[]` the empty `ClusterOption` vector (all defaults). One line, and the daemon lowers it to three `DeployContained`/`CheckContained`/`Release` triples.

## The same test — full form (options set, explicit steps)

```nota
(RunContainedCluster
  (fieldlab
    [(Member criome) (Member spirit) (Kinded router OsOnly)]   ;; members: terse Member, or Kinded with a DeploymentKind
    HermeticVm
    (Steps [
      (GateCase Criome AuthorizedShips      (Threshold 1 [(Signer spirit-local-signer)]))
      (GateCase Criome ThresholdShortDenied (Threshold 1 [(Signer spirit-local-signer)]))
      (GateCase Criome UnconfiguredHeld     NoGate)
      (Probe (OutboxDrained Spirit ServerCommitted))
      (Probe (RouterFanOut Router AttendPublishDeliverMatching))
      (DeployIntegrity Criome) (DeployIntegrity Spirit) (DeployIntegrity Router)])
    [(Lease 900) (MaximumGuests 3) (NetworkIsolation TapLayer3)]))   ;; options: a Vec of ClusterOption VARIANTS
```

The options are a **vector of `ClusterOption` variants** — `(Lease 900)`, `(MaximumGuests 3)`, `(NetworkIsolation TapLayer3)` — not labeled fields; drop any to take its default, reorder freely. The body is the `Steps` variant carrying a `Vec TestStep`; each step is a variant. This is the corrected NOTA.

## The authoring-layer schema (lowers to the operator's contract)

A small addition that reuses the operator's `NodeProfile` / `ContainedTarget` / `DeploymentKind` / `ProposalSource` / `FlakeReference` verbatim and adds only the cluster + verification vocabulary:

```
RunContainedCluster ClusterRun
ClusterRun { ClusterName * members (Vec MemberProfile) ContainedTarget * VerificationBody * options (Vec ClusterOption) }

MemberProfile   [(Member NodeName) (Kinded NodeName DeploymentKind)]          ;; terse, or kinded
VerificationBody [Gate (Steps (Vec TestStep))]                                ;; Gate = the 3-case shorthand
TestStep        [(GateCase ComponentKind GateOutcome ThresholdSpec) (Probe ProbeSpec) (DeployIntegrity ComponentKind)]
ComponentKind   [Criome Spirit Router]
GateOutcome     [AuthorizedShips ThresholdShortDenied UnconfiguredHeld]
ThresholdSpec   [NoGate (Threshold Integer (Vec KeyMember))]
KeyMember       [(Signer NodeName)]
ProbeSpec       [(OutboxDrained ComponentKind Durability) (RouterFanOut ComponentKind RouterCheck)]
Durability      [QueuedForMirror ServerCommitted]
RouterCheck     [AttendPublishDeliverMatching]
ClusterOption   [(Lease PositiveSeconds) (MaximumGuests Integer) (NetworkIsolation NetworkIsolation) (Source ProposalSource) (Flake FlakeReference)]
PositiveSeconds Integer                                                       ;; newtype; daemon rejects zero
NetworkIsolation [SharedHost TapLayer3 CrossMachine]
```

`RunContainedCluster` is a terse sibling root the daemon lowers — exactly the `TestRequest [(Run …) (Check …)]` / `TestDefaults::lower` idiom, not an under-filled request.

## How it lowers

For each `MemberProfile` m the daemon emits, against the operator's contract:

```
DeployContained (NodeProfile fieldlab <m-name> <kind>) <ContainedTarget+options> <source> <flake>   -> TestRunIdentifier r
CheckContained  r                                                                                     -> phase/outcome (runs VerificationBody)
Release         r
```

`Gate` lowers to the daemon's standard criome three-case integrity; `Steps` lowers to each step (today via the fixed check, wire-typed in wave-3). `Member` → `kind None` → `FullOs`; `Kinded n k` → that kind. Cluster-wide `ClusterOption`s fill the per-node `ContainedTarget`/source/flake defaults.

## Querying state back — same grammar

```nota
(Query (ByTestRun (TestRunLookup fieldlab criome (Some 7))))   ;; one run
(Query (ByTestRun (TestRunLookup fieldlab criome None)))       ;; all runs for the node, newest first
```

One grammar for authoring and querying, learned once.

## Verb shape — response to operator audit 235

Audit 235 asks whether to split status from body-execution into `CheckContained` vs `VerifyContained`, or pick a different verb shape before it hardens. Recommendation:

- **Status is `Query`, not a verb of its own.** "What phase/outcome is run r in?" is a read — the ordinary `Query (ByTestRun (TestRunLookup …))` already answers it. A `CheckContained` whose job is status is exactly the audit's finding #3 (it inspects the store directly); route it through the sema-engine read path as `Observe`/`Query`, not a bespoke store-peek.
- **The body-executing verb is `VerifyContained`**, carrying the typed `VerificationBody` (`Gate` / `Steps`); it runs the body against a run and returns a verdict. This is report 158's thin-assert op, named off the Sema-class word `Assert`.
- **So the triple is `DeployContained` / `VerifyContained` / `Release`, status via `Query`** — `CheckContained` dissolves (status role → `Query`, execution role → `VerifyContained`-with-body). The authoring layer above lowers `Gate`/`Steps` to `VerifyContained`; `(Query (ByTestRun …))` reads status. One grammar, no conflated verb.

The audit's other findings (accepted; all in the operator's daemon domain):

- **`DeployContainedRequest.source` should be made authoritative, not removed** — a `NodeProfile` build resolves its closure from that proposal source, so lowering ignoring it is the bug; if the daemon defaults source from config, `source` is the per-request override (still authoritative when present).
- **`CheckContained`/`Release` peeking the store directly violates the signal/nexus/sema bar** — agreed; the read path is `Observe` through sema-engine, the release a typed effect, not a direct redb read.
- **The `live-deploy-test-chain` branch rehomes as `VmHostGuest`, not `TestMode::Live`** — agreed, and already report 158's wave-2; `TestMode` is deleted and containment is the `ContainedTarget` variant.
- **Wave-0 is still open.** The POC compiles by pinning `schema-next`, which dodges the live toolchain — so the codegen gate (ordinary `DeployContained` + meta `Deploy` routed to one pipeline with no shared target supertype) is *not yet proven*. That remains the real blocker before the verbs harden; proving it on the current toolchain outranks adding surface.

## Coordination and next step

The operator owns the per-node contract and daemon (`system-operator-contained-test-poc`); this comfortable cluster layer is the designer "demonstrate the shape" contribution that lowers to it. Next concrete step: land `RunContainedCluster` + the verification vocabulary on a designer worktree atop the operator's branch (or hand it to the operator to fold into the contract), and review the operator's daemon lowering as it lands. **Router feasibility:** if the router source still fails to compile against the new schema generator, the criome+spirit subset runs and `RouterFanOut` is the honest stub until that lands — the example does not fake a passing router.
