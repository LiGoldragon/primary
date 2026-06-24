# Skill — reporting

## Reports vs chat

The two media have different audiences:

- **Reports are for agents** — peer roles, future readers, and your
  own future self after context compaction. Durable, scrollable,
  filename-indexed, citeable. Your current context is ephemeral; the
  report on disk survives.
- **Chat is for the user** — read now, acted on now. The user is the
  bottleneck on decisions, so chat is optimised for their attention.

If output explains, proposes, analyses, or summarises, write a
report in your lane's `reports/<role>/` subdirectory. Small things —
acknowledgements, tool-result summaries, "done; pushed" — don't need
reports.

Reports are role-owned and **exempt from the orchestration claim
flow**: the lane's report subdirectory is its implied write lock.
Creating, editing, correcting, superseding, or deleting a report in
your own lane needs no claim. If the same work also changes shared
files (skills, `AGENTS.md`, repo `INTENT.md`, schemas, code), claim
those non-report paths.

Private personal-affairs substance is the exception: assistant /
counselor private reports go in `private-repos/<role>-reports/`;
public reports carry only privacy-safe mechanism or status.

**Routine code landings: the commit description IS the report.** Do
not write a report whose only purpose is to repeat a `jj` commit
message, changed-file list, and test list — put that in the commit
description, bound to the changes. Write a report only when there is
analysis, design consequence, audit substance, user-facing decision
context, or cross-repo synthesis that doesn't fit the commit object.

## What chat carries when a report exists

A report does not relieve chat of being the user's working surface.
When a report lands, chat carries:

1. **The report's path, explicitly named** as the full relative
   workspace path (`reports/<role>/<filename>.md`).
2. **A 1–3 sentence headline** — what was found, decided, changed.
3. **Anything the user must read, decide, or act on, restated with
   full inline context** — open questions, blockers, surprising
   findings, recommendations awaiting approval — each stated so the
   user can engage *without opening the report*.

The user is the bottleneck: a question that needs the user's
attention but sits unread inside a report is a question answered
late. Chat eliminates that latency.

Chat does NOT carry: the full report content, implementation
narration ("first I did X then Y"), or tool-call diagnostics. Chat is
short — usually under one screen — but every sentence carries
substance the user needs to act on.

### Every substantive response paraphrases a report

The default pattern: **every chat response is the paraphrase of an
accompanying per-response report**. The report is the session log;
chat is the paraphrase — not a teaser pointing at it. (When no
per-response report exists — the small-report exceptions above — the
pattern doesn't apply.)

The chat reply carries **3-7 most important items**, spread
**more-evenly-than-not** across three categories:

- **(a) Questions / clarifications of intent** — open questions,
  ambiguous intent, decisions awaiting approval.
- **(b) Observations / suggestions / explanations of how new
  mechanisms work** — findings, design proposals, what changed in
  the architecture or contracts.
- **(c) Examples of recent work or evolving ideas** — concrete
  artefacts (paths, beads, commits) and what's evolving in the
  current line of work.

The even-ish balance is load-bearing: pure questions miss the
substance the agent owes; pure explanations drift toward
report-shape; pure artefact-listing is a status dump. Below 3 items
the response is under-substantive (the user could have read the bead
title); above 7 the user can't hold it in working memory while
running parallel agents.

This extends the shape-trigger rules in `AGENTS.md` §"Reports go in
files" (mermaid / table / `##`/`###` headings / multi-paragraph
explanation / list of >5 substantive items / code block >10 lines
that illustrates a design — these say *when* chat content must move
to a report). The paraphrase rule says *what* chat carries when the
report is the substance home.

## Tone in chat

**State results. Don't narrate process, apologise, or pre-announce
what you're about to do.** The chat reply is for what changed and
what's next; the *how* and *why* belong in the report.

## Always name paths

When chat references a report or any file the user might navigate to,
**name its full relative path** (`reports/<role>/<filename>.md`) for
every report produced in the session.

> "Two reports landed: `reports/designer/11-persona-audit.md` and
> `reports/designer/12-no-polling-delivery-design.md`."

…not "two reports landed". Chat is a **navigation surface, not a
teaser**.

**Commit hashes and report numbers are NOT paths.** "Report 433
landed as `33c84b46`" gives the user a number and a hash and zero
paths. The path is the substantive locator; hashes and numbers are
supplementary:

> "Report
> `reports/designer/433-whole-stack-comprehensive-every-part-with-code.md`
> (commit `33c84b46`) — …"

The same applies to any file chat references: if chat says "I edited
the schema," the schema's path goes in the next clause.

## Human-facing references are self-contained

Treat the current response as the user's whole world. The user should
not need to scroll back, query a store, open a report, or decode an
internal label before they can answer.

Whenever a reply mentions a shorthand, identifier, numbered point,
report, bead item, actor name, protocol term, or prior
recommendation, **restate the substance inline**. The description
leads; the reference is secondary and exists for verification.

- Asking about `primary-ar7`? Name the task title and why it matters.
- Discussing "point 6"? Restate point 6 as a sentence first.
- Using a term like `PTY fanout`? Define it against the concrete
  recommendation being made.
- Citing a report path? Include a one-line summary of the relevant
  claim.

**Opaque identifiers especially, and ESPECIALLY in chat.** A bead id,
record number, content hash, or jj change id cannot be decoded in a
human's head, and they have no store to query. In **chat**, lead with
what the thing IS or DECIDED and keep the bare identifier to a quiet
trailing reference, or omit it: say "the runner-extraction work," not
"`primary-l89s`" as the subject. In **reports** the identifier stays
(agents need it to find the thing) but is always paired with its
description. Every mention, every time. Never address the human as a
peer machine with query access.

## Questions to the user — paste the evidence, not a pointer

When you surface a question — a decision, an ambiguity, a choice —
**the question must carry the substance that lets the user answer
without opening files.**

The form: **question + concrete evidence (code, text, or symptom) +
why it matters + concrete options with tradeoffs.** A source report
may be cited as a "for longer context" footer, but the link is a
back-reference for verification, not the substance. If the user has
to follow the link to answer, the question is not yet asked.

Wrong:

> *"Should I collapse the four forwarding-trampoline actors? See
> `reports/designer/<N>-actor-discipline-sweep.md` §5.2 for context."*

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
> *The struct holds only `ActorRef` fields — no domain state. The
> handler routes messages and records trace events. If the trace IS
> the domain (witnessing the pipeline ran), keep them. If it's
> observability noise, collapse and route request → memory dispatch.*
>
> *Options: (a) collapse, lose per-stage witness; (b) keep, document
> the trace-as-domain carve-out; (c) keep but rename from
> `*Supervisor`."*

**Why:** the user is the bottleneck. A question that takes 2 minutes
to understand gets answered late or skipped; one that fits on a screen
with evidence inline gets answered immediately. The rule follows the
question, not the medium — it applies in chat, a report's "open
questions" section, `AskUserQuestion` prompts, or a hand-off.

## Where reports live

Each lane owns a subdirectory under `~/primary/reports/` named for
its exact lane (`reports/operator/`, `reports/designer/`,
`reports/system-operator/`, etc. — see `orchestrate/AGENTS.md`). Each
lane writes only into its own subdirectory; reading any public role
report is free.

To **build on** another role's report, rewrite the relevant content
into a new report in your own subdirectory — don't edit another role's
reports.

Per-repo reports follow the same `<N>-<topic>.md` shape under
`<repo-root>/reports/`.

### Meta-report directories — sub-agent sessions

When an agent dispatches sub-agents for a coordinated multi-slice
piece of work, the whole session lands as **one meta-report
directory** instead of flat sibling reports:

```
reports/<role>/<N>-<session-name>/
  0-frame-and-method.md       (orchestrator: session frame)
  1-<slice-name>.md           (sub-agent 1)
  2-<slice-name>.md           (sub-agent 2)
  ...
  N-overview.md               (orchestrator: synthesis)
```

The orchestrator takes the next number `N` in its subdir's sequence,
creates the directory with a kebab-case session-name slug, and each
sub-agent writes a numbered sub-report inside. The directory **IS**
the meta-report — no `meta-` prefix, because being a directory is the
signal. The orchestrator's frame goes in `0-frame-and-method.md`; the
synthesis in the highest-numbered file (`N-overview.md`). Sub-agents
own their numbered slices; the orchestrator owns the frame and
overview plus optionally a slice or two.

**Pre-launch lane allocation.** Parallel sub-agents receive their
report lanes — directory path and sub-report number — **before**
launch, stated in the dispatch prompt and recorded in
`0-frame-and-method.md`. Sub-agents do not pick their own number; if
they did, two parallel slices could collide on the same filename.

**Garbage collection.** The directory is collectable as **one session
unit**: when its substance migrates to permanent homes (ARCHITECTURE,
skills, ESSENCE, per-repo INTENT), the whole directory retires
together via a context-maintenance sweep, not piece by piece.

### Filename convention

`<N>-<primary-topic>[-<secondary-topic>]…-<title-slug>.md` where:

- `N` is one above the **highest-numbered report in this role's
  subdirectory** — per-role, not workspace-wide. No leading zeros, no
  date prefix.
- `<primary-topic>` is a durable topic word from the workspace
  vocabulary (`nota`, `schema`, `macros`, `runtime`, `wire`,
  `emission`, `discipline`, `workspace`, `intent`, …). Put it first so
  filename grep finds the topic cluster:
  `ls reports/designer/ | grep -E "^[0-9]+-schema-"`. A report may
  carry one or more topics; secondary facets follow the primary.
- `<title-slug>` is the specific subject in kebab-case. A `-YYYY-MM-DD`
  suffix is permitted only when same-day collision on one topic is
  likely; otherwise omit (git captures the date).

Examples: `390-nota-canonical-design.md`,
`391-schema-macros-canonical-design.md`,
`393-schema-emission-src-target-decision-2026-05-27.md`.

The filename answers two questions at a glance: what subject domain
(topic) and what specifically (title). The topic maps to
persona-spirit's intent-record `Topic` vocabulary, which grows with
use — let topic words emerge from the work rather than pre-declaring
them. Name the subject, not the conversational ancestry: avoid
`response-to-…`, `review-of-…`, `audit-of-…` that hide the subject
behind another report number.

**Forward-only.** Existing reports without topics in the filename
aren't renamed in bulk; renaming happens when a report is touched or
during a deliberate agglomeration pass.

### Numbering

Numbering is **per-role** — each role manages its own sequence.
`reports/operator/97-…md` and `reports/designer/97-…md` coexist; the
role subdir disambiguates. Roles work in parallel on independent
cadences, so a workspace-wide sequence would force every agent to scan
every other subdir and would collide on parallel landings.

To find the next number, scan only the current role's subdir:

```sh
ls ~/primary/reports/<role>/ | grep -E '^[0-9]+-' \
  | sort -t- -k1,1n | tail -1
```

Then `N = that + 1`. The number is a stable identifier within the
role — once assigned, it doesn't change. **Numbers are not reused
after deletion:** a removed report's number stays retired; the next
report takes next-highest-plus-one. Gaps are a visible signal that
something retired; the commit history holds the deleted content.
Cross-references between roles always include the subdir.

No dates in the filename: they collide on multi-report days and are
noise once a unique number exists. No leading zeros: numeric-aware
sort tools (`ls -v`, `sort -n`) handle non-padded numbers, and padding
needs the max digit count known up front.

### Topic agglomeration

When a topic accumulates many reports, produce **one primary report**
per topic carrying the load-bearing substance from the older ones.
Older reports retire when their substance fully migrates; they stay
only if they hold unique load-bearing detail not in the primary (e.g.
design-rationale enumerating competing alternatives). The primary
becomes the canonical reference; future reports on the topic either
append to it or land as new same-topic reports with the primary
updated to reference them if they become load-bearing.

### Iterating on a report — v2 / v3 suffix

When a topic is in active back-and-forth and the next version is
*substantially the same report with absorbed feedback*, rename with a
`-v2` (then `-v3`, …) suffix between the number and the topic:

- v1 (implicit): `225-workspace-redesign-direction.md`
- v2: `225-v2-workspace-redesign-direction.md`

**If the path has already been shared with the user or another agent,
the v-rename is mandatory** — do not silently edit a shared path for
substantive absorbed feedback. Publish the successor under the same
number with the next `-vN` suffix, **delete the predecessor in the
same commit**, and name the new path in chat. The file under a given
number is the canonical current version; don't accumulate
`v1`/`v2`/`v3` side by side — git history holds the lineage.

When the topic shifts enough that the name *after the number* should
change, it becomes a new report: take the next number, absorb what's
relevant, delete the predecessor in the same commit.

Stacking obsolete reports that recursively partial-supersede each
other is harder to reason about than a single current report with git
as the lineage record. Editing in place is fine for light fixes;
renames + deletions are the discipline for real iteration.

## Kinds of reports — closed set, with destination

Reports are a working surface, not the substance's permanent home.
Every report carries a **kind** (closed set, names what it IS
structurally) and **topics** (open string, names what it's ABOUT).
Both sit in the filename and the front matter. Each kind has a
destination home for its substance — name the kind, the topics, and
the destination *before* writing; if you can't name all three, the
report shouldn't be written (the substance is too small for a report,
is a discipline statement that belongs in a skill, or is a decision
clear enough to land directly in ARCHITECTURE).

| Kind | What it is | Destination / retirement |
|---|---|---|
| `design` | Propositional architecture — a typed contract, protocol, boundary placement, triad. Falsifiable examples; lets operator implement. | `<repo>/ARCHITECTURE.md` when settled. Report is staging; absorb the substance and retire. |
| `audit` | Verification of existing work against current intent/spec; names what landed, drifted, or gaps. | Retires when the named gaps land. Audit substance is tied to a moment. |
| `research` | Investigation of options (protocols, libraries, models, prior art); trade-offs without picking. | Retires when a `design`/`proposal` report picks and justifies. |
| `proposal` | Test-ready specification for operator: typed records, falsifiable test list, scope. | Retires when implementation acceptance fires green. |
| `review` | Output of context maintenance — refreshes older substance against current intent + new research. | Supersedes the report it refreshed (delete predecessor same commit); itself retires when absorbed or superseded. |
| `synthesis` | Wide workspace pass — digest across reports, state-of-art, prioritised psyche questions. | Retires when its questions are answered; substance flows into beads, design reports, skills, ARCH. |
| `handover` | Session/lane transition: what's done, open, load-bearing. | Retires when the next handover supersedes or its open items land. |
| `postmortem` | Reconstruction of a past failure with its lessons. | Retires once the lessons land in a skill (the "don't reintroduce this" rule, with the why). Skills never cite reports. |
| `psyche` | Deep self-contained context for the psyche to read directly — verbatim quotes, real code, decisions laid out for in-place ratification. | Retires when its open decisions are answered; substance flows into Spirit captures and permanent docs. |
| `update` | Recurring workspace-update report surveying changes since the last update report. See `skills/workspace-update-report.md`. | Retires when the next update report supersedes (named in its baseline). |

The closed kind set matches persona-spirit's intent-record structure
(kind + topic + summary) and prepares reports for eventual move into
persona-mind-managed storage. The kind set is closed; the topic
vocabulary is open.

### Psyche reports — show the code, not the summary

A psyche report MUST show **actual code with surrounding context**,
not line-count summaries or vague references. The psyche's reading of
a psyche report is their chance to see the most important code and
understand the project; "the five lines of CLI wiring" defeats that.

- **Cite file paths with line ranges, then include the code block
  itself** — verbatim lines from `spirit/src/bin/spirit.rs:34-40`,
  not "~5 lines of trace wiring."
- **Name the objects the code uses.** If it calls
  `TraceClient::from_environment(...)`, show the declaration of
  `TraceClient<Event>` or its method signatures alongside.
- **Show proposed change beside current code** — "this should become
  two lines instead of five" gets both as adjacent blocks.
- **Walk concrete examples through** — a `(Help (Verb Put))` round
  trip in actual Rust + NOTA, not described.

A psyche report stays self-contained: one citing sub-agent reports
inlines the load-bearing code excerpts from those sub-reports so the
psyche can read it alone. The mermaid 5-node cap (per §"Graphs are
short and focused") still applies; code blocks count toward report
length but not toward visual node count.

### Psyche reports — narrative voice, sparing citations

A psyche report is a HUMAN-FACING document that TELLS the psyche
what's going on. Numeric record IDs sprinkled on every claim interrupt
reading flow.

- **Default to narrative phrasing** — "fresh intent shows…", "today's
  decisions surface…", "recent capture leans toward…" carry the
  substance with less load than per-sentence citations.
- **Use record-number ranges to highlight regions**, not as
  per-sentence citations — "records `N–M` trace the privacy thread"
  marks a span worth looking up; a citation on every claim does not.
- **A single record number is fine when load-bearing** — if the
  report rests on one specific Decision it asks the psyche to ratify,
  name it. Sparingly, deliberately.
- **Restate substance, not the locator** — "the decision to reuse
  Magnitude on a privacy axis (Decision Maximum, today)" reads as a
  sentence; "per Spirit `<id>`" reads as a footnote.
- **Code and visuals stay rich.** Narrative discipline tightens the
  PROSE, not the code blocks or diagrams.

A psyche report is what the psyche reads when they want to ENGAGE — to
ratify, alter, or suggest. The reading experience should support
engagement, not impose decoding.

### Psyche reports — distinguish lean from ratification

A psyche statement that leans toward a choice *while explicitly asking
for more information* is **NOT a ratification**. "I'd go with X but is
there more context?" is a lean-pending-information. Mark psyche
statements correctly:

- **Ratified** — firm yes/no/choose-X without flagging an info-need.
  Captured as a Decision with appropriate magnitude.
- **Leaning, pending context** — a tentative direction AND an explicit
  ask for more. NOT captured as a Decision; surfaced as an open item
  the next round of context addresses.
- **Open** — psyche hasn't engaged with the choice yet.

Mis-labeling a lean as a ratification corrupts the intent layer. Show
the lean honestly and supply the missing context (via the report's
code-shown demos) so the next round can ratify or redirect with full
information.

### Intent Anchors — first body section

A report that rests on explicit intent begins its body with an
`## Intent Anchors` section, in this order:

1. YAML front matter.
2. Title heading.
3. `## Intent Anchors`.
4. The central bracket-quoted intent summaries, each its own paragraph
   with a blank line between anchors (citation discipline per
   `skills/intent-log.md` §"Citing intent in prose" — quote the
   summary in square brackets; not bullets, tables, or record numbers).
5. The report's analysis.

Required for psyche reports; for other kinds, include it when the
argument depends on explicit psyche intent; omit it for purely
mechanical reports. The point: the reader sees the load-bearing intent
before the agent's analysis starts.

## Report header — YAML front matter

Every report carries a YAML front matter block at the **top of the
file**, before the title heading. YAML is valid markdown and renders
cleanly in GitHub, VS Code preview, Obsidian, and static-site
generators; it is also the report's primary self-describing surface,
parseable by an agent walking the report tree without opening files.

```markdown
---
title: 17 — Real-time intent recording system
role: designer
variant: Design
date: 2026-05-22
topics: [intent, recording-system]
description: |
  Proposal for a typed real-time intent recording system that
  captures author Decisions / Principles / Corrections /
  Clarifications / Constraints as they happen.
---

# 17 — Real-time intent recording system

(report body...)
```

Fields, in canonical order:

- **`title`** — matches the `# <N> — …` heading on the next line.
- **`role`** — the writing lane's exact subdirectory name.
- **`variant`** — the report kind, capitalised (`Psyche`, `Design`,
  `Audit`, `Research`, `Synthesis`, `Closeout`, `Handover`).
- **`date`** — first-written date `YYYY-MM-DD`; reaffirmed on
  substantive rewrites, unchanged on small fixes.
- **`topics`** — YAML list of broad atomic topic words (kebab-case),
  mirroring the filename topic prefixes; first is primary.
- **`description`** — multi-line block scalar (`|`); self-contained, so
  a future agent reading just the front matter knows the subject.

Optional, for reports inside a meta-report directory:
**`parent_meta_report`** (path to the directory) and **`slot`**
(numeric position; 0 for frame, highest for overview).

**Forbidden: the semicolon-bracket pseudo-NOTA header.** A shape like

```text
; designer
[topic-1 topic-2 …]
[description text]
2026-06-03
designer
```

is not valid markdown, not valid NOTA (`;` alone is invalid; NOTA's
comment sigil is `;;`), and rendered by no markdown UI. The
italicised one-liner `*Kind: Design · Topics: …*` is also not used.
Use YAML front matter.

## Editing reports — act, don't narrate

When the conversation reveals a correction bearing on a report you
just wrote or are actively engaged with, **edit the report in the same
turn** — not later, not in a follow-up commit, not as a queued task.
Saying "I should edit X to reflect Y" is the failure mode this
eliminates: you have the context, the file, and the correction in
working memory; the edit is the action.

This applies when all three hold:

- **Fresh in context** — you wrote it this session or are reading it,
  so you still hold its reasoning.
- **Clearly indicated** — something specific (psyche statement,
  operator finding, code observation) names what's wrong.
- **Scoped** — the change is local to a paragraph or section, not a
  rewrite that means redoing the whole report.

When any fails (the report is old and out of context, the correction
is speculative, or the change means a full rewrite), flag it for
follow-up rather than edit blind. Fresh-in-context edits stay inside
the role-owned report lane — claim only if the correction also changes
shared non-report files.

### Versioning committed reports

| Report state | Edit size | Action |
|---|---|---|
| Uncommitted | any | Edit in place. No rename. |
| Committed | minor (typo, citation fix, paragraph refinement) | Edit in place; commit the refinement. |
| Committed | major (substantive reframing, recommendation reversal, large rewrite) | Rename to `<N>-v2-<rest>.md`, edit the renamed file; the prior `<N>-<rest>.md` retires. |
| Committed | uncertain whether major | Default in-place + flag in commit message; promote to v-rename if the edit grows. |

The `-v2-` segment goes immediately after the report number, before
the variant or topic:
`493-Design-schema-...-2026-06-03.md` →
`493-v2-Design-schema-...-2026-06-04.md`. For meta-report sub-files it
goes after the slot number: `2-help-namespace-design.md` →
`2-v2-help-namespace-design.md`. The commit message names the
supersession (`designer 493 → 493-v2: <reason>`); readers grepping
`493-` find both. Git history preserves the prior version intact.

**Major signals:** the recommendation changes direction; a section is
removed wholesale or added at the structural level; the headline
finding is reframed; more than ~30% of the body changes. **Minor
signals:** a code excerpt corrected, a citation refined, a paragraph
tightened, a typo fixed. When uncertain, in-place edit with a clear
commit message; the v-rename is for edits substantial enough that a
reader of the prior version benefits from seeing both.

## Hygiene — soft cap, supersession, periodic review

A role's `reports/` subdirectory is a working surface, not an archive.
The git log preserves everything; the filesystem holds only what's
currently load-bearing.

**Soft cap: 12 reports per role subdirectory.** When a subdir reaches
12, the next agent working there reviews the older reports before
adding a 13th. The cap is a review trigger, not a hard block — the aim
is a surface small enough that a fresh reader can scan the listing and
see what's active.

**Supersession deletes the older report.** When a new report
*replaces* an older one (a fresh audit of the same target, a redesign,
a pass that supersedes a transitional sketch), **delete the older one
in the same commit that lands the new one** — substance in the new
report, lineage in git history. First update cross-references in
surviving reports to point at the new one (or remove the citation);
dead pointers are a smell, and the cleanup is part of the supersession.

**Deleted reports live in the commit tree.** The working tree carries
only current-state reports; a deleted report is one `jj show` away, so
delete-in-the-same-commit is safe:

```sh
# Find the change that last touched the report, then read it:
jj log -p reports/designer/<N>-<topic>.md
jj show <change-id>:reports/designer/<N>-<topic>.md

# Find a deleting commit by what it replaced:
jj log -r 'description(glob:"*<keyword>*")'
```

Reach for `jj show` before assuming substance is lost. The report
tree's small size is a feature, not a forgetting mechanism.

**Periodic review when the subdir gets full.** When the count crosses
12, work through the older reports; for each, decide one:

| Action | When |
|---|---|
| **Keep** | Still load-bearing — current state, active design, a decision someone is still acting on. |
| **Forward** | Partially relevant — absorb the live parts into a current report, delete the old one. |
| **Migrate upstream** | Durable substance belongs in `skills/<name>.md`, `<repo>/skills.md`, `<repo>/ARCHITECTURE.md`, `ESSENCE.md`, code, or a tracked item. Move it, delete the report. |
| **Remove** | Stale, work done, design shipped, decision reversed — nothing load-bearing remains. Delete. |

The reviewing agent's question is always: *what does this report still
teach a future reader that they can't get from current code, skills,
architecture, or fresher reports?* If nothing — delete. The agent
decides from its own context; if the work doesn't touch the report's
topic, do a brief read of the relevant code/skills/recent reports to
find where the substance lives now, then decide.

**What gets absorbed, not kept indefinitely.** Permanent docs (skills,
architecture, ESSENCE) never cite reports, so a "kept-indefinitely"
report is structurally unreachable from the permanent surface. The
moment a rule is settled, inline it and retire the report:

- **Foundational decision records** (the *why* of a direction) →
  inline into the relevant `ARCHITECTURE.md` as a constraint,
  invariant, or short rationale (per `architecture-editor.md`); the
  report retires.
- **Postmortems** (the "don't reintroduce this" lesson) → inline the
  discipline into the relevant skill with the why stated as part of
  the rule (per `skill-editor.md`); the postmortem retires.

If the substance genuinely can't be expressed as a permanent
skill/architecture rule, it's not ready to be one — the report stays.
But the moment the rule is settled, inlining is the move.

## Context maintenance — research-driven refresh

Hygiene above is the *simple* maintenance: stale reports go,
load-bearing ones stay. Context maintenance is the *deeper*
discipline, triggered when the psyche names it ("do a context
maintenance pass," "refresh," "review the older reports") OR when a
report is still semantically relevant but has drifted against current
intent. The output is a **`review`-kind report** that brings older
substance into current state and supersedes the predecessor (deletes
it in the same commit). It is designer-authority work — assistant
lanes can identify candidates, but the refresh is designer-level.

### The four steps

1. **Read intent first; weight recent over old.** Query the deployed
   Spirit store before reading the older report. Recent intent
   outweighs old — a Maximum-certainty record from this week overrides
   a Medium one from last month on the same topic. This is the test
   for whether the older framing still holds.
2. **Ask how the older report relates to the engine, architecture, and
   intent now.** Three answers: **fully aligned** (substance holds, no
   refresh — mark kept), **drifted but recoverable** (some sections
   superseded, some hold, some need new research → step 3), or
   **superseded** (no longer load-bearing → delete per Hygiene, no
   review).
3. **Do new research where the older form drifted.** Re-research the
   gaps. The review isn't a re-edit of the older text — it's a fresh
   pass against current state, carrying older substance forward where
   it holds and filling gaps with new findings.
4. **Write the review report.** A `review`-kind report under the lane's
   subdir; names what it supersedes, states current-state findings,
   and ends with what carries forward / what changed. **Delete the
   predecessor in the same commit.**

The output READS AS CURRENT — not as a refresh of an older report.
The lineage lives in the supersession note and git log; the prose
describes current state directly (matching the present-tense rule).

**Context maintenance is NOT** a deletion ledger (the output is a
`review` report, not a list of removals), a digest of unchanged
reports (unchanged reports just stay), or a place to accumulate
(reviews can themselves be reviewed later; value comes from the tree
being small enough to read).

Eventually reports move into persona-mind; context maintenance then
becomes a query — find reports whose intent dependencies changed,
surface candidates, write review records directly. The filesystem path
is transitional; the discipline is durable.

## The report's medium — prose + visuals

Reports explain shapes, not implementations. Their medium is **prose
plus visuals** — Mermaid diagrams, swimlanes, flowcharts, tables,
dependency graphs. For Mermaid syntax workarounds see `skills/mermaid.md`.

**Visuals are Mermaid only.** Every diagram goes in a Mermaid code
block. ASCII text-block "diagrams" using box-drawing characters are
FORBIDDEN — they misalign, break across Unicode versions, don't
render, accumulate drift, and read worse than the Mermaid they could
have been. If you reach for box-drawing to convey structure, pick the
right Mermaid shape (`flowchart`, `sequenceDiagram`, `stateDiagram-v2`)
and let the renderer work. Pre-formatted text blocks stay allowed only
where they aren't pretending to be visuals: file-tree listings, shell
transcripts, NOTA samples, short code snippets.

**Graphs are short and focused.** A report graph explains *one*
relationship or scenario. Default budget: 3–6 nodes, 2–7 edges, one
direction of flow, no nested subgraphs unless the graph is about that
nesting, and one caption sentence naming what it proves. For a broad
system, use a sequence of small graphs ordered bottom-up or
scenario-by-scenario, each with the nearby Nix check, file path, CLI
call, schema snippet, or short code anchor that makes it testable. A
graph needing more than one screen of Mermaid source is several graphs.
An unreadable graph (clipped labels, paragraph-sized boxes, sideways
scrolling, too many nodes) is a report failure — fix it before landing
with `skills/mermaid.md` §"Total graph size" + §"Label sizing": split,
use short noun labels, wrap with `<br/>`, keep one-line labels within
~24-28 characters.

**Implementation code does not belong in reports.** Rust `impl`
blocks, function bodies, struct-with-methods definitions, full Nix
derivations — these go stale the moment they land and the real type
drifts, and readers can't tell whether the snippet or the repo is
authoritative. Visuals carry the same information without the freshness
trap. *Test:* more than a couple of lines that look like
implementation → refactor into a visual. (Psyche reports are the
exception — there, showing real code IS the point, per §"Psyche
reports — show the code".) The narrow allowance: a few-line *sample*
of the surface the design talks about — a config snippet showing its
shape, a one-line CLI invocation, a single field declaration to anchor
a name.

## Cross-references — relative paths, with inline summaries

When a report references files in sibling repos, link via
`../<repo>/...` (workspace symlinks) — the relative path resolves in
editors and survives repo renames. Report-to-report references use the
same shape (`reports/designer/<filename>.md` from within `reports/`;
`~/primary/reports/designer/<filename>.md` from outside). Avoid full
HTTPS URLs — deep file URLs rot when files move.

**Every external reference carries a short inline summary of the cited
substance.** A path plus a one-line summary of what's there is what
makes the reference useful; a bare path forces a lookup and turns the
report into a navigation puzzle.

Wrong:

> *"Operator/33 §4 and operator/34 §7 both keep 'explicit approval for
> every proposal' as the default."*

Right (path verifies; prose carries the substance):

> *"The default — explicit approval for every proposal — is kept in
> operator/33 §4 (open user-level decisions) and operator/34 §7 (rules
> to enforce while refactoring)."*

The reader follows the point from the sentence; the path is for
verification. This applies to all external references, not just
report-to-report — citing a skill or ARCHITECTURE section gets the
same treatment:

> *"`skills/contract-repo.md` §'Kernel extraction trigger' (extract
> when 2+ domain consumers exist) supports this."*

not just *"See `skills/contract-repo.md` §'Kernel extraction trigger'."*

## Dependency context — surface it by default

Thorough reports surface dependency relationships by default: with
many repositories, the psyche needs a running sense of what is used by
what. When a report touches a crate or component, cite its key forward
deps (which core crates it sits on — new-spine vs legacy), its
reverse-dep count (who consumes it), and its last-commit date inline,
using the `← N consumers, last commit MM-DD` shorthand. Reverse-dep
count is the cheapest live-vs-dead signal; last-commit disambiguates
*stale* from *legacy-but-shipping*. Mechanism + measurement
definitions: `skills/engine-report.md`.

## Tense and framing

**Present tense.** Reports describe what IS — the current state, the
proposed shape, the audit's findings as-of-now. The path that led here
lives in version-control history, not in the prose. When a direction
turns out wrong, **rewrite the report** to state the new direction;
don't accumulate "v2" / "previously we thought" / strikethrough — git
captures the lineage.

## When report substance becomes durable

When a report holds durable substance future agents will need, **move
it to the right home** rather than leaving it in `reports/`:

- Rules for how to act → `skills/<name>.md`
- Repo intent / invariants → `<repo>/skills.md`
- Architecture commitments → `<repo>/ARCHITECTURE.md`
- Workspace intent → `ESSENCE.md`

The report's body then becomes a thin pointer or is deleted, depending
on whether it still serves a narrative purpose (audit findings,
decision record).

## See also

- `skills/skill-editor.md` — how skills are written and
  cross-referenced (and why skills never reference reports).
- `skills/context-maintenance.md` — the deeper sweep discipline.
- `orchestrate/AGENTS.md` §"Reports" — subdir ownership and
  claim-flow exemption.
