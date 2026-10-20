Audit of the Ethos examples. This is evidence for the book's author only; it does not go into the book.

Checker used: ethos-zero 423103d (the ethos-proposals branch), run as
`nix run --option substituters https://cache.nixos.org github:LiGoldragon/ethos-zero/423103d -- '<request>'`.
The flake has no `ethos-proposals` attribute, and the prometheus cache timed out.

The library was declared two ways:
- File a: `Library.{ [] [ Word.{ String } Topic.[ Core Ethos Nexus Word ] ] [] [] }`.
- File b: the same, with `Word.String` (an alias) in place of `Word.{ String }`.

What Inspect witnesses:
- File a is accepted and generates `struct Word { string: String }` and `enum Topic { Core, Ethos, Nexus, Word(Word) }`.
- Both types carry `derive(Datomizable, Composing)` behind the feature `datom`.
- The Word variant is an ordinary variant, using the existing rule "a variant named as a defined type carries that type".
- No extendable-enum semantics exist in the checker: no open or extendable enum, and no casing check on variants or datom text. The patterns searched were extend, open.enum, non.exhaustive, uncapital, lowercase, camel, capitaliz, is_uppercase and is_lowercase.
- A case check exists only for declared type and trait names (src/checking.rs:528).

Conform on Topic, exact results (a = struct Word, b = alias Word): These runs used the earlier name Word; Coinage is the same shape.

| Datom text | Result for a | Result for b |
|---|---|---|
| `Core` | `Conformed.{ Topic Core }` | same as a |
| `sourceNexus` | `Unconformed.{ Topic Error.{ Composition [] Variant.{ Topic sourceNexus } } }` | same as a |
| `Word.{ sourceNexus }` | `Conformed.{ Topic «Word.{ sourceNexus }» }` | `Unconformed … Form.{ String Struct }` |
| `Word.sourceNexus` | `Unconformed … Form.{ Struct Bare }` | `Conformed.{ Topic Word.sourceNexus }` |
| `Word.«Source Nexus\»` | `Unconformed … Form.{ Struct String }` | `Conformed.{ Topic «Word.«Source Nexus\»» }` |
| `Word.source_nexus` | `Unconformed … Form.{ Struct Bare }` | `Conformed.{ Topic Word.source_nexus }` |
| `Word.SourceNexus` | `Unconformed … Form.{ Struct Bare }` | `Conformed.{ Topic Word.SourceNexus }` |

Gaps. Each one is a proposal with no implementation yet; the code follows once it is ruled.

1. **Bare made word in data** (Proposals 1 and 11).
   - Not implemented: a bare `sourceNexus` is refused as an unknown variant, so the enum is closed today.
   - The data example `[ Core sourceNexus ]` from the earlier Topic runs does not conform. `[ Red seaFoam ]` was not run; by the same closed-enum rule, it is expected to fail.
2. **Refusing a malformed word** (Proposal 8).
   - Not implemented: any string conforms in any casing (`Word.«Source Nexus»`, `Word.source_nexus`, `Word.SourceNexus`).
   - The check needs Coinage to be its own type, not an alias. For that reason the book declares `Coinage.{ String }`.
3. **Generation** (Proposal 7).
   - What is generated is witnessed.
   - What produces it is not something specific to extendable enums; it comes from the existing named-type rule.
4. **Unmarked extendable enum** (Proposal 6).
   - There is no real code for it.
   - `Topic.[ Core Ethos Nexus ]` generates a closed enum with no Coinage variant, so Proposal 6 carries no example.
5. **Promotion and stored values** (Proposals 9 and 10; 10 is now an explicit migration).
   - Not implemented.
   - Proposal 10 is a machine proposal. The living has said nothing about values that are already stored.
6. **Trait names.**
   - vision/ethos.md (lines 308–341) names the two traits `Datomizable` and `Compositional`.
   - The checker derives `datom_codec::Datomizable` and `datom_codec::Composing`.
   - The names differ between the vision and the code. The Ethos seat should take this up separately.
7. **Ethos form of the traits.**
   - An Ethos declaration does not show its traits. They are generated.
   - So every Ethos example in the book is paired with the generated Rust that shows both traits: Proposals 5 and 7; the Flow generated code sits under Proposals 14, 16, 20 and 21, the file it lands in.
8. **The flow checkout.**
   - Proposals 13, 14, 18 and 20 are against origin/main 67b80b3; Proposals 15 and 16 are against 67b80b3 with Proposals 13 and 14 applied, and Proposals 19 and 21 with Proposals 18 and 20 applied.
   - Switching Topic from String to an enum also touches store.rs and the other consumers listed under Code consumers of Topic.
9. **A bare topic under Proposal 13.** Under Proposal 13, `Topic.Coinage` is an alias of the struct, and Conform of Topic «core» gives `Unconformed.{ Topic Error.{ Composition [] Form.{ Struct Bare } } }`. A bare topic needs the bare reading of Proposal 11, or Coinage declared as an alias of String, which cannot carry its own check.
10. **The revision's checker runs.** At ethos-zero c4d82bf, Check returns `Checked` for Colour with Coinage (Proposal 5), Flow's library.ethos under Proposal 13, under Proposals 13 and 15, under Proposal 18, and under Proposals 18 and 19 (each applied to 67b80b3). The Rust hunks of Proposals 14 and 20, applied to the committed library.rs at 67b80b3, of Proposal 16, applied on top of Proposal 14, and of Proposal 21, applied on top of Proposal 20, equal byte for byte the Inspect output for the same Ethos. The Rust of Proposal 7 equals the Inspect output for the Ethos of Proposal 5. Every hunk of the book applies at exactly one place in its file: prose hunks at psyche-context main b938651, code hunks at Flow 67b80b3. The book has no datom example.
11. **Records behind the revision.**
    - 09562a (2026-10-11), at flow-evidence/da2038/unrelayed-comments-2026-10-17.md:240: topics start lowercase, and core is the permanent topic.
    - The 2026-10-16 record, at flows/da2038/vision/flow.md:213: every topic is uncapitalized, core and ethos included.
    - cd4395 (2026-10-12): "name" and "word" are rejected; give a few attempts at the type's name.
    - These records put a lowercase core first (Proposals 12 to 16). A capitalized Core is the amendment (Proposals 17 to 21).
    - The type names Coinage, Epithet and Appellation are machine candidates (Proposals 2, 3 and 4).
12. **Executable examples.** The data examples are gone. Proposal 11 (bare reading) stays as vision with no example until it is implemented. At ethos-zero c4d82bf, on the library of Proposal 18, Conform of Topic «fooBar» gives `Unconformed.{ Topic Error.{ Composition [] Variant.{ Topic fooBar } } }` and Conform of Topic «Core» gives `Conformed.{ Topic Core }`.
13. **The coinage check, in each alternative.**
    - Lowercase core (Proposals 15 and 16). The `Coined` trait, its `coin` capability and `Malformation.[ Capitalized NotCamelCase ]` are declared in Ethos; at ethos-zero c4d82bf, Check returns `Checked` for Proposals 13 and 15 applied to 67b80b3. Proposal 16 is the generated code for it: the `Malformation` enum, the `Coined` trait with `fn coin<N: protos::Textualizable>(input: N) -> std::result::Result<Self, Malformation> where Self: Sized`, and one assertion each that Coinage and Topic bear `Coined`. Under Proposal 13, Topic is an alias of Coinage (`pub type Topic = Coinage;`), so its assertion names the same type as Coinage's (this flow's reading of the generated code).
    - Capitalized Core (Proposals 19 and 21). The same trait and capability, with `Malformation.[ UndeclaredVariant NotCamelCase ]`, and Topic alone bearing `Coined`; Coinage does not. At ethos-zero c4d82bf, Check returns `Checked` for Proposals 18 and 19 applied to 67b80b3, and Proposal 21 on top of Proposal 20 equals byte for byte the Inspect output: the `Malformation` enum after Topic, the same `Coined` trait, and one assertion that Topic bears it.
    - In both, the body of `coin` is hand-written and unimplemented.

## Code consumers of Topic

The work was done in a disposable worktree of origin/main 67b80b3 and built on the builder; the active checkout was not touched. Full diffs:
- A (Proposals 13 and 14): scratchpad/topic-out/topic-a.diff
- B (Proposals 18 and 20): scratchpad/topic-out/topic-b.diff
(scratchpad = /tmp/claude-1001/-home-li-primary/804eb927-4185-5e72-9f8d-a83a88a5c12f/scratchpad)

- **Generation.** crates/flow-ethos/src/generated/library.rs is committed. build.rs regenerates it with ethos-zero 07714b0 and panics if the committed file is stale. The regenerated file is therefore part of the change, under Proposals 14 and 20, and 16 or 21 with the check.
- **Consumers.**
  - store.rs:5244 builds the record key "{aspect}:{len}:{topic}:{layer}". It is called from the store, address_hold, refresh and metaflow.
  - send_tool.rs:209 parses the topic from tool-call JSON.
  - context.rs:106 passes it to CallerMetaflow.
  - title.rs:60 lowercases it into the native title.
  - waking.rs:757 prints it.
  - flow and flow-meta CLI datom inputs (Start, Replace, Configure, Refresh).
  - Fixtures across about 15 files.
  - signal-flow imports Topic and compiles unchanged.
- **A** touches 17 files (+52, -47). Record keys and titles are unchanged. The datom form of an Address becomes `{ Mind { flow } Secondary }`, which reaches CLI input and the queued-request text in prompts.
- **B** touches 18 files (+76, -47). It adds a hand-written `Topic::word()` / `from_word()` with no trait, spelling Core as "core" both ways. That spelling is unruled, and an implementation without a trait sits against "Traits are explicit". Record keys and titles are unchanged. The datom form becomes `{ Mind Coinage.{ flow } Secondary }` and `{ Field Core Primary }`.
- **Tests, both alternatives.** `cargo check --workspace` is clean. `cargo test --workspace` gives flow-nexus lib 316 passed, 1 failed, 5 ignored. The one failure, a_pending_call_is_answered_after_start_and_reconnect, also fails on unmodified 67b80b3.
- **Stored data.** The live store is /home/li/.local/state/flow-production/flow.sema (redb, rkyv). Schema labels are hand-written, so a layout change is not detected automatically. B changes the layout; A may keep it (inferred, untested). A migration is needed for every record carrying an Address (metaflow, lock, address hold, refresh, launch attempt): a new version label, the old-layout type, and an UpgradeFrom conversion, as the existing StoredMetaflowV1→v2 does. No compatibility path was added. Doc examples, deployment command lines and the messenger's Address datoms also carry the old text form.
- **Open choices.** The datom text form under A or B. How Core is spelled under B. Whether a topic should read bare, which needs Proposal 11 implemented, or Coinage as an alias of String, which cannot carry its own check.

## What a landing still needs

The declaration and generated-file excerpts in the book (Proposals 13 to 16, or 18 to 21) are not a complete landing of either alternative. Each alternative also needs all of the following before it can be deployed:
- **Consumer changes.** The edits to every consumer of Topic listed above: the store's record key, the send tool's parsing, the caller metaflow, the native title, waking's output, the flow and flow-meta CLI inputs, and the fixtures. These are in the A and B diffs; neither is in the book.
- **A store migration.** A new version label, the old-layout type, and an UpgradeFrom conversion for every stored record carrying an Address, as StoredMetaflowV1 to v2 does. B changes the layout. A may keep it; that is inferred and untested, so A needs the migration or a test showing the layout unchanged.
- **The body of coin.** The hand-written implementation of `Coined` for the alternative's types: under A, Coinage and Topic refusing `Capitalized` and `NotCamelCase`; under B, Topic reading Core as the fixed variant, an uncapitalized camelCase word as a coinage, and refusing `UndeclaredVariant` and `NotCamelCase`. B's hand-written `Topic::word()` / `from_word()` gives way to it.
- **A ruled text form.** The living's ruling on how a topic is written in datom: under A, `{ Mind { flow } Secondary }`, or a bare topic, which needs Proposal 11 implemented; under B, `Coinage.{ flow }` and the spelling of Core. Doc examples, deployment command lines and the messenger's Address datoms then follow that form.
