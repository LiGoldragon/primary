# 216 — Criome routed authorization state (2026-05-18)

*Topic compendium for the criome routed authorization arc. Part of the
2026-05-18 workspace state-of-art series. Master index lives in
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.*

---

## 1 · State of art

The criome routed authorization arc converged on 2026-05-17 and shipped
implementation slices through 2026-05-18. The canonical record is
`reports/designer/214-criome-architecture-record-2026-05-17.md`
(supersedes designer/212 + /213, both deleted). The settled architecture:
**one criome daemon per (host, Unix user)**; **two policy classes**
(Simple self-signed, Complex quorum); **two escalation kinds** (sign,
approve); **three client classes mapped to two contracts**
(`signal-criome` for peers + consumers, future `owner-signal-criome` for
the owner); **ECDH-handshake-then-AEAD-encrypted owner-session**;
**store-minted authorization slots** (never digest-derived).

Canonical ARCHs:
`/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` at commit `4474bb8`
and `/git/github.com/LiGoldragon/signal-criome/ARCHITECTURE.md` at
commit `723e6c8`. Both repos are publicly shipped.

What's shipped: contract types (`AuthorizationPolicyClass`,
`RequiredSignatureThreshold`, `AuthorizationPolicySatisfaction`,
`AuthorizationDenialSource`, `AuthorizationStatus::Signing`,
`AuthorizationGrant.request_slot`); `AuthorizationCoordinator` Kameo
actor under `CriomeRoot`; Sema tables for requests / solicitations /
submissions / policy / peer-routes / replay nonces;
`StoreKernel.CreateAuthorizationState` (mints slots); owner-socket mode
`0600` witness; expiry + replay enforcement (`criome` `55077e2d`);
lojix-side `CriomeAuthorization` actor with `no-Nix-effect-before-grant`
witness (`lojix` `6a799dac` on `horizon-leaner-shape`, `signal-lojix`
`df49dae1`).

What's design-only: `owner-signal-criome` contract (no repo yet); real
BLS verification (currently digest equality); master-key signing for
simple-self-signed policy (only skeleton state); `ObserveAuthorization`
push stream (snapshot-only); cross-user-same-host routing; cross-host
transport; unattended-system-daemon bootstrap (v1 vs v2 TPM).

---

## 2 · Load-bearing reports

| Path | Carries |
|---|---|
| `reports/designer/214-criome-architecture-record-2026-05-17.md` | Canonical consolidated record; §11 holds the live open-items table; §13 surfaces the "criome IS a PKI" framing not yet in ARCH. |
| `reports/operator-assistant/149-criome-designer-214-implementation-pass-2026-05-17.md` | First operator pass; cites landed commits `9dff026`, `bd98b9d`, `2b74697`. |
| `reports/operator-assistant/150-criome-authorization-slot-identity-follow-up-2026-05-17.md` | Closes /214 §11.11 (store-minted slots); commits `be950e3`, `73d34bf`; Nix check `criome-authorization-slots-are-store-minted`. |
| `reports/operator-assistant/151-lojix-criome-authorization-gate-2026-05-17.md` | Only report carrying lojix-side gate substance; `criome_authorization_denial_blocks_every_fake_nix_effect` witness. Not yet in lojix `ARCHITECTURE.md` on main. |
| `reports/operator-assistant/152-criome-authorization-expiry-replay-guard-2026-05-18.md` | Closes /214 §11.13; commit `55077e2d`. Most-recent operator pass. |
| `reports/system-specialist/141-lojix-criome-arca-implementation-synthesis-2026-05-17.md` | `DeploymentArtifactSet` nine-digest shape; `NixConfigurationActor` include-point refinement; lojix actor enumeration. Not yet absorbed into lojix ARCH. |
| `reports/system-specialist/142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md` | User's corrections: regular `signal-criome` socket is **public + unencrypted**; permission artifact distinct from request digest; `AssertSigningDecision` shape. Not yet absorbed into /214 or ARCH. |
| `reports/system-assistant/22-audit-criome-routed-authorization-arc-2026-05-17.md` | Strongest cross-lane audit; surfaced per-(host, user) finding /214 adopted. |
| `reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md` | Live decision-order recommendation; Tier-1 blockers + new Q10 (criome receives content + digest, not digest-only) + Q11 (push-stream vs master-key-signing order). |
| `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md` | Substrate for OwnerSignal discipline that `owner-signal-criome` inherits. |

---

## 3 · Stale / superseded reports

| Path | Status | What's stale | Successor |
|---|---|---|---|
| `reports/operator-assistant/148-criome-signature-authorization-decisions-2026-05-17.md` | Partly stale | "tui-criome as separate component with its own Sema database and signing-client key custody" framing. | designer/214 §4 (tui-criome is owner client of the user's own daemon, not a separate triad) |
| `reports/system-specialist/140-lojix-criome-mediated-authorization-decision-2026-05-17.md` | Partly stale | "signed object is the canonical signal-lojix request" framing. | system-specialist/142 (signed object is a Criome permission artifact that *names* the request digest) |
| `reports/system-assistant/21-criome-routed-authorization-and-thin-cli-shape-2026-05-17.md` | Superseded | Single-criome-per-node framing + criome-as-ACL framing. | system-assistant/22 (per-(host, user); signature-derived not ACL) |

---

## 4 · Contradictions resolved by most-recent-wins

| Topic | Loser → Winner |
|---|---|
| tui-criome shape | OA/148 (separate component) → **designer/214** (owner client of own daemon) |
| Criome as ACL/policy-DB | SYS/21 → **designer/214** + ARCH §"Authorization model" (signature-derived, not ACL) |
| Per-node criome count | SYS/21 (one per node) → **designer/214** + SYS/22 (one per (host, user)) |
| Plaintext passphrase on owner socket | D/213 (no encryption added) → **designer/214 §2.1** + ARCH §"Security model" (ECDH/AEAD from day one) |
| Signed-object semantics | SYS/141 (the signal-lojix request) → **SYS/142** (a Criome permission artifact that may name the request digest); partially in `AuthorizationGrant` shape, `target_environment` field NOT yet in `signal-criome` |
| Slot derivation | OA/149 (digest-derived, known debt) → **OA/150** + commits `be950e3`/`73d34bf` (store-minted; witness `criome-authorization-slots-are-store-minted`) |

---

## 5 · Open questions awaiting decision

Priority per system-assistant/23 §2:

1. **`SignedObject` canonical bytes** (/214 §11.7, SYS/23 Q4) — which fields are in the signed digest: request_id, target cluster/node, action verb, expiry, anti-replay nonce, issuing criome identity, target_environment (per SYS/142). **Blocks** /214 §11.12 master-key signing.
2. **Criome receives content + digest, not just digest** (SYS/23 Q10) — BLS verification needs original bytes. Current `AuthorizeSignalCall` wire is digest-only. Needs explicit wire shape.
3. **`owner-signal-criome` contract design pass** (/214 §11.8, SYS/23 Q6) — request/reply vocabulary for passphrase submission, peer registration, policy mutation, escalation-to-approve prompts + replies. Includes cipher-suite choice (Noise XX vs hand-rolled X25519 + HKDF-blake3 + ChaCha20-Poly1305/AES-GCM). Blocks tui-criome implementation and CLI passphrase flow.
4. **Unattended-system-daemon bootstrap** (/214 §11.1, SYS/23 Q1) — `lojix-system` user's criome has no human at boot. v1: unencrypted master key + filesystem permissions (matches "Unix-user permission is the boundary" claim). v2: TPM-sealed with PCR-bound policy. **Blocks** cluster-side criome ship.
5. **Cross-user-same-host routing** (/214 §11.2, SYS/23 Q2) — predictable-socket-name pattern breaks across Unix-user runtime dirs. SYS/23 lean: persistent system-level routing socket owned by privileged-but-isolated routing daemon. SYS/142 partially undercuts this: regular `signal-criome` socket is reachable by anyone, gap may be smaller than D/214 framed.
6. **Verifier-policy vs originator-policy** (/214 §11.6, SYS/22 Q10) — when peer B verifies a SignedObject from peer A, does B check signers-acceptable-by-A's-policy or B's-policy? Lean: `SignedObject` carries the satisfied-policy spec; B verifies signatures-valid AND spec-acceptable-by-B's-policy. **Blocks** real BLS verification.
7. **System criome's role** (/214 §11.3, SYS/23 Q3) — full participant under operator-set policy vs machine-identity only.
8. **`target_environment` field on grants** (SYS/142 §"For signal-criome") — proposes adding this so criome-to-criome permission knows which environment it authorizes. Not yet in `signal-criome`.
9. **Owner approval shape: Assert vs Mutate** (SYS/142 §6, Q4) — lean: owner asserts a `SigningDecision` fact, daemon mutates pending authorization state. Belongs in owner-signal-criome design.
10. **Escalation-to-approve configurability** (/214 §11.5, SYS/22 Q7) — per-policy boolean vs scope-pattern predicate.
11. **`RegisterIdentity` placement** (/214 §11.4) — owner-class moves to owner-signal-criome; third-party variant (Developer registers Host) stays on signal-criome by default, but should itself be authorization-gated.
12. **Operator-offline-mid-quorum visibility** (/214 §11.9, SYS/22 Q12) — `ObserveAuthorization` must track solicited-but-not-responded signers. Depends on §11.10 push-stream first.

---

## 6 · Implementation state

### Design landed in

- `criome/ARCHITECTURE.md` (commit `4474bb8`) — single-owner-as-Unix-user; two policy classes; two escalation kinds; ECDH/AEAD owner-session; store-minted slots; expiry/replay constraints.
- `signal-criome/ARCHITECTURE.md` (commit `723e6c8`) — peer + consumer scope; owner moved to owner-signal-criome; peer discovery; routed-authorization relation; policy-satisfaction evidence.
- `criome/skills.md` (store-minted-slots invariant; plaintext-passphrase wording forbidden).
- `criome/flake.nix` (Nix architectural-truth checks: stale plaintext-passphrase wording rejected; `criome-authorization-slots-are-store-minted`; expiry/replay guard check).
- `signal-lojix/horizon-leaner-shape/ARCHITECTURE.md` — canonical `DeploymentRequestDigest` belongs to contract layer; blake3 over rkyv canonical bytes.
- `lojix/horizon-leaner-shape/ARCHITECTURE.md` — "no local Nix, SSH, rsync, GC-root, cache, or activation effect starts until the authorization gate grants the canonical digest and scope."

### Code landed in

| Repo | Branch | Commit | Wired | Stubbed |
|---|---|---|---|---|
| `signal-criome` | main | `9dff026`, `bd98b9d`, `be950e3` | Policy types; denial source; grant.request_slot; round-trip + NOTA witnesses | — |
| `criome` | main | `2b74697`, `73d34bf`, `55077e2d` | AuthorizationCoordinator; Sema tables; CreateAuthorizationState; owner-socket 0600 witness; expiry+replay | Master-key signing; real BLS verification; ObserveAuthorization push stream |
| `signal-lojix` | horizon-leaner-shape | `df49dae1` | DeploymentRequestDigest; digest-stability witnesses | — |
| `lojix` | horizon-leaner-shape | `6a799dac` | CriomeAuthorization actor in runtime root; deployment gate; denial witness | Real signal-criome socket client (fails closed; in-process tests use GrantForTests) |

### Beads

- **`primary-at7x`** (criome routed authorization) — in flight; description needs refresh per /214 §12 to name §11.10 (push stream), §11.11 (real BLS verification), §11.12 (master-key signing). Numbering shifted after OA/150/OA/152.
- **`primary-izze`** (tui-criome) — re-scoped per /214 §12.

---

## 7 · Recommendations for context maintenance

### Retire now (substance migrated; risk of misleading future passes)

- `reports/operator-assistant/148-criome-signature-authorization-decisions-2026-05-17.md` — substance absorbed into criome ARCH §"Authorization model" + /214; stale tui-criome framing risks future misdirection.
- `reports/system-assistant/21-criome-routed-authorization-and-thin-cli-shape-2026-05-17.md` — explicitly superseded by SYS/22's self-audit.
- `reports/system-specialist/140-lojix-criome-mediated-authorization-decision-2026-05-17.md` — superseded by SYS/141 + SYS/142.

### Forward to designer lane for absorption

- `reports/system-specialist/142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md` — corrections not yet in /214: public+unencrypted regular socket (D/214 §1 still draws it as `0660 group criome-peers`); `target_environment` field; `AssertSigningDecision`. Designer should reconcile.
- `reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md` — Q1/Q2/Q3 + new Q10. Designer should fold §11 forward.
- `reports/designer-assistant/116-permission-scoped-signal-contracts-and-sockets-2026-05-17.md` — OwnerSignal discipline should become a skill (`skills/owner-signal.md` or extend `skills/contract-repo.md`) so future contract passes don't re-litigate.

### Forward to operator lane

- `reports/system-specialist/141-lojix-criome-arca-implementation-synthesis-2026-05-17.md` — `DeploymentArtifactSet` nine-digest shape + `NixConfigurationActor` include-point not yet in lojix ARCH. Next lojix operator pass should absorb.
- `reports/operator-assistant/151-lojix-criome-authorization-gate-2026-05-17.md` — next slice (real signal-criome socket client) is named in §"Next Work". Worth a lojix-side bead complementing `primary-at7x`.

### Keep (current working state)

/214 (canonical), OA/149, OA/150, OA/151, OA/152, SYS/22, SYS/23. These form the working set for any next pass.

---

## See also

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — master compendium.
- `reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md` — adjacent lojix arc (CriomeAuthorization gate sits at the boundary).
- `reports/designer/219-persona-orchestrate-state-2026-05-18.md` — adjacent: OwnerSignal discipline is shared between orchestrate and criome.
