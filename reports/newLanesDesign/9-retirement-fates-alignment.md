# 9 — Lane retirement: decoupling report deletion from role retirement

Reopening the lane model on a point the psyche flagged. The just-landed
model fused three events into one atomic "close":

> report drains → delete the report directory → retire the lane

The psyche splits this into **two independent lifecycles**. The report
side and the lane/role side retire on different triggers and must not be
chained together. This thread does not supersede report 8 (closeout); it
corrects the retirement model 8 assumed.

## The correction (psyche, this session)

> "the lane's role might not be over. for example we are still designing
> the new lanes design, so decomissioning *the role* wasnt correct. but
> removing the last report(s) is a different story. so yes, something like
> analyze for durable content to make sure it lives somewhere
> (implementation, task or intent) then deleting it is good"

Two settled signals:

1. **Report retirement = distill-then-delete.** Before a report is
   removed, analyze it for durable content and ensure that content lives
   in a permanent home; *then* delete. Endorsed ("is good").
2. **Lane/role retirement is decoupled and work-gated.** A lane's role is
   not over just because its reports are. Retiring the role is wrong
   while the role's work continues. (Correction of the fused model.)

## What we are refining

| Surface | What it currently says |
|---|---|
| Spirit **6utp** (Decision, High) | *[When a session lane drains its report directory is deleted because git history and the session transcript hold the substance; a single append-only registry at protocols/retired-lanes.md records each retired lane... The thin index keeps drained sessions discoverable... without regrowing the working report tree.]* — **bundles** report-deletion AND the lane-retirement registry. |
| `skills/session-lanes.md` §"Lane retirement" | Three mechanical steps fired together: delete the report dir, append a `retired-lanes.md` row, `meta-orchestrate "(Retire (Lane …))"`. |
| `skills/session-lanes.md` §"Discipline persists" | *"A lane is a single work session"* — the line the multi-context question revises. |
| `protocols/retired-lanes.md` | *"the discoverable middle path between 'delete everything' and 'keep every report forever'."* |
| `AGENTS.md` (drain paragraph + lane table) | "When the lane drains, delete its `reports/<lane>/` directory — git history and the session transcript are the archive." |

## Lifecycle A — report retirement (distill-then-delete)

A report is **transient working substance**, not an archive. Its
retirement is its own event, on its own cadence, and can happen
repeatedly through a lane's life — not only at lane close.

The procedure before any report is deleted:

1. **Analyze the report for durable content** — the reusable substance:
   a synthesis, a decision, a mechanism walk-through, an implementable
   plan.
2. **Ensure that content lives in a permanent home**, one of three:
   - **implementation** — code, a `skills/` file, `ARCHITECTURE.md`, a
     per-repo `INTENT.md`, a durable doc;
   - **task** — a bead linked into the dependency graph
     (`bd dep <blocker> --blocks <blocked>`);
   - **intent** — a Spirit record.
3. **Delete the report.**

The durable-content analysis **is** the safeguard. Deletion is never the
unanalyzed automatic step — that automatic deletion is exactly what the
psyche pushed back on. No separate "preserve-as-reference" fate is
needed: a report worth keeping has its substance *promoted* into a
durable home (a skill / `ARCHITECTURE.md` / `INTENT.md`), and the raw
scaffolding then goes. Preservation lives in the canonical surface, not
in a frozen report.

## Lifecycle B — lane/role retirement (work-gated)

The lane carries a **role** — the intent-named body of work. Retiring the
lane (the daemon `Retire` plus the `retired-lanes.md` row) is triggered
by **the role's work being genuinely complete**, and by nothing else. Not
by a report draining; not, by itself, by a single context ending.

While the role's work continues, the lane lives on — including across the
fresh-context restarts taken for context hygiene. The last agent's error
was firing lane retirement off the report-drain trigger, moving to
decommission the `newLanesDesign` role while its design (this very work)
was still open.

## Open forks

**Fork 1 — lane definition.** Does **"lane = the intent-named body of
work that persists across fresh contexts until its role's work is
complete"** replace the current canonical line *"a lane is a single work
session"*?

- **Recommend: yes.** The psyche's own example is a lane already spanning
  contexts — `newLanesDesign` is still being designed *across a
  `/clear`*. And "favor a fresh session over endless compaction" already
  assumes the work outlives any single context. So a lane is the work;
  "drain" and "retire" become work-completion events, not context-end
  events.
- **Alternative:** keep "lane = one session" and only gate retirement on
  completion *within* a session — but that re-creates the fusion the
  psyche is rejecting every time a session restarts.

**Fork 2 — retirement authority.** Who pulls the trigger on *lane*
retirement (daemon `Retire` + `retired-lanes.md` row)?

- **Recommend: psyche-gated.** The agent presents a completeness case
  (where every report's durable content landed; the role's work is done)
  and the psyche confirms before retirement. Report-level
  distill-then-delete stays routine agent work — no per-report
  confirmation — because the durability analysis is its safeguard and git
  holds the bytes. Clean split: reports agent-routine, role retirement
  psyche-gated. This is the rule form of what just prevented the
  premature decommission.
- **Alternative:** agent judges completion autonomously — the automatic
  behavior the psyche objected to.

**Fork 3 — reference syntheses.** A report worth keeping is **promoted
into a durable home** (a `skills/` file, `ARCHITECTURE.md`, `INTENT.md`),
not kept as a standing raw report.

- **Recommend: yes — no separate "permanent reference report" category.**
  Preservation lives in the canonical surface.
- **Alternative:** allow a lane to keep a curated report on disk past
  distillation.

**Broader agenda (separate thread unless folded in):** `roles.list` →
dynamic-lane cutover (`primary-kooj`), intent-files deprecation
reconciliation (`primary-sfr3`), missing `videographer.md`
(`primary-dixg`).

## Surfaces that change once the fork is settled

- **6utp** — split the bundle. The record currently fuses report-deletion
  with the lane-retirement registry. Likely `Supersede` into (i) a
  report-retirement record (distill-then-delete; durable content to
  implementation/task/intent) and (ii) a lane-retirement record
  (work-gated, decoupled from report deletion; the thin `retired-lanes.md`
  index unchanged in purpose).
- `skills/session-lanes.md` — rewrite §"Lane retirement" into the two
  lifecycles; revise the "single work session" line per the fork.
- `protocols/retired-lanes.md` — clarify it indexes *role retirements*,
  not report deletions; a row is written at work-completion, not whenever
  reports are distilled away.
- `AGENTS.md` — the drain paragraph and the `reports/<lane>/` table row
  both name deletion as the close event; both move to the two-lifecycle
  framing.
- `ESSENCE.md` / `INTENT.md` — light touch only if the distill-then-delete
  philosophy reads as essence-level.

## Spirit-gate decision for this turn

Lifecycle A (distill-then-delete) is **settled** and capture-ready.
Lifecycle B's wording depends on the open forks (lane definition,
retirement authority). To avoid editing the load-bearing 6utp record
twice — and to avoid splitting its bundle the wrong way — capture and
implementation wait on the fork answers. The settled direction lives in
this report until then.
