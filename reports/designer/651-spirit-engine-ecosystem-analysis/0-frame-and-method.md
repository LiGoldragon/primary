# 651 — Spirit engine: ecosystem + core-dependency analysis (frame)

*The psyche asked for a wide, in-depth analysis of the Spirit engine with its
ecosystem and core dependencies — "which means a schema/nota engine analysis" —
with multi-layer visuals.* Spirit is not a hand-written daemon; it is **emitted
from** the schema/nota engine stack and runs **on** the sema state engine over the
signal-frame/triad runtime. So analysing Spirit *is* analysing that stack. This
meta-report dissects it layer by layer and then re-assembles it visually.

## The reframing

"Analyse Spirit" decomposes into the stack that produces and runs it:

```
            ┌─────────────────────────── apex: the application ──┐
   spirit   │  three planes (Signal/Nexus/SEMA) + guardian + CLI │
            └────────────────────────────────────────────────────┘
                 ▲ emitted-from                    ▲ runs-on
   ┌─────────────┴───────────────┐     ┌───────────┴──────────────┐
   │  schema/nota ENGINE          │     │  state + wire RUNTIME     │
   │  nota-next → schema-next     │     │  sema-engine, signal-frame│
   │  → schema-rust-next          │     │  triad-runtime, signal-*  │
   └──────────────────────────────┘     └───────────────────────────┘
```

The "core dependencies" the psyche names are the left column (the schema/nota
engine that *generates* Spirit) plus the right column (what it *runs on*).

## Method

Parallel deep-readers, one per layer, each reading that layer's `INTENT.md` →
`ARCHITECTURE.md` → key source, then writing a numbered report here with at least
one layer diagram and returning structured findings (role, components, dependency
edges, how Spirit uses it, a mermaid fragment, sharp facts). The orchestrator
(designer) writes this frame and the final synthesis with the cross-cutting
master diagrams. Verified-from-source is marked; inference is flagged.

## Layer map (files in this directory)

| # | Layer | Repos | Face |
|---|---|---|---|
| 1 | NOTA text + the derive seed | `nota-next` | text |
| 2 | Schema / type model + source codec | `schema-next` | type |
| 3 | Rust emission + build driver | `schema-rust-next` | generator |
| 4 | State engine + versioned families | `sema-engine`, `signal-sema` | state/bytes |
| 5 | Wire framing + daemon runtime spine | `signal-frame`, `triad-runtime` | wire |
| 6 | Spirit application: planes, guardian, records | `spirit`, `signal-spirit`, `meta-signal-spirit` | apex |
| 7 | Cartography: dependency DAG, three faces, self-host boundary | (cross-cutting) | map |
| 8 | **Synthesis** — the layered architecture, woven, with master diagrams | (all) | — |

## Verified dependency edges (from Cargo.toml, this session)

- `spirit` → `nota-next` (opt), `rkyv`, `sema-engine`, `signal-frame`,
  `signal-spirit`, `meta-signal-spirit`, `triad-runtime`, `schema-rust-next`
  (build), `schema-next` (build), `signal-sema`.
- `sema-engine` → `rkyv`, `signal-frame`, `signal-sema`. (No schema-next/nota-next
  dependency — it is a pure state engine over rkyv + framing.)
- The schema/nota engine (`nota-next` → `schema-next` → `schema-rust-next`) is a
  **build-time** dependency of Spirit: it generates `src/schema/*.rs`. sema-engine +
  the signal/runtime crates are **runtime** dependencies.
