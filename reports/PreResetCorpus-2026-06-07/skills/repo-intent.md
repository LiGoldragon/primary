# Skill — repository intent file

*Every repository carries an `INTENT.md` at its root capturing what
the psyche has explicitly intended for that project. Like
`ARCHITECTURE.md` but for intent: agent-written prose, 100% backed
by psyche statements, no embellishment, no inference.*

## What this skill is for

`ARCHITECTURE.md` says what the system IS. `INTENT.md` says what
the psyche wants this project to BE. The two complement: ARCH
carries shape and invariants; INTENT carries the psyche's stated
goals, constraints, and principles for THIS specific project.

The file exists because:

- Architecture docs say WHAT exists; they don't say WHY.
- Decisions made months apart need a common reference for "what
  was the psyche's vision."
- Future agents starting cold on a repo need to know the
  project-specific intent before reading the code.

## Where it lives

```
<repo>/INTENT.md
```

Repository root, alongside `ARCHITECTURE.md`, `AGENTS.md`,
`skills.md`. Uppercase to match `ARCHITECTURE.md` / `AGENTS.md` /
`CLAUDE.md`.

## What goes in

- **Project goals** the psyche has explicitly stated.
- **Project constraints** the psyche has explicitly stated.
- **Project principles** the psyche has explicitly stated as
  applying specifically to this project.
- **Things the psyche has explicitly said NOT to do** for this
  project.

Each item is a clear prose statement, **derived directly from
psyche statements**. The agent's role is synthesis without
embellishment — clear restatement of what was said, not
elaboration of what was implied.

**Verbatim psyche quotes go in markdown italics** (`*verbatim text*`)
inline within the prose. For multi-paragraph verbatim, use a
markdown blockquote wrapping italicised paragraphs (plain `*…*`
italics close at any blank line in CommonMark; the blockquote
carries the span). The italics flag "this is the psyche's own
words" — the surrounding prose is the agent's synthesis of intent-
log summaries. Full convention: `skills/intent-manifestation.md`
§"The verbatim-quoting convention".

## What does NOT go in

- Agent inference. If the psyche didn't say it, it doesn't go
  in `INTENT.md`.
- Architectural shape. That's `ARCHITECTURE.md`.
- Implementation discipline. That's skills.
- Reports / decisions / audits. Those live in `reports/`.
- Verbatim quotes. Those live in Spirit intent records.

The discipline: every statement in `INTENT.md` is a clear
restatement of a psyche-said thing. The agent's interpretation
is minimal — synthesis for clarity, not invention.

## Shape

Markdown prose, with sections grouping intent by theme. A
starter template:

```markdown
# INTENT — <project-name>

*What the psyche has explicitly intended for this project.
Synthesised from psyche statements; not embellished.*

---

## Goals

- <terse statement of a psyche-stated goal>
- <another>

## Constraints

- <terse statement of a psyche-stated constraint>

## Principles

- <terse statement of a psyche-stated principle for this project>

## Anti-patterns

- <terse statement of what the psyche has said NOT to do>

---

*Source statements live in Spirit intent records under the topics*
*that pertain to this project.*
```

The sections are illustrative; reshape per the psyche statements'
actual shape.

## How to derive from psyche statements

1. **Read Spirit intent records** for entries that mention this
   project.
2. **For each entry**, ask: is this a goal, constraint, principle,
   or anti-pattern? Place it in the appropriate section.
3. **Restate clearly.** The intent log carries verbatim + context;
   `INTENT.md` carries the agent's terse rephrasing for clarity.
   Stay tight to what was said.
4. **No conclusion-drawing.** If the psyche said "X is important"
   without saying why, `INTENT.md` records "X is important." Don't
   add "because Y" unless the psyche said Y.

## When to update

- New psyche statement specifically about this project lands in
  the intent log. Update `INTENT.md` accordingly.
- An existing `INTENT.md` statement is contradicted by new psyche
  intent (via `skills/intent-maintenance.md` supersession). Update
  after the supersession is confirmed.
- Periodic sweep (per `skills/intent-maintenance.md`) — check
  every statement still aligns with the recorded psyche
  statements.

**Only the psyche can override `INTENT.md`.** An agent
encountering `INTENT.md` content that seems wrong does NOT edit
based on inference; they consult the psyche
(`skills/intent-clarification.md`).

## Continuous manifestation discipline

Per spirit record 944 (Maximum, 2026-05-27) + record 943 (High,
operator-facing companion): **intent must be manifested into
per-repo files AT ALL TIME, not just at the workspace level**.
This is the load-bearing manifestation rule for repo-scope intent.

### The work-cycle obligation

When any agent starts working in a repo, the FIRST verification
step is whether recent psyche intent affecting that repo is
reflected in its `INTENT.md` (and, where architectural, its
`ARCHITECTURE.md`). If not, **manifest BEFORE proceeding** or
**manifest AS PART OF the work cycle**. Do not defer to a "later
pass" — that's the failure mode 944 corrects.

The discipline applies whenever **ANY new intent record affects
a specific repo's design, implementation, or test direction**,
not only intent statements explicitly scoped to that one repo. A
workspace-wide rule (e.g. *"every Rust function is a method on a
non-ZST"*, *"no \n escape inline NOTA"*) that changes how this
repo's code is authored MUST land in this repo's INTENT.md /
ARCHITECTURE.md as well, so an agent reading only the repo's
files knows the rule applies.

### Manifestation at psyche-prompt time

When a psyche prompt lands containing intent that affects
repo R:

1. Capture the intent through Spirit FIRST (per the hard
   override in `AGENTS.md`).
2. Identify whether the intent affects R's design /
   implementation / test direction.
3. If yes: edit R's `INTENT.md` (and `ARCHITECTURE.md` if the
   intent has architectural shape) on a designer feature branch
   in `~/wt/github.com/<owner>/R/<branch>/`, alongside or
   immediately after the Spirit capture.
4. Don't gate this on whether the prompt's primary subject was
   R — the manifestation discipline is about the repo's
   correctness as an agent-context surface, not the prompt's
   topic.

### Manifestation on entering a repo

When an agent enters a repo (worktree, edit, audit) for any
substantial work:

1. Read its current `INTENT.md` and `ARCHITECTURE.md`.
2. Query recent Spirit records (last session-or-two) for any
   that affect this repo.
3. Cross-check the records against the files. Any record whose
   substance is missing OR whose framing has drifted from the
   record's text is a manifestation gap.
4. Close the gap on the same feature branch as the work the
   agent is doing — manifestation is part of the work cycle,
   not a separate task.

### Failure mode this prevents

If intent only lives in Spirit + chat + reports, an agent
opening the repo sees stale framing in `INTENT.md` and codes
to the stale shape. The repo's INTENT.md / ARCHITECTURE.md are
the **canonical agent-context surface for that repo**; they
must reflect the current intent or they actively mislead.

### Cross-link

For the parallel ARCHITECTURE.md discipline (architectural
decisions captured in Spirit reflect into the repo's
`ARCHITECTURE.md` as part of the work cycle, not as a deferred
pass), see `skills/architecture-editor.md` §"Continuous
manifestation discipline".

## When to skip

A repo without psyche-stated intent doesn't need an `INTENT.md`.
The file appears when the first psyche intent specific to the
project lands; not before. A pure-skeleton repo or a repo whose
only purpose is mechanical (build artifact, codec, no psyche
input on direction) can stay without one.

## See also

- `skills/intent-log.md` — workspace-level recording discipline;
  Spirit is the source of new statements for `INTENT.md`.
- `skills/intent-clarification.md` — when to ask the psyche.
- `skills/intent-maintenance.md` — supersession protocol.
- `skills/architecture-editor.md` — the analogy this file
  follows; ARCH for shape, INTENT for psyche's stated direction.
- `ESSENCE.md` §"Intent is primordial; psyche is the source" —
  the apex this skill serves.
