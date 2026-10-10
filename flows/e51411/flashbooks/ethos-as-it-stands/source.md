# Ethos As It Stands

Made 2026-09-25 from flows/e51411/reports/ethos-audit.md, with whole programs taken out of the picture: no function bodies, no implementations, no manifest. Ethos is judged here as the data-description language it is meant to be today. The audit read ethos-zero 10.0.0. Three of its fixes have landed since; the tool is now ethos-zero 12.0.0 (origin/main 89a1ee8), and the probes marked "rerun" were run again against a build of that revision.

## Page 1 · The verdict

> I want you to reconsider if we exclude expanding ethos to do implementations (i.e., functions), which is all we would have, really. We would have implementations on objects, which are kinds actually. If we take that out then what is the state of ethos without that in the picture?

-- psyche, STT, 2026-09-25, to e51411 (flows/e51411/vision/ethos.md).

On that scope, Ethos is **a sound core with a narrow vocabulary and loose edges.**

- **Excellent:** types, kinds' signatures, and the Library/Signal/Sema roots turn into exact, fully qualified Rust with datom derives, typed refusals, and freshness tests that bind the 46 repos using ethos-zero.
- **Broken:** a variant can change meaning at a distance; errors name a protos path, not a line; the skills write a `Type` root the tool refuses; a contract can import a name that does not exist.
- **Missing:** sized integers, bytes, value rules, doc comments, a real newtype, and anything Sema needs to evolve.

## Page 2 · The shape of a Library

A Library has **four** sections, in this order (ethos-zero src/lib.rs, conception.rs):

```
Library  [ imports ] [ types ] [ kinds ] [ associations ]
Signal   [ imports ] [ queries ] [ responses ] [ types ]
Sema     [ imports ] [ record types ]
```

*Correction:* the kinds section is real. It holds kinds' signatures and is filled in the kinds files (datom-codec-kinds.ethos, protos-kinds.ethos). An ordinary file fills types, often imports, and writes `[] []` for the rest; `associations` is empty in every real file.

**Meaning comes from position.** Whether `[ … ]` is an enum, a vector or a section depends only on where it sits, and `.` means three things.

**The skills' `Type` root is refused** (rerun): `Conceptual.{ [] Root }`. Five root vocabularies are in use across the estate, and tree-sitter-ethos describes an older one.

## Page 3 · What is broken in the tool

Rerun against 12.0.0:

- **A variant that changes meaning at a distance.** `Sel.[ Locks ]` is a unit variant until a type `Locks` is declared anywhere; then it is `Locks(Locks)`. Still so.
- **Errors without a place.** An undeclared name answers `Conceptual.{ [ 1 1 0 1 1 ] Undeclared.Undeclared }`: a protos path, no line or column. There is no `Check` query; validation happens only by generating.
- **Docs out of step.** Vision/ethos.md still names the derive `Compositional`; it is `Composing` (the ethos and datom skills were corrected in Curriculum 02a3770). The README still says `Name.{ T1 T2 }` is a tuple variant.

Fixed since the audit:

- **Three `X_Data` items from one file** (fix 5): derived names are now unique across the file (`P_X_Data`, `Q_X_Data`).
- **Holes** (fix 6): all 17 fixtures compile; `Option`/`Result` are qualified; a declared `Result` is refused as `Intrinsic.Result`; `S.{ Self }` is refused as `Cycle.S`. It also now refuses datom-codec.ethos's `Meaning.String`, so that flake check fails until the declaration goes.
- **Recursion under rkyv** (fix 3): recursive Signal types archive and restore; only cycle-closing edges are boxed.

## Page 4 · What is broken in use

There are three pipelines. ethos-zero (a build dependency of 46 repos) is clean. The core-ethos bootstrap with its `Interface` root (7 repos) emits names like `pub struct z2VaBD(u64)` and maps `Integer` to `u64`. 17 repos, spirit and Persona among them, go through `.schema` files, and spirit's `.ethos` files beside them are orphaned.

Where ethos-zero is used, the ethos is the truth: signal-flow and meta-signal-flow regenerate their Rust in `build.rs` and assert it equals the committed file. *(Corrected: this page first said the flow's contract had drifted; that was read from a stale checkout, and the live repos agree.)* What the binding cannot catch is an import of a name that does not exist: meta-signal-flow imported a `RecipientDisposition` that signal-flow never defined. Four repos pinned to an older ethos-zero still commit Rust deriving `Compositional`.

**An ethos is only the truth where a freshness test binds it,** and about 20% of real files (15 of 76) have none. protos and datom-codec commit generated contracts that a Nix check keeps fresh but their code never imports.

## Page 5 · What real files cannot say

Ranked by how often it bites in the 76 files:

1. **Sized and unsigned integers.** The only integer is `i64`; lojix has 196 source lines that use an integer width.
2. **Bytes and fixed arrays.** `NameDigest([u8;32])`; `Signal<T>{bytes:Vec<u8>}` copied into 3 repos.
3. **Value rules.** lojix keeps 13 "Validated" shadow types only to add checks.
4. **Doc comments.** `;` comments are dropped.
5. **Time, maps, ordering, generic data wrappers, defaults.** All hand-written.
6. **Sema's evolution.** No key, identity or migration; no field ordinals.

**A name that is not a type.** `LockName.String` and `FlowId.String` become `pub type` aliases (rerun): a field name and no type safety. Authors hand-write `X(String)` newtypes anyway (9 in lojix and meta-signal-ethos-zero alone, dozens across the estate), and `Measurement.{ String }` is still accepted as a struct.

> A new type generally is like `name.string`, `age.integer`, or whatever we use: `int`.

-- psyche, typed, 2026-09-08 (flows/8e9e77/vision/single-field-structs.md).

*Inference, needs your ruling:* those words point at `Name.String` emitting a newtype.

## Page 6 · Fixes, ranked

Fix 1 (whole-program syntax) is out of this book's scope. The rest keep the audit's numbers and order. ✋ marks the ones that need your ruling.

2. ☐ **Drop meta-signal-flow's dangling import and repin Flow.** *(Corrected: the flow contracts are already bound. The import is dropped in meta-signal-flow 6.0.1; Flow still pins the revision before it.)*
3. ☑ **rkyv closes over recursion.** Landed, ethos-zero 11.0.0.
4. ☐ ✋ **Sized integers and bytes as intrinsics.** Needs your ruling on the names.
5. ☑ **Unique derived names.** Landed.
6. ☑ **Compile every fixture, close the holes.** Landed, ethos-zero 12.0.0.
7. ☐ **Errors with a line and column,** and a `Check` query.
8. ☐ ✋ **Rule on the `Type` root.** Implement it (a head type and one bracket), or rewrite the three skills to a Library.
9. ☐ ✋ **Doc comments, and alias versus newtype.** Carry `;` comments into `///`; rule whether `Name.String` is a newtype.
10. ☐ **Reconnect or retire the dead contracts; resync the docs;** repin the four repos still deriving `Compositional`. (The skills part has landed.)
