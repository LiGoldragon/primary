# Operator Proposal 350 - Schema Inline Declaration Scope Implementation

Target: make terse root inline declarations production-ready by promoting
reusable inline field declarations into the source namespace, while rejecting
duplicate declarations by name.

Recorded intent:

- Spirit record `tbff`: inline declarations inside root input/output payloads
  should enter source type scope and library export surface.
- Spirit record `3don`: duplicate declarations for the same type name are an
  error, not an override or merge.

## Desired Semantics

This source shape should be legal:

```nota
[(Record { Topic String Description String })
 (Select [(ByTopic { Topic * }) (ByKind { Kind * })])
 Version]
[(Recorded { RecordIdentifier (Bytes 12) DatabaseMarker * })]
{
  Kind [Decision Constraint]
  CommitSequence Integer
  StateDigest (Bytes 8)
  DatabaseMarker { CommitSequence * StateDigest * }
}
```

Meaning:

- `Record` is a public input payload type.
- `Topic` and `Description` are public newtype declarations introduced at first
  use inside `Record`.
- `Select` is a public input payload enum.
- `ByTopic` and `ByKind` are private operation-local helper payloads.
- `ByTopic { Topic * }` resolves `Topic` to the same public type introduced by
  `Record { Topic String ... }`.
- `Recorded` is a public output payload type.
- `RecordIdentifier` is a public newtype introduced by
  `Recorded { RecordIdentifier (Bytes 12) ... }`.
- The trailing namespace can refer to `Topic`, `Description`, or
  `RecordIdentifier` even though they are declared inline above.
- Library consumers see the promoted public types in the schema namespace.

The important non-rule: this is not "first inline declaration wins." The whole
source declares a single symbol table. If two source positions introduce
`Topic`, schema lowering fails.

## Current Implementation

Relevant code is in `/git/github.com/LiGoldragon/schema-next/src/source.rs`.

Current pieces already exist:

- `SourceField::to_lowered_field` treats a PascalCase field with an explicit
  reference as a named inline declaration. `Topic String` lowers into a
  `Topic(String)` newtype plus a `topic: Topic` field.
- `SourceStructBody::to_declaration_group` returns private declarations plus a
  primary declaration.
- `SourceRootEnum::public_inline_declarations` hoists root variant inline
  payload declarations into the exported namespace.
- `SourceLoweredNamespace::push_declaration` already rejects duplicate names.

Current gap:

- Field-created declarations are always private because
  `SourceField::to_lowered_field` returns them as `private_declarations`.
- `SourceTypeResolver::from_source` only collects explicit namespace names plus
  root inline payload names (`Record`, `Select`, `Recorded`). It does not collect
  field-created names (`Topic`, `Description`, `RecordIdentifier`) as
  source-scope declarations.
- A public trailing namespace declaration can therefore reference a private
  inline type accidentally. That is wrong for library use.

## Proposal

Introduce an explicit source-scope lowering policy instead of letting every
inline declaration fall into "private helper" by default.

### Public Source-Scope Declarations

Promote these to public namespace declarations:

- Explicit trailing namespace entries.
- Root variant inline payload declarations: `Record`, `Select`, `Recorded`.
- PascalCase field declarations immediately inside a public root inline payload
  struct: `Topic String`, `Description String`,
  `RecordIdentifier (Bytes 12)`.

Keep these private by default:

- Operation-local enum helper payloads inside an inline root enum, such as
  `ByTopic` and `ByKind`.
- Deeper nested helper declarations. If a deeper noun needs to be exported,
  author it at the root payload level or in the trailing namespace.

This keeps the root concise without turning deeply nested operation details into
library API by accident.

### Whole-Source Symbol Table

Before lowering declarations, build a source declaration table:

```text
SourceDeclarationTable {
  public_names:
    explicit namespace names
    root inline payload names
    public root payload field declaration names

  private_names:
    operation-local helper names
    deeper nested helper names
}
```

Rules:

- Every name is unique across public and private declarations.
- Duplicate `Topic` anywhere is an error, even if one is public and the other is
  private.
- Reference resolution sees the whole table, not only earlier text.
- Public declarations must not depend on private declarations unless the private
  declaration is intentionally emitted in the same generated module and not part
  of the library API. For root payload field declarations, prefer promotion to
  public so public types have public field types.

### Lowering Flow

Replace the current one-pass shape:

```text
lower explicit namespace
push root inline public declarations
assemble roots
```

with a planned two-phase shape:

```text
parse Source AST
collect declaration table
reject duplicate names
lower explicit namespace declarations
lower public root inline declarations, including promoted field declarations
lower private helper declarations
assemble root enums using the completed namespace
```

This still keeps NOTA parse separate from schema interpretation. NOTA produces
blocks; schema builds the typed source AST; then schema lowers that AST with a
source-scope plan.

## Code Shape

Suggested implementation in `source.rs`:

- Add `SourceInlineVisibility`:

```text
PublicSourceScope
PrivateHelper
```

- Add `SourceDeclarationOrigin` for diagnostics:

```text
NamespaceEntry(name)
RootPayload(root = Input|Output, variant = Record)
RootPayloadField(root = Input|Output, variant = Record, field = Topic)
PrivateHelper(parent = Select, name = ByTopic)
```

- Add `SourceDeclarationTable`:

```text
names: Vec<SourceDeclaredName>
insert(name, visibility, origin) -> duplicate-name error if already present
resolver() -> SourceTypeResolver
```

- Teach `SourceStructBody` to collect and lower field declarations under a
  policy:

```text
to_declaration_group(name, resolver, field_inline_visibility)
```

Under `PublicSourceScope`, PascalCase field declarations produce public
declarations. Under `PrivateHelper`, they stay private.

- Change root inline lowering to call the public policy for direct root payload
  structs.
- Keep nested enum helper lowering on the private policy.
- Keep `SourceLoweredNamespace::push_declaration` duplicate protection as the
  final guard, but do not rely on it for diagnostics. The table should catch
  duplicate names earlier and report both origins.

## Duplicate Errors

These should fail:

```nota
[(Record { Topic String })]
[]
{ Topic String }
```

```nota
[(Record { Topic String })
 (Describe { Topic String })]
[]
{}
```

```nota
[(Select [(ByTopic { Topic String })])
 (Record { Topic String })]
[]
{}
```

The error should say the duplicate name and both origins. Existing
`DuplicateSourceDeclaration { name }` is enough behaviorally, but production
diagnostics should be upgraded to include origins once the source table exists.

## Tests

Add source-level tests in `schema-next/tests/source_codec.rs`:

- root payload field declarations are exported:
  `Record { Topic String Description String }` yields public `Topic`,
  public `Description`, public `Record`.
- later root inline payload references earlier inline field declaration:
  `ByTopic { Topic * }` resolves to `Topic`.
- trailing namespace references root inline field declaration:
  `Wrapper { Topic * }` is public and its field type is public `Topic`.
- duplicate inline plus namespace declaration errors.
- duplicate inline plus inline declaration errors.
- private helpers remain private:
  `ByTopic` is private while `Select` is public.

Add Rust emitter integration tests in `schema-rust-next` after the schema crate
lands:

- generated public `Record` has `pub topic: Topic`.
- generated `Topic` type is public.
- generated public namespace/API surface exposes `Topic` for dependent schemas.
- generated code does not expose `ByTopic` unless the existing emitter contract
  requires private helper types to be module-visible.

## Rollout

1. Land schema-next source table and tests.
2. Bump schema-next version if the source semantics are considered externally
   observable.
3. Update schema-rust-next to consume the visibility/public surface correctly if
   it currently treats private declarations as public.
4. Port schema-next and schema-rust-next fixtures to the compact root inline
   style.
5. Re-pin downstream crates deliberately.

## Pushback

The only design point I would avoid is order-dependent resolution. It is tempting
to say "`Topic *` picks up the earlier `Topic String`," but the production rule
should be stronger: `Topic *` resolves to the unique source declaration named
`Topic`, independent of whether the declaration appears before or after the
reference.

That makes reformatting and root-vector reordering non-semantic, and it makes
duplicate declarations a clear authoring error.
