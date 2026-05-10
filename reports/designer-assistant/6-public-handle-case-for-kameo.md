# 6 - Public handle case for Kameo

*Designer-assistant counterproposal. This report argues for public
domain handles around Kameo actors. It does not propose a wrapper actor
runtime, a `workspace_actor` crate, a trait facade, or a way to pretend
Kameo is not the runtime.*

---

## Position

The current Kameo skill says `ActorRef<A>` should be the public consumer
surface, including for library users. That is coherent for internal actor
code, examples, tests, and low-level actor libraries.

I still think it overcorrects for Persona component libraries.

My recommendation:

- use direct `ActorRef<A>` freely inside a component;
- do not invent a second actor trait or runtime wrapper;
- do expose a public `ThingHandle` when the crate is offering a domain
  service, not just an actor example;
- make that handle a small concrete facade over one or more concrete
  `ActorRef<T>` fields;
- let the handle encode lifecycle, error mapping, timeouts, capability
  limits, and domain vocabulary.

That is not hiding Kameo for a hypothetical future runtime swap. It is
preserving the crate's domain API from actor-topology churn.

The bad abstraction is:

```rust
trait WorkspaceActor { ... }
```

or:

```rust
pub struct ActorHandle<A> {
    inner: kameo::actor::ActorRef<A>,
}
```

The good abstraction is:

```rust
pub struct MindHandle {
    root: kameo::actor::ActorRef<MindRoot>,
}
```

with methods named in the problem domain:

```rust
impl MindHandle {
    pub async fn submit(&self, envelope: MindEnvelope) -> Result<MindReceipt, MindError> {
        Ok(self.root
            .ask(Submit { envelope })
            .reply_timeout(Duration::from_secs(5))
            .send()
            .await
            .map_err(MindError::from_send)?)
    }
}
```

---

## Why ActorRef Is Not Always The Library API

`ActorRef<A>` is a precise runtime address. It is not automatically a
good public library contract.

Exporting `ActorRef<Ledger>` means the public API now includes:

- the actor type name;
- every public message type implemented by that actor;
- whether each operation is `ask` or `tell`;
- Kameo's `SendError` shape;
- Kameo timeout and mailbox knobs;
- the current actor topology.

That is fine when the library is "here is an actor." It is too much when
the library is "here is a mind service," "here is a ledger," or "here is
a claim normalizer."

The handle is not protecting users from the type system. It is protecting
the domain contract from accidental runtime vocabulary.

---

## Example 1 - Stable Library API While Topology Changes

Raw `ActorRef` makes this a public promise:

```rust
pub use kameo::actor::ActorRef;

pub struct Ledger {
    entries: Vec<Entry>,
    next_id: EntryId,
}

pub struct Append {
    pub body: EntryBody,
}

pub struct Read {
    pub id: EntryId,
}

pub type LedgerRef = ActorRef<Ledger>;
```

Every consumer can now write:

```rust
let id = ledger_ref.ask(Append { body }).await?;
let entry = ledger_ref.ask(Read { id }).await?;
```

That looks nice until `Ledger` stops being one actor. The natural
production shape may become:

```rust
struct LedgerRoot {
    writer: ActorRef<LedgerWriter>,
    reader: ActorRef<LedgerReader>,
    index: ActorRef<LedgerIndex>,
}
```

Now the public `ActorRef<Ledger>` contract is false. Keeping compatibility
requires a fake `Ledger` coordinator actor whose main job is preserving
the old public type. That is exactly the kind of backward abstraction we
try to avoid.

A public handle makes the topology private from the start:

```rust
pub struct LedgerHandle {
    root: ActorRef<LedgerRoot>,
}

impl LedgerHandle {
    pub async fn append(&self, body: EntryBody) -> Result<EntryId, LedgerError> {
        Ok(self.root
            .ask(AppendEntry { body })
            .reply_timeout(Duration::from_secs(2))
            .send()
            .await
            .map_err(LedgerError::from_send)?)
    }

    pub async fn read(&self, id: EntryId) -> Result<Option<Entry>, LedgerError> {
        Ok(self.root
            .ask(ReadEntry { id })
            .reply_timeout(Duration::from_millis(500))
            .send()
            .await
            .map_err(LedgerError::from_send)?)
    }
}
```

Later, the handle can change internals without changing the library API:

```rust
pub struct LedgerHandle {
    writer: ActorRef<LedgerWriter>,
    reader: ActorRef<LedgerReader>,
}

impl LedgerHandle {
    pub async fn append(&self, body: EntryBody) -> Result<EntryId, LedgerError> {
        Ok(self
            .writer
            .ask(AppendEntry { body })
            .await
            .map_err(LedgerError::from_send)?)
    }

    pub async fn read(&self, id: EntryId) -> Result<Option<Entry>, LedgerError> {
        Ok(self
            .reader
            .ask(ReadEntry { id })
            .await
            .map_err(LedgerError::from_send)?)
    }
}
```

This is not runtime swap insurance. It is topology-change insurance, and
actor systems change topology constantly as they become real.

---

## Example 2 - The Fallible Tell Trap Should Not Be Public

Kameo has a real footgun: `tell`ing a fallible handler can stop the actor
by default when the handler returns `Err`.

Raw public `ActorRef<ClaimNormalizer>` gives every caller this option:

```rust
normalizer.tell(NormalizeClaim { claim }).await?;
```

If `NormalizeClaim` has:

```rust
impl Message<NormalizeClaim> for ClaimNormalizer {
    type Reply = Result<NormalizedClaim, NormalizeError>;
    // ...
}
```

then using `tell` instead of `ask` is not just "ignoring the result." It
changes failure semantics.

A handle can remove that choice:

```rust
pub struct ClaimNormalizerHandle {
    normalizer: ActorRef<ClaimNormalizer>,
}

impl ClaimNormalizerHandle {
    pub async fn normalize(
        &self,
        claim: Claim,
    ) -> Result<NormalizedClaim, ClaimNormalizerError> {
        Ok(self.normalizer
            .ask(NormalizeClaim { claim })
            .reply_timeout(Duration::from_secs(3))
            .send()
            .await
            .map_err(ClaimNormalizerError::from_send)?)
    }
}
```

The message type can stay `pub(crate)`, or it can be public only in an
`advanced` module. The everyday API exposes the safe operation, not the
send primitive.

The skill currently says "there is no class of misuse a `*Handle`
newtype prevents." This is the counterexample. It prevents a caller from
choosing `tell` for an operation whose domain meaning requires `ask`.

---

## Example 3 - Capability Surfaces

`ActorRef<Ledger>` grants every message implemented for `Ledger`.
Sometimes the domain wants separate authorities:

```rust
pub struct LedgerReader {
    ledger: ActorRef<Ledger>,
}

pub struct LedgerWriter {
    ledger: ActorRef<Ledger>,
}

impl LedgerReader {
    pub async fn read(&self, id: EntryId) -> Result<Option<Entry>, LedgerError> {
        Ok(self
            .ledger
            .ask(ReadEntry { id })
            .await
            .map_err(LedgerError::from_send)?)
    }
}

impl LedgerWriter {
    pub async fn append(&self, body: EntryBody) -> Result<EntryId, LedgerError> {
        Ok(self
            .ledger
            .ask(AppendEntry { body })
            .await
            .map_err(LedgerError::from_send)?)
    }
}
```

Kameo has `Recipient<M>` and `ReplyRecipient<M, Ok, Err>`, which are good
for single-message capabilities. Handles are better when the capability
is a small domain surface, such as:

- `read`, `list`, `watch`;
- `append`, `commit`, `compact`;
- `submit`, `cancel`, `status`.

That surface is not "all messages this actor happens to implement." It is
the authority the library wants to hand to this caller.

---

## Example 4 - Lifecycle Is Not A Message

A useful component handle often means "this service has started and owns
its supervision tree."

```rust
pub struct MindHandle {
    root: ActorRef<MindRoot>,
}

impl MindHandle {
    pub async fn start(config: MindConfig) -> Result<Self, MindStartError> {
        let root = MindRoot::spawn(MindRoot::new(config));
        root.wait_for_startup_result().await.map_err(MindStartError::from_startup)?;
        Ok(Self { root })
    }

    pub async fn submit(&self, envelope: MindEnvelope) -> Result<MindReceipt, MindError> {
        Ok(self
            .root
            .ask(Submit { envelope })
            .await
            .map_err(MindError::from_send)?)
    }

    pub async fn stop(self) -> Result<(), MindStopError> {
        self.root
            .stop_gracefully()
            .await
            .map_err(MindStopError::from_send)?;
        self.root
            .wait_for_shutdown_result()
            .await
            .map_err(MindStopError::from_shutdown)?;
        Ok(())
    }
}
```

You can split startup into a builder if the configuration path is large:

```rust
let mind = Mind::builder()
    .sema(path)
    .clock(clock)
    .start()
    .await?;
```

But the returned value is still a handle to a live service. It is not just
a constructor. The handle names an owned relationship to a running actor
tree.

---

## Example 5 - Error Vocabulary Belongs To The Domain

Raw `ActorRef` exposes Kameo errors at every call site:

```rust
match root.ask(Submit { envelope }).await {
    Ok(receipt) => Ok(receipt),
    Err(SendError::HandlerError(error)) => Err(error.into()),
    Err(SendError::ActorNotRunning(_)) => Err(MindError::Stopped),
    Err(SendError::Timeout(_)) => Err(MindError::TimedOut),
    Err(other) => Err(MindError::Runtime(other.to_string())),
}
```

With a handle, that mapping is one tested function:

```rust
impl MindHandle {
    pub async fn submit(&self, envelope: MindEnvelope) -> Result<MindReceipt, MindError> {
        Ok(self.root
            .ask(Submit { envelope })
            .reply_timeout(Duration::from_secs(5))
            .send()
            .await
            .map_err(MindError::from_send)?)
    }
}
```

Callers should think in `MindError`, not `SendError<Submit, SubmitError>`.
The latter is useful inside the crate. It is noise at the library
boundary.

---

## A Rule That Fits Both Sides

The current skill is right to reject a handle whose only job is:

```rust
pub struct CounterHandle {
    counter: ActorRef<Counter>,
}

impl CounterHandle {
    pub async fn inc(&self) -> Result<i64, SendError<Inc>> {
        self.counter.ask(Inc).await
    }
}
```

For a toy `Counter`, use `ActorRef<Counter>` directly.

But for Persona components, a handle earns its keep when at least one of
these is true:

- it owns startup or shutdown;
- it maps runtime errors into domain errors;
- it applies timeouts or backpressure policy;
- it prevents unsafe send forms such as fallible `tell`;
- it narrows capabilities;
- it keeps message types private;
- it hides actor topology, not actor runtime;
- it offers domain verbs instead of mailbox verbs.

The handle must stay concrete:

```rust
pub struct ClaimNormalizerHandle {
    normalizer: ActorRef<ClaimNormalizer>,
}
```

No trait object. No generic runtime. No `workspace_actor`. No private
Kameo clone. No "maybe we switch runtimes someday" argument.

If advanced users need raw power, expose a deliberate escape hatch:

```rust
impl ClaimNormalizerHandle {
    pub fn actor_ref(&self) -> &ActorRef<ClaimNormalizer> {
        &self.normalizer
    }
}
```

or a narrower Kameo-native capability:

```rust
impl ClaimNormalizerHandle {
    pub fn normalize_recipient(
        &self,
    ) -> ReplyRecipient<NormalizeClaim, NormalizedClaim, NormalizeError> {
        self.normalizer.recipient()
    }
}
```

That keeps Kameo honest and visible without making it the first API every
domain caller has to learn.

---

## Naming

The `Actor` suffix should still mostly disappear. I agree with
`skills/kameo.md` there.

Use:

```rust
pub struct ClaimNormalizer { ... }          // actor state
pub struct NormalizeClaim { ... }           // message
pub struct ClaimNormalizerHandle { ... }    // live service facade
```

Avoid:

```rust
pub struct ClaimNormalizerActor;
pub struct NormalizeClaimMessage;
pub struct ClaimNormalizerActorHandle;
```

`Handle` is not a framework-category suffix like `Actor`. It names a
relationship: this value is the caller's held authority to a live service.
For remote networked services, `Client` may be better. For local in-process
actors, `Handle` is precise.

---

## Proposed Skill Wording

If I were editing `skills/kameo.md`, I would replace the absolute
`ActorRef<A>` public-surface rule with this:

> `ActorRef<A>` is the default internal actor surface and the right public
> surface for low-level actor examples or crates whose product is the
> actor itself. A public domain component may expose a concrete
> `ThingHandle` when the handle owns lifecycle, narrows capabilities, maps
> runtime errors into domain errors, enforces send policy, or preserves a
> stable domain API across actor-topology changes. Such a handle wraps
> concrete Kameo `ActorRef<T>` fields; it must not introduce a runtime
> abstraction trait, generic actor facade, or Kameo-hiding wrapper crate.

That keeps the anti-hallucination rule and still gives libraries a
professional public API.

---

## Bottom Line

The current skill correctly kills `*Actor`, `*Message`, and fake
`workspace_actor` abstractions. It should not also kill every public
domain handle.

`ActorRef<A>` is the right building block. A handle is the right library
surface when the library offers a service rather than a raw actor.
