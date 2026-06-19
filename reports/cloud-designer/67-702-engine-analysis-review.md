# 67 · Review of designer report 702 (deep engine analysis) — a cloud-designer read

Reading of `reports/designer/702-deep-engine-analysis/` (15 files, ~3,800
lines): the prime designer's deep architectural audit of the
schema-derived engine stack. This is a *review of the review* — does 702
hold up, what does it miss even after its own completeness pass, and what
does it mean for the cloud lane, which 702 names but never audited.

I read all 15 files end to end and independently corroborated the
keystone cross-stack risk (the kameo split-brain) and the one cloud claim
against the live lockfiles at `/git/github.com/LiGoldragon`. The verdict
below distinguishes what I verified from what I take on the report's word.

## 1 · Is the audit trustworthy? Yes — and the structure is why

702 is not a single pass dressed up as rigor; the rigor is structural,
and it shows in the parts that *fail* gracefully:

- **The adversarial ledger actually downgraded findings.** 6 of 30
  adjudicated P1/P2 findings were struck (`12-adversarial-verification.md`):
  mentci alone lost 3 to *phantom-file citations* — the lane cited
  `nexus.schema` / `sema.schema` / `FrameEscalation` that don't exist
  (only `schema/lib.schema` does). A pass that never downgrades anything
  is rubber-stamping; this one removed a fifth of its own findings and
  named the engine whose evidence was least trustworthy. The 80% survival
  rate is the right kind of number — high enough that the lanes were
  disciplined, low enough that the skeptic wasn't asleep.
- **The synthesis folds only Confirmed findings.** It explicitly refuses
  to carry the 6 downgrades as standing risks and relegates their
  grounded residue to P3 beads. That is the correct discipline and it is
  rare — most audits let a refuted-but-scary finding survive in the
  headline because it reads well.
- **Soundness-vs-surface is the spine, and it bites the right targets.**
  The audit-precision rule ("what does the *production daemon* do, not
  what a `#[cfg(test)]` harness *can* do") is what produces the central
  result: every component engine has the *logic* for its role, and almost
  none of it is reachable from a running daemon. criome's quorum is real
  but spirit never calls criome; router's matcher is live in-process but
  wire-unreachable; mirror's restore can't serve exactly-D; mentci closes
  a verdict into a never-read `Vec`. That pattern — correct library, no
  daemon caller — is the honest shape of the stack and the report is right
  to make it the headline.

Where I'd *trust but verify*: every "deployed" claim in 702 is
source-compiled-offline, never a built artifact. The report says so
itself (`13-completeness.md` (b), Seam 3) — no lane ran a nix/flake
build of any audited HEAD. That caveat is load-bearing for §3 below.

## 2 · The keystone risk, independently corroborated

The #1 ranked risk — the kameo fork split-brain — is the one finding the
whole synthesis leans on, and it's the one no *per-engine* lane saw (only
the completeness critic, looking across crates). Because it carries that
much weight, I re-derived it from the lockfiles rather than trust the
summary. It holds, with one refinement:

| Daemon | kameo resolved | triad-runtime pin | patches kameo |
|---|---|---|---|
| criome / router / mentci | fork `f491b45d` | `f46f66e` | yes |
| **cloud** | fork `f491b45d` | `f46f66e` | yes (`Cargo.toml:59-60`) |
| spirit | **stock `0.20` AND fork `f491b45d`** | `f46f66e` | no |
| mirror | stock only | `f46f66e` | no |

Two confirmations and one addition:

- **Confirmed:** criome/router/mentci run the fork; mirror runs stock;
  every daemon pins triad-runtime `f46f66e` (which declares stock kameo)
  and the fork-takers override via `[patch.crates-io]`. So triad-runtime
  — the shared codegen runtime leg both codegen audits depend on — is
  compiled against a kameo it was never pinned against, in exactly the
  daemons that took the fork. 702's framing is exact.
- **Refinement 702 didn't quite make:** spirit's lockfile carries *both*
  runtimes. Its production daemon links stock (Cargo.toml stock dep, no
  patch), but its dev/test closure resolves the fork too — pulled in by
  the `router`/`criome` dev-dependencies that declare kameo by git. The
  consequence is sharp: **the single green in-process e2e that is the
  propagation loop's only proof (`11-propagation-loop.md`) compiles an
  in-process `CriomeRoot` actor on fork-kameo beside spirit's own actors
  on stock-kameo.** The split-brain is not merely a deploy-fleet
  inconsistency — it is *live inside the one test that proves the loop
  green*. 702 said "spirit runs stock"; the lock says "spirit's daemon
  runs stock, its loop-prover links both." This strengthens, not weakens,
  the report's verdict: the loop is `PartialGreen` partly because its
  proof runs two actor runtimes in one process and nobody checked they
  agree on lifecycle/shutdown semantics.

## 3 · The gap the audit names but under-scopes: the fleet-fix bead

702's completeness critic correctly lists the fork-takers as criome,
router, mentci **plus cloud plus ~10 more** (message, introspect, mind,
terminal, repository-ledger, orchestrate, domain-criome, harness). But
the synthesis's own P1 remediation bead reads:

> "pick one runtime for **criome/router/mentci/spirit/mirror**, bump every
> triad-runtime pin…"

That names the **5 audited daemons** and silently drops the ~10
unaudited fork-takers and cloud — the exact daemons the completeness
critic flagged as the larger, unwitnessed surface. The bead's "whole
fleet" is the audited subset, not the fleet. This is the one place the
synthesis lets the crate-boundary frame leak back in after the critic
explicitly broke out of it. **The fleet-runtime decision has to enumerate
every `[patch.crates-io] kameo` holder, not the five the audit happened
to open** — otherwise the "one runtime for the whole fleet" fix lands on
a third of the fleet and the split persists in the daemons nobody looked
at. (Cheap to make exhaustive: `grep -l 'kameo.git' */Cargo.toml` across
the org enumerates the fork camp.)

## 4 · The cloud lane — what this means for my own just-shipped work

The completeness critic singles out cloud: *"the single most-changed
unaudited daemon … +1199 DigitalOcean Phase 1 … a new sema-engine `Store`
consumer, took the kameo fork. Zero coverage."* That is the DO Phase-1
work from the cloud-operator handoff (report 66, bead `primary-hpkj`).
Three things follow, all in-lane:

1. **Cloud is in the split-brain set — confirmed above.** The DO Phase-1
   daemon links fork-kameo `f491b45d` and pins triad-runtime `f46f66e`,
   identical to criome/router/mentci. Whatever fleet-runtime decision 702
   forces (risk #1), **cloud rides it** — and cloud is one of the daemons
   the bead omits. The cloud-operator integration on `cloud` main should
   not land a triad-runtime pin bump in isolation; it should wait for or
   join the fleet decision, or it re-forks the very inconsistency the
   audit flagged.
2. **The live path dodges most of the actor-runtime risk — for now.** The
   cloud DO live path is the synchronous `Store` (blocking `ureq`), not an
   actor-mediated path; the kameo fork's lifecycle/shutdown-semantics
   changes bite the *actor* surfaces (mailbox, supervision, shutdown). So
   the Tier-1 lifecycle I proved green is largely insulated from the fork
   question. But the moment cloud's daemon actor (the triad `EngineActor`
   shell) is the thing under test — Tier-2, the full daemon chain — it
   runs on fork-kameo, and "does cloud's actor agree with criome's on
   shutdown outcome" becomes a real question for any cross-daemon flow.
   This is a concrete reason the Tier-2 handoff (report 66 P2) should not
   be treated as a pure wiring exercise.
3. **Cloud needs a lane.** 702 audited mirror (the 690 gap) but left
   cloud, `upgrade`, and ~10 daemons unwitnessed. Cloud is now a
   production compute-provider surface with a new storage consumer and
   zero architectural review. The right next designer move for *my* lane
   is a cloud engine audit on the same template (invariants →
   soundness-vs-surface → the Store-consumer `FamilyDirectory` question
   `4-sema-engine.md` raised: does cloud's directory actually apply every
   row, or is it part of the storage TCB taken on trust). That audit is
   also where the image-home Decision (`ad53`) gets reflected into
   `cloud/INTENT.md`.

## 5 · Where I'd push back on the ranking

The eight ranked risks are all real (all Confirmed). Two ordering notes:

- **Kameo at #1 over the criome-gate-absent at #2 is defensible but not
  obvious.** The kameo split is a *latent* coherence risk — nothing has
  been observed to break; the fork's changed shutdown semantics *might*
  violate an actor invariant, and no lane proved they don't (or do). The
  criome-gate-absent (#2) is a *present, structural* intent violation:
  spirit ships outbound to a mirror with no authorization step, which the
  High-certainty records `d6he`/`nfvm`/`2st7` explicitly forbid, and it's
  the defining axis of the first production milestone. If the ranking
  metric is "gates the first milestone," #2 outranks #1. 702 ranks by
  blast radius (the fork touches every daemon) rather than by milestone
  centrality — a legitimate choice, but the synthesis should say which
  metric it's using, because the two orderings disagree at the top.
- **The true root is the missing nix witness (currently a P2 bead).**
  Every "deployed" claim, the kameo divergence, and the
  audited-source-vs-deployed-binary gap all collapse into one missing
  artifact: no flake build of any HEAD. Until that exists, "criome
  enforces quorum on the production path" and "the deployed binary runs
  the fork" are *both* unwitnessed assertions. I'd argue the nix witness
  is upstream of risk #1 — you can't even *confirm* the split-brain ships
  without it — so it reads low at P2. It's the cheapest thing on the list
  and it's the thing that turns every other claim from "source says" to
  "binary does."

## 6 · Net

702 is the strongest audit in the 690→702 line: deeper, adversarially
honest, and the first to break the crate-boundary frame (the kameo
finding only exists because one lane looked across lockfiles). Its
self-discipline — downgrading its own findings, folding only Confirmed
ones — is what makes it trustworthy. The two things I'd change are both
scope, not substance: the fleet-runtime bead must enumerate *all*
fork-takers (cloud + ~10, not the audited 5), and the nix-witness bead
should rank as the precondition it actually is.

For the cloud lane specifically: cloud is confirmed in the fork camp, the
synchronous live path insulates Tier-1 from the actor-runtime risk but
Tier-2 does not get that pass, and cloud has earned its own engine audit —
the same template, owned here.
