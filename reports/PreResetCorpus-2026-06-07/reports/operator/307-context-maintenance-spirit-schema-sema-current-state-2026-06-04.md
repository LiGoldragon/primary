---
title: 307 - Context maintenance - Spirit/schema/SEMA current state
role: operator
variant: Review
date: 2026-06-04
topics: [context-maintenance, spirit, schema, sema, triad-runtime, reports]
description: |
  Operator-lane context-maintenance review of the current Spirit/schema/SEMA
  report and code surface after the 2026-06-04 design refreshes and the
  operator landings in triad-runtime, sema-engine, and spirit. Names current
  canonical surfaces, stale or superseded surfaces, open threads, and exact
  retire/migrate recommendations. No Spirit capture and no report deletion.
---

# 307 - Context maintenance - Spirit/schema/SEMA current state

## Intent Anchors

[The new schema-derived spirit is the forward target and is nearly ready to move to production; new functionality targets it rather than the hand-written production daemon.] (Spirit 2540)

[Implement the operator-recommended runtime cleanup direction: keep schema responsible for component meaning, move reusable byte and process-edge mechanics into triad-runtime, and apply the cleanup in the sequence of shared length-prefixed framing, typed component arguments, then thiserror-based runtime errors.] (Spirit 2558)

[The triad engine separation is strict and absolute: SEMA owns durable state, Nexus owns decisions, Signal owns communication, and daemon code must not carry those concerns outside their engines.] (Spirit 2560)

[Sema-engine is the exclusive interface to the database; no component daemon may make direct redb calls, even as a pilot.] (Spirit 2563)

[Component databases use a .sema file extension instead of .redb.] (Spirit 2564)

[When schema-derived components expose a reusable storage need, improve the shared engine surface so generated SEMA code expresses its real storage identity and query needs directly.] (Spirit 2566)

## Scope And Worktree Status

This is a working-order context-maintenance pass. I did not record new intent.
I did not delete reports.

Primary's working copy already contained another agent's uncommitted designer
refresh sweep: deleted designer reports 351/352/443-494 and added designer
refresh reports 504-508. I read those files as local context, but they are not
pushed canonical surfaces until the designer lane commits them.

The main operator currently holds `/git/github.com/LiGoldragon/spirit` and that
repo has uncommitted internal rename work on top of pushed commit `6a339e20`
(`spirit: route SEMA storage through sema-engine`). I treat that dirty source
state as in-flight, not canonical.

## Current Canonical Surfaces

### Intent And Permanent Workspace Surfaces

- `ESSENCE.md` and `INTENT.md` are current for the schema-driven stack:
  schema specifies, signal moves, sema holds; symbols are paths; strings stay
  at user/display edges; trace/help/config are schema data.
- `protocols/active-repositories.md` is current for repository identity:
  `persona-spirit` is production Spirit, `spirit` is the schema-derived next
  implementation, `sema-engine` is the database engine library, and
  `triad-runtime` is shared runtime support. Its `triad-runtime` row is now
  slightly stale because commit `6daf2954` added the argument runtime surface.
- Spirit records 2540, 2558, 2560, 2563, 2564, 2565, and 2566 are the recent
  high-authority anchors for this topic.

### Pushed Operator Code State

- `triad-runtime` main commit `6daf2954` (`triad-runtime: extract frame and
  argument runtime nouns`) added `LengthPrefixedCodec`, `FrameBody`,
  `ComponentCommand`, `ComponentArgument`, and tests. This supersedes the
  "not implemented" status in operator report 306 for cleanup targets 1 and 2.
- `sema-engine` main commit `817236a7` (`sema-engine: add identified record
  families`) added identified table descriptors, engine-allocated
  `RecordIdentifier` values, identified assert/retract/match, `.sema`
  documentation, and tests.
- `spirit` main commit `6a339e20` (`spirit: route SEMA storage through
  sema-engine`) routes the schema-derived Spirit store through sema-engine and
  consumes `LengthPrefixedCodec` / `ComponentArgument`. This resolves the new
  Spirit sema-engine bypass named by system-designer report 63, at main.

### Current Report Surfaces

- `reports/designer/499-Psyche-persona-engine-state-and-vision-2026-06-04.md`
  is current for the whole-engine psyche-facing state: one proven schema-derived
  pilot, old-stack fleet, cutover ordering, and decisions still owed.
- `reports/designer/501-strict-engine-separation-audit-2026-06-04/4-overview.md`
  is current for strict engine separation. Its core finding remains right:
  the pilot passes intra-daemon separation; old-stack daemons need cutover; the
  runner makes the constraint structural. Its sema-engine failure is now fixed
  on `spirit` main by commit `6a339e20`.
- `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md`
  is current for the storage boundary correction. It supersedes the earlier
  "raw redb is acceptable for the pilot" framing in system-designer 61/62.
- `reports/system-designer/62-spirit-data-lifecycle-ladder-concept-and-new-spirit-readiness-2026-06-04.md`
  remains current for the lifecycle ladder and new-Spirit readiness, except its
  "storage-kernel adoption" punch-list item is now landed by `6a339e20`.
- `reports/operator/305-production-spirit-feature-port-audit-2026-06-04.md`
  remains current for production feature parity: direct ports are
  ChangeCertainty, topics, identifier ranges, modes/provenance, and certainty
  filters; non-direct ports are lifecycle/archive, watch/tap fanout, owner
  sockets, handover, and working-state behavior.
- `reports/operator/306-schema-centered-runtime-cleanup-analysis-2026-06-04.md`
  remains useful as rationale for frame/argument/thiserror ordering, but its
  execution status is stale after the pushed commits.
- If committed by designer, `reports/designer/504-Refresh-schema-stack.md`,
  `505-Refresh-triad-engine.md`, `506-Refresh-persona-and-spirit.md`,
  `507-Refresh-intent-and-reporting-discipline.md`, and
  `508-Refresh-legacy-audits-and-backlog.md` become the design-history landing
  witnesses for large blocks of older designer reports.

## Stale Or Superseded Surfaces

- `reports/operator/306-schema-centered-runtime-cleanup-analysis-2026-06-04.md`
  is stale where it says none of the three cleanup targets is implemented.
  Frame and argument extraction are landed; thiserror cleanup remains open as
  bead `primary-kwm2` (convert Spirit hand-written error enums to thiserror).
- `reports/operator/304-Psyche-repository-stack-state-2026-06-04.md` is stale
  in its SymbolPath paragraph: it says record 1577 is Maximum and flat
  SymbolPath is fully canonical. Current Spirit observation shows 1577 at
  Medium and 1586 at Zero, while designer reports 499/500 treat the
  structured-vs-flat question as not safely operator-settled. Do not use 304 as
  an implementation license for SymbolPath beyond the landed flat shape.
- `reports/system-designer/61-spirit-situation-projection-engine-analysis-proposals-2026-06-04.md`
  and report 62 are superseded only on raw-redb acceptability. Their archive,
  privacy, lifecycle, cutover, and readiness analysis still carries forward.
- `reports/designer/496-Psyche-schema-stack-state-and-decisions-2026-06-04.md`
  remains useful for the schema-stack state, but its "smaller cleanups" section
  is partially overtaken by commits `6daf2954` and `6a339e20`.
- Older operator maintenance reports 271, 276, 283, and 285 are stale as
  current implementation queues. They remain useful only until their leftover
  cleanup items are migrated to beads or newer reports.
- The locally deleted designer reports 351/352/443-494 are already retirement
  candidates in the designer refresh sweep, but this operator pass should not
  delete or commit those deletions. The landing witness belongs to designer's
  504-508 refresh commit.

## Load-Bearing Open Threads

- `primary-vllc` (schema-next dual lowering bug): still open. Fix by unifying
  on the most-correct lowering path and adding the both-paths/bare-header
  witness.
- `primary-l89s` (generic triad runner): still open. The frame and argument
  substrate landed; the runner itself has not.
- `primary-myku` (RustItem emission token model): still open. Ratified intent
  exists; `schema-rust-next` main still has hand-indented `self.line` output.
- `primary-kwm2` (thiserror): still open and correctly sequenced after the
  frame/argument extraction.
- `primary-o2kc` / `primary-f8gf` (Spirit internal rename): in progress in the
  `spirit` working copy under the operator lock. Do not open a parallel source
  edit there.
- `primary-tiyo` (new-Spirit archive/privacy/typed-feedback lifecycle): still
  open. Report 62 is the design concept; operator 305 is the port audit.
- `primary-y0ec` (peripheral sema-engine strays): still open for chroma,
  orchestrator, and schema-next. Spirit itself is no longer in this bucket
  after `6a339e20`.
- SymbolPath structured-vs-flat remains a design/intent-maintenance thread, not
  an operator implementation thread. The active code is flat; the report corpus
  contains a live disagreement about whether the structured prototype is still
  owed.

## Recommended Retire Or Migrate Actions

1. Keep `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md`
   as the canonical sema-engine boundary report until its substance is
   manifested into `skills/component-triad.md`, `sema-engine/ARCHITECTURE.md`,
   and `spirit/ARCHITECTURE.md`. After that, it can retire.
2. Keep system-designer 61/62, but mark or refresh their storage-readiness
   paragraphs through report 63 plus commits `817236a7` and `6a339e20`. Do not
   delete them yet; their archive/privacy/lifecycle substance is not fully
   migrated.
3. Keep operator 305 as the current production-feature port audit until the
   daily-use parity bead work lands. Then migrate the direct/non-direct port
   split into `spirit/ARCHITECTURE.md` or a successor implementation report and
   retire 305.
4. Treat operator 306 as superseded for cleanup targets 1 and 2. Retire it only
   after thiserror lands or a newer runtime-cleanup report absorbs its error
   boundary rationale.
5. Treat operator 304 as a repo-topology report, not a current design-decision
   report. Its SymbolPath paragraph should stay superseded by this report until
   designer/intent-maintenance resolves 1577/1586.
6. Update `protocols/active-repositories.md` when a bookkeeping window is safe:
   the `triad-runtime` row should name both `LengthPrefixedCodec` and
   `ComponentArgument` / `ComponentCommand`, not only trace/socket support.
7. Let the designer lane own the 504-508 refresh commit and the deletion of
   older designer reports. If those refreshes are pushed, they become the
   landing witnesses for the local designer deletions; if they are not pushed,
   no operator should assume those reports retired.
8. Run a separate operator report sweep after the active `spirit` rename
   finishes. First candidates: operator 271, 276, 283, and 285. Migrate any
   leftover small cleanup into beads, then delete the stale maintenance ledgers.

## What I Changed In This Pass

I added this report. I also added short context-maintenance notes to operator
reports 304 and 306 so future search does not treat their stale paragraphs as
current truth.
