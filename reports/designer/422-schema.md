# 422 — Schema: the type vocabulary, declarations, and emission over NOTA

*Kind: Current-design spec · Component: schema (schema-next → schema-rust-next) · Topics: schema, type-vocabulary, declarations, roots, assembled-schema, emission, modules · 2026-05-29*

*The consolidated agreed spec — folds the designer ([[424]], now removed) and
operator (report 233) views after every fork was resolved. Grounded in
`schema-next/src/asschema.rs` and records 1109 (everything is data), 1116
(assembled schema first), 1120 (pipe declarations), 1122 (everything is a
struct), 1129 (root from filename), 1130 (`.schema` is NOTA-legal first), 1137
(`(Vec X)` form, value-vs-type), 1138 (composability + modules), 1152 (scalar
names full-English), 1155 (roots + free datatypes), 1176 (the type vocabulary
lives in Schema). [[421-nota]] is the substrate; [[423-signal-nexus-sema]] the
reactive layer.*

## 1. Schema is NOTA read against a known type

A schema is itself a NOTA value, so a `.schema` file is **NOTA-legal first**: it
parses as raw NOTA (nota-next) before any schema interpretation (1130). Schema
reading is a second pass over an already-parsed document. The file is read as a
struct whose **root name comes from the filename**, mirroring Rust modules
(1129); the file does not restate its own name. Because the expected type is
known at every position, the reader needs no labels and no sigils (the
positional rule of [[421-nota]] one level up).

## 2. Schema is the composability + module layer (1138)

Schema turns NOTA into a system for **composable data types and data-driven
behavior**, programmable by the user to create new interfaces (node-graph data
types). Schemas **nest**: an engine can hold sub-engines, each with its own
schema. The namespace **mirrors Rust modules** — a schema is a module whose
entries are public symbols, names colon-qualified in one file or split across
files, importable and re-exportable. **Imports are data**: a map of module-name →
a data-carrying variant of the import kind (`FromGit` / `FromPath` / `Adjacent`
/ `FromRepositoryRoot` / …), no flags.

## 3. Schema owns the entire type vocabulary (1176)

NOTA is pure structure; **all type names are Schema's** type-reference
vocabulary:

- **Scalars** (full-English, 1152): `String`, `Integer`, `Boolean`, `Path`.
  (`Float`/`Bytes` deferred until a real need.)
- **Composites**: `(Vec X)`, `(Optional X)`, `(Map K V)` — tagged forms, *not*
  the value-level `[ ]`/`{ }` (1137: `[X]` is a vector *value*, `(Vec X)` is the
  vector *type*).
- **Declarations** use the `@`-sigil forms ([[428-at-sigil-declaration-syntax-spec]],
  settled): `Name@{ field@Type … }` multi-field struct, `Name@{ Type }` /
  `Name@Type` newtype (record 1235, single-element brace → tuple-struct emit),
  `Name@[ variant … ]` enum, `name@(Vec X)` composite. Field and variant
  positions accept the **`@Type` derived-name shorthand** (record 1232):
  `@Topics` is sugar for `topics@Topics` (struct field), and `@Foo` is sugar for
  the enum data variant `Foo@Foo`. The root is an implicit struct with
  positional fields (`{ }` struct, `[ ]` enum, `( )` composite/macro). The pipe
  forms `{| … |}` / `(| … |)` (1120) are **transitional**.
- **References** to declared types are bare names (lowering tags them `Plain`).

A field's type is a scalar, a composite, a declared name, or a nested
declaration; an unnamed composite field derives its name from the type
(`(Vec Proposal)` → `proposals`), falls back to a positional name only when
nothing derives, and an explicit name always wins (1119).

## 4. The assembled schema — the final data model

After lowering, the `.asschema` is macro-free serializable data (1116): a
**roots** section (the named entry-point set, 1155) plus the schema's **type
table** of visibility-tagged declarations (record 1226). The surface `.schema`
root struct has four **positional** fields — `imports` / `input` / `output` /
`namespace` per the schema-of-schemas — and the values at each are bare (record
1229): `{}` for imports, `[ Record@Entry … ]` for the signal-plane input
variants, `[ Recorded@Receipt … ]` for output, `{ …decls… }` for namespace. The
lowering pass assigns the canonical names `Input` / `Output` to the positional
enum bodies when building `roots: Vec<RootDeclaration>`; additional plane roots
declared **inside** the namespace (`NexusInput@[ … ]`, `SemaInput@[ … ]`) lower
as ordinary named root declarations. The `Name@Delimiter` rule applies only to
declarations — when the user invents a new name.

```rust
pub struct Asschema {
    identity: SchemaIdentity,
    imports: Vec<ImportDeclaration>,
    roots: Vec<RootDeclaration>,
    declarations: Vec<Declaration>,          // the type table — public + local
}
// NOTA form (Public Name Value) — a data-carrying variant, name then value (record 1226)
pub enum Declaration { Public(Name, TypeValue), Private(Name, TypeValue) }
pub enum TypeValue {
    Newtype(TypeReference),                  // (Public Topic { String }) — transparent wrapper (record 1235)
    Struct(Vec<(Name, TypeReference)>),      // a STRUCT IS a key-value map: field name → type (record 1226)
    Enum(Vec<Variant>),                      // variants
}
pub enum TypeReference {
    String, Integer, Boolean, Path,          // scalar built-ins (reserved, not Plain names)
    Plain(Name),                             // a declared type: Topic, Entry, …
    Vec(Box<TypeReference>), Optional(Box<TypeReference>), Map(Box<MapReference>),
}
```

In assembled NOTA the `TypeValue` variant is tagged explicitly — `(Struct
{ … })` / `(Newtype X)` / `(Enum [ … ])` — matching standard enum-variant
encoding. A **multi-field struct is a key-value brace map** (field name → type)
under the `Struct` tag; e.g. `Entry@{ @Topics  @Kind }` (using the `@Type`
derived-name shorthand, record 1232) lowers to `(Public Entry (Struct { topics
Topics  kind Kind }))`. A **newtype carries a single `TypeReference` under the
`Newtype` tag** — `Topic@String` or `Topic@{ String }` (both surface forms)
lowers to `(Public Topic (Newtype String))`, NOT `(Public Topic { text String
})` with a forced field name — and emits a tuple-struct `pub struct Topic(pub
String)` (record 1235), keeping the wrapper transparent.
**Visibility:** `Public` declarations are exported (the schema used as a
library); `Private` declarations — including **inline PascalCase types** logged
into the local-types table (sugar, [[428-at-sigil-declaration-syntax-spec]]) —
are module-local, not exported. Default is positional: top-level declarations
are public, inline ones private. The assembled schema is the state-machine
object holding this table.

Every type round-trips (1109); `.asschema` is NOTA + rkyv only (1110/1112). (The
live `asschema.rs` still has the older non-visibility `Vec<TypeDeclaration>` +
`input`/`output` shape; moving to roots + `Vec<Declaration>` with
`Public`/`Private` + struct-as-key-value is the operator migration this targets.)

## 5. Emission — derives over the shared codec, not a private reader

`schema-rust-next` emits ordinary Rust type definitions that **derive the shared
NOTA codec** ([[421-nota]] §3), instead of emitting a per-file reader:

```rust
#[derive(NotaRecord, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Entry { pub topic: Topic, pub kind: Kind, pub description: Description }

#[derive(NotaTransparent, rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct Topic(pub String);   // newtype stays transparent — NotaTransparent, not NotaRecord
```

So schema-generated and hand-written types are identical at the codec boundary —
one stack, three consumers (the engine's own `Asschema`, the generated types,
hand-written types). The newtype-vs-struct emission distinction
(`NotaTransparent` tuple-struct vs `NotaRecord` named struct) must survive even
though both are "structs."

## 6. Communication — traits on root objects

Cross-component features are an additional trait surface on the roots (see
[[423-signal-nexus-sema]]), not a separate object model:

```rust
pub trait SignalRoot: NotaEncode + NotaDecode + rkyv::Archive { fn short_header(&self) -> ShortHeader; }
pub trait RoutedMessage<Root> { fn origin_route(&self) -> OriginRoute; fn root(&self) -> &Root; }
```

Generated roots derive/receive impls for NOTA text, rkyv bytes, short-header
triage, origin-route tracking, and upgrade traits. One data object; the traits
state which surfaces it participates in.

## 7. The pipeline, macros, and what is gone

```text
.schema  →  read_syntax  →  SyntaxSchema  →  assemble  →  Asschema  →  emit_rust  →  Rust module
```

Each arrow is a method on the data-bearing noun (`RawSchemaFile::read_syntax`,
`SyntaxSchema::assemble`, `Asschema::emit_rust`) — no free-function helper layer.

**Macros are open.** With the type vocabulary native to Schema and declarations
being pipe forms, whether a separate user-macro system is needed, and at what
level, is unresolved (psyche 2026-05-28) — do not build macro machinery until
confirmed.

**Gone:** the `@`/`*` macro sigils (1122); the flat `(KeyValue K V)` shape
(1085); the hand-rolled line-format `.asschema`/`.witness.txt` (1110/1112).
**Live gap (operator migration):** move the codec into `nota-next`, make
`Asschema` derive it, replace the per-file emitted reader with derives, and shift
the assembled model to roots + scalar-floor + newtype-as-struct.

## 8. Testing — schema and assembled fixtures (record 1180)

A `.schema` fixture is lowered and checked against its `.asschema` golden — both
real files, loaded with `fixture!` ([[421-nota]] §7), never inline source. The
authored fixture shows the rules in one place: PascalCase type declarations,
camelCase fields, pipe forms, `(Vec …)` composites, scalars, declare-before-use:

```nota
; tests/fixtures/spirit.schema   — root: Spirit (from the filename)
Topic        String
Topics       (Vec Topic)
Description  String
Kind         (| Kind Decision Principle Correction |)
Entry        {| Entry topics Topics kind Kind description Description |}
Query        {| Query topics Topics limit (Optional Integer) |}
RecordSet    {| RecordSet records (Vec Entry) |}
```
```nota
; tests/fixtures/spirit.asschema   — the macro-free assembled golden (plain NOTA)
([example:spirit] [0.1.0]) [] []
[(Newtype [Topic [[text String]]])
 (Newtype [Topics [[items (Vec (Plain Topic))]]])
 (Enum    [Kind [[Decision Unit] [Principle Unit] [Correction Unit]]])
 (Struct  [Entry [[topics (Plain Topics)] [kind (Plain Kind)] [description (Plain Description)]]])
 (Struct  [Query [[topics (Plain Topics)] [limit (Optional Integer)]]])
 (Struct  [RecordSet [[records (Vec (Plain Entry))]]])]
```
```rust
#[test]
fn spirit_schema_lowers_to_golden() {
    let asschema = SchemaEngine::default().lower(fixture!("spirit.schema")).unwrap();
    assert_eq!(asschema.to_nota(), fixture!("spirit.asschema").trim());   // golden is itself NOTA
}
```

The `.schema` is the authored source; the `.asschema` is the plain-NOTA data it
must lower to (scalars as bare `String`/`Integer`, declared types as `(Plain
Name)`, composites as `(Vec …)`/`(Optional …)`). The assertion is the
lowering contract, and the golden round-trips back through `Asschema::from_nota`.
