# 393 — Schema-implied capabilities: operator feedback

## Read

The psyche's latest design point is that many method bodies should not be invented from
scratch. A schema noun already implies a set of standard operations by its shape: a newtype
has payload access; a record has fields; an enum has constructors; a stream has open/event
/close positions; a family has key/address behavior; a signal root has routing and codec
behavior. Those operations can become the built-in methods of the schema data language.

I tried the required Spirit gap-check for recent records, but the deployed CLI returned
connection refused. I did not write any new record.

## Verdict

This is sound, and it is the right way to prevent "code-is-data" from turning into a vague
general programming language too early.

The name I would use for the mechanism is **schema-implied capabilities**. A schema object
does not merely declare storage shape; it declares the capabilities that shape makes valid.
The expression language can then compose those capabilities:

- newtype shape implies `payload`, `reference payload`, `into payload`, and `Deref` when the
  target is unambiguous;
- struct shape implies field projection and, where owned values are available, field update;
- enum shape implies variant constructors and variant predicates / destructuring;
- vector/optional/map shapes imply iteration, wrap/unwrap, presence checks, and conversion
  families;
- signal roots imply route-preserving constructors, payload access, `From` lifts, and
  codec/framing implementations;
- stream/family declarations imply table/key/slot accessors and canonical generated impls.

That gives the method-body language a small safe base: not "any Rust method call by name,"
but "compose capabilities proven by the schema type."

## Design constraint

The compiler should not treat these as magic strings like `deref` or `field`. It should
resolve a typed expression against a typed capability registry:

- expression node says what operation is requested;
- receiver type is known;
- schema-derived capability set proves whether that operation exists;
- codegen emits the Rust method/operator for the resolved capability.

So `(reference (field self payload))` should lower because:

- `self` has type `EntryHandle`;
- `EntryHandle` is a newtype with a payload field;
- `field payload` is a valid projection capability;
- `reference` is valid on that lvalue projection;
- `Deref EntryHandle` expects `&Target`.

That is stronger than textual codegen and still much smaller than a full language.

## Landing implication

This changes the recommended slice slightly. The next mergeable slice should not just harden
`Deref`; it should introduce the first **capability registry** with one or two concrete
capability families:

1. Newtype payload projection.
2. Reference-of-projection.
3. Marker impl emission.
4. `Deref` as the first mechanical impl that composes 1 and 2.

Everything unsupported returns a typed `SchemaError`, not a panic/assert. Then later slices
add struct field projection, enum constructors, conversions, and frame routing.

## Risk

The main risk is over-expanding "built-in methods" into arbitrary Rust method lookup. That
would recreate a compiler hidden in codegen. The safe boundary is: built-ins are schema
capabilities derived from object shape, and every expression is typed against those
capabilities before Rust is emitted.

## Operator call

Green-light the direction. I would implement it as capability-directed expression lowering,
not as a bag of named helper methods. The Designer 660 proof already demonstrates the first
capability composition accidentally; this names it and makes it the next hardening target.
