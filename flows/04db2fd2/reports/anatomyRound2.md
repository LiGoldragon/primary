# Datom anatomy from first principles (design document, round 2)

Round 1 revised by the psyche's rulings this turn: Delineate accepted; delineation and anatomy are
protos; Prospective<T> liked; Datom probably a kind; direction asymmetry approved for Vision.
(offered) marks the flow's inference.

## The whole picture

    TEXTUAL                                      PROTOS (universal)                             REAL
    Text ─taken as─► Prospective<Datom> ─Delineate─► Delineation ─match Anatomy<T>─► T
                     kind known, type unsaid         portions + spans, untyped        Prospective<T> realized
    Text ◄──render── Delineation ◄──────────portion by Anatomy<T>────────────────── T
                     spans computed

In: fallible (prospective until it matches). Out: infallible (a real value is whole). Several passes each way.

## Universal principles of shape (protos; every dialect rides them)

1. Every object is a portion. A portion has a shape and a body; the body is text or portions.
2. Shape = enclosure + head. Enclosure: Open (delimiters implied by position) or Closed(Delimiter).
   Head: absent, or Head + Separator. Open and closed are two versions of the same thing.
3. What the enclosure says about arity — the anatomical principle:
   - `{}`  arity is anatomical: the count of portions belongs to the anatomy, and each position has its own anatomy.
   - `[]`  arity is free: any count; every portion shares one anatomy.
   - `<<>>` arity is free; portions come in pairs, one key anatomy and one value anatomy.
   - `""` and bare: no portions — text.
   - `()`  Meaning, later.
4. A head names an alternative: a Head is always a variant, and its body is that variant's portion.
   The separator adds a further distinction, read per context.
5. Context gives shapes their meaning (Intent). Within one enclosure, arity discriminates anatomies.
6. Anatomy is the tree of shapes with their arity — described without the type's name or meaning.

## Types (protos)

    Text                          the pure textual form; claims nothing
    Prospective<K>                text taken as a would-be K; delineatable when only the kind is known,
                                  realizable once the type is given
    Delineation = Portion         the untyped structural product
    Portion { enclosure: Open | Closed(Delimiter),
              head: Option<(Head, Separator)>,
              body: Text | [Portion],
              span: Option<Span> }         span found on the way in, absent/computed on the way out
    Head(String)                  what the head says
    Separator                     enum: `.` `:` `!` … — protos vocabulary, meaning per context
    Delimiter                     one type, open + close glyphs — the single table both directions use
    Span                          byte offsets start..end into the Text (research: what every parser does)
    Anatomy                       Positional{portions: [Anatomy]}   `{}`
                                  Repeated{portion: Anatomy}        `[]`
                                  Paired{key, value: Anatomy}       `<<>>`
                                  Headed{head, separator, body: Anatomy}   one alternative
                                  Alternatives{[Headed]}            the set a position may meet
                                  Text                              `""` / bare

Datom's reading: Positional = struct, Repeated = vector, Paired = map, Alternatives = enum,
Headed = variant, Text = string/integer/bool (integer and bool are Text anatomies with a canon).
Ethos declares anatomies; datom fills them. Enclosure is not in the anatomy: whether a Positional
appears braced or opened is decided by position.

## Kinds (verbs, as Realize/Textualize)

    Delineate    on Prospective<Datom>   → Delineation        protos
    Realize      on Prospective<T>       → T | Fault          protos trait, dialect impl
    Textualize   on T                    → Text               protos trait, dialect impl
    (offered) Anatomize  on a type       → Anatomy            protos; ethos generates

## Datom: kind (offered)

A kind is what a thing can do; a type is what a thing is — its anatomy. Datom has no anatomy of
its own; it is the capability of crossing the textual edge as pure typed data: having an anatomy,
hence Realize and Textualize. Every concrete datom (Report, OrchestrateRequest) is a type with the
Datom kind. So Prospective<Datom> — type unsaid — can be delineated (protos needs no type) but not
realized; Prospective<Report> can be realized. The expected type is the parsing context.

## Names offered

Portion — keep; the one word for field, variant, element; no Rust baggage. (Part, Member weaker.)
Span — keep; the universal parser word; byte offsets. Alternative in the psyche's own terms: Extent.
Delineate — the kind (verb, like Realize); Delineation — its product; "delineatable" = implements Delineate.

## Open

- Is Delineate context-free for every dialect? It is when delimiters balance and quoted/Meaning
  bodies are opaque. If a dialect's context ever changes what closes a portion, delineation
  needs the context too.
- Whether Alternatives (the set of heads a position may meet) is anatomy or context.
- Separator set: which glyphs are in the protos enum.

## Sources

- flows/04db2fd2/vision/*.md — the psyche's words this session (anatomy, portion, delineate, textualTypes, multiPass, directionAsymmetry)
- reports/anatomyFirstPrinciples.md — round 1
- reports/textPositionRepresentations.md — spans, green/red trees
- reports/protosDatomPsyche.md — earlier rulings; psyche-raw/Intent/protosParsing.md
- flows/b675f3d9/vision/structuralParsing.md — arity discriminates; separators carry type
