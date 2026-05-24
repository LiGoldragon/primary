# Frame and method — MVP advance + fix dispatch

*Per psyche directive (2026-05-24): "create your own critique or
advancement of the design in your reports. You can use subagents
to look at different angles and find the parts that you think
need clarification in what I enunciated as a design and what's
being implemented. Also, have an agent audit that because you
have an operator, so you can use the operator to go and edit
things which you know should be fixed right now for the migration
to go through." Intents captured: 412 (subagent authorization),
413 (cross-lane operator authority for MVP fixes), 414 (MVP
active phase).*

## 1 · What this meta-directory contains

A coordinated multi-subagent session targeted at the MVP
schema-language pilot work — the live workspace migration
captured by `primary-ezqx.1` (MVP schema-language pilot for
Spirit) per designer report /323 (latest scope authority).

Five sub-reports:

- `1-mvp-scope-clarification.md` (Subagent A) — read /320 + /321
  + /322 + /323; build MVP scope matrix; find ambiguities about
  spirit 396 (macro emits wire + sema + sema-lowering); produce
  open psyche questions.
- `2-macro-implementation-gap.md` (Subagent B) — read
  signal-frame-macros source; compare against /323 + intent
  records 397-408; produce file:line gap matrix for operator
  pickup.
- `3-design-clarifications-needed.md` (Subagent C) — read /164
  (my schema language v3) + intent 397-408 + /320-/323; find
  places where psyche-stated design and current design reports
  disagree or carry ambiguity; produce ordered open-question
  list with recommended leans.
- `4-operator-fixes-executed.md` (Subagent D — operator role)
  — execute the high-confidence mechanical fixes per intent 413:
  bracket-string sweep of /164's schema examples (intent 401),
  terminology pass on /163 (Tier 1 → short header per intent
  388), sema-engine ARCH dep-name fix (per /163 §8), and any
  other low-risk MVP-migration fixes identified in scope.
- `5-audit-of-findings.md` (Subagent E — auditor) — review A,
  B, C, D for contradictions, missed angles, operator-introduced
  issues, and unresolved clarifications.

Then `6-overview.md` (this orchestrator's synthesis).

## 2 · Wave coordination

```
Wave 1 — parallel:    A, B, C (research) + D (operator)
Wave 2 — sequential:  E (auditor; depends on Wave 1 outputs)
Wave 3 — sequential:  6-overview.md (my synthesis)
```

Subagents A, B, C are read-only research; D writes code/text
changes. All four run in parallel; D's edits don't depend on
A/B/C's findings (the operator scope is the already-known
fixes from /166 §9). E waits for all four.

## 3 · Authority basis

- Intent 412 (Maximum, 2026-05-24): second-designer dispatches
  subagents during MVP phase.
- Intent 413 (Maximum, 2026-05-24): cross-lane operator
  authority for MVP-blocking fixes.
- Intent 414 (Maximum, 2026-05-24): MVP is the active phase.
- Intent 403 (Maximum, 2026-05-24): counter-ego role — extended
  per 412 from doubt/critic into active advancement.

## 4 · Coordination with parallel audits

Two parallel external audits landed before this session:

- `reports/nota-designer/6-quoted-string-purge-audit-2026-05-24.md`
  — workspace bracket-string sweep; my reports are scope of
  `primary-36iq.7.1`. Subagent D's bracket-string fix is
  partial absorption of this scope.
- `reports/second-operator/176-designer-awareness-beads-and-report-audit-2026-05-24.md`
  — operator-side audit; identifies /323 as latest MVP scope
  authority and surfaces the /320/321/322/323 sema-lowering
  ambiguity. Subagent A picks up this thread.

Subagent E should cross-check this directory's findings
against both parallel audits.

## 5 · Deliverable shape

Each sub-report uses bracket-string NOTA per intent 401 (this
is forward-looking work; no inherited quote violations to
preserve). Mermaid diagrams allowed. Cite spirit records by
number + brief description. Cite designer reports by path.
Cite beads with inline description per AGENTS.md hard override.

## 6 · This frame's intent base

- Spirit records 388-408 (the macro/schema/short-header cluster).
- Designer reports /320 (pilot unblock), /321 (visual state),
  /322 (Spirit positional-schema worked example), /323 (MVP
  scope expansion).
- Second-designer reports /163 (signal-sema interaction), /164
  (schema language v3), /165 (counter-ego audit), /166
  (self-audit).
- Bead `primary-ezqx.1` (MVP schema-language pilot for Spirit).
- Parallel audits: nota-designer/6, second-operator/176.
