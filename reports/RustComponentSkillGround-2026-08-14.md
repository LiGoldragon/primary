# Rust Component Architecture Skill -- Research Ground

Researcher: session ba906ae2 (Designer-dispatched).
Date: 2026-08-14.
Purpose: raw ground for the skill proposal, organized as the psyche
directed. The Designer drafts the proposal with the psyche from this.

---

## 1. Still-Relevant Old Vision

Each excerpt is verbatim from the pre-reset corpus
(`reports/PreResetCorpus-2026-06-07/skills/`), followed by why it
stands under current rulings.

### 1A. The repo triad shape

> Every stateful capability is a triad of three repositories:
> `<component>/` ... `signal-<component>/` ... `meta-signal-<component>/`
> The contract crates carry no runtime, no actors, no `tokio` -- they
> declare typed wire vocabulary and generated method surfaces, and
> nothing else.

-- component-triad.md, "The shape"

**Why it stands.** The current skill (SKILL.md) restates this
verbatim. The psyche's 2026-08-14 "reconsider everything" entry
explicitly keeps Signal/Nexus/SEMA vocabulary and principles.
The 2026-08-11 ruling confirms "3 repos per component"
(threeStacks.md). The 2026-08-09 metaSignalNotOptional.md
supersedes the old corpus's "meta-signal is optional" (invariant 3
of the old component-triad.md, line 109).

### 1B. The five invariants (with one correction)

> 1. The CLI has exactly one Signal peer -- its own daemon
> 2. The daemon's external surface is exclusively signal-frame frames
> 3. [meta-signal is optional -- SUPERSEDED]
> 4. Two authority tiers -- both part of the triad
> 5. Policy state and working state -- both in one sema-engine DB

-- component-triad.md, "The five invariants"

**Why they stand (except 3).** Invariants 1, 2, 4, 5 are restated
in the current skill and confirmed by the psyche's repeated
statements about daemons speaking signal, CLI as text-to-signal
bridge, meta socket for configuration, and sema as the durable
store. Invariant 3 is overruled:

> the metasignal is not optional because otherwise there's no way to
> configure the daemon.

-- psyche, 2026-08-09T12:30Z (metaSignalNotOptional.md)

### 1C. The one argument rule

> Every component process takes exactly one argument on argv, and never
> a flag. The accepted encoding differs by edge.
> CLI / human-agent edge -- inline NOTA argument, a path to a NOTA
> file, or a path to a signal-encoded file.
> Daemon edge -- a path to a pre-generated signal-encoded/rkyv startup
> message/file only.

-- component-triad.md, "The one argument rule"

**Why it stands.** Restated in the current skill. The spirit daemon
binary confirms: `fn main() -> ExitCode { SpiritDaemon::run_to_exit_code() }`
(`spirit/src/bin/spirit-daemon.rs:4`).

### 1D. Contract repos: vocabulary only, closed enums, verb-form operations

> The contract crate owns: The Frame envelope and its encode/decode
> methods ... The closed enum of request kinds + paired reply kinds ...
> per-operation typed payloads (closed enums of typed kinds -- no
> generic record wrapper, no Unknown variant).

-- contract-repo.md, "What goes in a contract repo"

> The operation root is a verb, in verb form. Use Submit, not
> Submission; Query, not QueryRequest.

-- contract-repo.md, "Operation naming rule"

> Reply success variants are verb-past-tense matching the operation
> root. Submit -> Submitted; Register -> Registered.

-- contract-repo.md, "Reply discipline"

**Why it stands.** Directly restated in the current skill. The
psyche's 2026-08-14 ruling on interface sections confirms
sections are shape-defined, variants are data-carrying, and the
ethos generates the type in Rust (signalIsOurMessagingLayer.md
2026-08-14). The verb-form rule is not contradicted by any
current ruling.

### 1E. The runtime triad: Signal / Nexus / SEMA three execution centers

> Signal is the reactive external surface... Nexus (renamed from
> Executor) is the execution-layer schema type and the daemon's mail
> keeper + Signal-to-SEMA translator... SEMA is the single-writer
> state layer.

-- component-triad.md, "Runtime triad"

> NexusWork/NexusAction asymmetric pair + 5-variant action set
> (ReplyToSignal, CommandSemaWrite, CommandSemaRead, CommandEffect,
> Continue)

-- component-triad.md, "Nexus mechanism substrate"

**Why it stands.** The psyche's 2026-08-14 "reconsider everything"
keeps the Signal/Nexus/SEMA vocabulary and principles, while noting
"we aren't tied to how they were used and implemented in the past."
The NexusAction loop is confirmed landed in triad-runtime
(`triad-runtime/src/runner.rs:157-198` -- `Runner::drive()`).

### 1F. Actor discipline: actors all the way down

> Actors all the way down. Every non-trivial logical plane deserves
> an actor. Smallness is not an objection; triviality is.

-- actor-systems.md, "Core rule"

> Actor per plane: an actor-heavy system should look over-named to
> conventional Rust eyes.

-- actor-systems.md, "Actor per plane"

**Why it stands.** The psyche's 2026-08-14 entry explicitly recalls:
"I want the main engine to be driven by actors. And we did actually
even fork the actor library that we were using." Kameo 0.20 remains
the framework (confirmed by triad-runtime re-exporting kameo). The
fork at `/git/github.com/LiGoldragon/kameo/` has 6 commits ahead
of upstream with lifecycle control improvements.

### 1G. Subscription lifecycle

> The shape every push-stream subscription takes on a Signal channel:
> typed open, typed event stream, typed close, final acknowledgement,
> end. The producer pushes; the consumer subscribes; the close is a
> real request, not a socket hang-up.

-- subscription-lifecycle.md

> Every typed subscription passes through exactly five named states:
> Subscribing -> Streaming -> Retracting -> Closed.

**Why it stands.** Push-not-poll is spirit-level doctrine. The
current skill says "observation flows up ... state is observed
through push subscriptions -- a typed snapshot on open, typed
deltas after." The stream section design continues in psyche
(streamSection.md, observerFixtureBlessed.md).

### 1H. Micro-components: one capability, one crate, one repo

> Every functional capability lives in its own independent repository
> with its own Cargo.toml, flake.nix, and test suite. Components
> communicate only through typed protocols.

-- micro-components.md

**Why it stands.** The current skill says "one capability, one
component." The psyche's 2026-08-11 ruling confirms "3 repos per
component" and reusable shared libraries especially for shared
traits.

### 1I. Naming: full English words, verb-on-noun, no redundant ancestry

> Spell every identifier as a full English word ... Names don't carry
> their full ancestry -- the surrounding namespace already supplies
> that context.

-- naming.md

> Every reusable verb belongs to a noun. If you can't name the noun,
> the model isn't formed yet.

-- abstractions.md

**Why it stands.** The trait-first principle in the current skill
extends these: traits are the nouns verbs attach to. The psyche's
2026-08-13 ruling on trait naming (qualifiers, then verbs accepted)
adds precision but does not contradict the base rules.

### 1J. Storage and wire: redb + rkyv durable state and binary wire

> The boundary decision: in-process typed values, IPC rkyv, disk
> redb+rkyv, human NOTA/Datom. One redb file per component. Values
> are rkyv-archived bytes. The sema-engine pattern: two-layer
> substrate (sema kernel + sema-engine library).

-- rust/storage-and-wire.md (summary)

**Why it stands.** The current skill says the daemon owns its sema
database in a `.sema` file, reached only through sema-engine. The
psyche's 2026-08-14 entry says sema (the database engine) is
authored in ethos so stored types are visible, and matters MORE
than nexus. The redb/rkyv substrate is not questioned.

### 1K. Methods: behavior on data-bearing types, domain newtypes, one-object-in-out

> Schema-generated objects are the method surface. The labor split:
> .schema file -> emitted Rust -> agent-written methods on emitted
> nouns.
>
> Domain values are types. One type per concept. One object in, one
> object out. No string typification. Constructors: new/with_*/from_*.

-- rust/methods.md (summary)

**Why it stands.** The current skill says "traits live on data-bearing
types; a zero-sized type with behavior is a namespace pretending to
be a thing." The no-free-functions rule is directly stated. The
psyche's mandatory-traits Intent strengthens this: every method call
lives under a trait.

---

## 2. Fallen Parts

Each item names the old-corpus doctrine, then the ruling that felled
it (verbatim, dated).

### 2A. Meta-signal is optional (old invariant 3)

**Old doctrine:** "Some components have no owner relationship -- they
only need the ordinary signal-<component> contract." (component-triad.md,
line 109-113)

**Felled by:**
> the metasignal is not optional because otherwise there's no way to
> configure the daemon.

-- psyche, 2026-08-09T12:30Z (metaSignalNotOptional.md)

### 2B. Schema-rust-next as the code generator

**Old doctrine:** The entire runtime triad was generated by
`schema-rust-next`, emitting `RustEmissionTarget` variants
(WireContract, SignalRuntime, NexusRuntime, SemaRuntime). Schema
files (`signal.schema`, `nexus.schema`, `sema.schema`) lived inside
the daemon crate. (component-triad.md lines 30-47, 1140-1200)

**Felled by:**
> we can keep the Signal, Nexus, SEMA vocabulary and principles,
> but we aren't tied to how they were used and implemented in the
> past.

-- psyche, 2026-08-14T20:48+02:00 (rustComponentArchitecture.md)

And the ethos replacement:
> the ethos generates the type in rust

-- psyche, 2026-08-14T15:09+02:00 (signalIsOurMessagingLayer.md)

The `.schema` language is replaced by ethos as the authoring surface.
The schema-rust-next pipeline is the "incorrect new stack" that was
frozen (threeStacks.md 2026-08-10). The ethos-monolith daemon
replaces it:

> the shortcut stack for the new syntax ... it's going to be a daemon
> also. So to differentiate it, we should call it maybe the ethos
> monolith

-- psyche, 2026-08-14T20:48+02:00

### 2C. core-<component> as a library split

**Old doctrine:** "core-ethos is a dependency of the Ethos daemon"
(everythingIsInTheDaemon.md line 88-89, implied by the old repo
layout).

**Felled by:**
> I dont know if we need a core-* repo. I dont see much point. so
> ethos can have all the code, minus the two signal repos

-- psyche, 2026-08-11T00:39+02:00 (threeStacks.md)

The current skill preserves core-<component> as "optional" but the
psyche's direction is against it for new components.

### 2D. The "code/encoded" form vocabulary

**Old doctrine:** "The encoded form is the code" -- the rkyv
serialized payload is "the code." (encodedFormIsTheCode.md 2026-08-06)

**Felled by:**
> working form and signal form, drop code/encoded entirely

-- psyche, 2026-08-13 (encodedFormIsTheCode.md)

Replaced by three forms: real form (where values are born and
changed), signal form (portable rkyv projection), textual form
(protos syntax). The trait pair is protos::Realize and
protos::Textualize.

### 2E. "Transcodable" as trait vocabulary

**Old doctrine:** "all protos dialects are transcodable"
(traitsAsCapabilities.md 2026-08-13 early entry)

**Felled by:**
> I dont think it survives. I think we end up with things like
> WorkingFormCastable

-- psyche, 2026-08-13 (traitsAsCapabilities.md, "transcodable falls
with the drop")

Successors: protos::Realize (text-to-form) and protos::Textualize
(form-to-text), both confirmed 2026-08-14.

### 2F. Sema classification vocabulary on the public wire

**Old doctrine:** The six Sema classes (Assert, Mutate, Retract,
Match, Subscribe, Validate) appeared on public contracts.
(component-triad.md "Verbs come in three layers")

**Partially felled:** Per psyche 2026-06-04 (record 2612, in
contract-repo.md): "Sema classification vocabulary is forbidden on
the public contract wire." The classes remain as internal
classification (the ToSemaOperation trait), but public operations
use domain-specific verbs (Submit, Query, Configure, etc.).

### 2G. Persona-specific binary naming table

**Old doctrine:** The 13-row binary naming table mapping persona-*
components to CLI and daemon binary names.
(component-triad.md lines 179-194)

**Felled by:** The psyche's "find the parts that are skill, take out
the parts which act in any other way, like listing repos or other
such non-skill content." (rustComponentArchitecture.md 2026-08-09).
This is repo documentation, not universal skill. The PATTERN (CLI
takes the short role-name, daemon takes <component>-daemon) survives
in the current skill.

---

## 3. How the Old Daemons Actually Did It

Concrete mechanics from the living code, with file:line.

### 3A. The one-liner main

The spirit daemon main is truly one line:
```rust
fn main() -> std::process::ExitCode {
    SpiritDaemon::run_to_exit_code()
}
```
-- `spirit/src/bin/spirit-daemon.rs:3-5`

`SpiritDaemon` implements `ComponentDaemon`, the schema-emitted trait
at `spirit/src/schema/daemon.rs:80` that defines the daemon's
hook surface: `Configuration`, `Engine`, `Error` associated types,
`build_runtime()`, `handle_working_input()`, `start()`, `stop()`.

### 3B. The three-plane actor pattern

The canonical three-actor pattern (sema-storage reference):

- `SemaPlane` owns the `Engine` directly, handles `Execute` messages
  -- `sema-storage/src/lib.rs:240-244`
- `NexusPlane` holds `ActorRef<SemaPlane>`, forwards via `.ask()`,
  broadcasts `ChangeEvent` -- `sema-storage/src/lib.rs:515-528`
- `SignalPlane` holds `ActorRef<NexusPlane>`, admission counter
  -- `sema-storage/src/lib.rs:556-564`
- `Runtime::open` spawns Sema -> Nexus -> Signal in order
  -- `sema-storage/src/lib.rs:595-606`

This pattern repeats in ethos-engine and logos-engine.

### 3C. The NexusAction step-loop

`triad-runtime` implements the continuation-budgeted step loop:

- `NextStep` enum: `SemaWrite`, `SemaRead`, `RunEffect`, `Reply`,
  `Continue` -- `triad-runtime/src/runner.rs:26-32`
- `RunnerEngines` trait: `decide_next_step` method
  -- `triad-runtime/src/runner.rs:34-58`
- `Runner::drive()` loops until budget exhausted or Reply
  -- `triad-runtime/src/runner.rs:157-198`

Spirit's NexusEngine implementation:
- `impl NexusEngine for Nexus` -- `spirit/src/nexus.rs:962`
- Sema delegation: `apply`/`observe` -- `spirit/src/nexus.rs:868-885`

### 3D. The sema/redb store

Two-layer substrate:

**sema (kernel):** `sema/src/lib.rs`
- `Sema` struct owns `redb::Database` -- `:471-474`
- `Table<K, V>` typed wrapper, values always rkyv bytes via
  `TableDefinition<K, &[u8]>` -- `:231-268`
- `Sema::write`/`Sema::read` with closure-scoped transactions
  -- `:568-581`

**sema-engine (library):**
- Adds catalog, subscription, checkpoint, counter tables
  -- `sema-engine/src/engine.rs:42-80`
- `TableSpecification` trait -- `sema-engine/src/table.rs:27-84`

Spirit's Store implements SemaEngine:
- `impl SemaEngine for Store` -- `spirit/src/store/mod.rs:157`
- Wraps `Arc<SemaDatabase>`

### 3E. Subscription mechanics

Spirit manages subscriptions through:
- Token issuance in Nexus:
  `spirit/src/nexus.rs:572-582` (OpenIntentSubscription,
  ObserverSubscription)
- `IntentSubscriptionToken` bridging schema-emitted tokens to
  triad-runtime tokens: `spirit/src/subscription.rs:20-34`
- The emitted daemon module wires `SubscriptionRegistry` and
  `SubscriptionEventPublisher`:
  `spirit/src/schema/daemon.rs:30-31`

### 3F. The schema-emitted daemon module

`spirit/src/schema/daemon.rs` is `@generated by schema-rust` and
contains:
- `ComponentDaemon` trait (lines 80-160+): the hook surface
- `WorkingInputLane` enum: Immediate vs Staged (line 39-42)
- `StagedAdvance` trait for multi-phase operations (line 57-71)
- Kameo actor imports from `triad_runtime::kameo` (lines 14-21)
- Subscription infrastructure (line 30-31)

### 3G. The kameo fork

At `/git/github.com/LiGoldragon/kameo/`:
- 6 commits ahead of upstream (tqwewe/kameo)
- Focus: lifecycle control split, terminal lifecycle outcomes,
  weak shutdown result helpers
- Net: +2776 -8307 lines (significant cleanup/restructuring)
- The fork addresses the release-before-notify discipline from
  actor-systems.md (the supervision gotcha with redb handles)

---

## 4. Gaps the New Ground Demands

These are capabilities the psyche's 2026-08-14 charge names that
neither the old corpus nor the current skill covers.

### 4A. Traits as ontology

**The charge:** "every behavior to fall under a trait, which
essentially creates an ontology in code"
(rustComponentArchitecture.md 2026-08-14)

**What exists:** The current skill has "Traits first" -- every method
call lives in a trait. The mandatoryTraits Intent says the same.
But neither describes HOW traits create an ontology -- the
relationship between traits (sub-trait chains, capability
composition), how trait hierarchies express domain concepts, or
how the trait surface becomes the psyche's comprehension layer.

**Gap:** The skill needs a section on trait ontology design: how to
decompose a domain into traits, how trait hierarchies map to
conceptual hierarchies, what makes a good sub-trait chain versus a
flat collection of traits, and how the ethos-authored interface
exposes this ontology for reading.

### 4B. Actor-driven engine

**The charge:** "I want the main engine to be driven by actors"

**What exists:** The old actor-systems.md is detailed. The current
skill says nothing about actors at all -- it is completely absent.

**Gap:** The skill needs to specify: the daemon's engine is
actor-driven; the actor library is kameo; the three-plane actor
topology (Signal/Nexus/Sema as actors); supervision is part of the
design; the actor discipline from actor-systems.md needs at least a
summary presence in the skill.

### 4C. Sema-first design

**The charge:** "sema being the database engine ... it's probably
not designed to my standard at all ... sema was way more important
than nexus"

**What exists:** The current skill says "each daemon owns its own
sema database." The old storage-and-wire.md describes the redb/rkyv
substrate. Neither addresses sema as the FIRST design concern.

**Gap:** The skill needs to establish sema as the primary design
surface: design the stored types first, then nexus operations
follow from what the database holds. Sema's importance over nexus
should be stated. The sema-engine pattern (kernel + library) needs
presence.

### 4D. Ethos-authored nexus and sema

**The charge:** "exposing nexus and sema as ... ethos authored
interfaces ... so that I could see what the main operations were
inside nexus ... and then the same thing with sema"

**What exists:** The old corpus used `.schema` files (the legacy
schema language). The current skill mentions nothing about HOW
the interfaces are authored.

**Gap:** The skill needs to state that nexus and sema interfaces
are authored in ethos, so:
- The daemon's internal feature catalog (nexus) is readable in
  ethos, not hidden in Rust code
- The database types (sema) are readable in ethos
- Ethos generates the Rust types (signalIsOurMessagingLayer.md
  2026-08-14: "The ethos generates the type in rust")

### 4E. Operational editing yields database migrations

**The charge:** "through the operational editing, we could have
database migration operations come out instantly or along with the
editing operation"

**What exists:** The old component-triad.md mentions sema migration
on database load (`mod previous -> mod next` bridge) but says
nothing about operational editing producing migrations.

**Gap:** This is a new architectural concept: when an ethos
interface change modifies a sema type, the editing operation
itself should produce the corresponding database migration
operation. This is the core advantage of sema-first
ethos-authored design -- the migration is not a separate manual
step. The skill needs to at least name this as the destination
shape.

### 4F. Schema explanation mechanism

**The charge:** "a schema explanation mechanism ... I could point at
a certain object and it would print out its schema in ethos syntax"

**What exists:** The old corpus had Help operations ("(Help Main)"
and "(Help (Verb <name>))") but those are CLI discovery, not schema
explanation. Nothing in the old or current skill describes pointing
at a runtime object and getting its ethos-syntax schema.

**Gap:** The skill needs to name this capability: any object in the
system can be asked to explain itself by printing its ethos type
definition. This is enabled by the ethos-authored types -- since
the types are authored in ethos, the ethos source is the
self-describing explanation. The CLI is the first surface; Mentci
(the UI) is the eventual surface.

### 4G. The ethos-monolith daemon

**The charge:** "the shortcut stack ... it's going to be a daemon
also ... the ethos monolith"

**What exists:** The current skill does not mention the ethos
monolith or the shortcut stack at all.

**Gap:** The skill needs to acknowledge that the ethos-monolith is a
component following the same daemon architecture -- it is itself a
triad (ethos-monolith + signal-ethos-monolith +
meta-signal-ethos-monolith). It compiles ethos to Rust directly
(no nomos/logos intermediate daemons in this shortcut form).

### 4H. The three forms (real/signal/textual) and their traits

**The charge:** Implicit in the trait-ontology and ethos-authoring
requirements.

**What exists:** The current skill mentions signal as "rkyv binary
archive" but does not name the three forms or their traits.

**Gap:** The skill should name:
- Real form: where values are born and changed (Rust types in memory)
- Signal form: the portable rkyv projection (what rides the wire)
- Textual form: the protos syntax (what humans and editors read)
- protos::Realize (text to real), protos::Textualize (real to text)
- "signal. signal. signal. that is what we call it" -- our name for
  the serialized form is signal, not "archive"

---

## 5. Open Questions Only the Psyche Can Rule

### 5A. How much actor detail enters the skill?

The old actor-systems.md was 752 lines. The psyche said the skill
should be "about the daemon, the signal wire format, the CLIs, the
wire type repos, the traits first, etc" and "under a thousand lines."
How much actor detail belongs in the rust-component-architecture
skill versus a separate skill? The psyche's charge says actors
drive the engine -- does that mean the skill should include the
three-plane actor topology, supervision, blocking discipline,
and the kameo specifics?

### 5B. Does the NexusAction step-loop survive?

The 5-variant NexusAction (ReplyToSignal, CommandSemaWrite,
CommandSemaRead, CommandEffect, Continue) is a concrete mechanism
from the old implementation. The psyche keeps the Signal/Nexus/SEMA
vocabulary and principles but says "we aren't tied to how they were
used and implemented in the past." Does the NexusAction loop
survive as the canonical engine mechanism, or is it subject to
redesign in the ethos-authored world?

### 5C. Does the ComponentDaemon trait survive?

The schema-emitted `ComponentDaemon` trait
(`spirit/src/schema/daemon.rs:80`) is the hook surface that makes
one-liner daemon mains possible. In the ethos-monolith world, this
trait would be ethos-generated rather than schema-rust-generated.
Does the shape survive even as the generator changes?

### 5D. Sema classification vocabulary: still six classes?

The six Sema classes (Assert, Mutate, Retract, Match, Subscribe,
Validate) are kept off the public wire but remain as internal
classification. Does this classification survive unchanged, or
does the sema-first redesign reconsider it?

### 5E. What belongs in the skill versus in ethos-authored interfaces?

The old skill corpus encoded detail that the psyche wants to see
in ethos: the nexus feature catalog, the sema stored types, the
signal interface. If these are authored in ethos and readable there,
does the skill need to describe their internal structure, or only
name the principle that they are ethos-authored?

### 5F. The kameo fork's standing versus upstream

The psyche asked to investigate whether the fork is falling behind
upstream and whether upstream changes make the fork unnecessary.
The fork has 6 commits ahead of upstream focused on lifecycle
control. This is a factual question the psyche wants answered,
not a skill-design question, but it bears on whether kameo
references in the skill should name the fork or upstream.

### 5G. Stream as a fourth section kind

The psyche has ruled stream is "a fourth kind (forest kind)" in
interface files (streamAsFourthKindMvpFirst.md). Stream components
are separate objects in their respective sections; the bundled form
is disqualified (streamDisqualifiesBundling.md). The observer
fixture with Tap/Untap naming is blessed
(observerFixtureBlessed.md). How much of this stream anatomy
enters the component architecture skill versus staying in
protos/ethos-specific skills?

### 5H. Input/Output/Refuse trait design

The psyche floated "Input Output Refuse, like Write and Read" and
alternatively "a shared Process trait" for the interface section
types (signalIsOurMessagingLayer.md 2026-08-14). Word choices are
explicitly open. Does this trait design enter the component
architecture skill, or does it live in a protos/ethos skill?
