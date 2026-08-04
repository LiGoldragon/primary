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
