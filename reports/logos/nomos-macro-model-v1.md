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
only for genuine **names**: field names (`name`, `reference`), map keys, feature names
(`nota-text`), and local input bindings.

```
MacroName.( <input-type>  <result-template> )
```

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
  WireNewtype.( NewtypeDeclaration  <result-template> )
  Vector.( VectorApplication  <result-template> )
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

## 2. Sound input typing — the resolution path

**[ruling 25c]** The input section **names the input type**; every by-name access in the
body **resolves against that type's schema**. The input type here is the schema's own
newtype-declaration type, exposed to Nomos over **signal-nomos** (ruling 16). Its real
field shape [evidence, `schema-rust/src/lib.rs:1099-1111`]:

```rust
pub struct RustNewtype { name: Name, reference: TypeReference }   // accessors name(), reference()
```

So the schema-side declaration type carries two fields — **`name` (type `Name`)** and
**`reference` (type `TypeReference`)**. As a schema type it is [proposal]:

```
NewtypeDeclaration.{ Name  reference.TypeReference }
```

Field names by the composed rule [ruling]: `Name` → **`name`** (snake_case of the type);
the second field is given the **explicit** name **`reference`** (the composed rule permits
an explicit name — and the real code uses `reference`, not the naive `type_reference`,
`lib.rs:1109`). **The resolution path:** a macro whose input type is `NewtypeDeclaration`
has exactly the fields `name` and `reference` in scope; `name`/`reference` in the body bind
to those fields, resolved against the `NewtypeDeclaration` schema served by signal-nomos.
There is no dangling access — the accessible names are precisely the declared type's fields.
(v0's `declaration.name`/`.inner` failed because `SchemaNewtype`'s field schema was never
shown and `inner` was not one of its fields.)

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
WireNewtype.( NewtypeDeclaration
  Public.Newtype.(
    $name
    $(WireAttributes)
    $reference
  )
)

WireAttributes.( Unit
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ] )
```

**Variant B (dedicated bracket):**

```
WireNewtype.( NewtypeDeclaration
  Public.Newtype.(
    <<name>>
    <<(WireAttributes)>>
    <<reference>>
  )
)

WireAttributes.( Unit
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ] )
```

Reading either: `WireNewtype` is the macro name (head); `NewtypeDeclaration` is the input
type (§2); the `Public.Newtype.( … )` structure is the **quoted** logos result template
(the psyche-authored v2 target); `$name`/`<<name>>` and `$reference`/`<<reference>>`
**realize** the input's `name` and `reference` fields; `$(WireAttributes)`/`<<(WireAttributes)>>`
**recursively invokes** the `WireAttributes` macro, whose result — the constant attribute
vector — is realized as the second slot. `WireAttributes` takes `Unit` (no input) and its
template is pure logos (no escapes).

**End-to-end (variant A):** schema `CommitSequence.{ Integer }` → recognized as a
`WireNewtype` invocation over the typed `NewtypeDeclaration( name = CommitSequence,
reference = Integer )` (object-to-object, ruling 15) → Nomos realizes `$name`→`CommitSequence`,
`$reference`→`Integer`, and expands `$(WireAttributes)` → the logos:

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
