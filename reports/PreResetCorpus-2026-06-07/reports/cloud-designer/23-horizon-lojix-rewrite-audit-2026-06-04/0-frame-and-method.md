# Horizon / Logix rewrite — deep refresh + porting & simplification audit

Cloud-designer lane. 2026-06-04. **Meta-report directory** (orchestrator
frame + sub-agent reports + synthesis). The session: the psyche asked for a
full refresh on the intent, reports, skills, and repositories of the Horizon
and Logix (`lojix`) rewrite; an audit of what can be **simplified**; and the
**big questions for porting** the components onto the new triad engine and
schema-based component architecture — especially Logix, the more traditional
component. Horizon is "more of a hack for now, and that's fine." The goal is
to **finish the rewrite and cut over**, retiring the dual production/next
deploy-stack burden.

## The psyche's design intent (captured this session)

Five durable records were captured through Spirit before any analysis:

- `7ggswqdxqqz97za6o7w` (Principle, High) — Horizon and the cluster-data it
  carries should be elegant and minimal: express only **what** the psyche (as
  cluster user) wants the cluster to do, never **how** and never
  decision-making. Horizon emits simple typed facts that Nix consumes; **Nix
  composes those facts into the more complex decisions**, so complexity stays
  out of Horizon.
- `10v4744869xt5spwnam` (Principle, High) — Horizon data types should not
  repeat themselves across inputs and outputs: where the input type can also
  serve as the output type, **reuse it** rather than defining parallel in/out
  types. Fewer, reused types keep the model small.
- `1bok2bxvu3beswif9mv` (Clarification, High) — Horizon stays the simple
  projection surface ("a hack for now," acceptable), **not** a full triad
  component; **Logix (lojix)** is the more traditional component that receives
  the full triad-engine + schema-based-component port. This clarifies the
  earlier open runtime-shape record `1vymk533gmb43v78e46` (Medium): Horizon
  leans pure-and-simple, Logix carries the runtime triad.
- `75auhtr308tgt4kaa9a` (Decision, High) — finish the Horizon/Logix lean
  rewrite to cutover and retire the dual production-and-next deploy stacks.
- `1zd6v86uo9ycvuqnk3k` (Principle, High) — intent-refresh by **agglomeration**:
  combine many lower-certainty records that belong together into a single fresh
  higher-certainty record; leverage the certainty ladder to shrink agent
  reading load; retire the agglomerated originals under explicit supersession.

## Context the orchestrator gathered first (read directly, not delegated)

- `protocols/active-repositories.md` — the two-deploy-stack split (Stack A
  production monolith `lojix-cli`; Stack B lean rewrite on
  `horizon-leaner-shape`), the replacement-stack table, cutover discipline.
- `reports/system-designer/70-cluster-data-feature-horizon-criomos-2026-06-04.md`
  — the keystone: the whole `authored NOTA → horizon-rs projection → CriomOS
  Nix → runtime` pipeline, with the VmTesting worked example and the
  typed-source gap.
- `horizon-rs/ARCHITECTURE.md` + `skills.md` + `lib/src/proposal.rs` — the
  input model, the four-bucket sorter, the variant-not-boolean rule, the
  Magnitude ladder, and the in/out duplication (`*Proposal` input vs
  `Node`/`Horizon`/`Cluster` enriched output).
- `lojix/ARCHITECTURE.md` — daemon + thin CLI, owned surface (live-set,
  GC-roots, event-log, container lifecycle), on the **old** signal stack.
- `signal-lojix/ARCHITECTURE.md` — still a **skeleton**; documents a
  three-layer migration onto signal-frame/signal-core/signal-sema, NOT the new
  schema-derived triad. `meta-signal-lojix` does not exist yet.
- `criomos-horizon-config/horizon.nota` — the pan-horizon authored config
  (Stack B only).

Key existing Horizon/Logix intent already in Spirit (informs the agents):
`431pfi7l1akuu22b01b` (cluster-data must be typed end-to-end, typed-source-first),
`1vymk533gmb43v78e46` (runtime-shape open — now clarified by `1bok2bxvu3beswif9mv`),
`3zue95xkt8gzui12cao` (show through a working end-to-end prototype),
`5wo8xmt0qpl6u6t10md` (prototype must use designed components fully),
`6pmeinb6tqtdotsgi4u` (port high-confidence production CriomOS changes into the
rewrite stack), `6wzz3up583b428kh3ok` (schema-deep rewrite on nota-next +
schema-next; deep actor system; method-only Rust; psyche authorizes modifying
schema-next).

## Method — a two-phase, nine-agent fan-out

Phase A (intent) and Phase B (technical) run concurrently; each ends in a
synthesis/critic barrier that needs all of its phase's findings.

**Phase A — deep intent sweep + agglomeration**
- A1 — Spirit sweep, Horizon / cluster-data / criomos-cluster-config intent
  (all-time).
- A2 — Spirit sweep, Logix / lojix / deploy-orchestrator / schema-triad-port
  intent (all-time).
- A3 — legacy substrate sweep: `intent/*.nota` (horizon, deploy,
  component-shape) + the older design reports (designer 207/208/246/248,
  cloud-operator 11, system-operator 167, system-designer 51 schema-arc).
- A4 — agglomerated subject report (fed A1+A2+A3): the intelligible narrative
  of what the psyche wants from the rewrite. → file `1`.
- A5 — intent-refresh proposals (fed A1+A2+A3): clusters of lower-certainty
  records to fuse into single higher-certainty records, with proposed text and
  the originals to retire. → file `2`.

**Phase B — porting & simplification audit**
- B1 — Horizon simplification: which derived fields move to Nix composition,
  how far the output type collapses toward the input type (in/out reuse), the
  leaner model. → file `3`.
- B2 — Logix triad-port big questions: working/policy contract split
  (`signal-lojix.schema` vs `meta-signal-lojix.schema`), nix pipeline as Nexus
  CommandEffects, live-set/GC-roots/event-log as SEMA, the schema-next →
  schema-rust-next generation path, and reconciling the stale three-layer doc.
  Uses the cloud component as the worked template. → file `4`.
- B3 — CriomOS consumption + cutover/parity: what consumes Horizon, the Stack
  A↔B gap, the VmTesting typed-source gap, and the actionable sequence to cut
  over and retire the dual stack. → file `5`.
- B4 — completeness/adversarial critic (fed B1+B2+B3): unanswered big
  questions, risks, and cross-check against intent. Folded into the overview.

**Synthesis (orchestrator)** → file `6-overview.md`: the big questions for the
psyche, and the recommended actionable sequence to finish the rewrite.

All agents are read-only on the repos (design audit, not implementation); they
cite `file:line`; they do not touch `private-repos/`. Findings land as the
numbered files in this directory; the directory is the meta-report and is
garbage-collected as one unit.
