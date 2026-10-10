# 272.1 — Verification

## Summary

Designer report 449 is directionally correct and identifies the
right dominant stale clusters. Its exact priority distribution is stale
or internally inconsistent against live `bd` output, but the headline
open-bead count still matches.

The verified safe implementation surface is bead cleanup, not source
code. No source edit is required for this pass.

## Live counts

`bd count --status open` returned `269`.

`bd --readonly count --status open --by-priority` returned:

- P0: 1
- P1: 64
- P2: 156
- P3: 48

Report 449 names 269 open beads but also says "1 P0, 67 P1, 162 P2,
48 P3", which sums to 278. The current live priority distribution is
therefore not the report's distribution. The discrepancy does not
invalidate the stale-cluster diagnosis.

## Confirmed intent anchors

Recent Spirit records queried through the deployed `spirit` CLI
confirm the supersession anchors used by report 449:

- Spirit 1287, 1290, and 1292 establish the body-stream and
  `NotaBodyDecode` substrate, replacing wrapper-level macro handoff.
- Spirit 1294 and 1295 retire the dishonest enum-body shorthand and
  move schema source to structurally honest variant declarations.
- Spirit 1297 authorizes strict current prototype syntax rather than
  compatibility paths.
- Spirit 1300, 1301, and 1302 collapse semantic source/artifact splits
  when they describe the same object.
- Spirit 1305 through 1314 establish upgrade as SEMA-on-Asschema,
  schema-daemon as the schema editor, and the transitory-database
  upgrade pattern.
- Spirit 1315 through 1317 confirm recent churn in Spirit query
  design, but do not alter the bead-staleness verdict.

Designer 444, 446, and 447 were re-read. They support report 449's
central claim: the current stack work is schema-emitted Signal/Nexus/SEMA,
with the spirit fold as Phase 0, wave-1 ports after, schema-core
extraction before stateful wave-2 ports, and upgrade-as-SEMA replacing
the old handover mechanism.

## Confirmed stale clusters

The following clusters are still open in the live bead store and match
report 449's stale diagnosis.

### Persona-spirit handover and v0.1.x cutover

Verified open examples:

- `primary-602y` — rebuild persona-spirit v0.1.0.1 retrofit against
  current signal-frame.
- `primary-0jjz` — execute spirit v0.1.0 to v0.1.1 brief-outage
  cutover.
- `primary-1jql` — in-transition messages probe in the legacy
  nspawn handover test.
- `primary-ekxx` — promote signal-version-handover to schema-derived.
- `primary-x3ci` and `primary-x3ci.1` — v0.1.1 production cutover and
  pre-migration step.

The bead bodies are explicitly about the legacy persona-spirit
cross-version handover or its production deployment ceremony. Designer
447 and Spirit 1305-1314 replace that mechanism with schema-edit SEMA
operations and an upgrade daemon pipeline.

### signal_channel macro and Tap observability substrate

Verified open examples:

- `primary-3cl1` — `signal-frame-macros` `frame_micro()` projection in
  `signal_channel!`.
- `primary-bg9l` and `primary-l02o` — LogSummary/LogVariant observability
  on the legacy signal-frame macro path.
- `primary-v5n2`, `primary-ezqx`, `primary-ezqx.1`, `primary-ezqx.3`,
  and `primary-muu2` — consolidated `signal_channel!` and
  contract-section macro work.
- `primary-bann`, `primary-145a`, and `primary-8avm` — Tap/Tier-1
  persona-spirit and persona-introspect observability.

The live design surface has moved macro emission to schema source,
`nota-next`, `schema-next`, and `schema-rust-next`. Report 449 is
correct that the old macro/tap substrate should not remain as P1
operator work.

### Persona-prefix rename remnants

Verified open:

- `primary-0m1u` — persona-prefix rename wave epic.
- `primary-0m1u.11` — rename spirit triad after cutover.
- `primary-0m1u.12` — persona meta catch-up and CriomOS-home repin.

Designer 446 frames the next action as folding `spirit-next` into the
real `spirit` repo, not completing a legacy rename wave. The remaining
rename children depend on stale persona-spirit cutover beads.

### Persona-stack migration backlog

Verified open examples:

- `primary-a5hu` and `primary-4naq` — persona engine and
  signal-executor v4 migration epics.
- `primary-c620`, `primary-gu7t`, `primary-qjdp`, `primary-21gn`,
  `primary-krbi`, `primary-li7a`, `primary-aunn`, and `primary-e1pm` —
  per-component persona triad migrations to the old "current
  foundation."
- `primary-gvgj` plus `primary-gvgj.3` through `primary-gvgj.9` —
  persona-agent triad and backend migration.
- `primary-nobf`, `primary-q98d`, `primary-wvdl`, `primary-hj4`,
  `primary-hj4.1`, `primary-devn`, `primary-8n8`, `primary-07ot`,
  and `primary-ojxq` — persona engine, router, terminal, mind, and
  spirit work anchored in the pre-pivot substrate.

Designer 446 explicitly defers stateful runtime ports until after
schema-core extraction. The live plan is wave-2 porting through the
schema-emitted substrate, not signal-executor v4 migration.

## Confirmed actionable beads

Report 449's "keep/rewrite" class is also broadly correct:

- `primary-36iq` and `primary-36iq.3` remain live bracket-string work.
- `primary-kbmi` and `primary-kbmi.2` are live cloud/domain-criome work
  but carry the retired `role:system-specialist` label and pre-pivot
  wording.
- `primary-a1px` remains live as a spirit-next dispatcher follow-up, but
  should be read through designer 446 Phase 0.
- `primary-1xor` was not re-read in depth in this pass, but report 449's
  characterization matches designer 444's schema-core horizon.
- `primary-srmq` remains deploy-stack work and is not next-stack-pivot
  stale.

## Wrong or not implemented from report 449

- The exact priority distribution in report 449 is not live state.
- Report 449 recommends the designer lane directly apply some
  retirements. This session has explicit operator-subagent
  authorization to implement the audit, and BEADS is not lane-owned, so
  operator can close verified stale beads. The report's lane
  recommendation is therefore advisory, not a blocker.
- The report's P2/P3 estimates were not exhaustively re-verified in
  this session. The implementation should avoid closing broad P2/P3
  families unless the live bead query directly identifies them and the
  supersession evidence is the same.
- `primary-lrf8` is not safe to close as shipped without deeper source
  verification. Its acceptance criteria include explicit queue,
  worker-drain, multi-observer fanout, and concurrent processing. The
  live notes show related Nix tests and mail-keeper exercise, but this
  pass did not prove the full acceptance text.
- `primary-duuv` is safer: its own note says the acceptance is literally
  met and designer 444 names DatabaseMarker as live. It can be closed
  as shipped if implementation scope includes close-as-shipped actions.

## BEADS tooling observation

The installed `bd` CLI was inspected before editing. The backend is
`/home/li/primary/.beads/embeddeddolt`; the store uses an embedded
Dolt database. Parallel `bd` reads caused transient exclusive-lock
errors. Sequential `bd --readonly ...` reads succeeded. This session
therefore uses sequential `bd` commands for all writes.
