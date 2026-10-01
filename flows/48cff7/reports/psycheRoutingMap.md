# Psyche Routing Map

*Vision distillation proposal — pending living review*
*Flow 48cff7 · Primary MEDIUM · Opus 4.7 [1m] · 2026-09-16*
*Companion: `psycheRoutingGaps.md`*

The system as we intend it: how a psyche event travels through layers, stacks, and effort tiers before anyone is asked to think.

## Figure — brief for a subflow to draw

One diagram, wide format. Its claim: *a logged-psyche event fans into each stack's LOW packager; MEDIUMs process and mirror across stacks; HIGH stays quiescent until an explicit escalation.*

Layout: a 3×3 grid. Rows are the three stacks (Claude, Codex, Open — Open dashed / not-yet). Columns are the three effort tiers (LOW / MEDIUM / HIGH). Each cell is a small labeled box. Above the grid, a single LIVING band; below the grid, two short annotations covering LAYERS (walk-up) and NON-PSYCHE INPUT (funnel).

Arrows:

- From LIVING (top) a trunk branches into each row's LOW box, labeled *logged psyche*.
- Within each row: LOW → MEDIUM (solid, labeled *packet*); MEDIUM → HIGH (dashed, labeled *explicit only*).
- Vertical *mirror* arrows connect all three MEDIUM cells (Claude ↔ Codex ↔ Open), labeled *same effort*. These are the one visual element the map hinges on — draw them in the report's accent.
- Boxes in the HIGH column are dashed (quiescent). The whole OPEN row is dashed (unbuilt stack).

The diagram earns its place by showing the two rules the prose can't compact: same-effort mirroring across stacks, and LOW-as-packager sitting between LIVING and MEDIUM.

## Proposed distilled Vision — psycheRouting

Each item is offered as a distilled Vision statement pending the living's review. Accept, edit, or reject in place.

- **R1.01 — Address.** A flow's address is `(layer, role, effort, stack)`. Effort is a per-stack notion; "medium" is meaningful only inside a stack.
- **R1.02 — Mirror rule.** Living speech to a psyche at `(layer, effort)` mirrors to every stack's psyche at the same `(layer, effort)`.
- **R1.03 — Non-psyche funnel.** Living input to a non-psyche flow funnels through that layer's psyche first. Non-psyche flows never receive raw living input directly.
- **R1.04 — LOW is the packager.** A logged-psyche marker fires; the layer/stack's LOW picks up context and produces a self-contained message for MEDIUM.
- **R1.05 — MEDIUM is the processor.** It thinks, drafts, distills, and responds to the living.
- **R1.06 — HIGH is quiescent.** It is reached only on an explicit living word, or on a psyche's explicit escalation from below.
- **R1.07 — Layer walk-up.** If the addressed layer has no psyche, walk up one layer at a time until one is found. Core is the guaranteed floor.
- **R1.08 — Own authority.** A psyche flow acts under its own authority. That authority includes passing the message further up.
- **R1.09 — Presentation flow.** A presentation flow is a main flow, not a subflow. Low-powered by default; may unfold across multiple responses; delegates image-making to subflows and stitches them back.
- **R1.10 — Gatherer subflow.** A presentation flow's first subflow is a gatherer. It uses verbatim psyche as its guide and produces a report of what HIGH has said lately.
