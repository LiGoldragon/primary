# 138/5 — Synthesis: what landed, and three decisions for the psyche

*The psyche said "take on all the work yourself with subagents." Phase 1 ran four
tracks (build→adversarially-verify / panel→synthesis). All four returned clean,
honest results — including one that correctly declined to act. This file
synthesizes and surfaces the decisions that are genuinely the psyche's.*

## What landed (Phase 1)

| Track | Outcome | Status | Lands |
|---|---|---|---|
| A — router transport P1s | all 5 defects fixed; offline test-identity fenced out of production; reviewer **sound**, build reproduced | **pushed** branch `transport-p1-fixes-138` (`39ec67e9`) off `router-network-transport` | operator rebases router main |
| B — criome cross-host wire-crypto | recommend **ride the router transport** (9 vs TLS 4, SSH 3); criome moves nothing | **proposal** (138/2) | psyche decision → then Spirit + ARCHITECTURE.md |
| C — `signal-standard` crate | 14-variant roster + differentiator + lattice; reviewer **sound**, `nix flake check` green | **local** repo + branch `signal-standard-bootstrap` (`3f9d75ee`); no remote | operator creates remote + pushes |
| D — quorum "bug" | **not a bug** — correct m-of-n threshold guard; a `>n/2` rewrite would regress | **no change** (correctly) | designer corrects 685; I retracted 137 §7.3 |

Net: the nearest real win (the cross-host **transport**) is now merge-ready on a
branch; the shared component vocabulary exists and builds; the cross-host
**quorum** direction has a grounded recommendation; and a false bug was caught
before anyone "fixed" it.

## Three decisions for the psyche

### Decision 1 — criome cross-host transport direction (138/2)

Adopt **ride-the-router** (criome solicitations are routed objects the router
forwards; criome verifies the inner BLS envelope end-to-end; criome opens no
sockets)? This is the architecture's deliberately-open slot, so it's yours to
affirm. Affirming it unblocks designing the **milestone-3 criome
forward-attestation client** (the thing Track A's `CriomeVerifierUnavailable`
refusal waits for) and the cross-host quorum **return leg**. The four design
items (addressing-table mapping, return leg, replay-ownership, envelope binding)
are mine to specify once the direction is set.

### Decision 2 — registry owner, which gates the subscribe/fan-out surface (Phase 2 Track E)

Report 135 §3's still-open fork, now blocking: who owns the attendance matcher?
**Router-sole-matcher** (criome emits unfiltered references, router holds the
table and fans out — the `l2ha`-faithful reading) vs **criome-keeps-its-own +
router-also** (double filter). This is an **intent-layer contradiction** between
`m0p2` ("criome pushes to affected components") and `l2ha` ("the router matches
and fans the references out"), so per the ask-when-contradicted rule I will not
unilaterally build the router `Attend`/`Withdraw` surface to one side. Your call
resolves it and drives the `m0p2` `Clarify`/`Supersede`. (Note: signal-standard
now exists to key whichever table wins.)

### Decision 3 — report 685's Woe-3 is wrong (138/4)

The cross-machine quorum guard is a correct configurable m-of-n threshold check,
not a broken majority check; `majority`/`n/2`/`half` appear nowhere in criome.
Report 685 (a `designer/` file, not my lane to edit) should be corrected/closed
so no operator turns it into a regression. How do you want it handled —
designer-lane correction, or a Spirit note? (Report 137 §7.3 already retracted.)

## Phase 2 status

- **Track F — DONE, L1 GREEN under real KVM (138/6).** The two-kernel
  `runNixOSTest` built **and ran** (exit 0, reproduced twice): two separate
  kernels, a real guest-to-guest hop (192.168.1.1→.2), a real minted-slot durable
  receipt, and the loop guard refusing a `Forwarded` frame cross-kernel —
  assertions mutation-proven to bite. Reviewer: **MERGE**. Branch
  `transport-two-kernel-e2e-138` (polish `453bc281`), pushed. Offline-verifier
  mode (real-criome-BLS is milestone 3, Decision 1). The polish pass closed all
  three P3s: L1 **now proves delivery-to-the-actor** over the VM network (a
  cross-VM harness witness, mutation-proven), the node IPs are pinned, and the
  benign early-eof log is quieted — re-run GREEN under KVM.
- **Held pending Decision 2:** the router `Attend`/`Withdraw` subscribe/fan-out
  surface (Track E) — it commits to one side of the `m0p2`/`l2ha` contradiction.
- **Held pending Decision 1:** the milestone-3 criome forward-attestation client
  + cross-host quorum wiring.

## Intent gate

The prompt was a task order, not durable intent → no capture. Track B may warrant
a Decision **if** the psyche affirms the direction (then Record + reflect into
both ARCHITECTURE.md files). Track D warrants a report correction, not an intent
record. No unilateral capture taken.
