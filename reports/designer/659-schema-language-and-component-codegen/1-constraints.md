# 659/1 — The constraint catalog

Every active governing intent record for the schema/NOTA language, generics, traits/impls,
code generation, and the component triad, swept from the live Spirit store (0.13.0,
post-cleanup) and grouped by theme. Citations are bracket-quoted summaries; the id is the
opaque address.

## Foundational — everything is data, including code

- **`4itr`** (Constraint, **Maximum**): [EVERYTHING is a serializable data object, the MACRO
  most of all — name + position + pattern + template are data trees, not text-with-sigils;
  macros are pre-assembled/serialized/loaded as data; the ONLY code is one tiny generic
  interpreter, no per-macro bespoke parsing; the round-trip test (NOTA text + rkyv) defines
  whether a thing is built as data]. Forbids template-string-then-reparse expansion.
- **`7c71`** (Principle, VeryHigh): [a programming language IS a set of structural macros —
  struct, enum, fn, impl, generics included; freezing the macro set in the compiler makes it
  closed; treating it as data makes the language infinitely extensible and LLM-legible].
- **`2zed`** (Principle, High): [everything is data conforming to a schema-defined type; a
  macro is a value of a specialized struct; no privileged escape-hatch representation].
- **`vpbx`** (Decision, High): [schema-cc is the compiler-compiler: the schema language +
  compiler definition kept as typed data that GENERATES schema-next/schema-rust-next,
  bottoming out in the nota-next seed; push as much of the compiler into data as possible].
- **`549v`** (Decision, Medium): [dispatch precedence among reference forms reified as an
  explicit typed NOTA value, one canonical declared precedence].

## Compiler pipeline & architecture

- **`6grf`** (Decision, VeryHigh): [schema is a specialized NOTA dialect built on structural
  macro nodes — a schema file is full NOTA, not a separate language lowered into NOTA].
- **`6cfr`** (Decision, VeryHigh): [the separate Assembled-Schema IR is removed; the
  resolution it did (inline hoisting, visibility, ordering, symbol paths) lives as METHODS on
  schema-in-rust types during lower; the emitter does only Rust projection, not schema
  semantics].
- **`813q`** (Decision, VeryHigh): [canonical pipeline — authored schema (NOTA) deserializes
  via the structural-macro-node codec directly into schema-in-rust (rkyv, canonical
  round-trip), which lowers into Rust interface code].
- **`9rjq`** (Principle): [the schema/NOTA compiler is build-time-only; it emits typed Rust
  and never links into the runtime binary; shipped binaries carry only strict rkyv contracts].
- **`5ydx`** (Principle, Medium): [schema macro application iterates to a fixed point; each
  pass applies lowerers; macros can introduce macros; iterates until the namespace is pure
  enums/structs/newtypes].

## The structural-macro mechanism

- **`xai7`** (Principle, High): [the structural macro node is a NOTA enum decoded by SHAPE,
  not data tag; decode is type-directed (structural match per variant in declaration order,
  first match wins, recursive); encode emits matching NOTA; realized as
  `#[derive(StructuralMacroNode)]` with per-variant shape attributes; not a runtime registry
  or string-name dispatch].
- **`v0n6`** (Clarification, High): [everything reading NOTA-shaped structure above the raw
  parser goes through typed structural macro nodes; surviving hand-parsing is a design
  violation; if a node can't express a shape, surface to the psyche, don't work around].
- **`kchq`** (Principle, High): [NOTA extension programming is structural matching over nodes;
  ordered macro-node definitions match most-specific-first; absence of a match is a
  formatting/spec error].
- **`5xss`** (Decision, High): [the match-pattern language is a typed enum of bounded
  primitives — arity, atom-case, atom-sigil, delimiter-type, atom literal — so macro data
  stays serializable].

## Delimiters, kind, and the generic/trait assignment (the heart of this arc)

- **`j9du`** (Principle, Low): [NOTA's delimiter set is a closed enum: 3 base pairs
  (parenthesis, square-bracket, brace) + 3 piped (pipe-parenthesis, pipe-text, pipe-brace);
  pipe-text is strings; pipe-parenthesis and pipe-brace are reserved extension points for
  schema].
- **`3742`** (Principle, High — **reworded this arc**): [a type's kind must be explicit at its
  DECLARATION (a delimiter, a wrapping variant, or a reserved keyword head like Vector/Map),
  never left to syntactic-slot convention; positional-by-convention recognition of a
  parameterized declaration is the guessing this forbids; name-resolution at use sites against
  an explicit declaration is the legitimate mechanism].
- **`hh3z`** (Decision, High): [generics use pipe-parenthesis `(| … |)`; declaration is
  `Name (| [params] body |)` — pipe-paren marks the generic, params are the binder list, body
  is an ordinary struct/enum nested inside; realizes `j9du`, satisfies `3742`].
- **`bpyu`** (Decision, High — **recorded this arc**): [pipe-brace `{| … |}` is the trait/impl
  construct (traits and trait-impls as data), the second of `j9du`'s extension points;
  supersedes the deprecated pipe-brace-declares-a-struct assignment].
- **`n1px`** (Decision, Medium — **supersedes `7m84`**): [assembled schema stays legal NOTA;
  authored declarations use the positional struct/enum forms — the pipe delimiters are
  generics and traits, NOT declaration forms; inline PascalCase introduces local reusable
  types before later references; lowercase camelCase stays field names].
- **`own9`** (Correction, High): [the @-binder surface is abandoned; the authored surface is
  positional `{…}` struct bodies and `[…]` enum/variant lists; legacy pipe DECLARATION forms
  are transitional, replaced by the positional form].
- **`wqdi`** (Principle): [multi-argument type references use NOTA's flat positional form —
  head then arguments inline, like `Map K V` — not a grouped form]. (Generic *use* form.)
- **`3qjw`** (Decision, Medium) / **`0b9q`** (Correction): [pipe-text `[| … |]` is the
  bracket-safe/multiline string with common-indentation stripping; escape literal close-markers
  rather than widen fences]. (The one pre-assigned pipe slot.)
- **`qw1j`** (square-bracket = vector invariant), **`ghw7`/`1rci`** (brace = strict
  key-value map / namespace; key-value-ness is NOTA-level), **`f743`** (schema owns
  declarations, not NOTA; plain positions name scalars/composites) — base-delimiter meanings,
  orthogonal and unchanged.

## Component triad & the hand-written boundary

- **`zjmc`** (Principle, High): [the Signal/Nexus/SEMA reaction-frame types Work, Action, and
  the canonical five-variant action set are workspace-universal — declared once and bound per
  component; re-authoring them per component is a design failure].
- **`5hjv`** (Constraint, High): [generated schema types are the source of every operation
  data type; handwritten Rust may only implement BEHAVIOR on those generated nouns]. The
  deliberate hand-written boundary (not debt).
- **`ov30`** (Principle, High): [a struct field's role is its type; no two fields share a
  type; newtype-per-role / dimensional correctness; a Vector is a Map over an ordinal index;
  field-name = type-name by default].

## Verified current state (the cleanup landed)

Active pipe-delimiter assignment: `[| |]` = strings; `(| |)` = generic declaration (`hh3z`);
`{| |}` = trait/impl (`bpyu`). Generic *use* stays the flat `(Head Arg…)` name-resolved form
(`wqdi`/`3742`), not a pipe form. `td1d`/`010y`/`nbvg` hard-removed (Lookup returns
not-found); `7m84` superseded by `n1px`; `1rci`/`f743` clarified and active; `3742` reworded;
`hh3z`/`bpyu`/`own9` active. **No active record asserts pipe-brace=struct, treats legacy pipe
declarations as the authored surface, or contradicts `hh3z`/`bpyu`.** The store is internally
consistent post-cleanup.
