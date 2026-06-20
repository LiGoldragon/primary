# 704-5 — Multi-machine criome cluster: the build plan

Psyche direction (this session): the next target is the **multi-machine /
DigitalOcean cluster** (the original "fully tested networked criome cluster"
goal at full scope); the multi-party quorum is **over peer criome nodes**, each
signing with its own master key (`p43g` — "a criome-node quorum"; confirmed),
the requester just submits; **designer keeps prototyping the criome runtime** on
branches, operator rebases. This is genuinely unbuilt and multi-session.

## The load-bearing gap — E1 (701)

criome's `transport.rs` is `UnixStream`-only (`:2,233,254`). The peer-signature
*actor flow* already exists — `RouteSignatureRequest` / `SubmitSignature` /
`store_signature_solicitation` handled by `AuthorizationCoordinator`
(`actors/authorization.rs:38,42,174,268,373,385`) — but **no cross-criome
network transport carries those frames between daemons**. Without it there is no
quorum across machines.

## The model (after `p43g`)

A k-of-n quorum = **k of n criome nodes sign with their master keys**. The
current `criome-cluster-1of1` witness uses a *developer-signer-signs-evidence*
model (the now-corrected requester-signs reading) — **to rework** to the
criome-node-quorum shape. Flow for a submission needing 2-of-3:
1. Requester submits a content-addressed object to its local criome A
   (submitter authenticated by SO_PEERCRED, `2st7`).
2. criome A signs with its own master key, then **solicits** signatures from
   peers B and C over the peer transport (`RouteSignatureRequest`).
3. B and C each verify + sign + reply (`SubmitSignature`).
4. A aggregates; threshold met → `Authorized`; criome A signs/publishes the
   verdict (criome owns the keys + decides, `p43g`).

## Build, in dependency order (designer branch; operator rebases)

1. **E1 — cross-criome peer transport.** A TCP peer lane (`CriomePeerClient` +
   a daemon peer listener, alongside the Unix working/meta sockets). Wire crypto
   is **specified, not a fork**: each frame BLS-signed by the sender criome's
   master key, receiver verifies before parsing (`ARCHITECTURE.md:437`), carried
   over the tailnet (network-layer WireGuard). Peer addressing comes from
   cluster config (peer `host:port` + master pubkey per node).
2. **Networked quorum assembly.** Wire `route_signature_request` /
   `SubmitSignature` through the peer transport: criome A signs + solicits B/C +
   aggregates; 2-of-3 → `Authorized`. Rework the witness to the criome-node
   quorum (criome nodes are the signers, not a developer).
3. **3-criome-node nixosTest over a real network.** Extend `mkCriomeClusterTest`
   to N members (the `members` seam, now honest after audit B8): three criome
   guests on the driver's vlan, each a criome node with its master key admitted
   under the cluster root; submit to A; assert a real 2-of-3 over the wire →
   `Authorized`, and a 1-signature-short → held. This is the first genuinely
   cross-kernel (and, on real hosts / DO, cross-machine) quorum proof.
4. **Cluster-root admission (E2).** Each node's criome master key admitted under
   the cluster root (a ceremony) — operator + system-operator; the test fixture
   builds it (unblock-the-blocker-in-the-test).
5. **DigitalOcean substrate.** The `cloud` nixos-anywhere bring-up (per its
   Hetzner Phase-2 lean) stands criome on N droplets with a private network;
   `mkCriomeClusterTest substrate=live` runs the same quorum assertion on real
   cross-machine droplets, with a mandatory teardown guard + max-N cap.

## Lane + sequencing

- Designer prototypes E1 + the quorum assembly + the multi-node nixosTest on a
  criome branch (`criome-peer-transport`); operator rebases / integrates main.
- Independent of operator's Track A (park substrate, `root.rs`/actors): E1 is the
  transport layer (`transport.rs` + the coordinator's solicitation wiring), so
  the overlap is small.
- Honest: E1 (transport + per-frame BLS envelope + quorum solicitation) is a
  substantial multi-file build; the 3-node networked test is its proof; DO is the
  final cross-machine substrate. Multi-session.
