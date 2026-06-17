# 674.6 — Schema code: criome's limited typed policy language

*schema-author agent. The NOTA schema for criome's internal engine — the
object/verb vocabulary of a limited typed policy language over public-key
identity atoms (Spirit `vhs2`), built on `z9d6` content-addressed composable
authorization objects, criome auth-only (`wckt`), triad-consistent (criome's
Nexus vocabulary, not a fourth engine). Authored in the DEPLOYED schema-next
dialect and **validated** through the deployed compiler — see "Validation".*

## What this file is, and a note on the missing design file

The orchestrator's task pointed at `5-object-verb-design.md` as the design to
encode. **That file does not exist yet** — phase 2 (design-vocabulary) had not
landed when this agent ran (the directory holds only `0`–`4`). So the object/
verb vocabulary here is derived directly from the binding constraints (file `2`,
C1–C19), the existing-vocabulary ground truth (file `1`), and the two research
files (`3` chains, `4` primitives/reconciliation). Where file `5` later refines a
name or a field, this schema is the schema-author's faithful reconstruction of
the same design those inputs imply; reconcile on the same branch if `5` diverges.

The schema extends the deployed `signal-criome` contract. The closest existing
artifact — `criome/schema/criome.language.schema` + `criome/src/language.rs`
(the started POC, file `1` §f) — is the design pressure this converges on and
supersedes: it lifts that `Rule`/`Contract` evaluator into a wire vocabulary with
verb roots, content-addressing, replay/branch binding, weighted/time-varying
quorums, a first-class divergence object, and the oracle-resolution recursion.

## Dialect decision (load-bearing) — deployed `field Type`, not the `adnn` form

`skills/structural-forms.md` describes a positional struct body
(`Entry { Topics Kind Description }`, dot-differentiator `key.Type`) and says the
old `field Type` name-value form is "retired and rejected." **That retirement
lives only on the `next/structural-forms` epic branch.** The DEPLOYED
`/git/github.com/LiGoldragon/schema-next` is on `main` (commit "refresh nota
dependency"); it has **no** `RetiredStructFieldSyntax`, and the deployed
`signal-criome/schema/lib.schema` is written entirely in the `field Type` form
(`socket_path DaemonPath`). The task says explicitly: match the DEPLOYED
schema-next positional syntax and the rest of `lib.schema`. So this schema uses
the `field Type` name-value struct body, matching the deployed compiler and the
deployed sibling contracts. (When the structural-forms epic merges to criome,
this file migrates to `Type`/`key.Type` bodies in the same sweep — a mechanical
rewrite, no semantic change.)

## File location and shape

Proposed path: `signal-criome/schema/contract.schema` (a second module in the
ordinary working contract; cross-imports its own `lib` module for the identity
atoms). It is a standard schema-next file: optional import block, input-root
vector, output-root vector, then the type namespace. The verbs are the new
operation heads criome's Nexus engine accepts/emits for the policy language.

## The schema

```schema
;; criome.contract — the limited typed policy language over public-key
;; identity atoms (Spirit vhs2). A SELF-CONTAINED wire vocabulary that
;; cross-imports the deployed signal-criome identity atoms. It defines
;; content-addressed COMPOSABLE AUTHORIZATION OBJECTS (Spirit z9d6): an
;; AuthorizationObject is referenced by the blake3 digest of its own bytes,
;; and every reference between objects is a content-address reference
;; (AuthorizationObjectDigest), never a name into mutable state.
;;
;; This is NOT a general-purpose VM (vhs2 FIXED): the policy combinator set
;; is a closed taxonomy of public-key signatures, k-of-n quorums, time-locks,
;; time-varying thresholds, divergence-reconciliation, and oracle-resolution.
;; Evaluation is total and terminating by construction (no loops, no recursion
;; except the acyclic content-address DAG, no arithmetic VM). criome stays
;; auth-only (wckt): the verbs mint/compose/evaluate objects and verify
;; signatures; nothing here transports, routes, or version-controls.

{
  Identity signal-criome:lib:Identity
  BlsPublicKey signal-criome:lib:BlsPublicKey
  BlsSignature signal-criome:lib:BlsSignature
  SignatureScheme signal-criome:lib:SignatureScheme
  SignatureEnvelope signal-criome:lib:SignatureEnvelope
  ObjectDigest signal-criome:lib:ObjectDigest
  ReplayNonce signal-criome:lib:ReplayNonce
  TimestampNanos signal-criome:lib:TimestampNanos
  RequiredSignatureThreshold signal-criome:lib:RequiredSignatureThreshold
}

[(ComposeObject ObjectComposition)
 (EvaluateAuthorization AuthorizationEvaluation)
 (ResolveDivergence DivergenceResolution)
 (SubmitOracleVerdict OracleVerdictSubmission)
 (VerifyAuthorizationProof AuthorizationProofVerification)]

[(ObjectComposed ComposedObjectReceipt)
 (AuthorizationDecided AuthorizationDecision)
 (DivergenceResolved DivergenceReconciliation)
 (OracleVerdictAccepted OracleVerdictReceipt)
 (ProofVerified ProofVerificationResult)
 (ContractRejected ContractRejection)]

{
  ;; ============================================================
  ;; The atom: a public key is the irreducible unit of identity.
  ;; Above it everything composes. There is no identity below the key.
  ;; ============================================================
  IdentityAtom {
    public_key BlsPublicKey
    scheme SignatureScheme
  }

  ;; A content address: the blake3 digest of a composable object's own bytes.
  ;; A reference between objects is ALWAYS this digest (z9d6), never a name.
  AuthorizationObjectDigest {
    value ObjectDigest
  }

  ;; The TIME ATOM. Time enters the language only as interval selection over
  ;; a declared schedule (research file 4) — never as general arithmetic.
  ;; The default time source is the daemon's attested wall clock (TimestampNanos);
  ;; the trustless-delay (VDF) option is deferred (open question, report 5).
  Moment {
    value TimestampNanos
  }

  ;; Tezos three-part replay/branch binding (research file 3): a quorum
  ;; gathered on one side of a network split cannot be replayed on the other.
  BranchIdentity {
    value ObjectDigest
  }
  PolicyVersion {
    value Integer
  }
  ReplayBinding {
    object AuthorizationObjectDigest
    branch BranchIdentity
    version PolicyVersion
    nonce ReplayNonce
  }

  ;; ============================================================
  ;; The composable authorization object (z9d6 spine).
  ;; A keyless identity whose "signature" is the satisfaction of its policy
  ;; (Solana PDA, research file 3). Its address is the digest of its bytes.
  ;; The Policy is the closed combinator taxonomy — the whole limited language.
  ;; ============================================================
  AuthorizationObject {
    policy Policy
    binding ReplayBinding
  }

  ;; The CLOSED policy combinator set. No Unknown, no user code.
  ;; Every reference to a sub-object is by content-address (acyclic DAG),
  ;; so evaluation is total and terminating by construction (vhs2 FIXED).
  Policy [
    (Atom IdentityAtom)
    (Reference AuthorizationObjectDigest)
    (Quorum Quorum)
    (TimeLock TimeLock)
    (TimeVaryingThreshold TimeVaryingThreshold)
    (Conjunction PolicyConjunction)
    (Disjunction PolicyDisjunction)
    (Reconciliation ReconciliationPolicy)
  ]

  ;; ----- Quorum: k-of-n over public-key atoms, weighted (Tezos), nestable
  ;; (Gnosis Safe). A member is itself an atom OR another object by digest,
  ;; composing recursively + acyclically. weight=1 is flat k-of-n.
  WeightedMember {
    member PolicyMember
    weight MemberWeight
  }
  MemberWeight {
    value Integer
  }
  PolicyMember [
    (KeyMember IdentityAtom)
    (ObjectMember AuthorizationObjectDigest)
  ]
  Quorum {
    required_weight RequiredSignatureThreshold
    members (Vector WeightedMember)
  }

  ;; ----- Time-lock: an inner policy is active only inside a time window
  ;; (OpenZeppelin TimelockController). Either bound is optional, so this
  ;; expresses ActiveAfter (not_before set), ActiveUntil (not_after set),
  ;; or a bounded window. A separate veto quorum may cancel before maturity.
  TimeLock {
    inner_object AuthorizationObjectDigest
    not_before (Optional Moment)
    not_after (Optional Moment)
    veto_quorum (Optional AuthorizationObjectDigest)
  }

  ;; ----- Time-varying threshold: required weight is a step-function over a
  ;; piecewise time schedule (vhs2 "thresholds that increase or decrease over
  ;; elapsed time"; research file 4). Decreasing = dead-man/recovery;
  ;; increasing = decaying delegation that must be renewed. Time enters only
  ;; as interval selection — no arithmetic VM.
  ThresholdPhase {
    activates_at Moment
    required_weight RequiredSignatureThreshold
  }
  TimeVaryingThreshold {
    members (Vector WeightedMember)
    initial_weight RequiredSignatureThreshold
    phases (Vector ThresholdPhase)
  }

  ;; ----- Boolean composition over sub-objects (referenced by digest).
  PolicyConjunction {
    objects (Vector AuthorizationObjectDigest)
  }
  PolicyDisjunction {
    objects (Vector AuthorizationObjectDigest)
  }

  ;; ============================================================
  ;; Divergence-reconciliation (vhs2, first-class). When two networks split,
  ;; the language expresses both the divergence FACT and how reconciliation
  ;; is determined. Tezos self-amendment shape (research file 3): a tentative
  ;; weight-based winner vs a finalized quorum-gated resolution, with an
  ;; explicit terminal fork (Augur, research file 4) when no convergence.
  ;; ============================================================

  ;; The divergence fact: two named branches that diverged from a common base.
  NetworkBranch {
    branch BranchIdentity
    head AuthorizationObjectDigest
    attestation_weight MemberWeight
  }
  Divergence {
    common_base AuthorizationObjectDigest
    branches (Vector NetworkBranch)
    observed_at Moment
  }

  ;; How reconciliation is determined. A ReconciliationPolicy is itself a
  ;; Policy variant, so it composes like any other authorization object.
  ReconciliationMethod [
    (HeaviestBranch HeaviestBranchRule)
    (Quorum AuthorizationObjectDigest)
    (Oracle OracleResolution)
    (TerminalFork TerminalFork)
  ]
  ;; Automatic weight-based liveness winner (Gasper LMD-GHOST analogue).
  HeaviestBranchRule {
    minimum_weight MemberWeight
  }
  ;; Explicit recorded split into two self-consistent realities — a terminal
  ;; state, not a failure (Augur fork-as-last-resort).
  TerminalFork {
    branches (Vector BranchIdentity)
  }
  ReconciliationPolicy {
    divergence Divergence
    method ReconciliationMethod
    finality_quorum AuthorizationObjectDigest
  }

  ;; ============================================================
  ;; Oracle resolution. The language NEVER invokes an LLM; it VERIFIES a
  ;; quorum-signed, content-addressed verdict object (Chainlink OCR template,
  ;; research file 4). The oracle PROVIDER is itself an AuthorizationObject —
  ;; e.g. a paid expert panel as a k-of-n quorum (vhs2) — so the recursion
  ;; "the oracle resolves through one of those identity contracts" is visible
  ;; in the type: provider_contract is an AuthorizationObjectDigest.
  ;; ============================================================

  ;; The exact, content-addressed question put to the oracle. Pure of declared
  ;; inputs (EigenAI determinism, research file 4): the verdict is a function
  ;; of (provider, prompt digest, model measurement, decode policy).
  OracleQuery {
    divergence Divergence
    prompt_digest AuthorizationObjectDigest
  }
  ModelMeasurement {
    value ObjectDigest
  }
  DecodePolicy {
    value ObjectDigest
  }
  ;; The opaque verdict object that re-enters the language. Accepted iff the
  ;; provider_contract's quorum proof verifies over it.
  OracleVerdict {
    query OracleQuery
    provider_contract AuthorizationObjectDigest
    model_measurement ModelMeasurement
    decode_policy DecodePolicy
    chosen_branch BranchIdentity
    quorum_proof QuorumProof
  }
  ;; The reconciliation-policy variant that delegates to an oracle. The verb
  ;; is verify-attestation, never invoke-model. challenge_window keeps the
  ;; optimistic-acceptance + dispute backstop (EigenAI fraud-proof model).
  OracleResolution {
    provider_contract AuthorizationObjectDigest
    query OracleQuery
    challenge_window Moment
  }

  ;; ============================================================
  ;; Proofs / evidence. A QuorumProof is the content-addressable record of
  ;; "these signers attested this object" — a list of envelopes (uncompressed)
  ;; or a single aggregated BLS signature (transparent aggregate). The
  ;; evaluator checks the proof against the object's policy, totally.
  ;; ============================================================
  AggregationDiscipline [ListedSignatures AggregatedBls SingleKey]
  QuorumProof {
    discipline AggregationDiscipline
    object AuthorizationObjectDigest
    binding ReplayBinding
    signatures (Vector SignatureEnvelope)
  }

  ;; The complete evidence the evaluator decides over: the proof plus the
  ;; moment of evaluation (selects the active time-varying phase) plus any
  ;; accepted oracle verdicts referenced by the reconciliation policy.
  Evidence {
    proof QuorumProof
    evaluated_at Moment
    oracle_verdicts (Vector OracleVerdict)
  }

  ;; ============================================================
  ;; VERB PAYLOADS — Input roots.
  ;; ============================================================

  ;; Mint/compose a new content-addressed authorization object. criome returns
  ;; its digest; the object becomes referenceable by other objects (z9d6).
  ObjectComposition {
    object AuthorizationObject
    composed_by Identity
  }

  ;; Evaluate whether the evidence satisfies the named object's policy.
  ;; This is the pure, side-effect-free validation predicate (ERC-4337
  ;; validate/execute split made absolute) — criome's whole identity.
  AuthorizationEvaluation {
    object AuthorizationObjectDigest
    evidence Evidence
    requester Identity
  }

  ;; Open / advance a divergence-reconciliation over a recorded split.
  DivergenceResolution {
    reconciliation ReconciliationPolicy
    requester Identity
  }

  ;; Submit a quorum-signed oracle verdict for verification + acceptance.
  OracleVerdictSubmission {
    verdict OracleVerdict
    submitter Identity
  }

  ;; Verify a standalone quorum proof against an object (no decision side-effect).
  AuthorizationProofVerification {
    object AuthorizationObjectDigest
    proof QuorumProof
  }

  ;; ============================================================
  ;; VERB PAYLOADS — Output roots.
  ;; ============================================================

  ComposedObjectReceipt {
    digest AuthorizationObjectDigest
    composed_at Moment
  }

  ;; criome verifies bytes + principal; the consumer keeps the semantic
  ;; verdict (2st7 C11). So the decision is a cryptographic/mechanical fact.
  Verdict [Authorized Rejected]
  AuthorizationDecision {
    object AuthorizationObjectDigest
    verdict Verdict
    satisfied_members (Vector PolicyMember)
    active_required_weight RequiredSignatureThreshold
    decided_at Moment
  }

  ;; The resolved reconciliation: which branch won and how it was determined.
  ReconciliationOutcome [
    (BranchSelected BranchIdentity)
    (ForkRecorded TerminalFork)
    (AwaitingOracle OracleQuery)
  ]
  DivergenceReconciliation {
    divergence Divergence
    outcome ReconciliationOutcome
    finalized_by AuthorizationObjectDigest
    resolved_at Moment
  }

  OracleVerdictReceipt {
    verdict_digest AuthorizationObjectDigest
    accepted_at Moment
  }

  ProofVerificationResult {
    object AuthorizationObjectDigest
    verdict Verdict
    verified_at Moment
  }

  ;; ============================================================
  ;; Rejections — closed taxonomy, no Unknown (C6 typed-and-closed).
  ;; ============================================================
  ContractRejectionReason [
    MalformedObject
    UnknownObjectReference
    CyclicObjectReference
    UnsupportedSignatureScheme
    QuorumNotSatisfied
    OutsideTimeWindow
    ReplayBindingMismatch
    DivergenceUnresolvable
    OracleVerdictUnverified
    OracleProviderUnauthorized
    ReconciliationFinalityUnmet
  ]
  ContractRejection {
    reason ContractRejectionReason
  }
}
```

## Object/verb walk-through (how each piece satisfies a constraint)

| Schema object | Encodes | Constraint |
|---|---|---|
| `IdentityAtom` | the public key as the irreducible identity unit | C3 |
| `AuthorizationObjectDigest` | content-address reference; every object→object link | C1, z9d6 |
| `AuthorizationObject` (`policy` + `binding`) | the keyless composable object, addressed by its bytes | C1, Solana-PDA transfer |
| `Policy` enum (8 closed variants) | the whole limited combinator language; no `Unknown` | C5, C6 (FIXED) |
| `Quorum` + `WeightedMember` + `PolicyMember` | k-of-n, weighted, nestable (member = atom *or* object digest) | C4(a), z9d6 composition |
| `TimeLock` (optional bounds + veto quorum) | ActiveAfter / ActiveUntil / window; cancel-before-maturity | C4(b), OZ/Squads |
| `TimeVaryingThreshold` + `ThresholdPhase` | required weight as a step-function over time intervals | C4(b) (the `vhs2`-specific ask) |
| `Divergence` + `NetworkBranch` | the first-class divergence FACT (two diverged branches) | C15 |
| `ReconciliationPolicy` + `ReconciliationMethod` | how reconciliation is determined: weight / quorum / oracle / fork | C15, Tezos self-amendment |
| `OracleResolution` + `OracleVerdict` (`provider_contract`) | oracle delegation where the provider is itself an auth object | C16 (the recursion) |
| `QuorumProof` + `Evidence` | content-addressable proof the evaluator decides over | C9, C10 |
| `ReplayBinding` (object/branch/version/nonce) | a proof valid on one branch can't replay on the other | Tezos 3-part binding |
| Input roots (5 verbs) | compose / evaluate / resolve / submit-verdict / verify | C7 auth-only, C2 |
| `AuthorizationDecision` (`Verdict`) | a cryptographic/mechanical fact, not a semantic verdict | C11 |
| `ContractRejection` | closed rejection taxonomy | C6 |

### Why these verbs, and not transport verbs (C7)

The five input roots are `ComposeObject`, `EvaluateAuthorization`,
`ResolveDivergence`, `SubmitOracleVerdict`, `VerifyAuthorizationProof`. Every one
mints, composes, evaluates, or verifies an object/proof. **None moves bytes,
delivers a message, fetches, or version-controls** — that is router/mirror, kept
out by construction (`wckt` FIXED). `EvaluateAuthorization` is the pure,
side-effect-free validation predicate: ERC-4337's `validateUserOp` promoted to
the whole language (research file 3, the keystone transfer).

### The z9d6 composition, shown

A k-of-n quorum is not a primitive beside the objects — it *is* a composable
object: `Quorum.members` is `(Vector WeightedMember)`, and a `WeightedMember`'s
`PolicyMember` is either a `KeyMember` (a leaf atom) or an `ObjectMember`
(another object **by digest**). A time-window policy `TimeLock.inner_object` is a
digest. A reconciliation `finality_quorum` is a digest. So threshold / majority /
time-window all *emerge from composition over content-addressed objects* (C2),
exactly as `z9d6` demands — never bolted on as parallel features.

### The oracle recursion, shown in the type

`OracleResolution.provider_contract` and `OracleVerdict.provider_contract` are
both `AuthorizationObjectDigest`. The oracle provider *is* an authorization
object — a paid expert panel is a `Quorum`, addressed by its digest. The verdict
is accepted iff its `quorum_proof` verifies against that provider object. criome
never invokes a model; it verifies a quorum-signed, content-addressed verdict
(C16; Chainlink-OCR template). The PoC (file `7`) stubs the model call but the
recursion is structural, not stubbed.

## Validation — HONEST status: it parses, lowers, and resolves imports

**Validated against the DEPLOYED compiler.** I located the compiler at
`/git/github.com/LiGoldragon/schema-next` (on `main`, "refresh nota dependency";
no standalone CLI, so I drove the library API). Two levels, both green:

1. **Parse + lower** via `SchemaSourceArtifact::from_schema_text` — the schema
   parses and lowers with no error.
2. **Cross-import resolution** via `SchemaEngine::lower_source_with_resolver`
   with a real `ImportResolver::with_dependency("signal-criome",
   /git/.../signal-criome/schema, "0.1.0")` — every `signal-criome:lib:*` import
   genuinely resolves against the real deployed `signal-criome/schema/lib.schema`.
   Probed types (`AuthorizationObject`, `Policy`, `ReconciliationPolicy`,
   `OracleVerdict`, `Evidence`) all report **declared**.

**Negative control** (to prove the check is meaningful, not a no-op): renaming
one import to `signal-criome:lib:NoSuchTypeHere` makes the resolver fail with
`ImportedTypeNotFound { crate_name: "signal-criome", module: "lib", type_name:
"NoSuchTypeHere" }`. So the passing run is a real resolution, not an unchecked
parse.

**Baseline control:** the existing deployed `signal-criome/schema/lib.schema`
parses through the same harness (`OK`), confirming the dialect/harness are right.

The throwaway validation harness lives at `/tmp/criome-schema-validate/`
(`validate.rs`, `validate_resolved.rs`, `examples/criome.contract.schema`); it is
not committed.

### What validation does NOT cover (honest limits)

- **Acyclicity** of the content-address reference DAG (a `Policy::Reference` /
  `TimeLock.inner_object` / `Conjunction.objects` graph) is an **evaluator**
  invariant, not a schema-expressible one. The schema *names* the failure
  (`CyclicObjectReference`) but cannot prevent a cycle structurally; the PoC's
  evaluator (file `7`) must reject cycles and bound recursion depth, which is what
  makes evaluation total (C5). Content-addressing makes natural cycles
  impossible (a hash can't reference its own future hash) but the schema does not
  *enforce* that the digests are honestly derived.
- **Dialect drift:** authored in the deployed `field Type` form. When
  `next/structural-forms` reaches criome this migrates to the positional
  `Type` / `key.Type` body form — mechanical, no semantic change.

## Open questions carried to file `5`/`8`

1. **Module vs. file.** Proposed as `signal-criome:contract` (a second module).
   Alternative: fold the policy types straight into `signal-criome:lib` and
   retire `criome.language.schema`. The composition/evaluation verbs could also
   be argued onto the **meta** plane (policy mutation is meta-class, file `1` §c)
   — but evaluation is ordinary trust traffic, so the ordinary contract is the
   better home. Confirm in `5`.
2. **Time source.** `Moment` wraps `TimestampNanos` (attested wall clock). The
   VDF/trustless-delay option (research file 4 §A.5) for the adversarial
   no-trusted-clock case is deferred — flag whether divergence disputes need it.
3. **Oracle determinism strength.** `OracleVerdict` carries `model_measurement`
   + `decode_policy` to *permit* bit-reproducible re-execution, but the default
   posture is signed-verdict-only (research file 4 §B.4). Confirm criome requires
   only the quorum-signed verdict, with re-execution as the dispute backstop.
4. **`MemberWeight`/`PolicyVersion` as `Integer` newtypes** — they wrap `Integer`
   matching the deployed `RequiredSignatureThreshold { value Integer }` pattern.
   Per the dimensional principle (`ov30`) these are correctly distinct roles.
5. **SEMA family.** This vocabulary needs a `criome-contract` SEMA family (file
   `1` gap 1) keyed by `AuthorizationObjectDigest`; that is daemon-side (criome
   repo), out of the wire schema but named here for file `7`/`8`.
```
