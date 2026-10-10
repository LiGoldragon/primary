Presentation.{ «The word id, as a kind» }

Your words: "It's generic so we can use it for any hashes of any size. ... Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?" -- psyche, typed, book comment, 2026-10-03T16:08Z. Mind Astra designed it; ethos-zero as it runs today checked the ethos and generated the Rust; the Rust compiles. Here it is in code, for your word.

## 1. The kind, in ethos

A kind named `Wordable`: no superkinds; two associated kinds, its dictionary and its word sequence; one constant, the width in bits; two capabilities, render to words and read back. The dictionary is itself a kind carrying its version and its bits per word. It sits in the shared Library, so every type with a hash of any width can bear it.

```
Library
[]
[ DictionaryVersion.{ DictionaryName.String
                      Revision.Integer }
  WordParseError.[ Empty
                   NonCanonicalText
                   UnknownWord.String
                   WrongWordCount.{ Integer Integer }
                   InvalidIndex.Integer
                   DictionaryMismatch.{ DictionaryVersion
                                        DictionaryVersion }
                   NonCanonicalPadding ] ]
[ WordDictionary.{ []
                   []
                   [ VERSION.DictionaryVersion
                     BITS_PER_WORD.Integer ]
                   [] }
  WordSequence.[ text.[ String ] ]
  Wordable.{ []
             [ Dictionary<WordDictionary>
               Words<WordSequence> ]
             [ WIDTH_BITS.Integer ]
             [ as_words.[ Words ]
               parse_words:{ [ Words ]
                             [ Result<Self WordParseError> ] } ] } ]
[]
```

## 2. The Rust it generates, and the flow id bearing it

```rust
pub trait Wordable {
    type Dictionary: WordDictionary;
    type Words: WordSequence;
    const WIDTH_BITS: i64;
    fn as_words(&self) -> Self::Words;
    fn parse_words(input: Self::Words)
        -> Result<Self, WordParseError>;
}

pub struct FlowId(Words<Bip39EnglishV1, 3>);

impl Wordable for FlowId {
    type Dictionary = Bip39EnglishV1;
    type Words = Words<Bip39EnglishV1, 3>;
    const WIDTH_BITS: i64 = 33;
}
```

The first 33 bits of the harness's own id, read in a fixed byte order, through the 2048-word BIP-39 English list at 11 bits a word: exactly three words, no padding, and back again without a table. In datom the id is one bare word: `FlowId.abandonAbilityAble`. The full harness id stays in Flow's true registry beside the words; a lookup that finds two is answered `Ambiguous` and stops, never a guessed suffix. The kind never truncates; a wider or narrower id is its own type with its own width.

## 3. Your choices

1. Approve as written; the flow id becomes this type in the shared library, and Flow and the launchers switch to it.
2. Approve, but with a denser word list than BIP-39 (more bits a word, fewer or shorter words), as you wondered in September; Mind picks and reports the list.
3. Change the kind's name or the capabilities' names (write them).

One small detail: if the generated derive cannot print the id as that single bare word, a small hand-written printer for this one type is added; no generator change. Say if you would rather the generator learn it.
