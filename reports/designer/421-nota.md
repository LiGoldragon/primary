# 421 — NOTA: the data notation (pure structure + codec)

*Kind: Current-design spec · Component: nota (nota-next) · Topics: nota, data-substrate, delimiters, codec, positional-typing · 2026-05-29*

*One of three current-design component reports — [[422-schema]] and
[[423-signal-nexus-sema]] are the others. Grounded in `skills/nota-design.md`,
`nota-codec`/`nota-derive`, and records 1122 (everything is a struct), 1127/1128
(delimiter meaning is positional), 1176 (the type-name vocabulary lives in
Schema, not NOTA; NOTA is pure structure + codec + the `None`/`Some` value
literal). Obsolete forms named as gone in §6.*

## 1. What NOTA is

NOTA is the workspace's one data notation. Every value is a NOTA value: a
config, an intent record, a schema, an assembled schema, a macro. It has two
equal forms — **NOTA text** (authored, grep-able) and **rkyv bytes** (what runs)
— and the same value round-trips between them. If a thing can't serialize and
deserialize, it isn't a data object yet.

It is **positional, typed, terse**: meaning comes from a value's position
against a known type, never from `key value` labels. And it carries **no type
vocabulary of its own** — NOTA is structure, plus a codec that serializes Rust
types, plus one value literal. The names of types (`String`, `Vec`, …) belong to
the layer above, Schema (1176, [[422-schema]]).

## 2. NOTA is pure structure — the delimiters

The delimiters carry values and structure; NOTA parses them but does not assign
them type meaning:

```text
delimiter      structural form
---------      ---------------
[ … ]          a vector value (e.g. [1 2 3]); a STRING at a String position
{ … }          a key-value map value (odd = key, even = value)
( … )          a positional record / tagged value (first token = the tag at an enum position)
[| … |]        a string value, multi-line-safe, may contain bare [ ]
(| … |)        a pipe-paren block (Schema reads it as an enum declaration)
{| … |}        a pipe-brace block (Schema reads it as a struct declaration)
```

**The rule:** a delimiter's structure is fixed by NOTA; its *meaning* comes from
the expected position (1127, 1128) — the same `[ … ]` is a vector at a vector
position and a string at a String position; the same `( … )` is a plain struct
where a struct is expected and a tagged variant where an enum is. NOTA parses
the pipe blocks too, but reading them as struct/enum *declarations* is Schema's
job, not NOTA's. **The pipe blocks are transitional** (record 1199, settled):
the target declaration syntax is the `@`-sigil form ([[428-at-sigil-declaration-syntax-spec]])
— `Name@{ … }` struct, `Name@[ … ]` enum, `name@Type` field, `name@(Vec X)`
composite — defined through NOTA's sigil+delimiter macro interface (`{ }`
struct, `[ ]` enum, `( )` composite/macro). The one reserved word-literal is `None`
(Option-absent; present is `(Some x)`).

## 3. The serialization codec lives in NOTA

`nota-next` owns the typed codec — the `NotaEncode` / `NotaDecode` / `NotaMapKey`
traits and the `nota-derive` macros (`NotaRecord` / `NotaEnum` / `NotaTransparent`
/ `NotaMapKey`) — which serialize Rust types to and from NOTA text:

- scalars: `String`, integers, `bool`, `Path`, floats;
- composites: `Vec<T>` → `[ … ]`, `Option<T>` → `None`/`(Some x)`, maps → `{ … }`,
  sets, `Box<T>`.

This is the **one shared codec** used by hand-written Rust types, schema-emitted
types, and the assembled schema alike (see [[422-schema]] §5). It is
*serialization* — how a Rust value becomes NOTA text — and is distinct from the
schema *type-name vocabulary*: the codec serializes a `Vec<T>` to `[ … ]`; the
keyword `Vec` that a `.schema` writes to declare that type is Schema's (1176).

## 4. Everything bottoms out in a struct

A unit variant is a zero-field struct, a data-carrying variant a one-field
struct, an enum a single-field struct holding the active variant (1122). The
wire form needs no labels because fields are positional against the type the
position fixes. The reading model: `(VariantName …)` is a data variant; `(…)`
with no leading PascalCase is a struct; bare `VariantName` is a unit variant;
everything else is a primitive, a `[…]` sequence, or a `{…}` map.

## 5. Strings, and the property that falls out

Strings come **exclusively** from brackets — never quotation marks: `[content]`
inline, `[|content|]` block/multi-line, or a bare camelCase/kebab token at a
`String` position (a bare token at a `Path` position widens to allow `/` and
`.`). Because a complete NOTA expression never contains a `"`, it embeds
escape-free in any double-quote host — shell, JSON, Rust, Nix, TOML, a DB
column. That escape-free embedding is a load-bearing design property.

## 6. The boundary, and what is gone

NOTA is **structure + codec + the `None`/`Some` literal — and nothing else**.
The type-name vocabulary (scalars `String`/`Integer`/`Boolean`/`Path` and
composites `Vec`/`Optional`/`Map`/`Set`/`Box`) is **not** in NOTA; it is Schema's
type-reference vocabulary (1176, [[422-schema]] §3). Gone entirely: the `@`/`*`
macro sigils (`~ @ ! ? * =` are reserved nexus sigils, never macro markers); the
flat `(Foo A B)` shape (a paren is head + one grouped body, 1085); quotation-mark
strings.

Positional discipline holds throughout: every schema position is always present
(no defaults, no tail omission); `Option<T>` is `None` / `(Some x)`; no tuples
and no multi-field unnamed structs (a single-field unnamed struct is a
transparent newtype); maps and schema namespaces share the `{ }` rule.

## 7. Testing — fixtures from file (record 1180)

Tests never inline nota / schema / sema source as Rust strings. Each fixture is
a separate file under `tests/fixtures/` — a `.nota`, `.schema`, or `.sema` file
— loaded by a tiny shared helper, the `fixture!` macro (a small `nota-fixtures`
dev-dependency). `fixture!("record.nota")` expands to `include_str!` of
`tests/fixtures/record.nota` in the calling crate, so the artifact under test is
a real file, not an inline literal. (The big-example tests already `include_str!`
from `tests/fixtures/`; the macro standardizes that one pattern and is what
replaces the remaining inline `lower(…)` source strings.)

```nota
; tests/fixtures/record.nota
([workspace] Decision [assembled schema is plain NOTA data] High)
```
```rust
#[test]
fn record_round_trips() {
    let source = fixture!("record.nota");          // real file, never inline
    let value = Record::from_nota(source).unwrap();
    assert_eq!(value.to_nota(), source.trim());    // NOTA text → value → NOTA text
}
```

Helper sketch — the whole library is one macro:

```rust
#[macro_export]
macro_rules! fixture {
    ($rel:expr) => { include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/tests/fixtures/", $rel)) };
}
```

A runtime variant (`fn read(rel: &str) -> String` over `std::fs`) is added only
if a test needs a dynamically-chosen fixture name; the macro covers the common
compile-time case.
