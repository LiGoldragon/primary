# Criome Host Awareness — Build Design

A concrete, code-grounded build design for making the router a **routing fabric
with an actual routing table** whose **primary identity is the Criome host ID
(the master public key)**: a durable, updatable `Criome host ID → route` store,
the pubkey threaded as the fabric identity, criome origination unstubbed over the
router, and a live two-node founding-over-router proof. This is a design pass only
— no repository was edited, no claim taken, nothing committed.

Approved terminology, used exactly throughout:

- **Criome** = the cryptographic contract (the `Contract` type).
- **Criome host** = the daemon that runs and serves Criomes.
- **Criome host ID** = the host's Criome master public key (the value founding
  calls "node identity"). **This is the fabric's primary identity** (psyche
  decision, Fork 1).
- **Route** = the network locator (where to dial), owned by the router.

Ground truth verified against source at `/git/github.com/LiGoldragon/*` on
2026-07-05, building on
`agent-outputs/PersistentSpiritMirror/CriomeHostAwareness-CurrentStateScout.md`.

## 0 · Verification of the scout map

Every load-bearing scout claim was re-checked against current source and holds.
Refinements that matter to the build:

1. **The stub's named blocker is already resolved.**
   `RouterQuorumVoice::submit` errors with "waits for the clean signal-router
   routed-object constructor" (`criome/src/voice.rs:175-181`). That constructor
   now **exists**: `signal_router::Input::submit_routed_objects(payload)`
   (`signal-router/src/schema/lib.rs:3136`), with replies
   `RoutedObjectsAccepted`/`RoutedObjectsRefused` and the router-side handler
   `RouterRoot::apply_routed_object_submission` (`router/ARCHITECTURE.md:602-625`,
   §2.10). The criome unstub is **unblocked** at the router end.

2. **`signal-router` is self-contained** — no `signal-criome` dependency
   (`signal-router/Cargo.toml`), and it already owns a `PublicKey String` type in
   the attestation (`schema/lib.schema:136`). So converting the router-side fabric
   identity to the pubkey is entirely within `router` + `signal-router`, both
   clean and on `main` — no `signal-criome` edit required for the router-side
   conversion. This is the hinge of the clean sequencing (§1.5).

3. **The router can source its own Criome host ID from its co-resident criome.**
   criome exposes `ObserveNodePublicKey → NodePublicKey { public_key }`
   (`signal-criome/schema/lib.schema:36,68,270`). So a router learns its own
   pubkey identity at startup from the local criome rather than needing it
   hand-authored.

4. **Founding already resolves members by key.** `founding.member_by_key(...)`
   (`criome/src/actors/root.rs:2082`) and the RootGenesis anchor commit to the
   cohort's public keys (`criome/src/founding.rs`). The founding-cohort check is
   inherently pubkey-aware today, which is why the criome *attestation-registry*
   conversion (name→key lookup → pubkey-primary) is a genuine fast-follow and not
   a blocker for the founding proof (§1.5, §6).

5. **A dependency-pin reconciliation is required (Slice B).**
   `criome/Cargo.toml:75` pins `signal-router = { branch = "drop-next" }`, but the
   `SubmitRoutedObjects` origination surface is on signal-router `main`
   (`drop-next` stale, scout §6). The criome implementer must build against a
   signal-router revision carrying it.

Confirmed exactly as scouted: the in-memory `RemoteRouterRegistry`
(`router/src/remote_router.rs:30-68`); `ROUTER_SCHEMA_VERSION = 2` and the seven
families (`router/src/tables.rs:25-39`); production `SilentVoice`
(`criome/src/daemon.rs:56,78`); `CriomeDaemonConfiguration` carries no
peer/router fields (`signal-criome/schema/lib.schema:140-146`); the
durable-backlog persist/rehydrate pattern (`tables.rs` +
`router.rs:2501-2540`, rehydrated in `on_start` at `router.rs:3501`); §2.9.1's
fail-closed Yggdrasil audit (`router/ARCHITECTURE.md:552-591`, invariants
`:780-787`); and the criome↔router identity binding — a node signs as its
`Host(<name>)` identity, equal to its `router_identity`, resolved to the
registered master key by criome (`router/src/criome_attestation.rs:27-34,90-101`).
The route-registration seam `RouterRuntime::install_remote_peer`
(`router/src/router.rs:1408-1421`) already fires a backlog-drain push; the durable
persist attaches there.

## 1 · Design forks resolved

### Fork 1 — Route-store key and fabric identity: DECIDED (pubkey-primary)

**Psyche decision: the Criome host ID (master public key) is the fabric's primary
identity, effective now.** The raw master pubkey is the lookup key across the
fabric — the route-store key, the registry home value, the session-handshake
signer, and the forward-attestation signer — not a name handle. The name is
demoted to, at most, a transitional projection handle at the one boundary where
criome still verifies by name (§1.5), and is removed when that boundary converts.

Consequences threaded through this design:

- The route store is keyed by the Criome host ID (pubkey), §2/§3.
- `RemoteRouterIdentity` (signal-router) carries the pubkey value; the recommended
  beauty move is to introduce the canonical type `CriomeHostId` (the psyche's
  exact term) — see naming note in §2. The value is the pubkey either way.
- The session-handshake `ProofSigner` and forward-attestation `Signer` become the
  Criome host ID, §6 Slice A1.
- criome's attestation registry becomes pubkey-primary (verify-by-key), §6 Slice
  F1 — a fast-follow, for the reasons in §1.5.
- Horizon/CriomOS authoring seeds routes by Criome host ID, §6 Slice F2 — a
  fast-follow.

The security reasoning stands unchanged and is now even more direct: the name was
never a security token, and with the pubkey primary the router's fabric identity
*is* the verified key. A stranger still fails the session handshake fail-closed
(`UnknownSigner`); a stale or wrong address is still only a reachability miss
(§1.4).

### Fork 2 — Typed route model

**A closed typed record, no flag soup. Address *kind* is the enclosing record
(Yggdrasil baseline vs direct candidate), reachability is a sum-with-data, and
selection is a method — an enum-vs-enum contact point.** Full model in §2. The
store key is the Criome host ID.

The key structural fact that dissolves the special cases: **address kind is not a
security tag.** Both a Yggdrasil endpoint and a direct endpoint carry the *same*
end-to-end security — the PeerSession handshake authenticates by the Criome host
ID and encrypts regardless of the wire (§1.4). A route carries **reachability and
redundancy** distinctions, not trust:

- The **Yggdrasil baseline** — audited-hard, always-present fallback,
  secure-by-construction when the Yggdrasil system is operational.
- **Direct candidates** — preferred when reachable, because the PeerSession
  already secures the wire, making the Yggdrasil transport layer redundant
  overhead (plus restart/latency risk). Tentative for reachability, never less
  secure.

### Fork 3 — Route-update authority

**Near-term: owner-seeded and durable. Design-for: learned-from-authenticated-session,
gated on the fail-closed identity proof and carried by an existing push event.**

- **Seed (audited-hard):** owner-authored — the existing bootstrap document and a
  new owner-only `meta-signal-router` operation `SeedRemoteRoute` mirroring
  `SetMirrorEnabled` (0600 meta socket, persisted). Writes the Yggdrasil baseline;
  the only path that creates or replaces it.
- **Learn (tentative-soft, design-for):** when a peer completes the PeerSession
  handshake — proving its Criome host ID by BLS, fail-closed on a stranger — the
  router MAY record the observed source address as that peer's direct candidate
  (`Reachability::Reachable`, stamped at session-established time). Consistent with
  owner-gated / no-auto-approval: no new host is ever auto-admitted (a stranger
  fails the handshake); only a known, proven host's reachability hint is refreshed.
  Push, not poll: the existing `PeerSessionEstablished { peer, epoch }` event
  (`router/ARCHITECTURE.md:666-670`) is the hook. Learning updates only the
  tentative direct-candidate layer, never the audited baseline.

Near-term, durability of the seeded route delivers "last known route survives
restart" (satisfies re-bootstrap, Slice E). Learning is the fuller reading of the
psyche's "last known route." **Open for psyche (see §9):** build learning now or
defer.

### Fork 4 — §2.9.1 reconciliation

**Keep the fail-closed audit; reframe it as an integrity check on the *Yggdrasil
baseline* seed, cleanly separate from tentative direct-candidate selection.
Security lives at the PeerSession layer, not at address selection — the code
already names the two separately: "`.criome` answers where to connect; criome
answers who spoke" (`router/ARCHITECTURE.md:590-591`).**

- **Address selection is uniformly tentative** and reachability-driven. A stale or
  wrong address is never a security failure: the wrong host fails the PeerSession
  identity proof (fail-closed) and no traffic flows.
- **Identity verification is uniformly fail-closed** at the session layer, keyed
  now on the Criome host ID, independent of which address was dialed.

§2.9.1's audit is repositioned, not weakened: an integrity check on the
audited-hard Yggdrasil baseline (owner-seeded fallback). Learned/probed direct
candidates are tentative-soft and carry no such audit. ARCHITECTURE text in §7.

## 1.4 · Why direct IPs are not less secure (load-bearing insight)

The encrypted, mutually-authenticated PeerSession (§2.10,
`router/ARCHITECTURE.md:627-665`) authenticates the peer by its Criome host ID
(BLS) and encrypts every forward (ChaCha20-Poly1305 over X25519 ECDH) — over
whatever wire the route selected. So a Yggdrasil address adds a redundant second
transport-crypto layer (the reliable baseline), while a direct IP relies solely on
the PeerSession, which is already sufficient. The trust boundary is the handshake,
not the address — which is why direct candidates can be freely tentative.

## 1.5 · Pubkey-primary sequencing: before-proof vs fast-follow

The pubkey-primary conversion touches six surfaces. They split cleanly by repo
cleanliness and by whether the founding proof (Slice D) exercises them, giving a
sequencing where **everything that must be pubkey-primary before the proof lives
in clean repos (`router` + `signal-router`), and the two surfaces that would
collide with the in-flight drop-next rename are exactly the two that can
fast-follow.**

| Fabric surface | Repo(s) | Rename-entangled? | When |
|---|---|---|---|
| Route store key + typed model | `router`, `signal-router` | No (clean, on `main`) | **Before proof** (A2) |
| Registry home-value + `CriomeHostId` type | `router`, `signal-router` | No | **Before proof** (A1) |
| Session-handshake `ProofSigner` = pubkey | `router`, `signal-router` | No | **Before proof** (A1) |
| Forward-attestation `Signer` = pubkey | `router`, `signal-router` | No | **Before proof** (A1) |
| criome attestation registry (verify-by-key) | `criome`, `signal-criome` | **Yes** (`signal-criome` dirty rename edit, off-limits) | **Fast-follow** (F1) |
| Horizon / CriomOS route authoring by pubkey | `CriomOS` | **Yes** (`worker20-criomos-drop-next` active) | **Fast-follow** (F2) |

**The projection that makes fast-follow honest.** Before F1, criome still verifies
attestations by `Identity::host(name)` (`criome_attestation.rs:90-101`). The router
holds the peer's name co-committed in its own pubkey-keyed route record (a 1:1
binding it already has), and its criome-verify/sign boundary
(`router/src/criome_attestation.rs`, router repo, clean) projects
`Criome host ID → name` there, calling criome's existing name-based `Sign` /
`VerifyAttestation` unchanged. The router's *own* Criome host ID comes from its
co-resident criome via `ObserveNodePublicKey`; its own name comes from config for
the sign projection. So:

- **Every wire-visible fabric identity and every lookup key is the Criome host ID
  from the start** — route store, registry, session signer, attestation signer.
- **Only criome's private registry index lags by one slice**, behind a thin,
  clean, router-side projection handle that is deleted the moment F1 lands
  (criome verifies by explicit key, the founding path already does via
  `member_by_key`).

**Clean-vs-tradeoff:** a clean sequencing exists and is recommended, but it
**deliberately fast-follows two surfaces the psyche named** (criome registry,
horizon authoring) because converting them *before* the proof would edit
off-limits `signal-criome` mid-rename and the active CriomOS drop-next worktree,
and would delay the proof for surfaces the proof can exercise through the router
harness. This is a real sequencing choice, laid out for the psyche in §9.

## 2 · The typed route model

signal-router wire vocabulary (pseudo-NOTA), keyed by the Criome host ID. The kind
is the record, reachability is a sum-with-data, selection is a method.

```
;; The Criome host a route reaches, and how to reach it. STORE KEY is the
;; Criome host ID (master public key), the fabric's primary identity.
HostRoute {
  criome_host_id CriomeHostId                   ;; STORE KEY: the master public key
  registered_name.(Optional RemoteRouterIdentity) ;; transitional criome-verify handle;
                                                  ;; removed when criome verifies by key (F1)
  baseline YggdrasilBaseline                     ;; audited-hard, always-present fallback
  direct_candidates.(Vector DirectCandidate)     ;; preferred-when-reachable direct wires
}

;; The Criome host ID: the master public key, the fabric's primary identity.
;; A BLS public-key string (signal-router already owns `PublicKey String`).
;; Recommended new canonical type name; may repurpose RemoteRouterIdentity's
;; payload instead — the value is the pubkey either way.
CriomeHostId String

;; The Yggdrasil endpoint: secure by construction when the Yggdrasil system is
;; operational. Audited-hard (§2.9.1 name<->address integrity check applies here).
YggdrasilBaseline {
  address TailnetAddress                         ;; a [ygg-v6]:port literal (existing type)
}

;; A candidate direct (non-Yggdrasil) wire, preferred when its last probe
;; succeeded — the PeerSession already secures the wire. Tentative-soft.
DirectCandidate {
  address TailnetAddress
  reachability Reachability
}

Reachability [
  Unprobed                                       ;; seeded/learned, not yet proven reachable
  (Reachable ReachabilityObservation)            ;; last probe/push succeeded — selectable
  (Unreachable ReachabilityObservation)          ;; last probe/push failed — skip to baseline
]

ReachabilityObservation { observed_at TimestampNanos }
```

Selection is one method — an enum-vs-enum contact point, not scattered branches:

```rust
impl HostRoute {
    /// The endpoint to dial right now: the first reachable direct candidate in
    /// preference order, else the always-present Yggdrasil baseline.
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

- **`criome_host_id` is the key; `registered_name` is a transitional handle.**
  Under pubkey-primary the store keys on the master public key. `registered_name`
  is the 1:1 name the router hands criome's name-based verify/sign until F1, then
  it is removed (`Option`, so its removal is a field deletion, not a schema
  scramble).
- **`baseline` is required**, so "a host with no route" is unrepresentable.
  Direct-only hosts are a design-for that turns `baseline` into a
  `PrimaryEndpoint [Yggdrasil | Direct]` sum — not now.
- **Naming (design-quality):** `CriomeHostId` as the canonical type reads as
  English and matches the psyche's approved term; a `RemoteRouterIdentity` newtype
  now carrying a pubkey is a misleading name. Introducing `CriomeHostId` is the
  recommended beauty move; the `TailnetAddress` misnomer and the "router" name are
  bundled into the future anthropomorphic-rename proposition (§7), not touched now.
- **Minimal-slice population:** `baseline` only (`direct_candidates` empty). The
  direct-candidate/reachability machinery is shaped now, populated later
  (multi-IP probing, §7).

## 3 · Durable family + schema-bump plan

Mirror the proven `router-outbound-backlog` pattern (`tables.rs` insert/remove/
records + `router.rs` persist/rehydrate).

**`router/src/tables.rs`:**

- Bump `ROUTER_SCHEMA_VERSION` `2 → 3` (`tables.rs:25`) — a coordinated
  storage-schema upgrade, not a refactor. The new family is additive; confirm the
  sema engine treats an added family on an existing `router.sema` as
  additive-safe. A fresh family rehydrates empty and falls back to the bootstrap
  seed (ships-dark, same posture as backlog / mirror switch).
- Add `const REMOTE_ROUTES: TableName = TableName::new("remote_routes");` and
  `const REMOTE_ROUTES_FAMILY: &str = "router-remote-route";`; add
  `remote_routes: TableReference<StoredHostRoute>` to `RouterStore`, register in
  `open`.
- Durable record, **keyed by the Criome host ID** (mirroring `StoredOutboundForward`,
  `tables.rs:567-595`):

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
pub struct StoredHostRoute {
    pub criome_host_id: CriomeHostId,
    pub registered_name: Option<RemoteRouterIdentity>,  // transitional, dropped at F1
    pub baseline: YggdrasilBaseline,
    pub direct_candidates: Vec<DirectCandidate>,
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
durability (verb-belongs-to-noun).

- `peers: HashMap<String, TailnetAddress>` → `peers: HashMap<String, HostRoute>`
  keyed by the Criome host ID string; `resolve()` returns
  `HostRoute::preferred_endpoint()`.
- `homes: HashMap<ActorIdentifier, RemoteRouterIdentity>` → the home value becomes
  the Criome host ID (`CriomeHostId`), so `resolve` walks recipient → host ID →
  route.
- Give the registry an `Option<RouterTables>` handle; persist on `register_peer`;
  rehydrate in `on_start` (`remote_router.rs:114-119`, today a no-op) from
  `host_route_records()`, failing safe to empty like
  `rehydrate_outbound_backlog` (`router.rs:2519-2540`).

**`router/src/router.rs`:** `install_remote_peer` (`router.rs:1408-1421`) already
routes registration to the registry and fires the drain push; the persist happens
inside the registry. Thread the `RouterTables` handle in at construction.

**Wire (`signal-router/schema/lib.schema`):** add `CriomeHostId`,
`YggdrasilBaseline`, `DirectCandidate`, `Reachability`, `ReachabilityObservation`;
change the peer-identity type carried by `RegisterRemoteRouter`,
`RouterPeerAttestation.Signer`, `RouterIdentityProof.ProofSigner`, and
`RemoteRoute.home` to the Criome host ID; add the seed-record shape for
`SeedRemoteRoute`. One canonical asserted round-trip per new type (contract-repo
discipline). Versioned contract change.

The `homes` map stays bootstrap-seeded (owner-declared topology re-applied each
boot); only the route/address map is durable. Runtime actor-home learning, if
later added, gets the same durable family. Out of scope here.

## 4 · Criome-origination unstub approach

Replace the `RouterQuorumVoice::submit` stub (`criome/src/voice.rs:175-181`). The
router surface it needs already exists (§0). Unaffected by the pubkey-primary
change: this hand-off addresses the destination by `ActorIdentifier` (the router
destination actor), not by host identity.

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
optional routed-voice record (typed-records-over-flags: the "yes" branch carries
the router socket, this host's source actor, and the peer routes):

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
founding by CLI.

Note: this slice edits `signal-criome`, which is off-limits during the rename
(scout §6). Coordinate or stage against a clean `signal-criome` checkout once the
rename lands. The `peer_routes` here address peers by criome `Identity` (name)
inside the config; the router-level destination is an `ActorIdentifier`, so this
slice is independent of the pubkey-primary fabric identity change.

## 6 · Vertical slice build plan (re-scoped for pubkey-primary)

Each slice is an end-to-end, independently testable path. Bead-ready (no beads
filed this pass).

```
   A1 ──► A2 ──┐
 (pubkey-id   (durable pubkey-
  fabric)      keyed route store)
               ├──► D ──► E
   B ──► C ────┘   (proof)  (re-bootstrap)
                   │
                   ├──► F1 (criome registry verify-by-key; drop projection handle)
                   └──► F2 (horizon/CriomOS pubkey authoring)
```

No cycles. Validation (per-slice tests) precedes the proof (D). A1→A2 and B→C are
the two independent chains; both feed D. F1/F2 are the fast-follows that complete
the pubkey-primary conversion of the two rename-entangled surfaces.

### Slice A1 — Fabric peer identity becomes the Criome host ID

- **Changes:** introduce `CriomeHostId` (or repurpose `RemoteRouterIdentity`'s
  payload) in `signal-router`; change `RegisterRemoteRouter`,
  `RouterPeerAttestation.Signer`, `RouterIdentityProof.ProofSigner`, and
  `RemoteRoute.home` to carry it. In `router`, source the daemon's own Criome host
  ID from its co-resident criome via `ObserveNodePublicKey`; keep the thin
  `Criome host ID ↔ name` projection at the criome-verify/sign boundary
  (`router/src/criome_attestation.rs`) so criome's existing name-based `Sign` /
  `VerifyAttestation` is called unchanged (transitional, removed at F1).
- **Repos/crates:** `router`, `signal-router` (both clean, on `main`).
- **Test (proof):** the encrypted session handshake and a forward attestation
  round-trip with the Criome host ID as the signer identity — extend
  `router/tests/encrypted_peer_session.rs` and
  `router/tests/end_to_end_remote_forward.rs`. An unregistered pubkey is refused
  fail-closed.
- **Depends on:** nothing.
- **Bead DoD:** "The router fabric's peer identity is the Criome host ID
  everywhere on the wire (register, session proof, attestation), verified
  fail-closed; a thin name projection remains only at the criome boundary."

### Slice A2 — Durable pubkey-keyed route store

- **Changes:** §3 in full — schema `2→3`, `router-remote-route` family,
  `StoredHostRoute` keyed by the Criome host ID, registry `peers`→`HostRoute` and
  `homes` value → Criome host ID, persist-on-register + rehydrate-on-start;
  co-commit `registered_name` as the transitional criome-verify handle;
  `baseline` populated only.
- **Repos/crates:** `router`, `signal-router`.
- **Test (proof):** seed a `Criome host ID → route`, restart the store/registry,
  resolve the same host ID → same address without re-reading the tmpfs bootstrap.
- **Depends on:** A1 (uses the Criome host ID type).
- **Bead DoD:** "A seeded `Criome host ID → route` survives a daemon restart and
  resolves without re-applying the bootstrap document."

### Slice B — Criome origination unstub

- **Changes:** §4 — implement `RouterQuorumVoice::submit`; add the router
  working-socket client.
- **Repos/crates:** `criome`; reconcile the `signal-router` dependency pin (§8).
- **Test (proof):** `submit` against a stub/in-process router socket; the carried
  octets round-trip to a decodable `CriomeRequest` and the reply maps correctly.
  Extend `criome/tests/quorum_collection.rs` (`:475`).
- **Depends on:** nothing (router surface exists; identity-independent).
- **Bead DoD:** "A local criome hands a `FoundingConveyance` to its router via
  `SubmitRoutedObjects` and the router accepts it; the stub is gone."

### Slice C — Non-silent production voice + peer-route config

- **Changes:** §5 — `RouterVoiceConfiguration`; `from_configuration` selects
  `RouterQuorumVoice`; CriomOS lowering.
- **Repos/crates:** `signal-criome` (schema — coordinate with rename, §8),
  `criome`, `CriomOS`.
- **Test (proof):** configured host runs `RouterQuorumVoice` reaching its router
  socket; unconfigured runs `SilentVoice`; Nix eval/deploy check.
- **Depends on:** B.
- **Bead DoD:** "A deployed criome host with router-voice config runs
  `RouterQuorumVoice`, not `SilentVoice`."

### Slice D — Founding routed cross-node (the proof)

- **Changes:** integration harness only — two criome hosts, each with a
  `RouterQuorumVoice` to its local router; router A's pubkey-keyed store (A2)
  **seeded directly by the harness** with router B's Criome host ID → route and
  the destination-actor home (no horizon nix needed yet — that is F2). Owner
  initiates founding on node A over the meta socket; the Proposal conveys
  A→router A→router B→criome B; criome B accepts (owner-gated); the signature
  conveys back; the root founds on both. The founding-cohort check is already
  pubkey-aware (`member_by_key`, §0).
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

### Slice F1 — criome attestation registry becomes verify-by-key (fast-follow)

- **Changes:** criome gains a `Criome host ID → registration` reverse index and a
  verify-/sign-by-explicit-key path (the founding path already resolves by key via
  `member_by_key`, `root.rs:2082`); the router drops the transitional
  `Criome host ID → name` projection and the `registered_name` handle from the
  route record.
- **Repos/crates:** `criome`, `signal-criome` (**rename-entangled — off-limits
  until the drop-next rename settles**, §8).
- **Test (proof):** attestation/session verify succeeds against an explicit Criome
  host ID with no name in the path; a stranger key is refused fail-closed.
- **Depends on:** D (proven behavior to preserve) — the reverse-index change is
  validated against the working proof.
- **Bead DoD:** "criome verifies fabric attestations and session proofs by the
  Criome host ID directly; the router carries no name handle."

### Slice F2 — Horizon / CriomOS route authoring by Criome host ID (fast-follow)

- **Changes:** `CriomOS/modules/nixos/persona-router.nix` authors peer routes and
  the router's own identity by Criome host ID (pubkey) rather than hostname; the
  pubkey is projected from horizon/criome rather than `config.networking.hostName`.
- **Repos/crates:** `CriomOS` (**rename-entangled — `worker20-criomos-drop-next`
  active**, §8).
- **Test (proof):** a deployed two-node config seeds pubkey-keyed routes; the
  live founding path (D/E) runs from production config, not just the harness seed.
- **Depends on:** A2 + D.
- **Bead DoD:** "Production route seeding authors `Criome host ID → route`; the
  live proof runs from deployed config."

**Design-for slices — NOT built now** (shape only, §2 and §7): populate
`direct_candidates` via multi-IP exchange + safe-wire probing and select direct
over baseline; replace the probe with push-notified IP up/down events; router
awareness of Yggdrasil operational status; the anthropomorphic rename of "router"
(and `CriomeHostId`/`TailnetAddress` naming cleanup). Runtime route *learning*
(Fork 3) is design-for unless the psyche pulls it forward.

## 7 · ARCHITECTURE proposals (ready-to-apply text — do not apply this pass)

Apply to `router/ARCHITECTURE.md` during implementation.

### 7a · New: the routing fabric direction (add near §2.9, ahead of §2.9.1)

```markdown
### 2.9.0 · Direction: a routing fabric keyed on the Criome host ID

The router is becoming a real routing fabric. Routers talk router-to-router, and
every co-resident component reaches any host through its local router — the router
is the single network chokepoint and the sole holder of the route table.

The fabric's primary identity is the Criome host ID: a host's Criome master public
key. It is the lookup key across the fabric — the route-table key, the session
handshake signer, and the forwarded-frame attestation signer. A host name is not a
fabric identity; where a name still appears (criome's local registry), it is
resolved from the Criome host ID, not the other way round.

The route table is durable state, not a per-boot rebuild. A
`Criome host ID → route` mapping lives in the `router-remote-route` SEMA family,
seeded at bootstrap and by an owner-only meta operation, persisted on register,
and rehydrated on start, mirroring the outbound-backlog pattern (§2.10). A
last-known route therefore survives a restart, which is what lets a founded
cluster re-bootstrap from a single up node.

A route is a typed record, not an address string: a Yggdrasil baseline — the
audited-hard, always-present fallback, secure by construction when the Yggdrasil
system is operational — and zero or more direct candidates, preferred when
reachable because the encrypted authenticated peer session (§2.10) already secures
the wire, making the Yggdrasil transport layer redundant. Selection prefers a
reachable direct candidate and falls back to the baseline. Selection is a
reachability decision, never a trust decision: the peer session authenticates the
Criome host ID by BLS over whatever wire was selected, fail-closed, so a stale or
wrong address is a reachability miss, not a breach.
```

### 7b · Reframe §2.9.1 and its invariants (`ARCHITECTURE.md:780-787`)

```markdown
The audited, fail-closed `.criome`→Yggdrasil binding applies to the Yggdrasil
baseline — the owner-seeded, audited-hard fallback route. It is an integrity check
on the seed (the configured service name must resolve to the literal Yggdrasil
socket address the daemon dials, fail-closed on mismatch), not a claim that a
host's address is immutable. Learned or probed direct candidates are tentative-soft
and carry no such audit: they discover reachability at runtime and cannot
compromise anything, because identity is proven at the peer session by the Criome
host ID (§2.10), not at address selection. `.criome` answers where to connect for
the baseline; the peer session answers who spoke, keyed on the Criome host ID, for
every wire.
```

Invariant replacements:

```markdown
- The fabric's peer identity is the Criome host ID (the peer's Criome master
  public key). Route resolution, session-handshake identity proofs, and
  forwarded-frame attestations are keyed on it; a host name is never a fabric
  lookup key.
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

- **Multi-IP discovery and safe-wire probing.** Routers exchange candidate direct
  IP lists and probe the encrypted peer session across them, selecting a working
  direct route and falling back to the Yggdrasil baseline. Populates the
  `direct_candidates` layer.
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
  `CriomeHostId` type naming would be revisited alongside it. A future rename.
```

## 8 · Coordination

- **Build against `main`** for the seam repos (router, signal-router,
  meta-signal-criome, meta-signal-router): authoritative code is on `main`;
  `drop-next` branches are stale (scout §6). The **before-proof identity + store
  work (A1, A2) is entirely in `router` + `signal-router`, both clean** — no
  rename entanglement.
- **The two rename-entangled surfaces are both fast-follows, by design.** F1 edits
  `signal-criome` (dirty rename edit, **off-limits** now) — defer until the
  drop-next rename settles, or stage against a clean checkout. F2 edits `CriomOS`
  (`worker20-criomos-drop-next` active) — defer likewise. Slice C also touches
  `signal-criome` and must coordinate the same way; the founding proof (D) does not
  need C's production config if the harness wires the voice directly, so C can
  itself trail D's in-process twin if the rename blocks it.
- **Dependency-pin reconciliation (Slice B):** `criome/Cargo.toml:75` pins
  `signal-router = { branch = "drop-next" }`; the `SubmitRoutedObjects` surface is
  on signal-router `main`. Build criome against a revision carrying it; expect
  `-next → *` crate-name churn at land time.
- **No Orchestrate claims** on any in-scope repo; workers claim narrowly before
  editing. Avoid the active rename worktrees.
- **Schema-version coordination:** confirm the sema engine's additive-family
  behavior on existing `router.sema` before landing A2's `2→3` bump.

## 9 · Open questions / blockers for the psyche

1. **Pubkey-primary sequencing (the one to put to him, §1.5):** the recommended
   plan makes the Criome host ID the primary identity at every wire-visible fabric
   surface and every lookup key *before* the proof (route store, session signer,
   attestation signer — all in clean repos), and **fast-follows two surfaces he
   named** — criome's registry verify-by-key (F1) and horizon authoring (F2) —
   because converting them before the proof would edit off-limits `signal-criome`
   mid-rename and the active CriomOS drop-next worktree, and would delay the proof
   for surfaces the router harness can already exercise.
   - **Recommendation: accept the fast-follow.** The pubkey is genuinely the
     identity from the start; only criome's private registry index lags by one
     slice, behind a thin clean router-side projection that F1 deletes.
   - **The alternative** (convert F1/F2 fully before the proof) pays the
     signal-criome/CriomOS rename collision and delays the proof, for a surface
     that is not wire-visible. Not recommended.
   - His call: accept the recommended sequencing, or require fully-before-proof.
2. **Fork 3 learning (decision):** build runtime route learning from the
   authenticated session now, or defer (design-for)? The minimal proof needs only
   owner-seeded durable routes.
3. **Founding operator tool:** the live proof (D/E) drives founding over the meta
   socket; no owner CLI ships in criome `packages.default` today (scout §2d).
   Raw meta-socket call or a shipped tool? Affects C/E scope.
4. **Homes-map durability (confirm):** the actor-home map stays bootstrap-seeded
   (owner topology, re-applied each boot); only the route/address map is durable.
   Confirm the split, or ask for both durable now.

## Audit recommendation

Substantial cross-repo work; a distinct auditor per surface:

- **rust-auditor** for A1, A2, B (the pubkey-identity conversion, durable family +
  schema bump, registry refactor, criome unstub): evidence = the pubkey-keyed
  session/attestation round-trip tests, the `router-remote-route`
  restart-rehydrate test, the `RouterQuorumVoice::submit` round-trip, `cargo test`
  output, and a design-quality read on the route model (special cases dissolved,
  no flag soup, selection-as-method, `CriomeHostId` naming).
- **contract-repo review** for the `signal-router` (and later `signal-criome`)
  schema changes: one canonical asserted round-trip per new type; no daemon
  runtime in the contract crate.
- **rust-auditor** again for F1 specifically (verify-by-key, projection-handle
  removal): evidence = fail-closed stranger-key test and the name-free verify path.
- **nix-auditor / operating-system-implementer** for C's and F2's CriomOS lowering
  and E's operational re-bootstrap: module eval/deploy checks and the
  restart-then-refound behavior test on real nodes.
- **architecture-editor review** of the §2.9.0 / §2.9.1 / future-propositions
  edits before they land.

Findings and corpus observations from these audits are provisional until the
psyche accepts them.
