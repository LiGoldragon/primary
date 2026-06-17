# 1 — Ground: criome's existing object and verb vocabulary

*ground-criome agent. Inventory of the deployed/in-tree vocabulary so the
internal-engine design (`5`/`6`/`7`) extends it rather than reinventing it.
All paths are real; all type names are copied from source. The headline:
criome already has the identity model, the wire verbs, the SEMA families, and
— crucially — a **started** policy-language POC (`src/language.rs` +
`schema/criome.language.schema`) plus a **started** cluster-root admission
gate (`src/admission.rs`). The new vocabulary must converge on those two, not
start clean.*

## Repos read

| Repo | Role | Path |
|---|---|---|
| `criome` | daemon/runtime + thin CLI | `/git/github.com/LiGoldragon/criome` |
| `signal-criome` | ordinary working wire contract | `/git/github.com/LiGoldragon/signal-criome` |
| `meta-signal-criome` | meta policy/config contract | `/git/github.com/LiGoldragon/meta-signal-criome` |
| `domain-criome` | `.criome` registry/resolution daemon | `/git/github.com/LiGoldragon/domain-criome` |
| `signal-domain-criome` | domain resolution wire contract | `/git/github.com/LiGoldragon/signal-domain-criome` |

## (a) The identity model today

The atom of identity is a **BLS12-381 public key** (`blst` min-pk), carried on
the wire as the string newtype `BlsPublicKey`. The deployed model:

`signal-criome/schema/lib.schema`:
- `Identity` — closed enum, the principal vocabulary. Five variants, each
  wrapping a `PrincipalName`:
  `(Persona PrincipalName) (Agent PrincipalName) (Host PrincipalName) (Developer PrincipalName) (Cluster PrincipalName)`.
- `SignatureScheme [Bls12_381MinPk Bls12_381MinSig]` — closed; only `MinPk` is
  implemented and `MinSig` is *rejected, never parsed as min-pk bytes*
  (algorithm-confusion guard, asserted in `admission.rs` tests).
- `KeyPurpose [CriomeRoot PersonaRequest AgentRequest ReleaseAuthorization HostPublication]`
  — domain separation per key.
- `PrincipalStatus [Active Revoked]`.
- Newtypes: `BlsPublicKey`, `BlsSignature`, `PublicKeyFingerprint`,
  `PrincipalName`, `PrincipalId`, `ObjectDigest`, `ReplayNonce`,
  `TimestampNanos` (Integer), `RequiredSignatureThreshold` (Integer).
- `SignatureEnvelope { scheme public_key signature }` — the
  `(scheme, public_key, signature)` triple; the composable unit of attestation.
- `IdentityRegistration { identity public_key fingerprint purpose admission(Optional SignatureEnvelope) }`
  — note `admission` is already present.

**MasterKey** — `criome/src/master_key.rs`. `struct MasterKey { secret: SecretKey }`
holding the daemon's BLS secret; `generate`, `load_or_generate` (0600 atomic
persist, Spirit `psc6`), `public_key`, `fingerprint`, `sign`. Verification is a
trait `VerifyBls` on the wire `BlsPublicKey` ("the public key is the noun that
verifies"). `AttestationPreimage` builds the canonical signed byte preimage
(domain-tag `CRIOME-ATTESTATION-BLS12381G2-...`); `SystemClock` stamps/expires.

**RegistrationStatement + cluster-root admission** — `criome/src/admission.rs`
(Spirit `ermr`). `RegistrationStatement<'a> { identity public_key purpose }`
with `to_signing_bytes()` (domain-tag `CRIOME-REGISTRATION-ADMISSION-V1`).
`ClusterRoot { public_key }` with `admits(&registration, &admission) -> bool`:
checks scheme is min-pk, envelope key == configured cluster-root key, then BLS
verifies over the statement. Wired into `IdentityRegistry::register`
(`criome/src/actors/registry.rs:96-104`): when a `cluster_root` is configured,
a registration without a valid admission returns
`RejectionReason::UnauthorizedRegistration`. Virgin/dev daemons leave
`cluster_root: None` (self-asserted registry).

**BLS attestation** — real `blst` min-pk. `Attestation { content signer envelope
issued_at expires_at audit_context }`; out-of-band only (references content by
`ContentReference { digest purpose schema_version }`, never embedded).

## (b) Existing Signal input/output roots = the verbs criome accepts/emits

From `signal-criome/schema/lib.schema` (the two leading root vectors). These
are the **contract-local operation heads** — closed, no `Unknown`.

**Input roots (CriomeRequest):** `Sign`, `VerifyAttestation`,
`RegisterIdentity`, `RevokeIdentity`, `LookupIdentity`, `AttestArchive`,
`AttestChannelGrant`, `AttestAuthorization`, `AuthorizeSignalCall`,
`ObserveAuthorization` (opens `AuthorizationObservationStream`),
`VerifyAuthorization`, `RouteSignatureRequest`, `SubmitSignature`,
`RejectAuthorization`, `SubscribeIdentityUpdates` (opens
`IdentityUpdateStream`), `IdentitySubscriptionRetraction`,
`AuthorizationObservationRetraction`.

**Output roots (CriomeReply):** `SignReceipt`, `VerificationResult`,
`IdentityReceipt`, `IdentitySnapshot`, `AttestationReceipt`,
`AuthorizationPending`, `AuthorizationGranted`, `AuthorizationDenied`,
`AuthorizationExpired`, `AuthorizationUnavailable`,
`AuthorizationObservationSnapshot`, `SignatureRouteReceipt`,
`SignatureSubmissionReceipt`, `AuthorizationObservationRetracted`,
`SubscriptionRetracted`, `Rejection`.

**Stream events (CriomeEvent):** `IdentityUpdate` (on `IdentityUpdateStream`),
`AuthorizationUpdate` (on `AuthorizationObservationStream`).

The verb families cluster as: *attestation* (Sign/Verify/Attest*),
*identity registry* (Register/Revoke/Lookup/Subscribe), and **the
authorization machinery** — the closest existing analogue to the new policy
language. `AuthorizeSignalCall` carries `SignalCallAuthorization {
request_digest contract operation scope requester nonce expires_at }`; the
daemon mints a durable `AuthorizationRequestSlot`, collects signatures
(`RouteSignatureRequest`/`SubmitSignature`/`RejectAuthorization`), and issues
`AuthorizationGrant { request_slot authorized_object_digest authorized_contract
authorized_operation authorization_scope policy_satisfaction signature_result
signatures issued_by issued_at expires_at }`. The grant already carries an
`AuthorizationPolicySatisfaction { policy_class required_signature_threshold
satisfied_signers }` over `AuthorizationPolicyClass [SimpleSelfSigned
ComplexQuorum]` — *this is today's two-class policy, and the place the
k-of-n / time-lock / time-varying policy language must grow from.*

## (c) Meta-signal policy operations

`meta-signal-criome/schema/lib.schema` is deliberately tiny today:
- Input root: `Configure(CriomeDaemonConfiguration)` — the same
  `signal-criome:lib:CriomeDaemonConfiguration` the daemon decodes at startup
  (cross-imported, shared type identity).
- Output roots: `Configured { generation }`, `ConfigurationRejected { reason
  [ManagerAuthorityRequired MalformedConfiguration StoreUnavailable] }`,
  `RequestUnimplemented { operation reason }`.
- `CriomeDaemonConfiguration { socket_path store_path cluster_root(Optional
  BlsPublicKey) }`.

The richer meta surface ARCHITECTURE.md promises — passphrase submission,
**policy-table mutation**, peer-route mutation, escalation-approval replies,
the ECDH/AEAD session — is **not yet built**. *Policy mutation is where new
contract objects (a `Contract`/`Rule` definition operation) would land on the
meta plane.*

## (d) SEMA families / durable state

`criome/src/tables.rs` (`CriomeTables`, `CRIOME_SCHEMA_VERSION = 2`, store
`criome.sema` via `sema-engine`). Nine families:

| Family const | Table | Stored value |
|---|---|---|
| `criome-identity` | `identities` | `StoredIdentity { identity public_key fingerprint purpose status }` |
| `criome-revocation` | `revocations` | `StoredRevocation { identity fingerprint reason }` |
| `criome-attestation` | `attestations` | `StoredAttestation { slot attestation }` |
| `criome-authorization-state` | `authorization_requests` | `StoredAuthorizationState { state: AuthorizationStateRecord }` |
| `criome-authorization-replay-nonce` | `authorization_replay_nonces` | `AuthorizationRequestSlot` (keyed by `requester::nonce`) |
| `criome-signature-solicitation` | `signature_solicitations` | `StoredSignatureSolicitation { route }` |
| `criome-submitted-signature` | `submitted_signatures` | `StoredSignatureSubmission { submission }` |
| `criome-attestation-slot` | `attestation_next_slot` | `u64` monotonic counter |
| `criome-authorization-slot` | `authorization_next_slot` | `u64` monotonic counter |

Keys are typed projections: `IdentityKey` (`Kind:Name`), `AuthorizationSlotKey`,
`AuthorizationReplayKey` (`requester::nonce`), etc. Replay is enforced at
`put_new_authorization_state` (returns `Error::AuthorizationReplayAttempted`).
**There is no policy-table family yet** — the policy-class lookup is still a
skeleton (ARCHITECTURE §9 "real policy-table lookup … are the next milestones").
A new `criome-contract` / `criome-policy` family is an open slot.

Actor topology (`src/actors/`): `CriomeRoot` → `AttestationSigner`,
`AttestationVerifier`, `AuthorizationCoordinator`, `IdentityRegistry`,
`StoreKernel` (sole owner of `criome.sema`), `subscription`. Kameo, `Self IS
the actor`, BLS work on the blocking plane.

## (e) The domain-criome resolution surface (LLM-oracle relevance)

`signal-domain-criome/schema/lib.schema` verbs:
`Observe(Observation)`, `Resolve(ResolutionQuery)`, `Project(ProjectionQuery)`,
`Validate(Validation)`; replies `Observed`, `Resolved`, `Projected`,
`Validated`, `RequestRejected`. Key type:
`ResolutionScope [Public Internal Intelligent]` — the **`Intelligent`** scope
is the existing hook for non-deterministic / oracle resolution. `domain-criome`
is **content-addressed DNS** (ARCHITECTURE: each `.criome` domain is its own
authority server; `Resolve` for an unowned domain returns
`NotAuthoritative(Delegation { name authority_endpoint })`, following a
delegation chain). This is the closest existing pattern to the **divergence-
reconciliation** mechanism: a resolution that follows a delegation/authority
chain, where `Intelligent` scope already names a smarter-than-lookup path. The
new `AgreementRule`/oracle objects should mirror this content-addressed,
chain-following, authority-delegated shape — and an LLM-oracle provider is
itself resolved *through one of those identity contracts*.

## (f) Exact schema syntax in use, with a real example

**Wire contracts** use the positional type-prominent schema (schema-next). A
`lib.schema` file is, in order: optional import block `{...}`, **input root
vector** `[(Head PayloadType ...)]`, **output root vector**
`[(Head PayloadType ...)]`, then the **type block** `{...}`. Inside the type
block: `Newtype { field Type }`, enums `Name [VariantA VariantB]` or
data-carrying `Name [(Variant PayloadType) ...]`, structs
`Name { field Type field Type }`, `(Optional T)`, `(Vector T)`, `(Stream {...})`.
`opens StreamName` / `belongs StreamName` annotate subscription roots/events.
Cross-import is the single-colon path `signal-criome:lib:TypeName`. Real
fragment (`signal-criome/schema/lib.schema`):

```
[(Sign SignRequest)
 (RegisterIdentity IdentityRegistration)
 (AuthorizeSignalCall SignalCallAuthorization)
 (ObserveAuthorization AuthorizationObservation opens AuthorizationObservationStream)]
[(SignReceipt SignReceipt)
 (AuthorizationGranted AuthorizationGrant)]
{
  BlsPublicKey { value String }
  SignatureScheme [Bls12_381MinPk Bls12_381MinSig]
  Identity [
    (Persona PrincipalName)
    (Agent PrincipalName)
    (Host PrincipalName)
    (Developer PrincipalName)
    (Cluster PrincipalName)
  ]
  SignatureEnvelope { scheme SignatureScheme public_key BlsPublicKey signature BlsSignature }
  AuthorizationPolicyClass [SimpleSelfSigned ComplexQuorum]
}
```

NOTA instances are **positional**, head then fields in declared order
(`signal-criome/examples/canonical.nota`):
```
(RegisterIdentity ((Persona alice) public-key-1 fingerprint-1 PersonaRequest None))
(AuthorizeSignalCall (digest-lojix-request signal-lojix Deploy deploy-zeus-full-os (Persona alice) authorization-nonce-1 None))
(AuthorizationGranted (authorization-request-1 digest-lojix-request signal-lojix Deploy deploy-zeus-full-os (ComplexQuorum 1 [(Cluster uranus)]) RequiredSignaturesSatisfied [(Bls12_381MinPk public-key-1 signature-1)] (Cluster uranus) 110 None))
```

**The already-started policy language** uses a slightly different *concept-
schema* dialect (`criome/schema/criome.language.schema`): leading `[] []`
empty root vectors then the type block, with rule variants written as
`(Variant Payload)` inside a `Rule [...]` enum. The Rust mirror is
`criome/src/language.rs` and is the design-pressure POC the new work converges
on. Verbatim:

```
{
  KeyAtom { public_key BlsPublicKey }
  IdentityHandle { identity Identity }
  Moment { value TimestampNanos }
  Contract { controller IdentityHandle  rule Rule }
  Rule [
    (SignedBy IdentityHandle)
    (All (Vector Rule))
    (Any (Vector Rule))
    (Threshold Threshold)
    (ActiveAfter TimedRule)
    (ActiveUntil TimedRule)
    (TimeSwitch TimeSwitch)
    (Agreement AgreementRule)
  ]
  Threshold { required_signatures RequiredSignatureThreshold  authorities (Vector IdentityHandle) }
  TimedRule { boundary Moment  rule Rule }
  TimeSwitch { boundary Moment  before Rule  after Rule }
  AgreementRule { divergence ObjectDigest  resolution ObjectDigest  resolver IdentityHandle }
  Evidence { observed_at Moment  signatures (Vector IdentityHandle)  agreements (Vector AgreementFact) }
  AgreementFact { divergence ObjectDigest  resolution ObjectDigest  resolver IdentityHandle }
  Decision [Authorized Rejected]
}
```

`src/language.rs` implements `Contract::evaluate(&Evidence) -> Decision` over
this `Rule` tree (k-of-n `Threshold`, `ActiveAfter`/`ActiveUntil` time-locks,
`TimeSwitch` time-varying quorum, `Agreement` reconciliation-fact matching);
tests in `criome/tests/language.rs` exercise each. It imports from
`signal_criome` (`Identity`, `ObjectDigest`, `RequiredSignatureThreshold`,
`TimestampNanos`) — *the language atoms are already the wire identity types.*

## Gaps the new vocabulary must fill

1. **Lift the POC `Rule`/`Contract` into the contract + SEMA + verbs.** Today
   `language.rs` is an in-tree evaluator with no wire root, no SEMA family, and
   a non-canonical concept-schema dialect. It needs: a `signal-criome` (or meta)
   verb to define/store a contract, a `criome-contract`/`criome-policy` SEMA
   family, and the schema rewritten in the positional wire dialect that matches
   the rest of `lib.schema`.
2. **Connect contracts to the live authorization machinery.** The deployed
   `AuthorizationPolicyClass [SimpleSelfSigned ComplexQuorum]` is the two-class
   stub; the `Rule` tree is the generalization. The policy-table lookup the
   coordinator is missing (ARCHITECTURE §9) is exactly the slot where a stored
   `Contract` evaluates against collected-signature `Evidence`.
3. **Time-varying thresholds beyond the binary `TimeSwitch`.** `vhs2` asks for
   "thresholds that increase or decrease over elapsed time"; today there is only
   a single-boundary before/after switch. A graduated/piecewise time-threshold
   object is missing.
4. **The divergence-reconciliation + LLM-oracle objects.** `AgreementRule`/
   `AgreementFact` exist as fact-matching stubs but carry no notion of *two
   diverged networks*, no oracle-call object, and no statement that the oracle
   provider is itself resolved through an identity contract. The
   `domain-criome` `Intelligent` resolution scope + content-addressed
   delegation chain is the pattern to borrow; the reconciliation object family
   is the main net-new vocabulary.
5. **Meta verb for policy mutation.** `meta-signal-criome` has only `Configure`;
   defining/amending a contract is a meta-class operation with no verb yet.
6. **Naming/dialect reconciliation.** The POC uses `IdentityHandle`/`KeyAtom`/
   `Moment` wrappers and the spelling **criome** in the schema header while the
   wire uses bare `Identity`/`TimestampNanos` and the repos are **criome**;
   converge on one spelling and decide whether the handle wrappers survive.

## Source paths cited

- `signal-criome/schema/lib.schema`, `signal-criome/examples/canonical.nota`
- `criome/schema/criome.language.schema`, `criome/schema/criome.concept.schema`
- `criome/src/language.rs`, `criome/src/admission.rs`, `criome/src/master_key.rs`,
  `criome/src/tables.rs`, `criome/src/actors/registry.rs`, `criome/src/actors/store.rs`
- `criome/tests/language.rs`
- `criome/ARCHITECTURE.md` (§4 wire vocabulary, §5 SEMA families, §9 status)
- `meta-signal-criome/schema/lib.schema`, `meta-signal-criome/ARCHITECTURE.md`
- `signal-domain-criome/schema/lib.schema`, `domain-criome/ARCHITECTURE.md`
