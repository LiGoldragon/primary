# Ethos Import Syntax — Prometheus Witness Final

**Hostname:** `prometheus` (witnessed 2026-10-09)  
**Tool:** ethos-zero v16.0.0 (commit c2653d)  
**Method:** Fixture generation and testing on Prometheus via SSH

---

## Results Table: All Forms, All Positions

| Form | Position | Fixture Text | Result | Emitted Rust |
|------|----------|--------------|--------|--------------|
| `std:Mutex` | type decl | `Library [ ] [ MyType.std:Mutex ] [] []` | ✓ ACCEPT | `pub type MyType = std::Mutex;` |
| `std:Mutex` | struct field | `Library [ ] [ MyStruct.{ std:Mutex } ] [] []` | ✓ ACCEPT | `pub struct MyStruct { pub mutex: std::Mutex }` |
| `std:custom:Mutex` | type decl | `Library [ ] [ MyType.std:custom:Mutex ] [] []` | ✓ ACCEPT | `pub type MyType = std::Mutex;` |
| `std:custom:Mutex` | struct field | `Library [ ] [ MyStruct.{ std:custom:Mutex } ] [] []` | ✓ ACCEPT | `pub struct MyStruct { pub mutex: std::Mutex }` |
| `std:custom.Mutex` | type decl | `Library [ ] [ MyType.std:custom.Mutex ] [] []` | ✗ REJECT | `Expected.Reference` |
| `std.custom:Mutex` | type decl | `Library [ ] [ MyType.std.custom:Mutex ] [] []` | ✗ REJECT | `Expected.Reference` |
| `std:file.[A B]` | imports | `Library [ std:file.[ Mutex ] ] [ Type.String ] [] []` | ✗ REJECT | `Expected.Import` |

---

## Key Findings

1. **Topic:Name form** — Works in both type declaration and struct field positions. Emits `std::Name` in Rust.

2. **Topic:custom:Name form** — Works in both positions. Inner source (`custom`) is silently dropped by source overwrite (conception.rs lines 431–435). Emits only `std::Name`.

3. **Period (.) forms** — Both `Topic:custom.Name` and `Topic.custom:Name` rejected with `Expected.Reference`. Period is not valid in field type references.

4. **Import bracket form** — `source:file.[A B]` rejected in imports section with `Expected.Import`. Period not allowed between source and bracket list in import syntax.

5. **Bare type entries** — Any bare reference in types section (not part of a declaration) fails with `Expected.Declaration`. All forms must be part of a type declaration (`Name.Form`) or struct definition.

---

## Source Overwrite Mechanism (conception.rs:431–435)

When parsing `Topic:custom:Name`:
```rust
let mut r: Reference = body.conceive().place(1)?;  // Parses 'custom:Name'
r.source = Some(
    Source::try_from(head.0.as_str())  // Overwrites with 'Topic'
        .map_err(|text| Error::conceptual(...))?,
);
```

Result: Inner source (`custom`) discarded; outer source (`Topic`) replaces it. Final: `Topic:Name` only.

---

## Grammar Summary

**Accepted import forms:** `source:name` or `source:[name1 name2]`  
**Accepted inline field types:** `source:name` only (no period, no nested sources)  
**Source syntax:** Single identifier only (no `::` in import context)  
**Nested source forms:** Parsed but inner source overwritten and dropped

