# Ethos solution: implementation order for Ethos Zero

Seat d5df1d, for the secretary 1d0733, to build and test on Prometheus.
Repository: ethos-zero at c2653d, version 16.0.0 (all eight flake checks pass at this commit, flows/1d0733/reports/ethos-zero-c2653d-tests.md). The baseline vision is psyche-skills/vision/ethos.md at 850fd2.

Status words used on every item:
- ruled: the living said it; the record path and date follow.
- proposed, awaiting ruling: a book proposal not yet ruled; book and number follow.
- the design's own: this seat's inference; the living has not seen it.
- defect: the generator does something no record asks for.

Layer words: grammar (protos lexer/parser, outside ethos-zero), conception (src/conception.rs, text to File), checking/refusal (src/checking.rs, Problem values), generation (src/generation.rs, File to Rust), print (src/printing.rs, protosization). Backward compatibility is not a design variable: every consumer and every generated file is updated, none is kept beside the old shape.

Build every item in the order given. After each, run the flake checks and regenerate the committed generated Rust (tests/freshness.rs holds it fresh).

## 1. A declaration `Name.Type` is a new type, not an alias

Status: built and green rebased onto 07714b, all suites and 8/8 with scratch protos and datom-codec, evidence flows/1d0733/reports/item12-on-item5.md with patches item12-on-item5-<repo>.patch; landing order protos, datom-codec, ethos-zero; gate: the living's Fork 3 (types book), both answers built and witnessed with the special representation (flows/1d0733/reports/representation-fork3.md); both answers now have a complete candidate tree on 07714b, bare and braced, fixtures and goldens byte-equal between them, expectations differing only where the answer prints (flows/1d0733/reports/fork3-complete.md).

What changes. Today `FlowId.String` emits `pub type FlowId = String;` (src/generation.rs, the `TypeDeclaration::Alias` arm, ~876-886). It emits, for a plain value, the tuple struct below, bearing the derive every struct and enum already bears (types book, Proposal 3: "Ethos Zero emits a new type as a Rust struct of one unnamed position, bearing the same derive as every struct and enum it emits."):

```rust
#[derive(rkyv::Archive, rkyv::Serialize,
  rkyv::Deserialize, Clone, Debug,
  PartialEq, Eq, Hash)]
#[cfg_attr(feature = "datom",
  derive(datom_codec::Datomizable,
         datom_codec::Composing))]
pub struct FlowId(pub String);
```

The inner position is `pub`: the brief names `pub struct Name(pub Type);`. That choice is the types book's Fork 4 (c), proposed, awaiting ruling; it is the shape 1d0733 witnessed through the derive (types-book-tests.md, claim 5, `struct FlowId(pub String)` gives datom text `{ abc123 }`). Fork 4 (a) and (b) would replace it; keep the emission in one place so a ruling changes one line.

Data model. Rename `TypeDeclaration::Alias(Identity, Reference)` (src/lib.rs:285) to `NewType`; update its uses (conception.rs:475 and :247, checking.rs 67/286/375/597/652/1155, generation.rs 353/445/876, protosization.rs 140/269). Rename `Problem` and doc text that say "alias".

Scope. Only a name over a plain value (String, Integer, Decimal, Boolean) becomes a new type here. A name over a container (`Vector<T>`, `Option<T>`) or over a declared type stays what it is today until the types book's Fork 1 and Fork 2 are ruled (listed at the end). Fixtures fixtures/alias-format.ethos and its test `aliases_name_their_types` (tests/generated.rs:270) are container aliases and are untouched by this item.

Layer: generation (the emission), conception (the variant rename). Grammar unchanged.

Acceptance tests (Prometheus, Nix):
- `Library [] [ FlowId.String Age.Integer ] [] []` generates `pub struct FlowId(pub String);` and `pub struct Age(pub Integer);`, each with the derive above; the generated file compiles.
- A new compile test (the types book's claim 1 and 2): a function taking `FlowId` refuses a `LockName`, error E0308. Fixture pair, both compiled by rustc through the existing generated-module harness.
- Datom: `FlowId("abc123")` prints as `{ abc123 }` (today's derive; Fork 3 is open, so the test names the current form and is the one line a Fork 3 ruling changes).
- The generated file for every fixture in tests/generated/ is regenerated and passes tests/freshness.rs.
- size_of::<FlowId>() equals size_of::<String>() (claim 4, 24 and 24).

## 2. Single-field structs and double wrapping are refused

Status: built and green rebased onto 07714b, all suites and 8/8 with scratch protos and datom-codec, evidence flows/1d0733/reports/item12-on-item5.md with patches item12-on-item5-<repo>.patch; landing order protos, datom-codec, ethos-zero; gate: the living's Fork 3 (types book), both answers built and witnessed with the special representation (flows/1d0733/reports/representation-fork3.md); both answers now have a complete candidate tree on 07714b, bare and braced, fixtures and goldens byte-equal between them, expectations differing only where the answer prints (flows/1d0733/reports/fork3-complete.md).

What the books say, quoted:
- Invariants Proposal 1: "A struct holds two or more positions; a struct of one is refused. A type that holds one other type is written as its name, a dot and that type." Example: `Age.{ Integer }` refused, `Age.Integer` accepted.
- Invariants Proposal 2: "A type written as a name, a dot and one type never names another such type; it names what it holds." Example: `FlowId.String` with `Job.FlowId` beside it; `Job.FlowId` refused.
- Types book Proposal 2 adds: "A new type holds a plain value, a String, an Integer, a Decimal, a Boolean; a new type over a struct or an enum is refused."

The books give no refusal message text. Ethos Zero's refusals are `Problem` values with a located path ("the refusal names the place", invariants Proposal 1). The messages are therefore the design's own: add `Problem::SinglePosition` (the struct has one position, at the struct's path), `Problem::DoubleWrap` (a new type over a new type, at the declaration's path), and, for the third rule, `Problem::WrapsStructure` (a new type over a struct or enum). Each prints in the existing `Checked`/`Conceptual` reply form with the path vector, as `Undeclared.Event` does today.

Layer: checking/refusal, in `File::check` over `TypeDeclaration::Struct` and `Variant::Struct` (src/checking.rs ~1428, 1453-1477); also the inline payload form `X.{ T }` in a variant. The rule applies after inline expansion: a variant payload of one position is refused the same way.

Fixtures to change first, because they use a one-position struct and would now be refused: fixtures/inline-collision.ethos (`X.{ String }`, `Z.{ String }`, `X.{ Integer }`), fixtures/nested-collision.ethos (`X.{ String }`), fixtures/tree-types.ethos (`B.{ String }`), fixtures/generic-shadow.ethos (`A.{ String }`), fixtures/signal-decimal.ethos (`Measurement.{ Decimal }`), fixtures/empty-signal.ethos (`Shared.{ Name }`), fixtures/composition-types.ethos (`Vec.{ String }`, `Item.{ Vec Integer }` is two positions and stays). Rewrite each as a new type (`X.String`) or add a second position; their generated Rust and the tests that name the generated fields follow. The zero-position `Unit.{}` stays accepted until a ruling (audit item 26 notes it; no record speaks).

Acceptance tests:
- `Age.{ Integer }` is refused at the struct's path; `Age.Integer` is accepted (invariants Proposal 1, both blocks).
- `FlowId.String` with `Job.FlowId` refused at Job's path; `FlowId.String` alone accepted (invariants Proposal 2, both blocks).
- `Pair.Lock` where Lock is a struct is refused (types book, "A new type over a complex type").
- One-position inline payload `Started.{ String }` in an enum is refused.

## 3. The inline import `Topic.custom:Name`

Status: landed at b2fa8b, included in 07714b.

Already accepted today, in a types section and in a struct position (1d0733, flows/1d0733/reports/prometheus-witness-final.md; this seat's probe). No code change. Add the test that fixes it, in both positions:

```
Library
[]
[ Topic.custom:Name ]
[]
[]
```

and `Holder.{ Topic.custom:Name String }` in a struct. The generator takes `custom` as a Rust source path today (`custom::Name`); the test pins the accepted parse and the emitted type, and notes that the registry meaning of `custom` is item 7.

Defect to fix: `Topic:custom:Name`. In a struct position it is accepted and silently drops `custom` (the Colon arm of `Conceiving<Reference>`, src/conception.rs ~427-432: `r.source = Some(head)` overwrites the source the inner reference already carries). In a types section it is refused. 1d0733's mutex probe case a9 shows the same drop for `std:sync:Mutex<String>`, which emits `std::Mutex<String>`.

Fix, layer conception: when the body of a colon-headed reference already carries a source, refuse with `Problem::Expected(Form::Reference)` at the body's path, as the import position already does (`Expected.Import` at `[ 1 0 0 1 ]` for `std:sync:Mutex` in imports). The refusal form is the design's own; the refusal itself is required by the ruling (one source, told by a lowercase first letter and one colon).

Acceptance tests (all on the built c2653d-derived binary, answers compared whole):
- `Topic.custom:Name` accepted in types and in a struct position.
- `Topic:custom:Name` in a struct position is refused (today: accepted, `custom` dropped); in a types section refused as today.
- `Topic:custom.Name` refused as today (witnessed).
- `std:sync:Mutex<String>` inline is refused rather than emitting `std::Mutex<String>`.

## 4. The invariants the audit found unenforced

Each row: the invariant, status, the check Ethos Zero adds, layer, the test. Grades are the audit's (reports/ethos-audit.md section 3) and the invariants book table; the probes were rerun on Prometheus (flows/1d0733/reports/probes-rerun.md).

a. A struct of one position refused; no double wrapping. Item 2.

b. The print keeps every comment, at the element it was written on. Status: proposed, awaiting ruling: invariants book Proposal 3 ("The canonical print keeps every comment, at the element it was written on."). Today `File` has no field for comments and the print drops all of them (src/printing.rs delegates to protos `Textualizable`; tests/print.rs:135-150 strips `;` lines before comparing). Change: carry a comment on each section and declaration in `File`, conceive it in the reader, and print it back. Layer: conception and print. Test: read a file with comments beside elements, print it, assert every comment survives and sits at its element; the crate's own ethos-zero.ethos compared to its print without stripping `;` lines.

c. Each element on a new indented line; a comment beside or above, lined up. Status: the print layout is a ready patch (flows/1d0733/reports/fork-invariants-4.patch) pending invariants Proposal 4.

d. A variant name is capitalised. Status: the design's own (grade: not enforced, audit item 19; vision-ethos and knowledge-datom say "In datom a head is always a variant, so it is capitalized"). Probe: `Low.[ lowvariant Other ]` generates `pub enum Low { lowvariant, Other }`. Change: `Variant::check` (src/checking.rs 1453-1477) refuses a lowercase first letter. Layer: refusal. Test: that probe is refused at the variant's path; `Low.[ Lowvariant Other ]` accepted.

e. Derive name. Invariants Proposal 6 (proposed, awaiting ruling) renames `Compositional` to `Composing` in the skill text only; the generator already emits `datom_codec::Composing`. No generator change. Test: the freshness suite already holds it.

f. Everything else the audit grades "not enforced" waits on a ruling and is not in this order (see the last section): inline depth, who holds layout and comments, comment required on every layered line, kind-name qualifier form, authored underscore names, every trait written in ethos, memory upgrades.

g. Mutex is hard to express in ethos today. Status: Mutex both options ready (fork-invariants-f3-a/b.patch) pending invariants Fork 3.

## 5. The `kind` to `trait` rename across the generator

Status: landed in ethos-zero main at 07714b (parent a09bb8), package 17.0.0, eight checks on that revision, Field's receipts under flow-evidence/42265e/overnight-source-sequence/.

What changes, per the audit's list: `KindDeclaration` to `TraitDeclaration`, `Form::Kind`, `Role::Kind`, `Problem::KindWanted` to `TraitWanted`, `KindBody`, the section named "kinds" to "traits" in the documented section order (the file's fourth-from-last bracket; position unchanged, so no grammar change), the comment `; kinds` in every fixture and in ethos-zero.ethos and error.ethos, the CLI no-argument output (it prints ethos-zero.ethos), README.md and UPGRADES.md, the `datom` feature text. Rename fixtures capability-kinds, processable-kinds, self-kinds, streamable-kind to `-traits` and update include_str! and freshness lists. The skill knowledge-ethos (mind-skills) is knowledge and is changed by its owner, not here.

Layers: conception, checking/refusal, generation, print (comments and the CLI contract). Grammar unchanged. The fixture traits named `Kind...` inside the user-facing refusal text change with `TraitWanted`.

This is a breaking change to error names and the documented section name: bump the major version (17.0.0) and write it in UPGRADES.md.

Acceptance tests: grep of src/, tests/, fixtures/, README.md, UPGRADES.md, ethos-zero.ethos and error.ethos finds the word `kind` only where it means something else (none expected); `a_concrete_type_in_an_input_is_refused_as_wanting_a_kind` becomes `...wanting_a_trait` and answers `TraitWanted`; the flake checks pass; the generated files are fresh.

## 6. Flow as the current best example: the fixture the test suite builds

Status: in dry run on top of the set at 07714b, by 1d0733.

What the suite builds today: fixtures/print/flow-library.ethos, flow-signal.ethos, flow-operation.ethos and flow-memory.ethos; generated into tests/generated/flow-*.rs; held fresh by `the_flow_nexus_modules_are_fresh` (tests/freshness.rs:62) and compiled and round-tripped, with and without the datom feature, by `the_flow_nexus_contract_compiles_and_crosses_the_wire_with_and_without_datom` (tests/flow_contract.rs:64).

What changes. flow-library.ethos declares `FlowId.Integer`; change it to the following, which after item 1 emits `pub struct FlowId(pub String);`:

```
Library
[]                       ; imports: none
[ FlowId.String          ; a string for now, unideal:
                         ;   the flow id is to be a hash
  Voice.[ Psyche.Rank
          Mind.Rank
          Field.Rank ]
  Rank.[ Primary Secondary Tertiary ]
  Event.[ Started
          ToolUsed.String
          Stopped ] ]
[]                       ; traits
[]                       ; associations
```

(The printed layout follows item 4c once ruled; until then the fixture keeps the layout it has.) Update tests/flow_contract.rs: the wire values `flow_id: 7` become `FlowId("7".into())` style constructions of the new type; the re-export line `pub use library::{Event, FlowId, Voice}` stays. Update the signal, operation and memory files only where they name `FlowId` positions. Any one-position struct in the four files is rewritten under item 2.

Acceptance test: the four files read, generate, stay fresh, compile, and round-trip through rkyv and (with the feature) datom text; the FlowId comment is present in the fixture source (it is dropped by the print until item 4b).

## 7. `core:Name` and a lowercase single-segment source

Status: held until inline-import questions Q5, Q6, Q8 are answered.

Witnessed today (reports/inline-import-research.md, section 2.5): `core:Name` generates `core::Name`; rustc answers `error[E0425]: cannot find type 'Name' in crate 'core'`. `Topic:Name` generates `pub name: Topic::Name`, which names no crate. `Name` in ethos-zero (src/lib.rs:56-84) is the generator's own validated Rust identifier and runs no case check: `Topic`, `core`, `fooBar` and `snake_case` pass. A camelCase check on it would refuse every PascalCase type name.

Order for this item, smallest working shape, the design's own: until the registry questions (Q5, Q6, Q8 of the research) are ruled, a source named `core` is refused rather than emitting Rust that rustc refuses. Layer: refusal. Refusal value: `Problem::Source` at the head's path (existing `Problem::Name` is a Rust-identifier failure and does not fit; a new value is the design's own). Test: `Library [] [ Topic.core:Name ] [] []` and the struct-position form are refused; `Topic.protos:Name`, `Topic.custom:Name` and `std:Mutex` keep today's behaviour.

Not built here: the camelCaseExpression type with runtime checks, the registry, the `{ Subaspect.[ Vision Knowledge ] Topic:Name }` key, the meta-signal payloads, the blake3 hash, a capitalised head declaring a type. The research lists twelve questions; the record "Choice 3 ruled" settles only the `Topic.custom:Name` form (item 3). Whether a capitalised `Topic:Name` is read as Reading A (the head declares) or Reading B (the name decides) is research question 1, unruled.

## 8. Mutex is hard to express in ethos today

Status: ruled that implementers report what is hard to express (flows/ebbe30/vision/ethos.md, 2026-10-09, comment B; the sentence stands in compensation-behavior: "An implementer who meets something hard to express in ethos — a mutex, an exception, any need the language seems not to carry — reports it to the living as its own finding rather than working around it."; invariants book Proposal 5, "keep as it stands, or amend", proposed, awaiting ruling). Whether ethos should express a Mutex field is Invariants book, Fork 3, unruled.

Witness: flows/1d0733/reports/mutex-probe.md, built from c2653d on Prometheus. An import head is one segment (the lexer ends the head at the first `.`, `!` or `:`), so `std::sync:Mutex` is refused `Expected.Import`; every accepted form emits `std::Mutex`, `std::sync` or `std::sync<..>`; `std::Mutex<String>` fails E0425. With the path fixed by hand to `std::sync::Mutex<String>` the generated derives fail with 11 errors (Archive, Serialize, Deserialize, CheckBytes, Clone, PartialEq, Eq, Hash; 13 with the datom feature); only Debug passes. Ethos has no way to give a declaration fewer derives.

What the design does: nothing in the generator until Fork 3 is ruled. The implementer who meets a Mutex position reports it as a finding to the living through 1d0733, as the sentence above says. No Mutex test is added; the probe stays the witness.

## Not in this order

Waits on the living's ruling (book, number):

- Every option of types Forks 1 and 2 is a ready patch (flows/1d0733/reports/fork-types-12-<candidate>.patch, four candidates plus 1c's datom-codec reach), per flows/d5df1d/reports/fork-options-spec.md.
- Types book: Proposal 1 (new type section, replacing the alias, in vision-ethos); Proposal 2 (what is refused, awaiting its turn); Proposal 3 (what Ethos Zero generates; the tuple rule on lines 435-436); Proposal 4 (other alias sites); Proposal 5 (flow id stays a string, marked). Fork 1 (a name over a container), Fork 2 (a name over a declared type), Fork 3 (how a new type reads in datom), Fork 4 (how the value inside is reached), Fork 5 (every semantic string a new type).
- Ethos invariants: Proposal 1 (a struct of one position refused, asks its ruling now); 2 (no double wrapping); 3 (the print keeps every comment); 4 (each element on a new indented line); 5 (implementers report); 6 (the derive's real name). Fork 1 (how deep a type is declared inline), Fork 2 (who holds layout and comments), Fork 3 (a Mutex field in ethos).
- The golden ethos, fourth edition: Ruling 3 (the ethos of ethos in vision-ethos), with choices 1 to 4: Value, a comment in the anatomy, the receiver names, and Name as `Name.String` or `core:Name`.
- The inline import, third edition: Ruling D1 (the sentence for `Topic.custom:Name` in vision-ethos).
- The inline-import research, twelve open questions, among them Reading A or B, what `Topic:Name` declares, the registry entry, the isos environment, the meta-signal payloads.
- Not booked: the special representation (a trait for a custom datom encode/decode; 445410's work); every trait written in ethos (about 95 hand-written traits in the generator); memory-trait upgrades per version; Operation's section order (marked proposed in src/lib.rs); authored underscore names that read as derived; the kind-name qualifier form; zero-position structs.
