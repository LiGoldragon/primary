# 116 — Early Evaluation: Typed Requests and `signal_channel!` Redesign

*Operator evaluation, 2026-05-15. Reads
`reports/designer/172-typed-request-shape-and-execution-semantics.md`,
`reports/designer/174-signal-channel-macro-redesign.md`,
`reports/designer/175-rust-shape-and-nota-syntax-corrections.md`, DA's
attached findings, and the refreshed workspace skills. This is an
early implementation-readiness pass while the design is still moving.*

## Verdict

The design direction is good: `Request<Payload, Intent>`, closed
intent enums, non-empty operation batches, strict ordered execution,
read-your-own-writes, subscribe-last staging, and the
`validate`/`into_checked` split are the right core shape.

It is not implementation-ready yet. DA's findings are mostly correct.
`/175` fixes the alias-constructor direction, removes `custom_check`,
repairs the main NOTA syntax direction, and patches the stale
four-parameter `Frame` examples. It also introduces a new Rust-shape
problem: default generic type parameters on methods such as
`fn validate<Policy = DefaultPolicy>(...)` are not legal Rust.

The bigger operator reading is that 172 is a breaking semantic pivot
from the current seven-root implementation: `Atomic` disappears as a
root verb and becomes request/frame structure. That has to be treated
as the first migration step, not as a macro-only adjustment.

## Current Conflict Map

```text
current signal-core
  SignalVerb = Assert Mutate Retract Match Subscribe Atomic Validate
  Request<Payload>
  Frame<RequestPayload, ReplyPayload>
  Reply<Payload>
  signal_channel! macro_rules
  single-op helpers

172 target
  SignalVerb = Assert Mutate Retract Match Subscribe Validate
  Request<Payload, Intent>
  NonEmpty<Op<Payload>>
  RequestHeader<Intent>
  Reply<ReplyPayload, Intent>
  CheckedRequest<Payload, Intent>
  Atomicity is structural to the batch

174 target
  Frame<RequestPayload, ReplyPayload, Intent>
  NoIntent for channels without named intents
  generated operation-kind enum
  generated declarative batch-policy witness
  proc-macro preferred
```

The implementation order should reflect that dependency:

```text
signal-core request/reply/frame primitives
  -> signal_channel! macro surface
  -> contract repos
  -> component receive paths
  -> sema-engine execution semantics
```

Implementing the macro before the core request shape is settled will
produce churn.

## DA Findings

### 1. Alias constructors cannot compile

DA is correct. 174 proposes:

```rust
pub type ChannelRequest = signal_core::Request<MindRequest, MindBatchIntent>;

impl ChannelRequest {
    pub fn single(...) -> Self { ... }
}
```

That is an inherent impl on a type alias to an external generic type.
Rust does not allow it.

Implementation-compatible options:

| Option | Shape | Evaluation |
|---|---|---|
| Generic constructors only | `Request::single_anonymous(payload)` | Smallest and cleanest in `signal-core`; less channel-specific ergonomic sugar. |
| Payload enum methods | `MindRequest::into_anonymous_request(self)` | Legal because `MindRequest` is local; keeps behavior on a real type. Static batch builders on a payload enum are slightly awkward but workable. |
| Extension trait | `impl MindRequestConstruction for Request<MindRequest, MindBatchIntent>` | Legal because the trait is local; call sites depend on trait import and are less obvious. |
| Real local wrapper | `pub struct ChannelRequest(Request<MindRequest, MindBatchIntent>)` | Most type-correct for channel-specific methods; larger cascade because frame aliases and callers must unwrap or convert. |

`/175` corrects this by moving constructors to real types:

- single-op construction becomes default methods on `RequestPayload`;
- multi-op construction uses `BatchBuilder<Payload, Intent>`;
- per-channel aliases such as `ChannelBuilder` merely resolve generic
  parameters and call inherent methods that live on the real
  signal-core type.

That is the right direction. Keep it. The remaining naming detail:
`into_anonymous` / `into_tracked` / `into_named` are thin unless the
call site type says "request"; `into_anonymous_request` etc. may read
better if the method is commonly used outside typed context.

### 2. `BatchPolicy` is not mechanically connected

DA is correct. 174 says `Request::validate(&self)` consults the
channel policy, but 172's API only bounds `Payload: RequestPayload`.
There is no way for generic `Request<Payload, Intent>::validate` to
find a channel policy unless the policy is added to the type system.

The policy also likely depends on both `Payload` and `Intent`; an impl
only on `MindRequest` is under-specified.

`/175` tries to fix this with:

```rust
pub fn validate<Policy: BatchPolicy<P, I> = DefaultPolicy>(
    &self,
) -> Result<(), BatchVerbMismatch>
```

That shape does not compile. Rust does not allow default generic type
parameters on functions/methods. The corrected Rust shape needs either
two method names or a policy value.

Safer split:

```text
Request::validate()
  checks only universal Signal rules:
  - non-empty by type
  - verb/payload alignment
  - subscribe-tail position

Request::validate_with_policy::<Policy>()
  checks universal rules plus channel declarative policy:
  - max operation count
  - allowed verb mixes
  - per-intent restrictions
```

Concrete legal shape:

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
        // universal checks, then Policy checks
    }
}
```

Then contract receivers call:

```rust
request.validate_with_policy::<MindRequestPolicy>()?;
```

Do not make the generic request type magically discover policy without
a visible trait bound, and do not rely on invalid default generic
parameters on methods.

### 3. `custom_check` belongs outside contract crates

DA is correct. A closure in the macro invocation moves runtime
validation logic into a contract repo. That violates
`skills/contract-repo.md`: contracts own typed records and wire/text
derives, not validation pipelines or gate decisions.

`/175` removes `custom_check`; that is correct.

Keep macro policy declarative only:

```text
max_ops: 32
allow_mixed_read_write: true
forbid_subscribe: false
forbid_validate: false
```

Domain checks should be:

- typed `Validate` payloads crossing the channel, or
- daemon/runtime policy code using the contract types.

### 4. Lowercase NOTA annotations are wrong

DA is correct. Examples such as:

```text
[(intent SchemaUpgrade) (correlation cor-xyz) ...]
```

conflict with `skills/language-design.md`: NOTA has no new keywords
beyond truth values, and record heads are PascalCase. This should be
described as a Nexus/NOTA projection over typed records, not as a new
keyword grammar.

`/175` moves in the right direction with typed header records:

```text
(Batch (Named RoleHandoff "cor-abc-123")
       [(Retract (RoleClaim (role Designer)))
        (Assert  (RoleClaim (role Poet)))])
```

One refinement: avoid creating a parallel `BatchHeaderShape` if
`RequestHeader<Intent>` already is the concept. Prefer deriving the
NOTA projection on the real header type unless a separate projection
type has a concrete reason to exist.

The important constraint is that `intent` and `correlation` do not
become lowercase keyword records.

Also avoid saying "the NOTA grammar gains" unless `nota-codec` itself
changes. The better phrase is: the Signal/Nexus projection accepts a
NOTA sequence whose first element may be a typed header record.

### 5. 172 still carries stale four-parameter frame text

DA is correct. 172's macro-emission section still says:

```rust
Frame<MindRequest, MindBatchIntent, MindReply, MindBatchIntent>
```

That contradicts 174's three-parameter design. Fix before
implementation. This is exactly the kind of stale example operators
will copy.

`/175` and the current working copy of `/172` have fixed the main
`Frame<MindRequest, MindBatchIntent, MindReply, MindBatchIntent>`
examples. Some lower NOTA examples in `/172` still showed lowercase
`intent` / `correlation` while this report was written; those should
be swept before implementation.

### 6. `NoIntent` needs explicit trait requirements

DA is correct. `NoIntent` is not just a marker in prose; the generic
wire/text path will impose real bounds.

Minimum needed:

- `Archive`
- `Serialize`
- `Deserialize`
- bytecheck support through rkyv derive or manual impl
- `Debug`, `Clone`, `PartialEq`, `Eq`
- NOTA encode/decode behavior compatible with generic
  `RequestHeader<Intent>` parsing

Because `NoIntent` is uninhabited, encode can be an impossible match
and decode can always return a typed NOTA error when a named header
tries to decode one. This must be tested. If rkyv cannot derive cleanly
for an uninhabited enum in the selected feature set, the design needs
a different unconstructible shape, not a constructible unit struct.

`/175` names this as an empirical implementation check. That is the
right status.

## Additional Operator Findings

### A. Six verbs vs seven verbs must be explicitly superseded

172 says the root verbs are:

```text
Assert Mutate Retract Match Subscribe Validate
```

and `Atomic` is structural. Current `signal-core` and
`reports/designer/163-seven-verbs-no-structure-eighth.md` still carry
seven roots:

```text
Assert Mutate Retract Match Subscribe Atomic Validate
```

That is not a small macro edit. It changes:

- `SignalVerb`
- every contract variant mapped to `Atomic`
- tests that assert the verb set
- sema-engine operation-log shape
- batch construction and receive validation
- architecture and contract skill wording

This is fine if it is the chosen direction, but it must be named as a
breaking semantic migration: "six roots, no Atomic root." Otherwise
operators will accidentally mix the old and new models.

### B. Reply invariants should be typed, not comments

172 models per-op reply as:

```rust
pub struct SubReply<ReplyPayload> {
    pub verb: SignalVerb,
    pub status: SubStatus,
    pub payload: Option<ReplyPayload>,
}
```

and then states invariants:

```text
Ok iff payload is Some
RolledBack/Skipped imply payload is None
Failed may have detail
```

This is under-typed. The type system still permits invalid states,
for example `SubStatus::Ok` with `payload: None`.

A stronger shape:

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

That removes a whole validation surface. If every successful op really
must have a reply, this shape encodes it. If some successful ops have
no meaningful value, define an explicit acknowledgement payload in the
reply enum.

### C. Universal validation and runtime execution need two handles

`CheckedRequest<Payload, Intent>` should mean only:

```text
the wire request is structurally valid
```

It should not mean:

```text
the receiver can execute it
```

Those are different planes. A possible typed progression:

```text
Request<Payload, Intent>
  -> CheckedRequest<Payload, Intent>
  -> AcceptedRequest<Payload, Intent>
  -> ExecutedReply<ReplyPayload, Intent>
```

`CheckedRequest` is signal-core. `AcceptedRequest` is component
runtime policy. Execution is daemon-owned.

### D. Read-your-own-writes wording needs one sharpening

172 says pure reads share one snapshot, and mixed reads use
read-your-own-writes. The implementation model should say:

```text
Every batch starts from one base snapshot.
Each write creates an in-transaction overlay.
Each later op sees base snapshot + prior overlay.
Only completed write-bearing batches commit the overlay.
```

That phrasing avoids a possible contradiction between "shared
snapshot" and "reads see prior writes."

### E. Proc-macro is probably correct, but not first

174's proc-macro recommendation is sound once the target shape is
settled. The current core shape is still moving enough that a
proc-macro pass first would harden churn. Implement the core
primitives and tests first; then move the macro to proc-macro as the
contract surface catches up.

### F. Generated free functions are still suspect

`/175` suggests the macro may emit:

```rust
pub fn validate(request: &ChannelRequest) -> Result<(), BatchVerbMismatch> {
    request.validate::<MindRequestPolicy>()
}
```

That is a reusable free function in a contract crate. It also depends
on the invalid default-generic method syntax if written literally.
Prefer a method on `Request` (`validate_with_policy`) or a data-bearing
runtime policy object. If a contract-level policy marker is kept, it
should remain a trait witness with no inherent behavior, or be replaced
by declarative policy data.

## Suggested Implementation Gate

Before an operator changes code from 172/174, these should be settled
in the reports:

1. Confirm "six roots, no `Atomic` root" is the intended successor to
   the current seven-root implementation.
2. Replace all lowercase header examples with typed PascalCase NOTA
   records.
3. Remove all four-parameter `Frame` examples.
4. Replace `/175`'s invalid default-generic method signatures with a
   legal Rust shape.
5. Decide whether `SubReply` becomes a status enum carrying payloads
   directly.
6. Split universal request validation from channel/runtime policy,
   or specify the exact Rust trait bounds that connect policy to
   `Request::validate`.
7. Define and test `NoIntent`'s rkyv, bytecheck, and NOTA behavior.

## Operator Lean

The strongest implementation path is:

```text
1. Rewrite signal-core primitives:
   SignalVerb without Atomic, Request<Payload, Intent>,
   RequestHeader, NonEmpty, Op, CheckedRequest, Reply, SubReply.

2. Add universal validation only:
   verb/payload match, subscribe-tail, non-empty by type.

   Then add explicit policy validation through a legal method:
   `validate_with_policy::<MindRequestPolicy>()`.

3. Add typed tests:
   - mismatched verb rejected with original request recoverable
   - empty batch cannot construct / cannot bytecheck
   - subscribe in middle rejects
   - NoIntent cannot construct Named header
   - SubReply invalid states cannot compile or cannot construct

4. Only then redesign `signal_channel!`:
   generate payload enums, intent enum or NoIntent alias,
   RequestPayload impl, kind enum, payload methods, frame aliases.

5. Defer channel policy beyond declarative data until the first real
   daemon needs it.
```

This keeps the semantic kernel clean and prevents the macro from
becoming the place where unresolved design questions are hidden.
