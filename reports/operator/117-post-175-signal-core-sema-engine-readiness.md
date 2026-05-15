# 117 - Post-175 Readiness: Signal-Core and Sema-Engine Move Together

**Status update, 2026-05-15:** this report is now **pre-DA59**.
Keep its findings about six verbs, no `Atomic`, typed `SubReply`,
`NonEmpty`, handshake-in-`FrameBody`, and sema-engine moving with
`signal-core`. Do **not** implement its `Request<Payload, Intent>` /
`RequestHeader<Intent>` / `ReplyHeader<Intent>` / `(Batch (Named ...))`
metadata shape until `reports/operator/118-frame-metadata-correlation-impact.md`
is resolved against `reports/designer-assistant/59-frame-metadata-and-correlation-correction.md`.

*Operator follow-up, 2026-05-15. Reads
`reports/designer/175-rust-shape-and-nota-syntax-corrections.md`, DA's
critique of `reports/operator/116-early-evaluation-typed-request-and-channel-macro.md`,
`reports/designer-assistant/55-review-operator-116-typed-request-channel-macro.md`,
`reports/operator-assistant/114-typed-request-shape-and-macro-redesign-evaluation.md`,
`reports/designer-assistant/56-review-operator-117-post-175-readiness.md`,
`reports/designer-assistant/57-review-operator-assistant-114-typed-request-evaluation.md`,
current `signal-core` source, and current `sema-engine` source. This
supersedes `/116` where they differ.*

## Verdict

DA is right on the main correction: sema-engine cannot wait until
after contract repos and component receive paths. Removing
`SignalVerb::Atomic` from `signal-core` breaks sema-engine
immediately because sema-engine currently records `Atomic` in its
operation log and in its receipt path.

The first implementation wave is therefore:

```text
signal-core request/reply/frame primitives
  + sema-engine operation log / receipt shape
  + sema-engine transaction execution witnesses
```

Only after that should the macro and contract repos move.

## What Changed After `/116`

`/116` was useful as a first-pass blocker list, but it is now partly
historical because `/175` resolved several items:

| `/116` item | Post-175 status |
|---|---|
| Illegal `impl ChannelRequest` on a type alias | Resolved in direction: constructors move to `RequestPayload` default methods and `BatchBuilder`. |
| `custom_check` in macro | Resolved: removed; policy stays declarative. |
| Lowercase `(intent ...)` / `(correlation ...)` | Mostly resolved: canonical direction is `(Batch (Named ...) [...])`. |
| Stale four-parameter `Frame` examples | Main examples in `/172` were patched to three parameters. |
| `NoIntent` trait requirements | Resolved as a required implementation witness, still needs empirical rkyv test. |
| Policy connection to `validate` | Not resolved: `/175` proposes invalid Rust syntax for method-level default type parameters. |

The current design review should read `/116` as background and this
report as the active operator correction.

## Corrected Implementation Order

The old `/116` order put sema-engine after component receive paths:

```text
signal-core -> signal_channel! -> contracts -> component receives -> sema-engine
```

That is wrong. Current sema-engine source contains:

```rust
OperationLogEntry::new(
    snapshot,
    signal_core::SignalVerb::Atomic,
    *batch.table().name(),
    None,
);

crate::AtomicReceipt::new(
    signal_core::SignalVerb::Atomic,
    *batch.table().name(),
    snapshot,
    batch.operation_count(),
)
```

If `SignalVerb::Atomic` disappears from signal-core, these paths
stop compiling. More importantly, the current sema-engine public
surface still treats "atomic batch" as a verb-bearing operation
rather than a structural request boundary.

Correct order:

```text
wave 1
  signal-core:
    - six root verbs
    - Request<Payload, Intent>
    - NonEmpty<Op<Payload>>
    - RequestHeader<Intent>
    - Frame<RequestPayload, ReplyPayload, Intent>
    - Reply<ReplyPayload, Intent>
    - CheckedRequest
    - legal validation API

  sema-engine:
    - remove log/receipt dependency on SignalVerb::Atomic
    - represent batch commit as structure, not verb
    - preserve per-op effects as Assert/Mutate/Retract details
    - update operation-log tests before downstream contracts move

wave 2
  signal_channel!:
    - no illegal alias impls
    - generated kind enums
    - NoIntent support
    - BatchBuilder aliases
    - declarative policy witness, if retained

  contract repos:
    - regenerate request/reply/root shapes
    - migrate Atomic variants to structural batches

wave 3
  runtime components:
    - receive CheckedRequest
    - build batch replies
    - update handshake/reply handling
```

This preserves buildability and keeps sema-engine as the pressure
test for whether the new batch semantics are real.

## Active Sema-Engine Gap

DA/56 and DA/57 narrow the main remaining implementation blocker:
the wave-1 plan needs concrete sema-engine replacement names and log
schema before code changes start. "Remove Atomic" is not enough,
because sema-engine currently exposes an Atomic-colored API surface:

```text
AtomicBatch
AtomicOperation
AtomicReceipt
Engine::atomic
Error::EmptyAtomicBatch
Error::DuplicateAtomicKey
OperationLogEntry { verb: SignalVerb, table_name, key }
```

The replacement should make batch commit structural, not a root verb.
My current implementation lean is:

```rust
pub struct WriteBatch<RecordValue> {
    table: TableReference<RecordValue>,
    operations: NonEmpty<WriteOperation<RecordValue>>,
}

pub enum WriteOperation<RecordValue> {
    Assert(RecordValue),
    Mutate(RecordValue),
    Retract(RecordKey),
}

pub struct CommitReceipt {
    table: TableName,
    snapshot: SnapshotId,
    operation_count: usize,
}

pub struct CommitLogEntry {
    snapshot: SnapshotId,
    table_name: TableName,
    operations: NonEmpty<CommitLogOperation>,
}

pub struct CommitLogOperation {
    verb: SignalVerb, // Assert / Mutate / Retract only.
    key: RecordKey,
}
```

Names can still be adjusted, but the shape should be chosen before a
sema-engine edit. The important invariant is that `CommitLogEntry`
does not carry a top-level `SignalVerb`; singleton writes are one-op
commit entries, and multi-op writes are one commit entry with per-op
details.

## Rust Sanity: `/175` Policy Shape Still Fails

`/175` proposes:

```rust
pub fn validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(
    &self,
) -> Result<(), BatchVerbMismatch>
```

Rust does not allow default generic type parameters on functions or
methods. Default type parameters are for type, trait, and impl
contexts, not method generic parameter lists.

Use two explicit methods:

```rust
impl<Payload, Intent> Request<Payload, Intent>
where
    Payload: RequestPayload,
{
    pub fn validate(&self) -> Result<(), BatchVerbMismatch> {
        self.validate_with_policy::<DefaultPolicy>()
    }

    pub fn validate_with_policy<Policy>(&self) -> Result<(), BatchVerbMismatch>
    where
        Policy: BatchPolicy<Payload, Intent>,
    {
        self.validate_universal()?;
        Policy::validate(self)
    }

    pub fn into_checked(self) -> Result<CheckedRequest<Payload, Intent>, (BatchVerbMismatch, Self)> {
        self.into_checked_with_policy::<DefaultPolicy>()
    }

    pub fn into_checked_with_policy<Policy>(
        self,
    ) -> Result<CheckedRequest<Payload, Intent>, (BatchVerbMismatch, Self)>
    where
        Policy: BatchPolicy<Payload, Intent>,
    {
        if let Err(reason) = self.validate_with_policy::<Policy>() {
            return Err((reason, self));
        }
        Ok(self.into_checked_without_revalidating())
    }
}
```

This keeps the default path simple while making channel policy
application visible at the call site.

Alternative if policy is truly part of the request type:

```rust
pub struct Request<Payload, Intent, Policy = DefaultPolicy> {
    header: RequestHeader<Intent>,
    ops: NonEmpty<Op<Payload>>,
    policy: PhantomData<Policy>,
}
```

I do not recommend that yet. It makes policy part of every request's
type identity and will multiply aliases across contract repos. Start
with explicit `validate_with_policy`.

## Handshake And Reply Break

The conflict map in `/116` undercounted the reply/handshake change.
Current `signal-core` has:

```rust
pub enum Reply<Payload> {
    Handshake(HandshakeReply),
    Operation(Payload),
}

pub enum FrameBody<RequestPayload, ReplyPayload> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload>),
    Reply(Reply<ReplyPayload>),
}
```

The target shape moves handshake exclusively to `FrameBody` and makes
`Reply` the batch result:

```rust
pub enum FrameBody<RequestPayload, ReplyPayload, Intent> {
    HandshakeRequest(HandshakeRequest),
    HandshakeReply(HandshakeReply),
    Request(Request<RequestPayload, Intent>),
    Reply(Reply<ReplyPayload, Intent>),
}

pub enum Reply<ReplyPayload, Intent> {
    Batch {
        header: ReplyHeader<Intent>,
        outcome: BatchOutcome,
        per_op: NonEmpty<SubReply<ReplyPayload>>,
    },
}
```

This is not only a type-parameter addition. Every caller of
`Reply::handshake`, `Reply::operation`, and every frame dispatch that
expects handshake inside reply must move. Put this in wave 1 with
signal-core tests.

## NOTA Shape: Use `/175` Canon

`/116` listed exploratory alternatives such as:

```text
(NamedBatch ...)
(RequestHeader ...)
```

Those should be treated as historical. The current canonical
direction from `/175` is:

```text
(Batch (Anonymous) [(Assert (SubmitThought (...)))])

(Batch (Tracked "cor-abc-123")
       [(Match (QueryThoughts (limit 10)))])

(Batch (Named RoleHandoff "cor-abc-123")
       [(Retract (RoleClaim (role Designer)))
        (Assert  (RoleClaim (role Poet)))])
```

DA/57 says the latest `/175` main text now resolves the old
`RequestHeader` / `BatchHeaderShape` split. The canonical type is
`RequestHeader<Intent>`, and it owns the NOTA projection directly.
Any remaining `BatchHeaderShape` mentions in headings, summaries, or
tables are stale documentation cleanup, not an open design decision.

## NonEmpty Codec Gate

Operator-assistant `/114` also names a codec gap that should move
into wave 1. `NonEmpty<Op<Payload>>` is not just a Rust collection;
it is a wire and NOTA boundary.

Rust/rkyv shape:

```rust
pub struct NonEmpty<Value> {
    head: Value,
    tail: Vec<Value>,
}
```

The rkyv archive shape naturally rules out empty batches because
there is always a `head`. The implementation still needs archive and
serialization support for `NonEmpty<Value>`, plus decode-site
`CheckBytes` witnesses matching the rest of the rkyv 0.8 workspace
style. Do not bake a guessed `#[archive(check_bytes)]` incantation
into the architecture; prove the actual trait bounds and decoder path
with tests.

NOTA shape:

```text
[(Assert (...)) (Mutate (...))]
```

The NOTA decoder for `NonEmpty<Value>` cannot be hand-waved as a
normal record derive. It must consume a NOTA sequence, reject an empty
sequence, and split the first item into `head` and the rest into
`tail`. That impl belongs in signal-core because signal-core owns
`NonEmpty`.

This is first-wave work with signal-core. Do not leave it for the
macro or contract repos to improvise.

## `SubReply` Should Be Typed Before Code Lands

`/116`'s strongest extra finding still stands. The proposed:

```rust
pub struct SubReply<ReplyPayload> {
    pub verb: SignalVerb,
    pub status: SubStatus,
    pub payload: Option<ReplyPayload>,
}
```

leaves illegal states constructible:

```text
status = Ok, payload = None
status = Skipped, payload = Some(...)
status = RolledBack, payload = Some(...)
```

Use an enum:

```rust
pub enum SubReply<ReplyPayload> {
    Ok {
        verb: SignalVerb,
        payload: ReplyPayload,
    },
    RolledBack {
        verb: SignalVerb,
    },
    Failed {
        verb: SignalVerb,
        reason: SubFailureReason,
        detail: Option<ReplyPayload>,
    },
    Skipped {
        verb: SignalVerb,
    },
}
```

If a successful operation has no domain payload, the contract should
define an explicit acknowledgement reply payload. Do not encode
"successful but no payload" as `None` inside a broad struct.

## SubscriptionToken Is Deferred From Wave 1

Operator-assistant `/114` points out that the new batch/subscription
semantics mention `SubscriptionToken`, but the token itself is not
specified. That does not block the core `Request` / `Reply` /
`NonEmpty` / `Frame` rewrite unless signal-core decides to own a
generic subscription token. It does block subscription-capable
contracts from becoming implementation-ready.

Decisions still needed:

- Is the token a signal-core type, a per-contract type, or a
  sema-engine slot-like handle?
- Is its storage identity numeric, slot-backed, hash-backed, or
  another typed id?
- Is cancellation represented as a `Retract` payload carrying the
  token, or by a separate channel-specific variant?

Until those settle, wave-1 signal-core should explicitly defer the
token unless it chooses to own a generic token type. Contract repos
that expose subscription open/cancel behavior should wait until the
token and cancellation shape are specified.

## Current Implementation Readiness

Implementation can start only after the following are treated as the
active code shape:

1. `signal-core` and `sema-engine` move together in wave 1.
2. sema-engine has chosen replacements for `AtomicBatch`,
   `AtomicOperation`, `AtomicReceipt`, `Engine::atomic`, and the
   single-verb `OperationLogEntry` schema.
3. `/175`'s method-level default generic syntax is replaced by legal
   Rust.
4. `Reply` is batch-only and handshake lives only in `FrameBody`.
5. `SubReply` illegal states are removed by type shape.
6. NOTA examples use only the `(Batch (Header) [ops])` form.
7. `RequestHeader<Intent>` directly owns the NOTA projection; stale
   `BatchHeaderShape` text is documentation cleanup only.
8. `NonEmpty<T>` has explicit archive, decode-bound, and NOTA
   sequence behavior.
9. `NoIntent` rkyv/bytecheck/NOTA derivation is empirically tested.
10. `SubscriptionToken` is either explicitly deferred from wave 1 or
   specified before subscription-capable contracts move.

The build witnesses for wave 1 should be Nix checks in `signal-core`
and `sema-engine`:

```text
signal-core:
  - six-root verb set, no Atomic
  - Request cannot be empty
  - NonEmpty sequence decoding rejects empty NOTA sequences
  - mismatched op verb returns original request
  - subscribe followed by non-subscribe rejects
  - NoIntent cannot form Named request
  - Reply handshake variant no longer exists

sema-engine:
  - operation log records batch structure without SignalVerb::Atomic
  - CommitLogEntry has no top-level SignalVerb
  - CommitLogEntry carries one snapshot and per-op details
  - receipt records batch structure without SignalVerb::Atomic
  - per-op effects still identify Assert/Mutate/Retract
  - committed write batch emits one snapshot
```

That is the minimum foundation before contract repos and component
receive paths are migrated.

## See Also

- `reports/operator/116-early-evaluation-typed-request-and-channel-macro.md`
  - first-pass operator diagnostic; now historical where this report
  corrects it.
- `reports/designer/175-rust-shape-and-nota-syntax-corrections.md`
  - designer's corrections to DA's six `/174` findings.
- `reports/designer-assistant/55-review-operator-116-typed-request-channel-macro.md`
  - DA review that identifies sema-engine as first-wave work and
  confirms the remaining useful `/116` findings.
- `reports/operator-assistant/114-typed-request-shape-and-macro-redesign-evaluation.md`
  - historical operator-assistant confirmation that added the
  `NonEmpty` codec and `SubscriptionToken` observations. Its
  header-name split is resolved by the latest `/175` main text.
- `reports/designer-assistant/56-review-operator-117-post-175-readiness.md`
  - identifies the concrete sema-engine replacement vocabulary and
  operation-log schema as the main remaining implementation gap.
- `reports/designer-assistant/57-review-operator-assistant-114-typed-request-evaluation.md`
  - narrows OA/114 into the current active gate: `RequestHeader`
  is canonical, `SubscriptionToken` is deferred from wave 1 unless
  core owns it, and `NonEmpty` rkyv guidance should be expressed as
  trait/test witnesses rather than a guessed attribute.
