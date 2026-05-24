*Kind: Design Meta-Report · Topic: schema-language-v4 · Date: 2026-05-24 · Lane: second-operator*

# 179 — schema language v4 design research

## Trigger

The psyche asked second-operator to do an independent design of the
designer's schema design in `reports/designer/326-v3-spirit-complete-schema-vision.md`,
using subagents for research.

## Fresh intent base

Spirit records captured before research:

- 438 — schema files use `.schema`.
- 439 — header declarations come first and drive receive triage.
- 440 — schema file has no outer struct wrapper.
- 441 — header root is a vector of ordered enum variants.
- 442 — schema imports can be namespace imports with optional selection.
- 443 — namespaces use maps; other extensible schema shape favors enums and
  vectors.
- 444 — component schema defines regular signal, owner signal, and sema
  headers.
- 445 — PascalCase booleans are unit variants.

## Subagent allocation

- `1-designer-report-critique.md` — read the designer report and fresh
  intent; identify what is wrong, what survives, and what must be
  redesigned.
- `2-nota-shape-research.md` — focus on NOTA grammar, map/vector/enum
  representation, `.schema` syntax consequences, and concrete examples.
- `3-implementation-model-research.md` — inspect the new `schema` repo and
  propose the Rust type model that best fits the corrected design.

## Orchestrator synthesis

The orchestrator writes `4-overview.md` with the proposed v4 design,
remaining questions, and implementation direction.
