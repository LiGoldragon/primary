# 142 — Epic synthesis: the router ⇄ criome cross-host foundation

*The psyche asked for everything done in this epic. This is the capstone. The arc:
a status question — "where are we with the router, and passing criome messages to
other criome daemons across the network?" — turned into a worked foundation. Over
this session the cross-host transport went from "L0 loopback on a branch" to
**proven delivering across two real kernels under KVM**; the shared component
vocabulary, the router-sole fan-out surface, a scoped fork-safety guard, and the
admission ceremony all landed on merge-ready branches; the design forks that gated
everything were resolved and grounded against Spirit; and the remaining work was
handed to the lanes that own it. Method throughout: background multi-agent
`Workflow`s with adversarial (often mutation-tested) verification, on
`~/wt` feature branches — I moved no code-repo `main`.*

## 1 — The arc

1. **Status, verified not recited** (137). Four grounded readers swept the live
   code. The picture corrected my own stale notes: the router transport was far
   more built than "ZERO," criome↔criome was design-only, and the realness ladder
   sat at L0-on-a-branch.
2. **"Take on all the work"** → the 138 foundation. Phase 1 (four parallel
   tracks): cleared the router transport P1s, recommended the criome wire-crypto
   direction, built `signal-standard`, and investigated the "quorum bug" —
   correctly finding it *wasn't* one. Phase 2: built and **ran** the two-kernel
   nixosTest, then polished it from receipt-proof to delivery-proof.
3. **Designer handoff** (688) → 139–141. Both decisions I was holding on were
   already settled this session; I grounded them against Spirit, reconciled the one
   divergence, and built the now-unblocked work: the router-sole `Attend`/`Withdraw`
   fan-out surface and the scoped attested-moment majority guard.
4. **"Take all of it"** → 142 (this). Handoffs packaged, the deploy bead filed,
   and Phase 1 of the remainder launched: the Woe-4 `signal-criome` migration and
   the `criome.nix` deploy module.

## 2 — The branch fleet (all merge-ready; operator owns the merge to main)

| Branch | Repo(s) | What it delivers | Verification |
|---|---|---|---|
| `cluster-root-admission-ceremony` | criome | offline tool minting a cluster-root-signed `RegistrationStatement` the `ClusterRoot::admits` gate accepts | reviewed clean; real BLS; impostor rejected; persisted-key reload byte-identical |
| `transport-p1-fixes-138` | router | 5 P1 fixes + **fenced `AcceptFixedTestIdentity` out of the production daemon path** (refuses to start vs. silently insecure) | sound; build reproduced w/ forced recompile |
| `transport-two-kernel-e2e-138` | router | **L1**: transport across two real kernels + `message-router.nix` + deploy encoders + `forward-probe` + cross-VM harness witness | **ran GREEN under KVM** (×2); delivery mutation-proven |
| `signal-standard-bootstrap` | signal-standard | shared 14-variant `ComponentKind` + `Differentiator` + 4-rung interest lattice (reconciles 7+9+9 rosters) | sound; `nix flake check` green; freshness proven |
| `attested-moment-majority-guard-139` | criome | scoped `:578` fork-safe majority guard (`required > authorities.len()/2`) | **sound, no defects**; 6 boundary tests; mutation fails only at `n=2/r=1` |
| `attendance-fanout-139` (+`-compat`) | signal-standard / signal-router / router | router-sole `Attend`/`Withdraw` subscribe + reference-fanout, keyed by the interest lattice | sound, merge-ready; matcher mutation-verified; gating P2 closed |

In flight (workflow `wyxr0kx2k`):

| Branch | Repo | What |
|---|---|---|
| `signal-criome-positional-migration-142` | signal-criome | Woe-4: migrate off retired field-label syntax so it lowers on current schema-next main |
| `criome-nixos-module-142` | criome | `criome.nix` deploy module (sibling to `message-router.nix`) |

## 3 — The realness ladder (report 136)

- **L0** in-process loopback — done.
- **L1** two real kernels, real VM network, **delivery witnessed** — **done, GREEN
  under KVM.** The single biggest advance of the epic: at session start this was
  unbuilt; it now boots two qemu guests, forwards `192.168.1.1→.2`, and a harness
  witness on the far guest decodes the delivered message — mutation-proven (gating
  the harness connection fails the delivery assertion).
- **L2** routed over Yggdrasil peers — ahead (Phase 2 + deploy bead `primary-ymww`).
- **L3** real ouranos ⇄ prometheus over the mesh — ahead (needs real-host access;
  system-operator).

## 4 — Design decisions & reconciliations

- **Criome is the agreement-and-authorization *organ* of Telos, not Telos
  itself** (corrected the earlier conflation); the quorum is criome's universal
  primitive.
- **Cross-host transport = two lanes** (`lt44`): the router is the general
  payload-blind fabric, *and* criome gets a direct criome-to-criome peer lane for
  time-sensitive agreement (quorum signing, crystallized-time windows; BLS
  aggregate verify a v1 requirement). This refined my initial "ride the router for
  everything" (138/2) — general traffic rides the router; time-sensitive agreement
  uses the direct lane.
- **Router-sole fan-out** (`m0p2`): the router is the sole operational matcher;
  criome emits references and keeps **no operational delivery registry**. This made
  the attendance table router-local and *light* (not a governed criome contract),
  and resolved the `m0p2`/`l2ha` fork I was holding on.
- **The quorum guard is two sites, not one** — the epic's sharpest reconciliation.
  `Threshold::validate_shape` (`:414`, general m-of-n) stays caller-declared; a
  `>n/2` rewrite there would regress legitimate `required=1`/unanimity policies.
  `AttestedMoment::rejection_reason` (`:578`, the time-attestation / head-quorum
  path) is where strict majority belongs, because a decentralized quorum clock
  (`ay3y`) and quorum-backed objects (`m0p2`) must not be single-node-attestable.
  Both the designer (Woe-3) and I (138/4) were right about our respective sites; the
  hazard was applying the guard to the wrong one. Built scoped to `:578`.
- **`signal-standard`** is the new second shared `signal-` library: one
  closed-but-partitioned 14-variant roster in five zones, the `Differentiator`, and
  the interest lattice — cross-imported so router and criome share one matcher
  definition (retiring the report-135 drift risk).

## 5 — Intent grounding & corrections

I grounded the designer's handoff directly against Spirit (the forwarded-handoff
gap-check) and found the captures sound — `m0p2` (router-sole), `lt44` (two lanes),
`9s52` (per-Unix-user self-quorum; `n=1` the single-machine degenerate case),
`gc0n` (closed verdict), `ay3y` (crystallized-past clock) all confirm. No new
capture was owed (the prompts were task orders / proposals / status, not durable
intent); the designer owned the `m0p2` clarify and the `wckt`→`lt44` supersession.
Corrections I made to my own paper trail: **retracted 137 §7.3** (the quorum
"bug"), refined **138/2** (two lanes), reconciled **138/4** (two sites).

## 6 — Handoffs

- **Operator** (owns code-repo main): merge the fleet, and the **Woe-4 field-label
  migration is provably blocking** — `router/main` throws 69 errors against current
  `signal-router/main`. The integration sequence is in 141. My in-flight Phase 1
  delivers the `signal-criome` half of that migration on a branch. Advances
  existing beads — the router transport bead (`primary-9x9f`), the positional /
  structural-forms migration epic (`primary-cxyf`, which my `signal-criome`
  migration falls under), criome routed-auth (`primary-at7x`), and criome
  BLS/master-key (`primary-kr40`, which the admission ceremony advances).
- **System-operator** (owns OS/platform/deploy): the deploy ladder — now filed as a
  bead (the cross-host transport deploy work, `primary-ymww`) pointing at report
  140. Ready-now items (KVM CI host for L1; enable Yggdrasil for L2) are not gated
  on a code merge.
- **Held, deliberately not done autonomously**: creating the `signal-standard`
  GitHub remote (outward-facing — confirm first; operator-assigned) and the L3
  real-host deploy (needs real `ouranos`/`prometheus` access).

## 7 — What's still mine, ahead (Phase 2, after the migration lands)

- The **milestone-3 criome forward-attestation client** — lifts the
  `CriomeVerifierUnavailable` refusal Track A installed, enabling true-BLS
  attestation on the transport (the `#1` path); depends on the `signal-criome`
  migration landing.
- The **L2 Yggdrasil-routed two-node nixosTest** — the next ladder rung above L1.

## 8 — Method

Every substantive piece ran as a background `Workflow` with an adversarial verify
stage; the strongest findings came from **mutation testing** (the L1 delivery
witness, the fan-out matcher, the `:578` guard each proven to *fail* when the fix
is reverted). Honesty held under that pressure: Track D's agent **declined to
"fix" a non-bug** that would have regressed real policies; a reviewer caught that a
"clippy-clean" claim only held under one feature set; and the fan-out build
**surfaced the Woe-4 integration hazard** (the 69-error router/signal-router skew)
that confirmed the critical path rather than papering over it. No code-repo `main`
was moved; the whole epic lives on feature branches for operator to integrate.

## 9 — The paper trail

`137` (status, verified) · `138/0–6` (foundation: P1s, wire-crypto rec,
signal-standard, quorum non-bug, L1 nixosTest) · `139` (unblock + Woe-3
reconciliation) · `140` (system-operator deploy handoff) · `141` (fan-out + `:578`
guard landed) · `142` (this epic). Plus the deploy bead `primary-ymww`.
