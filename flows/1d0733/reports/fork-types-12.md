# Types Forks 1 and 2: four candidates built

Build host: `hostname` returned `prometheus` for every cargo and nix run. Base: a clone of ethos-zero at b2fa8b0 with `item12-final-ethos-zero.patch` applied and committed locally as 9a016fb. Each candidate is a copy of it under `/tmp/fk12-<candidate>` on Prometheus. Nix runs used `--override-input protos path:/tmp/protos-item12b`, and Cargo resolved datom-codec through the set's pin to `/tmp/datom-codec-item12b` rev 296b25. Each patch below applies with `git apply --check` to 9a016fb. Nothing was pushed, and nothing in Primary was committed.

Each candidate was regenerated with the built binary: src/error.rs, src/ethos-zero.rs, every `fixtures/*.ethos` and the four `fixtures/print` Flow files. The hand-written variants in src/error.rs came out byte-equal to the regenerated file.

## Results

| Candidate | cargo test | Flake checks | Failing |
|---|---|---|---|
| 1a+2a | all pass: lib 21, cli 17, ethos 35, flow_contract 1, freshness 4, generated 22, print 9, signal_without_datom 2 | 7 of 8 | clippy |
| 1a | all pass: lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 22, print 9, signal_without_datom 2 | 7 of 8 | clippy |
| 1c+2a | all pass: lib 21, cli 17, ethos 35, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2 | 6 of 8 | clippy, dependency-ethos |
| 1c | all pass: lib 21, cli 17, ethos 34, flow_contract 1, freshness 4, generated 20, print 9, signal_without_datom 2 | 6 of 8 | clippy, dependency-ethos |

Flake checks were run with `nix flake check --keep-going`, then each attribute was built on its own: build, clippy, dependency-ethos, doc, fmt, no-free-functions, no-inherent-methods and test.

**The clippy failure is the same in all four:** `clippy::type_complexity` fails under `-D warnings` on the `Deep` type. Under 1a it fails on the `pub struct Deep(pub Vec<Vec<Vec<Option<Result<String, i64>>>>>)` position, at tests/generated/tree-types.rs:155. Under 1c it fails on the field in `Wrapped` that `Deep` was moved into, at tree-types.rs:130 and 132. An alias was exempt from this lint; a struct position is not. No fix was applied. The two possible fixes are an allow in the generated module header or a shallower fixture; neither was tested.

**The dependency-ethos failure (1c and 1c+2a):** datom-codec's own `datom-codec.ethos` declares `Path.Vector<Integer>`. The built tool refuses it with `Rejected.{ …/datom-codec.ethos { 10 3 } Conceptual.{ [ 1 1 0 ] WrapsContainer } }`. The check script stops at the first refusal, so datom-codec-kinds.ethos was not reached. For this check to pass under 1c, datom-codec.ethos must change too, which is outside an ethos-zero patch.

## 1a+2a: `fork-types-12-1a+2a.patch`

19 files, +240 / −67.

Matches:
- Every name over a Vector or an Option emits `#header pub struct Name(pub T);`. This covers LockPaths, Locks, Forest, Deep, Login, the two Optional names and Nested.
- `OptionalSpiritGuardianProviderName.Option<SpiritGuardianProviderName>` and `Locks.Vector<Lock>` are accepted, because the double-wrap check looks only at the held head.
- `DuplicateName.Lock` is refused as `[ 1 1 1 ] WrapsStructure`. `Job.FlowId` is refused as `[ 1 1 2 ] DoubleWrap`. `Never.[] Holder.Never` is refused as `[ 1 1 1 ] WrapsStructure`. `FlowId.String` generates.
- tree-types.rs has `Loop(#[rkyv(omit_bounds)] std::boxed::Box<Knot>)` and no `pub type Loop`. orchestrate.rs loses `DuplicateName`, and empty-signal.rs loses `Shared`.
- The changed fixtures are orchestrate, tree-types and empty-signal. The changed goldens are alias-format, empty-signal, flow-operation, orchestrate and tree-types.
- No `pub type` remains in any golden.

Mismatches:
- `Paths.LockPaths` is refused as `DoubleWrap`, but at `[ 1 1 3 ]`, not `[ 1 1 2 ]`. A held reference with arguments, `LockPaths.Vector<LockPath>`, takes two path slots.
- The generation alias branch cannot be deleted. A sourced reference still emits an alias: tests/ethos.rs `a_sourced_generic_in_a_data_position_reads_and_reprints` expects `pub type Record = external::Vector<String>;` and passes. The branch was kept.
- The test source `Leaf.String A.{ Leaf B } B.A` in `a_type_with_no_finite_value_is_refused` is now refused as `[ 1 1 2 ] WrapsStructure`, not `[ 1 1 1 0 ] Cycle("A")`. Its expectation was changed to that.
- clippy fails (see Results).

Implementation choices: the test at tests/ethos.rs:163 (operation-free Signal) keeps its purpose with `[ Name.String ]`, and the refusals sit in the new `a_name_over_a_declared_type_is_refused`. In the finiteness list, `Holder.Never` became `Holder.{ Never Integer }`, which generates.

Files: error.ethos, fixtures/container-new-type.ethos (new), fixtures/empty-signal.ethos, fixtures/orchestrate.ethos, fixtures/tree-types.ethos, src/checking.rs, src/error.rs, src/generation.rs, tests/ethos.rs, tests/flow_contract.rs, tests/freshness.rs, tests/generated.rs, tests/print.rs, and tests/generated/ alias-format, container-new-type (new), empty-signal, flow-operation, orchestrate and tree-types (.rs).

## 1a: `fork-types-12-1a.patch`

12 files, +175 / −47.

Matches:
- `pub struct LockPaths(pub std::vec::Vec<LockPath>);` is emitted with the header.
- `LockPaths(vec![LockPath("a"), LockPath("b")])` prints `[ a b ]` and reads back. This is witnessed by the new test `a_name_over_a_container_reads_as_the_container_in_datom`.
- Only generation changed: the `Plain` capability. Conception is unchanged.
- The changed goldens are exactly orchestrate, tree-types, flow-operation and alias-format. Every existing fixture is byte-equal.
- The changed tests are the ones predicted: the `Login` assertion, `Locks(vec![])` (in `Observation` as well as `ObserveSelection`), `Planted(Forest(vec![..]))`, the alias test (renamed `new_types_name_their_types`), and `login` in tests/generated.rs and tests/flow_contract.rs.
- `a_name_over_a_container_is_a_new_type` passes: the struct is emitted and parses with syn. `Opt.Option<String>` gives `pub struct Opt(pub std::option::Option<String>);`.
- `a_recursive_container_new_type_compiles` passes. `Node.{ String Children } Children.Vector<Node>` archives and restores through rkyv.

Mismatches:
- The `omit_bounds` inference was not needed. The generated `pub struct Children(pub std::vec::Vec<Node>);` has no attribute and compiles; only Node's `children` position carries `#[rkyv(omit_bounds)]`, as it does today.
- The recursion test needs a compiled module, so it adds fixture container-new-type.ethos. The fixture counts in tests/freshness.rs (18 to 19) and tests/print.rs (20 to 21) changed as a result.
- clippy fails (see Results).

Files: fixtures/container-new-type.ethos (new), src/generation.rs, tests/ethos.rs, tests/flow_contract.rs, tests/freshness.rs, tests/generated.rs, tests/print.rs, and tests/generated/ alias-format, container-new-type (new), flow-operation, orchestrate and tree-types (.rs).

## 1c+2a: `fork-types-12-1c+2a.patch`

17 files, +123 / −76.

Matches:
- `LockPaths.Vector<LockPath>` is refused as `[ 1 1 1 ] WrapsContainer`.
- The rewrite `Lock.{ LockPath Vector<LockPath> }` generates `pub lock_path_vector: std::vec::Vec<LockPath>`.
- The Capsule field becomes `pub string_vector: std::vec::Vec<String>`.
- The fixtures changed are the ones predicted: orchestrate, tree-types (`Planted.Vector<Tree>`, with Deep moved into `Wrapped`), print/flow-operation and alias-format, plus empty-signal under 2a.
- The goldens changed are the same four, plus empty-signal.
- tests/print.rs `Locks.Vector<Lock>` is unchanged and passes: print does not run the checks.
- Every 2a refusal matches, as in 1a+2a, and no `pub type` remains in any golden.

Mismatches:
- The spec's acceptance line says "Both blocks above, plus `Opt.Option<String>`, are refused at `[ 1 1 0 ]`". It contradicts the spec itself: the first block was predicted at `[ 1 1 1 ]`, and the second block is its accepted rewrite. Observed:
  - The first block is refused at `[ 1 1 1 ]`.
  - `Opt.Option<String>` is refused at `[ 1 1 0 ]`.
  - The rewrite is accepted.
  - The named position `Memory [] [ Flow.{ Integer Login.Vector<String> } ]` is refused at `[ 1 1 0 1 1 ]`.
- Unpredicted: in orchestrate.ethos, `ObserveSelection.[ Locks ]` named the declared `Locks`. With `Locks` gone it becomes a unit variant, `Locks,`, and tests/generated.rs now writes `ObserveSelection::Locks`.
- Unpredicted: the unit test `approved_declared_and_inline_payloads_generate_named_fields` in src/lib.rs used `SyntaxError.Vector<FilePath>`. It is rewritten as the variant `SyntaxError.Vector<FilePath>` and asserts `SyntaxError(std::vec::Vec<FilePath>)`.
- Under 1c+2a not every `Name.Type` emits a new type: a sourced reference is still an alias, as in 1a+2a.
- The `Cycle("A")` test changes to `[ 1 1 2 ] WrapsStructure`, as in 1a+2a.
- dependency-ethos and clippy fail (see Results).

Files: error.ethos, fixtures/alias-format.ethos, fixtures/empty-signal.ethos, fixtures/orchestrate.ethos, fixtures/print/flow-operation.ethos, fixtures/tree-types.ethos, src/checking.rs, src/error.rs, src/lib.rs, tests/ethos.rs, tests/flow_contract.rs, tests/generated.rs, and tests/generated/ alias-format, empty-signal, flow-operation, orchestrate and tree-types (.rs).

## 1c: `fork-types-12-1c.patch`

15 files, +80 / −58.

Matches:
- Everything that matches under 1c+2a for Fork 1 also matches here.
- The aliases over declared types remain as predicted: `pub type DuplicateName = Lock;`, `pub type Loop = Knot;` and `pub type Shared = Name;`.

Mismatches: the same Fork 1 mismatches as 1c+2a, namely the self-contradicting acceptance line, the unit variant `ObserveSelection::Locks`, the src/lib.rs unit test, dependency-ethos and clippy.

Files: error.ethos, fixtures/alias-format.ethos, fixtures/orchestrate.ethos, fixtures/print/flow-operation.ethos, fixtures/tree-types.ethos, src/checking.rs, src/error.rs, src/lib.rs, tests/ethos.rs, tests/flow_contract.rs, tests/generated.rs, and tests/generated/ alias-format, flow-operation, orchestrate and tree-types (.rs).

## How the refusals are built

All three refusals are checked by one capability, `Wrapping` on `Reference` in src/checking.rs. It runs in the `NewType` arm after the cycle check, so it covers both types-section declarations and named struct positions. A sourced reference is never refused. The new Problem variants follow `SinglePosition` in error.ethos, in the order WrapsContainer, WrapsStructure, DoubleWrap. Under 1a, the `Plain` capability in src/generation.rs accepts a Vector or an Option with arguments and no source.

Provenance receipt: unavailable.
