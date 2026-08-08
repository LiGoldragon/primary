# Skill — intent manifestation

*Walk through the intent log, find recorded intent that hasn't yet
been expressed in the right guidance file, and manifest it there.
Intent records are raw psyche statements; guidance files are how
those statements actually shape agent behavior. Manifestation is
the bridge.*

## What this skill is for

The workspace records psyche intent in Spirit as typed intent
records (per `skills/intent-log.md` and `skills/spirit-cli.md`).
That is the sole capture surface: one entry per psyche statement;
the legacy file substrate is retired. Capture is necessary but not
sufficient. For intent to
actually shape what agents do, it has to land in a **guidance
file** — a file agents read to inform behavior.

Manifestation walks the gap: query Spirit, find entries whose
substance hasn't yet appeared in the right guidance file, edit the
guidance file to absorb the substance.

The forward target is automation. Once `persona-spirit` ships (see
`reports/designer/232-persona-spirit-new-component.md`), it queries
the intent layer for unmanifested entries and surfaces them as work
to do. Today, agents do this manually as a sweep skill.

## The destinations

Guidance files (per `INTENT.md` §"Guidance files"):

| Guidance file | What lands there |
|---|---|
| `ESSENCE.md` (workspace) | Highest-certainty universal psyche statements — the gold of the gold. Bar is high (per psyche intent). Statements that stand as founding rules. |
| `AGENTS.md` | Per-keystroke hard overrides. Short, every-session-read. The "buck the bad agent habits" stuff. |
| `INTENT.md` | Workspace intent in prose, synthesised from Spirit records and legacy history; verbatim psyche quotes in italics. Read once on starting; consult by topic. |
| `skills/<name>.md` | Topic-specific or workflow-specific discipline. Read when the topic comes up. |
| `<repo>/INTENT.md` | Per-repo prose synthesis of psyche intent for the project. Like ARCHITECTURE.md but for intent. |
| `<repo>/ESSENCE.md` (when exists) | Per-repo essential intent — the gold-of-the-gold for that project. |
| `<repo>/ARCHITECTURE.md` | The repo's structural shape. Some intent (architectural decisions) lands here. |
| `<repo>/skills.md` | Per-repo capabilities and invariants. |

## The decision tree

For each intent record, ask in order:

1. **Is this universal-and-maximum psyche intent?** A statement so
   foundational that it would stand as a rule of the whole way of
   working? → `ESSENCE.md`. Bar is high; few entries qualify.
2. **Is this a per-keystroke override?** A rule agents need every
   session to buck a bad habit? → `AGENTS.md` Hard Overrides.
3. **Is this onboarding-shaped — context-for-a-fresh-agent?** Not
   per-keystroke but read-once-on-start? → `INTENT.md`.
4. **Is this topic-specific discipline?** A rule that applies when
   working in a specific area (jj, NOTA, components, reports)? →
   the relevant `skills/<topic>.md`. If no skill exists yet, create
   one (per `skills/skill-editor.md`).
5. **Is this project-specific?** Intent specifically about one
   repo's direction? → that repo's `INTENT.md` (per
   `skills/repo-intent.md`).
6. **Is this an architectural decision for one repo?** → that
   repo's `ARCHITECTURE.md`.

One intent record can land in multiple destinations (e.g., a
psyche statement about NOTA grammar lands in both
`skills/nota-design.md` and the relevant nota repo's docs).

## How to walk through

For a topic:

1. **Query the topic's Spirit records.** Read every record in
   chronological order. The deployed Spirit store is the sweep
   substrate.
2. **For each record**, scan the guidance files you'd expect to
   carry its substance. Does the destination already say what the
   intent says? If yes, nothing to do — the intent is already
   manifested. If no, this record needs manifestation.
3. **Manifest by editing the destination.** Carry the substance
   into the destination's prose, applying the verbatim-quoting
   convention (next section). Keep the destination's voice
   (skills are imperative; ESSENCE is declarative; INTENT.md is
   project-specific synthesis).
4. **Cross-reference where useful.** A destination can name the
   intent record in passing ("recorded in Spirit topic `workspace`
   on 2026-05-19") but the substance lives in the destination, not
   the citation.
5. **Don't track 'manifested' explicitly.** No flag on the intent
   record; no sibling file. The sweep is idempotent — re-running
   it on already-manifested entries is a no-op. (If this becomes
   painful at scale, add a marker mechanism then.)

A sweep can be by-topic (process all Spirit records under `persona`
in one pass) or by-destination (sweep into `AGENTS.md` from every
topic). Both work; pick by what's in the current attention.

## The verbatim-quoting convention

In `INTENT.md` and ESSENCE files (workspace `ESSENCE.md` and per-
repo essence), the file body is **prose composed mostly of intent-
log summaries**, plus **verbatim psyche quotes** inline where the
exact wording is load-bearing. Mark verbatim quotes with
**markdown italics** — single asterisks:

```markdown
Persona-orchestrate is a real triad component, not a fold into
persona-mind. The state-vs-machinery split is the load-bearing
principle: *"the orchestration part where it allocates a certain,
where it, like, manages locks the way we manage locks now, really
belongs in orchestrate, so that doesn't need to go up to the mind.
But the memories actually do belong there."* Mind owns state;
orchestrate owns machinery.
```

The italicised span is the psyche's words (post speech-to-text
correction per `skills/stt-interpreter.md`). The surrounding prose
is agent-composed from the intent-log summaries.

For multi-paragraph verbatim, use a markdown blockquote with
italics:

```markdown
> *the multi-paragraph verbatim from the psyche, wrapped in
> italics inside a blockquote.*
>
> *the second paragraph stays italicised because the blockquote
> wraps both — plain `*…*` italics close at any blank line in
> CommonMark.*
```

The blockquote-with-italics is the only reliable way to carry
italics across paragraph breaks. For single-line or single-
paragraph verbatim, plain `*…*` is sufficient.

The italicised verbatim is *not* the same as the wholly-verbatim
`quote` field of an intent record — that lives in the NOTA log.
Here, the italics flag load-bearing pieces of original wording
that survive the prose synthesis.

## Voice of each destination

Each guidance file has a voice:

- **`ESSENCE.md`** — declarative. *"Intent is primordial."* *"Beauty
  is the criterion."* The reader feels the statement.
- **`AGENTS.md` Hard Overrides** — imperative, terse. *"Spell every
  identifier as a full English word."* *"Never quote a bare opaque
  identifier in chat output without an inline description."*
- **`INTENT.md`** — descriptive, contextual. *"Guidance files is
  the umbrella term for every file that shapes agent behavior."*
- **Skills** — imperative + discipline. *"When the psyche dictates
  a workspace term that the STT mangles, normalise to the canonical
  spelling before storing the verbatim."*
- **`<repo>/INTENT.md`** — descriptive synthesis. *"persona-spirit is
  the apex of the cognitive authority chain; it owns mind; it is
  spawned last."*

When manifesting, match the destination's voice. A statement that
reads as imperative in AGENTS.md will land as descriptive
synthesis in INTENT.md.

## When to skip manifestation

Some intent records don't manifest into a guidance file:

- **Brainstorm-in-flight** (Medium / Minimum certainty). Wait until
  the psyche settles before manifesting.
- **Acknowledgement / confirmation** records that re-state an
  existing intent without adding new substance.
- **Records about agent behavior during one conversation** that
  don't generalize past the session.

The bar: *does this record carry a rule, principle, decision, or
correction that future agents need to know about?* If yes,
manifest. If no, leave in the log as historical record.

## When the destination is missing

Sometimes the right destination doesn't exist yet:

- **New per-repo INTENT.md** — create per `skills/repo-intent.md`.
- **New skill** — create per `skills/skill-editor.md` if the
  intent is a new discipline area not yet covered.
- **New per-repo ESSENCE** — propose to the psyche before creating
  (per psyche intent "promotion path" — the psyche
  promotes to essence; the agent doesn't decide independently).

If the destination is unclear or the intent doesn't fit any
existing guidance-file shape, surface to the psyche per
`skills/intent-clarification.md`.

## Forward — automation by `persona-spirit`

Persona-spirit (per `reports/designer/232-persona-spirit-new-
component.md`) eventually queries the intent layer and surfaces
unmanifested intent as work. Until spirit ships, manifestation is
a periodic agent sweep. The discipline doesn't change once spirit
arrives — only the trigger does (from agent-initiated to
spirit-surfaced).

## See also

- `skills/intent-log.md` — capture discipline.
- `skills/intent-maintenance.md` — supersession + sweep cleanup.
- `skills/intent-clarification.md` — when to ask the psyche.
- `skills/repo-intent.md` — per-repo INTENT.md shape.
- `skills/skill-editor.md` — how to create or edit a skill.
- `skills/architecture-editor.md` — how to edit a repo's ARCH.
- `INTENT.md` §"Guidance files" — the umbrella naming.
