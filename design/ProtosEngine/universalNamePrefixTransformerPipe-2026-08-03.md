# Universal Name Prefix; Bare Pipe Marks the Transformer — 2026-08-03

> **Supersession notice (2026-08-06).** Later rulings supersede parts of this file; the text below is preserved unedited as the record. No longer in force:
> - Bare `|` as the name/transformer separator — superseded by `.( )` (`Name.Transformer.(...)`) (`llmTokenOptimizationRulings-2026-08-04.md`).
> - The sectioned `Name.(...)` form — subsequently cut (`llmTokenOptimizationRulings-2026-08-04.md`).
> The design log reads by recency; consult the named files for the current form.

Ruling chain from the psyche session of 2026-08-03, continuing the stream
syntax thread. Supersedes, within `streamNomosApplication-2026-08-02.md`:
the object-first standalone seating ("the Nomos object comes first:
`Stream.Observer.{...}`"), the dotted-chain parameter binding as a wanted
Nomos capability, and the both-name-placements clause. The method line
(design syntax by how it encodes and decodes) and the legitimacy of
sectioned name-first stand.

## Dotted-chain form dropped

Agent text answered: the manager's presentation of the encoded
operator-application record (`operator`, `name`, `fields` in
`core-ethos/src/whole.rs`) and the question whether third-and-beyond
dotted symbols should become legal authored surface.

Psyche ruling [psyche-verbatim]: "actually I think id rather drop the
whole thing. Stream.Observer.{} looks like a newtype. If a transformer
only needs a single argument, then it can certainly be Transformer.X,
but as soon as it takes more than one, we might as well just go with
Transformer.{}, so we would end up with Stream.{ Observer ... } . my
point is to avoid cognitively overloading patterns."

Seated:

- The dotted-name application form `Stream.Observer.{...}` is dropped;
  the chain-binding capability commission is withdrawn.
- Arity spelling: one argument `Transformer.X`; more than one,
  `Transformer.{...}`.
- The intermediate `Stream.{ Observer ... }` (name as first payload
  field) was superseded within the same session by the universal name
  prefix below. Do not implement it.

## Universal name prefix; a structural separator classifies what follows

Agent text answered: the manager's observation that classifying `A.B`
(transformer application vs type application) requires head resolution
against the Nomos transformer table, the call-marker glyph candidates,
and a stray `Struct.{...}` spelling.

Psyche ruling [psyche-verbatim]: "thanks for reminding me why agents are
not going to design my syntax. The prefix should universally be the
name. then something differentiates what comes after. Your ! is giving
me ideas which I hadnt expected. We would have needed a cognitively
different transformer syntax for non-trivial structs/enums, which would
have broken the concistency, but now we can introduce a new concept;"
[example block authored with `!`, before the separator ruling below]

```ethos
;; Name    transformer
Something!ComplexStruct.{ ... }
Observer!Stream.{ ... }

;; Regular struct
X.{ ... }
;; Regular enum
Y.[ ... ]
```

"maybe Name|Transformer is visually easier to see. or maybe something
else. Name-Transformer?"

## Separator ruling

Psyche ruling [psyche-verbatim]: "| wins"

Seated:

- At a declaration position the first symbol is universally the declared
  name. Name-first is the one parse model; this resolves the open
  "one parse model must win" from `streamNomosApplication-2026-08-02.md`.
- What follows the name classifies structurally, with no table lookup:
  `.` opens plain data — `{...}` a struct body, `[...]` an enum body, a
  symbol chain a type reference — and bare `|` declares that a Nomos
  transformer head follows, then its payload:
  `Observer|Stream.{ ... }`; single argument `Name|Transformer.X`
  [manager composition of the two rulings above].
- The dot-world is guaranteed plain data: no transformer can appear
  unmarked, so the Ethos parser needs no Nomos transformer table. This
  repairs the two decode incoherences that rejected name-first
  standalone forms on 2026-08-02: the separator distinguishes the form
  from a newtype, and the name stands outside the application, so no
  payload injection.
- Glyph claim: bare `|` is the name/transformer separator. Lexical
  safety verified against the glyph inventory: `|` is not a legal Ethos
  name character (`[A-Za-z0-9_:-]`) nor a Dotos bare-symbol continuation
  character; the compound pipe delimiters (`[|`, `(|`, `{|`) stay
  unambiguous because their `|` immediately follows an opening bracket
  while the separator's `|` always follows a name.
- Encoded form already fits: `WholeEthosOperatorApplication { operator,
  name, fields }` maps prefix name to `name`, transformer to `operator`,
  payload to `fields`. The change is textual surface and lexer only.
- `[...]` in a definition position is the enum body ("Regular enum:
  `Y.[ ... ]`").

Open:

- Sectioned entries where the position supplies the transformer
  (operator written zero times): does the separator vanish with the head
  (`Observer.{...}`) or survive alone (`Observer|{...}`)? Not ruled.
- Stream payload semantics (open-query, response, pushed event) remain
  the commissioned design; `primary-vq6.6` stays blocked on them alone.
