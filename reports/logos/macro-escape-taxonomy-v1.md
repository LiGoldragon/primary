# Macro escape taxonomy v1 — a closed survey of escape kinds across elaborate macro systems, mapped to typed-data Nomos

Design pickup document. Session `ProtosEngine`, lane `EscapeTaxonomy`, Fresh, Opus 4.8
(1M), 2026-07-19. This answers the psyche's three questions — *"dont we need more than one
type of escaping? What if we pass a type directly to another macro? What are all the
different types of escapes in the most elaborate macro systems in the world?"* — under his
framing constraint *"note that our macros are on typed data, so its all a bit different."*

Read this alongside `nomos-macro-model-v1.md` (the ruled realize / splice / recursive-invocation
core and the flagged fourth escape, name synthesis) and the field-name ban (Ruling E,
`stream-construct-design-v1.md` §0.0: field names are illegal everywhere; identifiers are
positional type-identity objects or deterministically derived, never free strings). Those two
local facts do most of the dissolving in §3.

Provenance markers: **[foreign]** = a verbatim artifact from another language, cited for
contrast, never Protos syntax; **[local]** = a ruled or observed Nomos/Protos fact carried from
the reports above; **[recommendation]** = this agent's reading, explicitly awaiting the psyche's
ruling. No concrete Nomos syntax is proposed beyond the already-chosen base sigil `$`; no
schema/NOTA/logos/Protos spelling is invented here.

## 1. The framing that changes everything

Every system surveyed below except two (Zig and Julia) shares one starting assumption: **the
meta-program manipulates *syntax* — token streams (Rust `macro_rules`), untyped s-expressions
(Lisp reader output), or syntax objects that wrap tokens with lexical context (Scheme/Racket,
Template Haskell `Exp`).** In those systems an escape does two jobs at once: it (a) crosses from
the quoted world back to the computing world, and (b) reconciles the *names* in the injected
fragment with the *names* in the surrounding template. Job (b) — hygiene, gensym, stage levels,
name capture — exists **because the material is names**.

Nomos is not in that family. **[local]** Nomos transforms typed encoded-form values: schema
encoded form in, logos encoded form out. Its inputs are meta-typed values (`Name`, `Type`,
`Fields`, `Variants`, …); its output is a typed logos value. A `Type` is not a token spelling a
type — it is an encoded-form value carrying an encoded type identity. There are **no free field
names to capture** (field names are illegal everywhere; positions are typed slots). And by the
2026-07-19 ruling, **the schema-to-logos transformation performs no string manipulation,
introduction, or reading of any kind** — identifiers inside it are opaque typed values (encoded
identities), and the deterministic name spelling (e.g. an output field's Rust name) is **not**
computed inside the transformation but supplied by a separate NameTable channel outside the
encoded flow. §6 analyzes every escape kind against this no-strings invariant.

So the honest thesis of this survey: **the escape kinds that exist to reconcile *names* mostly
dissolve for Nomos, and the escape kinds that exist to reconcile *values* remain.** Nomos sits
in the same corner as Zig `comptime` and Julia's value-level `Expr` manipulation — typed values,
including types themselves, flowing through ordinary computation — not in the corner of Template
Haskell name quotes and Scheme hygiene. The two-primitive core the psyche already has (realize +
splice) is the value-reconciliation core, and it is close to complete.

## 2. The systems, briefly, in the two families

### 2.1 Syntax-manipulating (name reconciliation is a first-class problem)

**Lisp / Scheme / Racket.** Quasiquote builds a list template; escapes step out of it.
**[foreign]**

```
`(1 2 ,x ,@ys)              ; Common Lisp: , unquotes x, ,@ splices ys
#`(let ([t #,val]) t)       ; Racket: #` quasisyntax, #, unsyntax, #,@ unsyntax-splicing
```

Scheme/Racket add **syntax objects** (`#'e`, `syntax`): a token tree plus its lexical context, so
`syntax-rules` / `syntax-case` macros are **automatically hygienic** — an identifier introduced
by the macro cannot capture or be captured by user identifiers, because each carries its scope
set. Deliberate capture requires `datum->syntax` to graft one form's lexical context onto
another. Fresh names come from `generate-temporary`. Nested quasiquote tracks **levels**: an inner
`` ` `` raises the level, each `,` lowers it, and only at level zero does an unquote actually
compute.

**Clojure.** Syntax-quote is the same shape with a hygiene shortcut baked into printing.
**[foreign]**

```
`(let [x# ~val] (+ x# ~@more))   ; ` syntax-quote, ~ unquote, ~@ splice, x# auto-gensym
```

Syntax-quote **namespace-qualifies** every plain symbol (`map` becomes `clojure.core/map`) — a
poor-man's hygiene by fully-qualifying — and `foo#` inside one syntax-quote expands to a single
fresh gensym, the ergonomic answer to name capture without full syntax objects.

**Template Haskell.** The richest *typed* member of this family, and the one that most directly
answers the type-passing question. It has **two** quote/splice pairs. **[foreign]**

```
[| f x |]        -- untyped expression quote       :: Q Exp
$( g )           -- untyped splice
$x               -- untyped splice, short form
[|| f x ||]      -- TYPED quote                     :: Code Q a   (was Q (TExp a))
$$( g )          -- typed splice
'foldr           -- value-name quote               :: Name
''Bool           -- TYPE-name quote                 :: Name   <-- literally "pass a type"
[t| Maybe Int |] -- type quote                      :: Q Type
[d| ... |]       -- declaration quote,  [p| |] pattern quote
```

TH is **not** hygienic by default; freshness is explicit via `newName :: Q Name` (a gensym), while
`mkName` makes a capturing, non-fresh name on purpose. The two name-quote sigils are the crux:
`'x` reifies a *term-level* name, and **`''T` reifies a *type-level* name** — a distinct sigil
precisely because, in a token/name world, a type occupies a different namespace than a value and
must be quoted differently.

**Rust.** Two mechanisms. `macro_rules!` matches token trees by **fragment specifier**, and one of
those specifiers is literally "a type": **[foreign]**

```
macro_rules! wrap { ($n:ident : $t:ty) => { struct $n($t); }; }
//                          ^^^ident        ^^^ty  <-- type captured as a fragment
$( $x:expr ),*    // repetition = splice-into-sequence on the matched side
```

Fragment specifiers: `expr ty ident path pat tt block item stmt lifetime literal meta vis`. The
`$(...)*` / `$(...),*` repetition is the splice. Proc-macros use `quote!` with `#` interpolation:

```
quote! { struct #name ( #(#field_types),* ); }   // #name realize, #(...) splice
format_ident!("{}_inner", base)                  // name synthesis
```

Rust hygiene is carried on `Span`: `Span::call_site()` (unhygienic, sees caller scope) vs
`Span::mixed_site()` (macro-def scope). So Rust exposes **all** the name-reconciliation machinery
explicitly — type capture (`:ty`), name synthesis (`format_ident!`), hygiene (`Span`) — because it
is a token system.

**Julia.** Quotation yields a first-class `Expr` value. **[foreign]**

```
:(a + $x)                  # quote with interpolation
quote; a + $x; end         # block form
:(f($(args...)))           # splat-interpolation = splice
```

Julia macros are hygienic by default; `esc(e)` opts a fragment *out* of hygiene (evaluate in
caller scope), and `gensym()` mints fresh symbols. **Crucially, types in Julia are ordinary
runtime values** (`Int` is a value of type `DataType`), so "passing a type" is just passing a
value — no special sigil. Julia therefore straddles the two families: `Expr` manipulation is
syntactic, but the *type* dimension is already value-level.

**Elixir.** `quote`/`unquote` over a three-tuple AST. **[foreign]**

```
quote do: unquote(name)(unquote_splicing(args))
```

Hygienic by default; `var!(x)` and `Macro.var/2` deliberately break hygiene; the AST is plain data
(`{:{}, meta, args}`), so name reconciliation is again the whole game.

**Nim.** `quote do:` with backtick interpolation, plus a distinguishing feature: a macro parameter
may be declared **`untyped`** (raw AST) or **`typed`** (a *type-checked* AST node), and types are
passed as `typedesc[T]` / `type`. **[foreign]**

```
macro make(name: untyped, T: typed) = quote do: (var `name`: `T`)
```

Nim's `typed` parameters are a real step toward Nomos: the macro receives material that has
**already passed the type checker**, closer to "operating on typed data" than the pure-token
systems.

### 2.2 Value-manipulating typed staging (name reconciliation largely absent)

**MetaOCaml (BER MetaOCaml).** Homogeneous **typed** multi-stage programming. **[foreign]**

```
.< 1 + 2 >.          (* bracket: build a code value,   : int code *)
.~ e                 (* escape: splice a code value into a bracket *)
Runcode.run c        (* run: execute a completed code value *)
```

The escape `.~` is the *only* escape, and it is purely value-level: it inserts one `'a code` value
into a surrounding bracket, and the type system guarantees the result stays well-typed (`int code`
into an `int`-shaped hole). There is **no name-quote, no gensym escape, no hygiene escape** in the
user surface — variable binding under brackets is handled by the implementation's alpha-renaming,
and **types never appear as escaped values at all**: a type lives in the `'a` of `'a code`, checked
by OCaml's ordinary type system at the meta level. **Cross-stage persistence** lets an outer-stage
value be used inside a bracket without re-quoting. Levels are tracked by escape depth exactly as in
Lisp quasiquote, but every level is typed.

**Scala 3 quotes.** Typed staging on the JVM. **[foreign]**

```
'{ println(${ msg }) }            // '{ } quote : Expr[T],  ${ } splice
def show[T](using Type[T]): ...   // a TYPE is passed as a given Type[T]
'{ (x: T) => x }                  // T inside a quote resolves from the given Type[T]
Type.of[T]                        // summon a Type[T] representation
```

The pivotal detail for Nomos: **a type is passed to a macro as an ordinary implicit/context value
of type `Type[T]`.** There is no separate "type escape" sigil; you carry `given Type[T]` alongside
`Expr[U]` arguments, and inside a quote the compiler pulls the type from that given. Expressions and
types travel by the **same mechanism** (a typed value in scope), differing only in the wrapper type
(`Expr` vs `Type`). Splicing an expression is `${ }`; "splicing" a type is just referring to `T`,
which the given resolves.

**Zig `comptime`.** The purest "macros on typed data," and the system Nomos most resembles.
**[foreign]**

```
fn List(comptime T: type) type {         // a type is a value of type `type`
    return struct { items: []T };        // ordinary code, run at compile time
}
const x = List(u8);                       // "passing a type to a macro" = a function call
@typeInfo(T), @field(v, name), @Type(info) // reflect/construct types as values
```

Zig has **no quotation and therefore no escape sigil at all.** The meta-language *is* the object
language; compile-time code manipulates typed values — including values of type `type` — with the
same syntax as run-time code. There is nothing to escape *from*, so hygiene, gensym, splice, and
nested levels have no surface: you build a struct by calling normal functions that return typed
values. This is the endpoint of the "typed data dissolves the escapes" argument.

**Multi-stage programming literature (Taha/Sheard MetaML, λ-circle calculi).** Formalizes exactly
three operators — **bracket** `<e>` (delay/quote), **escape** `~e` (splice into the next-out
stage), **run** `!e` (execute) — plus **cross-stage persistence**. The theory's whole content is
that a *typed* staging calculus needs only these; the name-level apparatus of Lisp macros is a
separate concern the type system subsumes. This is the academic backing for keeping Nomos's escape
set tiny.

## 3. The closed taxonomy of escape kinds

Eight kinds cover every surface above. For each: what it does, which systems carry it, and — under
the psyche's constraint — whether typed-data Nomos genuinely needs it or the typed setting
dissolves it.

### Kind 1 — Value unquote (realize): insert one computed value into a hole

Insert the single result of a computation at one position in the template.

- **Has it:** everyone with quotation — Lisp `,`, Clojure `~`, TH `$x` / `$$x`, MetaOCaml `.~`,
  Scala `${ }`, Rust `#name`, Julia `$x`, Elixir `unquote`, Nim backtick, MSP `~e`.
- **Nomos:** **needed — this is `realize`, already ruled.** It is the irreducible value-crossing
  operation and does not dissolve. `$` is the chosen base sigil for it. **[local]**

### Kind 2 — Splice-into-sequence: flatten a sequence into the enclosing sequence

Insert *many* elements where one position sits, flattening into the surrounding vector.

- **Has it:** Lisp `,@`, Clojure `~@`, Rust `#(...)*` / `$(...)*`, Julia `$(xs...)`, Elixir
  `unquote_splicing`, TH via list splices. MetaOCaml/Scala have no dedicated splice operator —
  sequence building is done by ordinary list-valued code, which is itself a signal (see §4).
- **Nomos:** **needed — this is `splice`, already ruled.** Because logos results are vectors of
  declarations/attributes, flattening a sub-result into an enclosing vector is a real structural
  need, distinct from realize. It does not dissolve. **[local]**

### Kind 3 — Identifier / name passing: reference an existing name as data

Carry an existing binding's *name* (not its value) as an argument.

- **Has it:** TH `'x` (value name), Rust `$x:ident`, Lisp symbols-as-data, Nim `untyped` params.
  Needed in token systems because a name is a distinct kind of syntactic material.
- **Nomos:** **mostly dissolves.** **[local]** Field names are illegal everywhere; there are no
  free identifiers for a macro to receive and re-place. The identifiers Nomos handles are **type
  identities** (`CommitSequence`, `Integer`) — which are `Type`/`Name` meta-values, i.e. Kind 1
  material, not a separate name-passing channel — and **derived output names**, which the macro
  never authors. What survives is `Name` as a meta-type input, and that flows by realize. There is
  no residual need for a distinct name-passing escape.

### Kind 4 — TYPE passing: pass a type as a macro argument

Hand a type to a macro so it can build structure parameterized by that type. **(The psyche's
second question.)**

- **Has it, and how they spell it:**
  - **Template Haskell:** a distinct sigil, **`''T`**, reifying a *type-level* name to a `Name`,
    plus `[t| ... |]` type quotes — a type is a different namespace, so it needs its own escape.
  - **Scala 3:** **no sigil** — a `given Type[T]` context value carried alongside `Expr` args;
    inside a quote the type appears as `T` and the compiler resolves it from the given.
  - **Zig:** **no sigil** — a type is a value of type `type`; passing it is a plain argument
    `comptime T: type`.
  - **Julia:** **no sigil** — types are ordinary runtime values; passing one is passing a value.
  - **Nim:** a `typed` / `typedesc[T]` parameter — a type-checked node.
  - **MetaOCaml:** **cannot** pass a type as a staged value at all — types live in the `'a` of
    `'a code` at the meta type-system level, never as escaped runtime data.
- **Nomos:** **dissolves into Kind 1.** **[local]** A Nomos type *is* an encoded-form value (a
  `Type` meta-value with an encoded identity). Passing a type to another macro is therefore
  **value passing** — the same `realize` that inserts any input — and needs **no distinct
  type-escape.** Nomos is in the Zig/Julia/Scala corner (types are values), not the Template
  Haskell corner (types are a separate quoted namespace needing `''T`). See §5 for the direct
  answer.

### Kind 5 — Name synthesis / gensym: mint or derive a fresh identifier

Construct a new identifier and place it in a *name* position (fresh binder, or a name derived from
another datum).

- **Has it:** Lisp `gensym`, Clojure `foo#`, Racket `generate-temporary`, TH `newName`, Rust
  `format_ident!`, Julia/Elixir `gensym` / `Macro.var`.
- **Nomos:** **largely dissolves; a narrow residue is the honest open.** **[local]** Two sub-cases:
  - *Deriving* a name from a datum (e.g. an output field's name from its type and position) is
    **automatic** under the deterministic derived-name rule and the field-name ban — the macro
    author never writes it. This sub-case is fully absorbed.
  - *Minting a fresh binder* (the classic gensym, avoiding capture of a temporary) is the residual.
    In a value-transforming, single-expansion setting with no user-visible temporaries injected into
    a shared lexical scope, it is unclear this ever arises. This is the **fourth-escape question**
    flagged in `nomos-macro-model-v1.md §3`; §6 recommends against seating it pre-emptively.

### Kind 6 — Nested quoting levels / stage crossing: multiple quote depths

Quote inside a quote, with escape depth selecting which stage a computation runs at.

- **Has it:** Lisp nested backquote (level counting), MetaOCaml / Scala 3 / MetaML multi-stage
  brackets, nested TH quotes.
- **Nomos:** **dissolves for the current design.** **[local]** Nomos expansion is a **single stage**
  — schema encoded form to logos encoded form, one transformation. Recursive macro invocation
  (already ruled) is *realize-of-a-macro-call* within that one stage, **not** a raised quoting
  level: the callee's typed result flows back as a value, exactly one level. Unless the psyche
  later wants macros that *emit macro definitions* (a genuine second stage), no level-tracking
  escape is needed, and the `$` sigil never needs a depth count.

### Kind 7 — Hygiene control: govern capture and renaming of names

Prevent (or deliberately allow) macro-introduced names from capturing user names.

- **Has it:** Scheme/Racket automatic hygiene + `datum->syntax` to break it; Clojure
  namespace-qualification + `foo#`; Julia `esc`; Elixir `var!`; Rust `Span` (`call_site` vs
  `mixed_site`). Notably **MetaOCaml and Zig expose no hygiene control** — the typed value world has
  no name-capture surface.
- **Nomos:** **dissolves.** **[local]** Hygiene is a property of injecting *names* into a *lexical
  scope*. Nomos injects typed values into a typed structure; there is no ambient variable
  environment for a name to capture, no free field names, and output identifiers are
  deterministically derived rather than author-chosen. The typed-value setting removes the
  substrate hygiene operates on — the same reason Zig and MetaOCaml need no hygiene escape. This is
  the strongest instance of the psyche's intuition that "typed data makes it different."

### Kind 8 — Typed quote / typed splice: the escape carries a static type guarantee

The quote and its splices are statically typed, so an ill-typed injection is a compile error at
the meta level (`Code Q a`, `Expr[T]`, `'a code`).

- **Has it:** Typed TH `[|| ||]` / `$$`, MetaOCaml `'a code`, Scala 3 `Expr[T]`, MetaML. The untyped
  members (Lisp, Clojure, Rust tokens, Julia `Expr`, Elixir, untyped TH) do **not** — their splices
  can build ill-typed code that fails only later.
- **Nomos:** **this is the ambient condition, not a distinct escape.** **[local]** Nomos is
  typed-data-in / typed-data-out by construction, so *every* realize and splice is already a typed
  injection into a typed hole. Nomos gets Kind 8's guarantee for free and pervasively; it is not a
  separate escape kind to add, but it is the reason Kinds 3–7 collapse — the type system is already
  doing the reconciliation work that names-based systems spend escapes on.

### Compact taxonomy table

```
KIND                         SYSTEMS THAT SPELL IT (verbatim)                    NOMOS VERDICT
---------------------------  --------------------------------------------------  ------------------------------
1 value unquote / realize    Lisp ,   Clojure ~   TH $x/$$x   OCaml .~           NEEDED  -> realize ($, ruled)
                             Scala ${} Rust #name  Julia $x    Elixir unquote
2 splice-into-sequence       Lisp ,@  Clojure ~@  Rust #(..)*  Julia $(xs...)     NEEDED  -> splice (ruled)
                             Elixir unquote_splicing
3 identifier / name passing  TH 'x    Rust $x:ident   Nim untyped                 DISSOLVES -> Name is a value;
                                                                                 field names banned
4 TYPE passing               TH ''T   Scala Type[T]  Zig comptime T:type          DISSOLVES -> type is a value
                             Nim typedesc   Julia (types are values)             -> realize (see section 5)
5 name synthesis / gensym    Lisp gensym  Clojure foo#  TH newName                MOSTLY DISSOLVES -> derived
                             Rust format_ident!   Racket generate-temporary      names automatic; fresh-binder
                                                                                 residue = the flagged 4th open
6 nested levels / staging    Lisp ``,,  OCaml/Scala/MetaML multi-stage            DISSOLVES -> single stage;
                                                                                 recursion is realize-of-a-call
7 hygiene control            Scheme datum->syntax  Julia esc  Elixir var!         DISSOLVES -> no lexical scope
                             Rust Span::mixed_site   Clojure ns-qualify           to capture on typed values
8 typed quote / typed splice TH [||..||]/$$   OCaml 'a code   Scala Expr[T]        AMBIENT -> the whole system
                                                                                 is typed; free, not an escape
```

Arrows read: `NEEDED` = a genuine primitive Nomos must carry; `DISSOLVES` = the typed-value setting
removes the need, with the mechanism it collapses into named; `AMBIENT` = present as a property of
the system, not as an escape to add.

## 4. Why the value systems need so few escapes — the load-bearing observation

Notice the pattern in §2.2: **MetaOCaml has one escape (`.~`). Scala 3 has one expression escape
(`${ }`) and passes types as plain givens. Zig has zero escapes.** As a macro system moves from
tokens toward *typed values*, escape kinds fall away, and they fall away in a specific order — first
hygiene (Kind 7), then name synthesis and name passing (Kinds 3, 5), then type passing (Kind 4),
leaving only value unquote and, where sequences are built structurally, splice.

The reason is uniform: **an escape kind exists to reconcile a kind of syntactic material that the
host language cannot otherwise carry as an ordinary value.** Names need hygiene because names carry
implicit scope. Types need `''T` because in a token AST a type sits in a different namespace than a
value. When *everything* — values, types, names — is already a first-class typed value, there is
one reconciliation operation (put this value in that hole) and its type-checked correctness is the
type system's job, not the escape's. Nomos is built on exactly that footing.

Splice (Kind 2) survives this collapse only because sequence-flattening is a *shape* operation, not
a name operation — MetaOCaml elides it by using list-valued code, but Nomos's logos results are
literal vectors where flatten-vs-nest is a real distinction, so Nomos keeps it as the model already
ruled.

## 5. Direct answer — "what if we pass a type directly to another macro?"

In the systems where types are values — **Zig** (`comptime T: type`), **Julia** (types are ordinary
values), and **Scala 3** (a type rides as a `given Type[T]` alongside expression arguments) —
passing a type to another macro is **just passing a value**, with no distinct type-escape; only
Template Haskell needs a special sigil (**`''T`**) because there a type is a separate quoted
namespace, and MetaOCaml cannot pass a type as staged data at all (types live in the `'a` of
`'a code`, checked at the meta level). Nomos is squarely in the value-is-a-type camp: a Nomos type
is an encoded-form value carrying an encoded identity, so passing a `Type` into another macro is
**the ordinary `realize` you already ruled** — the `Type` meta-value flows exactly like a `Name`,
a `Fields`, or any other input, needing no new escape kind. The one thing to keep straight is a
*distinction the type system already tracks*: passing the type *identity* (the `Type` value itself,
to be placed as a type reference) versus asking the callee to *compute over* that type (reflect its
fields, derive a name) — both are value operations here, differing only in what the callee does with
the value, not in how it is escaped.

## 6. Recommended minimal escape-kind set for typed-data Nomos

**[recommendation — awaiting the psyche's ruling.]** The survey converges hard on the core already
in `nomos-macro-model-v1`, and it argues *against* growing it. Recommended set, smallest that closes
the space:

**Seat exactly two escape primitives, both on the `$` base sigil:**

1. **realize (value unquote, Kind 1)** — insert one typed value at a hole. This single primitive
   **also covers type passing (Kind 4)**: a `Type` is a value, so no separate type-escape is
   warranted. Reasoning: it is the irreducible value-crossing operation shared by every system
   surveyed, and the typed setting gives it Kind 8's safety for free.

2. **splice (sequence unquote, Kind 2)** — flatten a typed sequence into an enclosing vector.
   Reasoning: logos results are vectors; flatten-vs-nest is a genuine shape distinction that
   realize cannot express, and it does not dissolve.

**Keep recursive macro invocation as a distinct *surface form*, not a third primitive** — it is
realize-of-a-macro-application, as already ruled; a call reads as a call, but it adds no new escape
semantics and, per Kind 6, introduces no quoting level.

**Do not seat these — the typed setting dissolves them, and seating them would re-introduce the
name-world problems the typed footing was meant to escape:**

- **Type passing (Kind 4)** — collapses into realize; a distinct type-escape would be dead weight.
- **Name passing (Kind 3)** and **hygiene control (Kind 7)** — no free names, no lexical scope to
  capture; there is nothing for these to act on.
- **Nested levels / staging (Kind 6)** — single-stage expansion; revisit only if the psyche wants
  macros that emit macro definitions (a real second stage), which would be a deliberate, separate
  design.

**Leave the one honest open exactly where v1 left it — name synthesis (Kind 5).** Recommendation:
**do not pre-emptively seat a general synthesize-name escape.** Deriving output identifiers is
already automatic (deterministic derived-name rule + field-name ban), so the only conceivable
residue is minting a genuinely fresh binder — and in a single-stage typed-value transform with no
injected user-scope temporaries, it is not yet demonstrated that this case ever occurs. If a real
instance appears, it wants a **narrow, named "derive/mint identifier from a typed datum" operation**
scoped to that case, not a general gensym escape. Until such an instance is shown, the two-primitive
core is complete.

**Net recommendation, one line:** `$` realize + `$` splice + recursive-invocation surface form is
the closed set; every other escape kind in the world's most elaborate macro systems either dissolves
into value passing or has no substrate in a typed-data macro. This is the agent reading; the escape
count and the fate of name synthesis are the psyche's to rule.
