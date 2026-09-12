# ethos-zero — the witnessed audit defects fixed, 6.1.6 → 7.0.0

Flow f6db8d, ethos-zero fix subflow. Slice: the ethos-zero defects in
`reports/substrate-audit.md` §4.2(a), §4.2(b), §4.2(c), §4.2(d), §4.2(e), §6
(no Sema generation coverage) and §4.4 (the four adjacency scanners).

- Repository `/git/github.com/LiGoldragon/ethos-zero`
- Before: 6.1.6 at `4695ee0c1f5d00dcf5cceba08f5fa00412b92184`
- **Released: 7.0.0 at `c8a6836920edeee19d9453f0eca9a5b0645d9ebd`**, pushed to `main`
- Orchestrate lock 1106 `EthosZeroDefectFix`, acquired before the first edit,
  released after the push.
- Dependency pins unchanged: protos `b543678cfc8609529cea7174eb4af8a64daa54ad`,
  datom-codec `f2cc06858d38a4028c928d33323a6d682e7c222f`, in `Cargo.toml` and
  `flake.nix`. No sibling fix was needed and none had landed (see §3).

Claims are marked **witnessed** (this flow ran it and saw the output) or
**read** (this flow read the source and cites it).

## 1. What was changed

### 1.1 The Signal query type is `Query` — Vision decides

Vision/ethos.md is explicit, twice. The emitted Rust:

```rust
// emitted by Ethos Zero into the signal crate
#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
pub enum Query { Lock(LockRequest), Release(LockId) }
```

and the placement rule: "Head then symbol is a variant of `Query` or `Response`
in a Signal's first two sections, an alias in the types section. … Ethos may
generate default implementations for Query and Response, which is why Signal is
its own root." Vision/signal.md names the sections "queries" and "responses" and
names no `Request`. The ethos skill's `Request` is the older design, which
Vision supersedes.

So the generator was right and the check was wrong. `Implying for File` and
`Checkable for Signal` (`src/checking.rs`) now seed `Query`, not `Request`, and
the AST field, the reader, the printer and the generator call the section
`queries` throughout (`src/lib.rs`, `src/conception.rs`, `src/protosization.rs`,
`src/generation.rs`). `Request` became an ordinary name: a Signal may declare a
type called `Request` and nothing is generated under it.

Witnessed before the fix, the pre-change source generating
`Signal [] [ Ask.Query ] [ Told.Query ] [ Query.{ String } ]`:

```
8:pub struct Query {
17:pub enum Query {
error[E0428]: the name `Query` is defined multiple times
 8 | pub struct Query {
   | ---------------- previous definition of the type `Query` here
17 | pub enum Query {
   | ^^^^^^^^^^^^^^ `Query` redefined here
```

After: `generate()` refuses the file as a duplicate, and the `Request` spelling
generates one `pub struct Request` beside exactly one `pub enum Query`.

### 1.2 Sema reserves nothing; a record may be named `Record`

Vision/sema.md names Sema's second section "record types" and reserves no name;
generation emits no Sema type of its own (read, `src/generation.rs`, the
`File::Sema` arm walks `sema.types` and nothing else). The reservation and the
`Implying` entry are gone.

A second defect was found while there, not in the audit (read and witnessed):
`Checkable for Sema` collected its declared names from section **2**, which Sema
does not have, while checking section 1 — so two Sema records with the same name
were accepted. Sema has two sections, imports 0 and record types 1. Corrected;
the duplicate is now refused, and there is a test for it.

### 1.3 `Self` in a data position no longer panics

`Self` is a Vision intrinsic. Its field base snake-cased to `self`, which is one
of the four keywords no raw identifier may spell, so `Ident::new_raw` aborted
the process (witnessed against the pre-change source:
``thread '…' panicked at src/generation.rs:438: `r#self` cannot be a raw
identifier``).

`Self` in a position *is* the enclosing type, so the field is now named for that
type: `Library [] [ Node.{ String Self } ] [] []` yields
`pub node: std::boxed::Box<Self>`. `crate`, `self`, `super` and `Self` reaching
a field base by any other route take a trailing underscore instead of aborting.

This changed one committed generation: `tests/generated/composition-types.rs`,
where `Tree.{ Option<Self> }` had the field `self_option` and now has
`tree_option`. The freshness test carries the change.

### 1.4 Four adjacency scanners became one, and it now carries a sourced generic

The four loops in `src/conception.rs` — type/argument lists, declaration lists,
variant lists, associated-type lists — each peeked at `index + 1` for an
`Enclosure::Angled` sibling. They are one trait, `Constraining`, whose single
capability pairs every node of a list with the constraints written against it
and hands each context the node, the constraints if any, and the node's own
index. The four contexts keep their own meanings for the pair and now differ
only in that meaning.

Two audit defects fall out of the unification:

- §4.2(d), the printer emitting a shape its own reader refused. The References
  context no longer keys on `Protos::Bare`; it conceives the node into a
  `Reference` and attaches the constraints, so a sourced generic in a data
  position — `Record.{ external:Vector<String> }`, exactly what
  `reference_nodes` prints — reads, reprints and generates
  `pub string_vector: external::Vector<String>`. Witnessed failing before the
  fix: `source did not read: Library [ external:[ Vector ] ] [ Record.{
  external:Vector<String> } ] [] []`.
- §4.2(e), the off-by-one in associated-type fault paths: `index += 1` no longer
  precedes the `place` calls, because the index is fixed before the pair is
  built.

A pair whose node cannot take constraints — an angled enclosure after a struct
declaration or a bare variant — is now a typed refusal naming the angled
position, where before the angled node was left to be conceived on its own.

## 2. Sema generation coverage

The audit's §6 qualification was right: the only Sema fixture was written under
the **Library** root despite its comment, and the Sema test only actualized.
There was no coverage at all of the Sema generation path.

- `fixtures/entry-sema.ethos` is now a `Sema` file. Its generated
  `tests/generated/entry-sema.rs` is byte-identical to what the Library-rooted
  fixture produced, which is the witness that the two roots agree on record
  types, and it is now reached through `Conceiving<Sema>` and the `File::Sema`
  emission arm. The freshness test covers it as it covers every fixture.
- `tests/generated.rs` compiles the generated Sema module and round-trips a
  record through the full datom ascent and descent. Its expected text came from
  Vision/datom.md, not from the code, and was wrong on the first run — the test
  was seen failing with `left: "{ root [ { first 1 } ] }"` against the expected
  `"Record.{ root [ Entry.{ first 1 } ] }"`. The code is right: a struct is
  braces, a head names a variant. The expectation was corrected, not the code.
- Four new tests in `tests/ethos.rs` cover Sema generation directly: a record
  named `Record`, two records with a `Vector<Entry>` position between them, and
  a refused duplicate.

Every new test was seen failing once against the pre-change source, in a scratch
copy of the repository at `4695ee0c` with the six changed source files restored
from `main` (witnessed):

```
test a_signal_declaring_the_query_type_is_refused ... FAILED
test a_sourced_generic_in_a_data_position_reads_and_reprints ... FAILED
test self_in_a_data_position_is_named_for_the_enclosing_type ... FAILED
test sema_generates_a_record_type_named_record ... FAILED
test sema_generates_every_declared_record_and_refuses_a_duplicate ... FAILED
test result: FAILED. 6 passed; 5 failed
```

(`a_signal_declaring_the_response_type_is_refused` passes on both sides;
`Response` was already reserved, and the test stands as its companion.)

## 3. The adjacency-scanner shape: protos cannot read the right shape today

The brief asked whether the current protos reader, or the fix sibling's if
landed, makes the rejected right shape readable. **It does not, and no sibling
fix had landed.** Witnessed and read:

- protos `main` is `b543678cfc8609529cea7174eb4af8a64daa54ad` — the same
  revision ethos-zero pins. Nothing new to pin.
- `Protos::Headed` (`protos/src/core.rs:28-36`) carries `separator: Separator`
  and `body: Box<Protos>` unconditionally. **There is no node for a name bearing
  constraints and no body.** The right shape is not merely unreadable, it is
  unrepresentable in the type.
- The reader is explicit about the rewind (`protos/src/core.rs:380-401`): on `<`
  after a run it parses the angled enclosure, and if the next glyph is not `.`,
  `!` or `:` it restores the offset and the budget and returns
  `Protos::Bare { text: run, end: angle_start }`, leaving the angled enclosure to
  be read as the next sibling.

So `Vector<Integer>` is two sibling structures, the re-join stays, and the
canonical reprint still writes `Vector <LockPath>` with a space.

**What protos would need**, precisely — recorded in the code on `Constraining`
in `src/conception.rs`, where the re-join is done:

1. A node for a name bearing constraints and no body: either constraints on
   `Protos::Bare`, or `separator` and `body` becoming optional on
   `Protos::Headed`.
2. A reader that keeps the constraints on that node instead of rewinding past
   them when no separator follows the closing `>`.
3. A writer that prints the constraints against the name with no space between
   them, so the canonical print reproduces Vision's own spelling.

All three are protos changes. Without (3), tightening the re-join to require
adjacency of extents rather than adjacency of shapes would break ethos-zero's
own round trip, because the printer emits the space the tightened reader would
refuse — the laxness the audit names in §4.4 is load-bearing until protos can
print the unsplit form. It was therefore left as it is, and not hidden: the
comment at the re-join says so.

## 4. Decisions taken on the living's behalf

The living was asleep and ordered autonomous work. Each of these was decided
from Vision and is recoverable from it.

1. **`Query`, not `Request`.** Vision/ethos.md emits `pub enum Query` and names
   the placement rule in terms of `Query`; Vision/signal.md calls the section
   queries. The ethos skill says `Request` and is the older design. The
   generator was kept and the check moved. Consequence: any Signal declaring a
   type named `Query` is now refused where it previously produced invalid Rust,
   and any that declared `Request` to dodge the old reservation is unaffected.
2. **The internal name follows Vision.** `Signal.requests` became
   `Signal.queries`. This is a public field of a public struct; it is why the
   version is a major bump. The disagreement between the two names is what
   produced the defect, so one name was made to stand.
3. **Sema reserves nothing.** Vision/sema.md reserves nothing and Sema generates
   nothing implied. The alternative — keeping `Record` reserved and teaching
   Sema to generate a `Record` type — would invent a Vision statement.
4. **`Self` names its field for the enclosing type** rather than faulting the
   file. The audit proposed "a whole-file fault is owed". Vision lists `Self` as
   an intrinsic and `composition-types.ethos` already used `Option<Self>` in a
   data position, so refusing it would retire a construct Vision sanctions and
   the fixtures exercise. Naming the field for the type `Self` stands for keeps
   the construct and obeys the type-first field rule.
5. **The scanners were unified, not deleted.** The brief's condition for
   deleting them is not met (§3). Unifying reduces four loops to one and is the
   whole of the reduction available without a protos change.
6. **A sourced generic in a data position now reads.** The printer already
   emitted it; making the reader take it back removes an asymmetry rather than
   adding a form. No Vision statement writes this shape either way.
7. **Version 7.0.0, not 6.2.0.** Public behavior and a public field both changed
   and both are breaking. No compatibility path was kept for either.
8. **README corrected where it was demonstrably false** about what was changed:
   the file-variants table listed the retired `Types` and `Kinds` roots and the
   wrong implied names and Sema shape, and named `src/contract.rs` for a file
   that is `src/ethos-zero.rs`.

## 5. Gate — full and local, witnessed

`cargo test --offline`, 49 tests, everything green:

```
test result: ok. 17 passed   (src/lib.rs behavior)
test result: ok. 7 passed    (tests/cli.rs)
test result: ok. 11 passed   (tests/ethos.rs)
test result: ok. 3 passed    (tests/freshness.rs)
test result: ok. 9 passed    (tests/generated.rs)
test result: ok. 2 passed    (tests/signal_without_datom.rs)
test result: ok. 0 passed    (doc-tests)
```

`cargo fmt --check` clean. `cargo clippy --offline --all-targets -- -D warnings`
clean. `cargo doc --offline --no-deps` clean.

`nix flake check -L --builders ''` — no remote builders, everything built
locally — ends:

```
ethos-zero-clippy> +++ command cargo clippy --release --locked --all-targets -- -D warnings
ethos-zero-clippy>     Checking ethos-zero v7.0.0 (/build/source)
ethos-zero-clippy>     Finished `release` profile [optimized] target(s) in 0.72s
all checks passed!
```

That covers `build`, `test`, `fmt`, `clippy`, `doc`, `dependency-ethos` (the
built tool reading protos's and datom-codec's own ethos declarations),
`no-free-functions` and `no-inherent-methods`.

## 6. Left standing, deliberately

Not in this slice, and each still open after this release:

- §1.9 / §4.2(f), `#[rustfmt::skip]` landing on the first item of a multi-item
  group. Latent: both the committed text and the freshness comparison come from
  prettyplease, so it bites only when rustfmt is first run over a generated file.
- §4.3, the qualification leak on the boxing path — visible in the file this
  release touched, `tests/generated/composition-types.rs`, as
  `Option<std::boxed::Box<Self>>` rather than `std::option::Option<…>`. It
  compiles only because `Option` is in the prelude, against Vision's "the
  generated code carries no `use` statements".
- §4.3's unstated emissions: `Sized` as a tenth intrinsic, the unconditional
  `Clone, Debug, PartialEq` and rkyv derives, `where Self: Sized`, the import
  rename form, `TYPE_DECLARATION_LIMIT`. Each needs the living, not a fix.
- §4.4's closing question — whether the canonical ethos reprint is allowed to
  differ from the notation Vision writes — is still for the living. §3 above
  gives the three protos changes that would make the answer "no".
- The `protos`, `datom` and `ethos` skills still describe the pre-distillation
  design (§5 of the audit). This release makes the ethos skill wrong on one more
  point: it says the Signal query enum is `Request`.

## Sources

- `/home/li/primary/flows/f6db8d/reports/substrate-audit.md`, §4.2, §4.3, §4.4,
  §6, §8 — the defects fixed here and the question this flow answered.
- `/home/li/primary/Vision/ethos.md` — the three roots, the `Query` emission and
  the placement rule; the intrinsics including `Self`.
- `/home/li/primary/Vision/signal.md` — the sections named queries and responses.
- `/home/li/primary/Vision/sema.md` — Sema's second section is record types and
  reserves nothing.
- `/home/li/primary/Vision/datom.md` — the datom text a struct and a vector take,
  used as the expected value of the Sema round-trip test.
- `/git/github.com/LiGoldragon/protos` at `b543678`, `src/core.rs:28-50` and
  `:380-401` — read, for what protos would need.
- `/git/github.com/LiGoldragon/ethos-zero` at `c8a6836` — the release.
- Scratch copy of ethos-zero at `4695ee0c` with the changed sources restored
  from `main` — the pre-fix failure witnesses in §1 and §2.
