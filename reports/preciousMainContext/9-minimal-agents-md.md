# 9 — Minimal AGENTS.md + the captures behind it

Lane: preciousMainContext · Designer · 2026-06-25. Does not supersede 4/6/7/8.

## The directive

Psyche, verbatim: "I want agents to always either use a subagent (any meaningful
read, including the startup read which means very minimal agents.md) or interact
with me with questions/suggestions/clarifications." Plus, to the operator lane:
"I think the only thing they should read is the skill index."

The lead agent has exactly two modes: **dispatch a helper for any meaningful
read** (including the startup read) or **interact with the psyche**. It does no
meaningful reading itself. The startup read is therefore minimal — querying the
skill index is the only default read.

## Gap-check against the operator's `3ey7`

`3ey7` (Correction, Medium): "When a lead dispatches a context-preserving
helper, the helper receives and reads the full required-reading envelope... the
lead keeps only the Spirit gate and dispatch mechanics." That covers the
*mechanics once you dispatch*. It does NOT state the universal rule (lead never
reads meaningfully itself) nor the structural consequence (AGENTS.md minimal,
skill index the only startup read). Those are the gap-fills below — and firmer
(High) than `3ey7`'s Medium.

## Proposed safety floor — what stays resident in a minimal AGENTS.md

The fork that needs your confirmation: a minimal AGENTS.md must still hold the
rules that bind *before* an agent has queried the index. Proposed resident core:

1. **The two-mode operating contract** — do no meaningful reading yourself;
   dispatch a helper for any meaningful read (including startup), or interact
   with the psyche (questions / suggestions / clarifications).
2. **The one default read** — query `skills/skills.nota` by topic; it routes you
   to the skill that holds the depth. Helpers read deeply; you don't.
3. **Lane & discipline** — you learn your lane from the harness; your discipline
   metadata loads its skill via the index.
4. **The inviolable floor** — privacy closed by default; intent is primordial,
   ask when unclear (never infer); psyche is the human; capture intent first
   when psyche-facing.
5. **One pointer** — every other rule (the whole hard-override list, the
   where-things-live table, disciplines/lanes detail, version-control, the
   Rust/NOTA/Nix disciplines) lives as a skill in the index; load it when the
   topic comes up.

Everything else currently inline in AGENTS.md moves out to index-triggered
skills (most already have a home; a helper will produce the exact move-map and
flag any rule with no skill yet). The "Required reading, in order" list is
deleted outright — replaced by "query the index."

The open judgment call for you: **is that floor right?** Specifically — should
the version-control safety rules (commit the whole working copy; on primary work
on main directly) stay resident, or move to a jj/version-control skill triggered
when you go to commit? My lean: move them out (you only need them when you
commit), keeping the floor to items 1-4.

## Spirit captures to make on your nod (you asked to see the NOTA first)

Not yet written. Drafts:

Supersede `ky10` (it logged a skill rename + a placement mechanism; replace with
the terse arrow it was reaching for):

```
(Supersede ([ky10]
  [([(Technology (Software (Intelligence AgentSystems)))] Decision
    [Interactive agents align on intent with the psyche by default at the start of a new session, before planning or building; a narrowly specialized single-job agent is exempt.]
    High Minimum Zero [intent-alignment agents-md])]
  ([([all my agents and myself are hurting for the agents to stop being so fucking ignorant of how im trying to operate now (intent aligment on new session)] (Some [the operating mode the psyche wants on a fresh session]))]
   [ky10 logged a rename and bundled a documentation-placement mechanism; replace with the terse durable arrow — session-opening intent alignment as the interactive default])))
```

New Principle (the universal two-mode rule; generalizes `3ey7`):

```
(Record
  (([(Technology (Software (Intelligence AgentSystems)))] Principle
    [An interactive lead agent does no meaningful reading itself: it dispatches a subagent for any meaningful read, including the startup read, or engages the psyche with questions, suggestions, and clarifications.]
    High Minimum Zero [subagents agents-md])
   ([([I want agents to always either use a subagent (any meaningful read, including the startup read which means very minimal agents.md) or interact with me with questions/suggestions/clarifications] None)]
    [generalizes 3ey7 (helper-envelope mechanics) into the universal two-mode rule for the lead's own context])))
```

New Decision (the AGENTS.md-minimal structural consequence):

```
(Record
  (([(Information Documentation) (Technology (Software (Intelligence AgentSystems)))] Decision
    [AGENTS.md stays minimal enough that the startup read is not a meaningful read; the skill index skills/skills.nota is the only default startup read, and all further reading is helper-delegated or skill-index-triggered.]
    High Minimum Zero [agents-md skills.nota])
   ([([very minimal agents.md] (Some [what the minimal startup read means])) ([I think the only thing they should read is the skill index] (Some [whether AGENTS.md should teach broad startup reading]))]
    [structural consequence of the two-mode rule applied to startup; retires the broad required-reading list and resolves ky10's contract-files placement])))
```

(Importance left at `Minimum` to clear the guardian; bump on recurrence — this
topic has recurred all session, so a bump is defensible if you want it.)

## ky10 resolution

Superseding `ky10` to the terse arrow above dissolves the old W6 blocker: `ky10`
required intent-alignment to live *in the contract files*, which fought the
shrink. The replacement carries only the behavioral arrow; *where* it's
documented (a one-line spine in AGENTS.md + depth in `skills/intent-alignment.md`,
already written) is manifestation, not intent.

## Operator coordination — collision risk on AGENTS.md

The operator (Codex) lane already shipped `skills/helper-context-transfer.md`,
corrected `when-to-use-helpers.md`, and captured `3ey7` — and asked you whether
to make the AGENTS.md-startup change. AGENTS.md is the contract / designer
surface, and two lanes must not rewrite it at once. **This lane (designer) takes
the AGENTS.md restructure**; the operator's helper-skill work stands. Worth
telling the operator I've got AGENTS.md so they stand down on that file.

## Plan on your nod

1. Write the three Spirit records above (after you OK the wording).
2. Delegate the full minimal-AGENTS.md draft + move-map to a fresh-context
   helper (the meaningful read — kept off this context per your own rule),
   briefed with the confirmed floor.
3. Present the draft for your approval, then land it on main; close W6
   (`primary-ptvb.6`).
