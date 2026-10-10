# Overview — Horizon / Logix rewrite: synthesis, forks, and the path to cutover

Cloud-designer orchestrator synthesis. 2026-06-04. The highest-numbered file
in this meta-report directory — it reconciles the five sub-reports (1 intent
agglomeration, 2 intent-refresh proposals, 3 Horizon simplification, 4 Logix
triad-port, 5 cutover/parity) and the adversarial critique, and reduces them
to the decisions the psyche must make and the actionable sequence that follows.

## The settled picture (decided, do not re-litigate)

- **The split.** Horizon is the minimal projection surface — it emits typed
  cluster facts (WHAT), and Nix composes the decisions (HOW). It stays "a hack
  for now," explicitly NOT a triad component. Logix (lojix) is the traditional
  component that gets the full triad-engine + schema-based-component port.
  (`1bok2bxvu3beswif9mv`, `7ggswqdxqqz97za6o7w`; closes the long-open
  runtime-shape trichotomy `1vymk533`.)
- **Minimal on two axes.** Semantic (facts not decisions) AND type-count (reuse
  the input type as the output type; no parallel in/out shapes; variants over
  booleans). (`7ggsw…`, `10v4744869xt5spwnam`.)
- **Typed-source-first is non-negotiable.** A node feature is a real typed
  `NodeService` variant authored in `goldragon/datom.nota`, projected typed,
  consumed typed — never a string key with an or-empty-list default. The
  VmTesting work was the named anti-pattern. (`431pfi7l1akuu22b01b`.)
- **Logix triad shape.** Two wire contracts (`signal-lojix` ordinary +
  `meta-signal-lojix` policy, born meta- not owner-), each wire-only and
  engine-trait-free; `nexus.schema` + `sema.schema` as separate files INSIDE
  the lojix daemon crate, importing the contract Signal IO; per-plane generation
  by schema-next → schema-rust-next; the deploy pipeline as Nexus
  `CommandEffect`s; the live-set / GC-roots / event-log / container records as
  SEMA tables. This maps cleanly onto the cloud-component template.
- **The goal.** Finish to parity, switch per node (not flag-day), retire the
  dual Stack-A/Stack-B burden. (`75auhtr308tgt4kaa9a`.)

## The decision forks (the big questions for the psyche)

### Fork 1 — Sequencing: port Logix before cutover, or cut over at parity first?

This is the single biggest fork, and it is a genuine tension between two High
intents that no single sub-report owned (critique Miss #1).

- **Port-then-cutover.** Finish the Logix triad port (B2) and the Horizon
  collapse (B1) FIRST, then cut over onto the schema-derived stack. Honors
  "use the designed components fully" (`5wo8xmt0qpl6u6t10md`,
  `6wzz3up583b428kh3ok`). Cleaner end-state. Slower to kill the dual-stack
  burden.
- **Cutover-at-parity-first.** Cut CriomOS over to the current lean lojix
  daemon at functional parity NOW (it still runs the OLD signal stack), killing
  the dual-stack burden fast (`75auhtr…`), then triad-port Logix afterward as
  its own track. Risk: retires Stack A onto a non-triad deployer, partially
  defeating `6wzz…` — and you would re-touch the deployer twice.
- **My recommendation:** a hybrid — treat the **Logix triad port** and the
  **Horizon/CriomOS cutover** as two independent tracks that meet at the end.
  Drive cutover-parity on Horizon+CriomOS (the high-value dual-stack kill) while
  the Logix triad port proceeds in parallel, and cut over onto the *ported*
  daemon once it reaches parity — so Stack A is never retired onto a non-triad
  deployer. This needs the daemon parity (B2 + B3 step 2) and the triad port to
  converge, which they can, since both are pre-cutover worktree work.

### Fork 2 — Horizon collapse: cutover precondition or after, and how far?

Reports 3 and 5 openly disagreed on ordering (critique §2.1): B1 treats the
derived-boolean collapse as THE deliverable; B5 says "cutover does not require
it." Both are right about their own leg — it is a real choice.

- **Depth.** B1's recommendation (which I endorse): MOVE to Nix the `behaves_as`
  9 bools, `type_is`, the gating booleans (`is_dispatcher`, `is_large_edge`,
  `enable_network_manager`), the lid-switch policy, the `at_least_*` ladders
  (by emitting the raw `Magnitude` ordinal), and `extra_groups`. KEEP in Rust:
  arch resolution, the rendered typed name/line newtypes, the cross-node fan-in
  lists, typed validation, and the secret-binding map. Output-only field count
  drops ~30 → under 12; the input type is reused as the output type where
  shape-equivalent. The safety hinge is one CriomOS `derive.nix` that re-exports
  `behavesAs` + ladders from raw facts so consumer modules stay untouched —
  **this is asserted but not verified** to thread through `specialArgs` like
  `horizon` does (critique §2.4); it must be proven, or every consumer changes.
- **Timing.** Precondition = cleaner cutover target but adds a large CriomOS
  consumer-rewrite to the critical path; after = faster dual-stack kill but
  ships a Horizon that still violates `7ggsw…` temporarily.
- **Sub-fork (raw `Magnitude` to Nix?).** Emitting the raw ordinal is the
  purest WHAT-fact, but invites `>=` comparisons scattered across consumers —
  the exact derivation-duplication we are trying to avoid. The `derive.nix`
  re-export mitigates it.
- **My recommendation:** collapse AFTER cutover. Parity is the bar for killing
  the dual stack (the High-priority goal); the collapse is a clean,
  well-scoped follow-on that does not gate retirement. Land the typed-source
  ends and the `derive.nix` seam during cutover so the collapse is a drop-in.

### Fork 3 — Logix authority split + the meta-signal-lojix repo

B2 makes a strong case (Q1): **Deploy / Pin / Unpin / Retire are owner-only**
(`meta-signal-lojix`); **Query / Watch / Unwatch are peer-callable**
(`signal-lojix`). A deploy mutates the live cluster and can break the router —
the strongest possible case for the owner socket. This needs a yes/no, because
it determines a new repo. The repo does NOT exist yet (critique Fork A), and the
cloud port hit the identical gate (its meta repo still uncreated).

- **My recommendation:** confirm the split; carry `meta-signal-lojix` as a
  local path-dep package (named `meta-signal-lojix`) inside the lojix tree until
  cutover — mirroring the cloud `owner-signal-cloud`-package-renamed stopgap —
  and create the real repo at cutover. Defers the deployment-surface commitment
  until parity is proven. And: born **meta-signal-lojix**, never
  owner-signal-lojix (the rename is active fleet work).

### Fork 4 — Apply the intent-refresh agglomerations?

File `2` proposes 7 agglomerations replacing ~21 records with 7 (net ~21→7
reads), raising three to VeryHigh on cross-lane convergence, and removing a
misleading Cert-Zero record and a contradicting Medium. Note: Proposals 1 and 2
would fuse-and-retire four records I captured THIS session (`7ggsw`, `10v47`,
`1bok2`, `75auhtr`) into two VeryHigh charter records — consistent with the
agglomeration principle `1zd6v86uo9ycvuqnk3k`, but worth a conscious yes. All
proposals are PROPOSE-ONLY; nothing was written to Spirit.

- **My recommendation:** apply Proposals 1, 2, 3, 5, 7 (the high-value charter
  fuses + the two that remove misleading artifacts); 4 and 6 are pure
  read-count hygiene, apply if you want the corpus tighter. Capture the fresh
  records first, then issue supersession on the originals.

## Corrections and concrete blockers the critique surfaced

- **Stale claim fixed (report 4 Q4 item 3).** The schema-next nested-resolver
  fix HAS landed — `schema-next` HEAD "preserve resolver through nested
  imports"; `resolution.rs:206` now calls `lower_with_resolver(engine, self)`.
  Report 4 has been corrected inline. Remaining schema-next unknowns for the
  lojix port are real but narrower: the **multi-effect pipeline** through
  `Continue` (cloud only ever ran ONE effect) and **streaming-subscription
  emission** (cloud's ordinary contract has no streams) are both unproven —
  lojix would be the first to exercise them. The cloud generated triad is itself
  NOT yet green (report 22 blockers 1-6 open), so "follow the cloud template"
  means follow the proven SHAPE, not a compiling reference.
- **Hard blocker — local-builds-disabled vs prometheus-must-self-build**
  (critique Risk c / Miss #2). The lojix daemon rejects local builds
  (`deploy.rs:1004`), but intent `mdbr9xbmuzgaxiapyi` requires model-heavy
  prometheus deploys to build ON prometheus (it owns the AI model cache/closure).
  As designed, the daemon cannot deploy the most critical node. This must be
  reconciled before the prometheus cutover step.
- **Cutover safety (B5 §5 is strong).** prometheus LAST, BootOnce
  (`5er7r9fj9whba2ewgit`), router networking intact (`5hir5bnz9af64zjg53d`),
  deploy as a durable systemd transient unit so an SSH drop doesn't strand it
  (`42s92u91qbilshxm6hn`), and verify the **independent backup network** is live
  on the Stack-B generation before the prometheus BootOnce
  (`75uceeptwptwlyciwao`) — B5 under-wove the backup network; add it.
- **Role-merge gap (subject report).** `NodeSpecies` + `NodeService` →
  `roles: Vec<Role>` is settled intent (INTENT.md:41-71) but NOT landed — the
  lean code still has separate `species` + `services`. Either the cutover lands
  it or the psyche confirms it deferred.
- **criomos-horizon-config branch posture** (critique Miss #5). Stack B's
  two-arg `project(horizon, viewpoint)` REQUIRES the `HorizonProposal` from this
  repo, but there is no `horizon-leaner-shape` worktree for it — a load-bearing
  cutover input, not a "worth confirming" footnote.

## The actionable sequence (low-regret, gated on the forks)

Regardless of Fork-1/2 timing, these pre-cutover steps carry zero production
risk (all worktree-only) and should start now:

1. **Close the typed/authored gaps on Stack B** — add the typed
   `NodeService::VmTesting` variant + author the fact in the leaner datom;
   re-derive the leaner goldragon datom clean from current production; convert
   the leftover quoted strings to bracket forms; drop the dead lojix-cli
   flake-lock node. (B5 step 0.)
2. **Field-by-field consumption parity audit** — diff every `horizon.node.*` /
   `cluster.*` / `exNodes.*` read across CriomOS + CriomOS-home against the lean
   `view::Node`; fix the renamed/regrouped reads. The likeliest silent-breakage
   source. (B5 step 1.)
3. **Author the two Logix wire contracts FIRST** (`signal-lojix.schema`
   ordinary, `meta-signal-lojix.schema` policy), wire-only, sharing record
   types; delete the stale three-layer section from signal-lojix and re-target
   to schema-derived per-plane. (B2 steps 1-2, Q5.)
4. **Daemon functional-parity completion** — all four operations, all six
   system actions (especially BootOnce), builder/substituter resolution, the
   secrets axis; resolve the local-builds-disabled-vs-prometheus collision. (B5
   step 2 + the hard blocker above.)
5. **Author the daemon plane schemas + wire build.rs** per the cloud template,
   importing EXACTLY the contract type names (avoid the cloud type-name drift);
   then port the prototype's domain logic into the generated engine impls,
   collapsing the 9-actor topology into three engines + effect handlers + one
   real container-observer actor. (B2 steps 3-5.)
6. **Shadow eval/build parity** — project + Build (not activate) each node on
   Stack B against production facts; diff the toplevel closure vs Stack A. (B5
   step 3.)
7. **Cut over per node** — zeus/tiger first, then non-router cache/builder
   nodes, prometheus LAST with BootOnce + backup-network + transient-unit
   safety; soak through a reboot cycle; then retire Stack A. (B5 steps 4-7.)

The Horizon collapse (Fork 2) slots in either before step 6 (precondition) or
after step 7 (cleanup), per the psyche's call.
