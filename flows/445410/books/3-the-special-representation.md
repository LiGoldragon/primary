Presentation.{ «The special representation» }

# The special representation

Some types are written in datom as a different type than they are in Rust. A 32-byte hash is written as 64 hex digits, a string. A number is written as digit words, a vector. The ethos file declares the real Rust type; the datom is the datom of another type, its representation type. Two hand-written bodies convert between them. This is built in datom-codec on development branch 445410, not in production.

## What the trait is

`Represented` names the representation type and holds the two conversions. A derive gives the type its datom kinds from them.

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

The derive writes the type's datom as its representation's datom, at the same path. Reading composes the representation, then converts; a refusal becomes a composition error at the path of the datom read.

## The ethos form

```ethos
Represented.{
  []
  [ Representation<Datomizable Composing> ]
  []
  [ represent.[ Representation ]
    from_representation:{
      [ Composing ]
      [ Result<Self ErrorKind> ] } ] }
```

## Wrong and right

Wrong: a bespoke datom impl per type, the representation type nowhere stated.

```rust
impl Datomizable for Digest {
    fn datomize(&self, at: Path) -> Datom {
        Datom { path: at,
                form: Form::Bare(hex(&self.0)) }
    }
}
impl Composing for Digest { /* ... */ }
```

Right: the representation is a named type, the kinds come from the derive, the bodies only convert.

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

## The tests

Nine tests, and the whole flake check passed on Prometheus: 10 checks.

- A hash is written as its hex string and read back, including all-zero and all-0xff. An integer is written as digit words, `[ Seven Four Two ]`, and read back, from `[ Zero ]` up to the largest value.
- Both also round-trip inside a derived struct, and the datom equals the representation's datom.
- Negative: a hash of 62, 63 or 66 digits, uppercase, or a non-hex digit is refused at its path. A vector where the string is expected is refused as that form.
- Negative: an empty vector, a leading Zero, or an overflow is refused at its path. An unknown word is refused at its position, and so is a bare word where the vector is expected.

## Open points

- Ethos cannot yet bind a type to its representation type. That binding would fix the input and output types of the two conversions. Today it is written in the Rust impl.
- The name `Represented` is offered for his word.
- The test wrappers are single-field structs, pending the ruling on the Rust form of an ethos new type.

## Proposal 1: Special representation

Target: `psyche-skills/skills/vision-ethos.md`

New section, shown whole. Source: `flows/445410/vision/ethos.md`, 2026-10-09.

```
## Special representation

A type whose datom representation differs from its Rust type has a special representation: ethos describes the real Rust type and names its representation type, and Rust implements the conversion between them.
```
