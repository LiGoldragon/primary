# software-design

Design the machine before writing code: the map first, the
three-part machine everywhere, types before traits, capabilities on
their subjects, conversions as the spine, the Nexus as the runtime
shape, actors only where the world is concurrent.

## The want and the map

Everything is demand-driven. Name the wanted output; ask what it
needs; ask what that needs -- what we need to get what we need to get
what we want. The demand chain, read right to left, is the type list.

The first act of design is the world model -- an ontology, an anatomy,
a map of what is being created. Code comes after the map. A checklist
that catches bad code at the keyboard means the failure already
happened upstream, when code was written without the map.

The map is of the world, not the process. It holds what exists, what
each thing contains, and what each thing can do. Steps are walks
across the map, never things on it. Where a proposed type names a
process instead of a thing -- a Resolver, a Controller, a Manager --
the process is a walk across existing things, and the type does not
belong on the map.

Enumerate the types before asking what anything does. The types are
the things that exist; turn every logical aspect into a type.

> "we need to think very carefully of what the types are. First,
> really, because the traits are something that the types implement.
> We don't look for traits and then think of types for that."

Then list what each type contains, before any behavior. Containment
is not behavior: a table has entries; it does not do lookups. When
something is built from two things, the pair is usually a thing
itself, waiting for its name -- an assembly file and a registry make
a resolved assembly.

Write the core as if its coherent inputs already existed; then ask
what produces them.

The map's destination form is the Ethos interface file. Ethos is not
yet runnable; the map is written in it anyway. Writing what cannot
yet run is how the notation and the design pull each other forward.

## The machine

Every machine, at every scale, has the same three parts:

    agglomerate multiple types --> create a coherent type --> convert it onward

Diverse inputs are gathered; they become one coherent thing; the
coherent thing converts into the next. That is the whole shape.

**The shape is the law -- not any one spelling.** At program scale the
machine appears as a conversion between named types. Inside a method
it may be variables accumulating in the body until they become the
block that is handed on. Both are the machine. Do not force every
machine into one syntactic form.

**The machine is fractal.** Zoom into any arrow and find another
three-part machine. A compiler is machines all the way down; so is a
single emit method. The outer machine's coherent output stands as the
inner machine's coherent input. At the very bottom of the output
side, methods agglomerate parts of the assembled result into blocks
of string -- and even those blocks may be typed when we want to be
very correct: an `ImplString`, an `ImplSignatureString`, a
`VariableAssignmentString`.

**The executable's special case.** An operating system only accepts
bytes, so a program that writes files is forced to hold a
"pre-output" type -- the result assembled whole in memory before
anything is written. Read as machines: the pre-output type is the
output machine's coherent input, and the unix-sense output -- bytes
leaving the program -- is the innermost final part.

    AssemblyFile ┐
                 ├──> ResolvedAssembly ──> AssembledRust ──> bytes -> OS
    Registry ────┘    └── machine 1 ──┘   └─ machine 2 ─┘  └ output machine ┘

Emission from the coherent type is a simple operation, or at least
one reviewable all in one place, under one trait -- logic is not
sprawled over everywhere. The cost of violating this is documented in
a flagship compiler: GCC's code generator, lacking a self-contained
representation, "reaches back and walks the source level 'tree'
form" to emit debug info. LLVM states the cure as an invariant: the
IR is "the only interface to the optimizer." rustc states it for
MIR: "all of that logic is centralized in MIR construction, and the
later passes can just rely on that."

### Conversions

At program scale, the machines chain as conversions between named
types: From when it cannot fail, TryFrom when it can. From is
preferred: creation is demand-driven -- things are created from other
things; nobody harvests a material and then asks what it can become.

Multi-input creation is TryFrom on a named agglomerate -- a defined
type holding the inputs. Conversions consume their inputs by value:
no references held into them, no clones up the chain, so the inputs
drop when the conversion is done. Memory doubles only at clone.

A struct with several fields names its fields -- the multi-field
tuple struct is refused. The newtype is allowed: its single unnamed
field is technically a tuple form, the only one permitted.

Main is a few lines tying the spec together. The chain begins at the
input -- a strictly typed object coming in as a datom; nothing enters
untyped:

```rust
fn main() -> Result<()> {
    let input    = Input::try_from(datom)?;
    let registry = Registry::try_from(input.registry)?;
    let assembly = AssemblyFile::try_from(input.assembly)?;
    let resolved = ResolvedAssembly::try_from(/* agglomerate */)?;
    let rust     = AssembledRust::try_from(resolved)?;
    rust.write()
}
```

The input's type is the interface's root enum: a data enum whose
variants are the main operations, each variant's data its options.
Configuration comes from the datom's very shape, not from a flag
grammar or a derive.

Most programs hide this schema between the lines -- the objects are
implicit, smeared through procedure. State the schema as types, and
main becomes a table of contents:

> "most programs create the schema in the code instead of creating
> the schema and then just tying it up with a few lines."

The spine is a design target ahead of practice; no surveyed project
spells its top level this way.

The nearest living relatives: walrus runs the whole shape in three
lines (`Module::from_buffer(&bytes)?` -> transform typed fields ->
`emit_wasm()`); cargo chains resolve -> UnitGraph -> an immutable
BuildContext -> Compilation; the Elm compiler's `compile` is five
typed stage conversions ending in an `Artifacts` value assembled
before any file is touched; gleam and Dhall put the *stage itself*
in the type, so passing phase one into phase three -- or using an
unresolved import -- is a compile error, not a runtime check:

```haskell
load :: Expr Src Import -> IO (Expr Src Void)   -- resolved, provably
```

### Names

A name describes what a value is at the moment it exists -- not what
will happen to it. Rust assembled in memory but not yet written is
AssembledRust, not GeneratedRust: "if you need to still write it, it
hasn't been generated yet." The same law at every scale, down to an
ImplString that is exactly the impl block it holds.

## Traits

Every method call lives in a trait, because traits are the
comprehension surface -- the layer where concepts become visible and
implementations are constrained to think within them. An inherent
method is a trait not yet extracted -- a concept hiding in a name.

The trait pass comes before any body is written: traits are the
specification expressed in code.

The traits and types are designed as one ontology -- the most unified
map of traits and types -- before any body is written; a new need
first finds its place in that map.

Defaults are given wherever a default is expressible. Rich
requirement chains (sub-traits) are what make defaults possible --
designing them is the work.

When behavior's domain is clear, reuse the existing trait or extend
it. When neither an existing trait nor a clear new placement can be
found, stop and escalate -- do not proceed.

A port starts from the map of what is being created; old code is at
most inspiration for that map.

Exceptions are permitted -- too trivial, proper trait cannot be
determined, not worth the trouble -- but each exception is noted at
the site where it is taken.

### Capabilities on subjects

A capability is placed on the type that contains its subject. The
thing that carries the name is the thing that resolves. The text
realizes; the real textualizes.

**The costume-trait fingerprint.** A trait method that must be handed
its own subject as a parameter is a regular function wearing a trait:

> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

Strip the trait wrapper -- if a free function serves equally well,
the trait added nothing. Boundary: parameters that narrow or direct
an operation the receiver already owns -- a query span, a callback,
an event payload -- are legitimate. Creation is exempt: the created
thing does not exist yet, so its inputs arrive as parameters and are
consumed into it.

The positive model, in the wild -- serde. `Value` serializes itself
in one match, one arm per variant, nothing escaping the impl:

```rust
impl Serialize for Value {
    fn serialize<S: Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        match self { /* one arm per variant */ }
    }
}
```

**Direction pairs never share a type.** The textual type carries
Realize; the real type carries Textualize. "You dont textualize the
text, and you dont realize the realized data." If both directions sit
on one type, the implementation is wrong.

### Names and form

Action traits take the bare verb: Walk, Write, Read, Resolve,
Create. The qualifier reading stands -- a type implementing Walk is
capable of walking.

One type carrying many single-function traits is probably one trait
not yet seen. Placeholder traits for every function create no
sensible ontology.

Traits live on data-bearing types. A zero-sized type with behavior
is a namespace pretending to be a thing -- the verbs belong to a
real noun.

Identity is trait-borne: an encoded form fingerprints itself -- by
default, the hash of its rkyv archive -- and every reference names
its target by that encoded name, never by spelling.

What a trait consumes or yields is a named type; a tuple in a trait
signature is a struct not yet named.

A long parameter list is a type not yet named -- often the method's
missing owner.

### No free functions

`fn main()` is the only production free function. When no owning
type exists, the model is incomplete -- name the missing type instead
of writing a floating verb. A zero-sized type created only to
namespace free functions is the same disease -- find the missing
abstraction.

## The Nexus

The runtime shape of everything we design is a Nexus.

A Nexus is a daemon with at least two sockets, a default CLI client
per socket, and the signal contracts it is compiled with. The
decision-making engine inside it is Nexus Core. A Nexus is a vertex
in the graph of nexuses. An edge joins two vertices and carries one
contract: every connected pair has an ordinary edge; only some pairs
have a meta edge.

### Naming

`<nexus>` is the repo holding the daemon and its logic; its daemon
binary is `<nexus>-daemon`.

`signal-<nexus>` is the wire type repo: the typed vocabulary of the
Nexus's public wire surface.

`meta-signal-<nexus>` is the owner's wire type repo: policy and
configuration vocabulary. It is never optional -- configuration flows
through it.

The CLI binary is `<nexus>`; the meta CLI is `<nexus>-meta`.

### The daemon

Everything is in the daemon. It loads its domain and holds the whole
thing -- every object as its own specifically typed object, a specific
type for every kind. It thinks in typed values, never in text: no
text arrives on its wire and none leaves it.

Each daemon owns its own sema database -- its typed durable store,
reached only through the sema-engine library, in a `.sema` file.
There is no central storage daemon. Policy state and working state
live in that one store; policy changes only through meta-socket
mutation.

A daemon starts from a single argument: a signal-encoded Configure
message. A virgin daemon applies it as first configuration; a daemon
with a populated store resumes from its store. The same Configure
type is accepted live over the meta socket. With no configuration,
the daemon waits in an unconfigured semi-started state -- it does not
guess.

A Nexus speaks only the signal contracts it is compiled with: those
of its own sockets and of every edge it has.

### Signal -- the wire format

Signal is the messaging layer. A message is an rkyv binary archive --
typed, portable, validated on receive. Frames are length-prefixed on
the socket. Nothing else rides the wire: no JSON, no text, no second
protocol.

Every Nexus opens at least two sockets: the ordinary socket, for any
authenticated peer, and the meta socket, privileged -- the Nexus's
root: configuration and privileged operations pass only through it.
A Nexus needing more levels of access opens more sockets. Every
surface answers with typed replies, including a typed refusal --
errors are vocabulary, not strings.

The signal wire vocabulary is versioned by its contract crate: the
crate's semver is the wire's semver, and consumers pin it.

### The CLIs

The CLI's role is to transform text into Signal. It is the boundary
where the textual form ends and the binary world begins.

A CLI speaks to exactly one daemon -- its own. It opens no database,
reaches no other Nexus, and carries no logic worth keeping: it is
bootstrap machinery, kept thin; when production no longer uses it,
it remains for debugging and testing. `<nexus>` fronts the ordinary
socket; `<nexus>-meta` fronts the meta socket. Every client, on any
socket, speaks pure signal; textualizing is the client's work, not
the Nexus's.

Every Nexus process takes exactly one positional argument: a typed
input object in DOTOS/NOTA text or signal-encoded binary. No flags,
no subcommands, no other argument shapes -- the type system is the
only interface. Flag-style arguments (`--anything`) are rejected.
The daemon accepts only the signal-encoded form.

### The wire type repos

A wire type repo declares vocabulary and nothing else: no runtime,
no actors, no async machinery. It owns the frame envelope and its
encode/decode, the protocol version, a closed enum of request kinds
with their paired replies, and the typed payload of every operation.
No catch-all variants -- the vocabulary is closed.

Operations are verbs in verb form: `Submit`, not `Submission`.
Replies are the verb's past tense; rejections name themselves.
Storage classification vocabulary does not appear on the public
wire -- what a peer may ask is domain language, not database language.

Every record kind lands as a concrete text example with a round-trip
test before its type is final: the example is the falsifiable
specification.

### How nexuses fit together

Peers depend on each other's wire type repos, not on each other's
daemons. The contract is the whole relationship.

Observation flows up, authority flows down: state is observed through
push subscriptions -- a typed snapshot on open, typed deltas after --
and commanded through the owner's mutation vocabulary. Polling is
forbidden; a correct system goes quiet when nothing changes.

When one intent spans several nexuses, the issuer commits on the
first success and records divergence on failure -- no distributed
rollback, no all-or-nothing stall.

One capability, one Nexus. A Nexus is sized to be held whole in one
mind -- human or model; when it outgrows that, it splits.

## Libraries

What legitimately is not a Nexus.

**Substrate libraries** carry the representation layer: protos (the
schema language's data model) and datom (the typed record substrate)
define how data is shaped, not what it means in a domain.

**Trait libraries** hold shared capability vocabularies -- concept
repos defining traits that multiple nexuses implement. The traits
live here when the capability crosses Nexus boundaries.

**Wire vocabulary repos** -- `signal-<nexus>` and
`meta-signal-<nexus>` -- declare the typed wire surface. Their
anatomy is described under The Nexus.

**Engine libraries** encapsulate a domain engine used by nexuses:
sema-engine (the typed durable store) is the current example.

The dividing line: libraries carry vocabulary and substrate; runtime
authority lives only in a Nexus.

## Actors

An actor is a thing on the map, never a step. It earns its mailbox
by what it IS: a truly concurrent activity of the world, holding its
own mutable state, owning its own lifecycle, its own failure domain,
its own pacing. The traditions converge on these properties from
independent origins; a thing with none of them is not an actor.
Armstrong's mapping law:

> "Use one parallel process to model each truly concurrent activity
> in the real world. If the mapping is not 1:1 the program will
> quickly degenerate."

Not for code organization. The Elixir documentation -- a language's
own docs, not commentary -- states the boundary exactly:

> "A GenServer must never be used for code organization purposes.
> Use processes only to model runtime properties, such as mutable
> state, concurrency and failures, never for code organization."

**The conversion arrows are not actors.** The machine's arrows are
demand-driven and stateless; they have no lifecycle, no failure
domain, no pacing. An actor per pipeline stage is code organization
wearing concurrency. The machine lives inside the actor: the logic
is a pure state machine -- the sans-io school's rule -- and the actor
is its shell at the I/O boundary, where the world is actually
concurrent: an ingress, a session, a store serving concurrent
writers.

Read as a machine, the actor is the three-part shape continued: the
mailbox and the current state agglomerate; the handler creates the
next coherent state; replies and effects convert onward. The actor's
state is a coherent type; the handler is a conversion. An actor
named for a process -- a ResolverActor, a ManagerActor -- is the
service object with a mailbox.

The message vocabulary is a closed enum -- the actor's whole
interface. The compiler checks exhaustiveness; reading the enum
tells everything the actor can be asked. Effects are data the
runtime interprets, not side effects performed mid-handler.

The remaining conventions the traditions state independently, each
in its own vocabulary, none citing the others: no shared mutable
state; bounded mailboxes under the consumer's control; messages as
the only channel between actors; one thread of execution per actor;
topology a DAG, cycles deliberate and bounded; terminal states
irreversible; do not block the executor; effects as data.

**Supervision is drawn on the map.** Failure domains are map
artifacts: which things die together and who restarts whom is
designed with the ontology, before code. The agent evidence is
one-sided: left to invent, agents produce unsupervised spawns,
sleep-based synchronization, and happy paths -- "crappy OTP by
default"; handed the supervision shape and the message vocabulary,
they translate faithfully. Actors are the map law at its sharpest:
the topology is the design, and code is its translation.

Granularity is a runtime question, not taste. Two million processes
per server (WhatsApp) and grains in the trillions (Orleans) worked
because the runtime owned lifecycle and placement. Where the
developer owns lifecycle -- as with our kameo actors -- every actor is
hand-managed, and the count stays at the world's own concurrency:
one actor per truly concurrent thing, none for anything else.

## The diseases, named

Seen in respected production code; recognize them on sight.

- **The service object** -- a step wearing the clothes of a thing.
  bat's `Controller { config, assets }` with `.run()`: it holds
  collaborators and represents a process; nothing like it belongs on
  a map.
- **Sprawled emission** -- output logic scattered across methods and
  passes. bat's four `print_*` methods with no coherent output type;
  ruff's `check_path()` accumulating one mutable `Vec<Diagnostic>`
  across six independent checker passes; GCC reaching back into the
  source tree during emission.
- **The costume trait** -- `fn resolve(&self, name: ...)` on a lookup
  table. The subject in a parameter; the receiver a bystander.
- **Placeholder traits** -- a trait hat on every function,
  fragmenting one concept into many single-method traits.
- **The schema between the lines** -- an 80-line main of flag
  dispatch, where the types the program is really about do not appear.
- **The actor costume** -- a mailbox on a stateless step; code
  organization wearing concurrency. Armstrong's rule: "don't use
  processes and message passing when a function call can be used
  instead."
- **The ask chain** -- pipeline stages as actors chained by
  request/response: synchronous RPC dressed as concurrency, each ask
  dozens of times heavier than a plain tell, a timeout race at every
  link.
