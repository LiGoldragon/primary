# Criome Host Awareness — Build Design

A concrete, code-grounded build design for making the router a **routing fabric
with an actual routing table** whose **primary identity is the Criome host ID
(the master public key)**: a durable, updatable `Criome host ID → route` store,
the pubkey threaded as the fabric identity, criome origination unstubbed over the
router, and a live two-node founding-over-router proof. Design pass only — no
repository was edited, no claim taken, nothing committed. This is the converged
final design; forks are settled.

Approved terminology, used exactly throughout:

- **Criome** = the cryptographic contract (the `Contract` type).
- **Criome host / Criome node** = the daemon that runs and serves Criomes,
  identified by its **Criome host ID**. This is what the pubkey conversion is
  about.
- **Criome host ID** = the host's Criome master public key (the value founding
  calls "node identity"). **The fabric's primary identity** (psyche decision,
  Fork 1).
- **OS host / OS node** = a CriomOS machine, identified by its **name**
  (hostname). Distinct concept; stays name-defined. The pubkey conversion does
  **not** touch OS/horizon host identity — see the callout below.
- **Route** = the network locator (where to dial), owned by the router.

### Two "host" concepts — keep them distinct

Implementers must not reconflate these:

| Concept | Identified by | Owned by | Touched by this build? |
|---|---|---|---|
| **Criome host / node** | **Criome host ID** (master public key) | Criome + router fabric | Yes — becomes the fabric's primary identity |
| **OS host / node** | **name** (hostname) | CriomOS / horizon | No — stays name-defined |

The router fabric keys internally on the Criome host ID. CriomOS/horizon continue
to define hosts by name. Where a name-defined OS host meets the pubkey-keyed
fabric (route seeding), the Criome host ID is resolved from that host's own criome
(`ObserveNodePublicKey`, exchanged out-of-band before founding, or committed in
the founding cohort) at the seed boundary — the OS layer never authors pubkeys.
This is a clean boundary translation, not a conflation.

Ground truth verified against source at `/git/github.com/LiGoldragon/*` on
2026-07-05 (post drop-next rename), building on
`agent-outputs/PersistentSpiritMirror/CriomeHostAwareness-CurrentStateScout.md`.

## 0 · Verification of the scout map

Load-bearing scout claims re-checked against current source; refinements that
matter to the build:

1. **The stub's named blocker is already resolved.**
   `RouterQuorumVoice::submit` errors "waits for the clean signal-router
   routed-object constructor" (`criome/src/voice.rs:175-181`). That constructor
   now **exists**: `signal_router::Input::submit_routed_objects(payload)`
   (`signal-router/src/schema/lib.rs:3136`), replies
   `RoutedObjectsAccepted`/`RoutedObjectsRefused`, router-side handler
   `RouterRoot::apply_routed_object_submission` (`router/ARCHITECTURE.md:602-625`).
   The criome unstub is unblocked at the router end.

2. **`signal-router` is self-contained** — no `signal-criome` dependency, and it
   already owns a `PublicKey String` type in the attestation
   (`schema/lib.schema:136`). Converting the router-side fabric identity to the
   pubkey lives in `router` + `signal-router`.

3. **The router can source its own Criome host ID from its co-resident criome**
   via `ObserveNodePublicKey → NodePublicKey { public_key }`
   (`signal-criome/schema/lib.schema:36,68,270`).

4. **Founding already resolves members by key.** `founding.member_by_key(...)`
   (`criome/src/actors/root.rs:2082`); the RootGenesis anchor commits to the
   cohort's public keys. So criome verify-by-key is a small, natural extension of
   an existing path, not a new mechanism.

5. **Dependency-pin reconciliation is required first** — see §8; several repos
   still pin `branch = "drop-next"` although the rename has landed on `main`.

Confirmed as scouted: in-memory `RemoteRouterRegistry`
(`router/src/remote_router.rs:30-68`); `ROUTER_SCHEMA_VERSION = 2` + seven
families (`router/src/tables.rs:25-39`); production `SilentVoice`
(`criome/src/daemon.rs:56,78`); `CriomeDaemonConfiguration` lacks peer/router
fields (`signal-criome/schema/lib.schema:140-146`); the durable-backlog
persist/rehydrate pattern (`tables.rs` + `router.rs:2501-2540`, rehydrated in
`on_start` at `router.rs:3501`); §2.9.1's fail-closed Yggdrasil audit
(`router/ARCHITECTURE.md:552-591`, invariants `:780-787`); the criome↔router
identity binding (`router/src/criome_attestation.rs:27-34,90-101`). The
route-registration seam `RouterRuntime::install_remote_peer`
(`router/src/router.rs:1408-1421`) already fires a backlog-drain push; the durable
persist attaches there.

## 1 · Design forks (settled)

### Fork 1 — Fabric identity is the Criome host ID (pubkey-primary)

**Decided by the psyche.** The Criome host ID (master public key) is the fabric's
primary identity, effective now: the route-store key, the registry home value, the
session-handshake signer, and the forward-attestation signer are all the pubkey,
not a name handle.

With `signal-criome` now free (rename done, §8), the criome verify-by-key side is
built **together with** the router send-side as one atomic identity conversion
(Slice A1). There is therefore **no transitional name-projection handle** and no
`registered_name` field on the route record — the earlier fast-follow that would
have made the name lag is folded in. The pubkey is the identity end-to-end, on
both the send and verify sides, from the first slice.

Security is now direct: the router's fabric identity *is* the verified key; a
stranger fails the session handshake fail-closed (`UnknownSigner`); a stale or
wrong address is only a reachability miss (§1.4).

### Fork 2 — Typed route model

A closed typed record, no flag soup. A **direct candidate (a possible-route) is an
IP address or a domain name** (psyche refinement); the Yggdrasil baseline stays
its own audited endpoint. Address kind and locator kind are records/sums, not
flags; selection is a method. Full model in §2.

The structural fact that dissolves the special cases: **address kind is not a
security tag.** Yggdrasil and direct endpoints carry the same end-to-end security
— the PeerSession authenticates by the Criome host ID and encrypts regardless of
wire (§1.4). A route carries **reachability and redundancy** distinctions:

- **Yggdrasil baseline** — audited-hard, always-present fallback,
  secure-by-construction when the Yggdrasil system is operational.
- **Direct candidates** — an IP address (dialed directly) or a domain name
  (DNS-resolved as part of probing), preferred when reachable because the
  PeerSession already secures the wire. Tentative for reachability, never less
  secure.

### Fork 3 — Route-update authority

**Near-term: owner-seeded and durable. Design-for: learned-from-authenticated-session.**

- **Seed (audited-hard):** owner-authored — the bootstrap document and a new
  owner-only `meta-signal-router` operation `SeedRemoteRoute` mirroring
  `SetMirrorEnabled` (0600 meta socket, persisted). Writes the Yggdrasil baseline.
- **Learn (tentative-soft, design-for):** when a peer completes the PeerSession
  handshake — proving its Criome host ID by BLS, fail-closed on a stranger — the
  router MAY record the observed source address as that peer's direct candidate.
  No new host is auto-admitted; only a known, proven host's reachability hint is
  refreshed. Push, not poll: the existing `PeerSessionEstablished { peer, epoch }`
  event (`router/ARCHITECTURE.md:666-670`) is the hook. Learning updates only the
  tentative direct-candidate layer, never the audited baseline.

**Open for psyche (§9):** build learning now or defer.

### Fork 4 — §2.9.1 reconciliation

**Keep the fail-closed audit; reframe it as an integrity check on the *Yggdrasil
baseline* seed, separate from tentative direct-candidate selection.** Security
lives at the PeerSession layer, keyed on the Criome host ID; address selection is
uniformly tentative and reachability-driven. A stale/wrong address fails the
identity proof fail-closed, so it is never a breach. ARCHITECTURE text in §7.

## 1.4 · Why direct IPs/domains are not less secure (load-bearing insight)

The encrypted, mutually-authenticated PeerSession (§2.10,
`router/ARCHITECTURE.md:627-665`) authenticates the peer by its Criome host ID
(BLS) and encrypts every forward over whatever wire the route selected. A
Yggdrasil address adds a redundant transport-crypto layer (the reliable baseline);
a direct IP or DNS-resolved domain relies solely on the PeerSession, which is
already sufficient. The trust boundary is the handshake, not the address — which
is why direct candidates (IP or domain) can be freely tentative.

## 2 · The typed route model

signal-router wire vocabulary (pseudo-NOTA), keyed by the Criome host ID. Kind is
the record, reachability and locator are sums-with-data, selection is a method.
No name handle.

```
;; The Criome host a route reaches, and how to reach it. STORE KEY is the
;; Criome host ID (master public key), the fabric's primary identity.
HostRoute {
  criome_host_id CriomeHostId                    ;; STORE KEY: the master public key
  baseline YggdrasilBaseline                      ;; audited-hard, always-present fallback
  direct_candidates.(Vector DirectCandidate)      ;; preferred-when-reachable possible-routes
}

;; The Criome host ID: the master public key, the fabric's primary identity.
;; A BLS public-key string (signal-router already owns `PublicKey String`).
;; Recommended canonical type name; may repurpose RemoteRouterIdentity's payload
;; instead — the value is the pubkey either way (naming note below).
CriomeHostId String

;; The Yggdrasil endpoint: secure by construction when the Yggdrasil system is
;; operational. Audited-hard (§2.9.1 name<->address integrity check applies here).
;; Carries the literal socket address already lowered from the audited .criome
;; service name at config time.
YggdrasilBaseline { address TailnetAddress }        ;; a pre-resolved [ygg-v6]:port literal

;; A direct (non-Yggdrasil) possible-route: an IP address dialed directly, or a
;; domain name DNS-resolved as part of probing. Tentative-soft.
DirectCandidate {
  locator DirectLocator
  reachability Reachability
}

;; The direct locator kind — a closed sum, not a flag.
DirectLocator [
  (IpAddress IpSocketAddress)     ;; a literal [ip]:port — probe dials it directly
  (DomainName DomainSocketName)   ;; a domain:port — probe DNS-resolves, then dials
]

IpSocketAddress String            ;; a literal [ip]:port
DomainSocketName String           ;; a domain host + port; DNS-resolved during probing

Reachability [
  Unprobed                                        ;; seeded/learned, not yet proven reachable
  (Reachable ReachabilityObservation)             ;; last probe/push succeeded — selectable
  (Unreachable ReachabilityObservation)           ;; last probe/push failed — skip to baseline
]

ReachabilityObservation { observed_at TimestampNanos }
```

Selection is one method — an enum-vs-enum contact point:

```rust
impl HostRoute {
    /// The endpoint to dial right now: the first reachable direct candidate in
    /// preference order (an IP dialed directly, or a domain DNS-resolved then
    /// dialed), else the always-present Yggdrasil baseline.
    fn preferred_endpoint(&self) -> RouteEndpoint {
        self.direct_candidates
            .iter()
            .find(|candidate| candidate.reachability.is_reachable())
            .map(RouteEndpoint::direct)
            .unwrap_or_else(|| RouteEndpoint::yggdrasil(&self.baseline))
    }
}
```

Design notes:

- **Keyed purely on `criome_host_id`** — no name field. criome verifies by the
  Criome host ID (Slice A1), so the fabric carries no host name anywhere.
- **`DirectLocator` is a closed sum, not a flag.** IP vs domain is the variant;
  the domain variant's semantics (DNS resolution during probing) live in the
  probe, not in a boolean. A DNS-resolution failure resolves to
  `Reachability::Unreachable`.
- **`baseline` is required** — "a host with no route" is unrepresentable.
  Direct-only hosts are a design-for that turns `baseline` into a
  `PrimaryEndpoint [Yggdrasil | Direct]` sum — not now.
- **Naming (design-quality):** `CriomeHostId` reads as English and matches the
  psyche's approved term; a `RemoteRouterIdentity` newtype carrying a pubkey is a
  misleading name. Introducing `CriomeHostId` is the recommended beauty move. The
  `TailnetAddress` misnomer and the "router" name are bundled into the future
  anthropomorphic-rename proposition (§7).
- **Minimal-slice population:** `baseline` only (`direct_candidates` empty). The
  direct-candidate / locator / reachability machinery is shaped now, populated
  later (multi-IP + domain probing, §7).

## 3 · Durable family + schema-bump plan

Mirror the proven `router-outbound-backlog` pattern (`tables.rs` insert/remove/
records + `router.rs` persist/rehydrate).

**`router/src/tables.rs`:**

- Bump `ROUTER_SCHEMA_VERSION` `2 → 3` (`tables.rs:25`) — a coordinated
  storage-schema upgrade. The new family is additive; confirm the sema engine
  treats an added family on an existing `router.sema` as additive-safe. A fresh
  family rehydrates empty and falls back to the bootstrap seed (ships-dark, same
  posture as backlog / mirror switch).
- Add `const REMOTE_ROUTES: TableName = TableName::new("remote_routes");` and
  `const REMOTE_ROUTES_FAMILY: &str = "router-remote-route";`; add
  `remote_routes: TableReference<StoredHostRoute>` to `RouterStore`, register in
  `open`.
- Durable record, **keyed by the Criome host ID**, no name field (mirroring
  `StoredOutboundForward`, `tables.rs:567-595`):

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub struct StoredHostRoute {
    pub criome_host_id: CriomeHostId,
    pub baseline: YggdrasilBaseline,
    pub direct_candidates: Vec<DirectCandidate>,   // DirectLocator: IpAddress | DomainName
}

impl EngineRecord for StoredHostRoute {
    fn record_key(&self) -> RecordKey {
        RecordKey::new(self.criome_host_id.payload())   // the master public key is the key
    }
}
```

- Add the backlog-mirroring trio: `insert_host_route`, `remove_host_route`,
  `host_route_records()`.

**`router/src/remote_router.rs`:** the registry owns route state, so it owns its
durability.

- `peers: HashMap<String, TailnetAddress>` → `peers: HashMap<String, HostRoute>`
  keyed by the Criome host ID string; `resolve()` returns
  `HostRoute::preferred_endpoint()`.
- `homes: HashMap<ActorIdentifier, RemoteRouterIdentity>` → home value becomes the
  Criome host ID, so `resolve` walks recipient → host ID → route.
- Give the registry an `Option<RouterTables>` handle; persist on `register_peer`;
  rehydrate in `on_start` (`remote_router.rs:114-119`, today a no-op) from
  `host_route_records()`, failing safe to empty like `rehydrate_outbound_backlog`
  (`router.rs:2519-2540`).

**`router/src/router.rs`:** `install_remote_peer` (`router.rs:1408-1421`) already
routes registration to the registry and fires the drain push; persist happens
inside the registry. Thread the `RouterTables` handle in at construction.

**Seed boundary (name→Criome host ID):** CriomeOS/horizon and the bootstrap
document author which hosts exist by OS name and their routes; the router resolves
each peer's Criome host ID (from that peer's criome, out-of-band, or the founding
cohort commitment) and seeds `Criome host ID → route`. OS host identity stays
name-based; the fabric key is the pubkey. For the founding proof (Slice D), the
harness seeds pubkey-keyed routes directly.

**Wire (`signal-router/schema/lib.schema`):** add `CriomeHostId`,
`YggdrasilBaseline`, `DirectCandidate`, `DirectLocator`, `IpSocketAddress`,
`DomainSocketName`, `Reachability`, `ReachabilityObservation`; change the
peer-identity type on `RegisterRemoteRouter`, `RouterPeerAttestation.Signer`,
`RouterIdentityProof.ProofSigner`, `RemoteRoute.home` to the Criome host ID; add
the `SeedRemoteRoute` seed-record shape. One canonical asserted round-trip per new
type (contract-repo discipline). Versioned contract change.

The `homes` map stays bootstrap-seeded (owner-declared topology re-applied each
boot); only the route/address map is durable. Out of scope here.

## 4 · Criome-origination unstub approach

Replace the `RouterQuorumVoice::submit` stub (`criome/src/voice.rs:175-181`).
Identity-independent: this hand-off addresses the destination by `ActorIdentifier`
(the router destination actor), not by host identity.

`submit(destination, request)` must:

1. Frame the criome request — `Self::request_octets(request)` (`voice.rs:164-173`).
2. Wrap as `RoutedContractObject { contract_name: "signal-criome",
   contract_operation, contract_payload_size, payload_octets }`.
3. Wrap in `ForwardedMessagePayload { source_actor, destination_actor:
   destination, body: "", attachments: [], routed_objects: [object] }`.
4. `signal_router::Input::submit_routed_objects(payload).encode_signal_frame()`
   (`signal-router/src/schema/lib.rs:3136,3574`).
5. Dial `self.router_socket` with a small router working-socket client (a
   `RouterClient` twin of `CriomeClient`); send; `decode_signal_frame` the reply.
6. `RoutedObjectsAccepted` → `Ok(())`; `RoutedObjectsRefused` →
   `Err(Error::VoiceDelivery(<reason>))`. Conveyance stays fire-and-forget
   best-effort per the trait (`voice.rs:37-46`).

Only genuinely new code: the router working-socket client. No wire change for the
unstub — the contract exists.

## 5 · Non-silent production voice + peer-route config

Switch production off `SilentVoice` when routed-voice config is present (keep
`SilentVoice` the default for single-node / unconfigured hosts).

**`signal-criome/schema/lib.schema` — `CriomeDaemonConfiguration`** gains one
optional routed-voice record (typed-records-over-flags):

```
RouterVoiceConfiguration {
  router_socket_path DaemonPath
  source_actor ActorIdentifier
  peer_routes.(Vector PeerActorRoute)     ;; peer Identity -> router destination ActorIdentifier
}
CriomeDaemonConfiguration {
  ... existing fields ...
  router_voice.(Optional RouterVoiceConfiguration)
}
```

**`criome/src/daemon.rs`** — `from_configuration` (`daemon.rs:61-81`): when
`router_voice` is `Some`, construct `RouterQuorumVoice`; else `SilentVoice`.

**`CriomOS/modules/nixos/criome.nix`** — lower the peer routes + router socket;
ship the owner-driven founding tool in `packages.default` if the live proof drives
founding by CLI. (`signal-criome` is now free to edit — §8.)

## 6 · Vertical slice build plan (converged)

Each slice is an end-to-end, independently testable path. Bead-ready (no beads
filed this pass).

```
   A1 ──► A2 ──┐
 (pubkey-id    (durable pubkey-      ├──► D ──► E
  fabric,       keyed route store)   │   (proof) (re-bootstrap)
  send+verify)                       │
   B ──► C ─────────────────────────┘
```

No cycles. Validation (per-slice tests) precedes the proof (D). A1→A2 and B→C are
the two independent chains; both feed D. No fast-follow slices remain — the former
F1 (criome verify-by-key) is folded into A1; the former F2 (horizon pubkey
authoring) is dropped (OS hosts stay name-defined).

### Slice A1 — Fabric identity is the Criome host ID (send + verify, atomic)

- **Changes:** (router send-side) introduce `CriomeHostId` in `signal-router`;
  change `RegisterRemoteRouter`, `RouterPeerAttestation.Signer`,
  `RouterIdentityProof.ProofSigner`, `RemoteRoute.home` to carry it; `router`
  sources its own Criome host ID from co-resident criome via `ObserveNodePublicKey`
  and stamps the pubkey as the attestation/proof signer. (criome verify-side)
  criome verifies attestations/session proofs by the Criome host ID directly (a
  small extension of `member_by_key`, `root.rs:2082`), so the router carries **no
  host name** anywhere. Confirm whether verify-by-key is a criome-internal reverse
  index (no wire change) or needs a `signal-criome` verify surface; either is now
  unblocked.
- **Repos/crates:** `router`, `signal-router`, `criome`, `signal-criome`.
- **Test (proof):** the encrypted session handshake and a forward attestation
  round-trip with the Criome host ID as the signer identity and **no name in the
  verify path** — extend `router/tests/encrypted_peer_session.rs` and
  `router/tests/end_to_end_remote_forward.rs`. A stranger pubkey is refused
  fail-closed.
- **Depends on:** nothing.
- **Optional subdivision:** implementers who want thinner units may split A1 into
  a send-side step (with a temporary name projection) then a verify-by-key step
  that removes it; the folded form is recommended because it avoids the transient
  projection entirely.
- **Bead DoD:** "The router fabric's peer identity is the Criome host ID on the
  wire and in criome's verification; no host name appears in fabric routing,
  session proofs, or attestations; a stranger is refused fail-closed."

### Slice A2 — Durable pubkey-keyed route store

- **Changes:** §3 in full — schema `2→3`, `router-remote-route` family,
  `StoredHostRoute` keyed by the Criome host ID (no name field), registry
  `peers`→`HostRoute` and `homes` value → Criome host ID, persist-on-register +
  rehydrate-on-start; `DirectLocator` (IP/domain) in the record; `baseline`
  populated only.
- **Repos/crates:** `router`, `signal-router`.
- **Test (proof):** seed a `Criome host ID → route`, restart the store/registry,
  resolve the same host ID → same address without re-reading the tmpfs bootstrap.
- **Depends on:** A1 (uses the Criome host ID type).
- **Bead DoD:** "A seeded `Criome host ID → route` survives a daemon restart and
  resolves without re-applying the bootstrap document."

### Slice B — Criome origination unstub

- **Changes:** §4 — implement `RouterQuorumVoice::submit`; add the router
  working-socket client.
- **Repos/crates:** `criome` (after the dep-pin reconciliation, §8).
- **Test (proof):** `submit` against a stub/in-process router socket; carried
  octets round-trip to a decodable `CriomeRequest`; reply maps correctly. Extend
  `criome/tests/quorum_collection.rs` (`:475`).
- **Depends on:** nothing (router surface exists; identity-independent).
- **Bead DoD:** "A local criome hands a `FoundingConveyance` to its router via
  `SubmitRoutedObjects` and the router accepts it; the stub is gone."

### Slice C — Non-silent production voice + peer-route config

- **Changes:** §5 — `RouterVoiceConfiguration`; `from_configuration` selects
  `RouterQuorumVoice`; CriomOS lowering.
- **Repos/crates:** `signal-criome`, `criome`, `CriomOS`.
- **Test (proof):** configured host runs `RouterQuorumVoice` reaching its router
  socket; unconfigured runs `SilentVoice`; Nix eval/deploy check.
- **Depends on:** B.
- **Bead DoD:** "A deployed criome host with router-voice config runs
  `RouterQuorumVoice`, not `SilentVoice`."

### Slice D — Founding routed cross-node (the proof)

- **Changes:** integration harness only — two criome hosts, each with a
  `RouterQuorumVoice` to its local router; router A's pubkey-keyed store (A2)
  **seeded directly by the harness** with router B's Criome host ID → route and
  the destination-actor home. Owner initiates founding on node A over the meta
  socket; the Proposal conveys A→router A→router B→criome B; criome B accepts
  (owner-gated); the signature conveys back; the root founds on both. The
  founding-cohort check is already pubkey-aware (`member_by_key`, §0).
- **Repos/crates:** `criome` (tests), `router` (tests), a combined harness.
- **Test (proof):** the router-mediated analogue of
  `criome/tests/founding_conveyance.rs` — in-process twin over two real routers on
  loopback TCP first, then the live two-node SSH-driven run. Every fabric identity
  exercised is the Criome host ID.
- **Depends on:** A1 + A2 + C.
- **Bead DoD:** "Two Criome hosts on two nodes found a root over the router voice,
  keyed end-to-end on the Criome host ID."

### Slice E — Re-bootstrap from a single node + post-founding behavior test

- **Changes:** node B restarts; node A (up, routing, durable pubkey-keyed store)
  still holds B's last-known route by Criome host ID; an agent SSHes into node B
  and passes the owner-gated accept to B's meta socket; re-adoption completes; a
  post-founding behavior test confirms the root is live on both.
- **Repos/crates:** `criome`, `router`, `CriomOS` — operating-system-implementer
  territory.
- **Test (proof):** restart-then-refound behavior test; the durable store (A2) is
  what lets node A reach node B without re-seeding.
- **Depends on:** A2 + D.
- **Bead DoD:** "After a node restart, the founded root is re-established from a
  single up node using the durable last-known route."

**Design-for slices — NOT built now** (shape only, §2 and §7): populate
`direct_candidates` via multi-IP + **domain-name** exchange and safe-wire probing
(DNS-resolve domains during probing) and select direct over baseline; replace the
probe with push-notified IP up/down events; router awareness of Yggdrasil
operational status; the anthropomorphic rename of "router" (and
`CriomeHostId`/`TailnetAddress` naming cleanup). Runtime route *learning* (Fork 3)
is design-for unless the psyche pulls it forward.

## 7 · ARCHITECTURE proposals (ready-to-apply text — do not apply this pass)

Apply to `router/ARCHITECTURE.md` during implementation.

### 7a · New: the routing fabric direction (add near §2.9, ahead of §2.9.1)

```markdown
### 2.9.0 · Direction: a routing fabric keyed on the Criome host ID

The router is becoming a real routing fabric. Routers talk router-to-router, and
every co-resident component reaches any host through its local router — the router
is the single network chokepoint and the sole holder of the route table.

The fabric's primary identity is the Criome host ID: a Criome host's master public
key. It is the lookup key across the fabric — the route-table key, the session
handshake signer, and the forwarded-frame attestation signer, verified by criome
by that key directly. A Criome host is not the same as the OS host it runs on: the
OS host is name-defined (CriomOS/horizon), the Criome host is pubkey-defined
(this fabric). Where a name-defined OS host meets the pubkey-keyed fabric (route
seeding), the Criome host ID is resolved from that host's own criome; the OS layer
never authors pubkeys and the fabric never keys on names.

The route table is durable state, not a per-boot rebuild. A
`Criome host ID → route` mapping lives in the `router-remote-route` SEMA family,
seeded at bootstrap and by an owner-only meta operation, persisted on register,
rehydrated on start (mirroring the outbound-backlog pattern, §2.10). A last-known
route survives a restart, which is what lets a founded cluster re-bootstrap from a
single up node.

A route is a typed record. A Yggdrasil baseline — the audited-hard, always-present
fallback, secure by construction when the Yggdrasil system is operational — plus
zero or more direct candidates, each an IP address dialed directly or a domain
name DNS-resolved as part of probing, preferred when reachable because the
encrypted authenticated peer session (§2.10) already secures the wire. Selection
prefers a reachable direct candidate and falls back to the baseline. Selection is
a reachability decision, never a trust decision: the peer session authenticates the
Criome host ID by BLS over whatever wire was selected, fail-closed, so a stale or
wrong address is a reachability miss, not a breach.
```

### 7b · Reframe §2.9.1 and its invariants (`ARCHITECTURE.md:780-787`)

```markdown
The audited, fail-closed `.criome`→Yggdrasil binding applies to the Yggdrasil
baseline — the owner-seeded, audited-hard fallback route. It is an integrity check
on the seed (the configured service name must resolve to the literal Yggdrasil
socket address the daemon dials, fail-closed on mismatch), not a claim that a
host's address is immutable. Learned or probed direct candidates (IP or domain)
are tentative-soft and carry no such audit: they discover reachability at runtime
and cannot compromise anything, because identity is proven at the peer session by
the Criome host ID (§2.10), not at address selection. `.criome` answers where to
connect for the baseline; the peer session answers who spoke, keyed on the Criome
host ID, for every wire.
```

Invariant replacements:

```markdown
- The fabric's peer identity is the Criome host ID (the peer's Criome master
  public key), verified by criome by that key directly. Route resolution,
  session-handshake identity proofs, and forwarded-frame attestations are keyed on
  it; a host name is never a fabric lookup key. The Criome host (pubkey-defined) is
  distinct from the OS host it runs on (name-defined).
- The owner-seeded Yggdrasil baseline route may use a service-scoped `.criome`
  name only as an audited startup binding: the daemon dials the literal Yggdrasil
  socket address lowered from the managed archive, fail-closed if the audited
  service name does not resolve to that same address.
- Route selection is tentative and reachability-driven; a stale or wrong address
  is never a trust failure, because the peer session authenticates the peer's
  Criome host ID by BLS over the selected wire, fail-closed.
```

### 7c · New: future design propositions section (append near the end)

```markdown
## Future design propositions

Not built; recorded so the fabric's shape anticipates them.

- **Multi-IP and domain-name discovery with safe-wire probing.** Routers exchange
  candidate direct locators — IP addresses and domain names — and probe the
  encrypted peer session across them (DNS-resolving domains as part of probing),
  selecting a working direct route and falling back to the Yggdrasil baseline.
  Populates the `direct_candidates` layer.
- **Push-notified network awareness.** The router is push-notified of IP up/down
  events rather than polling reachability — the producer of interface state pushes;
  the router subscribes once and updates candidate reachability on the event.
  Replaces the interim probe. (Router awareness of Yggdrasil operational status is
  explicitly deferred.)
- **Router awareness of Yggdrasil operational status.** The router learns whether
  the Yggdrasil system (component, interface, route interceptions) is up. Deferred;
  the baseline is treated as available today.
- **Anthropomorphic rename of "router."** The name collides with the networking
  term now that the component owns a real routing table; it wants a unique,
  anthropomorphic name. The `TailnetAddress` (misnamed for Yggdrasil) and the new
  `CriomeHostId` type naming would be revisited alongside it.
```

## 8 · Coordination — post-rename baseline (accurate as of 2026-07-05)

**The drop-next mass-rename has landed on `main` in every in-scope repo.** All
repos carry their authoritative code on `main`; there are no active rename
worktrees to avoid, no off-limits checkouts, and no Orchestrate claims on any
in-scope repo. Build on clean post-rename `main`.

Current `main` tips observed: `router`, `signal-router`, `criome`,
`meta-signal-criome`, `meta-signal-router`, `signal-criome` (0.8.0, "append
founding-conveyance wire"), `CriomOS`, `lojix`, `horizon-rs`. Note the
`signal-criome` working copy in the canonical checkout sits **off** `main`;
implementers must build from the `main` bookmark, not the current working copy.

**Dependency-pin reconciliation — DO THIS FIRST.** The rename landed, but several
consumer `Cargo.toml` files still pin `branch = "drop-next"` and must be repinned
to `branch = "main"` (then verify the workspace resolves against post-rename
`main`):

| Repo | `Cargo.toml` deps still on `branch = "drop-next"` |
|---|---|
| **criome** | `meta-signal-criome` (L68), `signal-frame` (L72), `signal-criome` (L74), `signal-router` (L75), `triad-runtime` (L78) |
| **signal-criome** | `signal-frame` (L36), `schema-rust` (L40) |

`router`, `signal-router`, `meta-signal-criome`, `meta-signal-router` already pin
their upstreams at `branch = "main"`; their git URLs retain `-next` repo-name
suffixes (`nota-next.git`, `schema-rust-next.git`) with the crate `package`
un-suffixed — that is the settled post-rename shape (GitHub repo name vs crate
name), not a blocker. The criome-side `signal-router@drop-next` pin (L75) is the
exact one that gated the Slice B unstub earlier; repinning it to `main` clears it
and gives criome the `SubmitRoutedObjects` origination surface.

Other standing coordination:

- **Schema-version coordination:** confirm the sema engine's additive-family
  behavior on existing `router.sema` before landing A2's `2→3` bump.
- Slice A1 spans `router` + `signal-router` + `criome` + `signal-criome`; all are
  free to edit. Claim exact paths narrowly before editing per workspace
  discipline.

## 9 · Open questions / blockers for the psyche

The pubkey-primary sequencing question is **resolved** — with the rename done there
is no before-proof/fast-follow tradeoff: the Criome host ID is the identity
everywhere from Slice A1 (send + verify together, no name handle), and F2 is
dropped (OS hosts stay name-defined). Remaining:

1. **Fork 3 learning (decision):** build runtime route learning from the
   authenticated session now, or defer (design-for)? The minimal proof needs only
   owner-seeded durable routes.
2. **Founding operator tool:** the live proof (D/E) drives founding over the meta
   socket; no owner CLI ships in criome `packages.default` today (scout §2d). Raw
   meta-socket call or a shipped tool? Affects C/E scope.
3. **Homes-map durability (confirm):** the actor-home map stays bootstrap-seeded
   (owner topology, re-applied each boot); only the route/address map is durable.
   Confirm the split, or ask for both durable now.

## Audit recommendation

Substantial cross-repo work; a distinct auditor per surface:

- **rust-auditor** for A1 (the atomic pubkey-identity conversion, send + verify):
  evidence = the pubkey-keyed session/attestation round-trip tests with **no name
  in the verify path**, a fail-closed stranger-key test, and a design-quality read
  that no host name survives in fabric routing.
- **rust-auditor** for A2 + B (durable family + schema bump, registry refactor,
  criome unstub): evidence = the `router-remote-route` restart-rehydrate test, the
  `RouterQuorumVoice::submit` round-trip, `cargo test` output, and a
  design-quality read on the route model (special cases dissolved, `DirectLocator`
  is a closed sum not a flag, selection-as-method).
- **contract-repo review** for the `signal-router` and `signal-criome` schema
  changes: one canonical asserted round-trip per new type; no daemon runtime in the
  contract crate.
- **operating-system-implementer / nix-auditor** for C's CriomOS lowering and E's
  operational re-bootstrap: module eval/deploy checks and the restart-then-refound
  behavior test on real nodes.
- **architecture-editor review** of the §2.9.0 / §2.9.1 / future-propositions
  edits before they land.

Findings and corpus observations from these audits are provisional until the
psyche accepts them.
