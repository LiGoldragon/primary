# Audit: ethos-zero 2.0.0 (a2e8eafcd45c)

Read-only audit of /git/github.com/LiGoldragon/ethos-zero at a2e8eafcd45c
(main; Cargo pins protos c5594f9d6f73 = 0.17.1 Rust, datomic 2c2e2073fd34 =
0.11.1 Rust; flake pins protos 2cb88849f3b1, datomic cf59b01bbbc8).
Every source file, fixture, test, .ethos and doc was read whole; every
fixture was generated with the built binary into the scratchpad and the
output compiled and round-tripped in a scratch crate against the pinned
protos/datomic. Method and evidence are stated per item. Observations,
inferences and unknowns are kept apart; "inference" marks the auditor's.

Verdict in one line: the crate reads the vision's grammar and its
generated datom machinery round-trips correctly for every shape tried,
but it is not solid: faults are never situated (every path is empty),
several vision shapes do not generate compilable Rust, `nix flake check`
fails (fmt and doc), the CLI does not speak its own contract, and the
"trait ontology" is two thin trait facades over 81 free functions.

## Item findings

### 1. File — compliant with two defects

Observed (src/lib.rs:23-60): `File` is an enum of `Types`, `Kinds`,
`Signal`, `Sema`; every variant's first field is `imports`; Types has
`imports, types, associations` (lib.rs:319-328, arity 3 enforced); Kinds
has `imports, kinds` (330-338). Sweet form is converted on text before
delineation (`Canonicalizing for str`, lib.rs:200-243) and the reader sees
only the braced form (lib.rs:278-305) — "before the text is read as ethos
at all, the file is converted mechanically to the canonical form"
(Vision/ethos.md, File). No version anywhere (grep: none; tests/ethos.rs:560
asserts `Library.{0 1 0}` is refused — witnessed: `Root at []`).
Canonical braced input is accepted: scratchpad/adv/canonical.ethos
generated (witnessed), tests/ethos.rs:70-75.

Defects witnessed:
- A sweet file whose last line is a comment with no trailing newline
  fails delineation: lib.rs:242 appends ` }` on the same line as the
  comment, so the closer is eaten (`delineation fault at 6..74` on
  scratchpad/adv/trailing-comment.ethos). With a trailing newline it
  reads. A mechanical conversion must not depend on the final byte.
- The root dispatch is a string match on the head (lib.rs:297-303), and
  every reader fault is at path `[]` (see item 7).

### 2. Types — compliant on shape; the vision's examples match modulo three additions

Observed generated Rust (scratchpad/gen/multi-types.rs):
`pub struct Record(pub protos::Text, pub protos::Integer);`,
`pub struct Report(pub protos::Text, pub Vec<protos::Integer>);`,
`pub enum SinkError { Closed, Full }`, `pub type LockId = protos::Integer;`
— the vision's four lines exactly. orchestrate.rs:301-304 gives
`pub enum Request { Lock(LockRequest), Release(LockId),
Observe(ObserveSelection) }` — the vision's Request exactly. No `use`
statement in any generated file (grep). `[ protos:Text ]` and the
intrinsic produce identical output (record-types.rs = multi-types.rs
Record, byte-identical).

Additions beyond the vision's shown Rust (not decidable from
Vision/ethos.md, which shows none of them): a leading
`#![allow(dead_code)]` (lib.rs:1051); `#[derive(Clone, Debug, PartialEq,
Eq)]` on every struct and enum, `Copy` added for unit-only enums
(lib.rs:1099-1105, 1111); and the Datomic impls after each type.

Non-compliant, witnessed:
- `Name.{ T1 T2 }` as a variant body does not become a tuple variant; a
  synthetic named struct `ParentVariant` is invented and the variant
  holds it (lib.rs:1185-1202): `Protoform.[ Headed.{ Head Separator
  Protoform } … ]` from protos.ethos generates `pub struct
  ProtoformHeaded(...)` and `Headed(ProtoformHeaded)`
  (scratchpad/depsgen/protos.rs:241-247). The vision: "every variant
  carrying data is a tuple variant"; the hand-written protos crate has
  `Headed(Head, Separator, Box<Protoform>)`. The generator invents names
  that are in no ethos, and the generated Rust API diverges from the
  crates whose ethos it is.
- A bare name in the types section (`[ Text Integer Bogus ]`) is
  accepted as a self-alias (lib.rs:409-414) — a form that is in no vision
  sentence; for a non-intrinsic it emits `pub type Bogus = Bogus;`, which
  does not compile (witnessed: E0391 cycle). This exists to read
  protos.ethos's `[ Text Integer Decimal Boolean … ]`.
- Inline qualification in a type position (`Structural.protos:Fault`, as
  the pinned datomic.ethos writes it) faults `TypeExpression at []`
  (witnessed). Whether that form is wanted is not in the vision
  (imports are `protos:Text`; the vision never shows one inline), but the
  consequence is decided: the pinned datomic.ethos does not read with the
  ethos-zero that pins it (see item 10).

### 3. Kinds — Summarizable, Fillable, Processable match; Streamable does not compile

Observed (scratchpad/gen/capability-kinds.rs): `pub trait Summarizable {
fn summarize(&self) -> protos::Text; }` and Fillable with `push(&mut self,
input: protos::Text) -> Result<protos::Integer, SinkError>`,
`drain(&mut self) -> Vec<protos::Text>`, `create() -> Self` — the
vision's Rust exactly. Receivers `.` `!` `:` map to `&self`, `&mut self`,
none (lib.rs:672-676, 1544-1548). Both capability shapes read
(lib.rs:678-704). Complex kind reads four brackets (lib.rs:568-584);
`[ CAPACITY.Integer ]` generates `const CAPACITY: protos::Integer;`.
Identity: `Processable<[Clonable Sendable] Serializable>` generates
`pub trait Processable<A: Clonable + Sendable, B: Serializable>`
(scratchpad/gen/processable-kinds.rs).

Non-compliant, witnessed:
- Streamable generates `fn next(&mut self) -> Option<Item>;`
  (streamable-kind.rs:5); the vision shows `Option<Self::Item>`. `Item`
  unqualified does not compile (E0425, witnessed in the scratch crate;
  compiles after the one-token patch). Same defect for `Fault` in the
  pinned protos-kinds.ethos: `fn conceive(&self) -> Result<Self, Fault>;`
  (depsgen/protos-kinds.rs). An associated type named in a capability
  must be emitted as `Self::Name`.
- A superkind with a constraint (`[ Conceivable<Datom> ]`) faults `Kind
  at []` (lib.rs:611-617 accepts bare symbols only; witnessed on
  scratchpad/adv/superkind-constraint.ethos and on the pinned
  datomic-kinds.ethos). The vision: "A constraint is a kind, or a bracket
  of kinds … Two heads that differ in a constraint are two kinds" — a
  kind's identity includes its constraints wherever the kind is named.
- The kind's own separator is ignored (`_sep`, lib.rs:544):
  `Summarizable:[ … ]` is accepted as a kind (witnessed). A kind
  declaration is a headed bracket/brace with the dot.
- A capability with an empty yield bracket (`run.[]`) faults
  `TypeExpression at []` — typed, but the problem is `TypeExpression`
  rather than the capability, and unsituated.

Not decidable from the vision: the vision's Rust for Processable reads
`A: Clone + Send, B: Serialize`, mapping Clonable/Sendable/Serializable to
Rust's names; the generator emits the ethos names unchanged. The vision
states no mapping rule; the living should say whether ethos kind names
that stand for std traits are mapped at the contact point.

### 4. Associations — compliant, with two defects

Observed (scratchpad/gen/sink-associations.rs:74-79): the `const _: ()`
block with `fn assert_sink_summarizable<T: Summarizable>() {}` / `let _ =
assert_sink_summarizable::<Sink>;` — the vision's block exactly. No
interaction body is ever generated (grep: no `impl Summarizable`); the
scratch crate proved the assertion bites (E0277 until hand-written impls
were added). Signal and Sema carry no associations section (lib.rs:48-60).

Defects, witnessed: a constrained kind in an association (`Sink.[
Conceivable<Datom> ]`) faults `Association at []`; a qualified type in an
association (`Vector<Sink>.[ Datomic ]`) silently drops the qualifier
and asserts on `Vector` (advgen/assoc-qualified-type.rs:40); an
intrinsic type in an association (`Text.[ Protosizable ]`) is emitted
unqualified as `Text`, not `protos::Text`
(advgen/intrinsic-assoc.rs:40; lib.rs:1581 uses `rust_ident` instead of
`resolve_type_name`), contradicting "an explicit import and an intrinsic
name mean the same thing".

### 5. Generated Datomic — correct where it compiles; recursion through a struct or Option does not compile; fault paths are dropped

Method: scratch crate at scratchpad/roundtrip with git deps at the exact
Cargo pins; every fixture's generated file added as a module; the
fixtures' undeclared names (SinkError, Clonable, Sendable, Serializable,
Summarizable, Fillable) supplied by a scratch prelude and hand-written
Sink interactions; `Self::Item` patched in streamable_kind (the only
edit). Round-trip tests in tests/roundtrip.rs and tests/recursive.rs.

Compiles and round-trips text → datom → value → text byte-for-byte
(11 tests, all pass): orchestrate Request/Response including
`Lock.{ MyLock 6329f1 [ /abs/path /abs/other ] “why I hold it” }`,
`Release.42`, `Observe.Locks`, `Observed.Locks.[]`,
`LockRejected.PathOverlap.{ /abs/path { 7 Other f1 [ /abs/path ] r } }`,
`ReleaseRejected.UnknownLockId`; multi-types Record/Report/SinkError/
LockId; the crate's own contract `Generate.{ /abs/file.ethos
/abs/out-dir }`, `Generated.[ /abs/out-dir/file.rs ]`,
`GenerationFault.{ … }`; a recursive enum `Tree.[ Leaf.Integer Node.{ Tree
Tree } Many.Vector<Tree> ]` (boxed through `TreeNode(Box<Tree>,
Box<Tree>)` + `impl_datomic_box!`); `Wrapped.{ Option<Integer>
Result<Text Integer> Vector<Option<Text>> }` with `{ Some.5 Ok.hello [
None Some.x ] }`; inline enum-in-enum `Nested.[ A.[ X Y.Integer ] B.{
Text } ]`; six-deep nesting with `Vector<Vector<Vector<Option<Result<Text
Integer>>>>>`. Struct positions are read in order and arity is checked
(lib.rs:1283-1289); bare and data variants both handled; aliases get no
impl (correct, they inherit).

Does not compile, witnessed:
- A recursive struct `Chain.{ Text Chain }` emits `pub struct Chain(pub
  protos::Text, pub Chain);` (E0072). Boxing is decided only in the Enum
  branch (lib.rs:1127); `fields_have_recursive_ref` exists but the Struct
  branch never consults it.
- Recursion through a container, `Maybe.Option<Tree>`, is not boxed
  (`is_direct_recursive` checks only a bare `Named`, lib.rs:1760) →
  E0072 "recursive without indirection".
- A duplicate type name is accepted silently and emits two definitions
  (E0428 and five E0119). A reference to an undeclared name is accepted
  silently (E0425 at compile time).

Non-compliant with the datomic ontology: the generated `incorporate_from`
never prepends the position index to a nested fault (lib.rs:1261,
1374-1390 pass faults through with `?`). Witnessed: a wrong value in
position 0 of the struct inside `Locked.{ … }` reports
`Corporate([], Value("notanumber"))`; a bad element inside a vector inside
`Observed.Locks.[ … ]` reports `Corporate([1], …)` — only datomic's own
Vec impl prepends. The Fault carries a Path so that a fault is situated;
generated code discards it at every struct position and every variant
body.

### 6. Signal and Sema — compliant; one silent drop

Observed: Signal reads `[imports] [requests] [responses] [types]`
(lib.rs:340-350) and generates `Request` and `Response` enums with
Datomic (gen/orchestrate.rs:301, 375; gen/ethos-zero.rs:80, 122). Sema
reads `[imports] [types]` (lib.rs:352-360). No Frame, Version, Refusal,
Reply, envelope or rkyv anywhere (grep over src, tests, fixtures,
Cargo.toml: none, except a negative test assertion and the no-version
test).

Defect, witnessed: an empty requests section generates no `Request`
enum at all (lib.rs:1613-1615; advgen/empty-requests.rs has only
Response). A signal without a query type is not a signal; this should be
a fault, not a silent omission.

### 7. CLI — the shape is right; it does not speak its own contract

Observed (src/main.rs): `ethos-zero 'Generate.{ /abs/file.ethos
/abs/out-dir }'` → `Generated.[ “…/record-types.rs” ]`; `<stem>.rs`
(main.rs:109-114); flags refused (main.rs:35, 45-50); no argument prints
the contract (main.rs:8-34) as the canonical one-line form with no
trailing newline.

Non-compliant, witnessed:
- The argument is walked by hand over Protoform (main.rs:62-88,
  `rejoin_text`), not incorporated through a generated `Request`. A
  quoted path (`“/git/…/record-types.ethos”`) is rejoined as the empty
  string (`rejoin_text` returns `String::new()` for Opaque, main.rs:143)
  and the CLI reports `GenerationFault.{ “” “No such file…” }`. Three
  children are accepted (`< 2`, main.rs:81). A relative path is accepted
  though the contract says `/abs`.
- Replies are `format!` strings, not textualized values of the contract's
  `Response` (main.rs:47, 57, 63, 68, 74, 79, 83, 91, 98, 101, 104, 118,
  122, 128). The contract declares `GenerationFault.{ Text Text }`; the
  flag/shape faults emit one field (`GenerationFault.{ “ethos-zero
  accepts one datom value and no flags” }`). The success reply always
  quotes the path; datomic's Text conceive would write a bare-safe path
  bare (the generated Response textualizes `Generated.[
  /abs/out-dir/file.rs ]`, witnessed in the scratch crate).
- Faults are not typed and not situated. The library's `Fault { path,
  problem }` (lib.rs:167-171) is constructed at 54 of 54 sites with
  `vec![]` (lib.rs, grep); the path is a field that is never filled. The
  rewrite report's "Paths into the protoform tree are more informative
  than text extents" describes a design that is not in the code. The CLI
  then flattens the fault to its Display string inside a Text
  (`“Section at []”`). The ethos `Fault` is not Datomic and implements
  neither `Pathed` nor `From<protos::Fault>`, so `Potential<File>` /
  `Actualizable` (protos c5594f9 lib.rs:891-917) cannot be used and the
  chain is hand-rolled in main.rs:96-105.
- Panic: an ethos name that is not a Rust identifier (`weird-name`)
  panics in `format_ident!` (lib.rs:1843; witnessed exit 101 with a
  quote-crate backtrace). `rust_ident` returns `Result` and never errs.

### 8. Self-hosting — not done, and the stated bootstrap problem is not real

Observed: no committed generated module; `self_description_reads` and
`self_description_generates` (tests/ethos.rs:454-470) only read and
string-check. The rewrite report says generation "requires the Signal
generation to produce compilable Rust against the crate's own types,
which is a bootstrap problem (the generated types depend on the crate
that generates them)."

Witnessed to the contrary: the generated ethos-zero.rs
(scratchpad/gen/ethos-zero.rs) references only `protos::` and
`datomic::`; it compiled in the scratch crate with no ethos-zero
dependency and round-tripped `Generate.{ /abs/file.ethos /abs/out-dir }`
and both responses. The generated contract depends on protos and
datomic, not on ethos-zero. There is no cycle for the library: lib.rs
generates without the contract; only main.rs consumes it.

Shape wanted (inference): commit `src/contract.rs` generated from
ethos-zero.ethos; `mod contract;` in main.rs; the CLI incorporates its
argument as `contract::Request` and textualizes `contract::Response`
(fixing item 7's quoted-path, arity and reply-shape defects at once); one
test regenerates from ethos-zero.ethos with the library and asserts
byte-equality with the committed file. No two-stage build is needed; if
lib.rs ever comes to use the contract itself, the committed file still
breaks the cycle, which is how every self-hosting compiler bootstraps.

### 9. Trait ontology — non-compliant

Observed: src/lib.rs has 76 free functions and 2 traits (`Canonicalizing`,
`Generating`, lib.rs:186-194); src/main.rs has 5 free functions and no
trait. Trait impls: `Conceivable<File>` for Delineation and Protoform,
`Protosizable for File`, `Generating for File`, `Canonicalizing for str`
— each a one-line facade over the free functions (lib.rs:200-204,
281-304, 736-745, 1022-1030). No inherent impl (grep `^impl [A-Z]`
without `for`: none) — compliant on that point. 61 closures in lib.rs,
most `|| fault(vec![], …)` and `.map(|p| bare_symbol(p)…)`. Import
resolution is a `HashMap<String, String>` built per file
(lib.rs:1033-1048) and threaded through 9 signatures; the root dispatch
is a string match (lib.rs:297-303). `Problem::Protos` is never
constructed. Dead bindings: `let _ = first;` (lib.rs:294), the no-op
`constraints` rebinding (lib.rs:562-566), `_parent` in two signatures
(lib.rs:1398, 1425).

Against Intent/mandatoryTraits.md ("Every method call in our Rust code
lives under a trait") and flows/995a164e/vision/rust.md ("We forbid
freestanding implementations", "I really despise free functions, and I
despise these inlined lambdas even more"): the crate is a free-function
reader and emitter. lib.rs reads as a data model followed by a parser,
not as an ontology: the reading of imports, declarations, variants,
type expressions, kinds, capabilities and associations is not a set of
kinds borne by Protoform, and the emission is not a set of kinds borne by
the declaration types. The engine does walk `File`, `TypeDeclaration`,
`Variant`, `KindDeclaration` enums variant by variant in the generator
(lib.rs:1053-1086, 1113-1156, 1170-1216) — compliant there.

Naming, not decidable from the vision alone: Vision/ethos.md Naming lists
Runnable, Textualizable, Structural, Embodied — all -able/-al/-ed; the
protos rewrite replaced `Printing` with `Textualizable`. `Canonicalizing`
and `Generating` are participles. The pinned protos.ethos itself declares
`Situating`, so participles exist in the stack. By the protos pattern
(the bearer is what undergoes the capability: Text is Protosizable), the
text would bear `Canonicalizable` and the File a kind named for what it
yields. The living should rule.

### 10. Legacy vocabulary, dead code, stale docs, gates

Source: clean of Library/Version/Frame/Reply/Corporal/Embodied/
Structural/Printing/datomize/realize/prospective/Portion (grep over src,
tests, fixtures, .ethos), save the negative assertions in
tests/ethos.rs:347 and :560-573. "Box" is accepted as a type constructor
(lib.rs:1700) and "Symbol" as an intrinsic (lib.rs:1728, 1752) — neither
is in the vision's intrinsic list.

Docs, all stale against 2.0.0: ARCHITECTURE.md describes `Library.{ver}`
/`Signal.{ver}`, `Actualizing`/`Emitting`, `Potential`, guillemet maps,
rkyv, Frame/Body/Refusal, `Structural`/`Corporal`/`datomize`; CLAUDE.md
describes `ethos_zero::read`/`emit` and "Library and Signal roots";
UPGRADES.md has no 2.0.0 entry and documents guillemets and Library;
README.md is current. No AGENTS.md exists. flake.nix sets six `ETHOS_*`
environment variables (flake.nix:36-41) that nothing reads (grep over
src, tests: none).

Gates, witnessed: `cargo test --offline` 47 pass (43 + 4). `cargo clippy
--offline --all-targets -- -D warnings` clean. `cargo fmt --check` fails
with 57 diffs (exit 1). `RUSTDOCFLAGS=-D warnings cargo doc` fails
(unclosed HTML tag `<File>` in lib.rs:5). `nix flake check --no-build`
evaluates; `nix build .#checks.x86_64-linux.fmt` fails (builder exit 1,
rustfmt diff) — so `nix flake check` fails on fmt and, by the local doc
result, on doc. The rewrite report's "nix build Success" is the package
only.

Coherence with the pinned dependencies, witnessed: of the four .ethos
files the flake pins, protos.ethos and protos-kinds.ethos generate (with
the `Self::` defect and a `Result<Sized, Fault>` yield from
`Incorporable<Sized>`), datomic.ethos faults (`TypeExpression at []`, the
inline `protos:Fault`) and datomic-kinds.ethos faults (`Kind at []`, the
constrained superkind). The rewrite report says these files were split
"to match the new variant-headed grammar"; two of the four do not read.

### 11. Adversarial inputs (scratchpad/adv, all witnessed)

| input | result |
|---|---|
| type referencing an undeclared name | silent; Rust E0425 later |
| duplicate type name | silent; Rust E0428 + E0119 later |
| capability with no yield (`run.[]`, `run.{ [ Text ] [] }`) | typed fault `TypeExpression at []`, unsituated |
| association to an undeclared kind | silent; Rust E0405 later |
| Signal with empty requests | silent; no Request enum emitted |
| head not one of the four (`Library`) | typed fault `Root at []` |
| sweet form with a comment on the head line | reads |
| deep nesting (six inline enums, five-deep containers) | reads, compiles, round-trips |
| canonical braced form | reads |
| trailing comment, no final newline | delineation fault (canonicalizer defect) |
| name not a Rust identifier (`weird-name`) | panic, exit 101 |
| lowercase type name (`record`) | silent; emits `pub struct record` |
| Rust keyword capability (`match`) | typed fault `Generation at []` |
| kind with `:` instead of `.` | silent acceptance |
| recursive struct, recursion through Option | silent; Rust E0072 later |
| `NAMES.Vector<Text>` associated constant | `const NAMES: Vec<protos::Text>;` |

No input produced a situated fault; no fault carried a non-empty path.

## Non-compliances ranked by severity, with the fix wanted

1. Faults are never situated: 54/54 `Fault` constructions carry an empty
   path; the CLI emits Display strings; generated `incorporate_from` drops
   position indices. Wanted: every reader fault carries the path of the
   protoform it faults on; generated struct and variant impls prepend the
   position to nested faults; the ethos Fault is Datomic and the CLI
   replies with the typed, textualized fault.
2. The trait ontology is absent: 81 free functions under 2 facade traits.
   Wanted: reading is kinds borne by Protoform/Delineation per context
   (imports, declarations, variants, type expressions, kinds,
   capabilities, associations), emission is kinds borne by the
   declaration types, resolution is borne by the import declarations —
   lib.rs reading top to bottom as the ontology; no free function, no
   lookup table, closures only where std's iterator adaptors demand.
3. Vision shapes that generate uncompilable Rust: associated types not
   `Self::`-qualified (Streamable, Conceivable); recursive struct and
   recursion through Option/Vector-of-self not boxed; bare-name
   self-aliases. Wanted: `Self::Name` for every associated type named in
   a capability; boxing decided by a recursion walk over the whole type
   expression for structs and enums alike; the bare-name form removed
   (or ruled by the living).
4. Kind identity ignored outside the declaration head: constrained
   superkinds and constrained kinds in associations fault; qualified
   association types drop their qualifier. Wanted: a kind reference is
   read as `Name<constraints>` everywhere a kind is named.
5. `nix flake check` fails (fmt, doc). Wanted: `cargo fmt` applied, the
   doc comment fixed, and the check witnessed green before the version
   stands.
6. The CLI does not speak its contract: hand-walked Protoform, quoted
   paths become empty, arity unchecked, replies as format strings with a
   shape that contradicts the declared `GenerationFault.{ Text Text }`.
   Wanted: a committed generated contract module; argument incorporated
   as `Request`, reply textualized from `Response` (item 8's shape).
7. Silent acceptance where a fault is owed: duplicate type names,
   undeclared names and kinds, empty requests section, a kind with the
   wrong separator, a non-identifier name (panic). Wanted: typed situated
   faults for each; the reader validates the file as a whole (names
   declared or imported, unique) before generation.
8. Self-hosting not done though the bootstrap is not real (item 8).
9. Invented forms and names: synthetic `ParentVariant` structs for inline
   struct variants; `Box` and `Symbol` accepted; bare-name self-alias.
   Wanted: tuple variants holding the positions directly; only the
   vision's intrinsics, or a ruling adding these.
10. Stale documents: ARCHITECTURE.md, CLAUDE.md, UPGRADES.md, dead
    `ETHOS_*` flake variables; the pinned datomic .ethos files do not read.
    Wanted: docs rewritten to 2.0.0 or deleted, the flake variables
    removed, and the dependency .ethos files made to read with the tool
    that pins them (or the pins dropped).
11. Canonicalizer: closing brace appended into a trailing comment.
    Wanted: the closer on its own line.

## Decisions the rewrite took on flow authority that the living would want to see

- Sema as `[imports] [types]` with Datomic implied for a list of types.
  The vision says a sema variant "holds a storage (record) type with its
  implied associated kinds" — singular, with kinds beyond Datomic
  unstated. Reason to surface: the rewrite shaped a variant the vision
  left open, and no consumer exists to correct it.
- Inline struct variants generate a synthetic named struct. Changes the
  Rust API of every enum with a `Name.{ … }` variant, and the generated
  protos/datomic shapes diverge from the hand-written crates.
- `Clonable`/`Sendable`/`Serializable` emitted unmapped, where the
  vision's example Rust shows `Clone`/`Send`/`Serialize`.
- Derives added to every generated type (`Clone, Debug, PartialEq, Eq`,
  `Copy` for unit-only enums), and `#![allow(dead_code)]` at the top of
  every module. Not in the vision's Rust; a reasonable contact point, but
  a policy the living has not seen.
- Capability inputs named `input` / `input_0`, `input_1`. The vision shows
  `input` for one; the numbered form is the rewrite's.
- `Canonicalizing` / `Generating` as participle kind names (item 9).
- `Fault { path, problem }` presented as situated by path; in the code the
  path is never set (item 7).
- The no-argument CLI prints the canonical one-line form rather than the
  sweet file, without a trailing newline.
- Self-generation deferred as a "bootstrap problem"; witnessed not to be
  one (item 8).

## Dependencies on the current protos/datomic shape (for the adapt pass)

Generated code (src/lib.rs): `datomic::Datom::Variant(head,
protos::Separator::Period, Some(body))` patterns at 1373, 1379, 1389 and
construction at 1411-1418 (three-field Variant with `Option<Box<Datom>>`
and a Separator — changes when Variant always carries a body with no
separator); `Datom::Bare` for unit variants at 1364, 1405;
`Datom::Struct(vec![…])` at 1277, 1283, 1287; `datomic::Fault::Corporate(
vec![], datomic::Problem::Arity(..))` and `Problem::Shape(
datomic::Expected::Struct|Variant, other)` at 1288, 1290, 1338, 1652
(changes when faults are situated by path and extent);
`datomic::Datomic::incorporate_from` at 1261, 1281, 1297, 1335, 1345,
1374, 1380, 1390, 1649, 1659 (changes if the Datomic kind's shape
changes); `impl protos::Conceivable<datomic::Datom> … type Fault =
Infallible` at 1274-1279, 1326-1333, 1640-1647; `impl
protos::Incorporable<T> for datomic::Datom` at 1294-1299, 1342-1347,
1656-1661; `datomic::impl_datomic_box!` at 1132; `datomic::Meaning` at
1733; `protos::{Text, Integer, Decimal, Boolean, Symbol}` at 1728-1730.
Reader/CLI: `protos::{Delineation, Enclosure, Head, Protoform,
Separator}`, `Head::Qualified`, `Delineation { protoforms, situation }`,
`protos::Situation::new()`, `protos::Path` (lib.rs:13, 169, 278-317,
736-745, 1793-1832); main.rs `fault.extent.0/.1` at 30, 57, 98,
`Protoform::Enclosed(protos::Enclosure::Braced, ..)` at 78. Tests:
string assertions on `impl protos :: Conceivable < datomic :: Datom >`,
`incorporate_from`, `impl protos :: Incorporable < Record > for datomic ::
Datom` at tests/ethos.rs:358-369.

## Unknowns

- Whether the living wants the bare-name form in a types section, inline
  `source:Name` qualification in type positions, `Box`/`Symbol` as
  intrinsics, the std-trait name mapping, or the derive policy.
- Whether participle kind names are acceptable given `Situating` in the
  pinned protos.ethos.
- Whether the pinned protos-kinds.ethos's `Incorporable<Sized>` and
  by-value `incorporate(self)` (no ethos receiver form exists for
  by-value self) are shapes the living intends; ethos has `.` `!` `:`
  only.

## Sources

- /git/github.com/LiGoldragon/ethos-zero at a2e8eafcd45c: src/lib.rs,
  src/main.rs, tests/ethos.rs, ethos-zero.ethos, fixtures/*.ethos,
  Cargo.toml, flake.nix, README.md, ARCHITECTURE.md, CLAUDE.md,
  UPGRADES.md, .gitignore — read whole.
- /git/github.com/LiGoldragon/protos: `git show c5594f9d6f73:src/lib.rs`;
  `git show 2cb88849f3b1:{protos.ethos,protos-kinds.ethos}`.
- /git/github.com/LiGoldragon/datomic: `git show 2c2e2073fd34:src/lib.rs`;
  `git show cf59b01bbbc8:{datomic.ethos,datomic-kinds.ethos}`.
- Authority: /home/li/primary/Vision/ethos.md, Vision/protos.md,
  Vision/datom.md, Vision/ethosMonolith.md, Intent/mandatoryTraits.md,
  Intent/data.md, flows/995a164e/vision/{rust,layerMatching,kinds,
  concept,contexts,explodedForm}.md,
  flows/5abf3be8/vision/sectionsExistToConferTraits.md.
- The rewrite's account: flows/1a6ca4/reports/rewriteEthosZero.md
  (claims checked against the code; none taken as given).
- Witness runs: `cargo test --offline`, `cargo clippy --offline
  --all-targets -- -D warnings`, `cargo fmt --check`, `RUSTDOCFLAGS=-D
  warnings cargo doc --offline --no-deps`, `nix flake check --no-build`,
  `nix build .#checks.x86_64-linux.fmt`; generation of every fixture and
  every adversarial input with target/debug/ethos-zero; scratch crate
  /tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/roundtrip
  (generated modules under src/, tests/roundtrip.rs, tests/recursive.rs;
  inputs under ../adv, outputs under ../gen, ../advgen, ../depsgen).
