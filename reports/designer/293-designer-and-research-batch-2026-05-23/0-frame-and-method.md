# 0 - Frame and method — designer and research batch 2026-05-23

*Meta-report directory per spirit record 231 (sub-agent session shape).
Orchestrator: prime designer. Per psyche directive 2026-05-23 ("take on
the designer and research work with subagents") four parallel subagents
were dispatched to cover the designer-lane + library-research work
filed as beads against /292 outcomes.*

## Scope of this session

Four parallel subagents, each producing one numbered report file in
this directory:

- **Subagent A — Vocabulary sweep + skill** — produces `1-vocabulary-sweep.md`.
  Lands `skills/workspace-vocabulary.md` (new canonical glossary
  reference); sweeps ARCH + designer reports for main/next, Persona
  naming, engine→engine_manager rename per settled spirit records 181,
  215/216, 199/240. Drives bead `primary-3t67`.

- **Subagent B — `unitbus` research** — produces `2-unitbus-research.md`.
  Evaluates `lvillis/unitbus` (purpose-built Rust SDK for systemd
  transient units over D-Bus) vs hand-rolled `zbus` for the
  `SystemdTransientUnitLauncher` backend per record 240 + bead
  `primary-a5hu.4`. Drives bead `primary-lm9o`.

- **Subagent C — `kameo` 0.16 Scheduler research** — produces
  `3-kameo-0_16-research.md`. Evaluates `kameo` 0.16's new `Scheduler`
  actor for handover drain timeouts, subscription keep-alive, persona
  reachability probes. Drives bead `primary-e4oq`.

- **Subagent D — `rkyv` 0.7→0.8 audit** — produces `4-rkyv-0_7-to-0_8-audit.md`.
  Workspace audit of rkyv 0.7→0.8 upgrade cost across signal-*,
  sema-engine, persona-spirit, etc. Drives bead `primary-haa3`.

The orchestrator (prime designer) synthesizes results in
`5-overview.md` after subagent return.

## Why parallel

Per the designer-protocol parallel-subagent authorization (psyche
2026-05-21) + record 220 chat normal-response policy + record 231
meta-report directory pattern — independent research and designer
substance is the canonical parallel-subagent shape. Each subagent's
work is bounded; no cross-subagent dependencies in this batch.

## Substance map

Each subagent received:

- Their specific bead's full description (as filed via `bd` in the
  prior round)
- The relevant spirit records cited in /292 §3.5 + per their topic
- /292 itself for the broader designer-lane context
- Skill files relevant to their topic (`skills/architecture-editor.md`
  for designer; `skills/mermaid.md` for visuals)
- Constraint: write into this directory only, no other workspace
  edits except for Subagent A (who does the vocab sweep + skill
  write per `primary-3t67` scope)

## Expected outputs

`1-vocabulary-sweep.md`: designer report covering the sweep diff +
   skill file landing + remaining items.

`2-unitbus-research.md`: research findings on `unitbus` API surface,
   maintenance posture, comparison to hand-rolled zbus + recommendation
   for primary-a5hu.4 implementer.

`3-kameo-0_16-research.md`: research findings on `kameo` 0.16
   `Scheduler` API + prototype suggestions for the three named use
   cases (handover drain timeouts, subscription keep-alive, reachability
   probes) + adoption recommendation.

`4-rkyv-0_7-to-0_8-audit.md`: per-crate inventory of rkyv usage +
   upgrade-effort estimate + recommendation on timing.

`5-overview.md`: orchestrator synthesis — what landed, what's
   actionable, recommended next steps.

## See also

- `/home/li/primary/reports/designer/292-designer-lane-top-issues-2026-05-22.md` — the source /292 that generated these beads + research questions
- Spirit records 231 (meta-report directory pattern), 248 (primary-a5hu decomposition), 249 (vocabulary sweep + skill), 250 (research beads disposition)
- Beads: `primary-3t67`, `primary-lm9o`, `primary-e4oq`, `primary-haa3`
