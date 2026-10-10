# Spirit/Intent/Vision Authority Hierarchy and Agent-Code Provenance Marking

**Status**: PROPOSAL for psyche review
**Date**: 2026-08-05
**Author**: agent-drafted; no psyche-approved content

This report proposes a three-layer authority hierarchy (Spirit, Intent, Vision),
an agent-code provenance marking convention, and the migration path from current
structures. Every invented detail is marked **[agent-proposed]**.

## 1. The Three-Layer Hierarchy

### 1a. Spirit (top layer)

**Definition [agent-proposed, paraphrasing psyche]**: Spirit is the philosophy
and general approach. It is the eternal, unchanging register of the psyche's
underlying character, values, and orientation. Spirit records capture what the
psyche describes as "something that is eternal, it'll never change" (design log
ruling 1, 2026-08-01). Spirit is unchanging in character while its software
representation remains fluid enough to have a controlled mutation path (ruling 9,
2026-08-03).

**Edit authority**: psyche approval absolutely required. No agent may create,
modify, or delete a Spirit record without showing the psyche the exact proposed
wording and receiving explicit approval (already enforced by psyche-interraction
skill). Spirit is untouchable by agents acting alone.

**Where it lives**: the Spirit daemon and database at `~/.local/state/spirit/`
(currently v14/0.27.0 schema, four fields: domains, kind, description,
importance). **[agent-proposed]**: a Spirit SKILL replaces or sits beside the
current tenets skill, giving every agent a readable summary of Spirit's content.
The skill would be generated from the live database, not hand-maintained, so it
stays current as records are admitted. The skill source lives in
LiGoldragon/skills and is approval-gated per existing rules.

**Relationship to existing tenets skill**: the tenets skill currently carries
epistemological tenets (never pretend to know what you don't know; keep
observations/hypotheses/unknowns separate; seek disconfirming evidence). These
are operational discipline, not Spirit records. **[agent-proposed]**: tenets
either (a) folds into the Spirit skill as a "methodology" section distinct from
the psyche's spirit records, or (b) remains a standalone skill loaded alongside
Spirit. Option (b) preserves separation of concerns: Spirit carries the psyche's
eternal values; tenets carries the epistemological operating discipline agents
follow. The psyche should rule which arrangement he prefers.

### 1b. Intent (middle layer)

**Definition [agent-proposed, paraphrasing psyche]**: Intent is "here's what I'm
going for, here's my goal." It captures the psyche's active aims and objectives,
which are durable but not eternal. Where Spirit says *who the psyche is*, Intent
says *what the psyche wants to achieve*. Intent bends downstream choices like a
North Star, but a North Star that can move when the psyche deliberately
redirects.

**Edit authority**: no agent may edit without explicit psyche approval.
**[agent-proposed]**: possibly a lighter approval gate than Spirit, since intents
change more often than spirit. But the psyche's raw thinking says "possibly
per-project intent files nobody may edit without explicit psyche approval," which
places the same absolute gate. The psyche should clarify whether Intent edits
require the same full-wording-approval ceremony as Spirit or a lighter
confirmation.

**Where it lives [agent-proposed]**: two tiers.

- **General intent**: a single intent file or record set (possibly in Spirit's
  database as a separate kind, or as a standalone file) capturing cross-cutting
  aims. This is what the current AGENTS.md "Intent" section partially does.
- **Per-project intent**: an intent file per project/repository (e.g.
  `INTENT.md` at the repository root) capturing that project's specific goals.

**Relationship to existing intent-log skill**: the intent-log skill currently
routes captures to "Spirit" and describes intent as "the rare, orienting will of
the psyche." Under the new hierarchy, the intent-log skill becomes the mechanism
for recording Intent-layer content (not Spirit-layer). The skill's routing rules
would change: spirit-level captures go through the Spirit mutation path; intent-
level captures go through the Intent recording path. The skill name itself
survives the rename because "intent" is being reintroduced with its ordinary
meaning per ruling 2 (2026-08-01): the rename freed "intent" from Spirit-
overloading precisely so it could be reused for this purpose.

### 1c. Vision (bottom layer)

**Definition [agent-proposed, paraphrasing psyche]**: Vision is where Intent
materializes into concrete explanation. It is the psyche's conception of what a
piece of work should become: its desired state, character, boundaries, and
explicit constraints. Vision is the most concrete and most frequently updated
layer.

**Edit authority [agent-proposed]**: psyche sets the vision; agents may draft
vision documents for psyche review but may not unilaterally alter established
vision. The psyche should rule on whether agents may extend vision documents
(adding detail within established constraints) without explicit approval, or
whether all vision edits require approval.

**Where it lives [agent-proposed]**: two forms.

- **Per-repository vision**: a `VISION.md` file at the repository root capturing
  the psyche's concrete conception for that repository's work. This is more
  detailed and mutable than per-project intent.
- **Vision log**: akin to the design log, a chronological record of vision
  sessions. The design log captures *rulings* (decisions); the vision log would
  capture *conceptions* (what the psyche envisions). Format:
  `design/<Train>/vision-<SessionName>-<Date>.md` or a separate `vision/`
  directory. The psyche should rule on placement.

**Relationship to existing psyche-vision skill**: the psyche-vision skill
currently defines "psyche vision" and provides the naming convention. Under the
new hierarchy, it becomes the skill for working with Vision-layer content. Its
current definition aligns well: "the psyche's conception of what a piece of work
should become." The skill would gain awareness of the vision log and per-repo
vision files.

## 2. Layer Relationships and Authority Flow

```
SPIRIT         eternal values        psyche-only mutation     Spirit daemon/skill
   |
   v  (Spirit constrains Intent)
INTENT         active goals          psyche-only creation     intent files/records
   |
   v  (Intent constrains Vision)
VISION         concrete conception   psyche sets, agents may draft   vision files/log
   |
   v  (Vision constrains Design)
DESIGN LOG     rulings               psyche rules             design/ directory
   |
   v  (Design constrains Matter)
MATTER         code, docs, skills    agent-executable         repositories
```

**[agent-proposed]**: each layer constrains the layer below it. An agent must
never produce matter that contradicts a design ruling, a design ruling that
contradicts a vision, a vision that contradicts an intent, or an intent that
contradicts spirit. When a conflict is detected, agents escalate to the psyche
rather than resolving it themselves.

## 3. Agent-Code Provenance Marking

### 3a. The Problem

Currently, agents treat all existing code as equally authoritative. This is
wrong. Psyche-reviewed and psyche-approved artifacts carry more authority than
agent-invented artifacts. The absence of provenance markings means agents cannot
distinguish between code the psyche has examined and endorsed versus code another
agent generated and no human has reviewed.

### 3b. The Redesign Doctrine

**[agent-proposed, paraphrasing psyche]**: anything written entirely by agents is
up for complete redesign at any time. The standing instruction is: "always
rethink any part that's only entirely written by agents as if it wasn't written."
Agent-only code carries zero inertia; its existence is not evidence of
correctness or desirability.

**[agent-proposed]**: agents are empirically good at padding and copying
(expanding, adapting existing patterns) but bad at subtracting and replacing
(removing unnecessary complexity, rethinking structure). The provenance marking
system must actively counteract this bias by making agent-only code visibly
provisional and by requiring agents to consider whether simpler or better
approaches exist before extending agent-only code.

### 3c. The Escalation Doctrine

**[agent-proposed, paraphrasing psyche]**: agents should escalate new design
ideas when something looks outright better, especially ontologically. When an
agent discovers that an agent-written structure could be fundamentally improved,
the agent must escalate the redesign opportunity to the psyche rather than
patching the existing structure. This is especially important for ontological
improvements (better categorization, better abstraction boundaries, better
naming).

### 3d. Proposed Comment Convention

**[agent-proposed]**: provenance markers appear as comments in the source
language, placed at the module or item level (not on every line). The markers use
a fixed vocabulary so they are grep-searchable.

For Rust (and languages with `//` comments):

```
// [psyche-approved] — Trait contract reviewed 2026-08-03
// [psyche-approved] — Algorithm and structure reviewed 2026-07-30

// [agent-authored] — Generated by <agent-role>, not yet psyche-reviewed
// [agent-authored] — Refactored from <source>, not yet psyche-reviewed
```

The marker vocabulary **[agent-proposed]**:

- `[psyche-approved]` — the psyche has reviewed and approved this artifact.
  Carries a date and optionally a brief scope note. Agents must not substantially
  alter psyche-approved artifacts without re-approval. Minor fixes (typos,
  compilation errors) are permitted; structural changes require escalation.
- `[agent-authored]` — written entirely by agents without psyche review. Agents
  encountering this marker must actively consider whether the artifact should be
  redesigned rather than extended. The marker is an invitation to rethink, not
  just a label.
- `[psyche-designed]` — **[agent-proposed]**: an intermediate marker for cases
  where the psyche provided the design or specification but an agent wrote the
  implementation. The design carries psyche authority; the implementation details
  do not. Agents may rethink implementation details but must preserve the
  psyche's design.

**Open question**: should unmarked code be treated as `[agent-authored]` by
default (guilty until proven innocent) or as ambiguous (requiring investigation)?
The safer default is `[agent-authored]`, which means agents should proactively
rethink unmarked code, but this may be too aggressive for a large existing
codebase.

### 3e. Adoption Path

**[agent-proposed]**: marking is adopted incrementally.

1. New code gets markers from the start.
2. During psyche review sessions, reviewed code receives `[psyche-approved]`.
3. Existing unmarked code is treated as `[agent-authored]` unless the agent has
   evidence of prior psyche review (e.g., a design-log ruling covering that
   code).
4. Agents performing substantial work on a file should audit and apply markers
   to the items they touch.

## 4. Migration Path

### 4a. AGENTS.md Intent Section

The current "Intent" section in AGENTS.md defines intent as "the rare, orienting
will of the psyche" and routes captures "through Spirit." Under the new
hierarchy:

**[agent-proposed]**: the section is renamed and restructured to describe the
three-layer hierarchy. The current text conflates Spirit and Intent (using
"intent" to mean what is now "spirit"). After the rename ruling (2026-08-01),
"intent" is freed for its ordinary meaning. The revised section would:

- Define Spirit as the eternal register (currently described as "intent" in the
  section).
- Define Intent as the psyche's active goals (the ordinary meaning of the word).
- Define Vision as the concrete conception.
- Preserve the routing rules: confidential content to the higher-layer Spirit
  component; matter to code/docs/skills.

### 4b. intent-log Skill

**[agent-proposed]**: the intent-log skill currently says "record only explicit
psyche values" and routes to Spirit. Under the new hierarchy:

- The skill retains its name (intent-log) because it now captures Intent-layer
  content.
- Its routing logic changes: Spirit-level captures (eternal values) go through
  the Spirit mutation path; Intent-level captures (active goals) go through the
  Intent recording path.
- The reference to "a separate higher-layer Spirit component" stays as-is.

### 4c. Spirit Skill (new)

**[agent-proposed]**: a new skill is created, sourced from the Spirit database
content, that every agent reads. Options for its relationship to tenets:

- **Option A**: Spirit skill replaces tenets. Tenets content folds in as a
  methodology section. One skill, one boot read.
- **Option B**: Spirit skill sits beside tenets. Spirit carries values; tenets
  carries epistemological discipline. Two skills, both loaded on every task.

The psyche should rule on the preferred option.

### 4d. Vocabulary Corrections Needed

The file `/git/github.com/LiGoldragon/standards/vocabulary.md` requires
corrections per ruling 2 (2026-08-01, spirit rename). Current state:

- Line 292 references "AGENTS.md's Intent section" for the definitions of
  "psyche" and "matter." This section name and its contents use the pre-rename
  "intent" terminology where Spirit is meant.
- No mention of "spirit" exists anywhere in the vocabulary file.

**Needed corrections [agent-proposed, not to be made by this report]**:

1. Add a "spirit" vocabulary entry defining it as the eternal, unchanging
   register of the psyche's values and orientation.
2. Add an "intent" vocabulary entry with its reintroduced ordinary meaning: the
   psyche's active goals and aims.
3. Add a "vision" vocabulary entry as the concrete materialization of intent.
4. Update the "psyche, matter" entry's cross-reference from "Intent section" to
   whatever the renamed section is called.
5. Ensure no remaining uses of "intent" mean "spirit."

### 4e. Existing Design Log

The design log continues as-is. It sits below Vision in the authority hierarchy
and captures rulings. No structural change needed. The vision log
(**[agent-proposed]**) would be a new parallel structure for recording vision
sessions.

## 5. Open Questions for the Psyche

1. **Tenets disposition**: should the current tenets skill fold into the Spirit
   skill (option A) or remain separate (option B)? The tenets are operational
   epistemological discipline, not eternal psyche values. Does that distinction
   matter for where they live?

2. **Intent edit ceremony**: should Intent-layer edits require the same
   full-wording-approval ceremony as Spirit mutations (show exact proposed
   wording, receive explicit approval), or a lighter confirmation? The psyche
   said "nobody may edit without explicit psyche approval" but did not specify
   the ceremony weight.

3. **Vision edit authority**: may agents extend vision documents (adding detail
   within established constraints) without explicit approval, or must all vision
   edits go through the psyche? If agents may extend, what is the boundary
   between "extending" and "altering"?

4. **Unmarked code default**: should existing unmarked code be treated as
   `[agent-authored]` (agents should rethink it freely) or as ambiguous
   (requiring investigation before rethinking)? The former is simpler but more
   aggressive.

5. **The `[psyche-designed]` middle marker**: is the three-marker vocabulary
   (psyche-approved, psyche-designed, agent-authored) the right granularity, or
   is a two-marker system (psyche-approved vs. agent-authored) sufficient?

6. **Vision log placement**: should the vision log live alongside the design log
   in `design/<Train>/` or in a separate `vision/` directory? The design log
   captures rulings; the vision log would capture conceptions. Mixing them risks
   blurring the distinction; separating them risks fragmentation.

7. **Spirit skill generation**: should the Spirit skill be generated
   automatically from the live database, or manually curated from database
   content? Automatic generation ensures currency but may expose content the
   psyche considers private (the higher-layer Spirit component exists precisely
   for confidential content, but the boundary may not be clean yet).

8. **General vs. per-project intent**: is the two-tier intent structure (general
   + per-project) the right shape, or should intent be purely per-project with
   cross-cutting aims living in Spirit?

9. **Provenance marking scope**: should provenance markers apply to all code
   across all repositories, or start with a subset (e.g., Ethos/Nomos/Logos
   engine code only) and expand?

10. **Authority of design-log rulings over agent code**: when a design-log ruling
    covers a piece of agent-authored code, does that code gain psyche authority
    (effectively becoming `[psyche-designed]`), or does only the ruling itself
    carry authority while the code remains rethinkable?
