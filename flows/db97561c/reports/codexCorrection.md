# Correct the port: the Prospective chain, the Library map syntax, the universal Nexus library, generation through the daemon

A prompt for the implementing flow. Supersedes `flows/db97561c/reports/mapSyntaxCorrection.md`. Read `flows/db97561c/reports/overnightPortAudit.md` first for what is wrong and where.

## 0. Standing

Rule of conduct: **when you meet a form or a name this prompt does not define, stop and ask the living.** Do not settle syntax, names, or ontology by judgment, whatever you are told about keeping going; report what is missing and wait. Every form below is either the living's ruling or a default the design flow chose; the defaults are listed here so the living can overrule them before you start — treat them as ruled unless the living says otherwise.

Defaults chosen by the design flow, not ruled by the living:
- The universal library's repository and crate are named `nexus`; Nexus Core stays the name of each component's own engine that the library hosts.
- `Prospective` is one kind with one capability, `embody`, at every stage.
- `Generate` names a source and a relative path resolved through the daemon's `sources.datom` manifest (the current shape), not a bare path.
- A types-and-kinds file opens with `Library.{major minor patch}`.
- In the kinds section the separator after a capability name is its receiver: `.` shared self, `!` mutable self, `:` no self.
- A map never carries a default implementation.
- The generic frame codec (today's four identical `codec.rs`) lives in the universal signal repository, named `signal`, new.

First act, before any edit: confirm that Codex flow 01a04a30 has ended (its session was alive on this tree holding Orchestrate locks 135 and 136 for the CriomOS-home Chroma repin). If it has not, stop and tell the living. Then fast-forward every checkout under `primary/repos` to its remote head; `horizon-rs` has no local checkout and gets one.

## 1. The direction chain — ruled

Positions in a kind's head hold kinds, never types. Text is never prospective toward a type; it is prospective toward Protos, and a Protos value toward a dialect.

    Text.[ Prospective<Protos> ]
    Protos.[ Prospective<Datomic> Textualizable ]
    Lock.[ Datomic ]

- `Protos` is a type: the portions and their protosic anatomy — what the port called `Delineation`. It is what protos produces from text and what protos prints back to text. The name `Delineation` goes; `Portion` stays as the name of one portion.
- `Prospective<K>` is a kind: the bearer taken as a would-be K. Its capability yields a value of the position's kind, the concrete type chosen at the call:

      Prospective<Protos>.[ embody.[ Result<Protos Fault> ] ]
      Prospective<Datomic>.[ embody.[ Result<Datomic Fault> ] ]

  In Rust: `trait Prospective<K> { fn embody<T: K>(&self) -> Result<T, Fault>; }` — `Text: Prospective<Protos>` (the delineation), `Protos: Prospective<Datomic>` (the typed match). `Prospective<Lock>` on Text is wrong: it skips the Protos stage.
- `Embodiable`, `Delineatable`, `TextEdge<T>`, `Text<T>` and its phantom go. `Embodied` stays as the kind of a final type (`Portion → Self`), `Textualizable` as `Self → Portion`, `Datomic` as the dialect kind a final type bears; whether `Datomic` is written as `Embodied` plus `Textualizable` or stays one kind is not yet ruled — keep today's `Datomic` and do not invent a merge.
- Never both directions on one type.

## 2. The Library file — exactly

    Library.{0 1 0}
    []
    {
      [
        Extent.{Start.Integer End.Integer}
        Separator.[Period Exclamation Colon]
        Symbol.{String}
        Portion.[Headed.{Extent Headed} Enclosed.{Extent Enclosed} Bare.{Extent Symbol}]
        Headed.{Head.Symbol Separator Body.Portion}
        Protos.{Portions.Vector<Portion>}
        Fault.{Extent Problem.FaultProblem}
        Layout.[Flat]
      ]
      [
        Prospective<Protos>.[ embody.[ Result<Protos Fault> ] ]
        Prospective<Datomic>.[ embody.[ Result<Datomic Fault> ] ]
        Embodied.[ embody:{[Portion] [Result<Self Fault>]} ]
        Textualizable.[ portion.[ Portion ] ]
        Printing.[ print.{[Layout] [Text]} ]
      ]
      [
        Text.[ Prospective<Protos> ]
        Protos.[ Prospective<Datomic> Printing ]
      ]
    }

Header `Library.{major minor patch}`; imports second (`[]`, or `source:Object`, `source:[A B]`, `source:file.[A B]`); body one braced object of three bracketed sections — types, kinds, associations. Sections confer: `Name.[…]` is an enum in the first section and an association in the third. Comments `;;` to end of line.

**Types.** `X.{…}` struct: portions positional, `Name.Type`, or bare `Name` when the portion's type has the same name. `Y.[…]` enum: variants bare or `Variant.Payload`; a payload is a type name, a full type expression (`Vector<Lock>`, `Result<A F>`), or an inline `{…}` / `[…]` declaring a derived-name type. A one-portion type is a one-portion struct: `Symbol.{String}`. A type's head carries no positions; what a type is made of is in its braces. No alias, no newtype, no tuple, no visibility, no non-exhaustive flag, no private field, no phantom: every portion is public, and the Rust is restructured so the type is exactly its map.

**Kinds.** `Kind.[ capability … ]`; a kind's positions in its head: `Prospective<Protos>`. Yields always bracketed, one or several: `embody.[ Result<Protos Fault> ]`. With inputs, the struct form: `print.{[Layout] [Text]}`. Receiver from the separator: `.` shared, `!` mutable, `:` none. `Self` is the bearer. A kind named in a yield or input is a position filled at the call (`fn embody<T: Datomic>`). Nothing else is written — no supertraits, associated-type lists, receiver words, defaults. A capability with one implementation for every bearer is a hand-written blanket interaction in the crate.

**Associations.** `Type.[ Kind Kind ]` → one compile-time impl check each.

Interface files keep their ruled shape: `Interface.{v}`, `Channel.{Name contract wire}`, imports, `{ [inputs] [outputs] [refusals] [streams] [types] }`; refusals in the third section, never among the outputs.

**Emitter.** From the map alone: `pub struct` / `pub enum` with all-public portions in map order; derived-name types for inline payloads; a `pub trait` per kind, one method per capability, receiver and signature from the forms above, kind positions as generics bounded by the kind's trait; one assertion per association. `derive`s, `Box` for recursion, lifetimes are emitter rules stated once in ethos-zero, never words in a map. If a map cannot say what the Rust does, the Rust changes.

The word `Schema` appears nowhere in the new stack — code, tests, docs, maps, commit messages.

## 3. The Nexus shape — ruled

- **`nexus`** is the universal Nexus library every nexus is built on: ordinary and meta sockets, the request loop, subscription fan-out (state on open, then each change; no polling), the Sema storage actor, the standard metadata tree with the configuration row and the first-configuration record (Configure reachable on the ordinary socket until it is set; reversed only on meta), default paths under `$XDG_RUNTIME_DIR/<component>-nexus/` and `$XDG_STATE_HOME/<component>-nexus/`, socket preparation with a liveness probe, and the datomic-converting CLI shell. Driven by Kameo actors (`LiGoldragon/kameo`). It is new: `triad-runtime` and `signal-frame` are frozen and are a checklist at most.
- **`signal`** is the universal signal repository: the generic length-prefixed frame codec over any generated `Frame`, the router enum, the handshake payload. The four hand-copied `codec.rs` files go.
- **`ethos-zero`** is the daemon and nothing else: `ethos-zero-nexus` on `nexus`, its reader and emitter inside it as its Nexus Core, `ethos-zero` and `ethos-zero-meta` CLIs as sibling crates, `signal-ethos-zero` and `meta-signal-ethos-zero` beside it. No consumer depends on ethos-zero as a library; the `ethos-zero` producer crate is no longer published for consumption.
- **Generation is a request to the running daemon.** `Generate.{Source RelativePath}` resolves the source through `sources.datom`, reads the `.ethos` through protos, emits — interface files to wire contracts, Library files to their declarations — writes the Rust beside the source, records the assembly. The committed Rust in every repository is produced by that act. The dev-dependency regeneration tests go; freshness is deliberately open (`Vision/ethos.md`). Generation zero of ethos-zero's own two contracts stays hand-written; the daemon regenerates them and the result is committed.
- Orchestrate is rebuilt on `nexus` and `signal` and redeployed; it is the proof that the library is universal.

## 4. Slices

Each slice: delete first, rewrite, prove under `nix flake check` and `cargo test`, bump per the versioning skill, commit and push, log. Show the living the rewritten `protos.ethos` before K1 and the `nexus` map before N1; stop on any undefined form.

- **K0 Reader and emitter.** In ethos-zero: delete the `Schema` branch and every invented form (`Struct`/`Enum`/`Tuple`/`Alias` markers, `Visibility`, `Private`/`Public` fields, `Methods`, `Receiver`, `Associated`, `Supertraits`, `Default`, `NonExhaustive`, `TupleStruct`); read and emit `Library` files per §2. Acceptance: the §2 example reads and emits compiling Rust; each invented form faults with an Extent.
- **K1 Protos.** Rewrite `protos.ethos` per §1–2: `Protos` replaces `Delineation`; `Text` has no parameter; kinds are `Prospective<Protos>`, `Embodied`, `Textualizable`, `Printing` and the anatomy-plane kinds that survive as real kinds (drop `EnclosedAnatomy`, `DelineatedText` — accessors, not kinds); no tuples (`Symbol.{String}`, `ContentHash.{Integer}`, Portion variants with inline `{Extent …}` payloads); no hidden fields. Declarations are generated from the map by the daemon and committed under `src/generated/`; interactions hand-written. Delete `NON_IDEAL_AGENTS.md`. Acceptance: the property round trips and all protos tests pass against generated declarations.
- **K2 Datomic.** `datomic.ethos` per §1–2: `Protos.[ Prospective<Datomic> ]` implemented here; `TextEdge`, `PortionViewing`, `DecimalViewing`, `PortionBuilding` go (accessors); the anatomy pattern per type unchanged otherwise. The four per-repo Nix grep guards go. Acceptance: round-trip suite green against generated declarations.
- **N1 `nexus` and `signal`.** New repositories per §3, each with its own `Library` map and `Interface` maps where it has sockets; extracted from the two existing daemons (`orchestrate/src/transport.rs`, `store.rs`, `defaults.rs`; `ethos-zero/nexus/src/lib.rs`; the four `codec.rs`). Acceptance: a test nexus built on the library binds two sockets, answers Configure on the ordinary socket before first configuration and refuses it after, serves a subscription, survives restart with its configuration.
- **N2 Ethos-zero as daemon.** Rebuild on `nexus` and `signal`; `Generate` emits both file kinds; CLIs on the library's shell; regenerate its own two contracts through itself and commit. Acceptance: `ethos-zero 'Generate.{…}'` against a running daemon regenerates protos', datomic's, and its own declarations byte-identically to what is committed.
- **N3 Orchestrate.** Rebuild on `nexus` and `signal`; regenerate `signal-orchestrate` / `meta-signal-orchestrate` through the daemon; deploy per the breaking-upgrades skill. Acceptance: live `Observe.Locks` round trip on the deployed Orchestrate; a subscription to Locks receives a Lock event.
- **C1 Consumers.** `chroma`, `horizon-rs`, `synchronizer`, `relative-age-display`, `claude-answers`, `chronos`: `Library.{…}` head and §2 forms; drop the ethos-zero dev-dependency and its regeneration test; regenerate through the daemon; commit; bump; repin protos/datomic at head. `goldragon` and `CriomOS-test-cluster` data files re-embody. CriomOS-home repins Chroma at its current head. Acceptance: each `nix flake check` green.
- **S1 Sweep.** Across the new stack: `grep -rn 'Schema\|Visibility\.\|Receiver\.\|Tuple\.\|Private\.\|Methods\.\|Supertraits\|Default\.Chain\|NonExhaustive\|Delineation\|TextEdge\|Embodiable\|Delineatable'` over `*.ethos`, `src/`, `tests/`, `*.md` returns nothing except `Vision/` and `flows/`.

## 5. References

- Audit and its evidence: `flows/db97561c/reports/overnightPortAudit.md`; artifact "Portion Pivot Audit". Rulings of the correction: `flows/db97561c/vision/prospective.md`, `flows/db97561c/vision/nexus.md`. The Nexus vision: `Vision/nexus.md`; the nexus skill.
- Ruled forms: `Vision/ethos.md`, `Vision/datom.md`; `flows/b675f3d9/vision/kinds.md`, `flows/04db2fd2/vision/kinds.md`, `flows/2b34fafa/vision/importResolution.md`, `flows/5abf3be8/vision/sectionsExistToConferTraits.md`.
- Duplication to extract for N1: this flow's transcript, subflow "Size the universal Nexus library" (file:line map of the shared machinery).
- Repositories at remote head: `protos` bfde3b8, `datomic` b670c72, `ethos-zero` b922afb (nexus 0.7.2), `signal-ethos-zero` 493742d, `meta-signal-ethos-zero` 19f1078, `signal-orchestrate` a597f1a, `meta-signal-orchestrate` 5cdf35a, `orchestrate` dadd537 (0.26, deployed), `chroma` 1b626d9, `horizon-rs` f8c5808, `synchronizer` 7d44944, `relative-age-display` 82f0100, `claude-answers` e637388, `chronos` 43703ad, `CriomOS-home` 0530bcd, `CriomOS` 93fdd1d.
- Skills: realization, nexus, testing, versioning, file-editing, repository-lifecycle, breaking-upgrades, psyche-interraction.
