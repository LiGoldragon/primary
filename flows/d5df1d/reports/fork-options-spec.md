# Fork options: dry-run specification

For 1d0733, to build on Prometheus as patches on top of the current set: ethos-zero b2fa8b0 plus `flows/1d0733/reports/item12-final-<repo>.patch` for protos, datom-codec and ethos-zero (report `item12-final.md`). Each option is one patch; the Combinations section says which must be built together.

Origins. The fork wording is quoted from `flows/d5df1d/books/types.md` (types Fork 1, Fork 2) and `flows/d5df1d/books/invariants.md` (Proposal 4, Fork 3). The baseline behaviour is 1d0733's witnesses: `item12-final.md`, `mutex-probe.md`, `types-book-tests.md`. The file, test and golden names below come from this flow's reading of ethos-zero b2fa8b0 with `item12-final-ethos-zero.patch` applied to a scratch copy (code read only, no build). Expected Rust and expected refusals are this flow's predictions. Each one becomes a witness only when 1d0733 runs it. **Inference** marks a choice that no book or record makes.

## What the set already does (read in the patch)

- `Name.Type` over String, Integer, Decimal or Boolean emits a tuple struct `pub struct Name(pub T);` with the standard header (below). The `Plain` kind in src/generation.rs decides this.
- A name over anything else (a container, a declared type) still emits `#[rustfmt::skip] pub type Name = T;`. These are the open cases for Forks 1 and 2.
- A struct of one position is refused: `Problem::SinglePosition`, for example at `[ 1 1 0 ]`.
- Double wrapping and a new type over a struct or enum are **not** refused. Ethos-solution item 2 names `DoubleWrap` and `WrapsStructure`, but the patch adds only `SinglePosition` to error.ethos.
- The datom derive treats every one-unnamed-field struct as its inner value, so `Name("abc123")` prints `abc123`.

The header is the exact text above every generated struct and enum. `// header` in the blocks below stands for it:

```rust
#[rustfmt::skip]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
```

The declarations that Forks 1 and 2 touch in the set's goldens. Container: orchestrate.rs `LockPaths`, `Locks`; tree-types.rs `Forest`, `Deep`; flow-operation.rs `Login` (declared inside a struct position); alias-format.rs `OptionalSpiritGuardianProviderName`, `OptionalSpiritGuardianMaximumOutputTokens`, `Nested`. Declared type: orchestrate.rs `DuplicateName = Lock` (a struct); tree-types.rs `Loop = Knot` (an enum); empty-signal.rs `Shared = Name` (a new type). Every other golden under tests/generated/ contains no `pub type`.

## Types Fork 1: a name over a container

The book asks: "**Fork 1. A name over a container.** `SyntaxError.Vector<FilePath>`, `LockPaths.Vector<LockPath>`. ... The same answer covers `Name.Option<T>`."

### Fork 1 (a): "a new type over the vector, `struct SyntaxError(Vec<FilePath>)`"

A name over `Vector<T>` or `Option<T>` emits a tuple struct with the standard header, the same way a plain value does. It prints and reads in datom as its inner value, because the derive is already in the set. Callers construct it as `LockPaths(vec![..])`. The vector methods are reached through `.0`.

```
Library
[]
[ LockPath.String
  LockPaths.Vector<LockPath> ]
[]
[]
```

```rust
// header
pub struct LockPaths(pub std::vec::Vec<LockPath>);
```

Datom: `LockPaths(vec![LockPath("a".into()), LockPath("b".into())])` prints `[ a b ]`, the same as the alias today. This is an inference from the derive code read and has not been run.

- Layer: generation. `Plain` widens to "plain, or a Vector or Option intrinsic with arguments and no source". Conception is unchanged. Changed goldens: tests/generated/orchestrate.rs, tree-types.rs, flow-operation.rs, alias-format.rs. Changed tests: tests/ethos.rs `a_named_position_declares_its_type_in_place` (the `pub type Login` assertion); tests/generated.rs (`Planted(Forest(vec![..]))`, `ObserveSelection::Locks(Locks(vec![]))`, `aliases_name_their_types`, `login: Login(vec![..])`); tests/flow_contract.rs:39 `login`.
- Byte-equal: every fixtures/*.ethos and fixtures/print/*.ethos source, and every other golden under tests/generated/. Acceptance: `a_name_over_a_container_is_a_new_type`. The block above generates the struct shown, `syn` parses it, and the datom round trip of `[ a b ]` succeeds. Also `a_recursive_container_new_type_compiles`: `Node.{ String Children } Children.Vector<Node>` must compile with rkyv. **Inference**: the new type's position may need `#[rkyv(omit_bounds)]` where it closes a cycle, as struct positions already do.
- Note: types Proposal 2 says "A new type holds a plain value". Option (a) contradicts that line, so (a) implies amending it. `Name.Result<..>`: **inference**, left as an alias. The book names only Vector and Option.

### Fork 1 (b): "it stays an alias"

This is the set as it stands: a name over a container keeps emitting `pub type`.

```rust
#[rustfmt::skip]
pub type LockPaths = std::vec::Vec<LockPath>;
```

Datom: `[ a b ]`, unchanged.

- Layer: none; the `Plain` documentation ("stays an alias until its ruling") is reworded to state the rule. Byte-equal: every fixture and golden. Acceptance: `a_name_over_a_container_stays_an_alias`. The block above generates exactly the alias line, and `.push` works on it.

### Fork 1 (c): "refused; the vector is written inline where it is used"

A types-section declaration (or a named struct position) whose held type is a Vector or Option is refused at its path. Every use writes the container inline, and the field is named after its type.

The block of 1 (a) is refused: `Conceptual.{ [ 1 1 1 ] WrapsContainer }`, Problem `WrapsContainer` with no Form. The name is **inference**, chosen to stand beside item 2's `WrapsStructure`; the path follows `SinglePosition`'s.

Accepted rewrite and its Rust:

```
Library
[]
[ LockPath.String
  Lock.{ LockPath Vector<LockPath> } ]
[]
[]
```

```rust
// header
pub struct Lock {
    pub lock_path: LockPath,
    pub lock_path_vector: std::vec::Vec<LockPath>,
}
```

The field name `lock_path_vector` is **inference**, by the same rule that gives today's `string_option_vector`.

- Layers: refusal (src/checking.rs, `TypeDeclaration::NewType` and the named-position path) and error.ethos (the new Problem). Generation loses its alias branch only if Fork 2 also removes it. Changed fixtures: orchestrate.ethos (`LockPaths` and `Locks` go inline; `Locks.Locks` becomes `Locks.Vector<Lock>`); tree-types.ethos (`Planted.Vector<Tree>`; **inference**: `Deep` moves into a `Wrapped` position); print/flow-operation.ethos (`Capsule.{ Home.String Vector<String> }`); alias-format.ethos (keeps `Short` and the two plain types).
- Changed goldens: the same four .rs files as (a). Changed tests: the same as (a), plus `string_vector` in place of `login`. tests/print.rs `a_reference_with_arguments_prints_as_it_was_written` holds `Locks.Vector<Lock>`; it changes only if `actualize` runs the checks, which the dry run observes.
- Byte-equal: all other fixtures and goldens. Acceptance: `a_name_over_a_container_is_refused`. Both blocks above, plus `Opt.Option<String>`, are refused at `[ 1 1 0 ]`.

## Types Fork 2: a name over a declared type

The book asks: "**Fork 2. A name over a declared type.** `DuplicateName.Lock` in a types section, which Ethos Zero emits today as `type DuplicateName = Lock`."

### Fork 2 (a): "Ethos Zero refuses it as an error"

A declaration whose held type names a type declared in the file is refused at its path. This brings in the refusals of item 2 and invariants Proposal 2: over a struct or enum, `WrapsStructure`; over a new type, `DoubleWrap`.

```
Library
[]
[ Lock.{ String Integer }
  DuplicateName.Lock
  FlowId.String
  Job.FlowId ]
[]
[]
```

Refused: `Conceptual.{ [ 1 1 1 ] WrapsStructure }`. With `DuplicateName.Lock` removed, the refusal is `Conceptual.{ [ 1 1 2 ] DoubleWrap }` for `Job`. The names come from ethos-solution item 2 and are the design's own; the paths are **inference**, by analogy with `SinglePosition`.

- Layer: refusal (src/checking.rs `NewType` arm; it looks up the held reference among the file's declarations) and error.ethos. Changed fixtures: orchestrate.ethos (line 14 `DuplicateName.Lock` deleted; the variant `LockRejection.[ DuplicateName.Lock .. ]` stays); tree-types.ethos (`Loop.Knot` deleted, Knot becomes `Knot.[ End Loop.Knot ]`); empty-signal.ethos (`Signal [] [] [] [ Name.String ]`).
- Changed goldens: orchestrate.rs (loses `pub type DuplicateName = Lock;`), tree-types.rs, empty-signal.rs. Expected in tree-types.rs: `Loop(#[rkyv(omit_bounds)] std::boxed::Box<Knot>)` and no `pub type Loop`. This is **inference**: the box closes the by-value cycle. Changed tests: tests/ethos.rs line 163 becomes a refusal test, and the finiteness source `Holder.Never` becomes refused. tests/generated.rs lines 226-234 use `Name` in place of `Shared`. The dry run lists any other test source that names a declared type.
- Byte-equal: every other fixture and golden. Acceptance: `a_name_over_a_declared_type_is_refused`. The block above is refused twice, as stated, and `FlowId.String` alone generates.

### Fork 2 (b): "it stays an alias for this case only"

`DuplicateName.Lock` keeps emitting `#[rustfmt::skip] pub type DuplicateName = Lock;`, as the set does now. **Inference**: "this case" is read as any name over a declared struct, enum or new type, so `Shared.Name` and `Loop.Knot` also stay aliases. An alias is not a wrap, so invariants Proposal 2 does not refuse it.

- Layer: none. Byte-equal: every fixture and golden. Acceptance: `a_name_over_a_declared_type_stays_an_alias`. It holds tests/ethos.rs:163 (`pub type Shared = Name;`) and checks `pub type DuplicateName = Lock;` in orchestrate.rs.

## Invariants Proposal 4: each element on a new indented line

This is a proposal, not a fork; its rulings are "land, amend, or refuse". Only "land" can be dry-run. "Refuse" is the set unchanged.

### Proposal 4, land

Every structure with an element that has a next layer opens its delimiter and ends the line there. Each element starts on its own line, indented two columns beneath the line that opened it, and the closer ends the last element's line. The root head and the sections stay at column 0, as src/printing.rs places them.

```
Library [] [ Voice.{ Aspect.[ Psyche Mind Field ]
  Topic.String } ] [] []
```

The print, without comments because Proposal 3 is not built:

```
Library
[]
[
  Voice.{
    Aspect.[
      Psyche
      Mind
      Field ]
    Topic.String } ]
[]
[]
```

Three points are **inference**, read from the book's Voice block: the types section breaks though it holds one element; an enum's leaves each take their own line; angle arguments stay tight, as today.

Datom print: unchanged. The layout must not land in protos's shared `Textualizable`. If it did, datom text such as `{ 3 19 }` (datom-codec `tests/composition.rs`) would break. So it is built in ethos-zero src/printing.rs, which today hands each section to protos. This placement is **inference**. It also strains vision-ethos's sentence "Ethos follows the canonical protos print".

- Layer: print (ethos-zero only; protos and datom-codec are byte-equal). Changed goldens: fixtures/print/flow-library, flow-signal, flow-operation and flow-memory (.ethos), rewritten to the new layout. ethos-zero.ethos and error.ethos are rewritten too, because `the_crates_own_ethos_is_written_in_the_canonical_print` compares them. tests/print.rs literals change in `a_one_line_layout_expands_to_the_canonical_print`, `leaves_stay_on_one_line_and_angles_stay_tight`, `a_capability_hangs_its_inputs_and_yield`, `a_badly_hung_layout_is_realigned` and `a_reference_with_arguments_prints_as_it_was_written`. Byte-equal: fixtures/*.ethos (they are only round-tripped, never compared to the print) and every tests/generated/*.rs. Acceptance: `each_element_starts_on_a_new_indented_line`. The one-line source prints exactly as above. Print of print equals print for all 20 sources in `every_fixture_prints_...`.

## Invariants Fork 3: a Mutex field in ethos

The book asks: "### Fork 3: a Mutex field in ethos ... Options: (a) ethos expresses a Mutex field ...; (b) shared mutable state stays outside ethos ...; (c) another form."

### Fork 3 (a): "imports of more than one segment, and a declaration that carries fewer derives"

The import half can be dry-run. **Inference**: the syntax is a chain of colon heads, `std:sync:Mutex`. The protos lexer already parses it, since probe c1 reached `[ 1 0 0 1 ]`, and `Source::try_from` already accepts `std::sync`. So conception folds the chain into one Source, and grammar is unchanged.

```
Library
[ std:sync:Mutex ]
[ Flow.String
  Nexus.{ Mutex<Vector<Flow>> Integer } ]
[]
[]
```

```rust
// header
pub struct Nexus {
    pub flow_vector_mutex: std::sync::Mutex<std::vec::Vec<Flow>>,
    pub integer: i64,
}
```

The field name is **inference**, by the probe's `string_mutex`. With the full header the code does not compile; that is probe V2's error set and is expected. The derive half has no form in the book (see Not an option here). If the declaration were marked, its expected header would be `#[derive(Debug)]` alone, with no datom kinds; this too is **inference**.

- Layer: conception (`Conceiving<Import>`, the chain fold). Changed goldens: none; this adds a fixture. Byte-equal: all.
- Acceptance: `a_multi_segment_import_reaches_its_path`. The block above generates `std::sync::Mutex<std::vec::Vec<Flow>>`, and rustc on it reports E0277/E0369 and no E0425.

### Fork 3 (b): "shared mutable state stays outside ethos, in hand-written Rust, and implementers report each case under Proposal 5"

The generator is unchanged. The probe's refusal is pinned:

```
Library
[ std::sync:Mutex ]
[ Holder.{ Mutex<String> Integer } ]
[]
[]
```

Refused: `Conceptual.{ [ 1 0 0 ] Expected.Import }` (Problem `Expected`, Form `Import`), as probe a1 observed.

- Layer: none. Byte-equal: all. Acceptance: `a_multi_segment_import_is_refused`.

### Fork 3 (c): "another form"

This option has no content and cannot be dry-run.

## Combinations

Fork 1 (b) and Fork 2 (b) change nothing, so six pairs reduce to four built sets: {1a+2a}, {1a}, {1c+2a}, {1c}. Pairs with (b) are {2a} alone and the baseline. Both Forks change orchestrate.rs, tree-types.rs and their tests, so each pair below is built as one patch, not two stacked ones.

The example source for every pair:

```
Library
[]
[ LockPath.String
  LockPaths.Vector<LockPath>
  Paths.LockPaths ]
[]
[]
```

- **1a × 2a.** `LockPaths` is a container new type over a declared new type. It is accepted under the reading that the double-wrap rule looks only at the held head, which is Vector. That reading is **inference**. `Paths.LockPaths` is refused with `Conceptual.{ [ 1 1 2 ] DoubleWrap }`. The same reading accepts the set's `OptionalSpiritGuardianProviderName.Option<SpiritGuardianProviderName>` and `Locks.Vector<Lock>`. In this pair no `pub type` remains anywhere, and the generation alias branch is deleted.
- **1a × 2b.** `LockPaths` is a struct. `Paths.LockPaths` emits `pub type Paths = LockPaths;`.
- **1b × 2a.** `LockPaths` is an alias. `Paths.LockPaths` names a declared alias and is refused. **Inference**: it is refused as `DoubleWrap`. Aliases remain only over containers.
- **1b × 2b.** The baseline: `pub type Paths = LockPaths;`.
- **1c × 2a, 1c × 2b.** `LockPaths` is refused with `WrapsContainer` at `[ 1 1 1 ]`, so `Paths.LockPaths` never arises. Fork 2 then acts alone. Under 1c × 2a every `Name.Type` declaration is a plain new type.

Independence:
- Proposal 4 touches only the print and is independent of Forks 1, 2 and 3. Its one overlap is textual: fixtures/print/flow-operation.ethos is rewritten by Proposal 4 and by 1c. Rebase, do not merge by hand. Proposal 4's comment sentence ("A comment sits beside the element ... lined up") needs Proposal 3 (comments kept), which is outside this spec. With Proposal 3 built too, the expected print is the book's Voice block byte for byte.
- Fork 3 is independent of the rest. It touches imports and the derive set, not declarations over containers or declared types.

## Not an option here

These are left to the living or to a design ruling and cannot be dry-run:
- Fork 3 (a) "a declaration that carries fewer derives": no form is given. Fork 3 (c) "another form". Proposal 4 amend.
- Proposal 4 "A vector of short items may hold several on a line up to a width": no width is given, and the book does not say which brackets count. Its own Voice example breaks `[ Psyche Mind Field ]`.
- Whether the double-wrap rule looks through a container (1a × 2a above); whether `Name.Result<..>` follows Fork 1; whether Fork 2 (b) "this case only" covers a name over a new type or an enum as well as over a struct.
- The refusal names `WrapsContainer`, `WrapsStructure` and `DoubleWrap`: the books give no message text.
- Types Fork 3 (bare or braced datom), on which every datom print above rests; the set already builds the bare answer. Types Fork 4 (`pub` inner), on which every `(pub T)` above rests.

Provenance receipt: unavailable.

