# Ethos audit: vision against ethos-zero

Implementation read: ethos-zero at /git/github.com/LiGoldragon/ethos-zero, HEAD c2653d (detached, equal to local `main`), crate version 16.0.0. Probes ran the existing `target/debug/ethos-zero` binary (mtime 2026-10-04, newer than the last `src/` commit of 2026-10-02; that it was built from HEAD is likely, not witnessed). No build and no `cargo test` was run; a test named below as backing an invariant was read, not run, unless marked "probe".

Probe files and their outputs are in /tmp/claude-1001/-home-li-primary/d5df1daf-854d-4469-8700-0997eb3babb1/scratchpad/probes (scratch; not durable).

## 1. The living's comments of 2026-10-09

The record /home/li/primary/flows/ebbe30/vision/ethos.md holds five sections dated 2026-10-09: one originating request and four comments on «The golden ethos». The brief named three; all four comments are quoted, in record order, so the main flow can pick.

### A. "The golden ethos is the ethos of ethos; kind is now trait"

Context: Comment on «The golden ethos», 2026-10-09.

> It's not ready, but it's a good push. The Golden Ethos would probably be the ethos of ethos itself, so we should do that too.
>
> This is a good example, Flow, since it's the first one we're making, but I don't think that we would say that we would put that code in the Vision Ethos. We would just say in the Vision Ethos that one of the best current examples of Ethos is Flow, and then they can load the Flow Ethos skill, which would have that code. Otherwise, we're going to duplicate ourselves.
>
> We can also use these flowcharts, although the kind has been changed to trait, so the flowchart in here doesn't actually work.

-- psyche, STT, 2026-10-09.

### B. "Mutex in ethos; implementers report what is hard to express"

Context: Comment on «The golden ethos», the diagram, typed 2026-10-09 18:23.

> This is good, and it reminds me: can we support mutex? I've seen mutex in Rust code once that was presented to me, and I was wondering if it was presented to me that way because we can't represent that abstraction in Ethos, or maybe we could. Maybe it's not hard. For any kind of exception or need or anything, we need to train any implementer to tell us if there is something that seems to be difficult to express in Ethos.

-- psyche, typed, 2026-10-09.

### C. "Trait; kind might be used to also mean traits"

Context: Comment on «The golden ethos» §1, typed 2026-10-09 18:25.

> If we agree that we can just use a trait, like I said, I don't know how the speech-to-text works. I'll see here. Let me see if it gets it. Yeah, I got it. I guess we can use traits. The main reason I switched to [kind] was just for speech-to-text reasons, and I thought maybe it was a better word. I think it is better, but not that much better. It might confuse the machine why we have two words, and you seem to be confused yourself. There were practical reasons. Now I'm not going to train the machine. To say that kind is not used, I think I would even just say that it might be used in the same context to talk about the same thing meaningfully (meaning that traits and kinds are so close in meaning that they're kind of interchangeable).
>
> You can land this without that last bit, without the negative guidance, and replace it with "kind might be used to also mean traits."

-- psyche, typed, 2026-10-09. Transcription corrected: "Kling" → "[kind]".

### D. "FlowId: not a struct, a string for now with a comment; new types, not aliases; a book on types; an Ethos Fable; special representation"

Context: Comment on «The golden ethos» §2, FlowId.{ String }, typed 2026-10-09 18:28.

> Well, this is already wrong. Ethos should be in the distill vision, but single-field structs are forbidden. If it was a string, it would be just a new type, and I want the new types not to be type aliases. That was never brought back to me. Also, type, new type, and type aliases: the difference, why we want new types, or why we might not. I need a book on that, but when I don't address a book, it has to be re-edited whenever the books are redone, and then we have an index book.
>
> First of all, it would not be a struct, and second of all, it should not be a string. I don't think we need it. Let's just leave it as a string for now, but let's put a comment there that says the string is very unideal, and we need a real ID based on the real hash bit that we're going to use to identify the flows.
>
> This also relates to the Ethos design, which should, by the way, have its own metaflow and psyche, at least secondary. We have more than enough right now to have a fable on Ethos. Let's get a fable on Ethos to make sure that we got the vision right, because there have been some changes, and I think the implementation doesn't follow them. There are some invariants that we want to enforce in the code.
>
> Also, the special representation is basically an implementation for a special way to decode and encode, so that the representation has a different type than the type when it's read into the Rust runtime. What would that look like? It would be a trait, a special representation, like a custom Datom conversion, basically. We need to be short, but we need to also describe what the trait is. It's a custom Datom, I guess, custom Datom, meaning a custom representation, encoding and decoding, and that needs to be implemented.
>
> In Ethos, we're going to describe the real type, the real Rust type that it has, and then the special representation is going to implement the representation type. We could maybe even somehow describe that type in Ethos, what that representation type is, which would be interesting because then we would force the input and output types, and we would let Rust do the implementation.
>
> I would like a book dedicated just for that, with some tests in Rust, done by Astra or Opus. Let's just do it with Opus because we have so much claude

-- psyche, typed, 2026-10-09.

## 2. The book «The golden ethos» and the rulings on it

Read with the Artifact tool, version 1791565140-b671 of https://claude.ai/artifact/F5ymU4N6ma6Rwt8RmNw7Lm. It opens with a figure (ethos file → types and kinds → associations) and holds three proposals, all targeting `psyche-skills/skills/vision-ethos.md`.

| # | Proposal | Ruling in the comments | Source |
|---|---|---|---|
| 1 | Name of the second anatomy: (a) keep kind, (b) "Trait is the word for the bearer of capabilities, the same word in ethos and in Rust; "kind" is not used." | Accepted (b), amended: drop the negative "kind is not used", replace with "kind might be used to also mean traits". | Comment C; also A ("the kind has been changed to trait") |
| 2 | "The golden standard": a new vision-ethos section with a Flow Nexus Library (FlowId, Layer, Details, Metaflow; kinds Layered, Wakeable; association Metaflow.[ Wakeable ]) that "every ethos file follows". | Rejected as placed: not ready; the code does not go into vision-ethos; vision-ethos says Flow is one of the best current examples and points to a Flow Ethos skill holding the code; the golden ethos is the ethos of ethos itself. Its line `FlowId.{ String }` is ruled wrong (single-field struct). The figure no longer fits because kind became trait. | Comments A, D |
| 3 | How a one-value type is written: (a) `FlowId.String`, a new type over String, vision-ethos "alias" wording changed to "a new type"; (b) `FlowId.{ String }`; (c) other. | (b) rejected: single-field structs are forbidden. For FlowId specifically, neither: leave it a plain String with a comment saying a string is very unideal and a real hash-based flow ID is needed. As a general rule the living wants new types not to be type aliases, which leans toward (a)'s "new type" reading but asks first for a book on type / new type / alias. | Comment D |

Additional orders in the comments that are not proposals of the book: Mutex support question and a rule that implementers report what is hard to express in ethos (B); a book on type vs new type vs alias (D); an Ethos Fable and an Ethos metaflow with at least a secondary psyche (D); a special-representation trait (custom datom encode/decode, possibly with its representation type declared in ethos), with its own book and Rust tests by Opus (D).

State of vision-ethos today (read through the Skill tool): the Kind section already reads "Trait is the word for the bearer of capabilities, the same word in ethos and in Rust; kind might be used to also mean traits." (Comment C landed.) The rest of vision-ethos still uses "kind" for the section and the concept, still calls `Name.Type` an alias ("an alias is not a new type and cannot carry a derive"), and has no golden-standard section, no single-field-struct rule, no Mutex, and no special representation.

## 3. Invariants, enforcement, and contradictions

Grades. Witnessed-probe: the binary was run on a probe file and its output observed. Witnessed-read: the enforcing code was read (and a test that asserts it was read, not run). Not enforced: the code was read or probed and does not enforce it. Unknown: the observation needed is named.

### 3a. Invariants the vision requires, and 3b. their enforcement

1. Four roots, Library / Signal / Operation / Memory; section orders fixed. Source: vision-ethos, Roots and Declaration: File ("Four roots: Library, Signal, Operation, Memory."; "A Library's sections, in order, are imports, types, kinds and associations.").
   Witnessed-read: `File` enum src/lib.rs:145-154; `Conceiving<File>` src/conception.rs:69-95 refuses other heads (`Problem::Root`), `Sema` as `Renamed.Memory` (conception.rs:92); section counts checked conception.rs:100-112. Tests: tests/ethos.rs `retired_roots_are_not_accepted`, `a_file_headed_sema_is_refused`; tests/cli.rs `a_file_headed_sema_is_rejected_naming_memory`. Operation's section order is marked "proposed, pending the living's word" in src/lib.rs:196-198 and ethos-zero.ethos; vision-ethos gives no Operation section order.

2. No version in a file. Source: vision-ethos, Declaration: File ("An ethos file carries no version").
   Witnessed-read (structural): the root must be one of four bare heads and the body exactly its sections (conception.rs:69-112); there is no place a version could sit.

3. Sweet form converted mechanically to the canonical braced form before reading. Source: vision-ethos, Declaration: File.
   Witnessed-read: src/canonicalization.rs (`Canonicalizable for String`, lines 14-70; `Resituating` maps errors back, lines 91-98). Test: src/lib.rs `sweet_structural_errors_resituate_to_the_authored_source`.

4. Imports `source:Name` / `source:[ … ]`; intrinsics String, Integer, Decimal, Boolean, Meaning, Vector, Option, Result, Self need none; generated code carries no `use`, names fully qualified. Source: vision-ethos, Imports.
   Witnessed-probe: generated files carry `std::vec::Vec`, `std::Mutex`, no `use` (probe golden.rs, m2.rs). Witnessed-read: test tests/ethos.rs `outer_option_and_result_are_written_fully_qualified`. Declaring an intrinsic's name is refused (`Problem::Intrinsic`, src/checking.rs:512-526; test `a_declared_intrinsic_name_is_refused_by_name`).

5. A struct field is named after its type in snake case, constructed types type-first, repeats as first/second. Source: vision-ethos, What a declaration turns into.
   Witnessed-read: src/generation.rs:556-659 (`SnakeCasing`, `Fielding`, `Ordinaling`, `FieldNaming`). Witnessed-probe: `flow_id_vector`, `string_mutex`. Beyond ten repeats the name falls back to `position_N_` (generation.rs:640-644); the vision gives no rule there.

6. Inline payload is a full type with a derived underscore name (`PathOverlap_Data`); a vector payload is carried as the vector. Source: vision-ethos, Inline types; A variant may declare its payload inline.
   Witnessed-read: `Inlining for File` src/checking.rs:840-860 (`X_Data`, `Owner_X_Data` on collision, `Enclosing_X_Data` when nested); collision with authored names refused (checking.rs:715-719; test `an_authored_name_capturing_a_derived_inline_name_is_refused`). Witnessed-probe: s2.rs nests to `A_Data_B_Data_C_Data_D_Data_E_Data`.

7. A variant named as a defined type carries that type. Source: vision-ethos, A variant named as a defined type carries that type.
   Witnessed-read: src/generation.rs:686-695 (`Variant::Bare` whose name has a declaration emits `Name(Name)`).

8. A type used once is declared inline; a type used in more than one place is declared once and named; inline nesting about three deep, past that the type comes from a Library. Source: vision-ethos, Inline types.
   Not enforced. Witnessed-probe: s2.ethos nests six enum levels and generates. No use-count check exists (no code counts references per type). The only `Depth` refusal is a cap of 512 type declarations (src/checking.rs:25, 954-956).

9. Every declared struct and enum bears Datomizable and Compositional; an alias carries no derive. Source: vision-ethos, Every declared type bears both kinds.
   Witnessed-read and probe: `DatomDeriving` src/generation.rs:777-788 emits on every struct and enum; aliases emit `pub type` with no derive (generation.rs:877-886). The derive named is `datom_codec::Composing`, not `Compositional` as vision-ethos writes; per knowledge-datom `Compositional: Composing` and the derive supplies both, so the substance matches and the vision text names the older form (inference).

10. The datom kinds are compiled in only where text is spoken: behind a feature the CLI enables and the Nexus does not. Source: vision-ethos, The datom kinds are compiled in only where text is spoken (`feature = "datom"`).
    Witnessed-read: `#[cfg_attr(feature = "datom", …)]` src/generation.rs:782, applied to every root. Tests: tests/signal_without_datom.rs (two tests), tests/flow_contract.rs `the_flow_nexus_contract_compiles_and_crosses_the_wire_with_and_without_datom`. knowledge-ethos names the feature `knowledge-datom`; the code says `datom`. That is a defect in the knowledge-ethos skill text, not in the code.

11. Placement carries the meaning: where types are defined a bracket is an enum, never a vector; head-then-symbol is an alias in types, a variant in queries/responses. Source: vision-ethos, Shapes and placement.
    Witnessed-read: `Conceiving<TypeDeclaration>` src/conception.rs:445-477 (braced → Struct, bracketed → Enum, bare → Alias); Signal/Operation sections read as variants (conception.rs:319-357).

12. Signal declares no Query/Response itself; Signal and Memory associations are implied, never written. Source: vision-ethos, Associations.
    Witnessed-read: Signal/Operation/Memory structs have no associations field (src/lib.rs:185-218); tests `a_signal_declaring_the_query_type_is_refused`, `…response…`, `an_operation_declaring_the_operation_or_outcome_type_is_refused`.

13. Kinds are explicit, never inferred; an association generates a compile-time assertion; bodies are hand-written. Source: vision-ethos, Kinds are explicit; bodies are hand-written.
    Witnessed-probe: golden.rs ends with `const _: () = { fn assert_metaflow_wakeable<T: Wakeable>() {} … }`. Witnessed-read: src/generation.rs:1095-1135; test `an_association_asserts_the_kinds_a_type_bears`.

14. In ethos there are no generics, only kinds; a constraint in a kind declaration is a kind, never a type; a data type carries no constraints. Source: vision-ethos, Kind and Identity.
    Witnessed-read: type declarations with constraints refused (src/checking.rs:1418-1423; tests `constrained_data_declarations_are_rejected`, `manually_constructed_constrained_data_is_rejected_before_generation`); constraints are referred with `Role::Kind` (checking.rs:1026-1041).

15. A kind's identity is its name and constraints, compiled as a Rust trait's generic parameters with bounds. Source: vision-ethos, Identity.
    Witnessed-read: `Parametrizing for Identity` src/generation.rs:213-243; test tests/generated.rs `constrained_kind_identity_compiles`.

16. Kind syntax: receivers `.` `!` `:`; capability with inputs is a headed brace; a yield bracket holds one type; complex kind is four brackets. Source: vision-ethos, Kind syntax.
    Witnessed-read: `Conceiving<Receiver>` conception.rs:512-519; `Problem::Yield` on a yield bracket not holding one (conception.rs:577, 601); `KindBody::Complex` lib.rs:312-326. Witnessed-probe: `fn wake(&mut self) -> FlowId` from `wake![ FlowId ]`.

17. A capability speaks in Self, the kind's parameters and other kinds; a concrete type in an input is a kind not yet named. Source: vision-ethos, Kind.
    Witnessed-read: `Signing for Reference` src/checking.rs:1567-1580 refuses a concrete input with `KindWanted`; tests `a_concrete_type_in_an_input_is_refused_as_wanting_a_kind`, cli `check_takes_a_kind_in_an_input_and_locates_a_concrete_type_there`. A yield may name a concrete type (vision does not forbid it).

18. Kinds are qualifier-named (Runnable, Textualizable). Source: vision-ethos, Naming.
    Not enforced. No check reads a kind name's form; only capitalization is checked (checking.rs:522).

19. A type or kind name is capitalized; a datom head (a variant) is always capitalized. Source: vision-ethos examples throughout; knowledge-datom, Syntax ("In datom a head is always a variant, so it is capitalized.").
    Types and kinds: witnessed-probe (`lower.[ a b ]` refused `Case.lower`) and test `a_lowercase_type_or_kind_name_is_refused`. Variants: not enforced. Witnessed-probe: `Low.[ lowvariant Other ]` generates `pub enum Low { lowvariant, Other }`; `Variant::check` calls only `define()` (src/checking.rs:1453-1477).

20. The inline derived name's underscore "never collides and reads at a glance as inferred from the sugar". Source: vision-ethos, Inline types.
    Partly enforced. Collision with a derived name is refused (item 6). An authored underscore name is accepted: probe `Under_Score.{ String Integer }` generates; the crate's own ethos-zero.ethos authors `Generation_Error`. An authored underscore name no longer reads at a glance as derived.

21. Ethos canonical spacing and vertical expansion. Source: vision-ethos, Spacing.
    Witnessed-read for the printer: src/printing.rs delegates to protos `Textualizable`; tests tests/print.rs (`a_one_line_layout_expands_to_the_canonical_print`, `leaves_stay_on_one_line_and_angles_stay_tight`, `a_badly_hung_layout_is_realigned`, round trips). Not enforced on input: probe s2.ethos with `Deep.[ A.[ B.[ … ] ] ]` on one line is accepted. Whether the vision wants the reader to refuse non-canonical layout is not stated (unknown).

22. Ethos carries a comment on every section and on every line that has a next layer. Source: vision-ethos, Spacing.
    Not enforced, and contradicted by the printer (see 3c-2). Witnessed-probe: s2.ethos, m2.ethos, single.ethos carry no comment and are accepted. Witnessed-read: tests/print.rs:135-150 compares the crate's own ethos to its print only after stripping `;` lines, because `File` has no field for comments and the print emits none.

23. Generation by request, `ethos-zero 'Generate.{ /abs/x.ethos /abs/out }'`; one inline datom argument, no flags; generated Rust committed and held fresh by a test. Source: vision-ethos, Generation; knowledge-datom, The interface shape.
    Witnessed-probe: `Generate.{ … }` writes and replies `Generated.[ … ]`; two arguments reply `Arguments.2`. Witnessed-read: tests/freshness.rs (error.rs, ethos-zero.rs, every fixture, the Flow Nexus files).

24. Self-description: a datom object's basic CLI help emits the Ethos that describes its anatomy. Source: vision-ethos, Self-description.
    Witnessed-probe: no-argument run prints ethos-zero.ethos (the CLI contract). Test tests/cli.rs `no_argument_prints_the_crates_own_ethos_ending_with_a_newline`.

25. The golden ethos is the ethos of ethos itself. Source: comment A.
    Not met. ethos-zero.ethos describes only the CLI's Query/Response and error.ethos the reader errors. The language's own concept, `File`, `Library`, `TypeDeclaration`, `Variant`, `KindDeclaration`, `Capability`, `Association` (src/lib.rs:143-384), is hand-written Rust, not generated from an ethos file.

26. Single-field structs are forbidden. Source: comment D ("single-field structs are forbidden"); earlier record /home/li/primary/flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md (2026-09-03, "a single-field struct … would be really bad design"), archived as distilled into vision-datom, but no distilled skill read (vision-ethos, vision-datom, knowledge-datom) carries the rule today.
    Not enforced. Witnessed-probe: the book's golden file generates three single-field structs, `FlowId { string }`, `Topic { string }`, `Past { flow_id_vector }`; `Unit.{}` (zero fields) also generates. No arity check on `TypeDeclaration::Struct` (src/checking.rs:1428) or `Variant::Struct`.

27. New types, not type aliases. Source: comment D ("I want the new types not to be type aliases").
    Contradicted (3c-1).

28. Implementers report what is hard to express in ethos; Mutex question. Source: comment B.
    Not expressible today (observation and inference). Witnessed-probe: import `std::sync:Mutex` and `std::sync:[ Mutex ]` are refused `Expected.Import` at the import; cause unknown (the `Source` doc at src/lib.rs:62 claims `std::clone` is a valid source; the multi-segment form was not reached, so the refusal likely comes from how protos splits `::` before `:`, not witnessed). `std:Mutex` is accepted and emits `std::Mutex<String>`, a path that does not exist in std. Inference, not compiled: even with a correct path the holding struct derives `rkyv::Archive`, `Clone`, `PartialEq`, `Eq`, `Hash` (generation.rs:781), which `std::sync::Mutex` does not implement, so the generated Rust would not compile. vision-nexus says "Arc-Mutex is permitted", without an ethos form.

29. A special-representation trait (custom datom encode/decode; representation type possibly declared in ethos). Source: comment D.
    Not present. No "representation" occurs in src/ (grep). It is a requested design, not yet a vision sentence.

30. Every trait is written in ethos; hand-written code that is not ethos-generated declares no trait. Source: compensation-design skill ("Every trait is written in ethos; hand-written code that is not ethos-generated declares no trait.").
    Contradicted (3c-3).

31. No tuple in the code we design, except at a contact point that forces one. Source: vision-ethos, Associations.
    Generated code: witnessed-probe, no multi-field tuple; every variant carries one value. Hand-written code: contradicted (3c-4).

32. Memory: a memory kind carries a standard successful-or-unsuccessful change and, per version, the upgrade from the previous format. Source: vision-ethos, Roots.
    Not implemented. `Memory` is imports plus record types (src/lib.rs:213-218); no "upgrade" or version handling in src/ (grep).

### 3c. Where the implementation does what the vision contradicts

1. Aliases. `Name.Type` emits `pub type Name = Type;` (src/generation.rs:877-886; test tests/generated.rs `aliases_name_their_types`). The living's comment D wants new types, not aliases. vision-ethos itself still prescribes the alias ("A declaration turns into…": `pub type LockId = Integer;`), so the code follows the current skill and both are out of line with comment D. The form a new type should take (a single-field tuple struct would collide with item 26) is the open question the living asked a book for.

2. Comments. vision-ethos requires a comment on every section and every line with a next layer; the canonical print (src/printing.rs, protos `Textualizable`) emits no comment, `File` keeps none, and a reprinted file loses every comment. The repository's own ethos files violate the rule: ethos-zero.ethos and error.ethos carry header comments only, and fixtures/print/flow-library.ethos carries none.

3. Hand-written traits. About 95 trait declarations in hand-written source (grep count of `trait ` lines: lib.rs 17, checking.rs 20, generation.rs 22, conception.rs 12, protosization.rs 8, main.rs 7, sectioning.rs 3, location.rs 3, signature.rs 2, canonicalization.rs 1). Only error.rs and ethos-zero.rs are generated, and they declare none.

4. Tuples in hand-written code. Tuple-carrying enums in the public concept: `Import::One(Source, Imported)`, `Import::Many(Source, Vec<Imported>)`, `TypeDeclaration::Struct(Identity, Vec<Position>)` and siblings, `Variant::Typed/Struct/Enum` (src/lib.rs:222-299); a tuple vector `Vec<(&Protos, Option<&Vec<Protos>>, usize)>` (src/conception.rs:152); `(bool, String)` in tests/cli.rs:6; `(Vec<i64>, Problem)` in tests/ethos.rs:293. `pub struct Name(String)` (src/lib.rs:60) is also a single-field tuple struct. src/lib.rs:295 documents `Variant::Struct` as "a tuple variant: `Node.{ Tree Tree }`", while the generated Rust gives it a named `_Data` struct; the comment is wrong about the generated form.

5. Free functions. src/lib.rs:32-34 states "no free function, is the crate's own rule", yet tests/cli.rs (`opaque`, `generate`, `check`) and tests/ethos.rs (`read`) define free functions. The rule's origin in a vision skill was not found in this audit (unknown).

6. Vocabulary. Code, error surface and ethos sections use "kind" (`KindDeclaration`, `Form::Kind`, `Role::Kind`, `Problem::KindWanted`, section "kinds"). The landed ruling says trait is the word and "kind might be used to also mean traits", so this is not a contradiction; whether the section and the error names should become trait is a ruling the living has not given.

### Unknowns

- Whether `target/debug/ethos-zero` was built from c2653d: needs a rebuild or a build-id comparison.
- The test suite's current pass/fail state: needs `cargo test` (or the flake check) on Prometheus.
- Why `std::sync:Mutex` is refused at the import: needs reading protos's colon handling or a protos probe.
- Whether a Mutex position would compile with a correct path: needs a compile of the generated module.
- Whether the reader should refuse non-canonical layout or missing comments, or only the printer should hold them: the vision states the form, not who enforces it.

## 4. Weighing by the living's rule, and the added sources

Rule applied, as relayed by the coordinator from Psyche Core Secondary: "the recent vision and the one that's been repeated a lot, which hasn't been overridden by newer decisions or statements", raw records included. Added sources read: /home/li/primary/flows/ebbe30/reports/book-audit-verified.md (C3-C9), /home/li/primary/flows/445410/vision/ethos.md, «The Flow Nexus vision» (https://claude.ai/artifact/KEzNHLfQJUcoyyyyqfo5Mz, version 1791563988-1d73), and the raw records those findings cite.

### 4a. Vision-ethos lines a newer statement overrides

| vision-ethos line (loaded skill) | Overridden by | Effect on the audit |
|---|---|---|
| "A declaration turns into…": `pub type LockId = Integer;`; Variant section: "FilePath is an alias of String", `pub type FilePath = String;`; "an alias is not a new type and cannot carry a derive" (book-audit C3, C4) | "It's a new type" (d4ae97/vision/ethos.md:45-49, typed 2026-10-06); "We want new types not type aliases." (d4ae97/vision/ethos.md, "Newtypes, not type aliases", 2026-10-06); "a new type should be just the name of the type and then the separator, which is a period, and then the name of the contained type" (8e9e77/vision/single-field-structs.md:15, 2026-09-08); comment D (2026-10-09). Four statements over five weeks: recent and repeated. | Item 27 and 3c-1 stand as a contradiction of current vision, not only of comment D. `Name.Type` is the new-type syntax; the generator emits an alias for it. |
| Roots: "Sema's are record types… Signal gives a Nexus its main types and Sema its database types." (C5) | "signal, operation, and memory" (91ea9f/vision/ethos.md:44, 2026-10-02) and the four-roots line already in the skill. | The implementation already follows Memory (item 1). The skill carries both lines. |
| Spacing: "a structure with more than one element opens on its line and its elements hang beneath the first, aligned" (C9) | "the new line indentation style, which should be favored over starting indentation on the same line" (e5a0bc/vision/ethos.md, 2026-10-06); "a new line and an indented new line for each element" (same file, 2026-10-07); d4ae97/vision/ethos.md "Line breaking" (2026-10-06): a block that would run too far right opens its first element on a new line, indented; vectors may wrap at a width aligned with the first item. | Item 21 changes grade: the printer's hang-aligned layout (protos `Textualizable`; knowledge-ethos "its elements hang aligned beneath the first"; tests/print.rs `a_badly_hung_layout_is_realigned`) now contradicts the newer vision. Added invariant: a comment sits above or beside what it comments on, lined up with its element (e5a0bc, 2026-10-06 and 2026-10-07); not enforced, since comments are dropped (item 22). |
| Inline types: "a type used in more than one place is declared once and named" | "I would want to make the inline declaration mandatory unless that particular type is so deep that it itself requires too much recursion to be declared inline. We have to explain some kind of algorithm…" (d4ae97/vision/ethos.md:40, 2026-10-06) | Item 8 now reads: inline is the default and the depth rule decides. Not enforced, and no algorithm is specified yet. |
| C4's proposed `FlowId.Integer` ("The flow ID is not a string, it's a hash.", edf227/vision/identifiers.md, 2026-10-03) | Comment D (2026-10-09): "Let's just leave it as a string for now, but let's put a comment there that says the string is very unideal". | For now, FlowId is a String with that comment. The hash identity stays the target. |

### 4b. Invariants added or strengthened

33. Single-field structs are refused in ethos. Sources: e4a40e archive (2026-09-03); 8e9e77/vision/single-field-structs.md:5-13 (2026-09-08, "I think we should possibly even refuse single-field struct types and ethos… This should be a new type"); comment D (2026-10-09, "single-field structs are forbidden"). Repeated and recent. Not enforced (item 26; probe).

34. No double wrapping: a new type does not wrap another new type. Sources: 8475a9/vision/flow.md:62 and d4ae97/vision/ethos.md:7 ("Don't double-wrap types."). Not enforced. Witnessed-probe: the Flow Nexus vision Memory, with `Event` replaced by `String` (the book's `Event` is undeclared and is refused `Undeclared.Event`), generates `pub type Topic = Dense; pub type Dense = String;`, and every `Name.Type` in it becomes `pub type` (`Past`, `Queue`, `Session`, `Events`).

35. Traits are load-bearing: "A trait that only has one function is suspicious and a trait that's only implemented by one type is doubly suspicious." (d4ae97/vision/ethos.md, "Traits are load-bearing abstractions", 2026-10-06). A design heuristic, not a checker rule; ethos-zero does not check it. Observation: most hand-written traits in ethos-zero have one method and one implementer (for example `Serving`, `Exiting`, `Invoking`, `Texting` in src/main.rs:23-36; `Fielding`, `Ordinaling`, `SnakeCasing` in src/generation.rs). That is a second ground for 3c-3.

36. Special representation (445410/vision/ethos.md, relayed from comment D): a trait for a custom datom encode/decode, so that the representation has a different type than the runtime Rust type; ethos describes the real Rust type, and possibly the representation type, "then we would force the input and output types, and we would let Rust do the implementation". Invariants this record implies, stated as the record's own and not designed here: (i) the ethos-declared type is the runtime type; (ii) a declared representation type, when present, fixes the encode input and decode output; (iii) the conversion body is hand-written Rust. None exists in ethos-zero. edf227/vision/identifiers.md (2026-10-03) gives the first consumer: FlowId held as a hash, its text forms only serialization. This is 445410's work.

37. Show the ethos, not the Rust it generates, unless the work is on generation (d4ae97/vision/ethos.md, 2026-10-06). This concerns books, not the generator. vision-ethos's many Rust blocks are allowed because they teach generation.

### 4c. «The Flow Nexus vision» and ethos

The book proposes a new skill `vision-flow-ethos.md` holding the Flow Nexus Memory and Signal ethos, plus a dependency line in vision-flow. This is the "Flow Ethos skill" that comment A wants vision-ethos to point to. Read for ethos content:

- It uses `Name.Type` in struct positions as new types (`Past.Vector<FlowId>`, `Session.String`, `Modules.Vector<Name>`, `Brief.String`). The generator makes each an alias (34).
- `Topic.Dense` / `Dense.String ; PascalCase, one to four words, letters only; checked on the way in` is a type that carries a validation, the kind of case the special representation or a validating new type serves (36). It is also a double wrap (34).
- `Refreshed.{ FlowId FlowId }` is a two-position inline payload; the generator names its fields `first_flow_id`/`second_flow_id` and drops the book's comments "the successor"/"the predecessor".
- Its layout opens each element on a new indented line with comments beside, the newer style (4a). It does not match the canonical print that ethos-zero produces.
- `Events.Vector<Event>` names an undeclared `Event`; the Memory file as written is rejected (probe).
- Whether the living has ruled on this book was not checked (unknown); no comment record for it was located in this audit.

## Sources

- /home/li/primary/flows/ebbe30/vision/ethos.md (read).
- «The golden ethos», https://claude.ai/artifact/F5ymU4N6ma6Rwt8RmNw7Lm, version 1791565140-b671 (Artifact read).
- Skills loaded through the Skill tool: vision-ethos, knowledge-ethos, intent-anatomy, knowledge-datom, operation-flow-evidence. compensation-design, vision-datom and vision-nexus were grepped as files (bottom stratum, cited as text only).
- /home/li/primary/flows/e4a40e/vision/archive-newtypeWrappingAndSingleFieldStructs.md; /home/li/primary/flows/d63804f2/vision/newtypeWrappingAndSingleFieldStructs.md.
- /git/github.com/LiGoldragon/ethos-zero at c2653d: src/lib.rs, src/checking.rs, src/conception.rs, src/generation.rs, src/printing.rs, src/main.rs, ethos-zero.ethos, error.ethos, fixtures/print/flow-library.ethos, tests/*.rs (read).
- Probes: the scratchpad probes directory named at the top (single, s2, mutex, m2, m3, golden; no-argument and two-argument runs).
- Added on the coordinator's message: /home/li/primary/flows/ebbe30/reports/book-audit-verified.md (C1-C9); /home/li/primary/flows/445410/vision/ethos.md; «The Flow Nexus vision», https://claude.ai/artifact/KEzNHLfQJUcoyyyyqfo5Mz, version 1791563988-1d73; /home/li/primary/flows/d4ae97/vision/ethos.md; /home/li/primary/flows/e5a0bc/vision/ethos.md; /home/li/primary/flows/edf227/vision/identifiers.md; /home/li/primary/flows/8e9e77/vision/single-field-structs.md; /home/li/primary/flows/8475a9/vision/flow.md:62; probe fnmem.ethos.
- Provenance receipt: unavailable (no PROVENANCE handoff; FLOW_ID and FLOW_DIRECTORY were empty in this environment, so the path came from the brief).
