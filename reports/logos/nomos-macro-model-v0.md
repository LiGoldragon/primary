# Nomos macro model v0 — terminology, hygiene, and a syntax strawman

Grounds the psyche's session-3 Nomos vision (design-v0.md §1.4) in the standard macro
vocabulary he asked to be taught, analyzes whether his identity-bearing objects make
hygiene a non-problem, and proposes a Nomos syntax strawman with two end-to-end worked
examples.

Discipline: **[standard]** = established fact/vocabulary (with a real citation where a
workspace example exists); **[agent analysis]** = my reasoning, flagged; **[proposal]** =
strawman syntax awaiting markup; **[psyche ruling]** cites design-v0.md §1.4. Written
2026-07-11 (session `schema-codex`, lane `nomos-macro-model`). Samples parse-checked
against nota 0.7.0 `f8de7a51`.

## Part A — The standard macro vocabulary (as requested)

**Quote** [standard]. Suppress evaluation; treat code as data. Common Lisp `'x` =
`(quote x)` yields the *symbol* `x`, not its value. In a macro, a quoted template is
*produced as structure*, not run.

**Quasiquote / backquote** [standard]. A template that is quoted *except* for marked
holes. Common Lisp `` ` `` (backquote), Scheme `` ` ``. The template is mostly literal
structure with a few evaluated positions.

**Unquote (comma)** [standard]. Inside a quasiquote, `,x` evaluates `x` and inserts its
value. `` `(1 ,x 3) `` with `x = 2` → `(1 2 3)`.

**Unquote-splicing (comma-at)** [standard]. `,@xs` evaluates `xs` (a list) and splices its
*elements* into the surrounding list. `` `(1 ,@xs 4) `` with `xs = (2 3)` → `(1 2 3 4)`.

**Hygiene** [standard]. A macro's introduced identifiers must not accidentally capture, or
be captured by, identifiers at the use site. Scheme `syntax-rules` is hygienic by
construction; Common Lisp `defmacro` is not (you call `gensym` for a fresh unique symbol).

**Pattern vs procedural macros** [standard]. *Pattern* (declarative) macros match a syntax
pattern and rewrite by template — Scheme `syntax-rules`, Rust `macro_rules!`. *Procedural*
macros run arbitrary code over the syntax tree — Common Lisp `defmacro`, Rust proc-macros
(which build output with `quote!`).

**Staging** [standard]. Explicit separation of compile-time (meta) from run-time
computation, often multi-level and *typed*. MetaML brackets `<e>` (quote / next stage) and
escape `~e` (splice); Template Haskell typed quotes `[|| e ||]` and typed splices
`$$( e )`, where the generated code's *type* is tracked.

### A.1 Compact real examples

Common Lisp backquote/comma (procedural; note the capture risk on `tmp`):

```lisp
(defmacro swap (a b)
  `(let ((tmp ,a))      ; let, tmp quoted (structure); ,a inserted (unquote)
     (setf ,a ,b)
     (setf ,b tmp)))
```

Scheme `syntax-rules` — hygienic by construction, `tmp` cannot capture:

```scheme
(define-syntax swap!
  (syntax-rules () ((_ a b) (let ((tmp a)) (set! a b) (set! b tmp)))))
```

Racket goes further: **syntax objects** carry lexical context (scope sets), so every
identifier knows its binding scope — hygiene is a property of the object, not a
convention.

Rust `quote!{ #name }` interpolation (proc-macro quasiquote; `#name` is the unquote): **the
workspace's own schema-rust emitter is written in exactly this idiom.** Real emitter lines:

- `schema-rust/src/migration.rs:253` — `quote! { pub #field: #field_type, }`
- `schema-rust/src/migration.rs:450` — `quote! { #name(#payload), }`

Here `pub`, `:`, `,`, the parentheses are quoted structure; `#field`, `#field_type`,
`#name`, `#payload` are unquotes interpolating Rust values into the emitted tokens. Nomos
generalizes this already-present pattern into a first-class **typed** macro model.

Template Haskell / MetaML are the **typed-staging precedent** most relevant to Nomos: the
splice/quote boundary carries a type, so a generated fragment is checked against the type
it must fill — exactly Nomos's situation (schema-typed input, logos-typed result).

### A.2 His words mapped to the terms [psyche ruling → standard]

| His words (design-v0 §1.4) | Standard term |
|---|---|
| "a **pure object** … as if passing the object directly" (ruling 19) | **quoted** — inserted as structure, unevaluated |
| "a **realized object** … turns into something in logos" (ruling 19) | **unquoted / spliced** — evaluated/expanded into the result |
| macro **input section** and **result section** (ruling 18) | a **typed macro signature** — typed input → typed (logos) result, in the MetaML / Template-Haskell typed-staging sense |
| body accesses input subcomponents **by name**, "defined in schemas" (ruling 18) | **typed destructuring over schema field names** — pattern-binding a schema-typed value and reading its named fields |
| pass **branches** to inner macros (ruling 20) | **sub-template expansion / macro delegation** — realizing a branch that is itself a macro invocation |

## Part B — Is hygiene a non-problem for Nomos? [agent analysis, flagged]

**The reasoning.** Lisps invented hygiene to solve **name capture**: because macros
operate on textual symbols, a macro-introduced `tmp` can collide with a use-site `tmp`.
Every hygiene mechanism (gensym, `syntax-rules`, Racket scope sets) exists to keep
identifiers with the *same spelling* distinct by tracking lexical context.

Nomos, per the design vision, operates on **identity-bearing objects**, not spellings:
CoreSchema→CoreLogos is a **continuous minted-identifier space**, with names only
*projected* through NameTables (design-v0 §2, §1.2). If every binding is a *minted
identity*, then two bindings that both project the name `tmp` are **two distinct
identities**. A macro that constructs logos nodes references its binders *by identity*; a
use-site identity that happens to project the same name is a different identity; they
cannot collide. **Capture dissolves by construction** — the very condition hygiene fights
(same-spelling collision) is impossible when the spelling is a non-authoritative
projection of a unique identity.

Two aspects, both covered:
- **Introduced-binder capture** (macro's `tmp` vs caller's `tmp`): each is a distinct
  minted identity; no capture. Where a macro must introduce a *fresh* binding, it **mints a
  new identifier** — which is exactly `gensym`, but native and automatic (identifier
  allocation is the CoreSchema/CoreLogos primitive), not a bolted-on escape hatch.
- **Referenced-free hygiene** (a template's reference to `Vec`/`let` should mean the
  macro-definition-site thing, not a use-site shadow): covered **iff** the macro captures
  its referenced frees as *identities at definition time*, so the reference is an identity,
  not a name to be re-resolved at the use site.

**So the strong claim holds for the intended architecture**: hygiene is not a feature Nomos
must implement; it is a property that falls out of identity-primary binding, the way it
falls out of Racket scope sets — but taken further, because identity (not name) is the
primary key and fresh-identity allocation subsumes gensym.

**Limits, stated honestly:**
1. **The identity layer is vision, not landed.** `TrueSchema` (the named semantic layer) IS
   landed (verified: `schema-rust/ARCHITECTURE.md` uses `schema_language::TrueSchema`
   throughout; `RustTrueSchemaLowering` is the real lowering entry). But the **CoreSchema /
   CoreLogos stringless minted-identifier + NameTable** layer this argument depends on is
   **design vision** (design-v0 §2, psyche-stated) — a grep of `schema-rust/src` finds
   `CoreSchema`/`NameTable` **zero** times. The "capture impossible by construction" claim
   is **conditional** on that layer being built as specified.
2. **Reference-hygiene is a design requirement, not automatic.** It holds only if macro
   templates bind their referenced frees to identities at *definition* time (aspect 2
   above). If a template carried bare projected names to be re-resolved at the use site,
   name capture would re-enter. So "identity-bearing" must extend to template *references*,
   not just *binders* — state this as a Nomos design obligation.
3. **Projection collisions are a display concern, not a semantic one.** Two distinct
   identities projecting the same name are unambiguous to the machine but may confuse a
   human reader; the NameTable projection may need a disambiguating suffix on display (the
   same rule as the repeated-field-name disambiguator, design-v0 §1.2). This is cosmetic,
   not capture.

## Part C — Nomos syntax strawman [proposal throughout]

Consistent with the settled grammar (dotted application/variants, `key.Value` pairs). Shown
in **scheme-current primary** delimiters (parens for application/record, brackets for
vectors) so the leaning reshuffle status is respected; the same forms re-delimit trivially
if the reshuffle lands.

### C.1 The quote / realize marking mechanism — primary and one alternative

**Primary [proposal]:** the result template is **quoted by default** (a pure logos
template), and a subcomponent is **realized** by the dotted variant **`Realize.( … )`**
(the unquote), with **`Splice.( … )`** for splicing a vector's elements (unquote-splicing).
This reuses the **already-settled dot-application binding** (ruling 5/12) — `Realize.(x)` is
just a dotted variant — so it needs **no new grammar mechanism**, and it reads as the
language rather than as punctuation.

**Alternative [proposal]:** a **sigil prefix** in the Lisp tradition (e.g. `~x` for realize,
`~@xs` for splice). Rejected as primary: a leading sigil is a *new* raw-grammar token
(nota currently retired the `@`-sigil surface and has no unquote sigil), whereas
`Realize.(…)` binds through the dotted mechanism nota is already gaining. The sigil is
terser but fights the "feels like logos, not exact-syntax" ruling (ruling 7).

Mapping: **default = quoted = pure object**; **`Realize.(…)` = unquote = realized object**;
**`Splice.(…)` = unquote-splicing**; a fresh binder is **`Fresh.(…)` = gensym** (mint a new
identity).

### C.2 Macro definition shape

Input section (schema-typed, destructured by name) + result section (a quasiquoted logos
template). By-name access is dotted field access `binding.field` (ruling 18, "like struct
field access"):

```
Macro.(
  wireNewtype
  Input.( declaration.SchemaNewtype )
  Result.(
    Public.Newtype.(
      Realize.(declaration.name)
      [ Literal.[rustfmt.skip]
        ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
        Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
      Realize.(declaration.inner)
    )
  )
)
```

- `Input.( declaration.SchemaNewtype )` — binds `declaration` to the schema `Newtype` value
  (typed input, signal-nomos-exposed per ruling 16).
- `Result.( … )` — a **quasiquoted logos template**: the `Public.Newtype.( … )` structure is
  the v2 psyche-authored logos output target, produced verbatim (quoted) except for two
  holes.
- `Realize.(declaration.name)` / `Realize.(declaration.inner)` — **unquotes** reading the
  input's schema fields by name and inserting the realized value.
- The attribute vector is **pure** (quoted) — emitted verbatim; it is the constant wire
  attribute vector.

### C.3 Worked example 1 — the wire newtype, end to end

**Stage 1 — schema declaration in** (`schema-rust` newtype surface):

```
CommitSequence.{ Integer }
```

**Stage 2 — schema lowers into a macro invocation** (schema knows this is a macro via
signal-nomos, ruling 16; conversion is object-to-object, not text, ruling 15):

```
wireNewtype.( SchemaNewtype.( CommitSequence Integer ) )
```

**Stage 3 — Nomos expands** the macro (§C.2): the `Result` template is realized —
`declaration.name` → `CommitSequence`, `declaration.inner` → `Integer` — producing the
typed logos object (constructed via signal-logos, ruling 16):

```
Public.Newtype.(
  CommitSequence
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
  Integer
)
```

This is exactly the psyche-authored v2 logos (`syntax-mockup-v2.md` §1). Nothing
materializes at the logos→Rust step (transcription); the wordiness was produced by Nomos at
schema→logos, from the brief schema declaration.

### C.4 Worked example 2 — a generic (Vector) with branch delegation

**Stage 1 — schema in**: `Domains.{ Vector.(Domain) }` — a newtype whose inner type is a
generic application `Vector.(Domain)`.

**The delegation** (ruling 20): `wireNewtype` handles the newtype wrapper, but
`declaration.inner` is itself a macro invocation (`Vector`). Realizing that branch
**delegates** it to the inner `vector` macro — realization of a branch that is a macro
invocation *is* the tree delegation. The inner macro:

```
Macro.(
  vector
  Input.( application.SchemaVector )
  Result.( LogosGeneric.( Vec Realize.(application.element) ) )
)
```

**Stage 2 — invocation**: `wireNewtype.( SchemaNewtype.( Domains Vector.( SchemaVector.( Domain ) ) ) )`.

**Stage 3 — expansion**: `wireNewtype` realizes `declaration.inner`, which is the
`Vector.(…)` branch → delegates to `vector`, which realizes `application.element` → `Domain`,
producing `LogosGeneric.( Vec Domain )` (the exploded, non-sugared logos generic — logos
carries `Vec` explicitly, no `<>` sugar, ruling 17). Final logos:

```
Public.Newtype.(
  Domains
  [ Literal.[rustfmt.skip]
    ConfigurationAttribute.Feature.( nota-text [NotaDecode NotaDecodeTraced NotaEncode] )
    Derive.[rkyv.[Archive Serialize Deserialize] Clone Debug PartialEq Eq] ]
  LogosGeneric.( Vec Domain )
)
```

Oracle check: this transcribes to `pub struct Domains(Vec<Domain>);` + the standard
derives — the real generated Rust (`signal.rs:546`).

### C.5 Parse check [evidence]

`samples/v2-nomos-macros.nomos` (the two macro definitions) and
`samples/v2-logos-outputs.logos` (the two expansion targets) raw-parse under nota 0.7.0 —
see §C.6. As with all dotted forms, `Macro.`, `Input.`, `Realize.`, `declaration.name`
etc. split the dot onto the preceding atom today; binding them as single application nodes
is the settled ruling-5/12 raw-grammar change (nota-grammar-revision-v0.md §2.1), not yet
implemented.

### C.6 Reproduction

Samples: `reports/logos/samples/v2-nomos-macros.nomos`,
`reports/logos/samples/v2-logos-outputs.logos`. Harness (throwaway): `scratchpad/notaparse`
against a `git-archive/nota` worktree at `f8de7a51`.

## Summary — where the macro model is under-determined (verdict)

The frame is solid — Nomos as a typed procedural macro system in the quasiquote/unquote
tradition (result = quasiquote, `Realize.(…)` = unquote, input = typed schema
destructuring), with hygiene falling out of identity-primary binding rather than needing a
mechanism. What the psyche must pin next: **(1)** the quote/realize marking — confirm
`Realize.(…)`/`Splice.(…)` over a sigil, and whether the result template is
default-quoted-with-explicit-realize (assumed here) or the reverse; **(2)** the input
destructuring language — how a macro pattern names and binds nested schema subcomponents,
and what happens on partial/optional matches; **(3)** the identity layer — the
hygiene-by-identity guarantee is **conditional** on the not-yet-landed CoreSchema/CoreLogos
minted-identifier + NameTable machinery, and on macro templates capturing referenced frees
as identities (a stated design obligation); **(4)** logos's own generic/expression
vocabulary (`LogosGeneric` here is a placeholder) — ruling 17 says spec logos first, and the
macro result type cannot be finalized until that exploded logos vocabulary exists; **(5)**
Nomos's own surface grammar, which the psyche marked **unknown** — this strawman assumes it
is NOTA-shaped and dotted, which he has not confirmed.
