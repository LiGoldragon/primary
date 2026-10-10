# Operational: harness-specific rules

## The classifier-refusal-stop rule I proposed isn't spirit-level — it's harness-specific. Spirit is universal; different models and harnesses have different classifier behaviors, so their operating rules belong at the harness / model level, in an AGENTS.md-style layer, or in a cloud-core system that owns those rules for that model — it's part of the system prompt for that harness

Context: typed to primary Psyche opus (Claude flow da1e3f) on 2026-09-17 correcting a proposal I made to lift the "a refusal is a stop" rule into the spirit skill. The correction places the rule at the right layer: harness-specific system-prompt content. This is the first entry in the design of a Prompt component (see operational-promptComponent.md, same date). Logged by the main flow before acting.

> No, I would make it like an agents.md thing, or it's specific to the model. It's not spirit level; it's specific to the model. Maybe we have a cloud core system, and that's where it would go. It's part of the system prompt.

-- psyche, typed.
