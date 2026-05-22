# Current state after designer/operator report absorption

## Scope

Read the current designer/operator keeper reports and the fresh operator
reports active as of 2026-05-22. I treated the supersession reports as
canonical for older material rather than re-expanding every historical report.

Key reports absorbed:

- `reports/designer/249-component-intent-gap-analysis.md`
- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
- `reports/designer/263-schema-specification-language-design.md`
- `reports/designer/266-persona-pi-triad-design.md`
- `reports/designer/268-persona-pi-operator-input.md`
- `reports/designer/270-sema-upgrade-component-design.md`
- `reports/designer/271-forge-component-family-design.md`
- `reports/designer/273-schema-migration-synthesis-post-operator-151.md`
- `reports/designer/274-forge-skeleton-reconciliation.md`
- `reports/designer/278-multi-version-daemon-coexistence.md`
- `reports/designer/279-nota-schema-language-and-version-hash.md`
- `reports/designer/280-session-handover-2026-05-22.md`
- `reports/operator/150-triad-signal-sema-migration-current-state.md`
- `reports/operator/153-intent-questions-after-designer-273-274.md`
- `reports/operator/154-spirit-versioned-daemon-cutover.md`
- `reports/operator/155-spirit-double-daemon-deployment-check.md`
- `reports/operator/156-spirit-v0-1-1-staging-and-report-currency.md`
- `reports/second-operator/163-lane-registry-implementation-result-2026-05-22.md`
- `reports/second-operator/165-current-situation-2026-05-22.md`
- `reports/second-operator/166-review-persona-orchestrate-migration-2026-05-22.md`
- `reports/second-operator/167-review-persona-engine-backlog-2026-05-22.md`
- `reports/second-operator/168-review-mind-router-policy-2026-05-22.md`
- `reports/second-operator/169-review-criome-lojix-authorization-2026-05-22.md`

## Situation

The active operational front is Spirit v0.1.1 cutover. The versioned
double-daemon shape exists: v0.1.0 and v0.1.1 daemons run side by side,
with unsuffixed `spirit` still pointing at v0.1.0. Operator `/156` says
v0.1.1 is no longer empty: the staged v0.1.1 database contains migrated
records through record 146 and the v0.1.1 daemon serves it. The system is
not atomically cut over because writes can still land on v0.1.0 after
staging; the next decision is dual-write, default flip with old read-only
fallback, or high-water-mark replay.

The schema-migration design has converged around content-addressable schema
identity. `/279` says the canonical identity is a Blake3 hash of a NOTA
schema language; semver is only a human label if kept at all. The component
schema hash covers public signal types plus private runtime storage wrappers.
Sema-upgrade should read stored schema hashes through a pre-service inspect
socket, not by opening peer databases. Two hard open points remain:
sema-upgrade's own self-upgrade bootstrap and the durable commit-sequence
scope. Designer lean is hand-written self-upgrade until stable and
per-database commit sequence.

The current Signal/Sema/Executor substrate is clear but not widely migrated.
The target is `signal-frame` plus contract-local operations, daemon-local
commands/effects, `signal-executor`, and payloadless `signal-sema`
classification. Spirit is the template. Many contracts are still stale:
mind, router, message, introspect, system, terminal, harness, criome, and
some owner contracts still carry old universal-verb or missing-observable
shape.

Second-operator's immediate implementation target is
`persona-orchestrate`. The lane-registry slice is done and pushed. The next
slice is executor-centered migration: local `Command`/`Effect`, ordinary and
owner lowerers, `signal-executor` request path, Sema observation projection,
and tests proving socket handlers no longer bypass the executor.

Persona engine design still has high-level intent gaps. Designer `/249` says
the engine-manager surface is large and weakly rooted in psyche intent.
Designer `/280` adds a concrete pending item: engine-manager rename axis 2
is not done internally. `signal-persona` wire names moved toward
engine-management, but persona internals and socket constants still carry
supervision language.

Forge direction is clarified but still not implementation-ready. Existing
`forge` and `signal-forge` should be treated as a real criome-stack executor
skeleton, not discarded. The open question is whether `forge-core` becomes a
separate pure-library vocabulary and whether `Deploy` remains in
`signal-forge` or moves toward lojix.

Persona-pi is a real future triad but not ready for code. Its settled shape:
standard triad, dual-path terminal-cell plus harness API, namespace adaptation
from Pi's flat API into typed noun-method records, and Codex arm of composite
designer. The next step is an operator implementation proposal, not a bead
for direct implementation.

## Questions needing psyche attention

1. Spirit cutover path: should the unsuffixed `spirit` temporarily dual-write
   to v0.1.0 and v0.1.1, should it flip to v0.1.1 and make v0.1.0 read-only,
   or should we wait for sema-engine commit-sequence replay before accepting
   more writes through v0.1.0?

2. First production migration rule: is stop-old-start-new explicitly
   acceptable for the first Spirit migration, with commit-sequence replay
   required only from migration 2 onward?

3. Sema-upgrade bootstrap: should sema-upgrade upgrade itself through a
   hand-written bottom-of-stack path until stable, or should it dogfood its
   own machinery immediately?

4. Engine-manager rename axis 2: should persona internals and socket names
   be renamed now from supervision language to engine-management language,
   even if that is an ABI/config break, or should the deferral be explicit?

5. Magnitude collapse: do health/readiness and mind `ItemPriority` collapse
   onto shared `signal-sema::Magnitude`, or do any of those remain distinct
   domain scales?

6. Forge boundary: should existing `forge` remain the criome-stack effect
   executor while `forge-nix-builder` is extracted underneath, and should
   `Deploy` stay in `signal-forge` for now?

7. Persona-pi priority: should the next operator proposal focus on
   persona-pi/composite-designer, or should sema-upgrade and Spirit cutover
   finish first?
