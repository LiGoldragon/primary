# 144 — What the router⇄criome attestation seam is, and what A vs B actually decides

*The psyche asked, mid-decision, "what is this about exactly?" This explains the
attestation seam from first principles, then what the A-vs-B choice concretely
changes. Companion to 143 (the spec + the three P1s).*

## 1 — The problem: who really sent this forward?

The router's job is to move a message from an actor on one host to an actor on
another — ouranos's router forwards to prometheus's router, which delivers to the
local harness. (That whole path is now proven: L1/L2 in reports 138/6 and 143.)

When prometheus's router receives a packet that says *"this is a forward from
ouranos's router, deliver it to actor X,"* it faces a security question: **is this
actually from ouranos, or is it a forgery or a replay from someone else on the
network?** The mesh (tailnet / Yggdrasil) encrypts the bytes in transit, but
encryption answers "can an eavesdropper read it," not "which router authored it."
Those are different guarantees. A compromised or malicious peer on the mesh could
fabricate a forward unless each forward carries proof of authorship.

So every forward carries a cryptographic **attestation** — a BLS signature, today
`RouterPeerAttestation { signer, scheme, public_key, signature, content_digest,
issued_at, nonce }` — that the receiving router checks before it trusts and
delivers anything. That check is the **attestation seam**.

## 2 — Why criome, not the router, does the checking

A Telos design principle (`lt44`, which superseded `wckt`): **the router moves
bytes but holds no keys and verifies no signatures — that is criome's job, reached
through a verifier seam.** criome is the authorization-and-agreement organ: it is
the **registrar** (it knows which identities are admitted and which public key each
holds — and an identity↔key binding is admitted *only* on a cluster-root signature,
`ermr`) and the **verifier**.

So the router doesn't decide validity itself. On receiving a forward it hands the
attestation to its **own host's** criome (per-Unix-user custody, `9s52` — a local
`0600` Unix socket, no network hop) and asks: *is this signer an admitted identity,
and is this signature valid, unrevoked, and fresh?* criome answers; the router
acts. This keeps the network-facing mover (the router) free of key material and
trust logic, concentrating both in the dedicated custody daemon.

## 3 — The two directions (and which one is contested)

```mermaid
sequenceDiagram
    participant HA as Harness (host A)
    participant RA as Router A
    participant CA as Criome A (local, 0600)
    participant RB as Router B
    participant CB as Criome B (local, 0600)
    participant HB as Harness (host B)

    Note over RA,CA: SEND — produce the attestation  (★ A vs B is ONLY here)
    HA->>RA: message for an actor homed on B
    alt Option A — no key in the router
        RA->>CA: Sign(forward preimage)
        CA-->>RA: BLS signature
    else Option B — router holds its own key
        RA->>RA: sign preimage locally with own key
    end
    RA->>RB: forward + RouterPeerAttestation (over tailnet / Yggdrasil)

    Note over RB,CB: RECEIVE — verify  (SETTLED; identical in A and B)
    RB->>CB: VerifyAttestation(attestation, content)
    CB-->>RB: VerificationResult — admitted? valid? fresh?
    alt valid
        RB->>HB: deliver to the actor harness
    else invalid
        RB-->>RB: refuse, no delivery
    end
```

- **Receive / verify — settled.** The receiving router calls its local criome's
  `VerifyAttestation` RPC (which already exists on the migrated `signal-criome`).
  criome checks wire-key == registered-key, then BLS-verifies under the criome DST,
  with scheme-confusion, content-binding, revocation, and expiry guards. The spec's
  skeleton for this is sound (a synchronous trait call wrapped off the ingress
  mailbox). **A vs B does not touch this direction.**
- **Send / sign — the question.** Before host A's router can forward, it must
  *produce* the attestation: BLS-sign the forward's canonical preimage with host
  A's forward-identity private key. Computing that signature requires the private
  key. **A vs B is solely about where that key lives and where the signing
  happens.**

## 4 — A vs B, concretely

The signature is over a *preimage* — the canonical bytes describing the forward
(signer, content digest, timestamps, a nonce, and — per P1 in report 143 — several
more fields criome's `to_signing_bytes` requires). Producing it needs the private
half of A's forward-identity key.

- **Option A — the router asks criome to sign.** The router holds **no** private
  key. When it needs to attest a forward, it calls its local criome's `Sign` RPC
  ("sign these bytes as my forward identity"); criome, which holds the key, returns
  the signature. Cost: one extra **local** Unix-socket round-trip per outbound
  forward — sub-millisecond, same host, and *symmetric* with the verify RPC the
  receive side already pays. No `signal-criome` contract change. Compromising the
  router yields no signing capability, because the router never has the key.

- **Option B — the router holds its own forward key.** criome mints the router a
  cluster-root-admitted forward-identity BLS key once; the router then signs every
  forward **locally**, with no per-forward round-trip (fastest send path). The cost
  is structural: a **BLS private key now lives inside the network-facing router
  process** — the one process listening on the mesh — which widens the attack
  surface, and it needs a new `KeyPurpose` variant in the `signal-criome` contract
  (a schema addition that overlaps and must sequence with the designer's active
  `nfvm` head-loop edits).

So it is the classic **key-custody trade-off**: A keeps every private key inside
the dedicated custody daemon (criome) and leaves the router keyless; B trades that
containment for a faster hot path by giving the network-facing daemon a key of its
own.

## 5 — Why this is genuinely the psyche's call

Putting a signing key in a network-facing process is a **trust-boundary
decision**, not a mechanical one. It interacts directly with `9s52` (criome is the
per-Unix-user custody boundary — the reason there's no shared/embeddable criome).
Both the design-spec and the adversarial critic independently flagged that B's new
trust surface needs explicit psyche confirmation before it becomes a Decision. A,
by contrast, changes no trust boundary — it's the conservative default.

## 6 — Is this even blocking right now?

Largely no, and that matters for the choice. The thing that lifts the
`CriomeVerifierUnavailable` refusal and enables a *real-criome-BLS* transport is the
**verify** direction — and verify is settled and independent of A/B. We could wire
**verify-first** (receive-side real attestation, the immediate unblock) and defer
the send-signing choice until the client is actually built. So A vs B does not have
to be answered to make the next real progress; it only has to be answered before
the *send* path is finalized. The two mechanical P1s from 143 (the preimage must
match criome's `to_signing_bytes` exactly; the replay-ownership model must be made
honest) are mine to fix in a spec-revision regardless of A/B.

## 7 — Recommendation

**A.** The only thing B buys is removing a sub-millisecond local round-trip on the
send path — and the receive path already pays an identical local round-trip, so the
asymmetry B removes is small. Against that, A keeps all key custody inside criome
(honoring the `9s52` model), adds nothing to the contract, and stays clear of
`nfvm`. If forward throughput later proves the per-send round-trip is a real
bottleneck, B is a clean, well-understood optimization to revisit then — with the
trust-surface decision made deliberately rather than for an unmeasured speedup.
