# 143 — L2 Yggdrasil rung GREEN, and the attestation-seam spec (three P1s + one psyche decision)

*Phase 2 of taking the rest. Track E built the **L2** ladder rung — the transport
over a real Yggdrasil mesh, GREEN under KVM. Track C design-spec'd the
router⇄criome forward-attestation seam **instead of blind-building it** — and the
adversarial critic found three P1s that an auto-build would have shipped into the
trust core. That outcome is the whole case for spec-before-build on a
security-critical, teammate-adjacent piece.*

## Track E — L2 over Yggdrasil: GREEN under KVM, mesh-routed

Branch `transport-yggdrasil-l2-142` (off `transport-two-kernel-e2e-138`), commit
`25284258`, pushed. New nixosTest `router-two-kernel-yggdrasil-transport`: both
guests run `services.yggdrasil` with **static PEM keys** → deterministic `200::/7`
addresses; they peer directly (a routed static `Peer` over the eth1 carrier); the
receiver binds its router ingress **on its Yggdrasil address only** (unreachable
over eth1); the sender's `RegisterRemoteRouter` peer and the forward-probe target
are the receiver's `ygg` address.

Reviewer-confirmed it genuinely traverses the mesh, not an eth1 fallback: the only
`:7777` listener/target anywhere is `[201:be7f:…]:7777` (zero `192.168.1.x:7777`
hits), `ygg0` rx_bytes advanced `400→1796` across the two forwards, and eth1
carries only the Yggdrasil peering TCP session. The L1 assertions still bite over
the mesh path — delivered to the far harness witness, real minted slots, loop
guard refusing a `Forwarded` frame. (Bonus finding: NOTA carries a bracketed IPv6
socket via the pipe-text `[|[ipv6]:port|]` form so `[` doesn't open a delimited
block — verified against the real nota-next parser.) **Ladder now at L2.** L3
(bare-metal ouranos⇄prometheus) remains cluster-operator deploy.

## Track C — the attestation seam: sound skeleton, NOT build-ready

The spec consumes the **already-migrated** `VerifyAttestation` / `VerificationResult`
RPC on `signal-criome-positional-migration-142` (no new contract type), with the
sound skeleton the critic confirmed:

- **Sync trait + `spawn_blocking`.** `ForwardAttestationVerifier` stays synchronous
  (held as `Arc<dyn …>`, which async-fn-in-trait would break); the criome call is
  one connect+write+read on the **local 0600 Unix socket** (sub-ms), wrapped off
  the ingress mailbox. The async-trait toolchain risk is real and correctly
  avoided.
- **BLS verify core is sound.** criome gates wire-key == registered-key *before*
  verifying, under the correct DST, with scheme-confusion / content-binding /
  revocation / expiry guards; the registry admits an identity↔key binding **only
  on a cluster-root signature** (`ermr`). Forge-resistance holds.
- **lt44 lane fit + non-circular.** This is the per-hop **local** forward-
  verification lane (receiving router → its own host's criome, `9s52`), distinct
  from the direct criome-to-criome quorum lane; the router→criome (verify) and
  criome-quorum→router (deliver) dependencies are different layers/artifacts and
  close no runtime wait-loop.
- **No nfvm collision** on any on-disk branch — verified by grep for `MirrorAdopter`
  / `AuthorizedObjectKind::Head` / `CRIOME-AUTHORIZED-HEAD-V1` (the head-loop work
  is on a not-yet-landed designer branch); the seam touches none of those surfaces.

### The three P1s the critic caught (why we didn't auto-build)

1. **Preimage mismatch — verify would always FAIL.** The spec's signing preimage
   (`signer ‖ scheme ‖ content_digest ‖ issued_at ‖ nonce`) doesn't match criome's
   actual `AttestationPreimage::to_signing_bytes` (`master_key.rs:179-215`), which
   also covers `content.purpose/digest/schema_version`,
   `audit_context.purpose/audience/policy_version/nonce`, scheme (tagged), signer
   (tagged), `issued_at`, **and** `expires_at`. `RouterPeerAttestation` carries none
   of the extras. Fix in revision: either extend `RouterPeerAttestation` to carry
   them, or pin fabricated constants both routers sign byte-identically.
2. **Replay ownership is gapped, not gap-free.** criome's `VerifyAttestation` path
   has **no nonce tracking** and structurally cannot return `ReplayAttempted` (that
   lives on the *authorization* RPC the seam doesn't call). So the router's
   `ForwardAdmissionWindow` is the only replay defense for forwards — a per-receiver
   bounded LRU that can't see cross-hop/cross-receiver replay. Fix: own per-hop
   replay honestly in the router and document the cross-hop reliance on the inner
   agreement envelope's own `ay3y` crystallized-moment freshness, **or** add nonce
   tracking to criome's verify path (a criome change that *does* touch nfvm-adjacent
   daemon files → must sequence with nfvm).
3. **Citation + footprint:** the spec cited the **superseded `wckt`** — re-justify
   the verifier-seam on the live `lt44`. And Recommendation B (below) needs a new
   `KeyPurpose`, a `signal-criome` contract addition in the same `schema/lib.rs`
   nfvm edits — so B is not zero-footprint and must sequence with nfvm.

### The one decision that is genuinely the psyche's

**Where does the router's outbound forward signature come from?**

- **A — router calls criome's `Sign` RPC per outbound forward.** No signing key in
  the router; criome stays the sole signer/registrar; **zero contract addition**;
  one extra *local* (sub-ms Unix-socket) round-trip on send — symmetric with the
  verify RPC already done on receive. Simplest, smallest trust surface.
- **B — router holds a criome-issued, cluster-root-admitted forward-identity BLS
  key.** Pure-local fast send (no per-forward round-trip), but a **BLS key in the
  network-facing router** (a new trust surface needing `9s52` confirmation) and a
  **new `KeyPurpose`** contract addition that collides/sequences with nfvm.

Both the spec and the critic flag B's new trust surface as requiring explicit
psyche confirmation. My lean is **A** — it keeps the key in criome, adds nothing to
the contract, and the only cost (a local sub-ms round-trip on send) is symmetric
with what receive already pays.

## Sequencing

Resolve A vs B (psyche) → one spec-revision fixing the preimage to match
`to_signing_bytes` exactly, correcting the replay model, the `lt44` citation, and
the chosen send path → coordinated build (router seam is mine; the criome
`VerifyAttestation` RPC already exists on the migrated contract). Option A is
nfvm-clear; option B needs explicit sequencing with the head-loop's `schema/lib.rs`
edits.
