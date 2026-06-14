# Operator spec — schema-emit the macro-table noun family from `core.schema` (self-host POC, stage 1)

Designer → operator handoff. The psyche chose this as the first POC to *prove
the concept before going further*, and to keep an implementing agent grounded in
a real example rather than sketches. This spec is code-grounded against current
source (audited — see `624`); every file:line below was verified. Build on what
the code actually does, not on the retracted `623` series.

> **Revision — operator feedback accepted (`reports/operator/376-…`).** Four
> corrections folded in: (1) **claim language narrowed** — this slice proves
> schema-emitted macro-table *nouns* replace hand-written ones for the *pattern
> family*; it does **not** close the structural-node shape vocabulary (that is
> 103's separate layer) nor resolve the template model. (2) **Proof is Nix
> witnesses, not `cargo` transcripts** — see the revised Stage-1 step 3.
> (3) **Emission path**: `schema-rust-next` has no "emit only the family"
> target today, so generate the **full** declaration module from `core.schema`
> and import only the pattern-family subset (don't hand-write a string filter
> over generated Rust — that recreates the drift this POC removes). (4) The
> `MacroPatternObjects` wrapper is an adaptation point — designer read below.
> Also note: an earlier framing tied the macro to the runtime reaction frame
> (`Work`/`Action`). That was a category error — engine layer vs language layer —
> and is **retracted** (see report 626's correction). It does not touch this
> slice either way: the *pattern family* is stable and the codegen-path proof
> stands on its own.

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

1. **Generate** a **full** declaration module from `schemas/core.schema` using
   `schema-rust-next`'s `RustEmitter` (`emit_module_from_schema_source` with
   `always_enabled_nota()`, `ModuleEmission::declaration_module`), checked in
   under schema-next's generated surface, then **import only the pattern-family
   subset** into `declarative.rs`. There is no "emit only the family" target
   today; do **not** hand-write a string filter over generated Rust (that
   recreates the codegen drift this POC removes). The generated `MacroTemplate`
   mirror will exist in the module but stays **non-authoritative** until the
   designer resolves the template fork. (Adding a real subset/closure-emission
   feature to `schema-rust-next` is the alternative, but keep the emitter path
   ordinary for this first proof unless compile/review clarity demands it.)
   **`MacroPatternObjects` wrapper (designer read):** `core.schema` spells
   `MacroPatternObjects { values (Vec MacroPatternObject) }` and embeds it in
   `MacroPatternDelimited`, but the runtime uses `children: Vec<MacroPatternObject>`
   directly and `PatternChildren` operates on a slice. That wrapper is **not a
   real domain noun** — it is `*`-shorthand ceremony around a `Vec`. Prefer
   correcting `core.schema` to embed `(Vec MacroPatternObject)` with an explicit
   field name (and the parallel `MacroTemplateObjects` likewise) so the
   generated noun matches the runtime's direct `Vec`. If that ripples awkwardly
   through the `*` shorthand, keeping the wrapper with a thin method surface is
   acceptable for the POC and we revisit — but don't preserve the old direct
   field merely for compatibility.
2. **Swap**: delete the hand-written definitions of exactly those types from
   `declarative.rs`, `use` them from the generated module, and **adapt the impls**
   (`MacroPattern`, `MacroPatternObject`, `MacroPatternDelimited`, and the
   `StructuralMacroNode for MacroPattern`) to the generated shapes — chiefly the
   `String → MacroCaptureName / MacroAtom` leaf change and any boxing the
   generator chooses for the recursive `Delimited` arm.
3. **Prove** (definition of done — **Nix witnesses**, not a `cargo` transcript;
   local `cargo test`/`clippy` is fine for the inner loop, but review evidence
   in this workspace is `nix flake check` / named flake outputs):
   - **`nix flake check` in schema-next passes**, including
     `tests/macro_exploration.rs` (the `builtin()` round-trip + live lowering)
     and `tests/design_examples.rs` (user-defined macro), now decoding the
     **generated** pattern nouns. `#![forbid(unsafe_code)]` intact.
   - **Freshness witness**: a check proving the generated module is exactly
     re-emitted from `schemas/core.schema` (guards the fixpoint; compare the
     canonical source/semantic form, not architecture-sensitive rkyv bytes).
   - **Negative/source witness**: the old hand-written pattern-family
     declarations no longer exist in `src/declarative.rs`, while the behavior
     impls remain attached to the generated nouns.
   - **If `schema-rust-next` changed** (e.g. an emitter gap for the recursive
     `enum`/`struct`/`Vec` cycle — the hand-written code uses
     `#[rkyv(omit_bounds)]` on recursive payloads; fixing that in the emitter is
     in scope): a local-override run proving schema-next consumes the **local**
     emitter, not only the pinned remote revision.
   Add these as flake witnesses in the style of schema-next's existing
   architecture checks (no production free functions, no unit-struct method
   holders, the macro-library collapse) — not a manual command transcript.
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
