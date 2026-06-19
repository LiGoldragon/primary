# 432 — operator feedback on designer 696 impl-reference syntax

## Scope

Audited Designer's `schema-next` branch `next/impl-reference-syntax` at commit
`b9689f4f` against report `reports/designer/696-impl-reference-prototype.md`.
The branch is one real commit ahead of schema-next main and leaves an empty
working-copy commit on top.

This is an audit, not a main integration. I did not edit schema-next.

## Verification

Commands run in
`/home/li/wt/github.com/LiGoldragon/schema-next/impl-reference-syntax`:

```sh
cargo fmt --check
cargo test --test impl_catalog
cargo clippy --all-targets -- -D warnings
cargo test
```

Observed results:

- `cargo fmt --check`: clean.
- `cargo test --test impl_catalog`: 13 passed.
- `cargo clippy --all-targets -- -D warnings`: clean.
- `cargo test`: 189 passed, 0 failed, matching Designer's count.

## Findings

### P1 — standalone impl blocks can target no schema type

The report says the body-optional form `TypeName {| ... |}` is for "impls for
an elsewhere-declared type." The implementation does not enforce that. In
`src/source.rs:808`, `SourceNamespaceEntry::to_impl_block` creates an
`ImplBlock` from `self.declaration_name(namespace)` and the catalog without
checking that the target resolves to a namespace declaration, root type, or
import.

The fixture confirms the gap rather than closing it:
`tests/fixtures/impl-catalog/body-optional.schema:5` is just:

```schema
StatementText {| Display (word_count {} Integer) |}
```

There is no `StatementText` declaration or import in the fixture, and the test
at `tests/impl_catalog.rs:311` asserts that no type declaration is minted. So
the proven behavior is not "attach impls to an existing type"; it is "accept a
free-standing catalog keyed by an arbitrary PascalCase name."

Before main integration, the branch needs a target-resolution witness:

- positive: `StatementText String` plus `StatementText {| Display |}` attaches
  to the existing type;
- positive: an imported/root target works if the design allows it;
- negative: `MissingType {| Display |}` fails with a typed error before a
  `RustSurface` can make it look valid.

### P1 — macro path still drops the catalog

The branch intentionally keeps only the typed source-archive path carrying the
catalog. The macro/document path accepts and segments `{| |}`, but drops the
impl block in `src/engine.rs:860`: `key_value_pairs` pushes only entries with
`definition`, and `NamespaceEntry` holds only `name` and `definition`
(`src/engine.rs:914`). The comment at `src/engine.rs:856` states that
body-optional entries mint no declaration and are dropped.

This is honest prototype scope, but not main-ready if `SchemaEngine::lower_source`
remains a public lowering path. Production module loading appears to use
`SchemaModuleSource::lower` -> `lower_schema_source`, so the normal package path
probably gets the catalog; the public convenience path still returns a semantic
`Schema` with empty impl catalogs for the same text.

Before main integration, either route `lower_source` through `SchemaSource` for
this syntax or make the no-catalog macro path an explicit non-catalog API. The
cleaner shape is parity: one schema text should not produce two semantic schemas
depending on which public lowerer read it.

### P2 — trait names in `{| |}` are not case-validated

`SourceImplCatalog::from_block` treats any non-parenthesized atom as a trait
name (`src/source.rs:1016`) and immediately constructs a `Marker` or `TraitImpl`.
Unlike method names and method parameter types, there is no
`SourceIdentifierCase::is_type()` validation for trait names.

That permits lowercase marker names in the schema source at a position that is
supposed to name a Rust trait/type role. The fix is small: validate trait names
as PascalCase type identifiers and add a negative test such as
`RecordIdentifier String {| display |}`.

### P2 — the missing-method error reports only the method name

The verifier compares full `MethodSignature` values, but on failure it stores
only `signature.name()` in `SchemaError::UnverifiedImplReference`
(`src/schema.rs:1432`). The doc comment at `src/schema.rs:1381` and the test
message at `tests/impl_catalog.rs:418` say the error names the exact signature.
It currently names only `matches`.

For the real crate surface builder, this should render the canonical method
signature, including parameter and return references. That makes a
parameter/return mismatch diagnosable instead of collapsing all failures for a
method name into one message.

### P2 — duplicate standalone blocks are not rejected

Because body-optional entries do not mint declarations, there is no duplicate
check for repeated standalone impl blocks targeting the same type. Two
`StatementText {| ... |}` entries would produce two `ImplBlock`s for the same
target and `Schema::referenced_impls()` would union them. That may be acceptable
only if duplicate blocks are intended to compose. If the intended model is one
catalog per target, this needs a typed duplicate-target error.

## What is good

The important parser change is real: a trailing pipe-brace is a separate root
object, so replacing `chunks_exact(2)` with stateful cursor walks is the right
move. The branch also does the useful thing by making the catalog typed and
rkyv-archivable rather than parser-only state.

The verification seam is directionally right. `RustSurface::verify_catalog`
turns the schema catalog into a checkable trust boundary instead of trusting the
source text. The negative tests for absent trait and absent method facts are
valuable and should survive integration after the exact-signature diagnostic is
fixed.

## Integration recommendation

Do not merge `next/impl-reference-syntax` to schema-next main as-is. Harvest it
as a strong prototype, but make the next operator slice:

1. enforce standalone target resolution;
2. make `lower_source` and `lower_schema_source` semantically agree for impl
   catalogs;
3. validate trait names;
4. improve the missing-method diagnostic to print the canonical signature;
5. decide duplicate standalone block semantics and test the decision.

After those fixes, the branch is a good base for the real crate-surface builder
and later method-call resolver.
