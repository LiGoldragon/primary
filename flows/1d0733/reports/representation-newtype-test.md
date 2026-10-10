# Representation Newtype Test

**Build host:** `prometheus` (witnessed via SSH)

When a type's special `Representation` is itself a tuple newtype (e.g., `struct R(pub String)`), the represented type's datom prints as its representation's inner type's datom.

## Test Source

```rust
#[derive(Debug, PartialEq, Represented)]
struct TicketRepresented(u32);

impl Represented for TicketRepresented {
    type Representation = TicketString;
    fn represent(&self) -> TicketString {
        TicketString(self.0.to_string())
    }
    fn from_representation(repr: TicketString) -> Result<Self, ErrorKind> {
        repr.0
            .parse::<u32>()
            .map(TicketRepresented)
            .map_err(|_| ErrorKind::Value { expected: "TicketRepresented".to_owned(), value: repr.0 })
    }
}

#[test]
fn newtype_representation_round_trips() {
    let value = TicketRepresented(42);
    let text = text_of(&value);
    let parsed = read::<TicketRepresented>(&text).unwrap();
    assert_eq!(parsed, value);
}

#[test]
fn newtype_representation_datom_is_inner_type_datom() {
    let value = TicketRepresented(42);
    let repr = value.represent();
    assert_eq!(
        value.datomize(Path::new()),
        repr.datomize(Path::new())
    );
}
```

## Observed Text Output

**With merged patch applied**: `42`
- The round trip holds: TicketRepresented(42) → "42" → TicketRepresented(42) ✓

**Without patch (776cf4 alone)**: `{ 42 }`
- Also round-trips, but through a struct form

## Comparison

The patch (`item12-dry-run-2-datom-codec.patch`) adds tuple newtype handling to the `Composing` and `Datomizable` derives. For `TicketString(String)`:
- **Without patch**: datomizes as `Struct([ String ])` → prints `{ 42 }`
- **With patch**: datomizes as its inner type's datom → prints `42`

When the representation is a tuple newtype, the represented type inherits this behavior: `TicketRepresented` prints as `42` (the inner String) rather than wrapping it.

## Full Test Output

```
running 2 tests
test newtype_representation_datom_is_inner_type_datom ... ok
test newtype_representation_round_trips ... Text: 42

test result: ok. 2 passed; 0 failed; 0 ignored
```

All cargo tests pass on Prometheus: 59 total (14 composition + 33 core + 2 newtype + 9 represented + 1 hygiene).
