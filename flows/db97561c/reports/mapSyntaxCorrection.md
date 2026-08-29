# Correct the Ethos maps and the schema reader to the ruled syntax

A prompt for the implementing flow. Scope: syntax of the type-and-kind map files and the reader/emitter branch that handles them, across the new stack. Not in scope: the kind vocabulary (Datomic vs Embodied/Textualizable), the costume kinds, the invented type names, the six data-syntax atoms — those wait for separate rulings.

## 0. Standing

The overnight flow 01a04a30 authored `protos.ethos`, `datomic.ethos`, `ethos-zero.ethos` and six consumer maps in an invented dialect: a `Schema.{0 1 0}` head (Schema is the dead ancestor's name), `Name.Struct.{…}` / `Name.Enum.[…]` / `Name.Tuple.[…]` / `Name.Alias.{…}` markers, `Visibility.Public`, `Private.X` / `Public.X` fields, `Methods.[… Receiver.Shared Output.… Inputs.[…] Associated.[…] Supertraits.[…] Default.Chain.[…]]`, `NonExhaustive.Yes`. None of it is Ethos. It happened because the previous prompt never defined this file kind and accepted E2 on "generated Rust identical to the hand-written Rust", which makes the map a transcript of Rust. This prompt defines the file kind exactly and turns the acceptance around: the map is upstream, the Rust is emitted from it.

Rule of conduct for this flow: **when you meet a form this prompt does not define, stop and ask the living.** Do not settle syntax by judgment, even if told to keep going; report what is missing and wait.

## 1. The library file, exactly

    Library.{0 1 0}
    []
    {
      [
        Extent.{Start.Integer End.Integer}
        Separator.[Period Exclamation Colon]
        Symbol.{String}
        Portion.[Headed.{Extent Headed} Enclosed.{Extent Enclosed} Bare.{Extent Symbol}]
        Headed.{Head.Symbol Separator Body.Portion}
        Fault.{Extent Problem.FaultProblem}
        Layout.[Flat]
      ]
      [
        Delineatable.[ delineate.[ Result<Delineation Fault> ] ]
        Embodiable.[ embody.[ Result<Embodied Fault> ] ]
        Embodied.[ embody:{[Portion] [Result<Self Fault>]} ]
        Textualizable.[ portion.[ Portion ] ]
        Printing.[ print.{[Layout] [Text]} ]
      ]
      [
        Text.[ Delineatable Embodiable ]
        Portion.[ Printing ]
      ]
    }

Header: `Library.{major minor patch}` — the head of a types-and-kinds file. Imports: the second object, `[]` when empty, otherwise the ruled import references (`source:Object`, `source:[A B]`, `source:file.[A B]`). Body: one braced object with three bracketed sections in this order — types, kinds, associations. Sections confer: the same form `Name.[…]` is an enum in the first section and an association in the third. Comments are `;;` to end of line.

**Types section.** `X.{…}` declares a struct: portions positional, each `Name.Type`, or bare `Name` when the portion's type has the same name (`Separator`, `Extent`). `Y.[…]` declares an enum: variants bare, or `Variant.Payload` where Payload is a type name, a full type expression (`Vector<Lock>`, `Result<A F>`), an inline `{…}` or `[…]` — an inline payload declares a derived-name type. A type with one portion is a one-portion struct: `Symbol.{String}`, `Assemblies.{Vector<AssemblySummary>}`. A type declaration has no positions on its head: what a type is made of is written in its braces, nothing else. There is no alias form, no newtype form, no tuple form, no visibility, no non-exhaustive flag, no private field: every declared portion is public; a Rust-only cache or phantom is not a portion and is not declared — the Rust is restructured so the type is exactly its map. In particular Text is `Text.{…}` with its real portions and no target parameter: the would-be type of a text is chosen where `embody` is called (see the kinds section), not carried by Text. Prospective is not declared in the map; whether it is a kind on Text or only vocabulary is unruled — stop and ask if a form for it is needed.

**Kinds section.** `Kind.[ capability … ]`. A capability's yields are always in brackets, one or several: `delineate.[ Result<Delineation Fault> ]`. With inputs, the struct form: `print.{[Layout] [Text]}` — inputs then outputs, each bracketed. The separator after the capability's name is its receiver: `.` shared self, `!` mutable self, `:` no self (a constructor or predicate: `embody:{[Portion] [Result<Self Fault>]}`, `matches:{[Portion] [Boolean]}`). `Self` is the bearer. A kind named in a yield or input (`Embodied` in `Result<Embodied Fault>`) is a position bounded by that kind, filled at the call: in Rust, `fn embody<T: Embodied>(&self) -> Result<T, Fault>`. A kind may carry positions in its head: `TextEdge<Datomic>.[ embody.[ Result<Datomic Fault> ] ]`. Nothing else is written: no supertraits, no associated-type lists, no receivers as words, no defaults. A capability that has one implementation for every bearer (today's `textualize` = `portion` then `print`) is not a default in the map; it is a hand-written blanket interaction in the crate on a kind of its own, or a plain capability the crate implements per type.

**Associations section.** `Type.[ Kind Kind ]` — the kinds a type bears; the emitter turns each into a compile-time impl check: `Text.[ Delineatable Embodiable ]`.

Interface files keep their ruled shape: `Interface.{v}`, `Channel.{Name contract wire}`, imports, `{ [inputs] [outputs] [refusals] [streams] [types] }`. Refusals live in the third section, never among the outputs.

## 2. What the emitter derives, and what it must not require

From the map alone the emitter produces: `pub struct` / `pub enum` with all-public portions in map order; derived-name types for inline payloads; newtypes as single-field structs; a `pub trait` per kind with one method per capability — receiver from the separator, inputs and outputs from the brackets, kind positions as associated types or generics bounded by the kind's trait; one `const _: () = { fn _check<T: Kind>() {} … }`-style assertion per association. Everything Rust needs beyond that (`derive`s, `Box` for recursion, lifetimes, `#[non_exhaustive]`) is an emitter rule stated once in ethos-zero's code, never a word in a map. If a map cannot express something the current Rust does, the Rust changes, not the map — except where this prompt's section 1 gives no form at all; then stop and ask.

## 3. Slices

Each slice: delete first, rewrite, prove under `nix flake check` and `cargo test`, bump per the versioning skill, commit and push, log.

- **M0 Reader and emitter.** In `ethos-zero`: delete the `Schema` branch and the `TupleStruct`, `Visibility`, `Receiver`, `AssociatedType`, `Method.default`, non-exhaustive vocabulary; read `Library.{…}` files per section 1; emit per section 2. The word `Schema` no longer appears anywhere in the crate — code, tests, docs, `.ethos` fixtures. Acceptance: the section-1 example reads into a typed `File` and emits compiling Rust; every invented form above faults with an Extent.
- **M1 Protos map upstream.** Rewrite `protos.ethos` in the ruled syntax, keeping today's type and kind set except: no tuples (`ContentHash.Integer`, `Symbol.String`, Portion's variants as inline `{Extent …}` payloads so Extent sits once on Portion), no hidden fields and no phantom (Text becomes exactly its map; the target type of an embodiment is the generic of `embody`, and `Text<T = ()>` goes away), no alias. Generate the declarations with ethos-zero as a dev-dependency into a committed `src/generated/` module, with the byte-identical regeneration test the signal crates already use; delete the hand-written declarations and keep only the interactions. Delete `NON_IDEAL_AGENTS.md`. Acceptance: the 13 protos tests and the property round trips pass against the generated declarations.
- **M2 Datomic and ethos-zero maps.** Same treatment for `datomic.ethos` and `ethos-zero.ethos`; delete the two stale `signal.ethos` / `meta-signal.ethos` at the ethos-zero repo root (the real ones live in the signal crates). Acceptance: datomic's round-trip suite and ethos-zero's file-contract tests pass against generated declarations; the four signal crates still regenerate byte-identically.
- **M3 Consumers.** `chroma`, `horizon-rs`, `synchronizer`, `relative-age-display`, `claude-answers`, `chronos`: change the head to `Library.{…}` with the three-section body, remove any invented form, regenerate, bump, repin protos/datomic/ethos-zero at head. Acceptance: each `nix flake check` green; the `.datomic` data files of goldragon and CriomOS-test-cluster still embody.
- **M4 Sweep.** Across all repositories of the new stack: `grep -rn 'Schema\|Visibility\.\|Receiver\.\|Tuple\.\|Private\.\|Methods\.\|Supertraits\|Default\.Chain\|NonExhaustive'` over `*.ethos`, `src/`, `tests/`, `*.md` returns nothing. Fast-forward the `primary/repos` checkouts to the pushed heads.

## 4. Show the living

Before M1: the rewritten `protos.ethos`, in full. Before M3: one consumer map. Any form not in section 1: stop, ask.

## 5. References

- The audit that found this: `flows/db97561c/reports/overnightPortAudit.md` and the artifact "Portion Pivot Audit"; the previous prompt, superseded on syntax by this one: `flows/db97561c/reports/protosDatomicEthosZeroRealization.md`.
- Ruled forms: `Vision/ethos.md`, `Vision/datom.md`; `flows/b675f3d9/vision/kinds.md` (`[]` yields, `!` mutable self), `flows/04db2fd2/vision/kinds.md` (one separator, options mutually exclusive; Result), `flows/2b34fafa/vision/importResolution.md` (imports), `flows/5abf3be8/vision/sectionsExistToConferTraits.md`.
- Repositories at remote head: `protos` bfde3b8 (0.14.0), `datomic` b670c72 (0.7.1), `ethos-zero` b922afb (0.7.1, nexus 0.7.2), `signal-ethos-zero` 493742d, `meta-signal-ethos-zero` 19f1078, `signal-orchestrate` a597f1a, `meta-signal-orchestrate` 5cdf35a, `chroma` 1b626d9, `horizon-rs` f8c5808, `synchronizer` 7d44944, `relative-age-display` 82f0100, `claude-answers` e637388, `chronos` 43703ad. The `primary/repos` checkouts are behind these.
- Skills: realization, testing, versioning, file-editing, psyche-interraction.
