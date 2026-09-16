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
> Claude Code carries Anthropic models. Effort tiers are the flow's discipline, not the API's; the model choice per tier is a convention set by the living. The Anthropic side does not use celestial persona names — models are named directly (Fable, Opus, Sonnet, Haiku); celestial names (Astra, Sol, Terra, Luna) name Codex-side models on the other stack.
>
> Models in use:
>
> - **Fable 5.1** (`claude-fable-5-1`) — top-tier orchestrator, the psyche-facing main flow model per `flows/9e7c9f/vision/models.md`. The doubter — "Fable has to try to see that there are pieces missing" (`flows/024bc7/vision/parallelSessions.md`). Pairs with Codex GPT 6 Astra.
> - **Opus 5** (`claude-opus-5`) — current top Opus.
> - **Opus 4.8** — Fast Mode capable (also Opus 5 via `/fast`).
> - **Opus 4.7 [1m]** — 1M-context Opus variant; this flow's model.
> - **Opus 4.6** and **Opus 4.6 [1m]** — the living's preferred psyche-facing interlocutor (`flows/5851f4/vision/psycheFacingModel.md`, `flows/58a86d/vision/subagentModel.md`).
> - **Sonnet 5** (`claude-sonnet-5`) — used for report-writing and visualization subflows.
> - **Haiku 4.5** (`claude-haiku-4-5-20251001`) — lightweight.

## Proposed addition to `codex-harness`

Add a section after the base-instructions paragraph:

> ### Models
>
> Codex CLI carries OpenAI GPT models. Model IDs are picked from `~/.codex/config.toml` at launch and can be pinned per invocation with `-m <model>`. All celestial persona names (Astra, Sol, Terra, Luna) sit on this side, not on Claude.
>
> Models in use:
>
> - **GPT 6 Astra** (`gpt-6-astra`) — top-tier implementer. "Astra's good at getting it done, but he's not really good at seeing that his idea probably doesn't meet what the living psyche wants" (`flows/024bc7/vision/parallelSessions.md`). Pairs with Claude Fable.
> - **GPT 5.6 Sol** (`gpt-5.6-sol`) — used as the audit / mid-tier subagent (`flows/162eb3/vision/subflows.md`: "Sol audit as a separate codex exec process"; `flows/358f143a/vision/entryFiles.md`: "Sol subagent constraint stays in AGENTS.md").
> - **GPT 5.6 Terra** (`gpt-5.6-terra`) — low-effort psyche on the Codex side (`flows/48cff7/vision/flowNaming.md`), used for report writing (`flows/01a0428b/vision/useASubflowToPutTheReportTogether.md`). Pairs with Claude Sonnet.
> - **GPT 5.6 Luna** (`gpt-5.6-luna`) — cheap-model worker, non-psyche (`flows/024bc7/vision/effort.md`, `flows/01a01bac/vision/skillDesigning.md`). Used for the transcript-extraction narrator (`flows/6cc91b/vision/transcriptExtraction.md`). Distinct from Terra: Luna is the low-effort *non-psyche* worker (extractor, messenger); Terra is the low-effort *psyche*.
>
> Effort mode:
>
> - `medium` is the working default (`flows/024bc7/vision/effort.md`).
> - `high` is a "waste" reserved for quota-burn scenarios.
> - `low` runs on Luna or Terra, per role.
>
> Cross-harness constraint: a Codex main flow does not launch another Codex to run OpenAI models, and a Claude main flow does not launch another Claude to run Anthropic models (`flows/162eb3/vision/subflows.md`). A Codex main flow may launch `claude -p` for an Anthropic subagent (Opus, etc.), and a Claude main flow may launch `codex exec` for a GPT subagent — each launches the *other* harness for the *other* vendor's models.

## Note on prior confusion (corrected)

An earlier version of this entry (and of `flows/48cff7/vision/flowNaming.md`) placed Sol on the Claude side. The living corrected this in the artifact comment thread `69c83ec9` on 2026-09-16: **all four celestial names sit on the Codex side** — `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`. Claude-side flows are named by their Anthropic model directly (Fable, Opus 4.6/4.7/4.8/5, Sonnet, Haiku).

## Open questions worth the living's word

1. Approve the two proposed additions verbatim, edit them, or reject.
2. Confirm the pair mapping — Fable↔Astra is settled; is Sonnet↔Terra correct; is Haiku↔Luna the low-worker pair; where does Sol pair (Opus 5? Opus 4.7 1M? something else).
3. Decide whether persona names stay in the harness skills, or move to their own `flow-personas` skill.
4. Any Codex models in use that were not named in the artifact comment thread (e.g. models below Luna, or above Astra).
