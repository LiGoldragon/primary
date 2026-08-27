# Review: anatomy of the Datom textualize/realize logic against the psyche

## Organs as they stand (code read, witness datomTextualizeRealizeAnatomy)

    textual form                 walk (protos)                      real form
    ------------                 -------------                      ---------
    SourceText ─BlockScanner─► Block{head,shape,body}            (typed values)
                                     │                                  ▲
                          RealizeWalk/RealizeScope                      │
                          frames: enter/close/resume ── dialect closure ─┘
                                                        ShapeDefined::select
                                                        DatomRealizing::realize_block (on the real type)

    (typed values) ──DatomTextualizing::textualize_in──► TextualizeScope::textualize_block
                                                          head. + open + children + close
                                                          one space between siblings ──► SourceText

    protos (1319 lines): Shape(11), Head, Block, BlockScanner, StructuralWalk,
      RealizeWalk/TextualizeWalk, RealizeScope/TextualizeScope, Realize, Textualize (form.rs, 14 lines)
    datom (1435 lines, one module): DatomRealizing, DatomTextualizing, DatomRoot, DatomHeadedUnit,
      DatomText<T>, Realized<T>/Projected<T> evidence, impls for scalars/collections/records
    callers: orchestrate CLI (realize), signal-orchestrate (78 generated impls), curriculum-deploy,
      signal-spirit, meta-signal-spirit; ethos-monolith generates the impls as string-built Rust

## Where the anatomy agrees with the psyche (observations)

- Realize and Textualize are protos traits; the universal substrate (walk, Shape, Head, scanner,
  string carriers) is in protos; datom rides it. — matches "The traits should live in protos
  regardless" (2026-08-14) and "I want universal stuff in protos" (2026-08-14).
- One frame discipline under both directions (StructuralWalk; enter/close/resume; parent resumes
  where it left off). — matches Intent protosParsing ("one walk in two directions").
- Context-driven dispatch: each block is realized inside its own scope by the type the shape+head
  announces (ShapeDefined::select). — matches "there is always a parsing context" (2026-08-11).
- At the top level the textual type realizes and the real type textualizes:
  DatomText<T>: Realize → T; Report: Textualize → ReportText. — matches 2026-08-18 ruling.
- Curly quotes are the default string delimiter in textualize (Bare if it fits, else CurlyQuoted);
  parenthesized strings are rejected in tests; maps use guillemets `<<…>>`; integers canonical bare.
  — matches 2026-08-26 rulings. (Parts of ac1e9ec8's four-divergence witness are now stale: the
  i64 gap and the curly-quote default have been closed in code since.)
- A string that fits bare is emitted bare. — "A string that doesnt need quotes *must not* be quoted".

## Where the anatomy sits oddly against the psyche (observations, with the psyche word they touch)

1. Below the top level, the real type carries both seams. `DatomRealizing::realize_block` is
   implemented on the real type (e.g. `impl DatomRealizing for i64`) as a constructor taking a
   `Block`; the only textual type under the root is the untyped `Block`, whose own `Realize` yields
   `Vec<Block>`. — Touches "realize isnt implemented by the same type as textualize … You dont
   realize the realized data" (2026-08-18) and "we need to define the block … turn every logical
   aspect into a type. ontology of source code" (2026-08-18). Whether a typed textual block is
   wanted between `Block` and the real type is the central open question (psyche unknown 1).
2. The shape→delimiter knowledge lives in three places: `Block::textualize`, 
   `TextualizeScope::textualize_block`, and implicitly in `BlockScanner::scan`'s character matches.
   — Touches "The minimum amount of code for the most elegant machinery" and "bullet proof not by
   lots of complex code, but by the right abstraction layers".
3. `Block` has a second textualize path outside the walk (no frames, no evidence). — Touches "one
   walk in two directions".
4. Bare-safety (`fits_bare`) and map-key ambiguity checks decide by re-parsing synthetic text
   through the scanner. — Touches "Big implementations are a sign of a missing logic plane"; the
   missing plane looks like a bare-safety predicate as its own type/trait. (Hypothesis.)
5. Protos `Textualize` is infallible; datom's `DatomTextualizing` is fallible; the protos-level
   `Textualize` impls for Report/InterimNote return a Result. — The psyche has not ruled which
   transitions are fallible below the top level (unknown 4).
6. Canonical output is flat: one space between siblings, no newlines, no indentation. — The
   psyche accepted `Observed.Locks.[]` as "good enough for now" (2026-08-27); layout of nonempty and
   nested output is unruled.
7. `<>` is "a real Protos delimiter of course" (2026-08-27); the Shape enum has no angle-bracket
   shape, only ASCII guillemets `<<`/`>>` for maps. Whether datom's guillemet is `<<>>` or `«»`, and
   whether `<>` is a datom shape or ethos-only, is unspoken.
8. Ethos-monolith mass-produces the per-type seams as string-concatenated Rust (78 impls in
   signal-orchestrate). Not wrong by any ruling; noted because the anatomy's type-driven dispatch
   makes every type need an impl, so the generator is where the anatomy is actually reproduced.

## Distillation debt seen in passing (not this flow's to fix)

- Vision/datom.md still carries parentheses-as-default-string and `[key.value …]` maps; the
  2026-08-26 rulings supersede both. ac1e9ec8's revision and b675f3d9's protos/datom proposals
  await the psyche's approval. The Realize/Textualize vocabulary lives only in that proposal.

## Unknowns carried forward

Psyche unknowns 1–10 from reports/protosDatomPsyche.md; plus: does the scanner accept a
multi-segment head such as `Observed.Locks.` (needed for `Observed.Locks.[]`)? Not read.

## Sources

- witnesses/datomTextualizeRealizeAnatomy.md (code read, this flow)
- reports/protosDatomPsyche.md (this flow) — verbatim psyche, ordering, unknowns
- reports/rememberedFlows.md (this flow) — flows 01a04339, b675f3d9, ac1e9ec8
- Vision/datom.md; psyche-raw/Intent/protosParsing.md
- flows/ac1e9ec8/witnesses/datomCurrentSyntax.md (prior witness, partly stale)
