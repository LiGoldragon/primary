# 5 - NOTA syntax exception audit

## 0. Summary

The audit found two concrete codec surfaces that were wrong:

| Surface | Wrong form | Correct form |
|---|---|---|
| Maps | `[(Entry key value)]`, then `[(key value)]` | `{key value key value}` |
| Rust tuple blanket impls | `(Tuple a b ...)`, then `[a b ...]` | no support |

The first pass fixed only the fake PascalCase heads. The correction after
review is stronger: `[(key value)]` is still not a map; it is a vector of
structs. A map needs its own delimiter. NOTA now uses `{ }` for maps, with
flat alternating key text and values. The schema chooses the scalar key type.

The tuple correction is also stronger: there is no NOTA tuple form. NOTA
has vectors, structs, enums, and key/value maps. Rust tuples are poorly
specified structs because their fields have positions but no names. The
codec no longer implements `NotaEncode` / `NotaDecode` for Rust tuple
values.

## 1. Implemented Shape

Maps now encode as:

```nota
{host localhost port 8080 User 100}
```

The map delimiter supplies the key/value interpretation:

| Position | Meaning |
|---|---|
| 1 | first key text |
| 2 | first value |
| 3 | second key text |
| 4 | second value |

Map keys are text by position. The typed schema can decode that text as
`String`, `Path`, or a constrained string-like newtype such as `NodeName`.
That means a bare PascalCase key is allowed:

```nota
{User 100}
```

`User` is not a unit enum variant there; the `{ }` delimiter has already
selected map key position. Keys with whitespace are rejected, including
quoted keys such as `"with space"`.

## 2. Removed Shape

Rust tuple blanket impls are removed. This no longer compiles:

```rust
(1u64, 2u64).encode(&mut encoder)?;
```

The intended replacement is a named-field struct:

```rust
pub struct Range {
    pub start: u64,
    pub end: u64,
}
```

which writes as a normal NOTA struct at a known schema position:

```nota
(1 2)
```

The field names live in the Rust schema, not in the text, but they are
still part of the specification. A tuple has no such names.

## 3. Surfaces That Remain Clean

`Option<T>` remains clean:

```nota
None
(Some value)
```

`bool` remains clean:

```nota
True
False
```

Mixed `NotaEnum` remains clean:

```nota
(NixBuilder (Some 8))
TailnetClient
```

Bare `Path` is not suspect. It is intentional schema-position syntax:
when the schema says `Path`, filesystem-shaped tokens like
`skills/operator.md`, `./foo`, and `/etc/hosts` can be bare.

## 4. Verification

`nota-codec` now has tests for:

| Constraint | Witness |
|---|---|
| `{ }` lexes as map delimiters | `tests/lexer_tokens.rs` |
| maps encode/decode as flat braces | `tests/horizon_rs_feedback_fixes.rs` |
| PascalCase map keys are key text | `map_key_position_accepts_pascal_case_as_string_content` |
| whitespace map keys are rejected | encode and decode tests |
| map keys must implement `NotaMapKey` | `tests/compile_fail/map_keys_must_implement_nota_map_key.rs` |
| custom key newtypes round-trip | `tests/map_key_round_trip.rs` |
| Rust tuples do not compile as NOTA values | `tests/compile_fail/rust_tuple_no_blanket_impl.rs` |

Verification passed:

```text
cargo test
nix flake check
```
