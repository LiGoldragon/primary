<!-- to-the-living:start -->
Presentation.{ «Word ids for flows — second edition» }

## Add `wordable-clj/ethos/wordable.ethos`

Removed: none; this is a new file in a proposed,
flow-id-specific Clojure source home.

Added:

```ethos
Operation
[ ]
[ PrefixFromUuid.SessionUuid
  WordIdFromPrefix.FlowPrefix
  PrefixFromWordId.WordIdText
  RegexFromWordId.WordIdText
  MatchPaths.MatchRequest ]
[ Prefix.FlowPrefix
  WordId.WordIdText
  Pattern.RegexPattern
  Matches.MatchSet
  Rejected.InputError ]
[ UuidText.String
  SessionUuid.{ UuidText }
  PrefixValue.Integer
  FlowPrefix.{ PrefixValue }
  WordIndex.Integer
  FirstWordIndex.{ WordIndex }
  SecondWordIndex.{ WordIndex }
  ThirdWordIndex.{ WordIndex }
  DictionaryId.[ Bip39EnglishV1 ]
  FlowWords.{ DictionaryId FirstWordIndex
              SecondWordIndex ThirdWordIndex }
  LowerCamelText.String
  WordIdText.{ LowerCamelText }
  JavaPatternSource.String
  RegexPattern.{ JavaPatternSource }
  PathText.String
  TranscriptPath.{ PathText }
  TranscriptPaths.Vector<TranscriptPath>
  MatchRequest.{ WordIdText TranscriptPaths }
  MatchSet.[ NoMatch
             OneMatch.TranscriptPath
             ManyMatches.TranscriptPaths ]
  UnknownWordText.String
  InputError.[ MalformedUuid InvalidPrefix
               InvalidWordId
               UnknownWord.UnknownWordText ] ]
```

The landed rule in
`mind-skills/skills/operation-clojure-development.md`
requires this Ethos anatomy to specify data and types
before Clojure behavior is implemented.

`SessionUuid` is canonical hyphenated UUID text. Accept
ASCII hex in either case; do not require a UUID version
or variant. `FlowPrefix` is an unsigned integer in
`[0, 2^33)`. Read canonical UUID text-order bytes,
most-significant bit first, and take the first 33 bits.
Do not use platform-specific GUID byte order.

`DictionaryId` identifies a proposed immutable word
list: `bitcoin/bips` commit
`e9d5abfe964db0429e9ca21274439fd981a8a342`, file
[`bip-0039/english.txt`](https://github.com/bitcoin/bips/blob/e9d5abfe964db0429e9ca21274439fd981a8a342/bip-0039/english.txt),
SHA-256
`2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda`.
It has 2,048 sorted unique lowercase English words,
indexed from 0 through 2,047. Carry the license
attribution from the pinned
[`BIP-0039 specification`](https://github.com/bitcoin/bips/blob/e9d5abfe964db0429e9ca21274439fd981a8a342/bip-0039.mediawiki).
This is a proposed selection, not an approved
dictionary.

`WordIndex` is an 11-bit index. `FlowWords` keeps the
three groups in most-significant-first order. Split the
prefix into consecutive 11-bit groups. Render the
corresponding words in lower camel case, capitalizing
the first letter of words two and three. Prefix value
`1` maps to `[0, 0, 1]`, `abandon`, `abandon`,
`ability`, and `abandonAbandonAbility`. This uses the
BIP-39 list only; it is not a wallet mnemonic and does
not use BIP-39 checksum or seed rules.

`WordIdText` accepts exactly three words in canonical
lower-camel form. Reject malformed casing, other word
counts, non-ASCII letters, and unknown words. Decoding
returns only the 33-bit prefix; it cannot reconstruct
the full 128-bit UUID.

`RegexPattern` is source for Java
`java.util.regex.Pattern`. Match only complete basenames
in these two forms: `UUID.jsonl` or
`rollout-YYYY-MM-DDTHH-MM-SS-UUID.jsonl`. The timestamp
is filename syntax only; do not validate its calendar
or clock values. Anchor the pattern at both ends. Use
case-insensitive matching for UUID hex, but keep the
other filename text exact. Do not constrain UUID version
or variant. For each prefix, format its first 32 bits as
eight hex digits and constrain bit 33's nibble to
`[0-7]` or `[89a-f]`. Call `Matcher.matches()` on each
basename. For prefix `1`, this Clojure expression
produces Java Pattern source:

```clojure
(str
  "^(?:(?i:00000000-[89a-f][0-9a-f]{3}-"
  "[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
  "\\.jsonl|rollout-[0-9]{4}-[0-9]{2}-"
  "[0-9]{2}T[0-9]{2}-[0-9]{2}-[0-9]{2}-"
  "(?i:00000000-[89a-f][0-9a-f]{3}-"
  "[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})"
  "\\.jsonl)$")
```

`MatchRequest` supplies one word id and paths; no file
is read. Match the basename only, never a directory
component. `MatchSet` reports zero, one, or many
matching paths.
`InputError` distinguishes malformed UUID, invalid
prefix, malformed word id, and an unknown word. The
operations convert UUID text to prefix, prefix to word
id, word id back to prefix, word id to regex, and word
id plus supplied paths to the complete match set.

This adds a prefix label and lookup over supplied paths.
It does not alter six-hex aliases or prescribe title or
registration grammar. A 33-bit prefix can collide; a
match set keeps that ambiguity visible. Canonical
word-ID/title integration is the next increment; this
anatomy does not silently replace current identities.

Ruling: approve the proposed pinned dictionary,
lower-camel spelling, and Ethos anatomy, or specify the
correction. The 33-bit prefix mapping is fixed by the
specified bit order and is not a separate choice.
Also rule on the `vision-flow` distillation below.

## Distillation

File root: `/git/github.com/LiGoldragon/`
Authored source: `psyche-skills/skills/vision-flow.md`

Removed: none.

Insert at line 22, immediately after the exact anchor
`and is written in words.`

Added:

```text
A word id represents the first 33 bits of its
harness id.
```

Provenance: `flows/0c85a3/notion/flow-identifiers.md`,
2026-10-09, relayed by 41fa34.

Ruling: approve these exact `vision-flow` lines.

<!-- to-the-living:end -->
