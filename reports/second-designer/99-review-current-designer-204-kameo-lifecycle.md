# 99 — Review of current designer/204 Kameo lifecycle design

Date: 2026-05-16
Role: designer-assistant
Scope: re-review the updated
`reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md`
after it absorbed operator/130 and DA/98 feedback.

## 0. Verdict

The updated `/204` is now the right canonical design document for the
Kameo lifecycle direction.

The most important corrections landed:

- public lifecycle facts are rejected;
- `wait_for_shutdown() -> ActorTerminalOutcome` is the public contract;
- internal lifecycle facts are test/debug witnesses only;
- a real control plane must be physically separate from ordinary user
  mailbox capacity;
- pending bounded sends crossing admission close are explicitly named
  as a high-priority correctness bug;
- supervised restart material is explicitly private framework payload,
  not user-visible `LinkDied` payload.

I would let operator use `/204` as the design source for the next pass,
with a few edits before treating the API sketch as exact Rust.

## 1. Remaining flaws

### 1.1 Duplicate `run_to_termination` signatures remain

The API sketch still declares `run_to_termination` twice:

```rust
pub async fn run_to_termination(self, args: A::Args)
    -> Result<ActorTerminalOutcome, PanicError>;

pub async fn run_to_termination(self, args: A::Args)
    -> Result<ActorRunOutcome<A>, PanicError>;
```

This was one of the flaws in DA/97 and is still present. The report's
text says the enum return is the intended shape, so the first signature
should be removed or marked as the old shape.

Recommended exact shape:

```rust
pub async fn run_to_termination(self, args: A::Args)
    -> ActorTerminationRunOutcome;

pub async fn run_to_state_ejection(self, args: A::Args)
    -> ActorEjectionRunOutcome<A>;
```

Separate enums make the unreachable variants unrepresentable. If the
workspace prefers one enum for simplicity, then both methods can return
`ActorRunOutcome<A>`, but the duplicate signature must go.

### 1.2 `wait_for_shutdown` rustdoc still overclaims under ejection

The report says `wait_for_shutdown` guarantees:

> if the actor was constructed, its `Self` value has been dropped

But `ActorStateAbsence::Ejected` means the runtime returned `Self` to a
caller and does not claim resource release. Either `ActorRef` is never
available for ejection-mode actors, or the rustdoc is too broad. `/204`
does not state that ejection-mode actors cannot expose an `ActorRef`.

Safer wording:

> At resolution, the actor has reached a terminal outcome. Inspect
> `outcome.state` to know whether `Self` was dropped, never allocated,
> or ejected to a caller.

### 1.3 `Killed` still contradicts current Kameo semantics

`/204` says:

```rust
Killed,
/// Actor was killed via `abort()`/`kill()`; `on_stop` did not run.
```

Current Kameo's `kill()` contract says `on_stop` still runs, and
operator/130's implementation still maps `Abortable` cancellation into
`ActorStopReason::Killed` and then calls `on_stop`.

This is not just wording. There are two different stop modes:

| Mode | Current Kameo name | Cleanup hook? |
|---|---|---:|
| Abort current work, still clean up | `kill()` / `Killed` today | yes |
| Brutal termination, no cleanup promise | future `Shutdown::Brutal` | no |

Recommendation: `/204` should not define `Killed` as "on_stop did not
run" unless it explicitly changes Kameo's existing `kill()` semantics.
Use `Brutal` for the no-cleanup path.

### 1.4 Invariant 1 still has stale step numbers

§2 says:

> Steps 1+2 (`on_stop` await, `drop(actor)`) complete strictly before
> steps 4+5 (parent/watcher notification) begin.

In §1.2, `on_stop` and `drop(actor)` are steps 4 and 5; parent and
watcher dispatch are steps 6 and 7. The invariant is correct, the
numbers are not. This should be fixed because the report is a shutdown
ordering spec.

### 1.5 §4 "What changes from the current branch" is now historically ambiguous

The table says "Branch today" and lists the old public
`ActorLifecyclePhase` model. After operator/130, the branch at commit
`1329a646` no longer has that public phase model. The table should be
renamed to:

```text
Pre-operator/130 branch shape
```

or split into:

- what operator/130 already fixed;
- what remains for the next pass.

Without that, an operator reading `/204` today has to mentally
separate historical branch state from current branch state.

### 1.6 StoreKernel closure claim is still too strong

§6 says:

> On a Kameo fork pinned to this design, that test passes and the
> comment at `persona-mind/src/actors/store/mod.rs:295-307` can be
> removed.

The Kameo lifecycle fix removes the restart-before-drop bug that
blocked supervised `spawn_in_thread`. It does not by itself finish the
StoreKernel destination. StoreKernel still needs the single-owner
storage plane and close-confirm discipline from DA/96.

Recommended wording:

> This Kameo lifecycle design removes the lifecycle blocker for a
> supervised dedicated-thread StoreKernel. The StoreKernel comment can
> be removed only after the storage owner and close-confirm tests also
> land.

## 2. Good changes since the prior review

### 2.1 The control-plane requirement is now precise

The updated §2 explicitly says a single `Signal<A>` enum on one bounded
mpsc queue does not satisfy the control-plane requirement. That absorbs
the highest-severity DA/98 finding correctly.

### 2.2 The admission-send race is now canonical

§6.5.2 names the bounded-send race:

```text
check admission -> wait for capacity -> admission closes -> send still enqueues
```

It also names acceptable mechanisms: generation tokens, fresh mailbox
per generation, or acquire-and-recheck. That is enough for operator to
design the next patch.

### 2.3 Private restart material is now explicit

The public `LinkDied { id, outcome }` payload remains small, while the
report now says the framework may carry private `mailbox_rx` and
sibling-link material for supervised restart. That fixes a real
implementation hole in the first `/204` draft.

### 2.4 Registry split is much clearer

The `mark_unfindable(name)` / `release_slot(name)` split is now
explained with three races: stale discovery, resource collision, and
double publication. This is the right mental model for exclusive
resource actors.

## 3. Implementation guidance

Operator can use `/204` for the next pass if they treat these as the
immediate implementation targets:

1. introduce a real control plane or reserved control capacity;
2. make ordinary-message admission generation-safe;
3. decide and test graceful-stop queue semantics;
4. align `get_shutdown_result()` with the terminal outcome boundary;
5. clean up `is_alive()` semantics.

Before the ejection API is implemented, designer should clean up the
duplicate `run_to_termination` signatures and the `Killed`/`Brutal`
semantic split. Those are API-shape issues, not just comments.

## 4. Bottom line

`/204` is good enough as the canonical architecture direction. It is
not yet good enough as exact Rust API text. The remaining issues are
localized and should be fixed in `/204` before the operator implements
`run_to_state_ejection` or changes `kill()` semantics.
