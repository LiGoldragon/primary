# 0 — Frame and Method

*Kind: meta-report frame · Topics: design-audit, reusable-planes, boilerplate-elimination, layering, operator-work-audit · 2026-05-31 · designer lane*

## What's being audited

Operator's work across the schema/NOTA stack as of 2026-05-31. Four repositories under active development:

- `nota-next` — universal NOTA codec + macro-node registry + Block primitives
- `schema-next` — schema vocabulary, asschema, macros, AsschemaStore
- `schema-rust-next` — Rust emission machinery
- `spirit-next` — the integrated runtime (Signal/Nexus/SEMA + CLI + daemon)

## The lens (from the psyche directive)

> "audit operator's work - look for broad possible design improvements - to make good logical planes that are re-usable, eliminating almost all boilerplate code is a good indication"

Two metrics to optimize:

1. **Reusable logical planes.** Each layer should own one responsibility; abstractions should compose. The four-object separation from Spirit 1272 (Asschema + AsschemaArtifact + AsschemaStore + RustEmitter) is the model: each object owns one thing, derives + macro-nodes do the work.
2. **Boilerplate elimination.** When the same pattern appears twice, the substrate is missing an abstraction. Spirit 1278 named the recent anti-pattern (`Asschema::to_nota` as a hand-rolled `[...].join("\n")`); this audit looks for the OTHER places where consumers are hand-rolling what the substrate should expose.

## Method — four parallel sub-agent audits

Each sub-agent reads its repo's live code (not just reports) and writes a focused audit. The sub-agent prompts share a common shape: identify repeated patterns, flag hand-rolled glue, find layering violations, name the top three broad improvements ordered by impact.

| Sub-agent | Repo | Focus |
|---|---|---|
| 1 | nota-next | codec + macro-node + Block primitives — the universal substrate; what abstractions should be lifted here for consumers? |
| 2 | schema-next | schema lowering, asschema, macro mechanisms, codec implementations — what's hand-rolled because nota-next doesn't expose it? what's repeated within schema-next? |
| 3 | schema-rust-next | Rust emission machinery — where does string concatenation hide a missing data model? |
| 4 | spirit-next | integrated runtime — what's boilerplate that schema-emission could simplify? |

The synthesis (`5-overview.md`) names the top broad design improvements across the stack, ordered by impact × scope, and identifies cross-cutting patterns the per-repo audits surface.

## What "broad" means here

This is NOT a checklist of small fixes. The audit looks for:

- **Substrate gaps** — consumers hand-rolling code because the substrate doesn't expose the right surface (Spirit 1278 is the canonical example)
- **Layering violations** — code in the wrong layer because the layer below doesn't reach high enough
- **Missing abstractions** — patterns repeated in three+ places that haven't yet been lifted
- **Cross-cutting reuse** — abstractions in one repo that should be available to all four
- **The Stage 5 horizon** — designs that won't survive when `core.asschema` emits its own Rust nouns

Small style nits (naming, formatting, missing tests) are out of scope unless they signal a deeper design issue.

## What the sub-agents will NOT do

- Write or edit code (audit-only)
- Dispatch their own sub-agents (one level only)
- Recommend specific refactors at the line-level (operator's lane)
- Comment on intent capture quality (covered separately by recent designer reports)

## Output format

```
reports/designer/443-design-improvements-audit-2026-05-31/
├── 0-frame-and-method.md        (this file)
├── 1-nota-next-audit.md          (sub-agent 1 output)
├── 2-schema-next-audit.md        (sub-agent 2 output)
├── 3-schema-rust-next-audit.md   (sub-agent 3 output)
├── 4-spirit-next-audit.md        (sub-agent 4 output)
└── 5-overview.md                 (synthesis — top broad improvements + cross-cutting patterns)
```

Per AGENTS.md `reports/<role>/<N>-<session-name>/` meta-report directory pattern — the directory IS the meta-report, garbage-collected as one session unit.

## Success criteria for the synthesis

The synthesis succeeds if it names **3-5 broad design improvements** that would each remove 100+ lines of boilerplate when implemented. Below that bar, the audit is finding nits; above it, the improvements are speculative. The right grain: large enough to matter, concrete enough to act on.
