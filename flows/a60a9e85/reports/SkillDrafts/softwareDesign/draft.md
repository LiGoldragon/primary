---
description: Software is being designed, built, or changed — including daemons, libraries, and their trait ontologies.
dependencies: []
---

## The want and the map

Design works backwards from the want. The end result is known first;
what it needs is asked; that yields the types. Everything is
demand-driven.

> "we know what's going to come out of it. So we can work backwards
> from what we want into, okay, so what are the things that this is
> going to need in order to create that, and then we have our types."

Before code, a map. The map is the object/capability-oriented layout
of what is being created — the ontology, the anatomy.

> "I think training the model to catch themselves before creating a
> fake trait means we have already failed; the model is trying to
> write code before it has a *model of the world*. could we say this
> is about building ontology, anatomy .. a *map* of what we are
> creating as an object/capability-oriented layout?"

The map is the Ethos interface file. Ethos is not ready yet, so the
model writes the Ethos it cannot run.

> "yes, except that it isnt ready to use yet, so the model writes
> the ethos but has no way to run it (yet)."

"The map" stands as a noted naming debt — broad and overloaded, but
fine for now.

Types are enumerated first, because traits are what types implement.

> "we need to think very carefully of what the types are. First,
> really, because the traits are something that the types implement.
> We don't look for traits and then think of types for that."

Every logical aspect becomes a type. A type is a thing that exists
on the map; its contents are designed before its behavior.

[OPEN — choice 2: "contents before behavior" as an explicit design
step is inferred from the worked example. The psyche stated
types-first; whether contents-before-behavior is its own step or
part of what types-first already means is unruled.]

The map shows things that exist. A process — resolving, controlling,
managing — is movement across the map's things. A type on the map
names a thing, an object, a subject; the walk it undergoes is
behavior, carried by traits.

[OPEN — choice 1: "steps are walks across the map" and the
formulation of process-named types as walks are agent coinages from
the import-resolution world map. The underlying doctrine — the map
is objects/capabilities and a type names a thing — is
psyche-sourced. The specific metaphor is unruled.]

Vocabulary drives the code design, and the implemented code drives
the vocabulary. Code is language.

> "the vocabulary drives the code design, and the implemented code
> must drive the vocabulary. code is language."

The minimum amount of code for the most elegant machinery — easily
understood by an engineer, easily extended, easily introspected — is
the best shape.

> "The minimum amount of code for the most elegant machinery, which
> can be easily understood by an engineer and easily extended and
> easily introspected, is the best shape."

A name is true of what exists at the moment it names. The value that
has been gathered and structured is assembled.

> "I wouldn't call it generated Rust because if you need to still
> write it, it hasn't been generated yet. So it would be more like
> assembled Rust."

A port starts from the map of what is being created; old code is at
most inspiration for that map.


## The machine

A machine has three parts: agglomerate multiple types, create a
coherent type, convert it to another type.

> "agglomerate multiple types -> create a coherent type -> convert
> it to another type"

The principle extends through every part of the design. Each part is
itself a three-part machine; the outer machine's coherent output is
the next machine's coherent input.

> "this principle can be extended to be used in every part of our
> software design. We could even think of the output in the same
> way (considering the 'output' its own 3 part machine)"

At the OS boundary, the executable forces a pre-output type, making
the visible shape appear as four parts; the general nature is the
three-part form.

The machine is not one form. At program scale it is a trait
conversion. At method scale it may be variables accumulating in a
body. String blocks assembled by methods may themselves carry a type
(ImplString, VariableAssignmentString) where correctness warrants it.

> "thats just one form of it. the machine might be accumulating
> variables in a method's body. Im not investing into a single
> form like this."

From and TryFrom are the conversion spelling. Creation is
demand-driven — from other things. The end result is named first
and asked what it comes from.

> "I think the From is better than Into, since in reality, we need
> to create things *from* other things; nobody harvests a material
> and then asks what this can be made into; everything is
> demand-driven."

TryFrom is preferred where it allows thinking about the end result
first. From where the conversion is infallible. A thing built from
two things gets a named type carrying both — the registry and the
assembly file make a ResolvedAssembly.

Main is a few clear lines. The knowledge lives in the types — a
spec, a fully compliant data tree that yields the whole program. The
code between types is conversions.

> "most programmers, most programs I guess you could say, create the
> schema in the code instead of creating the schema and then just
> tying it up with a few lines."

The chain begins at the input: a typed object arriving as datom.

> "I dont see the arg input. where is datom coming from?"

[OPEN — choice 9: the input type's name and the datom's carrier
(how the datom reaches main) are undesigned. The quoted sentence is
the psyche's actual typed words; the "strictly typed object coming
in as datom" phrasing in mainFunction.md is agent-constructed.]

### The worked example

```rust
fn main() -> Result<()> {
    let input    = Input::try_from(datom)?;
    let registry = Registry::try_from(input.registry)?;
    let assembly = AssemblyFile::try_from(input.assembly)?;
    let resolved = ResolvedAssembly::try_from((registry, assembly))?;
    let rust     = AssembledRust::try_from(resolved)?;
    rust.write()
}
```

Type names are sourced: Registry and AssemblyFile (assembly.md
2026-08-21), ResolvedAssembly as the assembled source, AssembledRust
as the coherent output before writing.

[OPEN — choice 5: `rust.write()` is a placeholder; the output
step's form (inherent method, Write trait, conversion to OS bytes)
is undesigned.]

[OPEN — choice 9: `Input` and `datom` are placeholders; the input
type's name and the datom's carrier are undesigned.]

[OPEN — the agglomerate line uses a tuple `(registry, assembly)` per
the dissolved Create-trait context; a named type carrying both is
consistent with the named-type guidance in the traits section.]


## Traits

Every method call in Rust code lives under a trait. Traits are the
comprehension surface — the layer where concepts become visible and
implementations are constrained to think within them.

> "Every method call in our Rust code lives under a trait, because
> traits are the comprehension surface — the layer where concepts
> become visible and implementations are constrained to think within
> them."

Rust is the new assembly language. Traits and main types are what
the psyche reads; everything else is implementation detail that
Ethos will eventually generate.

`fn main()` is the only production free function. When no owning
type exists, the model is incomplete — name the missing type.

> "I even want to make the broad statement that I want *all* method
> calls in our rust code to be part of a trait"

On greenfield, a new need requires a new trait or extends an
existing one. Extraction is for porting existing code to
mandatory-trait standard.

> "on a greenfield we wouldnt extract; a new need would require a
> new trait (or extending an existing one if that looks more
> appropriate. Extraction would be for porting existing code to
> mandatory-trait standard"

An inherent method is a trait not yet extracted — a concept hiding
in a name. Traits live on data-bearing types. A zero-sized type with
behavior is a namespace pretending to be a thing — the verbs belong
to a real noun.

Action traits take the infinitive verb form: Walk, Write, Read,
Resolve.

> "we would use the sort of infinitive form of the word, of the
> verb, I mean. If it's an action that can be purely described as
> an action, like write, read, resolve, create."

Commonality is the abstraction test. The more common traits across
types, the richer the abstraction.

> "if we take all the common behavior, we want to have as many
> common traits as possible, because then we're creating the right
> abstraction."

Module placement resolves ambiguity. A trait qualified by its module
is self-describing — protos::Textualize names the protos
textualization. Elaborate capability names are welcome where
specificity needs them.

### Trait placement

A capability belongs to the type that contains its subject. The type
that carries the name is the thing that resolves. The text realizes;
the real textualizes.

> "realize isnt implemented by the same type as textualize. if you
> cant find two different types, the implementation is wrong. You
> dont textualize the text, and you dont realize the realized data."

[OPEN — choice 3: the positive formulation "a capability is placed
on the type that contains its subject" is the agent's
generalization. The psyche's stated form is the diagnostic: "if
the type needs a 'name' to resove the import, then it's not
resolvable."]

A trait method's subject is its receiver; the type carrying the
subject is where the capability belongs.

[OPEN — choice 4: the honest boundary (parameters that narrow or
direct an existing capability — spans, callbacks, payloads — are
legitimate) and the creation exemption (the created thing does not
exist yet, so inputs arrive as parameters) are agent-derived from
research, unruled by the psyche.]

### Generic parameters

Every generic parameter names a real trait — the mandatory trait is
the answer to what T is.

> "the answer is the mandatory trait! so T would be a trait!"

### Named types

Every parameter and return in a trait signature is a named type.
Named types carry the design; they describe what the value is. The
newtype is the one tuple form this acknowledges — mentioned because
it technically is a tuple.

> "the newtype is allowed. the fact that its a tuple is unfortunate
> for us, so it would have to be mentionned in case."

Multi-field positional structs are not required by any standard
trait or pattern. Where a standard trait's type parameter calls for
compound data, a named type serves.

[OPEN — the consolidated tuple rule set was presented for approval
but the conversation moved to the merge ruling. What stands as
ruled: the newtype is allowed and must be mentioned. The full scope
— extension beyond trait signatures, standard-trait interactions,
body-level idioms — was discussed and answered but the answers were
not ruled. The psyche's characterization of tuples is in the
diseases section.]

### The trait pass

The traits and types are designed as one ontology — the most unified
map — before any body is written. A new need first finds its place
in that map. One type implementing many single-function traits is
one trait not yet seen.

> "this is good. deploy it"

Trait/types design is ontology in code.

> "trait/types design is ontology in code."

Defaults are given wherever a default is expressible. Rich
requirement chains (sub-traits) are what make defaults possible —
designing them is the work.

When behavior's domain is clear, reuse the existing trait or extend
it. When neither an existing trait nor a clear new placement can be
found, stop and escalate.

Exceptions are permitted — too trivial, proper trait cannot be
determined — but each exception is noted at the site where it is
taken.

Identity is trait-borne: the encoded form fingerprints itself — by
default, the hash of its rkyv archive — and every reference names
its target by that encoded name.

[OPEN — vocabulary: this is the approved nexus-skill text, but
"code/encoded" was dropped as form vocabulary ("ok, working form
and signal form, drop code/encoded entirely"); whether the drop
reaches the EncodedName lineage is listed as a consequence to
confirm, not yet ruled (encodedFormIsTheCode.md 2026-08-13).]


## The Nexus

Everything built takes the shape of a Nexus. A Nexus is a daemon
with at least two sockets, a default CLI client per socket, and the
signal contracts it is compiled with. Anything already built that
did not take this shape is rewritten.

> "everything we're going to build is going to be a nexus now, and
> anything that has already been built that did not take the shape of
> The nexus is going to be rewritten."

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract: every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

The decision-making engine inside the Nexus is Nexus Core.

One capability, one Nexus. A Nexus is sized to be held whole in one
mind — human or model; when it outgrows that, it splits.

### The daemon

Everything is in the daemon. It loads its domain and holds the whole
thing — every object as its own specifically typed object, a
specific type for every kind. It thinks in typed values.

Each daemon owns its own sema database — its typed durable store,
reached only through the sema-engine library, in a `.sema` file.
Policy state and working state live in that one store; policy
changes only through meta-socket mutation.

A daemon starts from a single argument: a signal-encoded Configure
message. A virgin daemon applies it as first configuration; a
daemon with a populated store resumes from its store. The same
Configure type is accepted live over the meta socket. With no
configuration, the daemon waits in an unconfigured semi-started
state — it never guesses.

### Signal — the wire format

Signal is the messaging layer. A message is an rkyv binary archive —
typed, portable, validated on receive. Frames are length-prefixed on
the socket. Signal is fully typed; both sides know the full schema.

> "signal is fully typed; both sides know the full schema."

Three forms of a type: textual (for editors, humans, LLMs), working
(in-memory, where values are born and changed), and signal (portable
rkyv, the wire form).

> "ok, working form and signal form, drop code/encoded entirely"

Every Nexus speaks only the signal contracts it is compiled with:
those of its own sockets and of every edge it has. Textualizing is
the client's work, never the Nexus's.

> "the Nexus component cannot be involved in texturalizing signal,
> because it would just destroy the beauty and the simplicity of the
> system."

Every Nexus opens at least two sockets: the ordinary socket for any
authenticated peer, and the meta socket, privileged — the Nexus's
root: configuration and privileged operations pass only through it.
The meta-signal repo is required — configuration flows through it.
A Nexus needing more levels of access opens more sockets.

> "the metasignal is not optional because otherwise there's no way
> to configure the daemon."

> "we should say *at least* two sockets. some nexus might need more
> than 2 levels of access."

Every surface answers with typed replies, including a typed
refusal — errors are vocabulary.

The signal wire vocabulary is versioned by its contract crate: the
crate's semver is the wire's semver, and consumers pin it.

### The CLIs

The CLI's role is to transform text into Signal. It is the boundary
where the textual form ends and the binary world begins.

A CLI speaks to exactly one daemon — its own. It is bootstrap
machinery, kept thin; when production no longer uses it, it remains
for debugging and testing. `<nexus>` fronts the ordinary socket;
`<nexus>-meta` fronts the meta socket.

> "the cli is for bootstrap and later on can be used for debugging
> and testing even after it isnt used in production anymore"

Every Nexus process takes exactly one positional argument: a typed
input object in DOTOS/NOTA text or signal-encoded binary. The type
system is the only interface. The daemon accepts only the
signal-encoded form.

> "CLIs cannot accept any other type of argument than the typed
> input object."

Datom creates configuration options by its very shape — a data enum
at the root with options in its data.

> "datom creates configuration options by its very shape, as the
> ethos interface shows; a data enum at the root (main operation)
> with options in its data"

### The wire type repos

A wire type repo is pure vocabulary. It owns the frame envelope and
its encode/decode, the protocol version, a closed enum of request
kinds with their paired replies, and the typed payload of every
operation. The vocabulary is closed — every variant is named.

Operations are verbs in verb form: `Submit`, not `Submission`.
Replies are the verb's past tense; rejections name themselves.

Storage classification vocabulary never appears on the public
wire — what a peer may ask is domain language.

Every record kind lands as a concrete text example with a round-trip
test before its type is final: the example is the falsifiable
specification.

### Naming

`<nexus>` is the repo holding the daemon and its logic; its daemon
binary is `<nexus>-daemon`.

`signal-<nexus>` is the wire type repo: the typed vocabulary of the
Nexus's public wire surface.

`meta-signal-<nexus>` is the owner's wire type repo: policy and
configuration vocabulary. It is required — configuration flows
through it.

The CLI binary is `<nexus>`; the meta CLI is `<nexus>-meta`.

Three repos per component, plus reusable libraries for shared
traits.

> "ethos can have all the code, minus the two signal repos, and so
> on (3 repos per component). other than reusable libraries of
> course, which we want to encourage for shared traits especially."

### How nexuses fit together

Peers depend on each other's wire type repos, never on each other's
daemons. The contract is the whole relationship.

Observation flows up, authority flows down: state is observed through
push subscriptions — a typed snapshot on open, typed deltas after —
and commanded through the owner's mutation vocabulary. A correct
system goes quiet when nothing changes.

When one intent spans several nexuses, the issuer commits on the
first success and records divergence on failure.


## Libraries

The Nexus is the runtime shape; libraries serve it. The psyche named
two kinds and invited the flow to name others; four are proposed:

**Substrate** — the shared structural primitive. Datom and Protos:
typed, positional, dense. Datom carries data only, strictly typed.
Ethos depends on datom; they share an approach but are different
languages with a shared substrate of traits and types.

> "datom doesnt do generics, it only carries data, like json (but
> strictly typed of course)"

The two main syntaxes most agents face: one specifies the types,
the other fills them with data.

> "the two main syntaxes most agents will face; one specifies the
> types, the other fills them with data"

**Trait-concept** — shared capabilities in their own repos. Every
concept has its repo; every concept has at least one trait, and
probably more.

> "every concept should really have its repo, and if anything goes
> in there, the traits can, since every concept deserves at least
> one trait, and probably more."

**Wire vocabulary** — the signal contract crates
(`signal-<nexus>`, `meta-signal-<nexus>`). Pure typed conversation;
carries no logic.

**Engine** — a functional core consumed by daemons. sema-engine is
the archetype: the typed durable store, reached by the daemon
through the library, held in the daemon's own `.sema` file. Sema is
the database engine — its trait surface and ethos interface are the
next design frontier.

> "sema being the database engine... you could say sema was way more
> important than nexus"

[OPEN — the four-kind enumeration is the flow's proposal. The psyche
named substrate (datom) and trait-concept ("trait libraries"); wire
vocabulary and engine are the flow's additions.]


## Actors

Actors are confirmed in the Nexus. Standards of use are undesigned;
a dedicated flow is wanted. Prior work is distrusted.

> "re actors: we are definitely using kameo actors in nexus. I just
> havent designed the standards of use"

> "I want to dedicate a flow to the actor question. Everything was
> done by previous flows that received little to no guidance on
> design in this respect. Distrust it all, including our fork."

[OPEN — the entire actors section below is agent synthesis from
sourced research, presented for ruling. The psyche has confirmed
actors and kameo, distrusted all prior implementation, and requested
a dedicated flow.]

An actor is a thing on the map. It earns its mailbox by what it IS:
a truly concurrent activity of the world, holding its own mutable
state, owning its own lifecycle, its own failure domain, its own
pacing.

[OPEN — choice 6: the earning-properties list (five properties) is
agent synthesis from convergent literature (Hewitt, Agha, De Koster,
Akka, Orleans, Armstrong); assembled as a single list by no source.
A sixth property (distribution/location transparency) was left out
as not yet load-bearing.]

Read as a machine, the actor is the three-part shape continued: the
mailbox and the current state agglomerate; the handler creates the
next coherent state; replies and effects convert onward. The actor's
state is a coherent type; the handler is a conversion.

[OPEN — choice 7: the actor-as-machine reading is agent synthesis,
explicitly deferred to the psyche.]

The machine lives inside the actor: the logic is a pure state
machine; the actor is its shell at the I/O boundary, where the
world is actually concurrent — an ingress, a session, a store
serving concurrent writers.

[OPEN — choice 7: the machine-inside-the-actor position and the
sans-io framing are sourced from practitioner literature and the
Elixir documentation; the psyche has not ruled.]

Supervision is drawn on the map. Failure domains are map artifacts:
which things die together and who restarts whom is designed with the
ontology, before code.

[OPEN — choice 8: supervision-on-the-map follows from
map-before-code; its application to actors specifically is agent
synthesis. The evidence that agents translate faithfully when given
the supervision shape rests on practitioner reports only.]


## Diseases

Three conditions the psyche has diagnosed. Each negative here traces
to the psyche's own confident characterization; the provenance
appendix carries the verbatim source.

**Code before the model.** Writing code before having a model of
the world means the design has already failed. The map is the
remedy.

**Functions pretending to be traits.** A trait method whose subject
arrives as a parameter is a regular function wearing a trait — the
receiver is not the thing with the capability. This is a cornerstone
of models not understanding the vision.

**Tuples as un-specification.** A tuple is a form of
un-specification. Named types carry the design; unnamed positions
carry nothing.


## Provenance of retained negatives

Every negative — a "never", a confident prohibition, or a
psyche-worded diagnosis — is listed here with the psyche's verbatim
words licensing it and the source path.

| Line in draft | Psyche's verbatim words | Source |
|---|---|---|
| "it never guesses" (The daemon) | Approved as deployed nexus skill text. Psyche: "this is good. deploy it" | flows/e06e4c07/vision/nexus.md:204; deployed nexus skill SKILL.md:34 |
| "Textualizing is the client's work, never the Nexus's" (Signal) | "the Nexus component cannot be involved in texturalizing signal, because it would just destroy the beauty and the simplicity of the system. So all Nexus components speak only pure signal" | flows/e06e4c07/vision/nexus.md:62; deployed nexus skill SKILL.md:61 |
| "Storage classification vocabulary never appears on the public wire" (Wire type repos) | Approved as deployed nexus skill text. Psyche: "this is good. deploy it" | flows/e06e4c07/vision/nexus.md:204; deployed nexus skill SKILL.md:79 |
| "Peers depend on each other's wire type repos, never on each other's daemons" (How nexuses fit together) | Approved as deployed nexus skill text. Psyche: "this is good. deploy it" | flows/e06e4c07/vision/nexus.md:204; deployed nexus skill SKILL.md:126 |
| "the design has already failed" (Diseases) | "I think training the model to catch themselves before creating a fake trait means we have already failed; the model is trying to write code before it has a *model of the world*." | psyche-raw/Vision/worldModelBeforeCode.md 2026-08-20 |
| "functions pretending to be traits" / "cornerstone of models not understanding the vision" (Diseases) | "your trait methods are just regular functions pretending to be traits... So we found one of the cornerstone of models not understand my vision." | psyche-raw/Vision/traitsAsCapabilities.md 2026-08-20 |
| "A tuple is a form of un-specification" (Diseases) | "I really dont like tuples, they're a form of un-specification" | flows/cff271af/vision/tuples.md 2026-08-22 |
