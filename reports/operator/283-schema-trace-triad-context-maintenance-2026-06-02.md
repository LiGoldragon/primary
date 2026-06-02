# Schema Trace Triad Context Maintenance

*Kind: Review · Topics: schema-stack, trace, spirit-next, introspect, triad · 2026-06-02*

## Frame

This is an operator-lane context-maintenance pass over the recent
schema/asschema/spirit-next/trace/introspect/triad report surface. It is
read-only with respect to `schema-rust-next` and `spirit-next` because the main
operator currently holds both repos for typed per-plane trace object work.

The work order itself carried no new durable psyche intent. I did not capture
new Spirit records.

## Current Load-Bearing Spine

### Trace / instrumentation

Current canonical working surface:

- `reports/operator/282-trace-header-generated-interface-situation-2026-06-02.md`
  is the current operator brief. It supersedes string/newtype trace names with
  generated typed trace identity: `TraceInterfaceObject`, `TraceActorObject`,
  `TraceObject`, and `TraceEvent`.
- `reports/designer/471-trace-name-structure-interface-header-2026-06-02.md`
  is the matching designer synthesis. It resolves designer 467's open
  TraceObjectName-vs-enum question in favor of macro-emitted closed enums.
- `reports/operator/280-spirit-next-live-trace-and-triad-situation-2026-06-01.md`
  remains the current implementation landing for the real process-boundary
  trace socket: trace-enabled CLI, daemon binary configuration, rkyv
  `TraceEvent` frames, differentiated Nix packages, and Layer 2 runtime tests.
- `skills/architectural-truth-tests.md` now permanently carries the
  proof-of-usage ladder and the testing-trace socket as the canonical Layer 2
  engine-trait witness.
- `skills/component-triad.md` permanently carries no-NOTA-between-components,
  build-config stratification, runtime triad engine traits, and trace hooks as
  part of engine-trait contracts.

Supersession spine:

1. Operator 277: in-process payload-bearing trace proved real runtime calls.
2. Operator 280: process-boundary trace socket landed.
3. Operator 281: generated engine wrappers and trace hooks became the live
   interface story.
4. Operator 282 + designer 471: next slice is typed generated trace identity,
   not string/newtype activation names.

### Triad actor / interface honesty

Current canonical working surface:

- `skills/component-triad.md` is the permanent rule for Signal/Nexus/SEMA engine
  traits.
- `skills/actor-systems.md` is the permanent rule for runtime roots as actors,
  hidden non-actor owners, and actor trace witnesses.
- `reports/operator/281-generated-interface-logic-with-macros-2026-06-02.md`
  is the current code-facing walkthrough of generated wrappers, inner runtime
  methods, and what still lives too low in `spirit-next`.
- `reports/designer/466-triad-engine-honesty-situation-2026-06-01/3-overview.md`
  remains the current design audit for behavior-level gaps: hidden `Engine`
  owner, full-payload observe output, and Nexus with a projection slot but
  little real decision logic.
- `reports/designer/468-developed-interfaces-spirit-persona-orchestrate-2026-06-02.md`
  is current as the developed-interface expansion source: multi-action roots,
  richer Nexus decision matrices, and the spirit/persona/orchestrate sketches.

### Introspect

Current canonical working surface:

- `reports/designer/469-introspect-component-design-2026-06-02.md` is the
  current introspect design: new `introspect` component, trace destination,
  policy hub, and queryable trace intelligence.
- `reports/designer/470-psyche-backlog-top-6-visual-2026-06-02.md` remains
  current only as a psyche-ratification queue. Its item 1
  `TraceObjectName(String)` shape is now superseded by the typed trace identity
  of operator 282 / designer 471, but its priority ordering is still useful:
  trace-name integration before broader spirit expansion and minimal
  introspect.

### Positive-grep / live witnesses

Current canonical permanent home:

- `skills/architectural-truth-tests.md` §"No positive grep as deployment
  proof" and §"Proof-of-usage ladder".
- `reports/operator/274-live-architecture-witness-research-2026-06-01.md`
  remains a useful cleanup target inventory for `schema-rust-next`,
  `schema-next`, and `nota-next`, but the general rule itself has migrated into
  the skill.

## Stale Or Superseded Reports

### Safe stale candidates after landing verification

Do not delete these today; delete only when the receiving lane verifies the
landing and no open action still points at the report.

- `reports/operator/275-schema-runtime-instrumentation-log-socket-prototype.md`
  is superseded by operator 280 plus `skills/architectural-truth-tests.md` and
  `skills/component-triad.md`. It should drop after confirming no test still
  depends on its exact event-sequence wording.
- `reports/operator/277-spirit-next-testing-trace-implementation-2026-06-01.md`
  is superseded by operator 280 for implementation truth and by operator 282
  for next-slice direction. Keep only until the current active refactor no
  longer needs the e4e5035/5fc9639 provenance.
- `reports/operator/278-gap-vision-and-subagent-implementation-brief-2026-06-01.md`
  is superseded by operator 280, 281, and 282. Its "trait-first" rule is now in
  `skills/component-triad.md`; its socket brief landed.
- `reports/operator/279-actionable-patterns-from-designer-463-2026-06-01.md`
  is superseded by `skills/component-triad.md`,
  `skills/architectural-truth-tests.md`, and operator 282. The only live piece
  is "trace follows the triad," which now belongs in component-triad if more
  wording is needed.
- `reports/operator/276-schema-thread-context-maintenance-2026-06-01.md` is
  superseded by operator 280-282 for trace and by this report for maintenance
  state. Its old immediate queue should no longer drive implementation.

### Forward, not delete yet

- `reports/designer/467-name-only-trace-research-and-prototype-2026-06-02.md`
  is superseded in design by designer 471, but it still names a pushed
  worktree branch and concrete test results. Keep until the main operator
  either integrates or explicitly abandons that branch.
- `reports/designer/470-psyche-backlog-top-6-visual-2026-06-02.md` remains
  forward as a decision queue, but any future paraphrase must update item 1:
  the next trace-name target is generated typed `TraceObject`, not
  `TraceObjectName(String)`.
- `reports/designer/466-triad-engine-honesty-situation-2026-06-01/` remains
  forward until its behavior gaps migrate into repo `ARCHITECTURE.md` files or
  code.
- `reports/operator/274-live-architecture-witness-research-2026-06-01.md`
  remains forward until the named `schema-rust-next`, `schema-next`, and
  `nota-next` positive-grep cleanup is complete or separately tracked.

### Drop candidates only after migration

- Older broad stack reports such as operator 248, 253, 258, 260, and 261
  should not remain just for rationale. Their live schema/asschema/macro
  substance should migrate into `schema-next`, `schema-rust-next`, or
  `nota-next` repo architecture docs when those repos are next touched. Until
  that migration is verified, mark them stale-background rather than deleting.
- Operator 271 remains partly useful for small cleanup inventory
  (`nota-next` parser discipline, CLI NOTA source helper, `SchemaError`
  display), but it is stale as schema-stack current truth. Move any still-open
  cleanup to beads or a newer implementation queue, then retire the report.

## Recommended Migrations

1. `schema-rust-next/ARCHITECTURE.md`: after the active operator slice lands,
   add that route enums are emitted for all plane roots and trace identity is a
   generated closed enum surface (`TraceInterfaceObject`,
   `TraceActorObject`, `TraceObject`), not strings.
2. `spirit-next/ARCHITECTURE.md`: after the active slice lands, replace any
   TraceObjectName/string wording with the generated typed trace header shape;
   keep operator 280's trace socket description as the process-boundary
   witness.
3. `skills/component-triad.md`: only if implementation lands cleanly, tighten
   the instrumentation subsection from "per-plane activation entry points" to
   "per-plane typed trace object values" so permanent discipline stops naming
   string hooks.
4. New `introspect` repo `ARCHITECTURE.md`: when the repo is created or
   entered, migrate designer 469's role split directly: trace destination,
   policy hub, queryable intel source; binary push ingestion; no NOTA between
   components.
5. Beads or a current operator queue: migrate operator 271's leftover small
   cleanup list before deleting that report.

## Open Psyche Questions

These remain user-facing because they decide architecture, not only tasks.

- Should actor-boundary trace and interface-object trace always both fire, or
  should testing configuration choose actor-only / interface-only / both?
- Should generated `Help` exist on every root enum immediately, or only on
  externally visible Signal roots first?
- Should compact headers be generated for every plane root, or only roots that
  cross process boundaries?
- Should extended trace recurse through nested enum payloads until the first
  struct/newtype leaf, or stop at one nested row?
- Should `introspect` store only typed `TraceObject` values, or also store
  pre-rendered display strings for query speed?
- Should the spirit pilot expansion include `Subscribe`, `Update`, and
  `Summarize` now, or trim that developed-interface set for the next slice?

## Main Operator Actions

1. Treat operator 282 + designer 471 as the current trace-name brief. Do not
   implement more string/newtype trace identity unless it is a temporary
   integration step explicitly replaced in the same slice.
2. Use operator 280 as the current implementation truth for trace socket and
   differentiated trace packages.
3. Ignore operator 276's "log-socket next" queue; it was overtaken by the
   socket landing and typed-trace-header design.
4. Do not delete reports during the active refactor. Once the main operator
   lands the typed trace object slice, do a narrow deletion/migration pass over
   operator 275, 277, 278, 279, and 276.
