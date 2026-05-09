# Skill — beads

*When to track a unit of work as a BEADS task, when to make
it a discipline instead, when to close.*

---

## What this skill is for

When you find yourself reaching for `bd create`, this skill
decides whether a bead is the right home for what you're
about to track. When you find an open bead that hasn't moved
in a while, this skill decides whether to drive it to
closure, reformulate it as a discipline, or close-without-
shipping.

BEADS is the workspace's short-tracked-item store, exposed
through the `bd` CLI. It is **transitional** per
`~/primary/AGENTS.md`: the destination is Persona's typed
messaging fabric. Don't deepen the BEADS investment; don't
bridge to Persona; use BEADS for what it's good at today
and design new shapes assuming BEADS goes away.

---

## When to file a bead

A bead is the right home when **all** of:

1. **It's a discrete unit of work.** Has a definition of
   done. Will be either resolved or explicitly deferred —
   not "ongoing forever."
2. **It needs cross-session memory.** A note in chat or a
   designer report would be lost; the work spans more than
   one session.
3. **It's not better-tracked elsewhere.** Not a code
   change (file an issue or just edit), not a discipline
   (write a skill), not a design decision (write a
   designer report).

Examples that fit:

- *"Migrate chroma to current nota-codec API (NotaSum,
  Decoder::new, Encoder::new)"* — discrete, concrete,
  spans sessions, will close when shipped.
- *"Design new role: critical-analysis"* — discrete
  designer task, will close when the report lands.
- *"Migrate ~/git to /git/github.com layout"* — discrete
  system-specialist task, mechanical scope.

---

## When NOT to file a bead

### Anti-pattern A: durable-backlog beads

A bead that says *"every X should have Y, incrementally"*
is a discipline statement, not a task. It will never close
as a single unit; it'll sit in the listing forever as a
P2 that doesn't move.

The fix: **make it a discipline, not a bead.** Land the
rule in the right skill (e.g. *"after substantive work in
a repo lacking `skills.md`, write one before finishing the
task"* lives in `skills/autonomous-agent.md`); close the
bead with a closing note pointing at the rule.

If visibility into the gap is the value (which repos
*haven't* done X yet?), that's a workspace doc or a CI
check — not a bead.

### Anti-pattern B: tracking design questions as beads

A bead that says *"figure out X"* without a definition of
done is a design question. The right home is a designer
report (or a thinking session that produces one). The
report carries the substance; the BEADS task is just a
re-pointer.

Acceptable bead form for design work: *"Land designer
report on X"* — discrete, will close when the report
lands. Not: *"Decide what X should be."*

### Anti-pattern C: tracking ongoing concerns

*"Monitor build performance"*, *"keep an eye on the chroma
daemon"*, *"check on lojix deploys regularly"* — none of
these are beads. They're either alerting (write the
alert), monitoring (write the dashboard), or noise
(don't track).

### Anti-pattern D: bead-as-reminder for a small fix

A bead is heavyweight relative to *"see this stale comment,
fix it next time you're in this file."* If the fix is a
one-line edit and you're in the file, fix it. If it's
forgettable but trivial, leave a `TODO` next to the code
and the next agent who passes will see it.

---

## Beads are not ownership locks

Per `~/primary/AGENTS.md`: *"BEADS is never an ownership
lock. Do not claim `.beads/`. Any agent may create, update,
comment on, or close BEADS tasks at any time."*

The corollary: don't treat *"someone filed a bead"* as
*"someone is going to do this work."* Beads are
queue-shaped tracking, not assignment. If the work needs
to land, an agent picks up the bead and does it; if no
agent does, the bead sits open until pruned.

## Taking on a bead — the task-lock bridge

When you start work on a bead, claim it through the
orchestration protocol so other agents see the work is in
flight. Per `protocols/orchestration.md` §"Claim Flow",
task locks use bracketed tokens:

```sh
tools/orchestrate claim system-specialist '[primary-f99]' -- chroma migration
# … do the work …
tools/orchestrate release system-specialist
bd close primary-f99 -r "<closing note>"
```

The bracketed token must be quoted in shell — `[` is a
glob character. The helper enforces exact-match overlap
across roles: if two roles try to claim `[primary-f99]`,
the second is rejected.

This bridges two coordination layers that BEADS alone
doesn't span:

- **BEADS lifecycle** (filed/open/closed) — durable
  task tracking; visible across machines via `bd list`.
- **Orchestration locks** (claim/release) — in-flight
  agent coordination on this machine; visible via
  `tools/orchestrate status`.

A bead in *open* state doesn't tell other agents *"someone
is working on this right now."* The task lock does.
Without it, two agents racing on the same bead is a real
risk: each does the work, only one push lands, the other
discovers their commits are now stale. The task lock
prevents the race up front.

When done with the work, **release the lock and close the
bead in the same flow.** Don't leave a stale task lock
after the bead closes; don't close the bead while still
holding the lock.

For non-BEADS work the same syntax extends naturally:
`'[pr:42]'` to coordinate review of a specific PR,
`'[draft:role-redesign]'` for a draft report not yet
filed. The helper treats brackets as exact-match
identifiers; the projection from the token to the
underlying artifact is the agent's responsibility.

---

## When to close a bead

### Shipped

When the work the bead names has shipped, close with a
note pointing at the canonical home (the report, the
commit, the skill change). Example:

```sh
bd close primary-8b6 -r "Shipped via chroma daemon (replaces \
darkman + nightshift). See \
~/primary/reports/system-specialist/96-system-specialist-agglomerated-archive.md \
(retired report 28 summary)."
```

The closing note is the breadcrumb a future agent reads
when the bead's ID surfaces in old reports or git history.
It points at *where the substance lives now*, not at what
the bead said when filed.

### Superseded

When a bead is rendered moot by a design change (e.g. a
bead about migrating a derive that no longer exists), close
with a note naming the supersession.

```sh
bd close primary-XYZ -r "Moot per designer/46 — the X derive \
was deleted; the migration this bead names is no longer needed."
```

### Reformulated as a discipline

When the bead is a durable-backlog bead (anti-pattern A),
close with a pointer to where the discipline now lives.

```sh
bd close primary-bmy -r "Discipline statement, not a unit of \
work. The rule lives in skills/autonomous-agent.md §'A repo has \
no skills.md, and you've just done substantive work in it'."
```

### Won't ship

When a bead is genuinely abandoned — the direction was
wrong, the work isn't going to happen, the cost outweighs
the benefit — close with a note naming why. Don't leave
zombies open.

```sh
bd close primary-XYZ -r "Won't ship — superseded by approach Y; \
see designer/N for context."
```

---

## Closing notes carry forward

Every closed bead's `-r` reason becomes the durable record
of *why this isn't being tracked anymore*. A future agent
finding the bead ID in old git history or in a stale
report can read the closing note and immediately
understand whether to revive (rare), reopen (also rare),
or move on (almost always).

The closing note is the bead's small designer report.
Treat it as such — name the path forward, not just *"done."*

---

## Stale internal references in bead descriptions

Bead descriptions decay the same way reports do. A bead
filed against an old report-number will name a path that no
longer exists after a cleanup; a bead filed against an old
crate name (`NexusVerb`) will name a name that no longer
exists.

**Don't fight to keep bead descriptions current.** Two
acceptable approaches:

1. **Bead description as timestamp** — what was true when
   filed. Edit only when the description is actively
   misleading future agents (rare).
2. **Close + new bead** — when the filed bead's premise has
   moved enough that the description doesn't survive,
   close it with a forwarding note and file a new bead
   carrying current context.

Either works. The default: option 1 + close-as-resolution.
Don't accumulate edits to bead descriptions trying to keep
them fresh; let the canonical home (the skill, the report,
the code) carry the current substance.

---

## The `bd` CLI shape

This skill names *when* to use BEADS; the CLI commands
themselves:

| Command | Use |
|---|---|
| `bd list --status open` | Workspace queue |
| `bd show <id>` | Read a single bead's full description + status |
| `bd create "title" -t task -p <P> -d "description"` | File a new bead |
| `bd close <id> -r "<closing note>"` | Close with reason |
| `bd dep <a> --blocks <b>` | a blocks b |
| `bd dep remove <blocker> <blocked>` | undo |

Priorities (`-p`): `1` (P1, urgent), `2` (P2, normal),
`3` (P3, deferred).

Types (`-t`): `task` (default), or other types if the
project has them defined.

For the full CLI reference and any project-specific
conventions, see `lore/bd/basic-usage.md` if it exists, or
`bd help <command>`.

---

## Periodic audit

A workspace's open-beads list should be small (~5-15
items) and most beads should be *moving* (recently filed,
recently updated, or recently closed). When the list grows
past ~15 items or contains beads filed weeks ago that
haven't moved, **audit:**

1. For each open bead, ask: *is this still load-bearing?*
2. Stale → close (per "When to close" above).
3. Active but stuck → name the blocker (file a closing
   note pointing at it, or update the bead's
   description).
4. Active and unstuck → that's a bead that should
   be moving; name what it needs to move.

The audit produces a designer report. (Audit 56 was the
worked example; retired in the 2026-05-09 cleanup once the
substance had migrated into this skill and `designer/68`'s
inventory.)

---

## When `.beads/` reports a database lock

Symptom: `bd` returns a database-lock error.

Cause: storage-engine contention. Two `bd` processes
trying to write at once, or a stale lock file.

Fix: retry as the next natural action. If retries keep
failing, the lock file may be stale — `ls -la .beads/`
to inspect; the workspace's BEADS skill (this one) does
not currently document the manual-unlock path because
recovering from BEADS lock state is a tooling concern, not
a coordination concern.

Per `~/primary/AGENTS.md`: *"If `bd` reports a backend
database-lock error, treat it as transient storage
contention, not coordination ownership."*

---

## See also

- `~/primary/AGENTS.md` §"BEADS is transitional" — the
  upstream framing; BEADS is current convenience, not
  destination.
- `~/primary/skills/autonomous-agent.md` §"Shared
  workspace work needs orchestration" — when to file a
  BEADS task for blocked work.
- `~/primary/skills/reporting.md` §"Hygiene — soft cap,
  supersession, periodic review" — the parallel
  hygiene discipline for designer reports.
- `~/primary/reports/designer/68-architecture-amalgamation-and-review-plan.md`
  §11 — the workspace's current open-beads inventory.
- `~/primary/reports/designer/4-persona-messaging-design.md`
  — the messaging fabric BEADS will eventually be
  superseded by.
