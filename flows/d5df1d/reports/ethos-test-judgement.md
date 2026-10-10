# ethos-test statement map, judgement (STATEMENTS.md 0f79c4 against vision/ethos.md 850fd2)

Every judgement below is mine, from reading these two files: `/git/github.com/LiGoldragon/psyche-skills/vision/ethos.md` (HEAD 850fd27, the same revision the map names) and `/git/github.com/LiGoldragon/ethos-test/STATEMENTS.md` with its `checks/` and `fixtures/` at 0f79c4f. I traced line dates with `git log -S` in Primary and psyche-skills, and took the raw records from `flows/*/vision/`. I ran no check. Nothing was edited or committed.

## 1. The four "differs, no target" entries

**(a) Identity, lines 111–112:** "Two heads that differ in a constraint are two traits."
- **What the map says ethos-zero does:** `Processable<Clonable>` beside `Processable<Sendable>` is refused as `Duplicate.Processable`. The map adds that Rust has no two traits of one name.
- **Status: a ruled rule.** The living said it on 2026-09-03 in the raw record e4a40e kinds, archived: "Yes, obviously those would be two kinds". It landed on 2026-09-04 (c2ac4c).
- **Rename:** it predates the kind→trait rename, but that rename (5c1922) only swapped the word.
- **Tension inside the rule:** lines 106 and 113–114 say a trait is identified "as a Rust trait is". Rust cannot hold two same-named traits in one module, so the statement gives no Rust form for two such heads.

**(b) Imports, lines 175–176:** "An explicit import and an intrinsic name mean the same thing."
- **What the map says ethos-zero does:** `protos:String` comes out as `protos::String`, while the intrinsic comes out as `String`. protos 15b41da exports no `String`.
- **Status: a rule in the reviewed vision**, not an example. It has been in the vision since 2026-09-04 (23aaf7). I did not find its raw record: the 6329f1 archive cited by that landing does not contain it.
- **Rulings:** it predates both rulings and is untouched by them. The vision's own File example (line 158) imports `protos:String` and then uses `String`.

**(c) Trait syntax, line 395:** `[ Fillable.[ push!{ [ String ] [ Result<Integer SinkError> ] } ; traits`
- **What the map says ethos-zero does:** it refuses this with `TraitWanted.String`, applying the Trait section's line 94: "A capability speaks in Self, the trait's own parameters and other traits; a concrete type in an input is a trait not yet named." The check uses `Self` as the input instead.
- **Status: an illustrative example.** It was present by 2026-09-09 (4053b2). The line-94 rule entered later, on 2026-10-02 (102383, "Curriculum a77dac"), so the example predates the rule it now breaks.
- **Rename:** only its `; kinds` comment changed on 2026-10-09.
- **Line 94 itself:** it does not say "refused". Reading it as a refusal is ethos-zero's interpretation.

**(d) What a declaration turns into, lines 202 and 210:** `LockId.Integer` becomes `pub type LockId = Integer;`.
- **What the map says:** 07714b emits an alias, which matches the vision. The ruled target, `ethos-zero-cargo-newtype`, departs from it by emitting a new type. So here the vision differs from the target, not ethos-zero from the vision.
- **Status: an illustrative example**, with matching alias wording elsewhere in the vision:
  - lines 237 and 354 repeat the alias form;
  - line 257: "FilePath is an alias of String";
  - lines 301–303: "An alias bears them through the type it names: an alias is not a new type";
  - line 335: "an alias in the types section".
- **Dates:** all of it landed 2026-09-09 (4053b2). That is before the newtype ruling (d4ae97 ethos, 2026-10-06T15:55: "It's a new type") and one day after the 8e9e77 single-field-structs records (2026-09-08: "This should be a new type … `name.string`, `age.integer`"). The 2026-10-09 re-landing left it unchanged.
- **Unarchived source:** the vision's Sources list includes `d4ae97 ethos` (line 538), but `flows/d4ae97/vision/ethos.md` has not been moved to an archive file.

## 2. Every other entry

| heading | map | check | judgement |
|---|---|---|---|
| Flow, a current best example | fixture | ethos-zero's 4 Flow files generate | weaker: the fixtures are ethos-zero's own; the named vision-flow-ethos skill does not exist |
| Where the golden ethos lives | no obs | — | sound |
| What Ethos is | no obs | — | sound |
| Why Ethos | no obs | — | sound |
| Roots | pass | 4 heads read; Query/Response and Operation/Outcome generated; `Nexus` refused `Root`; `Sema` refused `Renamed.Memory` | stronger: Outcome and the Sema refusal are not in the vision, and lines 57–60 and 441 still give Sema sections and roots |
| Roots: memory trait | no obs | — | sound |
| Non-repetition | no obs | — | sound |
| Self-description | pass | no-argument print passes `Check` and contains `Query.[ Generate… Check… ]` | weaker: "describes its anatomy" is reduced to "valid ethos naming two requests" |
| Horizon | no obs | — | sound |
| Trait | pass | `String` input refused `TraitWanted.String`; a trait input becomes a bounded parameter | stronger: line 94 does not say refused |
| Trait: the word | no obs | — | sound |
| Naming | no obs | — | sound |
| Identity | pass | head emits one generic parameter per constraint; cargo variant compiles with harness bounds | wrong observable: `ethos-zero-identity` passes on `std::Clonable`, a form the map's own differs row says rustc does not resolve. Weaker: "a constraint … is a trait, never a type" (line 111) is untested |
| Identity: the example's Rust | differs | emitted `std::*` vs the vision's Clone/Send/Serialize | sound observation |
| Declaration: File | pass | sweet and braced forms give the same Rust; version refused | weaker: the version check asserts only the `Rejected.{` prefix, so the bare `1` may be refused for another reason |
| Imports | pass | `datom::Datom` fully qualified, no `use`, intrinsics accepted | weaker: `protos:[ String Textualizable ]` is imported but unused, so `protos::` emission is unasserted; `Self` is not among the tested intrinsics |
| What a declaration turns into | pass | field names, gated derive, compiles with and without datom | sound for field naming; the gated derive comes from line 321, not this section |
| Inline types | pass | `PathOverlap_Data`; compiles | weaker: "never collides" is untested |
| Inline: everything is a type | no obs | — | sound |
| Inline: about three deep | unruled | — | wrong category: line 247 is landed text; "about" gives no observable, so it belongs under no observable |
| Variant named as a defined type | pass | Rust form; `SyntaxError.[ … ]` read and printed back | sound |
| Variant: `GenerationFailure.SyntaxError.[…]` datom | differs | datom-codec refuses it | sound observation |
| Variant may declare its payload inline | pass | vector and `Unwritable_Data` | weaker: an inline enum and recursion are untested |
| Every declared type bears both traits | pass | every struct and enum derives; the alias has none; rustc confirms | sound, but it asserts the name `Composing` |
| Bears both: name `Compositional` | unruled | — | wrong category: line 299 is landed text naming `Compositional` while ethos-zero emits `Composing`, so this is a differs; Proposal 6 is the unruled fix |
| Datom traits only where text is spoken | pass | gated derive; compiles with no datom-codec; with the feature, both traits are borne | sound |
| Shapes and placement | pass | Query/Response variants; a bracket among types is an enum | weaker: "an alias in the types section" (line 335) is untested |
| Shapes: default implementations | no obs | — | sound |
| Traits are explicit | pass | assertion emitted; E0277 without the body | sound |
| Trait syntax | pass | receivers, inputs, yield, complex trait | weaker: "a yield bracket holds one type" (line 389) and upper-case constants are untested. Stronger: asserts `where Self: Sized`, which the vision does not show. The non-cargo complex check passes on an unresolvable `std::Serializable` |
| Associations | pass | assertions; E0277; Signal fifth section refused; no-tuple | wrong observable: the Signal refusal is `Arity.{ 4 5 }` (any extra section), and "implied" associations are never asserted. no-tuple tests only the two-position variant payload |
| Associations: interactions | no obs | — | sound |
| Spacing | pass | spaces in brackets and braces; hanging alignment | sound for lines 472–474, but the same check asserts `Unreadable.{ String String }` on one line, against line 476 |
| Spacing: vertical | unruled | — | wrong category: line 476 is landed text, and the pass check above asserts its contrary |
| Spacing: comment on every line | unruled | — | wrong category: line 478 is an authoring rule, so no observable. Whether the print keeps comments is a separate question (Proposal 3) |
| Zero | no obs | — | sound |
| Generation | pass | `Generate` answers `Generated` and writes the file | sound |
| Generation: committed, held fresh | no obs | — | sound |
| Sources | no obs | — | sound |
| Item 1: new type | ruled | cargo-newtype, newtype-distinct | stronger: asserts `pub struct FlowId(pub String);`. The newtype-distinct check (E0308) holds to the ruling alone |
| Item 2: single position refused | ruled | single-position(-inline) | asserts the design's own name `SinglePosition` |
| Item 3: inline import | pass | inline-import | sound; not a vision/ethos.md statement; asserts the alias `pub type Topic = custom::Name;` |
| Item 5: kind→trait | pass | `TraitWanted` reply | sound |
| Item 6: Flow's FlowId | ruled | cargo-flow-id | stronger: same tuple shape as item 1 |
| Item 8: implementers report | no obs | — | sound |

## 3. Statements the map leaves out

- Lines 57–60: Signal's sections are queries and responses; "Sema's are record types, the rest to be decided"; Signal gives a Nexus its main types and Sema its database types.
- Line 69: "Terseness is in the low amount of noise, never in shortened words."
- Lines 76–78: the schema syntax serves two audiences.
- Lines 90–92: declaring a trait declares a Rust trait.
- Line 111: "a constraint in a trait declaration is a trait, never a type."
- Lines 116–118: angle brackets as a recycled protos delimiter.
- Line 139: "one file, one Rust module. No namespace inside a file."
- Lines 152–153: "Every root's first section is its imports."
- Line 247: "A variant's payload is written in the variant and bears the variant's name; no second type is invented to hold it."
- Line 389: "A yield bracket holds one type."
- Lines 411–412: associated constants are upper case.
- Lines 441–444: Sema's implied associations, and associations as a Library's fourth section.
- Lines 467–468: "No tuple in the code we design" has a check but no row of its own. The item-1 target's tuple struct `FlowId(pub String)` is not weighed against it.

## 4. Targets that rest on an unruled proposal

The status of each proposal below is as `flows/d5df1d/reports/ethos-solution.md` (lines 175–177) lists it: awaiting ruling.

- **cargo-newtype and cargo-flow-id** assert a struct of one unnamed position, which is Types Proposal 3. That its inside is `pub` is Types Fork 4(c). That FlowId stays a String is Types Proposal 5. Item 1's status line also gates landing on Types Fork 3 and the special representation. The checks assert no datom text, but they do compile the datom derive on the new type, which is Proposal 3.
- **single-position and single-position-inline** rest on Invariants Proposal 1, which ethos-solution line 176 lists as "asks its ruling now". Raw support: 8e9e77, 2026-09-08 ("possibly even refuse"; "make illegal now"). The refusal name is the design's own (map line 83).
- **The spacing pass check** pins the one-line `Unreadable.{ String String }`, a layout that Invariants Proposal 4 and Fork 2 would decide.
- **The derives and datom-feature pass checks** assert `Composing`, the name Invariants Proposal 6 would land in the vision.
- **The double-wrap refusal:** the map lists it as unruled, but raw d4ae97 ethos (2026-10-06T14:59) says "Don't double-wrap types. That's silly."
- **Clean:** no target rests on Invariants Proposal 3, Invariants Fork 3, Types Forks 1–2, or the Sources list.
