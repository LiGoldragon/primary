# E1 readiness — cross-criome peer transport

Sub-report 3 of the 705 criome-cluster reassessment. Read-only pass over
the four repo `origin/main`s. E1 is the load-bearing gap for the
multi-machine quorum (701 roadmap): without a TCP peer lane, criome-A
cannot solicit a signature from criome-B/C on another host, so `Quorum`
mode can never aggregate `k`-of-`n` across machines. This report defines
exactly what must be built, names the hard decisions, and pins the
smallest correct first slice that proves the lane end to end.

## What exists today (the substrate E1 builds on)

The pieces E1 needs to wire together already exist in working form; what
is missing is the wire *between hosts* and the coordinator logic that
drives it.

- **Frame codecs are stream-generic, not Unix-bound.** `CriomeFrameCodec`
  reads/writes over `&mut impl Read` / `&mut impl Write` with a 4-byte
  big-endian length prefix (`transport.rs:103-124`), and the frame
  type itself is `signal_frame::StreamingFrame<Input, Output, CriomeEvent>`
  (`signal-criome/src/lib.rs:17-18`) with `encode_length_prefixed` /
  `decode_length_prefixed` (`signal-frame/src/frame.rs:245,302`). The
  codec is reusable verbatim over a TCP stream — only `CriomeClient` /
  `CriomeMetaClient` hard-bind `UnixStream` (`transport.rs:222-262`).
- **BLS sign/verify primitives are ready for a per-frame envelope.**
  `MasterKey::sign(&[u8]) -> BlsSignature` (`master_key.rs`) and the
  `VerifyBls` trait on `BlsPublicKey` (`fn verify_bls(&self, sig, msg)
  -> bool`) are exactly the two operations a sign-then-send /
  verify-before-parse envelope needs. Both go through one domain-tag
  (`ATTESTATION_DST`); the peer envelope must use a *distinct* DST (see
  Decision E).
- **The peer signal verbs already exist on the working contract.**
  `CriomeRequest::RouteSignatureRequest(SignatureSolicitationRoute)` and
  `CriomeRequest::SubmitSignature(SignatureSubmission)` are live
  (`signal-criome/src/schema/lib.rs:1259-1260`), already routed by
  `CriomeRoot::submit` to the `AuthorizationCoordinator`
  (`root.rs` RouteSignatureRequest / SubmitSignature arms), and the
  coordinator persists both to the store
  (`authorization.rs:178-200`, `store_signature_solicitation` /
  `store_signature_submission`). The actor-side plumbing for "B receives a
  solicitation" and "A receives a submission" is already built and tested
  in-process. E1 is the *transport* that carries those two messages
  between hosts, plus the coordinator logic that emits the solicitation
  and tallies the submissions.
- **The 1-of-1 witness-test pattern is the proof harness to extend.**
  `src/bin/criome-cluster-witness-test.rs` already mints real BLS keys,
  seeds a real daemon over its socket, and asserts AUTHORIZED vs
  threshold-short REJECTED against a deployed `criome-daemon`. The E1
  proof is the 2-of-2 / 2-of-3 analogue across two daemons.

## What is missing (the E1 gap, precisely)

1. **No TCP anywhere.** `git grep` for `TcpStream|TcpListener|tokio::net::Tcp|PeerClient`
   over `criome/src` at `origin/main` returns nothing. `transport.rs` is
   `UnixStream`-only; `daemon.rs` binds two `UnixListener`s. The belief
   in the brief is confirmed.
2. **No per-frame BLS envelope.** Today a frame is `len ++ rkyv(frame)`.
   There is no sender-signature wrapper and no verify-before-parse step.
   The ARCHITECTURE candidate that matches the brief is row 2 of the
   §6.1 table (`ARCHITECTURE.md:439`): "Each cross-host frame is
   BLS-signed by sender's master key; receiver verifies before parsing."
   That choice is still listed as an *open design slot*
   (`ARCHITECTURE.md:432-444`, `:550-551`) — E1 is where it gets decided.
3. **No peer addressing in config.** `CriomeDaemonConfiguration`
   (`signal-criome/src/schema/lib.rs:395-401`) carries `socket_path`,
   `store_path`, `meta_socket_path`, `cluster_root`, `authorization_mode`
   — and *no peer table*. ARCHITECTURE §6.1 describes a peer-routing
   table mapping master pubkey → `(host, unix-user)` predictable socket
   name (`ARCHITECTURE.md:414-430`), but that is single-host only; there
   is no `host:port` for cross-machine peers. The config struct must gain
   a peer-node list (host:port + master pubkey per node).
4. **No outbound solicitation, no quorum tally.** `AuthorizationCoordinator`
   *stores* solicitations and submissions but never *initiates* a
   solicitation to a peer and never *aggregates* submissions against a
   threshold. `missing_authorities` is tracked on the state record
   (`authorization.rs:123,208`) but nothing decrements it on a verified
   submission or flips the state to Granted at `k`. ARCHITECTURE confirms
   "quorum aggregation [is one of] the next authorization milestones"
   (`ARCHITECTURE.md` status section). This is the coordinator-logic half
   of E1, distinct from the transport half.

## The four hard design decisions (from the brief)

### (a) Framing/codec reuse vs a new peer codec — REUSE, wrap, don't replace

Reuse `CriomeFrameCodec` verbatim for the inner payload; do **not** fork
the codec. The peer lane carries the *same* `CriomeRequest`/`CriomeReply`
signal frames (it must — `RouteSignatureRequest` and `SubmitSignature`
are working-contract verbs), so the inner bytes are identical to the Unix
lane. The new construct is an **outer BLS envelope** wrapping the existing
length-prefixed frame:

```text
peer frame  =  len32 ++ rkyv(PeerEnvelope {
                 sender_public_key: BlsPublicKey,
                 signature:         BlsSignature,   // over the inner frame bytes + DST
                 inner_frame:       Vec<u8>,        // the existing len-prefixed CriomeFrame
               })
```

`PeerEnvelope` is a new schema type (it crosses a wire, so it belongs in
`signal-criome`, not in the daemon crate). Receiver flow: read the outer
length-prefixed bytes → `verify_before_parse`: check `sender_public_key`
is an admitted peer AND `verify_bls(signature, inner_frame_bytes)` holds
→ only then `decode_length_prefixed` the inner frame. A signature failure
returns a typed error and the bytes are never handed to rkyv. This
realizes "verify before parsing" literally. A fresh codec would duplicate
the length-framing and the `Input/Output` typing for no gain.

### (b) Sync `UnixListener` + `block_on` vs async — keep sync inbound, add a SEPARATE blocking peer thread; do NOT rewrite the serve loop yet

The current `serve_forever` is a single-threaded busy-poll: set both
listeners non-blocking, `accept()` each, `block_on` the actor ask, sleep
10ms when idle (`daemon.rs` `serve_forever` / `try_serve_working_connection`).
This model **does not scale to outbound peer calls** in its current shape,
because A soliciting B is a *blocking outbound TCP round-trip executed
from inside an actor handler*, and the AGENTS hard rule forbids blocking
in actor message handlers. Two real constraints collide:

- The coordinator must not `block_on` a TCP round-trip inside `handle`.
- The single serve thread must stay responsive to local clients while a
  peer call is in flight.

Smallest-correct answer for the first slice: **do not go fully async.**
Add the peer listener as a *third* listener in the same non-blocking
busy-poll (`try_serve_peer_connection` alongside working/meta), so
*inbound* peer solicitations (B receiving A's RouteSignatureRequest) cost
nothing new architecturally — they are just another frame the existing
loop serves. For *outbound* solicitation (A → B/C), the coordinator must
not block: model it as **fire-and-collect**, not request-reply. A emits
`RouteSignatureRequest` to each peer over a short-lived TCP connection
from a dedicated peer-dispatch path (a `CriomePeerClient` that owns the
TCP `connect`+`write`), and B later *connects back* to A's peer listener
with `SubmitSignature` as an independent inbound frame. This matches the
brief's flow ("B+C sign, A aggregates") and the ARCHITECTURE integration
row ("Peer criome daemons … reply with `SubmitSignature`",
`ARCHITECTURE.md:460`) — submission is a *new inbound exchange*, not the
reply leg of the solicitation. That keeps every actor handler
non-blocking and avoids a tokio reactor rewrite in slice 1. A full async
serve loop (replace busy-poll with `tokio::select!` over async listeners)
is the right *eventual* shape and should be its own follow-up slice once
the peer lane's semantics are proven; doing it inside slice 1 couples two
risky changes.

The one unavoidable blocking call in slice 1 is A's *outbound connect* to
each peer. Run it off the actor thread: the coordinator, on parking a
quorum request, hands the solicitation set to a peer-dispatch component
that owns its own thread (or a `spawn_blocking` on the existing runtime),
never blocking inside `handle`.

### (c) Where peer config lives — a new `peers` field in `CriomeDaemonConfiguration`

Add a `PeerNodes(Vec<PeerNode>)` field to `CriomeDaemonConfiguration`
(`signal-criome/src/schema/lib.rs:395-401`), where each `PeerNode` carries
the peer's master `BlsPublicKey`, its `host:port`, and its `Identity`
(the `Identity::Cluster`/`Host` the peer signs as, needed to match
`required_signer` in a `SignatureSolicitation` and to credit the
submission in the tally). This is daemon configuration delivered as a
binary meta-signal (the hard rule: daemons take one rkyv startup arg and
accept config via authenticated binary `Configure`; `root.rs::configure`
already re-reads `cluster_root` and `authorization_mode` from a pushed
`CriomeDaemonConfiguration`, so `configure` extends naturally to absorb
`peers`). The bootstrap encoder `criome-write-configuration` and the
NixOS service module gain the peer list as deploy input. Naming: full
words, no ancestry — `PeerNode { master_public_key, address, identity }`,
field `peers` on the config. `address` is a `host:port` string typed as a
domain newtype (`PeerAddress(String)`), not a bare `String`, and not
`SocketAddr` (hostnames over the tailnet must resolve at connect time).

ARCHITECTURE's §6.1 predictable-socket scheme stays for *single-host*
cross-user peers; the new `peers` field is the cross-host superset. Do
not try to derive cross-host address from the pubkey hash — there is no
host in that hash.

### (d) How the requester / A-solicits / B+C-sign / A-aggregates flow maps onto existing actor messages

The actor messages already exist; E1 adds the transport edges and the
tally. Mapping (per p43g: the requester submits a content-addressed
object under SO_PEERCRED with no request-signing key; criome nodes sign
with their master keys):

| Step | Who | Existing message / new work |
|---|---|---|
| 1. Requester submits object to criome-A | client → A working socket | `EvaluateAuthorization(AuthorizationEvaluation)` in `Quorum` mode → `root.rs::evaluate_authorization` (exists) |
| 2. A determines `n` peers + `k` threshold, parks a slot, records `missing_authorities` | A coordinator | `CreateAuthorizationState` + threshold from the admitted `Contract`/`Threshold` rule (`schema/lib.rs` Rule::Threshold). **NEW: emit one `SignatureSolicitationRoute` per peer.** |
| 3. A solicits B and C | A → B/C peer TCP | **NEW** `CriomePeerClient.send_envelope(peer, RouteSignatureRequest(route))`; B/C inbound serve maps it to `AuthorizationCoordinator::route_signature_request` (exists, `authorization.rs:166-176`) |
| 4. B and C sign A's exact `request_digest` with their master keys | B/C signer | B/C build a `StampedSignatureEnvelope` via `MasterKey::sign` over the solicitation's digest preimage (signer logic mirrors `signer.rs::sign`; **NEW: a "sign a peer solicitation" path** distinct from attestation signing) |
| 5. B and C submit the signature back to A | B/C → A peer TCP | **NEW** `CriomePeerClient.send_envelope(A, SubmitSignature(submission))`; A inbound serve maps it to `AuthorizationCoordinator::submit_signature` (exists, `authorization.rs:178-188`) — currently it only *stores*; **NEW: verify the submitted BLS sig and decrement `missing_authorities`** |
| 6. A aggregates `k`-of-`n`, flips state to Granted, publishes | A coordinator | **NEW: tally logic** — when `missing_authorities` is satisfied at `k`, mint the `AuthorizationGrant` and `publish_authorized_object_update` (the publish path exists in `root.rs`) |
| 7. Requester observes the grant | client → A | `ObserveAuthorization` (exists) → grant; `VerifyAuthorization` checks digest match (exists, `authorization.rs:152-164`) |

So the *new* code is exactly: the envelope type + codec wrapper (a), the
`CriomePeerClient` + peer listener (a/b), the `peers` config field (c),
the **outbound solicitation emission** (step 2/3), the **peer-solicitation
signing path** (step 4), and the **submission-verify + threshold tally**
(step 5/6). Everything else is wiring to messages that already route.

## The smallest correct first slice (PR-sized, proves the lane end to end)

Goal: a 2-of-2 quorum across **two real `criome-daemon` processes** where
A solicits B over TCP, B signs and submits over TCP, A aggregates and
grants — proven by a witness binary the way 1-of-1 is proven today.

Slice contents, in dependency order:

1. **`signal-criome`: `PeerEnvelope` + `PeerNode`/`PeerNodes` + `PeerAddress`.**
   Schema types only (rkyv + nota-text derive, positional records). Add
   `peers: PeerNodes` to `CriomeDaemonConfiguration` with accessor +
   builder mirroring `with_cluster_root`/`cluster_root`
   (`src/lib.rs:172-178`). No behavior.
2. **`criome` transport: `CriomePeerCodec` (envelope wrap over `CriomeFrameCodec`) + `CriomePeerClient` (TCP connect, sign-then-send) + verify-before-parse read.**
   `CriomePeerClient::send_envelope` connects `TcpStream`, wraps the inner
   frame, signs with the local `MasterKey`, writes len-prefixed envelope.
   The inbound read verifies `sender_public_key ∈ peers` and `verify_bls`
   before `decode_length_prefixed`. New `Error` variants:
   `PeerSignatureRejected`, `UnknownPeer`, `PeerConnect`.
3. **`criome` daemon: bind a third `peer_listener` (TCP) and serve it in the busy-poll** (`try_serve_peer_connection` beside working/meta in `serve_forever`). Inbound peer frames route through `CriomeRoot::submit` exactly like Unix frames — verify happens in the codec layer before the frame reaches the actor.
4. **`criome` coordinator: outbound solicitation + tally.** On a `Quorum`
   park with a `Threshold` contract, emit a `RouteSignatureRequest`
   envelope to each `PeerNode` whose `identity` is a required signer
   (off-actor-thread dispatch per Decision (b)). On `SubmitSignature`,
   verify the submitted `StampedSignatureEnvelope` against that peer's
   configured `master_public_key`, decrement `missing_authorities`, and at
   `k` mint the grant + publish.
5. **`criome` peer-solicitation signing path.** B, on receiving a
   `RouteSignatureRequest`, signs the exact `request_digest` with its
   `MasterKey` and submits — a new signer method distinct from attestation
   signing, under a peer-quorum DST.
6. **Proof harness: `criome-cluster-2of2-witness-test`** (new bin under the
   `cluster-witness` feature, sibling to the 1-of-1 witness). And a
   **two-node NixOS test** (`pkgs.testers.runNixOSTest`) with nodes A and
   B on a shared test network, each running a real `criome-daemon`
   configured with the *other* as a peer (host:port + pubkey); the test
   submits to A, asserts A reaches Granted only after B's TCP submission.
   This is the first actual cross-machine networking proof and the direct
   answer to the psyche's "actually networked sandboxes" goal.

Scope discipline for slice 1: **2-of-2 with both peers reachable and
honest.** Defer to follow-ups — timeout/retry on an unreachable peer,
`k`-of-`n` with `n>k` partial collection, the full async serve-loop
rewrite, ECDH meta-session secrecy (the envelope gives *authenticity*,
not *confidentiality*; that is a separate ARCHITECTURE slot,
`ARCHITECTURE.md:659`), and the single-host predictable-socket peer path.
Slice 1 proves the load-bearing edge: a BLS-authenticated frame crosses a
real network between two real daemons and drives a real quorum grant.

## Key crypto / correctness notes for whoever builds this

- **Distinct DST.** The peer envelope signature and the peer-solicitation
  signature must each use a domain-separation tag *different* from
  `ATTESTATION_DST` (`master_key.rs`). Reusing the attestation DST would
  let a frame signature replay as an attestation or vice versa — the exact
  cross-purpose forgery the ARCHITECTURE domain-separation constraint
  forbids (`ARCHITECTURE.md` "Signed payloads carry domain separation").
- **Verify against configured pubkey, not submitted pubkey.** Step 5's
  tally must verify B's submission against the `master_public_key` from
  the `peers` config for B's identity — never trust a pubkey carried in
  the submission. The envelope's `sender_public_key` must equal the
  configured peer pubkey for the connection's claimed identity.
- **The grant binds the exact digest.** `VerifyAuthorization` already
  rejects a grant whose digest ≠ request digest (`authorization.rs:152-164`);
  the tally must mint the grant over A's `request_digest`, and each peer
  signs *that same* digest, so aggregate verification is well-defined.
- **Tally is a coordinator concern, persisted.** `missing_authorities`
  lives on the durable `AuthorizationStateRecord`
  (`store.rs:47`, `lib.rs:383-417`), so a peer submission arriving after
  an A restart still aggregates against persisted state. Build the tally
  as a read-modify-write of that record, not in-memory counters.

## Severity-tagged findings (see structured summary)

- E1 transport is genuinely unbuilt (HIGH — load-bearing for all
  multi-machine quorum).
- The peer signal verbs and actor plumbing already exist (INFO — the gap
  is narrower than "build peer messaging from scratch"; it is transport +
  tally).
- The sync busy-poll serve loop forces an architectural choice now (MEDIUM
  — solvable without a full async rewrite via fire-and-collect, but the
  wrong choice here couples two risky changes).
- Quorum aggregation/tally is missing even on the single-host path (MEDIUM
  — `RouteSignatureRequest`/`SubmitSignature` store but never tally).
- Config has no peer table (MEDIUM — blocks addressing; clean to add).
