# Types Forks 1 and 2: four candidates built

Build host: `hostname` returned `prometheus` for every cargo and nix run.

Each candidate is one patch on ethos-zero 9a016fb. That commit is b2fa8b0 with `item12-final-ethos-zero.patch` applied, committed only in a scratch clone. The scratch copies are `/tmp/fk12-<candidate>`.

The candidates were built with d5df1d's rulings and compared with the 299-line `fork-options-spec.md`.

Every patch applies with `git apply --check` and is byte-equal to the tree that was checked. Nothing was pushed, and nothing in Primary was committed.

Inputs:
- protos: `--override-input protos path:/tmp/protos-item12b` (the set's protos patch).
- datom-codec, Cargo: the set's pin, `/tmp/datom-codec-item12b` rev 296b25.
- datom-codec, flake (1c candidates only): `--override-input datom-codec path:/tmp/fk12-datom-codec`. This scratch is 296b25 plus `fork-types-12-1c-datom-codec.patch`.

Every committed module was regenerated with the built binary: src/error.rs, src/ethos-zero.rs, every fixture and the four Flow print files.

## Results

| Candidate | cargo test | Flake checks |
|---|---|---|
| 1a+2a | all pass: lib 21, cli 17, ethos 35, flow_contract 1, freshness 4, generated 22, print 9, signal_without_datom 2 | 8 of 8 |
| 1a | all pass: lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 22, print 9, signal_without_datom 2 | 8 of 8 |
| 1c+2a | all pass: lib 21, cli 17, ethos 35, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2 | 8 of 8 |
| 1c | all pass: lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2 | 8 of 8 |

The eight checks are build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods and test. `nix flake check --keep-going` exited 0 for each candidate, and each attribute was then built on its own and passed.

The scratch datom-codec's own `nix flake check` printed "all checks passed!" with its pinned ethos-zero.

## Shared by all four

- **Module head.** Generated code begins with `#![allow(dead_code, non_camel_case_types, non_snake_case, clippy::type_complexity)]`. The emission in src/generation.rs changed, and so did the expected text in tests/ethos.rs.
  - Every golden is regenerated, including src/error.rs and src/ethos-zero.rs. That is why each patch touches every file under tests/generated/.
  - The `Deep` fixture is kept: as a new type under 1a, and as an inline `Wrapped` position under 1c. It passes clippy with the allow.
- **Refusals.** One capability, `Wrapping` on `Reference` in src/checking.rs, refuses what a new type may not hold.
  - It runs in the `NewType` arm after the cycle check, so it covers both types-section declarations and named struct positions.
  - A sourced reference is never refused.
  - The new Problem variants follow `SinglePosition` in error.ethos, in the order WrapsContainer, WrapsStructure, DoubleWrap.

## Paths

The observed paths stand:
- `Paths.LockPaths` under 1a+2a: `[ 1 1 3 ] DoubleWrap`. A held reference with arguments takes two path slots.
- `LockPaths.Vector<LockPath>` under 1c: `[ 1 1 1 ] WrapsContainer`.
- `Opt.Option<String>` under 1c: `[ 1 1 0 ] WrapsContainer`.

Also observed:
- `DuplicateName.Lock`: `[ 1 1 1 ] WrapsStructure`.
- `Never.[] Holder.Never`: `[ 1 1 1 ] WrapsStructure`.
- The named position `Memory [] [ Flow.{ Integer Login.Vector<String> } ]`: `[ 1 1 0 1 1 ] WrapsContainer`.

## 1a+2a: `fork-types-12-1a+2a.patch`

37 files, +372 / −111.

**Matches**
- Every name over a Vector or an Option emits `// header` followed by `pub struct Name(pub T);`. This covers LockPaths, Locks, Forest, Deep, Login, the two Optional names and Nested.
- The double-wrap check looks only at the held head. So `Locks.Vector<Lock>` and `OptionalSpiritGuardianProviderName.Option<..>` are accepted.
- `Paths.LockPaths` is refused at `[ 1 1 3 ]`.
- `DuplicateName.Lock` is refused at `[ 1 1 1 ] WrapsStructure`.
- `Holder.Never` is refused, and `FlowId.String` generates.
- tree-types.rs has `Loop(#[rkyv(omit_bounds)] std::boxed::Box<Knot>)` and no `pub type Loop`.
- The 2a changes to fixtures orchestrate, tree-types and empty-signal match, as do their goldens. tests/generated.rs uses `Name` in place of `Shared`.
- **Inference (the design's):** a sourced reference with arguments is a container like any other. `Record.external:Vector<String>` emits `pub struct Record(pub external::Vector<String>);`, which tests/ethos.rs now asserts.
- The generation alias branch is deleted: `NewType` always emits the struct, and the `Plain` capability is gone. No `pub type` remains in any golden.

**Mismatches with the 299-line spec**
- The spec gives `Job.FlowId` (with `DuplicateName.Lock` removed) as `[ 1 1 3 ] DoubleWrap`. Observed: `[ 1 1 2 ]`. Only `Paths.LockPaths`, whose sibling has arguments, lands at `[ 1 1 3 ]`.
- The spec says tests/ethos.rs line 163 becomes a refusal test. Instead, that operation-free Signal test keeps its purpose with `[ Name.String ]` and asserts `pub struct Name(pub String);`. The refusals sit in `a_name_over_a_declared_type_is_refused`.
- `Name.Result<..>` is now a struct, not an alias, because the branch is deleted. The spec's Fork 1a section still says "left as an alias".

**Accepted consequences**
- The Cycle refusal changes. In `a_type_with_no_finite_value_is_refused`, the source `Leaf.String A.{ Leaf B } B.A` is now refused as `[ 1 1 2 ] WrapsStructure`, not `[ 1 1 1 0 ] Cycle("A")`.
- In the finiteness list, `Holder.Never` became `Holder.{ Never Integer }`, which generates.
- A new recursion fixture is added: fixtures/container-new-type.ethos, `Node.{ String Children } Children.Vector<Node>`, with its golden.
  - `a_recursive_container_new_type_compiles` passes with an rkyv round trip.
  - `pub struct Children(pub std::vec::Vec<Node>);` needs no `omit_bounds`.
  - The fixture counts move: tests/freshness.rs from 18 to 19, and tests/print.rs from 20 to 21.

**Files:** error.ethos; fixtures container-new-type (new), empty-signal, orchestrate, tree-types (.ethos); src checking, error, ethos-zero, generation (.rs); tests ethos, flow_contract, freshness, generated, print (.rs); all 23 files under tests/generated/.

## 1a: `fork-types-12-1a.patch`

32 files, +320 / −85.

**Matches**
- `pub struct LockPaths(pub std::vec::Vec<LockPath>);` is emitted with the header.
- `[ a b ]` prints and reads back. This is witnessed by `a_name_over_a_container_reads_as_the_container_in_datom`.
- Only generation changed; conception is unchanged.
- The fixtures that existed are byte-equal.
- The predicted test changes match: the `Login` assertion, `Locks(Locks(vec![]))`, `Planted(Forest(vec![..]))`, the alias test (renamed `new_types_name_their_types`), and `login` in tests/generated.rs and tests/flow_contract.rs.
- `a_name_over_a_container_is_a_new_type` passes, and the output parses with syn.
- `Record.external:Vector<String>` emits `pub struct Record(pub external::Vector<String>);`.
- For the combination example, 1a × 2b: `Paths.LockPaths` emits `pub type Paths = LockPaths;`. This was observed with the built binary.

**Mismatches with the 299-line spec**
- The Fork 1a section says "No `pub type` remains under 1a". The 1a × 2b combination, and Fork 2 (b), keep names over declared types as aliases.
  - This candidate follows Fork 2 (b). The alias branch stays only for a held reference that resolves to a type declared in the file, through a new `Aliasing` capability.
  - So `pub type DuplicateName = Lock;`, `pub type Loop = Knot;` and `pub type Shared = Name;` remain.
  - Every other name, including sourced, imported and `Result` names, emits a struct.
- The `omit_bounds` inference was not needed on the new type.

**Accepted consequences**
- The new recursion fixture and the two count changes, as in 1a+2a.

**Files:** fixtures/container-new-type.ethos (new); src error, ethos-zero, generation (.rs); tests ethos, flow_contract, freshness, generated, print (.rs); all 23 files under tests/generated/.

## 1c+2a: `fork-types-12-1c+2a.patch`, with `fork-types-12-1c-datom-codec.patch`

ethos-zero: 36 files, +261 / −102.

**Choosing 1c changes datom-codec.** Its datom-codec.ethos has `Path.Vector<Integer>`, which 1c refuses at `{ 10 3 }` as `[ 1 1 0 ] WrapsContainer`. The rewrite to the inline-field form deletes `Path.Vector<Integer>` and turns `Datom.{ Path Form }` into `Datom.{ Vector<Integer> Form }`. With that, dependency-ethos passes. The patch is `fork-types-12-1c-datom-codec.patch`: 1 file, against datom-codec 296b25, which is 4dff16b plus `item12-final-datom-codec.patch`.

**Matches**
- The refusal paths are as listed under Paths.
- The rewrite `Lock.{ LockPath Vector<LockPath> }` generates `pub lock_path_vector: std::vec::Vec<LockPath>`, and Capsule's field becomes `pub string_vector: std::vec::Vec<String>`.
- The fixture changes to orchestrate, tree-types (`Planted.Vector<Tree>`) and print/flow-operation match. The four goldens match, plus empty-signal from 2a.
- tests/print.rs still holds `Locks.Vector<Lock>` and passes: print does not run the checks.
- Every 2a refusal matches as in 1a+2a, and no `pub type` remains in any golden.

**Mismatches with the 299-line spec**
- The spec's 1c fixture list omits two fixtures that 1c forces:
  - alias-format.ethos: its two Optional names and Nested are removed.
  - tree-types.ethos: `Deep` is moved into a `Wrapped` position, as `string_integer_result_option_vector_vector_vector`.
- The alias branch stays. Under 1c a sourced reference is not refused, so `Record.external:Vector<String>` still emits `pub type`. The spec's "every `Name.Type` declaration is a plain new type" holds for the goldens, not for sourced references.
- `Job.FlowId` lands at `[ 1 1 2 ]`, not `[ 1 1 3 ]`, as in 1a+2a.

**Accepted consequences**
- The unit variant: `ObserveSelection.[ Locks ]` named the declared `Locks`, so it becomes the unit variant `Locks,`. tests/generated.rs writes `ObserveSelection::Locks`.
- The rewritten lib.rs test: the unit test in src/lib.rs, `approved_declared_and_inline_payloads_generate_named_fields`, now writes the variant `SyntaxError.Vector<FilePath>` and asserts `SyntaxError(std::vec::Vec<FilePath>)`.
- The Cycle refusal change from 2a, as in 1a+2a.

**Files:** error.ethos; fixtures alias-format, empty-signal, orchestrate, print/flow-operation, tree-types (.ethos); src checking, error, ethos-zero, generation, lib (.rs); tests ethos, flow_contract, generated (.rs); all 22 existing files under tests/generated/. In datom-codec: datom-codec.ethos.

## 1c: `fork-types-12-1c.patch`, with `fork-types-12-1c-datom-codec.patch`

ethos-zero: 35 files, +218 / −84. The datom-codec change and its patch are the same as for 1c+2a.

**Matches**
- The Fork 1 matches of 1c+2a.
- The aliases over declared types remain: `pub type DuplicateName = Lock;`, `pub type Loop = Knot;` and `pub type Shared = Name;`.

**Mismatches:** the Fork 1 mismatches of 1c+2a.

**Accepted consequences:** the unit variant and the rewritten lib.rs test.

**Files:** error.ethos; fixtures alias-format, orchestrate, print/flow-operation, tree-types (.ethos); src checking, error, ethos-zero, generation, lib (.rs); tests ethos, flow_contract, generated (.rs); all 22 existing files under tests/generated/. In datom-codec: datom-codec.ethos.

Provenance receipt: unavailable.
