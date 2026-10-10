---
title: 2 - Recent reports implementation candidates
role: weave-audit-operator
variant: Synthesis
date: 2026-06-25
topics: [reports, implementation, intent-alignment, beads]
description: |
  Scan of the most recent report surface for important implementable ideas,
  with the intent-alignment questions that should decide ordering, scope, or
  approval before work starts.
---

# 2 - Recent reports implementation candidates

## Scope

This scan read the newest report surface by modification time, centered on
reports from 2026-06-23 through 2026-06-24 plus the live follow-up reports they
point at. It prioritizes ideas that are both important and implementable:
already tracked as beads, ready to become beads, or framed as a narrow next
slice with acceptance checks.

Sources read included:

- `reports/weave-audit-operator/1-precious-main-context-handoff-audit.md`
- `reports/preciousMainContext/7-subagent-delegation-context-audit.md`
- `reports/schema-help-daemon-pilot-operator/1-skill-change-handoff.md`
- `reports/newLanesDesign/8-closeout-and-state.md`
- `reports/schema-designer/24-all-domain-and-skill-sourcing-implementation-design.md`
- `reports/schemaWorkAudit/1-schema-implementation-intent-alignment.md`
- `reports/schemaWorkAudit/2-schema-triad-vertical-slice-handoff.md`
- `reports/schema-designer/19-Refresh-schema-stack-position-2026-06-24.md`
- `reports/cloud-operator/393-Synthesis-cloud-domain-consumer-alignment.md`
- `reports/system-operator/240-Refresh-lojix-contained-cluster-current-surface.md`
- `reports/system-operator/241-Refresh-lojix-production-runtime-current-surface.md`
- `reports/system-operator/237-lojix-contained-deploy-test-visual-synthesis-2026-06-21.md`
- `reports/operator/463-spirit-guardian-psyche-advocacy-split.md`
- `reports/operator/464-handover-context-maintenance-correction.md`
- `reports/designer/728-Design-alignment-interview-method-and-skill-realignment-2026-06-24.md`
- `reports/designer/729-Closeout-skill-description-realignment-2026-06-24.md`
- `reports/designer/730-idea-disposition-2026-06-24/1-idea-ledger.md`

BEADS note: two broad BEADS commands failed because another process held the
embedded database lock. Targeted `bd show` calls succeeded for the top tracked
items, so the status below distinguishes "tracked and open" where verified from
"proposed in a report" where not verified.

## Highest-value candidates

### 1. Repair the helper-dispatch instruction surface

Status: partially landed, still not complete. Recheck on 2026-06-25 shows
`primary-ptvb.1` (human-interaction cut) and `primary-ptvb.5` (helper skill)
closed. `primary-ptvb.6` (shrink AGENTS.md to a thin spine) remains open and is
still blocked by the remaining skill-body cuts plus the ky10 reconcile bead.

Why it matters: the live Spirit records say all disciplines should delegate
non-trivial orientation/research to fresh-context helpers and avoid duplicating
the helper's broad read. The text a new agent reads still says the opposite for
non-designer lanes. This is a workspace-wide agent-behavior defect, not a local
doc nit.

Remaining implementation shape:

- complete the remaining W2-W4 skill-body cuts;
- reconcile ky10 through `primary-ptvb.11`;
- then unblock `primary-ptvb.6`, rewriting AGENTS.md to the thin spine and
  replacing the old designer-only dispatch default.

Intent-alignment question: Should the next primary-guidance slice prioritize the
helper-dispatch repair over new component work?

Recommended answer: yes, but phrase it as "finish the remaining helper-dispatch
surface repair," not "start helper-dispatch repair." The helper skill exists;
the still-live risk is AGENTS.md and the discipline-skill blockers that keep a
new agent from reading the settled rule cleanly. Alternative: leave W6 blocked
until the broader preciousMainContext pruning lane completes W2-W4.

### 2. Start the Spirit `All` domain cutover and the Spirit manual split in parallel

Status: tracked and open. Verified beads: `primary-w0xf`,
`primary-sfn5`, `primary-e4o9`, and `primary-64s3`.

Why it matters: `reports/schema-designer/24...` is unusually implementation-ready:
it names the generator recut, query verbs, guardian teaching, storage migration,
tests, redeploy, and the independent primary-side skill/manual split. The
`All` cutover unlocks parent-domain maxim retrieval and the founding top-level
maxim record. The manual split removes drift between deployed Spirit wire shape
and primary skills.

First executable roots:

- `primary-w0xf`: delete `Optional` from the Spirit domain tree source and
  inject `All` into every domain-tree enum through the generator;
- `primary-e4o9`: build the spirit-repo manual generator plus
  `ManualNarration` and a staleness check.

Intent-alignment question: Should the `All` domain recut and the Spirit manual
generator run as parallel first-wave roots now?

Recommended answer: yes. They are independent and both are already bead-backed.
The psyche-level decisions can wait until their natural gates: exact founding
maxim wording before `primary-xgcr`, and `intent-log.md` to
`intent-capture.md` rename before `primary-64s3`.

### 3. Build the schema triad vertical slice

Status: tracked and open. Verified bead: `primary-lwc6`.

Why it matters: the schema audit says the implementation is on trajectory but
not endpoint-aligned. The intended endpoint is a real schema component triad:
manifest-loaded environment, typed source maps, `SpecifiedSchema`, canonical
schema re-encode, Rust regeneration, and a daemon/language-server query surface.

First slice:

- load a schema environment manifest;
- resolve at least one versioned import across modules;
- produce typed source maps;
- lower to `SpecifiedSchema`;
- re-encode canonical `.schema`;
- regenerate Rust;
- expose one daemon-shaped feedback query.

Intent-alignment question: Should the first schema slice use a CLI command
backed by daemon-shaped library code, rather than waiting for the full daemon?

Recommended answer: yes. It preserves the daemon handler shape while getting
quick feedback. Alternative: build the daemon first, which is cleaner
architecturally but delays the proof of the manifest-to-`SpecifiedSchema` spine.

### 4. Settle and implement the Lojix contained-cluster next slice

Status: report-ready; exact bead status not verified in this pass.

Why it matters: `reports/system-operator/240...` says Lojix cannot yet deploy
test VM clusters. The missing mechanism is `RunContainedCluster` with daemon-owned
aggregate lifecycle, release-all, restart reconciliation, and queryable history.
The older companion report also warns that lower roots must not land with stale
shapes such as `CheckContained`, ignored `source`, direct redb peeks, or
`TestMode::Live`.

Intent-alignment question: Should system-operator treat `RunContainedCluster`
on `HermeticVm` as the next slice, with an explicit precheck that the lower
`DeployContained` / `VerifyContained` / `Release` semantics are truthful?

Recommended answer: yes. Follow the newer report 240, but include the lower-root
truth precheck from report 237 as an entry condition. Alternative: do only the
lower-root cleanup first, which lowers risk but postpones the cluster coordinator.

### 5. Finish the CriomOS-test-cluster domain consumer slice

Status: report-ready; `reports/cloud-operator/393...` says the cloud-operator
claim is blocking later test-cluster work.

Why it matters: the work is narrow and already aligned: prove downstream
consumers read `cluster.domainConfiguration` rather than hardcoded
`criome.net`, using pure/eval checks only. The report explicitly defers live
Cloudflare mutation and the Immich/WebHost hosting model.

Intent-alignment question: Should cloud-operator finish the domain consumer
migration with pure/eval checks, commit, push, and release the claim?

Recommended answer: yes. Acceptance is concrete: projected fixtures match,
structural contracts pass, rejection checks pass, and at least one real
downstream consumer reads `cluster.domainConfiguration`. Alternative: include
`CriomOS-test-cluster/ARCHITECTURE.md` in the same landing, which closes a repo
contract gap but widens the slice.

### 6. Update Spirit guardian prompts for direct psyche-declared metadata and repair-shaped remands

Status: report-ready; not verified as a bead.

Why it matters: `reports/operator/463...` finds the schema is already right:
`Entry`, `Testimony`, and `Reasoning` are separate. The gap is guardian prompt
behavior. The guardian should treat a psyche-declared certainty, importance, or
privacy rung as sufficient support for that rung, and rejections should point
to the repair operation family rather than only saying no.

Intent-alignment question: Should this prompt/test alignment ship as an
independent small Spirit task, rather than waiting for the `All` domain recut?

Recommended answer: yes. It touches guardian prompts and tests, not the domain
wire/storage migration. Alternative: batch it with the next Spirit redeploy,
which reduces deploy churn but delays guardian correctness.

### 7. Promote current-main trace and durability fixes above new guard features

Status: proposed in the designer idea ledger; not verified as beads.

Why it matters: the idea ledger flags current-main failures that undermine later
proofs:

- the trace plane is inert end-to-end because producer and consumer
  `EngineIdentifier` values disagree, record keys omit event identity, sequence
  numbers reset across restarts, component labels are wrong, and drain faults are
  swallowed;
- criome and mentci do not yet satisfy durable SEMA self-resume: mentci holds
  slot-to-question state in memory and criome configuration generation resets.

Intent-alignment question: Should operator fix trace-plane functionality and
criome/mentci self-resume before adding more guard-substrate features?

Recommended answer: yes. These are substrate correctness issues for observing
and resuming the system. Alternative: continue guard-substrate feature work
first, accepting that its proof surface remains weaker until trace and resume
are repaired.

### 8. Bring orchestrate's live daemon and worktree lifecycle up to the new lane model

Status: partially tracked. Verified `primary-kooj` for the roles.list/seed
cutover. The designer ledger also proposes live store migration and worktree
lifecycle work.

Why it matters: newLanesDesign landed the dynamic session-lane model, but
follow-up daemon infrastructure remains. The reports identify three related
implementation ideas: cut or reshape `orchestrate/roles.list`, migrate the live
orchestrate redb store and restart the daemon if production is behind source,
and implement real worktree lifecycle orders plus a GC reader.

Intent-alignment question: Should the orchestrate lane-model follow-up start
with production reality - migrate/restart the live daemon if needed - before
new lifecycle features?

Recommended answer: yes. A live registry mismatch makes new feature work hard
to trust. Alternative: implement `primary-kooj` first because it is a smaller
repo-local cleanup, then hand live migration to maintainer.

### 9. Decide whether to retire `newLanesDesign` now

Status: open drain decision in `reports/newLanesDesign/8-closeout-and-state.md`.

Why it matters: the lane model was deliberately dogfooded. Its closeout says the
lane is drainable: intent is captured, follow-up work is in beads, substance
landed in docs, and the remaining step is deleting `reports/newLanesDesign/`,
appending `protocols/retired-lanes.md`, and retiring the daemon lane.

Intent-alignment question: Should `newLanesDesign` be retired now?

Recommended answer: yes if the psyche accepts the cutover. Alternative: hold it
one more pass while W5/W6 fixes the helper-dispatch contradiction, because those
reports are adjacent to the lane-lifecycle model and still being used as live
context.

### 10. Fill the videographer discipline skill gap

Status: tracked and open. Verified bead: `primary-dixg`.

Why it matters: videographer is listed as one of the nine disciplines, but
`skills/videographer.md` does not exist. The required-reading contract says a
lane loads its discipline file; a videographer session therefore has no
discipline skill to load.

Intent-alignment question: Is videographer still a live discipline that should
receive a first skill file now?

Recommended answer: yes. If it remains one of the nine, create the skill. The
alternative is to remove it from the nine-discipline lists, which is a larger
intent question.

## Proposed ordering

The ordering below minimizes instruction-surface risk first, then unlocks the
highest-leverage component work:

1. Finish helper-dispatch surface repair: complete W2-W4 and ky10 reconcile,
   then land `primary-ptvb.6`.
2. Spirit `All` recut root `primary-w0xf` and manual generator `primary-e4o9`
   in parallel.
3. Schema triad vertical slice `primary-lwc6`.
4. Cloud domain consumer pure/eval landing, because the report says the claim is
   blocking follow-on work.
5. Lojix contained-cluster slice after explicitly reconciling report 240's
   `RunContainedCluster` next step with report 237's lower-root truth prechecks.
6. Guardian prompt/test update, trace-plane repair, and criome/mentci
   self-resume as substrate-quality tasks.
7. Orchestrate live migration / roles seed / worktree lifecycle.
8. Lane-drain and discipline-gap cleanup: retire `newLanesDesign`, create
   `skills/videographer.md`.

The broad designer idea ledger contains 70 proposed buildable items. Do not try
to approve it as one batch. The best use is per-cluster triage: accept the
specific high-severity substrate fixes above, then open a separate alignment
round for the remaining schema/codegen, criome/mentci, router, mirror, and cloud
clusters.
