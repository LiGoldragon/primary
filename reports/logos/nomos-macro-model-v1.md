# Nomos macro model v1 — headless, sound input typing, structural escapes

Supersedes `nomos-macro-model-v0.md`. The psyche tore into the v0 strawman (design-v0.md
ruling 25): no per-declaration `Macro.` head, no `Input.`/`Result.` label heads
(both "a named attributes design again … you agents really dont like the nota
philosophy"), the input section must DESCRIBE THE INPUT TYPE with body accesses resolving
against that type's schema (v0's `declaration.name`/`.inner` were dangling), escapes must
be STRUCTURAL and visually distinct ("$ or # type prefix"), and recursive macro invocation
is required. This v1 answers all five.

Discipline: **[ruling]** cites design-v0.md; **[evidence]** is worker-verified with source;
**[proposal]** is strawman awaiting markup. Written 2026-07-13 (session `schema-codex`, lane
`nomos-macro-model-v1`). Samples parse-checked against nota 0.7.0 `f8de7a51`.

## 1. Headless declarations and the document layout

**[ruling 25a/25b]** There is **no `Macro.` head** per declaration (the nomos file kind's
expectation already makes every declaration a macro) and **no `Input.`/`Result.` label
heads** (sections are positional). A macro declaration is headless of `Macro.`: its own
**name is the head** (exactly as a schema newtype is `CommitSequence.{ … }`, name-as-head),
and its two sections — **input type** then **result template** — are **positional**:

**Macro identifiers are CAPITALIZED** [ruling — "why lowercase? isnt WireNewtype a thing?"].
`Map` and `Vector` are macros and are capitalized objects; a macro is a declaration with a
minted identity invoked in **object** position, so capitalization semantics make it
**capitalized-leading** (`WireNewtype`, `WireAttributes`, `Vector`). Lowercase-leading stays
only for genuine **names**: field names (`name`, `type`), map keys, feature names
(`nota-text`), and local input bindings.

```
MacroName.( { <meta-types> }  <result-template> )
```

The first section is an **inline struct shape** over standard meta-types (§2), not a named
type; the second is the result template.

**The macro KINDS** [ruling — his earlier dispatch-mode ruling, §3]: the ruled design has
exactly **two** — **named macros** (present in the macro table, dispatched by name) and
**structural macros** (per-section positional defaults). By the **per-kind-blocks
invariant** (a new class of meta-objects earns a new block), these are **two separate blocks**
in a nomos document — which is what dissolves any need for a per-declaration kind head.
Document-level layout [proposal, scheme-reshuffled — wave one includes the reshuffle, ruling
24]:

```
;; a nomos document — two per-kind sections, positional under the nomos file kind.
;; Section 1: named macros (a vector of headless declarations).
[
  WireNewtype.( { Name Type }  <result-template> )
  Vector.( { Type }  <result-template> )
]
;; Section 2: structural macros (per-section defaults).
[
  ...structural macro declarations...
]
```

The two sections are identified by **position under the document grammar**, not by a label —
the same way schema distinguishes its `{…}` type block from its `[…]` operation lists by
delimiter + position, never by a keyword. [proposal] the exact section delimiters follow
whatever the nomos document schema fixes.

## 2. Sound input typing — an inline struct shape over standard meta-types

**[ruling 25c + psyche design statement 2026-07-13]** The input section is an **inline
struct shape** over a small vocabulary of standard meta-types — **not** a binding to a named
schema type. His words: **"so if WireNewType only takes a name and inner type, then the
input field would be `{ Name Type }`. Name and Type could be pretty standard things, perhaps
nomos builtins, even a concept shared with schema somehow (it is a schema concept after
all)."** So WireNewtype's input is literally `{ Name Type }`; the v0 `declaration.SchemaNewtype`
binding (and its `declaration.` prefix) **dissolves**.

### (a) Body accessors from the derived-field-name rule — no explicit binding

The input `{ Name Type }` **yields accessors automatically** via the composed derived-
field-name rule [ruling]: `Name` → **`name`** (snake_case of the meta-type), `Type` →
**`type`**. The body references `name` and `type` directly — there is no binding name and no
`declaration.` prefix, because there is exactly one input and its fields are in scope by their
derived names. The resolution is sound because the field *names* are computed from the input
struct's own meta-types, not guessed.

### (b) Repeated meta-types take the explicit-disambiguator rule

Exactly like struct fields, a repeated meta-type needs an explicit name [ruling — the composed
rule]. A `Map`-defining macro whose input is two `Type`s cannot leave both as `type`:

```
Map.( { Name  key.Type  value.Type }  <result-template> )
```

`Name` → `name`; the two `Type`s are disambiguated by explicit names `key` and `value` (the
same repeated-type rule as `Private.secretDigest.StateDigest` in the logos field form). Body
accesses are then `name`, `key`, `value`.

### (c) A plausible standard meta-type vocabulary [proposal]

Grounded in what schema declarations actually contain (not invented) — the two macro KINDS
need only what schema's own declaration forms carry:

- **`Name`** — a declared identifier (every declaration has one).
- **`Type`** — a type reference (newtype wrapped type, field type, generic argument). This is
  schema's `TypeReference` vocabulary (evidence below).
- **`Fields`** — an ordered vector of `{ Name Type }` (a struct's named fields).
- **`Variants`** — an ordered vector of variant shapes (an enum's variants: unit, tuple, or
  named-field).
- **`Attributes`** — the attribute vector (as in the wire attribute list).

So WireNewtype takes `{ Name Type }`; a struct macro takes `{ Name Fields }`; an enum macro
takes `{ Name Variants }`; `Map` takes `{ Name key.Type value.Type }`. Nothing here is beyond
what a schema `TypeDeclaration` already carries.

### (d) The shared-concept question — flagged [leaning, his hedges intact]

His hedges: **"perhaps nomos builtins, even a concept shared with schema somehow (it is a
schema concept after all)."** These meta-types are **schema's own self-description
vocabulary** — a meta-schema. So nomos's builtins may simply **BE** schema's meta-types,
carried **once** in the shared seed vocabulary and exposed via **signal-nomos**, rather than
redefined. [evidence] This is concrete, not hypothetical: the prior design
`reports/schema-designer/25-schema-self-describing-design.md` already (i) makes schema
**self-describing** through its own `TypeReference`/`Name` notation (its "five locked
decisions"), and (ii) **unifies the duplicate `TypeReference` vocabularies into the seed
crate `nota-next`** ("the structural type-reference vocabulary MUST live in `nota-next` (or
lower)", that doc §Area-2). If schema's `Name`/`TypeReference` already live once in the seed
crate, **nomos's `Name`/`Type` meta-types are the same objects** — shared, not duplicated.
**[leaning, not ruled]** whether nomos's meta-types are exactly schema's seed vocabulary or a
nomos-side mirror is the psyche's call; the seed-crate precedent makes "shared" the low-cost
option.

## 3. The escape set — enumerated and argued closed

Three template escapes, from the Lisp precedent plus his ruling 25e:

1. **realize** — unquote **one** object (Lisp `,` / Rust `#name`). Insert the realized value
   of a field or expression at one position.
2. **splice** — unquote a **sequence** into the surrounding vector (Lisp `,@` / Rust
   `#(...)*`). Where a sub-result is several elements that flatten into an enclosing vector.
3. **recursive macro invocation** — call another macro in the template [ruling 25e], its
   result realized (or spliced) in place.

**Closure argument, honestly.** Lisp template construction needs **exactly** unquote +
unquote-splicing; everything else (including calling another macro) is *unquote of a call*:
`,(foo x)`. So at the primitive level Nomos needs **realize + splice**, and **recursive
invocation is realize-of-a-macro-application** — not a fourth primitive, but worth a
distinct surface form for readability (a call is visually a call). That is the closed core.

**One genuine candidate for a fourth escape, flagged not hidden: name synthesis
(realize-into-name-position).** Realize inserts a *value*; but a macro sometimes must
*construct a new identifier* and place it in a **name** position — e.g. deriving the field
name `state_digest` from the type `StateDigest`, or minting a fresh binder (the gensym
case). Lisp does this with `intern`/`gensym` under unquote; Rust proc-macros use
`format_ident!`. This is a **real distinct need** (name position ≠ value position, and
identifier construction ≠ value insertion). Under the identity model it is "mint/derive an
identity, then realize it as a name" — I flag it as a likely **fourth** escape
(`synthesizeName`) the psyche should rule on, rather than pretend realize covers it.

## 4. Structural escape syntax — two proposals, same example

Both make the escape **visually unmistakable** inside a template that otherwise **is
logos**. Nomos owns its own grammar (ruling 14/25d), so a nomos-only lexical or bracket
addition is legitimate.

**Proposal A — sigil (`$`), owned by the nomos grammar.** `$name` realize; `$@items`
splice; `$(MacroName args)` recursive call. One sentence: terse and instantly distinct
(matches the universal `$`/`#` macro convention), but adds a **new lexical token** the nomos
tokenizer must own — generic nota reads `$name` as a plain atom, so the escape does not bind there (§6).

**Proposal B — dedicated bracket (`<< >>`), a nomos-only delimiter.** `<<name>>` realize;
`<<@items>>` splice; `<<(MacroName args)>>` recursive call. One sentence: unmistakable and
bracket-balanced like the rest of NOTA (no adjacency ambiguity), but spends a whole new
delimiter pair and is heavier to read/write than a one-char sigil.

The **same** worked example (§5) is shown in both.

## 5. Worked example — headless, sound input, structural escapes, recursive call

The newtype macro **delegates the standard attribute vector to an inner `WireAttributes`
macro** — tree delegation (ruling 20) made concrete via recursive invocation (ruling 25e).

**Variant A (sigil):**

```
WireNewtype.( { Name Type }
  Public.Newtype.(
    $name
    $(WireAttributes)
    $type
  )
)

WireAttributes.( { }
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ] )
```

**Variant B (dedicated bracket):**

```
WireNewtype.( { Name Type }
  Public.Newtype.(
    <<name>>
    <<(WireAttributes)>>
    <<type>>
  )
)

WireAttributes.( { }
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ] )
```

Reading either: `WireNewtype` is the macro name (head); `{ Name Type }` is the input struct
shape (§2), yielding accessors `name` and `type`; the `Public.Newtype.( … )` structure is the
**quoted** logos result template (the psyche-authored v2 target); `$name`/`<<name>>` and
`$type`/`<<type>>` **realize** the input's `name` and `type` fields;
`$(WireAttributes)`/`<<(WireAttributes)>>`
**recursively invokes** the `WireAttributes` macro, whose result — the constant attribute
vector — is realized as the second slot. `WireAttributes` takes an empty input `{ }` and its
template is pure logos (no escapes).

**End-to-end (variant A):** schema `CommitSequence.{ Integer }` → recognized as a
`WireNewtype` invocation over the input `{ Name Type }` filled `{ CommitSequence Integer }`
(object-to-object, ruling 15) → Nomos realizes `$name`→`CommitSequence`, `$type`→`Integer`,
and expands `$(WireAttributes)` → the logos:

```
Public.Newtype.(
  CommitSequence
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
  Integer
)
```

which transcribes to `pub struct CommitSequence(Integer);` + the standard derives (the
oracle).

## 6. Parse check [evidence]

`samples/v1-nomos-sigil.nomos` (variant A) and `samples/v1-nomos-bracket.nomos` (variant B).
Both files **raw-parse OK** in nota 0.7.0 (4 root objects each) — but in **neither** does the
escape *bind* with escape meaning. Measured:

- **Variant A (sigil `$`)**: `$name` and `$reference` are read as **single opaque atoms**
  (`$` is bare-atom-safe), and `$(WireAttributes)` splits into an atom `$` **plus** a separate
  `(WireAttributes)` paren — the call is not bound to the sigil. Nomos must **own `$`** as a
  lexical escape token.
- **Variant B (bracket `<< >>`)**: it does **not fail** — but not because it works. `<`/`>`
  are bare-atom-safe, so `<<name>>` is read as a **single opaque atom** and
  `<<(WireAttributes)>>` splits into `<<` + `(WireAttributes)` + `>>` (three objects). The
  bracket is **silently mis-lexed as atoms**, never recognized as a delimiter pair; nomos must
  **register `<< >>`** as real delimiters for it to bind.
- The **logos result templates** themselves (the `Public.Newtype.( … )` bodies) raw-parse as
  the dotted forms always have (dot rides on the preceding atom, pending the ruling-5 raw
  binding).

Headline, corrected and honest: **both surfaces raw-parse today, and in both the escape is
absorbed as bare atoms rather than binding as an escape** — so today's parseability does not
distinguish them; each is a distinct nomos-owned grammar addition (a `$` lexical token, or a
`<< >>` delimiter pair). This is exactly why the psyche ruled the escape must be *structural
and nomos-owned* (ruling 25d): generic nota gives it escape meaning for free in neither case.

## 7. Verdict — the escape set

Two primitives close the template-construction core exactly as in Lisp — **realize** (unquote
one object) and **splice** (unquote a sequence) — and **recursive macro invocation is
realize-of-a-macro-call**, deserving a distinct surface form but not a new primitive. The
one honest open is a likely **fourth** escape, **name synthesis** (realize-into-name-position
/ identifier construction, the gensym-and-derive case), which the psyche should rule on
rather than fold into realize.
