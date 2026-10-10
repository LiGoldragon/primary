# Form Positions: Types-Section vs Struct-Field Witness

**Hostname:** `ouranos` (NOT Prometheus — requires rerun on Prometheus for production witness)  
**Tool:** ethos-zero v16.0.0  
**Date:** 2026-10-09

## Results by Form and Position

| Form | Type Declaration | Struct Field | Notes |
|------|------------------|--------------|-------|
| `Topic:Name` | ✓ ACCEPTED | ✓ ACCEPTED | Basic form works both positions |
| `Topic:custom.Name` | ✗ REJECTED | ✗ REJECTED | Period invalid; Expected.Reference |
| `Topic:custom:Name` | ✓ ACCEPTED | ✓ ACCEPTED | Parses; custom dropped → `std::Mutex` |
| `Topic.custom:Name` | ✗ REJECTED (Expected.Reference) | ✗ REJECTED (Case.std) | Period before source fails |
| `source:file.[A B]` | ✗ REJECTED | — | Import form; Expected.Import |

## Exact Fixtures and Errors

### Topic:custom:Name (Type Declaration)
**Fixture:**
```
Library
[ ]
[ Type.std:custom:Mutex ]
[]
[]
```
**Result:** `Generated.[ /tmp/out/file.rs ]`  
**Output:** `pub type Type = std::Mutex;`

### Topic:custom:Name (Struct Field)
**Fixture:**
```
Library
[ ]
[ Struct.{ std:custom:Mutex } ]
[]
[]
```
**Result:** `Generated.[ /tmp/out/file.rs ]`  
**Output:** `pub struct Struct { pub mutex: std::Mutex, }`

### Topic:custom.Name (Type Declaration)
**Fixture:**
```
Library
[ ]
[ Type.std:custom.Mutex ]
[]
[]
```
**Error:** `Rejected.{ file { 3 14 } Conceptual.{ [ 1 1 0 1 1 ] Expected.Reference } }`

### Topic.custom:Name (Type Declaration)
**Fixture:**
```
Library
[ ]
[ Type.std.custom:Mutex ]
[]
[]
```
**Error:** `Rejected.{ file { 3 10 } Conceptual.{ [ 1 1 0 1 ] Expected.Reference } }`

### source:file.[A B] (Imports)
**Fixture:**
```
Library
[ std:file.[ Mutex ] ]
[ Type.String ]
[]
[]
```
**Error:** `Rejected.{ file { 2 12 } Conceptual.{ [ 1 0 0 1 1 ] Expected.Import } }`
