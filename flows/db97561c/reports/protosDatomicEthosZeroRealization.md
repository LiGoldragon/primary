# Realize Protos, Datomic, and Ethos-zero on the Portion pivot

A prompt for the implementing flow. Delete-and-rewrite, in place, in incremental vertical slices: Protos first, then Datomic, then Ethos-zero, ending with Orchestrate regenerated and round-tripping through the new stack.

## 0. Standing

The living psyche is present in your flow. What follows is the design flow db97561c's articulation of the current vision plus its own recommendations, which the living adopted *by instruction without reading them* ("I go with your recommendations" — a working instruction, not vision). Treat every design choice marked **(flow)** as yours to confirm with the living before you build on it; everything marked **(ruled)** is the living's own word, findable in the referenced records. Show the living each map (P0, D0, E0) before implementing its track. The existing code is not a reference: 04db2fd2 witnessed its eight anatomy oddities; the living's verdict was "the implementation must be pretty bad." Old code is at most inspiration for the map.

## 1. What the system is

### 1.1 Three forms, one substrate, two dialects

A value has three forms: **embodied** (Rust memory), **signal** (rkyv, what components speak to each other), **textual** (the edge, so LLMs and editors can understand signal). **(ruled)**

**Protos** is the concept and the universal machinery all dialects share — not a language. **Datomic** (the library; `datom` is freed for the eventual nexus) is the pure typed-data dialect: positional, no field names, the reader walks the expected type; it carries data only. **Ethos** is the schema language: it declares types and kinds and generates the Rust, which is committed. Ethos depends on Datomic (signal data intake). **(ruled)**

### 1.2 Protos — the pivot

Text comes in prospective and leaves as a value. Inbound may fault; outbound cannot. Spans are found on the way in and computed on the way out. Several passes, always inside a parsing context that *changes* rather than suspends: a met shape announces a type, that type's context takes over until its completing shape, then the parent resumes exactly where it left off. **(ruled; Intent protosParsing)**

The **Portion tree is the single pivot in both directions** **(flow, adopted)**:

    Text ──delineate──▶ Portion ──anatomy match──▶ embodied value        (may fault, Extents found)
    embodied value ──anatomy build──▶ Portion ──print──▶ Text             (cannot fault, Extents computed)

Protos owns `Text ⇄ Portion` (delineate, print). A dialect owns only `Portion ⇄ type` — its anatomies. No dialect ever touches characters; questions such as "can this string be written bare" are protos questions answered once, on the Portion plane, never by re-scanning. The printer is the only writer of characters in the whole system; the delineator is the only reader. "The parser is the parser; nothing implements its own parsing logic." **(ruled)**

**Protos types** **(ruled unless marked)**:
- `Text` — more than String: non-structural whitespace removed, so a content hash is reliable. Structural whitespace is the single space between bare siblings and anything inside an opaque portion.
- `Portion.[ Headed Enclosed Bare ]` — the universal term for a component: a field, a variant, an element. `Extent` sits once on Portion. Portion carries both its form and its anatomy; there are no separate Form and Anatomy types.
- `Headed.{ Symbol Separator Portion }` — head, separator, body; the body is another portion; heads daisy-chain (`Observed.Locks.[]`, `x.y.z.w`), possibly with different separators. `Separator.[ Period Exclamation Colon ]` — one separator per head, the options mutually exclusive.
- `Enclosed` — a non-opaque enclosed portion holds `Vector<Portion>` and records its arity (brace arity is anatomical; bracket arity is not, but is still kept for printers and editors). An opaque enclosed portion has no inner portions.
- `Bare.Symbol` — Symbol is a qualified string.
- Protos enclosures: `{ }` braced, `[ ]` bracketed, `« »` guillemeted (U+00AB/U+00BB), `< >` angled, `“ ”` curly-quoted (opaque). Parentheses are *not* protos: a dialect delimiter, content-opaque, balance-based (an unbalanced `)` is escaped).
- Pure anatomy is structural recognition of delineations, nothing more: for protos a Head is just a Head. A *type's* anatomy is the dialect's business.
- Faults carry the Extent they were found at. There is one delimiter table, in one place.

**Protos kinds** (a kind is what a Rust trait becomes; named as a qualifier; a capability is a function a kind has) **(ruled)**, written in Ethos as the living last saw them in 2ef42163 **(unruled state)**:

    Delineatable.[ delineate.[ Result<Delineation Fault> ] ]
    Embodiable.[ embody.[ Result<Embodied Fault> ] ]
    Embodied.[]
    Textualizable.[ textualize.[ Text ] ]

    Text.[ Delineatable Embodiable ]
    Lock.[ Embodied Delineatable Textualizable ]

`Text` is Embodiable; the final Rust type is Embodied and Textualizable; the two directions are never on the same type ("You dont textualize the text, and you dont realize the realized data"). `Prospective<T>` is text taken as a would-be T. The living's last open question: is `Embodied` a marker kind, or does it carry capabilities? **(flow, to confirm at P0):** on the pivot, an embodied type's anatomy is the pair `Portion → Self` (may fault) and `Self → Portion` (cannot fault); the recommended placement is `Portion → Self` under `Embodied` and `Self → Portion` under `Textualizable`, with `Delineatable` on a type meaning its delineations are intrinsic to its shape. `ShapeDefined` ("ShapeDefined is good", never retracted) survives as the kind of a type that selects among several anatomies by shape in its context — an enum choosing its variant, a position accepting several shapes — implemented as a match over the standard shapes. Confirm or let the living rename.

Structure tells the type, always context-dependently: brace arity, the delimiter after the head (`.{` struct, `.[` enum), the separator (`.` `!` `:`), and the presence or absence of a head. **(ruled)**

### 1.3 Datomic — syntax

All **(ruled)** unless marked. The reader walks the expected type; the text carries only data.

    {Q3 «north.[…] south.[…]» 42}          ;; a struct: bare braces, fields by position
    [alpha beta gamma]                      ;; a vector: one type for all components
    «north 1 south 2»                       ;; a map: guillemets, key value by position, never headed
    Observe.Locks                           ;; variant Observe carrying unit variant Locks
    Observed.Locks.[]                       ;; variant Observed carrying variant Locks carrying an empty vector
    Report.{Ops [Note.“sub note”] «kind core»}   ;; variant carrying a struct
    Tags.[alpha beta]                       ;; variant carrying a vector
    Note.“quick (aside) note”               ;; variant carrying a string, curly quotes, opaque
    Note.quick                              ;; the same when the bare form carries it
    0  42  -42                              ;; integers: bare decimal, no leading + or 0

- A Head is always a variant and always re-emits itself. A root enum starts with its variant; a root struct starts with `{`.
- A string is a string only where the type says string; there, a string that needs no quotes *must not* be quoted, and a bare string may carry symbols that are load-bearing elsewhere — the machinery is made fit for this by the right abstraction layer (protos decides bare-safety on the Portion plane). Curly quotes are the default delimiter; a curly-quoted block is opaque.
- Parentheses are reserved for **Meaning**, the structured string; postponed: `(…)` lands as plain String today, the later type marked in code.
- `< >` is accepted by delineation and kept compatible with Ethos; datom does not use it yet.
- Datom's kind is `Datomic`. `Prospective<Datom>` is Delineatable.
- No derive macros: "datom creates configuration options by its very shape" — a type's anatomy is declared in one place, by one pattern, hand-written until Ethos-zero generates it.

**Unruled atoms — put these to the living before D1, with these proposed defaults** **(flow)**: booleans as the bare unit variants `True` / `False`; floats bare decimal with a mandatory point (`0.5`, `-1.0`), no exponent; absent values as Rust's Option recycled (`None`, `Some.value`) since "rust syntax is the target"; comments `;;` to end of line, non-structural, dropped by normalization and not preserved on round trip; curly quotes balance-based like parentheses (they are an asymmetric pair), so nested balanced quotes are content and there are no escape sequences; canonical layout flat, one space between siblings, none inside enclosures — multi-line layout is a later ruling the printer must be able to take as a parameter.

### 1.4 Ethos-zero — syntax and generation

The **File** is the unit; a **Source** is what Rust calls a crate; no namespace inside a file. A file is: a header object, the channel, imports, the body — the body ethos-type-specific. **(ruled)** The interface file today:

    Interface.{0 2 0}
    Channel.{Orchestrate 1 5}
    []
    {
      [Observe.Observation Lock.LockSpecification Release.LockName]     ;; inputs — imperative, Observe universal
      [Observed.Observed Locked.Lock Released.LockName]                 ;; outputs — always an enum
      [Refused.Reason]                                                  ;; refusals
      []                                                                ;; streams
      [                                                                 ;; types
        Observation.[Locks]
        Observed.[Locks.Vector<Lock>]                                   ;; full type expressions in payloads (01a04339's blocker)
        Lock.{Name Flow Paths.Vector<Path> Description}
      ]
    }

(Shapes illustrative; the real Orchestrate contract is flows/01a03eda/reports/orchestrateChangesProposal.md, approved, and repos/signal-orchestrate/ethos/signal.ethos.)

- Sections confer kinds: an item is an input by standing in the input section; the word request is redundant. Variants are imperative; `Observe` is the universal root, sub-operations as a nested enum. A stream is a fourth section; its initiation and termination live in the input. **(ruled)**
- Types: `X.{…}` struct — always the same fields in the same order, any field type; `Y.[…]` enum — variable length, all components one type or kind; `Name.Type` a typed portion; an inline struct or enum inside a variant is shorthand for a derived-name type (no anonymous structs, no vectors of types); `Vector<T>`, `Result<A F>`; angle brackets hold kinds and positions — `Processable<[Clonable Sendable] Serializable>`. Rust syntax is the target: recycle it (`Result`, `Self`, `From`/`TryFrom` — no Create). No tuples in designed code. **(ruled)**
- Kinds live in a **separate block** from types **(ruled)**; capability forms: `head.[Yield …]` — yields always in brackets, even one; `head![…]` mutable self; `head.{[inputs] [outputs]}` the struct form, for complex kinds; a fallible yield is `Result<A F>`. Type–kind association `Type.[ Kind Kind ]` **(unruled proposal, 2ef42163)**. Ethos checks at build time that a type carries the kinds it claims — the living approved this checking mechanism. **(ruled)**
- Imports: `source:Object`, `source:[Object Thing]`, `source:file.[Object Thing]`, `source:dir/file.[Object]`; the source name resolves through a manifest written in datom; unresolvable is an error, no fallback; a bare path is local; there is no Import type, only an import reference. **(ruled)**
- Transformers (`Name:Transformer.{…}` / `.[…]`) belong to Nomos: out of scope. Parentheses are freed in Ethos.
- Generation: Ethos in, Rust out, emitted structurally (syn/quote), never by string concatenation; the generated Rust is **committed** in the consumer and `build.rs` generation goes away. Scope in this pass: interface files and the kinds block — kind declarations become Rust traits, type–kind associations become impl checks. Nexus and sema Ethos come later, in the component's main repository.
- Ethos-zero **is a nexus from the start** (privileged and ordinary sockets, one datom-converting CLI per socket as separate crates in the multi-crate repo, per the nexus skill). Its own signal interface is written in Ethos; generation zero of that signal crate is hand-written and committed; self-regeneration is the acceptance test. **(flow, adopted)**

### 1.5 What is not built

No touching `dotos`, `core-ethos`, `ethos-engine`, `signal-ethos`, `spirit-ethos`, tree-sitter grammars, `curriculum-deploy`, or any `signal-*`/`meta-signal-*` repository other than Orchestrate's two; they stay frozen on their pinned revisions and migrate in later flows. No compatibility shims, no parallel paths, no legacy modules. No second parser of anything — `.ethos` is read through protos like everything else. No per-repo architecture-guard binaries (the living: a universal tool or nothing). No derive macros. No Meaning type. No Nomos/Logos. No new bead tracking ("no more beads").

## 2. The slices

Each slice: **delete first** the code it replaces (the whole repo at the track's first slice), author or revise the map, write the Rust that mirrors the map, prove it, bump per the versioning skill, commit and push, log. A slice is done when its acceptance holds under `nix flake check` and `cargo test`. Show the living the map at P0, D0, E0 and any unruled atom the moment it is met.

### Protos track — `repos/protos` (git@github.com:LiGoldragon/protos.git), in place

- **P0 Map.** Delete `src/`, `tests/`, `checks/`. Author `protos.ethos` at the repo root: the types of 1.2 (Text, Symbol, Extent, Separator, Enclosure, Portion, Headed, Enclosed, Bare, Delineation, Fault) and the kinds (Delineatable, Embodiable, Embodied, Textualizable, ShapeDefined, Prospective). Show it to the living; take rulings on the (flow) items. Acceptance: the map is ruled on.
- **P1 Delineate.** Text → Portion tree with Extents: all five enclosures, opaque curly quotes and balance-based parentheses, bare symbols, the three separators, daisy-chained heads, arity recorded, faults with Extents. Acceptance: property tests over generated portion trees printed by a throwaway printer; the delimiter table exists once.
- **P2 Print.** Portion → Text with computed Extents, canonical flat layout; layout is a parameter of the printer, flat is the only value now. Acceptance: `delineate ∘ print` is the identity on every Portion tree; `print ∘ delineate` is the identity on normalized Text.
- **P3 Text and kinds.** `Text` normalization and content hash; `Prospective<T>`; the kinds as Rust traits exactly mirroring `protos.ethos`; the anatomy plane — the small set of protos-level questions a dialect asks of a Portion (is bare-safe, arity, head symbol, enclosure, separator) so no dialect re-scans. Acceptance: a toy dialect type embodies and textualizes through the pivot with no character handling of its own.

### Datomic track — `repos/datom` renamed `repos/datomic` (rename remote and directory per the repository-lifecycle skill), in place

- **D0 Map.** Delete the source. Author `datomic.ethos`: the `Datomic` kind; the anatomies of String/Text, Integer, the unruled scalars (after the living rules), Vector, Map, Option, struct, enum, unit and headed-unit variants; the Fault taxonomy with Extents. Show the living; rule the unruled atoms of 1.3.
- **D1 Scalars and containers.** Bare/curly strings with bare-safety asked of protos, integers, vectors, guillemet maps — embody and textualize through Portion only. Acceptance: round trips and faults on every scalar and container, including the unruled atoms as ruled.
- **D2 Structs and enums.** Positional structs, variants with unit / headed-unit / struct / vector / string payloads, chains, the root rule. Acceptance: `Observe.Locks`, `Observed.Locks.[]`, and a lock record round-trip byte-identical.
- **D3 Anatomy declaration.** The one pattern by which a Rust type declares its anatomy (hand-written until E2 generates it), sized so E2's generator can emit it verbatim. Acceptance: Orchestrate's real types from 01a03eda's contract, hand-declared, round-trip; `< >` and `( )` accepted, `( )` landing as String.
- **D4 Edge.** The public surface a nexus CLI needs: text in → typed value or fault with Extent; typed value → text. Acceptance: the toy of P3 and Orchestrate's types pass through the same two entry points.

### Ethos-zero track — `repos/ethos-monolith` renamed `repos/ethos-zero`, in place; new `signal-ethos-zero` and `meta-signal-ethos-zero` repositories (three repositories per component)

- **E0 Map.** Delete the source. Author ethos-zero's own `signal.ethos` and `meta-signal.ethos` (inputs such as Generate and Observe; outputs; refusals) and an `ethos-zero.ethos` of its internal main types (File, Header, Channel, ImportReference, Section, TypeDeclaration, KindDeclaration, Association, Assembly). Show the living.
- **E1 Read.** `.ethos` File → embodied File as an Ethos dialect over protos and datomic: header, channel, imports with manifest resolution, the five body sections, type expressions including `< >` and full type expressions in payloads, the kinds block. Acceptance: Orchestrate's `signal.ethos` and ethos-zero's own files read into typed Files; every malformed fixture faults with an Extent.
- **E2 Emit.** File → Rust with syn/quote: types (struct, enum, derived-name types, Vector, Result), section kinds (Input/Output/Refusal/Stream), datom roots and anatomy declarations in D3's pattern, kind declarations → traits, associations → impl checks. Acceptance: the emitted Rust for protos.ethos and datomic.ethos compiles and is identical (after rustfmt) to the hand-written P3/D3 code — or the hand-written code is corrected to the map.
- **E3 Nexus and bootstrap.** Ethos-zero as a nexus with its two sockets and two datom-converting CLIs; generation zero of `signal-ethos-zero` / `meta-signal-ethos-zero` hand-written and committed. Acceptance: ethos-zero regenerates both of its own signal crates identically (self-hosting); a text request through the CLI round-trips as datomic.
- **E4 Terminus.** Regenerate `signal-orchestrate` and `meta-signal-orchestrate` from their `.ethos` with ethos-zero, commit the generated Rust, remove their `build.rs` generation; repin protos, datomic, ethos-zero in `orchestrate`, `signal-orchestrate`, `meta-signal-orchestrate` only; the orchestrate CLI round-trips `Observe.Locks` ↔ `Observed.Locks.[]` and a lock/release; deploy per the breaking-upgrades skill. Acceptance: witnessed live round trip on the deployed Orchestrate.

## 3. How to work

Skills: realization, testing, versioning, file-editing, repository-lifecycle, nexus, breaking-upgrades, psyche-interraction. Build and prove with `nix flake check` (rust-build flake) and `cargo test`; cross-repo dependencies are git pins by commit. The maps are the spec: when the Rust and the map disagree, one of them is wrong and the living decides which. Keep the tree clean at the end of every slice. Log rulings in your flow's `vision/` as they land; log scope changes in `log.md`. Do not edit `Vision/`: the distillation of this vision is owed by the design flow, not by you; where `Vision/protos.md` says Realize, the living has since ruled Embody.

## 4. References

- Design flow: `flows/db97561c/log.md` and this file (`flows/db97561c/reports/protosDatomicEthosZeroRealization.md`).
- Fullest articulation of kinds, portion, anatomy (unruled): `flows/2ef42163/reports/distillProposalRound5.md`; the kind-syntax state is the last model response of flow 2ef42163.
- The eight oddities not to repeat: `flows/04db2fd2/witnesses/datomTextualizeRealizeAnatomy.md`, `flows/04db2fd2/reports/textualizeRealizeAnatomyReview.md`; verbatim psyche on protos and datom: `flows/04db2fd2/reports/protosDatomPsyche.md`.
- Orchestrate contract (approved): `flows/01a03eda/reports/orchestrateChangesProposal.md`; `Observed.Locks.[]` and the payload blocker: `flows/01a04339/vision/datom.md`.
- The handwritten capability page and structural-parsing rulings: `flows/b675f3d9/vision/structuralParsing.md`, `flows/b675f3d9/vision/kinds.md`.
- Intent: `psyche-raw/Intent/protosParsing.md`, `psyche-raw/Intent/mandatoryTraits.md`. Landed Vision (partly superseded as noted): `Vision/protos.md`, `Vision/datom.md`, `Vision/ethos.md`, `Vision/ethosMonolith.md`.
- Repositories: `repos/protos` (0.8.0), `repos/datom` (0.5.0) → `datomic`, `repos/ethos-monolith` (0.5.5) → `ethos-zero`, `repos/signal-orchestrate/ethos/signal.ethos`, `repos/meta-signal-orchestrate/ethos/signal.ethos`, `repos/orchestrate` (Nexus 0.25).
- Beads (all in `primary`; the superseded 2026-08-04 protos-engine epic — read for history only): primary-xqb, primary-xqb.8, primary-xqb.8.3, primary-xqb.8.4, primary-xqb.8.9, primary-xqb.8.10, primary-xqb.8.12.

## Sources

- Subflow gatherings of this flow (transcript): Protos records (~100), Datom records (78), Ethos records (71), cross-cutting syntax records; remembering of 2ef42163, 04db2fd2, acbb6006, ac1e9ec8, 01a04339, 01a03eda, b675f3d9; implementation survey; beads and `.ethos` path lookup.
- flows/2ef42163/reports/distillProposalRound5.md (read directly).
- Vision/protos.md, Vision/datom.md, Vision/ethos.md, Vision/ethosMonolith.md (read directly).
- The living's instruction in this flow: "I go with your recommendations." and the correction that it carries no vision (vision/psycheLogging.md).
