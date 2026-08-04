# LLM Token-Optimization Rulings — 2026-08-04

Session: syntax-revision discussion driven by the psyche's aim of optimizing
the Protos language family for LLM token cost. Evidence base: tiktoken
cl100k_base and o200k_base measurements plus Llama 3 and the public Claude 1/2
tokenizer (Claude 3+ tokenizer is proprietary; verification through the
count-tokens API is in progress).

## Ruling: the dot-prefix stays — `Name.{` confirmed

Agent text answered: "`Name.{`, `Name{`, and `Name {` all tokenize to exactly
2 tokens on every modern tokenizer tested, because BPE merges make `.{` and
` {` single tokens. … the choice between dot, space, or nothing is yours to
make on cognition grounds alone."

Psyche, verbatim: "Then it's Name.{ which is much better visually"

The universal name prefix ruling of 2026-08-03
(`universalNamePrefixTransformerPipe-2026-08-03.md`) stands unchanged. The
token doubt that triggered this revision is dissolved: the application dot is
free. Constraint that must hold: the operator never separates from its
delimiter — `Name. {` and `Name .{` cost one extra token per site and are not
legal forms.

## Given restored to record: projection profiles

Agent text answered: proposal to "define projection profiles — a canonical
token-lean projection (single-line records) that the engine emits for agent
consumption, and the pretty-printed projection for human editing. Since
round-trip is encoded-value equivalence, both are already legal text."

Psyche, verbatim: "That was already a given. I always knew this, and my
mentionning it is now lost to you. Worth making a note somewhere now."

Recorded as a standing given, previously stated by the psyche and lost from
agent context: the engine serves multiple textual projections of the same
encoded value — a token-lean canonical projection (single-line records) for
agent consumption, and a pretty-printed projection for human editing. Both are
legal because round-trip correctness is encoded-value equivalence
(`encodedMeaningRoundTrip-2026-08-02.md`). Measured stake: block layout costs
+33% (payload on one indented line) to +102% (field per line) over
single-line records, because newline-plus-indent never merges while a closing
delimiter fuses with a newline for free.

## Ruling: guillemets and curly quotes join the delimiter alphabet

Agent text answered: "«»/“” are 1-token and genuinely paired in training
data" (offered as the expansion alphabet, in place of exotic asymmetric pairs
such as `$…%` and `¿…?`, which measured token-neutral with no paired prior).

Psyche, verbatim: "I love it! We should definitely use those"

`«` `»` (U+00AB/U+00BB) and `“` `”` (U+201C/U+201D) are adopted as approved
delimiter pairs. Their syntactic slot is not yet assigned; candidates include
the trait-bound struct body currently proposed as `{| |}`, the trait-parameter
marking question, and text carriers. Slot assignment is an open question for
the psyche.

## Correction accepted: angle brackets do not collide under structural parsing

Agent text answered: "[bare `<` `>`] collide with less-than/greater-than and
with embedding in HTML/XML hosts."

Psyche, verbatim: "That isnt true, unless youre saying structural parsing
cannot work"

The collision claim is withdrawn at the parser level: under positional
structural parsing the expected type at every position decides content versus
delimiter, so `<` `>` are parseable data delimiters. The residual,
non-blocking concern is embedding-safety in markup hosts — the analog of the
quotation-safety principle that keeps double quotes out of Dotos. Token cost
of `<>` versus `{| |}` versus `«»` is under measurement; no adoption ruling
yet.

## Context note: the familiarity tax is transitional

Agent text answered: "a human can be trained on Protos; a frozen model
cannot — it has only the in-context legend."

Psyche, verbatim: "Thankfully, we will train new models. The heavens havent
stopped turning"

Design weighting: long-run token-optimality outranks frozen-model
familiarity, because the psyche intends models trained on Protos. A candidate
intent-log line was proposed to the psyche separately.

## Measured facts seated with these rulings

- Positional no-field-name records: −56% tokens versus compact JSON (56 vs
  128 on a 10-record payload; TOON 80, CSV 69). The wrapper alphabet moves
  under 2%; field-name elimination is where the budget is won.
- The data hot path is already optimal: repeated records in a vector are bare
  `{…}` with no name prefix, and the opener fuses with the first atom.
- Transformer sigil: `|` and `!` are identical in cost; a bare space would
  save exactly 1 token per call but erase the marker that keeps the dot-world
  provably pure data. `|` stands on both the visual ruling and the ledger.
- A 12-char hex hash costs 9 tokens — more than an entire 4-field record.
  Hashes stay out of textual projections; three-layer naming already so
  provides.

## Ruling: curly quotes become the string carrier (supersedes in part)

Agent text answered: round-2 measurement — `“ ”` (U+201C/U+201D) is the
stable typographic pair (+2.4% in both vocabs, `.“` merges free), while
`« »` is tokenizer-unstable (+2.4% in o200k but +13.5% in cl100k) and
recommended for demotion.

Psyche, verbatim: "if “” is different from "", then we should use it for
strings instead of () and (||), and make it common-indentation safe, so it
can parse indented blocks properly. but Ill need an easy way to type it (as
well as « » - no idea currently, im copy pasting yours just to mention it),
but dont bother yourself too much with this; a beads will suffice and ill
solve with with another agent."

Condition verified: `“` `”` are distinct codepoints from ASCII `"` (U+0022),
so the quotation-safety principle survives intact — Dotos still contains no
ASCII double quote and remains embedding-safe in every double-quote host.

Ruled: `“ ”` replaces `( )` multi-word text and `(| |)` pipe-text as the
string carrier, and inherits pipe-text's common-indentation semantics
(dedent by the minimal common indent of the block's lines). Non-string uses
of `( )` (such as Map-headed application) are not addressed by this ruling.
Typing ergonomics for `“ ”` and `« »` are tracked as a bead; the psyche will
solve input methods with another agent. This supersedes the guillemet
adoption above insofar as `« »` now carries no assigned slot and is
disfavored for wire use by the tokenizer-variance evidence.

## Ruling: piped delimiters dropped

Agent text answered: round-2 measurement — compound pipes lose the
dot-cluster merge (`Name.{|` costs +2 tokens/record), fragment under
nesting, and `[| |]` is the worst pair measured at +26%.

Psyche, verbatim: "so we should drop the piped delimiters."

Ruled: `(| |)`, `[| |]`, and the proposed `{| |}` leave the grammar. String
carriage moves to `“ ”` per the ruling above.

## Leaning recorded: no complex struct/enum form; trait delimiter gives optional generics

Psyche, verbatim: "I dont even think we need a complex struct/enum, if we
use a special delimiter for traits(generics), we get optional generics using
unambiguous parsing trick. im debatting different delimiters in my head
right now."

Candidate spellings under debate (psyche's own list):

```ethos
Vector.<Sortable>
Vector<Sortable> ;; cognitive reuse of rust, right?
Vector.«Sortable» ;; inefficient apparently
Vector«Sortable»
```

Also floated, explicitly with question marks: reserving `.< >` for a
dot-prefixed slot such as a transformer payload — "Observer.Stream.< ... >
??" — pending measurement of the `X.Y.<open>` chain patterns. No ruling
seated; the trait/generics delimiter remains open.

## Ruling: generics are bare Rust-style `< >`; transformer payload is `.( )`

Agent text answered: round-3 measurement — the dotted chain
`Observer.Stream.<…>` costs 1 token per call less than the ruled
`Observer|Stream.{…}` because `|` fuses with nothing while `.Stream` and
every dotted opener (`.<` `.{` `.(` `.[`) fuse to single tokens; bare
`Vector<Sortable>` equals `Vector.<Sortable>` flat and saves 1 token per
nested application (`Result<Vector<Sortable> Error>` = 7 vs 8); decision
list posed the transformer form and the generics delimiter as open rulings.

Psyche, verbatim: "we could use .() for transformers, and <> for generics"

Psyche, verbatim: "and I want the Result<Vector<Sortable> Error> syntax for
generics, since its more token efficient than using a dot, and recycles rust
cognition"

Seated:

- Generic/trait parameters are bare angle pairs, Rust-shaped:
  `Vector<Sortable>`, `Result<Vector<Sortable> Error>`. Angles are exclusive
  to generics.
- Transformer applications return to the dotted chain with a parenthesis
  payload: `Name.Transformer.(…)`. The `.(` opener is the structural
  transformer marker; it is token-equal to every other dotted opener, so the
  choice costs nothing and removes the bare-`<>`-versus-dotted-`<>`
  proximity concern entirely. `( )` is free for this duty because `“ ”` now
  carries strings.

Recorded as open pending psyche confirmation: whether `|` retires from the
grammar entirely; whether sectioned entries spell `Observer.(…)` with the
section supplying the operator, which would resolve the 2026-08-03 open
question; whether `Map.(alpha.1 beta.2)` is reinterpreted as an ordinary
transformer-style application under the new `.( )` meaning.

## Architecture statement: transformer schema mirroring down the daemon chain

Psyche, verbatim: "and ethos will need to know the (input) schema of the
nomos transformers, so we are looking at another type-mirroring like with
logos/nomos. Essentially, each daemon needs some types to store the objects
belonging to the next deamon down the chain."

Recorded: Ethos must carry the input schemas of Nomos transformers — a
type-mirroring layer parallel to the existing Logos/Nomos mirroring. The
implied general law: each daemon holds types that store the objects
belonging to the next daemon down the chain. This concerns typing, not
parsing: the 2026-08-03 invariant that the Ethos parser needs no Nomos
transformer table survives, because `.( )` marks transformer applications
structurally; the schemas are needed to type the payloads.

## Ruling: string escapes — balanced nesting plus backslash

Agent text answered: options for a literal `”` inside `“…”` — (a) backslash
escape, (b) balanced-pair nesting, (c) both, with a lean toward (c).

Psyche, verbatim: "sure"

Seated: inside `“ ”`, balanced `“ ”` pairs nest without escapes (the two
codepoints are distinct, so the parser counts depth for free). An unbalanced
literal `”` or `“` is written `\”` or `\“`; a literal backslash is `\\`. The
symmetric `\“` spelling and `\\` carry over from pipe-text's escape rule by
agent extension; flagged to the psyche in chat.

## Ruling: encoded forms use strict purpose-designed types

Psyche, verbatim: "Also, I want the encoded form to use strict types
designed specifically for each encoded form's needs. no Vec&lt;Fields&gt; and such
dirty types. former code isnt binding, we are in a deep redesign phase."

Seated: every encoded form is carried by types designed for that exact
form's needs; generic container shapes (`Vec<Fields>` and similar) are
barred from encoded surfaces. Existing codec code is not binding precedent —
the train is in a deep redesign phase. Tracked as a bead.

## Note: intent line approved

The psyche approved the intent line on training models on Protos ("sure")
and asked what the intent log is, distinct from Spirit; capture proceeds via
the intent-log mechanism with the approved wording.

## Correction: no Spirit capture was approved — the line is matter

Psyche, verbatim: "I never approved a spirit capture. I even explicitely
said no." and "its not called intent anymore, but if you meant the line for
"intent log"; that is matter, not spirit" and "no, not anymore, and like I
said, your proposal doesnt even come close to qualifying"

Supersedes the note above. The psyche's "sure" approved the line as a note,
not a Spirit capture; the agent misread "not spirit" as a question rather
than the correction it was. No Spirit record exists — the guardian rejected
the attempted capture as matter, which the psyche confirms was the right
judgment. The line stands as design-log matter only, in this file. The
intent log is a matter surface, not Spirit, and the concept is no longer
named intent.

## Ruling: the bare pipe retires

Agent text answered: "does `|` retire from the grammar entirely? With
`Name.Transformer.(…)` standalone and `Name.(…)` sectioned, I see no
remaining duty for the bare pipe."

Psyche, verbatim: "obviously. youre demonstrating that LLMs arent really
intelligent yet by asking. One syntax necessarily replaces another"

Seated: `|` leaves the grammar entirely. `Name.Transformer.(…)` standalone
and `Name.(…)` sectioned replace the 2026-08-03 pipe forms.

## Leaning: no stream section; a stream opens with a query, establishment answers

Psyche, verbatim: "I doubt we need a stream section. I did want to bring up
the fact that initiating a stream requires a query, and that its
establishment should give a response. right?"

Live discussion against the vq6.6 stream gate; not yet seated.

## Leaning: StreamInitiation and StreamTermination; Stream is the output object

Agent text answered: "`StreamRequest` is the input query, and `Stream` is
itself the output object. With bare-angle generics seated, the output is
`Stream<Event>` … what remains is the concrete shape of `StreamRequest`
(what a query minimally carries) and whether close is a method on the Stream
object or an input of its own."

Psyche, verbatim: "I might prefer StreamInitiation, which more naturally
opens the door for StreamTermination."

The Stream-as-output-object framing stands: per stream, the authored types
are the initiation payload and the event; the output is `Stream<Event>`.
Naming leaning: `StreamInitiation` for the opening query, paired with
`StreamTermination` — which implies close arrives as its own input type, not
as a method on the Stream object. Initiation shape still open.

## Ruling: one type per transformer; the mirror is shared Ethos source

Agent text answered: a sketch giving transformer applications a single
strict node, `TransformerApplication { name, transformer, payload }`, and
questions on whether the Ethos-side mirror is derived or hand-authored and
how deep it goes.

Psyche, verbatim: "a different type for each transformer; hence my
ethos/nomos overlap mention." and "so not that; it would a type for
StreamInitiation, etc. those will eventually be written in ethos, and
eventually that ethos code will be shared between nomos and ethos,
eliminating the repitition." and "1. we will do some hand written mirror for
now I guess" and "2. yes, full input schema"

Seated: there is no generic transformer-application node in the encoded
form. Each transformer has its own strict application type
(`StreamInitiation`, `StreamTermination`, …), carrying that transformer's
full input schema. For now the Ethos-side mirror of these types is
hand-written; the end state is that the types are authored once in Ethos and
that Ethos source is shared between Nomos and Ethos, eliminating the
repetition.

## Clarification: Sema is the database engine, not a chain daemon

Agent text answered: a question whether Sema sits in the daemon chain as a
mirrored layer.

Psyche, verbatim: "I dont understand. I thought sema is the database engine
that all daemons use. Do you mean the sema (storage) types?"

The mirroring law binds the language daemons (Ethos/Nomos, Nomos/Logos).
Sema is the shared database engine every daemon uses; the sema storage types
a daemon holds are its persistence for objects, including the next daemon's
mirrored objects, not a mirroring layer of their own.

## Ruling: nomos-types shared crate; transformer implementations stay in Nomos

Agent text answered: the shared-crate shape — pure data types (per-
transformer schemas) in one crate consumed by both core-ethos and
core-nomos; the transformer trait Nomos-owned so `impl Transformer for
StreamInitiation` satisfies the orphan rule; the crate as landing spot for
the hand-written mirror and later the Ethos-generated source; a dedicated
`nomos-types` recommended over widening `protos`.

Psyche, verbatim: "we could use a shared repo (nomos-types?) to hold those
so nomos and ethos can share the code? could the trait implementation
(transformer) still live in nomos?" then "ok" (proceeding to the bead
reorientation on this basis).

Seated: per-transformer types live in a shared `nomos-types` repository,
depended on by both core-ethos and core-nomos; the transformer trait and all
transformer implementations remain in Nomos.

## Ruling: current code is not binding; traits are the code ontology

Psyche, verbatim: "I also want to make it cleaar that current code is *not
binding*; redesign anything that should be, and make traits! traits are our
new code ontology, we need to make our way to one hundred percent of impls
living under a trait"

Seated: the deep-redesign license is general — any current code that should
be redesigned is redesigned without deference to what exists. Traits are the
code ontology; the target is one hundred percent of impls living under a
trait.

## Ruling: traits are a soft requirement with per-repo trait-migration files

Agent text answered: whether the 100%-traits target binds hand-written
engine Rust via a dedicated migration pass, or converges as code passes
through the redesign.

Psyche, verbatim: "yes, hand written rust, make it a soft requirement
(encouraged but not blocking; if a trait isnt obvious make a note in a
trait-migration file in each repo which Ill review with claude agent later)"

Seated: the target binds hand-written Rust as a soft requirement —
encouraged, never blocking. Where a trait is not obvious, the implementer
records the case in a trait-migration file in that repo; the psyche reviews
those files later with a Claude agent.

## Ruling: StreamInitiation MVP shape is agent-designed

Agent text answered: whether the psyche rules `StreamInitiation`'s minimal
contents now or leaves the stream work gated on it.

Psyche, verbatim: "you can figure out what the mvp needs, and design
something for now"

Seated: the previously open initiation shape is delegated — agents design
the minimal `StreamInitiation` (and `StreamTermination`) the MVP needs, as a
provisional form subject to later psyche review.

## Ruling: correctNaming translation table in the Rust emission

Agent text answered: the generic-pickup sketch using `Ord` as the trait
name, with the Rust parameter spelled `T`.

Psyche, corrected examples verbatim:

```ethos
Sorted.{Vector<Ordered>}              ;; struct Sorted<Ordered: Ord>(Vec<Ordered>)
Range.{<Ordered> <Ordered>}           ;; struct Range<Ordered: Ord>(Ordered, Ordered)
Status.[Pending Ready.<Numeric>]      ;; enum with a generic variant payload
```

Psyche, verbatim: "I want to create a translation table in logos' rust
textualform emission for correctNaming &lt;-&gt; incorrectNaming, like Ordered and
Ord, so we can have legible ethos/nomos/logos"

Seated: the concept layer uses correct, legible names throughout ethos,
nomos, and logos (`Ordered`, not `Ord`). Rust's abbreviated names are
incorrectNaming, confined to Logos' Rust textual-form emission through a
correctNaming ↔ incorrectNaming translation table (`Ordered` ↔ `Ord`, and
kin). The psyche's examples also show the Rust type-parameter taking the
trait's proper name (`Sorted<Ordered: Ord>`), not a minted `T`.
