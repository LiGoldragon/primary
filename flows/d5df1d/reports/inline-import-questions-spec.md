# Inline-import questions Q5, Q6, Q8: dry-run specification

For 1d0733 (or whoever 445410 names), to build on Prometheus through Nix as lands-nothing candidates. Base for every candidate: bare ethos-zero main 07714b, one tree, no ethos-test target. Each option is one patch; Combinations says which must be built together.

Origins. The question texts are quoted from `flows/d5df1d/reports/inline-import-research.md` §3, "The questions to rule". The numbering Q5, Q6, Q8 is the research's: ethos-solution item 7 cites "Q5, Q6, Q8 of the research" (`reports/ethos-solution.md` §7). The first edition of the book (`books/inline-import.md`) asked the same matter as its own Q3, Q4 and Q5, with proposed answers; those proposals are quoted as options. The second edition (`books/inline-import-2.md`) and the third ask none of the three. 1d0733's review (`flows/1d0733/reports/inline-import-review.md`) judged the book's Q3 and Q4 (finding 4) and its Q5 (finding 11). The code facts come from this flow's reading of ethos-zero 07714b, extracted with `git archive` (code read only, no build). Expected Rust and expected refusals are this flow's predictions; each becomes a witness only when the candidate runs. **Inference** marks a choice no source makes.

## What 07714b already does (read)

- An import or an inline source is a `Source`, any Rust path (src/lib.rs:62-135). It is made in conception at two places: an import's head (src/conception.rs:408) and a colon reference's head (:439). Neither checks the text `core`.
- Generation writes the source as written: `#source :: #name` (src/generation.rs:142-163). The one mapping is `std:Clone` and `std:Send` (:152-158).
- `Name.Type` emits `#[rustfmt::skip] pub type Name = T;` for every held type at 07714b; item 1 (new types) is not on main.
- Item 3 is on main: `Topic.custom:Name` generates `custom::Name` in types, struct and Memory positions (tests/ethos.rs `inline_imports_use_the_lowercase_source_in_type_and_struct_positions`); `Topic:custom:Name` is refused `Conceptual.{ [ 1 1 0 1 0 1 ] Expected.Reference }` (tests/cli.rs `check_refuses_a_second_inline_source_at_the_inner_reference`).
- No registry and no manifest exist; resolution is file-local (src/checking.rs:31-56). The CLI contract is `Generate.Generation`, `Generation.{ String String }`, source and target (ethos-zero.ethos).
- Sources in fixtures and goldens: `super`, `crate`, `std`, `serde`, `flow`, `protos`, `datom_codec`, `ethos_zero`. None is `core`. Tests also use `custom` and `external`.
- Witnessed by the research at c2653d (§2.5): `core:Name` generates `core::Name`, and rustc refuses `pub type Topic = core::Name;`.

Paths below follow the two witnessed refusal paths above: types section `[ 1 1 i ]`, the held reference `[ 1 1 0 1 ]`, its head `[ 1 1 0 1 0 ]`; a struct position adds `1 p`; the first import is `[ 1 0 0 ]`, its head `[ 1 0 0 0 ]`. Derived from those paths, not run.

The records the candidates rest on: `core:Name` as a camelCase expression type checked at creation, flows/445410/vision/flow.md 2026-10-09 (also flows/1d0733/vision/ethos.md, same date); the inline import with a capital head from the core built-ins and a lowercase head from the loaded environment's registry, flows/d5df1d/vision/ethos.md 2026-10-09; choice 3 (`Topic.custom:Name`, a lowercase source followed by one colon), same file, 2026-10-09 22:02. No candidate builds the camelCase type or its check.

## Q5. The registry entry

`reports/inline-import-research.md` §3, question 5: "**The registry entry.** The key `{ Vision ethos }` maps to what? Something like `{ psyche-skills «blake3…» vision/ethos.md }`? Is the "containing source" a repository, or a Source in the 2026-08-22 sense? Is the hash over the source tree, the commit, or the file? Is blake3 ruled? It is a dependency of content-identity, sema-engine and 11 other LiGoldragon crates, but not of ethos-zero, protos, datom-codec or Curriculum."

First edition, Q3 "The entry of the file-location registry", proposed: "the entry as drawn, the hash a blake3 digest held as its own type." Review finding 4: the key, hash and relative path describe how the Nexus locates context files, not an import registry; `Hash.String` goes against typed identifiers.

Options, as the source words them; the lettering is this spec's own: 5a "a repository"; 5b "a Source in the 2026-08-22 sense"; 5c "the source tree"; 5d "the commit"; 5e "the file"; 5f blake3 ruled; 5g blake3 not ruled; 5h the book's "entry as drawn", with `Hash.Blake3`.

The common example. The key is written in item 3's ruled form, since the key's own `Topic:Name` reads `Topic` as a source on 07714b:

```
Library
[ hash:Blake3 ]
[ Entry.{ Key.{ Subaspect.[ Vision
                            Knowledge ]
                Topic.core:Name }
          Location.{ Source.core:Name
                     Hash.Blake3
                     RelativePath.String } } ]
[]
[]
```

Expected Rust on 07714b, the lines that carry the question (`// header` is the standard derive header, as in fork-options-spec.md):

```rust
#[rustfmt::skip]
pub type Topic = core::Name;
#[rustfmt::skip]
pub type Source = core::Name;
#[rustfmt::skip]
pub type Hash = hash::Blake3;
#[rustfmt::skip]
pub type RelativePath = String;
// header
pub struct Location {
    pub source: Source,
    pub hash: Hash,
    pub relative_path: RelativePath,
}
```

- **5a, 5b.** What `Source` names is meaning carried by a comment on `Source`, not a type: both emit the lines above byte for byte. Layer: none.
- **5c, 5d, 5e.** What the hash covers is computed by the entry's writer (Curriculum or a Nexus), not by ethos-zero: no generated byte differs. Layer: none.
- **5f, 5h.** `Hash.Blake3` from a source: emits `pub type Hash = hash::Blake3;`, which no crate provides. **Inference**: with a real crate (`blake3::Hash`) the struct still fails to compile, since that type carries no rkyv or datom derives; the hash needs an ethos-declared type, e.g. `Blake3.Vector<Integer>` (the form is this spec's own).
- **5g.** The hash type stays open; the example writes `Hash.String` (review finding 4 calls this a string identifier), emitting `pub type Hash = String;`. Layer: none.
- Fixtures and goldens: all byte-equal; the candidate is an inline test in tests/ethos.rs. Acceptance: `a_registry_entry_generates`, asserting the lines above for 5a-5e and 5h, the `String` line for 5g.
- Finding: Q5's options are not separable by an ethos-zero dry run except through the hash type (5f/5h against 5g). The rest is Nexus or Curriculum behaviour.

## Q6. One registry or two, and where ethos-zero reads it

`reports/inline-import-research.md` §3, question 6: "**One registry or two.** Is the ethos library registry (resolving `flow:`) the same type as the context-module registry (`{ Subaspect Topic }`)? Which Nexus's Memory holds each, given there is no central store? Ethos-zero is not a Nexus: where does it read the registry from? A datom manifest (2026-08-20)? An assembly file (2026-08-21)? The `Generate` request?"

First edition, Q4 "The ethos import registry: one or two", proposed (book's own): "two registries. The core library's registry ships with the core library and is the same in every environment. The environment's registry belongs to the loaded environment." Review finding 4: this extends the Nexus file registry into an import registry, which no record does.

Options as worded; lettering this spec's own: 6a one type for both registries; 6b two types (library registry and context-module registry); 6c the book's two (core library's registry and the environment's); 6d "A datom manifest"; 6e "An assembly file"; 6f "The `Generate` request". "Which Nexus's Memory holds each" gives no options.

- **6a, 6b, 6c alone.** These choose the entry type a Nexus keeps; ethos-zero reads only what 6d-6f hand it. Layer: none; every fixture and golden byte-equal; no acceptance test in ethos-zero. Under 6c, **inference**: the core library's registry ships inside ethos-zero, since it is "the same in every environment"; that is option 8a's mapping (below) generalised to an entry.

The channels 6d-6f, built alone, check existence only: a source with no registry entry is refused; a registered one emits as today. This follows the 2026-08-20 ruling (the colon resolves from the manifest or is an error, flows/2b34fafa/vision/importResolution.md, cited in the research §1.5). The entry ethos-zero needs is this spec's own, the source name only:

```
Library
[]
[ Registry.Vector<Registered>
  Registered.{ Name.String } ]
[]
[]
```

The example, with only `flow` registered:

```
Library
[]
[ Launch.{ flow:Voice
           Brief.custom:Text } ]
[]
[]
```

Expected: refused, `Conceptual.{ [ 1 1 0 1 1 1 0 ] Source.custom }`. With `custom` removed: `pub voice: flow::Voice`, as today. Problem `Source` carrying the source text, no Form; the value is item 7's design (`Problem::Source`), the payload **inference**.

- **6d, datom manifest.** `Generation.{ String String String }`: source, target, manifest path. ethos-zero reads the datom file into `Registry`. Unreadable manifest: `Unreadable.{ path reason }`, as for the source.
- **6e, assembly file.** `Generate.String`, the assembly file's path; it names the source, the one target and the registry entries ("not more than one possible output", vision-raw/importResolution.md 2026-08-21). The file's root and sections are **inference**; no record draws them.
- **6f, Generate request.** `Generation.{ String String Registry }`: the entries travel inside the request datom on the argument line.
- Layers, all three: the contract (ethos-zero.ethos, src/main.rs), conception or checking (refuse an unregistered source at its head; the two `Source` sites, conception.rs:408 and :439), error.ethos and src/error.rs (`Source.String`). The library call `generate()` (src/lib.rs:542) takes the registry: **inference**, since a CLI-only check would leave tests/ethos.rs's 30 `generate()` calls unchecked.
- Changed: ethos-zero.ethos, error.ethos, src/error.rs, README.md (contract); tests/cli.rs (every request), tests/freshness.rs (its `fresh` passes a registry naming the fixture's sources), tests/ethos.rs (calls with sources).
- Byte-equal: every fixture and every tests/generated/*.rs, provided each test registry names `super`, `crate`, `std`, `serde`, `flow`, `protos`, `datom_codec`, `ethos_zero`, `custom`, `external` where used. Whether `crate`, `super` and `std` belong in a registry at all is not an option here.
- Acceptance: `an_unregistered_source_is_refused` (the example above) and, per channel, `the_registry_arrives_by_manifest`, `..._by_assembly_file`, `..._in_the_generate_request`, each running the CLI on the example and its fixed form.

## Q8. What the generator emits for core

`reports/inline-import-research.md` §3, question 8: "**What the generator emits for core.** `core::` collides with Rust (2.5). Is the emission `ethos_core::Name`? Which crate holds core's Rust?"

First edition, Q5 "What is emitted, and whether the imports section survives", proposed: "each registry entry also names what its source compiles to, and the generator emits that, never the source name itself." Its second half (the imports section survives for a source used more than once) is research question 11 and not dry-run here. Review finding 11: `ethos_core` is an invented crate name.

The question offers one worded alternative and an open one; the enumeration below is this spec's own, drawn from the research, the book and the solution: 8a `ethos_core::Name` (research); 8b the entry names the emission (book Q5); 8c refuse source `core` (ethos-solution item 7, the design's stopgap); 8d unchanged (07714b).

The example for every Q8 option:

```
Library
[ core:[ Name ] ]
[ Topic.core:Name
  Holder.{ Label.core:Name
           Name } ]
[]
[]
```

### 8a. Emit `ethos_core`

Source `core` emits as `ethos_core`, everywhere a source is written, beside the `std` mapping (src/generation.rs:152).

```rust
#[rustfmt::skip]
pub type Topic = ethos_core::Name;
#[rustfmt::skip]
pub type Label = ethos_core::Name;
// header
pub struct Holder {
    pub label: Label,
    pub name: ethos_core::Name,
}
```

- Layer: generation (both arms of src/generation.rs:142-163: the inline source and `Resolution::Imported`). Byte-equal: every fixture and golden. Acceptance: `the_core_source_emits_as_ethos_core`, comparing the text above. The Rust does not compile: no crate `ethos_core` exists (review finding 11). Order and field names are **inference**.

### 8b. The registry entry names the emission

Each entry carries the Rust path its source compiles to; generation writes that path, never the source name. Entry, this spec's own: `Registered.{ Name.String Emitted.String }`. With `core` registered as `ethos_core` the example emits exactly 8a's text; with `flow` registered as `signal_flow`, `Launch.{ flow:Voice }` emits `pub voice: signal_flow::Voice` (the research's collision 4). An unregistered source is refused as in 6d-6f.

- Layer: generation (the source tokens come from the entry), plus everything 6d, 6e or 6f changes. Cannot be built without one of them. Byte-equal: every fixture and golden when each test registry maps a source to itself. Acceptance: `a_registered_source_emits_its_entry`, comparing 8a's text and the `signal_flow` line.

### 8c. Refuse source `core` (item 7)

A source whose text is `core`, in an import or inline, is refused at its head. Other sources keep 07714b's behaviour.

Expected for the example: `Conceptual.{ [ 1 0 0 0 ] Source.core }`, the import read first (**inference**: sections are conceived in order). With the imports section empty and `Name` written `core:Name`: `Conceptual.{ [ 1 1 0 1 0 ] Source.core }`. In a struct position alone, `Library [] [ Holder.{ Label.core:Name } ] [] []`: `Conceptual.{ [ 1 1 0 1 0 1 0 ] Source.core }`. Problem `Source`, no Form.

- Layer: refusal, raised in conception at the two `Source` sites (conception.rs:408, :439) so the path is the head's; error.ethos gains `Source.String`, src/error.rs regenerated (`the_error_module_is_fresh`). Byte-equal: every fixture and golden. Changed: error.ethos, src/error.rs, src/conception.rs. Acceptance: `a_core_source_is_refused` (the three forms above) and, from item 7, `Topic.protos:Name`, `Topic.custom:Name` and `std:Mutex` unchanged.

### 8d. Unchanged

`pub type Topic = core::Name;`, `pub type Label = core::Name;`, `pub name: core::Name`; rustc refuses it. Layer: none. Acceptance: `a_core_source_emits_as_written`, pinning that text.

## Combinations

- 8a, 8c and 8d exclude one another. 8b replaces all three and is built only together with one of 6d, 6e, 6f, as one patch: {8b+6d}, {8b+6e}, {8b+6f}.
- 6d, 6e and 6f exclude one another. Each built alone is an existence check; with 8a or 8c it is one patch, since both touch the `Source` sites in conception: {6x+8a} emits `ethos_core` for a registered `core`; {6x+8c} refuses `core` even when registered (`Source.core`), so registering core proves nothing until 8c is dropped.
- 6a, 6b and 6c change no ethos-zero byte; they decide which Nexus entry type exists, so they pair with any channel without a build.
- Q5 interacts through its key, which holds `core:Name`. Q5's example under 8d emits `core::Name` and fails rustc; under 8a emits `ethos_core::Name`; under 8b needs `core` and `hash` registered; under 8c is refused at `Topic.core:Name`, `Conceptual.{ [ 1 1 0 1 0 1 1 1 0 ] Source.core }` (the first core use; path derived). So item 7's stopgap refuses the living's own registry key. With 5f/5h, `hash:Blake3` also needs 8b or a declared hash type.

Item 7's real form, one combination per reading of where `core` resolves. The readings are this spec's **inference**, drawn from the research §3 and the book's Q4:
- **Core is one registry entry, like `flow`** (research Reading A: "`core:Name` is then the lowercase form, with `core` as one registry entry"): {8b + 6a or 6b + one of 6d/6e/6f}. Expected: the example emits the entry's path; an unregistered `core` is `Source.core`.
- **Core's registry ships with the core library** (book Q4, 6c): {8b for the environment's sources + 8a's mapping held as a built-in entry + one of 6d/6e/6f}. Expected: `core` resolves with no environment entry; `flow` needs one.
- **Core's crate is fixed** (research Q8's literal reading): {8a} alone. Expected: 8a's text.

## Not an option here

Only the living can answer these; no candidate builds them:
- Which crate holds core's Rust (Q8, second half). No candidate names an existing crate; `ethos_core` does not exist.
- Which Nexus's Memory holds each registry (Q6); whether the import registry is the context-module registry at all (review finding 4).
- What the containing source is, what the hash covers, and whether blake3 is ruled (Q5): no ethos-zero byte depends on them.
- Whether Rust-path sources (`crate`, `super`, `std`, `serde`) enter the registry or stay Rust paths once the fallback is gone.
- The camelCase `core:Name` type and its check at creation; whether ethos-zero's own `Name` is that type.
- What the isos environment is (research question 9); the assembly file's form (6e).
- Whether the imports section survives (book Q5, second half; research question 11).
- The refusal value `Source` and its payload: item 7's design, no message text given.

Provenance receipt: unavailable.
