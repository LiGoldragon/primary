# highPowerAndUpgradePipeline

## 2026-09-16 — the language-UI naming: Psyche Fable, Psyche High Power; the vision-to-spirit upgrade pipeline; system-prompt conformance check

Context: at the end of the flow's working session, ahead of an overnight pass, the living laid out the language-UI naming for talking to psyche pair members, the pipeline that carries reports up to skills / intent / spirit, and the conformance check the same source vision drives against the stock system prompt.

> When we're ready for the overnight pass, we're going to start a new main flow for Psyche Fable, a new successor to the High Powered. If I say Psyche Fable, it's the High Powered, basically. It's actually a short. That's what we should call them: bi-model, Fable Psyche.
>
> In the aggregate, you could just say Psyche High Power, and then you would be talking to both Fable and Astra, or whatever is configured to run right now. I'm just defining the user interface here. This is a language-based user interface.
>
> Before we're ready to put this vision together into implementation, everything that is in the backlog, we use these reports to create the distilled vision. Every time, it's a proposal for a change in the vision, an addition, or a new vision, a new topic vision. These are the source for our skills. Some of them we upgrade to intent, which becomes a system prompt, and then spirit, which becomes accentuated and presented as an important part of the system prompt, like general guidelines.
>
> Also, whatever we put in there would be what we would use to check the system prompt that's currently in stock to find things that contradict what we want. Maybe change that part and then create a log of all these changes and what they were for, so that we can, in each harness, refer back to them and what part of the vision they were contradicting.

-- psyche, typed.

## Language-UI naming

The living's terms for addressing psyche flows:

- **Psyche Fable** — a short for the high-powered psyche on the Claude side (currently the Fable model). "If I say Psyche Fable, it's the High Powered."
- **Bi-model, Fable Psyche** — the living's own preferred phrasing captured verbatim; reading unclear ("bi-model" may mean the pair at that tier).
- **Psyche High Power** — the aggregate term for the whole pair (or triad) at the high tier. "You would be talking to both Fable and Astra, or whatever is configured to run right now."

The names are a *user interface*, not new components. The underlying flows are the same pair anatomy in `flows/48cff7/vision/psychePairAnatomy.md`; the names route the living's speech to the whole pair or to one side.

## The vision-to-spirit upgrade pipeline

The pipeline the living named — each step promotes material one level up in authority:

1. **Reports** — a flow's output distilled for review (per `flows/48cff7/vision/refreshPurpose.md`).
2. **Distilled vision** — each report becomes a proposal against the vision: a change, an addition, or a new topic vision. The vision entry is the source for skills.
3. **Skills** — the Curriculum-nexus generates the deterministic-named files from a vision subject's sections (per `flows/48cff7/vision/visionAsSkillSource.md`).
4. **Intent** — some vision items promote to intent. Intent enters the system prompt (top stratum).
5. **Spirit** — some intent (or its ground) promotes to spirit. Spirit is accentuated in the system prompt as the important general guidelines.

Each promotion carries the psyche citation (per `escalationHierarchy.md`). The living authorizes promotions past intent and spirit levels.

## System-prompt conformance check

The same source vision drives a conformance check against each harness's stock system prompt (Claude Code base + injected middle; Codex base instructions; the open-source harness once it lands).

Steps:

1. Read the stock system prompt for the harness in question.
2. Compare against current Intent and Spirit entries.
3. Where the stock contradicts a standing intent or spirit statement, change the stock — via the harness's replacement mechanism (Claude's `--system-prompt-file` / `--append-system-prompt-file`; Codex's `model_instructions_file`).
4. Log every change: what was changed, why, which vision entry it was contradicting.
5. The log lives per harness — one log file each — so a session can refer back to what changed and what standing item drove it.

## Consequences

- **The overnight pass has an ordered backlog.** Each vision entry produced this session becomes a distilled-vision proposal; each proposal drives one skill edit, one intent promotion, or one spirit promotion, on the living's word.
- **The signal-curriculum draft this flow just committed** (`flows/48cff7/proposals/signal-curriculum.md`) is a candidate implementation of steps 2–3 of the pipeline: it reads vision subjects and generates the derivative kinds. Codex is being sent it.
- **The conformance check needs a place to log.** Proposed name: `<harness>-conformance.log.md` in a per-harness folder, each row `{ date  changed  reason  vision-citation  commit-hash }`.

## Open questions worth the living's word

1. Confirm "Psyche High Power" as the aggregate name, or edit.
2. Confirm "Psyche Fable" as the Claude-side high-tier shorthand, or edit.
3. Whether "bi-model" is meant literally (two models) or as "pair"; the flow reads it as the pair, uncertainly.
4. Whether the conformance log lives in each harness's own repository, in this Curriculum, or in a top-level `Conformance/` folder.
5. Whether the pipeline steps have named waypoints on the wire (`ProposeVisionChange`, `PromoteToIntent`, `AccentuateAsSpirit`) or are handled outside the signal vocabulary.
