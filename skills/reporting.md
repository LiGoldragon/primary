# Skill — reporting

*How to write reports, when to write them vs answer in
chat, where they live, and how to reference them. Required
reading for autonomous agents.*

---

## What this skill is for

Whenever you produce output that explains, proposes,
analyses, or summarises — apply this skill before posting
to the chat. Reports go in files; chat carries pointers.
This skill names the boundary between the two and the
discipline that keeps both clean.

---

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

Two reasons reports exist at all:

1. **Chat UIs are poor reading interfaces.** Files are easier —
   scrollable, searchable, linkable, persistent.
2. **Agents reading later need the substance.** A future agent
   picking up the thread can't read your chat; they read the
   report. Chat is for the user's now-action; the report is for
   the agent's later-reference.

---

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

---

## Tone in chat replies

**State results. Don't narrate process; don't apologise;
don't pre-announce what you're about to do.** The chat
reply is for what changed and what's next. The *how* and
the *why* belong in the report, not in chat.

---

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

---

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

---

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

---

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

### Filename convention

**`<N>-<topic>.md`** where `N` is the next integer after the
**highest-numbered report in this role's subdirectory.** The
numbering is **per-role, not workspace-wide.** **No leading
zeros. No date prefix.**

Examples for `reports/designer/`:

- `4-persona-messaging-design.md`
- `12-no-polling-delivery-design.md`
- `13-niri-input-gate-audit.md`

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

**Why no leading zeros:** numeric-aware sort tools (`ls -v`,
`sort -n`, `sort -t- -k1,1n`) handle non-padded numbers
correctly. Padding adds noise at the cost of needing to
know the maximum digit count up front; the count grows
without warning.

---

## Kinds of reports — and where their substance ultimately lives

Reports are a working surface, not the substance's permanent
home. **For every report you write, name where its
substance is *destined* to live.** The typology below
catalogues the recurring shapes and their permanent homes
so future cleanups have a clear migration target.

| Report shape | Pattern | Permanent home for the substance |
|---|---|---|
| **Architecture decision** | A typed design decision (a record kind, a protocol shape, a boundary placement) that some other work depends on. | **`<repo>/ARCHITECTURE.md`**. The report is the staging-ground; the ARCH is the destination. Land the report; absorb the substance; retire the report. |
| **In-flight implementation roadmap** | A consolidated current-state report covering an active multi-track implementation push. Acceptance witnesses, bead trail, deferred-pieces inventory. | **Retires when the implementation acceptance fires green.** While in flight, the report is canonical state-of-art for the push. After acceptance, substance moves to ARCH (decisions) + git history (the path). |
| **Incident / postmortem** | A reconstruction of a past failure or surprise, with the lessons it teaches. | **Retires once the lessons land in a skill or rule.** The skill inlines the discipline (the "don't reintroduce this" rule, with the *why* stated as part of the rule); the postmortem itself doesn't outlive its migration. Skills do not cite reports — see `skill-editor.md` §"Skills never reference reports". |
| **Cross-role response** | A designer (or other role) reading another role's report and shaping the response: refinements, shape decisions, things missed. | **Retires when the recipient role absorbs the guidance** into their work — typically into a sibling repo's ARCH, a skill, or shipped code. While the back-and-forth is active, the response is load-bearing. |
| **Synthesis / state-of-art** | A wide pass across the workspace identifying gaps, dependencies, prioritised questions for the user. | **Retires when answered.** The substance flows into action: closed beads, new design reports, codified skills, ARCH edits. The synthesis itself is a working artefact; once the user has decided the questions, it stops being load-bearing. |
| **Cleanup ledger** | The record of a cleanup pass — what was deleted, what was absorbed, what was kept. | **Retires when the next cleanup ledger lands** (or sooner if its findings have all been acted on). Each cleanup ledger supersedes the previous one. |
| **Research / exploratory draft** | A first-sketch design exploring a problem before the answer is known. Marks itself as draft; leaves explicit open questions. | **Retires when a final design report lands** (or when the user closes the question without proceeding). The draft is intermediate; the decision record is permanent. |

The discipline that follows: when you write a report, ask
*what shape is this?* and *what's the destination home for
its substance?* If you can't name either, the report shouldn't
be written — the substance probably belongs in chat (too
small for a report), in a skill (a discipline statement
masquerading as a report), or in ARCH directly (a decision
clear enough to land permanently).

The pattern existed informally before; the explicit table makes
it teachable.

---

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

---

## The report's medium — prose + visuals

Reports explain shapes, not implementations. Their medium
is **prose plus visuals** — Mermaid diagrams, swimlanes,
flowcharts, tables, dependency graphs.

For Mermaid syntax workarounds (node labels, edge labels,
reserved-word IDs, Mermaid 8.8.0 safe forms for subgraphs,
edge labels, and sequence diagrams), see `skills/mermaid.md`.

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

---

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

---

## Tense and framing

**Present tense.** Reports describe what IS — the current
state, the proposed shape, the audit's findings as-of-now.
The path that led here lives in version-control history,
not in the report's prose.

When a direction turns out to be wrong, **rewrite the
report** to state the new direction. Don't accumulate
"v2" / "previously we thought" / strikethrough text — the
git log captures the lineage.

---

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

---

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
