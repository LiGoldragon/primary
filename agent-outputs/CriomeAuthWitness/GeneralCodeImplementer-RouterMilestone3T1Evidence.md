# Router Milestone 3 (T1) — real criome client behind ForwardAttestationVerifier

Task: replace the offline `AcceptFixedTestIdentity` stub on the persona
router's forward-attestation seam with a real criome client that BLS-signs
outbound forwards and verifies inbound ones over `config.criome_socket_path`,
proven by a Rust integration test that exercises the real BLS path (accept AND
fail-closed refuse). Brief: `reports/capacityAdmissionSlice/6-Translation-criome-auth-witness-vm-test.md`, card T1.

Status: COMPLETE. Both branches committed and pushed; cargo suite green; the two
named Nix checks build and pass in the Nix sandbox (on prometheus via the remote
builder). Routing/transport code changed zero lines.

## 1. Attestation type-mapping design decision (the reviewed checkpoint)

`RouterPeerAttestation` (signal-router) and criome's `Attestation` /
`ContentReference` / `VerifyRequest` are different types. The mapping (in
`router/src/criome_attestation.rs`) is the lossless projection the signal-router
schema already calls for ("mirrors what criome produces"; "receiver projects it
back into criome's Attestation").

### Digest derivation (the soundness core)

The criome `ContentReference.digest` is `ObjectDigest::from_bytes` (blake3, the
schema-emitted hasher) over `ForwardContentPreimage`: a domain-tagged,
length-delimited canonical encoding of

- the sending router's `RemoteRouterIdentity` (the origin), AND
- the entire `ForwardedMessagePayload`: source actor, destination actor, body,
  every attachment, and every `RoutedContractObject`'s contract name /
  operation / declared size / payload octets.

On send, the router computes this digest, hands it to criome `Sign`, and gets
back a BLS signature over criome's full preimage (which includes
`content.digest`). On receive, the router INDEPENDENTLY re-derives the digest
from the wire-claimed origin and the actually-received payload, reconstructs
criome's `Attestation`, and calls criome `VerifyAttestation(attestation,
re-derived-content)`. criome cross-checks `attestation.content == request.content`
AND verifies the BLS signature over the preimage. Therefore:

- a tampered payload → different re-derived digest → content mismatch / BLS
  failure → refused;
- a relabelled origin → different re-derived digest → refused (origin is bound,
  so the `verify`-returned `RemoteRouterIdentity` is cryptographically vouched,
  honouring "never the wire-claimed field");
- a signature from a criome whose key the verifier does not hold → criome
  resolves the signer identity to a different registered key → `InvalidSignature`;
- an unsigned/blank signature → BLS failure → `InvalidSignature`.

This is non-degenerate: it cannot pass regardless of content. `verify` accepts
iff `VerificationDecision::Valid`; every other decision and every transport error
collapses to `RouterForwardRefusalReason::AttestationInvalid` (fail-closed).

### The one new wire field (necessary schema change)

criome SERVER-STAMPS its own `issued_at` into the BLS-signed preimage
(`criome/src/actors/signer.rs` via `master_key::AttestationPreimage`). The
router's forward `issued_at` is a different value, and the freshness/replay
admission window (`forward_attestation.rs:167-171`) cross-checks
`attestation.issued_at == request.issued_at` (both the router's clock). Since
`peer_delivery.rs::forward_request` is off-limits (routing code) and pins
`RouterPeerAttestation.issued_at` to the router clock, criome's stamp cannot
reuse that field. Resolution: add `AttestationIssuedAt TimestampNanos` to
`RouterPeerAttestation` (appended last, positional fields stable). `issued_at`
stays the router clock (admission invariant + offline stub unchanged);
`attestation_issued_at` carries criome's stamp so the receiver reconstructs
criome's exact preimage. This was the single load-bearing impedance.

### Fixed conventions reproduced on both sides

content purpose = `SignedObject`; schema_version = `signal-router/RoutedContractObject`;
audit purpose = `SignedObject`; audience = `persona-router-peer`; policy_version =
`router-forward-attestation-v1`; audit nonce = the forward nonce; criome signer
identity = `Host("criome")` (matches criome's hardcoded `criome_identity`);
attestation_expires_at = None.

### Alternative rejected

Carrying the whole criome `Attestation` as opaque rkyv bytes in a new wire field:
rejected — it duplicates signature/public_key/digest, still needs a schema field,
and discards the schema's stated "project back into criome's Attestation" design.
The single typed `AttestationIssuedAt` field is the minimal lossless delta.

## 2. Files changed

signal-router (branch `criome-forward-attestation`, rev `d212ea8a0a3b3cf76c872d4f7cf3e5735d9e920d`):
- `schema/lib.schema` — add `AttestationIssuedAt TimestampNanos` to `RouterPeerAttestation`.
- `src/schema/lib.rs` — regenerated (`SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`).
- `tests/round_trip.rs`, `tests/canonical_examples.rs`, `examples/canonical.nota` — positional field added.
- `ARCHITECTURE.md` — attestation field-list prose updated.

router (branch `criome-forward-attestation`, rev `7141695c4863523e20867181c79525fab9e64b95`):
- `src/criome_attestation.rs` — NEW: `CriomeForwardAttestation` verifier, the
  `signal-criome` wire client, `ForwardContentPreimage` digest derivation, the
  deterministic criome mapping.
- `src/daemon.rs` — construction site 1: `from_configuration` builds the criome
  verifier when `criome_socket_path` is set, else the offline stub.
- `src/router.rs` — construction site 2: `RouterNetworkConfiguration::criome_listening` (+ import). No routing/transport logic touched.
- `src/forward_attestation.rs` — offline stub `attest` sets the new field.
- `src/lib.rs` — module + `CriomeForwardAttestation` export.
- `tests/criome_forward_attestation.rs` — NEW integration test.
- `flake.nix` — two named checks.
- `Cargo.toml` — signal-router → branch `criome-forward-attestation`; `criome` + `signal-criome` dev-deps.
- `Cargo.lock` — signal-criome 0.3→0.5, signal-frame 0.2→0.3, schema/schema-rust advanced.

## 3. Exact test commands and output

Inner-loop (repo toolchain), in `~/wt/github.com/LiGoldragon/router/criome-forward-attestation`:

```
$ cargo test --test criome_forward_attestation
running 2 tests
test router_accepts_forward_under_real_criome_bls_attestation ... ok
test router_refuses_forwards_without_a_valid_criome_attestation ... ok
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Full router suite (no regression from the dependency bump; offline
`end_to_end_remote_forward` still green): `cargo test` → all binaries `ok`
(lib 5, actor_runtime_truth 32, authorized_object_fanout 3,
criome_forward_attestation 2, end_to_end_remote_forward 1, no_shared_locks_truth 1,
observation_truth 12, process_boundary 3, schema_generated 2, smoke 16).

Durable Nix-owned witnesses (cargo --release --locked inside the Nix sandbox,
built on prometheus via the remote builder):

```
$ nix build -L .#checks.x86_64-linux.router-accepts-only-real-criome-attestation
router-test> +++ command cargo test --release --locked --test criome_forward_attestation router_accepts_forward_under_real_criome_bls_attestation -- --exact
router-test> test router_accepts_forward_under_real_criome_bls_attestation ... ok
router-test> test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out

$ nix build -L .#checks.x86_64-linux.router-refuses-forward-without-criome-credential
router-test> +++ command cargo test --release --locked --test criome_forward_attestation router_refuses_forwards_without_a_valid_criome_attestation -- --exact
router-test> test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out
```

What the refusal test proves in one run, against one receiving router + one
criome daemon (`router-test`'s `verify-trust` criome) plus a foreign criome
(`verify-foreign`, independent key):
- accept control: a forward BLS-signed by the trusted criome → `ForwardAccepted`;
- wrong key: same payload+identity but signed by the foreign criome → `ForwardRefused(AttestationInvalid)`;
- tampered: trusted-signed, then routed-object octets changed → `ForwardRefused(AttestationInvalid)`;
- unsigned: trusted-built, signature stripped → `ForwardRefused(AttestationInvalid)`.
The accept control sharing the same router+criome makes the refusals un-fakeable:
a degenerate always-accept mapping would accept the bad three and fail the test.

## 4. Branch + revision (for T4 to consume)

- signal-router: branch `criome-forward-attestation`, rev `d212ea8a0a3b3cf76c872d4f7cf3e5735d9e920d` (pushed to origin).
- router: branch `criome-forward-attestation`, rev `7141695c4863523e20867181c79525fab9e64b95` (pushed to origin). router's Cargo.toml already points signal-router at the branch.
- Not landed on main (gated on the independent audit, per brief). Canonical checkouts remain clean on main.

## 5. What surprised me / what T4 and the auditor MUST know

1. **criome's signing identity is hardcoded, not configurable.**
   `criome/src/actors/root.rs:1164` sets `criome_identity = Host("criome")`
   for every instance, and the verifier binds signer-identity → registered key
   (`criome/src/actors/verifier.rs:45-61`). Consequence: two INDEPENDENT criomes
   (A, B) with independent master keys CANNOT achieve a positive cross-instance
   verify by `RegisterIdentity` of A's pubkey, because B already self-registers
   `Host("criome")` with B's OWN key and the lookup returns B's key (mismatch),
   and a second `Host("criome")` registration collides. **T4's cross-instance
   trust anchor must therefore be one of: (a) the two criomes SHARE the signing
   key (shared cluster master key = shared cluster identity), or (b) a small
   criome change to make `criome_identity` configurable (A=`Host("criome-a")`,
   B=`Host("criome-b")`) plus a `RegisterIdentity` seed of A's pubkey into B.**
   This concretely answers the brief's D0/trust-anchor open question.

2. **T1 proves the seam with the trust anchor that needs no criome change.** The
   positive path uses ONE shared criome dialed by both routers (single trust
   domain). The load-bearing nature of the key binding is proven separately by
   the foreign-criome wrong-key refusal — criome returns Valid only for a
   signature bound to the key it holds. The full two-distinct-criome positive is
   a T4 concern gated on decision (1).

3. **Dependency baseline advanced.** Admitting the real `criome` crate forced
   signal-criome 0.3→0.5 and signal-frame 0.2→0.3 (plus schema/schema-rust) in
   router's lock — this is the criome generation the witness deploys. T4 must
   build the whole stack on consistent refs (router branch + signal-router branch
   + current criome main); router↔criome interop needs the same signal-frame
   wire generation on both VMs.

4. **`attest` is infallible by trait contract**, so a sender that cannot reach
   criome emits a fail-closed unsigned attestation (real digest, empty
   signature) which any receiver's criome refuses — rather than surfacing an
   error (which would require editing the off-limits `peer_delivery.rs`). The
   criome client call is synchronous/blocking inside the actor/ingress async
   context; fine for the slice and the co-resident-daemon topology, but a
   production hardening follow-up is to move it off the mailbox (spawn_blocking)
   — it cannot be done without changing the sync trait surface, so it is flagged,
   not done.

5. **Zero routing/transport lines changed**, as required: `peer_delivery.rs`,
   `remote_router.rs`, and `router.rs` routing logic are untouched; the only
   `router.rs` edits are one import and the additive `criome_listening`
   constructor. The seam swap is the two construction sites plus the new module.

6. **Follow-up (provisional recommendation, not authority):** the router's
   refusal path still emits no durable trace (only the wire reply), as the brief
   noted — the negative control is witnessed via the reply outcome here; in T4 it
   is additionally witnessed by the mirror's absence-of-append.
