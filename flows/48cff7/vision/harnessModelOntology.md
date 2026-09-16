# harnessModelOntology

## 2026-09-16 — the model-and-persona ontology belongs in the harness skills

Context: the living asked whether this flow knew the models on each harness, was told the Claude side but only fragments of the Codex side, and then set the fix.

> Well, we need to have that in the skills. This is the ontology. We need the ontology of our knowledge in the skills. We need to read the skills. Make a skill, or add to a skill, to understand which models are with which harnesses. Shouldn't that be with the different harnesses? You can read Codex harness and Claude harness skills. Find out what's missing from them. You probably have that information around. We've done so many flows. You could probably find stuff in the flows about this. I don't know. What's the most efficient way for you to find out?

-- psyche, STT.

Prior anchor: `flows/38dec9/vision/perHarnessSkills.md` — the original charter for per-harness skills, which asked to move "everything we know" into them; model lists were not filled in at that time. This entry proposes cashing that in.

Flow reading, not the living's words: the `claude-harness` and `codex-harness` skills already carry the strata, the system-prompt override flags, and the visibility rules. What is missing in both is the **model list by effort tier**, and the mapping from model to **persona name** used across the flows. Both are proposed here as additions, sourced only from psyche records this flow read.

## Proposed addition to `claude-harness`

Add a section after the strata paragraph:

> ### Models
>
> Claude Code carries four production Anthropic models. Effort tiers are the flow's discipline, not the API's; the model choice per tier is a convention set by the living.
>
> - **Fable 5.1** (`claude-fable-5-1`) — top-tier orchestrator, the psyche-facing main flow model on the Claude side per `flows/9e7c9f/vision/models.md` (2026-09-13). Persona: **Fable**, the doubter — "Fable has to try to see that there are pieces missing" (`flows/024bc7/vision/parallelSessions.md`).
> - **Opus 5** (`claude-opus-5`) — mid-to-high; used for subagents launched by main flows, including from Codex-side main flows via `claude -p` (`flows/162eb3/vision/subflows.md`). Persona: **Sol** — the "Sol audit" and "Sol subagents" naming (`flows/162eb3/vision/subflows.md`, `flows/358f143a/vision/entryFiles.md`). The living has a documented preference for Opus 4.6 over Opus 5 as an interlocutor (`flows/5851f4/vision/psycheFacingModel.md`, `flows/58a86d/vision/subagentModel.md`).
> - **Sonnet 5** (`claude-sonnet-5`) — the low-effort psyche model on the Claude side per `flows/48cff7/vision/flowNaming.md` (2026-09-16). Pairs with the Codex-side Terra.
> - **Haiku 4.5** (`claude-haiku-4-5-20251001`) — the lightweight tier.
>
> Fast mode swaps Opus onto a faster serving path via `/fast`; available on Opus 5 and Opus 4.8. This flow currently runs on Opus 4.7 [1m] — a 1M-context Opus variant not in the four-model production list.

## Proposed addition to `codex-harness`

Add a section after the base-instructions paragraph:

> ### Models
>
> Codex CLI carries OpenAI GPT-5 family models. Model IDs seen in the psyche records include `gpt-5.1`, `gpt-5.2`, and `gpt-5.6-luna` (`flows/4ddc321d/vision/hijackRepositories.md`, `flows/01a01bac/vision/skillDesigning.md`); the full catalogue is in `~/.codex/config.toml` at launch and can be pinned per invocation with `-m <model>`.
>
> Persona and tier convention:
>
> - **Astra** — the implementer persona; the Codex-side main flow at the Fable-paired tier. "Astra's good at getting it done, but he's not really good at seeing that his idea probably doesn't meet what the living psyche wants" (`flows/024bc7/vision/parallelSessions.md`). Pairs with Claude Fable.
> - **Terra** — the low-effort psyche persona/model on the Codex side (`flows/48cff7/vision/flowNaming.md`), used for report writing (`flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`). Pairs with Claude Sonnet.
> - **Luna** — the cheap-model persona on the Codex side, mapped to `gpt-5.6-luna` (`flows/024bc7/vision/effort.md`, `flows/01a01bac/vision/skillDesigning.md`). Used for the transcript-extraction narrator (`flows/6cc91b/vision/transcriptExtraction.md`). Distinct from Terra: Luna is the low-effort *non-psyche* worker (extractor, messenger), Terra is the low-effort *psyche*.
>
> Effort mode:
>
> - `medium` is the working default (`flows/024bc7/vision/effort.md`).
> - `high` is a "waste" reserved for quota-burn scenarios.
> - `low` runs on Luna or Terra, per role.
>
> Cross-harness constraint: a Codex main flow does not launch another Codex to run OpenAI models, and a Claude main flow does not launch another Claude to run Anthropic models (`flows/162eb3/vision/subflows.md`). A Codex main flow may launch `claude -p` for an Opus (Sol) subagent, and a Claude main flow may launch `codex exec` for a GPT subagent — each launches the *other* harness for the *other* vendor's models.

## Gaps this proposal does not fill

- **Codex model list beyond what psyche records name.** `gpt-5.1 / 5.2 / 5.6-luna` are the only IDs in the flows; the full family (mini, nano, o-series, other tiers) needs to come from the Codex CLI's own catalogue and be added at the same time.
- **Persona-to-model mapping on the Codex side is partial.** Astra is a persona; the model it runs on is not spelled out in the flows this pass covered.
- **Whether "persona" should live in the harness skills at all** — persona is arguably a cross-cutting concept (a psyche flow's role), separate from harness mechanics. If the living prefers, personas move to a new `flow-personas` skill and each harness skill only lists model IDs and tiers.

## Open questions worth the living's word

1. Approve the two proposed additions verbatim, edit them, or reject.
2. Fill in the Codex-side model list (mini/nano/o-series/other tiers) so the ontology is complete.
3. Confirm the Astra-to-model mapping (which GPT-5 variant Astra runs on).
4. Decide whether personas stay in the harness skills or move to their own skill.
