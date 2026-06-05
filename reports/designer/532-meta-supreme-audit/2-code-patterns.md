---
title: 532/2 — Code patterns, bad AND good — the schema-derived stack, live
role: designer
variant: Psyche
date: 2026-06-05
session: 532 meta-supreme deep audit — subagent report 2 of 5
topics: [audit, code-patterns, code-smell, good-patterns, nota-next, schema-next, schema-rust-next, triad-runtime, spirit, methods-on-nouns, tokens, pattern-of-patterns]
description: |
  The code-pattern dimension of the meta-supreme audit. Confirms report
  529's smells live (file:line, re-measured — most grew), adds new ones
  (the lone free function, the cross-plane From matrix, the
  string-emitted error enum, the duplicated macro SUBSYSTEM not just a
  method), and names the genuinely excellent patterns (the derive crate
  as gold standard, triad-runtime/frame.rs as the discipline made flesh,
  zero ZST namespaces, uniform typed Error enums). The decisive finding:
  the migration reports 530/531 PRESCRIBED is already half-live — the
  declaration emitter is now ToTokens-over-quote!, the runtime emitter is
  still the string god-struct, and both halves sit in one file. The
  pattern-of-patterns: every smell is an UN-NAMED AXIS enumerated by
  hand; every strength is a NAMED NOUN that owns its verb.
---

# 532/2 — Code patterns: bad AND good, across the schema-derived stack

This is the code-pattern dimension. Five crates swept live —
`nota-next`, `schema-next`, `schema-rust-next`, `triad-runtime`,
`spirit` — for both the smells (extending the operator audit, report
529) and the strengths. Everything below is grounded at file:line and
was re-measured against the current working trees, not the numbers
report 529 recorded three days ago. Most smells **grew** in the
interval — and, decisively, the fix reports 530/531 prescribed is
**already half-live in the code**.

## The honest verdict first

This is genuinely good code. Across five crates the methods-on-nouns
discipline holds almost perfectly: **zero ZST namespaces, zero
module-level free functions in four of five crates, uniform typed
`Error` enums per crate, typed newtype envelopes everywhere.** The
smells are real but they **concentrate in exactly two places** —
schema-next's resolution/parse layer and schema-rust-next's *runtime*
emitter — and those are precisely the two places the Asschema-removal
migration is rewriting. This is "fix-as-you-migrate," not "schedule a
cleanup." The strengths are not the absence of smells; they are
positive, teachable structures.

## Part 1 — the bad patterns (529 confirmed live + grown + new)

### 1.1 The pair-parse idiom, copy-pasted — CONFIRMED, byte-identical

Report 529's headline smell. The "open a brace, require an even
object count, chunk into pairs" routine is **byte-for-byte identical**
across `schema-next/src/source.rs`. The pair-parse + even-count guard
appears verbatim at `source.rs:232-247`, `:345-360`, `:496-…`
(`ExpectedEvenMapEntries` at lines 235, 348, 499), and the matching
`to_schema_text` empty-then-brace-join idiom is duplicated at the same
three sites (`return "{}".to_owned();` ×3). `from_block` itself is
defined **12 times** in this one file (lines 232, 309, 345, 422, 496,
671, 712, 813, 987, 1042, 1333…) and `from_delimited`/`chunks_exact(2)`
recur throughout. The *concept* "validated pair-map parse of a braced
block" exists a dozen times and is **named zero times.** The missing
layer is one method — `Block::parse_pairs_map(delimiter, context, f)`
— and the 12 copies collapse to 12 one-liners. **Live, unchanged.**

### 1.2 The SEMA resolvers — CONFIRMED, now EIGHT not four

529 found "4 identical SEMA resolvers ×2." The live count is **8
near-identical methods**: a 2 (write/read) × 2 (input/output) matrix
written out by hand *twice* — once for the type-name
(`schema-rust-next/src/lib.rs:3353-3411`:
`sema_write_input_type_name`, `sema_write_output_type_name`,
`sema_read_input_type_name`, `sema_read_output_type_name`) and once
for the root (`lib.rs:3413-3452`: the matching `..._root` quadruple).
Every method differs from its siblings only in **two string literals**
(`"WriteInput"` vs `"ReadInput"` vs `"WriteOutput"`…). The plane axis
— {write, read} × {input, output} — is a real concept enumerated by
hand across 8 methods. Missing layer: a `Plane`/`PlaneRole` value that
owns the axis; the 8 methods become one parameterised lookup.

### 1.3 The plane-type predicates — CONFIRMED, magic strings everywhere

529's "plane-type predicates scattered across 5+ functions" is live and
worse: the plane-type names are **bare string literals** scattered
through the emitter — `"NexusWork"`, `"WriteInput"`, `"ReadInput"`,
`"SemaWriteInput"`, `"SemaReadInput"` re-listed in `match` arms and
`has_type(declarations, "NexusWork")` calls across
`lib.rs:2307-2440`, `:2664-2765`, and more. There is no `PlaneType`
enum; the set of plane types and their relationships is smeared as
string-keyed lookups. A new plane type touches five-plus functions.
Missing layer: a `PlaneType` enum that owns the list. **Live.**

### 1.4 The RustWriter god-struct — CONFIRMED, GREW from 52 to 104

529 measured 52 `emit_*` methods. The live `impl RustWriter` block
(`schema-rust-next/src/lib.rs:1475-3853`) now holds **104 methods**
across ~2378 lines in a single impl. It grew during the in-flight
migration — adding `from_source`-side machinery onto the god-struct
rather than onto the nouns, exactly the failure mode 529 §"what to
check" warned about. The output is built by **567 `self.line(...)`
string-push calls** vs only 91 `format!`s — a hand-rolled code
generator emitting Rust *source text* line by line. The Rust-model
nouns it serves (`RustStruct` :689, `RustEnum` :743, `RustField`
:718, `RustEnumVariant` :772) carry data and accessors but the heavy
verbs live on the writer. **Live — but half-dissolved; see Part 3.**

### 1.5 The duplicated dispatch — CONFIRMED, and it's a whole SUBSYSTEM

529 flagged "two near-identical dispatch methods" in `nota-next`. Live,
it is larger than that: TWO parallel macro layers each carry a
near-identical `dispatch` AND a near-identical `validate_no_silent_
conflicts` AND a `silently_shadows`. `dispatch` at `macros.rs:469-491`
(over `self.variants()`, erroring `StructuralVariantError`) mirrors
`dispatch` at `macros.rs:1010-1034` (over `self.nodes`, erroring
`MacroError`) — same "accumulate tried/expected, filter by position,
return first match, else NoMatch" shape, differing only in the
collection and the error type. `validate_no_silent_conflicts` is
duplicated at `:493` and `:1036`; `silently_shadows` at `:352` and
`:901`. This is not one duplicated method — it is a **duplicated
match-dispatch SUBSYSTEM**, the footprint of two macro layers
(structural-variant and macro-node) that have not been unified onto one
generic dispatch over (position, candidates, error). Likely a
transitional state mid-migration; worth confirming the operator intends
to collapse them.

### 1.6 Type strings by concatenation — CONFIRMED

529's "type strings built by concatenation, no `TypeExpression` AST" is
live at `lib.rs:3816` (`format!("Vec<{}>", self.rust_type(inner))`)
and `:3822` (`format!("Option<{}>", ...)`). Types are assembled as
strings rather than as a typed tree. 531 already named the resolution:
this AST is `proc-macro2::TokenStream` — and the migration is adopting
exactly that (Part 3).

### 1.7 NEW — the lone free function `opening_starts_declaration`

A genuine methods-on-nouns violation report 529 didn't list:
`nota-next/src/parser.rs:972`, `fn opening_starts_declaration(name:
&str, opening: char) -> bool` — a module-level free function, a pure
predicate, outside `#[cfg(test)]`/`main`. It is the **only** non-proc-
macro free function in the entire five-crate sweep. The irony is sharp:
the very next item in the same file is a `trait AtBindingOpening` with
`impl … for Delimiter` (parser.rs:986+) — the author knows the
pattern and applied it one line below. The predicate wants the same
home: a method on a `DeclarationOpening` value or on the opening
`char`/`Delimiter` newtype it already reasons about. Low-stakes, tiny,
tested — but it is the one true crack in an otherwise perfect record.

### 1.8 NEW — the cross-plane `From` matrix in spirit/plane.rs

`spirit/src/plane.rs` hand-writes **six** `From<X::OriginRoute> for
Y::OriginRoute` impls — every direction of signal↔nexus↔sema — and
all six bodies are the byte-identical `Self(origin_route.0)`. It is a
3×3 conversion matrix (minus the diagonal) enumerated by hand. This is
the **same shape** as the 8 SEMA resolvers (1.2): an axis — here, the
three planes — written out by hand instead of named. The cleaner shape
is one wrapper newtype carrying the route value with `From` derived/
generic over the plane marker, or a macro over the plane set. Not
urgent (the impls are trivially correct), but it is the smell's
signature appearing in a *third* crate, which is what makes it
pattern-of-patterns evidence rather than a one-off.

### 1.9 NEW — the error enum emitted as string lines

`schema-rust-next/src/lib.rs:1942` literally does `self.line("pub enum
SignalFrameError {")` — the codegen **hand-writes an entire Rust error
enum as string text.** Downstream this produces `SignalFrameError`
duplicated across three generated files in spirit (`schema/sema.rs:315`,
`schema/signal.rs:798`, `schema/nexus.rs:404`). The string-emission of
a *typed structure* is the god-struct smell at its purest: a type that
should be a `ToTokens` impl is instead a sequence of `push(line)`
calls. The fix is the same as everything else in Part 3.

### 1.10 The unwrap/expect picture — mostly clean, named the exceptions

Density is low and the pattern is disciplined, not a smell:
`schema-rust-next` has **1**, `triad-runtime` **2**, `nota-next` **7**,
`spirit` **17**, `schema-next` **21**. The two larger counts are NOT
raw `.unwrap()`s: spirit's 17 are all `Mutex::lock().expect("…")` in
`engine.rs` (the standard poisoned-lock convention) and schema-next's
21 are `.expect("… checked")` with the invariant documented in the
message right after a length/shape check (`source.rs:45`,
`raw.rs:246`, `engine.rs:372`…). This is the *good* form of `expect` —
an asserted invariant with a stated reason — not the smell. Flagging
for completeness, not as debt.

## Part 2 — the good patterns (genuinely excellent)

### 2.1 The derive crate is the GOLD STANDARD the emitter should copy

`nota-next/derive/src/lib.rs` is the model of everything the runtime
emitter is not. (a) It uses **`quote!` over `proc-macro2` tokens, never
strings.** (b) Every per-variant concern is its **own tiny noun with
one method**: `UnitVariantDecode` (:490, `.arm()`), `PayloadVariant
Decode` (:510, `.arm()`), `VariantEncode` (:564, `.body_arm()`),
`GenericsWithCodecBound` (:expand_decode) — many small local impls, no
central special-casing. (c) The proc-macro entry points
(`derive_nota_decode` :12, `derive_nota_encode` :18,
`derive_structural_macro_node` :24) are the *only* legitimate free
functions in the crate and each immediately delegates to a method on a
real noun: `CodecDerive::new(input).expand_decode()`,
`StructuralDerive::new(input).expand()`. (d) The structural decode
expands to `#(#unit_variants)*` / `#(#payload_variants)*` repetition
**over the variant tree** (`lib.rs:388-457`) — the structure-tree-
fills-the-template idiom. This crate is the live proof of report 531's
core claim: the stack already knows how to do token-based codegen
right; the runtime emitter just hasn't been converted yet.

### 2.2 triad-runtime/frame.rs — the discipline made flesh

`triad-runtime/src/frame.rs` is exemplary, the canonical demonstration
of the workspace's own rules: every value is a **typed newtype**
(`MaximumFrameLength`, `FrameBody`, `LengthPrefixedCodec`), there is a
**typed `Error` enum** with `thiserror` and `#[from]`
(`FrameError`, :23), every verb is a **method on its owning noun**
(`encode_body`, `read_body`, `validate_length` on `LengthPrefixedCodec`;
`accepts` on `MaximumFrameLength`), constructors are `const fn`, and
there is **zero** free function, zero ZST, zero raw unwrap. A reader
learning the discipline should be pointed here first. The whole
`triad-runtime` crate holds this bar: zero free functions, typed errors
per module (`ArgumentError`, `ListenerError`, `TraceError`, the
generic `SingleListenerDaemonError<StartError, StopError>`).

### 2.3 The structural macro node + shadow-detection — real correctness

`silently_shadows` (`nota-next/src/macros.rs:352`, :901) is a method-on-
noun that recursively checks whether one macro pattern would *silently
swallow* inputs intended for another, wired into
`validate_no_silent_conflicts` so an ambiguous grammar is caught at
**construction time**, not at a confusing runtime mis-parse. The
`PositionPredicate` enum (:90) with `describe()` (:101) makes "where in
the block does this match" a typed, self-describing value rather than an
index. This is genuine compiler-grade design: ambiguity is a typed
error, not a latent bug. (The duplication in 1.5 is the *layering* of
two such subsystems, not a flaw in the design itself.)

### 2.4 The token-lowering wrapper-with-context — ALREADY PRESENT

The exact end-state pattern report 531 prescribed (the `InContext<T>`
wrapper that carries a `RenderContext` so `ToTokens`' fixed signature
can still receive context) is **already live** in schema-rust-next:
`RustStructTokens<'structure,'context>` (`lib.rs:1108`) holds
`structure`, `visibility`, and `&RustRenderContext`, and its `impl
ToTokens` (:1128) renders via `quote!` while threading the context. The
same wrapper exists for every declaration noun: `RustFieldTokens`
(:1147), `RustEnumTokens` (:1222), `RustEnumVariantTokens` (:1253),
`RustDeclarationTokens` (:1019), `RustAliasTokens` (:1062),
`RustNewtypeTokens` (:1094), `RustTypeReferenceTokens` (:977),
`RustIdentifier` (:961). This is the wrapper-plus-context idiom 531
called the correct shape — implemented, not just proposed.

### 2.5 Typed plane envelopes and uniform per-crate errors

Every plane's value types are newtype-wrapped (`OriginRoute`,
`SemaObjectName`, `MessageIdentifier`) and the cross-plane projections
are `From` impls on the typed values (the *good* part of plane.rs —
the `ActorStartFailure`/`ActorStopFailure` `From` impls at plane.rs:39+
are exhaustive `match`es that the compiler checks, not string lookups).
Typed `Error` enums are uniform across the whole stack
(`NotaDecodeError`, `MacroError`, `SchemaError`, `BuildError`,
`FrameError`, `StoreError`, `TransportError`, `DaemonError`…) — the
typed-per-crate-`Error` discipline is held without exception.

## Part 3 — the decisive finding: the prescribed fix is HALF-LIVE

This is the most important code-pattern observation in the audit, and
it revises the verdict of 529/530/531. **schema-rust-next is in a
clean, observable half-migrated state, and both halves sit in the same
file.**

- The **declaration** emitter — structs, enums, fields, type
  references, aliases, newtypes, identifiers — has **already been
  converted** to the `ToTokens`-over-`quote!`, wrapper-with-context
  shape that reports 530 ("render on the nouns") and 531 ("tokens not
  strings") prescribed. That is the family of `*Tokens` wrappers at
  `lib.rs:961-1253` (§2.4). The god-struct's *declaration* verbs have
  moved onto small per-noun token-wrappers. The fix is not theoretical;
  it is shipping.
- The **runtime/plane** emitter — the `NexusWork`→`NexusAction`
  projections, the 8 SEMA resolvers (1.2), the plane-type string
  predicates (1.3), the string-emitted error enum (1.9) — is **still
  the 104-method string god-struct** (1.4), `self.line(...)` line by
  line.

So the smells report 529 found are not "untouched debt." They are the
**not-yet-migrated half** of a migration whose first half is already
landed and correct. The declaration slice is the warm-up 531 predicted
("the declarations slice the operator started with is the clean warm-
up"); the runtime/plane slice is where the context concentrates and
where the remaining god-struct lives. The single highest-leverage code
recommendation in this whole audit: **finish converting the runtime
emitter to the same `*Tokens` wrapper shape the declaration emitter
already uses** — same crate, same proven idiom, same file. The SEMA
resolvers, plane predicates, type-concat, and string-emitted error
enum all dissolve into the pattern already standing five hundred lines
above them.

## The code pattern-of-patterns

**Every smell is an un-named axis enumerated by hand.** The pair-parse
×12 is the "validated pair-map" concept un-named. The 8 SEMA resolvers
are the {write,read}×{input,output} axis un-named. The plane-type magic
strings are the plane-type set un-named. The 6 cross-plane `From`s are
the three-plane axis un-named. The duplicated dispatch is the
"position-filtered match-dispatch" concept un-named. The 104-method
god-struct and the string-emitted error enum are the "a structure
renders itself" concept un-named. In every case the duplication and the
deep `match` are the **visible footprint of a concept that wanted to be
a noun and was inlined as an axis-by-hand instead.** This is report
529's hypothesis — repetition is the shadow of a missing layer — and it
holds across all five crates, not just the two the operator audited.

**Every strength is a named noun that owns its verb.** `FrameBody`
owns its bytes and its length check. `UnitVariantDecode` owns its one
arm. `silently_shadows` lives on the pattern that can shadow.
`RustStructTokens` owns its own `quote!`. `MaximumFrameLength` owns
`accepts`. The good code is good for *one* reason repeated everywhere:
the verb was given to the noun that owns the data, and when an axis
appeared (planes, directions, variants) it was made a **type** the
compiler enumerates, not a sequence of hand-written cases. The bad code
and the good code are the **same axis** — un-named vs named. The fix is
never "write less code"; it is "name the noun, and the duplication
collapses into it." The codebase already proves both directions in a
single file (schema-rust-next/lib.rs): the named half is small and
token-based; the un-named half is the 104-method string writer.

## Lineage

Extends report 529 (the operator audit — all six headline smells
re-confirmed live, most grown, four new ones added), 530 (render-on-
nouns — now observed partly implemented), 531 (tokens-not-strings — the
`*Tokens` wrappers are the live realisation; the wrapper-with-context
caveat is confirmed in `RustStructTokens`). Read-only; nothing changed;
no maintenance executed. Proposed code maintenance is *advisory to the
operator lane* (this is a designer reading of operator-owned code) and
is not a content/intent removal — so it carries no tombstone; the only
actionable proposal is "finish the runtime-emitter migration onto the
existing wrapper shape," which belongs to the operator's in-flight
Asschema-removal slice plan, not to this audit's executor.
