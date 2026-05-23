# 1 - NOTA User Notation Model

*Kind: Research | Topic: nota-user-notation | 2026-05-23*

## Frame

This slice describes NOTA as authored by a human. The user model is not "a lighter JSON" or "Lisp with keywords." It is typed positional data: the schema tells each position what it means, and the text writes the values in that order.

The design philosophy is load-bearing:

- Records are positional. Field names live in the schema, not in the text.
- Structs are untagged. A struct record is `(field1 field2 ...)`.
- Enums own PascalCase. Unit variants write `Variant`; data-carrying variants write `(Variant fields...)`.
- There are no tuples. Heterogeneous positional data is a named-field struct in the schema, written as an untagged record.
- Maps use braces, with flat alternating key/value tokens.
- Strings use bracket strings as the normal authored form. Legacy double quotes may decode, but they are not the canonical written style.

## Core Mental Model

A NOTA author asks two questions at every position:

1. What type does the schema expect here?
2. Does this value need a delimiter to reveal its shape?

The opening delimiter gives the structural family:

```nota
(...)  ;; record: struct or data-carrying enum variant
[...]  ;; sequence at collection positions; string at string-like positions
{...}  ;; map: flat key/value stream
```

The schema decides the meaning of a token inside that family. The same surface text can mean different things at different typed positions:

```nota
;; String position: one string value
[alpha beta]

;; Vec<String> position: two string elements
[alpha beta]
```

That is intentional. NOTA is not self-describing by field labels; it is self-describing by schema position plus delimiters.

## PascalCase Rule

PascalCase has exactly three value-position meanings:

```nota
Flow
```

Valid when the schema expects a unit enum variant.

```nota
(Node 100 (alice) None)
```

Valid when the schema expects a data-carrying enum variant. `Node` is the variant; `100`, `(alice)`, and `None` are its positional fields.

```nota
(alice)
```

Valid when the schema expects an untagged struct with one string field. There is no `Node` or `User` wrapper just because the Rust type has that name.

Common invalid forms:

```nota
(Node)
```

Invalid if `Node` is a unit variant. Unit variants are bare: `Node`.

```nota
NixBuilder
```

Invalid if `NixBuilder` is a data-carrying variant. Data variants need record form, for example `(NixBuilder (Some 8))`.

```nota
(Edge 100 200 Flow)
```

Invalid if `Edge` is a struct type, not an enum variant. A struct with fields `from`, `to`, and `kind` writes `(100 200 Flow)`.

```nota
(Foo)
```

Invalid at an ordinary `String` field. Bare PascalCase is reserved for enum variants; write `[Foo]` when the string content is capitalized.

## Positional Records

Struct records write only their fields:

```nota
(operator skills/operator.md Apex [Implementation as craft.])
```

That is the right shape for a schema like `name: String`, `path: Path`, `tier: Tier`, `description: String`.

The two recurrent wrong shapes are wrappers and labels:

```nota
(Skill operator skills/operator.md Apex [Implementation as craft.])
```

Invalid when every item is already known to be `Skill`. `Skill` would be read as an enum variant tag, not as helpful documentation.

```nota
(Skill (name operator) (path skills/operator.md) (tier Apex))
```

Invalid labeled-field shape. `(key value)` pairs are not NOTA records; they are nested records whose first value is `key`.

When a position can hold multiple shapes, use enum variants:

```nota
(Role operator skills/operator.md Apex [Implementation as craft.])
(Architecture component-triad skills/component-triad.md Apex [Daemon + thin CLI + signal-* contract.])
```

The variant names are the category. Do not put the category in a comment and then repeat it as a field.

## Options And Complete Fields

`Option<T>` is an enum, not an omitted tail field:

```nota
(100 (Some 5))
(100 None)
```

Both fields are present. `None` is the unit variant for absence; `(Some 5)` is the data-carrying variant for presence.

For a record shaped like `action: String`, `builder: Option<String>`, `substituters: Option<Vec<String>>`, these are valid:

```nota
(switch (Some zeus) (Some [prometheus]))
(switch None (Some [prometheus]))
(switch None None)
```

These are invalid:

```nota
(switch)
(switch (Some zeus))
```

NOTA has no "missing means default" rule. If the schema gains a field, old files must be migrated to carry the new position, often as `None` or `[]`.

## Strings

Use bracket strings for authored prose:

```nota
[hello world]
[he said 'yes']
[quote "yes"]
[array[0\]]
```

Inline bracket strings allow escapes for the delimiter and common controls: `\]`, `\\`, `\n`, `\t`, `\r`. Newlines do not belong directly inside an inline bracket string.

Use block strings for multiline content:

```nota
[|
  line one
  line two
|]
```

When the content begins with a newline, the block form dedents the shared leading whitespace from non-empty lines. That makes it suitable for hand-authored paragraphs, policies, certificates, and examples.

Bare camelCase and kebab-case identifiers are accepted where the schema expects `String`:

```nota
nota-codec
fooBar
with_underscore
```

Use bracket form when the content has spaces, non-ASCII, starts with a digit, equals `None`, contains `:`, contains `/` or `.`, or is PascalCase:

```nota
[01-intro.md]
[None]
[User]
[skills/operator.md]
```

Legacy double-quoted strings may decode in the codec, but new authored examples should prefer bracket strings.

## Paths

`Path` is a distinct schema position from `String`. At a `Path` position, filesystem-shaped content may be bare:

```nota
skills/operator.md
./foo
/etc/hosts
../bar
```

The same token at a `String` position is a typed error because `/` and `.` are path-shaped. Delimit it if it is string content:

```nota
[skills/operator.md]
```

Paths also fall back to bracket form for content that would confuse token dispatch:

```nota
[with space]
[01-intro.md]
[None]
```

Colon has a separate NOTA role as nested-name separator:

```nota
Char:Upper:A
Schema:Type:Field
```

Do not assume colon-bearing content is an ordinary bare string.

## Sequences

Sequences are homogeneous collection positions:

```nota
[]
[1 2 3]
[TailnetClient (NixBuilder None)]
```

If list elements need different shapes, the element type should be an enum. Do not use a vector as a tuple substitute for a fixed heterogeneous record.

## Maps

Maps use braces and alternate key/value tokens:

```nota
{host localhost port 8080}
{User 100 Admin 200}
{alpha 2 zeta 1}
```

Odd positions are key text. Even positions are values. PascalCase is allowed as a map key because the brace context says it is key text, not an enum variant.

Valid path keys:

```nota
{./local.nota 2 skills/operator.md 1}
```

Invalid map shapes:

```nota
[(host localhost) (port 8080)]
(Entry host localhost)
{[with space] 1}
{alpha 1 alpha 2}
```

The first is a sequence, not a map. The second is an enum variant named `Entry`, not a map entry. Keys with whitespace are rejected even in bracket form. Duplicate key text is rejected instead of silently overwriting.

## Comments

Line comments start with `;;` and run to the end of the line:

```nota
;; schema note for the reader
(100 200 Flow)
```

Comments are discarded. They are appropriate for schema notes and local explanation, not for load-bearing categories or values. If a future tool needs the information, it belongs in a typed field or enum variant.

## Literals And Reserved Forms

Common scalar forms:

```nota
42
-7
0xFF
0b1010
1_000_000
3.14
7.0
True
False
#deadbeef
2026-05-20
14:30:00
```

Floats keep a dot in canonical form so they re-lex as floats. Bytes use `#` followed by lowercase even-length hex; the empty byte array can write `#`.

Pure NOTA reserves several tokens for Nexus or future grammar and rejects them as NOTA syntax: `~`, `@`, `!`, `?`, `*`, comparison operators such as `<` and `!=`, and standalone `=`.

## Common Mistake Index

Most user mistakes come from importing habits from JSON, Lisp, Rust tuple syntax, or CLI flag syntax:

- Writing labeled fields: `(Request (target zeus) (force True))`. Use positional schema order: `(zeus True)`.
- Wrapping structs in their type name: `(Profile alice 42)`. If `Profile` is a struct, write `(alice 42)`.
- Lowercasing enum variants: `apex`, `none`, `true`. Variants are PascalCase: `Apex`, `None`, `True`.
- Using bare PascalCase as a string: `User`. At a `String` position, write `[User]`.
- Treating optional tails as omittable. Every field is explicit; absence is `None`.
- Using vectors as tuples: `[100 Flow]`. Fixed heterogeneous data is a struct record, for example `(100 Flow)`.
- Writing maps as entry records. A map is `{key value key value}`, not `[(key value)]` or `(Entry key value)`.
- Putting data in comments. Comments help humans read; they do not carry data.
- Assuming `[x y]` always means a list. At a string-like position it is one string; at a collection position it is a sequence.
- Using legacy double quotes in new examples. They may decode, but bracket strings are the authored form.

## Synthesis Hook

The shortest user-facing explanation is: NOTA is typed positional text. Parentheses write records, brackets write either strings or sequences depending on schema position, braces write maps, and PascalCase belongs to enum variants. If a writer wants labels, omitted fields, tuple syntax, or comment-carried categories, they are trying to use a different format.
