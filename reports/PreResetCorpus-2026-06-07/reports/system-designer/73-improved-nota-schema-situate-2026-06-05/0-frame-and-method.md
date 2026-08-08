# 73 — Improved NOTA/schema mechanism: situate + implications (frame)

Kind: meta-report directory (frame + gather sub-agents + situate synthesis + completeness critique).
Topics: nota, schema, schema-next, schema-rust-next, structural-macro-node, asschema-removal, schema-pipeline, spirit, record-shape, situate, implications.
Date: 2026-06-05.
Role: system-designer (orchestrator).

## Psyche directive

"Acquire the latest intent and check out some of the latest reports by operator
and designer about the improved nota and schema mechanism, and situate that in
terms of what we were working on previously, and then find all of the things
that this touches on or that now have to be maybe clarified that this new
direction would warrant."

So: (1) acquire latest intent + read the latest operator/designer reports on the
improved NOTA/schema mechanism; (2) situate it against our prior work; (3)
enumerate everything it touches / that now needs clarification.

## The new direction, as already spotted in the scout

- `(Spirit Decision vez8, Maximum)` [Schema is a specialized NOTA dialect built
  on structural macro nodes — NOT a separate language lowered into NOTA; a schema
  file IS full NOTA. Pipeline: authored schema (NOTA) DESERIALIZES via the
  structural-macro-node codec into schema-in-rust (typed rust, rkyv, canonical
  round-trip), which LOWERS into rust interface code. NO separate assemble step —
  ASSCHEMA IS REMOVED; the resolution it performed lives as methods on
  schema-in-rust types.]
- `(Spirit Principle xai7)` [The structural macro node — a NOTA enum decoded by
  SHAPE, not by a data tag; decode is TYPE-DIRECTED, a structural match per
  variant in declaration order.]
- Designer thread: reports 504, 511-525 (notably 519 structural-macro-node-is-a-
  type-derive, 520/522 asschema-removal design+converged-plan, 521 structural-
  derive operator-vs-designer, 523 resolution-is-the-datatypes, 524 the-schema-
  pipeline, 525 intent-maintenance-schema-thread-consolidation, 512 spirit-plane-
  schema-split).
- Operator thread: reports 312-316 (structural-macro-node implementation,
  asschema-removal comparison, structural-derive comparison, schema-pipeline
  feedback).

## What we were working on previously (the situate target)

The system-designer lane was redesigning the Spirit intent record architecture
in the schema-derived spirit pilot (`/git/.../spirit`), reports 71 and 72.
Captured intent: per-kind fields `(3awz)` → realized as a FLAT record after the
psyche's NOTA correction `(m27p)` [privacy is Optional, NOTA None=public]; no
composite type `(22t6)`; relations field is the only code change `(50qy)`;
refresh is agent behavior/skill `(66bd)`; auditor auto-proposes, psyche confirms
retire `(1gwe)`; weight=Magnitude `(515t)`; clean-break pilot `(o7lx)`; short id
min-4 `(tw81)`. The converged shape: a FLAT
`Entry { Topics, Kind, Description, Certainty, Weight, Privacy(Optional),
Relations(Vec<hash>) }` with hash identity (report 64), clean break in the pilot.

CRITICAL LINK: report 72's migration/regeneration mechanism referenced
**asschema headers**, the `build.rs` version literal propagating into
`*.asschema`, and `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` regeneration. If asschema is
removed (`vez8`), that mechanism is outdated and the pilot implementation
approach must be re-grounded on the new pipeline before any build.

Also in flight: lojix should adopt triad+schema `(4sff)`; horizon-rs is a
library "hack" `(4v45)`.

## Method

Four read-only gather sub-agents (barrier), one situate synthesis, one
completeness critique. The orchestrator writes the psyche-facing overview.

| File | Angle |
|---|---|
| `1-latest-intent.md` | Latest Spirit intent on the improved NOTA/schema mechanism, structural macro nodes, asschema removal, the pipeline. The current direction + load-bearing records. |
| `2-designer-thread.md` | Designer reports 504, 511-525: the mechanism, its evolution, the converged plan. |
| `3-operator-thread.md` | Operator reports 306-316: read/feedback/comparison/implementation status; landed vs proposed. |
| `4-source-grounding.md` | The repos (nota / nota-codec, schema, schema-rust-next): is asschema actually removed, are structural macro nodes implemented, what is the actual current pipeline in code. Landed vs proposed. |
| `5-situate-and-implications.md` | Situate the mechanism against our prior work; enumerate EVERYTHING it touches + what now needs clarification. |
| `6-overview.md` | Orchestrator psyche-facing synthesis (incorporates the completeness critique). |

## Discipline

- Gather agents are READ-ONLY; write ONE numbered report; no source edits, no
  commits, no mutating Spirit ops. Verify line/type/record citations.
- Cite intent as bracket-quoted summaries with the short code.
- Honesty about landed-vs-proposed: the mechanism is moving fast; say what is
  actually in source vs what is designed/intended.
- NOTA discipline if quoting: bracket strings only, positional, no quotes.
