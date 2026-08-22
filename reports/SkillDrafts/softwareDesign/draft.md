# software-design

Design the machine before writing its tissue: the map first, the
three-part machine everywhere, types before traits, capabilities on
their subjects, conversions as the spine, actors only where the
world is concurrent.

## The map comes first

The first act of design is the world model — an ontology, an anatomy,
an object-and-capabilities-oriented map of what is being created.
Code comes after the map. A checklist that catches bad code at the
keyboard means the failure already happened upstream, when code was
written without the map.

The map is of the world, not the process. It holds what exists, what
each thing contains, and what each thing can do. Steps are walks
across the map, never things on it. Where a proposed type names a
process instead of a thing — a Resolver, a Controller, a Manager —
the process is a walk across existing things, and the type does not
belong on the map.

The map's destination form is the Ethos interface file. Ethos is not
yet runnable; the map is written in it anyway. Writing what cannot
yet run is how the notation and the design pull each other forward.

## The three-part machine

Every machine, at every scale, has the same three parts:

    agglomerate multiple types --> create a coherent type --> convert it onward

Diverse inputs are gathered; they become one coherent thing; the
coherent thing converts into the next. That is the whole shape.

**The shape is the law — not any one spelling.** At program scale the
machine appears as a conversion between named types. Inside a method
it may be variables accumulating in the body until they become the
block that is handed on. Both are the machine. Do not force every
machine into one syntactic form.

**The machine is fractal.** Zoom into any arrow and find another
three-part machine. A compiler is machines all the way down; so is a
single emit method. The outer machine's coherent output stands as the
inner machine's coherent input. At the very bottom of the output
side, methods agglomerate parts of the assembled result into blocks
of string — and even those blocks may be typed when we want to be
very correct: an `ImplString`, an `ImplSignatureString`, a
`VariableAssignmentString`.

**The executable's special case.** An operating system only accepts
bytes, so a program that writes files is forced to hold a
"pre-output" type — the result assembled whole in memory before
anything is written. Read as machines: the pre-output type is the
output machine's coherent input, and the unix-sense output — bytes
leaving the program — is the innermost final part.

    AssemblyFile ┐
                 ├──> ResolvedAssembly ──> AssembledRust ──> bytes -> OS
    Registry ────┘    └── machine 1 ──┘   └─ machine 2 ─┘  └ output machine ┘

Emission from the coherent type is a simple operation, or at least
one reviewable all in one place, under one trait — never logic
sprawled over everywhere. The cost of violating this is documented in
a flagship compiler: GCC's code generator, lacking a self-contained
representation, "reaches back and walks the source level 'tree'
form" to emit debug info. LLVM states the cure as an invariant: the
IR is "the only interface to the optimizer." rustc states it for
MIR: "all of that logic is centralized in MIR construction, and the
later passes can just rely on that."

## Backwards from the want

Everything in the real world is demand-driven. We know what a machine
must produce before we know what produces it. So design runs
backwards: name the wanted output; ask what it needs; ask what *that*
needs — what we need to get what we need to get what we want. The
demand chain, read right to left, is the type list.

Write the core as if its coherent inputs already existed; then ask
what produces them.

## Types first; contents before behavior

Enumerate the types before asking what anything does. The types are
the things that exist; turn every logical aspect into a type.

> "we need to think very carefully of what the types are. First,
> really, because the traits are something that the types implement.
> We don't look for traits and then think of types for that."

Then list what each type contains, before any behavior. Containment
is not behavior: a table has entries; it does not do lookups. When
something is built from two things, the pair is usually a thing
itself, waiting for its name — an assembly file and a registry make
a resolved assembly.

The extreme of types-first, in production — the lexer of protox, a
pure-Rust protobuf compiler: one enum of 22 variants, every variant
carrying its matching rule, the derive generating the lexer state
machine from the type's shape:

```rust
#[derive(Debug, Clone, Logos, PartialEq, Eq)]
#[logos(skip r"[\t\v\f\r ]+")]
pub(crate) enum Token<'a> {
    #[regex("[A-Za-z_][A-Za-z0-9_]*")]
    Ident(&'a str),
    #[regex("[1-9][0-9]*", |lex| int(lex, 10, 0))]
    IntLiteral(u64),
    #[regex(r#"'|""#, string)]
    StringLiteral(Cow<'a, [u8]>),
    #[token("=")]  Equals,
    #[token(";")]  Semicolon,
    // [trimmed: 22 variants in all, every one attributed;
    //  IntLiteral carries four radix patterns]
}
```

The type's honest reach: the enum holds the token vocabulary and its
match rules, and the derive builds the recognizer from them; the
callbacks (`int`, `string`) construct the carried values and
continue where the pattern language stops — a string is lexed by its
callback from the opening quote on.

## Capabilities sit on their subjects

A trait is a capability a type has. Every method call lives under a
trait, because traits are the comprehension surface — the layer where
concepts become visible and implementations are constrained to think
within them.

A capability is placed on the type that contains its subject. The
thing that carries the name is the thing that resolves. The text
realizes; the real textualizes.

**The costume-trait fingerprint.** A trait method that must be handed
its own subject as a parameter is a regular function wearing a trait:

> "if the type needs a 'name' to resove the import, then it's not
> resolvable."

Strip the trait wrapper — if a free function serves equally well,
the trait added nothing. Boundary: parameters that narrow or direct
an operation the receiver already owns — a query span, a callback,
an event payload — are legitimate. Creation is exempt: the created
thing does not exist yet, so its inputs arrive as parameters and are
consumed into it.

The positive model, in the wild — syn and serde. `File` declares its
own parseability; no parser service exists. `Value` serializes itself
in one match, one arm per variant, nothing escaping the impl:

```rust
impl Parse for File { fn parse(input: ParseStream) -> Result<Self> { … } }

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

**Fragmentation is failure.** One type carrying many single-function
traits is probably one trait not yet seen. Placeholder traits for
every function create no sensible ontology.

**Names.** Action traits take the bare verb: Walk, Write, Read,
Resolve, Create. The qualifier reading stands — a type implementing
Walk is capable of walking.

## The spine is conversions

At program scale, the machines chain as conversions between named
types: From when it cannot fail, TryFrom when it can — never Into.
From is right because creation is demand-driven: things are created
*from* other things; nobody harvests a material and then asks what it
can become.

Multi-input creation is TryFrom on a tuple —
`TryFrom<(Registry, AssemblyFile)>` — one type parameter holding the
agglomeration. Conversions consume their inputs by value: no
references held into them, no clones up the chain, so the inputs drop
when the conversion is done. Memory doubles only at clone.

Main is a few lines tying the spec together:

```rust
fn main() -> Result<()> {
    let registry = Registry::try_from(registry_path)?;
    let assembly = AssemblyFile::try_from(assembly_path)?;
    let resolved = ResolvedAssembly::try_from((registry, assembly))?;
    let rust     = AssembledRust::try_from(resolved)?;
    rust.write()
}
```

Most programs hide this schema between the lines — the objects are
implicit, smeared through procedure. State the schema as types, and
main becomes a table of contents:

> "most programs create the schema in the code instead of creating
> the schema and then just tying it up with a few lines."

The spine is a design target ahead of practice; no surveyed project
spells its top level this way.

The nearest living relatives: walrus runs the whole shape in three
lines (`Module::from_buffer(&bytes)?` → transform typed fields →
`emit_wasm()`); cargo chains resolve → UnitGraph → an immutable
BuildContext → Compilation; the Elm compiler's `compile` is five
typed stage conversions ending in an `Artifacts` value assembled
before any file is touched; gleam and Dhall put the *stage itself*
in the type, so passing phase one into phase three — or using an
unresolved import — is a compile error, not a runtime check:

```haskell
load :: Expr Src Import -> IO (Expr Src Void)   -- resolved, provably
```

## Actors mark the world's concurrency

An actor is a thing on the map, never a step. It earns its mailbox
by what it IS: a truly concurrent activity of the world, holding its
own mutable state, owning its own lifecycle, its own failure domain,
its own pacing. The traditions converge on these properties from
independent origins; a thing with none of them is not an actor.
Armstrong's mapping law:

> "Use one parallel process to model each truly concurrent activity
> in the real world. If the mapping is not 1:1 the program will
> quickly degenerate."

Never for code organization. The Elixir documentation — a language's
own docs, not commentary — states the boundary exactly:

> "A GenServer must never be used for code organization purposes.
> Use processes only to model runtime properties, such as mutable
> state, concurrency and failures, never for code organization."

**The conversion arrows are never actors.** The machine's arrows are
demand-driven and stateless; they have no lifecycle, no failure
domain, no pacing. An actor per pipeline stage is code organization
wearing concurrency. The machine lives inside the actor: the logic
is a pure state machine — the sans-io school's rule — and the actor
is its shell at the I/O boundary, where the world is actually
concurrent: an ingress, a session, a store serving concurrent
writers.

Read as a machine, the actor is the three-part shape continued: the
mailbox and the current state agglomerate; the handler creates the
next coherent state; replies and effects convert onward. The actor's
state is a coherent type; the handler is a conversion. An actor
named for a process — a ResolverActor, a ManagerActor — is the
service object with a mailbox.

The message vocabulary is a closed enum — the actor's whole
interface. The compiler checks exhaustiveness; reading the enum
tells everything the actor can be asked. Effects are data the
runtime interprets, never side effects performed mid-handler.

The remaining conventions the traditions state independently, each
in its own vocabulary, none citing the others: no shared mutable
state; bounded mailboxes under the consumer's control; messages as
the only channel between actors; one thread of execution per actor;
topology a DAG, cycles deliberate and bounded; terminal states
irreversible; never block the executor; effects as data.

**Supervision is drawn on the map.** Failure domains are map
artifacts: which things die together and who restarts whom is
designed with the ontology, before code. The agent evidence is
one-sided: left to invent, agents produce unsupervised spawns,
sleep-based synchronization, and happy paths — "crappy OTP by
default"; handed the supervision shape and the message vocabulary,
they translate faithfully. Actors are the map law at its sharpest:
the topology is the design, and code is its translation.

Granularity is a runtime question, not taste. Two million processes
per server (WhatsApp) and grains in the trillions (Orleans) worked
because the runtime owned lifecycle and placement. Where the
developer owns lifecycle — as with our kameo actors — every actor is
hand-managed, and the count stays at the world's own concurrency:
one actor per truly concurrent thing, none for anything else.

## Names tell the truth

A name describes what a value IS at the moment it exists — not what
will happen to it. Rust assembled in memory but not yet written is
AssembledRust, not GeneratedRust: "if you need to still write it, it
hasn't been generated yet." The same law at every scale, down to an
ImplString that is exactly the impl block it holds.

## The diseases, named

Seen in respected production code; recognize them on sight.

- **The service object** — a step wearing the clothes of a thing.
  bat's `Controller { config, assets }` with `.run()`: it holds
  collaborators and represents a process; nothing like it belongs on
  a map.
- **Sprawled emission** — output logic scattered across methods and
  passes. bat's four `print_*` methods with no coherent output type;
  ruff's `check_path()` accumulating one mutable `Vec<Diagnostic>`
  across six independent checker passes; GCC reaching back into the
  source tree during emission.
- **The costume trait** — `fn resolve(&self, name: …)` on a lookup
  table. The subject in a parameter; the receiver a bystander.
- **Placeholder traits** — a trait hat on every function,
  fragmenting one concept into many single-method traits.
- **The schema between the lines** — an 80-line main of flag
  dispatch, where the types the program is really about never appear.
- **The actor costume** — a mailbox on a stateless step; code
  organization wearing concurrency. Armstrong's rule: "don't use
  processes and message passing when a function call can be used
  instead."
- **The ask chain** — pipeline stages as actors chained by
  request/response: synchronous RPC dressed as concurrency, each ask
  dozens of times heavier than a plain tell, a timeout race at every
  link.

## The worked ground

The import-resolution world map
(design/ProtosEngine/importResolutionWorldMap-2026-08-21.md) is the
protocol's first full exercise: the things and their contents drawn
first, one capability placed by the law, resolution as a walk,
the rejected Resolver as the recorded counter-example.
