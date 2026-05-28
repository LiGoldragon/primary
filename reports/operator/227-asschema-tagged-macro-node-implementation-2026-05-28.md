# 227 — ASSchema Tagged Macro Nodes and No-Sigil Macro Calls

## Frame

Psyche correction applied: macro invocation does not need a sigil. A macro
call is a tagged/data-carrying schema node at a position where the schema
expects a macro-capable node. Parenthesis means a known structured object:
the first object is the tag/variant, and the second object is the data carried
by that variant.

The implementation focus was deliberately ASSchema-first:

- represent macro calls as data before execution;
- keep `.asschema` as final NOTA data with no authored sugar;
- prove the old `@Vec` / `@Option` / `@KeyValue` surface is gone from active
  examples;
- keep Rust emission downstream of assembled schema, not wired back into a
  macro shortcut.

## Implementation

`nota-next` commit `183a1739` (`nota: add recursive pipe delimiters`) adds
the low-level delimiter support the schema layer needs:

```nota
(| Kind (Decision Correction) |)
{| Entry [Topic Kind] |}
```

Those are parsed as recursive blocks, not text. `[|...|]` remains the
string-safe pipe text form.

`schema-next` commit `9992a6a3` (`schema: model tagged macro nodes as data`)
changes the authored collection syntax to no-sigil tagged macro calls:

```nota
Topics [(items (Vec [Topic]))]
Query [(limit (Option [Integer]))]
RecordSet [(byTopic (KeyValue [Topic RecordIdentifier]))]
```

and adds `SchemaNode`, `SchemaNodeData`, `SchemaNodeValue`, and
`SchemaNodePair` as data-bearing Rust types. The concrete design witness is
`design_example_schema_node_macro_call_is_tagged_data`, which parses
`(Vec [Topic])` as:

```rust
SchemaNode {
    tag: Name::new("Vec"),
    data: SchemaNodeData::Vector(vec![
        SchemaNodeValue::Symbol(Name::new("Topic")),
    ]),
}
```

The assembled schema definition now also declares those schema-node data
types in `schemas/asschema.asschema`, so macro calls have an ASSchema home
instead of existing only as parser behavior.

`schema-rust-next` commit `808f4fc7` (`schema-rust: consume tagged schema
macros`) updates downstream examples and the lock file to consume
`schema-next` `9992a6a3`. Generated Rust output remains driven by final
ASSchema variants; the emitter still does not read authored macro calls.

## Constraints Added

`nota-next`:

- design test proving `(|...|)` and `{|...|}` are recursive blocks;
- structure-header support for `PipeParenthesis` and `PipeBrace`;
- intent/architecture updates stating macro heads are raw symbol candidates
  until schema context reads them.

`schema-next`:

- test proving `(Vec [Topic])` is a `SchemaNode` tagged-data object;
- tests rewritten from `(@Vec (T))` to `(Vec [T])`;
- Nix guard rejects `@Vec`, `@Option`, `@KeyValue`, `@Bag`, and `@HashSet`
  in active schema examples/source;
- `.asschema` final-data guard still rejects `@` and `$` in assembled data.

`schema-rust-next`:

- dependency pins updated to `nota-next` `183a1739` and `schema-next`
  `9992a6a3`;
- all authored fixture schemas moved to no-sigil tagged calls;
- Nix guard rejects the old `@` collection form in examples/source.

## Verification

`nota-next`:

```text
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed. The first Nix run fell back from the remote cache to local build
after cache timeouts, then passed.

`schema-next`:

```text
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed. One Nix run caught an MSRV issue (`usize::is_multiple_of` is too
new for the crate's Rust 1.85 floor); that was replaced with `% 2`.

`schema-rust-next`:

```text
cargo fmt && cargo test
nix flake check --print-build-logs
```

Both passed. This includes the generated Rust tests for NOTA parsing, RKYV
frames, automatic origin routes, Nexus trait dispatch, SEMA-oriented traits,
upgrade traits, cross-crate imports, and final `.asschema` fixtures.

## Current Truth

The stack now has a clear split:

- raw NOTA knows delimiters and symbols, not schema semantics;
- authored schema may use no-sigil tagged macro calls at macro-capable node
  positions;
- those calls can be represented as `SchemaNode` data;
- the macro engine lowers them into final `TypeReference` / declaration data;
- `.asschema` remains macro-free final NOTA data;
- `schema-rust-next` emits Rust only from assembled schema.

The remaining gap is macro-table bootstrapping: macro definitions themselves
still parse through the current declarative library. The next stronger pass is
to assemble macro definitions into serializable macro-table data first, then
load the runtime registry from that data.
