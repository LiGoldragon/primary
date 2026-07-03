# Router Transport Readiness — Scout Map

Scope: can the `router` component act as the single network-facing carrier
("the voice") that carries message bodies host-to-host and delivers them to the
right local component today? Read-only inspection of the checked-out repo at
`/git/github.com/LiGoldragon/router` (Persona family, `main`, package version
`0.4.1`, Rust edition 2024). Ground truth is the code; earlier lane notes were
treated as leads to confirm or refute.

## Verdict

PARTIAL — strongly built, one clear origination seam missing. The router
already IS a network-facing carrier: a standing `router-daemon` binds a TCP
tailnet ingress, and a real end-to-end run (real BLS auth, real loopback TCP,
real peer mirror) proves an actual Spirit record BODY crosses host-to-host and
durably lands in the right local component. What is NOT wired is the standing
daemon ORIGINATING a component-object forward on its own: a locally submitted
message forwards only a plain body string, so shipping a Spirit change / Criome
signature outbound today needs a dedicated sender bin, and the retry backlog is
in-memory (not crash-durable).

## Observations (direct, with paths)

### 1. What the router is today — daemon + thin clients (observed fact)

- `Cargo.toml` declares multiple binaries: `router-daemon` (`src/main.rs`, the
  long-lived runtime, no feature gate), plus thin CLIs `router` and
  `meta-router` (feature `nota-text`), config-writer bins, and
  `router-forward-witness` (feature `witness`).
- `src/main.rs` is `RouterProcessDaemon::run_to_exit_code()` — a standing
  supervised process. `README.md` and `AGENTS.md` describe it as "the
  long-lived router runtime". So the router is primarily a **running daemon**,
  with thin one-argument CLIs beside it (a mix, daemon-centric).
- `src/daemon.rs` `RouterEngine`/`RouterProcessDaemon` binds a Unix WORKING
  socket (`router.sock`) and a META socket, decoding only `signal-message`
  ingress and `signal-router` observation on the working tier and
  `meta-signal-router` policy on the meta tier.
- Actor runtime is Kameo. `RouterRuntime` is the root actor; children include
  `RouterRoot`, `HarnessRegistry`, `RemoteRouterRegistry`, `RouterPeerDelivery`,
  `HarnessDelivery`, `AuthorizedObjectFanout`, channels, adjudication.

### 2. Crossing machines — a real network-facing TCP ingress exists (observed fact)

- `src/router.rs` `RouterRuntime::bind_tailnet_ingress` (~line 1156): when
  `network.listen_address()` is `Some`, it binds a `TcpListenerDaemon` serving
  `TailnetForwardIngress` and stores the bound address. `None` ⇒ single-host, no
  TCP tier. It binds eagerly in `on_start` "the mirror pattern … the runtime IS
  the actor, so a receive-only node still binds."
- `src/router.rs` `TailnetForwardIngress` (~line 351): the network twin of the
  Unix working tier. It decodes ONLY `signal-router::Input::ForwardMessage` —
  "a TCP peer structurally cannot reach the policy surface." Anything else is
  refused. It verifies the attestation OFF the mailbox, then asks the runtime to
  apply the forward, and writes one `ForwardAccepted`/`ForwardRefused` reply.
- `src/peer_delivery.rs` `RouterPeerDelivery` is the outbound twin: one
  `DeliverRemote` opens one `TcpStream::connect(peer_address)`, writes ONE
  length-prefixed `ForwardMessage` frame, reads ONE reply. "One connection = one
  forward."
- `src/remote_router.rs` `RemoteRouterRegistry` is the cross-host routing table:
  `RemoteRouterIdentity -> TailnetAddress` (peers) and recipient
  `ActorIdentifier -> RemoteRouterIdentity` (homes), populated from a deploy-time
  bootstrap. `ResolveRemoteRoute` walks recipient → home → address.
- So the router carries messages host-to-host over TCP today, gated on a
  configured `tailnet_listen_address`. The config field is real:
  `src/config.rs` `Configuration::tailnet_listen_address` (projected from a NOTA
  `TailnetAddress` at load).

Note (observed fact): the manifest line "router.sock … internal traffic only;
external ingress via `message-daemon`" refers to the Unix WORKING socket and
LOCAL user-message ingress. The TCP tailnet ingress is a SEPARATE tier for
router↔router peer forwarding — it is not the message-daemon path.

### 3. Bodies vs references — the cross-host path carries real bodies (observed fact)

- The wire payload `signal_router::ForwardedMessagePayload` carries
  `source_actor`, `destination_actor`, `body` (the actual message body string),
  `attachments`, and `routed_objects` — a `Vec<RoutedContractObject>`. Each
  `RoutedContractObject` carries `contract_name`, `contract_operation`,
  `contract_payload_size`, and `payload_octets` (the actual bytes).
- `src/router.rs` `apply_forwarded` (~line 2353): on inbound, it reconstructs the
  message body from `payload.body` and carries `payload.routed_objects()` into
  the pending message. Bodies AND arbitrary component-object octets cross.
- `tests/criome_forward_lands_in_mirror.rs` is the decisive witness. Its second
  test forwards the REAL content-addressed record body — the rkyv-serialized
  `sema_engine::VersionedCommitLogEntry` that the production `ComponentShipper`
  ships, "the same content-addressing Spirit uses for its versioned log" — over
  real loopback TCP, and asserts the LANDED body re-hashes to Spirit's real head
  (`ObserveHead` value). This directly REFUTES "references, not bodies" for the
  cross-host path.
- The "references, not bodies" claim is TRUE only of a DIFFERENT, LOCAL
  mechanism: `src/authorized_object.rs` `AuthorizedObjectFanout` is a local
  subscribe/publish of `AuthorizedObjectReference` (component kind + digest +
  object kind) — a typed pointer, not a body, and not itself network-crossing.
  The earlier lane note conflated this local fanout with the peer-forward path.

### 4. Arrival routing — dispatch to the right local component IS built (observed fact)

- `src/harness_delivery.rs` `HarnessDelivery::deliver` dispatches by
  `EndpointKind`: `HarnessSocket` → a `signal-harness` `MessageDelivery` (a
  harness prompt), `PtySocket` → a terminal, `ComponentSocket` →
  `deliver_to_component_socket`, `Human` → no-op.
- `deliver_to_component_socket` (~line 130) opens a Unix socket to the local
  component and writes each routed object's raw octets as a length-prefixed
  frame (payload-blind — the router never decodes the component contract).
- Destination identification: the recipient `ActorIdentifier` resolves via
  `HarnessRegistry` (`ReadHarnessDeliveryTarget`) to an `Actor` with an
  `EndpointTransport { kind, target }`. "The right local component" = whichever
  endpoint is registered under that recipient id, from the deploy-time bootstrap
  (`RegisterActor` + `GrantChannel`). Proven for a real mirror in
  `tests/criome_forward_lands_in_mirror.rs` (mirror homed as `ComponentSocket`)
  and for a harness in `tests/end_to_end_remote_forward.rs`.

### 5. Delivery guarantees — retry/park exist; backlog is in-memory (observed fact)

- `src/router.rs` `retry_pending` (~line 2149) is the delivery loop over
  `self.pending: Vec<PendingRouterMessage>`. Local-first: it looks up the local
  harness target; on a miss for an `Origin` message it consults the remote-route
  table and forwards over TCP. Peer accept ⇒ dropped as delivered; peer refuse
  ⇒ parked (re-queued); transport error ⇒ restored (re-queued). So a peer being
  temporarily down does NOT drop the message — it is retried.
- Retries are event-driven (no polling, per `AGENTS.md`): `retry_pending` is
  called after a submission (~2056), after an inbound forward (~2385), and
  inside system/harness event handlers (~1733, ~1804).
- Durability: `self.pending` is initialized `Vec::new()` (~line 1701) and I found
  NO rehydrate-on-startup path. `src/tables.rs` registers only an
  `adjudication_pending` table — there is no pending-delivery-queue table. The
  parked retry backlog therefore lives in memory only.
- Replay/freshness admission IS built: `src/forward_attestation.rs`
  `ForwardAdmissionWindow` rejects replayed `(signer, nonce)` and clock skew
  (default 300s window, 4096 capacity), with unit tests. Exercised end-to-end in
  `tests/end_to_end_remote_forward.rs` (same-nonce second forward ⇒
  `ReplayDetected`).

### 6. Generality — one carrier, arbitrary component objects (observed fact)

- The forward contract is generic: `RoutedContractObject` names a `contract_name`
  + `contract_operation` + opaque `payload_octets`. The router relays octets
  payload-blind. `tests/end_to_end_remote_forward.rs` states it "can carry an
  opaque component-owned object to a component socket … the router treats both
  bodies as opaque bytes."
- The same carrier demonstrably moves a `signal-mirror` `Append`/`NotifyObject`
  AND (by the same octet-relay mechanism) any component contract. Criome
  signatures ride the SAME frame as the attestation
  (`RouterPeerAttestation`) and could equally ride as a routed object. So the
  "one carrier, different letters" property holds at the wire and receive level.

### 7. Attestation seam — real criome BLS is implemented (observed fact)

- `SO_PEERCRED` dies at the TCP hop; it is replaced by a criome BLS attestation
  riding inside the forwarded frame (`src/forward_attestation.rs` header).
- Two verifier impls behind the `ForwardAttestationVerifier` trait:
  `AcceptFixedTestIdentity` (offline milestone-2 stand-in, FNV digest, one fixed
  identity, no daemon) and `src/criome_attestation.rs` `CriomeForwardAttestation`
  (milestone-3 production: derives a blake3 digest over the full payload +
  origin, asks a co-resident criome daemon to BLS-`Sign`, and on receive asks
  criome to `VerifyAttestation`). `src/daemon.rs` selects the real verifier when
  `criome_socket_path` is configured, else the offline stand-in.
- `tests/criome_forward_lands_in_mirror.rs` runs the real path with a real
  `criome::daemon::CriomeDaemon` (real `blst`) on both sign and verify. Fail-
  closed: an unavailable criome yields an empty-signature attestation the
  receiver refuses.

## Interpretations (inferences, kept separate)

- The router is genuinely designed AS the single network-facing carrier the
  brief describes: the TCP tailnet ingress accepts only `ForwardMessage` (no
  policy/observation surface reachable from the network), local components reach
  peers only by handing a message to their own router, and delivery on arrival
  goes to a locally-registered endpoint. The architecture matches the intended
  "voice" role rather than being a different thing repurposed.
- The "cross-host transport between Criomes" open slot noted in the Criome
  inspection is, in the router's own architecture, meant to be filled BY the
  router: `ARCHITECTURE.md` frames the spirit-vcs milestone (Spirit `d6he`) as
  "criome auth-only, Router transport-only, mirror the version-control
  substrate." The router is the intended transport for BOTH Spirit changes and
  Criome signatures, so this is not a competing transport — it is the same one.
- The transport is real but its AUTOMATIC origination is the immature edge. The
  receive+verify+land path is production-grade and witnessed; the standing
  daemon's ability to, on its own, wrap a local Spirit change or Criome
  signature as a routed object and push it to a peer is the piece still done by
  hand (the witness bin).
- In-memory-only backlog is adequate for a live demo but is a convergence risk:
  a node that parks a remote forward (peer down) and then restarts loses that
  parked item, since only committed message records and adjudication survive, not
  the retry queue.

## The gap (for the "single network-facing carrier" role)

Built and production-shaped (with a witnessed real run):
- Network-facing transport: standing `router-daemon` TCP tailnet ingress
  (`TailnetForwardIngress`) + outbound `RouterPeerDelivery`; peer/home routing
  table (`RemoteRouterRegistry`).
- Body-carrying: real message body and real content-addressed Spirit record
  body cross host-to-host and land durably (mirror head advances, re-hashes to
  Spirit's head).
- Arrival routing to the right local component: `EndpointKind::ComponentSocket`
  payload-blind octet relay to a locally-registered component socket, keyed by
  recipient `ActorIdentifier`.
- Auth across the hop: real criome BLS sign/verify (`CriomeForwardAttestation`),
  replay + clock-skew admission window, fail-closed on missing signature.
- Generality: opaque `RoutedContractObject` carrier — one carrier for any
  component contract's octets.

Stubbed / conceptual / configuration-gated:
- Offline verifier (`AcceptFixedTestIdentity`) remains the default when no
  `criome_socket_path` is configured — a single-host/pre-criome deployment runs
  without auth. Real auth requires the criome socket wired in the daemon config.
- The TCP tier only exists when `tailnet_listen_address` is configured; a router
  with no listen address is single-host only. Whether production node configs
  actually set these two fields today was not verified (see Unknowns).

Entirely missing / net-new for the intended role:
- OUTBOUND origination of component-object forwards from the STANDING daemon.
  `src/peer_delivery.rs` `payload_for` builds `routed_objects = Vec::new()`, and
  origin submissions push `PendingRouterMessage::new` with empty routed objects
  (`src/router.rs` ~2451); `forward_to_remote` passes only the `Message`, not
  `pending.routed_objects`. `src/bin/router_forward_witness.rs` states this
  outright: "No router daemon ingress accepts a `RoutedContractObject` for an
  OUTBOUND forward … the routed-object forward can only be constructed directly."
  To ship (a) a Spirit change body or (b) Criome signatures automatically, the
  daemon needs: an origin-side way for a local component to hand the router a
  routed object (a submission surface carrying `RoutedContractObject`), and the
  retry loop to thread `pending.routed_objects` into `DeliverRemote` /
  `payload_for`. Today that origination is the standalone `router-forward-witness`
  bin (env-driven, one-shot), not the standing daemon path.
- Crash-durable delivery backlog. The parked/pending retry queue is an in-memory
  `Vec`; there is no pending table and no rehydrate. Needed for convergence if a
  node restarts while a peer is unreachable.
- No dedicated peer-down redial/backoff scheduler. Retry is triggered by other
  pushed events; a parked remote forward waits for the next unrelated event
  rather than a peer-reconnect signal (no-polling constraint makes this a
  design item, not a quick fix).
- Reverse/dynamic route resolution. `ARCHITECTURE.md` (~line 513) flags
  reverse resolution as "net-new"; homes today come from the deploy-time
  bootstrap, so a recipient with no pre-registered home cannot be resolved to a
  peer at runtime.

Net: to carry a Spirit change body and Criome signatures across to a peer and
deliver them locally, the RECEIVE + VERIFY + LAND half is built and proven; the
SEND half from an unmodified standing daemon is the primary net-new work, plus
backlog durability for convergence.

## Code locations (pickup map)

Repo root: `/git/github.com/LiGoldragon/router`
- `src/main.rs` — `router-daemon` entry (`RouterProcessDaemon`).
- `src/daemon.rs` — `RouterEngine`/`RouterProcessDaemon`; verifier selection
  from `criome_socket_path`; Unix working + meta connection handling.
- `src/config.rs` — `Configuration`: `tailnet_listen_address`,
  `criome_socket_path`, `router_identity`.
- `src/router.rs` — `RouterRuntime`, `RouterRoot`; `bind_tailnet_ingress`,
  `TailnetForwardIngress`, `retry_pending`, `forward_to_remote`,
  `resolve_remote_route`, `apply_forwarded`, `PendingRouterMessage`.
- `src/peer_delivery.rs` — `RouterPeerDelivery` outbound TCP forward; **`payload_for`
  is where routed objects are dropped (empty) — the outbound gap.**
- `src/remote_router.rs` — `RemoteRouterRegistry` peer/home routing table.
- `src/forward_attestation.rs` — `ForwardAttestationVerifier` trait,
  `AcceptFixedTestIdentity` (offline), `ForwardAdmissionWindow` (replay/skew).
- `src/criome_attestation.rs` — `CriomeForwardAttestation` (real criome BLS).
- `src/harness_delivery.rs` — `HarnessDelivery`; `EndpointKind` dispatch;
  `deliver_to_component_socket` (local-component octet relay).
- `src/authorized_object.rs` — `AuthorizedObjectFanout` (LOCAL references-only
  pub/sub; the true source of the "references not bodies" claim).
- `src/tables.rs` — durable tables (only `adjudication_pending`; no pending
  queue).
- `src/bin/router_forward_witness.rs` — deployable one-shot outbound
  routed-object sender; documents the outbound-origination gap.
- `tests/end_to_end_remote_forward.rs` — two-router loopback forward; body →
  harness; component-socket object; replay refusal.
- `tests/criome_forward_lands_in_mirror.rs` — real criome BLS + real
  `mirror::Engine`; real Spirit record body lands durably, head re-hashes.
- `tests/criome_forward_attestation.rs` — auth accept/refuse witnesses
  (referenced, not read in full this pass).
- `ARCHITECTURE.md` — spirit-vcs remote-mirroring milestone (Spirit `d6he`,
  archived intent `57f9`); milestone-2/3 verifier seam; net-new items.

Contract types (in `signal-router`, not read at source this pass but used
throughout): `ForwardedMessagePayload`, `RoutedContractObject`,
`RouterForwardRequest`, `RouterPeerAttestation`, `RouterForwardRefusalReason`
(`AttestationInvalid` / `ReplayDetected` / `ClockSkew` / `RecipientUnknown`),
`ForwardAccepted` / `ForwardRefused`, `RouterDeliveryStatus::ForwardedRemote` /
`Deferred`.

## Unknowns (and what would resolve them)

- Do PRODUCTION node configs actually set `tailnet_listen_address` and
  `criome_socket_path` today, or only tests/the witness bin? I confirmed the
  fields and the daemon wiring, not a deployed `RouterDaemonConfiguration`.
  Resolve by reading the router config emitted for a live node (CriomeOS/lojix
  bootstrap output) — out of scope for this read-only router-repo pass. NOTE: a
  sibling artifact `agent-outputs/PersistentSpiritMirror/
  OperatingSystemImplementer-LiveMirrorProof.md` and the recent primary commit
  "live A->B Spirit mirror proof on the standing prometheus guests" suggest a
  live run exists — corroborate there.
- Exact durability of a parked message across router restart. Strong evidence it
  is in-memory only (pending `Vec::new()`, no pending table, no rehydrate), but I
  did not read `persist_message`'s full body or a startup replay path end to end.
  Resolve by reading `persist_message` and `RouterRuntime` startup in
  `src/router.rs`.
- Whether any origin-side submission surface can attach a `RoutedContractObject`
  (vs body-only). Evidence says no (witness-bin comment + `payload_for` empty +
  `PendingRouterMessage::new` empty), but I did not exhaustively read the
  `signal-message` ingress contract. Resolve by reading `signal-message`'s
  `Input`/submission types.
- `RouterDeliveryStatus::Deferred` observable semantics for parked remote
  forwards vs local parks — referenced in `ARCHITECTURE.md` but not traced to the
  observation plane code this pass.

Not checked this pass: `src/adjudication.rs`, `src/channel.rs` internals,
`src/supervision.rs`, `src/observation.rs`, `src/meta.rs`, the
`signal-router`/`signal-mirror`/`signal-criome` contract crates at source, and
`tests/criome_forward_attestation.rs` in full.
