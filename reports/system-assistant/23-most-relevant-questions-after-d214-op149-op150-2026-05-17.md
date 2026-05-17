# 23 — Most-relevant questions after D/214 + OA/149 + OA/150

Date: 2026-05-17
Role: system-assistant
Scope: Short update to SYS/22's question catalogue. Reads the three
reports committed after SYS/22 landed at 19:46 — D/214 (20:20–22:58),
OA/149 (22:58), OA/150 (23:18) — and re-picks the live question set.

This is **not** another audit; SYS/22 carries the cross-lane critique.
This is just the updated question priority list.

---

## 0 · What's closed since SYS/22

| SYS/22 item | Now closed by | How |
|---|---|---|
| §4.5 plaintext-passphrase-over-local-socket weakness | D/214 §2.1 | Owner-signal-criome carries ECDH-handshake-then-AEAD-encrypted session from day one. ARCH text + Nix doc witness landed in op-149's `criome 2b74697`. |
| Q5 (denial source split) — was already a sharpening of SYS/141 Q | OA/149 `signal-criome 9dff026` | `AuthorizationDenial { source: AuthorizationDenialSource, reason }` distinguishes policy-refusal from signer-refusal on the wire. |
| Implicit: "threshold on grants" | OA/149 | `AuthorizationGrant` now carries `AuthorizationPolicySatisfaction { policy_class, required_signature_threshold, ... }` plus the signers that satisfied it. |
| Implicit: "request slot derived from digest is wrong" (op-149 known debt) | OA/150 `signal-criome be950e3` + `criome 73d34bf` | `AuthorizationRequestSlot` is now store-minted via `StoreKernel`'s `CreateAuthorizationState`; `authorization_next_slot` table; witness asserts two submissions of same `SignalCallAuthorization` yield two different slots. |

D/214 also consolidates D/212 + D/213 into one record and explicitly
adopts SYS/22's per-(host, user) criome framing (D/214 TL;DR bullet:
*"Many criome daemons per cluster. One per Unix user…"*) — that was
the biggest finding of SYS/22 and it landed.

---

## 1 · The live question set, re-prioritized

D/214 §11 enumerates 14 open items. Of those, OA/149 and OA/150
together closed §11.11 (typed slot) and the ECDH-on-owner-session
decision. The remaining 13 split by lane:

### Tier 1 — design decisions that BLOCK multi-node progress

| # | Item | D/214 ref | My lean (for the user to accept/reject) |
|---|---|---|---|
| Q1 | **Unattended-system-daemon bootstrap** | §11.1 (= SYS/22 Q3) | v1: master key unencrypted, filesystem-permission-protected only (matches D/214 §2's "Unix-user permission IS the boundary"). v2: TPM-sealed with PCR-bound policy. **Blocks cluster-side criome ship until decided.** |
| Q2 | **Cross-user-same-host routing** | §11.2 (= SYS/22 Q1) | Three candidates: (a) TCP loopback with peer-credential auth (works but breaks predictable-socket-name discipline); (b) **persistent system-level routing socket** owned by a privileged-but-isolated routing daemon (preserves Unix-socket discipline); (c) FD-passing via a spawn-time envelope (cleanest if every participating user is started by the same correctness root, weaker if not). **Lean: (b).** Blocks multi-user same-host quorum, which is today's in-scope quorum case. |
| Q3 | **System criome's role** | §11.3 (= SYS/22 Q2) | Full participant under operator-set policy — `lojix-system` criome can auto-sign routine internal effects (cache attestation, internal trust mutation under operator-set policy) but escalates high-risk actions (initial deploys, irreversible operations) to operator approval. Affects whether deploys can run while operator is offline. |

### Tier 2 — wire / contract decisions needed before next operator pass

| # | Item | D/214 ref | My lean |
|---|---|---|---|
| Q4 | **`SignedObject` canonical bytes** | §11.7 (= SYS/141 Q3, SYS/22 Q5) | All security-relevant context fields inside the signed digest: `request_id`, target cluster, target node, action verb, expiry, anti-replay nonce, issuing-criome identity. Anything outside is rebinding-attack territory. **Operator's next master-key-signing slice (§11.13) cannot proceed without this answered.** |
| Q5 | **Verifier policy vs originator policy** | §11.6 (= SYS/22 Q10) | `SignedObject` carries the *satisfied-policy spec* (which signers / what quorum). Receiving criome verifies signatures-valid AND spec-acceptable-by-my-local-policy-for-this-action. Wire definition needed before peer verification slice ships. |
| Q6 | **owner-signal-criome contract sketch** | §11.8 | Next designer report. Includes the ECDH-handshake-then-AEAD-encrypted-session shape; cipher choice (Noise XX vs hand-rolled X25519 + HKDF-blake3 + ChaCha20-Poly1305/AES-GCM). Decision needed for OA-lane to start. |

### Tier 3 — operability / policy decisions (less urgent but real)

| # | Item | D/214 ref | My lean |
|---|---|---|---|
| Q7 | **Escalation-to-approve configurability** | §11.5 (= SYS/22 Q7) | Per-policy-record optional `requires_owner_approval: bool` is the smallest v1 surface; scope-pattern predicates land with the deferred rich schema. |
| Q8 | **`RegisterIdentity` placement** | §11.4 | Owner-class (daemon's own master) → owner-signal-criome. Third-party variant (e.g. Developer registers Host) stays on signal-criome **but** is itself authorization-gated by criome's own policy ("which signers may register a Host"). Otherwise the identity registry is spammable. |
| Q9 | **Operator-offline-mid-quorum visibility** | §11.9 (= SYS/22 Q12) | Pending-authorization state tracks who's solicited-but-not-responded. Surfaces in the `ObserveAuthorization` event stream. **Depends on §11.10 (push stream) landing first.** |

### Tier 4 — new questions surfaced by reading D/214 + OA/149 + OA/150

These weren't in SYS/22 or earlier reports; they emerged from
reading the implementation pass.

| # | Item | Why this is new |
|---|---|---|
| Q10 | **Does criome see only the digest, or also the content?** | If only the digest: security metadata (target, action, expiry) MUST be inside the signed bytes (forces Q4 toward "all metadata inside"). If criome sees content: metadata can travel beside the digest. The current `AuthorizeSignalCall` wire is digest-only — but does criome need the content to do BLS verification (§11.12) of the signers' signatures over the content? **The verifier's BLS check requires the original bytes, not just a digest.** So criome receives `(signed_object_bytes, claimed_digest)` — this needs to be made explicit in the wire. |
| Q11 | **Implementation order between push stream (§11.10) and master-key signing (§11.13)** | Op-149's note: §11.13 "is the most load-bearing next implementation slice." But §11.10 (push stream) is the prerequisite for §11.9 (operator-offline visibility) AND for `lojix-daemon` restart-mid-AwaitingAuthorization survival. Lean: §11.13 first (gives an end-to-end simple-self-signed flow that's testable via poll-snapshot for the prototype); §11.10 lands as soon as operator-interactivity is in scope. |
| Q12 | **tui-criome owner-session lifecycle vs ECDH session lifetime** | The ECDH handshake is per-connection. A one-shot CLI connects → handshakes → submits → closes — natural. A long-running TUI: does the ECDH session persist for the TUI's entire run, or do individual operations each open a fresh session? Daemon restart: TUI re-handshakes with fresh ephemeral keys? Key rotation policy for long sessions? These are owner-signal-criome contract questions (per Q6) but worth pre-flagging. |
| Q13 | **`AuthorizationRequestSlot` representation on the wire** | OA/150 noted: "remains a string newtype at the contract boundary; daemon now mints numeric string slots in store, which is better than digest-derived identity, but a future contract pass may want a stronger slot shape." Wire pass to decide if `Slot<AuthorizationRequest>` with internal structure is worth the contract evolution cost vs an opaque string. |
| Q14 | **Cross-host transport "fail-closed" wire shape** | D/214 §9: cross-host slots fail closed with `AuthorizationUnavailable` + typed reason. But the peer-routing table needs to *distinguish* same-host from cross-host before that error can be raised cleanly. Implies the routing table carries `(host, user)` pairs from day one even though cross-host transport is future work — every routing-table entry whose `host` slot is non-local triggers fail-closed. This is a small contract addition but easy to miss. |

---

## 2 · Decision-order recommendation (revised since SYS/22)

Designer-lane bottleneck (in dependency order):

1. **Q4 (SignedObject canonical bytes)** — blocks operator's §11.13 master-key signing. Smallest, sharpest answer.
2. **Q10 (criome receives content + digest, not just digest)** — falls out from Q4. Make it explicit in the wire.
3. **Q1 (unattended-bootstrap v1 = unencrypted + filesystem-permissions)** — blocks cluster ship. User decision; v1 is the only blocker.
4. **Q6 (owner-signal-criome contract sketch including ECDH/AEAD cipher choice)** — needed for tui-criome and CLI passphrase submission.
5. **Q2 (cross-user-same-host routing)** — blocks today's quorum case.
6. **Q3 (system criome role — full vs machine-identity)** — affects deploy operations while operator offline.
7. **Q5 (verifier policy vs originator policy wire shape)** — needed for §11.12 real BLS verification.
8. Lower-priority: Q7, Q8, Q12, Q13, Q14.

Operator-lane can proceed on:
- §11.13 master-key signing for simple-self-signed policy (load-bearing; needs Q4 answered)
- §11.10 push stream for `ObserveAuthorization` (operator can build this in parallel with Q4 thinking; design is clear)
- §11.12 real BLS verification in `VerifyAuthorization` (needs Q4 + Q10 + Q5)
- §11.14 replay-guard + expiry enforcement (independent of design; spec already in ARCH)

---

## 3 · Carry-forward from SYS/22 that's still on the table

These are unchanged:

- **Criome IS a PKI** (SYS/22 §7.4 / D/214 §13). Both reports surface
  this as a load-bearing architectural strength. Worth keeping
  visible — it makes the future TLS option for cross-host transport
  much cheaper and unifies cross-component trust resolution.
- **Cross-host transport** (SYS/22 Q6 / D/214 §9) is explicitly
  future work. Lean: per-frame BLS-signed envelope. Decision can
  wait until same-host quorum lands.
- **ClaviFaber first-boot key bundle** (SYS/22 Q3, sharpened from
  SYS/141 Q7) — separate per trust domain, generated together.
  Affects the unattended-bootstrap path (Q1 above): unencrypted
  master key at filesystem-permission protection is only as safe as
  ClaviFaber's first-boot key custody.

---

## 4 · No-effect-before-grant invariant — still the right first witness

SYS/141 §"Actors I expect in lojix" stated the invariant:

> *"No actor that mutates Nix, the store, a cache session, or a
> system profile runs before `CriomeAuthorizationActor` grants the
> exact request/scope."*

This remains the right *first* witness for the lojix↔criome
integration. OA/149 has the criome-side actor skeleton; the
lojix-side `CriomeAuthorizationActor` doesn't exist yet. The
witness, once both sides exist, should be:

1. **No-Nix-effect-before-grant.** Submit a deploy intent; assert
   no fake Nix tool was invoked before `AuthorizationGranted`.
2. **Digest-mismatched-grant-rejected.** Submit a grant for digest
   X against a request whose actual digest is Y; assert rejection.
3. **Missing-required-signer-rejected.** Submit a grant whose
   signers don't satisfy the required policy class/threshold;
   assert rejection.

All three become writable once Q4 + Q5 land and `CriomeAuthorization
Actor` skeleton on the lojix side exists.
