# Layer 3 — NOTA describes itself: the delimiter type + extension headroom

> **Partially corrected — see `reports/designer/624-audit-of-report-623-self-hosting-macros.md`.**
> The delimiter facts in this file audit as TRUE (the table, `PipeText`, the two
> unassigned piped variants). The framing is what's off: schema-ing NOTA's
> delimiter set is presented as a future foundation, but `MacroDelimiter` is
> **already** a closed enum in code *and* already declared as schema —
> `schema-next/schemas/core.schema:22` has
> `MacroDelimiter [SquareBracket Brace Parenthesis PipeParenthesis PipeBrace]`.
> So "the notation describing itself" is further along than this note implies;
> the genuine open frontier is generating the macro-table *type* from schema, not
> the delimiter type. Facts: reliable. Framing: see 624.

The deepest layer of the self-describing closure, and the foundation under
layers 1–2. Grounded against nota-next source (verified). Spirit `j9du`.

## NOTA's delimiter set is already a closed enum (verified)

`nota-next/src/macros.rs:42` (`MacroDelimiter`) and `src/parser.rs` enumerate the
delimiters NOTA recognizes:

| Glyph | Name | Status |
|---|---|---|
| `( … )` | `Parenthesis` | base — typed records / applications |
| `[ … ]` | `SquareBracket` | base — sequences / enum bodies |
| `{ … }` | `Brace` | base — records with named fields |
| `[\| … \|]` | `PipeText` | **in use** — bracket-safe / multiline strings |
| `(\| … \|)` | `PipeParenthesis` | **exists, no assigned meaning** |
| `{\| … \|}` | `PipeBrace` | **exists, no assigned meaning** |

So the psyche's model is exactly the implementation: three base pairs, each with
a piped variant; `[\|…\|]` is the one NOTA already spends (on strings); the other
two piped delimiters are recognized by the lexer but carry no semantics.

## The closure

The self-describing arc completes here:

1. schema describes the **contracts** (each component's signal/sema/nexus) —
   already true;
2. schema describes the **structural macro nodes** that decode NOTA — the
   `t85k` epiphany (note `2-…`);
3. schema describes **NOTA itself** — its delimiter set is already a closed enum;
   schema-ing it makes the notation self-hosting.

The notation describes itself, top to bottom. The base decoder is a small
hand-written bootstrap; everything above it — contracts, macros, and NOTA's own
grammar — is data.

## Extension-language headroom

The two unassigned piped delimiters, `(\|…\|)` and `{\|…\|}`, are **reserved
extension points**: base NOTA leaves them open for *extended NOTA languages*
(schema is one) to give them meaning. So an extension built on NOTA gets two
fresh structural delimiters to claim, without touching the base grammar. This is
the layering: base NOTA → extended NOTA languages that assign the free piped
delimiters.

## This reframes the `<>` question (note `2-…`)

Last note flagged: do generics need a new `<>` delimiter? The headroom answer:
probably **not a brand-new pair** — if a generic-parameter structure earns a
distinct delimiter, schema (as an extended NOTA language) can claim one of the
two reserved piped delimiters (`(\|…\|)` or `{\|…\|}`) for it, rather than
introducing `<>` and a fourth base pair. *"Delimiters earn their place"* is
satisfied by spending reserved headroom, not minting new syntax. Whether
generics want a distinct delimiter at all (versus staying bare in the head) is
still the open call — but if they do, the slot already exists.

## Open

- **The bootstrap core.** Schema-ing NOTA still needs the minimal hand-written
  decoder that reads the definition language — the irreducible seed. Naming it is
  the first concrete task (shared with note `2-…`).
- **Does `PipeParenthesis` / `PipeBrace` get a NOTA-level meaning or stay purely
  extension-reserved?** The psyche's lean is the latter (reserved for
  extensions); confirm before any base-grammar use.
</content>
