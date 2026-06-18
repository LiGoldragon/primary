# 138/2 — Track B: criome's cross-host wire-crypto layer (recommendation)

*A 3-advocate judge panel → synthesis, grounded in the live router + criome code.
This is the deferred "open design slot" (`signal-criome/ARCHITECTURE.md:333-335`,
`criome/ARCHITECTURE.md:6.1`). **This is a designer proposal awaiting psyche
choice — the architecture authors deliberately left it open, so committing one
option is a real architectural Decision that belongs to the psyche, not an
agent.***

## Recommendation: ride the existing router transport (score 9 of 10)

A cross-criome quorum solicitation travels as a `signal-criome`
`RouteSignatureRequest` / `SubmitSignature` frame **packed into the router's
existing `RoutedContractObject`** (contract name + operation + opaque rkyv
octets) inside `ForwardedMessagePayload`, delivered router-to-router over the
already-attested tailnet path (`RouterPeerAttestation` + `ForwardAdmissionWindow`
per hop), with criome verifying the **inner `StampedSignatureEnvelope`** (peer
BLS over the canonical solicitation digest) end-to-end against the peer master
key already in its identity registry.

**criome opens no network connections, holds no transport keys, adds no daemon
and no flags — it stamps and verifies; the router moves the bytes.** This is the
exact reading of the Telos principle the router's own INTENT states (`wckt`:
"the router carries cross-host delivery … never holds keys or verifies
signatures; that is criome's job, reached through a verifier seam"). The
`StampedSignatureEnvelope` already exists in the contract precisely for the
cross-criome quorum surface.

| Approach | Score | Why |
|---|---|---|
| Signed-envelope routed object over the router transport (RIDE) | **9** | zero new transport code; criome moves nothing; reuses the vetted forward seam |
| Mutual-TLS between criome daemons (OWN transport) | 4 | makes criome a mover; duplicates `peer_delivery.rs`; second identity surface + PKI; redundant with tailnet encryption |
| SSH / wireguard tunnel (OWN transport) | 3 | heaviest operational surface; SSH session/credential state as daemon config strains the no-flags rkyv discipline; third identity layer |

Both rejected approaches stand up a **parallel mover inside criome**, duplicating
the router's role and contradicting the micro-component + Telos disciplines.

## Adopt with one accepted constraint + four design items

1. **Constraint (accept + document):** cross-host quorum is gated on router
   availability. The layering is non-circular — the inner solicitation envelope's
   validity does not depend on trusting the router — but the *operational*
   coupling is real. criome's `pending`/`expiry` states are the
   graceful-degradation path. Single-host quorum (peers under different Unix users
   on one host) stays on the existing predictable Unix-socket path and never
   touches the router.
2. **Addressing mapping (undefined):** criome's peer-routing table (peer master
   pubkey → host, unix-user) must project onto the router's `RemoteRouterRegistry`
   (recipient actor → home identity → tailnet address), and the remote router must
   hand the inner frame to the correct remote criome daemon's Unix socket.
3. **Return leg:** the router forward path is fire-and-deliver
   (`ForwardAccepted`/`ForwardRefused` at the hop); a solicitation needs
   `SubmitSignature`/`RejectAuthorization` to come **back**. Model the reply as a
   second routed object (or an observation), not a synchronous request/reply.
4. **Replay/freshness ownership:** the router has `ForwardAdmissionWindow`
   (nonce + clock-skew) per verified router identity; criome has its own
   authorization-replay-nonce. Decide which layer owns which guarantee so
   freshness is neither duplicated nor gapped at the seam.
5. **Inner-envelope binding (verify, don't assume):** the `StampedSignatureEnvelope`
   must cover the canonical solicitation digest (request slot, digest, scheme,
   moment) so a malicious/buggy router cannot substitute a different solicitation
   — confirm the preimage before relying on "the router is untrusted."

## The layering tension, stated plainly (so nobody bolts on a parallel pipe)

- Milestone-3 swaps a **criome client into the router's `ForwardAttestationVerifier`
  seam** → router-depends-on-criome to *verify a forward* (a local call on the
  receiving host).
- Ride-the-router adds criome-quorum-depends-on-router to *deliver a solicitation*.

These are **two independent layers** (per-hop attestation vs. end-to-end inner
envelope), not a cycle. Written down here so a future maintainer doesn't read it
as circular and reintroduce a second transport.

## Intent

No capture from this synthesis — it's a proposal. The "criome moves nothing"
principle is already anchored (`wckt`); the cross-host transport *choice* is the
new decision. **If the psyche affirms ride-the-router, that becomes a Decision to
Record via Spirit and reflect into both repos' `ARCHITECTURE.md`/`INTENT.md` on
the same branch as the wiring work.** A gap-check against recent Spirit records
for any already-captured cross-host-transport intent is warranted first.
