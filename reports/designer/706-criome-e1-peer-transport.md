# 706 — E1: cross-criome peer transport (design + situation update)

The headline multi-machine slice. E1 carries authorization signature traffic
between criome daemons on different hosts so a k-of-n quorum can assemble across
machines — the load-bearing gap behind the original "actually networked criome
cluster" goal. Governed by [criome owns key custody and is the authorization
decider; a multi-party quorum is k of n peer criome nodes signing with their own
master keys] (Spirit `p43g`).

## Situation at a glance

| Thread | State | Where |
|---|---|---|
| criome auth runtime (3 modes) | landed on main | criome `6a5e797` |
| Track A boundary hardening | landed on main (+174 tests) | criome `6a5e797` |
| ClientApproval park flow | **proven** (process-level, real daemon) | branch `criome-client-approval-witness` `2bb8645e` |
| auto-approve + 1-of-1 VM checks | green, **branch-only** (not on test-cluster main) | `criome-cluster-test` `115131f` |
| de-branch (input→main, merge to test-cluster main) | blocked: test-cluster claim + needs witness bins on criome main | cloud-operator lock |
| Prometheus VM-host test node | in progress (parallel lane) | system-designer |
| DigitalOcean live deploy | confirmed on a real droplet | cloud-designer `76`/`77` |
| witness bins on criome main | **landed by operator (de-branch step 1)** | criome `68b92c66` |
| **E1 peer transport** | **increments 1-3 landed + verified; inc-3 reviewed + hardened + re-verified** | contracts `signal-criome-peers` `f4b64fc5`; primitive `criome-peer-transport` `081f6f7c` |

## What already exists in criome (verified at `6a5e797`)

E1 is narrower than the roadmap implies: the peer-signature *message design and
actor plumbing are already built and in-process tested*. The two working-contract
verbs are live and routed to `AuthorizationCoordinator`, which persists both:

```rust
// criome/src/actors/authorization.rs — already on main, dormant (no network carrier)
async fn route_signature_request(&self, route: SignatureSolicitationRoute) -> CriomeReply {
    let request_slot = route.solicitation.request_slot.clone();
    let routed_to = route.routed_to.clone();
    if self.store_signature_solicitation(route).await.is_err() {
        return rejection(RejectionReason::MalformedRequest);
    }
    CriomeReply::SignatureRouteReceipt(SignatureRouteReceipt { request_slot, routed_to })
}

async fn submit_signature(&self, submission: SignatureSubmission) -> CriomeReply {
    let request_slot = submission.request_slot.clone();
    let signer = submission.signer.clone();
    if self.store_signature_submission(submission).await.is_err() {
        return rejection(RejectionReason::MalformedRequest);
    }
    CriomeReply::SignatureSubmissionReceipt(SignatureSubmissionReceipt { request_slot, signer })
}
```

So "B receives a solicitation" and "A receives a submission" exist. What is
missing is four things: (1) a **network carrier** for those frames; (2) a
**per-frame BLS envelope** so a receiver authenticates the sender before parsing;
(3) **peer addressing** in the daemon config; (4) **quorum tally** — nothing yet
reads `submitted_signatures` back, verifies a submission, decrements
`missing_authorities`, or flips state to `Granted` at threshold k (missing even
single-host).

`transport.rs` is `UnixStream`-only — there is no `TcpStream`/`TcpListener`
anywhere in the crate.

## Target architecture

```mermaid
flowchart TB
  subgraph hostA["host A — criome daemon"]
    wsA["Unix working socket 0600"]
    msA["Unix meta socket 0600"]
    ptA["TCP peer listener (NEW)"]
    rootA["CriomeRoot"]
    coordA["AuthorizationCoordinator"]
    storeA["StoreKernel + master key"]
    wsA --> rootA
    msA --> rootA
    ptA --> rootA
    rootA --> coordA --> storeA
  end
  reqA["local requester (SO_PEERCRED / 0600)"] --> wsA
  mentciA["mentci (client-approval)"] --> msA
  coordA -. "CriomePeerClient (NEW): BLS-enveloped frames over the tailnet" .-> hostB
  coordA -. .-> hostC
  hostB["host B — criome daemon (peer)"]
  hostC["host C — criome daemon (peer)"]
```

## The quorum flow (2-of-3, after `p43g`)

```mermaid
sequenceDiagram
  participant R as Requester
  participant A as criome A (local)
  participant B as criome B (peer)
  participant C as criome C (peer)
  R->>A: EvaluateAuthorization(object) [working socket]
  Note over A: A signs with its master key (sig 1 of k)
  A->>B: RouteSignatureRequest [TCP, BLS-enveloped]
  A->>C: RouteSignatureRequest [TCP, BLS-enveloped]
  Note over B,C: each verifies envelope + object, signs
  B-->>A: SubmitSignature [TCP, BLS-enveloped]
  C-->>A: SubmitSignature [TCP, BLS-enveloped]
  Note over A: tally: 2 of 3 >= k -> threshold met
  A->>A: status Granted; publish AuthorizedObjectUpdate
  A-->>R: Authorized
```

## Wire crypto

Each cross-host frame is BLS-signed by the sender criome's master key; the
receiver verifies the signature against the sender's *admitted* peer public key
*before* decoding the inner frame (`ARCHITECTURE.md:439`). Authenticity, not
confidentiality — the tailnet (WireGuard) provides the confidentiality layer
beneath. The envelope signature uses a **domain-separation tag distinct from
`ATTESTATION_DST`** so a peer frame can never be replayed as an attestation.

The envelope is a **thin authenticated header**, not a byte container. The peer
wire is two length-prefixed blobs: the header, then the inner `CriomeFrame`. The
signature covers the inner frame bytes; the receiver verifies before decoding
them (so no nested byte field, and `nota-next` stays out of the contract's link
surface):

```
peer frame = [ length-prefixed PeerEnvelope ][ length-prefixed CriomeFrame bytes ]
PeerEnvelope = { sender master public key, BLS signature over the following frame bytes }
verify: sender ∈ configured peers  AND  bls_verify(sig, frame_bytes, sender_pubkey, PEER_DST)  THEN decode the frame
```

## Increment plan (each compiles green on its own)

1. **Peer addressing contract (signal-criome)** — `PeerAddress`, `PeerNode`,
   `(Peers (Vec PeerNode))` on `CriomeDaemonConfiguration`. **DONE + verified**
   — branch `signal-criome-peers` `6315694` off `ff9ac192`; codegen regenerated,
   `expect_fresh()` + `--features nota-text` + 17 tests green; companion
   `with_peers()` / `peers()` accessors + `PeerNode::new` added in `src/lib.rs`.
2. **Wire envelope header (signal-criome)** — `PeerEnvelope`. **DONE + verified**
   — branch `signal-criome-peers` `f4b64fc5`; `expect_fresh()` + `--features
   nota-text` + tests green. Designed as a **thin authenticated header**
   `{ sender_public_key.BlsPublicKey  signature.BlsSignature }`, NOT a
   frame-carrying wrapper. (First pass embedded the frame as a `Bytes` scalar,
   which lowers to `nota_next::ByteSequence` and silently flipped `nota-next` to
   a non-optional dep of the whole contract crate — caught in review and reworked
   to the header so the inner frame is carried by the peer codec as the next
   length-prefixed blob, keeping `nota-next` optional.)
3. **Peer transport primitive (criome)** — **DONE + verified + reviewed** —
   branch `criome-peer-transport` `0fb1e0b1` off criome `68b92c66`. `CriomePeerCodec`
   (write/read enveloped: sign the exact length-prefixed `CriomeFrame` bytes under
   a distinct `PEER_FRAME_DST`, write `[envelope][frame]`, verify-before-decode),
   `CriomePeerClient` (sync TCP), a shared `LengthPrefixed` framing helper, and
   `Error::{PeerConnect, UnknownPeer, PeerSignatureRejected}`. Proven by a
   real-TCP loopback test (valid round-trip + tampered→`PeerSignatureRejected` +
   unadmitted→`UnknownPeer`), 15/15 green. Consumes the contract via a local-path
   `[patch]` scaffold (operator removes when landing `signal-criome-peers`).
   Adversarial review: **wire-framing clean** (bounds-checked before alloc on both
   blobs, typed errors, validating rkyv), **crypto sound** (preimage byte-identity,
   genuine DST separation, admitted-peer check, verify-before-decode, secure blst
   config), **concurrency** correct for a primitive. **Hardened** (`081f6f7c`):
   cross-DST negative regression test, client connect/read/write timeouts (5s),
   frame write-cap, dedicated `PeerEnvelope{Encode,Decode}` error variants, and a
   tighter 8 KiB pre-auth envelope cap. **Independently re-run green** by the
   designer — 62 tests, 0 failed, including `attestation_and_peer_frame_signatures_
   never_cross_verify` (the DST-separation guard) and the real-TCP round-trip +
   tamper/unknown-peer/closed-port negative cases.
4. **Daemon integration + solicitation + tally (criome)** — wire the primitive
   in: a third TCP peer listener in the serve loop **with a read timeout**
   (the review's one high finding: the current single-thread busy-poll would let a
   stalled remote peer freeze the daemon — TCP peers are remote/adversarial unlike
   the 0600 Unix sockets), read admitted peers + listen address from config
   (`Peers`), and `AuthorizationCoordinator` signs locally + solicits peers and
   aggregates k. Per the review, **outbound solicitation must be fire-and-collect
   off the actor/serve thread** (a worker pool / `spawn_blocking` with per-peer
   deadlines, concurrent dispatch, first-k-wins) — never a blocking
   `CriomePeerClient` call inside a Kameo handler. The tally is a
   read-modify-write of the persisted state record so it survives a restart, and
   **must bind a per-solicitation nonce/epoch into the signed frame** so a replayed
   peer signature is not counted as a fresh independent attestation (the transport
   is authenticity-only; freshness lives here).
5. **2-of-2 witness + two-node nixosTest** — the first real cross-kernel quorum
   proof (needs the test-cluster repo; currently lock-blocked).
6. **N-node + DigitalOcean** — extend members; run the same assertion on real
   cross-machine droplets with a teardown guard.

## Increment 1 — the contract being added now

`CriomeDaemonConfiguration` today (signal-criome `schema/lib.schema`):

```
CriomeDaemonConfiguration {
  socket_path.DaemonPath
  store_path.DaemonPath
  (MetaSocketPath (Optional DaemonPath))
  (ClusterRoot (Optional BlsPublicKey))
  AuthorizationMode
}
```

The increment-1 additions (designed; compile-verification in flight on branch
`signal-criome-peers`):

```
PeerAddress String                       ;; a host:port address

PeerNode {                               ;; one admitted peer criome node
  master_public_key.BlsPublicKey
  address.PeerAddress
  Identity                               ;; bare type — role equals type
}

CriomeDaemonConfiguration {
  socket_path.DaemonPath
  store_path.DaemonPath
  (MetaSocketPath (Optional DaemonPath))
  (ClusterRoot (Optional BlsPublicKey))
  AuthorizationMode
  (Peers (Vec PeerNode))                 ;; NEW — positional append
}
```

Regenerated via `SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`, gated by
the `expect_fresh()` check on a plain `cargo build`. **Landed + verified** on
branch `signal-criome-peers` (`6315694`): the generated
`PeerNode { master_public_key: BlsPublicKey, address: PeerAddress, identity:
Identity }` and the `peers` config field are emitted; `expect_fresh()`,
`--features nota-text`, and 17 round-trip tests all green. The companion
non-generated `src/lib.rs` gained `CriomeDaemonConfiguration::with_peers()` /
`peers()` and `PeerNode::new()` (the schema generates the wrapper, the
hand-written builder/accessors live beside `cluster_root()` — a `new()` that
omitted the field is an `E0063`, the one friction caught and fixed). Ready for
operator to rebase onto signal-criome main.

## Lane + blocking notes

- E1 is invasive (`transport.rs`, `daemon.rs`, coordinator, signal-criome) —
  operator's hot zone — so it lands as clean per-increment designer branches;
  operator rebases. Operator is currently idle, lowering collision risk.
- Increments 1-4 are fully unblocked (criome + signal-criome). Increment 5's
  *proof* needs `CriomOS-test-cluster`, which is lock-held by cloud-operator —
  the same lock blocking the park VM-proof close. The two unblock together.
- Open questions deferred until the transport exists: in-transit encryption
  (tailnet-assumed vs slice-1), and whether peer admission flows through E2
  cluster-root admission vs static config first (`705/6` question 5).
