# 0 — Frame and Method

*Kind: meta-report frame · Topics: stack-vision, canonical-presentation, agglomeration, graph-size-cap, signatures-and-nota-syntax · 2026-05-31 · designer lane*

## What the psyche asked for

> "Present me your latest best understanding of what I intend to create with the most important parts of the code, and at least the signatures and the syntax, the nota syntax of everything, the data type equivalence, and how everything is parsed and all of the logic that I emphasized shown, and the graphs not having too many nodes. I also want you to change the scale for that. The graph should have only a few nodes so that we can still read them ... use more graphs to break it down into parts ... You can agglomerate all the old reports into this new representation of the vision, and then delete all the old ones and make your best presentation. Make several reports. Use sub-agents."

## What this meta-report is

A canonical re-presentation of the schema/NOTA stack vision after the recent operator work landed. Four focused body reports plus this frame and the closing overview synthesis. Old superseded vision reports are retired with landing evidence in the synthesis; their content is agglomerated into the new presentation.

## State of the stack at 2026-05-31 (after recent operator work)

Material that has landed since the older vision reports were written:

- **nota-next** — `14ad2f8` (known-root body codec) + `05c91c8` (docs) + `b041e64` (derive known-root bodies + nested macro constraints) + `3f46c2e` (expose delimiter substrate + recursive macro patterns). The substrate gaps named in designer 442 + designer 443 sub-agent 1 are CLOSED for known-root and Delimiter; nested macro constraints close part of sub-agent 1 Finding 2.
- **schema-next** — `57bab60` (derive asschema known-root document codec) + `62d78bc` (use nota document body codec). The anti-pattern from designer 442 is FIXED — Asschema's `to_nota` and `from_nota_document_fields` are derive-driven; no more `[...].join("\n")` hand-roll.
- **schema-rust-next** — `c733a0d` (repin known-root schema stack)
- **spirit-next** — `c4bf4d7` (repin known-root schema stack)

The four-object separation (Asschema + AsschemaArtifact + AsschemaStore + RustEmitter) is fully realized in main. The data flow Rust ↔ NOTA ↔ rkyv ↔ sema is derive-driven end-to-end. Macro nodes at the NOTA layer with recursive structural constraints are live. The runtime triad (Signal → Nexus → SEMA) operates on schema-emitted types.

## The four body reports

| File | Topic | Lens |
|---|---|---|
| `1-four-logical-planes.md` | The four typed objects (Asschema + Artifact + Store + Emitter) | Per Spirit 1272 — what each plane owns; how they compose; the generic substrate horizon |
| `2-data-model.md` | Rust types + NOTA syntax + rkyv equivalence | Per Spirit 1270 + 1271 — each major type shown across all three representations |
| `3-nota-parsing-and-structural-macros.md` | Two-layer parsing + macro nodes + known-root codec | Per Spirit 1263 + 1278 + 1279 + 1280 — structural matching, ordered patterns, no-match-as-error |
| `4-runtime-integration.md` | Schema → Rust → CLI/daemon → Signal/Nexus/SEMA | Per Spirit 1244 + 1272 — schema-emitted types ARE the runtime nouns; the CLI/daemon split; the schema-core horizon |

The synthesis (`5-overview.md`) ties them together and names the agglomeration evidence (which old reports get retired into which new sections).

## Graph-size discipline (hard cap)

The psyche named the graph-size issue explicitly. Hard cap for every mermaid graph in this meta-report:

- **Maximum 5 nodes per graph** (6 only if absolutely necessary).
- **Use multiple graphs** to break down complex flows into small pieces.
- **Each graph emphasizes one specific transition** — type to type, layer to layer, plane to plane.
- **No graph with more than 5 nodes** can have small unreadable text by definition; this discipline forces every graph to stay legible.

When a flow would need more nodes, split it across two graphs with a shared anchor node (e.g., "Asschema" appears as the final node of graph 1 and the first node of graph 2).

## Content discipline

Each body report must show:

1. **Code signatures** — the Rust type declarations with their derives, organized so the reader sees the data model in one block.
2. **NOTA syntax** — the text projection of each type, with concrete examples that match live code in `schemas/core.asschema` or test fixtures.
3. **Data type equivalence** — explicit demonstration that Rust ↔ NOTA ↔ rkyv ↔ sema are projections of the same value; the derives are the proof.
4. **Parsing logic** — how documents become typed objects (and back); which derives carry which corner-to-corner edge.
5. **The logic the psyche emphasized** — strict-brace key-value (1259), macro nodes at NOTA layer (1263), notation honesty (1267-1269), three categories (1270), rkyv-in-SEMA (1271), four-object separation (1272), positional reading (1274), input/output as struct fields (1277), known-root abstraction (1278), two-layer structural matching (1279), structural over text macros (1280).

## Retirement policy for old vision reports

The synthesis (`5-overview.md` §"Agglomeration ledger") names which old reports retire with their landing evidence pointing into the new presentation:

- `reports/designer/430-codec-opt-in-research-rkyv-base-nota-on-top.md` → codec opt-in is live (NotaSurface gating per operator 246); content in §4.
- `reports/designer/431-daemon-zero-nota-state-aware-startup-multi-signal.md` → zero-NOTA daemon is live; state-aware startup is a future horizon; content in §4.
- `reports/designer/434-live-assembled-schema-bootstrap-and-loop-closure.md` → asschema-as-artifact is live (Spirit 1246); content in §1.
- `reports/designer/435-vision-for-the-four-remaining-gaps.md` → Gap A/B closed; Gap C/D pending; content in §4 + 5.
- `reports/designer/437-strict-brace-key-value-explanation-and-implementation-try.md` → strict-brace is live (operator 256); content in §2 + §3.
- `reports/designer/438-macro-nodes-at-nota-layer-vision-focused-on-critical-parts.md` → macro nodes live (operator 261 + nota-next 3f46c2e); content in §3.
- `reports/designer/441-asschema-types-rkyv-sema-roundtrip.md` → four-object separation + AsschemaStore live (operator 84ce382); content agglomerated across §1, §2, §4.
- `reports/designer/442-known-root-nota-anti-pattern-and-elegant-path.md` → anti-pattern FIXED (schema-next 57bab60 + nota-next 14ad2f8); content in §3.

Retained (not retired):
- `reports/designer/443-design-improvements-audit-2026-05-31/` — the four-sub-agent audit + ordered backlog; remains actively referenced for the schema-core extraction + remaining boilerplate horizons.
- `reports/designer/351`, `352`, `412`, `415`, `439` — historical intent + maintenance ledgers; not vision reports.

## Sub-agent dispatch

Four sub-agents, one per body report. Each reads the live code in the relevant repos + the old reports being agglomerated + the recent Spirit records. Each writes to its numbered slot in the meta-report directory. The synthesis comes after all four return.

## Success criteria

The new presentation succeeds if a reader unfamiliar with the prior vision reports can pick up this meta-report and understand:

1. What the architecture IS today (signatures + NOTA syntax + live code references)
2. WHY each piece is shaped the way it is (the psyche's emphasized principles)
3. HOW the pieces compose (the four logical planes, the two-layer parser, the four-corner round-trip)
4. WHAT remains (the horizons from designer 443's audit)

Without scrolling through the retired reports. The retired reports go away; the truth lives here.
