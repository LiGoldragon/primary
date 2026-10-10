# Ethos Import Syntax — Witness Report

**Date:** 2026-10-09  
**Hostname:** `ouranos` (rerun needed on Prometheus for production witness)  
**Target:** ethos-zero v16.0.0 (built c2653d via Nix)  
**Method:** Parser source inspection + fixture trials in both type-declaration and struct-field positions

## Grammar: Imports and Field References

**Import section syntax** (from `conception.rs` lines 397–415):  
Import requires a Headed form with Separator::Colon: `source:name` (one import) or `source:[name1 name2]` (many). Source is validated via `syn::parse_str::<syn::Path>()`, accepting single-segment (`protos`) or multi-segment with `::` (`std::sync`). In practice, sources in the import section must be a single identifier followed by `:`.

**Grammar (one line):** `<source>:<name>` or `<source>:[<names>]` where source is one segment; field types use `<source>:<name>` inline.

---

## Part (a): Accepted Import Forms

| Form | Status | Notes |
|------|--------|-------|
| `std:Mutex` | ✓ Accepted | Single import from source |
| `std:[ Mutex Other ]` | ✓ Accepted | Multiple imports from source |
| `std::sync:Mutex` | ✗ Rejected | Multi-segment sources fail; `::` is not valid in import syntax position |
| `source:file.[ A B ]` | ✗ Rejected | Period not allowed between source and bracket list |

**Evidence:**
- **Fixture:** `Library [ std:[ Mutex Other ] ] [ State.String ] [] []`
- **Command:** `ethos-zero 'Generate.{ single-import.ethos /tmp/out }'`
- **Result:** `Generated.[ /tmp/out/single-import.rs ]` — accepts `std:Mutex` and `std:[ Mutex Other ]`

---

## Part (b): Field References and Rust Generation

Fields carry types without names; names are generated from the type in snake_case. Imported types referenced as field types use the `source:Name` form inline.

**Example fixture:**
```
Library
[ crate:[ Error Protos ] ]
[ MyStruct.{ crate:Error crate:Protos Integer } ]
[]
[]
```

**Generated Rust:**
```rust
pub struct MyStruct {
    pub error: crate::Error,
    pub protos: crate::Protos,
    pub integer: i64,
}
```

Field names (`error`, `protos`, `integer`) are auto-generated from types; the source prefix converts from `:` to `::` in Rust output.

---

## Part (c): Inline Type Forms — Parse Results (Dual Position)

| Form | Type Declaration | Struct Field | Notes |
|------|------------------|--------------|-------|
| `Topic:Name` | ✓ ACCEPTED | ✓ ACCEPTED | Works both positions; `std::Mutex` |
| `Topic:custom.Name` | ✗ Expected.Reference | ✗ Expected.Reference | Period invalid both positions |
| `Topic:custom:Name` | ✓ ACCEPTED | ✓ ACCEPTED | Works both; custom dropped → `std::Mutex` |
| `Topic.custom:Name` | ✗ Expected.Reference | ✗ Case.std | Period before colon fails both |
| `source:file.[A B]` | — | — | Import form: ✗ Expected.Import |

**Critical finding — source overwrite (from `conception.rs` lines 431–435):**

```rust
let mut r: Reference = body.conceive().place(1)?;
r.source = Some(
    Source::try_from(head.0.as_str())
        .map_err(|text| Error::conceptual(vec![0], Problem::Name(text)))?,
);
```

When ethos parses `Topic:custom:Name`:
1. Head parses as `Topic` (becomes outer source)
2. Body parses as `custom:Name` (inner Reference with source `custom` and name `Name`)
3. Line 432 **overwrites** the inner reference's source, replacing `custom` with the outer `Topic`
4. Result: `Topic:Name` only; `custom` is silently dropped

**Witnessed in struct field context:**
- **Fixture (exact):** `Library\n[ ]\n[ Struct.{ std:custom:Mutex } ]\n[]\n[]`
- **Output:** `pub struct Struct { pub mutex: std::Mutex, }` — `custom` segment discarded

**Type declaration fixture (exact):**
- **Fixture:** `Library\n[ ]\n[ Type.std:custom:Mutex ]\n[]\n[]`
- **Output:** `pub type Type = std::Mutex;` — `custom` segment discarded

**Rejected `Topic:custom.Name` fixture:**
```
Library
[ ]
[ Type.std:custom.Mutex ]
[]
[]
```
**Error:** `Rejected.{ file { 3 14 } Conceptual.{ [ 1 1 0 1 1 ] Expected.Reference } }`

---

## Summary

**Grammar:** `source:name` or `source:[names]`; sources are single identifiers only in import sections. Inline field types use same syntax.

**(a)** Accepted forms: `std:Mutex`, `std:[Mutex Other]`; multi-segment sources (`::`) are rejected.

**(b)** Fields reference imported types via `source:Name` inline; names auto-generated snake_case from type; Rust emits `source::Name`.

**(c)** Inline forms tested in both type-declaration and struct-field positions:
- `Topic:Name` ✓ both
- `Topic:custom:Name` ✓ both (custom dropped, final: `source:Name`)
- `Topic:custom.Name` ✗ both (Expected.Reference)
- `Topic.custom:Name` ✗ both
- `source:file.[A B]` ✗ imports (Expected.Import)

**⚠️ Witness note:** Run on `ouranos`; requires Prometheus rerun for production witness.
