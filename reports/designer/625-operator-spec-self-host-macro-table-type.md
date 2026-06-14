# Operator spec — close the self-host bootstrap: generate the macro-table type from `core.schema`

Designer → operator handoff. The psyche chose this as the first POC to *prove
the concept before going further*, and to keep an implementing agent grounded in
a real example rather than sketches. This spec is code-grounded against current
source (audited — see `624`); every file:line below was verified. Build on what
the code actually does, not on the retracted `623` series.

## The goal, and the fixpoint

schema-next already has a working, test-proven **macros-as-data** system: a
`MacroLibrary` decodes `(SchemaMacro …)` definitions from NOTA and
`DeclarativeSchemaMacro` executes them at runtime. But the *types* that do this
decoding — `MacroLibrary`, `SchemaMacro`, `MacroPattern…` — are **hand-written
Rust** in `schema-next/src/declarative.rs`. The remaining self-hosting step (the
schema-next README names it) is to **generate those types from `core.schema`
instead of hand-writing them.**

The fixpoint that makes this worth doing: `schemas/core.schema` *already
describes* the macro-table types (verified — see the inventory below). So the
generated types decode `schemas/builtin-macros.macro-library`, which is itself a
NOTA artifact re-expressing the **same vocabulary** `core.schema` declares. The
notation describes the type that reads the notation. This POC closes that loop
for a real, non-trivial recursive family of types.

## Grounding — exact current state (verified)

**The hand-written types** (`schema-next/src/declarative.rs`):
`MacroLibrary` (29), `SchemaMacro` (201), `MacroPattern` (312),
`MacroPatternObject` (408), `MacroPatternDelimited` (542), `MacroTemplate` (591),
`TypeTemplate` (684), `MacroTemplateObject` (806), `MacroTemplateDelimited`
(967), `MacroDelimiter` (1002), `MacroLibrarySourceEntry` (1048).

**The behavior** that must survive (impl blocks, same file): `impl MacroLibrary`
(33, the `builtin`/`from_source`/`from_nota_source`/`into_macros` loaders),
`impl StructuralMacroNode for {SchemaMacro (256), MacroPattern (355),
MacroTemplateObject (914)}` (the sigil-source read path), the pattern/expansion
impls (`MacroPattern` 316, `MacroPatternObject` 415, `MacroTemplate` 602,
`TypeTemplate` 702, `MacroTemplateObject` 813), and
`impl SchemaMacroHandler for DeclarativeSchemaMacro` (1259, the interpreter),
plus `CaptureName` (1156), `MacroBindings` (1184), `ExpandedObject` (1403).

**The schema that describes them** (`schema-next/schemas/core.schema`, lines
9-25): `MacroLibrarySourceEntry [(SchemaMacro)]`,
`SchemaMacro { MacroName * MacroPosition * MacroPattern * MacroTemplate * }`,
`MacroName String`, `MacroPattern MacroPatternObject`,
`MacroPatternObjects { values (Vec MacroPatternObject) }`,
`MacroPatternObject [(Capture MacroCaptureName) (RestCapture MacroCaptureName) (Atom MacroAtom) (Delimited MacroPatternDelimited)]`,
`MacroPatternDelimited { delimiter MacroDelimiter MacroPatternObjects * }`,
`MacroCaptureName String`, `MacroAtom String`,
`MacroDelimiter [SquareBracket Brace Parenthesis PipeParenthesis PipeBrace]`,
`MacroPosition [RootImports RootInput RootOutput RootNamespace NamespaceDeclaration StructFields EnumVariants TypeReference]`.

**The codegen leg** (`schema-rust-next`, branch `pqwnolzoqsxp`): the public
emitter is `RustEmitter` (`src/lib.rs:60`).
`RustEmitter::new(options).emit_module_from_schema_source(name, source)`
(lib.rs:104) → `RustModule` → `.render()` → `RustCode`. NOTA-enabled output:
`RustEmissionOptions::always_enabled_nota()` (lib.rs:432). The build-time wiring
(`SchemaPackage` / `ModuleEmission`, `src/build.rs`) is how a crate generates a
module at build; `ModuleEmission::declaration_module(module)` (build.rs:146) is
the relevant entry for a plain declaration module.

## The decisive subtlety — what is clean vs. what is a design fork

**Clean to generate now (the pattern family + leaves):** `MacroDelimiter`,
`MacroPosition`, `MacroCaptureName`, `MacroAtom`, `MacroPatternObject`,
`MacroPatternObjects`, `MacroPatternDelimited`, `MacroPattern`. This sub-graph is
**self-contained in `core.schema`** (every reference resolves inside the family)
and decodes the pattern portions of the real artifact. One real difference from
the hand-written types, and it is an *improvement*: the leaves are typed newtypes
(`MacroCaptureName`, `MacroAtom`) where `declarative.rs` currently uses raw
`String` (408-413). Adapting the impls to the newtypes satisfies the
typed-domain-values discipline — do it, don't fight it.

**A design fork — DO NOT GUESS (gated on designer):** `core.schema` models
`MacroTemplate` as a *structural NOTA mirror* (`MacroTemplate MacroTemplateObject`,
core.schema:16, parallel to the pattern side), but `declarative.rs` models it as
a *typed output kind* — `MacroTemplate = Type(TypeTemplate) | Fields | Variants |
Reference` (591) with `TypeTemplate = Struct | Enum | Newtype` (684), which is
what lets a consumer know the output kind before expansion. These are two
genuinely different designs. Because `SchemaMacro` *references* `MacroTemplate`,
generating `SchemaMacro` / `MacroLibrary` cleanly is **blocked on resolving this
fork**, which is designer + psyche work (the "absorb Rust into schema, bit by
bit" thread). Operator: stop at the family above; leave `SchemaMacro`,
`MacroTemplate`, `MacroLibrary` hand-written for stage 1.

## Stage 1 — the POC slice (operator, now)

1. **Generate** the pattern family + leaves above from `schemas/core.schema`
   using `schema-rust-next`'s `RustEmitter`
   (`emit_module_from_schema_source` with `always_enabled_nota()`), into a new
   module in schema-next (e.g. `src/declarative/generated.rs`). The cleanest
   harness is likely a focused `schema-rust-next` integration test or a small
   build step in schema-next that emits + writes the module; pick whichever
   keeps the generated artifact checked in and re-derivable.
2. **Swap**: delete the hand-written definitions of exactly those types from
   `declarative.rs`, `use` them from the generated module, and **adapt the impls**
   (`MacroPattern`, `MacroPatternObject`, `MacroPatternDelimited`, and the
   `StructuralMacroNode for MacroPattern`) to the generated shapes — chiefly the
   `String → MacroCaptureName / MacroAtom` leaf change and any boxing the
   generator chooses for the recursive `Delimited` arm.
3. **Prove** (definition of done):
   - `cargo test` in schema-next is green — specifically
     `tests/macro_exploration.rs` (the `builtin()` round-trip + live lowering)
     and `tests/design_examples.rs` (user-defined macro) still pass, decoding
     the **generated** pattern types.
   - `cargo clippy` clean; `#![forbid(unsafe_code)]` intact.
   - The generated module is checked in and reproducibly re-emittable from
     `core.schema` (a test that re-emits and asserts equality is ideal — it
     guards the fixpoint).
4. **Report** to `reports/operator/<N>-…` with: the generated module, the diff of
   what was deleted/re-homed, the test evidence, and any place `core.schema` had
   to be corrected to match reality (e.g. recursion/boxing, the `*` field
   shorthand). If `core.schema` and the generator disagree on a *pattern-family*
   detail, fix `core.schema` (it is the source of truth pre-production) and note
   it — but escalate anything touching the template fork to designer.

## Constraints

- **Lane / branch.** Operator lane, operator's integration discipline: land on a
  feature branch / worktree under `~/wt/github.com/LiGoldragon/schema-next` (and
  `schema-rust-next` if the emitter needs a fix), prove green, then integrate to
  main per operator's rebase ownership. Don't disturb schema-next main until the
  tests pass.
- **Rust discipline** (`skills/rust-discipline.md` + sub-files): every function a
  method/assoc-fn/trait-impl on a data-bearing type; per-crate typed `Error`;
  typed domain values (hence the newtype leaves); no hand-rolled parsers; schema
  emits the nouns, impls add the verbs. The generated module is the nouns; keep
  the verbs in hand-written impl files.
- **No backward-compatibility burden.** Pre-production. If the cleanest shape
  changes the types' fields or the `String`→newtype leaves, take it; break
  consumers in the same change. Don't preserve the old hand-written shape for its
  own sake.
- **`jj` inline only.** Commit the whole working copy; descriptions via `-m`,
  never `$EDITOR`. (`skills/jj.md`.)
- If `schema-rust-next`'s emitter cannot yet express something the pattern family
  needs (recursive boxing, the enum-payload shape, the `(Vec X)` field), that is
  a real schema-rust-next gap — fix it there and note it; it is squarely in scope
  (the whole point is the codegen producing these types).

## Out of scope (named, so it isn't silently pulled in)

- The `MacroTemplate` structural-vs-typed fork and generating `SchemaMacro` /
  `MacroLibrary` (stage 2, gated on a designer decision).
- Extending the **closed** template/reference vocabulary (`Vec`/`Optional`/`Map`/
  `ScopeOf`/`Bytes` are hand-matched in `declarative.rs:1534-1581`) — separate
  future work.
- Wiring the declarative library into the **default** engine
  (`with_schema_defaults`, `src/engine.rs:529`) — separate.
- Anything in the nota-next `pascal-head-body-shape` / `typeref-shape` branches —
  unrelated low-level derive shapes, not this layer.

## Why this is the right first cut

It is the smallest slice that genuinely closes the loop: a recursive, real family
of macro-table types, schema-derived, decoding the actual `builtin-macros`
artifact, proven by the existing tests. It improves the types on the way (typed
leaves). And it cleanly fences off the one genuine design decision
(the template model) for the designer thread, so the implementing agent is never
guessing — which is exactly what the psyche asked this POC to guarantee.
