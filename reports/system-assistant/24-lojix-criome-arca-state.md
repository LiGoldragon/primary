# 24 — lojix + criome + arca state (system-assistant view)

State of the deploy-substrate arc as the system-assistant lane sees it,
prepared for the next context. Reads alongside the designer compendiums:

- `reports/designer/215-workspace-state-of-art-2026-05-18.md` — workspace master
- `reports/designer/216-criome-routed-authorization-state-2026-05-18.md` — criome arc
- `reports/designer/221-lojix-arca-horizon-leaner-shape-state-2026-05-18.md` — lojix arc

This report carries what's specific to my lane's view: the question
slate, the bidirectional reconciliation between system-assistant
audits (this lane) and the designer-lane consolidation, plus the
session-end pickup points.

---

## 1 · Where the arc stands

**Code landed.** lojix `horizon-leaner-shape` carries the
`CriomeAuthorization` actor (`lojix 6a799dac`); the
`criome_authorization_denial_blocks_every_fake_nix_effect` witness
proves the SS/141 invariant ("no Nix effect before grant"). signal-lojix
`horizon-leaner-shape` carries `DeploymentRequestDigest` (`signal-lojix
df49dae1`). criome's `AuthorizationCoordinator`, Sema tables,
store-minted slots, expiry+replay, and owner-socket `0600` witness all
landed (`criome 2b74697`, `73d34bf`, `55077e2d`).

**Design settled.** D/214 is canonical for the criome architecture:
per-(host, user) criome; two policy classes (Simple, Complex/quorum);
two escalation kinds (sign, approve); three client classes mapped to
two contracts (`signal-criome` for peers + consumers, future
`owner-signal-criome` for the owner); ECDH-handshake-then-AEAD
owner-session. Per-node four-daemon shape (criome, lojix, arca, nix)
with three-mesh control plane (signal-criome, signal-lojix,
signal-arca).

**Cutover NOT done.** Production stack on `main` still runs the old
monolithic `lojix-cli`; lean rewrite still on `horizon-leaner-shape`
branches. Per `protocols/active-repositories.md` §"Two deploy stacks
coexist".

**Doc drift caught.** `/git/.../signal-lojix/ARCHITECTURE.md` on
`main` still claims skeleton-only; the worktree has implementation.
Update is pending per `reports/designer/221-...` §11.

---

## 2 · Live decisions awaiting psyche direction

In dependency order; smallest, sharpest first.

1. **`SignedObject` canonical bytes** (D/214 §11.7;
   `reports/system-specialist/141-lojix-criome-arca-implementation-synthesis-2026-05-17.md`
   Q3; `reports/system-assistant/22-audit-criome-routed-authorization-arc-2026-05-17.md`
   Q5; `reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md`
   Q4). Which fields are inside the signed digest. Lean: request_id,
   target cluster, target node, action verb, expiry, anti-replay nonce,
   issuing criome identity, target_environment. **Blocks** D/214 §11.12
   master-key signing — the single most load-bearing next operator slice.

2. **Criome receives content + digest, not just digest**
   (`reports/system-assistant/23-...` Q10). BLS verification needs
   original bytes; current `AuthorizeSignalCall` wire is digest-only.
   Falls out of (1) but needs explicit wire shape.

3. **`owner-signal-criome` contract sketch** (D/214 §11.8;
   `reports/system-assistant/23-...` Q6). Request/reply vocabulary +
   ECDH cipher choice (Noise XX vs hand-rolled X25519 + HKDF-blake3 +
   ChaCha20-Poly1305/AES-GCM). Blocks tui-criome + CLI passphrase.

4. **Unattended-system-daemon bootstrap** (D/214 §11.1;
   `reports/system-assistant/22-...` Q4;
   `reports/system-assistant/23-...` Q1). A `lojix-system` user's
   criome has no human at boot. Lean: v1 unencrypted master + filesystem
   permissions; v2 TPM-sealed. **Blocks** cluster-side criome ship.

5. **D/214 ↔ SS/142 reconciliation** (surfaced in my prior chat brief;
   not yet folded). D/214 §1 mermaid draws the peer socket as
   `mode 0660, group criome-peers`; SS/142 says regular `signal-criome`
   is public + unencrypted. Designer-lane to reconcile; concrete edit
   list lives in my chat-only brief from earlier this session (see §4
   below for the residue).

6. **Cross-user-same-host routing scope** (was D/214 §11.2). SS/142
   substantially undercuts this — if the regular socket is public, a
   `lojix-system` process can talk to operator-user-criome's regular
   surface directly. The residual is only peer-discovery (how does
   criome A know criome B's socket path under another user's runtime
   dir). Smaller problem than D/214 framed.

7. **Verifier policy vs originator policy** (D/214 §11.6;
   `reports/system-assistant/22-...` Q10). Wire shape for the
   satisfied-policy spec carried on `SignedObject`.

---

## 3 · Lojix-side gaps carried forward from SS/18

These are lojix-mesh-specific (separate from the criome-side list
above). Currently captured in
`reports/system-assistant/23-most-relevant-questions-after-d214-op149-op150-2026-05-17.md`
§4. Repeated here for the next-session pickup:

- **Peer-daemon discovery** for `peer_daemons` runtime population (static config v1).
- **`DeploymentReleased { request_id }`** wire signal so builder/cache/target can release GC roots.
- **Concurrent-deploy + network-partition mid-transfer** failure-mode coverage.
- **`CancelDeployment` wire shape** with explicit cancellation scope variants.
- **Per-deploy observability granularity** (per-phase default, per-derivation opt-in).
- **Concurrent deploys to same target** queuing/rejection policy (per-target activation lock + FIFO-with-rejection in v1).
- **`idempotency_key` on `wire::DeploymentSubmission`** — cheap, do before any consumer beyond the current authorization-gate skeleton ships.

---

## 4 · Concrete D/214 edits the designer-lane should pick up

From the cross-reading I did of `reports/designer/214-criome-architecture-record-2026-05-17.md`
against the canonical `criome/ARCHITECTURE.md` (`4474bb8`) and
`reports/system-specialist/142-criome-public-socket-and-deploy-approval-clarification-2026-05-17.md`:

1. **§1 mermaid:** strike `(mode 0660, group criome-peers)` from `peerA`. The canonical ARCH leaves the peer socket permissions unspecified, consistent with the SS/142 public-socket reading.
2. **§2 Security model:** add a sub-section distinguishing owner-socket trust (Unix-user via mode `0600`) from regular-`signal-criome` trust (signatures + receiving-daemon policy; public reachability is by design).
3. **§7 client-classes table:** add a footnote noting consumer + peer-signer share a public socket; only the owner contract gets mode-`0600` enforcement.
4. **§11.2 (cross-user-same-host routing):** narrow to just the peer-discovery residual described in §2 above.
5. **§11.7 (`SignedObject` canonical bytes):** absorb SS/142's `CriomePermissionGrant` field enumeration — `target_environment`, `authorized_action_scope`, `authorized_object_bytes_or_canonical_ref`, etc.
6. **§6 (Two escalation kinds):** name the owner approval verb — SS/142's lean is `Assert SigningDecision`.

---

## 5 · Side notes worth keeping (not actionable yet)

- **note: workspace canonical for the deploy CLI repo is `lojix`** (directory name; `skills/stt-interpreter.md` table). Both "lojix" and "logix" are STT-heard forms; the canonical for verbatim records is the directory-derived form. This session captured psyche statements with several STT artifacts (logic steam → lojix daemon; Nyx cache → Nix cache; next store → Nix store; ARCA/SEMA → Arca/sema); intent files now hold the canonical normalisations.
- **possibly useful: criome IS a PKI** (`reports/system-assistant/22-...` §7.4; D/214 §13). ClaviFaber registers nodes, criome masters anchor identity, peer routing is intrinsic. Makes TLS for cross-host transport much cheaper; unifies cross-component trust resolution. Worth keeping visible as cross-host transport gets designed.
- **undecided: whether to retire `reports/system-assistant/22-...` and `reports/system-assistant/23-...` after D/216/D/221 absorb them.** Both still cited as load-bearing in D/216 §2; safest to keep until designer explicitly absorbs into ARCH text.

---

## 6 · Next-session pickup points

When the next system-assistant session opens:

1. Read this report + the three designer compendiums above. Sufficient to re-orient on the arc state.
2. Watch for landed answers to §2 questions — if any have moved (especially Q1 SignedObject bytes, Q4 unattended-bootstrap), update §2 and propagate to D/216 + D/221.
3. Check whether the §4 D/214 edit list has landed (designer-lane work) — if so, this report can shrink.
4. If `reports/designer/215-workspace-state-of-art-2026-05-18.md` has been refreshed for the 2026-05-19 day, fold accordingly.

This report itself retires when (a) all §2 questions have answers, (b) §4 edits land, and (c) §3 gaps are either addressed in code or migrated to a successor working artifact.
