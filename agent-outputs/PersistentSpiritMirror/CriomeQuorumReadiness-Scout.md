# Criome Quorum Readiness — Scout Map

Scope: read-only inspection of the `criome` crate at
`/git/github.com/LiGoldragon/criome` (the "BLS authentication/attestation
daemon", `repos-manifest.nota` Family Criome). Question: is the Criome
quorum-consensus concept (persistent multi-signature root-contract
establishment + M-of-N enforcement) production-ready for the persistent,
both-directions Spirit mirror whose rule is "a quorum of nodes' Criomes
authorizes, or nothing changes"?

No files were edited. No build or test was run. Claims are tagged
`[observed]` (direct code/output) vs `[interpretation]`.

## Verdict

**Partial.** The M-of-N quorum *evaluator* is real, durable, and wired to a
production request path (fail-closed threshold logic with per-signer BLS
verification over a reboot-surviving contract store) — but the multi-node
*signature collection/aggregation* across peer Criomes, the cross-host
transport that would carry peer votes, and a first-class cluster
membership/genesis ceremony are absent; the only live-witnessed flow is
1-of-1 on a single daemon. Criome can *judge* an already-assembled quorum;
it cannot yet *gather* one across nodes.

## Observations

### Real BLS cryptography (single-key)
- `[observed]` `blst = "0.3"` and `blake3 = "1"` are direct dependencies
  (`Cargo.toml`). No `anyhow`; typed errors via `thiserror`.
- `[observed]` `src/master_key.rs`: `MasterKey::sign` uses real BLS12-381
  min-pk (`blst::min_pk`) under domain-separation tag
  `CRIOME-ATTESTATION-BLS12381G2-...` (`ATTESTATION_DST`). `VerifyBls::verify_bls`
  on `BlsPublicKey` does real `Signature::verify`. Master secret persists to a
  `0600` file created atomically (`load_or_generate`, `persist`,
  `from_secret_file` rejects non-regular / loose-permission files). Tests
  `sign_then_verify_round_trips`, `tampered_message_fails_verification`,
  `persisted_key_reloads_to_the_same_public_key`.
- `[observed]` No BLS *aggregate*/threshold-signature anywhere: a crate-wide
  search for `aggregate|AggregateSignature|fast_aggregate|threshold.?sig`
  returns nothing. Quorum is N *individually verified* signatures, counted.

### Real M-of-N quorum evaluator — `src/language.rs`
- `[observed]` `Threshold::decide` (lines ~418-443): counts satisfied members,
  returns `EvaluationDecision::Authorized` iff `satisfied >= required`, else
  `Rejected(QuorumShort{required,satisfied})`. Genuine majority counting.
- `[observed]` `QuorumShape::is_valid_majority` (~671-674): enforces
  `required != 0 && required <= authorities && required > authorities/2`
  (strict majority — this is the 2-of-3 / 2-of-2 rule).
- `[observed]` `Evidence::has_valid_signature_from` (~568-583): per-member real
  BLS verification, binds each signature to the member's admitted key, the
  operation, and the `AttestedMoment` stamp; scheme-checked (min-pk only).
- `[observed]` Admission-time shape validation `Threshold::validate_shape`
  (~455-477) rejects `EmptyThreshold`, `ThresholdUnsatisfiable`
  (sub-majority), and `DuplicatePolicyMember`. `ContractStore::admit` also
  rejects `DanglingReference`.
- `[observed]` Full rule tree present and evaluated: `SignedBy`, `All`, `Any`,
  `Threshold`, `ActiveAfter/Until`, `TimeSwitch`, `Agreement`, `Workflow`,
  `Composition`, `EscalateToPsyche`. Time proofs
  (`AttestedMoment::rejection_reason`) also require a quorum of authority
  signatures.

### The evaluator IS wired to a production request path
- `[observed]` `CriomeRoot::evaluate_authorization` (`src/actors/root.rs`
  ~685-711): on `CriomeRequest::EvaluateAuthorization`, in
  `AuthorizationMode::Quorum` (the default — `daemon.rs:45`, `root.rs:81`) it
  calls `store.evaluate(&contract, &evidence, &registry)` — the real
  `language.rs` engine.
- `[observed]` `contract_store()` (~1123-1133) rebuilds a `ContractStore` from
  the persisted contract snapshot; `key_registry()` (~1135-1162) rebuilds a
  `KeyRegistry` from persisted identities↔keys. Evaluation is fail-closed:
  `MissingContract` → `ContractMissing`, missing registry/store →
  `MalformedRequest`.
- `[observed]` Contracts are admitted via `CriomeRequest::AdmitContract` →
  `StoreContract` → durable `CONTRACTS` sema-engine table; identities persist
  via `put_identity`. ARCHITECTURE §9 states "the contract DAG therefore
  survives daemon restart."

### Persistence / reboot survivability — `src/tables.rs`
- `[observed]` `CriomeTables::open` builds on `sema_engine::Engine::open` from a
  filesystem `StoreLocation` path (records rkyv-encoded), registering durable
  tables: identities, revocations, attestations, `authorization_states`,
  `authorization_replay_nonces`, `contracts`, `signature_solicitations`,
  `submitted_signatures`, intercept policies, parked requests, and slot
  counters.
- `[observed]` ARCHITECTURE §9: on start `CriomeRoot` reconciles the master key
  against the registered `Host("criome")` identity and fails loud
  (`Error::Startup`) on mismatch, so a restored store beside a wrong key cannot
  mint attestations its own verifier would reject.

### Cluster-root admission gate (single-key, 1-of-1) — `src/admission.rs`
- `[observed]` `ClusterRoot::admits`: a *single* configured cluster-root key
  verifies a BLS signature over a canonical `RegistrationStatement`
  (identity+key+purpose, tag `CRIOME-REGISTRATION-ADMISSION-V1`).
- `[observed]` It is wired in: `IdentityRegistry::register` (`registry.rs`
  ~106-131) returns `UnauthorizedRegistration` unless the configured
  `ClusterRoot` admits the registration (dev/virgin daemons with no configured
  root skip the gate). The cluster-root public key comes from daemon config
  (`configure`, `root.rs` ~419; `CriomeDaemonConfiguration.cluster_root()`).
  Note: the `admission.rs` module doc-comment still says the gate is unwired —
  that comment is stale relative to `registry.rs`.
- `[observed]` This is a *1-of-1 trust anchor over membership admission*, not a
  quorum over membership.

### The OTHER authorization surface (signal-call lifecycle) is 1-of-1 / skeleton
- `[observed]` `AttestationSigner::sign_authorization_grant` (`signer.rs`
  ~265-309) hardcodes `AuthorizationPolicyClass::SimpleSelfSigned`,
  `RequiredSignatureThreshold::new(1)`, a single satisfied signer (itself), and
  `SignatureAuthorizationResult::SingleSignature`. The `ComplexQuorum` policy
  class exists in the type system but the runtime never emits it.
- `[observed]` `AuthorizationCoordinator::verify_authorization`
  (`authorization.rs` ~160-172) grants on a *digest match*
  (`request_digest == authorized_object_digest`), not a signature quorum.
- `[observed]` `route_signature_request` / `submit_signature`
  (`authorization.rs` ~174-196) only *store* solicitations/submissions and
  return receipts; nothing counts them against a threshold or flips state to
  Granted. `CreateAuthorizationState::signing` (`store.rs` ~250-264) always
  sets `missing_authorities: Vec::new()`.
- `[observed]` ARCHITECTURE §9 concedes for this coordinator: "This is still a
  skeleton: master-key signing, pushed observation events, and quorum
  aggregation are the next authorization milestones."

### No cross-node collection; cross-host transport is an open slot
- `[observed]` `CriomeRequest::RouteSignatureRequest` / `SubmitSignature` route
  to the coordinator, which only persists rows. No code dials a peer criome
  socket, solicits, receives, and assembles Evidence (no `UnixStream::connect`
  / peer-dial in the actors).
- `[observed]` ARCHITECTURE §6.1: "Complex (quorum) policies require signatures
  from peer criome daemons"; "**Cross-host transport is an open design
  slot**"; "Single-host quorum (peers under different Unix users on one host)
  works today" — i.e. only when Evidence is pre-assembled locally.

### What has actually been demonstrated live
- `[observed]` `src/bin/criome-cluster-witness-test.rs` (~203-242, behind the
  non-production `cluster-witness` feature) seeds identities + a **1-of-1**
  contract, admits it over the socket, then proves (a) one valid signature →
  `Authorized` and (b) threshold-short (0 signatures) → not `Authorized`. It
  exercises the real evaluator end-to-end but at **threshold 1 on a single
  daemon**. Sibling witnesses cover `AutoApprove` and `ClientApproval` modes.
- `[observed]` `ContractStore::evaluate` (the real engine) is called only from
  `tests/language.rs` and the `cluster-witness`-gated witness binaries — never
  from a non-test production caller other than the `EvaluateAuthorization`
  request handler in `root.rs`.

## Interpretations

- `[interpretation]` The evaluator is production-quality for *judging* an
  already-assembled multi-signature Evidence bundle inside one daemon: it does
  real per-signer BLS verification, strict-majority counting, admission-time
  shape safety, and is fail-closed. Arbitrary M-of-N (2-of-3, 2-of-2) is
  supported by the code even though only 1-of-1 has been witnessed.
- `[interpretation]` The psyche's rule ("a quorum of *nodes'* Criomes
  authorizes, or nothing changes") needs the part that is missing: a protocol
  that solicits each node's signature, carries it across hosts, and drives a
  cluster decision. Criome today is the judge without the ballot box. Nothing
  currently pushes a Spirit-mirror change *through* the quorum path with
  collected peer signatures.
- `[interpretation]` The "root contract naming the signer set" maps onto a
  durable content-addressed policy `Contract` with a `Threshold` rule over
  `PolicyMember::KeyMember(identity)`. Establishing it is operator-driven
  (`AdmitContract` + registering each node key, itself gated by the single
  cluster-root); there is no automatic genesis ceremony, no membership-rotation
  flow, and no distinguished cluster-membership object type.
- `[interpretation]` Two authorization surfaces invite confusion. The
  *contract-quorum* path (`AdmitContract`/`EvaluateAuthorization`) is the real
  one; the *signal-call* path (`AuthorizeSignalCall`/`SubmitSignature`/
  `VerifyAuthorization`) is a 1-of-1 skeleton. A mirror-change design should
  target the contract path.
- `[interpretation]` The earlier lane note ("Stage-A 1-of-1 works, Stage-B
  multi-node quorum unbuilt") is directionally right but *understates* the
  evaluator: the M-of-N judging engine and its durable contract store are built
  and wired; what is unbuilt is the multi-node collection/aggregation and
  cross-host transport (fairly called Stage-B).

## The gap (establishment / enforcement / threshold / aggregation / persistence)

- **Establishment — PARTIAL.**
  - *There:* durable content-addressed policy contracts (the membership/threshold
    record) admitted via `AdmitContract`, surviving reboot; a single cluster-root
    admission anchor that persists (config) and gates member registration.
  - *Missing:* a first-class cluster genesis/membership ceremony, a distinguished
    "root contract" bootstrap, and membership rotation. Today an operator must
    hand-admit the threshold contract and register each node's key.
- **Threshold — BUILT (in the evaluator), NOT in the signal-call path.**
  Arbitrary M-of-N with strict-majority validation at admission, derived from the
  contract's `required_signatures` and member set. The signal-call grant path is
  still hardcoded to `SimpleSelfSigned` / threshold 1.
- **Enforcement — PARTIAL / context-dependent.**
  Contract evaluation is fail-closed and real (threshold-short → Rejected,
  witnessed at threshold-1). But it enforces only over the signatures already
  present in the Evidence handed to *one* daemon; it does not gather them. The
  signal-call `VerifyAuthorization` is a digest match, not a signature quorum.
- **Aggregation / cross-node collection — MISSING.**
  No BLS aggregate/threshold signatures (N individual sigs counted). No working
  peer signature-solicitation loop (`RouteSignatureRequest`/`SubmitSignature`
  persist but do not dial peers). Cross-host transport is an explicit open design
  slot (candidate shapes only: TLS signal-frame, per-frame signed envelope, SSH
  tunnel).
- **Persistence — BUILT.**
  Master key (0600 file), identities, contracts, authorization states, replay
  nonces durable via sema-engine; contract DAG survives restart; startup
  master-key↔identity reconciliation fails loud on mismatch.

To reach "quorum-authorizes-or-nothing" across nodes, an implementer must add,
on top of the existing evaluator: (1) a cluster membership/genesis step that
durably establishes the signer set and each node's registered key; (2) a
cross-host peer transport (one of the three candidate shapes); (3) a
signature-solicitation/collection driver that gathers each node's operation
signature and assembles the `Evidence` bundle; (4) a caller (the mirror path)
that submits the change as an `EvaluateAuthorization` and withholds the change
until the decision is `Authorized`, retrying/waiting when the quorum cannot yet
be gathered; and optionally (5) fold the signal-call authorization path into the
contract-quorum path so there is one enforcement surface, not two.

## Code locations (pickup map)

- `src/language.rs` — the quorum/policy evaluator (`Threshold::decide`,
  `QuorumShape::is_valid_majority`, `Evidence::has_valid_signature_from`,
  `ContractStore::{admit,evaluate}`, `KeyRegistry`). The M-of-N core.
- `src/actors/root.rs` — request routing; `evaluate_authorization` (~685),
  `admit_contract` (~1083), `contract_store`/`key_registry` (~1123/1135),
  `configure` (~407, cluster-root wiring), `apply_*_approval` (parked flow).
- `src/actors/signer.rs` — `sign_authorization_grant` (~265, hardcoded 1-of-1;
  where a real contract-derived grant would be produced).
- `src/actors/authorization.rs` — signal-call lifecycle
  (`verify_authorization`, `route_signature_request`, `submit_signature`) — the
  un-aggregated path to fold in.
- `src/admission.rs` — `ClusterRoot` single-key admission gate (stale
  doc-comment).
- `src/actors/registry.rs` — `register` gating on `ClusterRoot`.
- `src/master_key.rs` — real BLS sign/verify + key persistence.
- `src/actors/store.rs` + `src/tables.rs` — durable sema-engine tables;
  `CreateAuthorizationState` variants; contract/identity/solicitation
  persistence.
- `src/daemon.rs` — daemon assembly, `AuthorizationMode` default `Quorum`,
  socket binding (working 0660, meta 0600).
- `src/bin/criome-cluster-witness-test.rs` — the live 1-of-1 end-to-end proof
  (feature `cluster-witness`).
- `ARCHITECTURE.md` §6.1 (peer routing / cross-host open slot), §8
  cross-system trust root (cluster-root), §9 (implementation status, incl. the
  "quorum aggregation is a next milestone" admission).
- Governing Spirit intent already cited in code (not re-queried; brief supplied
  the operative intent): `ermr` (cluster-root trust decision, `admission.rs`),
  `psc6` (master-key custody, `master_key.rs`).

## Unknowns (and what would resolve them)

- `[unknown]` Whether any deployment/tooling actually establishes an initial
  2-of-3 membership contract and registers all three node keys, or whether that
  is entirely manual. I found the mechanism (`AdmitContract` + register), not a
  seeding routine. Resolve via: CriomOS deployment Nix modules,
  `meta-signal-criome` config, or a witness test at threshold 2-of-3.
- `[unknown]` Whether `EvaluateAuthorization` is reachable by the persona-router
  in production, or only by the witness harness. Resolve via: the router's
  criome client call sites (`signal-router`).
- `[unknown]` Whether the single-host multi-user "quorum works today" path has a
  real signature-collection driver, or still requires the caller to pre-assemble
  `Evidence`. Code shows `Evidence` is caller-supplied to `EvaluateAuthorization`
  and I found no collection driver; I did not exhaustively read every binary.
- `[unknown]` Exact durability guarantees of `sema_engine::Engine` (WAL/fsync
  semantics) beyond the asserted "survives restart" — I read the API usage, not
  the engine internals.

## Not checked (explicit)
- The `signal-criome` / `meta-signal-criome` contract crate internals (wire type
  definitions for `Contract`, `Threshold`, `AuthorizationEvaluation`, etc.).
- The CriomOS cluster deployment and the persona-router↔criome integration.
- No build, `cargo test`, or witness binary was executed.
