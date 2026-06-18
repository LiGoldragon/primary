# 137 — Where we are: router transport vs criome-to-criome quorum across the network

*The psyche asked where we are with the router and with passing criome messages
to other criome daemons across the network. Method: a four-reader verification
workflow over the live code (`signal-router`/`router`/`meta-signal-router`,
`criome`/`signal-criome`, the CriomOS mesh/test repos) and recent cross-lane
reports — every claim below carries a file:line or commit. This corrects report
135's "router half is ZERO": one router half is far more built than that; the
other half is still unbuilt; and the two are different halves.*

## 1 — The question is two tracks; don't conflate them

"The router" and "passing criome messages to other criome daemons across the
network" are **two independent tracks at very different maturity**:

- **Track A — router → router transport.** Carrying bytes between hosts. This is
  the pipe. **Real and working, on a branch.**
- **Track B — criome daemon → criome daemon (cross-party quorum).** Multiple
  criome daemons reaching agreement across the network. This is what would *flow
  through* the pipe. **Designed only; not built — criome is single-daemon today.**

And a third thing the word "router" can mean — the **subscribe / interest /
fan-out** surface from reports 134/135 (`Attend`/`Withdraw`/`Differentiator`) —
is **still entirely absent**. That is a separate router half from the transport,
and it remains this lane's unbuilt design work.

## 2 — Track A: router cross-host transport (real, on a branch)

| Piece | Status | Evidence |
|---|---|---|
| Wire schema: `RoutedContractObject`, `RouterForwardRequest`, `ForwardMarker`, `RouterPeerAttestation`, `RemoteRouterIdentity`, `RegisterRemoteRouter`, `EndpointKind::RemoteRouter` | **on main** | `signal-router/src/schema/lib.rs:71,180,366,384,424,432` |
| `EndpointKind::ComponentSocket` (deliver to a component) | **on main** | commit `2022200` (2026-06-17); `router/src/harness_delivery.rs:138` |
| Real TCP forward: `RouterPeerDelivery::forward()` opens `TcpStream::connect`, writes length-prefixed `ForwardMessage`, reads reply | **on branch** `router-network-transport` | `router/src/peer_delivery.rs:97-119` |
| Signed peer attestation + monotonic replay nonce per forward | **on branch** | `peer_delivery.rs:52-59,87`; `forward_attestation.rs` |
| `RemoteRouterRegistry` + `TailnetForwardIngress` async ingress | **on branch** | `router/src/remote_router.rs`, `router/src/router.rs` |
| e2e: two in-process routers forward over **real loopback TCP** with attestation | **on branch, passing** | `router/tests/end_to_end_remote_forward.rs`; system-operator audit 229 |

The transport is genuinely built — real sockets, real signatures, a green
loopback e2e. But it lives on `router-network-transport` (`signal-router`
`74484ac` + `router` `b536487`, both 2026-06-16) and **is not merged to main**;
main (`430f1de`, today 17:28) post-dates the branch and carries only the schema.
The branch hasn't advanced since the 06-16 audit, which logged **P1 merge
blockers** (system-operator 229): `cargo fmt` fails on 5 files; `ForwardAccepted`
returns a **fake slot 0** instead of the real minted slot; "Accepted" semantics
ambiguous (durable-peer-receipt vs delivered-locally); the `ForwardMarker` loop
guard is unused; and — most important for going live — the **daemon path still
installs `AcceptFixedTestIdentity("router-offline-test")` even when a real
identity is configured**, so the offline test verifier is not fenced out of
production. `tailnet_listen_address` exists but isn't bound to a real provider.

## 3 — Track B: criome → criome across the network (design only)

**criome is single-daemon today.** Real BLS12-381 signing/verify and the
`ClusterRoot::admits` admission gate are on main (`criome` `068f9db`, today 18:30,
"port to strict signal-criome contract"; `master_key.rs`, `admission.rs:74-102`).
But **one criome daemon does not talk to another** yet:

- The contract *names* the verbs — `RouteSignatureRequest` / `SubmitSignature` /
  `RejectAuthorization` and a predictable peer-socket discovery scheme
  (`signal-criome/ARCHITECTURE.md:74,318-330`).
- The daemon **only stores** a routed solicitation — `route_signature_request`
  (`criome/src/actors/authorization.rs:174-196`) has **no outbound peer
  connection**, no `connect` to a peer, no gossip/sync actor.
- Cross-host transport is an **explicit open design slot**: "Local Unix sockets
  do not cross hosts; quorum policies that name peers on other hosts need a
  wire-crypto layer" (`signal-criome/ARCHITECTURE.md:333-335`; TLS / signed-
  envelope / SSH-tunnel listed as candidates).
- Multi-party signatures are **collected per-signer, not BLS-aggregated**
  (`StampedSignatureEnvelope`, `ARCHITECTURE.md:355`); quorum threshold logic
  exists (`AuthorizationPolicySatisfaction`, `Threshold`, `signal-criome/src/lib.rs:167-199`)
  but the **cross-machine majority guard is wrong** — it tests `> count` rather
  than the fork-safe `> n/2` (designer 685, `language.rs:578,414`), and the
  cross-machine "head" assembly layer is entirely absent (no `Head`
  `AuthorizedObjectKind`, no `CRIOME-AUTHORIZED-HEAD-V1` preimage, no
  `MirrorAdopter`).

One genuine advance since report 135: the criome `SubscriptionRegistry` now
**delivers filtered references** (filters by subscriber interest, returns a
snapshot — `criome/src/actors/subscription.rs:114-153`), not just counts matchers
as 135 reported.

## 4 — The realness ladder (report 136), where we actually sit

- **L0 in-process loopback TCP** — **DONE, on branch** (`end_to_end_remote_forward.rs`).
- **L1 two-kernel nixosTest with real criome BLS** — **not built.** The only
  two-node test on main is `mkDeployTest.nix` (hermetic lojix deploy smoke,
  deployer→target via in-test `networking.hosts`) — not a criome/router mesh.
- **L2 routed over Yggdrasil** — **designed only.** Yggdrasil is configured in
  CriomOS (`modules/nixos/network/yggdrasil.nix`) but **disabled in the test
  cluster** (`CriomOS-test-cluster/flake.nix`, `lib.mkForce false`). The m3
  deploy plan (designer 669/4) picks the Yggdrasil fabric and names node
  addresses, but the `criome.nix` and `message-router.nix` NixOS modules **do not
  exist** and nothing is deployed.
- **L3 two real hosts (ouranos↔prometheus)** — **not built.** Prometheus is a
  single build/nspawn host, not a mesh peer; `ouranos-mind`/`prometheus-responder`
  appear only as test actor names (`round_trip.rs:46-47`). No live multi-host
  router/criome deployment exists anywhere.

So the honest position: **L0 on a branch.** Everything above L0 is design.

## 5 — The chain from here to live criome-to-criome

For one criome daemon to authorize against another across the network, in order:

1. **Merge + production-fence Track A** — clear the 229 P1s, and especially
   replace `AcceptFixedTestIdentity` in the daemon path with the real verifier.
2. **Build criome's cross-host wire-crypto layer** — the deferred "open design
   slot"; today's Unix-socket peer routing cannot leave the host.
3. **Land the router subscribe/fan-out half** (134/135) **and** `signal-standard`
   — currently `/tmp`-only, not a git repo — so components address each other by
   `(component, kind)` rather than ad-hoc actor names.
4. **Fix the cross-machine quorum invariant** (`> n/2`) and build the head-
   assembly layer (685's missing `Head`/preimage/adopter).
5. **Create the NixOS modules + enable Yggdrasil + provision per-node identities**
   — which is where my **cluster-root admission ceremony** plugs in: it mints the
   cluster-root-signed `RegistrationStatement` the on-main `ClusterRoot::admits`
   gate accepts. It sits on branch `cluster-root-admission-ceremony` (`6ab6a4c`),
   reviewed clean, **not yet merged** — operator owns integrating it to main.

## 6 — What is this lane's, and intent hygiene

- **Mine, still unbuilt:** the router subscribe/`Attend`/`Withdraw`/fan-out
  surface (135 §4) and its `signal-standard` differentiator. The transport
  (Track A) and the criome auth stack (Track B substrate) are operator/
  system-operator work on their branches; the cross-host quorum design is shared
  with designer (685).
- **Intent flags (already raised in 135 §6, not acted on unilaterally):** `m0p2`
  vs `l2ha` still need a `Clarify` to name one fan-out owner; the
  `ComponentPrincipal`-collapse decision still has no Spirit anchor (lives only in
  a commit + report 681). No new capture is owed by this status check — "where
  are we" is a current-state question, not durable intent.

## 7 — For the psyche

1. **Track A is the nearest real win:** the cross-host router transport works on
   a branch and is blocked only by mergeable P1s + a production-identity fence.
   Want me to push operator to land it (and the L1 two-VM nixosTest that would
   make it real beyond loopback)?
2. **Track B (criome↔criome) is a design fork still open:** the cross-host
   wire-crypto layer is undecided (TLS vs signed-envelope vs SSH-tunnel). That is
   a designer call I can drive to a recommendation.
3. ~~The wrong **`> n/2` quorum guard** is a correctness bug in the cross-machine
   path~~ — **RETRACTED (2026-06-18, see 138/4).** Investigation found this is
   *not* a bug: `language.rs:414`/`:578` are correct admission-time well-formedness
   guards on a caller-declared **m-of-n** threshold (`0 < m ≤ n`), not a majority
   check; satisfaction is `satisfied >= required` (correct). A `> n/2` rewrite
   would *regress* legitimate `required=1` and `required=n` contracts. The error
   was in report 685's Woe-3, which misread the declared threshold field as a
   collected-signature tally.
