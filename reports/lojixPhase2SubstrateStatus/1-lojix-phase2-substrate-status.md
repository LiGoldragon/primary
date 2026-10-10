# Lojix phase-2 substrate status — code-only

Read-only status check for the lead. SOURCE only; no orchestrate role/lock
observation; prior session reports were not trusted. Verdicts reflect what the
current code shows on 2026-06-27.

Phase-2 intent (from the psyche): all inter-system action happens through each
component's own lojix daemon; the local daemon is authoritative for local
state; a request is sent from one daemon to another through the router; this
requires criome authentication propagated so criome runs on all components and
daemons can authenticate to each other.

## Verdicts

1. criome auth propagation — **net-new** (local auth primitives exist; the
   inter-daemon propagation layer does not).
2. lojix inter-daemon action (phase 2) — **net-new** (a router peer-forward
   fabric exists, but for Persona messages only; lojix is unwired in both
   directions and has no outbound transport).

## 1. criome auth propagation — net-new

Canonical source: `/git/github.com/LiGoldragon/criome` (symlinked
`repos/criome`).

### What exists (real, but local single-authority)

- Master BLS keypair, secret persisted `0600`, never crosses a wire:
  `src/master_key.rs:38-121`. BLS verify trait: `src/master_key.rs:125-146`.
- Identity registry (`Identity <-> BlsPublicKey`, Active/Revoked):
  `src/actors/registry.rs:98-202`.
- Signer (signs grants as criome's identity, gated on active identity):
  `src/actors/signer.rs:198-234`. Verifier (resolves signer in the LOCAL
  registry, checks revocation/scheme/signature/expiry):
  `src/actors/verifier.rs:40-109`.
- Authorization coordinator — local signature-quorum state machine:
  `src/actors/authorization.rs:104-238`.
- Cluster-root admission gate (closest thing to cross-instance trust): a
  configured `ClusterRoot` BLS pubkey must sign a registration statement for a
  key to be admitted — `src/admission.rs:73-102`
  (`ClusterRoot::admits`), wired into `register` at
  `src/actors/registry.rs:106-116`. Bypassed entirely when no cluster root is
  configured; gates LOCAL registration of a key, not a peer-daemon connection.

### Transport / admission are local-socket only

- Client connects `UnixStream` to `CRIOME_SOCKET` or `/tmp/criome.sock`:
  `src/transport.rs:220-237` (and the only `connect(` calls are
  `transport.rs:233` and `:254`; no `TcpStream`/`TcpListener` anywhere in
  `src/`).
- Daemon binds a `UnixListener` at `0600`
  (`bind_private_socket`, `src/daemon.rs:129-137`); `handle_connection` reads a
  frame and serves it with NO peer authentication — `src/daemon.rs:139-154`.
  Sole access control is filesystem `0600` (same-UID); no `SO_PEERCRED`, no
  cryptographic peer challenge. Caller origin is a self-asserted `AuditContext`.

### Gap to "one daemon authenticating to another via criome, criome on every component"

- No remote transport. Cross-host is explicitly an open design slot:
  `ARCHITECTURE.md:204-209` and `:432-444` (deferred to a follow-up report).
- No peer-routing table / peer client (peer pubkey -> host+unix-user, peer
  socket naming) — described `ARCHITECTURE.md:277-279`, `:414-430`, not
  implemented.
- `RouteSignatureRequest` only stores the solicitation locally; nothing opens a
  socket to another criome — `src/actors/authorization.rs:174-184` ->
  `store_signature_solicitation:276-286`. `routed_to` is a recorded field, not
  a delivered request.
- No mutual auth handshake: the `signal`-crate handshake is protocol-version
  only; `client_name` is "not authoritative", multi-instance `server_id`
  "lands when multi-instance criome is implemented"
  (`/git/github.com/LiGoldragon/signal/src/handshake.rs:20-25,47-64`).
- criome is not "running on every component" as an inter-daemon auth layer.
  Consumers use a LOCAL co-resident criome over the `0600` socket: spirit
  (`/git/github.com/LiGoldragon/spirit/src/criome_gate.rs:18-24` — "1-of-1
  LOCAL criome gate"), mentci tests (local daemon), orchestrate (only
  `signal_criome` wire types, no daemon client), router (depends only on
  `signal-criome` wire vocab — `router/Cargo.toml:47`). lojix has NO criome
  dependency at all; its only "criome" tokens are SSH/DNS domain names
  (`CriomeDomainName`, `root@<node>.<cluster>.criome`) for Nix deploy targets
  (`/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:19,599-605,3516-3526`).

The integration map at `criome/ARCHITECTURE.md:447-462` ("peer criome daemons
via signal-criome peer routing") is design, not code.

## 2. lojix inter-daemon action (phase 2) — net-new

Canonical source: lojix daemon `/git/github.com/LiGoldragon/lojix`; router
`/git/github.com/LiGoldragon/router` (symlinked `repos/router`).

### What exists

Lojix is local-only and inbound-only:

- CLI client dials ONLY local Unix sockets (defaults
  `/run/lojix/ordinary.sock`, `/run/lojix/owner.sock`) via `UnixStream::connect`
  — `src/client.rs:22-25,48`. That is the ONLY `connect(` in lojix `src` (no
  `TcpStream::connect`, no other outbound socket).
- Daemon binds two local Unix listeners and nothing else
  (`AsyncListenerSocket` Ordinary + Owner on one `AsyncMultiListenerDaemon`) —
  `src/daemon.rs:85-112`; never opens an outbound connection.
- Owner surface explicitly refuses TCP peers, admits only same-uid Unix peers —
  `OwnerPeerAuthority::authorize`, `src/daemon.rs:240-259`.
- No daemon-to-daemon RPC verb. Ordinary contract = Query / WatchDeployments /
  WatchCacheRetention / Unwatch / CheckHostKeyMaterial; Owner contract = Deploy
  / Pin / Unpin / Retire / Test (`src/client.rs:56-58,117-118`,
  `daemon.rs:350`). Request type is only
  `SignalInput::{OrdinaryInput,MetaInput}` with one work item
  `NexusWork::SignalArrived` — `src/schema/nexus.rs:62-64,403-404`. No
  peer/forward variant.
- lojix's "remote" is Nix remote builders (SSH/`nix build` to a builder
  machine), not peer daemons — `src/schema_runtime.rs` (e.g. 3570-3577, 2879,
  4276).
- `Cargo.toml` deps: signal-lojix, meta-signal-lojix, sema-engine,
  triad-runtime, kameo, horizon-lib, nota-next, rkyv, rustix, tokio
  (`Cargo.toml:34-46`). NO router / signal-router / signal-message — and
  `Cargo.lock` has none either (grep count 0).

The router IS a working "request from one daemon to another through a router"
fabric — but for Persona `signal-message` traffic only:

- "Persona message router and delivery state machine"; inbound binds local
  working/meta Unix sockets, applies signal-message/signal-router frames —
  `router/src/daemon.rs:103-172`.
- Outbound peer delivery exists: `RouterPeerDelivery` dials a peer router over
  TCP (`TcpStream::connect`, `router/src/peer_delivery.rs:110`) and writes a
  `signal-router::ForwardMessage` frame (`peer_delivery.rs:97-119`).
- Peer routing table: `RemoteRouterRegistry` resolves recipient
  `ActorIdentifier` -> home peer -> `TailnetAddress`
  (`router/src/remote_router.rs:60-67`).
- Inbound peer ingress: `TailnetForwardIngress` accepts forwards from peer
  routers over TCP — `router/src/router.rs:341-421`, wired in `RouterRuntime`
  at `router.rs:1099-1158`.

### Gap to "lojix daemon -> another daemon through the router"

- No outbound transport in the lojix daemon at all (it needs the analogue of
  router's `RouterPeerDelivery` / a router-client). Every byte path is an
  inbound Unix listener.
- lojix and router are unwired both ways: no router/signal-router dep in lojix;
  no lojix dep in router. The only `lojix` token in router is a
  `ComponentKind::Lojix` taxonomy enum
  (`router/src/authorized_object_projection.rs:44`), identity mapping, not a
  route.
- No remote/peer request verb in signal-lojix / meta-signal-lojix.
- The router fabric is scoped to Persona `signal-message` payloads addressed by
  actor identity; it has no concept of a lojix daemon endpoint or of carrying a
  lojix Deploy/Query request. Carrying lojix requests needs a new
  payload/contract and registry entries, not a config flip.
- Neither ARCHITECTURE/INTENT describes a lojix-through-router path; only
  thin-CLI-to-own-local-socket language at `lojix/ARCHITECTURE.md:91`,
  `lojix/INTENT.md:32`.

## Bottom line

Both phase-2 substrate pieces are net-new at the daemon-to-daemon layer. The
building blocks are unevenly present: criome has genuine local auth primitives
(BLS sign/verify, identity registry, cluster-root anchor) but no remote
transport, peer table, peer client, or mutual-auth handshake; the router has a
genuine peer-forward fabric but only for Persona messages and with lojix
entirely unwired. The single missing seam shared by both is the same: lojix has
no outbound transport and no peer/remote request verb, and is linked to neither
the router nor criome. "Daemon-to-daemon request through the router,
authenticated by criome" is unbuilt in code today.
