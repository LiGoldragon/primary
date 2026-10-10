# Datom anatomy from first principles (design document, round 1)

Drawn from the psyche's 2026-08-27 monologue (flows/04db2fd2/vision/*). Code set aside.
Everything marked (offered) is the flow's inference, put to the psyche; the rest is the psyche's.

## Forms and direction

    textual form                                                 real form
    Text ──Delineate──► Delineation ──match Anatomy<T>──► T        (Realize: fallible; text is prospective)
    Text ◄──render──── Delineation ◄──portion by Anatomy<T>── T    (Textualize: infallible; a real T is a datom)

Asymmetry is intrinsic (psyche): what comes in is a prospective datom, untrusted until it matches;
what goes out is a datom. (offered) Hence Realize carries a fault and Textualize carries none;
spans exist on the way in and are computed on the way out.

## Kinds (capabilities)

| Kind        | Carried by                 | Yields                          | Level  |
|-------------|----------------------------|---------------------------------|--------|
| Delineate   | Text                       | Delineation (portions + spans)  | protos |
| Realize     | Prospective<T> (textual)   | T, or a fault                   | protos trait, dialect impl |
| Textualize  | T (real)                   | Text                            | protos trait, dialect impl |
| (offered) Anatomize | a type             | Anatomy — the type's data graph | protos; ethos generates it |

The psyche's first cut was Decomposable → composable parts → recomposable. Its second cut was
"keyframes": find where portions begin and end and roughly what they are, before typing. (offered)
Both survive as two passes: Delineate is the untyped keyframe pass; matching against Anatomy is the
typed decomposition; composing portions by Anatomy is the reverse.

## Types (protos, universal to all dialects)

- Text — the pure textual form; claims nothing. (Name for the unscanned text: see Names.)
- Portion — every object is a portion; the universal term for field, variant, element.
  - enclosure: Open (delimiters implied by position: bare string, opened struct) | Closed(Delimiter)
  - form (recursive):
    - Headed { head: Head, separator: Separator, body: Portion }   — x.y.z.w is Headed whose body is Headed …
    - Braced / Bracketed / Guillemeted { portions: [Portion] }
    - Quoted { text } / Parenthesized { … Meaning, later }
    - Bare { text }
  - span: absent until computed (input: found by Delineate; output: computed by render)
- Head — a string (what the head says).
- Separator — an actual enum: `.`, `:`, `!`, … (the set is a protos vocabulary; meaning is per context).
- Delimiter — one type, open+close glyphs, used by Delineate and render alike (one table, not three).
- Span — representation pending research (byte offsets vs line/col vs rope).
- Anatomy — a type's anatomy as data: how many portions, of what kind. (offered) Struct{portions},
  Enum{variants}, Vector{portion}, Map{key, value}, Unit, String, Integer, Bool, …
  This is the same thing ethos declares; it is the bridge between the two prongs.

## Names (offered, psyche asked)

For the unscanned text ("not blob"): Text (pure; the stage is carried by what it can do), or if the
unscanned-ness must be in the name: Intake, Unread.
For the text taken as a would-be T: Prospective<T> — the psyche's own word. Alternatives: Putative<T>,
Candidate<T>.
For the keyframe pass ("annotate" rejected): Delineate → Delineation (to mark the outline and
boundaries). Alternatives: Survey → Survey, Chart → Chart.

## Multi-pass

Passes are wanted, not a single pass. In: delineate, match, construct. Out: portion, render.
Beginning/end are not intrinsic to an object; they are found on the way in and computed on the way out.

## Datom as a nexus

Stays a library for now; a translating nexus between formats is a later possibility.

## Questions put to the psyche

1. Delineate/Delineation for the keyframe pass?
2. Is Delineation the universal protos product, with anatomy-matching the dialect's part?
3. Separator: a protos-universal enum whose meaning is assigned per context (like delimiters)?
4. Daisy chain x.y.z.w = right-nested Headed portions — so Observed.Locks.[] is Headed(Observed,
   Headed(Locks, Bracketed[]))), mirroring variant-in-variant-in-vector?
5. Anatomy textualizes as ethos (per "cli help emits the ethos syntax that describes their anatomy"),
   not as datom?

## Sources

- flows/04db2fd2/vision/*.md — the psyche's 2026-08-27 monologue, by topic
- reports/protosDatomPsyche.md — earlier rulings (forms, Realize/Textualize, Head, context)
- witnesses/datomTextualizeRealizeAnatomy.md — only as the thing set aside
