# Second audit: protos 0.18.0 and datomic 0.12.0 against the distilled vision

Audited: protos `3b29b61e431b` (main, /git/github.com/LiGoldragon/protos) and datomic
`83d92f9d5047` (main, /git/github.com/LiGoldragon/datomic), every tracked file read
whole (`src/*.rs`, `tests/*.rs`, both `.ethos` files per crate, Cargo.toml, flake.nix,
README.md, .gitignore, rust-toolchain.toml, the proptest regression file). Method: read
first; then `cargo test`, `cargo clippy --all-targets -- -D warnings`, `cargo fmt
--check`, `cargo doc` (`-D warnings`) and `nix flake check` in both; then a scratch crate
(`scratchpad/adv2/tests/{situ,deep,esc,vision,adv,layers1-5}.rs`, `src/bin/depth.rs`)
driving both public APIs with inputs of this audit's own; then ethos-zero 2.0.0
(`a2e8eaf`, extracted by `git archive` into `scratchpad/ez2`) over the four `.ethos`
files. The second-pass report (`reports/rewriteProtosDatomic2.md`) was read after the
code and is cited only where its claims were checked. *Witnessed* = seen in code or a
run; *inference* = this audit's reading; unknowns are named.

Line references: P = `protos/src/lib.rs`, PD = `protos/src/delineation.rs`, PT =
`protos/src/textualization.rs`, PA = `protos/src/actualization.rs`, D =
`datomic/src/lib.rs`, DT = `datomic/tests/datomic.rs`, PTT = `protos/tests/delineation.rs`.

One event to record first: this audit's own unbounded run of
`brackets(99_998).protosize()` in a debug build reached ~24 GB RSS plus swap and was
OOM-killed, taking the harness scope with it. Every later probe ran under `ulimit -v
4000000` in release with a timeout. The memory is itself finding 1 below.

## 1. The first audit's thirteen items

| # | First-audit item | Status in the code | Witness |
|---|---|---|---|
| 1 | Non-structural faults never situated | **Not closed.** Conceptual faults are situated; Corporate faults are not, except by accident | Datom root conceived at `[0]` (D248, D257) and the delineation situates the top-level protoform at `[0]`; but every `incorporate_from` starts its path at `vec![]` (D511, D615, D657 …) and no caller prepends the root's 0, so `Vec<i64>` on `[ 1 x ]` yields `Corporate([1], ..)` while the delineation holds `[0, 1]`: `Situated(None, ..)` (scratch `situ.rs`, 24 of 28 non-structural cases `None`). The four that carry an extent (`Some.x`, `Ok.x`, `Some.Some.x`, `Some.42.x`) carry the *wrong* one: path `[0]` is the whole text, so `Some.x` reports extent (0,6) = `Some.x`, not `x`. Struct/Option/Result/Box do prepend now (D611, D655, D694, D1126; test structs DT31-35) — paths are right relative to the root. No test in DT calls `actualize` or asserts a `Situated` extent; the first audit's `actualize` helper and its tests were deleted (git diff cf59b01..83d92f9) |
| 2 | Untrusted text can abort the process | **Not closed; changed shape.** Stack recursion in the delineator is gone; memory is now quadratic in nesting depth, and the concept layer is still recursive | Delineation peak RSS, release, bounded: 1 000 brackets 10.5 MB; 8 000 342 MB; 10 000 550 MB; 16 000 1.41 GB; 32 000 6.25 GB; 50 000 allocation failure under a 4 GB bound (scratch `scale.rs`, `depth.rs`). ×4.1–4.4 per doubling: quadratic. Cause (read): every `Frame` clones the full `Path` (PD414, PD205-209) and every situation entry is a full-length `Vec<Integer>` (PD69, PD93, PD221), so n nested structures store n²/2 integers — `Situation = BTreeMap<Path, Extent>` (P41) is quadratic by construction. A 100 000-long head chain likewise (PD90-94: body paths of length depth+1 each): killed at 12 GB (scratch `deep.rs` d4). Recursion: `Datom` textualize/`to_protoform` (D134-161, PT80-96 for Enclosed) overflows an 8 MiB main stack between 50 000 and 100 000 nested vectors; `Datom` drop between 200 000 and 400 000; `conceive_at` (D191-242) and `Protoform::clone` recurse; `Protoform` drop is recursive and reachable through `delineation.protoforms.clone()` (the only way to take the protoforms, since `Delineation` has `Drop`, P365) and through `Head::Qualified` constraints, which the iterative Drop skips (P370-372) |
| 3 | Inner structural faults swallowed | **Closed** | `[ { 1 ] }` → `Unopened` at (6,7); `{ 1 ` → `Unclosed(Braced)` (0,4) (scratch `situ.rs`). Closed by deleting `MissingBody`/`MissingHead` (P119-126) — see decisions. New fabrication: the depth limit reports `Problem::Unclosed(enc)` at (pos, pos+1) (PD406-411, PD598-603, PD670-675, PD744-749) for an enclosure that is not unclosed |
| 4 | Layer table not borne as the vision states | **Mostly not closed** | Only `Datom` bears `protos::Textualizable` and `protos::Protosizable` (D163, D176). Corporate types still do not: `<i64 as protos::Textualizable>::textualize` fails to compile (scratch `layers1.rs`, E0277); they get `Datomic::textualize`, the same-named default method the first audit named (D273). `Incorporable` on Text/Protoform absent (`layers4.rs`, E0277). `Potential<Delineation>::actualize` does not compile (`layers2.rs`); `Potential<i64>::actualize` does not compile without the concept parameter (`layers5.rs`); the identity `impl Incorporable<Datom> for Datom` remains (D1096-1116) |
| 5 | Reader not under the trait ontology | **Closed by the letter, not the intent** | 0 free functions, 0 inherent impls in either `src/` (grep); protos flake carries the two grep checks (protos flake.nix:26-39). But: the reader is `struct Delineator { source, pos, stack }` (PD272) with the old inherent methods regrouped under private traits `Traversing`, `Delineating`, `BoundaryReading`, `BareRunHandling` (PD279-816); `parse_bare_run` and `attach_body_to_deepest` became static capabilities on zero-sized structs `BareRunParser`, `BodyAttacher` (PD33, PD116) — the "behavioral noun without data" datomic's own `no-zst-behavior` check forbids (datomic flake.nix:44) and protos's flake does not carry. The `other =>` arm still fabricates an empty head (PD135-143). `Identifying`/`Recognizing` are a `find` over a hand-listed `let variants = [...]` array, written five times (P286, P293, P298, P305, P310) — the roster the living rejected, now local. Glyphs live once for delimiters and separators (P240-282); the comment glyph `';'` is a literal at PD312, PD332, PD739 and D333, the escape glyph `'\\'` at PD496-501 and PT27-28. datomic's own delimiter table is gone (D319-337 uses `Recognizing`) |
| 6 | Parenthesis escaping does not round-trip | **Closed for round-trip; open as vision** | Property test PTT78-89 over `[ -~]{0,100}`; this audit's `\`, `(`, `)`, `\(`, `\\)`, trailing `\`, nested, curly quotes inside, empty, newline all round-trip (scratch `esc.rs`). But the escape is unconditional (PT21-34): balanced pairs are escaped too, so Vision/datom.md's Note textualizes as `{ Ada (The build passed on the third try \(after two timeouts\)) }` and Standup likewise (scratch `vision.rs`) — the vision says "a parenthesis pair inside it is structure of its own ... an unbalanced parenthesis inside it is escaped". U+201D: no type, no refusal, no fault — a module doc comment (PT5-6). `"a”b".textualize()` → `“a”b”`, which reads back as `Unopened` (esc.rs); `Datom::Text("a”b").protosize()` **panics** at D171 (`expect("canonical text delineates")`), as does `Datom::Bare("{").protosize()` |
| 7 | `.ethos` files break the Declaration | **Partly closed** | Types and kinds now in separate variant-headed files, no version, imports first, associations third (protos.ethos:13, datomic.ethos:8) — closed. Still undefined by Vision/ethos.md Declaration: `Situated<Sized>.{ Option<Extent> Sized }` (a generic *type* with a constraint; "in ethos there are no generics, only kinds"; `Sized` used as a type in a position and in yields `Result<Sized Fault>`, protos-kinds.ethos:9-11); complex kinds with three sections instead of four (protos-kinds.ethos:8-11; Declaration: superkinds, associated types, associated constants, capabilities); inline `Structural.protos:Fault` with `Fault` absent from the import list (datomic.ethos:2, 7); `Symbol` used undeclared (protos.ethos:7). Unfaithful to the Rust: `Glyphing.glyph.[ Text ]` yields `char` (P155); `Identifying.identify:[ Option<Self> ]` and `Recognizing.from_opener:` omit their `char` input (P169, P175); `Situating.situate.{ [ Integer ] ..}` takes `&[Integer]` (P227); `Delineation.{ Vector<Protoform> }` still omits `situation` (P110); `Pathed`, `Potential`, `Path`, `Situation` absent; `Datomic` omits `Fault = Infallible` (D268); associations for `Vec`, `Option`, `Result`, `Box`, `protos:Problem`, `protos:Fault` absent. ethos-zero 2.0.0 run: `protos.ethos` generates (with `pub Sized` as a field type); `protos-kinds.ethos` → `GenerationFault "Kind at []"` (bisected to the three-section kinds); `datomic.ethos` → `"TypeExpression at []"` (bisected to `Structural.protos:Fault`); `datomic-kinds.ethos` → `"Kind at []"` (bisected to the constrained superkind `Conceivable<Datom>`). ethos-zero 2.0.0 itself generates against datomic 0.11's `Datom::Variant(String, Separator, Option<Box>)`, so nothing it emits compiles against 0.12.0 |
| 8 | `cargo fmt --check` fails | **Closed** | Both clean (witnessed) |
| 9 | Stale documents and tracked `result` | **Closed** | Four documents deleted in each crate; README rewritten; `result` untracked and in `.gitignore`; no legacy vocabulary in any tracked file (grep for corporal, embodied, datomize, guillemet, portion, MissingBody, Signal., Library., dotos, realize, ShapeDefined, Prospective) |
| 10 | Scores example not in tests | **Partly closed, with a regression** | `Observed.Locks.[]` and `Success` round-trip typed (DT287-298). `{ Ada [ 12 7 -3 ] }` is still not in the tests verbatim: `scores_example` (DT254) reads a hybrid `{ Ada [ 12 7 -3 ] { “12 Rue de la Paix” Paris 75002 } }`. The vision's Person (with `born` and `roles [ Author Reviewer.{ 2024 17 } ]`), Note, Remark, Standup and Lock typed tests that 0.11.0 had were **deleted** (40 tests → 29; git diff cf59b01..83d92f9). This audit ran them: Person and Scores round-trip verbatim; Note and Standup read but do not print verbatim (item 6) |
| 11 | Ascent computes no spans | **Implemented as a re-read; wrong; unused; can panic** | `Protosizable for Datom` (D166-173) prints then delineates. Nothing on the ascent path calls it: `Datomic::textualize` (D273) and `Textualizable for Datom` (D176) go `to_protoform().textualize()` and compute nothing. Its output inherits the reader's situation bug (section 3): for `{ 42 Some.{ “a b” } }` it situates `[0,1]` as `Some` (5,9), not `Some.{ “a b” }`, and has no entry for `[0,1,0]` (scratch `situ.rs` ascent_situation). The only test (DT471-483) asserts `is_some()` on three bare paths. The `.expect` at D171 panics on any Text carrying U+201D |
| 12 | Two forms for a variant carrying nothing; `Head::Qualified` leak | **Half closed** | `Datom::Variant(Head, Box<Datom>)`, nothing-carrying variants are `Bare` (D21-34) — closed. The fake datoms remain: `Datom::Bare("Angled")` (D226), `Datom::Bare("Qualified")` (D237), now under a new `Expected::Bare`. `Problem::Separator` (D71) is never constructed (grep) — a dead variant kept alive by its own datomization (D780, D814) |
| 13 | Hand-written derives, triplicate impls, closures | **Derives closed; the rest traded** | All `#[derive]` now (P34-146, D20-87). The triplicate blocks became `impl_datomic_scalar!` fed by **two closures per type** (D477-503; eleven uses, 22 closures) — "I despise these inlined lambdas even more" (flows/995a164e/vision/rust.md). 17 `map_err(|f| f.prepend(i))`; 24 `.unwrap()` in D (15 of them on `Infallible`) |

## 2. The passes as implemented

**protos.** `Protosizable for Text` (PD822) constructs a `Delineator` and calls
`delineate` (PD342-452): a character loop over `pos` with an explicit `Vec<Frame>` stack,
classifying each character by asking the enums (`Enclosure::from_closer` …), then
branching into `handle_bare_run` (PD560-646, 87 lines with a five-deep `if let` ladder),
`handle_bare_then_angle`, `pop_frame`, `handle_post_qualified`, `set_or_combine_pending`.
Bare runs are parsed by `BareRunParser::parse_bare_run` (static, on a ZST) and chains
re-attached by `BodyAttacher::attach_body` (static, on a ZST, still with the empty-head
fabrication at PD137). This is a procedural reader with a trait vocabulary over it; the
kinds are borne by the reader's private struct or by nothing, not by the layer's type.
Where an enum is walked variant by variant it is `Delimiting`/`Glyphing` (P240-282: real,
and the single home of eight of the ten glyphs) and the five `variants` rosters
(P286-311). `Textualizable for Protoform` (PT114-134) is iterative over the head chain
only; `LeafTextualizing` (PT77-111) recurses through enclosures and `Head::Qualified`
(PT58-67). `Actualizable for Potential` (PA159-186) is the chain, with three `map_err`
closures.

**datomic.** `Conceiving::conceive_at` (D191-242) walks `Protoform` variant by variant —
this one is what the vision describes — but it hangs on a private kind with a path
parameter, not on `Conceivable<Datom> for Protoform`, which delegates (D244-250).
`Protosizing::to_protoform` (D130-161) walks `Datom` variant by variant. The scalars are
closures in a macro. `BareSafety::is_bare_safe` (D319-365) decides whether a Text prints
bare by **running the whole delineator on the string and conceiving it** (D354-358): the
ascent runs the reader once per Text field, then (if `Datom::protosize` is used) once
more over the whole output.

**Counts.** Free functions: 0 and 0. Inherent impls: 0 and 0. Closures: protos 8 (five
`find`, three `map_err`); datomic 52 sites (22 macro arguments, 17 `prepend`, 5
`is_ascii_digit`/`map_err`, rest in match guards). Tables/constants carrying what belongs
in impls: five `let variants = [...]` rosters (P286-311), `DEPTH_LIMIT` (PD12), literal
`';'` ×4 and `'\\'` ×5, the variant-name strings `"Some"/"None"/"Ok"/"Err"/"True"/"False"`
written twice each (conceive and incorporate, 11 sites). ZSTs bearing behaviour: 2
(PD33, PD116). Private trait facades: protos 10, datomic 7.

**Naming.** Vision/ethos.md Naming gives `Runnable, Textualizable, Structural, Embodied`:
-able/-al/-ed qualifiers of the bearer. `Texted` fits. `Glyphing`, `Delimiting`,
`Identifying`, `Recognizing`, `Prepending` and the seventeen private `-ing` kinds
(`Traversing`, `Framing`, `Attaching`, `BareRunParsing`, `Escaping`, `Spacing`,
`Protosizing`, `Conceiving`, `IntegerParsing`, `DecimalPrinting`, …) name the act, not
the bearer; `BareSafety` is a noun. Whether -ing counts as qualifier-naming is not decided
by the vision (unknown). Weight: `Glyphing`/`Delimiting` carry theirs (one home for the
glyphs). `Identifying`/`Recognizing` are the roster in disguise. `Prepending` carries a
real rule but is public and in the `.ethos` for what is a two-line path insert.
`Escaping` = the old `escape_parens_for_print`; `Traversing` = the old `peek_char/
advance_char/skip_whitespace_and_comments`; `BareRunParsing` = the old `parse_bare_run`;
`Attaching` = the old `attach_body_to_deepest` (first audit P337, P438, P510, P851): the
old helpers renamed.

## 3. Situation

**Convention.** Stated nowhere in either crate as a sentence. In the code: the
delineation puts top-level protoform *i* at `[i]`, children of an enclosure at `[..,
j]`, a headed body at `[.., 0]` (PD92, PD260); datomic conceives the single root at `[0]`
(D248) and prepends `0` for a variant body (D197) — so far agreeing — but every
`incorporate_from` starts at `[]` and no one supplies the root's `0` (section 1, item 1).
Two crates, two conventions, and the fault paths of the corporate layer are in the
second.

**The delineation's own map is wrong for every headed structure whose body is enclosed,
opaque or qualified** (scratch `adv.rs`, `situ.rs`; every case below witnessed):

| text | entry | witnessed | wanted |
|---|---|---|---|
| `Reviewer.{ 2024 17 }` | `[0]` | `Reviewer` (0,8) | whole (0,20) |
| same | `[0,0]` (the struct) | absent | (9,20) |
| `Some.(x)` | `[0,0]` | absent | (5,8) |
| `A.B<C>.D` | `[0]` | `D` (7,8) | (0,8) |
| `x.y.z<w>.v` | `[0]`, `[0,0]`, `[0,0,0,0]` | `v`, `y`, `w` | `x.y.z<w>.v`, `y.z<w>.v`, `z<w>.v`/`v` |
| `a<b>.{ 1 }` | `[0,0]` | `b` (the constraint) | `{ 1 }` (the body) |
| `{ 42 Some.{ “a b” } }` from the ascent | `[0,1]` | `Some` (5,9) | (5,19) |

Causes (read): (a) `add_child` with a pending chain pushes `(child_path, chain_start..end)`
and then extends with `pending.sub_situations`, which holds the same `child_path` with
the head-only extent (PD218-226 with PD69); the later `insert` into the `BTreeMap` wins
(PD445-447). (b) The body of a pending chain gets no entry: `pop_frame` passes `vec![]`
(PD702) and the pending branch of `add_child` records nothing at `body_path`. (c)
`Head::Qualified` constraints are pathed as `[.., 0, k]` (PD677, PD683), the same slots as
the body. The only situation tests (PTT587-611) use bare bodies, where none of this
shows.

**Innermost fault.** Structural: yes (item 3). Corporate: the innermost path is reported
(`[3,1,0,1]` for `x` inside `Reviewer.{ 2024 x }` inside `roles`), then not found.

**"Computed on the way out".** The report: situation on ascent by textualize-then-
delineate, "cost is a full re-parse, justified by the vision's multi-pass principle".
Judged against Vision/protos.md — "Spans are found on the way in and computed on the way
out"; "Extents are not intrinsic to objects; when we textualize, these can be computed" —
this audit's reading is that *computed* means computed by the writer: the textualization
pass knows the offset of every piece as it emits it, so extents fall out of the write at
no extra cost and cannot disagree with the text. Re-reading the emitted text is a
shortcut, and a poor one: it doubles the ascent's cost (and, with the quadratic map,
its memory), it makes a pass that "cannot fault" depend on one that can (the `expect`
panic at D171 is the symptom), it inherits every reader bug (table above), and it is not
on any path a consumer uses (`textualize` never calls it). Multi-pass in the vision is
several *distinct* passes, each a mental model; running the same pass twice is not that.
The wanted shape is a textualization that yields text *and* situation from one walk.

## 4. Recursion bounded (all runs bounded, release unless stated)

| probe | result |
|---|---|
| 100 000 nested `[` (opener only, debug, first unbounded run) | faulted `Unclosed(Bracketed)` after 59.5 s — then the 99 998-pair run was OOM-killed |
| 99 998 bracket pairs, delineate | allocation failure under 4 GB (extrapolated ~60 GB); 32 000 pairs = 6.25 GB |
| 100 000-long head chain, delineate | killed at 12 GB (`deep.rs` d4); 10 000 (PTT689) passes |
| 100 000-element flat vector as `Vec<i64>` | ok, 41 MB, 0.1 s |
| `Datom` 100 000 nested vectors, textualize | **stack overflow, SIGABRT** (8 MiB main thread); 50 000 ok |
| `Datom` 100 000 nested, protosize (ascent situation) | **stack overflow** |
| `Datom` 100 000 nested, drop | ok on the main thread; overflows at 400 000; **overflows at 100 000 on a 2 MiB test thread** (`deep.rs` d7c) |
| `Protoform` 100 000 nested, drop (built or cloned) | **stack overflow** (`deep.rs` d8b) — reachable: `delineation.protoforms.clone()` is the only way to own the protoforms since `Delineation: Drop` |
| `Delineation` 99 998 deep, drop | not reachable: cannot be built within memory |
| 50 000 nested `A<A<…>>` (qualified) | allocation failure (memory), `deep.rs` d9 |

So the report's "none aborts" holds for nothing at 100 000 except the flat vector; what
changed is that the delineator now dies of memory rather than stack. The recursive
`Protoform` Drop is reachable. The 2 000/10 000 depths the tests use (PTT679-701) are
below every threshold.

## 5. Escapes

Read (PD487-532): `\(`, `\)`, `\\` unescape; `\x` keeps the backslash; balance counted on
unescaped parens; lone `\` at end → `UnclosedBoundary`. Print (PT21-34): `(`, `)`, `\`
each escaped, always. Property test PTT78-89 (printable ASCII, ≤100 chars) and this
audit's cases all round-trip; `(a\)` and `((a)` fault correctly, `(a))` faults `Unopened`
at the last `)`. Against the vision: the balanced inner pair of a Meaning is markup that
should survive verbatim and only an unbalanced one be escaped; the canonical print
escapes both, so the two Meaning examples in Vision/datom.md are not canonical text of
their own values. U+201D: witnessed above (item 6, item 11); the "typed decision" is a
comment.

## 6. Datom

One form per meaning: yes (D21-34). Non-dot separators: `a:b`, `a!b`, `name:first` in a
Text position read and print bare (DT386, scratch); `Some:42` as `Option` faults
`Shape(Variant, Bare("Some:42"))` — reasonable, but `Problem::Separator` is now
unreachable. Qualified head in a Text position: `Vector<Text>` → `Conceptual Shape(Bare,
Bare("Qualified"))` — the fault is right (angles are delimiters, the word is not bare),
the reported datom is fabricated. In a variant position `A<x>.{ 1 2 }` → `Shape(Variant,
Variant(Qualified(..), ..))`. Integer: `+1`, `01`, `-0` refused, `-9223372036854775808`
accepted (witnessed). Decimal: point mandatory, digits both sides, no exponent (`1e300`
refused), leading zero refused, shortest print (`1.50` → `1.5`,
`123456789012345678901234567890.5` → `123456789012345680000000000000.0` — a bare
30-digit print is a decision, see section 10). `true` refused, `True` accepted. Vision
examples, by name in DT: Reply ×3 (DT261-284), `[ 0 42 -42 ]` (DT405), `Observed.Locks.[]`
(DT287), `Success` (DT294) present; **Person, Scores (verbatim), Note, Remark, Standup
absent** (deleted this pass). All nine run typed by this audit: seven verbatim, Note and
Standup not (section 5).

## 7. `.ethos` self-descriptions

Section 1, item 7. Summary: valid under the Declaration in their sectioning; invalid in
five forms the Declaration does not define; unfaithful to the Rust in eight capabilities
or types; three of four refused by ethos-zero 2.0.0, and the fourth generates a
`Situated(pub Option<Extent>, pub Sized)`.

## 8. Legacy vocabulary, dead code, docs, artifacts, checks

Vocabulary clean (grep list in item 9). Dead: `Problem::Separator` (D71); `Expected::Bare`
exists only to carry fabricated datoms; `proptest` is a datomic dev-dependency with no
proptest test; the `Modules` banner is duplicated at P357-359 and P378-380. Tracked
artifacts: none (`result` gone). `cargo test` 47/29 pass; clippy, fmt, doc clean in
both; `nix flake check` **passes in both** (witnessed, ~10 min, substituted from
prometheus). Note that protos's flake lacks datomic's `no-zst-behavior` check, which
PD33/PD116 would fail.

## 9. Solidity beyond the checklist (adversarial, witnessed in `adv.rs`)

- `a..{ 1 }` → `Headed("a.", {1})`: a head symbol containing a separator, while `a..b`
  stays `Bare("a..b")` — the trailing-separator path (PD573-631) and the split rule
  (PD36-59) disagree.
- `a.{ 1 }.b`, `a.“x”.b`, `a.(b).c`, `{ 1 }.a`, `<a>.b` → the trailing `.x` becomes a
  sibling `Bare(".b")`; `a<b>c`, `a<b>.c<d>e` → two siblings with no whitespace between
  them. No fault, no whitespace, two values: a datom `Some.{ 1 }.x` in an `Option`
  position reads as `OneValue` rather than naming the stray `.x`.
- Depth-limit fault reports `Unclosed` of an enclosure that is closed (PD406-411).
- `Delineation: Drop` (P365) forbids moving `protoforms` out; every consumer that wants
  to own them clones a recursive tree.
- `Potential::protosize` and `actualize` copy the text on every call (PD840, PA169).
- Text position: `a;b` reads as `a` silently (comment rule) — consistent, worth knowing.
- Accepted that should fault per the position rule: none found beyond the sibling cases.
  Faulted that should be accepted: `a<b` as a Text — `<` is a delimiter, so quoting is
  the rule; consistent.

## 10. Remaining non-compliances, ranked, with the fix wanted

1. **Memory quadratic in nesting depth; a 200 KB text needs ~60 GB** (section 4). Wanted:
   situation storage linear in the size of the text — extents kept beside the tree they
   describe (per node, positionally), paths derived by walking, no full-path clone per
   frame or per entry; a test that delineates 100 000 nested brackets in bounded memory
   and time.
2. **Corporate faults are not situated** (item 1). Wanted: one path convention written
   once (in Vision or the crate's ethos) and honored by delineation, conception and
   incorporation; `actualize` on `{ Ada 1990 { … } [ Author Reviewer.{ 2024 x } ] }` as
   Person yields the extent of `x`; a test per container (Struct, Vector, Option,
   Result, Box, Variant) asserting extent, through `actualize`.
3. **The delineation's situation is wrong for headed structures with enclosed, opaque or
   qualified bodies** (section 3). Wanted: `[0]` of `Reviewer.{ 2024 17 }` is the whole,
   `[0,0]` the struct; qualified constraints pathed apart from the body; tests for
   headed+enclosed, headed+opaque, headed+qualified, chain+enclosed.
4. **The ascent still computes no situation on its own; the re-read path is wrong, unused,
   and panics** (item 11, section 3). Wanted: textualization that emits text and
   situation from one walk; `Datom::protosize` never `expect`s; the re-read removed.
5. **Concept-layer recursion: `Datom` textualize/protosize/conceive/drop and `Protoform`
   drop/clone overflow** (section 4). Wanted: either iterative walks with a depth bound
   stated once, or a depth bound at delineation low enough that every later pass is
   safe on every thread — and stated as such.
6. **The layer table is still not borne as the vision states** (item 4). Wanted as in the
   first audit: `protos::Textualizable` on every Datomic type (generated, not a default
   method), `Incorporable` through the chain, `Potential<T>` actualizing for
   Delineation and for corporate types without a second parameter, the identity impl
   gone.
7. **Unrepresentable U+201D is a comment, not a decision** (item 6). Wanted: the living's
   ruling (refuse at construction, escape, or fault on the way out — the third
   contradicts "cannot fault"), then a type that enforces it; no ascent output that
   the reader refuses.
8. **Balanced parentheses escaped in Meaning** (section 5). Wanted: the vision's rule —
   inner balanced pairs verbatim, unbalanced ones escaped — with the round-trip property
   proven for that rule; or the vision reopened.
9. **Reader remains procedural under trait names; ZST bearers; variant rosters ×5; closure
   macro** (section 2, item 13). Wanted: the delineator as kinds borne by protos's own
   types (a `Frame`/`Delineator` may carry data, but its capabilities should read as
   the vision's context-switching parse: each shape announcing its type, that type's
   context reading until its completing shape); no zero-sized bearers; variant
   enumeration from one place; `impl_datomic_scalar!` replaced by generated impls or
   plain impls, no closures; protos flake carrying `no-zst-behavior`.
10. **`.ethos` files** (item 7). Wanted: only Declaration-defined forms; generic types
    either given a form in Vision/ethos.md or left out with the omission recorded;
    four-section complex kinds; every capability's inputs and yield as in the Rust; every
    borne kind listed; `Fault`/`Problem`/`Symbol` imported or declared; a freshness test
    once ethos-zero speaks 0.12.0.
11. **Vision-example tests deleted; Scores not verbatim** (item 10). Wanted: Person,
    Scores, Reply ×3, `[ 0 42 -42 ]`, Note, Remark, Standup, `Observed.Locks.[]`,
    `Success`, each typed, verbatim, and named after its example.
12. **Fabricated datoms in faults; dead `Problem::Separator`; depth-limit reported as
    `Unclosed`** (items 12, 3). Wanted: a fault that names the protoform kind found
    (`Angled`, `Qualified`) and a `Problem` for the depth bound; dead variants removed.
13. **Two-values-without-whitespace cases** (section 9). Wanted: a ruling whether `a.{ 1
    }.b` and `a<b>c` are one structure, two, or a fault; then one behaviour, tested.
14. Minor: `Delineation: Drop` blocking ownership; text copies in `Potential`; unused
    `proptest` dev-dependency; duplicated banner; `';'`/`'\\'` literals.

## 11. Decisions taken on the flow's authority that the living would want to see

- **`MissingBody`/`MissingHead` deleted; `a.`, `.a`, `a..b` are bare words** (PD36-59).
  Closes the swallowed-fault item by removing the faults. Vision/datom.md's bare-word
  rule (no space, no delimiter) admits them, so this is defensible; but the stale skill
  and 0.17 treated them as faults, and `a..{ 1 }` now yields a head `a.`.
- **Balanced parentheses escaped unconditionally** — contradicts the vision's Meaning
  sentence and de-canonicalizes its examples (section 5).
- **U+201D left unrepresentable, silently** (item 6).
- **Situation on ascent by re-reading** (section 3) — the report calls it "justified by
  the multi-pass principle"; this audit reads the vision otherwise.
- **`Situation` kept as `BTreeMap<Path, Extent>`; `Frame` clones full paths** — the
  quadratic memory is a consequence of this representation, chosen without a ruling.
- **`DEPTH_LIMIT = 100 000`, reported as `Unclosed`** — a bound is wanted; its value,
  its fault, and whether it belongs in protos or in the caller were not asked.
- **`Datomic::textualize` kept as a default method** beside `Textualizable for Datom`;
  corporate types still do not bear the protos kind (item 4).
- **`impl_datomic_scalar!` with closure arguments** — the living's stated worst smell,
  chosen to remove triplicates.
- **Zero-sized bearers `BareRunParser`, `BodyAttacher`** in protos while datomic's own
  flake forbids the pattern.
- **Decimal rules** (point mandatory, no exponent, leading zero refused, shortest
  round-trip print, huge values printed as 30-digit integers with `.0`) — Vision/datom.md
  has no decimal section.
- **`-0` refused** — carried; unasked.
- **Non-dot separators conceive as `Bare` text** (D200-203) — Vision/datom.md says the
  dot is the separator; whether `Some:42` is text or a fault in a variant position is
  unasked. `Problem::Separator` left in as a corpse.
- **`Head::Qualified` and `Enclosure::Angled` kept in protos, faulted in datom with
  fabricated datoms** — unchanged from the first pass.
- **Vision-example tests deleted** (Person with roles, Note, Remark, Standup, Lock, the
  `actualize` helper) — no reason given in the report; coverage of the very examples the
  vision writes went from typed-verbatim to absent.
- **`Delineation` given a `Drop`** — makes the struct non-destructurable; a consequence
  not weighed in the report.
- **Kinds named with -ing gerunds** — a naming family the vision's examples do not use.

## 12. Verdict

Observation: both crates build, pass their own tests, clippy, fmt, doc and `nix flake
check`; the trailing-separator faults, the stale documents, the tracked artifact, the
derives, and the datom concept's single form per meaning are fixed; every vision example
reads typed. Observation: the situation machinery — the pass's central deliverable — is
wrong on both sides (the delineation misplaces every headed structure with an enclosed
body; the corporate fault paths are off by the root), no test exercises it through
`actualize`, and the situation representation makes memory quadratic in depth so that a
200 KB text kills the process; the concept layer still overflows the stack; the ascent
can panic. Inference: datom is **not** solid enough to build the consumers on now. What
consumers would inherit is not a rough edge but the fault-reporting and resource model
itself: any Nexus reading untrusted datom can be killed by a small text, and any fault
it reports back points nowhere. The next pass should be the situation and memory
design (items 1-5 above) with tests written first from this audit's inputs, before any
consumer is re-pinned. Unknowns: whether the living wants -ing kind names; whether the
depth bound belongs in protos; the U+201D ruling; the Meaning escape ruling; whether
`a.{ 1 }.b` is one structure or two.

## Sources

- /home/li/primary/Vision/protos.md, Vision/datom.md, Vision/ethos.md — authority
- /home/li/primary/Intent/mandatoryTraits.md, Intent/protosParsing.md, Intent/data.md
- /home/li/primary/flows/995a164e/vision/{rust,layerMatching,kinds,concept,contexts,explodedForm}.md
- /home/li/primary/flows/1a6ca4/vision/datom.md — the rewrite directive
- /home/li/primary/flows/1a6ca4/reports/auditProtosDatomic.md — the first audit (acceptance list)
- /home/li/primary/flows/1a6ca4/reports/rewriteProtosDatomic2.md — the second pass's account (claims only)
- /git/github.com/LiGoldragon/protos @ 3b29b61e431b: src/{lib,delineation,textualization,actualization}.rs, tests/delineation.rs, tests/delineation.proptest-regressions, protos.ethos, protos-kinds.ethos, Cargo.toml, flake.nix, README.md, .gitignore, rust-toolchain.toml; git diff 2cb8884..3b29b61
- /git/github.com/LiGoldragon/datomic @ 83d92f9d5047: src/lib.rs, tests/datomic.rs, datomic.ethos, datomic-kinds.ethos, Cargo.toml, flake.nix, README.md, .gitignore, rust-toolchain.toml; git diff cf59b01..83d92f9; `git show cf59b01:tests/datomic.rs`
- /git/github.com/LiGoldragon/ethos-zero @ a2e8eaf (2.0.0), extracted by `git archive` (the working tree there is a dirty, non-building 3.0.0 rewrite, untouched)
- Scratch witness crate (session-local): /tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/adv2/{tests/situ.rs,tests/deep.rs,tests/scale.rs,tests/esc.rs,tests/vision.rs,tests/adv.rs,tests/layers1-5.rs,src/bin/depth.rs}; ethos-zero outputs under scratchpad/ezout and scratchpad/ezbis; nix logs scratchpad/nix-{protos,datomic}.log
