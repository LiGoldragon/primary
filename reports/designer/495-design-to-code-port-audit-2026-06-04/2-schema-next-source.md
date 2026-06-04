---
title: "Schema-next source audit — SymbolPath, header resolution, alias lowering, dual-path divergence"
role: designer
variant: Audit
date: 2026-06-04
topics: [schema-next, SymbolPath, multi-pass-parsing, alias-lowering, header-public-interface, constraint-witnesses]
description: >
  Slice-2 completeness-and-quality audit of the schema-next lowering engine against
  recent psyche intent (records 1506/1507 symbol paths, 1555/1556/1562 header
  resolution + multi-pass, 1560/1561 alias-vs-newtype, 1565 constraint witnesses).
  Finds a load-bearing divergence: bare-header-name resolution and multi-pass
  reference resolution live ONLY on the SchemaSource path; the registry document
  path (lower_source — what every test and the README use) silently drops the
  payload. Alias/newtype lowering is complete and well-witnessed. SymbolPath shape
  is correct but its canonicality is unproven (no downstream consumer). The two
  parallel lowering engines (source.rs vs engine.rs+declarative.rs) are the
  dominant missing-abstraction smell.
---

# Slice 2 — schema-next source audit

`schema-next` (repo `/git/github.com/LiGoldragon/schema-next`) lowers NOTA
structure into `Asschema`, the macro-free assembled-schema endpoint. It does
NOT emit Rust. The operator has landed typed `SymbolPath`s, bare-header
namespace resolution, and alias-vs-newtype lowering. This audit asks, per the
psyche directive, how complete each landed mechanism is versus the full intent,
what edge or constraint is missing, and what bad patterns the lowering passes
carry.

The headline finding is a behavior divergence between two parallel lowering
engines that share no code: the registry document path
(`SchemaEngine::lower_source` / `lower_document`) and the typed-source path
(`SchemaSource::lower` → `to_asschema`). Recent intent (multi-pass header
resolution) is implemented on only one of them, and it is NOT the one the test
suite and README exercise.

## Pipeline shape — two engines, one named in docs

`src/engine.rs` builds a `MacroRegistry` and lowers a `nota_next::Document`
through position-aware macro handlers (`RootEnumMacro`, `RootNamespaceMacro`,
`KeyValueDeclarationMacro`, …) into `Asschema`. `src/source.rs` builds a typed
`SchemaSource` value (`SourceRootEnum`, `SourceNamespace`, `SourceStructBody`,
`SourceEnumBody`, `SourceReference`) and lowers it through
`SchemaSource::to_asschema`. Both end at the same `Asschema` type, but the two
implementations are wholly separate code.

The intent says schema lowering is multi-pass: [the source reader first
preserves authored objects, then collects candidate type names from namespace
entries and inline root declarations, then resolves variant payload shorthand
against that namespace before producing assembled schema] (record 1556). That
pass-1-collect / pass-2-resolve discipline exists in `source.rs`:

`src/source.rs:106-126` (`to_asschema`):
```rust
let resolver = SourceTypeResolver::from_source(self);                 // pass 1: collect names
let mut namespace = SourceLoweredNamespace::from_source(&self.namespace, &resolver)?;
namespace.push_public_declarations(self.input.public_inline_declarations(&resolver)?)?;
namespace.push_public_declarations(self.output.public_inline_declarations(&resolver)?)?;
let input = self.input.to_asschema_enum(&namespace)?;                 // pass 2: resolve
let output = self.output.to_asschema_enum(&namespace)?;
```

`SourceTypeResolver::from_source` (`src/source.rs:965-975`) collects every
namespace name plus the inline-declaration names from both root enums up front,
so a bare header variant can reference a namespace type declared later in the
file. This is genuine multi-pass resolution and matches record 1556.

The registry document path has no such resolver. `AssembledVariant::lower`
(`src/declarative.rs:1839-1854`) lowers a bare PascalCase variant straight to
`payload: None`:
```rust
} else if self.object.qualifies_as_pascal_case_symbol() {
    Ok(EnumVariant {
        name: self.object.schema_name()?,
        payload: None,
    })
}
```

There is no namespace lookup, no resolver, no forward-reference pass.

## The divergence is observable, not theoretical

I lowered the same source through both paths (probe since removed):

```
source = "{}\n[Lookup]\n[]\n{\n  Lookup RecordIdentifier\n  RecordIdentifier Integer\n}"

ENGINE lower_source: variant=Lookup payload=None
SOURCE  path:        variant=Lookup payload=Some("Lookup")
```

For an identical schema, the registry path drops the header payload and the
source path resolves it. The intent [root input/output headers may list
exported variant object names directly; when a bare root variant name resolves
to a declaration in the schema namespace, the variant carries that same-named
payload type] (records 1555/1562) is implemented on exactly one of the two
paths.

Why the green test suite hides this:

- The header-resolution witnesses
  (`tests/source_codec.rs:48` `root_header_bare_names_resolve_to_exported_namespace_payloads`
  and `:92`) call `SchemaSourceArtifact::from_schema_text(...).source().lower(...)`
  — the SOURCE path.
- The equivalence witness
  (`tests/source_codec.rs:26` `schema_source_lowers_to_same_asschema_as_direct_source`)
  asserts `lower_source` (registry) == `source().lower()`, but its fixture
  (`tests/fixtures/spirit-crate/schema/lib.schema`) uses only explicit
  `(Record Entry)` payload forms — never a bare header name — so the two paths
  agree there by construction.
- `tests/symbol_path.rs`, `tests/lowering.rs`, and most of
  `tests/design_examples.rs` use `lower_source` (registry) with explicit
  payloads, sidestepping the gap.

The only production caller is `SchemaModuleSource::lower`
(`src/module.rs:102-104`), which goes through `lower_schema_source` (the source
path). So production gets header resolution; the documented Pipeline path and
the entire test surface do not. The ARCHITECTURE.md "Pipeline" section
(`ARCHITECTURE.md:5-16`) describes ONLY the registry path; the header
resolution prose at `ARCHITECTURE.md:45-53` describes ONLY the source path, and
nothing flags that the registry path lacks the behavior. A reader following the
Pipeline section would conclude header resolution is universal. It is not.

This is the heart of the record-1565 ask — [audit implementation against intent
for missing constraint witnesses; add tests that prove the intended path] — and
the missing witness is precisely the one that would have caught this: an
assertion that BOTH lowering paths produce the same payload for a bare header
name.

## SymbolPath — correct shape, unproven canonicality

The intent: [schema symbol identity is a typed path, not a free text
convention; SymbolPath is assembled-schema data over Name segments; it derives
paths from known positions; it round-trips through NOTA and rkyv as a vector of
names rather than an opaque slash-delimited string] (INTENT.md + records
1506/1507).

Landed shape (`src/asschema.rs:85-86`):
```rust
pub struct SymbolPath(Vec<Name>);
```

A flat `Vec<Name>`, not a structured `{component, plane, variant, …}` record.
The structured role is recovered separately by `SymbolPathPosition`
(`src/asschema.rs:88-105`, a four-variant borrow enum) via
`Asschema::symbol_path_position` (`:332-375`), which validates the component
segment and classifies the local path against the owning schema. This is the
right call: [the stored path stays a segment vector so deeper schema positions
can grow without changing the binary object] (ARCHITECTURE.md:130-135), and
role is data-derived from the schema rather than guessed from segment count.
The NOTA/rkyv round-trip is well-witnessed
(`tests/symbol_path.rs:157` and `:178` reject the opaque slash-string body).

Two completeness gaps against the FULL intent:

1. **Canonicality is asserted in prose but unproven in code.** Records
   1506/1507 frame the path mechanism as [canonical, not per-design] and as
   [schema-emitted Rust types and NOTA renderings are two projections of one
   symbol-path identity space]. In schema-next today, `SymbolPath` is
   constructed and consumed ONLY inside `src/asschema.rs` and exercised ONLY by
   `tests/symbol_path.rs` (confirmed: no other `src/*.rs` references it). The
   trace/help/indexing/emission consumers that would make it the universal
   identity live downstream (schema-rust-next, runtime). So the canonical-
   identity claim is correct-but-latent here. Classify: OPERATOR-ACTIVE /
   downstream — the witness that proves canonicality (a consumer reading symbol
   paths) belongs to schema-rust-next, not this repo.

2. **Position recovery requires the owning Asschema.** A bare `SymbolPath`
   cannot report its own role; `symbol_path_position` takes `&self` on
   `Asschema`. That matches the design intent (role is schema-derived), so it
   is not a defect — but it means a `SymbolPath` handed across a boundary
   without its schema is role-opaque. If downstream trace/help needs role
   without the schema, the segment vector alone is insufficient. Worth noting
   for the schema-rust-next slice, not a schema-next gap.

The four constructors `type_path` / `root_variant_path` / `field_path` /
`enum_variant_path` (`src/asschema.rs:138-164`) all funnel through
`from_identity_and_segments` (`:112-119`), so the construction is not
duplicated — good.

## Alias-vs-newtype lowering — complete and well-witnessed

The intent: [bare namespace bindings such as `Rejected SignalRejection`,
`Topic String`, and `Topics (Vec Topic)` lower to `TypeDeclaration::Alias`, not
to tuple newtypes; a brace body that lowers to exactly one field is a Newtype]
(records 1560/1561).

Source-side flow is clean. `SourceDeclarationValue::to_declaration_group`
(`src/source.rs:412-427`) sends a bare `Reference` straight to `Alias`:
```rust
Self::Reference(reference) => Ok(SourceDeclarationGroup::primary(
    TypeDeclaration::Alias(AliasDeclaration::new(name, reference.to_type_reference())),
)),
```
and `SourceStructBody::to_declaration_group` (`src/source.rs:463-481`) picks
Newtype vs Struct on field count:
```rust
let primary = if fields.len() == 1 {
    TypeDeclaration::Newtype(NewtypeDeclaration::new(name, fields[0].reference.clone()))
} else {
    TypeDeclaration::Struct(StructDeclaration::new(name, fields))
};
```

`AliasDeclaration` and `NewtypeDeclaration` (`src/asschema.rs:625-656`) are
distinct types, both `{name, reference}`, so the alias/newtype distinction is
carried in the type system, not a flag. The `TypeDeclaration` enum
(`src/asschema.rs:579-584`) has all four arms. The witnesses are strong:
`tests/lowering.rs:73` (`bare_reference_declarations_lower_to_aliases`),
`:94` (`single_field_brace_declarations_lower_to_newtypes`), `:113`
(`single_field_inline_pascal_declarations_lower_to_newtypes`), and
`tests/source_codec.rs:82` proves a bare header binding lowers to `Alias`. This
mechanism is DONE.

One open edge: the single-field→Newtype rule is implemented twice (see bad
patterns below), so a future change to that rule must be made in two places or
the paths diverge — the same class of latent divergence as the header bug.

## Bad patterns

### 1. Two parallel lowering engines (dominant missing-abstraction smell)

The single most consequential smell. `source.rs` and `engine.rs`+`declarative.rs`
each implement the full authored-schema → asschema lowering, with no shared
core:

| Concept | Source path (`source.rs`) | Registry path (`declarative.rs`/`engine.rs`) |
|---|---|---|
| single-field → Newtype | `SourceStructBody::to_declaration_group` :475 | `AssembledStructBody::lower_type` :1554 |
| multi-field → Struct | same, :478 | same, :1561 |
| bare ref → Alias | `SourceDeclarationValue` :418 | `KeyValueDeclaration::lower_newtype` engine.rs:571 |
| `(Vec T)`/`(Optional T)`/`(Map …)` | `SourceReference::from_record` :879 | `AssembledReference::lower_object` :1903 + `TypeReference::from_parenthesis_objects` asschema.rs:1100 |
| enum variant lowering | `SourceVariantSignature::to_enum_variant` :761 | `AssembledVariant::lower` :1839 |
| header bare-name resolution | YES (`SourceTypeResolver`) | **NO** |

The divergence in the last row is the bug; the rest is duplicated logic waiting
to diverge next. Per [repeated nested variant-wrapper construction signals bad
design or a missing logic/emission layer] (record 1557), generalized in
`skills/abstractions.md` §"repetition resolves into a named pattern": the
collection-reference lowering (`Vec`/`Optional`/`Map` head dispatch) appears in
THREE places — `source.rs:893-900`, `declarative.rs:1919-1931`, and
`asschema.rs:1106-1131` — each a slightly different spelling of the same
head-match. The missing abstraction is a single reference-lowering owner that
both engines call.

The cleanest dissolution: make `SchemaSource` the one lowering front-end (it
already owns multi-pass resolution and is the only production caller), and
retire `lower_source`/`lower_document`/`AssembledVariants`/`AssembledFields` as
a second engine — or, if the registry path must stay for macro execution, route
its root-enum and namespace lowering THROUGH `SchemaSource` so header resolution
and the single-field→Newtype rule have exactly one home.

### 2. Single-field→Newtype rule duplicated verbatim

`src/source.rs:475-479` and `src/declarative.rs:1554-1565` are the same
`if fields.len() == 1 { Newtype } else { Struct }` decision. Also a third
spelling inside `TypeReference::from_inline_struct` (`src/asschema.rs:1062-1072`).
Three copies of one rule. Abstraction proposal: a `FieldSet` (or method on the
existing field collection) that owns `into_type_declaration(name)` and decides
Newtype-vs-Struct once; all three call sites delegate.

### 3. `Name::field_name` case conversion is logic without a clear owner edge

`Name::field_name` (`src/asschema.rs:41-56`) hand-rolls PascalCase→snake_case.
It is a method on `Name` (correct owner), but the same lowercase-first-char
predicate is reimplemented as `SourceIdentifierCase::is_type`
(`src/source.rs:1120-1126`), `SourceVariantName::is_valid`
(`src/source.rs:843-849`), and `AssembledFields::starts_ambiguous_pascal_pair`
(`src/declarative.rs:1635-1646`). Four ad-hoc "is this PascalCase / is this a
type name" checks. Abstraction proposal: a single `AtomCase`-style predicate on
`Name` (`Name::is_type_name`, `Name::is_field_name`) — note `nota_next` already
exports `AtomCase`/`AtomClassification` (used at `asschema.rs:58`), so the owner
may already exist upstream; consolidate onto it.

### 4. Naming — abbreviations are absent; no crate-prefix violations

Identifiers are clean full-English-word throughout (`registry`, `context`,
`declaration`, `reference`, `identity`, `namespace`). No `ctx`/`tok`/`cfg`.
The `Source*` prefix on `source.rs` nouns (`SourceRootEnum`, `SourceNamespace`,
`SourceReference`) reads as a meaningful logical-plane qualifier (authored-
source-language vs assembled), not redundant ancestry — defensible. The
`Assembled*` prefix on `declarative.rs` nouns is the symmetric plane qualifier.
No naming defects found.

### 5. No free functions / ZST namespaces

Every function is a method on a data-bearing type or a trait impl; `fn main`
is absent (library crate). The small notation/diagnostic helpers
(`SourceRawNotation`, `SchemaNodeNotation`, `DelimitedNotation`) are real
borrow-newtypes carrying a `&Block`/`Delimiter`, not ZST namespaces — they pass
the erase-the-name test. No methods-on-types violations found.

## Constraint-witness inventory (record 1565)

| Invariant | Intent | Witness | State |
|---|---|---|---|
| bare ref binding → Alias | 1560/1561 | `tests/lowering.rs:73`, `source_codec.rs:82` | WITNESSED |
| single-field brace → Newtype | 1560 | `tests/lowering.rs:94`, `:113` | WITNESSED |
| header bare name resolves through namespace (source path) | 1555/1562 | `tests/source_codec.rs:48` | WITNESSED (source path only) |
| header bare name resolves (registry path) | 1555/1562 | none | **MISSING — and the behavior is absent** |
| both paths agree on bare-header payload | 1556 | `source_codec.rs:26` (fixture has no bare header) | **MISSING — gap hidden by fixture choice** |
| multi-pass forward reference (namespace type declared AFTER header use) | 1556 | none (existing tests declare namespace, but no test isolates forward-vs-backward order) | **MISSING** |
| SymbolPath NOTA/rkyv round-trip as names | 1506/1507 | `tests/symbol_path.rs:157`, `:178` | WITNESSED |
| SymbolPath role recovered from schema | 1506/1507 | `tests/symbol_path.rs:66` | WITNESSED |
| SymbolPath as canonical cross-consumer identity | 1507 | none in this repo | OPERATOR-ACTIVE (downstream) |

## Manifestation gaps (INTENT.md / ARCHITECTURE.md)

INTENT.md (322 lines) and ARCHITECTURE.md (444 lines) are well-maintained and
already capture multi-pass lowering (INTENT.md:204-207), header-as-exported-
vocabulary (INTENT.md:195-202), and the SymbolPath typed-identity shape
(INTENT.md:107-113). Two recent-intent deltas are genuinely missing:

1. **Record 1555 "header variants are the component public type interface."**
   Neither file states the framing that [every PascalCase name in the schema
   header becomes an exported top-level type library consumers import]. The
   header is described as "exported operation vocabulary" but not as the public
   TYPE interface that downstream crates `import`. Tier-1 doc delta proposed
   below.

2. **The dual-path divergence is undocumented.** ARCHITECTURE.md's Pipeline
   section describes the registry path as THE pipeline and the header-
   resolution section describes the source path, with no note that they differ.
   At minimum the docs must state which path is canonical and that header
   resolution is source-path-only (until the code is unified). Tier-1 doc delta
   proposed below.

The SymbolPath-canonical (1507) and two-projections-of-one-identity-space
framing is downstream-facing; I do NOT propose porting it into schema-next's
docs, since schema-next has no emission/consumer side to manifest it against.
