# 212 — Brace namespace correction and schema module implementation

## Trigger

This report captures the operator-facing state after the latest schema-stack
correction on 2026-05-27. The first correction is the brace namespace pair-only
rule. The second implemented slice is the beginning of the schema module
system: crate-local `schema/lib.schema`, single-colon fully qualified names,
and generated Rust under a schema-shaped Rust module path.

This is the handoff point for the next operator or designer pass. It records
what is implemented now, what is only a tested loader/emitter slice, and what
still remains conceptual.

## Spirit records 891-901

- Spirit record 891: brace objects in schema are always key/value maps. The
  pair-style namespace is correct; parenthesized named-object entries inside
  braces are wrong and must be removed from code and docs.
- Spirit record 892: schema namespace additions should eventually be
  append-only, adding new names at the end of the namespace so future
  enum-like compilation and upgrade logic can remain compatible.
- Spirit record 893: a brace namespace conceptually defines a dynamic enum of
  named objects, but its authored and lowered representation is key/value
  pairs. Macros operate on the key and value pair, not on a parenthesized
  object wrapper.
- Spirit record 894: brace always means key/value map at the NOTA layer. The
  schema namespace uses pair-style form; the named-object wrapper is redundant.
  Conceptually, a namespace is a dynamic enum whose type name is the variant
  tag and whose type definition is the payload. The future dynamic enum is
  append-only in the Cap'n Proto style so existing positions stay stable and
  can eventually compile to an enum-tag space with upgrade support.
- Spirit record 895: schema fully qualified names should use a single colon as
  the namespace separator, mirroring Rust crate and module structure while
  avoiding Rust double-colon syntax in schema text.
- Spirit record 896: each Rust crate participating in schema generation should
  carry a standard `schema/` folder with `lib.schema` as the entry point and
  additional module schemas, such as `signal.schema`, loaded through that root
  in Rust module style.
- Spirit record 897: schema-generated Rust should emit into a dedicated schema
  module tree inside crate source, with generated lib-style module files
  mirroring the schema module layout before normal Rust compilation consumes
  them.
- Spirit record 898: schema imports should resolve by crate name from the
  imported crate's standard schema folder, so schema and source travel together
  as one compilation and namespace unit.
- Spirit record 899: development tooling for schema-derived crates should
  regenerate emitted Rust automatically, or through one central command,
  whenever schema files change, then rerun the relevant build or tests.
- Spirit record 900: before creating the next schema-stack version, operators
  and designers should study each other's latest work first. Designers rebase
  prototype worktrees from operator main; operators integrate valid fresh
  designer intent into main.
- Spirit record 901: brace namespaces can later compile into enum tables with
  non-conflicting fully qualified names, but the current implementation should
  keep the structural key/value map while preserving append-only ordering for
  that future path.

## Implemented correction and module slice

The brace correction landed across the running schema pilot stack:

- `schema-next` commit `8c821cba` (`make schema namespaces key-value only`)
  removes support for parenthesized namespace entries and makes the root
  namespace macro accept only flat brace key/value pairs.
- `schema-rust-next` commit `b5a851a1` (`consume key-value schema namespaces`)
  consumes the corrected `schema-next` assembled shape and continues the
  generated-Rust no-free-functions proof.
- `spirit-next` commit `8ef16bc5` (`use key-value schema namespace in spirit
  pilot`) updates the runnable Spirit pilot schema to pair-style namespace
  form and keeps the generated-build-time proof wired through the declarative
  macro path.

The operative rule is now simple: a brace object is a map. In schema
namespace position, the entries are `Name Body` pairs. The older
`(Name Body)` namespace entry shape is not compatibility syntax; it is the
wrong shape and should stay removed from engine code, examples, tests, and
docs.

The module-system slice then landed on top:

- `nota-next` commit `1c11876b` (`allow colon-qualified nota symbols`) allows
  `schema:module:Type` to remain one NOTA symbol, so schema-qualified names can
  be parsed before schema-specific validation.
- `schema-next` commit `807c5250` (`add schema package module entrypoint`)
  introduces `SchemaPackage` and `SchemaModuleSource`. A package can load
  `schema/lib.schema`, derive identities such as `spirit-next:lib`, and map a
  colon-qualified schema name to a sibling module schema path.
- `schema-rust-next` commit `5ca1c964` (`emit schema module file paths`) maps
  assembled schema identities to Rust module paths. For example,
  `spirit-next:lib` emits `schema/lib.rs`, and
  `spirit-next:signal:public` emits `schema/signal/public.rs`.
- `spirit-next` commit `e004fc62` (`load spirit schema from lib entrypoint`)
  renames the pilot schema entry point to `schema/lib.schema`, loads it through
  `SchemaPackage`, and includes the generated artifact from
  `OUT_DIR/schema/lib.rs`.

## Conceptual model

The structural representation and the conceptual model are intentionally
different.

Structurally, the schema namespace is a key/value map because NOTA braces mean
key/value map everywhere. That gives composition convenience and avoids a
redundant parenthesis wrapper around every declaration.

Conceptually, the namespace is dynamic-enum-like. The declaration name is the
variant tag; the declaration body is the variant payload. The future path is
append-only: new namespace entries append at the end of the namespace so
existing positions remain stable. That preserves a route toward compiled enum
tables, compact tags, and upgrade logic without changing today's authored
shape.

## Module-system direction now represented in code

The module direction is now represented by a real loader and emitter boundary,
though not by a full import resolver yet. It is a crate-local schema module
system that mirrors Rust without copying Rust syntax.

Fully qualified schema names use a single colon:

```text
crate-name:module-name:TypeName
```

The crate name is the top namespace level. It comes from the Rust crate, so
schema files do not need to redeclare a conflicting root namespace. Module
names come from schema files loaded through the root entry point.

Each schema-derived Rust crate should carry:

- `schema/lib.schema` as the schema entry point, analogous to `src/lib.rs`;
- module files such as `schema/signal.schema`, loaded through `lib.schema`;
- imports resolved by crate name from the imported crate's standard schema
  folder;
- generated Rust under a dedicated schema module tree. The current pilot writes
  this tree under Cargo's `OUT_DIR`; the future development-mode form can
  materialize the same tree under `src/schema/` for reviewable generated
  source.

The development loop should make schema the edited source of truth. When a
schema file changes, one central command or watch hook regenerates the Rust
module tree and then runs the relevant build or checks.

## Remaining implementation gaps

- The loader can load `schema/lib.schema` and compute sibling module paths, but
  `lib.schema` does not yet declare and transitively load sibling module
  imports.
- Generated Rust still exists as a build artifact in the current pilot shape:
  `OUT_DIR/schema/lib.rs`. A reviewable development-mode `src/schema/` emission
  target and watch hook are not implemented yet.
- Cross-crate imports are not yet resolved by crate name from each crate's
  standard schema folder.
- Append-only namespace ordering is a preserved direction, not yet a checked
  schema evolution invariant.
- The dynamic-enum / enum-table future is conceptual. There is no compiled
  namespace enum table, compact tag allocation, or enum-upgrading facility yet.
- Schema diff and upgrade derivation remain unimplemented.
- The root schema/bootstrap layer still has Rust-known positions. The root
  positions and default macro registry still need to become schema-described
  rather than directly wired by bootstrap Rust.
- `spirit-next` remains a pilot: it proves the corrected schema path and
  method-only runtime shape, but it still lacks durable redb SEMA storage.

## Immediate next pass

Before cutting the next schema-stack version, the operator should read the
fresh designer prototype/report surface and the designer should rebase from the
current operator main state. The loader boundary now exists; the next
implementation pass should make imports real.

The highest-value next slice is:

- extend `schema/lib.schema` with an import declaration shape;
- load sibling modules through that declaration instead of only through direct
  `SchemaPackage::load_module(...)` calls;
- preserve the colon-qualified names through the assembled schema tree;
- make `schema-rust-next` emit a multi-file schema module tree from that
  package, still through generated Rust objects and methods;
- add a Nix check that changes a schema module and proves the regenerated Rust
  path and compiled interface move together.
