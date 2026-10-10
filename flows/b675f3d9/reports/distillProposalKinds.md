# Distillation proposal: Vision/kinds.md and Vision/anatomy.md

Composed in flow b675f3d9 from reports/distillCandidatesKinds.md.
Each statement lands only on the living's explicit approval.

---

# Vision/kinds.md (proposed)

# Kinds

## Kind is the word

In Ethos the word is kind, not trait. A kind is what a Rust trait
becomes, one abstraction up: declaring a new kind declares a new
trait on the Rust side, and implies things Rust has no word for,
still to be settled. "Trait" is set aside for being acoustically
ambiguous in speech.

## A kind is named as a qualifier

A kind's name says what its bearer can be — Runnable, Writable,
Readable — never the bare verb. Write is not a kind. This closes the
earlier acceptance of verb and infinitive names.

## Capability

A capability is an actual function a kind has. Runnable is the kind;
run is one of its capabilities.

## Interaction

An interaction is a kind's implementation on a type — what Rust calls
an impl. An interaction always involves the type itself; one that
does not use the type is not an interaction of that type.

## Concept

A concept is a type or a kind: the word for any position that may
hold either.

## There are no generics, only kinds

Every position Rust fills with a generic parameter and its bounds is,
in Ethos, a kind standing in that position. Several kinds in one
position adjust the emitted Rust; the parameter itself never appears.

## A kind's identity is its name and its positions

As in Rust, a kind is identified by its name together with the
identity parts of its data: the kinds standing in its positions. They
are written in the head — `Processable<[Clonable Sendable]
Serializable>` — each position holding one kind or a homogeneous
vector of kinds. Superkinds, associated types and capabilities are
not identity.

## Kinds are declared explicitly

A kind is declared, never extracted from its interactions. Recovering
what a kind is and how many interactions it has from implementations
would be complex, and is not done.

## Declaration is the first scope

The first Ethos declares kinds; it does not implement them.
Declaration syntax is the scope of the first version; implementation
syntax is a later, larger job.

## Creation is From

Creation is TryFrom or From, called by those names. There is no
Create kind and no alias over them.

## Rust's own traits keep their names  (lean — approve, hold, or drop)

Referring to Rust's existing traits through a translation table costs
more than it gives; a Rust trait may be referred to as Rust names it.

---

# Vision/anatomy.md (proposed)

# Anatomy

## The map before the code

An agent that writes code before it holds a model of the world has
already failed; catching a fake kind afterwards is too late. Work
begins with a map of what is being made — its ontology, its anatomy,
an object- and capability-oriented layout. The map is the Ethos
interface file. Old code is at most inspiration for the map.

## Ontology is designed before it is implemented

Every behaviour falls under a kind, which makes an ontology in code.
Placeholder kinds created for each function make no ontology. The
ontology is designed first; agents are trained and given a workflow
for it. A protocol for creating the anatomy of a well-designed
object-and-capability machine is still owed. The universal nexus
kinds — the basic ontology of an actor/dataflow system — are
designed first of all.

## Types first

Types are thought through first; kinds are what types implement.
Kinds are not sought first with types invented to fit them.

## Costume kinds

A kind whose capabilities are ordinary functions wearing a trait's
clothing misses the approach entirely. This is the cornerstone
misunderstanding agents have of the vision.

## The three-part machine

A machine agglomerates several types, creates one coherent type from
them, and converts it to another type. The shape nests fractally and
takes many spellings — a method body accumulating variables is one —
and no single spelling is invested in.

## Demand-driven: From over Into

Things are created from other things; nothing is harvested and then
asked what it might become. From is preferred to Into.

## Sections confer

Sections exist to confer different kinds on their items — Input,
Output, Refusal. That is the point of having sections.

## Processing is for the effect

When an object enters a nexus, the point is the effect it has; the
response is an effect of that effect, not the aim. Conversion is the
wrong picture of processing. The verb for it is not yet ruled.

## A spoken vocabulary

Programming was never done in speech. A spoken vocabulary for
software engineering is being created, one abstraction up from Rust;
the discipline may be called logic engineering.

---

## Suspected impurities — the living's judgement asked

- kinds.md "Declaration is the first scope" — MVP scope: working
  decision or vision?
- anatomy.md "Ontology is designed before it is implemented": "A
  protocol ... is still owed" and "The universal nexus kinds ... are
  designed first of all" — the first is a task, the second may be a
  working priority.

## Not distilled (open)

- The word for a kind's declaration itself ("trait declaration" still
  in operational use).
- The effect verb (Apply liked, uncertain; "we need a new terminology").
- What declaring a kind implies beyond Rust (tbd).
- Tuples (no tuple in designed code, allowed at a contact point only)
  — belongs to a Rust-conventions topic, not kinds.
- The structural Capability enum, arity and head delimiters — go with
  protos syntax, pending that gatherer.

## Sources

- flows/b675f3d9/reports/distillCandidatesKinds.md (record ids there)
