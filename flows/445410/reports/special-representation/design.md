# Special representation: the Represented trait

A type whose datom is another type's datom. The ethos-declared type is the
runtime Rust type; its Representation is the type its datom is written as;
two hand-written bodies convert between them. Lives in datom-codec, branch
`445410` (development, not in production).

## The trait

```rust
pub trait Represented {
    type Representation: Datomizable + Composing;
    fn represent(&self) -> Self::Representation;
    fn from_representation(
        representation: Self::Representation,
    ) -> Result<Self, ErrorKind>
    where
        Self: Sized;
}
```

`#[derive(Represented)]` gives the type `Datomizable` (the
representation's datom, at the same path) and `Composing` (compose the
representation, then `from_representation`; a refused `ErrorKind` becomes
a Composition `Error` at the path of the datom read). The two bodies are
the only hand-written part.

## The ethos form

Declared in `datom-codec-kinds.ethos`; the pinned ethos-zero generates the
trait above, signature for signature.

```
Represented.{ []
              [ Representation<Datomizable Composing> ]
              []
              [ represent.[ Representation ]
                from_representation:{ [ Composing ]
                                      [ Result<Self ErrorKind> ] } ] }
```

The input `Composing` resolves to `Self::Representation` because the
associated type is bound by that trait; the bounds are a plain list inside
the angles, not a bracket. Binding a declared type to its representation
in ethos (for example `Digest` with `Representation` = `String`) has no
generator form yet; today the binding is written in the Rust impl.

## Wrong and right forms

Wrong: the conversion hand-written into the datom kinds, one bespoke
impl per type, with the representation type nowhere stated.

```rust
impl Datomizable for Digest {
    fn datomize(&self, at: Path) -> Datom {
        Datom { path: at,
                form: Form::Bare(hex(&self.0)) }
    }
}
impl Composing for Digest { /* parse, path */ }
```

Right: the representation is named as a type, the datom kinds come from
the derive, and the bodies only convert.

```rust
#[derive(Represented)]
struct Digest([u8; 32]);

impl Represented for Digest {
    type Representation = String;
    fn represent(&self) -> String {
        /* 64 lowercase hex digits */
    }
    fn from_representation(hex: String)
        -> Result<Self, ErrorKind> {
        /* refuse Value { Digest, hex } */
    }
}
```

## Tests (`tests/represented.rs`, 9, all pass)

Round trips, representation differing from the Rust type:

- `a_digest_is_written_as_its_hex_string_and_read_back`: `[u8; 32]` as a
  bare 64-hex String, exact text, plus all-zero and all-0xff.
- `a_ticket_is_written_as_its_digit_words_and_read_back`: `u32` as
  `[ Seven Four Two ]`, `[ Zero ]`, up to `u32::MAX`.
- `represented_positions_round_trip_inside_a_derived_struct`: both inside
  a derived struct, from generated and from hand-written text.
- `a_represented_datom_is_the_datom_of_its_representation`: datom
  equality at a nested path.

Negative cases:

- `a_digest_that_names_no_thirty_two_bytes_is_refused_at_its_path`:
  62, 63 and 66 digits, uppercase, a non-hex digit.
- `a_digest_in_a_form_its_representation_refuses_is_refused_as_that_form`:
  a vector where the String is expected.
- `a_ticket_that_names_no_number_is_refused_at_its_path`: empty vector,
  leading Zero, u32 overflow.
- `a_ticket_word_that_is_no_digit_is_refused_by_the_representation`:
  unknown word at path `[1]`, a bare word where the vector is expected.
- `a_refusal_inside_a_struct_names_the_position_it_arose_at`: refusals
  at paths `[0]` and `[1]`.

## Open

- The binding of a declared type to its Representation has no ethos
  syntax; ethos-zero would need it to emit the impl skeleton and the
  derive.
- datom-codec's real traits stay hand-written in `src/core.rs`; the
  generated kinds file is checked byte for byte and compiled only in
  `tests/kinds.rs`. `Represented` follows that existing split.
- The test types are single-field tuple newtypes in Rust; the Rust form
  of an ethos new type is an open ruling.
- Naming: `Represented` (qualifier-named); "special representation" is
  the living's phrase.
- No version bump on the branch.

## Sources

- datom-codec branch `445410`, commits 4ac787 and 776cf4.
- `nix flake check github:LiGoldragon/datom-codec/776cf4…` on
  Prometheus: 10 checks, exit 0 (witnessed).
- /home/li/primary/flows/ebbe30/vision/ethos.md, comment D.
- /home/li/primary/flows/d5df1d/reports/ethos-audit.md, items 26, 27, 36.
- «The golden ethos», https://claude.ai/artifact/F5ymU4N6ma6Rwt8RmNw7Lm.
- Provenance receipt: unavailable.
