# Skill — reporting

*How to write reports, when to write them vs answer in
chat, where they live, and how to reference them. Required
reading for autonomous agents.*

## What this skill is for

Whenever you produce output that explains, proposes,
analyses, or summarises — apply this skill before posting
to the chat. Reports go in files; chat carries pointers.
This skill names the boundary between the two and the
discipline that keeps both clean.

## When to write a report vs answer in chat

The two media have different audiences:

- **Reports are for agents.** Peer roles, future versions of
  yourself, future readers piecing the work back together —
  they consume the report. Reports are durable, scrollable,
  filename-indexed, and citeable by other reports.
- **Chat is for the user.** Read now, acted on now. The user
  is the project's bottleneck on decisions; the chat is their
  working surface.

If your output would be more than a few lines of substance,
**write a report** in the appropriate `reports/<role>/`
subdirectory. The report is the durable artifact other agents
will read.

Then write the **chat reply for the user, with full context
inline**. Don't reduce it to a path pointer when the user has
something to attend to — see §"What goes in chat when a report
exists" below.

Small reports are fine — the report doesn't have to be long.
Acknowledgements, tool-result summaries, "done; pushed"
confirmations don't need reports. Anything that explains,
proposes, analyses, or summarises does.

Routine implementation commits are a named exception to "small
reports are fine": **the commit description is the report for the
code it lands.** Do not create a report whose only purpose is to
repeat a `jj` commit message, changed-file list, and test list. Put
that substance in the commit description itself, where it is bound
to the file changes. Write a report only when there is analysis,
design consequence, audit substance, user-facing decision context,
or a cross-repo synthesis that does not fit in the commit object.

The intended long-term reader for routine landing summaries is a
repository-change ledger daemon that indexes `jj`/Git commits and
their metadata. Until that exists, agents reconstruct routine code
landings from `jj log`, `jj show`, and the pushed branch history,
not from duplicate short reports.

Two reasons reports exist at all:

1. **Chat UIs are poor reading interfaces.** Files are easier —
   scrollable, searchable, linkable, persistent.
2. **Agents reading later need the substance.** A future agent
   picking up the thread can't read your chat; they read the
   report. **This includes future versions of *yourself* after
   context compaction** — your current context is ephemeral, but
   the report on disk survives. Chat is for the user's now-action;
   the report is for the agent's later-reference, by any agent
   including your future self. Reports are also **passable
   objects** — the user can hand the work off to a peer agent by
   naming a path, instead of copy-pasting chat excerpts.

## What goes in chat when a report exists

A report does not relieve the chat of being the user's working
surface. When a report lands, the chat must carry:

1. **The report's path, explicitly named** (per §"Always name
   paths" below).
2. **A 1–3 sentence summary** of what's in the report — what
   was found, what was decided, what changed.
3. **Anything the user must read, decide on, or act on,
   restated with full inline context.** Open questions,
   blockers, surprising findings, recommendations awaiting
   approval — each stated with enough substance that the user
   can engage *without opening the report*.
4. **Any cross-references** — to reports, tasks, IDs, section
   numbers, file paths — carry an inline summary. Never just
   the locator. The user is not navigating a database while
   reading; "see /164 §5.2" without naming what §5.2 says
   creates friction this rule eliminates.

The discipline's deeper reason: **the user is the bottleneck**.
A question or finding that needs the user's attention but sits
inside a report waiting to be opened is a question that takes
longer to answer. The chat is the surface that prevents that
latency. When the chat says *"I wrote a report; here are the
three questions in it that need your attention, each restated
with full context,"* the user can engage immediately without
navigating files.

What does **not** go in chat:

- The full report content (the report is the report).
- Implementation tour, "first I did X then Y" narration.
- Tool-call diagnostics, intermediate state.

What **does** go in chat:

- The report path, named explicitly.
- The headline finding, in 1–3 sentences.
- The user-attention items, each with full inline context.

The chat is short — usually less than one screen. But every
sentence carries substance the user needs to act on.

## Tone in chat replies

**State results. Don't narrate process; don't apologise;
don't pre-announce what you're about to do.** The chat
reply is for what changed and what's next. The *how* and
the *why* belong in the report, not in chat.

## Standard agent behavior — every response paraphrases a report

Per intent record 232, the default operating pattern for every
agent in the workspace is: **every chat response is the
paraphrase of an accompanying per-response report**. The report
is the session log; the chat reply is the paraphrase. The
report holds the substance; chat holds the items the user must
attend to right now.

This extends the shape-trigger rules in `AGENTS.md` §"Reports go
in files; chat is for the user" (per intent 218), it does not
replace them. The shape triggers (mermaid / table / `##` or
`###` headings / multi-paragraph explanation / list of >5
substantive items / code block >10 lines that illustrates a
design) say *when chat content must move to a report*. The
per-response paraphrase says *what the chat carries when the
report is the substance home*: a paraphrase of the report, not
a teaser pointing at it.

The chat reply carries **3-7 most important items**, spread
**more-evenly-than-not** across three categories:

- **(a) Questions / clarifications of intent** — open
  questions the user must answer, ambiguous intent that
  needs clarification, decisions awaiting approval.
- **(b) Observations / suggestions / explanations of how
  new mechanisms work** — substantive findings, design
  proposals, explanations of what changed in the
  architecture or contracts.
- **(c) Examples of recent work or evolving ideas in the
  thread** — concrete artefacts (paths, beads, commits) +
  what's evolving in the current line of work.

The "more-evenly-than-not" balance is the load-bearing
constraint: pure questions miss the substance the agent owes
the user; pure explanations drift toward report-shape; pure
artefact-listing is a status dump. The three-category mix is
how the agent's paraphrase encodes its understanding of the
system back to the user.

**Below 3 items** the response is under-substantive for the
user's attention (the user could have read the bead title
instead). **Above 7 items** the user can't hold the response in
working memory while running parallel agents. The 3-7 bound is
the working-memory budget.

When a per-response report does not exist (acknowledgements,
"done; pushed" confirmations, tool-result summaries), the
standard pattern doesn't apply — those are the small-report
exceptions named under §"When to write a report vs answer in
chat" above. The pattern applies whenever the response has
substance worth a report.

## Always name paths

When you reference a report or any other file the user
might want to navigate to, **name its path explicitly.**

> "Two reports landed: `reports/designer/11-persona-audit.md`
> and `reports/designer/12-no-polling-delivery-design.md`."

…not "two reports landed" without paths. The chat is a
**navigation surface, not a teaser.** Make the user able
to open the file without guessing.

The same rule applies to any file the chat references —
name it explicitly with its path. If the chat says "I
edited the schema," the path of the schema file goes in
the next clause.

## Human-facing references are self-contained

Treat the current response as the user's whole world. The
user should not need to scroll back, query BEADS, open a
report, remember an earlier numbered list, or decode an
internal label before they can answer or judge what you
said.

Whenever a reply mentions a shorthand, identifier, numbered
point, report, BEADS item, actor name, protocol term, or
prior recommendation, **restate the substance inline**.

Examples:

- If you ask about `primary-ar7`, also name the task title
  and why it matters. The ID is a locator, not the context.
- If you discuss "point 6," restate point 6 as a sentence
  before explaining its terms. The number is a locator, not
  the argument.
- If you use a term like `PTY fanout`, define it in relation
  to the concrete recommendation being made. A glossary entry
  without the recommendation is not an answer.
- If you cite a report path, include a one-line summary of the
  relevant claim from that report. The path is a verification
  link, not the substance.

The rule is general: **reference + inline description**. The
description can be short, but it must carry the decision-relevant
meaning. A locator alone creates work for the user; the agent's job
is to remove that work.

## Questions to the user — paste the evidence, not a pointer

When you surface a question for the user — asking for a
decision, clarifying ambiguity, choosing between options —
**the question must carry the substance that lets the user
answer without opening files.**

Wrong:

> *"Should I collapse the four forwarding-trampoline actors?
> See `reports/designer/<N>-actor-discipline-sweep.md` §5.2
> for context."*

This forces the user to open a report and find §5.2 just to
understand what's being asked. The question becomes a chore;
the user disengages.

Right:

> *"Should I collapse the four forwarding-trampoline actors in
> `persona-mind`?*
>
> *Code (`/git/.../persona-mind/src/actors/dispatch.rs:14-18`):*
>
>     pub(super) struct DispatchSupervisor {
>         domain: ActorRef<domain::DomainSupervisor>,
>         view:   ActorRef<view::ViewSupervisor>,
>         reply:  ActorRef<reply::ReplySupervisor>,
>     }
>
> *The struct holds only `ActorRef` fields — no domain state.*
> *The handler routes messages and records trace events. If the*
> *trace recording IS the domain (witnessing the pipeline ran),*
> *keep them. If the trace is observability noise, collapse them*
> *and route straight from request → memory dispatch.*
>
> *Options: (a) collapse, lose per-stage witness; (b) keep and*
> *document the trace-as-domain carve-out; (c) keep but rename*
> *from `*Supervisor` to something less misleading."*

The user reads the question once and has everything needed
to decide.

**The form: question + concrete evidence (code, text, or
symptom) + why it matters + concrete options with
tradeoffs.**

Cite the source report as a "for the longer context" footer
if useful — but the link is a *back-reference for verification,
not the substance*. If the user has to follow the link to
answer the question, the question is not yet asked.

**Why:** the user is the bottleneck on decisions. Forcing
them through navigation chores stalls work and makes them
less likely to engage. The skill's job is to eliminate that
friction. A question that takes 2 minutes to understand will
get answered late or skipped; a question that fits on one
screen with the evidence inline gets answered immediately.

**Applies anywhere a question is surfaced to the user** —
chat, a report's "open questions" section, `AskUserQuestion`
prompts, or a hand-off to another role's report. The rule
follows the question, not the medium.

## Where reports live

Each role owns a subdirectory under `~/primary/reports/`:

- `reports/operator/`
- `reports/operator-assistant/`
- `reports/designer/`
- `reports/designer-assistant/`
- `reports/system-specialist/`
- `reports/poet/`
- `reports/poet-assistant/`

These are **exempt from the claim/release flow** — agents
write reports without coordinating a lock. Each role
writes only into its own role subdirectory; reading any
other role's reports is free.

If you want to **build on** another role's report, rewrite
the relevant content in a new report inside your own
subdirectory. Don't edit another role's reports.

For per-repo reports (specific to one repo's work), the
convention is the same `<N>-<topic>.md` shape under
`<repo-root>/reports/`. See that repo's own `AGENTS.md` /
`ARCHITECTURE.md` for any per-repo refinements.

### Meta-report directories — sub-agent sessions

Per intent record 231, when an agent dispatches sub-agents
to do a coordinated multi-slice piece of work, the whole
session lands as **one meta-report directory** instead of a
flat list of sibling reports:

```
reports/<role>/<N>-<session-name>/
  0-frame-and-method.md       (orchestrator: session frame)
  1-<slice-name>.md           (sub-agent 1)
  2-<slice-name>.md           (sub-agent 2)
  ...
  N-overview.md               (orchestrator: synthesis)
```

The orchestrating agent takes the next number `N` in its
report-subdir's sequence, creates the directory with a
session-name slug (kebab-case, names the session's topic —
e.g. `152-persona-engine-architecture-overview`), and each
sub-agent writes a numbered sub-report inside. The directory
**IS** the meta-report — no `meta-` prefix needed because
being a directory is the signal.

The orchestrator's frame goes in `0-frame-and-method.md`; the
final synthesis goes in the highest-numbered sub-report
(commonly `N-overview.md` or `N-synthesis.md`). Sub-agents own
their numbered sub-reports; the orchestrator owns the frame
and overview plus optionally one or two slices.

**Garbage collection.** The directory is garbage-collectable
as **one session unit**. When the substance migrates to
permanent homes (ARCHITECTURE.md files, skills, ESSENCE.md,
per-repo INTENT.md), the whole directory retires together,
not piece by piece. The retirement lands via a
context-maintenance sweep per §"Context maintenance" below.

**Worked example.** The current session's home —
`reports/second-designer/152-persona-engine-architecture-overview/`
— is the first instance of this pattern. The orchestrating
second-designer dispatched per-component sub-agents; each
sub-agent wrote its numbered slice inside; the overview ties
them together. Read that directory as the canonical worked
example.

### Filename convention

**`<N>-<kind>-<topic-and-title-slug>.md`** where:

- `N` is the next integer after the **highest-numbered report in
  this role's subdirectory.** Per-role, not workspace-wide. No
  leading zeros. No date prefix.
- `<kind>` is a single lowercase word from the closed kind set
  (`design`, `audit`, `research`, `proposal`, `review`,
  `synthesis`, `handover`, `postmortem`) — see §"Kinds of reports".
- `<topic-and-title-slug>` is the report's subject in kebab-case.
  A short date suffix (`-YYYY-MM-DD`) is permitted at the end for
  reports likely to land same-day with another report on the same
  topic; otherwise omit (git captures the date).

Examples for `reports/designer/`:

- `4-design-persona-messaging.md`
- `12-design-no-polling-delivery.md`
- `13-audit-niri-input-gate.md`
- `143-synthesis-designer-state-digest-2026-05-21.md`
- `17-review-recording-system.md`

The kind is inserted between the number and the topic so the
filename answers two questions a reader scans for at a glance:
**which shape is this** (the kind), **what is it about** (the
topic-and-title). The pair maps directly to persona-spirit's
intent record vocabulary (kind + topic + summary) and seeds the
move to persona-mind-managed reports (per intent records 107 +
108).

**Forward-only.** Existing reports without the kind in the
filename are not retroactively renamed. The next time a report
gets a Review refresh (per §"Context maintenance") or is
otherwise touched, the new file takes the new format. The bash
report directories stay readable through the transition.

The topic names the report's subject, not its conversational
ancestry. Avoid names like `response-to-...`, `review-of-...`, or
`audit-of-...` when they hide the actual subject behind another
report number. A future agent should learn what the report is about
from the path without opening a chain of prior reports.

To find the next number, scan **only the current role's
subdir** and take one above the maximum:

```sh
ls ~/primary/reports/<role>/ | grep -E '^[0-9]+-' \
  | sort -t- -k1,1n | tail -1
```

Then `N = (that number) + 1`.

The number is a stable identifier within that role — once
assigned, it does not change. The git log captures the
lineage if a report gets updated.

**Numbering is per-role.** Each role manages its own sequence.
`reports/operator/97-…md` and `reports/designer/97-…md` can
coexist; the role subdirectory in the path is the
disambiguator, not the number. A fresh agent looking at a
single role's subdir sees a coherent chronological sequence
for that role's work.

**Why per-role.** Roles work in parallel and produce reports
on independent cadences. A workspace-wide rule forces every
agent to scan every other role's subdir before numbering and
makes parallel landings collide; per-role numbering lets each
role count its own work without coordinating with peers. When
two reports cite each other across roles, the path
(`reports/<role>/<N>-...md`) carries the disambiguation.

**Cross-references between roles always include the subdir:**
`reports/operator/97-...md` — the role subdir names the
author; the number names the position in *that role's*
sequence.

**Numbers are not reused after deletion within a role.** When
a stale report is removed (see Hygiene below), its number
stays retired in that role's subdirectory. The next report in
that role takes the next-highest-plus-one *within that role's
subdir*, not the freed number. Gaps in a role's listing are a
visible signal that something was retired; the commit history
holds the deleted content.

**Why no dates:** dates collide when more than one report
lands in a day, and the date itself is noise once you have
a unique number. Commit timestamps already record when each
report landed; the filesystem doesn't need to repeat that.

**Iterating on a report — v2 / v3 suffix.** When a topic
is in active back-and-forth with the user or another agent
and the next version is *substantially the same report with
absorbed feedback*, rename the file with a `-v2` (then
`-v3`, …) suffix between the number and the topic:

- v1 (implicit, no suffix): `225-workspace-redesign-direction.md`
- v2: `225-v2-workspace-redesign-direction.md`
- v3: `225-v3-workspace-redesign-direction.md`

If the report path has already been shared with the user or
passed to another agent, this rule is mandatory: do not
silently edit the original path for substantive absorbed
feedback. Publish the successor under the same number with
the next `-vN` suffix, delete the predecessor in the same
commit, and name the new path in chat.

The file under the same number is the canonical current
version. Delete the predecessor in the same commit that
lands the successor — git history holds the lineage.
**Don't accumulate `v1`/`v2`/`v3` side-by-side.**

When the topic shifts enough that the *name after the
number* should change, that is the judgment call where it
becomes a new report. Take the next number, absorb anything
still relevant from the predecessor, then **delete the
predecessor** in the same commit. The pattern:

```
write   reports/<role>/226-new-topic.md  (absorbs /225)
delete  reports/<role>/225-old-topic.md  (same commit)
```

The number sequence is per-role and gap-tolerant; the
deleted number stays retired.

**Why this shape.** Stacking obsolete reports that
recursively partially-supersede each other is harder to
reason about than a single current report with the git log
as the lineage record. Editing in place is fine for light
fixes; renames + deletions are the discipline for real
iteration.

**Why no leading zeros:** numeric-aware sort tools (`ls -v`,
`sort -n`, `sort -t- -k1,1n`) handle non-padded numbers
correctly. Padding adds noise at the cost of needing to
know the maximum digit count up front; the count grows
without warning.

## Kinds of reports — closed set, with destination

Reports are a working surface, not the substance's permanent
home. Every report carries a **kind** (closed set) and a
**topic** (open string). The kind names what the report IS
structurally; the topic names what the report is ABOUT. Both
sit in the filename (per §"Filename convention") and in the
report's metadata header (per §"Report header").

Eight kinds, each with its destination home for the substance.

| Kind | Pattern | Permanent home for the substance |
|---|---|---|
| `design` | Propositional architecture work — a typed contract shape, a protocol, a boundary placement, a new component triad. Carries falsifiable examples; lets operator implement. | **`<repo>/ARCHITECTURE.md`** (when settled). The report is the staging-ground; the ARCH is the destination. Land the report; absorb the substance; retire the report. |
| `audit` | Verification of existing work against current intent or spec. Names what landed cleanly, what drifted, what gap remains. | **Retires when the named gaps land (in new design, new code, or a skill rule).** Audit substance is by definition tied to a moment; once the moment passes, the report goes. |
| `research` | Investigation of a landscape of options — protocols, libraries, models, prior art. Sketches trade-offs without picking. Marks itself as exploratory. | **Retires when a `design` or `proposal` report lands** that picks and justifies. The research informs the choice; the chosen direction is permanent. |
| `proposal` | Test-implementation-ready specification for the operator. Typed records, falsifiable test list, scope boundaries. Hand-off artifact between designer and operator. | **Retires when the implementation acceptance fires green.** The contract has landed in code; the proposal's job is done. |
| `review` | The output of context maintenance (per §"Context maintenance"). Refreshes older substance against current intent + a new wave of research where the older form drifted. | **Supersedes the prior report it refreshed** (delete the predecessor in the same commit). The review itself retires when its own substance gets absorbed elsewhere or a successor review supersedes. |
| `synthesis` | Wide pass across the workspace — digest across multiple reports, state-of-art summary, prioritised questions for the psyche. | **Retires when its questions are answered.** Substance flows into action: closed beads, new design reports, codified skills, ARCH edits. The synthesis is a working artefact. |
| `handover` | Session/lane transition. Catches the next agent up: what's done, what's open, what's load-bearing. | **Retires when the next handover supersedes** or when a session lands its open items. |
| `postmortem` | Reconstruction of a past failure or surprise, with the lessons it teaches. | **Retires once the lessons land in a skill or rule.** The skill inlines the discipline (the "don't reintroduce this" rule, with the *why* stated as part of the rule); the postmortem itself doesn't outlive its migration. Skills do not cite reports — see `skill-editor.md` §"Skills never reference reports". |

The discipline that follows: when you write a report, **name
its kind and its topic before you start writing**, and ask
*what's the destination home for its substance?* If you can't
name all three, the report shouldn't be written — the substance
probably belongs in chat (too small for a report), in a skill
(a discipline statement masquerading as a report), or in ARCH
directly (a decision clear enough to land permanently).

The closed kind set matches persona-spirit's intent record
structure (kind + topic + summary) and prepares reports for the
eventual move into persona-mind-managed storage (per intent
records 107 + 108). The kind set is closed; the topic
vocabulary is open.

## Report header — kind, topic, date

Every report (under the new format) carries a metadata line
**immediately after the title heading**:

```markdown
# 17 — Real-time intent recording system

*Kind: Design · Topic: recording-system · 2026-05-22*

(report body...)
```

Three fields, one line, italicised. The fields:

- **Kind** — the closed-set kind (Design / Audit / Research /
  Proposal / Review / Synthesis / Handover / Postmortem).
  Capitalised. Same value as in the filename.
- **Topic** — the open-string topic. Matches intent topic
  vocabulary (`recording-system`, `lane-management`,
  `persona-orchestrate`, `signal-frame`, etc.). Kebab-case.
- **Date** — `YYYY-MM-DD` when the report was first written.
  Reaffirmed on substantive rewrites; unchanged on small fixes.

The header is the report's primary self-describing surface —
parseable by an agent walking the report tree without opening
each file. When reports move into persona-mind, this header
becomes the typed record shape.

## Hygiene — soft cap, supersession, periodic review

A role's `reports/` subdirectory is a working surface, not
an archive. The git log preserves everything; the filesystem
should hold only what's currently load-bearing.

### Soft cap: 12 reports per role subdirectory

When a role's subdir reaches 12 reports, **the next agent
working in that subdir reviews the older reports** before
adding a 13th. The cap is soft — it's a trigger for review,
not a hard limit that blocks new work. The aim is to keep
the surface small enough that a fresh reader can scan the
listing and understand what's currently active.

### Supersession deletes the older report

When a new report **replaces** an older one — a fresh audit
of the same target, a redesign that obsoletes the prior
design, an architectural pass that supersedes a transitional
sketch — **delete the older report in the same commit that
lands the new one.** The substance lives in the new report;
the lineage lives in the commit history. Don't accumulate
"v1, v2, v3" reports side-by-side.

Before deleting, **update cross-references** in surviving
reports to point at the new one (or remove the citation if
no longer relevant). Dead pointers in surviving reports are
a smell; the cleanup is part of the supersession.

### Periodic review when the subdir gets full

When the count crosses 12, work through the older reports.
For each, decide one of:

| Action | When |
|---|---|
| **Keep** | The report is still load-bearing — current state, active design, decision record someone is still acting on. |
| **Forward into a new report** | The substance is partially still relevant; absorb the live parts into a current report and delete the old one. |
| **Migrate upstream** | Durable substance belongs in `skills/<name>.md`, `<repo>/skills.md`, `<repo>/ARCHITECTURE.md`, `ESSENCE.md`, code, or a `bd` tracked item. Move it there and delete the report. |
| **Remove** | The substance is stale, the work is done, the design has shipped, the decision was reversed — nothing in the report is still load-bearing. Delete. |

The reviewing agent decides these based on **its own
context**. If the agent's current work touches the report's
topic, it has the context to judge directly. If not, the
agent does a brief read of the relevant code, skills, or
recent reports to figure out where the substance lives now;
then decides.

The reviewer's question is always: *what does this report
still teach a future reader that they can't get from
current code, skills, architecture docs, or fresher
reports?* If nothing — delete.

### What gets absorbed, not kept

Foundational decisions and incident lessons used to be candidates
for "kept indefinitely as reports." That pattern is retired:
permanent docs (skills, architecture, `ESSENCE.md`) never cite
reports, so a "kept indefinitely" report is structurally
unreachable from the permanent surface.

What replaces it:

- **Foundational decision records** — the *why* of a direction.
  When the why is load-bearing for understanding the shape, inline
  it into the relevant `ARCHITECTURE.md` (as a constraint, an
  invariant, or a short rationale paragraph) per
  `architecture-editor.md` §"Architecture files never reference
  reports". The decision report then retires.
- **Postmortems** — the "don't reintroduce this" lesson. Inline
  the discipline into the relevant skill (with the why stated as
  part of the rule), then retire the postmortem per
  `skill-editor.md` §"Skills never reference reports".

If the substance genuinely can't be expressed as a permanent
skill/architecture rule, it's not yet ready to be one — the report
stays a report. But the moment the rule is settled, the inlining
is the move; the report retires.

These earn their seat permanently. Most reports don't.

## Context maintenance — research-driven refresh

The Hygiene discipline above (soft cap, supersession, periodic
review) is the **simple** maintenance: stale reports go, load-
bearing reports stay. Context maintenance is the **deeper**
discipline, triggered when the psyche names it explicitly OR
when a report is still semantically relevant but has drifted
against current intent.

The output of context maintenance is a **`review`-kind report**
that brings older substance forward into current state and
supersedes the predecessor (deletes it in the same commit).

### When context maintenance fires

- The psyche asks for it ("do a context maintenance pass," "let's
  refresh," "review the older reports").
- An agent encounters an older report whose substance is still
  load-bearing but has drifted noticeably against recent intent
  — and the agent has the authority + context to refresh it.
- The soft cap (per §Hygiene) is crossed AND the older reports
  carry substance that isn't fully expressible as ARCH/skill
  edits yet.

The discipline is designer-authority work. Assistant lanes can
identify candidates but the refresh itself is designer-level.

### The discipline — four steps

**Step 1 — Read intent first; weight recent over old.** Open
`intent/*.nota` (or use spirit CLI to query) before reading the
older report. Recent intent has more weight than old; a Maximum-
certainty intent record from this week overrides a Medium-
certainty record from last month on the same topic. This is the
load-weight test for whether the older report's framing still
holds.

**Step 2 — Ask: how does the older report relate to the engine,
the architecture, the intent as it is now?** Three possible
answers:

- **Fully aligned.** The older report's substance still holds.
  No refresh needed; the report stays as-is. If the agent is
  doing a sweep, mark it kept and move on.
- **Drifted but recoverable.** The substance is still relevant
  but the framing or specifics no longer fit. Some sections are
  superseded; some still hold; some need new research. → Step 3.
- **Superseded.** The substance is no longer load-bearing; intent
  has moved past it. → Delete per §Hygiene. No review needed.

**Step 3 — Do new research where the older form drifted.** Re-
research the gaps. *Maybe we haven't done enough research even
before* (psyche). The review isn't just a re-edit of the older
text — it's a fresh pass against current state, with the older
substance carried forward where it still holds and new findings
filling where it doesn't.

**Step 4 — Write the review report.** New `review`-kind report
under the lane's reports subdirectory, with the new filename
format (`<N>-review-<topic>.md`) and the metadata header. The
report names what it supersedes in §"What this review supersedes",
states current-state findings in the body, and ends with §"What
substance carries forward / what changed". **Delete the
predecessor in the same commit** that lands the review.

### Why research, not just rewrite

The simple sweep (delete stale, keep load-bearing) doesn't catch
the case where a report is still relevant but its substance has
drifted because the workspace moved. The review's research step
catches that: the older report's framing gets tested against
current intent and recent work, and gaps get filled with new
research before the substance carries forward.

The output is a report that READS AS CURRENT — not as a refresh
of an older report. The lineage lives in §"What this review
supersedes" and in the git log; the prose itself describes
current-state directly.

### Predecessor deletion in same commit

Reviews supersede. The predecessor goes when the review lands —
in the same commit, with cross-references in surviving reports
updated to point at the new path (or removed if no longer
relevant). No `v1`/`v2` side-by-side; git holds the lineage.

This matches the prose-tense rule from §"Tense and framing":
reports describe what IS, and the workspace's report tree
should hold only current-state reports. A review is the
mechanism for bringing older substance into current state.

### What context maintenance is NOT

- Not a deletion ledger. The output is a `review` report, not a
  list of what was removed.
- Not a digest of unchanged reports. If a report is unchanged
  from a sweep, it stays; the maintenance pass is about reports
  that need refresh.
- Not a place to accumulate. Reviews themselves can be reviewed
  later if intent moves again; the tree's value comes from being
  small enough to read.

### The migration to persona-mind

Eventually reports move into persona-mind (per intent record
108). When they do, context maintenance becomes a query: find
reports whose intent dependencies have changed since they were
written, surface them as candidates, write the review records
into persona-mind directly. The filesystem path is transitional;
the discipline is durable.

## The report's medium — prose + visuals

Reports explain shapes, not implementations. Their medium
is **prose plus visuals** — Mermaid diagrams, swimlanes,
flowcharts, tables, dependency graphs.

For Mermaid syntax workarounds (node labels, edge labels,
reserved-word IDs, Mermaid 8.8.0 safe forms for subgraphs,
edge labels, and sequence diagrams), see `skills/mermaid.md`.

### Visuals are Mermaid only — no ASCII text-block diagrams

Per psyche 2026-05-22 (spirit record 243), **every diagram
in a report goes in a Mermaid code block**. ASCII text-block
"diagrams" using box-drawing characters (`┌─┐`, `│`, `└─┘`,
arrows, etc.) are FORBIDDEN. They are error-prone (misaligned
borders, broken arrows, version-specific Unicode), they don't
render as actual diagrams, they accumulate drift, and they
read worse than the Mermaid source they could have been.

If you find yourself reaching for box-drawing characters or
a pre-formatted text block to convey structure, you've
crossed into territory that wants a Mermaid `flowchart`,
`sequenceDiagram`, or `stateDiagram-v2`. Pick the right
Mermaid shape; let the renderer do its job.

The allowance for pre-formatted text blocks stays narrow:
file-tree listings (the output of `tree` or `ls -R`),
shell-command transcripts, NOTA record samples, and short
code snippets are still fine in fenced code blocks because
they're not pretending to be visuals — they're showing the
literal text the report names.

Implementation code (Rust `impl` blocks, function bodies,
struct definitions with methods, full Nix derivations)
**does not belong in reports.** Code in a design doc goes
stale the moment it lands and the real type drifts;
readers can't tell whether the report's snippet or the
repo's actual type is authoritative. Visuals carry the
same information without the freshness trap.

**Test:** if the report has more than a couple of lines
that look like Rust / Python / Nix implementation,
refactor those into a visual.

**The narrow allowance** — a few-line *sample* of the
surface the design talks about (a snippet of a config
showing its shape, a one-line CLI invocation, a single
field declaration to anchor a name) is fine. The rule is
about implementation blocks, not about showing the shape
of the thing the design is about.

## Cross-references — relative paths and prose

When a report references files in sibling repos, link via
`../<repo>/...` (the workspace symlinks). The relative
path resolves in editors and stays valid across repo
renames.

References to other reports use the same shape:

- `reports/designer/<filename>.md` from within `reports/`
- `~/primary/reports/designer/<filename>.md` from outside
  (e.g., a per-repo report)
- `<repo>'s reports/<filename>.md` for cross-repo
  references in prose

Avoid full HTTPS URLs (deep file URLs rot when files
move) — see this workspace's `skills/skill-editor.md` for
the cross-reference convention.

### Inline-summary rule

**Every external section reference must carry a short
inline summary of the cited substance.** Naming a path is
fine; naming a path *plus* a one-line summary of what's
there is what makes the reference useful.

Wrong:

> *"Operator/33 §4 and operator/34 §7 both keep 'explicit
> approval for every proposal' as the default."*

This forces the reader to open both reports and find §4 and
§7 to follow the point. The chat or report becomes a
navigation puzzle.

Right:

> *"Operator/33 §4 (open user-level decisions) and operator/34
> §7 (rules to enforce while refactoring) both keep 'explicit
> approval for every proposal' as the default."*

Or, denser:

> *"The default — explicit approval for every proposal — is
> kept in operator/33 §4 and operator/34 §7."*

The reader picks up the substance from the surrounding
sentence; the path is provided for verification, not for
forcing a lookup.

**The form: `report/N §X (one-line summary)` or surrounding
prose that names the substance, then the path.** Either way
works; what matters is that the reader can follow the point
without opening the cited section.

**Why:** as the report tree grows, cross-references become
dense. A reader navigating four or five reports to follow a
single argument loses the thread. The substance has to live
where the argument is being made, not in the cited section.
The cited path is for verification (and for picking up the
full context if needed); the inline summary is for following
the argument.

**Applies to all external references in reports**, not just
report-to-report. When citing a skill section, an
ARCHITECTURE.md section, or a library text:

> *"`skills/contract-repo.md` §'Kernel extraction trigger'
> (extract when 2+ domain consumers exist) supports this."*

Not just:

> *"See `skills/contract-repo.md` §'Kernel extraction
> trigger'."*

## Tense and framing

**Present tense.** Reports describe what IS — the current
state, the proposed shape, the audit's findings as-of-now.
The path that led here lives in version-control history,
not in the report's prose.

When a direction turns out to be wrong, **rewrite the
report** to state the new direction. Don't accumulate
"v2" / "previously we thought" / strikethrough text — the
git log captures the lineage.

## When report substance becomes durable

When a report contains durable substance that future
agents will need, **move it to the right home** rather
than leaving it in `reports/`:

- Rules for how to act → `skills/<name>.md`
- Repo intent / invariants → `<repo>/skills.md`
- Architecture commitments → `<repo>/ARCHITECTURE.md`
- Workspace intent → `ESSENCE.md`

The report's body either becomes a thin pointer or gets
deleted, depending on whether the report still serves a
narrative purpose (audit findings, decision record).

## See also

- `~/primary/orchestrate/AGENTS.md` §"Reports" — the
  role-coordination side (subdir ownership, exemption
  from claim flow).
- this workspace's `skills/skill-editor.md` — how skills
  are written and cross-referenced.
- this workspace's `skills/autonomous-agent.md` — when to
  act vs ask; reports are how blocked decisions get
  surfaced.
- this workspace's `ESSENCE.md` §"Documentation layers" —
  where each layer lives in the doc hierarchy.
- `lore/AGENTS.md` — the workspace agent contract; points
  at this skill for the reporting discipline.
