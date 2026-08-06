# Protos Renewed Psyche Vision

Date: 2026-08-06
Author: Fable main-assistant session 9c422214-09c8-437c-89e3-018ce67b5e55.
Supersedes: reports/deep-vision/protos-engine-renewed-vision-2026-08-04.md.

Purpose: the current psyche-vision document for Protos. Every redesign
agent holds this in context. It is a vision and authority map, not an
implementation plan and not a design log. Where it conflicts with the
2026-08-04 report, this document wins; where it is silent, the
2026-08-04 report's uncontradicted material still stands and is
referenced rather than repeated.

## Sources

- design/ProtosEngine/visionReacquisitionRulings-2026-08-05.md
- design/ProtosEngine/deepCenterVision-2026-08-05.md (includes the
  2026-08-06 rulings appended to the session log)
- design/Spirit/SpiritIntentVisionGradation-2026-08-05.md
- reports/deep-vision/protos-engine-renewed-vision-2026-08-04.md
- handoffs/CodexProtosAddendum-2026-08-05.md

## Provenance key

- **Psyche**: directly stated or directly confirmed by the psyche.
- **Approved proposal**: agent-supplied shape the psyche confirmed.
- **Delegated**: the psyche or doctrine gave agents authority to
  choose the provisional shape.
- **Management**: decided by the Fable management session under
  standing doctrine; low seniority until psyche-reviewed.
- **Inference**: synthesis that is not itself authority.

## The spine: development is staged

**Psyche.** Protos develops in stages. This sentence governs how every
other sentence in this document may be used.

The destiny in the next section is direction and acceptance test. It
is never the scope of the current stage, and no stage can be refuted
by observing that it is not the destination. The bootstrap stage
deliberately leaves executable behavior in handwritten Rust; that is
the method, not a defect the current artifacts must compensate for.
Behavior gains its schema home when the train reaches the Logos
slice. A stage's artifacts are judged on strictness, beauty, and
extendability — that nothing in them forbids the later homes — never
on completeness against the destiny.

Two named failure modes, both observed in practice and both
forbidden: promoting a bootstrap artifact into a universal taxonomy,
and gating the current stage on questions that belong to a later one.
An agent that finds a place where a bootstrap shape would actively
block a future slice has found something real, and reports it as a
constraint on extendability. An agent that finds a domain merely
absent has found the method working.

## The deep center

**Psyche.** "Within a year, anybody worth his salt will use protos.
Within 2 or 3 years every other language will only exist in history
books." Protos is a general medium intended to replace programming
languages at large. The estate is the first consumer, not the
boundary. Schemas are designed for the world.

**Psyche.** "Ethos will be how humans and agents visualize and think
about code in general, along with dotos for data." The surfaces are
how one thinks and sees, whoever performs the mutation. Near-term
concretes: the harness will adopt Dotos, with LLM responses formatted
in Dotos triggering harness machinery that spawns further LLM calls;
Mentci, the slated GUI, will render most textual parts of the UI in
Ethos and Dotos. Readers of these formats include harnesses, agents,
and GUIs from the start — they are not compiler food.

**Psyche.** The yes-moment is the full self-hosting cascade: Protos
self-hosted, then rustc rewritten in Protos, then LLVM, then Mentci
and all components, finally the entire operating system. Nothing in
any schema may assume Rust, LLVM, or the current OS as a permanent
substrate. The cascade is itself the proof that development is
staged: it is a sequence, entered from the bootstrap.

**Psyche, spirit-grade.** "Beauty and elegant, extendable logic
always wins over everything, always. Beauty rules this universe."
When beauty or elegant, extendable logic conflicts with token cost,
familiarity, or convenience, beauty wins. This orders every trade-off
in the family, and the intent statement carries the same order: the
most beautiful text-based programming language, also geared towards
LLM efficiency, with terseness and information density as secondary
effect.

## Vision in one frame

**Psyche.** Encoded form is the truth; text, including Rust, is a
projection. The final system is a stateful, typed, operationally
edited language engine: encoded objects in daemon slots, changed
through atomic operations, rendering requested textual projections.
Text files are the bootstrap interface.

**Psyche.** The family's complementary surfaces: Dotos fills types
with data. Ethos specifies types and is the terse, sweet declaration
surface. Nomos is the typed transformer language that makes Ethos
adaptable — if Nomos never becomes a real language and the transforms
stay hand-written forever, the engine has failed its purpose. Logos
is the complete explicit program representation and the gateway to
assembly-Rust; executable behavior lives at Logos and below. Rust is
assembly and a Logos textual projection, not the authored semantic
center.

**Psyche.** Ethos does not cover runtime logic yet, because the
engine is not developed enough: the family starts with interfaces and
the language is extended, stage by stage, to take over more of Rust's
functionality later. Today an author writes a component's interfaces
in Ethos and its behavior in Rust; each stage moves that boundary
further down, until Rust is only assembly at the bottom. Beneath the
authored surface, Logos remains the complete explicit representation
of whatever the language covers at a given stage — ordinarily
generated through Nomos, directly authorable when needed. Programming
is not outside Protos; it is territory the language takes over as it
grows.

## Ruled surface, 2026-08-05 and 2026-08-06

Full wording lives in the rulings log; agents implement from these
without re-deriving.

- **Shapes and traits split on the surface.** Shape applications keep
  bare `< >`; trait pickups take guillemets `« »`. The 2026-08-04
  one-surface-syntax account is superseded.
- **Trait marks stand everywhere.** A trait requirement is
  guillemet-marked at every position it occupies, including inside
  shape slots. One pair may carry several trait symbols; the slot
  then requires all of them. Unmarked names inside shape slots are
  ordinary type references.
- **Canonical spellings** (derived mechanically from the rulings;
  canonical per the psyche's standing instruction unless he corrects
  them on sight): `Vector<«Ordered»>` ·
  `Result<Vector<«Ordered»> «Error»>` ·
  `«Left.Sortable» «Right.Sortable»` ·
  `Status.[Pending Ready.«Numeric»]` · `Range.{«Ordered» «Ordered»}` ·
  `«Ordered Serializable»`.
- **Imports.** An import entry's imported-name payload is a
  square-bracket vector: `interface.[Entry Referent RecordSet]`.
  Braces there are wrong. The colon is the qualification separator in
  import space, context-scoped; unquoted single-word strings keep
  interior colons. Token cost of the colon in this exact context is
  still to be measured (a task, not a ruling).
- **Parsing is a context machine.** Every symbol's meaning is scoped
  by the active typed parsing context; delimiter collision arguments
  against a symbol are void where context disambiguates.
- **Containers are modules, uniformly.** No coined root-container
  term: the outermost container is simply a module, the root of the
  module tree, submodules recursing beneath. All 2026-08-05
  candidates and the coining direction are rejected.
- **Textual-form metadata is bound to the encoded identity.** One
  record per object, keyed to the encoded ID, carrying visible name
  and module/file placement. Renames resolve through it to exactly
  one encoded identity; lookups work both directions. Module
  qualification lives in metadata, not in the object's name proper.
- **Ethos sources live in the owning component's repository.** The
  spirit-ethos repository proposal is rejected.

## Identity

**Psyche.** The ruled scheme: a true name is the hash of the object's
full body — its own name excluded, references included as the
referents' encoded names. Encoded names are randomly minted, never
content-derived; identity lives in the association table
`{EncodedName TrueName}`, updated by atomic operations, replayed from
the change log by reading, never re-derivation. References to living
objects go by encoded name, so self-reference and mutual reference
cost nothing. Rebirth mints fresh — deletion is a real death.
True-name Merkle recursion is reserved for frozen closures (pins,
releases) where the dependency DAG law bars cycles.

**Delegated.** Implementation details of the table are the
implementer's, provisional and reviewable: random mint of at least
128 bits, concrete storage and operation shapes chosen elegantly and
noted where review is useful.

**Management.** The half-finished content-identity/name-table
migration found doubled in the dependency graph (old hash-domain API
and flat name-table on one side, ContentAddressedHash and encoded
name-table on the other) is superseded as a destination: work tracked
as primary-eyr.1 lands directly on the ruled scheme above, treating
both intermediate sides as evidence. Finishing an intermediate whose
destination a ruling has displaced would make superseded code the
design reference, which the redesign doctrine forbids. If
implementation shows the ruled scheme fails to cover a concrete need
of those crates, that returns to the psyche as a specific question.

## The train and the current stage

**Psyche.** The family converges on main. Breakage on main is
licensed until the train completes and the new stack runs end to end;
consumer repos carry a temporary notice not to advance pins until
upstream is marked stable. Old code is not the design reference — the
gate is forward: file-kind schemas ruled first, then hand-written
bootstrap readers, then generation, then the next slice.

**Psyche, unchanged.** The MVP boundary stands: Spirit runs through
the redesigned generated Protos stack and demonstrates a live
`Stream<Event>` lifecycle plus persisted restart. The concrete finish
line, slice path, and non-goals of the 2026-08-04 report remain
operative.

**Current stage deliverable.** The three bootstrap file kinds
(interface, nexus, sema) as strict, beautiful, extendable schemas.
The proposal (reports/ProtosFileKindSchemas-2026-08-05.md, as revised
under the interfaces-first correction) is provisionally accepted for
MVP use — bootstrap readers may proceed on it — with the psyche's
review deferred and tracked as primary-5pm; the schemas carry
provisional seniority and remain revisable by that review.
Their behavior remains handwritten Rust by design. Questions about
schematizing executable behavior, effects, resources, concurrency, or
general data anatomy belong to later stages of the language's growth
and are filed as beads against those passes, never held as gates on
this one.

## Supersessions in force

The 2026-08-04 report's supersession list stands, plus:

- The one-surface quality syntax is superseded by the shape/trait
  delimiter split; guillemets are spent on trait pickup and are no
  longer a reserved extension pair.
- The open encoded-name minting question is closed: random mint.
- Root-container coinage (and the crate-analogue framing) is
  superseded by uniform module terminology.
- The intermediate content-identity/name-table migration is
  superseded as a destination (management ruling above).
- The pre-redesign nota/schema surface is historical; no
  compatibility with it anywhere.

## Open and deliberately pending

- Colon token-cost measurement in import space (task; result feeds
  the design log, not a gate).
- reports/ProtosFileKindSchemas-2026-08-05.md: provisionally in MVP
  use; deferred psyche review tracked as primary-5pm.
- reports/SpiritHierarchyProposal-2026-08-05.md,
  reports/AnatomyOfAGoodMachine-2026-08-05.md: pending psyche review.
- primary-eyr.1 identity-scheme landing: direction set above;
  execution follows the train.
- The Logos-slice behavior schema pass: future; collect its questions
  as beads.
