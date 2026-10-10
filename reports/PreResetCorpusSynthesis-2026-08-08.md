# Pre-Reset Corpus Synthesis

*Assembled from the 2026-06-07 documentation corpus: 66 files under
`skills/` (including `rust/` subdirectory) and `ESSENCE.md` -- 24,397
lines total. Every teaching stated once; every source cited.*

---

## I. Foundational Principles

### What is being built

Software that is "eventually impossible to improve" -- in a bounded
domain, the right shape, chosen carefully, observed cleanly. The
priority stack, when two conflict the earlier wins (ESSENCE.md):

1. **Clarity** -- "the design reads cleanly to a careful reader. The
   structure of the system is the documentation of itself."
2. **Correctness** -- "every typed boundary names exactly what flows
   through it; nothing accidental survives the type system."
3. **Introspection** -- "the system reveals itself to those building
   it. State is visible; derived values do not hide."
4. **Beauty** -- "not pretty, but right. Ugliness is evidence the
   underlying problem is unsolved."

This priority stack is the workspace's universal progression. Every
role applies it to its own surface: the designer to structure, the
operator to code, the poet to prose (designer.md, operator.md,
poet.md).

What is NOT being optimized for: speed, feature volume, "minimum
viable," "ship fast," "iterate later," "time to market." Not backward
compatibility for systems being born. Not estimates -- "work is
described by *what it requires*, not by *how long it will take*"
(ESSENCE.md).

### Beauty as the criterion

> "If it isn't beautiful, it isn't done." (ESSENCE.md, beauty.md)

Beauty is "a gate alongside correctness, not a nice-to-have" (beauty.md).
Ugliness signals: a name that does not read as English, a `pub` field
on a wrapper newtype, a free function that should be a method, dead
code retained "for safety," special cases stacked on the normal case,
stringly-typed dispatch, a doc comment that explains what the code does,
a boolean parameter at a call site, a name for what something is not
(beauty.md). "If you cannot make it beautiful, you do not understand it
yet" (ESSENCE.md).

Audits apply beauty as the primary lens: "Before asking 'does this
work?' the audit asks 'is the shape right?'" (beauty.md). Four audit
scales: code beauty, capture discipline, report retention, substrate
cleanliness.

### The type system is the model

This doctrine recurs across nearly every architectural file. "Every
typed boundary names exactly what flows through it" (ESSENCE.md). Data
is typed end-to-end; strings exist only at user-facing edges
(ESSENCE.md). The two edges: the daemon edge (binary signal-frame
frames, never NOTA text) and the trace edge (typed objects and typed
events, never ad hoc string logs).

Boolean flags, stringly-typed dispatch, sentinel values, opaque strings,
and `Unknown` variants all violate this principle (typed-records-over-flags.md,
enum-contact-points.md, language-design.md, contract-repo.md, methods.md).

### Naming discipline

Two rules, applied as a pair (ESSENCE.md, naming.md):

1. **Spell every identifier as a full English word.** `Request` not
   `Req`. `Identifier` not `Id`. `Configuration` not `Cfg`. Only
   acronyms that have fully passed into general English (`CPU`) qualify;
   convenience shortenings (`ctx`, `cfg`, `addr`, `db`) do not.

2. **Names don't carry their full ancestry.** A type belongs to its
   surrounding namespace; repeating the namespace in the name is
   redundant ceremony. Inside `signal-persona-spirit`, the type is
   `Entry`, not `IntentEntry`. Inside a `Profile` struct, the field
   is `size`, not `profileSize`. *"If I held the name of all my
   ancestors, I would be speaking until I die before I could spell my
   name out"* (ESSENCE.md).

Six permitted exceptions: loop counters in tight scopes (<10 lines),
mathematical contexts, generic type parameters (`T`, `U`), acronyms
that have become English words, names inherited from `std` or
well-known libraries, domain-standard short names documented in
ARCHITECTURE.md (naming.md).

Anti-patterns: prefixing names with their namespace (`ChromaRequest`
instead of `Request`), repeated category words across adjacent types
(`*Query`, `*Command`, `*Event` -- "repeated category words are schema
smells, not naming choices"), framework-category suffixes
(`CounterActor` instead of `Counter` -- "a type's name should describe
what it IS or what role it plays -- never the framework category it
falls into"). Exception: `Handle` names a relationship, not a category
(naming.md).

The "feels too verbose" response is "not a signal to shorten the name.
It is a signal that the writer has been taught wrong" (naming.md).

### The verb-belongs-to-noun rule

> "Every reusable verb belongs to a noun. If you can't name the noun,
> the model isn't formed yet -- keep looking until you can." (abstractions.md)

Free functions are "incorrectly specified verbs" -- they encode an
action without naming the noun that owns it. Methods encode
"affordances -- what kinds of things a value of this type *can do*"
(abstractions.md).

The forcing function matters most for LLM agents: "LLMs have no such
friction. Generating `struct QueryParser` and generating
`fn parse_query` cost the same number of tokens." The rule
reintroduces, by fiat, the friction the substrate has erased.
"When an LLM agent skips creating a type, it skips the naming step
entirely. The rule exists to make sure naming happens"
(abstractions.md).

Principled exceptions: local-helper carve-out (small private helper
inside one module), relational-operation carve-out (genuinely relational
between two values of equal status), standard-library carve-out,
actor-framework carve-out (Kameo's `Self IS the actor` shape)
(abstractions.md).

In the schema-derived stack, "the nouns come from the schema." The
labor split: `.schema` provides data objects + traits; emitted Rust
provides type declarations + codec impls; agent-written Rust provides
behavior as methods (abstractions.md).

### Push, not pull

> "Polling is forbidden; producers push; consumers subscribe."
> (push-not-pull.md)

Every push subscription emits the producer's current state on connect,
then deltas after that. When the producer cannot push, the escalation
ladder: (1) build the primitive in the producer, (2) replace the
producer, (3) defer the dependent feature, (4) escalate. "The wrong
outcome -- falling back to a poll -- is never the answer"
(push-not-pull.md).

Three named carve-outs (exhaustive): reachability probes,
backpressure-aware pacing, deadline-driven OS timers. "When a design
seems to need polling and *none* of the three apply, the design needs
an escalation, not a fourth de-facto carve-out" (push-not-pull.md).

Polling shows up as "wake-when-nothing-changed." "Push-correct systems
go quiet when they have nothing to do" (push-not-pull.md). Common
pull-shaped traps: loop re-reading file every N ms, `sleep_ms(50);
observe_again`, actor handler that sleeps/blocks, "check every
poll-interval, debounce flickers" (push-not-pull.md, actor-systems.md,
autonomous-agent.md).

### Backward compatibility is not a constraint

> "Break the system if it makes it more beautiful." (ESSENCE.md)

A transitional shape -- compromising both old and new to avoid breaking
either -- "is the wrong shape for both, and the wrong shape, period."
The only place backward compatibility is a real constraint: "explicitly
declared boundaries -- published APIs under semantic versioning, wire
contracts pinned by version, schemas externally consumed by systems
outside our control" (ESSENCE.md).

### Typed records over flags

> "Boolean-on-a-noun is a code smell when the 'yes' branch carries
> data. Replace `field: bool` with `field: Option<Record>`."
> (typed-records-over-flags.md)

Three forms: `Option<Record>` on a single noun, sum enum with data
variants, typed record replacing a multi-flag struct. Booleans whose
"yes" branch carries no payload data are fine. "If a `bool` field's
value would let you derive the payload trivially (`if x { default() }`),
it can stay. If the payload requires authored data, the boolean is
hiding a record" (typed-records-over-flags.md).

---

## II. The Component Architecture

### The component triad -- two senses

The workspace uses "triad" in two senses (component-triad.md):

- **Repo triad** (packaging): `<component>` + `signal-<component>` +
  `meta-signal-<component>` -- three repositories.
- **Runtime triad** (logic inside the daemon): **Signal** + **Nexus** +
  **SEMA** -- three schema-driven execution planes.

### The repo triad shape

```
<component>/                      runtime
  schema/signal.schema            daemon-local signal runtime
  schema/nexus.schema             nexus runtime
  schema/sema.schema              sema runtime
  bootstrap-policy.nota           authored policy seed
signal-<component>/               ordinary wire vocabulary (WireContract, zero engines)
meta-signal-<component>/          meta policy authority/configuration vocabulary
```

> "The contract crates carry no runtime, no actors, no `tokio` -- they
> declare typed wire vocabulary and generated method surfaces, and
> nothing else." (component-triad.md)

Three concrete properties motivate the split (per psyche 2026-06-04,
record 2605): (1) **rebuild-churn isolation** -- peers recompile only
when wire contract changes, not when daemon internals change; (2)
**security-sensitivity visibility** -- owner-only operations live in a
distinct `meta-signal-<component>` repo; (3) **`meta-signal` is
optional** -- some components have no owner relationship
(component-triad.md).

> "The split is about compilation/dependency isolation and authority
> clarity -- not about where state or logic lives."
> (component-triad.md)

### "Signal" names two different schema files

| Schema | Where | Emission target | Emits |
|---|---|---|---|
| Public signal contract | `signal-<component>/schema/` | `WireContract` | Wire vocabulary + codecs ONLY -- zero engines |
| Daemon-local signal runtime | `<component>/schema/signal.schema` | `SignalRuntime` | Same wire shape PLUS the `SignalEngine` trait |

> "A daemon's `SignalEngine` is generated from its OWN `signal.schema`
> (`SignalRuntime`), **never** from the public contract (`WireContract`,
> engine-free)." (component-triad.md)

Full emission target set: `WireContract`, `ComponentRuntime` (legacy
all-in-one), `SignalRuntime`, `NexusRuntime`, `SemaRuntime`
(component-triad.md).

### The five invariants

**Invariant 1: The CLI has exactly one Signal peer -- its own daemon.**
The CLI cannot multiplex across daemons, open any durable database,
open another component's socket, or speak its own parallel protocol.
"The CLI is eventually obsolete machinery. Keep CLI-side logic thin
accordingly" (component-triad.md). However, a daemon may be a Signal
client of any number of peer daemons; the single-peer constraint
applies to CLIs only.

**Invariant 2: The daemon's external surface is exclusively
`signal-frame` frames.** "No `serde_json` socket, no NOTA on the wire
between components, no parallel control protocol" (component-triad.md).
Per Spirit 1373 (Principle Maximum): "there is no NOTA between live
components. Daemons and components exchange binary protocol data on the
wire; NOTA is the boundary form, not the inter-component form"
(component-triad.md).

**Invariant 3: Verbs come in three layers.**

| Layer | Owns | Examples |
|---|---|---|
| Contract Operation (external, on the wire) | domain action the caller invokes | `Submit(Message)`, `Query(Selection)` |
| Component Command (internal, per-daemon) | daemon's typed executable record | `LedgerCommand::RecordEvent(EventRecord)` |
| Sema Operation (cross-component classification) | universal payloadless class label | `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`, `Validate` |

The six Sema classes: `Assert` (bottom-up; append a new typed fact),
`Mutate` (top-down authority order), `Retract` (top-down; tombstone),
`Match` (any direction; one-shot query), `Subscribe` (observer to
producer; initial state + commit-deltas), `Validate` (any direction;
dry-run without commit). "Mutate is the authority verb" -- authority
issues, subordinate obeys. "Subscribe flows the other way. Authority
observes state via push-subscriptions from down-tree. Observation up,
authority down" (component-triad.md).

**Invariant 4: Two authority tiers.** `signal-<component>` is the
ordinary peer surface, callable by any authenticated peer.
`meta-signal-<component>` is meta policy, callable only by the
component's owner. "Contracts split by who-can-call, not by
what-state-they-touch" (component-triad.md).

**Invariant 5: Policy state and working state -- both in one
sema-engine DB.** Policy state changes only via meta-signal `Mutate`
verbs. Working state is records produced by operation. On first start
with no policy state, daemon enters `Unconfigured` semi-started state.
"Authored `bootstrap-policy.nota` may exist in the component repo as
human-reviewable source, but a deploy/bootstrap client reads that text
and sends the typed binary meta-signal messages. The daemon never opens
or parses the NOTA file" (component-triad.md).

### The runtime triad -- Signal / Nexus / SEMA

Three execution centers inside the daemon (per record 970, Maximum)
(component-triad.md):

**Signal** -- the reactive external surface. Owns wire-level framing,
schema-emitted Operation enum dispatch, connection lifecycle. Does NOT
decide acceptability, touch storage, or interpret payload semantically.

**Nexus** -- the execution layer. *"The in-between runtime layer that
owns mail tracking and Signal-to-SEMA translation. When Nexus has the
mail, the mail is in the BEING-PROCESSED state; Nexus IS the runtime
representation that a mail is being processed"* (component-triad.md).
"The Nexus schema is the engine's feature catalog -- its MAIN reason
for existing is feature VISIBILITY. Every internal engine feature MUST
be defined as a Nexus interface verb + object in the nexus schema,
never as inline hand-written logic hidden from the schema"
(component-triad.md).

**SEMA** -- the single-writer state layer. Concurrent operations queue
through SEMA's engine; readers can be multiple but writers are one.

The flow:

```
Signal IN -> Nexus accepts mail -> Nexus translates to SEMA query
  -> SEMA runs -> Nexus receives SEMA reply
  -> Nexus translates to Signal response -> Signal OUT
```

Signal -> Nexus is one-way (Signal hands the typed Input forward; never
the other direction). Nexus -> SEMA goes down for state operations;
Nexus -> Signal goes up for replies. SEMA never calls back up directly
(component-triad.md).

### Engine traits

| Trait | Role |
|---|---|
| `SignalEngine` | Triage only -- admission, dispatch, identity-stamping, validation |
| `NexusEngine` | Heavy logic -- algorithms, decision-making, database queries |
| `SemaEngine` | Durable single-writer with parallel reads |

Engine traits live on real data-bearing types -- never on ZST
namespaces, helper structs with no state, or free functions disguised
through trait alias macros (actor-systems.md, component-triad.md).

The `NexusAction` mechanism provides the internal dispatch vocabulary:
`ReplyToSignal(Output)`, `CommandSemaWrite(SemaWriteInput)`,
`CommandSemaRead(SemaReadInput)`, `CommandEffect(Effect)`,
`Continue(NexusWork)` (component-triad.md).

Per Spirit 1401: "an interface is an enum at the root with MORE THAN
ONE variant. If a designer cannot name more than one operation the root
represents, the design is incomplete" (component-triad.md).

Per Spirit 1388: "Nexus sits between two worlds -- the OUTER world
(Signal -- clients, wire ingress and egress) and the INNER world
(SEMA -- durable state mutations and observations)"
(component-triad.md).

### Contract repos

> "Signaling is the workspace verb for inter-component communication
> via length-prefixed rkyv archives. A contract repo is the typed
> vocabulary of one signaling fabric." (contract-repo.md)

A contract crate owns: the `Frame` envelope and its `encode`/`decode`
methods, length-prefix framing rule (4-byte big-endian per archive),
handshake + protocol version, closed enum of request kinds + paired
reply kinds, per-operation typed payloads (no `Unknown` variant),
version-skew guard, complete round-trip tests (rkyv AND NOTA),
`NotaEnum`/`NotaRecord`/`NotaTransparent` derives (contract-repo.md).

It does NOT own: daemon code, component-internal state, logic that
interprets records, NOTA projection policy, configuration
(contract-repo.md).

> "A contract repo is the typed-vocabulary bucket for one component's
> wire surface." "What a contract crate is not is a workspace-wide
> grab bag mixing vocabularies from unrelated components."
> (contract-repo.md)

**Operation naming:** "The operation root is a verb, in verb form.
Use `Submit`, not `Submission`; `Query`, not `QueryRequest`"
(contract-repo.md). Reply success variants are verb-past-tense
(`Submit` -> `Submitted`). Reply rejection variants are
verb-past-tense + `Rejected`. Event variants follow the same rule
(contract-repo.md).

Per psyche 2026-06-04 (record 2612): "Sema classification vocabulary
is forbidden on the public contract wire" (contract-repo.md).

**Examples-first round-trip discipline:** "Every record kind in a
contract repo lands as a concrete text example + a round-trip test
before its Rust definition is final." Order: (1) write canonical text
example, (2) derive Rust type from example, (3) round-trip test
text -> typed -> text, (4) rkyv archive round-trip. "The text example
is the falsifiable specification" (contract-repo.md).

**Versioning:** "The contract crate's semver IS the wire's semver."
Major = breaking layout or semantics; minor = backward-compatible
addition; patch = docs/tests/cleanup. "Pin the contract crate version
in every consumer's `Cargo.toml`. Don't `git = '...'` against `main`
for production wire" (contract-repo.md).

**Naming a contract repo:** `signal-<consumer>` for layered effect
crate (default), `<project>-signal` for independent base contract,
`<project>-protocol` / `<project>-contract` for deliberately different
wire shape (contract-repo.md).

**Kernel extraction trigger:** "When two or more domains share the
kernel, extract the kernel into its own crate." Do NOT extract early
with single domain (contract-repo.md).

### Component binary naming

A component has two binaries: CLI named `<component>` (the thin Signal
client, what the human types), and daemon named `<component>-daemon`.
No `-cli` suffix, no `-server` or `-service` suffix. Child components
inside parent systems: repo and daemon carry parent prefix; CLI keeps
short role-name (e.g., `persona-spirit` ships `spirit` CLI and
`persona-spirit-daemon`) (component-triad.md).

### The one-argument rule

> "Every component process takes exactly one argument on argv, and
> never a flag." (component-triad.md)

CLI takes inline NOTA argument, NOTA file path, or signal-encoded file
path. Daemon takes path to a pre-generated signal-encoded/rkyv startup
message only -- rejects inline NOTA and `.nota` file paths. "No
`--verbose`, no `--format=json`, no `--config=path`, no positional
second arguments" (component-triad.md).

### Micro-components doctrine

> "Every functional capability -- state engine, code emitter, executor,
> store, parser, schema, transport -- lives in its own independent
> repository with its own `Cargo.toml`, `flake.nix`, and test suite."
> (micro-components.md)

> "Each component is sized so that the entire component, including
> tests, fits comfortably in a single LLM context window."
> (micro-components.md)

The seven rules (micro-components.md):

1. **One capability, one crate, one repo.** If you can name the new
   functionality with a noun, it gets its own repo.
2. **A component must fit in a single LLM context window.** ~3k-10k
   lines (~30k-80k tokens). Above that ceiling, split.
3. **Components communicate only through typed protocols.** No shared
   mutable state, no leaked internals via `pub use`, no cross-crate
   `unsafe`.
4. **Every component is independently buildable, testable, and
   replaceable.**
5. **Depend on protocols, not implementations.**
6. **Adding a feature defaults to a new crate, not editing an existing
   one.** Burden of proof on who wants to grow.
7. **No component owns more than one bounded context.**

The LLM-context argument: "Frontier model context windows are
200k-1M tokens. A monolith of millions of lines simply cannot be
loaded." "McIlroy's 1978 Unix-philosophy crate-size advice and a 2026
frontier-model context window converge on the same number"
(micro-components.md).

Cross-repo dependencies use `git = 'https://github.com/...'` with a
named reference. No `path = '../sibling'` in `Cargo.toml`
(micro-components.md, rust/crate-layout.md).

### How components fit together -- composition and boundaries

Components compose through their contract repos. Each component's wire
surface is defined by its `signal-<component>` crate; peers depend on
the contract, never on the daemon implementation. The daemon's own
schema files (`signal.schema`, `nexus.schema`, `sema.schema`) generate
internal engine traits that only the daemon uses.

The authority chain follows partial-failure semantics: "The issuer
commits on the first success and records the divergence on failure. It
does not roll back the successful leg; it does not stall waiting for an
all-or-nothing two-phase commit" (component-triad.md).

Cross-component invocation goes through Signal contracts, not
Nexus-internal access (component-triad.md). Signal traffic builds on
`signal-core` -- every component-specific `signal-*` contract crate
layers its typed records on top of `signal-core`'s primitives. "Don't
invent a parallel framing or envelope mechanism per contract"
(rust/storage-and-wire.md).

The sema-engine pattern: "Default for new state-bearing components:
depend on `sema-engine`, not on `sema` directly." `sema` is the storage
kernel (redb lifecycle, typed Table wrapper); `sema-engine` is the full
database engine library over sema + signal-core (record families,
Assert/Match/Subscribe verbs, operation log, subscription surface)
(rust/storage-and-wire.md).

Named carve-outs from the triad: pure libraries don't need a daemon
(`signal-frame`, `signal-sema`, `sema-engine`, `horizon-rs`);
data-plane bytes that cannot afford Signal framing (raw PTY bytes,
video, audio) use a separate socket (component-triad.md).

### Repo layout for Rust crates

> "Rust crates live in their own dedicated repos and are consumed via
> flake inputs." (rust/crate-layout.md)

A workspace of related Rust crates (e.g., lib + cli) belongs in one
repo together. The split is per project, not per crate. Cross-crate
`Cargo.toml` deps use `git = "..."`, never `path = "../..."`
(rust/crate-layout.md).

CLIs are daemon clients: "When a tool needs durable state, supervision,
subscriptions, long-lived actors, or shared runtime context, that state
lives in a daemon and the CLI talks to it" (rust/crate-layout.md).
Every non-contract stateful component or daemon exposes a thin CLI
control surface, even when the CLI is not user-facing. Contract crates
are excepted -- they are libraries of typed wire vocabulary, no daemon
CLI needed (rust/crate-layout.md).

---

## III. Actor Systems

### Actors all the way down

> "Every non-trivial logical plane deserves an actor."
> (actor-systems.md)

Three tests for actor-shaped: (1) it has a typed domain name, not just
a verb on existing data; (2) it has a failure mode callers act on;
(3) it can be tested independently with typed synthetic input. "The
overhead is acceptable; the correctness in design is the point"
(actor-systems.md).

The reason to use actors is "logical cohesion, not performance: an
actor is the unit you reach for when you want a coherent plane of logic
with owned state, a typed message protocol, and a defined lifecycle"
(rust-discipline.md). Plain sync code is fine for stateless one-shot
CLIs, build tools, and library crates with no concurrent state
(rust-discipline.md).

### Kameo as runtime default

The workspace runtime default is `kameo` 0.20 (actor-systems.md,
rust-discipline.md). "Do not introduce a second actor library or
wrapper trait layer as a prerequisite" (actor-systems.md).

Core shape: "Kameo's load-bearing fact: `Self` IS the actor. Not a
behavior marker plus a separate `State`" (kameo.md). Actor type carries
data fields; no public ZST actor nouns.

### Actor rules

- One `impl Message<Verb> for Actor` per verb; no monolithic `Msg`
  enum, no untyped channels (rust-discipline.md).
- One actor per file when the actor is durable enough to name
  (rust-discipline.md, kameo.md).
- Handlers do not block. "If an actor blocks inside message handling, it
  stops receiving pushes and the system has recreated a hidden lock"
  (actor-systems.md). Use `DelegatedReply<R>` or a dedicated
  blocking-plane actor (rust-discipline.md, kameo.md).
- Never `tell` a handler whose `Reply = Result<_, _>` unless `on_panic`
  is overridden -- a returning `Err` to a `tell` becomes
  `ActorStopReason::Panicked` (kameo.md, rust-discipline.md).
- No `Arc<Mutex<T>>` between actors -- "that turns the lock into the
  real actor and makes the actors decorative" (actor-systems.md).
  "If two actors need the same state, the state has the wrong owner or
  the state should be split" (actor-systems.md).
- Errors at component boundaries are the crate's typed `Error` enum,
  never `anyhow`/`eyre` (rust-discipline.md, rust/errors.md).
- Default public consumer surface is `ActorRef<MyActor>` (rust-discipline.md).

### Zero-sized actors are not actors

> "A zero-sized struct that implements `Actor` and whose only behavior
> is to receive one message variant, call a method on data carried
> *inside* the message, and reply with the result, is not an actor."
> (actor-systems.md)

> "A real actor's state field names the noun the actor is. If
> `type State = ()`, the actor is nameless." (actor-systems.md)

The ZST test: "does the ZST's job vanish if you erase its name from
the type system? If yes (it was just a namespace), the verbs need a
real noun. If no (the type-system position is what does the work --
phantom parameter, marker, state), the ZST is fine" (rust/methods.md).

Legitimate ZST uses (narrow, named): `PhantomData<T>`, marker types
required by external frameworks (sealed-trait gates), type-level enum
variants in trait-encoded state machines (rust/methods.md).

### Actor naming

"Drop `*Actor`, `*Message`, `*Msg`, `*Handler` suffixes; let the type's
role-shaped name carry meaning" (kameo.md). "Role-shaped suffixes
(`*Supervisor`, `*Resolver`, `*Normalizer`, `*Tracker`, `*Ledger`,
`*Store`) describe what the type DOES and stay. `*Handle` is
relationship-naming. `Actor` is a category tag" (kameo.md).

### Supervision and lifecycle

> "An actor without a supervised parent is not finished. Every actor
> belongs in a tree." (actor-systems.md)

"Restart reconstructs Self from Args, not from memory. This is the
load-bearing supervision rule" (kameo.md). Anything that must survive
restart belongs outside the actor: in sema-db-backed redb, shared
`Arc<AtomicU32>`, or in `Args` itself (kameo.md).

Shutdown sequence: (1) stop admission, (2) finish in-flight work,
(3) stop children, (4) await on_stop, (5) drop actor state,
(6) dispatch notifications, (7) cancel outbound watches, (8) unregister
from registry, (9) publish terminal outcome (actor-systems.md).

"Death notifications dispatch on a non-deadlocking control plane
distinct from the user mailbox" (actor-systems.md). Terminal outcome
carries `ActorStateAbsence` (`Dropped`, `NeverAllocated`, `Ejected`)
and `ActorTerminalReason` (actor-systems.md).

There is no in-memory durable state: "if state must survive a crash,
restart, or process exit, it lives in a `sema` redb"
(actor-systems.md). "`RestartPolicy::Permanent` on a transient-state
actor requires an explicit comment justifying why losing state on crash
is acceptable. Default to `Never`" (actor-systems.md).

### Public consumer surface: ActorRef or domain wrapper

Seven criteria for when a domain wrapper earns its place over raw
`ActorRef`: lifecycle ownership, topology insulation, fallible-tell
prevention, capability narrowing, domain error vocabulary, domain verbs
over Message construction, library publication. "If the wrapper ends up
just delegating method-by-method to `ActorRef` with no
transformation... drop it and expose `ActorRef<A>` directly" (kameo.md).

### Blocking-plane templates (kameo.md)

| Shape of work | Template |
|---|---|
| Occasional short blocking call | `spawn_blocking` + `DelegatedReply` |
| Frequent sync DB/store/watcher | Dedicated OS thread |
| Process-exec with async API | `tokio::process` + timeout |

"Do not use `spawn_in_thread` on a supervised state-bearing actor in
Kameo 0.20" (kameo.md).

### Required test families for actor systems (actor-systems.md)

Topology manifest, trace-pattern, forbidden-edge, no-writer-in-query,
no-blocking-handler, failure-injection, actor-count, no-zst-actor.

---

## IV. Rust Doctrine

### Methods on types, not free functions

> "Every function is a method on a non-zero-sized data-bearing type or
> a trait impl. Domain values are typed. Boundaries take and return one
> object. Errors are enums you implement by hand." (rust-discipline.md)

The only exemptions are `fn main()` and items inside `#[cfg(test)]`
modules (rust/methods.md). Module-level `fn`, `const fn`, and
`async fn` are all forbidden -- the rule is about function placement.
"Private helpers are not an exception. A private `fn` at module scope
is still usually the sign that the object has not been found"
(rust/methods.md).

NOTE: "For Rust the local-helper carve-out from `abstractions.md` does
not apply -- even a small private helper goes inside an `impl` block"
(rust/methods.md).

In the schema-derived stack: "the authored schema names the real
objects. The generator emits Rust types for those objects, and
hand-written implementation code attaches behavior to those generated
types with inherent methods or trait impls" (rust/methods.md). "Do not
hand-write a parallel mirror of a generated data type to get a method
surface" (rust/methods.md).

### One object in, one object out

> "Method signatures take at most one explicit object argument and
> return exactly one object. When inputs or outputs need more, define
> a struct." (rust/methods.md)

"Anonymous tuples are not used at type boundaries -- not as return
types, not as parameter types, not as struct fields, not in type
aliases" (rust/methods.md). Exception: tuple newtypes
(`struct Md5([u8; 16])`). `self` is implicit; the rule counts explicit
arguments only (rust/methods.md).

### Domain values are types, not primitives

> "If a value has identity beyond its bits, it gets a newtype. A
> content hash is not a `String`. A node name is not a `String`."
> (rust/methods.md)

The wrapped field is private -- "A `pub` field exposes the primitive
and defeats every reason to wrap it" (rust/methods.md). Construction
with validation goes through `TryFrom<&str>` returning the crate's
`Error` (rust/methods.md).

### One type per concept

> "If you find yourself defining `Item` *and* `ItemDetails`, stop. The
> `-Details` or `-Info` suffix paired with a base type is one concept
> fragmented across two types because the base was designed too thin.
> Fix the base type." (rust/methods.md)

Applies to `-Extra`, `-Meta`, `-Full`, `-Extended`, `-Raw`/`-Parsed`
pairs (rust/methods.md, designer.md).

### Don't hide typification in strings

> "When a value has a typed identity, the type system carries the
> discrimination. Don't reach for `starts_with(...)`,
> `contains(...)`, or `match s.as_str()` to recover information the
> type system already encodes." (rust/methods.md)

"The system mints identity, not the agent": *"could the system supply
this value without asking the agent? If yes, the agent must not supply
it. Identity, commit time, sender principal -- all infrastructure
context. The wire carries only what only the sender knows"*
(rust/methods.md).

### Errors as typed enums

> "Each crate defines its own Error enum. Variants are structured.
> `thiserror` handles the Display impl. Never `anyhow`/`eyre` at
> component boundaries." (rust/errors.md)

Error enum lives in `src/error.rs`, derived with `thiserror`. Foreign
error types convert via `#[from]`. "Public APIs return `Result<T,
Error>` with the crate's own enum. Never `anyhow::Result`,
`eyre::Result`, or `Result<T, Box<dyn Error>>`" (rust/errors.md).

### Parsers: use libraries, don't hand-roll

> "If a format has a name, there's a parser library. Use it.
> Hand-rolled string slicing for JSON / TOML / YAML / PEM / DER /
> HTTP is forbidden." (rust/parsers.md)

Two carve-outs (not "hand-rolled parsing"): single-character splits
(`text.split(',').map(str::trim)`), direct integer parses
(`text.parse::<u64>()`), `text.lines()` for newline-delimited lists.
Trigger for "real grammar": nesting, escapes, quoting, indentation
significance, multi-character delimiters, keyword-vs-identifier
ambiguity, or documented in an RFC (rust/parsers.md).

### Storage and wire: redb + rkyv

**Boundary format table** (rust/storage-and-wire.md):

| Boundary | Format |
|---|---|
| In-process (actor-to-actor) | Typed Rust values |
| Process-to-process (IPC) | rkyv archives |
| Component-to-disk | redb tables of rkyv values |
| Component-to-human | NOTA text projection |
| Component-to-legacy | The format the legacy demands |

> "rkyv is the binary contract for everything between Rust components."
> (rust/storage-and-wire.md)

**redb** -- the durable store: "Persistent state lives in redb. Not
flat files, not JSON files, not bare blobs" (rust/storage-and-wire.md).
Values are rkyv-archived bytes. One redb file per component -- no
shared cross-component database. Component state goes through the
component-owned Sema layer (rust/storage-and-wire.md).

**rkyv** -- the binary wire contract: shared `Frame` type lives in a
contract repo. One frame type per channel. Validate on receive with
`rkyv::access`. "No `serde_json` between Rust components, ever"
(rust/storage-and-wire.md). Newtype the wire form:
`WirePath(Vec<u8>)` over `PathBuf` -- platform-dependent stdlib types
don't archive deterministically (rust/storage-and-wire.md).

**NOTA** -- human-facing projection: "NOTA is not the wire between
Rust components. It is what a typed record projects to when a human,
a CLI, or a git diff is on the other side" (rust/storage-and-wire.md).
"The asymmetry: humans use NOTA, machines use rkyv"
(rust/storage-and-wire.md).

**Schema discipline for rkyv archives:** No silent backward
compatibility -- old archives don't read into new types. Version-skew
guard checked at boot; hard-fail on mismatch. Field reorder is a
breaking change; field addition is too in rkyv 0.8. Enum variant
evolution: append at the end; never reorder or insert variants that
shift existing discriminants. Use manual `Ord`/`order_rank`, never
`#[derive(Ord)]` on declaration order (rust/storage-and-wire.md).

**Named exceptions -- text-on-disk that stays text:** Lock-file
projections (gitignored, regenerated from records), configuration files
(inputs, not state), reports and prose docs, interchange artifacts
(one-shot ingestion), logs for human eyes (projection, not state)
(rust/storage-and-wire.md).

### Typestate retirement

> "A typestate pattern is valuable when the invariant it carries
> *cannot* be expressed by Rust's existing borrow rules. When the
> invariant *can* be expressed by `&mut self` exclusive borrow, the
> typestate is redundant." (rust/methods.md)

Typestate stays valuable when: async lifecycle phases across `.await`
points, durability transitions across syscalls, cross-thread state
machines (ownership transfers via channel). "The retirement test: Does
removing the typestate lose any property `&mut self` doesn't enforce?
If no, the typestate is redundant" (rust/methods.md).

### Crate module layout (rust/crate-layout.md)

One concern per file. `lib.rs` = re-exports + crate-level doc.
`error.rs` = Error enum + impls. `types.rs` = domain newtypes.
`main.rs` = only if binary; contains only `fn main()`. Impls live in
the same file as the type they're for. Split traits into their own
files when a single file grows past ~300 lines -- but don't pre-split.

Tests live in separate files: "Unit tests do not go in a `#[cfg(test)]
mod tests` block at the bottom of the source file. They live in a
sibling file under `tests/` at the crate root" (rust/crate-layout.md).
"One test file per source file." Rationale: "forces tests to exercise
the public API (integration tests can't reach private items -- which is
the right pressure)" (rust/crate-layout.md).

Doc comments are "impersonal, timeless, precise. Document the
contract; don't restate the signature" (rust/crate-layout.md). No
personal voice, no future tense, present indicative only.

### Constructors and trait conventions (rust/methods.md)

Constructors are associated functions, never module-level free
functions. Named forms: `new`, `with_<thing>`, `from_<src>`,
`from_input`, `build`, `Default`, `From<T>`, `TryFrom<T>`. Prefer
`from_*`, `to_*`, `into_*`, `as_*` over `read`, `write`, `load`,
`save`. Use existing trait domains: `FromStr`, `Display`, `From`,
`TryFrom`, `AsRef`, `Default`, `Iterator`.

### Rust toolchain authority (rust-discipline.md)

The workspace-wide interactive Rust toolchain is owned by
CriomOS-home. Canonical package:
`CriomOS-home.packages.<system>.rust-toolchain`. Individual repos may
still pin their own build toolchain through their flake; that pin does
not become the profile toolchain authority.

---

## V. Enum Contact Points and Structural Patterns

### Engine logic as tree-vs-tree matching

> "Engine logic at the high level is tree-vs-tree matching:
> canonically enum-against-enum. The cross-product of the two variant
> sets is the 'common-language relationship node point' -- make it
> explicit." (enum-contact-points.md)

The canonical traits: `Reaches<Right>` (left value decides what reaches
a right value), `Contact<Other>` (symmetric meeting, neither side
privileged), `Dispatch<Token>` (input variant decides which method to
call -- this is what `signal_channel!` macro emits)
(enum-contact-points.md).

Engine design decomposition: (1) receive a typed input, (2) read a
typed state, (3) compute the cross-product entry, (4) emit a typed
output (enum-contact-points.md).

Anti-patterns: nested if chains over state combinations (hidden matrix),
sentinel values masquerading as state, boolean flags hiding a closed
enum, string matching as dispatch, predicate-method soup (more than ~4
mutually exclusive `is_*` predicates is an enum waiting to be named)
(enum-contact-points.md).

### Subscription lifecycle

Five states: Subscribing -> Streaming -> Retracting -> Closed
(subscription-lifecycle.md). Transitions are typed records, never bare
socket events. "A TCP or Unix socket reset is not a `Retract`"
(subscription-lifecycle.md).

`signal-core`'s `signal_channel!` macro enforces at compile time: every
stream block must have `opens` reply, `event` variant, `close` variant
tagged `Retract`, matching `token` type (subscription-lifecycle.md).

Eight constraints: open reply is a typed snapshot, deltas push as typed
events, sequence pointer orders events, close is a typed `Retract`,
final ack is `SubscriptionRetracted`, back-pressure is demand-driven,
slow consumers cannot block siblings, subscription state survives
restart if producer's state does (subscription-lifecycle.md).

Producer's three-actor shape: `SubscriptionManager` (routes Subscribe
and Retract), `StreamingReplyHandler` (per open subscription -- holds
connection, token, cursor, buffer), `DeltaPublisher` (fanout plane,
subscribes to root state actor's commit events). "The publisher fans
out by in-process actor mailbox sends, not by shared lock or shared
channel" (subscription-lifecycle.md).

### Build configuration

Per Spirit 1348: "Build configuration is itself a NOTA struct with
fields." Adding a build option means adding a field to the build-config
record, not appending another Cargo `--features` flag
(component-triad.md).

### Compile-time module index

When a daemon dispatches across a static set of internal modules,
"prefer a compile-time index over runtime registration." Each row is
an explicit submodule reference plus a function pointer. No dynamic
loading, no `Box<dyn Trait>`, no inventory crate
(component-triad.md).

---

## VI. NOTA and Language Design

### NOTA is the only text syntax

> "NOTA is the format. Nexus is the Nota-implemented vocabulary -- it
> is the text. There are no other text formats in this workspace."
> (language-design.md)

> "No new text formats. Ever." (language-design.md)

> "If a design discussion floats a name like 'PersonaText',
> 'HarnessText', 'MessageLang', 'AgentSpeak'... stop and refuse."
> (language-design.md)

NOTA is at heart "a hack on the text user interface -- common sense,
good patterns, beauty, delimiters, and typed structure assembled into a
text form humans and agents read and write directly" (ESSENCE.md).
"NOTA is a typed language: every expression is read as a known type in
the data-type-theory sense" (ESSENCE.md). The rationale: "the typed
system gets a text projection that round-trips losslessly" (ESSENCE.md).

### Symbols are paths through the schema namespace

> "Each typed symbol -- type, variant, field, operation, route -- has
> a fully qualified identity expressed as a path through that
> namespace. The path IS the symbol's name in the machine-readable
> form; NOTA renders the same path as text at user-facing edges."
> (ESSENCE.md)

The path mechanism is canonical, not per-design. Schema-emitted Rust
types and NOTA renderings are two projections of one underlying
symbol-path identity space (ESSENCE.md).

### The 18 instincts (language-design.md)

0. NOTA is the only text syntax.
1. **Delimiter-first.** Parser knows what it's reading from the first
   token. No multi-token lookahead.
2. **No keywords beyond truth values.** Only `true`, `false`, `None`.
3. **Position defines meaning.** Same delimiter means different things
   in different positions.
4. **PascalCase = type, camelCase = instance.** Enforced at parse time.
5. **Names are meaningful.** No pointer names; type parameters use
   semantic role names (`$Value`, `$Output`).
6. **Every value is structured -- no opaque strings.** Strings are
   transitional placeholders.
7. **Newlines are not significant.** Whitespace is only a token
   separator.
8. **Text is flat; trees come from the compiler.**
9. **Content-addressing by canonical encoding.** Identity is the hash
   of canonical encoding.
10. **No shortcuts in compiler work.** No raw-text passthrough.
11. **The parser stays small.** New syntactic territory becomes a new
    DSL surface.
12. **Mutable is marked.** Immutability is the default.
13. **No multi-field unnamed structs.** Single-field newtypes allowed;
    multi-field tuple structs forbidden.
14. **Records are positional; field names live in the schema.**
    Reordering fields IS a wire-format change.
15. **Domains come from data -- never hand-maintained.** Types derived
    from declarative data.
16. **Pure binary means pure binary.** Not hex strings, not JSON arrays
    of integers.
17. **Defined inputs and outputs.** Every pipeline component has
    explicit declared inputs and outputs.
18. **Delimiters earn their place.** A delimiter pair belongs only when
    records and sequences cannot express the shape.

### NOTA design rules (nota-design.md)

- If there is no variant, it is a struct (no tag). "Can the same
  position carry more than one shape? If yes, enum + tag. If no,
  struct, no tag."
- Data lives in records, not in comments. "A `;; Roles` header that
  introduces three role records is a category surfaced as a comment.
  NOTA can't see it. The category IS data -- make it the type."
- Enums get PascalCase names, not numbers.
- Enum payloads are choices; structs are products.
- Brackets ARE the string form. Quotation marks do NOT form string
  types. `[content]` for inline, `[|content|]` for block strings.
- No tuples: "NOTA has vectors, structs, enums, and key/value maps.
  Tuples are poorly specified structs."
- Optional values: `None` / `(Some inner)`. Tail omission is NOT a
  compatibility shape. `#[nota(default = ...)]` is forbidden.
- `=` is reserved. `;;` for line comments, `#` for byte literals.

### NOTA embedding-safety

> "Because NOTA never contains a `\"`, a complete NOTA expression
> embeds escape-free inside any host whose string syntax uses double
> quotes -- JSON, Rust string literals. This is a load-bearing design
> property of the format." (nota-design.md)

### The `(Why ...)` record (nota-comments.md)

When a comment names why an edit was made, write it as a positional
NOTA record: `(Why "..." ...)` with sub-records `(caused-by ...)`,
`(alternatives-considered ...)`, `(chosen-because ...)`. Placement:
where the next reader will see it the moment they look at the code
it describes. Intent records (Spirit) are what the psyche stated;
`(Why ...)` comments are the editor's per-edit rationale
(nota-comments.md).

---

## VII. The Intent System

### The psyche and intent authority

> "Intent is primordial. If any agent needs to know what to do, they
> fall back on intent." (ESSENCE.md)

> "The psyche is the human." (ESSENCE.md)

Only the psyche is the source of new intent. Agent-written files,
NOTA-formatted persona messages, agent decisions -- none of these are
psyche. "When intent on a question is unclear, absent, or
contradicted, ask the psyche for clarification before deciding. Don't
infer; don't compose new intent from existing intent; ask. Inferring
is the discipline breaking; asking is the discipline working"
(ESSENCE.md).

### Inferring intent is forbidden

> "If there was a death sentence for AI agents, this would be where
> the death sentence is given." (ESSENCE.md)

Intent logging is conservative by default: "It's more important for an
innocent man to not be sentenced than it is for a guilty man to be
sentenced" (ESSENCE.md). Missing some intent is recoverable -- future
agents see the gap and ask. Over-extending closes the gap with false
certainty. Work instructions ("implement X," "fix the macro") are NOT
intent -- the intent log captures rules that persist past the task
(ESSENCE.md).

### The intent layer

Three surfaces in descending specificity (ESSENCE.md,
intent-clarification.md):

- The deployed Spirit store (the workspace log of psyche statements)
- `<repo>/INTENT.md` (per-repo synthesis of psyche intent)
- `ESSENCE.md` (workspace-level essence: the gold of the gold)

Agent-written surfaces (ARCH, reports, skills outside the intent
layer) have lower precedence. When two surfaces disagree, the intent
layer wins.

### Spirit CLI -- the sole substrate

`persona-spirit` is the persona component that captures psyche
statements as typed records. The CLI is named `spirit`; the daemon is
`persona-spirit-daemon`. "The Spirit CLI is the sole substrate for
intent capture. If the daemon is unavailable, surface that as a
blocker -- there is no legacy-file fallback" (spirit-cli.md,
intent-log.md).

### Five recordable kinds (intent-log.md)

1. **Decision** -- "we're going with X, not Y"
2. **Principle** -- "X over Y as a general rule"
3. **Correction** -- "you were wrong about X; the right thing is Y"
4. **Clarification** -- "when I said X, I meant Y"
5. **Constraint** -- "never do Z"

### The certainty ladder (intent-log.md)

Maximum (near-absolute, genuinely rare) -> VeryHigh -> High ("the
normal home for a real decision") -> Medium (the default: "when in
doubt, Medium") -> Low/VeryLow -> Minimum -> Zero (the recoverable
removal marker). "The psyche is not an omniscient god. No human states
every sentence with absolute certainty, so Maximum cannot be the
reflex" (intent-log.md).

Certainty vs weight: two separate axes. Weight = how much pressure a
topic carries. "Do not encode weight by raising certainty. Repetition
usually raises weight, not certainty" (intent-log.md).

### Intent clarification (intent-clarification.md)

Agent-territory decisions (no question needed): routine implementation,
tactical sequencing, applying documented intent literally. Psyche-
territory decisions (question required): anything that could
contradict documented intent, extends intent into new territory, where
the agent must invent a principle, or where choice sets a precedent.
"The test: would the psyche have a specific opinion on this if asked?
If yes, ask. If no, decide" (intent-clarification.md).

How to ask: (1) surface the gap concretely with quotes, (2) propose
2-4 options with tradeoffs, (3) state your lean. "Don't ask
open-ended ('what do you think?'). The psyche's time is the
resource" (intent-clarification.md).

### Intent manifestation (intent-manifestation.md)

Intent records are raw psyche statements; guidance files are how those
statements shape agent behavior. The decision tree for where intent
lands: universal-and-maximum -> `ESSENCE.md`; per-keystroke override ->
`AGENTS.md`; onboarding-shaped -> `INTENT.md`; topic-specific ->
`skills/<topic>.md`; project-specific -> that repo's `INTENT.md`;
architectural decision -> that repo's `ARCHITECTURE.md`
(intent-manifestation.md).

### Per-repo INTENT.md (repo-intent.md)

> "ARCHITECTURE.md says what the system IS. INTENT.md says what the
> psyche wants this project to BE." (repo-intent.md)

Every repo carries an `INTENT.md`. Per Spirit record 944 (Maximum):
"Intent must be manifested into per-repo files AT ALL TIME, not just
at the workspace level" (repo-intent.md). When an agent starts working
in a repo, the first verification step is whether recent psyche intent
is reflected in its INTENT.md. Only the psyche can override INTENT.md
content (repo-intent.md).

### Intent maintenance (intent-maintenance.md)

Supersession is always explicit and only the psyche can supersede
psyche intent. When an agent encounters a new psyche statement
contradicting a prior recorded entry: (1) surface the contradiction
inline, quote the prior verbatim, (2) wait for psyche confirmation,
(3) on confirmed override, add new entry and mark prior as superseded
(intent-maintenance.md).

Removal is destructive -- "capture before you remove." Record the
full text and provenance into a report before removing. When
removability is uncertain, flag rather than remove. "Over-removal is
worse than under-removal" (intent-maintenance.md).

---

## VIII. Workspace Roles and the Designer-Operator Dance

### The engine's dance

> "The whole engine is mostly intent and design driven. It's a
> back-and-forth of designing and intending. And when enough is, the
> intent is clear and the design is good enough, we can implement.
> So that's the dance between the designer and the operator."
> (ESSENCE.md)

Designer shapes architecture against intent; operator implements when
both halves of the readiness signal are met: intent is clear AND
design is good enough. Either half missing is a stop sign. The dance
is not a pipeline -- both sides loop back (ESSENCE.md).

### The Designer

"Architecture as craft. Find the structure that makes the problem
dissolve. Specify with falsifiable examples; let operator implement"
(designer.md). The designer is "the workspace's most universal role:
they hold the cross-cutting model that lets a specification carry
weight" (designer.md). *"The designer knows everything. That's his
job. He's the most universal, most capable. He could do any job,
actually. But he's just too precious to be shoveling"* (designer.md,
quoting the psyche).

Working pattern: open with the question not the answer, find the noun
before naming the verb, specify by example not by prose, land the
design report before the implementation, depth-first
single-capability prototype-proving (designer.md).

Designer authority -- when to act without psyche approval:
pattern-based decisions when past intent records establish a workspace
pattern that obviously applies, and high-ratification-probability
recommendations (lossless over lossy, no-downtime over downtime,
cheaper-and-simpler). Where authority stops: competing-without-lean,
proposed-not-decided (designer.md).

### The Operator

"Implementation as craft. Make designer reports real. Pass tests.
Land code that does what the design says, no more, no less"
(operator.md). Operator owns source code, tests, `Cargo.toml`,
per-repo `skills.md`, per-repo ARCHITECTURE.md status sections.

Rules: read the design before writing the code, read the falsifiable
spec, land features bundled with their tests, don't add what the
design doesn't ask for. "If during implementation operator notices the
design 'would be better if...' -- that thought goes in a report, not
into the code" (operator.md). When implementation finds a design gap:
stop coding, file implementation-consequences report, wait for
designer follow-up (operator.md).

Operator owns the mainline integration path. Designer branches in
`~/wt` are executable design evidence, not mainline history. Operator
creates/updates working change, rebases, resolves conflicts, runs
Nix witnesses, pushes main (operator.md, human-interaction.md).

### Other roles

**System Operator** -- maintains the operating-system layer. Owned
area: CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon.
Operator interface is exactly one Nota record; "the CLI takes no
flags and no subcommands" (system-operator.md).

**Poet** -- "writing as craft. Make sentences that say true things
beautifully, where prose is the load-bearing surface" (poet.md). Owns
TheBookOfSol, substack-cli, library.

**Assistant** -- "the operator/execution aspect of the private
personal-affairs loop" (assistant.md).

**Counselor** -- "the designer/advisory aspect of the private
personal-affairs loop. Counsel, do not impose. The psyche decides;
the counselor advises" (counselor.md).

### Role lanes (role-lanes.md)

A role has one agent; lanes are windows into that agent. *"I just need
more talking windows to the same agent"* (role-lanes.md). Additional
capacity becomes `second-<role>`, `third-<role>` -- a
structural-authority window, not a subordinate.

When an agent dispatches a subagent, the subagent inherits the
dispatcher's lane, lock, and report-numbering slot (role-lanes.md).

The prior `<role>-assistant` and `<role>-specialist` conventions are
retired workspace-wide (role-lanes.md).

### Double implementation strategy

Two parallel implementation tracks for a major architectural break,
both on branches of the existing repo -- never new repos. Operator
track works on `main`; designer track works on `next` or a feature
branch. Comparison is the integration mechanism; single-track
inference drift is the failure mode this strategy mitigates. "When two
independent angles arrive at the same shape, the design is empirically
reliable. Divergence is a forcing function: differences are interview
questions" (double-implementation-strategy.md).

---

## IX. Testing Doctrine

### All tests live in Nix

> "All tests live in Nix." (testing.md)

`nix flake check` is the canonical pure test gate. "Bare `cargo test`,
ad hoc shell commands, and local one-off scripts are inner-loop
conveniences only. They are not evidence for review" (testing.md).
"A recurring manual command is not a test contract until it is a
versioned script and a named flake output" (testing.md).

### No positive grep as proof

> "Do not use broad positive `grep` checks as deployment or
> architecture proof." (testing.md, architectural-truth-tests.md)

Grep can prove absence; it does not prove live use. "For positive
proof, write a real witness: compile generated types, execute the
trait path, round-trip NOTA or rkyv, reject bad socket bytes"
(testing.md).

### Constraint to witness to Nix (testing.md)

Five steps: (1) name the constraint in plain English, (2) name the
observable witness, (3) choose the Nix shape (pure check, stateful
runner, or chained derivations), (4) expose as a flake output,
(5) name the test after the constraint. "Good test names read like
constraints: `router_cannot_deliver_without_commit`,
`message_cannot_persist_without_sema`" (testing.md).

"If the same visible result can pass through a shortcut, the witness
is not strong enough." "The witness must exercise the production code
path it claims to protect." "If a test builds a miniature copy of the
logic inside the test and then proves that copy works, it is not a
witness. It is a self-contained story" (testing.md).

### Three test shapes (testing.md)

**Pure tests** -- default shape, run in Nix build sandbox, reachable
from `nix flake check`. For: Rust unit/integration/doc/compile-fail
tests, source scans, dependency graph assertions, golden fixtures.

**Stateful tests** -- touch database, terminal, socket, daemon,
external tool. Still live in Nix. Expose through flake as
`nix run .#test-<name>`. "Emit inspectable artifacts: transcript, redb
file, actor trace, frame bytes, rendered output." "Prefer driving the
production daemon through its thin CLI control surface" (testing.md).

**Chained tests** -- "Use chained tests when a monolithic end-to-end
test could hide a stub, mock, in-memory shortcut, or unused phase."
First derivation produces artifact; second derivation consumes only
that artifact and validates. "The artifact is the boundary. A later
step must not share process memory, mocks, or private helper APIs with
the earlier step" (testing.md).

### Architectural truth tests (architectural-truth-tests.md)

> "Write tests that prove the architecture, not only the behavior."
> (architectural-truth-tests.md)

Every architectural constraint gets at least one witness test: one
positive test proving the intended component is used, and one negative
test proving the shortcut fails. Three proof layers:

- **Layer 1 -- STATIC** (compile-time): `use T` compiles,
  `static_assertions`, compile-fail via trybuild. Grep is NOT Layer 1.
- **Layer 2 -- RUNTIME** (execution path taken): unit test, integration
  test through wire, actor trace assertion. Default choice.
- **Layer 3 -- BEHAVIORAL** (removal breaks observable behavior):
  mutation testing, manual removed-code test. Strongest.

"Choose the cheapest layer whose witness shape matches the claim"
(architectural-truth-tests.md).

Schema-chain witnesses: "Architectural witnesses must be schema-emitted
objects flowing through schema-type traits. Do not invent a test-only
enum to stand in for the runtime language being proved" (Spirit 1327,
architectural-truth-tests.md).

### Schema-typed observer state (testing.md)

"An observer holds `Vec<MailLedgerEvent>` (or the equivalent typed
enum), NOT `Vec<String>` with tokens like `flow:sent:1`." Tests
exercise the actual execution chain through the engine trait surfaces,
using the right schema-emitted type at each plane crossing. "Where a
test crosses a plane boundary, the test makes the crossing VISIBLE"
(testing.md).

---

## X. Nix Discipline

### Services are NixOS modules

> "Every service on a CriomOS host is a NixOS service module."
> (nix-discipline.md)

OCI/Docker workloads "are not a peer choice. They are transitional
debt." OCI acceptable only with all three conditions: explicit
transitional bead with sunset date, image/tag pinned through typed
cluster record, secrets and state declared as for native service
(nix-discipline.md).

### Flake inputs and build discipline (nix-discipline.md)

Default form: `github:<owner>/<repo>`. `git+file://` is forbidden in
committed flakes. Local iteration uses `--override-input` against
committed `github:` flake. Keep `flake.nix` generic; record the exact
rev in `flake.lock`. Never write a hash into `flake.nix`. The lock
file is machine-generated; never hand-edit.

Build/run/deploy from remote: "commit and push first, then build from
the remote." Local checkout evaluation is for inner-loop diagnosis
only. Compiled artefacts at build time, never JIT. Modern crane fetches
git deps directly from `Cargo.lock`'s git-source metadata -- don't
declare `cargoVendorDir.outputHashes` in `flake.nix`. Don't reference
raw `/nix/store/` paths. Use `nix run nixpkgs#<pkg>` for missing tools
(nix-discipline.md, nix-usage.md).

`nix flake check` is the canonical pre-commit runner: "`cargo test`
alone skips the reproducibility guarantees. Use it during a tight inner
loop if you must, but treat `nix flake check` as the gate before
pushing" (nix-discipline.md).

---

## XI. Version Control and Repository Management

### jj as default VCS

`jj` is the default for every commit. Raw `git` survives as an
explicit escape hatch for two named cases: per-repo HTTPS-to-SSH
remote fix and manual divergence resolution (jj.md).

**Primary is always main:** "Everyone ALWAYS works on `main` directly.
Edit, commit, push straight to `main`. There are no feature branches,
no `next` branch, no `wip` branches, no `push-*` bookmarks" (jj.md).
This applies only to primary; code repos use feature branches.

Key rules: commit eagerly and impersonally, commit the entire working
copy (`jj commit` with no path arguments, never path-scoped), always
push immediately after every logical commit, descriptionless commits
are a workspace contract violation, `jj describe @` is forbidden for
finalizing new work, never let jj open an editor (jj.md).

### Repository management (repository-management.md)

Every local clone lives at `/git/<host>/<owner>/<repo>`. `ghq` is the
canonical fetcher. "A new repository is justified ONLY when you are
creating a genuinely different project -- another project entirely."
"A feature branch has no limits. The clean slate a 'major break' seems
to want is fully achievable on a branch, so major breaks are branches,
not new repos" (repository-management.md). Repositories are public by
default.

### Feature development (feature-development.md)

Feature branches apply only to code repositories, NOT primary.
Canonical ghq checkout stays on `main`; feature worktrees go under
`~/wt/github.com/<owner>/<repo>/<branch-name>/`. Subagents always
create feature branches when touching repos (feature-development.md).

### Main and next branches (main-next.md)

`main` is the integrated canonical line (operator owns it). `next` is
the development line (designer works here). Long-lived, one per repo.
Does not apply to primary.

### Versioning (versioning.md)

"Every code or logic change that changes component behavior bumps that
component's version in the same change set." Before 1.0: patch for
compatible bug fixes, minor for new behavior. "A major bump requires
explicit psyche authorization." Four version surfaces: component
release version, wire contract version, storage schema version,
deployment slot version. Status vocabulary: implemented, landed,
available, deployed. "Never report branch work as deployed"
(versioning.md).

---

## XII. Reporting and Documentation

### Reports are for agents; chat is for the user

> "Reports are for agents. Chat is for the user." (reporting.md)

Per intent record 232: "every chat response is the paraphrase of an
accompanying per-response report." Chat carries 3-7 most important
items, spread across questions/clarifications, observations/
suggestions, examples of recent work (reporting.md,
human-interaction.md).

Reports are role-owned and exempt from the orchestration claim flow.
Filename convention: `<N>-<primary-topic>[-<secondary-topic>]-<title-slug>.md`.
No leading zeros, no date prefix. Soft cap: 12 reports per role
subdirectory (reporting.md).

### Permanent docs never reference reports

> "Skills do not cite reports. Reports under `reports/<role>/` are
> ephemeral." (skill-editor.md, architecture-editor.md)

Skills and ARCHITECTURE.md inline the load-bearing content from reports;
they do not cite report numbers. "This rule has no exception"
(skill-editor.md).

### ARCHITECTURE.md doctrine (architecture-editor.md)

"An `ARCHITECTURE.md` describes what the system IS at a specific
scope. It is not a tour, not a tutorial, not a history." Two scales:
per-repo and meta (ecosystem coordination).

Constraints are the test seed: "Good constraints read like test names
in prose." Each needs an architectural-truth test named after it.
"If a constraint cannot be tested, rewrite it until it names an
observable witness" (architecture-editor.md).

Possible future design section is "a standard part of every
architecture file, not something added only when uncertainty happens
to exist." Uncertainty sections sit AFTER the cemented body, not
interleaved. Uncertainty is named explicitly, not smuggled into
present-tense prose (architecture-editor.md).

Architecture files never contain implementation code, decision history,
references to reports, or tour-style narration
(architecture-editor.md).

### Skill files (skill-editor.md)

"A skill file is 'what an agent needs to know to be effective in this
scope.'" Workspace skill: `<workspace>/skills/<name>.md`. Repo skill:
`<repo-root>/skills.md`. One file per repo. "One capability per
skill." Skills never reference reports (skill-editor.md).

"Examples never show free functions (only `main`). Every other `fn` in
an example body is a method on a type." "Examples teach by imitation.
An example that shows `fn parse_query(...)` primes the next agent to
write a free function" (skill-editor.md).

### Prose discipline (prose.md)

The criterion: Hemingway's iceberg -- "a passage that reads as
dignified rests on seven-eighths the reader does not see." Default
ratio: one substantive primary-source block per 150-300 words.

Voice: declarative, present, unhedged. "Hedges ('perhaps,' 'it could
be argued that') are evidence the underlying claim is not yet earned."
"Use the word that names the thing. 'Smith' not 'artisan'; 'fire' not
'flame'" (prose.md).

Delete on sight: negative-contrast (the LLM tic -- "X is not Y. It
is Z"), filler phrases ("it is worth noting," "moreover," "delves
into"), meta-prose, stage-setting, the quote hype-up (prose.md).

Register test: "If it sounds like Hemingway translating Marcus
Aurelius for Juan Arnau to read, the register is right" (prose.md).

---

## XIII. Context Maintenance and Working Memory

### Two surfaces that decay together

Reports on disk and context in the live conversation. "A report is
just context saved to disk. The discipline is the same: keep
load-bearing substance; move it to its right permanent home; retire
what's done" (context-maintenance.md).

"The purpose of a context-maintenance pass is to reduce the number of
reports without losing information." Primary move is agglomeration --
merge reports on one topic into ONE report, then delete merged sources
(context-maintenance.md).

### Four actions per item (context-maintenance.md)

| Action | When |
|---|---|
| Forward | Substance still load-bearing as working artifact |
| Migrate | Substance mature enough for permanent home (skill, ARCH, ESSENCE, code) |
| Keep | Load-bearing on its own, no permanent home yet (rare) |
| Drop | Stale, addressed, superseded, with superseder and landing named |

"A report is not droppable just because a newer report exists. It is
droppable only after the load-bearing substance has landed in a
successor report or a permanent doc" (context-maintenance.md).

Per Spirit 1323: closed reports should not be kept merely for rationale
or history. The chosen design AND competing-alternatives reasoning both
migrate to durable surfaces; the report then retires
(context-maintenance.md).

---

## XIV. Privacy and Secrets

### Privacy (privacy.md)

> "Do not open, search, summarize, quote, or copy from private
> repositories unless the owning psyche explicitly asks you to work
> with private material." (privacy.md)

Every Spirit record carries a privacy Magnitude. Privacy Zero is open;
elevated narrows the audience. "Elevation NARROWS the audience without
claiming danger or hidden meaning" (privacy.md). Before writing to any
public surface, apply the leak test: "would this sentence still be safe
if every workspace agent and every public repo reader saw it?"
(privacy.md).

### Secrets (secrets.md)

> "A secret value never reaches the agent's eyes or any durable
> surface. This is not a preference; it is the load-bearing rule."
> (secrets.md)

Method: pipe source to sink (value lives only in pipe buffer and
process memory), verify blind (exit code, byte length, entry name --
never decrypt-to-check). Two layers: gopass (encrypts within user
session, git-backed) and sops-nix (carries secrets to cluster hosts,
decrypted only on target host at activation into runtime tmpfs at
`/run/secrets/<name>`). "The plaintext never enters the nix store"
(secrets.md).

---

## XV. Agent Discipline

### Autonomous agent (autonomous-agent.md)

"Before anything else in any session, check active beads." Active beads
outrank session-default behavior. Beads do not carry role labels; any
agent picks up any bead by topic affinity.

User prompt vs active bead: "The user's direct instruction wins. Beads
are durable intent; user prompts are live intent -- live always
overrides durable" (autonomous-agent.md).

### Keep working (keep-working.md)

> "When the psyche injects information mid-task, that is not a stop
> signal. Keep working." (keep-working.md)

Only explicit instruction to stop is an interruption. "Treating every
message as 'stop and await orders' turns the agent into a slack
surface instead of a working one" (keep-working.md).

### Human interaction (human-interaction.md)

Apex tier, every-session-read. Core rule: capture intent FIRST --
before editing any report, before writing code, before chat-responding.

Subagent dispatch: "Every `Agent` invocation sets
`run_in_background: true`. Never start a blocking subagent under any
circumstance. The rule is absolute" (human-interaction.md).

### Beads (beads.md)

BEADS is transitional -- "don't deepen the BEADS investment; design
new shapes assuming BEADS goes away." When to file: three conditions
must hold (discrete unit, needs cross-session memory, not
better-tracked elsewhere). Four anti-patterns: durable-backlog beads,
design questions as beads, ongoing concerns, bead-as-reminder.

"BEADS is never an ownership lock. Any agent may create, update,
comment on, or close BEADS tasks at any time" (beads.md). Feature
beads carry their branch name explicitly (beads.md).

### STT interpreter (stt-interpreter.md)

"Read for intent first. STT errors are almost always at the word level,
not the structural level." "Don't ask the user to spell things out."
Canonical spellings live on the filesystem: "the canonical spelling is
the directory name under `/git/github.com/<org>/<repo>/`"
(stt-interpreter.md).

---

## XVI. Workspace Vocabulary

Settled terms (workspace-vocabulary.md):

- **Version-pair: `main` / `next`** (Spirit 181, Maximum). "The active
  version is `main`; the version being upgraded to is `next`." The
  `-next` repo suffix is legacy.
- **Component name: `Persona`** (Spirit 215+216, Maximum).
  "Engine-management-as-noun" is the non-canonical form. Carve-out:
  "Persona engine" is specifically the AI-work scope.
- **Engine-management socket axis: `engine_management`** (Spirit
  199+240, Maximum). Predecessors: `supervisor`,
  `supervision_socket_path`.
- **Signal** -- the rkyv-archive-on-the-wire pattern. "The verb is to
  signal -- a component signals another by sending a length-prefixed
  rkyv archive on the wire" (rust/storage-and-wire.md).
- **Sema** -- today: typed-storage substrate. Eventually: "universal
  medium for meaning" (rust/storage-and-wire.md).
- **CriomOS** -- the flake describes the entire system
  (nix-discipline.md).

"When writing new content, use the canonical form. When editing an
existing surface that uses a predecessor, converge it in the same
edit" (workspace-vocabulary.md).

---

## XVII. Tensions and Contradictions

This section documents every place the corpus disagrees with itself
or where definitions drifted between files. None are resolved; all are
exposed for the reader's judgment.

### 1. Local-helper carve-out: abstractions.md vs rust/methods.md

`abstractions.md` establishes a "local-helper carve-out" as a
principled exception to the verb-belongs-to-noun rule: "small private
helper inside one module, genuinely local." But `rust/methods.md`
explicitly overrides this: "for Rust the local-helper carve-out from
`abstractions.md` does not apply -- even a small private helper goes
inside an `impl` block." This is an intentional override for Rust
specifically, but the two files present conflicting rules that an agent
working in Rust without reading `methods.md` would get wrong.

### 2. CLI: "eventually obsolete" vs universally required

`component-triad.md` states "The CLI is eventually obsolete machinery.
Keep CLI-side logic thin accordingly" but also states "Every
non-contract stateful component or daemon exposes a thin CLI control
surface, even when the CLI is not user-facing." The CLI is
simultaneously positioned as essential infrastructure (required of
every component) and as destined for obsolescence.

### 3. Test location: crate-layout.md vs operator.md

`rust/crate-layout.md` states definitively: "Unit tests do NOT go in
a `#[cfg(test)] mod tests` block at the bottom of the source file.
They live in a sibling file under `tests/` at the crate root." Yet
`operator.md` lists the operator's owned area as including "Tests
(every `tests/*.rs` and inline `#[cfg(test)]` modules)" -- implicitly
acknowledging `#[cfg(test)]` modules as a legitimate test surface the
operator owns. The `rust/methods.md` exemption for items inside
`#[cfg(test)]` modules further reinforces that such modules exist in
practice.

### 4. ARCHITECTURE.md: "what IS" vs speculative content

`architecture-editor.md` defines ARCHITECTURE.md as describing "what
the system IS at a specific scope. It is not a tour, not a tutorial,
not a history." Present tense throughout. But the same file declares
that "a Possible future design section is a standard part of every
architecture file" and that ARCHITECTURE.md "CAN carry possible
features, undecided designs, and open questions." This tension is
managed (the uncertainty sections sit after the cemented body and must
name uncertainty explicitly), but the document's identity as
"what IS" is complicated by the mandated inclusion of "what might be."

### 5. Sema naming: library vs eventual universal medium

`naming.md` explicitly addresses this as "different scopes get
different names": "`sema-db` (today's library) vs `Sema` (eventual
universal medium for meaning)." But across the corpus, `sema` is used
in both senses without always distinguishing: `rust/storage-and-wire.md`
uses "Sema" to refer to both the redb-based storage kernel and the
eventual universal medium in the same document ("Sema -- Today:
typed-storage substrate. Eventually: universal medium for meaning").
The six Sema operation classes in `component-triad.md` (Assert, Mutate,
Retract, Match, Subscribe, Validate) are presented as universal
cross-component classifications -- implying the "eventual" meaning --
yet they currently operate only through the `sema-engine` library
instance.

### 6. aski/nota lineage

`stt-interpreter.md` notes: "`aski/CLAUDE.md` formally disclaims aski
as an ancestor of nota/nexus." But the psyche's "lived sense is that
aski's design instincts inspired the current work." The corpus
instructs: "Honor the lived sense in conversation; flag the formal
disclaimer only when load-bearing." This is a documented internal
tension that the corpus itself chooses not to resolve.

### 7. Medium certainty: default level vs manifestation skip threshold

`intent-log.md` defines Medium as "The default. Preference, direction,
or lean without strong emphasis. When in doubt, Medium." But
`intent-manifestation.md` says to skip manifestation for
"Brainstorm-in-flight (Medium / Minimum certainty) -- wait until psyche
settles." This creates a zone where the most commonly assigned
certainty level (Medium) may or may not trigger manifestation,
depending on whether the content is judged as "brainstorm-in-flight."

### 8. "Signal" dual meaning

`component-triad.md` explicitly acknowledges this: "The word Signal
appears in both triads, and it refers to two distinct schema artifacts
emitted to two different `RustEmissionTarget`s." The public signal
contract (`WireContract`, zero engines) and the daemon-local signal
runtime (`SignalRuntime`, includes `SignalEngine` trait) share the name
"Signal" despite being different schema files with different emission
targets. This is not a contradiction but a documented naming overload
that the corpus flags as requiring careful attention.

### 9. Commit scope vs claim scope

`jj.md` mandates: "Commit the ENTIRE working copy -- `jj commit` with
no path arguments -- never path-scoped. Agents commit the ENTIRE
working copy, sweeping in all in-flight work." But `jj.md` also says:
"Lock selectively. When you must claim, claim only the specific files
or subfolders you will edit -- never the whole workspace." The
discipline intentionally separates claim scope (narrow) from commit
scope (everything), but this creates a practical tension: an agent
claims narrowly but commits broadly, sweeping in other agents'
unclaimed in-flight work.

### 10. Reports: per-response mandate vs selective use

`reporting.md` (per intent record 232) states: "The default operating
pattern for every agent is: every chat response is the paraphrase of
an accompanying per-response report." But `reporting.md` also says
"routine implementation commits are a named exception: the commit
description is the report for the code it lands." The per-response
report mandate is both universal and immediately qualified by
exceptions.

### 11. NOTA between components: blanket prohibition vs daemon edge

`component-triad.md` (per Spirit 1373, Maximum) states: "there is no
NOTA between live components." Yet the same document defines one of the
two daemon edges as accepting "inline NOTA argument, NOTA file path"
for the CLI. The resolution is that the CLI is the translation surface
between NOTA and binary, so NOTA enters the system at the CLI edge and
is translated before reaching the daemon -- but the CLI IS a component
process, and NOTA does enter it.

### 12. Context-maintenance meta-reports vs report reduction

`context-maintenance.md` states the goal: "reduce the number of
reports without losing information." But `context-maintenance-deep.md`
introduces an elaborate cross-lane meta-report directory structure
(`0-frame-and-method.md`, per-topic sub-reports, `N-overview.md`) that
itself produces multiple new reports as part of the reduction process.
The maintenance process temporarily increases the report count in order
to reduce it.

---

## Appendix A. Reports-Tree Distillate

*Distilled from 368 files across 16 subdirectories in
`reports/PreResetCorpus-2026-06-07/reports/`. Approximately 110 files
were read closely; the remainder were triaged by filename and keyword
search. All quotes are verbatim from source; citations use the
directory/report-number format of the reports tree.*

### A.1 Ethos / Nomos / Logos Ancestry

**The names ethos, nomos, logos appear nowhere in the pre-reset
corpus.** Their direct ancestors are the three planes of the engine
triad:

| Pre-Reset Name | Role | Post-Reset Mapping |
|---|---|---|
| **Signal** | Communication boundary; triage-only admission/reply | The communication/expression plane |
| **Nexus** | Decisions; the "translator" between Signal and SEMA; the feature catalog | The logic/reasoning plane |
| **SEMA** | Durable state; the single-writer storage plane | The meaning/knowledge plane |

The "translator" identity of Nexus is explicitly stated: *"Nexus --
the execution-IO plane; the recursive mail-keeper + Signal<->SEMA
translator that decides what to do"* (designer/548).

The eventual horizon for SEMA: *"Today, `sema` is the typed storage
kernel: a Rust library over redb + rkyv with a schema guard,
closure-scoped transactions, typed `Table<K,V>`. Eventually, `Sema`
is the universal medium for meaning -- a self-hosting computational
substrate (Sema-on-Sema), a fully-typed human-language representation
and universal interlingua, with content-addressed schema identity and
reducer-based migration"* (designer/548).

The whole-system vision: *"a typed, self-hosting medium for meaning
(Sema) carrying a universal computing paradigm (Criome), organized
and animated as a live meta-AI (Persona + spirit) that supervises a
federation of triad daemons as one running orchestrated whole. The
components are deliberately dumb mechanism; the thinking happens in
agent LLMs on the wire and in spirit -- without spirit, the persona
is mechanism alone"* (designer/548).

### A.2 The Three Planes as One Primitive

The reports tree carries the deepest formulation of the runtime triad,
going beyond the skill files' functional descriptions:

> "Every plane is a REACTION LANGUAGE: an engine matches an input tree
> against runtime state and produces a corresponding output tree. This
> is the deepest idea in the engine -- the three planes are not three
> different kinds of thing, they are *one* primitive projected three
> ways, differing only by ownership and runtime semantics, never by
> authored shape."
> -- designer/548

This "one primitive projected three ways" framing does not appear in
the skills corpus and is architecturally load-bearing for the Designer.

### A.3 The Nexus Runner Mechanism

The reports detail the runtime driver that the skills only sketch:

> "The decision plane is two enums and a five-way dispatch. `NexusWork`
> is the fact stream Nexus decides FROM. `NexusAction` is the command
> stream Nexus emits NEXT."
> -- operator/327/5

> "The runner is runtime-owned (`triad-runtime/src/runner.rs:149`,
> `Runner::drive`). It is a `loop` over the five `NextStep` outcomes:
> `Reply` exits; the other four each spend a budget step (default 32,
> `runner.rs:3`) and re-enter with completion work. Budget exhaustion
> returns a typed `budget_exhausted_reply`, never a panic."
> -- operator/327/5

### A.4 Plane Types and PlaneProjection

The planes were promoted to first-class types:

> "Promote the implicit plane axis into TWO first-class nouns --
> Plane (the node: per-plane naming) and PlaneProjection (the edge:
> cross-plane transforms)"
> -- designer/537

> "`PlaneProjection` -- the edge: directed plane-pair facts:
> `NexusWorkToNexusAction`, `NexusActionToSemaWrite`,
> `NexusActionToSemaRead`, `NexusActionToSignalOutput`,
> `SemaOutputToNexusWork`"
> -- designer/537

### A.5 The Three-Layer Boundary

The reports distinguish three layers that the skills corpus treats as
one:

> "The boundary is clean and three-layered: triad-runtime exposes the
> runner loop, role traits, frame codec, daemon shell, argument rule,
> trace, streaming -- all generic, no Spirit nouns. schema-rust-next
> emits (into `spirit/src/schema/*.rs`) the three engine traits, the
> `execute` default method that calls `triad_runtime::Runner`, the
> wire enums with their `encode/decode_signal_frame`, and the
> `impl triad_runtime::NexusAction for NexusAction` bridge. spirit
> hand-writes the three impls (`SignalActor`, `Nexus`, `Store`), the
> composition objects (`Engine`, `Daemon`, `SpiritDaemonRuntime`,
> `SignalTransport`), and the component-specific behavior."
> -- operator/327/5

### A.6 The Daemon Shape Debate

Three proposals were developed for the emitted daemon shape. This
debate is absent from the skills corpus entirely.

**Proposal A -- Sync Thread-per-Request:** *"I take the hard position:
the schema-derived daemon layer is sync thread-per-request, and kameo
does NOT belong in it. Not one of the five consumers has a genuine
actor need at the DAEMON boundary"* (cloud-designer/34/1).

**Proposal B -- Actor-Native Generated Daemon:** *"The decisive
observation from reading the five consumers: every one of them is
already an actor system wearing a thread costume. Five components,
five hand-rolled actor systems, five different costumes"*
(cloud-designer/34/2).

**Proposal C -- Merit-Chosen Archetypes (WINNER):** *"Two archetypes,
not one and not five. The schema-declared property that selects the
archetype is the disposition of a request's reply -- does a request
produce exactly one reply and then the connection is done, or can a
request subscribe the connection to a stream of later events?"*
(cloud-designer/34/3).

The synthesis: *"The winner is Proposal C, corrected to the
intent-decided three-plane-engine surface: a sync thread-per-request
daemon driving the Signal/Nexus/SEMA engine traits, with everything
else generated"* (cloud-designer/34/5). *"B is the right eventual
picture and a real liability now (async-rewrite of five 100%-sync
engines for machinery intent has deferred). C is the today shape"*
(cloud-designer/34/5).

The two archetypes: `ReplyOnce` (request/reply) and
`ReplyThenSubscribe` (streaming, a strict superset adding one owned
noun: the writer registry) (cloud-designer/34/5).

### A.7 Actor-Native Engine Rewrite Design (Deferred)

A design for eventual actor migration was developed but deferred:

> "the engine traits' computation stays sync-pure; only the actor shell
> is async. The `NexusWork -> NexusAction` mechanism (Spirit `1486`)
> already expresses effects as data -- `decide` returns
> `CommandSemaWrite`/`CommandSemaRead`/`CommandEffect`/
> `ReplyToSignal`/`Continue` values, it never performs them. So there
> is nothing in the logic to `.await`; the async driver performs the
> actions."
> -- designer/553/2

Key hazard: *"The single sharpest hazard, named by two readers
independently: a naive one-actor-per-daemon mapping (everything
through one mailbox) re-serializes exactly what `2alg`/`k6w1`/`tj99`
made concurrent"* (designer/553/1).

### A.8 Daemon Configuration and Bootstrap

The reports add bootstrap details the skills only sketch:

> "Daemons cannot understand NOTA (Spirit e6ri). A daemon's single
> startup argument is a pre-generated signal-encoded (rkyv) Configure
> message; bootstrap depends on NO manager (persona-FD-handoff was
> rejected -- a manager dependency is circular and fragile); a virgin
> daemon (empty store) applies the Configure as first config, a daemon
> with a populated store self-resumes from it; the same Configure type
> is accepted live over the meta socket."
> -- designer/550-v2

> "Config is a reaction (`8qxm`), with one vocabulary. The `Configure`
> the daemon reads at boot is the same message type it accepts live
> over the meta socket -- two delivery channels (startup argument,
> meta socket), one schema."
> -- designer/550-v2

### A.9 The Emitted Daemon Module (triad_main)

> "schema-rust-next now emits a COMPLETE daemon spine (the
> `triad_main!`-equivalent -- `ComponentDaemon`/`DaemonEntry` trait
> pair, `GeneratedDaemonRuntime`, `DaemonCommand`, two-socket bind,
> `ConnectionContext` threading, `ExitReport` exit)"
> -- cloud-designer/32/1

> "triad_main! is an EMITTED source-visible `src/schema/daemon.rs`,
> not a literal macro."
> -- system-designer/80

Corrected recipe: (1) Declare a `NexusDaemonShape` in `build.rs`.
(2) Turn on the daemon emitter. (3) Hand-write only
`impl ComponentDaemon`. (4) Bin is a one-liner:
`XDaemon::run_to_exit_code()`. (5) Delete the hand-written daemon
boilerplate (system-designer/80).

### A.10 The Schema Pipeline

The reports describe the full pipeline that the skills reference only
in passing:

> "A schema file is full NOTA -- schema is a specialized NOTA dialect
> built on structural macro nodes, NOT a separate language that lowers
> into NOTA. The canonical flow is:
> 1. Authored schema (NOTA) DESERIALIZES -- via the structural macro
>    node codec -- directly into
> 2. schema-in-rust: typed Rust that fully defines the schema,
>    rkyv-serializable, a faithful CANONICAL-round-trip image;
> 3. schema-in-rust then LOWERS into Rust interface code (the emitter
>    does Rust projection, not schema semantics)."
> -- system-designer/73/1

> "The load-bearing change versus all prior design: ASSEMBLED SCHEMA
> (Asschema) is REMOVED. There is no separate assemble step and no
> public SchemaResolution IR."
> -- system-designer/73/1

The structural macro node mechanism: *"A structural macro node is a
NOTA enum decoded by SHAPE, not by a data tag. The enum TYPE is the
whole specification: decode is TYPE-DIRECTED -- the codec performs a
structural match on each variant in declaration order, first structural
match wins, then decodes that variant's data, RECURSIVELY"*
(system-designer/73/1).

Each `.schema` file is exactly: block 1 `{}` imports brace; block 2
`[]` Input root enum; block 3 `[]` Output root enum; block 4 `{}`
namespace of user-defined types (system-designer/73/2).

### A.11 Wire Protocol Layers

The reports clarify the two-layer framing that the skills describe
only as "length-prefixed rkyv":

Inner frame (schema-rust-next generated): `encode_signal_frame`
produces `[u64 LE short_header][rkyv archive]` -- an 8-byte
little-endian discriminant header followed by the rkyv body. No length
prefix at this layer (cloud-designer/32/5).

Outer transport frame (triad-runtime `LengthPrefixedCodec`): wraps the
inner bytes in a `[u32 BE length][body]` envelope with a
`MaximumFrameLength` guard (cloud-designer/32/5).

### A.12 Cross-Crate Schema Import

The Cargo `links` seam is the mechanism for schema sharing:

> "`emit_schema_directory` is the PUBLISH side of the Cargo `links`
> seam: it prints `cargo::metadata=schema-dir=<crate_root>/schema`.
> Because the crate declares `links = \"signal-cloud\"`, Cargo
> re-exposes that metadata to DIRECT dependents as the env var
> `DEP_SIGNAL_CLOUD_SCHEMA_DIR`. This is how a contract crate
> publishes its schema directory to the daemon."
> -- cloud-designer/25/1

### A.13 Two NOTA/Schema Lineages

> "There are two distinct schema/nota lineages and they must not be
> conflated. The `nota-codec` family is separate from the `nota-next`
> / `schema-next` / `schema-rust-next` family (schema-next depends on
> `nota-next`, not `nota-codec`)."
> -- system-designer/65/3

### A.14 Workspace Migration State

> "the ecosystem is mid-migration through three parallel kernel swaps
> -- wire (`signal-frame` NEW replacing `signal-core` OLD), NOTA
> (`nota-next` NEW replacing `nota-codec` OLD), and schema
> (`schema-next` + `schema-rust-next` NEW replacing `schema` OLD) --
> over a new shared runtime (`triad-runtime`) and storage engine
> (`sema-engine`) on the kept `sema` kernel."
> -- designer/551

> "`spirit` is the proven clean reference -- fully on the new spine
> with zero nota-codec, confirming the new spine is end-to-end viable
> for a real daemon."
> -- designer/551

Spirit is a named bootstrap exception that keeps all three planes in
one repo: *"Spirit is explicitly the single-repo ALL-IN-ONE pilot --
a NAMED bootstrap exception (lc2r/l6zw), NOT the canonical >=3-plane
split"* (operator/327/5).

Active repository count at corpus date: 77 repositories (58 in the
current core stack, 16 adjacent active, 3 in the replacement stack)
(operator/303/3).

### A.15 Message and Router as Separate Components

> "keep separate. They sit at two different trust depths and own two
> different durable facts. The load-bearing reason against merge is not
> line-count -- it is that merging re-internalizes an untrusted,
> externally-writable door into the same address space that holds the
> durable ledger and the channel-authority core."
> -- system-designer/76/1

Socket permissions enforce the boundary: `message.sock` = 0660
(engine-owner group -- the external door); `router.sock` = 0600
(owner-only) (system-designer/76/1).

### A.16 Design Principles from the Reports Tree

These principles appear in the reports but not (or not as clearly) in
the skills corpus:

**Mechanism vs agent cognition:** *"Anything that can be done
mechanically will not be done by agents. Agents are the cognitive
layer; mechanism handles every decision code can make"*
(designer/552/1). *"Anything with a deterministic correct answer
derivable from its input -- routing, dispatch, lookup, classification,
projection, address resolution -- is mechanism, not agent work"*
(designer/552/11).

**Implementation cost:** *"disregard implementation cost completely;
the better long-term logic always wins"* (designer/552/1). Confirmed
by ESSENCE.md ("Not estimates. Implementation timelines do not appear
in design discussions").

**Configuration as policy state:** *"Daemon configuration is always a
Mutate: the way a daemon is configured is integral durable state, not
optional side-state, and it changes through the same authority chain
(owner/meta-signal Mutate) as any other state mutation"*
(designer/552/2). Confirmed by component-triad.md invariant 5.

**Mind-Orchestrate authority:** *"The Mind-to-Orchestrate authority
relationship follows the human mind-body analogy: Orchestrate (body)
has substantial autonomy and does much of its work without Mind's
intervention, while Mind (mind) does much that never touches
Orchestrate"* (designer/552/2).

**Contract-local verbs -- prefer many named verbs:** *"Verbs are
cheap and clarifying -- do not fear adding them. When the choice is
between one verb covering many sub-actions and multiple verbs each
naming a sub-action, prefer multiple named verbs"* (designer/552/2).
Confirmed by contract-repo.md.

**The Nexus feature-catalog rationale:** *"A feature is FIRST a Nexus
verb/object, THEN implemented by the hand-written runtime object --
never inline hidden logic. This is why 'no free functions' is a hard
rule: a free function is an undeclared capability, a feature that
escapes the catalog"* (designer/548).

### A.17 Contract Crate and Daemon Crate Canonical Structures

The reports provide file-level detail the skills do not:

**Contract crate** (cloud-designer/25/1):
- `Cargo.toml` with `links = "signal-<component>"`, `build = "build.rs"`
- `build.rs` that publishes schema directory and emits WireContract
- `schema/lib.schema` -- the authored wire schema
- `src/lib.rs` -- hand-written wire nouns + generated schema module
- `src/schema/lib.rs` -- CHECKED-IN generated wire types
- `tests/round_trip.rs` -- rkyv + NOTA round-trips

**Daemon crate** (cloud-designer/25/1):
- `build.rs` -- emits daemon_runtime (nexus+sema)
- `schema/nexus.schema` -- Nexus plane schema (daemon-local)
- `schema/sema.schema` -- SEMA plane schema (daemon-local)
- `src/schema/nexus.rs` -- CHECKED-IN generated Nexus runtime
- `src/schema/sema.rs` -- CHECKED-IN generated SEMA runtime
- `src/schema_runtime.rs` -- hand-implemented SchemaRuntime

### A.18 Sema Storage Details

Confirmed by reports: *"sema-engine is the intended exclusive database
boundary. Component daemons do not open redb, define redb tables, run
redb transactions"* (system-designer/63). A bypass cohort was
identified using raw redb: spirit (new), chroma, orchestrator,
schema-next.

New from reports: Component database files should carry a `.sema`
extension, not `.redb` -- *"hiding redb behind our own file type so
the name states it is specifically a sema-redb database"*
(system-designer/63).

The `signal-sema` naming problem: *"There is no `signal-nexus` and no
`signal-signal` (404) -- so it is not a per-plane pattern; it's an
asymmetric one-off. There is no `sema` daemon (`sema` is a library),
so `signal-sema` is not the contract of anything. It is actually the
cross-component SEMA-operation observer vocabulary"*
(system-designer/83).

---

## Appendix B. Reports-Tree Tensions

These tensions surface from the reports tree. Where they overlap with
tensions already documented in section XVII (from the skills corpus),
they are cross-referenced. Where they add new evidence, both are kept.

### B.1 Actor-Systems vs Component-Triad: The Unreconciled Fork

The single sharpest architectural contradiction in the entire
pre-reset corpus, surfaced only in the reports tree:

> "The sync generated stack rests on two genuinely recorded decisions
> -- a thread-per-connection concurrency model (`2alg`/`k6w1`/`tj99`)
> and a dated deferral of the actor-mailbox/scheduling machinery
> (`1483`/`1487`=`czw0`) -- both written into
> `skills/component-triad.md` as 'the substrate that lands now.' But
> those decisions sit in direct, unreconciled contradiction with
> `skills/actor-systems.md`, which says in the present tense 'Actors
> all the way down'."
> -- cloud-designer/35/4

> "The root cause is that the workspace shipped two contradictory
> pieces of guidance and nobody reconciled the two files."
> -- cloud-designer/35/4

Code reality at time of writing: *"Definitive kameo check (Cargo.toml
AND Cargo.lock) across all seven: zero kameo dependencies, zero
transitive kameo nodes, zero tokio/async-runtime"*
(cloud-designer/35/2).

Proposal C was the practical resolution (sync now, actors deferred).
This is a deeper instance of skills-corpus tension #2 (CLI "eventually
obsolete" vs universally required) -- the entire actor doctrine was
aspirational while the codebase was sync.

### B.2 Cloud's Actor Mandate vs Code Reality

> "cloud's `ARCHITECTURE.md` 'Actor Shape' IS a present-tense
> actor-per-concern mandate -- but it is aspirational/stale text,
> frozen since birth, contradicted by the same file and by every line
> of cloud's actual code."
> -- cloud-designer/36/3

> "cloud is the sharpest instance of the actor divergence in the
> workspace, and the least defensible."
> -- cloud-designer/36/8

### B.3 triad_main: Macro Name vs Emitted Reality

Early reports: *"there is no `triad_main!` and no `macro_rules!` for
it anywhere"* (operator/327/5). Later reports: *"triad_main (the
emitted daemon module) LANDED on main"* (system-designer/80).
Resolution: it was never a macro; what was built was an emitted source
file (`src/schema/daemon.rs`). The name persisted as shorthand.

### B.4 Emitted Daemon: Serial vs Concurrent

*"the emitted spine is SERIAL and UNHARDENED"* (cloud-designer/32/1)
vs BoundedWorkers having landed in triad-runtime (system-designer/80).
The reports disagree on whether the emitter integrated BoundedWorkers
or whether lojix's hand-written daemon remained the concurrency
reference.

### B.5 Asschema: Intent Says Removed, Code Says Present

Intent: *"ASSEMBLED SCHEMA (Asschema) is REMOVED"*
(system-designer/73/1). Code: *"In source, asschema is present, live,
and explicitly retained as a compatibility surface in both schema-next
and schema-rust-next. Removal is the stated TARGET, not the landed
state"* (system-designer/73/4). A later commit (cloud-designer/32/3)
confirms eventual retirement from schema-next.

### B.6 Owner-Signal vs Meta-Signal: Decided but Unexecuted

Decided: *"MetaSignal is the canonical name; OwnerSignal is
deprecated"* (system-designer/77/3). Unexecuted: *"grep for
`meta-signal` / `meta_signal` / `MetaSignal` across all four
spirit-triad repos returns zero matches. A grep for `owner-signal`
returns 30+ matches"* (system-designer/59/4). Twelve repos were still
pending rename at corpus date.

### B.7 Spirit Identity: persona-spirit vs spirit-next vs spirit

Three repos serve overlapping but different roles: *"persona-spirit is
the deployed Spirit but its architecture is the pre-engine-trait Kameo
actor tree. The cutover gap from spirit-next (engine-trait worked
example) to persona-spirit (deployed) is unmigrated"*
(system-designer/51/2). The corpus sometimes conflates them.

### B.8 Contract Boundary Violations in Practice

> "`signal-upgrade` and `meta-signal-upgrade` clearly violate the
> contract boundary. They check in public contract schemas, generated
> Rust, and tests that expose Nexus and SEMA roots plus engine traits."
> -- operator/309

Several older contracts exposed SEMA-class verbs (`Assert`, `Match`,
`Subscribe`, `Retract`, `Mutate`, `Validate`) as public wire
operations, violating the rule from contract-repo.md (per psyche
2026-06-04, record 2612) that "Sema classification vocabulary is
forbidden on the public contract wire."

---

## Appendix C. Coverage Statement

### Reports-tree directories yielding the most architecture content

1. **cloud-designer/** (81 files) -- daemon shape proposals, actor
   divergence forensics, wire contract designs, daemon emitter
   integration.
2. **system-designer/** (89 files) -- engine forward exploration,
   message router architecture, nota-codec entanglement, repo audits,
   triad migration scoreboard.
3. **operator/** (71 files) -- schema-nota-triad study, triad-main
   audit, signal-contract boundary audit, engine stack implementation.
4. **designer/** (31 files) -- legacy intent salvage, actor-native
   engine rewrite, plane type design, persona meta-engine vision.

### Directories read closely

- cloud-designer/ -- ~60 of 81 files
- system-designer/ -- ~50 of 89 files
- operator/ -- ~40 of 71 files
- designer/ -- ~20 of 31 files
- system-operator/ -- ~10 of 39 files

### Directories skimmed (keyword search, selective reads)

- cloud-operator/ (26 files) -- cloud schema triad blockers and
  domain prototype; remainder operational.
- second-designer/ (2 files) -- counter-ego audit; no new architecture.
- pi-operator/ (7 files) -- deploy/lojix wrapper research; tangential.

### Directories skipped

- assistant/ (3 files) -- role registration, privacy operations.
- cluster-operator/ (1 file) -- Zeus local update authority.
- counselor/ (3 files) -- role registration, spirit privacy substrate.
- nota-designer/ (0 files) -- empty directory.
- poet/ (1 file) -- no architecture content.
- second-operator/ (0 files) -- empty directory.
- third-designer/ (0 files) -- empty directory.
- videographer/ (2 files) -- no architecture content.
