# Datom syntax distillation proposal

Proposed self-standing statements to enter `Vision/datom.md`, drawn
from the records gathered by this flow's acquisition. Nothing here
stands until the living approves it statement by statement. Each
statement is numbered for review. The current `Vision/datom.md`
sections are kept; statements below are additions to them, plus two
new sections (Round trip, Open).

## Syntax — additions

- S1. The dot opens a delimiter. A Head is bare text ending in a dot
  written immediately before the delimiter it opens, with no space.
  Everything in a datom text is data; there is no other kind of
  content.
- S2. The shapes are the bare symbol, the parenthesis string, the
  brace block, the bracket block, the legacy curly-quote string, and
  the Head-prefixed form of each delimited shape. Distinct shapes are
  distinct variants of one shape vocabulary; the unquoted form is
  named the bare symbol.
- S3. A colon is plain content in a position expecting a string.
- S4. Guillemets are reserved for the next special syntax need; they
  carry no meaning today.
- S5. The old request form that wraps a verb and its noun in
  parentheses is obsolete. A request is a root-enum variant carrying
  its Head.

## De/serialization — additions

- D1. The parser is the parser: there is one, and nothing implements
  its own parsing logic.
- D2. Meeting a shape yields a type, and that type implements its own
  parsing context; every level of the walk carries its own set of
  shape-determined types. The table from shape to type is data, not
  functions. A large implementation signals a missing logic plane:
  every part is simple, the complexity lives in the whole.

## Round trip — new section

- T1. Text realizes into the real form, and the real form textualizes
  back into text; the two traits are Realize and Textualize, homed in
  the substrate. A textualized variant re-emits its Head, and must be
  read in its right context when printed alone.
- T2. The real form is the typed value where values are born and
  changed; the signal form is the portable projection written once
  and read in place. Code and encoded are not form words.

## Meaning — additions

- M1. The name Meaning is provisional — it smells of a verb — and is
  reopened together with the type.
- M2. The structured string is annotated text: annotations are enums
  used throughout the tree, an emphasis variant being the first
  example. The aim is the most advanced structured meaning system ever
  made.
- M3. A string position expects a string. Either a separate type
  accepts meaning or plain string, or Meaning itself accepts plain
  text as its simplest structured form.

## The interface shape — additions

- I1. Root variants are named in the imperative voice: the slot itself
  already says request, so a variant named Request is redundant.
- I2. A program accepts no argument other than its typed datom input;
  every option lives in that input's shape, never in a flag.

## Repository and migration — additions

- R1. No Dotos files remain; datom text has no legacy sibling on disk.
- R2. Every wire message, configuration input, registry, and assembly
  file is datom text, authored and read by agents and humans alike. A
  program's main begins at its typed datom input; the future harness
  speaks only typed datom messages in and out.

## Open — new section

Questions the living has raised or left unruled; no statement is
proposed for these:

- O1. Numbers: how a decimal or float is written, and whether a float
  position reads a dotted number such as a version. Asked, never
  answered; nothing implemented.
- O2. Comments: the living's own early examples used a double
  semicolon; no ruling for datom; nothing implemented.
- O3. Newlines and indentation: no ruling. The code treats all
  whitespace as separator and emits one space.
- O4. Absent values: no ruling. The code writes None and Some.value for
  text only.
- O5. The name of the structured string type (see M1).

## Left out as not datom syntax

- Kinds instead of generics; angle brackets for generics; the colon
  transformer form; slash for imports — Ethos syntax.
- Tuples as un-specification; single-field structs disliked; newtypes
  allowed — type-shape rulings for their own topic.
- The ruling on negatives in distillation — distillation practice.
- The skill family (a simple protos skill; fleshed-out, explicit,
  concrete-example ethos and datom skills) — carried into this flow's
  skill work, not into `Vision/datom.md`.

## Sources

- `flows/ac1e9ec8/reports/datomSyntaxWrittenPsyche.md`
- `flows/ac1e9ec8/reports/datomSyntaxTranscripts.md`
- `flows/ac1e9ec8/witnesses/datomCurrentSyntax.md`
- `flows/ac1e9ec8/reports/rememberedFlows.md`
- `Vision/datom.md`, `psyche-raw/Intent/protosParsing.md`,
  `psyche-raw/Vision/encodedFormIsTheCode.md`
