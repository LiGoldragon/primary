# 234 - NOTA Codec and Asschema Unification Implementation State

Date: 2026-05-28  
Lane: operator  
Subject: implementation status of `reports/operator/233-nota-codec-asschema-unification-target-2026-05-28.md`

## Status

Report 233 is mostly a target, not a completed implementation.

## Implemented

`nota-next` implements the raw structural floor:

- `Document`
- `Block`
- `Delimiter`
- atoms
- source spans
- structure header

It deliberately does not know schema, fields, macro calls, or typed Rust
objects.

`schema-next` implements a real `.schema` lowering path:

- parse `.schema` with `nota-next`
- raw schema file / raw datatype inspection
- syntax layer that distinguishes struct field lists from `(Vec T)` style type
  references
- `Asschema` as typed in-memory Rust data
- import resolution and macro registry pieces

`schema-rust-next` implements real Rust emission from `Asschema`:

- Rust structs/enums
- rkyv derives on generated component types
- NOTA parsing/rendering for generated component types
- vector/map/optional decoding and formatting
- short-header / signal-frame / mail / plane-support surfaces
- fixture and Nix checks proving generated code compiles and runs in the
  current prototype stack

## Partially Implemented

`Asschema` exists as Rust data, but it is not yet itself a fully serialized
NOTA/rkyv object model.

Current `Asschema` is:

- in-memory
- typed enough for emitter input
- testable through Rust assertions

It is not yet:

- derived through a shared `NotaEncode` / `NotaDecode` surface
- emitted as canonical `.asschema` NOTA
- rkyv-derived as a stored/cached macro-free schema artifact
- used as the serialized input to macro tables or code emission

## Not Implemented

The shared next-stack typed NOTA codec does not exist yet.

Specifically:

- `nota-next` has no `NotaEncode` trait.
- `nota-next` has no `NotaDecode` trait.
- `nota-next` has no derive crate or derive-compatible codegen surface.
- hand-written Rust types cannot currently get ergonomic direct NOTA reading
  through `nota-next`.

`schema-rust-next` still emits a private mini-codec into generated modules:

- local `NotaDecodeError`
- local `NotaSource`
- local `NotaBlock`
- local `from_nota_block`
- local `to_nota`
- local collection parser/formatter helpers

That is exactly the split report 233 says should be removed.

## Best Current Summary

The current stack can do:

```text
.schema -> Asschema in memory -> generated Rust -> generated local NOTA codec
```

The target stack should do:

```text
.schema -> Asschema as NOTA/rkyv data -> generated Rust -> shared nota-next codec traits
```

And direct hand-written Rust should also do:

```text
Rust type -> shared nota-next codec traits -> NOTA text
```

## Next Implementation Step

The right next code pass is to add the typed codec surface to `nota-next` first:

- `NotaReader`
- `NotaWriter`
- `NotaEncode`
- `NotaDecode`
- `NotaMapKey`
- typed error
- primitive/container impls
- record/enum support, initially hand-written or emitter-generated

After that, `schema-rust-next` can stop emitting `NotaSource` / `NotaBlock` /
`NotaDecodeError` into every generated file and instead emit trait impls
against `nota-next`.
