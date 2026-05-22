# 141 — criome triad audit (BLS auth + attestation substrate)

*Audit of the criome triad: `criome` runtime (daemon + thin CLI),
`signal-criome` working contract, and the MISSING owner-signal-criome
policy contract. Addresses the /150 §6.9 open question on whether
`signal-criome` should split by relation/authority surface (identity /
attestation-authorization / peer-signing). Proposes the owner-signal
shape.*

## 0 · TL;DR

The criome triad is **two legs of three present**, but the present
two are stale on every workspace pattern surveyed in /257 and /258:

- `signal-criome` still depends on `signal-core` (retired in favour
  of `signal-frame`), still uses universal-verb prefixes
  (`Assert / Validate / Retract / Match / Subscribe`) at the contract
  layer, still carries the `AuthorizedSignalVerb` enum that the
  three-layer model retired, still has `TimestampNanos(u64)`
  single-field nanosecond timestamps, and uses the
  `request CriomeRequest { ... }` shape rather than the current
  `operation Verb(Payload)` grammar.
- The `criome` daemon does not use `signal-executor`; the request
  path is a hand-rolled `match` in `CriomeRoot::submit` dispatching
  to per-actor messages. There is no `Lowering`, no
  `CommandExecutor`, no `ToSemaOperation` / `ToSemaOutcome`
  projections, no `BatchErrorClassification`.
- `owner-signal-criome` does not exist. The criome architecture
  describes substantial owner-only operations — passphrase
  submission, master-key operations, policy mutation, peer-route
  mutation, escalation-to-approve prompts/replies, owner-session
  ECDH/AEAD envelope — but no contract crate carries them. The
  daemon binds its socket with mode `0600` and reads
  `CRIOME_SOCKET` from the environment, but it currently exposes
  exactly one socket and runs only the working contract.
- The thin CLI invariants are violated: the `criome` daemon binary
  reads `CRIOME_SOCKET` (daemons cannot read environment
  variables per `intent/component-shape.nota` 2026-05-20T13:00:00Z);
  there is no `criome` thin CLI binary as a separate `src/bin/`
  artifact.

**On the split question (per /150 §6.9 + §8).** Designer
recommendation: **do not split `signal-criome` into multiple
contract crates today.** The recommendation reasoning is in §2.1;
the short form is that the three relations the report names
(identity / attestation-authorization / peer-signing) share types
through `Identity`, `ObjectDigest`, `ContentReference`, and
`AuthorizationGrant` so deeply that splitting would mostly produce
cross-crate imports of the same shared vocabulary, not independent
contract crates. Use Rust modules inside one `signal-criome` crate to
express the relation seams, per the
`intent/component-shape.nota` 2026-05-21T10:30:00Z guidance
(modules disambiguate, not macro prefix knobs).

**Priority order for the next migration slice** (mirrors the
spirit / engine-manager template from /258):

1. Cut the contract over to `signal-frame` and the
   `operation Verb(Payload)` grammar; drop the
   `AuthorizedSignalVerb` enum (it is now part of the
   `SignalCallAuthorization` payload, not a separate Sema-classification surface).
2. Reshape the request tree: lift `Attest*` family into a `Attest`
   parent; lift `Authorize*` flow into authorization-relation
   operations under one or two parents; lift `*Identity` family
   under an `Identity` parent.
3. Create `owner-signal-criome` with the owner-class operations
   described in `criome/ARCHITECTURE.md` §Authorization model and
   §Security model.
4. Migrate the daemon onto `signal-executor` with a typed
   `CriomeCommand` / `CriomeEffect` pair; the existing per-actor
   message types become the lower-layer `CriomeCommand` variants.
5. Add the observable block question — see §2.5 (open psyche
   question: is criome a "persona component" under the
   2026-05-21T10:00:00Z "debug the debugger" rule?).

## 1 · /257 findings status

`signal-criome` is the unmigrated case named in
/257 §1.1 ("Old universal-verb shape"; signal-criome listed
explicitly) and in /257 row "signal-criome" of the migration
status table ("still on signal_core; old shape").

### /257 §1.1 — Old universal-verb shape

**Status: NOT FIXED.** `signal-criome/src/lib.rs:846-864` still
declares the channel in the pre-/238 grammar:

```text
request CriomeRequest {
    Assert Sign(SignRequest),
    Validate VerifyAttestation(VerifyRequest),
    Assert RegisterIdentity(IdentityRegistration),
    Retract RevokeIdentity(IdentityRevocation),
    Match LookupIdentity(IdentityLookup),
    Assert AttestArchive(ArchiveAttestationRequest),
    Assert AttestChannelGrant(ChannelGrantAttestationRequest),
    Assert AttestAuthorization(AuthorizationAttestationRequest),
    Assert AuthorizeSignalCall(SignalCallAuthorization),
    Subscribe ObserveAuthorization(AuthorizationObservation) opens AuthorizationObservationStream,
    Validate VerifyAuthorization(AuthorizationVerification),
    Assert RouteSignatureRequest(SignatureSolicitationRoute),
    Assert SubmitSignature(SignatureSubmission),
    Assert RejectAuthorization(AuthorizationRejection),
    Subscribe SubscribeIdentityUpdates(IdentitySubscription) opens IdentityUpdateStream,
    Retract IdentitySubscriptionRetraction(IdentitySubscriptionToken),
    Retract AuthorizationObservationRetraction(AuthorizationObservationToken),
}
```

Seventeen request variants, every one Sema-verb-prefixed. The
contract's `MUST IMPLEMENT` block in
`signal-criome/ARCHITECTURE.md:18-66` already names this migration
and lists rename candidates; nothing has landed.

### /257 §1.2 — Doubling smell

**Status: PRESENT and severe.** Five sites:

- `Validate VerifyAttestation(VerifyRequest)` — Validate verb,
  VerifyAttestation variant, VerifyRequest payload. Triple-stuttered.
- `Match LookupIdentity(IdentityLookup)` — Match verb,
  LookupIdentity variant, IdentityLookup payload.
- `Subscribe ObserveAuthorization(AuthorizationObservation)` —
  Subscribe verb, ObserveAuthorization variant,
  AuthorizationObservation payload.
- `Subscribe SubscribeIdentityUpdates(IdentitySubscription)` — Subscribe
  twice plus IdentitySubscription payload.
- `Retract IdentitySubscriptionRetraction(IdentitySubscriptionToken)`
  — Retract verb, *SubscriptionRetraction variant, *SubscriptionToken
  payload. Same pattern repeated for the authorization-observation
  stream close.

The contract's `MUST IMPLEMENT` block (lines 30-37) names some of
these renames (`VerifyAttestation → Verify`, payload renames) but
not all.

### /257 §1.4 — Repeated-suffix smell

**Status: SEVERE on multiple axes.**

Operations carry three repeated category clusters:

- `Attest*` cluster (3 siblings):
  `AttestArchive(ArchiveAttestationRequest)`,
  `AttestChannelGrant(ChannelGrantAttestationRequest)`,
  `AttestAuthorization(AuthorizationAttestationRequest)`. The
  Attest prefix is the parent operation; the suffix is the
  attestation kind. Per `intent/naming.nota`
  2026-05-19T18:55Z, the three siblings ask for a parent enum.
- `*Identity` cluster (3 siblings + 1 related):
  `RegisterIdentity`, `RevokeIdentity`, `LookupIdentity`, plus
  `IdentitySubscriptionRetraction`. The Identity suffix marks the
  read/write surface on the identity table.
- `Authorization*` / `*Authorization` mixed cluster: `AuthorizeSignalCall`,
  `ObserveAuthorization`, `VerifyAuthorization`,
  `RejectAuthorization`, `RouteSignatureRequest` (related),
  `SubmitSignature` (related), `AuthorizationObservationRetraction`.
  Five+ variants on one relation. The mix of prefix-style
  (`AuthorizeSignalCall`) and suffix-style (`ObserveAuthorization`)
  is itself diagnostic that the schema layer has not been pulled out.

Replies carry the same cluster pattern:

- `Authorization*` cluster (6 sibling reply variants):
  `AuthorizationPending`, `AuthorizationGranted`,
  `AuthorizationDenied`, `AuthorizationExpired`,
  `AuthorizationUnavailable`, `AuthorizationObservationSnapshot`.
  Five terminal-or-temporary outcome variants for one relation.
  Per /257 §1.4, these belong as variants under one parent enum
  (`AuthorizationOutcome` or similar) inside one reply variant
  (`Authorized(AuthorizationOutcome)`).
- `*Receipt` cluster: `SignReceipt`, `AttestationReceipt`,
  `SignatureRouteReceipt`, `SignatureSubmissionReceipt`,
  `IdentityReceipt`. Five sibling receipts.

The proposed migration shape in §2 lifts these.

### /257 §1.5 — Ancestry-prefixed type names

**Status: PRESENT.** Inside `signal-criome`:

- `CriomeRequest`, `CriomeReply`, `CriomeEvent` — these are
  macro-emitted from `channel Criome { ... }`. After the
  `signal-frame` migration + the clean-emit fix (per
  `intent/component-shape.nota` 2026-05-21T10:30:00Z), they
  become `Operation`, `Reply`, `Event`.
- `CriomeRoot` is fine (it is the daemon's actor root, not a contract
  type, and `Criome` is the domain noun — defensible per /257 §1.5's
  closing note on domain-concept prefixes).

The contract has fewer ancestry-prefix violations than
signal-persona-router or signal-persona-terminal, because most
types carry attestation / authorization / identity domain nouns,
not crate-name prefixes. The cleanup here is small.

### /257 §1.6 — `*RequestUnimplemented` redundancy

**Status: N/A in this contract.** `signal-criome` does not have a
`RequestUnimplemented` reply variant at all. It has `Rejection {
reason: RejectionReason }` (line 833-835), which is the right
shape — no `operation` field redundancy.

Note: there is no `Unimplemented` placeholder. The reply enum
treats every operation as implemented or rejected with a typed
reason; this is more aggressive than spirit's
`RequestUnimplemented` shape and probably right for criome.

### /257 §1.7 — Empty marker records

**Status: NOT PRESENT in this contract.** Every operation payload
carries data; no empty markers.

### /257 §1.8 — Single-variant enums

**Status: BORDERLINE.** Two candidates:

- `AuthorizationPolicyClass { SimpleSelfSigned, ComplexQuorum }`
  — two real variants today (per ARCH §Authorization model).
  Defensible.
- `AuthorizationDenialSource { Policy, Signers }` — two real
  variants. Defensible.

The contract is unusually clean on this axis.

### /257 §1.9 — Frame type alias boilerplate

**Status: NOT PRESENT in src/lib.rs**, because the contract
predates the alias-dance discipline. After the migration to
`signal-frame` and the unprefixed-emit fix, the question becomes
moot.

### /257 §1.10 — No observable block

**Status: NOT PRESENT — but see §2.5 below.** The criome
contract is documented as NOT requiring Tap/Untap because criome
is "not a persona component" (see
`signal-criome/ARCHITECTURE.md:39-43` and the explicit comment in
the MUST IMPLEMENT block). The argument: criome is a workspace-
ecosystem authentication daemon, not part of the persona engine.

**This decision needs explicit psyche reaffirmation.** The
`intent/persona.nota` 2026-05-21T10:00:00Z record ("debug the
debugger") said every persona component is observable, including
introspect itself. The question is whether criome counts as a
persona component under that rule. Today it sits outside the
persona engine boot order, but the substrate is essential to
persona operation (every authorization grant flows through it).
Per /150 the criome split question itself implies criome is
**adjacent to** persona, not inside it.

Designer lean (low certainty): observable IS warranted on
criome's working channel for cross-component introspection
parity. Confirm with psyche before adding.

### /257 §1.11 — Single-field timestamps (excess precision)

**Status: PRESENT.** `signal-criome/src/lib.rs:185-197`:

```rust
pub struct TimestampNanos(u64);
```

Used for `Attestation.issued_at` / `expires_at`,
`AuthorizationGrant.issued_at` / `expires_at`, etc. Nanosecond
precision is excessive for "this attestation expires at" timestamps;
seconds suffice. Aligns with /257 §1.12 designer lean.

### /257 §1.13 — `supervision::` namespace stale

**Status: N/A.** Not relevant to criome.

## 2 · New findings specific to this triad

### 2.1 — The signal-criome split question (per /150 §6.9 + §8)

`signal-criome/ARCHITECTURE.md:60-66` (the MUST IMPLEMENT block)
poses this exact question:

> *"signal-criome has nineteen request variants spanning three
> relations (consumer ↔ criome, criome-peer ↔ criome-peer,
> subscriber ↔ criome). Whether these stay one contract-relation or
> split into multiple signal_channel! blocks per signal-persona
> precedent is a designer call before the operator picks this up."*

And /150 §6.9 frames the split rationale:

> *"signal-criome should likely split by relation / authority
> surface, not because of name collisions. The rationale is
> dependency and authority separation: identity; attestation /
> authorization; peer signing. Those may be separate contract crates
> while still being served by one daemon socket if the authority
> model allows it."*

#### Dependency graph of the current types

Reading `signal-criome/src/lib.rs:1-901`, the types cluster as:

**Identity relation** (types touching the identity registry):
`Identity`, `PrincipalName`, `PrincipalId`,
`PublicKeyFingerprint`, `BlsPublicKey`, `KeyPurpose`,
`PrincipalStatus`, `IdentityRegistration`, `IdentityRevocation`,
`IdentityLookup`, `IdentityReceipt`, `IdentitySnapshot`,
`IdentitySubscription`, `IdentityUpdate`,
`IdentitySubscriptionToken`. About 15 types.

**Attestation relation** (types signing/verifying typed content):
`Attestation`, `SignatureEnvelope`, `SignedObject`,
`DelegationGrant`, `ComponentRelease`, `SignedPersonaRequest`,
`SignatureScheme`, `ContentReference`, `ObjectDigest`,
`AuditContext`, `ContentPurpose`, `VerificationDecision`,
`SignReceipt`, `VerificationResult`, `AttestationReceipt`,
`ArchiveAttestationRequest`, `ChannelGrantAttestationRequest`,
`AuthorizationAttestationRequest`, `SignRequest`, `VerifyRequest`.
About 20 types.

**Authorization relation** (the routed-authorization flow):
`SignalCallAuthorization`, `AuthorizedSignalVerb`, `ContractName`,
`AuthorizationRequestSlot`, `AuthorizationScope`,
`AuthorizationPolicyClass`, `AuthorizationPolicySatisfaction`,
`AuthorizationStatus`, `AuthorizationDenialReason`,
`AuthorizationDenialSource`, `AuthorizationDenial`,
`AuthorizationGrant`, `AuthorizationObservation`,
`AuthorizationVerification`, `AuthorizationPending`,
`AuthorizationDenied`, `AuthorizationExpired`,
`AuthorizationUnavailable`, `AuthorizationStateRecord`,
`AuthorizationObservationSnapshot`,
`AuthorizationObservationToken`,
`AuthorizationObservationRetracted`, `AuthorizationUpdate`,
`RequiredSignatureThreshold`, `ReplayNonce`. About 25 types.

**Peer-signing relation** (cross-criome signature solicitation):
`SignatureSolicitation`, `SignatureSolicitationRoute`,
`SignatureSubmission`, `SignatureRouteReceipt`,
`SignatureSubmissionReceipt`,
`AuthorizationRejection` (peer rejects a solicitation).
About 6 types.

**Shared types crossing all relations**:
`Identity` (every relation references Identity for principals).
`ObjectDigest` (attestation + authorization both reference
content digests; peer-signing routes solicitations *about a digest*).
`ContractName`, `AuthorizationScope` (authorization + peer-signing).

#### Why the relations aren't independent

The peer-signing relation exists **only because of** the
authorization relation: a peer criome is solicited for signatures
to satisfy an authorization request's quorum policy. The
solicitation carries `AuthorizationRequestSlot`, `ObjectDigest`,
`ContractName`, `AuthorizedSignalVerb`, `AuthorizationScope`,
`requester: Identity`. Splitting peer-signing into its own crate
means re-importing every authorization shape that frames what is
being signed.

The attestation relation references identities deeply: every
`Attestation` carries `signer: Identity`, every
`DelegationGrant` carries `issuer: Identity` and `subject:
Identity`. Splitting attestation from identity means making
`Identity` an upstream shared crate that both depend on (a
`signal-criome-identity` or similar).

The authorization relation carries content digests of attestations
it is authorizing (the `AuthorizationVerification` checks that a
grant's digest matches a particular request). Authorization and
attestation are co-tied at the type level.

#### Recommendation: do NOT split, use modules

The cleanest expression of the relation structure is **one
`signal-criome` crate with three module seams**:

```text
signal-criome/
└── src/lib.rs
    ├── pub mod identity { ... }
    ├── pub mod attestation { ... }
    ├── pub mod authorization { ... }
    └── signal_channel! { channel Criome { ... } }
```

Reasoning:

1. **No name collisions across the relations.** Every type's
   name reads cleanly in its current flat namespace, so module
   disambiguation is not load-bearing — the modules are only an
   organizational device.
2. **Shared types stay at crate root.** `Identity`,
   `ObjectDigest`, `ContractName`, `AuthorizationScope`,
   `ReplayNonce` cross relations. Splitting into separate crates
   forces a shared upstream (`signal-criome-types`); inside one
   crate, they live at the root.
3. **One daemon, one socket, one channel.** Per /150 §6.9 ("served
   by one daemon socket if the authority model allows it"), the
   criome daemon serves all three relations on its working
   socket. The Authorization model's policy table, signature
   solicitation, and grant issuance flow through criome's central
   actor coordination. Splitting the *contract* into three crates
   while keeping one channel means the macro invocation would
   re-import all three to declare one channel — bookkeeping
   overhead with no separation benefit.
4. **Authority separation is a daemon-internal concern.** The
   working/policy split (owner-signal-criome vs signal-criome) is
   the real authority surface. Within signal-criome, the
   identity/attestation/authorization/peer-signing relations all
   share the same peer-authority model (peer-callable, no owner
   gating). There is no second authority tier *inside*
   signal-criome that splitting could express.
5. **`signal-persona` precedent is the wrong precedent.**
   `signal-persona` carries two channels (`Engine` and
   `Supervision` / `EngineManagement`) in one crate per /258 §2.4
   because the two channels serve *different sockets* (the manager
   socket and the supervision socket). Criome has one working
   socket; the precedent does not apply.

If a future relation appears that lives on a different socket
(e.g., an introspection consumer surface separate from the working
contract), that is the moment to split — but at the socket
boundary, not at the relation boundary.

### 2.2 — BLS signature envelope shape

`signal-criome/src/lib.rs:506-511`:

```rust
pub struct SignatureEnvelope {
    pub scheme: SignatureScheme,
    pub public_key: BlsPublicKey,
    pub signature: BlsSignature,
}
```

This is the clean shape. Three observations:

1. **`BlsPublicKey` and `BlsSignature` carry `Bls` prefix.** Per
   ESSENCE §Naming, that prefix restates a fact already named by
   the `scheme: SignatureScheme` field. If the contract's
   universe is BLS-only (per the architecture's "BLS12-381 from
   day one" + the `tests/round_trip.rs` constraint that "the
   signature-scheme vocabulary is BLS only"), the `Bls` prefix
   could drop to `PublicKey` and `Signature`. **Recommendation:
   drop the prefix.** The closed-enum `SignatureScheme` carries
   the scheme distinction; the key/signature byte-shape types are
   just typed wrappers.

2. **`SignatureScheme` has two real variants** (`Bls12_381MinPk`,
   `Bls12_381MinSig`) — both BLS12-381, differing in min-pk vs
   min-sig parameter. Defensible per /257 §1.8 multi-variant test,
   but if only one will be picked at implementation time, the enum
   could collapse to a unit type until the second is real.

3. **No `signed_at: TimestampNanos` field on the envelope itself.**
   The signed-at time lives on the containing `Attestation`
   (`issued_at`). Defensible — the envelope is the raw signature
   primitive, and the timestamp is provenance, not part of the
   signed bytes.

### 2.3 — Identity record / delegation grant / component release / OOB attestation shapes

The four payload records sit at the core of the attestation
relation. Their shapes:

```rust
// signal-criome/src/lib.rs:731-736
pub struct IdentityRegistration {
    pub identity: Identity,
    pub public_key: BlsPublicKey,
    pub fingerprint: PublicKeyFingerprint,
    pub purpose: KeyPurpose,
}

// :534-539
pub struct DelegationGrant {
    pub issuer: Identity,
    pub subject: Identity,
    pub scope: ContentPurpose,
    pub expires_at: Option<TimestampNanos>,
}

// :543-547
pub struct ComponentRelease {
    pub component: PrincipalName,
    pub artifact: ObjectDigest,
    pub authorized_by: Identity,
}

// :515-522
pub struct Attestation {
    pub content: ContentReference,
    pub signer: Identity,
    pub envelope: SignatureEnvelope,
    pub issued_at: TimestampNanos,
    pub expires_at: Option<TimestampNanos>,
    pub audit_context: AuditContext,
}
```

The four records are **structurally consistent with
out-of-band attestation discipline**: every record references
content by `ObjectDigest` or `ContentReference`; no proof fields
embed in content records elsewhere.

Smaller issues:

- `ComponentRelease.component: PrincipalName` reuses the
  `PrincipalName` type for a *component-name* role. The type
  carries no semantic distinction between principal names and
  component names; both are strings. A `ComponentName` newtype
  would type-disambiguate without adding cost.
- `DelegationGrant.scope: ContentPurpose` is a closed enum (7
  variants: `SignedObject`, `ComponentRelease`, `ChannelGrant`,
  `ChannelRetract`, `Authorization`, `Archive`,
  `PrivilegeElevation`). The enum is reused as the `purpose`
  field in `ContentReference`. Reuse is fine. But the variant
  `Archive` is generic ("archive of what?"); other variants name
  the content kind. Consider renaming to clarify (e.g.,
  `ComponentArchive` if archive means component-release archives).
- `Attestation.audit_context: AuditContext` is a four-field
  record (`purpose`, `audience`, `policy_version`, `nonce`). The
  `policy_version: PrincipalName` reuse is the same type-overload
  smell as `ComponentRelease.component`. A `PolicyVersion`
  newtype would help.

### 2.4 — Ancestry prefix: `AuthorizedSignalVerb` should retire

`signal-criome/src/lib.rs:212-219`:

```rust
pub enum AuthorizedSignalVerb {
    Assert,
    Mutate,
    Retract,
    Match,
    Subscribe,
    Validate,
}
```

This enum literally re-defines the six Sema operations inside
`signal-criome` because the contract pre-dates `signal-sema`. After
the migration to `signal-frame` + `signal-sema`, this enum becomes
`signal_sema::SemaOperation` (the canonical six classes). The
local copy + the `From<signal_core::SignalVerb> for
AuthorizedSignalVerb` conversion impls (lines 221-245) all retire.

The `verb: AuthorizedSignalVerb` field in `SignalCallAuthorization`
(line 563) and `SignatureSolicitation` (line 589) and
`AuthorizationGrant.authorized_verb` (line 624) all become
`signal_sema::SemaOperation` references.

### 2.5 — Observable block — psyche call

Per /257 §1.10, persona components are mandatory-observable. The
criome architecture's MUST IMPLEMENT block declares:

> *"Subscription observability. Criome is not a persona component;
> the mandatory Tap/Untap observable block does not apply. The
> existing identity-updates and authorization-observation
> subscriptions stay as domain-specific Subscribe/Retract pairs."*

But /150 §6.9 lists criome as one of the unmigrated triad
components, alongside persona-mind, persona-router, persona-message,
etc. — implying it sits inside the same observable scope. And
`intent/persona.nota` 2026-05-21T10:00:00Z (debug-the-debugger)
broadens the observable mandate to include even introspect.

The question is **definitional**: what counts as a "persona
component" for the observable mandate? Two candidate readings:

- **Narrow reading.** Only components named `persona-*` and
  members of the persona engine. Criome is workspace
  infrastructure, not persona — keep observable optional. This
  is what the criome ARCH currently says.
- **Broad reading.** Any daemon that persona-introspect should
  be able to monitor cross-component. Criome's authorization
  decisions flow into every persona deploy authorization;
  persona-introspect should be able to subscribe to "all Asserts
  on criome" the same way it subscribes to spirit. Add the
  observable block.

Designer lean (low certainty): **broad reading**. The
debug-the-debugger principle reads as universal ("a tool that
observes other tools must itself be observable") and criome is
exactly the kind of substrate where cross-component activity
monitoring is valuable. But this needs psyche confirmation
because the criome ARCH explicitly opts out. **Open question.**

### 2.6 — Daemon does not use signal-executor

`criome/src/actors/root.rs:118-199` is a hand-rolled
`match request { ... }` dispatching to per-actor messages. There
is no `Lowering`, no `OperationPlan`, no `BatchPlan`, no
`CommandExecutor`, no `ToSemaOperation`/`ToSemaOutcome`, no
observer publication.

This is the same gap /255 found in spirit and /258 §2.2 found in
the engine-manager daemon. The migration target (per /150 §7 and
the spirit template) is:

```rust
pub enum CriomeCommand {
    RecordIdentityRegistration(IdentityRegistration),
    RecordIdentityRevocation(IdentityRevocation),
    ReadIdentity(IdentityLookup),
    OpenIdentitySubscription(IdentitySubscriptionToken),
    CloseIdentitySubscription(IdentitySubscriptionToken),
    RecordAttestation(Attestation),
    VerifyAttestation(VerifyRequest),
    CreateAuthorizationState(SignalCallAuthorization),
    ReadAuthorizationState(AuthorizationRequestSlot),
    RecordSignatureSolicitation(SignatureSolicitationRoute),
    RecordSignatureSubmission(SignatureSubmission),
    RecordAuthorizationRejection(AuthorizationRejection),
    OpenAuthorizationObservation(AuthorizationObservationToken),
    CloseAuthorizationObservation(AuthorizationObservationToken),
    VerifyAuthorization(AuthorizationVerification),
}

pub enum CriomeEffect {
    IdentityRegistered(IdentityReceipt),
    IdentityRevoked(IdentityReceipt),
    IdentityRead(Option<IdentityReceipt>),
    IdentitySnapshotRead(IdentitySnapshot),
    IdentitySubscriptionOpened(IdentitySnapshot, IdentitySubscriptionToken),
    IdentitySubscriptionClosed(IdentitySubscriptionToken),
    AttestationRecorded(AttestationReceipt),
    AttestationVerified(VerificationResult),
    AuthorizationStateCreated(AuthorizationStateRecord),
    AuthorizationStateRead(AuthorizationStateRecord),
    AuthorizationGranted(AuthorizationGrant),
    AuthorizationDenied(AuthorizationDenied),
    AuthorizationExpired(AuthorizationExpired),
    AuthorizationUnavailable(AuthorizationUnavailable),
    AuthorizationRouteRecorded(SignatureRouteReceipt),
    AuthorizationSignatureRecorded(SignatureSubmissionReceipt),
    AuthorizationObservationOpened(AuthorizationObservationSnapshot, AuthorizationObservationToken),
    AuthorizationObservationClosed(AuthorizationObservationToken),
    AuthorizationVerificationResult(AuthorizationVerification),
    Rejection(Rejection),
}
```

The existing per-actor message types in `criome/src/actors/*.rs`
become the `Lowering::lower()` decoding step; the existing
`StoreKernel` becomes the `CommandExecutor::execute_atomic_batch`
implementation backing.

`ToSemaOperation` projections (per `signal-criome/ARCHITECTURE.md`
§"Sema classification projections (Layer 3)" lines 227-252) are
already mapped in the ARCH:

```text
Sign                            -> Assert
Verify                          -> Validate
Register                        -> Assert
Revoke                          -> Retract
Lookup                          -> Match
AttestArchive                   -> Assert
AttestChannelGrant              -> Assert
AttestAuthorization             -> Assert
Authorize                       -> Assert
Observe                         -> Subscribe
RouteSignatureRequest           -> Assert
SubmitSignature                 -> Assert
RejectAuthorization             -> Assert
SubscribeIdentityUpdates        -> Subscribe
IdentitySubscriptionRetraction  -> Retract
AuthorizationObservationRetraction -> Retract
```

Move this projection into the daemon crate as `impl
ToSemaOperation for CriomeCommand`.

### 2.7 — Daemon reads environment variable for socket path

`criome/src/daemon.rs:27-32`:

```rust
pub fn from_environment() -> Self {
    let socket = std::env::var_os("CRIOME_SOCKET")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("/tmp/criome.sock"));
    Self::new(socket, StoreLocation::from_environment())
}
```

This violates the env-var carve-out scope rule from
`intent/component-shape.nota` 2026-05-20T13:00:00Z:

> *"the CLI is the only place where we allow the use of an
> environment variable... Daemons never read environment
> variables; all daemon configuration is NOTA."*

The daemon's socket path must come from the NOTA configuration
record (its single argument). The CLI may read `CRIOME_SOCKET`
for socket-path override; the daemon may not.

`StoreLocation::from_environment()` at the same line is the
same violation in the storage-path direction.

### 2.8 — No bundled thin CLI binary

The component triad invariant (per `skills/component-triad.md`
and /150 §2) is that the runtime repository ships
`src/bin/<name>-daemon.rs` AND `src/bin/<name>.rs`.

`criome/src/bin/` exists but is empty in the structure I saw;
`Cargo.toml:13-16` declares only one binary:

```toml
[[bin]]
name = "criome"
path = "src/main.rs"
```

The repository ships **one binary named `criome`** at
`src/main.rs`. This conflates the daemon and the CLI into one
binary — same antipattern as the pre-spirit shape. The migration
target (per /150 §2 and the spirit template) is:

```toml
[[bin]]
name = "criome-daemon"
path = "src/bin/criome-daemon.rs"

[[bin]]
name = "criome"
path = "src/bin/criome.rs"
```

The `criome` thin CLI uses the `signal_cli!` macro (per
/150 §2 and reports/second-designer/129) to dispatch between
the working socket and the owner socket once both contracts exist.

### 2.9 — Ancestry word redundancy in payload record names

Several payload records carry their relation prefix:

- `IdentityRegistration`, `IdentityRevocation`, `IdentityLookup`,
  `IdentitySubscription`, `IdentitySubscriptionToken`,
  `IdentityReceipt`, `IdentitySnapshot`, `IdentityUpdate`.
- `AuthorizationObservation`, `AuthorizationVerification`,
  `AuthorizationPending`, `AuthorizationGranted`,
  `AuthorizationDenied`, `AuthorizationExpired`,
  `AuthorizationUnavailable`,
  `AuthorizationObservationSnapshot`,
  `AuthorizationObservationToken`,
  `AuthorizationObservationRetracted`, `AuthorizationUpdate`,
  `AuthorizationRequestSlot`, `AuthorizationStateRecord`,
  `AuthorizationGrant`, `AuthorizationRejection`,
  `AuthorizationDenial`, `AuthorizationDenialReason`,
  `AuthorizationDenialSource`,
  `AuthorizationPolicySatisfaction`, `AuthorizationPolicyClass`.

Per /257 §1.5: after the relation modules land (per §2.1's
recommendation), these names move into `pub mod identity { ... }`
or `pub mod authorization { ... }` and drop the prefix. The
reader writes `identity::Registration`, `authorization::Grant`,
etc. The crate-level re-exports retire.

### 2.10 — `IdentityUpdate` is in reply enum but emitted on a stream

`signal-criome/src/lib.rs:867-882` shows `IdentityUpdate(IdentityUpdate)`
listed as a reply variant. But the stream block at lines 887-898
declares `event IdentityUpdate(IdentityUpdate) belongs IdentityUpdateStream`.

The macro grammar (per /258 and /150) expects event-belonging
variants to live in the `event` block, not the `reply` block. The
duplication looks like leftover boilerplate from a pre-stream-block
shape. After the `signal-frame` migration, the macro should
emit `IdentityUpdate` only as an event, not also as a reply
variant; reading the current `CriomeRequest`/`CriomeReply` shape
suggests this is a contract bug not caught by current witnesses.

### 2.11 — `Rejection` is overloaded

`signal-criome/src/lib.rs:833-835`:

```rust
pub struct Rejection {
    pub reason: RejectionReason,
}
```

This reply variant carries operation-rejection reasons (request
malformed, identity revoked, etc.). It is **distinct from**:

- `AuthorizationDenied(AuthorizationDenied)` — terminal
  authorization outcome.
- `AuthorizationRejection` (the *request* type, not a reply,
  carrying a peer criome's denial of a signature-solicitation).

Three different "denial / rejection" concepts in one contract.
After the §2.1 module split, they live in separate modules and
the name clash dissolves; before that, the contract is harder
to read than it needs to be.

## 3 · Proposed owner-signal-criome

The owner contract is the largest single hole in the triad. The
criome architecture (`criome/ARCHITECTURE.md:84-178`,
§Authorization model + §Security model) already names the
operations that belong here; the contract crate does not exist
yet.

Below is a proposal for the owner-signal-criome shape. **All of
this is designer proposal, not psyche intent — the owner contract
needs psyche review on scope, on the encrypted-session
boundary, and on the exact verb set.**

### 3.1 — Owner operations

Five operation families, each grouping multiple variants:

**Master-key lifecycle:**

```rust
operation SubmitPassphrase(Passphrase),
operation RotateMasterKey(MasterKeyRotation),  // future possibility per ARCH §8.1
```

**Policy mutation** (the policy table that names which signatures
satisfy which content-addressed request kinds):

```rust
operation InstallPolicy(PolicyInstallation),
operation RetractPolicy(PolicyIdentifier),
operation InspectPolicies(PolicyInspection),
```

`PolicyInstallation` carries the policy class
(`SimpleSelfSigned`/`ComplexQuorum`), the named signers, the
threshold, the request kind / digest pattern, expiry. Today's
policy schema is narrow (two classes); the variant set may grow
per ARCH §8.1 (richer policy schema as a future possibility).

**Peer-routing table mutation** (peer master public key → host /
unix-user):

```rust
operation RegisterPeer(PeerRegistration),
operation RetractPeer(PeerIdentifier),
operation InspectPeers(PeerInspection),
```

`PeerRegistration { public_key, host, unix_user }`.
`PeerIdentifier { public_key }`. `PeerInspection` is a query of
the peer-routing table.

**Escalation-to-approve flow** (the long-running owner approval
prompt loop — the load-bearing `tui-criome` use case):

```rust
operation ApproveEscalation(EscalationApproval),
operation DenyEscalation(EscalationDenial),
operation Watch(EscalationSubscription) opens EscalationStream,
operation Unwatch(EscalationSubscriptionToken),
```

`EscalationSubscription` is what tui-criome subscribes to so it
gets a push event when criome needs the owner's signature
approval. The reply event carries `EscalationPrompt { content,
audience, policy_satisfied_so_far, missing_signatures, ... }`.
`ApproveEscalation { prompt_token }` / `DenyEscalation {
prompt_token, reason }` are the owner's answers.

**Daemon configuration:**

```rust
operation Configure(Configuration),
operation Inspect(ConfigurationInspection),
```

`Configuration` carries: socket paths, store location,
master-key file location, owner identity (the Unix user that
owns this daemon), session-encryption parameters (the AEAD cipher
suite per `criome/ARCHITECTURE.md:166-170`).

### 3.2 — Owner reply enum

```rust
reply Reply {
    PassphraseAccepted(PassphraseAcceptance),
    PassphraseRejected(PassphraseRejection),
    PolicyInstalled(PolicyReceipt),
    PolicyRetracted(PolicyReceipt),
    PoliciesInspected(PolicyListing),
    PeerRegistered(PeerReceipt),
    PeerRetracted(PeerReceipt),
    PeersInspected(PeerListing),
    EscalationApproved(EscalationReceipt),
    EscalationDenied(EscalationReceipt),
    EscalationWatchOpened(EscalationSubscriptionOpened),
    EscalationWatchClosed(EscalationSubscriptionRetracted),
    Configured(ConfigurationReceipt),
    ConfigurationInspected(Configuration),
    OperationRejected(OperationRejection),
}
```

Per /257 §1.4, watch consider lifting the past-tense receipt
family into a single `*Receipt(Receipt)` parent enum. The shape
above keeps them flat for now; landing the right shape can come
after the working signal is migrated and the patterns are
visible side-by-side.

### 3.3 — Owner event enum (escalation stream only)

```rust
event Event {
    EscalationPrompted(EscalationPrompt) belongs EscalationStream,
}

stream EscalationStream {
    token EscalationSubscriptionToken;
    opened EscalationSubscriptionOpened;
    event EscalationPrompted;
    close Unwatch;
}
```

`EscalationPrompt` carries enough context for the owner to decide:
the content being signed, the requester identity, the policy
class, the signatures already collected, the missing
authorities, the expiry deadline. The owner answers via
`ApproveEscalation` or `DenyEscalation` on the same socket
(the working request side).

### 3.4 — Session encryption boundary

The criome ARCH names the encrypted owner session as part of the
security model:

> *"the owner-signal-criome session starts with an ECDH exchange,
> derives a symmetric session key through HKDF, then carries
> AEAD-encrypted frames. The exact cipher suite belongs to the
> owner-signal-criome contract pass; candidates are Noise XX or a
> direct X25519 + HKDF-blake3 + ChaCha20-Poly1305 / AES-GCM
> shape."*

This is a substantial boundary that touches `signal-frame` itself —
the encrypted-frame envelope is not a current `signal-frame`
capability. The owner-signal-criome design must either:

- carry its own encryption envelope above the `signal-frame`
  request/reply (the owner-signal Operation payload is itself a
  ciphertext-record that encrypts a NOTA-encoded inner operation);
- or extend `signal-frame` with an optional handshake-and-AEAD
  channel mode that owner sockets use.

**The cleaner shape is to extend `signal-frame`** — every
owner-signal-* contract eventually needs the same envelope (per
`intent/component-shape.nota` 2026-05-20T12:11:26Z, every
stateful component has an owner contract). But this is a
workspace-wide infrastructure decision, not a criome-specific
one.

**Designer lean:** scope the first `owner-signal-criome` slice to
*plaintext owner socket* (matching today's spirit owner socket
and the other landed owner contracts), and treat encrypted
owner-session as a follow-up infrastructure arc that adds the
envelope to `signal-frame`. The architectural constraint:

> *"plaintext owner-session handling must not be added while the
> owner-signal contract is absent."*

reads as a constraint on adding owner traffic on the **ordinary
socket**; it does not block plaintext owner traffic on a
dedicated owner socket once that socket exists. **Open question
for psyche before implementing.**

### 3.5 — Bootstrap policy

Per `intent/component-shape.nota` 2026-05-19T01:30:00Z and the
`bootstrap-policy.nota` discipline, every triad daemon has a
declared first-start policy file in the runtime repo. For
criome:

```text
criome/bootstrap-policy.nota
```

Content sketch (NOTA, positional, not labeled):

```nota
(BootstrapPolicy
  (Identity (Cluster "criome-bootstrap-cluster"))
  (Policy SimpleSelfSigned (RequiredSignatureThreshold 1))
  (CipherSuite (X25519HkdfBlake3ChaCha20Poly1305))
  ; the bootstrap policy installs the daemon's own master key as
  ; the only authorized signer for self-signed authorizations
)
```

The bootstrap file's exact shape is owner-contract design and
follows once the owner operation set is settled.

## 4 · Recommended next slice for the criome triad

In priority order:

1. **Migrate `signal-criome` to `signal-frame`.** Drop the
   `signal-core` dep; rewrite the `signal_channel!` invocation to
   the `operation Verb(Payload)` grammar; drop the
   `AuthorizedSignalVerb` enum (replace references with
   `signal_sema::SemaOperation`); fix the duplicate-event-in-reply
   bug (§2.10); drop `BlsPublicKey`/`BlsSignature` prefixes
   (§2.2).

2. **Reshape the request tree.** Lift the relation clusters into
   typed parent enums:

   ```rust
   operation Identity(IdentityOperation),
   operation Attest(AttestationRequest),
   operation Authorize(AuthorizationOperation),
   operation Verify(VerificationOperation),
   operation Route(SignatureSolicitationRoute),
   operation Submit(SignatureSubmission),
   operation Reject(AuthorizationRejection),
   operation Watch(Subscription) opens Stream,
   operation Unwatch(SubscriptionToken),
   ```

   Where the typed sums are:

   ```rust
   pub enum IdentityOperation {
       Register(IdentityRegistration),
       Revoke(IdentityRevocation),
       Lookup(IdentityLookup),
   }

   pub enum AttestationRequest {
       Sign(SignRequest),
       Archive(ArchiveAttestationRequest),
       ChannelGrant(ChannelGrantAttestationRequest),
       Authorization(AuthorizationAttestationRequest),
   }

   pub enum AuthorizationOperation {
       SignalCall(SignalCallAuthorization),
       Observe(AuthorizationObservation),
   }

   pub enum VerificationOperation {
       Attestation(VerifyRequest),
       Authorization(AuthorizationVerification),
   }

   pub enum Subscription {
       Identity(IdentitySubscription),
       Authorization(AuthorizationObservation),
   }
   ```

   Symmetric reply tree (per /257 §1.4 / /150 §3):

   ```rust
   reply Reply {
       IdentityResult(IdentityResult),
       Attested(AttestationOutcome),
       Authorized(AuthorizationOutcome),
       Verified(VerificationOutcome),
       SignatureRouted(SignatureRouteReceipt),
       SignatureSubmitted(SignatureSubmissionReceipt),
       Rejected(AuthorizationOutcome),
       Watched(SubscriptionOpened),
       Unwatched(SubscriptionRetracted),
       Rejection(Rejection),
   }
   ```

3. **Move types into relation modules.** `pub mod identity { ... }`,
   `pub mod attestation { ... }`, `pub mod authorization { ... }`,
   `pub mod peer_signing { ... }`. Drop the relation prefix
   on each type's name (per §2.9). Shared types
   (`Identity`, `ObjectDigest`, `ContractName`, etc.) stay at
   crate root.

4. **Confirm or override the observable-block decision** (§2.5) —
   psyche call.

5. **Create the `owner-signal-criome` crate** with the working
   shape sketched in §3.

6. **Migrate the `criome` daemon onto `signal-executor`.**
   Define `CriomeCommand` / `CriomeEffect` per §2.6; implement
   `Lowering`, `CommandExecutor`, `ToSemaOperation`,
   `ToSemaOutcome`, `BatchErrorClassification`. Wire the
   socket handler through `Executor::execute`.

7. **Split the binaries** (§2.8): `src/bin/criome-daemon.rs` for
   the daemon, `src/bin/criome.rs` for the thin CLI generated by
   `signal_cli!`. Daemon takes a NOTA config record; CLI takes a
   NOTA request string or file path.

8. **Drop daemon environment-variable reads** (§2.7). Move
   socket path and store location into the daemon's NOTA
   configuration record.

9. **Timestamp precision** — drop `TimestampNanos` to a
   seconds-precision `Timestamp` (§/257 §1.11). Subject to the
   open psyche call on runtime-protocol timestamps (per /257
   §1.12 designer lean).

10. **Add the observable block** if §2.5 resolves to broad
    reading.

11. **Encrypted owner-session** — separate infrastructure arc
    (§3.4); not blocking the first owner-signal slice.

## 5 · Cross-cutting notes

### 5.1 — Coordination with /150's other unmigrated triads

The criome migration is structurally identical to spirit's
landed migration and engine-manager's pending migration. The
spirit template (per /258 §4) is the model. The criome triad
should not invent new shapes; it should mirror the spirit shape
with criome's domain payloads.

### 5.2 — Coordination with lojix

`criome/ARCHITECTURE.md:55-58` names the routed-authorization
flow as the criome ↔ lojix integration point. The lojix daemon
depends on criome for authorization grants over signal-lojix
request digests. After the contract reshape, lojix consumers of
`signal-criome` need updates — the `SignalCallAuthorization`
operation type changes name (becomes
`AuthorizationOperation::SignalCall` under the §4 reshape) and
the `AuthorizedSignalVerb` enum becomes
`signal_sema::SemaOperation`.

This is migration churn, not design churn. Coordinate the criome
contract migration and the lojix consumer update in the same
slice so lojix is not left referencing retired types.

### 5.3 — Today vs eventually

The criome ARCH carries an explicit today-vs-eventually marker
(per `criome/ARCHITECTURE.md:9-29`). Today's criome is the
Spartan BLS substrate. Eventual Criome is the universal computing
paradigm in Sema. **The migration recommendations above apply to
today's narrow scope.** None of the renames or relation
structures assume the eventual Criome's shape; that is a separate
design discussion when (and if) eventual Criome's scope settles.

## 6 · Open psyche questions

The following carry enough load that designer-derivation is
inappropriate:

**Q1 — Observable block on criome's working channel.** The
criome ARCH explicitly says criome is not a persona component
and skips the mandatory Tap/Untap. /150 §6.9 lists criome
alongside persona-mind, persona-router etc. as unmigrated triad
work; the debug-the-debugger principle (per `intent/persona.nota`
2026-05-21T10:00:00Z) reads as universal. Should criome's
working channel get the observable block? **Designer lean:
yes**, but psyche call needed because the criome ARCH explicitly
opts out.

**Q2 — signal-criome split (this report's main subject).**
Designer recommendation in §2.1 is **do NOT split** — use
modules inside one `signal-criome` crate to express the three
relations. The contract crates would mostly cross-import each
other for shared types (`Identity`, `ObjectDigest`,
`ContractName`). The /150 §6.9 framing ("dependency and authority
separation: identity / attestation-authorization / peer-signing")
identifies real relations, but the inter-relation type sharing
means splitting yields cross-crate boilerplate, not independence.
Psyche call: does the dependency analysis change the recommendation?

**Q3 — Encrypted owner-session scope.** The criome ARCH
describes ECDH+AEAD for owner-signal-criome sessions. The first
owner-signal-criome slice can ship plaintext on a dedicated owner
socket (matching the landed owner contracts for spirit / mind /
orchestrate / router) and treat encryption as a follow-up arc that
adds the envelope to `signal-frame`. Designer lean: **plaintext
first**. Psyche call: does the criome owner socket need
encryption from day one, or is the dedicated-socket-with-0600 mode
enough until the universal owner-session envelope lands?

**Q4 — Bootstrap-policy contents.** The
`criome/bootstrap-policy.nota` file shape (§3.5) is a sketch
based on the simple-self-signed policy class. Does the psyche
have intent on what the first-start policy should declare?
(Probably this is designer-judgment.)

**Q5 — `Identity` enum membership.** Today's
`Identity { Persona, Agent, Host, Developer, Cluster }`. The
existing ARCH lists these five. Are any others needed? Forge?
Lojix-as-principal? (Probably designer-judgment, but worth
checking.)

## 7 · References

- `/150` — `reports/operator/150-triad-signal-sema-migration-current-state.md`
  — workspace-wide migration current state (§6.9 names criome split
  question).
- `/255`, `/256` — spirit migration template (the canonical model
  the criome triad should follow).
- `/258` — `reports/designer/258-persona-signal-triad-audit-2026-05-21.md`
  — engine-manager audit (same structural gap pattern).
- `/257` — `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  — workspace-wide signal-contract audit (criome listed as
  unmigrated).
- `/129` — `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — signal_cli! macro pattern for the thin CLI.
- `intent/component-shape.nota` 2026-05-18T22:13:54Z — two authority
  tiers (working + policy; no middle).
- `intent/component-shape.nota` 2026-05-19T19:30:00Z + 19:45:00Z —
  contract-local verbs; bird/cloud metaphor.
- `intent/component-shape.nota` 2026-05-20T02:00:00Z — three-layer
  model + Tap/Untap mandate for persona components.
- `intent/component-shape.nota` 2026-05-20T12:11:26Z — universal
  owner-contract; "signal-type naming is architecture" principle.
- `intent/component-shape.nota` 2026-05-20T13:00:00Z — six CLI
  records (binary naming, env-var carve-out, two-socket dispatch).
- `intent/component-shape.nota` 2026-05-21T10:30:00Z —
  macro-emission cleanliness; modules-not-prefix-knobs.
- `intent/persona.nota` 2026-05-21T10:00:00Z — debug-the-debugger
  Clarification (broadens observable mandate).
- `ESSENCE.md` §"Today and eventually" — scope discipline applied
  in §5.3.
- `ESSENCE.md` §"Naming" — pair-of-rules applied throughout.
- `skills/component-triad.md` — triad invariants criome currently
  violates (§2.7, §2.8).
- `skills/naming.md` — ancestry-prefix and repeated-suffix rules
  applied throughout.
- Code under audit:
  - `/git/github.com/LiGoldragon/criome/src/lib.rs:1-18`
  - `/git/github.com/LiGoldragon/criome/src/daemon.rs:14-141`
  - `/git/github.com/LiGoldragon/criome/src/actors/root.rs:15-348`
  - `/git/github.com/LiGoldragon/criome/Cargo.toml:13-39`
  - `/git/github.com/LiGoldragon/signal-criome/src/lib.rs:1-901`
  - `/git/github.com/LiGoldragon/signal-criome/ARCHITECTURE.md:1-426`
  - `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md:1-615`
  - `/git/github.com/LiGoldragon/criome/skills.md:1-146`

This report retires when (a) signal-criome is migrated to
signal-frame with contract-local verbs AND owner-signal-criome
exists AND the criome daemon uses signal-executor AND the
binaries are split, OR (b) a successor audit supersedes.
