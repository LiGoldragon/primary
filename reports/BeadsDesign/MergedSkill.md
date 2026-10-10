# Merged psyche-vision skill — draft for attack

Draft only. Nothing was edited: no manifest, no skill source, no file in
`LiGoldragon/skills`. Everything below is proposed text.

Revised for the three-way merge. The earlier draft merged `context-handover` and
`work-tracking` under the name `beads`; the psyche has since folded
`psyche-vision` in and named the result. The content rule, the recovered
lock-retry and staleness doctrine, the field set, the pickup half, and the
not-one-store finding all stand unchanged.

Read the open questions in the last section before shipping any of this. One of
them contradicts a factual premise I was given.

## Decisions

**Name: `psyche-vision`.** The psyche named it. My `beads` recommendation is
withdrawn.

Worth recording that this settles the naming tension I flagged rather than
overriding it. I had written that `beads` names a tool while his own rule says
"Skills name capabilities. Workspaces name the implementations that fill them,"
and that I was taking the weaker reading. `psyche-vision` is the capability;
beads and handovers are two implementations of it. His name obeys his rule and
mine did not.

**The corpus goes 22 to 20.** `context-handover`, `work-tracking`, and
`psyche-vision` become one entry.

**Description:**

```
Use when the psyche states a goal, when recording one so a later agent can pick it up, or when handing work to the next session.
```

Three triggers, each observable before the work starts, and they cover both
halves of the scope. The first fires on recognition, the second and third on
transmission. The previous proposal fired only on the transmission half.

The manifest line it would replace, for reference only:

```nota
(Skill (psyche-vision psyche-vision Meta Mechanism [|Use when the psyche states a goal, when recording one so a later agent can pick it up, or when handing work to the next session.|] [AgentsSkill ClaudeSkill]))
```

Category is `Meta Mechanism`. The old `psyche-vision` was `Meta Topic` and
`context-handover` was `Meta Mechanism`; the merged skill carries procedures, so
`Mechanism` is right and `Meta` survives from two of the three sources.

**What psyche vision is.** One sentence, plus one sentence excluding the
mechanism:

```
Psyche vision is the goal the psyche wants and his reasoning for it.
A mechanism for reaching that goal is not part of it.
```

Derived from what he has ruled, not from AGENTS.md. Three things fell out of
that constraint:

- It does not say "load-bearing will", "aims, values, beliefs, priorities", or "decides whole classes of choices". That is AGENTS.md's definition of *intent*, and the deployed `psyche-vision` copied it nearly word for word. He rejected it as wrong for vision.
- It says nothing about sorting vision from matter, because he ruled vision *is* matter. The consequence an agent needs is a destination, not a taxonomy, so the skill carries one routing line — `Route vision to a bead or the design log, never to Spirit.` — and no classification apparatus.
- It is the content rule stated as a definition. The content rule is the same sentence stated as an instruction. Recognition and transmission are one rule, so the skill states the definition once and the instruction once, and nothing else repeats it.

**The unification.** His framing is that a bead is vision passed to a future
agent and a handover is vision passed to a future session. I did not write that
as a sentence, because as two parallel clauses it is exactly the matched-pair
shape he rejects. It appears instead as the one line that directs the choice:
`Carry vision forward in a bead when the work outlives the session or another
agent picks it up, and in a handover when the next session continues the same
thread.`

**Field set: `title`, `description`, `issue_type` when `decision`, `priority`
when raised, and `blocks` / `parent-child` dependencies. Nothing else.**

Dropped, with counts from the live store: `acceptance_criteria` (495/1515),
`labels` (1347/1515), `notes` (315/1515), `assignee` (79/1515), `design`
(14/1515), `spec_id` (9/1515), and everything the CLI offers but the store never
carried. Reasoning per field is in "Lines cut" below. The single line
`Leave the remaining fields at their defaults.` removes all of them at once, so
the skill never has to name a field it does not want used.

**Handovers.** A handover becomes a set of beads plus a response. The goals go
into beads before the handover is written; the handover names them. The prose
with no bead field splits three ways: a standing psyche invariant goes to the
intent log, a characterization of how the psyche works goes to
`psyche-interraction` as doctrine rather than being rewritten per handover, and
the session's own chronology and self-critique stay in chat. The landed-work
table disappears entirely into close reasons on the closed beads — the CriomOS
store already does exactly this (`"Full merge landed on main at 68279001."`,
`"Merged CriomOS main c256c13b2e0e and deployed host generation 93"`).

A handover stays a report only when the substance is a durable analysis that a
description cannot hold — a research corpus, a design pickup point. Then the
bead names the goal and points at the report, and the report carries the
substance. That is `AGENTS.md`'s existing report rule; the skill does not
restate it.

**Scope: reading and writing both.** The content rule only works if the agent
picking a bead up knows to take its approach from standards. A write-only skill
would leave undefined the half the rule exists for. Reading is also where the
Dolt lock hits, where `bd sql` fails, and where staleness gets judged.

**One thing the merge fixes on its own.** Two of the three sources define psyche
vision, and they do not agree. `context-handover` says it is "the psyche's aims,
values, priorities, and desired outcome for the work" — goal-shaped, close to
right. `psyche-vision` says it is "the psyche's load-bearing will: the aims,
values, beliefs, and priorities that decide whole classes of choices" —
intent-shaped, and the definition he rejected. An agent that loaded both got two
answers. After the merge there is one.

## Source 1 — current `context-handover`

`/git/github.com/LiGoldragon/skills/skills/context-handover.md`, verbatim:

```markdown
Write the handover in the response.
## Psyche vision
Psyche vision is the psyche's aims, values, priorities, and desired outcome for the work.
Preserve every non-repetitive, load-bearing psyche statement in recognizable language and full resolution.
## References
Include only the references needed to resume the thread.
```

## Source 2 — current `work-tracking`

`/git/github.com/LiGoldragon/skills/skills/work-tracking.md`, verbatim:

```markdown
# Skill — work tracking

- Track work only when it must survive the session or coordinate independent work.
- Give each item an outcome, proof, and dependencies.
- Close an item only with durable evidence.
```

## Source 3 — current `psyche-vision`

The deployed file, `/home/li/primary/.claude/skills/psyche-vision/SKILL.md`,
verbatim including frontmatter. None of it survives.

````markdown
---
name: psyche-vision
description: 'Psyche vision rules.'
---

# Psyche vision

Psyche vision is the psyche's load-bearing will: the aims, values, beliefs, and
priorities that decide whole classes of choices.

## Test

Ask whether the statement would still guide the work if every current mechanism
were replaced. If yes, it is vision. If no, it is matter.

## Not vision

A mechanism, artifact, name, status, or implementation decision.
Approval, recency, and emotional salience do not turn matter into vision.

## Handling

Never infer or manufacture vision.
When a statement is not clearly vision, treat it as matter.
````

The skills-repo source at `/git/github.com/LiGoldragon/skills/skills/psyche-vision.md`
is the same body without frontmatter.

## Source 4 — current `bead-weaver`

Not named in the task, but it is the third live surface about the same artifact.
`/git/github.com/LiGoldragon/skills/skills/bead-weaver.md`, verbatim:

```markdown
# Module — work graph

- Create tracked work only when independent work or durable coordination needs it.
- Give each item an outcome, proof, boundary, and dependency.
- Do not claim `.beads/`.
```

It is a `RoleComposition` module, not a runtime skill. If the merged skill ships,
this becomes a second statement of the same rules. Recommendation is in the open
questions.

## Recovered — `modules/work-tracking/full.md` at `7f5753642f1d^`

Verbatim, whole file:

```markdown
# Skill — work tracking

## Use work items for short tracked work

A bead is a small work item with enough context, acceptance criteria, and dependency links for another agent to pick up. Use beads when work must survive the session or coordinate with other work.

## Claim before working

Before editing for a bead, inspect its state and dependencies. Claim only the bead you are actively working. Do not claim a broad area to reserve it.

Record the claim in the tracker surface the repo uses. If no tracker is configured, ask or use the task's explicit instruction.

## Retry transient tracker locks

Run `bd` tracker commands sequentially, not through parallel tool calls or
concurrent shells. `bd` uses a single-writer embedded Dolt store; if a command
reports the exclusive `.beads/embeddeddolt` lock, wait for the owning operation
to finish and retry the same command. Do not spawn concurrent retries. Treat the
lock as a blocker only after several short retries fail, and report the exact
command and error.

## Keep bead text executable

A good bead states:

- the desired outcome;
- the owning repo or component by canonical name;
- files or surfaces likely involved;
- acceptance criteria;
- dependencies and blockers;
- verification expected.

Avoid transcript, speculation, and generic how-to prose.

## Split by acceptance boundary

Split a bead when part of the work can land and be verified independently. Keep a bead together when the acceptance proof is one atomic behavior.

Dependencies are directional: producer before consumer, schema before generated code, contract before implementation, migration before removal.

## Update as facts change

When discovery changes scope, update the bead with observed facts and the new blocker or split. Do not rewrite history into certainty. Keep comments concise and evidence-backed.

## Weigh age when judging staleness

Age is an important factor in a bead's staleness, though not the sole test and not an auto-close threshold. The older an open bead, the more its retention must be justified rather than assumed: as a rough gradient, roughly two weeks old is suspicious and about a month old is strongly suspect. Keep an old bead only when it still maps to an actively developed line of work, shown by recent commits; otherwise treat it as a candidate to close as invalidated with a reversible reason. When triaging a backlog, sort by age and scrutinize the oldest first.

## Close with evidence

Close a bead only after the acceptance criteria pass or the bead is explicitly invalidated. Include commit identifiers, commands run, and any remaining follow-up bead. If blocked, leave it open and name the blocker.

## Anti-patterns

- beads that restate a prompt without acceptance criteria;
- umbrella beads that hide independent work;
- closing because code was written but not validated;
- keeping an old bead open by inertia when nothing active maps to it;
- using comments as an archive;
- creating repo-specific process doctrine in the bead body.
```

## Recovered — `modules/bead-weaver/full.md` at `7f5753642f1d^`

Verbatim, whole file:

````markdown
# Module - bead weaver

## Rules

Use beads only after intent is aligned enough to decompose into independently actionable work. Do not file speculative beads to force unresolved design shape or split a clear routine linear operation that one implementation worker can complete.

A weave is a dependency graph of discrete jobs. Each bead needs a clear goal, definition of done, evidence signal, constraints, and out-of-scope boundary. Do not file beads for permanent disciplines, broad concerns, or unresolved decisions; land those in the owning guidance or architecture surface.

Build from outcomes backward:

1. Name the final observable outcome.
2. Name the smallest proof that shows it works.
3. Name prerequisites that can ship independently.
4. Put architecture or schema decisions before implementation beads that would otherwise guess.
5. Put verification beads after the build beads they witness.

Prefer a thin first slice over a broad backlog.

## Filing

Create descriptive titles and wire dependencies explicitly:

```sh
bd create "<title>" -t task -p <priority> -d "<description>"
bd dep <blocker-bead> --blocks <blocked-bead>
```

File blockers first so dependency commands read in work order. Read the graph back with `bd show` or `bd list` and fix unclear descriptions immediately.

Run `bd` commands sequentially, not through parallel tool calls. If embedded
Dolt reports the exclusive `.beads/embeddeddolt` lock, wait for the owning
operation to finish and retry the same command; do not spawn concurrent retries.

Do not claim `.beads/`. Treat an Orchestrate `.beads/` claim as invalid agent policy state; force-release or remove it instead of treating it as a lock. If you begin working a bead after filing it, claim the task if the workspace uses claims; filing alone is not a claim.
````

## Recovered — `modules/context-handover/full.md` at `7f5753642f1d^`

Verbatim, whole file:

```markdown
# Skill — context handover

## Rules

When the psyche requests a handover with an explicit next-session focus, write only for that focus. Strip unrelated matter.

When the psyche requests a handover without an explicit focus, infer the focus from the active session. Anchor on the session's original intended direction: how it began, the first accepted objective, or the first clear psyche-stated goal. Side issues may become evidence, blockers, constraints, open questions, or follow-up lanes, but they do not replace the original direction unless the psyche explicitly redirects or the original direction has been thoroughly addressed.

Ask for focus only when the original direction, later redirects, and unresolved work create genuinely competing handover targets. Do not default to the subject of the most recent prompt unless the psyche explicitly narrowed the handover to that subject.

A handover's whole purpose is to carry the psyche's invariants and vision — his unbending directives and the direction he holds — as cleanly as possible into a fresh context, so the next session can think fresh. First and foremost it is that transfer: a focus-scoped freshness aid, not a chronology of what the session did, a comprehensive change-list, a plan, a transcript, a correction log, or a display of agent reasoning.

The agent holding the session's accumulated context writes the handover itself; context only that agent holds cannot be delegated to a subagent that holds none of it.

Do not relay what sub-agents reported as known fact. The writing agent did not witness that work firsthand, so forwarding it presents secondhand claims as knowledge. Point instead to the durable artifacts that hold the truth — commits, ARCHITECTURE.md, beads.

Handover ends active lanes. Do not inherit a lane through handover; the next worker receives a new lane or an explicit Recovery registration.

Print handover content in the agent response. Never write a handover to a file.

Carry the settled current term, shape, or decision. Resolved correction history is not handover context unless the psyche explicitly asks to preserve it or a worker output says the earlier term remains relevant.

Keep it lean. Lead with the psyche's invariants and vision, then confirmed facts, live uncertainties or suspicions with their uncertainty preserved, open questions, and pointers to the durable artifacts that already hold completed work. Do not narrate that work as a change-list.

Exclude the session's own opinions, recommendations, and interpretive framings; importing the former session's patterns of thought pollutes the fresh context with views that were never psyche intent. Carry such a framing only when the psyche explicitly endorsed it, and then attribute it as psyche-settled.

Do not tell the next agent what to do beyond the requested focus. Leave room for questions and independent rediscovery.

State completed changes as completed, open questions as open, and suspicions as suspicions.

Exclude reasoning trails, apologies, tool and work chronology, stale branches, resolved mistakes, routine working-copy state, and instructions the next agent can load from owning surfaces.

Prefer canonical artifact names and concise evidence pointers over long excerpts.

Every line must pass: does this help a fresh agent rediscover the focused matter and the psyche's invariants without inheriting stale opinion? If not, delete it.
```

## Recovered — `skills/beads.md`, the earlier repo-local doctrine

Not in the skills repo. This is the file the 449 staleness audit cited and that
the research report could only quote secondhand. Recovered from `primary`'s own
history at `a7bddc66cdbe^`, its last living revision. Reproduced in full because
it holds three rules nothing else in the corpus has.

````markdown
# Skill — beads

BEADS is the workspace's short-tracked-item store, exposed through the
`bd` CLI. It is **transitional**: the destination is Persona's typed
messaging fabric. Don't deepen the BEADS investment and don't bridge to
Persona; use it for what it's good at today and design new shapes
assuming it goes away.

## Never a bare bead id to the psyche

A bead id like `primary-l89s` is a database handle. The psyche cannot
decode it in their head and has no `bd` to query. When you mention a
bead to the human — chat or report — lead with what it IS and keep the
id to a quiet trailing reference, or drop it from chat entirely. Say
"the runner-extraction work," not "`primary-l89s`". The id exists so
*agents* can find the bead; alone it is noise to the human, and a chat
reply full of bare ids reads as if addressed to a peer machine. Same
for Spirit record numbers. See `reporting.md`.

## When to file a bead

A bead is the right home when **all** of:

1. **It's a discrete unit of work** — has a definition of done; will be
   resolved or explicitly deferred, not "ongoing forever."
2. **It needs cross-session memory** — a chat note or report would be
   lost; the work spans more than one session.
3. **It's not better-tracked elsewhere** — not a code change (file an
   issue or just edit), not a discipline (write a skill), not a design
   decision (write a designer report).

Fits: *"Migrate chroma to current nota-codec API"* — discrete,
concrete, spans sessions, closes when shipped.

## When NOT to file a bead

**Durable-backlog beads.** *"Every X should have Y, incrementally"* is
a discipline statement, not a task — it never closes as one unit and
sits forever as a P2 that doesn't move. Fix: land the rule in the right
skill, and close the bead with a note pointing at the rule. If
visibility into the gap is the value (which repos haven't done X yet?),
that's a workspace doc or a CI check.

**Design questions.** *"Figure out X"* without a definition of done is a
design question; its home is a designer report. Acceptable bead form:
*"Land designer report on X"* — discrete, closes when the report lands.
Not: *"Decide what X should be."*

**Ongoing concerns.** *"Monitor build performance"*, *"keep an eye on
the chroma daemon"* — these are alerting (write the alert), monitoring
(write the dashboard), or noise (don't track).

**Reminders for a small fix.** A bead is heavyweight relative to *"fix
this stale comment next time you're in the file."* If it's a one-line
edit and you're in the file, fix it. If it's forgettable but trivial,
leave a `TODO` next to the code.

## Beads are not ownership locks

Any agent may create, update, comment on, or close any BEADS task at any
time; never claim `.beads/`. The corollary: *"someone filed a bead"*
does not mean *"someone is going to do this work."* Beads are
queue-shaped tracking, not assignment. If no agent picks it up, the bead
sits open until pruned.

## Taking on a bead — the task-lock bridge

When you start work on a bead, claim it through the orchestration
protocol so other agents see the work is in flight. Task locks use typed task tokens:

```sh
orchestrate "(Claim (system-operator [(Task primary-f99)] [chroma migration]))"
# … do the work …
orchestrate "(Release system-operator)"
bd close primary-f99 -r "<closing note>"
```

The daemon enforces exact-match overlap across roles: a second role claiming
`(Task primary-f99)` is rejected.

This bridges two layers BEADS alone doesn't span: BEADS lifecycle
(filed/open/closed — durable, visible via `bd list`) and orchestration
locks (claim/release — in-flight coordination on this machine, visible
via `orchestrate "(Observe Roles)"`). A bead in *open* state doesn't tell
other agents someone is working on it right now; the task lock does.
Without it, two agents race the same bead — each does the work, one push
lands, the other discovers stale commits.

When done, release the lock and close the bead in the same flow. Don't
leave a stale lock after the bead closes; don't close the bead while
still holding the lock.

The same syntax extends to non-BEADS work: `'[pr:42]'` to coordinate
review of a PR, `'[draft:role-redesign]'` for a draft report not yet
filed. The helper treats brackets as exact-match identifiers; projecting
the token to the underlying artifact is the agent's responsibility.

### Beads as session anchors

For any task larger than a tiny one-step edit, ensure a bead names the
goal before the work sprawls. If one exists, claim it with a task lock.
If none exists and the work could survive a context compaction or a
handoff, create one. At session end, read the bead again: if its
definition of done is satisfied, close it; if not, leave the next action
or blocker in the bead before releasing the lock. Don't rely on chat
history or harness memory to carry that state.

## Feature beads carry their branch name

A `feature` bead represents work that lives on a **non-main branch** for
the feature arc — typically spanning more than one commit, often across
multiple repos and agents. `task` beads land directly on main; feature
beads name the parallel branch where the work happens.

The bead description declares the branch name explicitly, near the top:

```text
Branch: horizon-re-engineering
Repos:  horizon-rs, lojix, signal-lojix, CriomOS, CriomOS-home, goldragon
```

For multi-repo features, name every repo whose branch carries the work —
every repo uses the same branch name so any agent picking up the bead
lands on the right surface in each.

**Why:** without an explicit branch name, agents picking up the same
bead at different times each create a fresh branch with a slightly
different name (`feature/horizon`, `horizon-refactor`, …), producing
parallel reimplementations to reconcile or throw away. The bead is the
rendezvous; the branch name makes it concrete on the file system.

**How:**

- When filing a `feature` bead, name the branch before any agent picks
  it up. If unknown, say so: `Branch: TBD — first agent to claim picks
  the name and updates this bead`.
- When picking up a `feature` bead, find the declared branch; if
  missing, comment a branch name before starting so the next agent sees
  what you chose.
- Sub-task beads blocked-by a feature bead inherit the parent's branch
  unless their scope is genuinely narrower.
- Branch names are bare descriptive names (`horizon-re-engineering`),
  not `push-` prefixed — `push-` is for short-lived review-cycle
  bookmarks (`jj.md`); long-lived feature branches use the bare form.
- When the feature lands and merges, close the bead with a note pointing
  at the merge commit, and delete the merged branch in every repo
  (`jj.md`).

`task` beads don't need this — they land on main as small commits with
no parallel branch life.

## When to close a bead

Every closed bead's `-r` reason is the durable record of *why this isn't
tracked anymore*. A future agent finding the id in old git history or a
stale report reads the closing note and knows whether to revive (rare),
reopen (rare), or move on (almost always). The closing note is the
bead's small designer report — name the path forward, point at where the
substance lives now, not just *"done."*

**Shipped.** Close with a note pointing at the canonical home (the
commit, the skill change, the `ARCHITECTURE.md` section):

```sh
bd close primary-8b6 -r "Shipped via chroma daemon (replaces darkman + \
nightshift). See chroma repo HEAD and skills/system-operator.md §'Chroma daemon'."
```

**Superseded.** When a design change renders a bead moot (e.g. a
migration for a derive that no longer exists), close with a note naming
the supersession.

**Duplicate — preserve information from both.** When two beads cover the
same work, closing one as a duplicate must preserve all information from
the closed bead. Competing design ideas in particular are kept rather
than collapsed: agents working those fields compare and essay the
alternatives, and premature collapse destroys that comparison surface.
The closing note absorbs every load-bearing field the closed bead
carried — design substance, alternative approaches, blocker analysis. If
the surviving bead doesn't already carry that content, update its
description before closing the duplicate.

```sh
bd close primary-XYZ -r "Duplicate of primary-ABC (which now carries the \
alternative-approach analysis from this bead). All design substance preserved on primary-ABC."
```

**Reformulated as a discipline.** For a durable-backlog bead, close with
a pointer to where the discipline now lives.

**Won't ship.** When a bead is genuinely abandoned — wrong direction,
not going to happen, cost outweighs benefit — close with a note naming
why. Don't leave zombies open.

## Stale internal references in bead descriptions

Bead descriptions decay the same way reports do — a bead filed against
an old report-number or an old crate name (`NexusVerb`) names something
that no longer exists. Don't fight to keep descriptions current. Two
acceptable approaches:

1. **Description as timestamp** — what was true when filed; edit only
   when actively misleading future agents (rare).
2. **Close + new bead** — when the premise has moved enough that the
   description doesn't survive, close with a forwarding note and file a
   new bead carrying current context.

Default: option 1 + close-as-resolution. Don't accumulate edits trying
to keep descriptions fresh; let the canonical home (skill, report, code)
carry current substance.

## The `bd` CLI shape

| Command | Use |
|---|---|
| `bd list --status open` | Workspace queue |
| `bd show <id>` | Read a single bead's full description + status |
| `bd create "title" -t task -p <P> -d "description"` | File a new bead |
| `bd close <id> -r "<closing note>"` | Close with reason |
| `bd dep <a> --blocks <b>` | a blocks b |
| `bd dep remove <blocker> <blocked>` | undo |

Priorities (`-p`): `1` (urgent), `2` (normal), `3` (deferred). Types
(`-t`): `task` (default), or other types the project defines. For the
full reference and project conventions, see `lore/bd/basic-usage.md` if
it exists, or `bd help <command>`.

## Periodic audit

A workspace's open-beads list should be small (~5-15 items) and most
beads should be *moving* (recently filed, updated, or closed). When it
grows past ~15 items or contains beads filed weeks ago that haven't
moved, audit each open bead:

1. Still load-bearing? Stale → close (per "When to close").
2. Active but stuck → name the blocker (closing note or updated
   description).
3. Active and unstuck → name what it needs to move.

The audit produces a designer report.

## When `.beads/` reports a database lock

Symptom: `bd` returns a database-lock error. Cause: storage-engine
contention — two `bd` processes writing at once, or a stale lock file.
Treat it as transient storage contention, not coordination ownership.
Fix: retry as the next natural action. If retries keep failing, the lock
file may be stale — `ls -la .beads/` to inspect. Recovering from lock
state is a tooling concern, not a coordination one.

## See also

- `autonomous-agent.md` — when to file a BEADS task for blocked work.
- `reporting.md` — the parallel hygiene discipline for designer reports.
- `jj.md` — branch-naming and bookmark cleanup after merge.
````

## Proposed merged skill

Ready to paste as `skills/psyche-vision.md` in `LiGoldragon/skills`.

```markdown
# Skill — psyche vision

Psyche vision is the goal the psyche wants and his reasoning for it.
A mechanism for reaching that goal is not part of it.

## Carrying it

Record the goal and the reasoning.
Leave out how the work is done.
Preserve every non-repetitive, load-bearing psyche statement in recognizable language and full resolution.
Add only the references needed to find where the work lives.
Carry vision forward in a bead when the work outlives the session or another agent picks it up, and in a handover when the next session continues the same thread.
Route vision to a bead or the design log, never to Spirit.
Land a standing rule in the skill that owns it instead of a bead.
Keep substance in its owning artifact and point at it.

## Bead fields

Fill `title` and `description`. Leave the remaining fields at their defaults.
Set `issue_type` to `decision` for a question only the psyche can answer.
Raise `priority` above its default only when the bead outranks work already open.
Link with `blocks` when one bead must land before another, and with `parent-child` when one bead decomposes into several.
Split a bead when a part of it can land and be observed on its own.

## Picking a bead up

Take the approach from the standards repository, not from the bead.
Read the bead's references before re-deriving what they hold.

## Running bd

Run `bd` from the directory whose store the bead belongs to, and confirm it with `bd where` before the first write.
Pass `--actor <your role>` on every write.
Run `bd` commands one at a time, never through parallel tool calls or concurrent shells.
On the `.beads/embeddeddolt` exclusive-lock error, wait and retry the same command. Report the lock as a blocker only after several retries fail.
Read the store with `bd list`, `bd query`, and `bd show`, and the whole corpus with `bd export --all -o <file>`.
`bd sql` does not run against this backend.
Leave `.beads/` unclaimed.

## Age

Sort an open backlog by age and triage the oldest first.
Justify keeping an open bead past two weeks by recent commits on the work it names.
Close a bead open past a month that no recent commit maps to, with a reason naming what replaced it.

## Closing

Close a bead after its outcome is observed, and record the observation and its commit in the close reason.
Leave a bead open and name the blocker when its outcome is not observed.

## Handover

Write the handover in the response.
File the goals the next session needs as beads first, then name those beads in the handover.
Name a bead to the psyche by what it is, and keep its id to a trailing reference.
```

Thirty-two lines, of which two are the definition. The three skills it replaces
carry fourteen between them. The recovered sources carry roughly three hundred.

The definition and `Record the goal and the reasoning.` / `Leave out how the work
is done.` are the same rule twice, once for recognition and once for
transmission. That repetition is the merge's whole point and is the only
repetition in the file.

## Lines kept, and from where

From current `context-handover`, kept verbatim:

- `Write the handover in the response.`
- `Preserve every non-repetitive, load-bearing psyche statement in recognizable language and full resolution.`

From current `context-handover`, kept in substance: `Include only the references
needed to resume the thread.` became `Add only the references needed to find
where the work lives.` The phrasing moved from thread-resumption to work-location
because under the merge the reference sits on a bead, not in a document, and may
be read months later by an agent with no thread to resume.

From current `work-tracking`, kept in substance:

- `Track work only when it must survive the session or coordinate independent work.` folded into the carry-vision-forward line, which now states both carriers and both triggers in one rule.
- `Close an item only with durable evidence.` became the close-after-observed line, with the evidence made specific: the observation and its commit.

`Give each item an outcome, proof, and dependencies.` was cut — see below.

From current `psyche-vision`, kept: nothing verbatim. One line survives in
substance and inverted. `When a statement is not clearly vision, treat it as
matter.` presumed a boundary between the two; since vision is matter, what an
agent actually needs is the destination, and that became `Route vision to a bead
or the design log, never to Spirit.`

From current `bead-weaver`: `Do not claim `.beads/`.` kept as `Leave `.beads/`
unclaimed.`

From recovered `work-tracking/full.md`:

- The whole sequential-lock-retry rule, compressed from five sentences to two lines. This is the single most-recovered item; it was independently rediscovered twice (the pre-slashdown module and the June 1 operator postmortem) before being deleted.
- `Treat the lock as a blocker only after several short retries fail` kept as the retry-exhaustion line.
- The age gradient, both thresholds. Two weeks and one month survive as the two lines in the Age section.
- `When triaging a backlog, sort by age and scrutinize the oldest first.` kept nearly verbatim.
- `Split a bead when part of the work can land and be verified independently.` kept, with "verified" changed to "observed" to match the closing rule's language.
- `If blocked, leave it open and name the blocker.` kept.

From recovered `skills/beads.md`:

- The bare-bead-id rule, compressed from a paragraph to one line. Provenance is strong: commit `962edf9cd8de` records it as a psyche correction — "do not address the human as a query-capable machine".
- `not a discipline (write a skill)` and the durable-backlog section, compressed to `Land a standing rule in the skill that owns it instead of a bead.` This is the rule the 449 audit's Pattern 4 was about.
- The closing-note-as-record principle, compressed into the close-reason line and the stale-close line.

## Lines cut, and why

### The whole of the old `psyche-vision`

**The definition — `Psyche vision is the psyche's load-bearing will: the aims,
values, beliefs, and priorities that decide whole classes of choices.`** This is
AGENTS.md's definition of *intent* with the word changed: AGENTS.md has "an aim,
value, or belief he holds against his own convenience and that bends a whole
class of downstream choices." Two surfaces defining two different things
identically is how vision came to be routed to Spirit. Replaced by the
goal-and-reasoning definition.

**The `## Test`** — `Ask whether the statement would still guide the work if
every current mechanism were replaced. If yes, it is vision. If no, it is
matter.` Void. It sorts vision from matter, and vision is matter, so every
correct answer to it is "matter" and the test returns nothing. It is also built
as a matched pair.

**The `## Not vision` list** — `A mechanism, artifact, name, status, or
implementation decision.` and `Approval, recency, and emotional salience do not
turn matter into vision.` A negative-example list, which is forbidden. The first
line's content survives positively: the definition says a mechanism is not part
of vision, and `Leave out how the work is done.` directs the action. The second
line has no positive form because it exists only to defend the void test.

**`Never infer or manufacture vision.`** AGENTS.md already carries `when unsure,
ask instead of inferring`, and `tenets` already carries `Never pretend to know
what you don't know`. A third statement changes nothing.

**`When a statement is not clearly vision, treat it as matter.`** AGENTS.md:
`When it is not clearly intent, it is matter.` Same line, and under the new
ruling the disjunction it describes does not exist.

**The frontmatter description `'Psyche vision rules.'`** — the exact placeholder
the corpus effort exists to remove, and it was already named as open question 6
in the `SkillsCorpusRedesign` handover.

### From the other sources

**`Give each item an outcome, proof, and dependencies.`** (current
`work-tracking`) — "proof" is the acceptance-criteria field under another name,
and it is what the content rule removes. Proof at write time is a guess about a
mechanism that will have changed by pickup. Proof at close time is an
observation, and that survives in the Closing section.

**`acceptance_criteria` as a field, and every line about it.** The recovered
doctrine leaned on it hard, including the anti-pattern "beads that restate a
prompt without acceptance criteria." I dropped it because acceptance criteria in
practice is where the how-to goes: a criterion phrased as an outcome is already
the goal, and a criterion phrased as a check is a mechanism from the standards of
the day. Stating the goal so its achievement is checkable does the same work with
one field instead of two. This is a deliberate override of recovered doctrine and
the most likely place I am wrong.

**`labels`, including the `role:*` convention** (1347/1515 records carry labels).
Cut because a role label ties a permanent record to a transient organizational
term. The store carries 66 records labelled `role:system-specialist`, a lane name
the 449 audit documents as retired. Also, which role does the work is a
how-question.

**`assignee`** (79/1515) — the recovered doctrine already says beads are
queue-shaped tracking, not assignment, and that "someone filed a bead" does not
mean someone will do it. An assignee field contradicts that in the schema.

**`notes`** (315/1515) — the research found the `primary-56d1` epic carrying
several kilobytes of running ruling text in one `notes` field. `Keep substance in
its owning artifact and point the bead at it.` replaces it.

**`design`** (14/1515), **`spec_id`** (9/1515) — under 1% each. A field the
practice does not use.

**`epic` as a type.** The store has 55. The 449 audit: "the bead store's 'epic'
abstraction has soured... The pivot made every epic's definition of done
unreachable." `parent-child` covers decomposition without a type whose lifecycle
never closes. Excluded by omission, not by a prohibition.

**`feature` beads carrying a branch name** (recovered `skills/beads.md`, a whole
section) — a branch name is a mechanism, and naming it in the bead is the exact
shape the content rule forbids. The failure it prevented was real (parallel
reimplementations under divergent branch names). Naming that failure as still-open
in the questions below rather than keeping the rule.

**The task-lock bridge** (recovered `skills/beads.md`, a whole section) — it
predates the current Orchestrate lane model, and `edit-coordination` now covers
claiming. Its own premise is also gone: `edit-coordination` states "A claim is
advisory bookkeeping. Nothing is locked."

**"BEADS is transitional; Persona replaces it"** (recovered `skills/beads.md`,
opening paragraph; also the deleted `AGENTS.md` section) — Persona-the-messaging-
fabric has no evidence of existing, the workspace has kept using `bd` for eleven
weeks since, and a skill that opens by telling the reader its subject is going
away teaches nothing.

**The anti-pattern list, as a list.** Negative examples are forbidden. Four of
the six items survive as positive rules: umbrella beads became the split line,
closing unvalidated became the close-after-observed line, inertia became the Age
section, comments-as-archive became the owning-artifact line. Two were dropped:
the acceptance-criteria one for the reason above, and "creating repo-specific
process doctrine in the bead body" because the content rule is strictly stronger.

**The periodic-audit procedure and the ~5-15 open-bead target** (recovered
`skills/beads.md`) — the store has run at 209-364 open beads for three months. A
target the practice has never met once is not a rule, it is a wish. The Age
section directs the same triage without a number that gets ignored.

**"The audit produces a designer report."** — `AGENTS.md` governs when to write a
report.

**Focus selection for handovers** (recovered `context-handover/full.md`, first
three paragraphs) — under the merge the focus is the bead, so there is nothing to
scope.

**The handover exclusion list** (recovered `context-handover/full.md`: "Exclude
reasoning trails, apologies, tool and work chronology, stale branches, resolved
mistakes, routine working-copy state") — a list of what not to write.

**"Every line must pass: does this help a fresh agent..."** — a test the agent
applies to its own prose, which is what a capable model does untold.

**Twelve further paragraphs of recovered `context-handover` doctrine** on
subagent relay, lane inheritance, correction history, framing attribution, and
tense discipline. Each is either covered by `tenets` (do not relay a subagent's
claim as fact), covered by `edit-coordination` (lanes), or ordinary.

## Lines added, and the failure each prevents

**`Psyche vision is the goal the psyche wants and his reasoning for it.` /
`A mechanism for reaching that goal is not part of it.`**

Two definitions of vision were live in the corpus at once and neither was his
(quoted above under Source 1 and Source 3). The failure is the one that already
happened: vision defined as intent gets routed to Spirit, and the routing line
alone would not have stopped an agent that had read the old definition.

**`Route vision to a bead or the design log, never to Spirit.`**

The consequence of his ruling that vision is matter, stated as a destination
instead of a taxonomy. The old skill's `Test` and `Not vision` sections existed
to make this call and got it backwards; one line replaces both.

**`Carry vision forward in a bead when the work outlives the session or another
agent picks it up, and in a handover when the next session continues the same
thread.`**

His unification, written as the choice an agent has to make rather than as the
observation that the two are the same act. Before the merge an agent had two
skills and no line telling it which carrier applies.

**`Run `bd` from the directory whose store the bead belongs to, and confirm it
with `bd where` before the first write.`**

The brief states there is one centralized store. That is not what is on disk.
Six `.beads/` directories hold an `embeddeddolt` database, and three were written
to this month:

| store | `interactions.jsonl` | last write |
|---|---|---|
| `/home/li/primary/.beads` | 696264 bytes | 2026-07-19 |
| `/git/github.com/LiGoldragon/CriomOS/.beads` | 4099 bytes | 2026-07-25 |
| `/git/github.com/LiGoldragon/CriomOS-home/.beads` | 3648 bytes | 2026-07-15 |
| `/git/github.com/LiGoldragon/library/.beads` | 685 bytes | 2026-05-02 |
| `/git/github.com/LiGoldragon/brightness-ctl/.beads` | 0 bytes | 2026-04-23 |
| `/git/github.com/LiGoldragon/clavifaber/.beads` | 0 bytes | 2026-04-23 |

The CriomOS store has its own ID prefix (`CriomOS-c9g`, `CriomOS-syd`), its own
Dolt database name, and was written to yesterday — one day before this task, and
six days *after* the primary store went quiet. `bd --help` confirms the mechanism:
`--db string  Database path (default: auto-discover .beads/*.db)`. `bd where`
from primary reports `prefix: primary`.

The failure this prevents: an agent working in a repo files a bead that lands in
that repo's store, invisible to every query run from primary, and no error is
raised. This is the one line I added against the brief's stated facts rather than
in support of them. See the open questions.

**`Pass `--actor <your role>` on every write.`**

`created_by` is `li` on 1487 of 1515 records because `--actor` defaults to
`$BEADS_ACTOR`, git `user.name`, then `$USER`, and every agent runs as the same
Unix user. The store cannot tell a goal the psyche set from one an agent invented.
A skill whose subject is the psyche's vision depends on that distinction, and the
failure is an agent months later reading its predecessor's invention as the
psyche's goal. `--actor` is a global flag and needs no schema change.

This is a change to how the store is written, and the psyche has not ruled on it.
It is listed as an open question rather than assumed settled.

**`Take the approach from the standards repository, not from the bead.`**

The content rule stated for the reader rather than the writer. Without it the
rule is half-installed: the writer omits the approach and the reader has nowhere
to get one.

**`Read the bead's references before re-deriving what they hold.`**

The real handover at `reports/SkillsCorpusRedesign/context-handover.md` carries a
section titled "Research already paid for, still unconsumed", listing six
commissioned research documents that never reached the corpus. That is the
failure: references were carried and not read.

**`Set `issue_type` to `decision` for a question only the psyche can answer.`**

The handover's "Open, needing the psyche" section is twelve numbered items with
no destination. As beads they become queryable, and the work waiting on each one
gets a real `blocks` edge instead of a prose sentence. The type already exists in
the store with 12 records.

**`Raise `priority` above its default only when the bead outranks work already
open.`**

640 of 1515 records are P1 and 708 are P2. P1 covers 42% of the corpus, which
makes it indistinguishable from the default. The line directs the comparison that
keeps the field meaning something.

**`Read the store with `bd list`, `bd query`, and `bd show`, and the whole corpus
with `bd export --all -o <file>`.` / ``bd sql` does not run against this
backend.`**

A Dolt-backed store invites SQL. `bd sql` returns "not yet supported in embedded
mode". The research lost a turn to this.

## Worked example — a well-formed bead

Taken from open question 9 of the real handover. Every line is vision, goal,
intention, or reference.

```sh
bd create "Skill descriptions become authored source" \
  --actor write-critical \
  -d 'The description is the field the harness reads to decide whether to load a
skill. Most of the corpus generates it from the skill name, so selection runs on
noise: "Mermaid rules.", "Psyche vision rules."

Each description states when the skill applies, in terms a dispatcher can answer
about a task before starting it.

References:
  manifests/active-outputs.nota in LiGoldragon/skills carries the field.
  reports/BeadsDesign/Research.md section 10 on how the three loaders read it.'
```

Nothing here says which file to edit first, what to grep for, how to regenerate,
or what to validate. An agent picking this up in September gets the goal and the
two places to look, and takes its method from standards as they stand then.

The close, when it lands:

```sh
bd close primary-XXXX -r "All 22 active-outputs descriptions authored; \
LiGoldragon/skills <commit>. Generator no longer derives description from name."
```

That close reason is what replaces the handover's "What landed" table. The
CriomOS store already writes them this way.

## Worked example — a handover-sized bead

The `SkillsCorpusRedesign` handover is 211 lines. As beads it is one parent and
twelve children, and about half the document does not survive because it was
never a goal.

Parent:

```sh
bd create "Skills and roles redesign" \
  --actor write-critical \
  -d 'An instruction earns its place only by changing behavior. The test is
unusualness: agents already behave in the usual way, so a line matching what an
agent would do untold changes nothing. The unusual line is load-bearing and is
cut last.

A rule needs evidence. Write a rule only when it prevents a failure that has
happened, or states a choice an agent cannot derive. Name the incident or the
choice. If you can name neither, do not write the rule.

Minimalism means cutting what carries nothing. It never means compressing what
carries something into a tautology.

Three destinations for every line: skills carry behavior, standards carry domain
facts, everything else goes.

Repositories are independent; each documents itself. Skills name capabilities;
workspaces name the implementations that fill them.

The psyche owns doctrine. Agents may flag harmful or unclear guidance. They do
not infer authority to rewrite it.

References:
  LiGoldragon/skills, manifests/ and skills/.
  7f5753642f1d^ holds the pre-slashdown corpus.
  agent-outputs/ holds six commissioned research documents, unconsumed.'
```

Children, each its own bead with a `parent-child` edge:

```sh
bd create "48 skills reduced to 23" --actor write-critical -d '...'
bd create "nix-usage and nix-discipline merge into one skill" ...
bd create "version-control redesigned" ...
bd create "intent-log states what qualifies as intent" ...
bd create "Skill descriptions become authored source" ...
bd create "14 orphaned RoleComposition modules resolved" ...
bd create "Lane registration has a documented home" ...
bd create "Worktrees stop being created inside the ghq owner directory" ...
bd create "Spirit daemon returns to service" ...
```

Three of the twelve are questions, not work, and take the `decision` type:

```sh
bd create "NOTA optional-effort encoding" -t decision --actor write-critical \
  -d 'Shipped as (claude-haiku-4-5 None) / (gpt-5.4-mini (Some Medium)).
The alternative is [] / [Medium], which admits an invalid two-effort state.
Reference: manifests/role-depths.nota, manifests/model-catalog.nota.'

bd create "Read permission on Codex is prose only" -t decision ...
bd create "Technology and Software as Spirit domains need a home" -t decision ...
```

Then the edges:

```sh
bd dep <decision-bead> --blocks <the-work-that-waits-on-it>
```

What does not become a bead:

- The "Vision" section's invariants are standing psyche will and go to the intent log. The parent bead's description carries them only as the vision for this goal, in his language.
- "Style the psyche wants" and "Style the psyche rejects, in his own words" belong in `skill-designing`, which already absorbed the cut-list and keep-list.
- "How he works" belongs in `psyche-interraction` as doctrine, written once, rather than re-characterized in every handover.
- "What landed" becomes close reasons on nine closed beads.
- "My own failures this session" stays in chat.

The handover response is then short: the parent bead named by what it is, the
three decisions the psyche owes a ruling on, and nothing else.

## Open questions

**1. The bead data is not committed, and the psyche's stated fear is losing work.**

`.beads/.gitignore` excludes the Dolt database, `issues.jsonl`, and
`interactions.jsonl`. Only `config.yaml`, `metadata.json`, `README.md`, and the
`.gitignore` itself are tracked. A handover in `reports/` is committed and
travels with the repo. A bead does not travel at all — it exists on one machine,
in one untracked directory, and `bd gc` deletes closed issues past a 90-day
window while `bd flatten` is documented as irreversible.

Moving the handover into beads therefore moves it from tracked to untracked. I
did not solve this in the skill. It is a storage decision and it is yours.

**2. The store is not centralized, and the skill I wrote says so.**

Evidence in the table above. Three stores were written to this month; the CriomOS
one is the most recently active in the workspace. The brief told me to write "one
centralized store at `/home/li/primary/.beads`"; I could not write that and stay
honest, so the skill says to confirm the store with `bd where` instead.

If centralization is what you want, it is a migration, not a skill line, and the
skill should then say to run `bd` from primary always. If per-repo stores are
what you want, the skill is correct as written but `bd export --all` reads one
store at a time and there is no cross-store query. Either way this needs your
ruling before the skill ships.

**3. `--actor` is a change of practice I proposed without being asked.**

Named again here so it is not shipped by inattention. Drop the line and the store
keeps recording every change as `li`.

**4. `bead-weaver` becomes a third statement of the same rules.**

It is a `RoleComposition` module in `manifests/module-dependencies.nota`, so it
is inlined into role packets rather than loaded at runtime. If the merged skill
ships, `bead-weaver` should be deleted and the roles that composed it should name
`psyche-vision` instead. That would take the corpus from 22 to 20 skills and drop
one module. I did not touch the manifests.

**5. The branch-name rule was cut and its failure is still real.**

Multi-repo feature work under divergent branch names produced parallel
reimplementations. The content rule forbids the fix as written, because a branch
name is a mechanism. It may belong in the standards repository instead. Not
proposing where.

## Weakest lines in my own draft

Named so you do not have to find them.

1. **`Pass `--actor <your role>` on every write.`** Unasked-for, adds friction to every command, and makes new records inconsistent with 1487 old ones.
2. **Dropping `acceptance_criteria` entirely.** It overrides recovered doctrine that treated a missing acceptance criterion as an anti-pattern. My argument is that the content rule subsumes it. If you disagree, this is the field to restore.
3. **`Psyche vision is the goal the psyche wants and his reasoning for it.`** Still the line I am least sure of, though less exposed than in the previous draft: a skill whose stated job is explaining what vision is has a legitimate place for a definition, where a work-tracking skill did not. What remains at risk is the content. You have corrected two attempts at this sentence, and this is a third derived from your rulings rather than offered as my own reading. "Goal" and "reasoning" are the two words carrying it. If either is wrong, the whole skill is aimed wrong.
4. **`Carry vision forward in a bead when the work outlives the session or another agent picks it up, and in a handover when the next session continues the same thread.`** The longest line in the file, and it states two carriers and three triggers. I judged that splitting it would break the unification into the two separate skills the merge exists to end. It may still be one line doing two jobs.

The old fourth item, the name `beads`, is withdrawn.
