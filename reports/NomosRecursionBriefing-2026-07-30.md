# Nomos Recursion Briefing — po2.19

This report explains the pending po2.19 decision from the psyche's vision
down to the concrete surface question now on your desk. It covers what
recursion is for, why the current engine cannot do it, what the overnight
train proposed, and why the real choice is narrower than it first appears.

## 1. The Vision This Hangs From

The protos engine is a four-language family over one substrate. Ethos is
the stable authored sugar syntax (renamed from schema). Nomos is the
transformation language. Logos is the assembly-like true representation
("kind of like Shen's kernel lambda," as you put it), projected to Rust
text only at the edge. NOTA is the fourth, the base notation. The shared
textual style itself is named protos.

Of these four, Nomos is the engine's reason to exist. Your own words, from
the triple-language dictation of 2026-07-29:

> the entire reason why we have nomos is so that we can modify the
> transformation using the nomos language. So if the nomos language was
> never implemented, then the entire engine is currently a failure because
> the whole point of creating nomos was to be able to modify.

A transformer (the term you ruled in place of "macro" — "macro is
overloaded ... agents associate it too much with string transformation,
and this is really a type transformation") converts Ethos encoded form
into Logos encoded form. Strictly encoded-form to encoded-form, zero
string manipulation, ever. Your ruling on what "template" means here was
explicit:

> if we talk about template, I think you mean string templates, in which
> case that's not at all what I'm looking for.

A template in this engine is a typed Logos skeleton with typed escape
positions — never a string template.

The long-term direction you stated (explicitly long-term, same dictation):

> we will eventually make Nomos the most load-bearing part that could do
> all of the correctness verification or more than what the Rust compiler
> actually does today.

## 2. Templates and the Escape Algebra

A template is a typed Logos skeleton with typed escape positions. The
landing types at those positions are computed, never handwritten: every
placeholder position is value-or-future-value, derived once from Logos type
declarations. You challenged the hidden assumption before assenting to this
mechanism ("what will write the type with the placeholding future type? I
bet if I hadnt asked, they would be handwritten in rust"), and your
acknowledgment when the computed answer resolved it — "ahh, so every
placeholder is value-or-future-value, so there is no handwritten type per
transformer" — carried delegated-assent grade. That mechanism is now
implemented and witnessed: the 878-line handwritten universe was deleted
and three source-scan tests guard its reintroduction.

The escape algebra was ruled closed at two primitives plus Invoke.
Realize unquotes a bound value into a position. Splice expands a bound
vector into a sequence. Invoke calls another transformer. In the ruled
closure wording: "two primitives plus Invoke for recursion."

In the v1 "base door" textualform these are spelled as plain-NOTA keyword
applications: `Realize.<binding>`, `Splice.<binding>`,
`Invoke.<transformer>`. The dollar-sigil spelling belongs to a
ruled-but-deferred second textualform.

What closure means in practice: the authored vocabulary of holes is
deliberately tiny and fixed. An author writing Nomos sees exactly three
kinds of escape — realize a value, splice a sequence, invoke a
transformer. There is nothing else. This keeps authored Nomos readable and
checkable: any escape in a template body is one of three things, and
the reader knows which from the keyword.

## 3. Why Recursion Is Needed

Recursive transformer invocation was ruled required on 2026-07-13: "We
also need to be able to call more macros recursively." The requirement is
structural. Transformed data is tree-shaped — declarations contain types
containing types; expansions like ScopeOf synthesize whole families of
items from a single authored declaration — so a transformer must be able
to descend into children and build results upward.

Separately, you stated a targeted-insertion requirement during the Entry 5
dictation:

> We can even be talking about a particular spot in a vector where a
> certain item gets inserted.

This is something Splice (whole-vector expansion) cannot express. Splice
expands an entire bound sequence into a vector wholesale; it has no
mechanism for inserting at a specific position within a partially-built
sequence. This targeted-insertion need is a second gap in the current
algebra, distinct from the recursion question but related — both surface
as "things the escape algebra cannot yet do."

## 4. What Exists Today

The 2026-07-30 audit ran the full test suite directly: 258 tests passed,
0 failed, across six crates. The escape enum is exactly three variants —
no Fold code exists anywhere. Template(Logos) is genuinely derived
generically, as the delegated-assent mechanism specified. Typed
pre-evaluation refusal for futures works.

But today's Invoke is only a stub relative to what recursion requires.
This is codex's own honest account from the 2026-07-30 audit: the
current Invoke is a zero-argument, acyclic named call. It requires an
empty target signature, passes no arguments, rejects every invocation
cycle, and has no child selection, no fresh recursive frame, no
structural-decrease proof, and no ordered child-result aggregation. It
can call WireAttributes from WireNewtype (a simple delegation), but it
cannot walk a tree.

## 5. The Overnight Lean and the Open Question

While you slept, under your explicit authorization ("go with your leans,
mark those topic as not-understood by psyche, and produce an addendum for
codex to be able to keep slicing while I sleep"), the train proposed
growing the algebra with two new authored members:

1. **Fold** — tree recursion: fresh typed parameters bound per step, leaf
   termination checkable before evaluation.

2. **A targeted positional-insertion construct** — for the vector-slot
   insertion that Splice cannot express.

These were recorded at the not-understood-by-psyche grade in
`reports/NomosTrainAddendum-2026-07-30.md`, tracked as open question 14
and bead po2.19. The addendum is design only; no code was written for
either construct.

## 6. The po2.19 Cut Codex Proposes

The concrete engineering plan: append boxed new variants without changing
existing tags or archive layout. Everything persisted — capsules,
identities, deployment bytes, engine state — stays byte-identical and
restarts. Old binaries typed-refuse capsules using new escapes (clean
error, not a crash). External exhaustive Rust matches stop compiling until
updated. All version pins advance. Deliberately no migration, fallback,
or compatibility adapter.

Plus: review-marked plain-NOTA V2 syntax for the new escapes,
whole-population structural preflight (checking every transformer's
recursion for termination before any evaluation), postorder typed
reduction (results aggregate bottom-up, not top-down), and immutable
sequence-boundary insertion (the InsertAt mechanism for targeted vector
positions).

## 7. The Exchange That Sharpened It

You (via the manager) asked one question before ruling: why is Invoke
insufficient — why must Fold be a new escape member rather than recursion
through Invoke?

Codex's answer, honest and load-bearing: current Invoke's poverty does
not prove Fold must be a separate authored concept. Recursive Invoke can
work, but needs the complete Fold machinery regardless — typed subject
and arguments, strict-child traversal, leaf/step behavior,
whole-population preflight, postorder result aggregation, separate
termination judgment. Codex's own formulation: "That is Fold algebra
under an Invoke spelling."

The machinery is identical in both options. The essential split is
internal: ordinary acyclic Invoke versus structurally-decreasing
RecursiveInvoke with its own validation. For archive reuse the strongest
design preserves existing Invoke bytes and appends a boxed RecursiveInvoke
internal variant.

The only thing being ruled on is what authors see.

## 8. The Decision Now on Your Desk

**Option A — one authored Invoke concept.** Authors write
`Invoke.<transformer>` for every call; the engine distinguishes internally
between ordinary acyclic calls and structurally-decreasing recursive
calls. The authored algebra stays at the ruled three members (Realize,
Splice, Invoke); recursion machinery becomes implementation matter below
the authored surface.

Cost: one authored word covers two behaviors. Call-sites alone do not show
where recursion happens — `Invoke.ScopeOfExpander` looks exactly like
`Invoke.WireAttributes`. The manager's proposed mitigation: require the
target transformer's declaration to carry its recursive nature and
termination judgment, so declarations are where recursion is honestly
visible while call-sites stay uniform. A ScopeOfExpander transformer
would declare itself as recursive (with its structural-decrease proof)
in its definition header; call-sites would simply say `Invoke`.

**Option B — distinct authored Fold member.** Recursion is a visible
deliberate authored act at every use site. The template body would contain
`Fold.source.PayloadVariants { ... }` instead of `Invoke.ScopeOfExpander`,
making it immediately visible that tree recursion is happening at that
position.

Cost: grows a ruled-closed authored algebra with a fourth member whose
difference from Invoke is arguably engine mechanics rather than authorial
meaning. Fold is a call to a recursive pattern, and Invoke is a call to
a transformer — but in both cases the author is asking the engine to
execute another transformer.

**Prior rulings lean toward A.** The closure was worded "two primitives
plus Invoke for recursion." The 2026-07-13 ruling said recursive
invocation. Fold-as-authored-member was never psyche vision — it is an
overnight lean, explicitly graded not-understood-by-psyche.

Either way, InsertAt proceeds as a new authored member, grounded directly
in your vector-insertion requirement ("a particular spot in a vector where
a certain item gets inserted"). Note that InsertAt is itself a growth of
the closed algebra and should be acknowledged as such in the ruling.

**The manager's recommendation:** Option A at delegated-assent grade, with
the declaration-visibility requirement. Recursion is honestly declared at
the transformer definition, not hidden inside the engine, but call-sites
stay uniform under the single Invoke keyword. The archive-compatibility
contract (existing bytes untouched, old binaries typed-refuse new
constructs, no migration adapter) is mandatory as part of the acceptance
surface.

## 9. Grades Ledger

**Psyche-ruled** (your words, character-exact from the logs):

- Algebra closure: "two primitives plus Invoke for recursion"
- No strings in transformation: "strictly no string manipulation of any
  kind"
- Template is not a string template: "if we talk about template, I think
  you mean string templates, in which case that's not at all what I'm
  looking for"
- Recursion required: "We also need to be able to call more macros
  recursively" (2026-07-13)
- Targeted insertion required: "a particular spot in a vector where a
  certain item gets inserted"
- Reuse is correctness (archive compatibility as a design constraint)
- Tuples forbidden in Rust: restored 2026-07-30 — ad-hoc tuple types and
  multi-field tuple structs are prohibited; newtype (one-field wrapping
  struct) is the sole exception; named-field shapes required

**Delegated assent** (authorized for implementation, not reviewed
conviction):

- Template(X) mechanism — computed value-or-future-value landing types,
  derived grammar. Now implemented; handwritten universe deleted; three
  source-scan tests guard reintroduction.

**Not-understood-by-psyche** (overnight leans, explicitly reversible):

- Fold as an authored escape member
- Targeted positional insertion as a typed construct
- ScopeOf helper identity (implementation structure, not durable
  declarations)
- The other overnight leans (positional-fields law scope, alias law scope,
  syn/quote/prettyplease scope, Capsule removal scope, rkyv-witness scope,
  test-architecture scope)

**Undecided** (this briefing's subject):

- po2.19: whether recursion is a visible authored concept (Fold / Option B)
  or implementation matter under Invoke (Option A)

**Today's related context:** the tuple cleanup (po2.21 through po2.24,
scheduled by codex per `reports/RustTupleViolationsRegister-2026-07-30.md`)
means any new po2.19 variants are built under the restored no-tuples rule:
named-field shapes throughout, newtype exception only.
