# Logos + Nomos — syntax mockup v1 (1-to-1 vision, strawman for markup)

Supersedes `syntax-mockup-v0.md`, which assumed a thin TrueLogos. The psyche ruled
that reading "totally missed my vision, by a long shot." This v1 draws Logos as
**1-to-1 with Rust** ("wordy as fuck"): every Rust token is positionally homed in
logos, **nothing materializes at projection**, and **logos→Rust is transcription**.
Empty slots are avoided by **proliferating specialized structure types**, not by
optional/general types. Full ruling text: `design-v0.md` section 1.1.

Discipline unchanged: every choice is **[licensed by ruling]** (cited) or
**[proposal — psyche to mark up]**. Written 2026-07-11 (session `schema-codex`, lane
`logos-mockup-v1`). Oracle: `repos/signal-spirit/src/schema/signal.rs` and
`repos/schema-rust/tests/fixtures/collections_generated.rs`. Samples (raw, parser-
checked against nota 0.7.0 `f8de7a51`) live in `reports/logos/samples/v1-*`.

## 0. Open choices — decide these first

**OPEN CHOICE 1 (carried, unresolved): dotted-prefix `Head.(…)` vs headed-delimiter
`(Head …)`.** [licensed by ruling — dotted-prefix invariant] for the primary form,
but the raw nota layer treats the dot as ordinary atom text (section 7): `Head.(…)`
splits into an atom `"Head."` plus a separate block, never bound. Headed-delimiter
`(Head …)` parses as one clean tree and matches nota's landed structural dispatch.
Samples are given in dotted-prefix primary form with a headed comparison retained
(`v1-wire-headed.logos`). Still the psyche's call: keep dotted + pair in the logos
layer, teach nota a dot rule, or adopt headed.

**OPEN CHOICE 2 (new, the centerpiece of this iteration): maximally-slotted vs
maximally-specialized.** Both keep everything represented; they differ in WHERE the
constant wire attribute+derive combo lives. See section 2 — drawn both ways, trade-off
stated, not picked.

**Bodies-are-positional clarification** [licensed by ruling — Correction 2]: inside a
structure body, a head appears only to (a) name a nested structure TYPE value
(`Vector.(Domain)`) or (b) select a SUM VARIANT (`MatchArm.(…)`, `UnitVariant.(…)`) —
never to LABEL a positionally-fixed product slot. Product bodies are bare. This is the
line between legitimate variant-tagging and the forbidden named binding.

## 1. Worked example 1 — DatabaseMarker + CommitSequence, drawn 1-to-1

Pipeline `schema (brief) → Nomos expansion → logos (wordy) → Rust (transcription)`.

**Stage 1 — schema source** (`signal.schema`, real, the brief view):

```
CommitSequence Integer
DatabaseMarker { CommitSequence StateDigest }
```

**Stage 3 — actual generated Rust** (the oracle, verbatim; shown before stage 2 so the
1-to-1 mapping is checkable):

```rust
#[rustfmt::skip]
#[cfg_attr(feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct CommitSequence(Integer);

#[rustfmt::skip]
#[cfg_attr(feature = "nota-text",
    derive(nota::NotaDecode, nota::NotaDecodeTraced, nota::NotaEncode))]
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub struct DatabaseMarker {
    pub commit_sequence: CommitSequence,
    pub state_digest: StateDigest,
}
```

**Stage 2a — TrueLogos, MAXIMALLY-SLOTTED** (`v1-wire-slotted.logos`). The structure
type `PublicSimpleTupleStruct` fixes the slot layout
`( rustfmt-attr gated-derives plain-derives Name FieldType )`; the body is bare
positional:

```
PublicSimpleTupleStruct.(
  RustfmtSkip
  ( nota-text NotaDecode NotaDecodeTraced NotaEncode )
  ( Archive Serialize Deserialize Clone Debug PartialEq Eq )
  CommitSequence
  Integer
)

PublicSimpleNamedStruct.(
  RustfmtSkip
  ( nota-text NotaDecode NotaDecodeTraced NotaEncode )
  ( Archive Serialize Deserialize Clone Debug PartialEq Eq )
  DatabaseMarker
  (
    ( commit_sequence CommitSequence )
    ( state_digest StateDigest )
  )
)
```

Every stage-3 token is homed: `rustfmt::skip` -> `RustfmtSkip`; the `cfg_attr`
nota-text gate -> the gated derive list (slot 2, gate name `nota-text` first, then the
three derives); the plain derive block -> slot 3; `pub` + `struct` + named/tuple shape
-> the structure type itself; `DatabaseMarker` -> the name slot; the two fields ->
bare `( fieldname FieldType )` pairs, field names stored explicitly
[licensed by ruling — Choice 3]. Derive leaf names are shown; the crate path
(`rkyv::`, `nota::`) lives in each derive symbol's own logos definition and is
transcribed at projection [proposal].

**Stage 2b — TrueLogos, MAXIMALLY-SPECIALIZED** (`v1-wire-specialized.logos`). The
type `WireTupleStruct` / `WireNamedStruct` intrinsically carries the constant combo
(rustfmt::skip + gated nota derives + rkyv/std derives + `pub`); instances spend zero
slots on it:

```
WireTupleStruct.( CommitSequence Integer )

WireNamedStruct.(
  DatabaseMarker
  ( ( commit_sequence CommitSequence ) ( state_digest StateDigest ) )
)
```

Still 1-to-1: the derives are represented in logos (in the `WireStructureFamily`
definition, section 6), just factored out of the instance. Projection transcribes
type-fixed + instance parts.

## 2. The slot-vs-specialize spectrum (OPEN CHOICE 2) — trade-off, not a pick

The same `CommitSequence` above is 6 body lines slotted (2a) versus one line
specialized (2b). The trade-off, stated in two sentences and left for the psyche:

**Maximally-slotted** keeps few structure types but repeats the constant wire
attribute+derive combo as explicit slots on every one of the hundreds of wire
declarations (uniform and maximally wordy, but the same ~10 derive tokens recur
everywhere). **Maximally-specialized** folds that constant combo into the structure
type's definition so instances carry only their varying parts (far terser instances,
the derive combo represented once per family), at the cost of one distinct structure
type per attribute/derive/visibility combination the corpus actually uses.

Note both honor the 1-to-1 ruling — neither materializes anything at projection; they
differ only in whether the constant combo is transcribed per-instance or per-type. A
middle point exists (specialize the always-constant parts, slot the genuinely varying
ones); the psyche should mark the balance.

## 3. Worked example 2 — a generic (Vector) 1-to-1

**Stage 1 — schema** (`signal.schema`): `Domains (Vector Domain)`

**Stage 3 — Rust oracle** (verbatim): `pub struct Domains(Vec<Domain>);` with the same
two derive groups + `#[rustfmt::skip]`.

**Stage 2 — TrueLogos** (specialized form shown; `Vector.(Domain)` is a generic
application whose macro has a definition [licensed by ruling — Choice 5: vector = a
generic with a definition; array would be a builtin]):

```
WireTupleStruct.( Domains Vector.(Domain) )
```

The tuple field type slot holds the nested generic-application value `Vector.(Domain)`
— a legitimate typed sub-value, not a label. `Vector` lowers to `Vec<…>` per the Nomos
`GenericMacro` (section 6).

## 4. Starter vocabulary — mined from the oracle, wide and evidence-bound

Headline: **~19 top-level specialized structure types (13 wire-contract, 6
daemon-runtime)**, plus supporting positional sub-node types, plus — for the runtime
tier only — a Rust expression/pattern/statement grammar (section 5). Node types are
cheap [licensed by ruling — wide-flat inversion]; each below is justified by a real
occurrence. [evidence] for occurrences; the type NAMES are [proposal].

Wire-contract shapes:
1. **ScalarAlias** — `pub type Integer = u64;` (`signal.rs:4-10`).
2. **WireTupleStruct** — `pub struct X(T);` newtype (`CommitSequence`, `signal.rs:634`;
   hundreds per module).
3. **WireNamedStruct** — `pub struct X { pub f: T, … }` (`DatabaseMarker`,
   `signal.rs:730`).
4. **WireUnitEnum** — all-unit-variant enum (`ObserverFilter`, survey §1).
5. **WireTupleVariantEnum** — mixed payload/unit variants, 20+ (`Input`/`Output`,
   `signal.rs:2109`).
6. **PlainErrorEnum** — struct-shaped error enum, named-field variants, the SMALLER
   derive set (`SignalFrameError`, `collections_generated.rs:445`).
7. **DisplayImpl** — match-bearing `impl Display` (`collections_generated.rs:454`).
8. **ErrorMarkerImpl** — `impl Error for X {}` (`collections_generated.rs:477`).
9. **FromImpl** — `impl From<Payload> for Variant` (138× in `spirit_nexus_generated`).
10. **ConstructorFactory** — per-variant constructor method (`Output::marker_reported`).
11. **Reexport** — `pub use crate::path::X as X;` (`signal.rs:1-70`, 43 lines).
12. **GenericStruct** — `pub struct Signal<Root>` (type param, no lifetime; survey §1).
13. **GenericEnum** — `pub enum Plane<SignalRoot, NexusRoot, SemaRoot>` (survey §1).

Daemon-runtime shapes:
14. **TraitDef** — trait with supertrait bounds + associated types
    (`pub trait ComponentDaemon: Sized + 'static`, `daemon.rs`).
15. **GenericsBoundedStruct** — `pub struct EngineActor<Daemon: ComponentDaemon> {
    engine: Daemon::Engine }` (bounded param, associated-type field; `daemon.rs:531`).
16. **ActorImpl** — `impl<Daemon: …> Actor for EngineActor<Daemon>` with `type Args`
    and two async handler bodies (`daemon.rs:533`).
17. **MessageImpl** — `impl<…> Message<WorkingInput> for EngineActor<…>` (`daemon.rs`).
18. **LifetimeBoundedTraitImpl** — `impl<'engine, Engine> … where Engine: NexusEngine`
    with associated types and multi-statement async fns (`runner_generated.rs:1843`).
19. **DocComment** — `/// …`, confined to the daemon-runtime target (`daemon.rs`).

Supporting positional sub-node types (each bare-positional): `Field ( name Type )`,
variant kinds (`UnitVariant`, `TupleVariant`, `NamedFieldVariant`), `GenericParam`,
`BoundedGenericParam`, `LifetimeParam`, `WhereClause`, `AssociatedType`, `Visibility`,
derive-group and gated-derive-group, and the builtins `Integer`-style aliases plus raw
primitives `Usize`/`U64`/`StaticStr`.

## 5. Stress test — the daemon-runtime shape (where it scales or breaks)

Example 3 is the emitted match-bearing `Display` impl for `SignalFrameError`
(`collections_generated.rs:445-478`, verbatim oracle). Drawn 1-to-1 in
`v1-runtime-stress.logos`; the enum and one representative pair of arms:

```
PlainErrorEnum.(
  SignalFrameError
  (
    UnitVariant.( ArchiveEncode )
    NamedFieldVariant.( FrameTooShort ( ( found Usize ) ) )
    NamedFieldVariant.( UnknownHeader ( ( root_enum StaticStr ) ( header U64 ) ) )
  )
)

DisplayImpl.(
  SignalFrameError
  Method.(
    fmt
    ( SelfRef ( formatter MutRef.(Formatter ElidedLifetime) ) )
    FmtResult
    MatchSelf.(
      MatchArm.( VariantPattern.(ArchiveEncode)
                 MethodCall.( formatter write_str ( [|failed to encode rkyv archive|] ) ) )
      MatchArm.( NamedFieldPattern.( FrameTooShort ( found ) )
                 WriteMacro.( formatter [|signal frame too short: {found} bytes|] ( found ) ) )
    )
  )
)
```

**What it forces, named honestly:** the data-shape tier (section 4, wire) is a dozen
wide flat types and the vision scales cheaply there. The moment an impl BODY enters
1-to-1 scope — and the oracle proves schema-rust already emits these bodies (this match
Display, and the multi-statement async fns in `runner_generated.rs`) — logos must also
carry a full Rust **expression / pattern / statement grammar**: `MatchSelf`,
`MatchArm`, `VariantPattern`, `NamedFieldPattern`, `MethodCall`, `WriteMacro`, format-
string literals, `SelfRef`, `MutRef`, `ElidedLifetime`, and everything the general case
adds (binary ops, `?`, let-bindings, closures, `.await`). This is exactly the
expression-grammar-dominated ~150–250-node cost the prior-art brief flagged
(`design-v0.md` §7.2). The vocabulary does not break — it stays wide and flat — but its
SIZE is now dominated by the expression grammar, not the ~19 declaration types.

**The decision this surfaces for the psyche:** are impl bodies (a) fully 1-to-1 logos
(adopt the whole expression grammar — largest but purest), or (b) a drawn tier boundary
where bodies are carried as a narrower construct (e.g. a small fixed set of "emitted
body shapes" the generator actually uses, since schema-rust emits only a handful of
body templates, not arbitrary Rust)? Option (b) fits the specialize-don't-generalize
instinct: enumerate the specific body shapes the emitter produces (a match-to-write
Display body, an actor `on_start`/`on_stop` body, a `RunnerEngines` delegating body)
as their own specialized structures, rather than a general expression grammar. [open]

## 6. Nomos — the brief→wordy expanders (`v1-types.nomos`)

Positional bodies throughout; no dotted-head labels inside a body. All [proposal].

```
GenericMacro.( Vector 1 ( Vec Element ) )

WireStructureFamily.(
  RustfmtSkip
  ( nota-text NotaDecode NotaDecodeTraced NotaEncode )
  ( Archive Serialize Deserialize Clone Debug PartialEq Eq )
  Public
  ( WireTupleStruct WireNamedStruct )
)

StructuralMacro.(
  WireStructDefaults
  Types
  WireTupleStruct
  WireNamedStruct
  ( SnakeCaseOfType RepeatDisambiguator )
)
```

`WireStructureFamily` stores the constant combo once (the specialized-form home for the
derives). `StructuralMacro` slot 3 handles a one-field brief decl (-> tuple newtype),
slot 4 a many-field decl (-> named struct); arity is the Nomos-side selector, so the
tuple-vs-named split is not a logos question [licensed by ruling — Choice 4 dissolves].
`FieldNameRule ( SnakeCaseOfType RepeatDisambiguator )` computes field names at
expansion, stored explicitly in logos [licensed by ruling — Choice 3].

## 7. Parsability — real nota 0.7.0 parse of every v1 sample

Method: `nota::Document::parse`, nota 0.7.0 `origin/main` `f8de7a51`, via the
scratchpad harness. Results:

- **All five v1 samples RAW-PARSE with zero errors.**
- **Dotted forms** (`v1-wire-slotted`, `v1-wire-specialized`, `v1-runtime-stress`,
  `v1-types`): each dotted head splits into an atom (dot absorbed) plus a separate
  block — e.g. `v1-wire-slotted.logos` yields 8 root objects (4 head-atoms + 4 bodies).
  Same OPEN CHOICE 1 behavior as v0; head-to-body binding needs the logos layer.
- **Headed form** (`v1-wire-headed.logos`): 4 clean single-tree root objects, head as
  first child — ready for landed structural dispatch.
- **Nested positional bodies parse exactly as drawn**: fields `( found Usize )`,
  variant lists, and the match/arm nesting all resolve; lowercase names (`found`,
  `formatter`, `write_str`) classify as symbols, PascalCase as pascal-symbols.
- **Format strings survive losslessly**: the pipe-square form `[| … |]` carries
  `{found}`, `0x{header:016X}`, and `:` as a single `pipe-text` block with zero
  children — i.e. Rust format strings with braces/colons raw-parse without being
  misread as structure. Plain square `[text]` was NOT used for interpolated strings for
  this reason; the pipe-square form is the robust literal carrier. [evidence].

Verdict unchanged in spirit from v0: everything raw-parses as structural triage; all
MEANING (which head is a type, which slot is a derive list, how a dotted head binds)
awaits the not-yet-built logos/Nomos expectation tables. The one new empirical win is
that the wordier 1-to-1 bodies, including impl-body expressions and format strings,
still sit inside the raw grammar today.

## 8. Annotation legend and reproduction

**[licensed by ruling]** cites `design-v0.md` (prior-session invariants, the
2026-07-11 dispatch/identity/1-to-1/positional-body rulings, and the resolved
Choices 3/4/5). **[proposal]** is invention awaiting markup. **[evidence]** is a
worker-verified fact with source.

Samples: `reports/logos/samples/v1-wire-slotted.logos`,
`v1-wire-specialized.logos`, `v1-wire-headed.logos`, `v1-runtime-stress.logos`,
`v1-types.nomos`. Harness (throwaway, not committed): `scratchpad/notaparse` against a
`git-archive/nota` worktree at `f8de7a51` (nota 0.7.0).
