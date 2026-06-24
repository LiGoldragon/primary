---
title: 5 — context-maintenance cutover to the session-drain discipline
role: newLanesDesign
variant: Design
date: 2026-06-24
topics: [context-maintenance, lanes, sessions, drain, lane-retirement, beads, spirit]
description: |
  Reframes skills/context-maintenance.md and skills/context-maintenance-deep.md
  around the dynamic session-lane model. Context maintenance becomes the
  close-of-session DRAIN discipline: every idea routes to one of three fates
  (intent via Spirit / work via a bead in a dependency graph / abandon). Lane
  retirement now deletes the report directory and appends one line to
  protocols/retired-lanes.md. Topic-recency ranking, forward/migrate/keep/drop,
  agglomeration/Refresh, and using-agents-for-the-sweep are preserved, reworded
  role -> lane.
---

# 5 — context-maintenance cutover to the session-drain discipline

## What this slice changed

Both context-maintenance skills assumed the retired model: ~9 fixed
role-lanes with permanent `reports/<role>/` subdirectories, and lane
"retirement" that freed a role *identifier* and left an empty
directory. This slice cuts them over to the session-lane model — a
lane is a throwaway work-session named for its intent, `reports/<lane>/`
is a session directory, and the lane retires by being *deleted* and
indexed.

### skills/context-maintenance.md

- New opening section **"Context maintenance is the session-drain
  discipline"** naming the drain at close as the spine; the everyday
  agglomeration/topic-recency sweeps are reframed as the same
  discipline applied mid-life.
- New **"The three-fate disposition"** section: a table routing every
  drained idea to exactly one of intent (Spirit CLI record) / work
  (a bead linked via `bd dep <blocker> --blocks <blocked>`) / abandon
  (git + transcript preserve it). Aligned with Spirit `pm1b` (lane
  retirement gated on context-maintenance of leftover reports + beads).
- **"When to invoke"** rewritten: session-drain trigger is now the
  first and primary trigger ("favor a fresh session over endless
  compaction"); the soft-cap trigger is reworded role -> lane; the
  lane-retirement trigger now states the directory is deleted and the
  registry line appended once triage completes.
- Connective note in **"Per item, decide"** relating the four moves
  (Forward / Migrate / Keep / Drop) to the three fates — the four
  actions are the moves, the three fates are the outcome.
- `reports/<role>/` -> `reports/<lane>/` throughout (inventory step,
  handover-report path). The `Two surfaces` "matures upward" list
  dropped its `ESSENCE.md` mention to avoid touching the out-of-scope
  `8rpu` deprecation drift; the pre-existing `ESSENCE.md` reference in
  the Migrate-action row was left untouched (also out of scope).
- Preserved unchanged in substance: topic-recency ranking (already
  cross-lane), the staleness landing gate, forward/migrate/keep/drop
  band, agglomeration + the Refresh variant, distribute order,
  competing-alternatives migration, manifest-into-architecture, small
  thoughts, and "Using agents for the sweep".

### skills/context-maintenance-deep.md

- **"When this fires"** reworded to several session lanes rather than
  the fixed `designer + operator + system-operator + qualified` list.
- **"Retired lanes"** subsection retitled "route by topic, then delete
  the directory": there is no "main lane" to fold into under the
  session model, so content routes by the three-fate disposition and
  live working-artifact substance agglomerates by topic into the
  current canonical report; the directory is then deleted.
- **"Retiring a lane"** rewritten as the canonical archival flow:
  triage reports, triage beads (reassign now links into the dependency
  graph), resolve pending decisions, **delete the report directory**
  (`rm -rf reports/<retiring-lane>/`), and **append one line to
  `protocols/retired-lanes.md`** carrying lane / discipline / git range
  / transcript pointer / drain date / one-line decision. Closing note
  records that `LanesObserved` indexes active lanes and
  `protocols/retired-lanes.md` indexes retired ones.
- Removed the "explicit psyche direction" gate on retirement and the
  "until a dedicated retired-lane sweep agent is hired" / "prime
  designer" phrasing — replaced with "whichever lane the psyche
  directs", consistent with the discipline-vs-lane split.

## Cross-references this slice creates (owned by other slices)

- `protocols/retired-lanes.md` — referenced by both skills as the
  single append-only retired-lane registry. It does not yet exist; I
  did not create it (out of my assigned file scope). The slice that
  owns `protocols/` and/or the registry must create it with the schema
  these skills now describe: one line per retired lane carrying lane,
  discipline, git revision range, transcript pointer, drain date, and a
  one-line decision statement.
- The skills reference `reporting.md` (meta-report directory shape,
  soft cap, pre-launch lane allocation), `intent-maintenance.md`,
  `intent-alignment.md`, and `architecture-editor.md`. If a sibling
  slice reworks `reporting.md`'s soft-cap or directory sections to the
  lane model, the §-anchor references here stay valid as long as those
  section names persist.

## Open questions for synthesis

- The drain text assumes a session's reports can forward live
  substance into "the canonical report on its topic, which may belong
  to another active session." That presumes cross-session topic
  ownership is allowed mid-flight; the cross-lane authority boundary in
  the deep skill (dispatcher records, never executes, another lane's
  drop) still holds for *sweeps*, but a draining lane writing into a
  peer's live session directory is a slightly different move. Confirm
  the synthesis is comfortable with a draining lane agglomerating into
  a peer's canonical report, versus leaving the substance as a bead/
  Spirit record and letting the topic-owning session pull it.
- `protocols/retired-lanes.md` schema is described in prose in two
  places (the deep skill step 5 and this report). If the registry
  owner picks a stricter row format (e.g. a markdown table vs a bullet
  line), the deep-skill prose may want a one-word tightening to match.
