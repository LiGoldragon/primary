# 65 — nota-codec entanglement meta-investigation (frame + method)

Kind: meta-report directory (frame + angle sub-agents + orchestrator psyche report).
Topics: nota-codec, bracket-strings, hand-rolled-parsers, sema-engine, version-pin, dependency-graph, migration, meta-investigation.
Date: 2026-06-04.
Role: system-designer (orchestrator).

## Psyche directive

The psyche asked for a full, detailed psyche report with full context on the
nota-codec entanglement (open-item #4): understand it properly, find a real
solution, and cover everything it touches / everything related. Explicitly:
"Let's make this a meta-investigation."

The triggering finding: porting `chroma` to `sema-engine` (the boundary
cleanup) was blocked because adding `sema-engine` pulls
`sema-engine → signal-sema → signal-frame → schema-rust → schema`, which
requires a NEWER `nota-codec` (`NotaMapEntry`/`NotaRecordShape`), while
`chroma`'s hand-rolled `config.rs` parser requires the REMOVED old `nota-codec`
`Token::Str`/quoted-string lexer. Cargo unifies `nota-codec` to one version, so
the two collide. `chroma` only builds today because its stale `Cargo.lock`
pins old `nota-codec`. Tracked: bead `primary-n1ao`.

## Intent Anchors

[NOTA strings come EXCLUSIVELY from bracket forms; quotation marks do not form string types; the nota-codec encoder structurally cannot emit a quote; legacy quoted-string input is accepted only as migration and is authorised for removal once emitters migrate.] (AGENTS.md hard override / nota-design discipline)

[No hand-rolled parsers — parsing goes through the NOTA codec / NotaDecode derive surface, not bespoke lexers.] (skills/rust/parsers.md discipline)

[Sema-engine is the exclusive interface to the database; the boundary cleanup is what surfaced this entanglement.] (Spirit 2563 Correction High)

[Components that bypass the kernel with raw redb on the stale cohort are pinned to old nota-codec; adopting current sema-engine forces nota-codec forward and breaks their stale hand-rolled parsers.] (system-designer 63 finding; chroma report, bead primary-n1ao)

## Method

Four angle sub-agents, each writing a numbered report into this directory and
returning structured findings; the orchestrator then writes the psyche-report
synthesis as the highest-numbered file.

| File | Angle |
|---|---|
| `1-version-delta-and-dependency-graph.md` | Old vs current `nota-codec`: the exact API/behavior delta (Token::Str/quoted-string removal; NotaMapEntry/NotaRecordShape additions; bracket-only strings) and the full dependency graph showing where the version requirements collide. The mechanics of the conflict. |
| `2-blast-radius-stale-parser-cohort.md` | Every active component/crate with a hand-rolled NOTA parser and/or an old-`nota-codec` pin (chroma config.rs is the seed; search the active repos for `Token::Str`, bespoke `Lexer`, quoted-string handling, stale pins). Per-component: what breaks when nota-codec moves forward, the migration need, rough effort. The true scope. |
| `3-conceptual-root-and-related.md` | WHY this happened and what it connects to: the quotation-mark→bracket-string NOTA discipline (why Token::Str was removed), the no-hand-rolled-parsers rule and the NotaDecode/derive surface as the intended path, and how the entanglement ties into the sema-engine boundary cleanup, the redb-2 cohort, the schema stack, and the two-deploy-stacks. Other latent instances of the same shape. |
| `4-solution-and-sequencing.md` | The proper fix: migrate bespoke parsers onto the NotaDecode/Decoder derive surface; unify nota-codec across the stack; compat-shim vs pure-migration; the recommended ordered sequence and its relationship to the sema-engine adoption. Concrete plan. |

## Discipline for the angle agents

- Read-only investigation; write ONE numbered report; do not edit source, do
  not commit. Verify line numbers against current source before citing.
- Cite intent as bracket-quoted summaries (the short id is the address).
- Honesty about state over fidelity to brief; report what is actually there.
- NOTA discipline if quoting NOTA: bracket-form strings only.

## Lane coordination

This is the designer-side investigation. The chroma config migration is beaded
`primary-n1ao`; the broader sema-engine boundary cleanup is `primary-y0ec`;
the strict-engine-separation cutover is `reports/designer/501-...`. This
investigation feeds the operator's sequencing decision, it does not pre-empt
the owning lanes' implementation.
