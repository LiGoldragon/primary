Archived 2026-08-23 by flow 68512643; distilled into Vision/datom.md.
## 2026-08-22 — no derive for cli config: datom creates configuration options by its very shape; a data enum at the root (main operation) with options in its data

Design session `bc05da32`, typed (captured 2026-08-22), answering the
Designer's proposed datom-config derive crate for the program input
and the argv-derive family (clap derive, argh) it was modeled on:

> there is no production lexer yet, its still in development.

> and I dont think we need a derive on a datom type for what we want.
> its simpler than that; datom creates configuration options by its
> very shape, as the ethos interface shows; a data enum at the root
> (main operation) with options in its data

Context (agent-authored, separate from the psyche's words): the
datom-config derive idea is dead. The program's configuration
surface is the datom's shape as the ethos interface declares it —
the root data enum's variants are the main operations, each
variant's data its options; nothing generates a UI because the
shape already is one. Extends the 2026-08-07 root-enumerator ruling
above. The first line answers the Designer's "realize it through
the project's datom parser": the parser is still in development —
the design is written ahead of what can run, per
worldModelBeforeCode.md 2026-08-21.
