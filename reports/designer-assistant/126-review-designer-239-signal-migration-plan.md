# Review Of Designer 239 Signal Migration Plan

Date: 2026-05-19
Role: designer-assistant
Target: `reports/designer/239-signal-architecture-migration-plan.md`

## Verdict

`reports/designer/239-signal-architecture-migration-plan.md` is the right
migration direction: `signal-frame` owns frame/exchange mechanics,
`signal-sema` owns Sema execution vocabulary, and component contracts expose
contract-local public operation verbs.

The report is implementation-useful, but four parts need correction before
operators treat it as a complete playbook:

1. The universal observer hook is too broad and too trusting.
2. `signal-frame` still carries database-shaped semantics through "atomic"
   request language and per-operation reply outcomes.
3. The transparent `Operation<Payload>` wrapper and always-OK
   `Request::check()` are suspicious transitional surfaces.
4. The plan asks architecture and skill files to reference reports, which
   violates current workspace guidance.

## Current Foundation State

The foundation repositories already exist locally:

```text
/git/github.com/LiGoldragon/signal-frame
/git/github.com/LiGoldragon/signal-sema
```

`signal-frame/ARCHITECTURE.md` says the split has landed:

- `signal-frame` is domain-free and verb-free.
- `Operation<Payload>` is transparent and carries only payload.
- `Request<Payload>` is `NonEmpty<Operation<Payload>>`.
- The `signal_channel!` macro is still transitional and still emits references
  to removed types such as `SignalVerb` and `RequestPayload::signal_verb()`.

`signal-sema/ARCHITECTURE.md` says:

- `SemaOperation` owns `Assert`, `Mutate`, `Retract`, `Match`, `Subscribe`,
  and `Validate`.
- `PatternField<T>`, `Bind`, `Wildcard`, `Slot<Payload>`, and `Revision` live
  there.
- `signal-sema` does not depend on `signal-frame`.

So `/239` is no longer merely a plan for future repo creation. It is now the
coordination document for finishing an already-started split.

## Finding 1: Observer Hook Is Too Broad

`/239 §3.F` says:

> Every daemon publishes its operations and Sema effects to optional observers.
> Subscription lives on the public socket. Observation is not a security concern
> — no secrets cross the wire.

That last sentence is not safe.

Inbound contract operations and lower Sema effects can contain sensitive
material:

- user messages;
- private intent records;
- daemon configuration;
- repository paths and commit messages;
- credentials if an owner contract is poorly shaped;
- future keys, tokens, model prompts, or system paths.

The psyche's current answer was not "always log everything" and not "public
observation is harmless." It was:

```text
If persona-introspect subscribes to an event class, the component emits or
records that event class; otherwise it is not necessarily logged unless normal
operation already requires it.
```

That implies subscription-driven introspection, not a universal public debug
tap.

### Correction

Replace "universal observer hook on public socket" with a typed observation
relation:

```text
ordinary signal-<component>
  exposes non-sensitive observation classes that are safe for peer callers

owner-signal-<component>
  exposes privileged observation classes, including owner configuration and
  sensitive state-effect traces

persona-introspect
  subscribes to the classes it is allowed to observe
```

The rule should be event-class-specific. Some observation classes can be public
within the trusted local federation. Some should require owner authority. Some
should not exist at all.

## Finding 2: `signal-frame` Still Says Atomic Too Strongly

`/239` says `signal-frame` retains:

```text
Operation<Payload>
Request<Payload>
NonEmpty<T> for atomic operation sequences
Reply plumbing with per-operation outcomes
```

The current `signal-frame/ARCHITECTURE.md` also says:

```text
Multi-operation atomicity is structural — the Request<Payload>'s NonEmpty<Operation>
sequence is the unit.
```

This smells like Sema semantics leaking back into the frame layer.

Under the old model, atomicity belonged naturally in `Request` because every
operation was a database-shaped operation. Under the new model, public contract
operations can be domain actions:

```nota
(Submit (Message ...))
(Query (RecentRepositories ...))
(Configure (...))
(Handoff (...))
```

A sequence of public domain actions is not automatically a database transaction.
It may involve routing, forwarding, process spawning, external effects, or
policy decisions. Sema atomicity begins only after the daemon lowers a public
operation into a Sema operation plan.

### Correction

`signal-frame` should probably say:

```text
Request<Payload> is a non-empty exchange sequence.
It preserves operation order and pairs per-operation replies positionally.
It does not itself promise database atomicity.
Atomic commit semantics belong to signal-sema / sema-engine, or to a specific
contract that explicitly promises atomic handling of its public operations.
```

If the workspace still wants a multi-operation public contract request to be
all-or-abort at the contract level, that must be a deliberate contract
semantics decision, not a universal frame guarantee.

## Finding 3: Transparent `Operation` May Not Earn Its Seat

Current `signal-frame/src/operation.rs` says `Operation<Payload>` is now just:

```rust
pub struct Operation<Payload> {
    pub payload: Payload,
}
```

Its NOTA codec emits the payload directly. It carries no verb, no transport
identifier, no timestamp, no policy, and no frame metadata.

There are two possible answers:

1. Keep it because "operation" is the semantic unit that aligns with
   per-operation replies.
2. Delete it and let `Request<Payload>` be `NonEmpty<Payload>`.

The current wrapper is not wrong, but it should be made to earn its place. If
it is only a naming wrapper around payload, it may be transitional ceremony
left over from the old `SignalVerb` design.

### Question

Should `Operation<Payload>` remain as a semantic unit even though it has no
fields beyond payload, or should `Request<Payload>` become `NonEmpty<Payload>`
under the contract-local-verb design?

## Finding 4: `Request::check()` Returning `Ok(())` Is A False Witness

Current `signal-frame/src/request.rs` keeps:

```rust
pub fn check(&self) -> Result<(), RequestRejectionReason> {
    Ok(())
}
```

The comment says this is retained so existing call sites that defensively
validate before sending continue to compile.

That is backward-compatibility thinking in a part of the system that is being
redesigned specifically to avoid preserving the wrong shape. A method named
`check()` that always succeeds can mislead future agents into thinking frame
validation happened.

### Correction

Prefer one of:

```text
Remove Request::check() entirely.
```

or:

```text
Rename it to a construction helper whose name does not imply validation.
```

If there are still universal frame invariants, implement those. If there are no
universal checks, do not keep a no-op validator.

## Finding 5: Macro Redesign Is The Hard Gate

`/239` says Phase 1 includes "the `signal_channel!` macro is updated." The
local `signal-frame/macros/README.md` is more explicit: the macro currently
compiles as a proc-macro crate but emits code that cannot compile because it
references removed `SignalVerb` surfaces.

That means no contract migration can be considered real until there is a
positive contract fixture that uses the new grammar and compiles.

### Completion Criterion

Phase 1 should require:

```text
signal-frame positive macro fixture using:
  signal_channel! { channel Ledger { operation Query(Query) ... } ... }

generated code compiles
generated NOTA round trips compile and pass
streaming channel fixture compiles if stream support stays in v1
compile-fail fixtures cover old verb-tagged grammar rejection
```

Without that, every component migration is blocked or will hand-roll what the
macro should emit.

## Finding 6: Architecture Files Must Not Reference Reports

`/239 §3.G` says affected `ARCHITECTURE.md` files should reference `/239` and
`/238`. `§8` says components should add a `MUST IMPLEMENT` section pointing
back at `/239` and `/238`.

This conflicts with `skills/architecture-editor.md`:

```text
ARCHITECTURE.md files do not cite reports.
```

The correct pattern:

- Reports can coordinate the migration.
- Architecture files inline the current shape and constraints.
- Temporary `MUST IMPLEMENT` notes can name the local missing shape, but should
  not depend on report paths for meaning.

If a report path is needed as implementation coordination, keep it in the bead,
task, or report. Permanent architecture should stand without it.

## Finding 7: Skills Must Not Reference Reports

`/239 §5` says skill edits are part of Phase 1. That is right. But current
`skills/contract-repo.md` already contains direct references to
`reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`.

That conflicts with `skills/skill-editor.md`:

```text
Skills do not cite reports.
```

The skill should inline the rule:

```text
Public contract operations are contract-local verbs.
The six former universal roots are Sema execution vocabulary.
```

It should not cite the report path. Reports retire; skills do not.

Also, the current `skills/contract-repo.md` section has a duplicate sentence:

```text
The payload that follows the operation is usually a noun:
The payload that follows the operation is usually a noun:
```

That is minor, but it signals the skill edit needs a cleanup pass before being
treated as canonical.

## Finding 8: `signal-sema` Dependency Scope Needs Precision

`/239` says add `signal-sema` if a component "uses Sema operations internally
for executor lowering / introspection."

That may be too broad. If every triad daemon uses sema-engine for state, but
only sema-engine itself needs to traffic in `SemaOperation`, then forcing every
daemon to depend on `signal-sema` recreates a universal layer by another route.

Possible split:

```text
Daemon uses sema-engine API directly.
sema-engine depends on signal-sema for typed operation/effect vocabulary.
Daemon depends on signal-sema only if it emits typed SemaEffect observations,
speaks signal-sema on a socket, or constructs explicit Sema plans as data.
```

That preserves `signal-sema` as a real contract/vocabulary rather than a
required import for every stateful component.

## Questions To Bring Forward

### Q1. Observation permissions

Should observation of inbound operations and lower Sema effects really live on
the ordinary public socket for every component?

My recommendation: no. Make observation event classes permissioned. Ordinary
socket observation can exist for safe classes; owner-signal or a dedicated
introspection authority should be required for sensitive classes.

### Q2. Frame-level atomicity

Should `signal-frame::Request` still promise atomicity?

My recommendation: no. Rename the guarantee to ordered non-empty exchange
sequence. Atomic commit belongs to `signal-sema` / sema-engine or to a specific
contract that explicitly promises atomic public-operation execution.

### Q3. `Operation<Payload>` wrapper

Should `Operation<Payload>` survive if it only contains `payload`?

My recommendation: decide explicitly. Keep only if the name "operation" as a
semantic per-reply unit is worth the wrapper. Otherwise simplify
`Request<Payload>` to `NonEmpty<Payload>`.

### Q4. No-op request validation

Should `Request::check()` remain if it always returns `Ok(())`?

My recommendation: remove it. A no-op check is worse than no check because it
creates a false witness.

## Bottom Line

`/239` is the right migration direction but should be tightened before it is
treated as an operator playbook. The most important correction is to stop
letting frame mechanics carry hidden database semantics. If public verbs are
contract-local, then atomicity, validation, and observation permissions also
need to move to their rightful layers instead of staying in `signal-frame` by
habit.
