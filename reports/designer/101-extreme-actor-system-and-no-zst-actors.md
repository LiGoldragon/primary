# 101 — Extreme actor system + no-ZST actors — designer companion to operator/102

*Designer report. Operator/102
(`~/primary/reports/operator/102-actor-heavy-persona-mind-research.md`)
makes the actor-as-correctness-device case and surveys the
Rust actor framework field. This designer companion adds two
moves to that direction: (1) pushes the actor-density rule
to "every non-trivial logical step is an actor" with a
principled boundary for where the rule stops, and (2)
dissolves the ZST-actor pattern that ractor's trait shape
forces, by making the actor type carry the actor's data —
no separate `State` shell. Together these produce the elegant
interface the user is reaching for: actors as named, typed,
data-bearing participants, not behavior markers.*

---

## 0 · TL;DR

Operator/102's thesis (*"actors as a correctness device, not
a performance device; every phase that has a name and a
failure mode deserves an actor"*) is right and stays. This
report sharpens two questions operator/102 leaves loose.

**Move 1 — push density, with a principled boundary
(§1 + §3).** *"Every non-trivial logical step is an actor"*
is the right rule. *"Non-trivial"* needs a discriminator so
agents know where the rule stops. Proposed: a step gets an
actor when **all three** are true: it has a *typed name in
the domain*, it has a *failure mode that callers care about*,
and it has *independent testability*. Pure deterministic
transformations (e.g. *"strip trailing slash"*,
*"base32-encode bytes"*) stay as methods on the parent
actor's state. Hundreds of actors per process is normal at
scale; thousands at component scale.

**Move 2 — dissolve the ZST-actor pattern (§2 + §4 + §5).**
ractor's `Actor` trait forces a `pub struct ClaimNormalize;`
ZST whose only purpose is to hold trait-impl methods that
delegate to a separate `State` type. This is exactly the
*"no ZST method holders"* anti-pattern in
`~/primary/skills/rust-discipline.md` — the type carries no
data; the data lives one type away; the actor type is a
namespace label, not a noun. The user's philosophical
argument is right: types should carry their qualities;
empty types are labels, not types. The fix is the
**`PersonaActor` trait** in §4 — `Self` IS the actor's data;
`open` constructs `Self`; `handle(&mut self, msg)` mutates
`Self`. ractor compatibility lives in the wrapper layer
(`persona-actor` per operator/102 §6), invisible to consumer
code.

**Move 3 — agent-thinking scaffolding (§6).** Agents fall
back to method calls because the actor model isn't in their
default vocabulary. The fix isn't more documentation; it's
*architectural-truth tests that fail when an agent collapses
an actor into a helper method*. Plus a project-template
shape that makes the actor scaffold the path of least
resistance.

§7 names the persona-actor crate's discipline pieces; §8
names the skill updates this requires.

---

## 1 · The density rule — "every non-trivial logical step"

Operator/102 §4 names the rule loosely: *"if a phase has a
name and a failure mode, it probably deserves an actor."*
The "probably" is where agents lose discipline. They reason:
*"this step is small / fast / pure — does it really need an
actor?"* — and collapse it into a helper method.

**Sharper rule — three-part conjunction:**

A logical step gets its own actor when **all three** are true:

1. **Typed domain name** — the step is something the workspace
   would name as a noun (`ClaimNormalize`, `EdgeValidate`,
   `IdMint`), not a verb-on-existing-data
   (`strip_trailing_slash`, `lowercase`).
2. **Failure mode callers act on** — the step can produce a
   typed `Failure` value that downstream code matches against.
   *"Returns `Result<T, !>` because it always succeeds"*
   means it's not actor-shaped.
3. **Independent testability** — the step's input/output is
   typed enough that a test can submit synthetic input and
   assert the output without standing up its callers. Pure
   transformations of one byte string into another don't
   need an actor for testability — a unit test on the method
   is identical.

When all three are true: actor. When any one fails: method
on the parent actor's state.

### Worked discrimination

| Step | Has typed domain name? | Has caller-acted failure? | Independently testable? | Verdict |
|---|---|---|---|---|
| Normalize a path scope | Yes (`ScopeNormalize`) | Yes (`PathNotAbsolute`, `EscapesRoot`) | Yes (synthetic strings → typed result) | **Actor** |
| Detect claim-scope conflict | Yes (`ClaimConflict`) | Yes (`Conflict { conflicting_role, conflicting_scope }`) | Yes | **Actor** |
| Mint a `DisplayId` | Yes (`IdMint`) | Yes (`CollisionExhausted` is impossible but `IndexUnreachable` is real) | Yes | **Actor** |
| Strip trailing slash | No (verb-on-string) | No (always succeeds) | Trivially | **Method** on `ScopeNormalize` |
| BLAKE3-encode bytes | No (verb-on-bytes) | No | Trivially | **Method** on `IdMint` |
| Base32-crockford encoding | No | No | Trivially | **Method** on `IdMint` |
| Validate target item exists for an `EdgeAdd` | Yes (`TargetResolve`) | Yes (`UnknownItem`) | Yes (synthetic store + target) | **Actor** |
| Update the `META` schema-version counter on commit | Yes (`SchemaCounter`) | Yes (`VersionMismatch`) | Yes | **Actor** |

This rule produces hundreds of actors per component without
producing thousands of trivial wrappers. It also gives agents
a one-question check at edit time: *"would I want to test
this independently with synthetic input?"*

### Density at scale

For `persona-mind` Phase 1, this rule plus operator/102 §4's
already-listed actors yields ~80–120 actor types in the
crate. Per-instance counts (one `ItemActor` per open item;
one `RequestSessionActor` per in-flight request) scale by
workload. Operator/102 §10.7 *"actor count and residency
tests"* covers the runtime-cost validation; the design
question (this report) is structural.

---

## 2 · The ZST-actor problem

ractor's trait forces this shape (paraphrased from
`/home/li/primary/repos/lore/rust/ractor.md` and ractor's own
docs):

```rust
// The actor "type" — empty; carries no data.
pub struct ClaimNormalize;

// The actor's state — the actual data lives one type away.
pub struct ClaimNormalizeState {
    config:    NormalizationConfig,
    in_flight: HashMap<RequestId, PathBuf>,
    metrics:   Metrics,
}

// Arguments for construction.
pub struct ClaimNormalizeArgs {
    config: NormalizationConfig,
}

// Messages.
pub enum ClaimNormalizeMsg {
    Normalize { request: RequestId, path: WirePath, reply: RpcReplyPort<NormalizeResult> },
}

// The trait impl — methods take &self (the empty ZST) plus state.
impl Actor for ClaimNormalize {
    type State     = ClaimNormalizeState;
    type Arguments = ClaimNormalizeArgs;
    type Msg       = ClaimNormalizeMsg;

    async fn pre_start(&self, _myself, args) -> Result<Self::State, _> {
        Ok(ClaimNormalizeState {
            config:    args.config,
            in_flight: HashMap::new(),
            metrics:   Metrics::default(),
        })
    }

    async fn handle(&self, _myself, msg, state) -> Result<(), _> {
        match msg {
            ClaimNormalizeMsg::Normalize { request, path, reply } => {
                let result = state.normalize(path);  // ← state has the methods
                let _ = reply.send(result);
                Ok(())
            }
        }
    }
}
```

`ClaimNormalize` is the type the world sees. It carries no
data. Every method that does real work is on `ClaimNormalizeState`,
which is a *different type* the world doesn't see — it lives
one indirection away, accessed only through the trait's
`state` parameter.

This is the *exact* anti-pattern named in
`~/primary/skills/rust-discipline.md` §"No ZST method holders":

> *"A `pub struct Foo;` whose `impl Foo` is just a parking
> lot for functions that do real work on data they don't
> carry is a free function in namespace clothing. The ZST is
> a label, nothing more — the type doesn't track what the
> work operates on, only what it's named after."*

The skill's current ractor exception (*"Marker types required
by external frameworks — ractor actor behaviour markers …"*)
is a pragmatic compromise with the framework's shape. The
user's philosophical argument is that we shouldn't compromise:

> *"Types, anything even an abstract concept, hold data. Like
> its qualities, for example. Like laziness can be said to
> be undesirable. So actors have, and also all actors are
> going to have some sort of state."*

A type that names a thing should carry the thing's qualities.
An actor type should carry the actor's qualities. There IS
no actor with no qualities — even the most "stateless"
dispatcher has routing tables, supervision links, identity.
The ZST exists because the framework couldn't figure out
where the data should live; it's not a feature.

### Why the workaround matters

When the actor's data lives one type away:

- **Methods float between types.** `state.normalize(path)` is a
  method on the State; the actor type's `handle` is a switch
  statement that delegates. Two types per actor; the verb
  belongs to whichever one the framework accepts.
- **Construction is split.** `pre_start` constructs the State
  from `Arguments`; the actor type plays no role in its own
  construction. The "actor" doesn't construct itself; the
  framework constructs the State for it.
- **Testing the State requires sidestepping the actor.** Unit
  tests pull `ClaimNormalizeState` out of the actor wrapping
  to test methods directly — bypassing the very actor
  boundary operator/102 wants tests to enforce.
- **Naming gets ugly.** `ClaimNormalize` (the actor),
  `ClaimNormalizeState` (the data), `ClaimNormalizeArgs` (the
  constructor input), `ClaimNormalizeMsg` (the messages),
  `ClaimNormalizeReply` (replies). Five types per concern,
  none of which is the noun.

The fix is to remove the split. There's one type, it carries
the data, it constructs itself, methods on it do the work,
and the framework adapts to *that* shape — not the other way
around.

---

## 3 · Dissolving the ZST: actor type IS state type

The proposed shape (illustrative; full trait in §4):

```rust
/// The actor — its type IS its data. No ZST shell, no
/// separate State, no Arguments-vs-State split.
pub struct ClaimNormalize {
    config:    NormalizationConfig,
    in_flight: HashMap<RequestId, WirePath>,
    metrics:   Metrics,
}

impl ClaimNormalize {
    /// Construction of the actor IS construction of self.
    /// The "actor type" and "state type" are the same noun.
    pub fn open(arguments: ClaimNormalizeArguments) -> Result<Self, ClaimNormalizeFailure> {
        Ok(Self {
            config:    arguments.config,
            in_flight: HashMap::new(),
            metrics:   Metrics::default(),
        })
    }

    /// The verb that does real work. Operates on self's data
    /// directly. Verb belongs to the noun whose data it reads
    /// and writes.
    pub fn normalize(&mut self, path: WirePath) -> Result<NormalizedScope, ClaimNormalizeFailure> {
        // … pure method on the actor's data …
    }
}

impl PersonaActor for ClaimNormalize {
    type Argument = ClaimNormalizeArguments;
    type Message  = ClaimNormalizeMessage;
    type Reply    = ClaimNormalizeReply;
    type Failure  = ClaimNormalizeFailure;

    fn open(arguments: Self::Argument) -> Result<Self, Self::Failure> {
        Self::open(arguments)
    }

    async fn handle(&mut self, message: Self::Message) -> Result<Self::Reply, Self::Failure> {
        match message {
            ClaimNormalizeMessage::Normalize { path } => {
                let scope = self.normalize(path)?;
                Ok(ClaimNormalizeReply::Normalized { scope })
            }
        }
    }
}
```

What changed:

- **One type per actor.** `ClaimNormalize` carries `config`,
  `in_flight`, `metrics`. The same type appears in trait
  impls, in handle types, in test fixtures.
- **Self-construction.** `ClaimNormalize::open(args)` returns
  `Self`. The actor constructs itself; the framework hosts
  the result.
- **Methods on the noun.** `self.normalize(path)` is a method
  on `ClaimNormalize`. The verb attaches to the noun whose
  data it touches.
- **Tests target the noun directly.** A unit test calls
  `ClaimNormalize::open(args)?.normalize(path)?` and asserts
  on the result — no actor framework needed for the
  reducer-shaped test, but the actor framework wraps the
  same noun for runtime hosting.
- **Three associated types instead of five.** `Argument`,
  `Message`, `Reply` (`Failure` is the typed error per
  `~/primary/skills/rust-discipline.md` §"Errors"). The State
  type and Args-vs-State split disappear.

### What about supervisors?

Same shape. A supervisor's data is its children's handles
plus its supervision policy:

```rust
pub struct ClaimSupervisor {
    normalize: ActorHandle<ClaimNormalize>,
    conflict:  ActorHandle<ClaimConflict>,
    collapse:  ActorHandle<ClaimCollapse>,
    policy:    SupervisionPolicy,
}

impl PersonaActor for ClaimSupervisor {
    type Argument = ClaimSupervisorArguments;
    type Message  = ClaimSupervisorMessage;
    type Reply    = ClaimSupervisorReply;
    type Failure  = ClaimSupervisorFailure;

    fn open(arguments: Self::Argument) -> Result<Self, Self::Failure> {
        Ok(Self {
            normalize: ActorHandle::spawn_under(&arguments.parent, normalize_args)?,
            conflict:  ActorHandle::spawn_under(&arguments.parent, conflict_args)?,
            collapse:  ActorHandle::spawn_under(&arguments.parent, collapse_args)?,
            policy:    arguments.policy,
        })
    }

    async fn handle(&mut self, message: Self::Message) -> Result<Self::Reply, Self::Failure> {
        match message {
            ClaimSupervisorMessage::Normalize { path } => {
                let normalized = self.normalize.ask(ClaimNormalizeMessage::Normalize { path }).await?;
                Ok(ClaimSupervisorReply::Normalized { /* … */ })
            }
            // … other variants …
        }
    }
}
```

The supervisor IS its state — owns its children's handles
as fields. No ZST anywhere; the qualities of the supervisor
(which children, what policy) are visible on the type itself.

### What if an actor truly has nothing to carry?

It doesn't exist. Even the most "empty" actor has:

- A name (the type itself; `ActorKind` derives from
  `type_name<Self>()`).
- A supervision link to its parent.
- Possibly a creation timestamp.
- Possibly metrics counters.

If your design produces an actor whose `Self { }` is empty,
the actor isn't doing anything load-bearing — it's a label,
not a noun. Per §1's discriminator, that step doesn't pass
the "typed domain name + failure mode + testability" rule;
it's a method on its parent.

The user's philosophical point applies: there's no actor
without qualities; if you find one, you've found a label
masquerading as a type.

---

## 4 · The `PersonaActor` trait — design code

The full trait `persona-actor` exposes:

```rust
pub trait PersonaActor: Sized + Send + 'static {
    /// Construction input. Carries everything the actor needs
    /// to assemble its initial data.
    type Argument: Send;

    /// The closed message vocabulary this actor accepts.
    type Message: Send + 'static;

    /// The closed reply vocabulary this actor produces.
    type Reply: Send + 'static;

    /// Typed failure (per `~/primary/skills/rust-discipline.md`
    /// §"Errors") — never `anyhow`.
    type Failure: std::error::Error + Send + 'static;

    /// Build the actor's data from arguments. The returned
    /// Self IS the runtime actor; no separate State type.
    fn open(arguments: Self::Argument) -> Result<Self, Self::Failure>;

    /// Handle one message. Operates on self's data directly.
    /// The reply travels back through the handle's reply port.
    async fn handle(
        &mut self,
        message: Self::Message,
    ) -> Result<Self::Reply, Self::Failure>;

    /// Optional cleanup hook before the actor's data drops.
    /// Default: no-op.
    async fn close(self) -> Result<(), Self::Failure> {
        Ok(())
    }

    /// Stable typed identity for trace + manifest comparison
    /// (per operator/102 §10.1).
    fn kind() -> ActorKind {
        ActorKind::from_type_name::<Self>()
    }
}
```

The handle that consumers use:

```rust
pub struct ActorHandle<A: PersonaActor> {
    sender: ActorSender<A::Message>,
    join:   ActorJoin,
    kind:   ActorKind,
    path:   ActorPath,
}

impl<A: PersonaActor> ActorHandle<A> {
    /// Spawn `A` under `parent`'s supervision.
    pub fn spawn_under(
        parent: &impl SupervisorRef,
        arguments: A::Argument,
    ) -> Result<Self, SpawnFailure<A::Failure>> {
        // Wrapper: A::open(arguments)? produces Self of A.
        // The wrapper hosts that Self in ractor's loop,
        // adapting between PersonaActor's shape and ractor's
        // ZST-shaped trait. Consumer never sees the
        // adaptation.
    }

    /// Send a message; await the reply. The typed reply port
    /// is constructed inside the wrapper.
    pub async fn ask(&self, message: A::Message)
        -> Result<A::Reply, AskFailure<A::Failure>>;

    /// Send a message; don't wait. Useful for fire-and-forget
    /// notifications.
    pub fn tell(&self, message: A::Message)
        -> Result<(), TellFailure>;

    /// Topology introspection — the typed path of this actor
    /// in the supervision tree (per operator/102 §10.1).
    pub fn path(&self) -> &ActorPath { &self.path }
}
```

### The ractor adapter

`persona-actor` wraps ractor internally — the consumer-facing
trait is `PersonaActor`; the runtime hosts it via a generic
ractor adapter:

```rust
/// Internal — never imported by consumer crates.
struct RactorAdapter<A: PersonaActor>(PhantomData<A>);

impl<A: PersonaActor> ractor::Actor for RactorAdapter<A> {
    type State     = A;                             // ← Self IS the state
    type Arguments = A::Argument;
    type Msg       = AdapterMessage<A>;

    async fn pre_start(
        &self,
        _myself: ActorRef<Self::Msg>,
        arguments: Self::Arguments,
    ) -> Result<Self::State, ActorProcessingErr> {
        A::open(arguments)
            .map_err(|f| ActorProcessingErr::from(f))
    }

    async fn handle(
        &self,
        _myself: ActorRef<Self::Msg>,
        msg: Self::Msg,
        state: &mut Self::State,    // ← state IS A; methods on A run directly
    ) -> Result<(), ActorProcessingErr> {
        match msg {
            AdapterMessage::User { message, reply } => {
                let result = state.handle(message).await;
                let _ = reply.send(result);
                Ok(())
            }
            AdapterMessage::Close => { /* state.close().await; */ Ok(()) }
        }
    }
}
```

The `RactorAdapter<A>` ZST is the ONE permitted ZST in the
system — it's the framework boundary. Consumers never see it,
never name it, never write impls for it. The `persona-actor`
crate's public surface is `PersonaActor` + `ActorHandle<A>`;
that's all consumer code touches.

This is the *narrow named ZST exception* the skill already
allows for "marker types required by external frameworks" —
applied once, at the framework boundary, never repeated per
actor.

---

## 5 · The elegant interface — what consumer code reads like

Inside `persona-mind`, an actor declaration becomes:

```rust
// src/actors/claim/normalize.rs

use persona_actor::PersonaActor;

pub struct ClaimNormalize {
    config:    NormalizationConfig,
    in_flight: HashMap<OperationId, WirePath>,
    metrics:   ClaimNormalizeMetrics,
}

pub struct ClaimNormalizeArguments {
    pub config: NormalizationConfig,
}

pub enum ClaimNormalizeMessage {
    Normalize { operation: OperationId, path: WirePath },
}

pub enum ClaimNormalizeReply {
    Normalized { scope: NormalizedScope },
}

#[derive(Debug, thiserror::Error)]
pub enum ClaimNormalizeFailure {
    #[error("path is not absolute: {0}")]
    NotAbsolute(WirePath),
    #[error("path escapes root: {0}")]
    EscapesRoot(WirePath),
    #[error("storage error: {0}")]
    Storage(#[from] StorageFailure),
}

impl ClaimNormalize {
    fn validate(&self, path: &WirePath) -> Result<(), ClaimNormalizeFailure> {
        // pure method — no actor needed for sub-step (per §1)
    }

    fn collapse_double_slashes(&self, path: WirePath) -> WirePath {
        // pure method — no actor needed
    }
}

impl PersonaActor for ClaimNormalize {
    type Argument = ClaimNormalizeArguments;
    type Message  = ClaimNormalizeMessage;
    type Reply    = ClaimNormalizeReply;
    type Failure  = ClaimNormalizeFailure;

    fn open(arguments: Self::Argument) -> Result<Self, Self::Failure> {
        Ok(Self {
            config:    arguments.config,
            in_flight: HashMap::new(),
            metrics:   ClaimNormalizeMetrics::default(),
        })
    }

    async fn handle(&mut self, message: Self::Message) -> Result<Self::Reply, Self::Failure> {
        match message {
            ClaimNormalizeMessage::Normalize { operation, path } => {
                self.in_flight.insert(operation, path.clone());
                self.validate(&path)?;
                let collapsed = self.collapse_double_slashes(path);
                let scope = NormalizedScope::from(collapsed);
                self.metrics.normalize_count += 1;
                self.in_flight.remove(&operation);
                Ok(ClaimNormalizeReply::Normalized { scope })
            }
        }
    }
}
```

Consumer code (the supervisor) calls it:

```rust
let scope = self.normalize.ask(ClaimNormalizeMessage::Normalize {
    operation: operation_id,
    path:      raw_path,
}).await?;
```

Tests target the actor's data directly OR through the handle:

```rust
#[tokio::test]
async fn normalize_strips_double_slashes() {
    // direct — tests the reducer shape
    let mut actor = ClaimNormalize::open(ClaimNormalizeArguments { /* … */ }).unwrap();
    let reply = actor.handle(ClaimNormalizeMessage::Normalize {
        operation: OperationId::new(1),
        path:      WirePath::new("/foo//bar"),
    }).await.unwrap();
    assert_matches!(reply, ClaimNormalizeReply::Normalized { scope } if scope.as_str() == "/foo/bar");
}

#[tokio::test]
async fn normalize_through_handle_records_trace() {
    // hosted — tests the runtime + trace
    let handle = ActorHandle::<ClaimNormalize>::spawn_under(
        &test_supervisor(),
        ClaimNormalizeArguments { /* … */ },
    ).unwrap();
    let trace = TraceProbe::start();
    let reply = handle.ask(/* … */).await.unwrap();
    assert!(trace.recorded(ClaimNormalize::kind()));
}
```

Both shapes work. The reducer test exercises the methods on
`Self`; the hosted test exercises the runtime through the
handle. The actor type is the same noun in both.

---

## 6 · Scaffolding agents into actor thinking

operator/102 §1 names the agent-thinking gap explicitly:
*"agents are having a hard time thinking in terms of actors,
so we're going to have to push really hard."* Designer-side
contributions to the push:

### 6.1 · Architectural-truth tests that punish non-actor code

Operator/102 §10 already names trace tests + topology
manifest tests. Add a third class — *"this work has no actor
home"*:

| Test | Catches |
|---|---|
| Every `pub fn` in a `persona-mind` module is either inside `impl <Actor>` or inside `impl Persona Actor for <Actor>` | Free functions sneaking back |
| Every `impl <Actor>` block's data type is `Sized + Send` and not a ZST | ZST actors slipping past the discipline |
| Every actor type has a non-empty struct body (at least one field) | Empty actors that "don't have qualities" — per the user's philosophical rule |
| Every `pub fn open(args) -> Result<Self, _>` exists for every type implementing `PersonaActor` | Self-construction discipline |

These are mechanical lint-shaped tests; cheap to write; high
signal.

### 6.2 · Project template that makes actors the path of least resistance

A new `persona-mind`-style component, when scaffolded by a
script (`tools/new-persona-component`), produces:

```
new-component/
├── Cargo.toml          (depends on persona-actor + signal-* + persona-sema)
├── flake.nix           (inherits canonical fenix per /99)
├── src/
│   ├── lib.rs          (module entry)
│   ├── error.rs        (typed Error enum)
│   ├── actors/
│   │   ├── mod.rs      (actor module entry)
│   │   ├── root.rs     (RootActor — empty children list to be filled in)
│   │   └── README.md   (per-actor file convention; how to add a new actor)
│   └── main.rs         (minimal — spawn root, handle one request, exit)
└── tests/
    ├── trace.rs        (template trace test — agent fills in expected sequence)
    └── topology.rs     (template manifest test — agent declares actor tree)
```

The agent's first task in any new component is *"add the
actors that make this component do its job."* Free
functions and helper modules are not in the template — they
require deliberate addition against the lint-shaped tests
above.

### 6.3 · Vocabulary discipline in skills/

A new workspace skill `~/primary/skills/actor-discipline.md`
captures:

- The §1 density rule (typed name + failure mode + testability)
- The §3 dissolution (actor type IS state type)
- The §4 trait shape (`PersonaActor`, `ActorHandle`)
- The §5 example (`ClaimNormalize` worked)
- The §6.1 lint-shaped witnesses
- The relationship to `persona-actor` crate (operator/102 §6)

Cross-reference from `~/primary/skills/rust-discipline.md`
§"Actors" — replace the current "ractor actor behaviour
markers" carve-out with "use `persona-actor`'s `PersonaActor`
trait; the framework adapter is the single permitted ZST and
lives inside `persona-actor` only."

### 6.4 · The reading-direction cue

When an agent reads Persona code, the first question every
type prompts should be: *"Is this an actor?"* If yes, the
type carries its actor's data + has a `PersonaActor` impl.
If no, it's a domain record (Item, Edge, Note) or a typed
helper (NormalizedScope, OperationId).

There's no third category. No "service object," no "manager,"
no "controller," no "engine." Persona's runtime is actors +
records. Anything else is a smell.

---

## 7 · Compatibility with operator/102's `persona-actor` crate

Operator/102 §6 names `persona-actor` as a discipline crate
wrapping ractor. This designer report fills in the trait
shape (§4), the discrimination rule (§1), and the
agent-scaffolding (§6). They compose:

| operator/102 §6 piece | designer/101 contribution |
|---|---|
| `ActorManifest` | (operator's; declares topology) |
| `ActorKind` | §4 — derived from `type_name<Self>()` |
| `ActorPath` | (operator's; typed runtime path) |
| `SpawnPlan` | §4 — `ActorHandle::spawn_under(parent, args)` |
| `ActorTrace` + `TraceProbe` | (operator's; trace plumbing) |
| `SupervisorPolicy` | §4 — typed field on supervisor actors |
| `MessageEdge` | (operator's; allowed sender → receiver relations) |

The trait `PersonaActor` and handle `ActorHandle<A>` are the
public surface that consumer code sees. The
manifest/trace/spawn-plan plumbing is operator's discipline
layer. Both fit in `persona-actor` cleanly.

The single ractor-shaped ZST (`RactorAdapter<A>`) is internal
to `persona-actor`. Consumers never name it.

---

## 8 · Skill updates needed

Once `persona-actor` ships:

1. **`~/primary/skills/rust-discipline.md` §"Actors"** —
   replace the current "ractor actor behaviour markers"
   ZST exception with "use `persona-actor`'s `PersonaActor`
   trait; the actor type carries the actor's data; the
   framework adapter is the single permitted ZST and lives
   inside `persona-actor`." Update the example shape.

2. **`~/primary/skills/rust-discipline.md` §"No ZST method
   holders"** — remove "ractor actor behaviour markers" from
   the legitimate-ZST list. The ractor exception was the
   compromise; persona-actor is the resolution.

3. **`~/primary/skills/abstractions.md` §"When the language
   doesn't have methods"** — extend with: actor frameworks
   that *do* have methods (most Rust actor libraries) should
   put the methods on the noun whose data they touch, not on
   a ZST behavior marker. The framework's accommodation of
   ZST-shape is a workaround; persona-actor removes the
   accommodation.

4. **NEW: `~/primary/skills/actor-discipline.md`** —
   per §6.3, the workspace skill that captures the density
   rule, the no-ZST shape, the trait, and the agent-thinking
   scaffolding. This is the canonical home for "how to write
   actors in this workspace."

5. **`~/primary/repos/lore/rust/ractor.md`** — add a section
   *"Don't use ractor's `Actor` trait directly in Persona
   components — use persona-actor's `PersonaActor` trait
   instead. ractor remains the runtime; persona-actor is the
   discipline."* lore documents the tool; the workspace skill
   documents how the workspace uses it.

System-specialist or designer files these as the
implementation cascade lands.

---

## 9 · Open questions

1. **`PersonaActor::handle` returns `Result<Self::Reply,
   Self::Failure>`.** What about messages that produce no
   reply (fire-and-forget tells)? Lean: `type Reply = ()` for
   those actors; the handle's `tell()` ignores the unit
   reply. Or: separate `handle_tell` method without reply.
   The first is simpler.

2. **Async vs sync `handle`.** The trait is async per the
   `tokio` runtime. For pure-CPU actors (id mint, encode),
   sync is enough. Either: keep `async fn` everywhere
   (uniform); add a sync trait sibling `PersonaSyncActor`
   with a sync adapter. Defer until profile shows real cost.

3. **Can `PersonaActor::open` itself be async?** Some actors
   need async setup (open a file, contact a sibling). Lean
   yes — make it `async fn open(args) -> Result<Self, _>`.
   The wrapper's `pre_start` is already async.

4. **Virtual actors (operator/102 §3.3).** The `PersonaActor`
   shape works for resident actors; virtual actors need
   activation-on-message-receipt. Likely a separate trait
   `PersonaVirtualActor` whose `open` is *"load Self from
   sema by ID"* and which deactivates after idle. Defer until
   virtual actors land.

5. **What does the agent see when `cargo doc` renders an
   actor?** The struct's fields, its `impl PersonaActor`, its
   inherent `impl` block. The actor's identity, qualities,
   and verbs are all in one place. Worth an explicit doc-render
   smoke test that the actor's docstring reads as one
   coherent thing.

6. **`MindEnvelope` from designer/100 §3.** Should it itself
   be an actor's input? Lean: yes — `IngressSupervisorActor`'s
   `Argument` includes `MindEnvelope`-routing config; the
   `EnvelopeActor` builds the envelope; downstream actors
   consume it as part of their `Message` payloads.

---

## See also

- `~/primary/reports/operator/102-actor-heavy-persona-mind-research.md`
  — the actor-as-correctness research and Rust-framework
  survey this report is a designer companion to.
- `~/primary/reports/operator/101-persona-mind-full-architecture-proposal.md`
  — the actor-dense architecture; this report's trait shape
  is what its actors should follow.
- `~/primary/reports/designer/100-persona-mind-architecture-proposal.md`
  — sibling designer companion; its §3 caller-identity
  mechanism becomes one of the actors this trait shape
  hosts.
- `~/primary/skills/rust-discipline.md` §"No ZST method
  holders" — the rule the current ractor pattern partially
  violates; §8 here proposes the skill update that removes
  the ractor exception.
- `~/primary/skills/abstractions.md` §"The Karlton bridge"
  — the verb-belongs-to-noun rule the trait shape upholds
  (the verb on the actor data, not a ZST shell).
- `~/primary/skills/naming.md` — the full-English-words
  rule the trait fields and methods follow.
- `~/primary/repos/lore/rust/ractor.md` — current ractor
  reference; §8 proposes adding the *"use persona-actor
  instead"* note.
- `~/primary/ESSENCE.md` §"Beauty is the criterion" — the
  no-ZST argument is the user's diagnostic reading of an
  ugliness in the framework's accommodation.
