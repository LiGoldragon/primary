# 138/7 — Router↔criome forward-attestation seam (milestone-3 design spec)

Design only. No code, no branch this round. This spec lifts the
`Error::CriomeVerifierUnavailable` refusal that `router.rs:1001`
(`from_daemon_configuration`, branch `transport-p1-fixes-138`) installs whenever
`criome_socket_path` is set, by specifying the criome-backed
`ForwardAttestationVerifier` that fills the seam left open at
`forward_attestation.rs:8-14`.

Grounded against live code: router `transport-p1-fixes-138`, criome on its current
checkout, and `signal-criome` on `signal-criome-positional-migration-142`.

## 1. What already exists (so the build is wiring, not invention)

The criome verification RPC is **already in the migrated contract** — this seam
does not add a contract type, it consumes one.

- `signal-criome` `Input::VerifyAttestation(VerifyRequest)` →
  `Output::VerificationResult(VerificationResult)` (`src/schema/lib.rs:1642`,
  `:1670`). `CriomeRequest = Input`, `CriomeReply = Output` (`signal-criome/src/lib.rs:15-16`).
- `VerifyRequest { attestation: Attestation, content: Content }` (`:1492`).
- `VerificationResult { result_decision: ResultDecision(VerificationDecision),
  verified_identity: Option<Identity>, verification_expires_at: Option<TimestampNanos> }`
  (`:1583`).
- `VerificationDecision ∈ { Valid, InvalidSignature, UnknownSigner, Expired,
  Revoked, ReplayAttempted }` (`:189`).
- The criome daemon already routes `VerifyAttestation` to
  `AttestationVerifier::verify` (`criome/src/actors/verifier.rs:40-109`), which:
  rejects content mismatch → `InvalidSignature`; resolves the signer in the
  identity registry → `UnknownSigner` if absent; `Revoked` if status is revoked;
  rejects scheme confusion; runs real BLS verify
  (`master_key.rs:129` `VerifyBls for BlsPublicKey`) against the **registered**
  key under DST `CRIOME-ATTESTATION-BLS12381G2-XMD:SHA-256_SSWU_RO_V1`
  (`master_key.rs:33`); and downgrades a past-expiry-but-valid signature to
  `Expired`.
- The daemon binds a `0600` Unix socket (`criome/src/daemon.rs:76-77`) — one
  daemon per Unix user, per `9s52`.
- A blocking Unix-socket client already exists: `CriomeClient`
  (`criome/src/transport.rs:107-138`) with `CriomeFrameCodec` length-prefixed
  framing. The router's milestone-3 client is the analogue of this.

The router side already has the receive path wired to call `verify` **off the
mailbox**, inside the ingress task (`router.rs:377-382`, `TailnetForwardIngress::handle_forward`,
an `async fn`). The `ForwardAdmissionWindow` (`forward_attestation.rs:137-205`)
is built and unit-tested but **not yet invoked** in the live
`ApplyForwardedMessage` handler (`router.rs:1502-1520` → `RouterRoot` at `:2898`);
wiring it is part of this milestone.

So milestone 3 = a new `ForwardAttestationVerifier` impl in router that calls the
existing criome RPC, plus wiring `ForwardAdmissionWindow` into the apply path,
plus a small router-side identity-registry projection. No new criome daemon
surface; one already-present contract RPC.

## 2. Router-side seam: `CriomeForwardVerifier`

The seam is `forward_attestation.rs:31` `ForwardAttestationVerifier`
(`attest` + `verify`), held as `Arc<dyn ForwardAttestationVerifier>` in
`RouterNetworkConfiguration` (`router.rs:932`), shared by `RouterPeerDelivery`
(sending, `peer_delivery.rs:38`) and `TailnetForwardIngress` (receiving,
`router.rs:341`).

### 2.1 Sync vs async — and the async-trait toolchain risk

**Keep the trait synchronous (no `async fn`). This is the load-bearing decision.**

`ForwardAttestationVerifier` is used as `Arc<dyn …>`. The router builds on edition
2024 / Rust 1.89 stable (`router/rust-toolchain.toml`,
`Cargo.toml` `rust-version = "1.89"`). Native `async fn` in a trait (RPITIT) is
stable since 1.75 and the codebase already uses it for `AsyncConnectionRuntime`
(`router.rs:413`) — **but only on a statically-dispatched impl**. An `async fn`
in trait is **not dyn-compatible**: you cannot have `Arc<dyn ForwardAttestationVerifier>`
if `verify` is `async fn`, without either the `#[async_trait]` macro (boxes every
call, adds a proc-macro dep, and was deliberately avoided elsewhere in this tree)
or `trait_variant` + hand-written `Box<dyn Future>` returns. Both are toolchain/ergonomics
risk the seam does not need.

The criome call is one connect + one write + one read on a **local** `0600` Unix
socket (sub-millisecond, no network). Make it blocking and keep the trait sync.
The receive path already runs `verify` off the mailbox in the ingress task
(`handle_forward`, `router.rs:377`), so a blocking syscall there must not stall the
actor — wrap the criome round-trip in `tokio::task::spawn_blocking` (or run the
ingress accept loop on a blocking-friendly runtime). The clean shape:

```
struct CriomeForwardVerifier {
    client: CriomeUnixClient,          // owns the socket path; data-bearing
    registry: RouterIdentityProjection, // RemoteRouterIdentity ↔ criome Identity + registered key
    local_signer: LocalForwardSigner,  // this router's criome-issued signing handle (attest side)
}
impl ForwardAttestationVerifier for CriomeForwardVerifier {
    fn attest(&self, payload, nonce, issued_at) -> RouterPeerAttestation { … }   // sync
    fn verify(&self, attestation, payload) -> Result<RemoteRouterIdentity, RouterForwardRefusalReason> { … } // sync, blocking criome round-trip
}
```

Every method here lives on a data-bearing noun (`CriomeForwardVerifier` holds the
client, projection, and signer), satisfying the no-free-function rule. `CriomeUnixClient`
mirrors `criome/src/transport.rs:107` but lives in router's crate (router cannot
depend on the criome daemon crate — only on `signal-criome`). It is its own noun
owning the path + codec.

### 2.2 The attest (send) side

`attest` must produce a `RouterPeerAttestation` whose `signature` criome will later
accept. There are two viable shapes; the spec recommends (B):

- (A) **Router asks criome to Sign on the send side too.** Symmetric: `attest`
  sends `Input::Sign(SignRequest)` to the local criome, gets a `SignReceipt`,
  projects it into `RouterPeerAttestation`. Costs one extra criome round-trip per
  outbound forward.
- (B, recommended) **Router holds a criome-issued signing handle.** The router's
  own forward-signing key is registered in criome's registry (cluster-root admitted,
  `admission.rs`); the router signs the forward preimage locally with that key
  (the same DST). `attest` is then pure-local and fast; only `verify` touches
  criome. This keeps the send path off the criome socket and matches `wckt` ("the
  router … never holds keys or verifies signatures" — note: the *attestation*
  signing key is a forward-identity key the router legitimately holds to prove
  *its own* identity, distinct from criome's master/attestation keys; criome
  remains the sole *verifier* and the sole *registrar*). This needs an explicit
  intent confirmation (see open questions) because it puts a signing key in the
  router process.

Either way the **preimage `attest` signs and `verify` checks must be identical and
canonical** over: `signer ‖ scheme ‖ content_digest(payload) ‖ issued_at ‖ nonce`,
domain-tagged. The offline stub's FNV `content_digest` (`forward_attestation.rs:77-96`)
becomes the canonical content digest fed to criome as `Content`/`ContentReference.digest`.

### 2.3 Refusal mapping (closed, total)

`verify` maps the criome `VerificationDecision` onto `RouterForwardRefusalReason`:

| criome `VerificationDecision` | router `RouterForwardRefusalReason` |
|---|---|
| `Valid` | `Ok(verified_origin)` — stamped from criome's `verified_identity`, never the wire `signer` |
| `InvalidSignature` | `AttestationInvalid` |
| `UnknownSigner` | `AttestationInvalid` (origin not cluster-root-admitted) |
| `Revoked` | `AttestationInvalid` |
| `Expired` | `AttestationInvalid` (criome-issued validity lapsed; distinct from router clock-skew) |
| `ReplayAttempted` | `ReplayDetected` |
| socket unreachable / decode error | `AttestationInvalid` (fail closed) |

Fail-closed is the security invariant the refusal at `router.rs:1001` already
encodes: if criome is unreachable the forward is **refused**, never admitted.

## 3. The BLS flow (what is signed, verified against which key)

1. **Send.** The originating router computes the canonical forward preimage
   (`signer ‖ scheme ‖ content_digest(payload) ‖ issued_at ‖ nonce`) and BLS-signs
   it (min-pk, signature in G2) under the criome DST with its **forward-identity
   key** (recommendation B), producing `RouterPeerAttestation`
   (`signal-router` `:496`): `{signer, scheme, public_key, signature,
   content_digest, issued_at, nonce}`.
2. **Wire.** The attestation rides inside `RouterForwardRequest` over the existing
   tailnet TCP forward (`peer_delivery.rs:97-119`), tailnet supplying confidentiality.
3. **Receive.** `TailnetForwardIngress::handle_forward` (`router.rs:377`) projects
   `RouterPeerAttestation` + `ForwardedMessagePayload` into a criome
   `VerifyRequest { attestation: Attestation, content: Content }`. The projection
   maps: router `signer`→ criome `Attestation.signer: Identity` (via the
   `RouterIdentityProjection`), router `{scheme, public_key, signature}` → criome
   `Attestation.envelope: SignatureEnvelope { scheme, public_key, envelope_signature }`,
   router `content_digest` → criome `Content` / `ContentReference.digest`,
   `issued_at` → `Attestation.issued_at`, `nonce` → `AuditContext.nonce`.
4. **criome verifies** (`verifier.rs:40-109`): content-binding equality, signer
   resolution **against the registered identity↔key binding** in its registry
   (admitted only by cluster-root signature, `admission.rs:86`), revocation status,
   scheme (no algorithm confusion), and the actual BLS verify of `signature` over
   the reconstructed `AttestationPreimage` (`master_key.rs:164-216`) against the
   **registered public key** (not the wire-claimed one — `verifier.rs:59` rejects a
   mismatch). The key verified against is therefore the cluster-root-admitted
   forward-identity key, the trust root being criome's configured `ClusterRoot`.
5. **Result.** `VerificationResult` returns `Valid` + `verified_identity`. The
   router stamps **`verified_identity`** as the authoritative origin
   (`ApplyForwardedMessage.verified_origin`, `router.rs:386`), never the wire field.

The DST is consistent end-to-end: criome's `Bls12_381MinPk` = pubkey in G1,
signature in G2, DST `…BLS12381G2…`. The router preimage MUST be signed under the
identical DST or `verify_bls` (`master_key.rs:143`) returns false. The seam must
not invent a router-local DST.

## 4. Replay / freshness ownership split (neither duplicated nor gapped)

Two layers each own a distinct guarantee; the seam pins which is which so they do
not double-count or leave a hole.

- **Router `ForwardAdmissionWindow` owns transport-hop freshness + per-hop replay.**
  It is keyed on `(verified_origin, nonce)` (`forward_attestation.rs:230-243`) and
  enforces clock-skew against `issued_at` (`±DEFAULT_FRESHNESS_WINDOW_NANOS = 300s`,
  `:145`). This is the **per-hop, per-receiving-router** guard: it answers "has THIS
  router already accepted this exact forward, and is it fresh on the wire?" It must
  be keyed on the **criome-verified** `verified_origin` (the output of step 5), not
  the wire `signer` — so it has to run **after** `verify` succeeds. Milestone-3
  work: invoke `ForwardAdmissionWindow::admit` in the `ApplyForwardedMessage`
  handler (`router.rs:1502`/`:2898`) where it is currently absent.

- **criome owns end-to-end authorization-level replay/freshness.** criome's
  `VerificationDecision::ReplayAttempted` and the attested-moment / nonce machinery
  (`ay3y`: every quorum-signed object carries a crystallized moment for "freshness
  and replay reasoning") own replay of the **inner authorization/agreement**, which
  is meaningful across hops and across the direct lane. The router's per-hop window
  is deliberately a coarser, local, capacity-bounded LRU (`:193-204`) and is **not**
  authoritative for authorization replay — it cannot be, since the same authorized
  object may legitimately traverse multiple hops.

The split, stated as the invariant: **the router window protects the transport hop
(this socket, this receiver, recent wall-clock); criome protects the authorization
semantics (this authorized object, ever).** They share the `nonce` value but answer
different questions, so there is no gap (criome catches cross-hop authorization
replay the router window cannot see) and no duplication (the router does not try to
remember authorizations forever; criome does not police per-hop wire freshness).
`ReplayAttempted` from criome maps to `ReplayDetected` so the operator sees one
refusal vocabulary.

Boundary check already in code: `ForwardAdmissionWindow::admit` rejects a
request whose outer `nonce`/`issued_at` disagree with the attestation's inner copy
(`forward_attestation.rs:167-171`) — that envelope-binding check stays router-side
and is independent of criome.

## 5. Fit with `lt44`'s two lanes

`lt44` (Decision, confirmed 2026-06-18) splits CriomOS transport into two lanes.
This seam is **the per-hop LOCAL forward-verification lane only** — explicitly
distinct from the direct criome-to-criome quorum lane.

- **General fabric lane (this seam).** The router is the payload-blind fabric;
  cross-host forwards carry a `RouterPeerAttestation` and the receiving router
  reaches criome **locally over the `0600` Unix socket on the receiving host** to
  verify. criome "never holds keys or verifies signatures; that is criome's job,
  reached through a verifier seam" — the verifier seam is exactly
  `ForwardAttestationVerifier`. No router→criome network hop: the criome consulted
  is always the **local** daemon of the receiving host (per `9s52` per-Unix-user
  custody; the receiving router asks its own host's criome whether the inbound
  origin identity is admitted in that criome's registry).
- **Direct criome-to-criome quorum lane (NOT this seam).** Time-sensitive agreement
  (quorum signing, crystallized-time windows, `ay3y`, `m0p2`) uses criome's own
  direct peer lane, carrying agreement/authorization messages only. That lane is
  out of scope here; report 138/2's "ride the router for general traffic" recommendation
  governs general non-time-sensitive criome traffic, which is a *separate* future
  build from this forward-attestation seam.

This seam touches only the first lane: it is per-hop, local, and synchronous, with
no quorum and no cross-criome messaging. The freshness split in §4 is precisely the
seam between "per-hop local" (router window) and "authorization-level, possibly
quorum-backed, possibly crossing the direct lane" (criome).

## 6. Non-circular argument

The worry: router depends on criome (to verify a forward), and 138/2's ride-the-router
plan has criome-quorum depend on the router (to deliver a solicitation). Read naively
that is a cycle. It is not, for two independent reasons:

1. **Different layers, different artifacts.** "Router verifies a forward via criome"
   is a **per-hop, local, synchronous** call: receiving router → its own host's
   criome over a Unix socket, about the **outer transport attestation**
   (`RouterPeerAttestation`). "criome-quorum delivers via router" is an
   **end-to-end, cross-host** path about the **inner agreement envelope**
   (`StampedSignatureEnvelope`, `signal-criome:1200`). These are two different
   message classes at two different layers — the dependency graph has no node that
   depends on itself.
2. **The dependencies do not close a runtime loop.** The router→criome verify call
   is local and completes without any router forward (it is a Unix-socket RPC to a
   co-resident daemon). The criome-quorum→router deliver path uses the router *after*
   the local verify has already gated the hop. Verification (forward, local) is
   strictly upstream of delivery (solicitation, end-to-end); delivery never needs to
   re-enter verification of the same frame on the same host. Concretely: to **verify**
   an inbound forward, the receiving router needs only its **local** criome — it never
   needs to **forward** anything to complete a verify. So even when criome later rides
   the router to deliver a quorum solicitation, that solicitation's own per-hop verify
   bottoms out at each hop's **local** criome, not at a forward. No frame waits on its
   own delivery.

Stated as the invariant a future maintainer must preserve: **the verify dependency
is always to the local co-resident criome and never requires a router forward to
resolve; therefore adding criome→router delivery cannot create a wait-for cycle.**
The graceful-degradation correlate (138/2 item 1): if the local criome is down,
forwards fail closed (refuse); if the router is down, criome quorum degrades to
`pending`/`expiry`. Neither outage deadlocks the other.

## 7. Collision check against the designer's ACTIVE nfvm head-loop work

The ACTIVE designer work to avoid: `nfvm` — `AuthorizedObjectKind::Head`,
`CRIOME-AUTHORIZED-HEAD-V1`, `MirrorAdopter`, in criome's language/head/mirror
surfaces.

**Finding: no source overlap on any current branch.** A grep for `MirrorAdopter`,
`AuthorizedObjectKind::Head`, `CRIOME-AUTHORIZED-HEAD`, and `::Head` across
`language-content-addressed-bls`, `main`, `attested-moment-majority-guard-139`, and
`cluster-root-admission-ceremony` returns nothing — the nfvm head-loop work is
in-flight on a designer branch not yet landed into the checkouts this spec reads.
The current `AuthorizedObjectKind` (`signal-criome:1022`) has exactly
`{ Operation, Contract, Agreement, Time }`; `Head` is the nfvm addition.

**Where the two could touch, and how to stay clear:**

- **`signal-criome` contract enum `AuthorizedObjectKind` / `AuthorizedObjectInterest`
  (`:1022`, `:1040`).** nfvm adds a `Head` variant here and the
  `CRIOME-AUTHORIZED-HEAD-V1` domain tag. **This seam adds NOTHING to that enum** —
  it consumes the already-present `VerifyAttestation`/`VerificationResult` RPC. The
  forward-attestation build must not touch `AuthorizedObjectKind`, the authorized-object
  surfaces, or any head/mirror language file (`criome/src/language.rs`). Clear by
  construction: the seam's contract footprint is `VerifyRequest`/`VerificationResult`
  + the router's own `signal-router` types, none of which nfvm edits.
- **The migrated contract file `signal-criome/src/schema/lib.rs`.** Both efforts
  are downstream of the positional migration on `signal-criome-positional-migration-142`.
  If this seam needs any contract change (it should not — see §1), it would edit the
  same generated file nfvm edits, a merge hot-spot. Mitigation: **this seam declares
  zero `signal-criome` contract additions.** All new types live in the router crate
  (`CriomeForwardVerifier`, `CriomeUnixClient`, `RouterIdentityProjection`) and in
  `signal-router`. The only criome-repo code this seam might touch is the **client
  shape** (router's own copy of the `transport.rs` pattern) — which is in the router
  crate, not criome.
- **Identity registry (`criome/src/actors/registry.rs`, `admission.rs`).** The seam
  relies on cluster-root-admitted router forward-identities being registered here.
  This is shared infrastructure with the head-loop work (both authenticate against
  the registry), but it is **read-only consumption** by the verify path
  (`verifier.rs:46-55` already resolves signers) — the seam adds no new registry
  mutation. nfvm's `MirrorAdopter` operates on head/mirror adoption, a different
  write path. No write-write conflict.

**Coordination ask:** the forward-identity registration ceremony (recommendation B,
§2.2) reuses the cluster-root admission path (`admission.rs`) that the operator is
landing per the latest commit (`c8f2f51f`: admission GATE exists+tested, only the
signing ceremony missing). Sequence the forward-identity key registration **after**
that admission-signing ceremony lands, rather than in parallel, since both want the
same `ClusterRoot::admits` entry point. This is a sequencing dependency, not a code
collision.

## Intent

No capture from this spec — it is a design proposal sitting under the open
architectural slot, and `lt44` already anchors the two-lane decision this seam fits
into. Recommendation B (router holds a criome-issued forward-signing key) is the one
genuinely new trust-surface choice and needs a psyche confirmation before it becomes
a Decision; flagged in open questions, not recorded.
