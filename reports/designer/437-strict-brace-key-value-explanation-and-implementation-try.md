# 437 — Strict brace = key-value: explanation back, and the implementation try

*Kind: Architectural revision proposal · Topics: brace-strict-key-value, schema-syntax-revision, typed-key-enum, value-dispatched, derived-name-marker, honest-brace, schema-of-schema, lowering · 2026-05-30 · designer lane*

*Captures the rule you laid out reading 433 + `schema-next/schemas/core.schema` —
the NOTA brace is a strict key-value map, the current schema sugar
(`Entry@{ @Topics @Kind }`) violates that contract by using single-token
entries inside braces, and the fix is value-side markers + sigil-typed keys.
Spirit record 1259 (Decision, High). Reads as: what I heard you say, then the
implementation try. Connects to records 1126, 1127, 1128 (delimiter-as-structure
positional), 1226 (struct-as-key-value-map), 1232 (current `@Type` shorthand
that's being revised), 1235 (newtype as single-element brace — also touched by
this revision).*

## 1. What I heard you say (explanation back)

The architectural rule, restated:

> NOTA's brace `{ }` is a **strict key-value map**. Every entry inside the
> brace is exactly **two objects** — a key and a value. There are no
> single-token entries. The current schema sugar uses single tokens
> (`@Topics`, `@Kind`) inside the brace which is **dishonest about what the
> brace contract says**. To honor NOTA, every entry must be a pair, and the
> shorthand (derived field name = camelCase of key type-name) becomes a
> **value-side marker** instead of dropping the value entirely.

Then the deeper insight:

> The KEY inside the brace can be **typed** — its form (case, sigil) selects
> a variant of a typed Key enum. The VALUE is **dispatched** on the key's
> variant: different key variants admit different value types. So the brace
> is equivalent to `Vec<(KeyVariant, KeyVariant::Value)>` — a list of typed
> enum variants expressed in brace pair-rhythm rather than vector positional
> rhythm. **Sigils on the key are the variant tags.** Match on the key's
> sigil (or case) to determine what type the value should be read as.

The concrete consequence: schema's namespace + struct body + enum body all
need to be revised so they honor brace = key-value, and the `@Type` shorthand
moves from single-token-in-brace to a value-side `(Derive)` marker.

The verification you asked for ("is that possible? Do you understand?"):
**yes** — it's structurally clean, decodes mechanically, and the
NOTA-canonical form is `(Derive)` as a unit-variant marker in the
TypeReference enum. The implementation try follows.

## 2. What's wrong in `schema-next/schemas/core.schema` today

Looking at the actual file, three legacy-syntax violations:

```nota
; current core.schema (head)
Input@[]                                                  ; OLD top-level Name@ form
Output@[]                                                 ; OLD top-level Name@ form
{
  CoreSchema@{ @BuiltinMacroPositions @BuiltinMacroShapes @BuiltinMacroOutputs @BuiltinMacroDefinitions }
  ; ^^^ outer Entry@{ ... } is single-token; inner @Type entries are single-token
  Entry@{ @Topics @Kind @Description @Magnitude }          ; same pattern
  ; ...
}
```

Three distinct violations:

1. **Top-level `Input@[]` / `Output@[]`** — pre-record-1229 syntax. The
   root's input/output positions are **positional struct fields** (bare
   `[ … ]`), not declarations needing `Name@` prefixes. This was fixed in
   1229 but core.schema didn't catch up.
2. **`Name@{ … }` is single-token-in-brace at the outer level** — the
   namespace's brace contains `CoreSchema@{ … }` as one token. The brace's
   contract says key + value, two tokens.
3. **`@Topics` is single-token-in-brace at the inner level** — inside
   `Entry@{ … }`, the entries are `@Topics`, `@Kind`, etc. — single tokens.
   Same violation, at a different position.

(2) and (3) are the SAME structural issue (the `@Type` shorthand from records
1232 + 1235) — single tokens where brace contract requires pairs.

## 3. The cleaned-up namespace form

The schema's body is a sequence of four positional values (per record 1229):
imports, input, output, namespace. The **namespace** position is a brace,
which under the strict rule is:

```nota
{
  TypeName        TypeDefinition
  TypeName        TypeDefinition
  ...
}
```

Concretely, where `TypeDefinition` is a NOTA-tagged positional record naming
the variant — `(Newtype X)` / `(Struct { … })` / `(Enum [ … ])`:

```nota
; spirit.schema namespace, strict
{
  Topic           (Newtype String)
  Topics          (Newtype (Vec Topic))
  Description     (Newtype String)
  RecordIdentifier (Newtype Integer)
  Kind            (Enum [ Decision Principle Correction Clarification Constraint ])
  Magnitude       (Enum [ Minimum VeryLow Low Medium High VeryHigh Maximum ])
  Entry           (Struct { topics Topics  kind Kind  description Description  magnitude Magnitude })
  Query           (Struct { topicMatch TopicMatch  kind (Optional Kind) })
  RecordSet       (Newtype (Vec Entry))
}
```

Every entry is exactly TWO objects. Brace contract honored.

The previous `Topic@String` and `Topic@{ String }` (records 1232 + 1235) both
become `Topic (Newtype String)` — explicit, two-token, NOTA-canonical. The
`(Newtype X)` value form was already the canonical assembled-NOTA shape (per
operator 245); now it's also the AUTHORED form. Surface and assembled
converge.

## 4. The cleaned-up struct field body

A struct body inside `(Struct { … })` is a brace. Under the strict rule:

```nota
(Struct {
  fieldName     TypeReference
  fieldName     TypeReference
  ...
})
```

Concretely:

```nota
(Struct {
  topics            Topics
  kind              Kind
  description       Description
  magnitude         Magnitude
})
```

Every entry: two tokens. `camelCase fieldName  TypeReference`.

### The derived-name shorthand: value-side `(Derive)` marker

For the case where the field name would just be the camelCase of the type
name (the previous `@Topics` shorthand), the strict form is:

```nota
(Struct {
  Topics            (Derive)
  Kind              (Derive)
  Description       (Derive)
  Magnitude         (Derive)
})
```

**Key**: PascalCase symbol (the TYPE name).
**Value**: `(Derive)` — a unit-variant marker in the TypeReference enum.

The schema reader sees:
- Key is PascalCase → match `StructFieldKey::Derived(Name)` variant
- Value is `(Derive)` → confirm derived form
- Lower to: field name = camelCase(Name), type = `(Plain Name)`

Lowered assembled form (same as before):

```nota
(topics (Plain Topics))
(kind (Plain Kind))
(description (Plain Description))
(magnitude (Plain Magnitude))
```

Alternative shorthand sigils you mentioned (`*`, etc.): `(Derive)` is
NOTA-canonical because it's just an enum variant — no new symbol to teach
the parser. The schema reader checks the value: if it's `(Derive)` and the
key is PascalCase, apply the derivation. Otherwise the value is a normal
TypeReference.

### Mixed example: explicit + derived in the same struct

```nota
(Struct {
  Topics            (Derive)                ; derived: field `topics` of type `Topics`
  Kind              (Derive)                ; derived
  limit             (Optional Integer)      ; explicit: field `limit` of optional integer
  byTopic           (Map Topic RecordIdentifier)   ; explicit: field with composite type
})
```

Both forms coexist; the schema reader dispatches on the key's case.

## 5. The cleaned-up enum form (already correct, briefly)

Enum bodies use brackets `[ … ]`, not braces. Brackets are positional
vectors. So enum body doesn't have the key-value violation problem:

```nota
(Enum [
  Decision                              ; unit variant — bare PascalCase
  Principle                             ; unit variant
  Recording  Entry                      ; data variant — pair (Variant, Payload)
  Observing  Query
])
```

Wait — actually, looking at the spirit.schema's enum bodies, the current form is:

```nota
[ Record@Entry  Observe@Query  Remove@RecordIdentifier ]
```

Using `Variant@Type`. Under the strict rule, since `[ ]` is a vector (not a
brace), each entry is one positional value. A data variant is a pair, which
in vector position is `(Tag Payload)` — a positional record. So:

```nota
[ (Record Entry)  (Observe Query)  (Remove RecordIdentifier) ]    ; data variants, positional records
[ Decision  Principle  Correction ]                                 ; unit variants, bare PascalCase
```

Mixed:

```nota
[ (Record Entry)  Heartbeat  (Observe Query) ]                       ; mix unit + data variants
```

The `Variant@Type` shorthand inside brackets (from spirit.schema) can stay if
it lowers identically, but the canonical form is the positional-record one.
Cleanest: drop the `@` form here too.

For the **derived-name enum variant** (the `@Type` case from record 1232 inside
enums) — same value-side marker:

```nota
[ Entry  Query  RecordIdentifier ]               ; bare PascalCase — UNIT variants today
```

But unit variants and derived-name data variants look the same in NOTA at
this position. To distinguish, the derived-data form needs a marker too:

```nota
[ (Entry)  (Query)  (RecordIdentifier) ]         ; data variants with the type as both name and payload
                                                  ; lowers to (Record { name: Entry, payload: Plain(Entry) }) etc.
```

Or — alternative — use a marker variant:

```nota
[ (Entry Derive)  (Query Derive)  Decision ]      ; explicit Derive marker for data-derived, bare for unit
```

The `(Entry)` paren-with-just-PascalCase form is **already a NOTA enum
variant with no payload**, which under positional reading IS a unit variant.
So `(Entry)` ≡ `Entry` semantically. That gives a clash.

The cleaner solution: at an enum-body position, the `@Type` derived shorthand
becomes the SAME `(Tag Payload)` shape but with `Type` as both — `(Entry
Entry)`. Honest, positional, and unambiguous.

```nota
[ (Entry Entry)  (Query Query)  Decision ]      ; data variants with same name as type, plus a unit variant
```

This is verbose but explicit. Or keep `Variant@Type` as a vector-position
sugar — the violation is only inside braces. Open question for you at §10.

## 6. The key-as-enum, value-dispatched generalization

The deeper architectural insight: **at any brace position, the set of valid
keys is a typed enum** (the `KeyEnum` for that position). Each key variant
dispatches to a different value type.

In Rust pseudo-trait form:

```rust
trait BraceKey {
    type Value;    // the value type dispatched on this key variant
    fn from_nota_atom(atom: &Atom) -> Option<Self>;   // recognize the key's form
}
```

### At the namespace position

```rust
pub enum NamespaceKey {
    TypeDeclaration(Name),    // bare PascalCase symbol
    // future variants for imports, macros, re-exports — sigil-tagged
}

impl BraceKey for NamespaceKey {
    type Value = TypeDefinition;   // (Newtype X) / (Struct {…}) / (Enum [...])
}
```

The reader sees a key, asks NamespaceKey::from_nota_atom — if it's
PascalCase, it's a TypeDeclaration variant. Read the value as TypeDefinition.

### At the struct field position

```rust
pub enum StructFieldKey {
    Explicit(Name),    // camelCase — value is TypeReference
    Derived(Name),     // PascalCase — value is (Derive) marker; derive field-name as camelCase(Name)
}

impl BraceKey for StructFieldKey {
    type Value = StructFieldValue;
}

pub enum StructFieldValue {
    Reference(TypeReference),    // matches the Explicit variant
    Derive,                       // matches the Derived variant
}
```

The reader dispatches on case: PascalCase key → expect `(Derive)` value;
camelCase key → expect a TypeReference value.

### The pattern generalized

```rust
pub trait BracePosition {
    type Key: BraceKey;
}

pub struct BraceEntry<P: BracePosition> {
    pub key: P::Key,
    pub value: <P::Key as BraceKey>::Value,
}

pub fn parse_brace<P: BracePosition>(block: &Block) -> Vec<BraceEntry<P>> {
    block.entries_pairwise().map(|(key_atom, value_block)| {
        let key = P::Key::from_nota_atom(key_atom).expect("valid key for position");
        let value = <P::Key as BraceKey>::Value::from_nota_block(value_block).expect("valid value");
        BraceEntry { key, value }
    }).collect()
}
```

Each brace POSITION has a Key type; the Key's variant chooses the Value type.
The reader is purely mechanical: pair up the brace contents, parse key as
KeyEnum, parse value as the dispatched Value type.

### Match-on-key example

```rust
for entry in parse_brace::<StructFieldPosition>(&block) {
    let (field_name, type_ref) = match (entry.key, entry.value) {
        (StructFieldKey::Explicit(name), StructFieldValue::Reference(ref_)) => {
            (name, ref_)
        }
        (StructFieldKey::Derived(type_name), StructFieldValue::Derive) => {
            (Name::camelcase_of(&type_name), TypeReference::Plain(type_name))
        }
        (key, value) => return Err(SchemaError::KeyValueMismatch { key, value }),
    };
    fields.push((field_name, type_ref));
}
```

The case-on-key gives the SAME assembled-schema output for both forms; the
surface just chose between them by ergonomics.

## 7. The implementation try — Rust types + lowering

Combining §3-§6 into a minimum sketch the operator could implement:

```rust
// schema-next/src/asschema.rs additions

#[derive(NotaDecode, NotaEncode, rkyv::Archive, ...)]
pub enum TypeReference {
    String, Integer, Boolean, Path,
    Plain(Name),
    Vector(Box<TypeReference>),
    Optional(Box<TypeReference>),
    Map(Box<TypeReference>, Box<TypeReference>),
    Derive,                                       // NEW — the derived-field marker
}

// schema-next/src/syntax.rs additions

pub trait BraceKeyDispatch {
    type Value;
    fn classify_atom(atom: &Atom) -> Result<Self, SchemaError>;
}

pub enum NamespaceKey {
    TypeDeclaration(Name),
}

impl BraceKeyDispatch for NamespaceKey {
    type Value = TypeDefinition;
    fn classify_atom(atom: &Atom) -> Result<Self, SchemaError> {
        let name = Name::from_atom(atom)?;
        if name.is_pascal_case() {
            Ok(NamespaceKey::TypeDeclaration(name))
        } else {
            Err(SchemaError::InvalidNamespaceKey)
        }
    }
}

pub enum StructFieldKey {
    Explicit(Name),
    Derived(Name),
}

impl BraceKeyDispatch for StructFieldKey {
    type Value = StructFieldValue;
    fn classify_atom(atom: &Atom) -> Result<Self, SchemaError> {
        let name = Name::from_atom(atom)?;
        match name.case() {
            NameCase::Camel => Ok(StructFieldKey::Explicit(name)),
            NameCase::Pascal => Ok(StructFieldKey::Derived(name)),
            _ => Err(SchemaError::InvalidStructFieldKey),
        }
    }
}

pub enum StructFieldValue {
    Reference(TypeReference),
    Derive,
}
```

### Lowering, mechanical

```rust
fn lower_namespace_body(block: &Block, namespace: &mut Vec<Declaration>) -> Result<(), SchemaError> {
    for (key_block, value_block) in block.brace_pairs() {
        let key = NamespaceKey::classify_atom(key_block.expect_atom()?)?;
        let value = TypeDefinition::from_nota_block(value_block)?;
        let NamespaceKey::TypeDeclaration(name) = key;
        namespace.push(Declaration {
            visibility: Visibility::Public,    // default — sigils can adjust later
            name,
            value,
        });
    }
    Ok(())
}

fn lower_struct_body(block: &Block, fields: &mut Vec<(Name, TypeReference)>) -> Result<(), SchemaError> {
    for (key_block, value_block) in block.brace_pairs() {
        let key = StructFieldKey::classify_atom(key_block.expect_atom()?)?;
        let value = StructFieldValue::from_nota_block(value_block)?;
        let (field_name, type_ref) = match (key, value) {
            (StructFieldKey::Explicit(name), StructFieldValue::Reference(ref_)) => {
                (name, ref_)
            }
            (StructFieldKey::Derived(type_name), StructFieldValue::Derive) => {
                let field_name = Name::camelcase_of(&type_name);
                (field_name, TypeReference::Plain(type_name))
            }
            (StructFieldKey::Explicit(_), StructFieldValue::Derive) => {
                return Err(SchemaError::CamelCaseKeyWithDeriveValue);
            }
            (StructFieldKey::Derived(_), StructFieldValue::Reference(_)) => {
                return Err(SchemaError::PascalCaseKeyWithReferenceValue);
            }
        };
        fields.push((field_name, type_ref));
    }
    Ok(())
}
```

Mechanical, pure data, no Rust-side macro impls — the dispatch is just
`match` on the key's case + the value's variant.

## 8. Migration — what core.schema becomes

Current head of `schema-next/schemas/core.schema`:

```nota
Input@[]
Output@[]
{
  CoreSchema@{ @BuiltinMacroPositions @BuiltinMacroShapes @BuiltinMacroOutputs @BuiltinMacroDefinitions }
  Entry@{ @Topics @Kind @Description @Magnitude }
  ...
}
```

After the revision:

```nota
{}                              ; imports (positional, empty)
[]                              ; input (positional, empty bracket)
[]                              ; output (positional, empty bracket)
{                               ; namespace (positional, strict key-value brace)
  CoreSchema      (Struct {
                    BuiltinMacroPositions    (Derive)
                    BuiltinMacroShapes       (Derive)
                    BuiltinMacroOutputs      (Derive)
                    BuiltinMacroDefinitions  (Derive)
                  })
  Entry           (Struct {
                    Topics       (Derive)
                    Kind         (Derive)
                    Description  (Derive)
                    Magnitude    (Derive)
                  })
  Topic           (Newtype String)
  Kind            (Enum [ Decision Principle Correction Clarification Constraint ])
  ; ...
}
```

The four root-level values become `{}` / `[]` / `[]` / `{ … }` (positional,
bare per 1229). The namespace's brace honors key-value strictly. The struct
bodies inside the namespace honor key-value strictly. The enum bodies stay
brackets (no change needed).

Every brace is now legible as "this is a Map<TypedKey, DispatchedValue>"
— the strict reading the architectural rule demands.

## 9. What this changes about the macro layer (and report 436)

Report 436 §2 proposed `schemas/core.schema` as the next move for self-hosting
the macro vocabulary. **This revision is upstream of 436** — it changes what
core.schema can validly LOOK like before anything in 436 happens. The right
sequence:

1. **This revision (437)** lands first: strict brace contract enforced; `(Derive)`
   marker in TypeReference; lowering refactored to dispatch by key case.
2. **Then operator 255's plan (and 436)**: schemas/core.schema declares the
   macro type nouns in the strict-brace form; the macro vocabulary is generated
   from there. The macros themselves describe how the strict-brace forms lower
   — the dispatch logic in §7 above is what the bootstrap macros encode.

Without 437 first, the macro vocabulary in 436 would lock in the dishonest
brace forms; with 437 first, it locks in the honest forms. Order matters.

## 10. What I want you to confirm before the operator implements

A. **`(Derive)` as the value-side marker** — is this the right NOTA-canonical
   choice, or do you want a single-character sigil (`*`, `~`, `=`)? I think
   `(Derive)` is cleanest because it's just an enum variant; no new parser
   symbol. But it's verbose; if you prefer `*` for terseness, fine — the
   parser change is bounded.

B. **Sigils on namespace keys** (§6) — for now my sketch only has the bare
   PascalCase → TypeDeclaration variant. Do you want sigil-tagged variants
   for imports / re-exports / macro definitions at the namespace level
   already, or defer those until after 436?

C. **Enum body data variants** (§5) — do we revise enum-body too, requiring
   `(Variant Payload)` positional records for data variants and dropping
   `Variant@Type` from brackets? Or keep `Variant@Type` as vector-position
   sugar since the brace violation doesn't apply at bracket position?

D. **Root-level Input / Output cleanup** — the broken `Input@[]` / `Output@[]`
   in core.schema is a separate fix (record 1229 already settled it; core.schema
   just didn't catch up). Do that in this slice or split?

E. **`Name@{ Type }` newtype short form** (record 1235) — under strict brace,
   `Name@{ Type }` is still single-token-in-brace at the OUTER level (the
   namespace brace). The strict form is `Name (Newtype Type)`. Do you want
   `Name@{ Type }` retained as namespace-level sugar that lowers to the
   strict form, or dropped entirely?

Once these five are confirmed, the operator has a clean slice to implement.
The architectural rule (Spirit 1259) is firm; the surface choices in A-E are
ergonomic refinements I want your call on.
