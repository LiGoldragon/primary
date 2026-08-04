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
