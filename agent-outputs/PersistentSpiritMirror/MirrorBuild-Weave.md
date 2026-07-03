# Mirror Build Weave — launch-ready

Epic: **primary-nbmq** — [EPIC] Persistent both-directions quorum-gated Spirit
mirror (router-mediated, no new component). 13 child beads.

Authoritative design: `agent-outputs/PersistentSpiritMirror/MirrorArchitecture-Design.md`
(Build sequence + Pickup map). This weave encodes that build order as dependencies.
Supersedes the discarded direct-mirror epic `primary-1e6b` (all 9 of its beads closed;
see Reconciliation).

Nodes: A = `5::7` (mirror-alpha), B = `5::8` (mirror-beta). Toggle is OFF by default.
The live two-VM proof (`.12`) is the psyche's actual done-bar.
Secrets stay out of every bead: no keys, no session material, no tokens are recorded here.

## Progress

- **DONE (closed-with-evidence, pushed):** `.1` router self-origination, `.2` Spirit authorized-apply live ingress, `.3` A→B live join + Spirit origination rework, `.4` Criome quorum collection, `.6` mutual identity proof + encrypted session, `.7` off-by-default toggle, `.8` spirit.nix module.
- **IN PROGRESS:** `.5` durable outbox + push redial (on the router checkout).
- **READY NOW:** `.11` security audit (parallel track — reads the `.4`/`.6` code, needs no deploy).
- **Endgame remaining:** `.9` deploy/live-wiring, `.10` both-directions + Spirit async rewire, `.12` live two-VM proof (done-bar), `.13` router ARCHITECTURE consolidation.
- Edge fix + Wave-3 fold-ins applied — see below.

## Beads (id, one-line scope, repo, role, intensity)

| Bead | One-line scope | Repo | Role | Intensity | State |
|---|---|---|---|---|---|
| primary-nbmq.1 | Router origination — standing daemon sends a component-object forward on its own (piece 1) | router (+signal-router) | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.2 | Spirit authorized-apply ingress — land an arriving record LIVE, quorum re-judged (piece 4) | spirit (+signal-spirit) | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.3 | ONE-direction A→B live join (1-of-1) + Spirit origination rework (hand to local router; removed shipper.rs/mirror-shipper/mirror crate) | spirit source + router integration | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.4 | Criome quorum collection — propose→gather→judge→commit driver, withhold-until-authorized (piece 3) | criome (+signal-criome) | strongest Rust implementer (security-strong) | strongest-high-thinking | DONE |
| primary-nbmq.5 | Durable outbox + push redial — crash-durable outbound backlog, rehydrate on start (piece 2) | router | strong Rust implementer | ordinary-implementation | IN PROGRESS |
| primary-nbmq.6 | Encrypted authenticated router session + mutual per-session identity proof, forward secrecy (pieces 7+8) | router (+signal-router) | strongest Rust implementer (crypto-literate) | strongest-high-thinking | DONE |
| primary-nbmq.7 | Off-by-default SetMirrorEnabled toggle on the router meta socket, persisted (piece 6) | router (+meta-signal-router) | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.8 | Author spirit.nix — the missing first-class Spirit node module (piece 6) | CriomOS | operating-system-implementer | ordinary-implementation | DONE |
| primary-nbmq.9 | Deploy + seed + LIVE-WIRE the pair — enable encrypted session on the standing daemon, criome recipient/route bootstrap, mutual identity seed, admit 2-of-2, autostart, vmt firewall, Spirit working-socket perms (piece 6) | CriomOS (+persona-router bootstrap, router daemon config, criome.nix) | operating-system-implementer (+ router-bootstrap Rust) | ordinary-implementation (deploy-gated) | blocked by .5 |
| primary-nbmq.10 | BOTH directions autonomously + convergence tests + Spirit async propose→completion rewire (from 1-of-1 gate to quorum boundary) (piece 5) | integration (all repos; Spirit source rewire) | strong Rust + operating-system-implementer | strongest-high-thinking | blocked by .9 |
| primary-nbmq.11 | Security AUDIT of the quorum + identity + encryption path (+ plaintext-migration path, caller-supplied round ids) | audit over router+criome (read-only) | security-strong auditor (rust-auditor) | strongest-high-thinking | READY |
| primary-nbmq.12 | FINAL PROOF on the two live VMs — both directions live, toggle on, reboot-survivable (DONE-BAR) | CriomOS live VMs | operating-system-implementer | ordinary-implementation (deploy-gated) | blocked by .10,.11 |
| primary-nbmq.13 | Consolidated router ARCHITECTURE.md update (pieces 1/2/6/7/8) — single doc writer after the router track | router (docs only) | architecture-editor / router-track Rust | ordinary-implementation | blocked by .5 |

## Dependency graph

```
[.1 ✓]─┬─►[.3 ✓]─►[.4 ✓]─┬─► .5* (outbox) ─┬─► .9 (deploy+live-wire) ─► .10 (both dirs + async rewire) ─┐
[.2 ✓]─┘         [.6 ✓]───┤                 │                                                          │
[.6 ✓]───────────────────►.5*               ├─► .13 (router ARCH.md)                                   │
[.1 ✓]─►[.7 ✓]───────────────────────────────┤ (also .6,.7 → .13)                                      ├─► .12 (live proof, DONE-BAR)
[.8 ✓]───────────────────────────────────────┤                                                         │
[.4 ✓]+[.6 ✓] ──────────────────────────────► .11 (audit, READY now, parallel) ─────────────────────────┘
```
(`✓` closed, `*` in progress.)

Edges (blocker → blocked):
- .1 → .3 ; .2 → .3   (done)
- .3 → .4   (done)
- **.4 → .5 ; .6 → .5**   (edge fixed: `.5` now depends on `.6`, reversed from the stale `.5→.6`)
- .1 → .7   (done)
- .8 → .9 ; .7 → .9 ; .4 → .9 ; .6 → .9 ; **.5 → .9**   (added: deploy ships the durable outbox)
- .9 → .10
- .4 → .11 ; .6 → .11   (both done → .11 READY)
- .10 → .12 ; .11 → .12
- .5 → .13 ; .6 → .13 ; .7 → .13

No cycles (`bd dep cycles` clean).

## Home-stretch plan (endgame ready/sequencing)

| Bead | Waits on | Unblocks | Role / intensity | Repo(s) |
|---|---|---|---|---|
| `.5` (outbox) — IN PROGRESS | .4 ✓, .6 ✓ | .9, .13 | strong Rust / ordinary | router |
| `.11` (audit) — READY NOW | .4 ✓, .6 ✓ | .12 | security-strong auditor / strongest-high-thinking | read-only over router+criome |
| `.9` (deploy + live-wire) | .4✓ .6✓ .7✓ .8✓ + **.5** | .10 | operating-system-implementer (+router-bootstrap Rust) / ordinary (deploy-gated) | CriomOS + persona-router bootstrap + router daemon config + criome.nix |
| `.13` (router ARCH.md) | .5, .6✓, .7✓ | — | architecture-editor / ordinary | router (docs) |
| `.10` (both dirs + async rewire) | .9 | .12 | strong Rust + operating-system-implementer / strongest-high-thinking | integration (all repos; Spirit source) |
| `.12` (live two-VM proof, DONE-BAR) | .10, .11 | — (final) | operating-system-implementer / ordinary (deploy-gated) | CriomOS live VMs (5::7, 5::8) |

Ready-timing:
1. **Now:** launch `.11` (audit) in parallel; `.5` is in flight.
2. **When `.5` lands:** `.9` (deploy/live-wire) and `.13` (router doc) become ready. `.13` can run parallel to `.9`/`.10` (single router-doc writer; no code collision since it waits on `.5`).
3. **When `.9` lands:** `.10` (both directions + Spirit async rewire).
4. **When `.10` AND `.11` land:** `.12` — the live-on-the-metal proof, the psyche's done-bar.

Serialize/parallel: `.11` is read-only → parallel to the whole deploy chain. The deploy
chain `.9 → .10 → .12` is serial. `.13` is docs-only, parallel once `.5` lands. `.5`/`.13`
both touch the router checkout but never concurrently (`.13` waits on `.5`).

## Wave-3 fold-ins (handoff flags now in the tracker)

- **Edge fix → `.5`/`.6`:** reversed the stale `.5→.6` to `.6→.5` (`.6` ran first and exposes the session-up seam `.5` consumes); the `.6` worker had to `--force` past the old edge. Graph is now truthful.
- **Added edge `.5 → .9`:** the deployed pair must ship the durable outbox, so deploy waits on `.5` (matches the "after `.5`" endgame framing).
- **(1) Deploy live-wiring → note on `.9`:** standing router daemon still uses the plaintext `None` prover — enable the encrypted session via `RouterNetworkConfiguration::criome_session_listening` (`router/src/daemon.rs`) plus the mutual identity→key seed and peer/route bootstrap; the router bootstrap needs a `RegisterActor{ComponentSocket(criome_socket)}` recipient, a direct-message channel grant, and remote-route/peer entries per router; `persona-router.nix` is stale vs current `router_write_bootstrap.rs`; plus the `.8` Spirit working-socket UMask/socket-mode fix.
- **(2) Spirit async rewire → note on `.10`:** `.10` also owns switching Spirit origination from the 1-of-1 gate (`.3`) to the async propose→completion quorum boundary (`.4`).
- **(3) Auditor scope → note on `.11`:** (a) the router ingress DUAL-ACCEPTS the encrypted session AND legacy plaintext `ForwardMessage` during migration (tunnelled forward still carries its per-forward criome attestation) — audit the plaintext path and when to close it; (b) quorum-round ids are caller-supplied — collision is fail-SAFE (votes bind to the operation via signatures) but a liveness concern; assess binding the round id to the operation digest.

## Reconciliation of the prior weave (epic primary-1e6b — closed)

All 9 beads of `primary-1e6b` are closed; `primary-1e6b` superseded by `primary-nbmq`.

- **DISCARDED (direct mirror-component path):** `1e6b.5` mirror-shipper sender leg, `1e6b.4` mirror receiver store-row seed, `1e6b.8` deferred router-attestation stub.
- **Superseded:** `1e6b.3` one-directional seed → mutual seeding in `.9`; `1e6b.6` state-creation fork → pending-proposal semantics (`.2`/`.4`); `1e6b.7` one-direction verify → `.3` + `.12`.
- **Carried forward:** `1e6b.1` guests `5::7`/`5::8` (reused as A/B) and `1e6b.2` their deploy → re-encoded in `.9`.

Pre-existing referenced beads left untouched: `85hv`, `x3l7`, `om4g.1`, `om4g.2`, `sos8`
were already CLOSED; `dw95` (VmHost) and `yluj` (spirit redeploy) remain OPEN infra.
