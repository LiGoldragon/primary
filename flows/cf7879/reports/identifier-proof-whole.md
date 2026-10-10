# Identifier proof — whole review material

Proposal only. Source revision `cdf4912f7cbabc6a84850a8d903d59dcec850f14` on `proposal/cf7879-word-identifiers-validation`. This is not a merge or an adopted identifier vocabulary.

The three nominal reference types hold 3, 6 or 12 word indices. The full BLAKE3 digest remains separate. The corrected decode boundary checks indices before exposing a reference; build-time validation checks the exact Ethos shapes. Seven focused tests passed remotely and the check output was copied from Prometheus; a separately captured final Nix client exit is unavailable.

These short references do not guarantee uniqueness. A production lookup must detect collisions and disambiguate using the full digest; the 33-bit local form is especially limited. Authentication is outside this proof. No runtime registry or migration is implemented here.

Below are complete immutable source files, including the implementation tests and build-time schema validation. The build file also contains pre-existing Signal generation logic; its inclusion does not imply that logic was newly authored.

## ethos/identifiers.ethos

SHA256 `8056c4fba2f110ee0b596a599a2b3c309822f8e9d15f566f8035dcb4e0c4c78c`; 265 bytes.

```text
Library
[]
[ LocalNameReference.{ Integer Integer Integer }
  ClusterNameReference.{ Integer Integer Integer Integer Integer Integer }
  PublicNameReference.{ Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer Integer } ]
[]
[]
```

## src/identifiers.rs

SHA256 `68348ef598d0ab0e1700f0d161b4241eff1c60f82e76653b9644b8bbec1c2b55`; 11998 bytes.

```rust
//! Readable, nominal identifiers for local, cluster, and public references.
//!
//! `ethos/identifiers.ethos` is the schema for the three fixed-width forms.
//! Datom's available intrinsics at this revision are `String` and `Integer`,
//! with no standard hash primitive. `NameDigest` is therefore a Signal-owned
//! BLAKE3 adapter, not a claim about a Datom hash type or authentication.

use bip39::Language;
use std::fmt;

pub const BIP39_WORDS: usize = 2048;
pub const BITS_PER_WORD: usize = 11;
pub const LOCAL_WORDS: usize = 3;
pub const CLUSTER_WORDS: usize = 6;
pub const PUBLIC_WORDS: usize = 12;
pub const LOCAL_BITS: usize = LOCAL_WORDS * BITS_PER_WORD;
pub const CLUSTER_BITS: usize = CLUSTER_WORDS * BITS_PER_WORD;
pub const PUBLIC_BITS: usize = PUBLIC_WORDS * BITS_PER_WORD;

#[derive(
    rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Copy, Debug, PartialEq, Eq, Hash,
)]
pub struct NameDigest(pub [u8; 32]);

#[derive(
    rkyv::Archive, rkyv::Serialize, Clone, Copy, Debug, PartialEq, Eq, Hash,
)]
pub struct LocalNameReference([u16; LOCAL_WORDS]);
#[derive(
    rkyv::Archive, rkyv::Serialize, Clone, Copy, Debug, PartialEq, Eq, Hash,
)]
pub struct ClusterNameReference([u16; CLUSTER_WORDS]);
#[derive(
    rkyv::Archive, rkyv::Serialize, Clone, Copy, Debug, PartialEq, Eq, Hash,
)]
pub struct PublicNameReference([u16; PUBLIC_WORDS]);

// The raw archive shapes are private: received indices must cross the
// validated `decode` boundary below, rather than exposing rkyv's structural
// deserialization as proof that an index names a BIP-39 word.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
struct RawLocalNameReference([u16; LOCAL_WORDS]);
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
struct RawClusterNameReference([u16; CLUSTER_WORDS]);
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]
struct RawPublicNameReference([u16; PUBLIC_WORDS]);

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum NameParseError {
    Empty,
    NonCanonical,
    UnknownWord(String),
    WrongLength { expected: usize, actual: usize },
    InvalidIndex(u16),
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum NameDecodeError {
    InvalidArchive,
    InvalidIndex(u16),
}

impl NameDigest {
    pub fn of_bytes(bytes: impl AsRef<[u8]>) -> Self {
        Self(*blake3::hash(bytes.as_ref()).as_bytes())
    }
    pub fn local(self) -> LocalNameReference {
        LocalNameReference(words(&self.0, LOCAL_WORDS).try_into().expect("fixed width"))
    }
    pub fn cluster(self) -> ClusterNameReference {
        ClusterNameReference(
            words(&self.0, CLUSTER_WORDS)
                .try_into()
                .expect("fixed width"),
        )
    }
    pub fn public(self) -> PublicNameReference {
        PublicNameReference(
            words(&self.0, PUBLIC_WORDS)
                .try_into()
                .expect("fixed width"),
        )
    }
}

impl LocalNameReference {
    pub fn try_from_indices(indices: [u16; LOCAL_WORDS]) -> Result<Self, NameParseError> {
        validate(&indices).map(|_| Self(indices))
    }
    pub fn parse(text: &str) -> Result<Self, NameParseError> {
        parse_words(text, LOCAL_WORDS).map(|words| Self(words.try_into().expect("fixed width")))
    }
    pub fn decode(bytes: &[u8]) -> Result<Self, NameDecodeError> {
        let raw = rkyv::from_bytes::<RawLocalNameReference, rkyv::rancor::Error>(bytes)
            .map_err(|_| NameDecodeError::InvalidArchive)?;
        Self::try_from_indices(raw.0).map_err(decode_error)
    }
}
impl ClusterNameReference {
    pub fn try_from_indices(indices: [u16; CLUSTER_WORDS]) -> Result<Self, NameParseError> {
        validate(&indices).map(|_| Self(indices))
    }
    pub fn parse(text: &str) -> Result<Self, NameParseError> {
        parse_words(text, CLUSTER_WORDS).map(|words| Self(words.try_into().expect("fixed width")))
    }
    pub fn decode(bytes: &[u8]) -> Result<Self, NameDecodeError> {
        let raw = rkyv::from_bytes::<RawClusterNameReference, rkyv::rancor::Error>(bytes)
            .map_err(|_| NameDecodeError::InvalidArchive)?;
        Self::try_from_indices(raw.0).map_err(decode_error)
    }
}
impl PublicNameReference {
    pub fn try_from_indices(indices: [u16; PUBLIC_WORDS]) -> Result<Self, NameParseError> {
        validate(&indices).map(|_| Self(indices))
    }
    pub fn parse(text: &str) -> Result<Self, NameParseError> {
        parse_words(text, PUBLIC_WORDS).map(|words| Self(words.try_into().expect("fixed width")))
    }
    pub fn decode(bytes: &[u8]) -> Result<Self, NameDecodeError> {
        let raw = rkyv::from_bytes::<RawPublicNameReference, rkyv::rancor::Error>(bytes)
            .map_err(|_| NameDecodeError::InvalidArchive)?;
        Self::try_from_indices(raw.0).map_err(decode_error)
    }
}

impl fmt::Display for LocalNameReference {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        display(&self.0, f)
    }
}
impl fmt::Display for ClusterNameReference {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        display(&self.0, f)
    }
}
impl fmt::Display for PublicNameReference {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        display(&self.0, f)
    }
}

fn words(bytes: &[u8; 32], count: usize) -> Vec<u16> {
    (0..count)
        .map(|word| {
            let bit = word * BITS_PER_WORD;
            let mut value = 0u16;
            for offset in 0..BITS_PER_WORD {
                value = (value << 1)
                    | u16::from((bytes[(bit + offset) / 8] >> (7 - ((bit + offset) % 8))) & 1);
            }
            value
        })
        .collect()
}

fn display(indices: &[u16], f: &mut fmt::Formatter<'_>) -> fmt::Result {
    for (position, index) in indices.iter().enumerate() {
        let word = Language::English
            .word_list()
            .get(usize::from(*index))
            .ok_or(fmt::Error)?;
        let mut chars = word.chars();
        let first = chars.next().expect("BIP39 word");
        write!(
            f,
            "{}{}",
            if position == 0 {
                first
            } else {
                first.to_ascii_uppercase()
            },
            chars.as_str()
        )?;
    }
    Ok(())
}

fn parse_words(text: &str, expected: usize) -> Result<Vec<u16>, NameParseError> {
    if text.is_empty() {
        return Err(NameParseError::Empty);
    }
    if !text.is_ascii()
        || text.contains(|c: char| !c.is_ascii_alphabetic())
        || !text.as_bytes()[0].is_ascii_lowercase()
    {
        return Err(NameParseError::NonCanonical);
    }
    let starts = text
        .char_indices()
        .filter_map(|(at, character)| (at == 0 || character.is_ascii_uppercase()).then_some(at))
        .collect::<Vec<_>>();
    let pieces = starts
        .iter()
        .enumerate()
        .map(|(position, start)| {
            let end = starts.get(position + 1).copied().unwrap_or(text.len());
            let word = &text[*start..end];
            format!("{}{}", word[..1].to_ascii_lowercase(), &word[1..])
        })
        .collect::<Vec<_>>();
    if pieces.len() != expected {
        return Err(NameParseError::WrongLength {
            expected,
            actual: pieces.len(),
        });
    }
    pieces
        .into_iter()
        .map(|word| {
            Language::English
                .find_word(&word)
                .map(|index| index as u16)
                .ok_or(NameParseError::UnknownWord(word))
        })
        .collect()
}

fn validate(indices: &[u16]) -> Result<(), NameParseError> {
    indices
        .iter()
        .find(|index| usize::from(**index) >= BIP39_WORDS)
        .copied()
        .map_or(Ok(()), |index| Err(NameParseError::InvalidIndex(index)))
}

fn decode_error(error: NameParseError) -> NameDecodeError {
    match error {
        NameParseError::InvalidIndex(index) => NameDecodeError::InvalidIndex(index),
        _ => unreachable!("index validation only returns InvalidIndex"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn widths_are_explicit() {
        assert_eq!((LOCAL_BITS, CLUSTER_BITS, PUBLIC_BITS), (33, 66, 132));
    }
    #[test]
    fn display_round_trips_each_context() {
        let digest = NameDigest::of_bytes(b"signal identifier proof");
        assert_eq!(
            LocalNameReference::parse(&digest.local().to_string()).unwrap(),
            digest.local()
        );
        assert_eq!(
            ClusterNameReference::parse(&digest.cluster().to_string()).unwrap(),
            digest.cluster()
        );
        assert_eq!(
            PublicNameReference::parse(&digest.public().to_string()).unwrap(),
            digest.public()
        );
    }

    #[test]
    fn fixed_blake3_empty_digest_vector_has_stable_word_indices() {
        // BLAKE3's published empty-input digest. These are literal index
        // fixtures, independent of this module's extraction loop.
        let digest = NameDigest([
            0xaf, 0x13, 0x49, 0xb9, 0xf5, 0xf9, 0xa1, 0xa6,
            0xa0, 0x40, 0x4d, 0xea, 0x36, 0xdc, 0xc9, 0x49,
            0x9b, 0xcb, 0x25, 0xc9, 0xad, 0xc1, 0x12, 0xb7,
            0xcc, 0x9a, 0x93, 0xca, 0xe4, 0x1f, 0x32, 0x62,
        ]);
        assert_eq!(digest.local(), LocalNameReference::try_from_indices([1400, 1234, 883]).unwrap());
        assert_eq!(digest.cluster(), ClusterNameReference::try_from_indices([1400, 1234, 883, 1887, 1232, 1690]).unwrap());
        assert_eq!(digest.public(), PublicNameReference::try_from_indices([1400, 1234, 883, 1887, 1232, 1690, 1032, 77, 1873, 1463, 402, 1177]).unwrap());
        assert_eq!(digest.local().to_string(), "pyramidOlympicHover");
        assert_eq!(digest.cluster().to_string(), "pyramidOlympicHoverTypicalOldSpy");
        assert_eq!(digest.public().to_string(), "pyramidOlympicHoverTypicalOldSpyLibraryAnswerTuitionReportCraneNasty");
    }
    #[test]
    fn rejects_noncanonical_and_unknown_words() {
        assert_eq!(
            LocalNameReference::parse("AbandonAbilityAble"),
            Err(NameParseError::NonCanonical)
        );
        assert_eq!(
            LocalNameReference::parse("wibbleAbilityAble"),
            Err(NameParseError::UnknownWord("wibble".into()))
        );
    }
    #[test]
    fn nominal_reference_archives_and_restores_through_validated_boundary() {
        let value = NameDigest::of_bytes(b"archive").cluster();
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&value).unwrap();
        assert_eq!(
            ClusterNameReference::decode(&bytes).unwrap(),
            value
        );
    }
    #[test]
    fn rejects_bad_indices_without_display_panic() {
        assert_eq!(
            LocalNameReference::try_from_indices([BIP39_WORDS as u16, 1, 2]),
            Err(NameParseError::InvalidIndex(BIP39_WORDS as u16))
        );
    }

    #[test]
    fn decode_rejects_invalid_archived_indices() {
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(&RawLocalNameReference([
            BIP39_WORDS as u16,
            1,
            2,
        ]))
        .unwrap();
        assert_eq!(
            LocalNameReference::decode(&bytes),
            Err(NameDecodeError::InvalidIndex(BIP39_WORDS as u16))
        );
        assert_eq!(
            LocalNameReference::decode(&[0]),
            Err(NameDecodeError::InvalidArchive)
        );

        let cluster = rkyv::to_bytes::<rkyv::rancor::Error>(&RawClusterNameReference([
            1, 2, 3, 4, 5, BIP39_WORDS as u16,
        ]))
        .unwrap();
        assert_eq!(
            ClusterNameReference::decode(&cluster),
            Err(NameDecodeError::InvalidIndex(BIP39_WORDS as u16))
        );

        let public = rkyv::to_bytes::<rkyv::rancor::Error>(&RawPublicNameReference([
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, BIP39_WORDS as u16,
        ]))
        .unwrap();
        assert_eq!(
            PublicNameReference::decode(&public),
            Err(NameDecodeError::InvalidIndex(BIP39_WORDS as u16))
        );
    }
}
```

## examples/name_identifier.rs

SHA256 `ff385f41fa5c9eeea18fefa2b4cb2472e54822483711f05dc86c5f09716bdd9a`; 436 bytes.

```rust
use signal::NameDigest;
fn main() {
    let digest = NameDigest::of_bytes(b"signal identifier proof");
    println!("local={} ({} bits)", digest.local(), signal::LOCAL_BITS);
    println!(
        "cluster={} ({} bits)",
        digest.cluster(),
        signal::CLUSTER_BITS
    );
    println!("public={} ({} bits)", digest.public(), signal::PUBLIC_BITS);
    println!("digest={:02x?} (full, non-authenticating digest)", digest.0);
}
```

## build.rs

SHA256 `c8d7ba34532e9008ee735852170e5a270ed108f51835e0553d4bdd5b6c206eed`; 2336 bytes.

```rust
use ethos_zero::{Actualizing, File, Generating, Potential, TypeDeclaration};
fn main() {
    let root = std::path::PathBuf::from(std::env::var_os("CARGO_MANIFEST_DIR").expect("manifest"));
    println!("cargo:rerun-if-changed=ethos/signal.ethos");
    println!("cargo:rerun-if-changed=src/generated/signal.rs");
    let source = std::fs::read_to_string(root.join("ethos/signal.ethos")).expect("source");
    let file = Potential::<File>::from(source)
        .actualize()
        .unwrap_or_else(|_| panic!("read"));
    let generated = file.generate().unwrap_or_else(|_| panic!("generate"));
    assert_eq!(
        generated,
        std::fs::read_to_string(root.join("src/generated/signal.rs")).expect("generated")
    );

    // The identifier reference shapes are intentionally a separate Ethos
    // library, so they do not alter Signal's generated frame ABI. They still
    // must actualize whenever this crate is built; otherwise this claimed
    // schema authority could silently drift.
    println!("cargo:rerun-if-changed=ethos/identifiers.ethos");
    let identifiers = std::fs::read_to_string(root.join("ethos/identifiers.ethos"))
        .expect("identifier source");
    let identifiers = Potential::<File>::from(identifiers)
        .actualize()
        .unwrap_or_else(|_| panic!("read identifier schema"));
    let File::Library(library) = identifiers else {
        panic!("identifier schema must remain a library");
    };
    let expected = [
        ("LocalNameReference", 3),
        ("ClusterNameReference", 6),
        ("PublicNameReference", 12),
    ];
    assert_eq!(library.types.len(), expected.len(), "identifier type count");
    for (declaration, (name, width)) in library.types.iter().zip(expected) {
        let TypeDeclaration::Struct(identity, fields) = declaration else {
            panic!("identifier reference must remain a struct");
        };
        assert_eq!(identity.name.as_ref(), name, "identifier type name");
        assert!(identity.constraints.is_empty(), "identifier type constraints");
        assert_eq!(fields.len(), width, "identifier field count");
        assert!(fields.iter().all(|field| {
            field.source.is_none() && field.name.as_ref() == "Integer" && field.arguments.is_empty()
        }), "identifier fields must be unqualified Integer positions");
    }
}
```

## reports/identifier-poc.md

SHA256 `63483bfc0fbfb74115830e942ecab5b53264534ff4e73f0937212b159ce5bb55`; 2075 bytes.

```text
# Word identifiers proof

`ethos/identifiers.ethos` is a native sweet-form `Library` with imports, types, kinds, and associations sections. It declares the three fixed-width reference shapes and stays outside `ethos/signal.ethos`, so this proof does not alter Signal's frame ABI or generated taxonomy.

`src/identifiers.rs` provides rkyv-serializable nominal `NameDigest`, `LocalNameReference`, `ClusterNameReference`, and `PublicNameReference` types. None is a `String` internally. The full digest is BLAKE3 over input bytes; it is a correlation/deduplication digest and makes no authentication claim.

The chosen alphabet is BIP-39 English: its pinned crate supplies 2,048 CC0 English words, or 11 bits per word. BIP-39 mnemonic checksums are not used.

| Context | Words | Bits | Capacity |
|---|---:|---:|---:|
| Local/private | 3 | 33 | 2^33 |
| Cluster | 6 | 66 | 2^66 |
| Public | 12 | 132 | 2^132 |

The display form is lowerCamelCase BIP-39 words, such as `abandonAbilityAble`. Parsing accepts only ASCII alphabetic lowerCamelCase with BIP-39 English words and the exact context width. It rejects PascalCase, colon, dots, other punctuation, unknown words, invalid word indices, and noncanonical counts. The display is a short reference; the full 256-bit `NameDigest` is the explicit long form.

Pinned Datom and Protos provide text and integer intrinsics but no standard hash primitive. The Ethos library therefore models only the word-index references; the Signal-owned 32-byte BLAKE3 `NameDigest` is an explicit adapter outside that schema, without claiming a Datom standard or editing Datom.

Real `tiktoken 0.12.0` measurements of the running example's exact lowerCamelCase output: cl100k_base and o200k_base both count local (33 bits) as 3 tokens, cluster (66 bits) as 8 tokens, and public (132 bits) as 17 tokens. These are sample-string measurements, not a claim about the production Codex tokenizer.

`examples/name_identifier.rs` prints each form and full digest. Tests cover widths, display/parser round trips, invalid forms, and rkyv archive restoration.
```
