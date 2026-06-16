# 120 — Networking through the router: design + build plan

*Psyche directive (2026-06-16): "lets not worry about key encryption for
now. we need networking through the router." This is the concrete,
code-grounded design for giving the per-system router daemon a networked
router↔router transport — the load-bearing gap from report 119 §2. Grounded
by six parallel readers over the real code (signal-router, router,
triad-runtime, mirror, the deploy/encryption reality, message-vs-router
split) and hardened by an adversarial critique that verified every claimed
API against the source and caught two structural defects in the first draft.
Those defects are corrected here; the report records both the corrected
design and the corrections themselves.*

## 1 — The shape, in one paragraph

Lift mirror's **proven** green tailnet-TCP pattern into the router. Give
`RouterRuntime` a second ingress — a hand-wired `triad_runtime::TcpListenerDaemon`
bound to the host's tailnet address — plus a symmetric outbound peer client
(the network twin of the existing `HarnessDelivery`). The router stays one
concern: routing policy + delivery state. Transport copies mirror exactly:
one length-prefixed `LengthPrefixedCodec` frame per connection, decoded
through a **forwarding-only** contract into the single `RouterRuntime`
mailbox (preserving the single-writer invariant). The TCP ingress
structurally cannot reach the meta surface — it decodes only the working
forwarding contract, the same way mirror's `TailnetIngress` decodes only the
working `signal-mirror` contract. Encryption stays **tailnet-transparent**:
plain TCP bound to the Yggdrasil (200::/7) or WireGuard interface, no in-band
crypto, exactly as mirror does it. The one hard problem — `SO_PEERCRED` dies
at the network hop — is solved by carrying a **criome BLS attestation inside
the forwarded frame**, verified by the receiving router against the
cluster-root-admitted registry (`ermr`) before the payload is routed. The
signed frame replaces the kernel's local vouching one-for-one.

## 2 — The sound core (critique-verified)

The adversarial pass independently verified, against the source, that:

- **The transport choice is real and the API exists.** `TcpListenerDaemon::new(SocketAddr, runtime, RequestErrorLog)` (`triad-runtime/src/tcp.rs:46`), `.bind()` → `BoundTcpListenerDaemon` (`:68`), `.local_address()` (`:98`), `.serve_connections()` (`:121`), `.stop()` (`:106`); `AsyncConnectionRuntime<TcpStream>` with `handle_connection` + `AcceptedConnection`. No invented methods. Mirror's `service.rs:304-323` (`TailnetIngress`) + `shipper.rs:43` are the literal template.
- **The peer-identity model is fundamentally sound, not hand-waving.** `SO_PEERCRED` is meaningless across TCP (triad hands the ingress only `PeerIdentity::Tcp(remote_address)`, a re-homable address). Replacing kernel vouching with an in-frame criome attestation verified against the cluster-root registry is coherent and every named criome type exists: `VerifyRequest{attestation, content}`, `VerificationResult{decision, identity, expires_at}`, `Attestation`, `AuditContext{…nonce}`, `Identity[Persona Agent Host Developer Cluster]`, `KeyPurpose[CriomeRoot …]`.
- **Single-writer is preserved** and doing the criome verify **off the mailbox** (in the ingress task, before handing to the actor) is the correct stall mitigation.
- **Local-first ordering** (harness lookup before remote resolution) + **reusing `apply_stamped_message_submission`** for forwarded messages (so remote- and local-origin share one durable ledger, channel policy, and trace) is right.
- **The local Unix `SO_PEERCRED` path is untouched** — verify runs only on the new TCP ingress; the message daemon's `OriginPolicy` and the router's Unix working/meta handlers are unchanged.
- **Discipline holds:** every addition is a method/trait-impl on a data-bearing type (`RemoteRouterRegistry` actor, `RouterPeerDelivery` actor, `TailnetForwardIngress impl AsyncConnectionRuntime`); typed per-crate `thiserror`; schema-emitted nouns; no free functions, no ZST namespaces, no hand-rolled parsers. Tailnet-transparent encryption matches Spirit `wckt` (tailnet encrypts bytes, BLS authenticates identity — two separate concerns).

## 3 — Two corrections the critique forced (recorded honestly)

The first draft had two **high-severity structural defects**. Both are fixed
in §4; recording them so the next agent doesn't reintroduce them.

1. **The "parked `network-{peer}` recipient" seam was a misread.** `router.rs:556-558` (and `:1462`, `:2697`, `adjudication.rs:144`) mint `network-{peer}` as the **sender** identifier from an inbound `ConnectionClass::Network` *origin* — never as a recipient. The recipient is `submission.recipient`, a plain actor name (`router.rs:1526`). The real seam is **`router.rs:1605-1607`: any unregistered recipient parks.** So remote forwarding is triggered by **net-new reverse resolution**, not by an identifier the code already mints.
2. **The TCP-bind location was structurally impossible.** The draft bound the listener in a `RouterEngine` method "after the OnceCell inits." But `RouterEngine` (`daemon.rs:30`) is a plain struct, not an actor — no lifecycle hook — and the `runtime` `OnceCell` (`daemon.rs:65-75`) inits **lazily on the first Unix connection**. A node that only *receives* remote forwards would never init the cell and never bind its listener. Mirror works only because its `Service` **is** the kameo actor whose `on_start` binds TCP. **Fix: own the listener in `RouterRuntime::on_start` (eager bind), threading the network `Configuration` into the runtime's start args** (today it gets only `tables` via `start_with_tables`, `router.rs:824`).

Two further real issues, downgraded but folded in: replay-defense is
**router-owned** (criome's `ReplayAttempted` is its own authorization-flow
nonce tracking, *not* forward-replay detection — criome's `VerifyRequest` is
stateless w.r.t. the router's forward stream), so the seen-nonce window must
land **with** real attestation, not two milestones later; and the **re-forward
loop guard must be a first-class field**, not a risk footnote.

## 4 — The corrected design

### 4a — Contract delta (`signal-router`), milestone 1, decision-independent

All additions are self-contained nouns per the crate's stated policy; every
new request/reply/enum variant gets a `canonical.nota` witness and a
`round_trip.rs` round-trip + exhaustiveness test (house rule, not optional).

- **Addressing nouns:** `TailnetAddress { value String }` (bracketed Yggdrasil/WireGuard IPv6 literal + port), `RemoteRouterIdentity { value String }` (the peer router's stable criome `PrincipalName` — *addresses re-home, identity does not*), `HostName { value String }` (mirrors signal-message).
- **Forwarding root:** request `(ForwardMessage RouterForwardRequest)`; reply `(ForwardAccepted RouterForwardAccepted)` / `(ForwardRefused RouterForwardRefused)`. `RouterForwardRequest { stamped <local stamped-submission record>, attestation <Attestation reference>, forwarded <ForwardMarker>, nonce ReplayNonce, issued_at TimestampNanos }`. Closed `RouterForwardRefusalReason [UnknownPeer AttestationInvalid ReplayDetected ClockSkew RecipientUnknown ChannelUnauthorized AlreadyForwarded]`.
- **Loop guard (first-class):** `ForwardMarker` carries a hop discriminant; a message that arrived via forward is delivered-local-or-parked only, **never re-resolved to a remote route** — refused `AlreadyForwarded` if it would be. This guard keys on the marker the inbound handler sets deterministically, *independent of* the criome-derived origin (which is a `Host`/`Cluster` identity, so an "origin == Network" guard would not fire).
- **Peer manifest:** new `RouterBootstrapOperation` variant `RegisterRemoteRouter { identity RemoteRouterIdentity, address TailnetAddress }` (deploy-time peer table; bootstrap-as-config, not runtime discovery).
- **Endpoint extension:** `EndpointKind` gains `RemoteRouter`; for that kind `EndpointTransport.target` is a `TailnetAddress`, `auxiliary` a `RemoteRouterIdentity` — one address model, not a parallel one.
- **Config:** `RouterDaemonConfiguration` gains `tailnet_listen_address (Optional TailnetAddress)` (absent ⇒ single-host, no TCP tier), `router_identity RemoteRouterIdentity` (this router's own stable identity), `criome_socket_path (Optional WirePath)` (the local criome daemon to ask `VerifyAttestation`).
- **Trace:** `RouterDeliveryStatus` gains `ForwardedRemote` so `RouterMessageTrace` can report a message left for a peer.

### 4b — Daemon delta (`router`), milestone 2+

- **`RemoteRouterRegistry`** (new child actor): owns `RemoteRouterIdentity → TailnetAddress` (from `RegisterRemoteRouter`) and the recipient → `RemoteRouterIdentity` reverse map (source = the §5 decision). `ResolveRemoteRoute { recipient } → Option<RemoteRouterIdentity>`. Sibling to `HarnessRegistry` (whose `delivery_target` is strictly local), keeping the single-concern split.
- **The seam (corrected):** at `router.rs:1605-1607`, when the recipient is unregistered locally, ask `RemoteRouterRegistry.ResolveRemoteRoute` **before** parking. Resolvable ⇒ hand to `RouterPeerDelivery`; unresolvable ⇒ today's park-for-adjudication. Local-first preserved.
- **`RouterPeerDelivery`** (`peer_delivery.rs`, new): outbound twin of `HarnessDelivery`. `DeliverRemote { remote, stamped }` opens `TcpStream::connect(tailnet_address)` (modeled on `shipper.rs:43` + `harness_delivery.rs:50-67`), builds the `ForwardMessage` frame with the criome attestation attached, writes one length-prefixed frame, reads one `ForwardAccepted`/`ForwardRefused`, maps refusal to a delivery-attempt result. One connection = one forward.
- **`TailnetForwardIngress`** (`daemon.rs`, new): `impl AsyncConnectionRuntime<TcpStream>` (copy `service.rs:304-323` in shape). Reads one frame, decodes **only** `ForwardMessage`, **verifies the attestation off-mailbox**, then `runtime.ask(ApplyForwardedMessage{…})`, writes the reply. Holds the live `ActorRef<RouterRuntime>`.
- **Bind location (corrected):** `RouterRuntime::on_start` (`router.rs:989`) eagerly binds the `TcpListenerDaemon` when `tailnet_listen_address` is `Some`, using its own `ActorRef` for the ingress, and `tokio::spawn(listener.serve_connections())` — the real mirror pattern. Network `Configuration` is threaded into the runtime's start args. Store the `JoinHandle`, `.abort()` on stop.
- **`ApplyForwardedMessage`** (`router.rs`, new): inbound twin of `ApplySignalMessage`. Stamps the **verified** criome `Identity` as the authoritative origin (never the wire-claimed field), sets the loop-guard marker, then runs the **same** `apply_stamped_message_submission` path (`:1475-1499`) — so a forward targeting a local harness delivers locally and the channel-auth check runs identically.
- **`config.rs`:** project `tailnet_listen_address → Option<SocketAddr>` (the one std parse at config load — not NOTA), `router_identity`, `criome_socket_path → Option<PathBuf>`; dedicated accessors, **not** on `BindingSurface` (that trait is Unix-only).
- **`error.rs` (disambiguated):** `TailnetListener(#[from] AsyncListenerError)` lives on the **daemon-side** `RouterDaemonError` (`daemon.rs:36`, where IO boundaries already sit); attestation-verify domain failures map to refusal reasons on the runtime `Error` — avoiding a duplicate `#[from]`.

### 4c — Auth / peer-identity (the cross-host origin proof)

Sending router → asks its **local** criome (`Sign`/`AttestAuthorization`
over `criome_socket_path`) for an `Attestation` whose `content` digest covers
the exact stamped submission and whose `signer` is this router's
cluster-root-admitted `RemoteRouterIdentity`. The attestation rides in
`RouterForwardRequest`. Receiving router's ingress → asks its **local**
criome `VerifyAttestation(attestation, recomputed-content)`; only
`decision == Valid` proceeds, and the returned `identity` becomes the
authoritative origin. The router **never holds keys or verifies signatures
itself** — it delegates to the colocated criome daemon, keeping
*criome-signs / router-transports* clean (`wckt`). The content-digest binding
prevents replaying an envelope onto a different payload. **Replay/freshness is
router-owned:** a bounded seen-`(signer, ReplayNonce)` window rejects
duplicates (`ReplayDetected`); `issued_at` outside a skew tolerance is
`ClockSkew`. This lands **with** real attestation (milestone 3), because a
valid attestation is trivially replayable until the window exists.

## 5 — The one decision for the psyche (gates milestone 2, not milestone 1)

**How does router A know that recipient actor X lives on host B?** Milestone 1
(the wire contract) is independent of this — it ships the forwarding contract
+ peer manifest without committing to the resolution mechanism. But milestone
2 (`RemoteRouterRegistry.ResolveRemoteRoute`) needs it. Three shapes:

- **(A) `RegisterActor` gains `home (Optional RemoteRouterIdentity)`** *(recommended for the 2-node bed)* — local actors register `home = None`, known remote actors register `home = Some(peer)`. One actor model; reverse map is trivial; everything stays in `signal-router` bootstrap. Cost: each router's bootstrap must enumerate the remote actors it may address (table replication — fine at two nodes).
- **(B) `RegisterRemoteRouter` enumerates the actors behind that peer** — groups remote actors under their peer (one op per peer). Same replication, with peer/actor enumeration coupled.
- **(C) Address-carries-host** — a recipient is `(ActorIdentifier, Optional HostName)`; `RemoteRouterRegistry` maps `HostName → RemoteRouterIdentity → TailnetAddress`, so **no per-actor replication**. This is the likely long-term shape and aligns with signal-message's existing `HostName` / `OtherPersonaEngine{host}` modeling — but it touches the **signal-message** contract (a cross-repo change), so it's heavier now.

Recommendation: build milestone 1 now (decision-free); take **(A)** for the
first working e2e; treat **(C)** as the planned successor once cross-host
addressing proves out. Flag if you'd rather go straight to (C).

## 6 — Milestones

1. **Contract** *(building now)* — the §4a `signal-router` additions; regenerate via schema-rust-next; `canonical.nota` + `round_trip.rs` witnesses. Buildable in isolation: `nix flake check` on `signal-router`, no daemon, no network.
2. **Offline two-router loopback forward** — `TailnetForwardIngress` + `RouterPeerDelivery` + `RemoteRouterRegistry` + `ApplyForwardedMessage` + config projection + the corrected `on_start` eager bind. Attestation verify behind a trait with an accept-fixed-test-identity offline impl. Acceptance: `router/tests/end_to_end_remote_forward.rs` (modeled on `mirror/tests/end_to_end_arc.rs`) — two in-process `RouterRuntime`s on OS-assigned ports (`local_address`), submit on A for an actor registered only on B, assert A's trace = `ForwardedRemote`, B delivers to its local harness, reply = `ForwardAccepted`. **Fully offline, no tailnet, no criome daemon.**
3. **Real criome attestation + replay window** — swap the offline verifier for a criome client over a temp Unix socket with test cluster-root keys; add the seen-nonce + freshness window. Acceptance: admitted-identity forward routes; unadmitted is `AttestationInvalid`; wrong-digest refused; a replayed frame is `ReplayDetected`; window survives a simulated restart (a sixth `router.sema` table family).
4. **Live ouranos↔prometheus tailnet forward** — two router daemons bound to each node's Yggdrasil address, cross-pointing `RegisterRemoteRouter` manifests, real criome daemons with cluster-root-admitted router identities. Acceptance on the live bed: a submit on ouranos for a prometheus-local actor delivers over Yggdrasil (~16ms); meta-over-TCP structurally rejected; plain-TCP-on-tailnet confirmed.

## 7 — Risks (carried)

- **Single-writer back-pressure:** `TcpListenerDaemon` defaults to `RequestConcurrencyLimit::one()` (`tcp.rs:53`); forwards serialize through one mailbox. Mitigated by verifying off-mailbox; may need `with_concurrency_limit` tuning.
- **criome on the hot path:** every inbound cross-host message blocks on a local criome `VerifyAttestation`. Local-only routing must stay unaffected (verify runs only on the TCP ingress).
- **Address re-homing:** routes keyed by identity, dialed by a static manifest address; a re-homed peer needs re-bootstrap (no live discovery yet — acceptable at two nodes).
- **In-flight durability:** a down peer ⇒ forward fails to park-for-adjudication; verify the pending sema entry survives restart and re-resolves remote.
- **Clock skew:** freshness rejection needs loosely-synced clocks; window must bound the replay table without false rejects.
- **Cross-component dep:** milestones 3-4 need real BLS landed on criome (the `criome-auth-pilot` branch) + a cluster-root with admitted router identities deployed on the two nodes (report 226).

## 8 — Build status

Milestone 1 (the `signal-router` forwarding contract) is being built now on a
designer feature branch. Milestone 2 needs the §5 decision. The investigation
that grounded this (6 readers + design + adversarial critique) ran as workflow
`router-network-transport-design`; the full maps/plan/critique are in its
transcript.
