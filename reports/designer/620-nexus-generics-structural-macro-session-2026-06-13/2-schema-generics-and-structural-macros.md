# Schema generics + the structural-macro machinery verdict

The core technical thread. Verified against nota-next/schema-next source.

## What schema needs to express (the two new forms)

Today a `.schema` file expresses only: (a) closed type declarations
(`Name [...]` enum, `Name {...}` struct, `Name Type` newtype) and (b) concrete
imports (`LocalName source:path:Type`). It cannot express **a type with holes
and the filling of those holes** — i.e. generics. The universal reaction frame
needs exactly that. Two halves, in two places:

### 1. Parameterized DEFINITION (where parameter names are written) — once

A shared `reaction.schema` declares the frame once. The declaration HEAD
carries the type-parameter names:

```
;; reaction.schema (shared, declared once for the workspace)
{
  (Work Event Write Read Effect)
    [(SignalArrived Event) (SemaWriteCompleted Write) (SemaReadCompleted Read) (EffectCompleted Effect)]
  (Action Reply Write Read Effect Continuation)
    [(ReplyToSignal Reply) (CommandSemaWrite Write) (CommandSemaRead Read) (CommandEffect Effect) (Continue Continuation)]
}
```

`Event Write Read Effect` are the parameter names — written ONLY here. New
NOTA syntax: a declaration head can be a parenthesized `(Name Param Param …)`
instead of a bare `Name`. (Like `Vec<T>` defining `T` once.)

### 2. Type APPLICATION (where arguments are written) — per component

Generalize the existing `(Vec Domain)` form to a multi-arg application of an
imported generic. The component's `nexus.schema` puts the application in the
Input/Output **root position** (which today holds a bare `[Variant …]` list):

```
;; component nexus.schema — root positions hold frame APPLICATIONS
{ …imports…  reaction signal-reaction:reaction … }
(reaction:Work   SignalInput SemaWriteOutput SemaReadOutput EffectOutcome)   ;; Work root
(reaction:Action SignalOutput SemaWriteSet SemaReadInput EffectCommand)      ;; Action root
{ …only the payload vocabularies: SemaWriteSet, EffectCommand, EffectOutcome, records… }
```

Arguments fill parameters **positionally** (first arg → first param), exactly
like `Vec<i32>` (you write `i32`, never `T`). No alias (positional in the root
slot), no ZST. With direct-parameter generics, derives work natively.

The `TypeReference` AST gains one variant (the only plane-grammar touchpoint):
```
TypeReference::Application { head: ResolvedImport, arguments: Vec<TypeReference> }
```
beside the existing `Vector`/`Optional`.

### Per-component generics need NO new section

A parameterized declaration is just another declaration SHAPE, recognized
anywhere declarations are decoded. A component defines a local generic inline
in its ordinary `{declarations}` block: `(Paged Item) { Items * Cursor * }`.
"Shared vs local" is the import/export boundary, identical to concrete types —
not a grammar or section distinction. `reaction.schema` is "a file of
parameterized declarations meant to be imported," not a different grammar.

## The structural-macro machinery verdict

The psyche's worry ("maybe the structural macro design wasn't implemented as I
intended") prompted a hard look. **The machinery DOES implement the concept**
(shape-dispatch at flexible positions, type-directed, first-match-wins,
recursive, bidirectional). Earlier claims (mine + SD's) that "captured head
can't be expressed" are WRONG.

The `#[derive(StructuralMacroNode)]` (aka `ln`) shape vocabulary
(`nota-next/derive/src/lib.rs:865` `StructuralVariantShape`):

- `pascal_atom` — a bare PascalCase atom (named type / unit variant)
- `keyword = "x"` — a specific keyword atom
- `head = "X", arity = N` — FIXED head + N total objects (N-1 child fields)
- `head = "X", body` — FIXED head + VARIABLE-arity body (`Vec<Item>` tail)
- `pascal_head, arity = N` — **CAPTURED head** (any PascalCase atom, captured
  into field 0) + N objects. THIS is generic application.

Proof in `tests/macro_nodes.rs:545`: `DerivedReference` is literally a
TypeReference-with-generics —
`Named(#[pascal_atom]) | Optional(#[head="Optional" arity=2]) | Application(#[pascal_head arity=2])` —
decoding `(Optional Integer)` and `(Foo Bar)`. `DerivedVariantSignature` uses
`pascal_head arity=4`; `DerivedTemplate` uses `head="Variants" body` (variable
arity); the registry detects when a general head shadows a specific one and
errors at build time (reachability). The underlying `MacroRegistry`/`Pattern`/
`BlockShape` API is even richer (recursive `.with_children`, `AtomShape::symbol`,
`MacroObjectCount::Even/Exact`).

### The REAL gaps (narrow)

1. **`pascal_head + body`** (captured head + VARIABLE-arity body) is NOT a
   derive form — the parser only allows `pascal_head + arity` (fixed) or
   `head="X" + body`. But application `(reaction:Work A B C D)` and the
   parameterized-decl head `(Work Event Write Read Effect)` need captured head +
   variable arity (a generic may have 2 or 4 args). So this is the one genuine
   derive-vocabulary gap. The underlying Pattern API can express it (capture a
   head atom + read the tail as a vector); the convenience derive doesn't expose
   the combination. Fix: add `pascal_head + body` to the derive, OR hand-`impl
   StructuralMacroNode` via the Pattern API.
2. **head alias-sets** ({Vec, Vector}) — no `head = ["Vec","Vector"]` form.
   DISSOLVES under no-backcompat: collapse each alias to one canonical spelling
   (only `Vec`, only `Optional`) and `head = "Vec"` suffices.

### SD's D5-1 / primary-xzzf (TypeReference) — corrected

SD reported TypeReference is a hand-rolled `match head { "Vec"|"Vector" => … }`
(violating "everything is a structural macro"), and listed three missing derive
forms: alias-sets, nested-pairs (Map K V), numeric-atoms. Corrected against
current source:
- **alias-sets**: real but dissolves under no-backcompat (above).
- **nested-pairs `(Map K V)`**: ALREADY expressible — `head = "Map", arity = 3`
  with two `TypeReference` fields (like `head="Optional" arity=2` for one). SD's
  "no form" was outdated; multi-field arity works (`DerivedVariantSignature`
  arity=4 proves it).
- **numeric-atoms**: possibly a narrow gap, but MOOT for TypeReference (type
  refs carry no numerics).
- The actual blocker for converting TypeReference to a structural macro AND for
  generics is the SAME one new form: **`pascal_head + body`** (so application
  `(Foo A B …)` with variable arity decodes). Plus the alias collapse.

So: the SD TypeReference fix and the generics support are the SAME piece of
work — extend the derive with `pascal_head + body`, then both TypeReference and
the application form become genuine structural macros. `v0n6` already mandates
this (hand-parsing is a violation; if a shape can't be expressed, the design
wasn't implemented properly — surface it). Here the shape CAN be expressed at
the API level; the derive convenience layer just needs one more form.

## reaction.schema is a new schema-file KIND (psyche's framing, confirmed)

The frame definition file is read by its own structural-macro grammar (a
`FrameSchema` of `ParameterizedDeclaration`s), distinct from the plane grammar.
But the parameterized-declaration SHAPE is a reusable structural-macro node
added to the shared declaration grammar — not a grammar fork. The plane grammar
moves by exactly one shape: `TypeReference::Application`. Emit side: a new
`RustEmissionTarget` emits the generic frame once; `NexusRuntime` emits the
application + payload enums instead of a concrete per-component frame.

## Emitter precedents (schema-rust-next) for the implementation

- `PlaneEnvelopeTokens` (`lib.rs:2887`): already emits `pub struct #name<Root>`
  with rkyv derives + `impl<Root>` incl. `map_root<NextRoot>` — proves the
  emitter generates generic-over-param types + derives, and rkyv-derive on a
  generic struct (direct field) ships and compiles.
- `RustNewtype` + `NewtypeInherentImplTokens` (`lib.rs:992/1827`): schema decl →
  `LowerToRust` noun → `ToTokens` emits the type + `From` impls. The per-item
  emit pattern.
- `NexusRunnerNextStepProjectionTokens` (`lib.rs:2017`): already emits a
  per-component trait impl with associated-type bindings + `into_next_step` —
  the shim to DELETE. A frame-binding emitter is a simpler version of this.

## Implementation plan (task #407)

On a feature branch off nota-next main (designer lane, `~/wt`):
1. Extend the `StructuralMacroNode` derive with `pascal_head + body`
   (captured head + variable-arity body). Add a test mirroring `DerivedReference`
   but with variable args.
2. In schema-next: add `TypeReference::Application` + the parameterized-decl
   declaration shape; resolve the frame import; accept application in the root
   position.
3. Convert the hand-rolled TypeReference codec to a StructuralMacroNode
   (closes SD D5-1). Collapse Vec|Vector etc. aliases to one spelling.
4. Define the shared `reaction.schema` frame; emit it once
   (new emission target); change `NexusRuntime` to emit application + payloads.
5. Prototype-validate (task #408) that the generic frame's wire derives compile
   (direct-parameter generics should derive natively).
