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
- Applied: design.md cadence paragraph (rolling distillation) and psyche-distillation.md proactive-dispatch mode — Curriculum 9e114dc6, primary f24a5b1b (that primary commit also swept in this flow's then-dirty log.md and vision/portion.md under a different message).
- Psyche 2026-08-27 (typed): no timestamps and no session id in psyche records (flow dir implies session); Delineate accepted ("Yes! That's what I was looking for"); delineation and anatomy are protos; Prospective<T> liked, Datom probably a kind; direction asymmetry approved straight into distilled vision (→ Vision/protos.md, subflow); design + psyche-distillation edits approved (subflow applying).
- Flow-protocol failure found: reports/anatomyFirstPrinciples.md (mine) and reports/datomVisionFix.md (subflow) lacked `## Sources`; fixed. Cause: I wrote a "design document" (a category the subflows skill grants but the flows layout has no home for) into reports/ without the report rule; the subflow was dispatched without loading the flows skill.
- Vision/datom.md updated (reports/datomVisionFix.md): curly quotes default string delimiter; guillemets delimit a map, key and value separated by a space, positional; a map in expected position carries no Head; a Head is always a variant. Balance-based parenthesis rules moved under Meaning. Open: the old escape rule ("an unbalanced interior parenthesis is escaped") was dropped — needs the psyche's word.
(none yet)

## Witnessed
- witnesses/datomTextualizeRealizeAnatomy.md (code read): two crates, protos v0.8.0 (Shape, Block, BlockScanner lexer, StructuralWalk / RealizeWalk / TextualizeWalk, scoped handles) and datom v0.5.0 (single datom.rs, DatomRealizing / DatomTextualizing / DatomRoot / DatomHeadedUnit / DatomText<T>). Textualize is flat, single-space, no newlines or indentation. Realize is two-pass: BlockScanner lexing, then RealizeScope::realize_body dispatch. Oddities: delimiter mapping in three places; Block has its own Textualize impl; bare/key validation re-parses through the scanner; ethos-monolith emits Datom impls as string-concatenated Rust.

## Psyche records (vision/)
Provenance lines reduced to `-- psyche, STT.` / `-- psyche, typed.` per the no-timestamps ruling. Added this turn: delineate, directionAsymmetry; appended to psycheLogging, rollingDistillation, textualTypes, anatomy, portion.
datomMaps, textualTypes, decomposable, portion, anatomy, multiPass, datomNexus, psycheLogging, rollingDistillation, softwareAnatomySkill — 2026-08-27 monologue, recorded in the excerpt-with-`...` form the psyche asked for.

## Reports
- reports/anatomyRound2.md — universal principles of shape (arity anatomical for {}, free for [] and <<>>), protos types incl. Anatomy vocabulary, kinds, Datom-as-kind argument, names for Portion/Span/Delineate.
- reports/psycheLoggingProposal.md — excerpt protocol: psyche-interraction.md gains the per-topic excerpt rule with ` ... ` and a transcript provenance line; flows.md's "words verbatim" narrowed to "excerpted to the parts relevant to that entry". Awaiting the psyche.
- reports/rollingDistillationProposal.md — design.md gains a cadence paragraph (every second or third turn, dispatch gathering, propose distillation before any Vision/ change); psyche-distillation.md names proactive dispatch as a mode. Awaiting the psyche.
- reports/textPositionRepresentations.md — ropes solve editor mutation, not spans; parsers store byte-offset pairs (rustc, rowan/text-size, tree-sitter) and compute line/col on demand; rowan's green (untyped, widths only) / red (typed, offsets accumulated lazily) tree mirrors delineate-then-match with computed spans. Recommendation (inference): byte-offset spans; green-tree-style delineation.
- reports/anatomyFirstPrinciples.md — round-1 design from the psyche's 2026-08-27 monologue: forms, kinds (Delineate/Realize/Textualize/Anatomize), Portion/Head/Separator/Delimiter/Span/Anatomy, names offered, five questions.
- reports/protosDatomPsyche.md — verbatim catalogue of all psyche on protos/datom/textualize/realize; two active conflicts in Vision/datom.md (string delimiter, map syntax) superseded by 2026-08-26 rulings; ten unknowns.
- reports/textualizeRealizeAnatomyReview.md — the anatomy set against the psyche: six agreements, eight odd fits, central open question.
- reports/textPositionRepresentations.md — research: ropes are irrelevant (editor mutation structure, not span representation); byte-offset pairs (u32 start/end) are the standard for parsers (rustc, rust-analyzer/text-size, tree-sitter); line/col computed on demand; rowan green/red tree parallel to untyped-delineation-first / typed-matching-second design.

## Settled
- Applied: design.md cadence paragraph (rolling distillation) and psyche-distillation.md proactive-dispatch mode — Curriculum 9e114dc6, primary f24a5b1b (that primary commit also swept in this flow's then-dirty log.md and vision/portion.md under a different message).
- Psyche 2026-08-27 (typed): no timestamps and no session id in psyche records (flow dir implies session); Delineate accepted ("Yes! That's what I was looking for"); delineation and anatomy are protos; Prospective<T> liked, Datom probably a kind; direction asymmetry approved straight into distilled vision (→ Vision/protos.md, subflow); design + psyche-distillation edits approved (subflow applying).
- Flow-protocol failure found: reports/anatomyFirstPrinciples.md (mine) and reports/datomVisionFix.md (subflow) lacked `## Sources`; fixed. Cause: I wrote a "design document" (a category the subflows skill grants but the flows layout has no home for) into reports/ without the report rule; the subflow was dispatched without loading the flows skill.
- Vision/datom.md updated (reports/datomVisionFix.md): curly quotes default string delimiter; guillemets delimit a map, key and value separated by a space, positional; a map in expected position carries no Head; a Head is always a variant. Balance-based parenthesis rules moved under Meaning. Open: the old escape rule ("an unbalanced interior parenthesis is escaped") was dropped — needs the psyche's word.
- The anatomy agrees with the psyche on: traits in protos; one frame discipline both ways; context-driven dispatch; top-level textual-realizes / real-textualizes; curly-default strings; guillemet maps; bare-when-fits.

## Open
- Psyche logging protocol redrafted (reports/psycheLoggingProposal.md): single home psyche-interraction.md; flows.md keeps a pointer clause; timestamps and session id removed; a record carries only `-- psyche, STT.`/`typed.`; excerpt rule with ` ... `. Awaiting the psyche. Note: psyche-distillation.md still ids a record by session short id + count.
- Is a design document a report (Sources) or does a flow get design/?
- Escape rule for Meaning parentheses.
- Round-2 questions: Delineate context-free for every dialect? Alternatives anatomy or context? Separator set.
- Psyche 2026-08-27 monologue: design from first principles (code set aside); vision records by topic in vision/ (subflow); Vision/datom.md fix (guillemet maps, space-separated key value; curly-quote strings) (subflow); psyche-logging excerpt protocol proposal and rolling-distillation proposal (subflow); span/rope research (subflow).
- Central question for the psyche: below the root, the real type carries both seams (DatomRealizing on the real type, taking an untyped Block). Is a typed textual block wanted between Block and the real type ("define the block … ontology of source code")?
- Delimiter knowledge in three places; Block's second textualize path outside the walk; bare-safety by re-parse.
- Unruled: fallibility of textualize below the top; layout of nonempty/nested output; `<>` in datom vs `<<>>`.
- Distillation debt: Vision/datom.md stale on strings and maps; protos.md proposal unapproved (b675f3d9, ac1e9ec8).
