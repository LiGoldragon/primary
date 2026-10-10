# Spirit Ethos Fixtures — Review Walkthrough — 2026-08-02

Three fixtures authored for whole-syntax review, per the bootstrap
proposal's Phase 1. They cover spirit's core admission, query,
registration, and observation surface with real vocabulary from
`signal-spirit` 0.13.0 and the spirit domain lineage; the long tail
(stash, supersession, retirement, clarification...) follows the same
forms mechanically and is omitted to keep the review focused.

## Reading the files

Every file is three objects: **header** (`Kind.Version`), **imports**
(grouped by source; `[]` when nothing external is needed — every field
present), **body** (a brace product of the kind's fixed positions, each
position a bracket list of declarations).

The delimiter semantics used throughout, position-local as ruled:

- `{ }` — **all-of**: a product. Struct bodies, trait bodies (a
  trait's methods are an all-of bundle), the file body itself.
- `[ ]` in a definition — **one-of**: enum alternatives.
- `[ ]` at a section position — **many-of**: a variable-length list of
  entries.

## interface.ethos

Body positions: inputs, outputs, refusals, shared types.

- `Record.Entry` in the inputs position: an input named Record carrying
  an Entry. The section supplies Input-trait membership — nothing
  written.
- Refusal entries carry their shape (`GuardianRejection.{GuardianReason
  Explanation}`); the section supplies Refusal membership, and the Rust
  error machinery is emitted, never authored.
- `Stream.Observer.{ObserverFilter ObserverSubscription
  ObservationEvent}` — operator-first standalone application in the
  types list, beside name-first shape declarations; the resolution rule
  distinguishes them. Payload positions: open-query, receipt, event.
- **Stream-open types do not appear in the inputs section**: the Stream
  declaration already says ObserverFilter opens Observer, and the
  object emits its Input membership — listing it under inputs would be
  repetition.
- Universal names (`Text`, `Integer`, `Vector`, `SubscriptionToken`,
  `Unit`) are prior definitions and need no import.

## nexus.ethos

Body positions: operand types, traits.

- Fallible machinery returns decision enums
  (`AdmissionDecision.[Accepted Rejected.GuardianReason]`) rather than
  a Rust `Result` — Result is assembly; Ethos declares the type.
- `recordDecision.{AdmissionDecision Unit}` shows the explicit `Unit`
  return (absence of a result is information the position cannot
  infer).
- Imports show the sibling-file form: `interface.{Entry Referent
  RecordSet GuardianReason}` — the guardian's refusal reasons are the
  wire refusal vocabulary, referenced, not redeclared.

## sema.ethos

Body positions: record types, families.

- Families are name-first `table.{Record Key}` — the section supplies
  the family operator, so it is written zero times.
- `signal-domain.Domain` shows the cross-component import; the family
  keys are Domain-typed as in spirit's live sema schema today.

## Conventions used, awaiting your reaction

1. Method names are lowerCamel (`guardReferent`); types and variants
   PascalCase; table names bare lowercase atoms.
2. Trait bodies use braces (all-of), per the approved
   `ScopeContainment.{contains.{Scope Bool}}` shape.
3. A stream's receipt is an authored type (`ObserverSubscription`)
   wrapping the universal token; two streams may share or own receipt
   types freely.
4. Version is a bare integer for now (`Interface.1`), bumped per the
   future standard.
5. The body is one brace object of fixed positions; each position is a
   bracket list. Fixed-arity products take braces, variable-length
   collections take brackets — everywhere.
