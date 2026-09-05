# Audit: protos 0.17.0 and datomic 0.11.0 against the distilled vision

Audited: protos `c5594f9d6f73` (main, /git/github.com/LiGoldragon/protos) and datomic
`2c2e2073fd34` (main, /git/github.com/LiGoldragon/datomic), every tracked source file,
test file, `.ethos`, manifest, flake and markdown read whole. Method: read first,
then `cargo test`, `cargo clippy --all-targets -- -D warnings`, `cargo fmt --check`,
`cargo doc` in both repositories, then a scratch crate under the session scratchpad
(`adv/tests/{adv,deep,layers,pos}.rs`) driving both public APIs with adversarial
inputs. Everything marked *witnessed* was seen in the code or in a run; everything
marked *inference* is this audit's reading; unknowns are named as such. The
rewrite's own report (`reports/rewriteProtosDatomic.md`) was read after the code and
is cited only where its claims were checked.

Line references are `protos/src/lib.rs` = P, `datomic/src/lib.rs` = D,
`protos/tests/delineation.rs` = PT, `datomic/tests/datomic.rs` = DT.

## 1. Layers, kinds, bearers, bound, Potential/actualize, fault direction

| Vision sentence (Vision/protos.md Layers) | Verdict | Witness |
|---|---|---|
| "Text, Protoform, Concept, Corporate — four layers" | compliant | P5-9 Text; P100-139 Protoform/Delineation; D19 Datom; corporate = Rust types |
| "textualize (Textualizable), goes to Text, borne by Protoform, and the layers below through the chain" | **non-compliant** | `protos::Textualizable` is borne by Head, Protoform, Delineation only (P283, P296, P361). Datom and every corporate type do not bear it: `<Datom as Textualizable>::textualize` fails to compile (scratch `layers.rs`, E0277). They get a same-named default method on `Datomic` (D316) instead |
| "protosize (Protosizable), goes to Protoform, borne by Text, where it is the delineation, and Concept" | compliant | P866 `impl Protosizable for Text`; D213 `impl Protosizable for Datom`. Extra, unnamed by the vision: P883 `impl<C> Protosizable for Potential<(), C>` |
| "conceive (Conceivable), goes to Concept, borne by Protoform and Corporate" | compliant | D289 Protoform, D294 Delineation, D435-D1048 every corporate type |
| "incorporate (Incorporable), goes to Corporate, borne by Concept, and the layers above through the chain" | **partly non-compliant** | Concept bears it (D447 onward, `impl Incorporable<T> for Datom`). Text and Protoform do not: `<String as Incorporable<i64>>::incorporate` fails to compile (scratch `layers.rs`). The chain exists only as `Actualizable` on `Potential` (P891) |
| "Sized is the bound borne by every corporate type" | compliant | P256 `Actualizable<T: Sized>`; D313 `Datomic: Sized + ...`; no `Embodied` anywhere |
| "Potential and actualize go universally, layer to layer: a potential Protoform actualized yields a Protoform" | **non-compliant** | Only `Potential<T, C>: Actualizable<T>` where `C: Incorporable<T>` exists (P891). `Potential<Delineation>::actualize()` does not compile (scratch `layers.rs`, E0599). `Potential<Datom, Datom>` works only through the identity `impl Incorporable<Datom> for Datom` (D993) |
| "Incorporate ... may fault ... Textualize ... cannot fault" | compliant in the types | All descent capabilities return `Result` with a `Fault` associated type; ascent (`Textualizable`, `Conceivable<Datom>` on corporate types with `Fault = Infallible`, `Protosizable for Datom` Infallible) cannot fault. See section 8 for ascent output that is not readable back |
| "Spans are found on the way in and computed on the way out" | **non-compliant on the way out** | Datom → Delineation (D216-221) yields `situation: Situation::new()`, empty; witnessed `situate(&[0])` is `None` after `Datom::Struct(..).protosize()` (scratch `adv.rs` g). No ascent capability computes extents |

## 2. Delimiters, separators, heads, comments, map, spacing, opaque regions

| Item | Verdict | Witness |
|---|---|---|
| "Five delimiter pairs in all: three structural — braces, brackets, angle brackets — and two opaque" | compliant | P41-62 `Enclosure {Braced, Bracketed, Angled}`, `Boundary {CurlyQuotes, Parentheses}`; P368-377 the ten glyphs; no guillemet in either `src/` |
| "The separators are period, exclamation and colon" | compliant | P25-29; P397 |
| "The head is a symbol" | not decidable | `Head::Bare(Symbol)` with `Symbol = Text` (P9, P74). The vision says the qualification rule "is not yet stated"; the code applies no rule beyond "non-empty run without whitespace/delimiter". P862 can build `Head::Bare(String::new())` (an empty head) — unreachable by this audit's reading, but present |
| "Heads may be daisy-chained: different separators too" | compliant | `a.b.c` and `a:b:c` right-associative, PT217-233, PT70-89; scratch `Head!body` → `Variant("Head", Exclamation, ..)` |
| "A single semicolon opens a comment" / never printed | compliant | P540-547 skip; PT191-215; comment inside curly quotes and parentheses is content (scratch c). Side effect witnessed: `a;b` in a Text position yields `"a"` silently (scratch `pos.rs`) — consistent with the rule, but worth knowing |
| "The key-value map, and the guillemets ... are dropped entirely" | compliant in text; a Rust map remains | No `Map`, `Pair`, guillemet in either crate's `src/` or tests. `Situation = BTreeMap<Path, Extent>` (P22) is an internal Rust map; it is never textualized (Delineation is not Datomic) and `protos.ethos:16` omits it |
| Canonical spacing: "a space inside every bracket and brace delimiter, at both ends ... and never inside curly quotes, where a space is content" | compliant | P311-320; PT112-151; `“ a ”` round-trips as `" a "` (scratch c). Angles print tight `<a b>` (P318) |
| Vision/protos "leave a space between the delimiters and the content, except for the curly quotes" | not decidable | Vision/protos.md says the only exception is curly quotes; Vision/ethos.md's own examples write angles tight (`Vector<Integer>`, `Processable<[Clonable Sendable] Serializable>`); Vision/datom.md says "bracket and brace". The code follows the examples (tight angles, verbatim parentheses). A ruling is wanted |
| Opaque regions verbatim | compliant for curly quotes; **not for parentheses** | Curly-quote content is stored and printed byte-for-byte (P646, P325). Parenthesis content is un-escaped on the way in (P662-666: `\x` → `x` for any x) and re-escaped on the way out only for unbalanced `)` (P337-359): `Meaning("a\\b")` prints `(a\b)` and reads back `"ab"`; `Meaning("a(b")`, `Meaning("((")`, `Meaning(")(")`, `Meaning("\\")` print text that faults on reading (scratch c). The escape is not stated in Vision/ (only in the stale skill) |
| "Parentheses, read by balance" | compliant | P655-693; PT167-179; nested `(a (b) c)` and `(a\n(b\n)c)` read whole (scratch c) |

## 3. Datom

| Item | Verdict | Witness |
|---|---|---|
| Six forms | compliant | D19-26 `Datom { Variant, Struct, Vector, Text, Meaning, Bare }`; braces → Struct, brackets → Vector, headed → Variant, curly → Text, parens → Meaning, bare → Bare (D232-286); Angled faults (D269) |
| "the reader walks the expected type" (Vision/datom.md; Intent/protosParsing.md "only the current context gives shapes their meaning") | **partly non-compliant** | The text is read with no type in hand: delineation (P866) then an untyped `Datom` (D289), and only `incorporate_from` consults the type. The position-typed effect is reconstructed afterwards: a bare chain is re-joined into a string in a Text position (D512 `rejoin_chain`) and a Text is quoted on the way out when not "bare-safe" (D370-397). Witnessed consequences: `a.`, `a..b`, `.a`, `a.b.` in a Text position are structural faults, not strings, though the vision's bare-word rule (no space, no delimiter) admits them (scratch `pos.rs`); `“x”` in an Integer position is a Corporate Shape fault, correct |
| "a bare word means what the position says" | compliant at the incorporate step | `True`, `None`, `Pending`, `Some.x`, `42`, `-0`, `3.14` in a String position all land as strings; `[ True None Pending ]` as `Vec<String>`; `Some.None` as `Option<Option<String>>` is `Some(None)` and as `Option<String>` is `Some("None")` (scratch f) |
| Every Vision/datom.md example round-trips verbatim in the tests | **non-compliant, one missing** | Person DT453-461 (typed, verbatim); Reply ×3 DT463-480; `[ 0 42 -42 ]` DT482; Note/Remark/Standup DT509-536 (typed, verbatim); `Observed.Locks.[]` and `Success` DT485-507 only at the untyped `Datom` level, not through an enum type. **`{ Ada [ 12 7 -3 ] }` (the Scores example, Vision/datom.md De/serialization) is absent from both test files** |
| "today a parenthesized text lands as a plain String, with the later type marked in code" | compliant | D60 `Meaning::Plain(Text)`; D24 `Datom::Meaning(Text)`; a Meaning in a Text position and a Text in a Meaning position both fault (D510-513, D530-532) |
| Integers: "ASCII digits, no leading plus, no leading zero except 0 itself" | compliant | D403-428; witnessed `+1`, `01`, `00`, `1_000`, `١٢`, `0x10`, `1e3`, `9223372036854775808` all fault; `-9223372036854775808` reads (scratch h). `-0` is rejected (D423) — the vision does not say this; see section 10 |
| `True`/`False` | compliant | D452-466; DT52-56 |
| Decimal | not decidable | Vision/datom.md states no decimal rule. Witnessed: `01.5` → 1.5 and `1.50` → 1.5 accepted (leading zero admitted where integers refuse it); `1.` and `.5` are structural faults (MissingBody/MissingHead); `1e300` prints as a 301-character decimal (scratch h) |

## 4. Faults

| Item | Verdict | Witness |
|---|---|---|
| Layer-named | compliant | D129-133 `Fault { Structural(protos::Fault), Conceptual(Path, Problem), Corporate(Path, Problem) }` |
| Carries what "potential datom, untrusted until it matches its type" implies | compliant in shape | `Problem::Shape(Expected, Datom)` carries the expected form and the datom found (D107); `Value(Text)` the offending word; `Arity(expected, actual)`; `UnknownVariant(Symbol)`; `Separator(Separator)` |
| Situated, with spans found on the way in | **non-compliant (witnessed, every case tried)** | Every Conceptual and Corporate fault comes back `Situated(None, ..)`: `{ 1 x }` as Extent, `[ 1 x ]` as `Vec<i64>` (path `[1]`), `Some.x` as `Option<i64>`, `Some!42`, `{}` as `Vec<i64>`, `Vector<Text>` as `i64` (scratch b, d, g). Cause, read in the code: the datom's root is conceived at path `[]` (D298 `pf.conceive_at(&[])`) while the delineation situates its single top-level protoform at `[0]` (P596-602), so `delineation.situate(fault.path())` (P908, P913) never finds the key. Structural faults are situated (extent copied at P902) |
| Paths inside structs, Option, Result | **non-compliant** | Only `Vec<T>` prepends the child index (D562). Struct fields (D900-901, D971-972, D1039-1040, and every hand-written struct in DT), `Option` (D594), `Result` (D631-632), `Box` (D1004) pass the child's fault up unchanged, so `{ 1 x }` as Extent reports path `[]`, not `[1]` (scratch g) |
| Structural faults inside enclosures | **non-compliant** | P625 and P766 discard the inner fault (`Err(_)`) and report `Unclosed(enclosure)` over the whole enclosure: `{ a. }` → `Unclosed(Braced) (0,6)` instead of `MissingBody (3,4)`; `[ { a ] }` → `Unclosed(Bracketed) (0,9)`; `{ .a }`, `[ a. b ]` likewise (scratch a). P568-574 additionally fabricates `Extent(0,0)`/`Unclosed(Braced)` regardless of the real enclosure, relying on the caller to overwrite it |
| No test covers a situated non-structural fault | observation | DT542-582 and DT655-659 construct faults by hand or assert only `is_err()`; no test asserts a `Situated` extent or a nested path |

## 5. The trait ontology (Intent/mandatoryTraits.md; flows/995a164e/vision/rust.md, layerMatching.md)

| Rule | Verdict | Witness |
|---|---|---|
| "Every method call in our Rust code lives under a trait" / "I really despise free functions" | **non-compliant in protos** | Eight module-level free functions: P337 `escape_parens_for_print`, P381 `is_delimiter`, P397 `is_separator`, P401 `separator_from_char`, P410 `enclosure_for_opener`, P419 `closer_for_enclosure`, P427 `is_closer`, P438 `parse_bare_run`, P851 `attach_body_to_deepest`. datomic `src/` has none (its flake check forbids them; protos' flake has no such check) |
| "We forbid freestanding implementations. All implementations must be of a trait" | **non-compliant in protos** | P196 `impl<T, C> Potential<T, C> { pub fn text() }` and P510 `impl<'a> Delineator<'a> { new, remaining, peek_char, advance_char, skip_whitespace_and_comments, parse_contents, parse_one }` — the whole reader is an inherent impl on a private struct. datomic's flake regex (`impl[[:space:]]+name[[:space:]]*\{`) would not catch either form (`impl<..>`) even if applied |
| "I despise these inlined lambdas even more" | **non-compliant, mild** | protos: closures at P288, P315, P363, P739, P798, P836 (`find(|(p, _)| p == path)`), P901, P906, P912. datomic: D417, D427, D490, D552, D562, D580, D614, D618, and five `unwrap_or_else(|e| match e {})` (D318, D552, D580, D614, D618) that an irrefutable `let Ok(x) = ..` would replace on the 1.85 toolchain. Some `map_err` closures are what `Result` forces; the `find` and `map(|c| c.textualize())` ones are not |
| "no separate data table ... it must live in their capabilities" | **non-compliant** | The delimiter glyphs live in a constant table (P368-379) consulted by free functions (P381-436), *and again* as literals in `Textualizable for Protoform` (P306-310, P325, P329), *and again* in datomic as `let delimiters = ['{', '}', '[', ']', '<', '>', '“', '”', '(', ')', ';']` (D373) plus separator literals `'.' | '!' | ':'` (D379, D382) — a dialect re-declaring protos' delimiters, against Vision/protos "this is the code that can be shared between all parsers and belongs in protos". `Separator` has a `Glyphing` capability (P273; duplicated at D352-364) but `Enclosure` and `Boundary` have none |
| "go through the enum, variant by variant" | compliant where an enum exists | `Conceiving for Protoform` (D232) and every `incorporate_from` match variant by variant. The character reader itself (P556-848) is a hand-rolled position/char state machine, not an enum walk; it is the 0.15.1 reader with comments stripped and guillemets removed (git diff 4806136..c5594f9, witnessed) |
| lib.rs reads as the ontology: layers, kinds, types first; implementation under | **partly non-compliant** | protos: types P5-235, public kinds P237-267, then a private kind P269, impls, then free functions and constants, then the reader struct — the reader is not under a kind. datomic: `pub trait Datomic`, the crate's own kind, is declared at D313, after three private helper kinds and after the Protosizable/Conceivable impls (D160-302); the helper kinds `Prepending`, `Protosizing`, `Conceiving`, `VariantChaining`, `Glyphing`, `BareSafety`, `IntegerParsing` are private and not in `datomic.ethos` |
| Repetition (spirit: correctness, "anatomically and directly") | observation | Hand-written `Debug`/`PartialEq`/`Eq` that replicate `#[derive]` exactly: P14-18, P31-39, P48-56, P64-71, P79-98, P108-133, P141-156, P167-177, P185-192, P214-232; D28-57, D64-70, D89-103, D115-126, D135-143. Each `Datomic` type carries three near-identical impl blocks (`Conceivable`, `Datomic`, `Incorporable` delegating to `incorporate_from`), e.g. D435-450, repeated 17 times |

## 6. The `.ethos` self-descriptions (Vision/ethos.md Declaration)

| Rule | protos.ethos | datomic.ethos |
|---|---|---|
| Variant-headed, no version, imports first | compliant (`Types`, `[]`/import list first, no version) | compliant |
| "a types variant, which only holds types" / "a kinds variant, which only holds kinds" | **non-compliant**: kinds in section 3 of a `Types` file (line 19-24) | **non-compliant**: `Datomic` kind in section 3 (line 14) |
| "In a types file they [associations] are the third section, after the types" | **non-compliant**: associations are the fourth section (line 25) | **non-compliant**: fourth (lines 15-22) |
| Kind identity "name and constraints, written as one head" | **inconsistent**: `Incorporable<Sized>` (line 22) but Rust `Conceivable<C>` and `Actualizable<T: Sized>` are written bare `Conceivable`, `Actualizable` (lines 21, 23) while datomic.ethos uses `Conceivable<Datom>` | `Datomic.{ [ Sized Conceivable<Datom> ] .. }` omits the `Fault = Infallible` constraint (D313) |
| Faithful to the Rust | **not faithful**: `conceive.[ Result<Self Fault> ]` and `actualize.[ Result<Self Fault> ]` yield `Self` where Rust yields `C`/`T` (P248, P258); `Delineation.{ Vector<Protoform> }` omits `situation` (P136-139); `Potential`, `Situated`, `Situation`, `Pathed`, `Glyphing` absent; associations omit `Head.[ Textualizable ]`, `Potential.[ Protosizable Actualizable ]`; line 4 lists `Text Integer Decimal Boolean` as bare words in the types section, a form the Declaration section does not define | **not faithful**: `Datomic` omits the static capability `incorporate_from:` (D314); associations list `Incorporable<..>` for five scalars only, omitting Vector/Option/Result/Box/Situated/Expected/Problem/Fault/Separator/Enclosure/Boundary/Extent/protos:Problem/protos:Fault/Datom (D568-D1051); `Datom.[ Datomic ]`, `Expected/Problem/Fault/Separator/Enclosure/Boundary/Extent.[ Datomic ]` absent; `Vector<Datomic>.[ .. ]` and `Structural.protos:Fault` (inline qualified reference, `protos:Fault` not in the import list) use forms the Declaration section does not define |

## 7. Legacy vocabulary and dead code

Witnessed by grep over every tracked file:

- protos `ARCHITECTURE.md` (whole file): `Structural::delineate`, `Conceptual`, `Printing::print`, `Corporal`, `Embodied`, `Datomic::datomize`, "Six structural pairs", Guillemets, `Library.{0 15 0}`. Stale in full.
- protos `AGENTS.md`: `ShapeDefined`, `shapes()`, `Realize`, "Signal". protos `NON_IDEAL_AGENTS.md`: "Signal", "quick-new". protos `UPGRADES.md`: `Structural`, `Embodied`, `Printing`, `Prospective`, `datomize`, guillemets (historic upgrade notes, unrevised).
- datomic `ARCHITECTURE.md` (whole file): `Structural::delineate`, `Conceptual<Datom>`, `Datomic::incorporate`/`datomize`, `Corporal`, "Guillemets -> Map(pairs)", `BTreeMap<K,V>: Map`. datomic `AGENTS.md`: "Protos `Portion`". datomic `UPGRADES.md`: `Corporal<Datom>`, `embody`, `datomize`. datomic `flake.nix:2`: "positional typed data over Protos Portion".
- datomic `result` → `/nix/store/...-datomic-0.11.0` is **git-tracked** (mode 120000, added in the rewrite commit 66e5753; `.gitignore` has only `/target/`).
- `src/`: `Head::Qualified` / `Protoform::Bare(Head::Qualified)` (P76, P762) — the "Qualified as a Protoform" the brief names is gone as a variant but survives as a `Head` variant that datom rejects at D238 and D280 (a conceptual fault named `"Qualified"` as a fake datom). `Datom::Variant(_, _, None)` (D20) duplicates `Datom::Bare` for a variant carrying nothing (D194 prints both the same). P862 `other =>` arm fabricates an empty head. Tests keep `delineate` as a helper name (PT7) and `situated_fault_datomizes_as_struct` (DT719).
- The rewrite report's claim "Flake code quality checks ... all pass": not witnessed by this audit for `fmt` (see 8); the four grep checks pass by construction on datomic and do not exist on protos.

## 8. Solidity

Witnessed runs (toolchain 1.85.0 per `rust-toolchain.toml`):

- `cargo test`: protos 38 passed; datomic 40 passed. `cargo clippy --all-targets -- -D warnings`: clean in both. `cargo doc` with `-D warnings`: clean in both.
- **`cargo fmt --check` fails in both** (protos exit 1, three diffs; datomic exit 1, 117 diff hunks — the one-line `fn .. { .. }` bodies). Both flakes carry a `fmt` check, so `nix flake check` would fail; the rewrite report says it was not run.
- **Stack overflow (SIGABRT) on nesting**: 2000 nested brackets abort an 8 MiB thread in debug *and release*; a head chain of 10 000 (`a.a.a...`) aborts in debug, 50 000 in release (scratch `deep.rs`). `parse_contents`/`parse_one` (P556-848), `parse_bare_run` (P469), `attach_body_to_deepest` (P860), `conceive_at` (D247) and `Box<Protoform>` drop are all recursive. An untrusted text can kill the process instead of faulting.
- Unbalanced delimiters: all fault; inner faults are misreported as `Unclosed` of the enclosing structure (section 4). `“a (b” c)` correctly `Unopened` at `)`.
- Separators at end: `a.`, `a. b`, `a.}`, `a.;c`, `Some.`, `a!`, `a:` → `MissingBody` at the separator; `a..b`, `a:.b`, `.a` → `MissingHead`; `Some!42`/`Some:42` as Option → `Corporate Separator(..)` (unsituated).
- Nested opaque: `(a (b) c)`, `(a “x” b)`, `(a ; b)`, `“a ; b”`, `“ a ”`, `()`, `“”` all correct. Meaning escape asymmetry: section 2. A `Text` containing `”` textualizes to `“””`, which reads back as `Unopened` — the ascent "cannot fault" but its output is unreadable; the vision gives quotes no escape, so this is the format's unrepresentable case, unhandled and untested.
- Empty structures: `[]` as Vec ok; `{}` as Vec → Shape; `{}`/`{ 1 }`/`{ 1 2 3 }` as Extent → Arity; `<>` delineates but faults in datom; empty text or two top-level values → `Conceptual OneValue`; `{a}` prints `{ a }`.
- Bare variant names in Text positions: section 3, all land as strings.
- Integers/decimals: section 3.

## 9. Non-compliances, ranked by severity, with the fix wanted (what, not how)

1. **Non-structural faults are never situated** (4). Wanted: every Conceptual and Corporate fault returned by `actualize` carries the extent of the structure it names; the datom root and the delineation's situation agree on one path origin; struct fields, Option, Result and Box prefix the child's index as Vec already does; tests assert the extent and path of a nested fault.
2. **Untrusted text can abort the process** (8). Wanted: nesting depth cannot overflow the stack — any text yields a Delineation or a Fault; a test with deep nesting proves it.
3. **Inner structural faults are swallowed into `Unclosed` of the parent** (4, P625, P766, P568-574). Wanted: the fault found first, at its own extent, is the fault returned; no placeholder `Extent(0,0)`/`Unclosed(Braced)`.
4. **The layer table is not borne as the vision states** (1). Wanted: `protos::Textualizable` borne by Concept and Corporate (Datom and every Datomic type), not a same-named default method on `Datomic`; `Incorporable` borne by Text and Protoform through the chain; `Potential<Delineation>` and `Potential<Datom>` actualize without an identity impl; `Potential<(), C>` gone.
5. **The reader is not under the trait ontology** (5). Wanted: no free function and no inherent impl in protos; the reader's behaviour under kinds borne by protos' own enums (`Enclosure`, `Boundary`, `Separator` know their glyphs as capabilities), the glyph constant table gone, and datomic's copy of the delimiter and separator tables gone; protos' flake carrying the same free-function and inherent-impl checks as datomic's, with a regex that also catches `impl<..>`.
6. **Parenthesis escaping does not round-trip** (2, 8). Wanted: any `Meaning` text textualizes to text that reads back to the same value, or the unrepresentable set is named and faulted on the way out is impossible — so refused at construction; the escape rule is either put in Vision/ or removed; the unrepresentable `”` inside a Text is treated the same way.
7. **`.ethos` files break the Declaration** (6). Wanted: kinds out of the `Types` variant (their own file or variant), associations third, kind heads carrying their constraints consistently, capabilities yielding what the Rust yields, `incorporate_from` declared, every borne kind listed, `Situated`/`Potential`/`Situation` declared, no undefined forms (bare intrinsics as declarations, inline `protos:Fault`, `Vector<Datomic>` associations) unless Vision/ethos.md is extended to define them.
8. **`cargo fmt --check` fails in both** (8). Wanted: both trees formatted so the flakes' own `fmt` check passes.
9. **Stale documents and a tracked build artifact** (7). Wanted: `ARCHITECTURE.md`, `AGENTS.md`, `NON_IDEAL_AGENTS.md`, `UPGRADES.md` in both crates and datomic's flake description rewritten in the new vocabulary or deleted; `result` untracked and ignored.
10. **The Scores example is not in the tests** (3). Wanted: `{ Ada [ 12 7 -3 ] }` round-tripping verbatim through a typed struct; `Observed.Locks.[]` and `Success` through typed enums.
11. **Ascent computes no spans** (1). Wanted: `Protosizable for Datom` (and textualize) computes the situation, or Vision/protos "computed on the way out" is reopened.
12. **Two representations of a variant carrying nothing** (`Datom::Bare` and `Datom::Variant(_, _, None)`) and the `Head::Qualified` leak into datom faults as a fake `Datom::Bare("Qualified")` (7). Wanted: one form per meaning in the concept; a fault that names the protoform kind found, not a pretend datom.
13. **Hand-written derives and 17 triplicate impl blocks; closures where a loop or an irrefutable `let` would do** (5). Wanted: `#[derive]` where the derive is exact; one declaration per Datomic type; the closures named in section 5 removed where std does not force them.

## 10. Decisions taken on the flow's authority that the living would want to see

- **`textualize` as a default method on `Datomic` instead of `protos::Textualizable`** (D316). The rewrite's stated reason (orphan rule on a blanket impl) is true for a blanket; a concrete `impl protos::Textualizable for Datom` and a generated impl per Datomic type are not blocked. This choice makes the vision's table false for two layers.
- **`incorporate_from` as a second static capability on `Datomic`** (D314) beside `Incorporable<T> for Datom`, with every type carrying both. The rewrite reports a trait-solver overflow on stable as the reason; not reproduced by this audit. The living asked for the logic to be clear through the ontology; two capabilities for one act is the opposite.
- **Reader carried over, not rewritten** (P438-848 is the 0.15.1 reader minus comments and guillemets; git diff witnessed). The living said "yank stuff out, and rewrite it better and more anatomically". The delineator was yanked of comments, not rewritten.
- **Angles tight, parentheses escaped with backslash** — neither is in Vision/; both are carried from the stale skill.
- **`-0` rejected as an integer** (D423). Vision/datom.md says "no leading zero except 0 itself"; `-0` is arguably `0` with a sign. Untested against the living's intent.
- **Decimal rules invented** (leading zero admitted, point mandatory, non-finite refused, 301-digit printing for 1e300) — Vision/datom.md has no decimal section.
- **`Datom::Variant` keeps the `Separator`** (D20) so a datom can carry `!` or `:` heads that the type layer then rejects (D590, D627). Vision/datom.md says "the dot is the separator" — whether the concept should admit the other two at all is unasked.
- **Symbol rule "non-empty, no whitespace, no delimiter"** — stated by the rewrite as the minimum; Vision/datom.md says heads are capitalized variants in datom, and no head validation exists anywhere.
- **All doc comments removed from both crates** (git diff witnessed): the previous `//!`/`///` explanations were deleted wholesale. No vision sentence asks for or against this.
- **`result` symlink committed** — almost certainly an accident, but it is on main.

## 11. Unknowns

- Whether the living wants angles spaced (Vision/protos wording) or tight (Vision/ethos examples).
- Whether a Text containing `”` should be refusable at construction, escaped, or left unrepresentable.
- Whether `Potential<T>` for Delineation/Datom is wanted through `Incorporable` on Text/Protoform, or through a separate impl set; the vision states the effect, not the mechanism.
- Whether the flow's reported trait-solver overflow is real on 1.85 with the vision's shape (one `Incorporable` capability, no `incorporate_from`); this audit did not attempt that construction.
- Whether "ethos-zero solid" was in this rewrite's scope; the crate was not audited here.

## Sources

- /home/li/primary/Vision/protos.md, Vision/datom.md, Vision/ethos.md — authority
- /home/li/primary/Intent/mandatoryTraits.md, Intent/protosParsing.md, Intent/data.md
- /home/li/primary/flows/995a164e/vision/{rust,layerMatching,kinds,concept,contexts,explodedForm}.md
- /home/li/primary/flows/1a6ca4/vision/datom.md — the rewrite directive
- /home/li/primary/flows/1a6ca4/reports/rewriteProtosDatomic.md — the rewrite's own account (claims only)
- /git/github.com/LiGoldragon/protos @ c5594f9d6f73: src/lib.rs, tests/delineation.rs, protos.ethos, Cargo.toml, flake.nix, README.md, ARCHITECTURE.md, AGENTS.md, NON_IDEAL_AGENTS.md, UPGRADES.md, rust-toolchain.toml; git diff 4806136..c5594f9
- /git/github.com/LiGoldragon/datomic @ 2c2e2073fd34: src/lib.rs, tests/datomic.rs, datomic.ethos, Cargo.toml, flake.nix, README.md, ARCHITECTURE.md, AGENTS.md, UPGRADES.md, result; git diff 4712361..2c2e207
- Scratch witness crate: /tmp/claude-1001/-home-li-primary/1a6ca4f9-e0fa-4f2c-bd6f-a40651590354/scratchpad/adv/tests/{adv,deep,layers,pos}.rs (session-local; outputs quoted above)
