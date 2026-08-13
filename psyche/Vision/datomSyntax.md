# Datom syntax

## 2026-08-11 — Datom carries data only; no generics

> datom doesnt do generics, it only carries data, like json (but
> strictly typed of course)

— psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07), typed,
correcting the Designer's syntax sheet, which had carried the
2026-08-04 bare-angle-bracket generics ruling as a Datom gap:
generics belong to Ethos; Datom is the data carrier — strictly
typed, like JSON. The 2026-08-04/06 syntax rulings predate the
Datom/Ethos split; each ruled construct needs its language assigned.

## 2026-08-11 — fix Datom first; the syntax must become consistent

> So we can just fix datum [Datom] first because we need that. We
> need the syntax to start being consistent.

> I'm not even sure where parentheses are going to be in datum
> [Datom] because in ethos, they're for transformers.

— psyche, 2026-08-11T17:35+02:00 (Designer session 012fbf07),
dictated; bracketed readings are agent transcription repairs. Datom
syntax is fixed first — consistency is the need. Open fork carried
to the syntax round: where parentheses land in Datom, given Ethos
uses them for transformers.

## 2026-08-11 — parentheses must not be unused in Datom

> On parenthesis: It would be strange for parenthesis to be unused in
> datom. They are a major symbol of cognition.

— psyche, 2026-08-11T18:53+02:00 (Designer session a5587095), typed,
answering the Designer's proposal that parentheses leave Datom
entirely. Parentheses must carry a Datom duty; which duty is open.
In the same message the psyche freed parentheses in Ethos
(colonFormTransformerSyntax.md) and floated the structured string
type (structuredStringType.md) without assigning it a delimiter.

## 2026-08-11 — parentheses delimit the structured string; one string type, two variants

> 1. I am considering it, yes. This would require a new type (in
> rust, later ethos-generated) which can be met with either a curly
> quotes or parenthesis (two variants, legacy and structured). The
> structured type would allow for an arbitrary depth, since it is a
> graph of sorts.

> 3. shape is still up in the air, but () would be the delimiter

— psyche, 2026-08-11T19:17+02:00 (Designer session a5587095), typed,
answering the Designer's structured-string anatomy questions 1
(assignment) and 3 (shape). One string type (Rust now, Ethos-
generated later), two variants: legacy — curly quotes U+201C/U+201D
— and structured — parentheses, arbitrary depth, "a graph of
sorts". The parenthesis delimiter is ruled; the full assignment is
"considering"; shape is open. Detail in structuredStringType.md.

## 2026-08-11 — map payload is a vector: `Map.[key.val …]`

> Yes, map would use .[ since a map is conceptually a list of
> key/values

— psyche, 2026-08-11T19:17+02:00 (Designer session a5587095), typed.
Supersedes the ported `Map.(…)` encoding: the map payload is a
square-bracket vector of `key.value` entries.

## 2026-08-13 — Meaning postponed in datom; () or curly quotes both land as String for now

> we'll postpone the Meaning type in datom to get a working syntax
> asap. lets accept a () or the curly quotes for strings for now,
> with the actual shapedefined implementation just casting both into
> a string for now, with a comment to implement the Meaning type
> later (the super-string type we discussed before).

— psyche, 2026-08-13 (Designer session 06196cc7), typed. Interim
surface for a working syntax asap: the string slot accepts
parenthesis-delimited or curly-quote text, and its ShapeDefined
implementation selects plain String for both, with a code comment
pointing at the later Meaning type (structuredStringType.md). This
defers, not supersedes, the 2026-08-11T19:17 parentheses-as-
structured-string ruling; Meaning's shape and vocabulary stay open
under bead primary-xqb.8.5.
