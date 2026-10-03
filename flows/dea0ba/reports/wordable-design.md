# Wordable: typed, reversible word encodings

This is a design proposal for living review.  It does not claim an adopted
codec, a generated library change, or a collision-free short identifier.

## Proposed Ethos surface

```ethos
Library
[]
[ DictionaryVersion.{ DictionaryName.String Revision.Integer }
  WordParseError.[ Empty NonCanonicalText UnknownWord.String
                    WrongWordCount.{ Integer Integer }
                    InvalidIndex.Integer
                    DictionaryMismatch.{ DictionaryVersion DictionaryVersion }
                    NonCanonicalPadding ] ]
[ WordDictionary.{ [] []
    [ VERSION.DictionaryVersion BITS_PER_WORD.Integer ] [] }
  WordSequence.[ text.[ String ] ]
  Wordable.{ [] [ Dictionary<WordDictionary> Words<WordSequence> ]
    [ WIDTH_BITS.Integer ]
    [ as_words.[ Words ]
      parse_words:{ [ Words ] [ Result<Self WordParseError> ] } ] } ]
[]
```

`Wordable` is the reusable contract: a typed value has canonical words and
canonical words either recover that value or describe why they do not.
`WordDictionary` is necessary because vocabulary ordering, revision, and word
bit width are shared library facts. `WordSequence` is necessary only to make
the associated word representation opaque to the contract; implementations can
choose compact indices or text without dictating the public value shape.
`DictionaryVersion` is needed when words cross a persisted or untyped boundary,
where a receiver must not silently pick a vocabulary. `WordParseError` reports
only parse failures.

There is deliberately no `WordCode` data wrapper, no encoding-metadata
envelope, and no truncation capability. A wrapper becomes appropriate only if a
future wire format stores bare words without surrounding dictionary context.

## Concrete FlowId and its identity boundary

`FlowId` is a real 33-bit word-addressed value. It is the first 33 bits of the
native harness UUID, in the UUID's specified byte order, encoded with the
selected dictionary; it is not a display alias and it cannot reconstruct the
UUID. The full UUID remains a separately stored native-harness correlation in
the registry.

For BIP-39 English revision 1, the 2,048-entry vocabulary supplies 11 bits per
word, so `FlowId` has exactly three words:

```rust
pub struct FlowId(Words<Bip39EnglishV1, 3>);

impl Wordable for FlowId {
    type Dictionary = Bip39EnglishV1;
    type Words = Words<Bip39EnglishV1, 3>;
    const WIDTH_BITS: i64 = 33;
    // as_words / parse_words
}
```

The intended Datom-facing rendering is a scalar headed form, for example
`FlowId.abandonAbilityAble`; the index vector is internal codec bookkeeping,
not the user interface. The current datom-codec README permits a bare string
when it contains no delimiter characters, which covers that lower-camel word
text. If the generated derive cannot emit this scalar form, add a small owned
Datom adapter; this proposal does not require generator work.

A registry lookup by `FlowId` may find zero, one, or multiple full UUIDs. More
than one is explicit `Ambiguous` at the lookup boundary and fails closed. It
must never choose a UUID or add an automatic suffix. Broader widths and any
shortening of another identifier are separate, explicit projections with their
own collision handling; `Wordable` itself never truncates.

## Canonical codec rules

This proposal supports dictionaries whose cardinality is a power of two. Read
source bits most-significant-bit first. Emit `ceil(width / bits_per_word)`
words; when there is a partial final word, right-pad it with zero bits and
reject non-zero padding on parse. With an 11-bit dictionary: 32 bits uses three
words and one required zero bit; 33 uses three exact words; 64 uses six words
and two required zero bits; 128 uses twelve words and four required zero bits.
The parser checks declared dictionary/version context, exact word count,
vocabulary membership, index range, canonical text, and final padding.

`as_words` is infallible because a constructed typed value is valid. Parsing is
fallible. A non-power-of-two dictionary needs a different base-conversion
contract and is outside this first kind.

## Generator and Rust evidence

The proposal was checked with the current `ethos-zero` binary using an
isolated fixture containing the Ethos above:

```text
cargo run --manifest-path /git/github.com/LiGoldragon/ethos-zero/Cargo.toml -- \
  Check.«…/wordable.ethos»
# Checked.…/wordable.ethos

cargo run --manifest-path /git/github.com/LiGoldragon/ethos-zero/Cargo.toml -- \
  Generate.{ «…/wordable.ethos» «…/out» }
# Generated.[ …/out/wordable.rs ]
```

It generated the following actual shape (with `Integer` rendered as `i64`):

```rust
pub trait Wordable {
    type Dictionary: WordDictionary;
    type Words: WordSequence;
    const WIDTH_BITS: i64;
    fn as_words(&self) -> Self::Words;
    fn parse_words(input: Self::Words) -> Result<Self, WordParseError>
    where Self: Sized;
}
```

An isolated `rustc --edition=2024` probe compiled and ran with
`Words<D, const COUNT: usize>` and the `FlowId` implementation above. A second
probe established that stable Rust rejects an array type calculated as
`[u16; (BITS + 10) / 11]`: generic parameters may not participate in that
const operation. Therefore the public contract should carry associated
`Words` and `WIDTH_BITS`, while each implementation uses a fixed word count
(such as three for `FlowId`) or other storage it controls. No Ethos generator
change is evidenced by this proposal.

The existing `signal-5f4fea-word-identifiers` prior work independently shows
fixed BIP-39 3/6/12-word `u16` arrays and MSB-first bit handling. It is useful
codec prior art, but its hard-coded widths and index representation are not the
public contract proposed here.
