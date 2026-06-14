# Operator frame for Structural Forms

This is the operator-side implementation frame for the Structural Forms epic
named in `reports/designer/627-structural-forms-the-concept.md`. It reads that
report together with `reports/designer/625-operator-spec-self-host-macro-table-type.md`,
`reports/designer/626-vision-language-as-data-macros.md`, and
`reports/system-designer/103-structural-macro-as-schema-data.md`.

The short version: the direction is coherent, and parts of it are already real
in the current Spirit stack. The implementation must stay strict about which
layer is being specified:

- NOTA is the structural data syntax.
- Schema is the typed description of the shapes.
- Schema files are typed component interface contracts.
- Generated Rust is the current execution/rendering layer, not the source of
  truth.
- The runtime engine implements the typed contracts; it is not the language
  substrate.

## Fresh intent captured

Two records were added from the psyche prompt because they changed durable
architecture, not just today execution.

`xbc2` records the constraint that schema files are strict typed component
interface contracts: their input/output roots, imports, and namespace define the
messaging/API surface the engine implementation must use.

`0678` records the decision that stable public signal schemas belong in contract
repositories separate from daemon logic crates, so consumers compile against the
stable interface instead of rebuilding when daemon internals change. Its
certainty is Medium because the exact generated-Rust hosting rule still needs a
mechanical decision.

## What is already true

The Spirit stack already demonstrates the contract/daemon separation the prompt
describes.

`/git/github.com/LiGoldragon/signal-spirit` owns the ordinary peer-callable
Spirit signal contract. Its `schema/signal.schema` defines the public operation
and reply roots:

```schema
[State Record Propose Clarify Observe Remove ChangeRecord Tap Untap Version Marker]
[RecordAccepted Proposed RecordsObserved RecordRemoved RecordChanged ObservationTapped Error Rejected]
```

`/git/github.com/LiGoldragon/spirit` no longer owns that ordinary public signal
schema. Its local schemas are daemon-side planes (`nexus`, `sema`, and
`meta-signal`), and `spirit/build.rs` imports `signal-spirit` through
`DependencySchema::from_cargo_metadata`.

The daemon-side Nexus schema then specializes the runtime frame by importing the
public contract as the thing that arrives and the thing that leaves:

```schema
{
  SignalInput signal-spirit:signal:Input
  SignalOutput signal-spirit:signal:Output
}
[SignalArrived SemaWriteCompleted SemaReadCompleted EffectCompleted]
[CommandSemaWrite CommandSemaRead ReplyToSignal CommandEffect Continue]
```

That is the good bridge: schema types specialize the runtime. It does not make a
macro into a runtime reaction. It makes the runtime implementation obey the
schema-defined interface.

The current code also already treats generated artifacts as a freshness-checked
contract. `spirit/build.rs` generates schema artifacts and calls
`write_or_check("SPIRIT_UPDATE_SCHEMA_ARTIFACTS")`, so checked-in generated Rust
is not just stale cargo; it is a reviewable witness that the data contract still
matches the source schema.

## What is not yet true

Structural Forms as a language substrate are not complete yet.

- Macro definitions are already data, but the macro-table nouns are still
  partly hand-written in `schema-next`. That is the `625` operator slice.
- The shape vocabulary (`#[shape]`, `StructuralNodeSpec`, and friends) is not
  yet itself schema data. That is the `103` slice.
- Generated Rust hosting is not fully settled. Some generated modules can live
  in a contract crate as checked-in reference/witness code, but any implementation
  that needs local trait implementations has to respect Rust coherence. If the
  generated type lives in one crate and the trait lives in another, a third crate
  cannot implement the foreign trait for the foreign type without a wrapper.
- Worktree/lane hygiene is not encoded strongly enough. There are many old
  worktrees under `~/wt/github.com/LiGoldragon`. Some may be merged, some may be
  abandoned, and some may carry useful unmerged design. That needs a separate
  audit pass before the Structural Forms branch stack becomes noisy.

## Core constraints

Structural Forms only works if we do not smuggle the old compiler back in.

Do not hand-write parsing logic for each elegant syntax. The durable unit is a
typed shape definition. The matcher should be a small recursive structural decode
over NOTA blocks, driven by schema-defined forms.

Do not filter generated Rust strings to fake partial self-hosting. If the first
slice needs only the macro pattern family, the emitter should either generate a
real namespaced module and import the needed nouns, or learn an explicit
schema/family selection concept. A substring pass over emitted source recreates
the drift this work is trying to remove.

Keep the frozen seed named and small. The seed is the NOTA block parser plus the
minimal derive/runtime logic required to bootstrap structural decoding. Everything
above that seed should be data, generated from data, or checked against data.

Treat Rust as the current lowering target, not as the semantic authority. Rust
can be optimized as an assembly-like layer, but the operator implementation still
needs typed Rust source that reviewers and the compiler can inspect. "Rust as
assembly" is not permission for opaque generated strings or untyped escape
hatches.

Prefer contract crates for stable public interfaces. Daemon-local schemas can
live with the daemon. Public signal schemas belong in signal contract repos so
callers do not rebuild just because daemon logic changes.

## Syntax sketches

These are deliberately small; the point is to show what must remain structural.

A component interface contract is a schema file shaped like a function
signature: imports, input roots, output roots, then the local vocabulary.

```schema
{
  Entry signal-spirit:signal:Entry
  RecordIdentifier signal-spirit:signal:RecordIdentifier
}
[Submit Observe]
[Accepted Observed Rejected]
{
  Submit Entry
  Observe RecordIdentifier
  Accepted RecordIdentifier
  Observed Entry
  Rejected String
}
```

An enum is not magic syntax. It is a structural form that says this noun has a
closed set of variants in this scope:

```schema
IntentAction [(Submit) (Observe) (Reject)]
Submit Entry
Observe RecordIdentifier
Reject String
```

A future form definition should itself be data. This sketch is not current
syntax; it is the operator shape I would expect `103` to converge toward:

```schema
StructuralForm {
  name EnumForm
  delimiter Bracket
  head EnumName
  children (Repeat VariantReference)
  produces EnumDeclaration
}
```

The important property is recursive structural matching. The block form, child
slots, and produced typed value are data. A new language construct is a new
typed form definition, not a new parser branch.

## First operator slice

I would start with the `625` macro-table self-host slice, not with the whole
language dream.

The branch should prove this narrow claim:

> The macro-table pattern-family Rust nouns used by `schema-next` can be emitted
> from `schemas/core.schema`, then imported by the hand-written macro expander,
> with generated artifacts checked by the existing Nix/Cargo freshness path.

That branch should not attempt to make `StructuralNodeSpec` data yet. It should
leave `103` cleanly next.

Expected implementation pressure points:

- `MacroCaptureName String`, `MacroAtom String`, and similar bare declarations
  lower as newtypes, not aliases. That is correct.
- `MacroPatternObjects { values (Vec MacroPatternObject) }` is currently a
  wrapper around a vector where hand-written code may expect a direct vector.
  Treat that as an adaptation point, not as a reason to weaken schema emission.
- Recursive rkyv bounds may need explicit emitted attributes or a local emitter
  rule equivalent to the current hand-written `#[rkyv(omit_bounds)]`.
- If the emitter can only generate a full `core.schema` declaration module at
  first, keep it namespaced and explicitly import the pattern family. Do not
  claim that as final family-selection design.

## Branch and worktree handling

For the first implementation branch, I would use a lane-marked descriptive name
such as `operator-structural-forms-macro-table` under
`~/wt/github.com/LiGoldragon/schema-next/operator-structural-forms-macro-table`
or the equivalent repository-specific worktree path.

That naming is intentionally boring. The branch name should answer who owns the
worktree and what it is proving. Designer can later codify the exact lane prefix
rule in the skills.

I would not clean old worktrees opportunistically during the first implementation
branch. The current `~/wt/github.com/LiGoldragon` surface has enough historical
branches that deletion needs an audit report first: merged, abandoned,
superseded, and unmerged-useful are different outcomes.

## Open decisions

Generated Rust hosting still needs a precise rule:

- Contract repo checks in generated Rust as the reference/witness.
- Consumer repo either imports the contract crate directly, regenerates local
  modules from the schema source, or includes generated code under its own crate.
- The choice depends on which traits must be implemented locally and whether
  those traits/types are foreign under Rust coherence.

The right answer may be mixed: public wire nouns live in the contract crate;
daemon-local runtime implementations live in the daemon crate; generated
schema-derived declarations can be copied/regenerated only where coherence
requires ownership.

Worktree lifecycle also needs a skill update:

- feature worktrees should be lane-marked;
- merged worktrees should be cleaned promptly;
- unmerged designer branches should be reviewed by operator before integration;
- unmerged operator branches should be auditable by designer when they carry
  design consequences.

## Operator recommendation

Accept Designer's name, **Structural Forms**, and treat it as the meta-epic.
Implement it in small proof slices:

1. `625`: schema-emit macro-table pattern nouns from `core.schema`.
2. `103`: make the structural node/form vocabulary data.
3. Contract hosting: write the generated-Rust ownership/coherence rule and
   enforce it in one real contract/daemon pair.
4. Only after those pass, represent richer implementation logic as schema data.

The reason for that order is mechanical: it keeps each proof tied to one layer.
If the first branch tries to prove self-hosted language, structural forms,
contract repos, Rust-as-lowering, and worktree policy at once, the result will be
too broad to debug. The macro-table pattern family is the smallest load-bearing
brick that still points at the whole system.

## Verification run

I checked the current schema syntax assumptions against `schema-next`:

```text
cargo test design_example
cargo test bare_reference_declarations_lower_to_newtypes
```

The design-example suite passed, including the four-part schema document shape,
structural macro nodes, direct enum variant shapes, and schema-declared
signal/nexus/sema planes. The lowering test passed and confirms that bare
reference declarations lower to newtypes, which matters for schema-emitted
macro-table leaves like `MacroCaptureName String`.
