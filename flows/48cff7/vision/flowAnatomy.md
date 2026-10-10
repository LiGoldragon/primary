# flowAnatomy

## 2026-09-16 — every major flow has its own custom harness system prompt; anatomy = what varies per flow

Context: while dispatching the transcript-nexus build to Codex, the living opened the "flow anatomy" topic. They asked to see the shape in ASCII so they can read it in the terminal.

> The visualization: every major flow, like a visualization flow or a psyche flow, has its own custom harness system prompt. Let's look at that. We can work with an ASCII chart because whoever is going to render it can render an ASCII chart just as well as anything else. He can even infer the graph from the ASCII chart, and then I can read it in the terminal. Unless it's more efficient to use Mermaid, maybe it's more efficient. It's just with it, but I want to see the anatomy of whatever I was talking about.

-- psyche, typed.

Flow reading, not the living's words: every named flow type (psyche, visualization, narrator, gatherer, implementation, …) is *shaped* by two things: a shared harness base and a role block that varies. The role block is the anatomy — that is what makes a visualization flow different from a psyche flow. ASCII carries the anatomy readably in the terminal; a renderer can infer the same graph from it that it would from mermaid, so the choice is stylistic when the density is low.

## Anatomy (ASCII)

```
flow harness system prompt
├── shared across flow types
│   ├── harness base                tool schemas · tone guidance · doing-tasks guidance
│   ├── project instructions        CLAUDE.md · NON_MANAGEMENT_AGENTS.md · SKILL_VARIABLES.md
│   ├── skills index                <name> — <one-line description>
│   └── environment                 cwd · git status · session id · date
│
└── role block                      ← varies per flow type; the anatomy
    ├── role name                   psyche · visualization · narrator · gatherer · implementation · …
    ├── effort tier                 LOW · MEDIUM · HIGH
    ├── stack                       Claude · Codex · open
    ├── layer                       primary · secondary · core
    ├── authority scope             what this flow may do; what it must never do
    ├── peers                       coordinating sessions
    ├── ad hoc skill body inline    setup-specific behavior not yet in Curriculum
    └── role skills to load         Curriculum skills the role's work always uses
```

## Example role blocks

```
role block — psyche · MEDIUM · Claude · primary  (this flow, 48cff7)
├── role name          psyche
├── effort tier        MEDIUM
├── stack              Claude
├── layer              primary
├── authority          draft locally, respond to living, dispatch subflows
│                      · NEVER contact HIGH without living word
│                      · NEVER refresh Codex, change settings, use reset
│                      · NEVER render (charts, SVG, HTML)
├── peers              Codex d9961c (native thread 01a0aacb-ac84-71a1-88a0-05ed9961ca9d)
├── ad hoc skill body  psyche-power-protocol
└── role skills        psyche · spirit · main-flow · transcript-search · datom · nexus

role block — visualization · [effort] · [stack] · [layer]  (does not yet exist)
├── role name          visualization
├── effort tier        (low; rendering is cheap)
├── stack              (any)
├── layer              (primary)
├── authority          receive (pointer, anatomy, ethos, intent), fetch block via transcript-nexus,
│                      produce SVG · NEVER edit source of truth · NEVER speak to living directly
├── peers              (whichever main flow dispatched it)
├── ad hoc skill body  (per dispatch)
└── role skills        transcript-search · datom · artifact-diagramming · artifact-design
```

## Open questions worth the living's word

1. Whether "stack" and "layer" belong inside the role block, or in the shared header (all flows in a given deployment carry the same stack and layer).
2. Whether "authority scope" is expressed as prose (as today) or as an ethos-typed capability set.
3. Which role skills are the fixed floor for each flow type (this is what "we should have started with" would look like made explicit).
4. Whether the ad hoc skill body should always be inline in the role block, or referenced by hash from Curriculum once a role stabilises.
5. Whether the "environment" bullet belongs above or below the role block in the actual prompt order (I put shared first here; the current Claude Code layout interleaves them).
