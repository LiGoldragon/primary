# Positional, type-prominent struct syntax — and the differentiator separator

Two moves, from the dialogue: (1) struct declarations should be **positional —
a list of types**, mirroring how the data reads in NOTA, retiring the
`fieldName Type` name-value form; (2) when a slot needs an explicit name, attach
it to the type with a **separator** (a schema-layer "string macro," like the
namespace colon). The separator choice is open; this argues the candidates for
and against. This is `639`'s dimensional principle made syntactic.

## The shift, rendered

The win is immediate. A normal struct loses all ceremony:

```
;; today
Entry { Topics * Kind * Description * Magnitude * }
;; proposed — just the types, positionally; the field name IS the type
Entry { Topics Kind Description Magnitude }
```

The bare type *is* the default: the field name is derived from the type. This
absorbs the `*` shorthand — `*` was pointing at exactly this idea ("name =
type"); making it the default lets the star disappear. The declaration now
mirrors the data: a `(spirit-min)` entry in NOTA is positional values, and the
schema is now positional types.

The separator only appears in the **rare** slot that needs a distinct name — and
only in the *schema*, never in data. The live case is the map entry:

```
;; today
TypeReferencePair { key TypeReference value TypeReference }
;; proposed (separator = "." shown; candidates below)
TypeReferencePair { key.TypeReference value.TypeReference }
```

(Per `639`, this case is itself a collection primitive's internals, so in
ordinary structs it should be vanishingly rare — the separator is an escape
hatch, not the norm.)

## What punctuation is already spent (so we don't collide)

Grounded in the parser and name layer — atoms break only on whitespace and
`( ) [ ] { } "`, so every candidate below is a *single atom*; the split is a
schema-layer convention:

| Mark | Already means | Free for this? |
|---|---|---|
| `:` | **namespace scope** separator — `name.split(':')`, `schema-core:mail:Magnitude` | **No** — hard overload |
| `-` | **kebab-case** identifier char — `schema-core`, `no-free-fns` | **No** — ambiguous inside names |
| `.` | float decimal point **inside numeric atoms only** (`3.14`) | **Yes** for non-numeric atoms |
| `/` | on-disk form of `:` (module path `a:b` → `a/b`) | mostly — but reads as scope/path |
| `;` | `;;` is a comment marker | risky — comment-adjacent |
| `,` | nothing — but NOTA is whitespace-separated | free, but alien |
| `@` | nothing structural (bare-eligible punctuation) | **Yes** |

## The separator candidates — for and against

| Sep | Example | For | Against |
|---|---|---|---|
| **`.` dot** | `key.TypeReference` | universal member/qualifier; quiet, compact; free in non-numeric atoms; instantly readable | faint decimal-point association; "member access" semantics fit a *rename* only loosely |
| **`@` at** | `TypeReference@key` | reads cleanly type-first — "a TypeReference **at** role key"; bare-eligible; aligns the type column | visually heavier; carries handle/address/decorator baggage |
| `/` slash | `key/TypeReference` | path/role feel; echoes scoping | it *is* the on-disk form of scope `:` — scope-adjacent, muddies the two axes |
| `:` colon | `key:TypeReference` | familiar `name: type` look | **collides** with the scope separator — `key:TypeReference` could be a scoped name; reject |
| `-` hyphen | `key-TypeReference` | — | **collides** with kebab identifiers — ambiguous with one name; reject |
| `;` semicolon | `key;TypeReference` | — | comment-adjacent (`;;`), visually noisy; reject |
| `,` comma | `key,TypeReference` | — | means "next item," not "qualifier"; alien to whitespace-NOTA; reject |

The two that survive are **`.`** and **`@`**.

## A second axis: which comes first

The separator interacts with order, and order trades against your stated goal
(*"just seeing the type of each"*):

- **name-first** `key.TypeReference` — reads "key, a TypeReference"; the name is
  an optional prefix on the type anchor; matches the old `Name *` left-to-right
  feel.
- **type-first** `TypeReference.key` / `TypeReference@key` — aligns the **type**
  in the left column so you scan types first (your cognitive goal); reads "a
  TypeReference, in role key."

Because the bare default is already type-only, *almost every* field is a clean
type in a scannable column; the separator rows are the exception. So order
mostly affects how the rare exception reads. `@` reads best **type-first**
("Type at role"); `.` reads acceptably **either** way.

## The two strongest packages, side by side

```
;; Package A — dot, name-first (quiet, familiar)
TypeReferencePair { key.TypeReference value.TypeReference }
Edge              { source.NodeId target.NodeId }

;; Package B — at, type-first (type-column aligned, "at role")
TypeReferencePair { TypeReference@key TypeReference@value }
Edge              { NodeId@source NodeId@target }
```

Both keep the common case identical and clean: `Entry { Topics Kind Description
Magnitude }`.

## Recommendation

- **Lean: Package A — `.`, name-first** (`key.TypeReference`). It is the quietest
  and most universally legible, `.` is genuinely free for non-numeric atoms, and
  it sits naturally beside the existing scope `:` as "a different axis of
  qualification" (scope = where a name lives; dot = what to call this slot).
- **Strong alternative: Package B — `@`, type-first** if you want to *maximise*
  type-prominence in the rare named row and like the literal "Type at role"
  reading. Choose this if the type column mattering even in exceptions outweighs
  the extra visual weight.
- **Reject** `:` (scope), `-` (kebab), `;` (comment), `,` (semantics). `/` only
  if you decide differentiation and scoping are the *same* idea (I don't think
  they are — scope is namespace, differentiation is role).

## What it would change

`root.schema`'s declarations go positional (`FieldDeclaration`,
`StructDeclaration`, etc.), the `*` shorthand retires into the bare-type default,
and the schema reads as a graph of types with rare named escape hatches. It is a
breaking syntax change — fine pre-production, and squarely in the NOTA-positional
spirit.

## Recordable

Once you pick a separator, this plus `639`'s dimensional principle form one
coherent, durable design worth recording together (positional type-prominent
structs; field-name = type-name default; `<sep>` differentiator for the rare
named slot). I'll capture the bundle then — or the dimensional principle alone
now if you'd rather lock that first.
