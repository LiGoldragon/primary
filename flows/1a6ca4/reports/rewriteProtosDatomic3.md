# Third pass: protos 0.19.0 and datomic 0.13.0

Written by the write subflow of flow 1a6ca4 (Fable) after landing protos `205408679738`
and datomic `e6005c6578a5`, both on main. Acceptance list: `reports/auditProtosDatomic2.md`,
section 10, fourteen ranked items. Design authority: Vision/protos.md, Vision/datom.md, the
brief's fixed design. *Witnessed* = seen in a run of this pass; *claim* = this pass's own
account of its code; unknowns are named. Test names refer to `protos/tests/{delineation,
textualization,scale}.rs` and `datomic/tests/{vision,situated,reading,scale}.rs`.

## 1. The audit's items

| # | Item | Status | How (test) |
|---|---|---|---|
| 1 | Memory quadratic in depth | **closed** | `Situation { extent, children }` is one node per structure beside the tree; no path stored per node, no path cloned per frame. Witnessed (release, bounded): 100 000 nested brackets read in 25 MB, ×~6 per ×10 depth (`scale.rs`, both crates, asserts `peak(100k) ≤ peak(1k) + 15·(peak(10k) − peak(1k)) + 16 MB` and < 1 GB per probe, each probe its own process under `ulimit -v 2 000 000` and `timeout 120`) |
| 2 | Corporate faults not situated | **closed** | One convention on `protos::Pathed` (head 0, body 1, enclosed in order, constraints under the head); conceive keeps it for the datom; every fault carries `Locus { path, extent }` from the node at hand. `a_bad_element_is_reported_at_its_own_extent` (`[ 1 x ]` → path `[1]`, extent of `x`), `a_bad_field_deep_in_the_person` (`[3,1,1,1]`), `three_deep_through_every_container` (Struct, Vector, Option, Result, Box, Variant: `[0,2,1,1,1,1]`), `a_variant_body_is_child_one` |
| 3 | Delineation's situation wrong for headed structures | **closed** | `head_with_enclosed_body` (`[0]` = whole, `[1]` = the struct), `chain_with_enclosed_body`, `head_with_opaque_body`, `qualified_head_with_body` (`[0,0]` = the constraint, `[1]` = the body), `nested_enclosures_situated` |
| 4 | Ascent computes no situation; re-read; panics | **closed** | `Situating::situate` on Protoform records each node's start as it begins it and its end as it finishes it: text and situation from one walk; `Datom::protosize` is build + situate, no re-read, no `expect` (zero `unwrap`/`expect`/`panic` in either `src/`, grep witnessed). `writer_extents_index_the_written_text`; every canonical example asserts writer situation == reader situation (`agrees`, `deep_situation_matches_the_reader`); `the_concept_is_situated_by_the_reader_and_by_the_writer` |
| 5 | Concept-layer recursion | **closed** | Reader (frame stack), writer (step stack), conceive (step stack + path stack), protoform build (step stack), and Drop for Protoform, Situation and Datom (worklist) are iterative. Witnessed at 100 000 nested and a 100 000-head chain: `scale.rs` read/write/drop in both crates. Incorporation recurses by the corporate type's own nesting, which the text cannot exceed — see decisions |
| 6 | Layer table not borne as the vision states | **closed as the brief settles it** | `Text`/`String`: Protosizable; `Situated<Protoform>`, `Delineation`: Conceivable<Datom>; `Datom`: Incorporable<T> for every Datomic T, Textualizable, Protosizable; `Potential<T, C>`: Actualizable<T> by the protos blanket chain; `Datomic` provides `textualize`. The identity impl is gone; `Datom` is not Datomic. `Potential<Delineation>` is not actualizable (would overlap the blanket) — protosize on text is the delineation |
| 7 | U+201D a comment, not a decision | **closed** | `protos::Text(String)` with `TryFrom<String>` → `Refusal { glyph, offset }`; every opaque content and the corporate text scalar is `Text`; `String` is not Datomic. `text_refuses_the_closing_curly_quote` (both crates). Recorded as a decision for the living below |
| 8 | Balanced parentheses escaped | **closed** | Only an unbalanced parenthesis and a backslash are escaped (`only_unbalanced_parentheses_and_backslashes_are_escaped`); Note and Standup textualize verbatim (`note`, `standup`); property `any_meaning_text_round_trips` (protos) and `any_meaning_round_trips` (datomic) over `[^”]*` |
| 9 | Procedural reader; ZSTs; rosters; closure macro | **closed** | Reader: `Reader` (data) bearing `Delivering`, `Reading`, `HeadPushing`, `Delineating`, `Bounding`; each glyph class announces its shape (`Glyph`), each frame reads to its completion. Zero-sized bearers: none; protos flake now carries `no-zst-behavior`. Rosters: gone — `Serial::{first, after}` is the walk, `Recognizing`/`Identifying` iterate it. Macro: gone — `Worded` scalars with provided `incorporate_word`/`conceive_word`; closures in `src/`: 0 in both crates (grep witnessed) |
| 10 | `.ethos` files | **closed (with recorded omissions)** | Four files, Declaration forms only, four-section complex kinds, every capability's inputs and yield as in the Rust, every borne kind listed for non-generic types, `StructuralProblem.Problem`/`StructuralFault.Fault` imported by alias. ethos-zero 3.0.0 (`73d4794f`, git archive in scratchpad `ez3`) generates from all four (witnessed: `Generated.[ … ]` ×4). Omissions: generic types (`Situated`, `Potential`, `Path` alias is declared), borrowed handles (`Site`, `Positions`, `Variant`), generic bearers (`Vec`/`Option`/`Result`/`Box`), `char` written `Text`, named-field structs written positional |
| 11 | Vision examples deleted; Scores not verbatim | **closed** | `vision.rs`: `person_with_roles`, `reply_accepted`, `reply_refused`, `reply_pending`, `scores` (`{ Ada [ 12 7 -3 ] }` verbatim), `integer_vector`, `note`, `remark`, `standup`, `observed_locks_empty`, `success`, `lock` — each typed, verbatim, through `Potential::actualize` and back through `textualize` |
| 12 | Fabricated datoms; dead `Separator`; depth as `Unclosed` | **closed** | `Problem::Formless(Found)` names the form (`Angled`, `Qualified`, `Chain`); `Problem::Shape(Expected, Found)` carries no datom; `Separator` problem gone; no depth limit at all (`conceptual_faults_name_the_form_found`) |
| 13 | Two values without whitespace | **closed by the brief's ruling** | Siblings: `adjacency_without_one_trailing_separator_yields_siblings` (`a..{ 1 }`, `a.{ 1 }.b`, `a{ 1 }`, `a<b>c`) |
| 14 | Minor: `Delineation: Drop`; text copies; unused proptest; banner; literals | **closed** | `Delineation` has no Drop (Protoform and Situation drop iteratively themselves; `Situated` destructures); `Potential` copies once at `From`; proptest used in both crates; one module doc per file; `';'` and `'\\'` live once in `Mark::glyph` |

## 2. Memory (release, `systemd-run --user --scope -p MemoryMax=4G -p MemorySwapMax=0`, each probe under `ulimit -v 2000000` and `timeout 120`; peak RSS = VmHWM of the probe process, ~2.5 MB of it the process itself)

| probe | 1 000 | 10 000 | 100 000 |
|---|---|---|---|
| protos read: nested brackets | 2.4 MB | 4.3 MB | 25.0 MB |
| protos read: head chain `A.A.…A` | 2.6 MB | 5.4 MB | 35.9 MB |
| protos read: head chain into `{}` | 2.5 MB | 5.0 MB | 32.7 MB |
| protos read: flat vector of n | 2.5 MB | 4.3 MB | 25.5 MB |
| protos write (textualize + situate) + drop: nested | 2.5 MB | 4.3 MB | 22.5 MB |
| protos write + drop: flat vector | 2.5 MB | 4.2 MB | 25.6 MB |
| datomic read + conceive: nested vectors | 2.6 MB | 5.0 MB | 28.8 MB |
| datomic read + conceive: variant chain | 2.8 MB | 7.4 MB | 52.6 MB |
| datomic actualize `Vec<i64>` of n | 2.7 MB | 5.6 MB | 39.9 MB |
| datomic write (textualize + protosize) + drop: nested | 2.6 MB | 5.3 MB | 32.1 MB |
| datomic write + drop: `Vec<i64>` of n | 2.7 MB | 5.9 MB | 37.9 MB |

Second audit, same probe: 10 000 brackets 550 MB, 50 000 allocation failure under 4 GB.
Debug builds run within ~1 MB of these. None of the eleven probes faulted, overflowed or timed out.

## 3. The passes

| pass | kind | borne by | yields | faults |
|---|---|---|---|---|
| delineate | `Protosizable` | `str`, `String` | `Delineation` (situated protoforms) | `protos::Fault`: Unclosed, Unopened, Unterminated, Stray |
| conceive | `Conceivable<Datom>` | `Situated<Protoform>`, `Delineation` | `Situated<Datom>` | `Fault::Conceptual(Locus, Formless \| OneValue)`, Structural passed through |
| incorporate | `Incorporable<T>` / `Datomic::incorporate` | `Datom` / every corporate type, from a `Site` | `T` | `Fault::Corporate(Locus, Shape \| Arity \| UnknownVariant \| Value)` |
| actualize | `Actualizable<T>` | `Potential<T, Datom>` | `T` | the three above |
| conceive (ascent) | `Datomic::conceive` | every corporate type | `Datom` | cannot |
| protosize (ascent) | `Protosizable` | `Datom` | `Delineation`, situated by the writer | cannot (`Infallible`) |
| textualize | `Textualizable` | `Protoform`, `Delineation`, `Datom`; `Datomic::textualize` | `String` | cannot |
| situate | `Situating` | `Protoform` | `Situated<String>` | cannot |

## 4. Anatomy

protos (src 1 480 lines): `lib` 35 · `anatomy` types 130 · `kinds` 97 · `glyph` Glyphing/Delimiting/Serial/Classifying 200 · `text` Text, Refusal 69 · `run` pieces of a run 65 · `delineation` reader (Delivering, Reading, HeadPushing, Delineating, Protosizable) 367 · `opaque` Bounding 82 · `textualization` writer (Spacing, Escaping, Stepping, Situating, Textualizable) 224 · `situation` Locating, Drop 36 · `actualization` Potential, Actualizable 62 · `dropping` Shedding, Drop 44. Tests 750.

datomic (src 1 450 lines): `lib` 28 · `anatomy` 113 · `kinds` Datomic, Worded, Sited, Positional, Counted, Carrying, Headed 91 · `site` Site, Positions, Variant, Incorporable 231 · `conception` Conceivable<Datom> 234 · `protosization` Forming, Protosizable, Textualizable 129 · `worded` Worded ×8 and their Datomic 302 · `containers` Text, Meaning, Vec, Option, Result, Box 116 · `faults` Pathed, From, Datomic for the faults 176 · `dropping` 30. Tests 1 097.

## 5. Public API changes since protos 0.18.1 / datomic 0.12.1 (ethos-zero re-pins on these)

protos: `Text` is a newtype (`TryFrom<String>`/`TryFrom<&str>` → `Refusal`, `Deref<str>`, `Display`, `From<Text> for String`); the whole-text type is `String`; `Textualizable::textualize` → `String`. `Situation { extent, children }` tree; `Situated<T>(Situation, T)`; `Delineation(Vec<Situated<Protoform>>)` (no `situation` map, no Drop); `Situating::situate` → `Situated<String>` (was a path lookup; lookup is now `Locating::{locate, part}` on `Situation`). `Head::Symbol` (was `Bare`); `Protoform::Opaque(Boundary, Text)`; `Protoform`, `Head`, `Delineation`, `Situation` no longer `Clone`. `Problem::{Unclosed, Unopened(Enclosure), Unterminated, Stray}` (was `UnclosedBoundary`, `Unopened`). `Conceivable<C>::conceive` → `Result<Situated<C>, _>`; `Incorporable<T>::incorporate(&self, at: &Situation)`; `Pathed::{path, within}`; `Serial`, `Classifying`, `Glyph` new; `Identifying`, `Recognizing` removed (crate-private); `Protosizable` on `str`/`String` (not `Text`). No depth limit.

datomic: `Datom::{Variant(Symbol, Box<Datom>), Struct, Vector, Text(Text), Meaning(Text), Word(String)}` (was `Bare`, `Variant(Head, _)`); `Meaning::Plain(Text)`; `Datomic { incorporate(Site<'_>) -> Result<Self, Fault>; conceive(&self) -> Datom; textualize }` (was `incorporate_from(Datom)` + `Conceivable<Datom>`); `Site`, `Positions`, `Variant` and the kinds `Sited`, `Positional<T>`, `Counted`, `Carrying<T>`, `Headed` are the reader surface generated code uses; `Worded` with `EXPECTED`, `from_word`, `to_word`; `Fault::{Structural, Conceptual(Locus, Problem), Corporate(Locus, Problem)}`; `Problem::{Shape(Expected, Found), Arity, UnknownVariant, Value(String), Formless(Found), OneValue(Integer)}`; `Expected::Word`, `Found` new; `Prepending`, `Situated<F>: Datomic`, `impl_datomic_box!`, the identity impl removed; `Potential<T>` alias of `protos::Potential<T, Datom>`; `String` is not Datomic (`Text` is).

## 6. Decisions taken on the flow's authority

- Situation is a separate tree beside the structure (`Situated<T>(Situation, T)`), not an extent inside each node: Vision/protos.md says extents are not intrinsic to objects; the brief's wording admits both.
- `protos::Text` refuses U+201D at construction and is the type of every opaque content, Meaning included, and of the corporate text scalar; `String` does not bear Datomic. A Meaning therefore cannot contain `”` either.
- No depth limit: every walk is iterative and memory linear, so depth is bounded by the text; a limit would only protect recursive consumers, which 100 000 would not.
- Incorporation recurses by the corporate type's nesting (schema-driven, generic over T); a text deeper than the type faults at the type's leaf. Recursive types (`Box` in their own definition) recurse as deep as their data — the consumer's type, the consumer's stack.
- A run is a chain only when every segment is a symbol; otherwise it is one word (`a..b`, `a.b.` are words). A chain with a non-dot separator conceives as a Word; a mixed chain `a.b:c` is a Variant carrying the word `b:c`, and the Text scalar rejoins any chain with the dot.
- Scalars accept a dotted chain as their word (`3.14` reads as the chain `3`·`14`; Decimal rejoins it). Integer refuses `1.0` as a Value, not a Shape.
- The `Worded` blanket over `Datomic` cannot coexist with `Datomic for Box<T>` (Box is `#[fundamental]`, so a downstream crate may declare `Box<Local>: Worded`); Box wins, and the eight worded types delegate to `Worded`'s provided capabilities in seven-line impls.
- Reader kinds split by constraint for the ethos: `Positional<Datomic>` / `Counted`, `Carrying<Datomic>` / `Headed` — one kind per yield type, as `Conceivable<C>` is.
- `Headed::nothing` yields the variant itself (`Result<Self, Fault>`): ethos has no unit type.
- Structs with named fields (`Situation`, `Fault`, `Refusal`, `Locus`, `Site`) are declared positional in ethos; `char` as `Text`; ethos `Text` stands for both `String` (whole text) and `protos::Text` (quotable content).
- `Debug` and `PartialEq` derives recurse; they are test and display paths, not on any consumer's data path.
- Generic types, borrowed handles and generic bearers left out of the `.ethos` files (no Declaration form); `Sized`/`Datomic` name a kind's unnamed constraint in yields, as ethos-zero 3.0.0 accepts.
- `Delineation::conceive` with n ≠ 1 structures faults `OneValue(n)` at path `[]` over the first start to the last end.

## 7. Commits and versions

protos 0.18.1 `bf808deee5ee` → 0.19.0: `6c62ef45d72e` rewrite · `2dcfc0ee30bf`, `cc87b23866af` export `Glyph`/`Classifying` · `48fb287e7047` ethos + README · `205408679738` split `opaque`. datomic 0.12.1 `bad18213302c` → 0.13.0: `3cc78780506e` rewrite (pins protos `cc87b23866af`) · `bdd8db41650a` ethos + kinds split + README · `9e9699abdc34`, `e6005c6578a5` re-pin protos `205408679738`. All pushed to main.

## 8. Gates

Both crates: `cargo fmt` clean, `cargo clippy --all-targets -- -D warnings` clean, `cargo doc` with `-D warnings` clean, `cargo test` green (protos 18 + 10 + 6 probes; datomic 15 + 10 + 14 + 5 probes). `nix flake check` on protos `205408679738` and datomic `e6005c6578a5`, built on the remote builder prometheus (witnessed, logs `nix-protos.log`, `nix-datomic.log` in the scratchpad): protos `running 9 flake checks` (build, test, clippy, doc, fmt, no-production-free-functions, no-production-inherent-methods, no-zst-behavior, no-forbidden-vocabulary) exit 0; datomic `running 15 flake checks` exit 0. The size probes ran inside the sandboxed `cargo test` of both checks.

## 9. Left hanging

- ethos-zero 3.0.0 pins protos `bf808deee5ee` and datomic `bad18213302c`; nothing it generates compiles against 0.19.0/0.13.0 until it re-pins (section 5 is its list).
- The `.ethos` omissions in section 6: a Declaration form for generic types and borrowed handles, and for `char`, is not in Vision/ethos.md.
- Whether a Meaning may carry `”` (decision above) and whether `3.14` being a chain is wanted at the protos layer are for the living.
- `-ing` kind names (`Delivering`, `Reading`, `Stepping`, …) remain, all crate-private; the audit's naming question is unanswered by the vision.

## Sources

- /home/li/primary/Vision/protos.md, Vision/datom.md, Vision/ethos.md
- /home/li/primary/flows/1a6ca4/reports/auditProtosDatomic2.md — the acceptance list
- /git/github.com/LiGoldragon/protos @ 205408679738; /git/github.com/LiGoldragon/datomic @ e6005c6578a5
- /git/github.com/LiGoldragon/ethos-zero @ 73d4794f, by `git archive` into the session scratchpad (`ez3`, outputs in `ezout`); its working tree untouched
- Session scratchpad: `design.md` (the design note), `nix-protos.log`, `nix-datomic.log`
