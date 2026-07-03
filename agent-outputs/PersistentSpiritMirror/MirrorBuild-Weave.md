# Mirror Build Weave — launch-ready

Epic: **primary-nbmq** — [EPIC] Persistent both-directions quorum-gated Spirit
mirror (router-mediated, no new component). 12 child beads.

Authoritative design: `agent-outputs/PersistentSpiritMirror/MirrorArchitecture-Design.md`
(Build sequence + Pickup map). This weave encodes that build order as dependencies.
Supersedes the discarded direct-mirror epic `primary-1e6b` (all 9 of its beads closed;
see Reconciliation).

Nodes: A = `5::7` (mirror-alpha), B = `5::8` (mirror-beta). Toggle is OFF by default.
Secrets stay out of every bead: no keys, no session material, no tokens are recorded here.

## Beads (id, one-line scope, repo, role, intensity)

| Bead | One-line scope | Repo | Role | Intensity |
|---|---|---|---|---|
| primary-nbmq.1 | Router origination — standing daemon sends a component-object forward on its own (piece 1) | router (+signal-router) | strong Rust implementer | ordinary-implementation |
| primary-nbmq.2 | Spirit authorized-apply ingress — land an arriving record LIVE, quorum re-judged locally (piece 4) | spirit (+signal-spirit) | strong Rust implementer | ordinary-implementation |
| primary-nbmq.3 | DE-RISK milestone — prove ONE direction A→B live WITHOUT quorum (1-of-1 gate) | router+spirit integration test | strong Rust implementer (test author) | ordinary-implementation |
| primary-nbmq.4 | Criome quorum collection — propose→gather→judge→commit driver, withhold-until-authorized (piece 3) | criome (+signal-criome) | strongest Rust implementer (security-strong) | strongest-high-thinking |
| primary-nbmq.5 | Durable outbox + push redial — crash-durable outbound backlog, rehydrate on start (piece 2) | router | strong Rust implementer | ordinary-implementation |
| primary-nbmq.6 | Encrypted authenticated router session + mutual per-session identity proof, forward secrecy (pieces 7+8) | router (+signal-router) | strongest Rust implementer (security/crypto-literate) | strongest-high-thinking |
| primary-nbmq.7 | Off-by-default SetMirrorEnabled toggle on the router meta socket, persisted (piece 6) | router (+meta-signal-router) | strong Rust implementer | ordinary-implementation |
| primary-nbmq.8 | Author spirit.nix — the missing first-class Spirit node module (piece 6) | CriomOS | operating-system-implementer | ordinary-implementation |
| primary-nbmq.9 | Deploy + seed the pair — modules on, MUTUAL identity seed, admit 2-of-2, guest autostart, vmt firewall (piece 6) | CriomOS (+persona-router bootstrap, criome.nix) | operating-system-implementer | ordinary-implementation (deploy-gated) |
| primary-nbmq.10 | Enable BOTH directions autonomously + convergence tests (write-while-peer-down → waits → converge) (piece 5) | integration (all repos, symmetric config) | strong Rust + operating-system-implementer | strongest-high-thinking |
| primary-nbmq.11 | Security AUDIT of the quorum + identity + encryption path | audit over router+criome (read-only) | security-strong auditor (rust-auditor) | strongest-high-thinking |
| primary-nbmq.12 | FINAL PROOF on the two live VMs — both directions live, toggle on, reboot-survivable | CriomOS live VMs | operating-system-implementer | ordinary-implementation (deploy-gated) |

## Dependency graph

```
primary-nbmq.1 (router orig) ─┬─► .3 (one-dir proof) ─► .4 (quorum) ─┬─► .5 (outbox) ─► .6 (enc session)
primary-nbmq.2 (spirit apply)─┘                                      │
                                                                    (.4)─┐
primary-nbmq.1 ─► .7 (toggle) ──────────────────────────────────────────┤
primary-nbmq.8 (spirit.nix) ─────────────────────────────────────────────┤
                                          .6 ──────────────────────────────┤
                                                                          ├─► .9 (deploy+seed) ─► .10 (both dirs) ─┐
                                          .4 ─┬───────────────────────────► .11 (audit) ────────────────────────────┤
                                          .6 ─┘                                                                     ├─► .12 (final live proof)
```

Edges (blocker → blocked):
- .1 → .3 ; .2 → .3
- .3 → .4
- .4 → .5 ; .5 → .6
- .1 → .7
- .8 → .9 ; .7 → .9 ; .4 → .9 ; .6 → .9
- .9 → .10
- .4 → .11 ; .6 → .11
- .10 → .12 ; .11 → .12

No cycles (`bd dep cycles` clean). Full chain renders under `bd dep tree primary-nbmq.12`.

Build-order note (encoded, per the design Build sequence): prove ONE direction live
(.3) BEFORE layering quorum (.4); transport hardening (.5 outbox, .6 session) is
sequenced AFTER quorum. `.5`/`.6` are technically transport-independent of `.4` (their
true prereq is `.1`); the orchestrator MAY pull the router-hardening track parallel to
`.4` once `.1` lands, at the cost of departing from the encoded de-risk order.

## READY TO START NOW (no unmet deps)

| Bead | One-line | Role / intensity | Repo |
|---|---|---|---|
| primary-nbmq.1 | Router origination — standing daemon sends a component-object forward on its own | strong Rust implementer / ordinary-implementation | router (+signal-router) |
| primary-nbmq.2 | Spirit authorized-apply ingress — land an arriving record LIVE, quorum re-judged | strong Rust implementer / ordinary-implementation | spirit (+signal-spirit) |
| primary-nbmq.8 | Author spirit.nix — the missing first-class Spirit node module | operating-system-implementer / ordinary-implementation | CriomOS |

### Serialize vs parallel for the ready set

- All three ready beads are in **different repos** (router, spirit, CriomOS) → **run in parallel**, no file collision.
- **Router-repo collision group: .1, .5, .6, .7** (all touch `router/src` and/or `signal-router`/`meta-signal-router`). Serialize on one checkout, or give each a worktree. Only `.1` is ready now; `.5`/`.6`/`.7` unlock later and must not run concurrently with each other or `.1` on the same checkout.
- **CriomOS-repo collision group: .8, .9.** `.9` depends on `.8`; serialize (natural order).
- **spirit-repo: .2** is the only spirit-source bead; `.3` also touches spirit but as an integration test — low collision.
- **criome-repo: .4** is sole; no collision.
- `.11` (audit) is read-only and can run parallel to `.9`/`.10` once `.4`+`.6` land.

## Roles + intensity per bead (summary)

- Strong Rust implementer (ordinary-implementation): .1, .2, .3, .5, .7
- Strongest Rust implementer, security-strong (strongest-high-thinking): .4, .6
- Operating-system-implementer (ordinary-implementation; .9/.12 deploy-gated): .8, .9, .12
- Strong Rust + operating-system-implementer (strongest-high-thinking): .10
- Security-strong auditor / rust-auditor (strongest-high-thinking): .11

## Reconciliation of the prior weave (epic primary-1e6b — now closed)

All 9 beads of `primary-1e6b` are closed. `primary-1e6b` marked superseded by `primary-nbmq`.

- **Retired / DISCARDED (direct mirror-component path):**
  - `1e6b.5` — direct-mirror sender leg (mirror-shipper feature + `MirrorTarget::Address` → separate mirror daemon over TCP, router not in path). Rejected per the corrected vision. Replaced by router origination `.1` + Spirit apply `.2`.
  - `1e6b.4` — mirror receiver store-row seed. The separate mirror daemon is dropped, so there is no store-row to pre-register. Replaced by Spirit apply ingress `.2`.
  - `1e6b.8` — deferred router-attestation stub. The router-mediated path is now the whole design, fully woven (`.1`, `.5`, `.6`), not parked.
- **Superseded (behavior changed):**
  - `1e6b.3` — one-directional A→B trust seed → now MUTUAL both-directions seeding + admit 2-of-2 contract in `.9`.
  - `1e6b.6` — state-creation-on-A fork → dissolved by pending-proposal semantics (`.2`/`.4`).
  - `1e6b.7` — one-direction direct-path verification → replaced by `.3` (de-risk) and `.12` (final both-directions live).
- **Carried forward (still valid):**
  - `1e6b.1` — guests mirror-alpha `5::7` + mirror-beta `5::8` authored+pushed on goldragon main `824ffe6498c3`; REUSED as nodes A/B. Deploy re-encoded in `.9`.
  - `1e6b.2` — reproject + BootOnce redeploy of the two guests → folded into `.9`.

Pre-existing referenced beads NOT part of the prior weave were left untouched: `primary-85hv`,
`primary-x3l7`, `primary-om4g.1`, `primary-om4g.2`, `primary-sos8` were already CLOSED;
`primary-dw95` (VmHost on prometheus) and `primary-yluj` (spirit redeploy) remain OPEN as
general infra still valid to the deploy tail.
