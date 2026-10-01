# Flow 48cff7 — Full Proposal

*Primary MEDIUM Claude psyche · Opus 4.7 [1m] · 2026-09-16*
*Branch: `flow/48cff7` on origin · latest commit noted at handoff*
*This is the accumulated proposal of this flow. It is the refresh package a successor psyche-main-flow session loads on `/main-flow`. Every claim carries a psyche citation in the linked vision entry.*

## Framing

Distillation is the psyche flow's output. Everything below is a candidate distilled Vision statement, sourced from the living's speech during this session and this flow's own reading. Nothing here stands until the living reviews it.

The material is grouped by topic, not by chronology. Each group cites the vision entries in `flows/48cff7/vision/` and the proposal files in `flows/48cff7/proposals/` that back it.

## What distillation is

The psyche flow's output is distillation. Raw entries under `flows/<flow>/vision/` and `flows/<flow>/notion/` become distilled Vision in `Vision/<topic>.md`, and on the living's word, distilled Intent in `Intent/<topic>.md`. Spirit is the top level, accentuated in the system prompt.

Cites: `psycheIsDistillation.md`, and the addition proposal `proposals/psyche-distillation-addition.md` (into the `psyche` skill).

## Routing model

An address is `(layer, role, effort, stack)`. Effort is per-stack; "medium" is meaningful only inside a stack.

- Living speech to a psyche at `(layer, effort)` mirrors to every stack's psyche at the same `(layer, effort)`.
- Living input to a non-psyche flow funnels through that layer's psyche first.
- LOW is the packager: a logged-psyche marker fires, and LOW picks up surrounding context to hand MEDIUM a self-contained packet.
- MEDIUM is the processor: it thinks, drafts, distills, responds.
- HIGH is quiescent by default; reached only on an explicit living word or a psyche's explicit escalation.
- Layer walk-up: if the addressed layer holds no psyche, ascend one layer at a time. Core is the guaranteed floor.

Cites: `psychePropagation.md`, `lowPsycheRole.md`, `pocShapeConfirmed.md`, `presentationFlow.md`, `psycheIsDistillation.md`.
Skill proposals: `proposals/psyche-pair.md`, `proposals/flow-role-separation.md`.

## Layers, tiers, and personas

Personas on the Codex side (celestial names): `gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`, `gpt-5.6-luna`.
Personas on the Claude side: named directly by model — Fable 5.1, Opus 5, Opus 4.8, Opus 4.7 [1m], Opus 4.6 (+ 1M), Sonnet 5, Haiku 4.5. All celestial names are Codex-side.

Language-UI shortcuts named by the living:

- **Psyche Fable** — the Claude-side high-tier psyche shorthand.
- **Psyche High Power** — the aggregate name for the whole pair (or triad) at the high tier.

Pair-and-triad anatomy: same-effort mirror across stacks; mode-aware (a peer in conservation mode drops out of the mirror); Fable spent last; core layer stays quiescent as defense.

Cites: `flowNaming.md`, `harnessModelOntology.md`, `psychePairAnatomy.md`, `highPowerAndUpgradePipeline.md`.

## Escalation

Every up-message qualifies only if it carries a psyche citation (Vision, Intent, Spirit, or raw verbatim log) plus one sentence naming what it is in response to. The higher layer judges the citation before acting; it decides to merge here or escalate again.

Effort escalates within a stratum up to the highest thinking power. From the highest, the next step is *out of stratum* — either to the harness's top stratum (promotion into base instructions for every future flow) or to the core layer (doubt-and-defense pass through the tertiary layer). Both are non-exclusive; core-then-top is a likely full path.

Even MEDIUM may address the living directly with a question when a citation warrants it; not routine, admitted.

Urgency accrues with each step up. At the core layer it reaches the express lane — bypass do-not-disturb, wake in the night — reserved for danger or major system problems.

Cites: `escalationHierarchy.md`, `messagingUp.md`.

## Nexus family

Every misimplemented durable component ports to a Nexus, not a parallel compatibility path. Nexuses at issue:

- **transcript-nexus** — replaces the argparse `transcript` shim; ordinary + meta sockets; signal ops `Show / Search / Raw / Block` for anchor-based extraction. Draft: `proposals/transcript-nexus.md`. Codex design brief queued at `01a0ac70-…`.
- **mind-nexus** — verified-fact store; records carry fact, date, trust variant (`Verified / Attested / Provisional / Deprecated`), evidence, subject. Interim before Nexus: folder-per-variant on the filesystem, matching the psyche's own layout. Draft: `proposals/mind.md`. Vision: `mind.md`.
- **curriculum-nexus** — reads vision subjects and generates deterministic-named skill files (Core body, Rationale, Extended, Experimental, UndecidedProposal, plus raw records / open questions in the source). Draft signal vocabulary: `proposals/signal-curriculum.md`. Codex design brief queued at `01a0acb8-…`.
- **messenger-nexus** (implied, not drafted) — the ordinary/express-lane message channel from flows up to the living, and the mirror-in from the living down to peers.

Cites: `transcriptNexus.md`, `mind.md`, `visionAsSkillSource.md`, `skillKindsTaxonomy.md`, `messagingUp.md`.
Skill proposals: `proposals/nexus-porting-addition.md` (into the `nexus` skill).

## Flow anatomy

A flow's harness system prompt has a shared layer and a role block. The shared layer is identical across flow types (harness base + project instructions + skills index + environment). The role block, appended by the launch package, carries role name, effort tier, stack, layer, authority scope, peer sessions, ad hoc skill body inline, and the Curriculum skills the role always loads. The role block is what varies between flow types.

Cites: `flowAnatomy.md`.
Skill proposal: `proposals/flow-anatomy.md`.

## Refresh purpose and presentation

A psyche flow's turn produces a middle-layer package (flowcharts, visuals, concepts, relations, new-nexus anatomy, open questions). Two hooks: **Report** to the living, **PromptUp** to a higher thinking power.

Presentation is its own main flow, not a subflow. Low-power by default. It writes the report in Markdown and dispatches visualization subflows for figures. Each visualization subflow receives, as one inline datom: a pointer to the source block (via `transcript-nexus Block`), the anatomy, the ethos, and one sentence of intent. Do not inline figure content in the subflow's prompt when a pointer will do.

Visualisation is *highlighted whole view*, not diff-only: the reader sees the entire document with additions, removals, and rephrasings marked inline.

Cites: `refreshPurpose.md`, `presentationFlow.md`, `visualDiffAndLeanComments.md`, `pocShapeConfirmed.md`.
Skill proposals: `proposals/presentation-flow.md`.

## Vision-to-spirit upgrade pipeline

1. **Reports** — a flow's session output.
2. **Distilled vision** — each report becomes a proposal against the vision.
3. **Skills** — the Curriculum-nexus generates the deterministic-named files.
4. **Intent** — some vision items promote to intent; intent enters the system prompt.
5. **Spirit** — some intent (or its ground) promotes to spirit; spirit is accentuated in the system prompt.

Each promotion carries a psyche citation. The living authorizes past intent.

Cites: `highPowerAndUpgradePipeline.md`, `skillPromotionAndLayering.md`.

## Skill kinds — two axes

**Derivative axis** (sections within one subject): Core · Rationale · Extended · Experimental · UndecidedProposal · RawRecords · OpenQuestions.

**Source axis** (which layer produced the content): Vision-derived (design) · Mind-derived (fact) · Usage (tool language).

The two axes are orthogonal. A single skill file is one derivative kind of one subject drawn from one source layer.

Cites: `skillKindsTaxonomy.md`, `skillSourceKinds.md`, `skillPromotionAndLayering.md`.

## Migration

Every composed Curriculum skill (44 of them) becomes a vision entry automatically. Harness-default skills do not migrate — they belong to their harnesses. Mind- and usage-appropriate entries move later; for now everything is vision.

The Curriculum-nexus, once running, regenerates the skill files from vision subjects. Today's `Curriculum/skills/*.md` become generated evidence when that happens.

Cites: `skillSourceKinds.md`, `visionAsSkillSource.md`.

## Conformance

The same source vision drives a per-harness conformance check against the stock system prompt (Claude Code base + injected middle; Codex base instructions; open-source once landed). Where the stock contradicts a standing Intent or Spirit, change the stock via the harness's replacement mechanism and log the change against its citation. A per-harness log carries `{ date  changed  reason  vision-citation  commit-hash }`.

Cites: `highPowerAndUpgradePipeline.md`.

## Subagents

The `visual-report-from-md` subagent is proven: it takes one Markdown file path, publishes one Claude Artifact, returns a small JSON receipt (tested at commit `ad36526b`; artifact `e31893f6-…`).

Curriculum's authored surface (`skills/*.md` + `roles.datom`) has no slot for specialty subagents; the six generated `.claude/agents/*.md` cover only the permission×depth matrix. Interim: authored source at `Curriculum/skills/visual-report-from-md.md` at `a6c0d66` with a `kind: subagent` marker; runtime does not yet honour it. Rethink pending — this is a design gap.

Cites: `curriculumSubagentGap.md`.
Runtime file: `.claude/agents/visual-report-from-md.md` on `flow/48cff7`.

## Repo conformance checklist

A ten-item draft checklist for any repo this flow enters: nexus shape, wire types in Ethos, datom at boundaries, README currency, skill coverage, Curriculum reference, attribution & psyche citation, generated-tree hygiene, artefact locations, round-trip tests. Non-conformance protocol: cite psyche, ask designer or escalate, modernize, record citation in commit.

Cites: `repoChecklist.md`.

## Dispatches in flight

- **Codex `d9961c` · thread `01a0aacb-…`**
  - Msg `01a0ac70-…` — transcript-nexus design brief (ontology-first pass).
  - Msg `01a0acb8-…` — signal-curriculum design brief (ontology-first pass).
  - No return signal has reached this flow. Feedback path (peer → this session) is the routing gap `G06` on the earlier map.

## Artifacts published

- `https://claude.ai/code/artifact/d3e552bf-…` — 13-slide vision book of this flow's material (Sonnet 5 subagent). Thread `69c83ec9` resolved: model ontology corrected in `harnessModelOntology.md` and reply posted.
- `https://claude.ai/code/artifact/e31893f6-…` — mind proposal visualisation (Sonnet 5 subagent test of the `visual-report-from-md` concept). Thread `6bab0b72`: folder-per-variant interim added to `mind.md` and reply posted.

## Skill proposals landed (`flows/48cff7/proposals/`)

New skills — psyche-main-flow · mind · flow-role-separation · flow-anatomy · psyche-pair · transcript-nexus · presentation-flow.
Additions — psyche-distillation-addition (into `psyche`) · nexus-porting-addition (into `nexus`).
Ethos wire draft — signal-curriculum.
Subagent authored source — `Curriculum/skills/visual-report-from-md.md` at `a6c0d66`.

## Open questions the living must settle before the next promotion pass

1. Which of the current 44 Curriculum skills classify as *usage* today vs vision or mind.
2. Whether `mind` and `curriculum` are one Nexus (unified with a `SourceLayer` variant) or two peer Nexuses.
3. The pair mapping — Fable↔Astra is settled; Sonnet↔Terra is likely; Sol and Luna's pair partners on the Claude side are undecided.
4. Whether the mind's interim shape is folder-per-subject-file or one file per variant.
5. What "higher stratum" means at escalation past the top tier — top stratum, core layer, or core-then-top.
6. Section boundaries in a vision file — Markdown headings named by kind, HTML-comment markers, or a datom preamble.
7. Whether `-experimental` and `-undecided-proposal` are one kind with a status field or two.
8. Whether the lean comment envelope is harness-side (rewrite before delivery) or subflow-side (a `comment-decoder`).
9. Whether the conformance log lives per-harness in the harness repo, in Curriculum, or in a top-level `Conformance/`.
10. Where the concept subagent's runtime `.claude/agents/*.md` files should live per flow until Curriculum handles them.

## Recommended overnight-pass plan

1. **Living reviews this proposal end-to-end** — accept, edit, or reject each numbered open question.
2. **Living authorizes the Codex work to progress past step 1 (ontology) into step 2 (bodies)** for whichever Nexus is going first.
3. **A dedicated migration flow** — dispatched by the living — moves the 44 Curriculum skills into vision entries under `Vision/`, one topic each, following the skillSourceKinds classification.
4. **The Curriculum-nexus, once bodies exist,** regenerates the skill tree from vision subjects. Old `Curriculum/skills/*.md` become generated evidence and can be deleted from the authored surface.
5. **A conformance flow** — dispatched by the living — runs the per-harness check and lands the first conformance log.
6. **A new psyche-main-flow session** — started by the living via `/main-flow` or its equivalent, with this `full-proposal.md` as its middle-layer refresh package. The proposed `psyche-main-flow` skill (`flows/48cff7/proposals/psyche-main-flow.md`) governs its behaviour.

## On self-refresh

This flow cannot literally reset its own middle stratum. The harness owns that. What this flow *can* do is produce the refresh package (this document) so a successor psyche-main-flow session on `/main-flow` inherits it. Point that successor at:

- Branch `flow/48cff7` on origin, tip commit at handoff.
- This full-proposal file: `flows/48cff7/reports/full-proposal.md`.
- The psyche-main-flow skill proposal: `flows/48cff7/proposals/psyche-main-flow.md`.

The successor loads the vision entries in `flows/48cff7/vision/` and the proposals in `flows/48cff7/proposals/` as its opening middle-layer content, then continues.
