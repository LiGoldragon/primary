# 136 — The router: vision, and how to test it end-to-end on real networking

*The psyche asked for my vision for the router and — especially — how to test it
e2e with real networking. This is both. The test strategy is the larger half,
because "real networking" is precisely where green tests lie. Method: a grounded
design workflow (the actual router test + deploy surface, two independent e2e
architectures) plus an adversarial real-networking critic that verified every
claim against source and caught the masquerades; I hold the synthesis. Builds on
reports 120/121/133/134/135.*

## Part I — Vision

### 1. What the router is

The router is the **transport and object-distribution fabric of Telos's
agreement machine** — the third step of the `spirit → criome → router → mirror`
chain ([`d6he`]). criome decides *may this propagate* and stamps the object; the
router *carries the fact*; the mirror *moves the bytes*. The router is the
propagation spine: when criome admits an object, the router matches who cares and
fans out a **reference**, and the interested component fetches the bytes by
digest. It is small, payload-blind, and authentication-bearing-but-not-
authenticating: it carries the proof, criome makes the verdict.

### 2. The invariants it holds (all anchored)

- **Payload-blind** ([`57f9`]): the router envelope carries routing + object
  metadata for a serialized rkyv payload; the router reads the envelope, hashes
  the octets, routes, authenticates, delivers — it never decodes the inner
  contract payload.
- **References, not payloads** ([`m0p2`]): the pulse pushes a digest; the
  component fetches the rkyv object through the object-distribution layer. The
  heavy bytes never travel the pulse.
- **criome stamps, the router fans out** ([`l2ha`]): criome stamps + authorizes;
  the **router** matches subscriptions and fans references to interested
  subscribers. criome holds no fan-out duty ([`wckt`]: criome auth-only, moves
  nothing).
- **Cross-host, BLS-in-frame replaces `SO_PEERCRED`.** The kernel proves the
  *local* caller; across hosts that proof is gone, so a criome BLS attestation
  chained to the cluster-root travels **in-frame** and is the *only* principal
  proof on the wire.
- **Tailnet-transparent encryption.** Plain TCP over the `ln`/Yggdrasil mesh
  (`ln.goldragon.criome`): the fabric encrypts the link, BLS authenticates the
  principal *and* the content. The router is transport-agnostic
  (`triad_runtime::TcpListenerDaemon` "does not know what a tailnet is").
- **Loop-guarded** (`ForwardMarker [Origin Forwarded]`) and **replay-windowed**
  (a durable, router-owned seen-`(signer, nonce)` window + clock-skew rejection).

### 3. Milestones

| M | State | What |
|---|---|---|
| M1 forwarding contract | **landed** (`signal-router` main) | `ForwardMessage`, `RemoteRouterIdentity`, `RegisterRemoteRouter`, `ForwardMarker`, `ForwardedRemote` |
| M2 offline two-router forward | **landed** (`router` main) | real OS-TCP loopback forward; `AcceptFixedTestIdentity` stub + process-local replay |
| **M3 real criome attestation + durable replay** | **not built** | the BLS-in-frame attestation via a criome client; the durable seen-window; **gated on the cluster-root admission-signing ceremony** |
| **M4 live ouranos↔prometheus over `ln`/Yggdrasil** | **not built** | two real hosts, real mesh, production deploy |
| (router half) Attend/Withdraw fan-out | **not built** | the classified-object subscription surface ([`l2ha`]); Sema-free verbs ([`7l7l`]); see report 135 |

## Part II — How to test it e2e on real networking

### 4. The principle (and why this section is the larger half)

Per `skills/human-interaction.md`: the test runs under the **most real-world
conditions available**; a sandbox-only shortcut that omits a load-bearing piece
of production topology is **not** real-world testing; and when production lacks a
capability the test needs, you **build a retrofitted variant for the test** and
**unblock the blocker inside the test**. For the router that bites hard, because
the load-bearing pieces — a real network hop, real BLS attestation, durable
replay, the cluster-root chain — are exactly the pieces currently stubbed.

### 5. What is real today, and the three masquerades

**Genuinely real now:** the router's TCP transport is production code
(`RouterRuntime::start_networked` binds a real Tokio listener; `peer_delivery`
dials a real `TcpStream`); the M2 e2e forwards a real length-prefixed rkyv frame
and delivers to a **real Unix-socket** component witness; the loop guard and the
content-binding-digest path are real; `process_boundary` spawns a **real
daemon** from a binary rkyv config (no flags).

**The three masquerades a naïve e2e would smuggle in** (each verified against
source):

1. **Loopback-as-remote.** The M2 e2e is *two `RouterRuntime`s in one process* on
   `127.0.0.1`. No OS process boundary, no network hop. `127.0.0.1` between two
   processes is still not remote.
2. **FNV-stub-as-BLS.** On-path attestation is `AcceptFixedTestIdentity`: it
   fills `public_key`/`signature` with literal `"offline-test-…"` strings and
   `content_digest` with an FNV-1a fold. `scheme` *says* `Bls12_381MinPk` but **no
   BLS math runs**. A "tampered-payload-fails" assertion against this proves a
   hash mismatch, not a signature break.
3. **In-RAM-window-as-durable-replay.** `ForwardAdmissionWindow` is a `HashSet` +
   `VecDeque` in memory. The landed test asserts `ReplayDetected` *once, within
   one process*. Nothing survives a restart — so a signed frame is replayable
   across a restart, and the green replay test is an active lie about replay
   defense.

### 6. The prerequisite to confront *first* (the biggest hidden fake)

Both candidate architectures assumed M3 is "swap `AcceptFixedTestIdentity` for a
criome client — a clean trait-body swap." **It is not clean, and pretending it is
would fake the whole criome integration.** Verified: the router's
`RouterPeerAttestation` is loose `String`s (`public_key`, `signature`,
`content_digest`) with **no blst and no criome dependency**; criome, by contrast,
**signs as its *own* identity** (`signer.rs:92`, criome's master key) over an
`AttestationPreimage` whose content is a `ContentReference`, and **verifies that
exact shape** (`verifier.rs:40`, signer must resolve in criome's registry). The
router's mental model — "the sending router holds a BLS key and signs the frame;
the receiver checks that per-router signature" — is **not** criome's model.

So before any "real BLS" e2e, prototype the criome `Attestation` round-trip the
router actually needs:

- The sender router asks its **local** criome: `Sign(SignRequest { content:
  ContentReference(forward-payload-digest), signer: <router's criome-registered
  identity> })`, and ships criome's `Attestation` in-frame.
- The receiver router asks its **local** criome:
  `VerifyAttestation(VerifyRequest { attestation, content })` and gets a
  blst-verified `VerificationDecision`, stamping the **criome-resolved** signer
  identity (never the wire-claimed field).
- **Decide explicitly** whether `RouterPeerAttestation` is *replaced by* criome's
  `Attestation`/`SignatureEnvelope` types or *wraps* them — do not keep the
  loose-String shape and pretend criome filled it.

This reconciliation is the real M3 design work, and it belongs in the *first*
real test, not hand-waved.

### 7. The ladder of realness

Each rung kills exactly one masquerade; the gate type is explicit.

| Rung | What runs | What's real / still simulated | Gate |
|---|---|---|---|
| **L0 — loopback (landed)** | two in-process `RouterRuntime`s, `127.0.0.1:0` | real TCP/frame/routing/loop-guard/Unix-socket delivery; **sim:** same process, FNV stub, in-RAM replay, no criome | flake `router-two-router-loopback-forward-delivers-remotely` |
| **L1 — real-criome-BLS over a real hop** | **two router-daemon processes + two criome-daemon processes** across **two kernels** (a `runNixOSTest` with two guests), bound on distinct IPs over a real virtual L2; the reconciled criome `Sign`/`VerifyAttestation` on-path; **durable** SEMA replay window; admission minted by a **persisted-key** cluster-root signer | real processes, real kernel/network boundary, **real blst attestation via criome**, real cluster-root admit, durable replay surviving `kill -9` + restart; **sim:** still a virtual bridge, not Yggdrasil | new flake `runNixOSTest` check (CI-able, hermetic) |
| **L2 — routed Yggdrasil binding** | L1, but the router binds its ingress on the guest's **Yggdrasil `[ygg-ipv6]:port`** with the router port opened on `yggTun`, and the two guests peer via **explicit static `Peers`** (not link-local multicast) | + real fabric bind/address/firewall path, routed-peer topology; **sim:** VMs not metal | new flake `runNixOSTest` check |
| **L3 — two real hosts (M4)** | router+criome on **ouranos** and **prometheus** over the live `ln.goldragon.criome` mesh; the full `d6he` chain incl. mirror restore | **fully real** | manual acceptance (cluster-operator deploy authority) |

The promotion to a **two-kernel `runNixOSTest`** at L1 (not a single-host
two-process loopback) is deliberate: it is the cheapest rung that is genuinely a
real network hop *and* CI-reproducible, and it forces the systemd
binary-rkyv-startup path and the criome round-trip to be real.

### 8. Non-negotiables (a rung that violates one is not real-networking)

- **Separate OS processes across a real hop** — two kernels at L1+, two hosts at
  L3. Same-process loopback never counts as remote.
- **Real blst BLS attestation minted+verified by a real criome on path** via the
  reconciled `Sign`/`VerifyAttestation` (§6) — not the FNV stub.
- **Real cluster-root admission:** the receiving criome holds a configured
  `cluster_root` public key and rejects any identity whose `RegistrationStatement`
  wasn't signed by it. **Assert `cluster_root: Some` on every node** — `registry.rs`
  *skips the gate entirely* when `cluster_root: None`, so a misconfigured node
  silently admits everyone and goes green. The admission must be **minted by a
  signer that loads the cluster-root secret from its persisted 0600 file** (not a
  fresh `MasterKey::generate()` per run, which never exercises key-load/encode).
- **Durable replay landed *with* attestation:** SEMA/redb-backed seen-`(verified
  signer, nonce, issued_at)`, asserted by `kill -9` + restart + replayed frame
  still `ReplayDetected`. A durable window guarding *unauthenticated* frames is
  meaningless, so durability and real BLS land in the same change.
- **Clock-skew** rejection against real wall-clock `issued_at` (backdated *and*
  future-dated). No such test exists today.
- **Real fabric bind** at L2+: ingress on the `[ygg-ipv6]:port`, the port opened
  on `yggTun` (today only link-local 9001/10001 are open), explicit routed
  `Peers` (the production mesh is routed, not one broadcast domain).
- **Loop guard:** a `Forwarded`-marked frame is never re-forwarded.
- **Daemons take only binary rkyv startup** (no flags) — the NixOS modules encode
  typed NOTA → rkyv before the daemon sees it.

### 9. Assertion matrix (positive + negative, against the real path)

- **POSITIVE forward+deliver:** a message injected on sender crosses the real hop
  and the receiver delivers it to a **real Unix-socket** component witness;
  `ForwardedMessagePayload` arrives intact; sender trace = `ForwardedRemote`.
- **POSITIVE attestation verify:** receiver's criome returns a blst-verified
  decision over the exact content digest under the sender's **admitted** key, and
  the **criome-resolved** origin is stamped.
- **NEGATIVE replay:** byte-identical resend → `ReplayDetected`; **and still
  rejected after a receiver `kill -9` + restart** (durability).
- **NEGATIVE clock skew:** `issued_at` outside the freshness window (past/future)
  → `ClockSkew`.
- **NEGATIVE unknown peer:** an identity minted by an **impostor key** (not the
  configured cluster-root) → `UnauthorizedRegistration`.
- **NEGATIVE tampered payload:** mutate a body byte / a routed-object octet
  **after the attestation is minted** → real BLS `InvalidSignature` (run only
  once real BLS is on path — against the FNV stub this proves nothing).
- **NEGATIVE loop guard / channel unauthorized:** `Forwarded` frame not
  re-forwarded; inner/outer attestation-field mismatch or ungranted channel
  refused.

### 10. Unblock-the-blocker fixtures (built for the test, retrofitted to prod)

- **One-shot cluster-root signer** (criome `src/bin/`, a real data-bearing type
  whose method holds the secret — not a free fn): loads/persists a cluster-root
  `MasterKey` to a 0600 file, takes an `Identity` + `BlsPublicKey` + purpose,
  builds `RegistrationStatement::to_signing_bytes`, signs, emits the
  `SignatureEnvelope`. Lifts criome's `#[cfg(test)]` minting into a one-NOTA-arg
  tool — and *is* the M3/at7x/5zur admission-signing ceremony (report 133 §4).
- **`CriomeForwardVerifier`** implementing the existing `ForwardAttestationVerifier`
  trait, reconciled to criome's `Attestation`/`ContentReference` shape (§6); the
  daemon picks it when `criome_socket_path` is set, keeps `AcceptFixedTestIdentity`
  otherwise (L0 stays green).
- **`message-router.nix` + `criome.nix` NixOS modules** (named to avoid the
  WiFi-router collision; modeled on the real `mirror.nix`): systemd units running
  the deploy-time NOTA→rkyv encode then launching the daemon from its rkyv file;
  `criome.nix` takes the cluster-root pubkey as a module option.
- **SEMA-backed replay window** persisted in the router's `.sema`.
- **mirror-on-Yggdrasil** (L3 only): rebind `mirror.nix` off `tailscale0:7474` to
  `yggTun` so the `d6he` chain terminates on one fabric.

### 11. What to defer out of the first real e2e

The `d6he` object **fan-out** (Attend/Withdraw + the `(ComponentKind,
AuthorizedObjectKind)` classification match) is **unbuilt in source** (signal-router
`Input` is `Summary`/`MessageTrace`/`ChannelState`/`ForwardMessage` only). Any
"fan-out works end-to-end" assertion today would necessarily run against a
test-only scaffold — a scaffold-shaped green lie. Likewise mirror-on-Yggdrasil
and the byte-identical restore belong to the chain rung, not the first forward.
**Sequence honestly:** prove the single-message authenticated cross-host forward
first; add fan-out + mirror restore as a later milestone built on it.

### 12. The sharpest first rung to build

A **two-separate-process, two-kernel** router↔router forward (a `runNixOSTest`
with two guests) with **a real criome daemon on each path**, after first
prototyping the criome `Attestation` round-trip (§6). Mint each router identity
into each criome registry via the **persisted-key** cluster-root signer; bind
ingress on distinct guest addresses (the Yggdrasil address + `yggTun` firewall
where the mesh is in play). Required assertions on this one rung: happy
cross-host delivery to a real Unix-socket witness; **post-attestation tamper →
`InvalidSignature`**; **replay → `ReplayDetected`, still rejected after `kill -9`
+ restart**; **impostor-key → `UnauthorizedRegistration`** with `cluster_root:
Some` asserted. This forces the criome-attestation-shape reconciliation — the
biggest hidden fake — into the very first real test, and defers everything
unbuilt.

### 13. Sequencing & ownership

- **Mine (system-designer, offline/contract + test design):** the §6
  attestation-shape reconciliation; the `CriomeForwardVerifier` design; the SEMA
  replay-window shape; the test ladder + fixtures; the Attend/Withdraw surface
  (later). Not blocked on the key track for the *design*.
- **Cross-lane:** the cluster-root **admission-signing ceremony** is the gating
  unblock (psyche ruling pending — report 133/135); operator/system-operator own
  the `message-router.nix`/`criome.nix` deploy modules, the live mesh, mirror-on-
  Yggdrasil, and the prometheus host-pubkey pin; cluster-operator owns the L3
  acceptance deploy.
- **The one prerequisite that gates the router half** (not this forward): the
  registry-owner decision from report 135 §3 (router sole matcher vs criome+router).
