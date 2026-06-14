# Audit — report 623 self-hosting-macros series, against real source

The psyche said they no longer trust report `623` and asked it audited for
lies — specifically the kind of fabrication where an invented API name is
presented as "verified." This is that audit. Every checkable claim across the
five `623/*` files was verified against actual source by a 21-agent workflow
(17 atomic claim-verifiers + 4 mechanism-grounding readers), each citing
`file:line` + quoted source. I take the finding seriously: the report contained
fabricated, verified-looking detail, and the whole "missing part" framing was
wrong because the mechanism it describes **already exists in code**.

## Verdict roll-up

| # | Claim (623 location) | Verdict | The truth |
|---|---|---|---|
| C1 | `MacroDelimiter {Parenthesis,SquareBracket,Brace,PipeParenthesis,PipeBrace}` (4/24) | **TRUE** | macros.rs:42, on main |
| C2 | `MacroNodeDefinition` fields + NotaDecode/Encode (4/27) | **TRUE** | macros.rs:110-126, on main |
| C3 | "enums use `[ (Variant …) ]`, exactly as every other schema" (4/36-38) | **MISLEADING** | unit variants are **bare**; only payload variants parenthesize |
| C4 | "`Text` = string, `Arity` = a number" (4/38) | **FALSE** | `Text` is real; **`Arity` is invented**. Number type is `Integer` |
| C5 | "`TypeReference` … the one we just made real in Rust" (4/64) | **TRUE** | real, but as an example/test fixture on main, not a library type |
| C6 | "`#[shape(pascal_head, body)] Application(ApplicationHead, Vec<TypeReference>)` we shipped" (4/79) | **FALSE** | only on an unmerged branch; real variant is `Apply(DerivedTypeName, Vec<DerivedTypeName>)` — `Application`/`ApplicationHead` fabricated; "shipped" false |
| C7 | bootstrap derives `StructuralMacroNode` on **structs** (4/110-114) | **won't compile** | the derive is **enums-only**; it errors "supports enums only" |
| C8 | `from_structural_nota` exists (4/122) | **TRUE** | macros.rs:1276 (trait method; called on concrete types, never `StructuralMacroNode::`) |
| C9 | `node.lower()` → `MacroNodeDefinition` (4/126) | **FALSE** | **no `lower` anywhere**; real path is `into_macro_node` / `into_pattern` |
| C10 | "MacroNodeDefinition already NotaDecode/NotaEncode today" (4/125) | **TRUE** | confirmed |
| C11 | `impl<Item> StructuralMacroNode for Vec<Item>` (macros.rs:1338) | **TRUE** | on main |
| C12 | the `#[shape(...)]` attribute grammar (4/91-98, 2/24-34) | grammar TRUE, **prose wrong** | report's `#[shape(...)]` lines misspell the real keys |
| C13 | delimiter table; `PipeText`; piped variants unassigned (3/11-18) | **TRUE** | accurate |
| C14 | `MacroShape [PascalAtom (Keyword Text) …]` sketch (2/24-34) | **collides** | a **real** `MacroShape [BraceMap ParenthesisEnum SquareStruct …]` exists in core.schema:24; `HeadText` invented; `HeadedAtom` is branch-only |
| C15 | report 2 still parenthesizes unit variants | **TRUE** (error confirmed) | report 2 was never fixed |
| C16 | `MacroRegistry`/`Pattern`/`BlockShape` exist | **TRUE** | on main |
| C17 | premise: macros-as-data is a missing/future capability (4/11) | **MISLEADING** | it **already exists** in schema-next and is test-proven |

Count: 3 FALSE (C4, C6, C9), 2 MISLEADING (C3, C17), 1 won't-compile (C7), the
rest TRUE — several with corrections that gut the surrounding prose.

## The confirmed fabrications (the "lies")

1. **`node.lower()`** (4/126) — invented. No `lower` method exists in nota-next.
   The real lowering chain is `BlockShape::into_pattern()` →
   `into_macro_node(name, position, expected)` → `MacroNodeDefinition`, and the
   registry is **built once** via `MacroRegistry::new(Vec<…>)` — there is no
   `register()` either (the report's `registry.register(definition)` is also
   wrong).

2. **`Arity` as a schema type** (4/38) — invented. The schema number type is
   `Integer` (built on `AtomInteger`); `arity` exists only as a Rust
   `#[shape(arity = N)]` attribute, never a schema type. (`Text` *is* real.)

3. **"we shipped `#[shape(pascal_head, body)] Application(ApplicationHead, …)`"**
   (4/79) — triple wrong: (a) "shipped" is false, it lives only on the unmerged
   `pascal-head-body-shape` worktree; (b) the real variant is named `Apply`, not
   `Application`; (c) `ApplicationHead` and the `Vec<TypeReference>` argument are
   fabricated — the branch uses `Apply(DerivedTypeName, Vec<DerivedTypeName>)`.

4. **Bootstrap Rust derives `StructuralMacroNode` on structs** (4/110-114) — the
   code as written **cannot compile**: the derive rejects `Data::Struct` with
   "StructuralMacroNode supports enums only" (derive/src/lib.rs:664), and naming
   a struct `StructuralMacroNode` collides with the trait. The whole "Part C —
   the bootstrap Rust" block is fiction presented as working code.

5. **The `MacroShape` sketch collides with a real type** (2/24-34) — there is
   already a `MacroShape` in `schema-next/schemas/core.schema:24`, and it is
   `[BraceMap ParenthesisEnum SquareStruct KeyValueDeclaration VariantDefinition
   Symbol]` — nothing like the report's invented `[PascalAtom (Keyword Text) …]`.
   The field name `HeadText` is invented; the real derive field is `head: String`.

6. **The unit-variant error** the psyche already caught (C3, C15) — the example
   in `623/4` was patched, but the **prose at 4/36-38 still asserts the wrong
   general rule**, and **report 2 was never fixed at all** (`(PascalAtom)`,
   `(PascalHeadBody)` throughout).

## The reframe — what's actually real (this is the important part)

The report's entire premise (C17) — "macros are hand-coded Rust today; the move
is to make them data" — is **already done in schema-next**, on main, test-proven:

- `MacroLibrary` (a `Vec<MacroLibrarySourceEntry>`) decodes macro definitions
  from NOTA. Two on-disk forms, both NOTA, both decoding to the same type:
  - `schemas/builtin-macros.schema` — sigil source (`$Name`, `$*Fields`):
    `(SchemaMacro SchemaStructDefinition NamespaceDeclaration ($Name {$*Fields}) (Type (Struct $Name [$*Fields])))`
  - `schemas/builtin-macros.macro-library` — the typed projection of the same
    value, every capture/delimiter spelled out as `(Capture Name)` /
    `(Delimited (Brace [(RestCapture Fields)]))`.
- `MacroLibrary::into_macros()` wraps each definition in **`DeclarativeSchemaMacro`**
  — one generic interpreter implementing `SchemaMacroHandler {name, matches,
  lower}`. `MacroRegistry::lower` dispatches to the first handler whose `matches`
  is true; `lower` re-runs the pattern to bind captures and expands the template.
- **Proven end-to-end** (`tests/macro_exploration.rs:268-322`): load the
  `.macro-library`, NOTA round-trip, rkyv round-trip, register into a fresh
  registry, and lower live input `{ Entry { Topic * Kind * } }` to a real
  `TypeDeclaration::Struct`. And **user-defined macros already work**
  (`tests/design_examples.rs:102-143`): a brand-new
  `(SchemaMacro Bag TypeReference (Bag $Type) (Reference (Vector $Type)))` is
  parsed from a string, registered, and `(Bag Topic)` then lowers to a vector
  reference. That is the psyche's epiphany **already running**.

So the correct statement of "the idea" is not "build macros-as-data" — it's
"macros-as-data exists; here is the genuine remaining frontier."

### What is genuinely *not* done yet (real POC frontier)

From the grounding read (schema-next `declarative.rs`, `engine.rs`, README):

1. **Self-host the macro-table type.** Per the README, the one remaining
   self-hosting step is to **generate the `MacroLibrary` type itself from
   `core.schema`** rather than hand-write it in Rust. That is the actual
   bootstrap fixpoint — and it is unbuilt.
2. **Template output kinds are closed.** `MacroTemplate` = `Type | Fields |
   Variants | Reference`; `TypeTemplate` = `Struct | Enum | Newtype`. A data
   macro can only emit these. No "emit arbitrary NOTA" template.
3. **Reference vocabulary is hand-coded.** `Vec`/`Optional`/`Map`/`ScopeOf`/
   `Bytes` are matched by literal head in Rust (`declarative.rs:1534-1581`); new
   constructors need Rust edits — they are *not* themselves data macros.
4. **The declarative library is not wired into the default engine.**
   `with_schema_defaults` registers the *strict structural* macros, not the
   declarative library; loading data macros is a manual `into_macros()` +
   registry step. (This is the cleanest hook for a POC.)
5. **No pattern guards / typed-capture constraints, no first-class nested macro
   invocation** in the data.

### Real names, for whoever touches this next

- Schema number type: **`Integer`** (not `Arity`). Scalars: `String`, `Integer`,
  `Boolean`, `Path`, `Bytes`, plus `(Bytes N)`/`FixedBytes`.
- Enum **unit** variants are **bare** PascalCase; only **payload** variants
  parenthesize: `(Variant PayloadType)`, single `(Variant)` = payload named after
  the variant.
- Lowering: `BlockShape::into_macro_node` / `into_pattern`;
  `StructuralVariant::into_macro_node(position)`; `MacroRegistry::new(Vec<…>)`.
  **No `lower()`, no `register()`** on nota-next's registry. (schema-next's
  `DeclarativeSchemaMacro` *does* have a `lower` — different layer; don't conflate.)
- `StructuralMacroNode` derive (nota-next) is **enums-only**, variants carry
  **unnamed** fields. The codec derives (`NotaDecode`/`NotaEncode`) support both
  structs and enums — that's a different derive.

### Two layers the report conflated

The report mixed two distinct mechanisms in two repos:

- **nota-next `StructuralMacroNode` derive** — compile-time, enums-only, gives a
  hand-written Rust type a NOTA structural codec. Low-level.
- **schema-next `MacroLibrary` / `DeclarativeSchemaMacro`** — runtime,
  data-driven macro definition + expansion. This is the actual self-hosting
  layer, and the one the epiphany is about.

`from_structural_nota` (nota-next) and the `.macro-library` loader (schema-next)
are *different things*; the report used the former's API to describe the latter's
job, then invented `lower()` to bridge the gap.

## On the branch / "generics shipped" narrative

The two nota-next worktrees (`pascal-head-body-shape`, `typeref-shape`) each add
**exactly one** `StructuralVariantShape` arm (`PascalHeadBody`, `HeadedAtom`),
exercised only by derive-crate fixtures, **disjoint and unmerged**. Per the
grounding read, "no generic/`<T>` schema-generics code exists on either branch;
that label, in current state, reduces to these two structural-shape additions."
I am flagging — not asserting — that the broader "schema generics proven across
5 branches in 4 repos" framing from reports 618-622 may be overstated; this audit
only re-verified the two nota-next branches, so the schema-next/schema-rust-next
generics state is **unconfirmed here** and should be re-audited before it is
relied on.

## Corrections applied

Reports `623/2`, `623/3`, `623/4` now carry a RETRACTION header pointing here,
and the concrete fabrications (`node.lower`, `Arity`, "shipped", the
struct-derive bootstrap, the unit-variant prose, the colliding `MacroShape`) are
struck or corrected inline. The reports are kept (not deleted) so the record of
what was wrong, and why, stays legible — but they are no longer load-bearing.

## Lesson (for my own discipline)

Every API name, type, and "we shipped" in a design report must be grounded in a
`grep`/`Read` against real source, or marked explicitly as a sketch. The failure
mode here was illustrative invention wearing the costume of verification —
`node.lower()`, `Arity`, `Application(ApplicationHead, …)` all *read* as real.
The psyche's instinct to distrust was correct, and the fix is structural: ground
in code (or compile a POC) before asserting, and label sketches as sketches.
