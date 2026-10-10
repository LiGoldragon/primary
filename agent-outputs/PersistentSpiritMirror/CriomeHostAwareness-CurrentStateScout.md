# Criome Host Awareness — Current-State Scout

Read-only situational map for the follow-on build-method proposal and the
implementation workers who will add a **route store** (a `Criome host ID → route`
mapping in the router's durable state) so that a live two-node cross-node
founding ceremony can actually convey founding "over the router."

Ground truth = source at `/git/github.com/LiGoldragon/*` (canonical working set;
`repos/` is empty, `/home/li/wt/...` mirrors the same). Observation is separated
from interpretation throughout. Citations are `path:line` against the checkouts
inspected 2026-07-05.

Approved terminology used here (from the brief): **Criome** = the `Contract`
cryptographic type; **Criome host** = the daemon that runs/serves Criomes;
**Criome host ID** = a host's Criome master public key (the value founding calls
"node identity"). **Route** = the network locator owned by the router.

## 0 · Headline

- The router **already carries the whole cross-host transport** — TCP tailnet
  ingress, encrypted mutually-authenticated peer session, criome BLS attestation,
  durable outbound backlog, one witnessed real two-node loopback forward. The
  net-new piece is **host awareness**: a durable, updatable `host ID → route`
  store. Today that mapping (`RemoteRouterRegistry`) exists but is **in-memory and
  seeded once from a tmpfs bootstrap document each boot** — never persisted,
  never updated at runtime, no discovery.
- The founding ceremony's "convey over the router" is **stubbed on the criome
  side** (`RouterQuorumVoice::submit` returns an error) and the production criome
  daemon runs a **`SilentVoice`** that reaches no peer at all. So the cross-node
  founding path is two independent stubs plus an unpopulated route store.
- The **seam** is `router/src/remote_router.rs` (`RemoteRouterRegistry`) backed by
  a new SEMA family in `router/src/tables.rs`, mirroring the existing durable
  `router-outbound-backlog` rehydrate pattern.
- **drop-next coordination:** nothing has landed to `main` in any repo. The four
  repos central to this seam — `router`, `signal-router`, `meta-signal-criome`,
  `meta-signal-router` — have their authoritative code on **`main`** (their
  `drop-next` branches are *stale*, `main` moved ahead). `signal-criome` has a
  **dirty working copy** (active rename edit — coordinate, do not touch). No
  Orchestrate claims on any in-scope repo.

## 1 · Current router durable-state model

Repo: `/git/github.com/LiGoldragon/router` (Persona family). ARCHITECTURE.md is
large and current (61 KB, covers §2.9 networked forwarding + §2.10 persistent
mirror transport).

### 1a · Durable SEMA families (observed)

`src/tables.rs`: `ROUTER_SCHEMA_VERSION = 2` (`tables.rs:25`). Registered families
(`tables.rs:33-88`):

- `router-channel`
- `router-adjudication-pending`
- `router-message`
- `router-delivery-attempt`
- `router-delivery-result`
- `router-mirror-switch` (single-row owner toggle; added at schema v2)
- `router-outbound-backlog` (durable forward queue; added at schema v2)

**There is no route/peer/host family.** The `RemoteRouterRegistry` route table is
absent from durable storage.

Durable store path in production: `/var/lib/persona-router/router.sema`
(`CriomOS/modules/nixos/persona-router.nix:35`, `stateDirectory`, mode 0700,
persistent).

### 1b · The route table today — in-memory, bootstrap-seeded (observed)

`src/remote_router.rs` `RemoteRouterRegistry` (`remote_router.rs:30-68`):

```
peers: HashMap<String, TailnetAddress>          // RemoteRouterIdentity payload → address
homes: HashMap<ActorIdentifier, RemoteRouterIdentity>   // recipient actor → home peer
```

- `ResolveRemoteRoute { recipient }` walks recipient → home identity → address
  (`remote_router.rs:60-67`), returning `RemoteRoute { home, address }`.
- Doc header (`remote_router.rs:1-16`): both maps are "populated from the
  deploy-time bootstrap document (report 120 §4b, decision §5 shape A)" —
  "identity is stable, address re-homes."
- The two write handlers `RegisterRemotePeer` / `RegisterRemoteActorHome`
  (`remote_router.rs:122-144`) are called **only** from the bootstrap-apply path:
  `router.rs:1400` and `router.rs:1415`, dispatched by `BootstrapApply::apply`
  (`router.rs:4157/4163`) over a `RouterBootstrapDocument`. There is **no**
  runtime learn/update/refresh/persist/rehydrate path for routes (grep for
  `learn|update_route|refresh_route|persist.*route` returns only an unrelated
  outbound-backlog doc comment at `tables.rs:564`).

Interpretation: the route table is rebuilt from scratch on every daemon start
from an rkyv bootstrap archive that itself lives on **tmpfs** (see §1d). It is
neither persistent nor a last-known-route store; a peer whose address changed
between boots is simply re-read from whatever the bootstrap document says.

### 1c · Router already knows its own location and identity (observed)

`src/config.rs` `Configuration`:

- `tailnet_listen_address() -> Option<SocketAddr>` (`config.rs:93`) — its own TCP
  ingress bind address; `None` ⇒ single-host, no TCP tier.
- `router_identity() -> &RemoteRouterIdentity` (`config.rs:99`) — this router's
  own stable identity, stamped into outbound attestations.
- `criome_socket_path() -> Option<&Path>` (`config.rs:106`) — the co-resident
  criome working socket.

All three come from the binary `RouterDaemonConfiguration` archive written at
startup; the daemon never parses NOTA (`config.rs:37-46`). So "the router needs
to know its own location" is **already satisfied** — statically, from config.

### 1d · The existing durable-backlog pattern to mirror (observed)

ARCHITECTURE §2.10 (`ARCHITECTURE.md:673-696`) + `tables.rs`: the live forward
queue `RouterRoot.pending` is now backed by the durable `router-outbound-backlog`
SEMA family — every pending item is `persist_outbound_backlog`'d before entering
the in-memory queue, removed only on terminal outcome, and **rehydrated on
`RouterRoot::on_start`** (`rehydrate_outbound_backlog`) before admitting new work.
This is the exact persistence+rehydrate shape a durable route store should copy.
(Note: the sibling `RouterTransportReadiness-Scout.md` predates §2.10 and lists
backlog durability as missing — that gap is now closed; the **route table**
durability gap is what remains.)

## 2 · Current founding-conveyance code path

Repos: `criome`, `signal-criome`, `meta-signal-criome`, `CriomOS`. (Prior sibling
scout `CriomeCeremony-CurrentStateScout.md` covers the ceremony internals in more
depth; this section focuses on the router-conveyance seam.)

### 2a · The intended "over the router voice" wire surface (observed)

signal-criome working-socket ops (`signal-criome/schema/lib.schema`):

- `ObserveNodePublicKey → NodePublicKey { public_key: BlsPublicKey }`
  (`schema:36,68,270-272`) — a public read-op so a founding client can display and
  exchange a node's **Criome master public key** out-of-band before founding.
- `ConveyFounding(FoundingConveyance) → FoundingConveyed(FoundingConveyanceReceipt)`
  (`schema:37,70`). `FoundingConveyance` (`schema:211-262`) =
  `[(Proposal FoundingProposal) (Signature FoundingSignatureReturn)
  (Founded FoundedRoot)]` — the three founding movements between cohort criomes.
  Schema comment: "Founding conveyance (node-to-node, over the router voice) …
  across peers' working sockets."

meta-signal-criome owner-driven cross-node ops (0.5.0, commit `bf916c1`, currently
on `main`):

- `InitiateRootFounding(RootFoundingInitiation { cohort: RootGenesis })`
  (`meta-signal-criome/schema/lib.schema:45,133-135`).
- `AcceptRootFounding(RootFoundingAcceptance { anchor, cohort })` (`schema:44,101-104`).
- `ObserveRootFounding` → `RootFoundingStatus { state, pending }` (`schema:46,62,157-160`).
  Schema comment (`schema:122-133`): "Cross-node founding (owner-driven, over the
  router voice) — the owner initiates a multi-node founding on ONE node (the
  initiator) … sends the founding Proposal to each peer over the router voice."

**Routing content of every founding/meta op: none.** Fields are `Identity`
(a host-name enum), `RootGenesis`, `BlsPublicKey`, `RootAnchorDigest`,
`FoundingSignature`. `initiator` is an `Identity`, not an address. Founding
carries *who*, never *where*.

### 2b · The criome runtime path (observed)

`criome/src/actors/root.rs` (methods on `CriomeRoot`):

- `initiate_root_founding` (`root.rs:2347`) records pending, then for each non-self
  cohort member calls `self.voice.convey(&member.identity,
  CriomeRequest::convey_founding(FoundingConveyance::Proposal(...)))`
  (`root.rs:2364-2375`).
- `convey_founding` (`root.rs:2193`) → `receive_founding_proposal` /
  `receive_founding_signature` / `receive_founded_root`.
- `accept_root_founding` (`root.rs:2047`) is the only place the master key signs.
- Single-node founding, reboot verify/adopt, real BLS: all real
  (`criome/src/founding.rs`, `criome/src/master_key.rs`).

### 2c · The voice — where host location lives, and where it stubs out (observed)

`criome/src/voice.rs`, trait `QuorumVoice { convey(recipient, request); … }`
(`voice.rs:37-46`). Three impls:

- `SilentVoice` (`voice.rs:50-56`) — default; conveys nothing.
- `DirectDialQuorumVoice { routes: Vec<PeerSocketRoute> }` (`voice.rs:77`),
  `PeerSocketRoute { peer: Identity, socket: PathBuf }` (`voice.rs:60-63`) — REAL,
  dials the peer's working Unix socket directly. Used only in tests.
- `RouterQuorumVoice { router_socket, source_actor, routes: Vec<PeerActorRoute> }`
  (`voice.rs:134-138`), `PeerActorRoute { peer: Identity, destination: ActorIdentifier }`
  (`voice.rs:119-122`) — the intended criome→router handoff. Its framing helper
  `request_octets` is real (`voice.rs:164-173`), but **`submit` is stubbed**:
  returns `Err(Error::VoiceDelivery("… router conveyance waits for the clean
  signal-router routed-object constructor"))` (`voice.rs:175-181`).

`SubmitRoutedObjects` / `RoutedContractObject` appear in criome **only in
doc-comments** (`voice.rs:11,131,132`); `ForwardMessage` does not appear at all.

### 2d · Production wiring — not connected (observed negative evidence)

- `CriomeDaemon::from_configuration` hard-codes `voice: Arc::new(SilentVoice)`
  (`criome/src/daemon.rs:78`); `from_environment`/`new` likewise (`daemon.rs:56`).
  `with_quorum_voice`, `DirectDialQuorumVoice`, `RouterQuorumVoice`,
  `PeerSocketRoute`, `PeerActorRoute` are constructed **only in `criome/tests/*`**,
  never in `src/`. A deployed CriomOS criome host runs with `SilentVoice` and
  cannot reach any other host.
- `CriomeDaemonConfiguration` (`signal-criome/schema:140-147`) is exactly
  `{ socket_path, store_path, meta_socket_path, cluster_root, AuthorizationMode,
  node_identity }` — **no peers, no router socket, no host list.** There is no
  config field through which a criome host learns another host's route.
- CriomOS `modules/nixos/criome.nix` header (`criome.nix:32-52`): "CLEAN GENESIS
  … RETIRES the old hand-seeding surface … `cluster_root` is always `None`."
  Founding happens at runtime over the meta socket, but no operator meta-socket CLI
  ships in `packages.default` (`criome.nix:112-116`), and no non-silent voice is
  wired.
- The two-node founding test `criome/tests/founding_conveyance.rs:1-10` states it
  is "the in-process, direct-dial analogue of the live 2-node proof" over
  `DirectDialQuorumVoice` — it does **not** use the router.

### 2e · node identity = Criome master pubkey (observed)

Not a literal equality in code:

- `node_identity: Optional Identity` is configured; `Identity::Host(PrincipalName)`
  is a **name string**, not a key (`signal-criome/schema:132-138`). Default
  `Identity::host("criome")` (`root.rs:158-160`).
- The master key is minted/read from a separate file
  (`store.masterkey`, `root.rs:2447-2448`; `master_key.rs:45-107`).
- The **binding** identity→master-pubkey is a registry record written at `on_start`
  (`root.rs:2470-2502`): `IdentityRegistration::new(criome_identity,
  master_public_key, fingerprint, KeyPurpose::CriomeRoot, None)`; the daemon
  refuses to start if an existing record's key differs (`root.rs:2478-2483`).
- In a cohort the binding is `FoundingMember { Identity, public_key: BlsPublicKey }`
  and the anchor `blake3(rkyv(RootGenesis))` self-certifyingly commits to the keys
  (`founding.rs:5-7`, `signal-criome/schema:176-197`).

Cross-check with the router: `router/src/criome_attestation.rs:90-101` derives a
node's criome signer identity as `Identity::host(node.payload())` where `node` is
the `RemoteRouterIdentity`; the comment (`:27-34`) states criome's configured
`node_identity` **equals** this node's `router_identity`. So the router's peer
identity string and criome's `Host(<name>)` principal are the **same name**, and
criome's registry maps that name → the registered BLS master key.

## 3 · Wire-contract routing surface

Full type survey (see the wire-contract sub-scout for exhaustive `path:line`).
Generated Rust lives at `src/schema/lib.rs`; doc-bearing source at
`schema/lib.schema`. **No wire type anywhere derives `Hash`.**

### 3a · signal-router — the only address-bearing contract (observed)

Addressing vocabulary (`signal-router/schema/lib.schema:45-50`):

```
;; Addresses re-home; identity does not — a peer is dialed by its
;; TailnetAddress but routed by its stable RemoteRouterIdentity.
TailnetAddress       String     // an opaque "[IPv6]:port" literal
RemoteRouterIdentity String     // the peer's stable criome PrincipalName (ARCHITECTURE:225-227)
HostName             String     // DEFINED BUT STRUCTURALLY UNUSED — no field references it
```

- `RegisterRemoteRouter { identity: Identity, address: Address }` where
  `Identity(RemoteRouterIdentity)`, `Address(TailnetAddress)` (`schema:70-80`,
  generated `src/schema/lib.rs:333`). This is exactly `host ID → route`.
- `RegisterActor { actor: Actor, home: Option<RemoteRouterIdentity> }`
  (`schema:63-69`): `home = None ⇒ local`, `Some(peer) ⇒ actor lives behind that
  remote router` — schema comment: "how a router learns which host a recipient
  lives on (the production source for remote-route resolution)."
- `RouterBootstrapOperation [RegisterActor GrantDirectMessage
  InstallStructuralChannels RegisterRemoteRouter]` (`schema:81-88`);
  `RouterBootstrapDocument { Operations: Vector<RouterBootstrapOperation> }`.
- Forward transport types: `RoutedContractObject`, `ForwardedMessagePayload`,
  `RouterForwardRequest`, `RouterPeerAttestation`, `ForwardMarker [Origin Forwarded]`,
  `RouterForwardRefusalReason [UnknownPeer AttestationInvalid ReplayDetected
  ClockSkew RecipientUnknown ChannelUnauthorized AlreadyForwarded MirrorDisabled
  SessionRequired]`.

### 3b · Absences that define the tentative/Yggdrasil work (observed)

- **No tentative / best-effort / last-known / staleness / reliability / reachability
  field or variant** anywhere across signal-router, meta-signal-router,
  signal-criome, meta-signal-criome. `TailnetAddress`, `Address`,
  `TailnetListenAddress`, `RemoteRouterIdentity` are all bare `String` newtypes
  (or `Option` thereof). The only "addresses change" notion is the prose comment
  "addresses re-home; identity does not."
- **No typed Yggdrasil-vs-raw-IP address-kind distinction.** `TailnetAddress` is a
  single opaque string; "Yggdrasil/WireGuard IPv6" appears only as a free-text
  comment in `signal-router/examples/canonical.nota:85`. No `SocketAddr`/`std::net`
  type on any wire contract.
- `HostName(String)` in signal-router is an addressing noun with **no field
  referencing it** — a latent, unused slot.

### 3c · signal-criome / meta-signal-criome — no address types at all (observed)

Pure crypto identity/authority/attestation: `Identity [Persona Agent Host Developer
Cluster]` (name strings), `BlsPublicKey String`, `NodePublicKey`, `RootGenesis`,
`FoundingMember`, `RootAnchorDigest`, `FoundingSignature`. There is **no**
host-address, network-locator, route, endpoint, SocketAddr, IP, or peer-reach type
in either criome contract. Routing content stays entirely router-side.

### 3d · meta-signal-router — policy vocabulary, not dialable (observed)

`Input [Grant Extend Revoke Deny SetMirrorEnabled]` (`meta-signal-router/schema/lib.schema:51`).
It defines `HostName String`, `NetworkPeer String`, `OtherPersonaEngine`,
`ConnectionClass`, `ChannelEndpoint` — but these are **trust-class / channel-grant
endpoints**, not dialable transport addresses, and carry no address-kind or
staleness metadata. This is the meta socket where an owner-only route-update /
route-store-write op would naturally live (mirroring `SetMirrorEnabled`), but no
such op exists today.

## 4 · The `Criome host ID → route` store seam

### 4a · Where it lives (observed)

- **Store**: `router/src/remote_router.rs` `RemoteRouterRegistry` (in-memory maps).
- **Durable model**: `router/src/tables.rs` (SEMA families + `ROUTER_SCHEMA_VERSION`).
- **Seed source**: `RouterBootstrapDocument` → `RegisterRemoteRouter` +
  `RegisterActor{home}` ops, applied once at startup (`router.rs:4139-4170`).
- **Bootstrap production origin**: `CriomOS/modules/nixos/persona-router.nix`.
  `peers` / `actorHomes` / `grants` come from the horizon `PersonaRouter`
  node-service payload (`persona-router.nix:82-84`); they are lowered to a NOTA
  `BootstrapWriteRequest`, written by `router-write-bootstrap` at `ExecStartPre` to
  `/run/persona-router/bootstrap.rkyv` (a **tmpfs** runtime dir), and applied by
  the daemon at start. Own location/identity/criome-socket are lowered into
  `ConfigurationWriteRequest` (`persona-router.nix:104-114`); the module example
  is `(Some 0.0.0.0:7440) <routerIdentity> (Some /run/criome/criome.sock)` with
  `routerIdentity = settings.identity or config.networking.hostName`
  (`persona-router.nix:44`) — i.e. **the NixOS hostname by default**.

### 4b · Current shape vs what must be added (observation + interpretation)

Observed current shape:
- Key = `RemoteRouterIdentity` **String payload** = a criome `PrincipalName` /
  `Host(<hostname>)` name. Value = `TailnetAddress` String (`[IPv6]:port`).
- Lifecycle = seed-once, in-memory, thrown away and rebuilt each boot.

Net-new for a durable route store (interpretation, grounded in the existing
`router-outbound-backlog` pattern §1d):
1. A durable SEMA family (e.g. `router-remote-route` keyed by host identity) in
   `tables.rs`, which raises `ROUTER_SCHEMA_VERSION` to 3 (coordinated upgrade per
   the schema-version guard).
2. `persist` on register + `rehydrate` on `RouterRoot`/registry `on_start`, so the
   **last-known route** survives restart instead of being re-read from tmpfs.
3. A runtime **route-update** path (currently only bootstrap writes exist): either
   an owner-only meta op (`meta-signal-router`, mirroring `SetMirrorEnabled`), a
   working-socket bootstrap-style op, or learned-from-inbound-session — a design
   decision (see §7).

Tentative / Yggdrasil representation (interpretation):
- **Tentative/best-effort**: net-new typing. Add a route-quality/confidence and/or
  `last_seen` marker on the stored route record (nothing exists today). The wire
  `TailnetAddress` newtype has no such field.
- **Yggdrasil-vs-IP**: net-new typing. Add an address-kind tag (Yggdrasil is
  expected "far more reliable" per the brief). Today it is a single opaque string.
- **Design tension to resolve (load-bearing):** ARCHITECTURE §2.9.1
  (`ARCHITECTURE.md:552-591`, invariants `:781-787`) currently treats the Yggdrasil
  service binding as an **audited, fail-closed startup check** — "a mismatch is a
  startup failure, not a best-effort warning." That is the *opposite* of the
  brief's "routes are tentative hints that can go stale." The build method must
  reconcile these: which routes are audited-hard (own binding / bootstrap seed) vs
  tentative-soft (learned / last-known). The natural anchor for the soft side is
  the existing "addresses re-home; identity does not" split — identity stable, route
  tentative.

## 5 · Concrete gap to a live two-node cross-node founding

What is BUILT and witnessed (observed):
- Router cross-host transport: `TailnetForwardIngress` (inbound), `RouterPeerDelivery`
  (outbound), encrypted mutually-authenticated `PeerSession` (X25519 ECDH +
  ChaCha20-Poly1305), criome BLS `ForwardAttestationVerifier`
  (`CriomeForwardAttestation`), replay/clock-skew admission window, durable
  outbound backlog. Proven by `tests/end_to_end_remote_forward.rs`,
  `tests/criome_forward_lands_in_mirror.rs` (real criome BLS + real mirror body
  crossing loopback TCP and re-hashing to Spirit's head),
  `tests/encrypted_peer_session.rs`.
- Static route seeding surface exists end-to-end: `persona-router.nix` → bootstrap
  doc → `RemoteRouterRegistry` → `ResolveRemoteRoute`.

What is MISSING for cross-node founding (observed stubs/absences):
1. **criome origination over the router is stubbed.** `RouterQuorumVoice::submit`
   errors (`criome/src/voice.rs:175-181`) "waits for the clean signal-router
   routed-object constructor." No criome code hands a `FoundingConveyance` to its
   local router via `SubmitRoutedObjects`.
2. **Production criome runs `SilentVoice`** (`criome/src/daemon.rs:78`) and has
   **no config field for peer routes** (`CriomeDaemonConfiguration` lacks them).
   Even the static path is unwired on the criome side.
3. **The route store is not durable and not host-aware beyond static seed.** No
   `host ID → route` SEMA family, no rehydrate, no runtime update, no discovery
   (`router/src/remote_router.rs`, `router/src/tables.rs`).
4. **No operator founding tool ships** in criome `packages.default`
   (`CriomOS/modules/nixos/criome.nix:112-116`).
5. **Reverse/dynamic route resolution is flagged net-new** in the router itself
   (`ARCHITECTURE.md:508-515`): homes come only from the deploy-time bootstrap, so
   a recipient with no pre-registered home cannot be resolved at runtime.

Minimal critical path to a live two-node founding (interpretation):
- criome side: implement `RouterQuorumVoice::submit` (SubmitRoutedObjects to the
  local router working socket) and wire a non-silent voice + peer-actor routes into
  the deployed daemon (needs new `CriomeDaemonConfiguration` fields or a router
  handoff that resolves peers itself).
- router side: make `RemoteRouterRegistry` a durable, host-aware route store so
  criome A's router resolves "criome B lives on node B at address X" — the piece
  that turns "founding conveyed over the router" from schema into behaviour.
- Both sides already share the identity model: criome `Host(<name>)` == router
  `RemoteRouterIdentity` == the master-key registration; the master pubkey is
  exchanged out-of-band via `ObserveNodePublicKey` before founding.

## 6 · drop-next naming / branch state + coordination flags

An overnight authoritative mass-rename ("drop-next") is dropping a `-next` suffix
from upstream dependency repo/crate references (`nota-next → nota`,
`schema-rust-next → schema-rust`, `schema-next → schema`) across the LiGoldragon
repos. Post-rename names are authoritative. Read-only observation below (per-repo
`jj` ancestry + working-copy state); no claim or edit made.

**Landed to `main`: NONE.** `drop-next` is not an ancestor of `main` in any repo.

| Repo | main tip | drop-next vs main | State | Dirty? | Notes |
|---|---|---|---|---|---|
| **router** | `0af3624a` | diverged: drop-next 2 ahead, **main ~10 ahead** | in-progress, drop-next **stale** | clean | main still refs `nota-next`,`schema-rust-next`,`schema-next` |
| **signal-router** | `81c39d85` | diverged: **main 4 ahead** | in-progress, drop-next stale | clean | seam code (SessionRequired etc.) is on main |
| **meta-signal-criome** | `bf916c1d` | diverged: **main 4 ahead** | in-progress, drop-next stale | clean | **0.5.0 cross-node founding ops are on main** |
| **meta-signal-router** | `31f9262d` | diverged: **main 1 ahead** | in-progress, drop-next stale | clean | SetMirrorEnabled is on main |
| **criome** | `0608a42c` | main ⊆ drop-next (drop-next ahead) | ready to fast-forward | clean | deps pinned `branch="drop-next"` |
| **signal-criome** | `c71ef716` | main ⊆ drop-next | ready to fast-forward | **DIRTY: M Cargo.lock** | active rename edit — coordinate |
| **lojix** | `9f42435f` | main ⊆ drop-next | ready to fast-forward | clean | deps pinned `branch="drop-next"` |
| **horizon-rs** | `cfa13fa5` | main ⊆ drop-next | ready to fast-forward | clean | ~16 `-next` residues on main |
| **CriomOS** | `399f29e7` | main ⊆ drop-next | ready to fast-forward | clean | `flake.lock` refs `*-next`; also unrelated bookmark `next` (ignore) |

Coordination flags for the follow-on build:

- **Target `main`, not `drop-next`, for the seam repos.** router / signal-router /
  meta-signal-criome / meta-signal-router carry their authoritative current code on
  `main`; their `drop-next` branches are stale and will need re-integration when the
  rename lands. Expect crate/dep name churn (`*-next → *`) at land time; do not hard
  depend on the `-next`-suffixed dependency identifiers.
- **`signal-criome` has a dirty working copy** (`M Cargo.lock`) on its `drop-next`
  tip — the rename agent appears mid-edit. Do not touch that checkout; coordinate.
- **Active rename worktrees** (own jj workspaces, avoid colliding): `worktrees/
  worker2-signal-spirit-drop-next` (signal-spirit/drop-next) and `worktrees/
  worker20-criomos-drop-next` (CriomOS/drop-next). The `*-landing` worktrees are
  idle/clean on primary `main`.
- **No Orchestrate claims/locks on any in-scope repo.** `(Observe Roles)` shows one
  active claim only: `cloud-maintainer → /git/github.com/LiGoldragon/cloud`
  (unrelated). The rename agent coordinates via worktrees, not role-claims.
- Primary `main` records a tracked "rename-propagator: record Worker30 landing
  blocker" — landing is not complete.

## 7 · Open unknowns (and where each resolves)

1. **Route-store key: raw master pubkey or PrincipalName/hostname?** Current code
   keys on the `Host(<hostname>)` name string; the brief's "host ID = master public
   key" is a different value bound to that name in criome's registry. Which is the
   store key is a design decision. Resolve in the build-method proposal (and confirm
   with the psyche if it bends the identity model).
2. **Tentative vs audited Yggdrasil binding** (§4b tension). Resolve by deciding
   which routes are hard-audited (own binding, bootstrap seed) vs soft-tentative
   (learned, last-known), then updating `ARCHITECTURE.md §2.9.1` invariants.
3. **Route-update authority surface.** Meta-socket owner op (like `SetMirrorEnabled`)
   vs working-socket bootstrap op vs learned-from-session. Not decided in code.
   Resolve in build method; check `push-not-pull` doctrine (no polling).
4. **Does a live 2-node horizon config already populate `peers`/`actorHomes`?**
   `persona-router.nix` reads them from the `PersonaRouter` node-service payload, but
   whether a deployed 2-node cluster sets them was not confirmed here. Resolve by
   reading a live node's horizon payload and the sibling artifacts
   `OperatingSystemImplementer-LiveMirrorProof.md` and
   `OperatingSystemImplementer-MirrorStandUpFindings.md` in this directory (a live
   A→B mirror run is reported to exist).
5. **`report 120` / `decision §5 shape A`** cited in `remote_router.rs:6-7` — the
   original design record for the registry. Not located under `reports/` or
   `agent-outputs/` this pass; resolve by asking the orchestrator or searching the
   rename agent's records if the shape-A rationale matters to the build.
6. **Criome side of the router handoff** (how criome learns peer `ActorIdentifier` +
   which local router socket) — `RouterQuorumVoice` needs routes it never receives
   in production. Whether criome resolves peers itself or defers entirely to the
   router's store is undecided. Resolve in build method jointly with §5.1/§5.2.

## Pickup pointers

- Router seam code: `router/src/remote_router.rs`, `router/src/tables.rs`,
  `router/src/config.rs`, `router/src/router.rs` (bootstrap apply ~`1380-1430`,
  `4085-4210`), `router/src/criome_attestation.rs`, `router/ARCHITECTURE.md`
  §2.9 / §2.9.1 / §2.10.
- Criome founding code: `criome/src/voice.rs` (the stub), `criome/src/actors/root.rs`,
  `criome/src/daemon.rs` (SilentVoice), `criome/src/founding.rs`.
- Contracts: `signal-router/schema/lib.schema`, `signal-criome/schema/lib.schema`,
  `meta-signal-criome/schema/lib.schema`, `meta-signal-router/schema/lib.schema`.
- Production wiring: `CriomOS/modules/nixos/persona-router.nix`,
  `CriomOS/modules/nixos/criome.nix`.
- Sibling artifacts in this directory to build on (not re-derived here):
  `RouterTransportReadiness-Scout.md`, `CriomeCeremony-CurrentStateScout.md`,
  `MirrorArchitecture-Design.md`, `OperatingSystemImplementer-LiveMirrorProof.md`.
