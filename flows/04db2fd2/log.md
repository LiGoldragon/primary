# Flow 04db2fd2 — design

## About
Review the anatomy of the Datom textualize/realize logic, in awareness of
flows 01a04339, b675f3d9, ac1e9ec8 and all psyche around protos and datom.

## Remembered
Remembered: 01a04339, b675f3d9, ac1e9ec8 — depth 1 (reports/rememberedFlows.md)
- 01a04339: psyche's provisional ruling that the empty observation reply textualizes as `Observed.Locks.[]` ("good enough for now"); last response was a read-only impact audit of every site that must move from Debug to Datom output. Open: realize and prove the reply contract; nonempty payload rendering unsettled.
- b675f3d9: kind-declaration syntax, capability anatomy, structural parsing (arity discriminates types; head delimiters carry bearer mode; `<>` is a real Protos delimiter); proposed Vision/protos.md (new, carrying Realize/Textualize vocabulary), Vision/datom.md revision, Vision/ethos.md additions — all awaiting approval. Last response: five suspected vision impurities put to the psyche, awaiting ruling.
- ac1e9ec8: full datom-syntax acquisition; Vision/datom.md corrected (curly quotes default string delimiter, parentheses reserved for Meaning, datom is signal's edge form). Witnessed four divergences of code from vision (root wrapping, Map head, parentheses for strings, curly quotes not default). Datom skill never started.
- Current state: no datom/protos/ethos authored skill exists; Vision/protos.md exists only as proposal; Realize/Textualize vocabulary lives only in that unapproved proposal.

## Settled
(none yet)

## Witnessed
- witnesses/datomTextualizeRealizeAnatomy.md (code read): two crates, protos v0.8.0 (Shape, Block, BlockScanner lexer, StructuralWalk / RealizeWalk / TextualizeWalk, scoped handles) and datom v0.5.0 (single datom.rs, DatomRealizing / DatomTextualizing / DatomRoot / DatomHeadedUnit / DatomText<T>). Textualize is flat, single-space, no newlines or indentation. Realize is two-pass: BlockScanner lexing, then RealizeScope::realize_body dispatch. Oddities: delimiter mapping in three places; Block has its own Textualize impl; bare/key validation re-parses through the scanner; ethos-monolith emits Datom impls as string-concatenated Rust.

## Reports
- reports/protosDatomPsyche.md — verbatim catalogue of all psyche on protos/datom/textualize/realize; two active conflicts in Vision/datom.md (string delimiter, map syntax) superseded by 2026-08-26 rulings; ten unknowns.
- reports/textualizeRealizeAnatomyReview.md — the anatomy set against the psyche: six agreements, eight odd fits, central open question.

## Settled
- The anatomy agrees with the psyche on: traits in protos; one frame discipline both ways; context-driven dispatch; top-level textual-realizes / real-textualizes; curly-default strings; guillemet maps; bare-when-fits.

## Open
- Central question for the psyche: below the root, the real type carries both seams (DatomRealizing on the real type, taking an untyped Block). Is a typed textual block wanted between Block and the real type ("define the block … ontology of source code")?
- Delimiter knowledge in three places; Block's second textualize path outside the walk; bare-safety by re-parse.
- Unruled: fallibility of textualize below the top; layout of nonempty/nested output; `<>` in datom vs `<<>>`.
- Distillation debt: Vision/datom.md stale on strings and maps; protos.md proposal unapproved (b675f3d9, ac1e9ec8).
