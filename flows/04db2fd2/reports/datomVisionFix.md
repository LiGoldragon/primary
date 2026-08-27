# Vision/datom.md — curly-quote strings, guillemet maps

Two superseded positions replaced per the living's rulings of
2026-08-26 (flow ac1e9ec8) and 2026-08-27 (this session).

## Change 1: Syntax section — strings and maps

### Before

Consistency comes first: datom's syntax is fixed before the rest.
Parentheses carry a duty — they are a major symbol of cognition —
and are the default string delimiter, balance-based: interior
balanced pairs are plain content (parentheses inside text are
markup, the seed of the structured string), the string closes at the
final unbalanced closer, and an unbalanced interior parenthesis is
escaped. A string is written bare whenever the bare form can carry
it, and a bare string may carry symbols that are load-bearing
elsewhere — the machinery is made fit for this by the right
abstraction layers. String blocks are opaque: interior delimiters
become content until the block closes. A bare brace block is a
struct; a dot-parenthesis block is a string-carrying variant. The
dotted prefix of a delimited block is part of the block's type; its
official name is Head; a variant always re-emits its Head when
textualized. A map's payload is a square-bracket vector of key.value
entries, since a map is conceptually a list of key/values.

### After

Curly quotes are the default string delimiter. A string is written
bare whenever the bare form can carry it, and a bare string may
carry symbols that are load-bearing elsewhere — the machinery is
made fit for this by the right abstraction layers. String blocks are
opaque: interior delimiters become content until the block closes. A
bare brace block is a struct; a dot-parenthesis block is a
string-carrying variant. The dotted prefix of a delimited block is
part of the block's type; its official name is Head; a variant
always re-emits its Head when textualized. Guillemets delimit a map;
inside, key and value are separated by a space, resolving by
position. A map in a position that expects a map carries no Head; a
Head is always a variant.

### What changed

- "Parentheses are the default string delimiter" replaced with
  "curly quotes are the default string delimiter."
- The balance-based parenthesis content rules moved to the Meaning
  section (they describe the structured string, not ordinary strings).
- "Consistency comes first: datom's syntax is fixed before the rest"
  removed — the psyche asked what "the rest" meant, indicating it
  was unclear; the proposal also dropped it.
- Square-bracket map form replaced with guillemet-delimited map;
  key/value by space, positional; no Head on a map in expected
  position; Head is always a variant.

## Change 2: Meaning section

### Before

The structured super-string type, Meaning, is postponed so a working
syntax lands as soon as possible: parenthesis-delimited and
curly-quote text both land as plain String for now, with the later
Meaning type marked in code. The eventual shape is one string type
with two variants — legacy (curly quotes) and structured
(parentheses, arbitrary depth, a graph of sorts).

### After

Parentheses are reserved for the structured string, Meaning, still
to be designed. Parentheses carry a duty — they are a major symbol
of cognition — and parentheses inside text are already markup, the
seed of the design: balance-based, interior balanced pairs being
content and the string closing at the final unbalanced closer, to
arbitrary depth, a graph of sorts. One string type carries both
forms: plain (curly quotes) and structured (parentheses).

### What changed

- Removed the "postponed so a working syntax lands" framing — task
  language, not vision.
- Removed "legacy (curly quotes)" — curly quotes are the default
  delimiter, not legacy.
- Moved the balance-based parenthesis rules here from Syntax, since
  they describe the Meaning/structured string form.
- Wording closely follows the proposal in
  flows/ac1e9ec8/reports/datomVisionProposal.md (Meaning section),
  which was written after the living's corrections.

## Uncertainty

- The escape rule ("an unbalanced interior parenthesis is escaped")
  appeared in the old Syntax section as part of the parenthesis
  string delimiter rules. The proposal's Meaning section does not
  include it. Since the living's corrections did not address
  escaping and the proposal dropped it, I dropped it from Meaning
  as well. It may need to be re-stated if the structured string
  design retains it.
