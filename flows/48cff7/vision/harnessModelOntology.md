# harnessModelOntology

## 2026-09-16 — the model-and-persona ontology belongs in the harness skills

Context: the living asked whether this flow knew the models on each harness, was told the Claude side but only fragments of the Codex side, and then set the fix.

> Well, we need to have that in the skills. This is the ontology. We need the ontology of our knowledge in the skills. We need to read the skills. Make a skill, or add to a skill, to understand which models are with which harnesses. Shouldn't that be with the different harnesses? You can read Codex harness and Claude harness skills. Find out what's missing from them. You probably have that information around. We've done so many flows. You could probably find stuff in the flows about this. I don't know. What's the most efficient way for you to find out?

-- psyche, STT.

Prior anchor: `flows/38dec9/vision/perHarnessSkills.md` — the original charter for per-harness skills, which asked to move "everything we know" into them; model lists were not filled in at that time. This entry proposes cashing that in.

Flow reading, not the living's words: the `claude-harness` and `codex-harness` skills already carry the strata, the system-prompt override flags, and the visibility rules. What is missing in both is the **model list by effort tier**, and the mapping from model to **persona name** used across the flows. Both are proposed here as additions, sourced only from psyche records this flow read.
