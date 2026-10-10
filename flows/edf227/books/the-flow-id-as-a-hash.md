# The flow id as a hash

Back burner, as you said; designed so it is ready. The question was how the Nexus can hold the id as a hash and never see text, while the CLI reads and writes its text forms.

## 1. What the id is

The id is a number of a fixed width — 33 bits of the harness's session id — not text. The Nexus stores and compares the number. Text is a rendering: today the six hex characters, later three words. Both renderings are reversible, so tools get from the text back to the number and from the number to the transcript.

Drawing: one number in the middle (a box labelled "33-bit hash"), two arrows out to "hex: 6329f1" and "words: abandonAbilityAble", two arrows back; the Nexus drawn around the number only, the CLI drawn around the text.

## 2. In ethos

A newtype over the integer, bearing a kind that states its width and its renderings. A kind is where "special deserialization" lives: one implementation per rendering, written once, behind the type.

```
Library                              ; shared by Flow, its CLI and every component
[]
[ FlowId.{ Integer }                 ; a number of its own type, not a bare integer
  HashError.[ Malformed              ; the text is not a rendering of this width
              Collision.Vector<Self> ] ]  ; more than one hash matches; every match is returned
[ Hashable.{ []                      ; a kind: a fixed-width hash with renderings
             [ Hex                   ; its text forms are associated types
               Words ]
             [ WIDTH_BITS.Integer ]  ; the width, 33 for FlowId
             [ as_hex.[ Hex ]        ; render; read back; same for words
               parse_hex:{ [ Hex ]
                           [ Result<Self HashError> ] }
               as_words.[ Words ]
               parse_words:{ [ Words ]
                             [ Result<Self HashError> ] } ] } ]
[]
```

## 3. Where the text lives

The renderings compile only into the CLI side, with the datom feature. The Nexus is built without it: it holds the number, keys its records by the number, and answers refusals as vocabulary. A collision in the rendering comes back as a typed refusal naming every match, and reaches you.

Drawing: two columns, "Nexus build" and "CLI build"; the FlowId number in both; the Hashable renderings only in the CLI column; the wire between them carrying the number.

## 4. What must change, and the choice

The generator gains one thing: a declared link from a kind's rendering to the type's datom form, so the derive reads and writes the rendering instead of the raw number. Today the id is a bare string everywhere and the Nexus itself reads hex; that goes.

1. This shape: a newtype over the integer, a Hashable kind, renderings in the CLI build only.
2. A hash intrinsic in the substrate instead, with the rendering chosen by a kind parameter.
3. Keep the harness's whole id as bytes in memory; the short text form resolved by a query.
4. Leave it on the burner; comment later.
