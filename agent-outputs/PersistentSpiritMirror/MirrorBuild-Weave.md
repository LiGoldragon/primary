# Mirror Build Weave — launch-ready

Epic: **primary-nbmq** — [EPIC] Persistent both-directions quorum-gated Spirit
mirror (router-mediated, no new component). 13 child beads.

Authoritative design: `agent-outputs/PersistentSpiritMirror/MirrorArchitecture-Design.md`
(Build sequence + Pickup map). Supersedes the discarded direct-mirror epic
`primary-1e6b` (all 9 of its beads closed; see Reconciliation).

Nodes: A = `5::7` (mirror-alpha), B = `5::8` (mirror-beta). Toggle is OFF by default.
The live on-metal two-VM proof (`.12`) is the psyche's actual done-bar.
Secrets stay out of every bead: no keys, no session material, no tokens are recorded here.

## Progress (home stretch)

- **DONE (closed-with-evidence, pushed):** `.1 .2 .3 .4 .5 .6 .7 .8 .9 .11`.
  - `.9` closed its CODE+MODULE surface (M1 plaintext door shut; M2 verifier/prover wired when criome-socketed; M3 Quorum-default + `quorumContracts` 2-of-2 seeding; deploy modules validated + pushed — router `24592be8`, signal-router `81c39d85`, CriomOS `e838bba5`). Its LIVE-INSTANTIATION moved to the head of `.12`.
  - `.11` security audit closed; its should-fixes routed to the `.10` tail.
- **IN PROGRESS:** `.10` both-directions + Spirit async propose→completion rewire (over the encrypted session; audit-tail attached).
- **READY NOW:** `.13` router ARCHITECTURE.md consolidation (parallel, docs-only; `.5/.6/.7` done).
- **DONE-BAR:** `.12` now = live instantiation + on-metal both-directions proof; waits only on `.10` (`.11` done).

## Beads (id, one-line scope, repo, role, intensity)

| Bead | One-line scope | Repo | Role | Intensity | State |
|---|---|---|---|---|---|
| primary-nbmq.1 | Router origination — standing daemon sends a component-object forward on its own (piece 1) | router (+signal-router) | strong Rust implementer | ordinary | DONE |
| primary-nbmq.2 | Spirit authorized-apply ingress — land an arriving record LIVE, quorum re-judged (piece 4) | spirit (+signal-spirit) | strong Rust implementer | ordinary | DONE |
| primary-nbmq.3 | A→B live join (1-of-1) + Spirit origination rework (removed shipper.rs/mirror-shipper/mirror crate) | spirit + router integration | strong Rust implementer | ordinary | DONE |
| primary-nbmq.4 | Criome quorum collection — propose→gather→judge→commit driver, withhold-until-authorized (piece 3) | criome (+signal-criome) | strongest Rust (security-strong) | strongest-high | DONE |
| primary-nbmq.5 | Durable outbox + push redial — crash-durable outbound backlog, rehydrate on start (piece 2) | router | strong Rust implementer | ordinary | DONE |
| primary-nbmq.6 | Encrypted authenticated router session + mutual identity proof, forward secrecy (pieces 7+8) | router (+signal-router) | strongest Rust (crypto-literate) | strongest-high | DONE |
| primary-nbmq.7 | Off-by-default SetMirrorEnabled toggle on the router meta socket, persisted (piece 6) | router (+meta-signal-router) | strong Rust implementer | ordinary | DONE |
| primary-nbmq.8 | Author spirit.nix — the missing first-class Spirit node module (piece 6) | CriomOS | operating-system-implementer | ordinary | DONE |
| primary-nbmq.9 | Deploy CODE+MODULE surface — encrypted-session/quorum wiring + deploy modules (M1/M2/M3). Live-instantiation moved to .12 | router + signal-router + CriomOS | operating-system-implementer (+router Rust) | ordinary | DONE |
| primary-nbmq.10 | BOTH directions + convergence + Spirit async propose→completion rewire, OVER the encrypted session (no plaintext fallback); +audit should-fix tail | integration (all repos; Spirit source) | strong Rust + operating-system-implementer | strongest-high | IN PROGRESS |
| primary-nbmq.11 | Security AUDIT of the quorum + identity + encryption path (should-fixes → .10 tail) | audit over router+criome | security-strong auditor (rust-auditor) | strongest-high | DONE |
| primary-nbmq.12 | LIVE INSTANTIATION (flake bump, goldragon exNodes, BLS key exchange/two-pass deploy, activation) + on-metal both-directions proof — DONE-BAR | external repos + goldragon + CriomOS live VMs | operating-system-implementer | ordinary (deploy-gated) | blocked by .10 |
| primary-nbmq.13 | Consolidated router ARCHITECTURE.md update (pieces 1/2/6/7/8) — single doc writer | router (docs only) | architecture-editor / router-track Rust | ordinary | READY |

## Dependency graph (remaining)

```
[.1..9 ✓, .11 ✓]

.10* (both dirs + async rewire, over encrypted session) ──► .12 (live instantiation + on-metal proof, DONE-BAR)
.11 ✓ ─────────────────────────────────────────────────────►  (satisfied)

.5 ✓ / .6 ✓ / .7 ✓ ──► .13 (router ARCHITECTURE.md, READY, parallel, unblocks nothing)
```
(`✓` closed, `*` in progress.)

Remaining edges (blocker → blocked):
- .10 → .12 ; .11 ✓ → .12   (so `.12` waits ONLY on `.10`)
- .5 ✓ → .13 ; .6 ✓ → .13 ; .7 ✓ → .13   (so `.13` is READY)

No cycles.

## Home-stretch plan (to the done-bar)

| Bead | Waits on | Unblocks | Role / intensity | Repo(s) |
|---|---|---|---|---|
| `.10` both dirs + async rewire — IN PROGRESS | .9 ✓ | .12 | strong Rust + operating-system-implementer / strongest-high | integration (all repos; Spirit source) |
| `.13` router ARCHITECTURE.md — READY NOW (parallel) | .5✓ .6✓ .7✓ | — | architecture-editor / ordinary | router (docs) |
| `.12` live instantiation + on-metal proof — DONE-BAR | **.10** (.11 ✓) | — (final) | operating-system-implementer / ordinary (deploy-gated) | external repos + goldragon + CriomOS live VMs (5::7, 5::8) |

Ready-timing:
1. **Now:** `.10` is in flight; `.13` is ready and runs parallel (docs-only, no code collision — its router deps are all closed).
2. **When `.10` lands:** `.12` unlocks — the only remaining gate, since `.11` is done.
3. **`.12` is the done-bar:** flake.lock bump first (router `24592be8`, criome `8fbde55`, spirit `7fc43d6`), then goldragon exNodes for `mirror-alpha`/`mirror-beta`, the post-boot BLS key exchange / two-pass deploy, then live activation + the on-metal both-directions proof.

## Wave-4 record (the `.9` split + fold-ins)

- **`.9` closed (code+module surface).** M1/M2/M3 mechanisms + deploy modules (`persona-router.nix`, `criome.nix`, `spirit.nix` UMask `0007`, `criomos.nix` gated-inert, per-guest autostart) validated and pushed.
- **Live-instantiation → head of `.12`** (note): (i) `flake.lock` bump router→`24592be8`, criome→`8fbde55`, spirit→`7fc43d6` (FIRST; eval needs external horizon); (ii) goldragon exNodes for `mirror-alpha 5::7`/`mirror-beta 5::8` carrying the PersonaRouter payload (peers, criome-recipient `actorHome` endpoint `/run/criome/criome.sock`, peer→local-criome grant), `services.criome.enable` + `quorumContracts` 2-of-2 over both host names, `services.spirit.enable` + `workingSocketGroupAccess`, `peerIdentitySeeds`; (iii) post-boot BLS public-key exchange / two-pass deploy; (iv) live activation + on-metal both-directions proof.
- **`.10` fold-in (note):** M1 makes the encrypted session the ONLY peer path once criome-socketed — the async propose→completion rewire MUST run over the session (no plaintext fallback); preserve withhold-until-authorized + the independent apply re-judge. **Tail (audit should-fixes):** bind round-ids to the operation digest, drop non-member votes, add the two missing negative tests — split to a follow-on if `.10` defers.

## Reconciliation of the prior weave (epic primary-1e6b — closed)

All 9 beads of `primary-1e6b` are closed; `primary-1e6b` superseded by `primary-nbmq`.

- **DISCARDED (direct mirror-component path):** `1e6b.5` mirror-shipper sender leg, `1e6b.4` mirror receiver store-row seed, `1e6b.8` deferred router-attestation stub.
- **Superseded:** `1e6b.3` one-directional seed → mutual seeding (now in `.12` instantiation); `1e6b.6` state-creation fork → pending-proposal semantics (`.2`/`.4`); `1e6b.7` one-direction verify → `.3` + `.12`.
- **Carried forward:** `1e6b.1` guests `5::7`/`5::8` (reused as A/B) and `1e6b.2` their deploy → re-encoded in `.9`/`.12`.

Pre-existing referenced beads left untouched: `85hv`, `x3l7`, `om4g.1`, `om4g.2`, `sos8`
were already CLOSED; `dw95` (VmHost) and `yluj` (spirit redeploy) remain OPEN infra.
