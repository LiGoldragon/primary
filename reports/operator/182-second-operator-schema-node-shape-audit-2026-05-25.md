# 182 - Second-operator schema node-shape audit

Kind: Operator audit + corrective implementation report  
Topic: second-operator schema macro pipeline work and operator follow-up branch  
Date: 2026-05-25  
Lane: operator

## Bottom line

Second-operator's mainline port is directionally strong. `nota-codec` main now
has the `NotaValue` tree and shape methods, and `schema` main now has the
six-position `SchemaDocument`, a `MacroIndex`, and a `MacroPipeline` that
lowers the live Spirit schema through `NotaValue` shape dispatch.

The flaw I found is architectural, not an immediate wrong-result bug:
`schema` still hid the structure-match boundary for namespace values in a
private `TypeMicroMacro` and collapsed `Record` and `Newtype` into the same
private `RecordOrNewtype` branch before transformation. That weakens the
current design's load-bearing claim from `reports/second-designer/189`:
structure-match should return an explicit classification tag, and the
transformation macro should consume that tag.

I implemented the correction on a separate worktree branch:

- Worktree: `/home/li/wt/github.com/LiGoldragon/schema/operator-node-shape-boundary`
- Bookmark: `operator/node-shape-boundary`
- Commit: `2288914c` — `schema: expose node-shape macro boundary`

## What second-operator landed correctly

The schema repo's `main` now contains the important pieces second-operator
described in `reports/second-operator/189-schema-engine-running-model-2026-05-25.md`:

- `SchemaDocument::from_six_values` validates the six positional `.schema`
  fields.
- `MacroIndex::from_document` indexes imports, headers, namespace values, and
  features before lowering.
- `MacroPipeline::run` walks indexed candidates in source/precedence order and
  lowers through `BuiltinMacroVariant` and `LoweringContext`.
- The live Spirit fixture is tested for byte-equivalence against the canonical
  parser path.

That is a real advance. The implementation is not just report-shaped; it is
executable and Nix-tested.

## Flaw

The public macro contact point stopped one step too late.

Before my branch, the type recognizer did this:

```rust
match TypeMicroMacro::from_value(value)? {
    TypeMicroMacro::Enum => ...
    TypeMicroMacro::RecordOrNewtype => ...
    TypeMicroMacro::Alias => ...
}
```

The problem is `RecordOrNewtype`. The design wants a structure-match phase that
classifies the node before transformation. A newtype and a record are different
macro shapes:

- `(String)` is a newtype declaration.
- `((state State))` is a one-field record declaration with a named field.
- `(Vec Topic)` is a newtype over a container expression.
- `((topic Topic) (kind Kind))` is a record declaration.

The old code eventually produced the correct assembled type for the existing
fixture, but the classification was not visible as a public shape boundary and
had no direct tests. That left the most important macro-system invariant
protected only by successful end-output equivalence.

## Correction implemented

I added `src/node_shape.rs` with two public enums:

```rust
pub enum NodeDefinitionShape {
    ImportDirective,
    HeaderRoot,
    NamespaceValue(NamespaceValueShape),
    FeatureItem,
    UpgradeRule,
}

pub enum NamespaceValueShape {
    Enum,
    Record,
    Newtype,
    Alias,
}
```

`NodeDefinitionShape::recognize(point, value)` now pairs the
`NodeDefinitionPoint` with the observed `NotaValue` shape. Namespace values are
classified explicitly into `Enum`, `Record`, `Newtype`, or `Alias` before
`TypeMacroRecognizer` transforms them.

The classifier has the subtle single-field rule the first failed Nix run
surfaced:

- `(String)` is `Newtype`.
- `(Vec Topic)` is `Newtype`.
- `((state State))` is `Record`, because the single inner record is a named
  field, not the newtype's one inferred expression.

I updated `ARCHITECTURE.md` to describe `NodeDefinitionShape` as the visible
macro boundary and removed the private `TypeMicroMacro` collapse from the
pipeline.

## Tests added

`tests/node_shape.rs` adds five constrained witnesses:

- `namespace_shape_recognizer_splits_enum_record_newtype_and_alias`
- `container_namespace_value_is_a_newtype_shape`
- `single_named_field_namespace_value_is_a_record_shape`
- `node_shape_error_reports_definition_point_and_value_kind`
- `multi_pass_pipeline_accepts_all_public_namespace_shapes`

These tests intentionally prove the boundary, not only the final assembled
output. The error test checks that a bad shape names both the schema point
(`HeaderRoot`) and the observed NOTA kind (`Sequence`), which makes the
macro-dispatch failure visible to future macro authors.

## Verification

Ran from the operator worktree with the remote builder:

```sh
nix flake check --option max-jobs 0 --print-build-logs
```

Result: all checks passed. The log showed every check building on
`ssh-ng://nix-ssh@prometheus.goldragon.criome`, satisfying the max-jobs-0
builder rule.

## Recommendation

Merge `operator/node-shape-boundary` into `schema` main unless designer objects
to the naming. It does not replace second-operator's work; it tightens the
macro boundary that their implementation made possible.

The next useful slice is to reuse `NodeDefinitionShape` at the import/header/
feature recognizer boundaries too, so every builtin macro starts from the same
point-plus-shape recognition surface instead of each recognizer spelling its
own first error.
