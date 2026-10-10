# Trait-First Development — research synthesis, 2026-08-11

Research directed by the psyche ("Do a trait-first development
research, finding people who argue everything should go through
traits", 2026-08-11T22:04+02:00, rustComponentArchitecture.md).
Subagent web research, Designer-condensed. Information layer — the
psyche rules what becomes skill and what becomes Intent.

## 1. Rust's own design already argues the thesis

- `std::fs::File` has no inherent I/O methods: reading and writing
  come entirely from implementing `Read` and `Write`. Traits are
  not supplementary; they are what makes the type functional.
- The Rust API Guidelines mandate types "eagerly implement all
  applicable, common traits" (Copy/Clone/Eq/Hash/Debug/Display/
  Default/From/TryFrom/AsRef/Send/Sync; FromIterator/Extend for
  collections; Error for errors). The orphan rule makes omission
  unfixable downstream — trait boundaries must be thought first.
- The dominant ecosystem pattern for adding behavior is the
  extension trait (`Itertools`, `StreamExt`, `AsyncReadExt`,
  `ServiceExt`): behavior flows through traits, not inherent
  methods.
- Sealed traits publish a concept while controlling who inhabits
  it — the answer to "this will only ever have one implementation".

## 2. Naming betrays the trait (the psyche's observation, grounded)

Rust's naming conventions are literally trait names:

| Method name | Latent trait |
|---|---|
| `to_string()` | `Display` (via `ToString`) |
| `parse()` | `FromStr` |
| `from_x()` / `try_from_x()` | `From<X>` / `TryFrom<X>` |
| `into_x()` | `Into<X>` |
| `as_x()` | `AsRef<X>` |
| `iter()` / `into_iter()` | `IntoIterator` |
| `default()` | `Default` |
| `collect()` | `FromIterator` |
| `serialize()`, `validate()`, `render()`, `compare()` | the verb is the trait |

An inherent method named `from_bytes()` is, by the guidelines' own
logic, a trait not yet extracted — "a trait in exile." Go proves
the same point from the other side: writing a method with the right
name and signature *is* implementing the interface, declared or
not — naming a method is declaring a concept membership. This is
the psyche's "they do conceptually, if not explicitely" as a
formal language rule.

## 3. The intellectual lineage

- Gang of Four (1994): "Program to an interface, not an
  implementation" — the first design principle of the book.
- Meyer, Design by Contract (Eiffel, 1986): the contract is the
  abstraction; implementations satisfy it.
- Alan Kay on Smalltalk: "The big idea is messaging" — the protocol
  is the interface; the object is whoever answers.
- ML modules/functors: signatures precede and constrain structures;
  implementations cannot violate invariants except through the
  signature.
- Dave Cheney / Go proverb: "Accept interfaces, return structs";
  `io.Reader`/`io.Writer` as single-method concepts composing into
  everything.
- The maximalist: John De Goes, "Principled Type Classes" (2014) —
  abstractions must be *lawful*: "If you cannot define laws for a
  type class, then it is not useful as an abstraction." The trait
  is not a method list but a set of guarantees.

## 4. Counterarguments (tradeoffs within the paradigm, not
## refutations)

- Premature abstraction: a trait before its second implementation
  may fix the wrong axis; community caution is "extract from
  observed commonality". (Sealed traits and concept-documentation
  value answer the single-impl case.)
- Compile time: monomorphization and trait solving degrade
  feedback loops on large trait-heavy codebases.
- Discoverability: extension traits need imports; behavior spread
  across impls resists grep; the method's home is not the type's
  file.
- Indirection: `dyn` dispatch costs in tight loops; even static
  dispatch splits reading across trait definition and impl.
- Orphan-rule friction: foreign-trait-on-foreign-type needs
  newtypes.

No prominent voice argues for fewer std traits; the live debate is
only when application code extracts them.

## 5. Resonances with standing rulings (Designer notes, marked)

- De Goes's lawful traits ↔ the witness culture: a trait's laws are
  exactly what round-trip witnesses test. "Traits with laws" gives
  the comprehension-through-traits intent its verification story.
- Go's implicit interfaces ↔ "function names often betray the
  trait": the detection heuristic is mechanical — a verb in a
  method name names its concept.
- Extension-trait ecosystem ↔ the shared-substrate ruling (traits
  with a shared implementation and types, protos repo).
