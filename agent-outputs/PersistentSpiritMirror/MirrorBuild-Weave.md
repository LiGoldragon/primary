# Mirror Build Weave — launch-ready

Epic: **primary-nbmq** — [EPIC] Persistent both-directions quorum-gated Spirit
mirror (router-mediated, no new component). 13 child beads.

Authoritative design: `agent-outputs/PersistentSpiritMirror/MirrorArchitecture-Design.md`
(Build sequence + Pickup map). This weave encodes that build order as dependencies.
Supersedes the discarded direct-mirror epic `primary-1e6b` (all 9 of its beads closed;
see Reconciliation).

Nodes: A = `5::7` (mirror-alpha), B = `5::8` (mirror-beta). Toggle is OFF by default.
Secrets stay out of every bead: no keys, no session material, no tokens are recorded here.

## Progress

- **Wave 1 DONE (closed-with-evidence, pushed):** `.1` router self-origination, `.2` Spirit authorized-apply live ingress, `.8` spirit.nix node module.
- **Wave 2 (ready now):** `.3` one-direction A→B join (next on the de-risk path), `.7` toggle (parallelizable side-task).
- Wave-1 handoff flags folded in — see "Wave-1 fold-ins" below. New bead `.13` added for the consolidated router ARCHITECTURE.md.

## Beads (id, one-line scope, repo, role, intensity)

| Bead | One-line scope | Repo | Role | Intensity | State |
|---|---|---|---|---|---|
| primary-nbmq.1 | Router origination — standing daemon sends a component-object forward on its own (piece 1) | router (+signal-router) | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.2 | Spirit authorized-apply ingress — land an arriving record LIVE, quorum re-judged (piece 4) | spirit (+signal-spirit) | strong Rust implementer | ordinary-implementation | DONE |
| primary-nbmq.3 | ONE-direction A→B live join (no quorum, 1-of-1) + Spirit origination rework (hand to local router; rip out shipper.rs/mirror-shipper/mirror crate) | spirit source + router integration test | strong Rust implementer | ordinary-implementation | READY |
| primary-nbmq.4 | Criome quorum collection — propose→gather→judge→commit driver, withhold-until-authorized (piece 3) | criome (+signal-criome) | strongest Rust implementer (security-strong) | strongest-high-thinking | blocked by .3 |
| primary-nbmq.5 | Durable outbox + push redial — crash-durable outbound backlog, rehydrate on start (piece 2) | router | strong Rust implementer | ordinary-implementation | blocked by .4 |
| primary-nbmq.6 | Encrypted authenticated router session + mutual per-session identity proof, forward secrecy (pieces 7+8) | router (+signal-router) | strongest Rust implementer (crypto-literate) | strongest-high-thinking | blocked by .5 |
| primary-nbmq.7 | Off-by-default SetMirrorEnabled toggle on the router meta socket, persisted (piece 6) | router (+meta-signal-router) | strong Rust implementer | ordinary-implementation | READY |
| primary-nbmq.8 | Author spirit.nix — the missing first-class Spirit node module (piece 6) | CriomOS | operating-system-implementer | ordinary-implementation | DONE |
| primary-nbmq.9 | Deploy + seed the pair — modules on, MUTUAL identity seed, admit 2-of-2, guest autostart, vmt firewall; +Spirit working-socket perms fix | CriomOS (+persona-router, criome.nix) | operating-system-implementer | ordinary-implementation (deploy-gated) | blocked |
| primary-nbmq.10 | Enable BOTH directions autonomously + convergence tests (write-while-peer-down → waits → converge) (piece 5) | integration (all repos) | strong Rust + operating-system-implementer | strongest-high-thinking | blocked |
| primary-nbmq.11 | Security AUDIT of the quorum + identity + encryption path | audit over router+criome (read-only) | security-strong auditor (rust-auditor) | strongest-high-thinking | blocked by .4,.6 |
| primary-nbmq.12 | FINAL PROOF on the two live VMs — both directions live, toggle on, reboot-survivable | CriomOS live VMs | operating-system-implementer | ordinary-implementation (deploy-gated) | blocked by .10,.11 |
| primary-nbmq.13 | Consolidated router ARCHITECTURE.md update (pieces 1/2/6/7/8) — single doc writer after the router track | router (docs only) | architecture-editor / router-track Rust | ordinary-implementation | blocked by .5,.6,.7 |

## Dependency graph

```
[.1 done] ─┬─► .3 (one-dir join + Spirit orig rework) ─► .4 (quorum) ─┬─► .5 (outbox) ─► .6 (enc session) ─┐
[.2 done] ─┘                                                          │                                   ├─► .13 (router ARCH.md)
                                                                      │                          .7 ──────┘
[.1 done] ─► .7 (toggle) ───────────────────────────────────────────┤
[.8 done] ──────────────────────────────────────────────────────────┤
                                                    .6 ───────────────┤
                                                    .4 ───────────────┼─► .9 (deploy+seed) ─► .10 (both dirs) ─┐
                                                    .4 ─┬────────────► .11 (audit) ───────────────────────────┤
                                                    .6 ─┘                                                     ├─► .12 (final live proof)
```

Edges (blocker → blocked):
- .1 → .3 ; .2 → .3   (both done → .3 READY)
- .3 → .4
- .4 → .5 ; .5 → .6
- .1 → .7   (done → .7 READY)
- .8 → .9 ; .7 → .9 ; .4 → .9 ; .6 → .9
- .9 → .10
- .4 → .11 ; .6 → .11
- .10 → .12 ; .11 → .12
- .5 → .13 ; .6 → .13 ; .7 → .13

No cycles (`bd dep cycles` clean). Full chain renders under `bd dep tree primary-nbmq.12`.

Build-order note (encoded, per the design Build sequence): prove ONE direction live
(.3) BEFORE quorum (.4); transport hardening (.5 outbox, .6 session) is sequenced AFTER
quorum. `.5`/`.6` are technically transport-independent of `.4` (true prereq is `.1`, now
done); the orchestrator MAY pull the router-hardening track parallel to `.4`, at the cost
of departing from the encoded de-risk order.

## READY TO START NOW (Wave 2)

| Bead | One-line | Role / intensity | Repo |
|---|---|---|---|
| primary-nbmq.3 | ONE-direction A→B live join (no quorum, 1-of-1) + Spirit origination rework (hand to local router; remove shipper.rs / mirror-shipper feature / mirror crate); build `ApplyAuthorizedRecord` exactly as `.2` defined | strong Rust implementer / ordinary-implementation | spirit source + router integration test |
| primary-nbmq.7 | Off-by-default SetMirrorEnabled toggle on the router meta socket (persisted, default OFF) | strong Rust implementer / ordinary-implementation | router (+meta-signal-router) |

`.3` is THE next critical de-risk bead. `.7` is off the critical path (a deployment piece
needed later by `.9`) but is unblocked now — slot it opportunistically.

### Serialize vs parallel for the ready set

- **`.3` now touches Spirit SOURCE** (origination rework: hand to local router, remove shipper.rs/mirror-shipper/mirror crate) **plus router integration tests.** No active Spirit collision (`.2` is done).
- **Router collision group is now `.5/.6/.7/.13`** (all touch `router/src`, `signal-router`/`meta-signal-router`, or `router/ARCHITECTURE.md`). Of these only `.7` is ready now.
- **`.3` and `.7` both touch the router checkout** (`.3` integration tests, `.7` router src + meta-signal-router). Prefer **separate worktrees**, or serialize them on one checkout. They are otherwise independent (different files; `.3`'s Spirit-source half is a different repo).
- Everything downstream (`.4` criome, `.5/.6` router, `.9/.10/.12` CriomOS/live, `.11` audit) stays blocked until `.3` (and, for `.11`, `.4`+`.6`) lands.

## Wave-1 fold-ins (handoff flags now in the tracker)

- **(a) Frame contract → note on `.3`:** the router→Spirit join must build `ApplyAuthorizedRecord` exactly as `.2` defined — fields `record_identifier`, hex-encoded rkyv `VersionedCommitLogEntry`, hex-encoded rkyv signal-criome `Evidence`; enforce fail-closed on apply the binding `evidence.operation == OperationDigest::from_bytes(versioned_entry.entry_digest())`.
- **(b) Spirit origination rework → folded into `.3` scope (note):** `.2` deferred handing Spirit's entry to its LOCAL router and removing `shipper.rs` / the `mirror-shipper` feature / the old `mirror` crate (ripping them earlier would have broken `.2`'s green origination path). Now in scope for `.3` since `.1` has landed. Not lost.
- **(c) Router ARCHITECTURE.md consolidation → new bead `.13`:** `.1` deferred the router doc; the design assigns Router ARCHITECTURE a CONSOLIDATED update spanning pieces 1/2/6/7/8. `.13` is the single doc writer, blocked by `.5/.6/.7`. `.5/.6/.7` carry a note: land CODE only, defer the doc to `.13`.
- **(d) Spirit working-socket perms → note on `.9`:** Spirit's WORKING socket is umask-derived (not group-accessible; only the meta socket is hardcoded 0600). For the co-resident router to dial it at deploy, `.9` must set a looser systemd `UMask` or add a `signal-spirit` socket-mode field. Cross-referenced in `.3`.

## Roles + intensity per bead (summary)

- Strong Rust implementer (ordinary-implementation): .1(done), .2(done), .3, .5, .7
- Strongest Rust implementer, security-strong (strongest-high-thinking): .4, .6
- Operating-system-implementer (ordinary-implementation; .9/.12 deploy-gated): .8(done), .9, .12
- Strong Rust + operating-system-implementer (strongest-high-thinking): .10
- Security-strong auditor / rust-auditor (strongest-high-thinking): .11
- Architecture-editor / router-track Rust (ordinary-implementation): .13

## Reconciliation of the prior weave (epic primary-1e6b — now closed)

All 9 beads of `primary-1e6b` are closed. `primary-1e6b` marked superseded by `primary-nbmq`.

- **Retired / DISCARDED (direct mirror-component path):**
  - `1e6b.5` — direct-mirror sender leg (mirror-shipper feature + `MirrorTarget::Address` → separate mirror daemon over TCP, router not in path). Replaced by router origination `.1` + Spirit apply `.2`.
  - `1e6b.4` — mirror receiver store-row seed. The mirror daemon is dropped. Replaced by Spirit apply ingress `.2`.
  - `1e6b.8` — deferred router-attestation stub. The router-mediated path is now the whole design (`.1`, `.5`, `.6`).
- **Superseded (behavior changed):**
  - `1e6b.3` — one-directional trust seed → MUTUAL both-directions seeding + admit 2-of-2 in `.9`.
  - `1e6b.6` — state-creation fork → pending-proposal semantics (`.2`/`.4`).
  - `1e6b.7` — one-direction direct-path verify → `.3` (de-risk) and `.12` (final both-directions live).
- **Carried forward (still valid):**
  - `1e6b.1` — guests mirror-alpha `5::7` + mirror-beta `5::8` (authored+pushed on goldragon main `824ffe6498c3`); REUSED as nodes A/B, deploy re-encoded in `.9`.
  - `1e6b.2` — reproject + BootOnce redeploy → folded into `.9`.

Pre-existing referenced beads NOT part of the prior weave were left untouched: `primary-85hv`,
`primary-x3l7`, `primary-om4g.1`, `primary-om4g.2`, `primary-sos8` were already CLOSED;
`primary-dw95` (VmHost on prometheus) and `primary-yluj` (spirit redeploy) remain OPEN as
general infra still valid to the deploy tail.
