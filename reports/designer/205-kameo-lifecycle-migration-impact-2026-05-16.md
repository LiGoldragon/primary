# 205 — Kameo lifecycle migration impact on Persona

Date: 2026-05-16
Role: designer
Scope: assess how operator/130's Kameo lifecycle change affects
Persona component implementations. Direct API breaks, migration
patterns Persona should adopt, and operational risks not
explicitly asked about.

References:
- `reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md` — the design
- `reports/operator/130-kameo-terminal-lifecycle-implementation.md` — landed implementation
- `reports/designer-assistant/98-review-operator-130-kameo-lifecycle-implementation.md` — HIGH gaps still open
- `reports/designer-assistant/99-review-current-designer-204-kameo-lifecycle.md` — /204 review
- kameo branch `kameo-push-only-lifecycle` commit `1329a646`

## 0. TL;DR

**Public usage is affected — three breaking changes, one silent
semantic change, one signature break.** Most Persona actors that
implement `on_link_died` need a one-line signature update.
Anywhere Persona uses `is_alive()` as a terminal predicate now
races cleanup — silent bug class until grepped and migrated.

**Three migration patterns Persona should adopt:**
1. **Branch on `outcome.state` in supervisors** instead of
   relying on supervised-restart magic.
2. **Test resource-release falsifiably per component** —
   redb file lock, socket unbind, child process exit.
3. **Replace `is_alive()` with explicit phase queries** —
   `is_running()` for sendability, `is_terminated()` for
   doneness.

**Five things the request didn't ask about but are
load-bearing:**

- The HIGH correctness gaps in operator/130 (DA/98 §1.1 + §1.2)
  are blockers for safe Persona adoption. Pinning to
  `1329a646` *as-is* risks deadlock and stale-message-across-
  restart bugs in production.
- The supervised `spawn_in_thread` case (StoreKernel Template-2
  deferral) is not specifically tested in operator/130's six
  lifecycle tests — verification still pending.
- `is_alive()` semantic shift is a SILENT migration trap.
- Persona component ARCHs reference stale lifecycle terminology
  (`StateReleased`, `LinksNotified`); need a sweep.
- The `shutdown_result` compat surface should be deprecated;
  Persona should migrate off it explicitly rather than letting
  it linger.

## 1. Direct API breaks — what compiles differently

### 1.1 `wait_for_shutdown()` now returns `ActorTerminalOutcome`

**Old:**
```rust
actor_ref.wait_for_shutdown().await;
// just resumes; no return value used
```

**New:**
```rust
let outcome = actor_ref.wait_for_shutdown().await;
// outcome: ActorTerminalOutcome { state, reason }
```

**Impact:** existing call sites that ignore the return compile
fine (just `let _ = ...await`). Call sites that previously did
`actor.wait_for_shutdown().await` as a statement (no `let`)
also compile — the return value is just dropped.

**Migration cost:** zero forced, but every call site is now a
correctness opportunity. Supervisors that previously didn't
know *why* the child stopped can now branch.

### 1.2 `on_link_died` signature changed (BREAKING)

**Old:**
```rust
async fn on_link_died(
    &mut self,
    actor_ref: WeakActorRef<Self>,
    id: ActorId,
    reason: ActorStopReason,
) -> Result<ControlFlow<ActorStopReason>, Self::Error>
```

**New:**
```rust
async fn on_link_died(
    &mut self,
    actor_ref: WeakActorRef<Self>,
    id: ActorId,
    outcome: ActorTerminalOutcome,
    reason: ActorStopReason,
) -> Result<ControlFlow<ActorStopReason>, Self::Error>
```

**Impact:** every Persona actor that overrides `on_link_died`
needs the new parameter. The default impl handles the case
where the actor doesn't override.

**Grep targets** to find affected sites across Persona crates:
```sh
rg "fn on_link_died" /git/github.com/LiGoldragon/persona*
```

### 1.3 `is_alive()` semantics changed silently (HIGH RISK)

**Old strong** (`ActorRef`): `!mailbox_sender.is_closed()`
— flips false at terminal shutdown (mailbox sender closed
when receiver drops, late in the sequence).

**Old weak** (`WeakActorRef`): `!shutdown_result.initialized()`
— flips false at `CleanupFinished` boundary.

**New both**: `is_accepting_messages()` — flips false at
`AdmissionStopped`, which is **the FIRST step** of shutdown.

**Impact:** any Persona code that uses `is_alive()` to mean
"is this actor still functional / can I act as if it's done?"
now races the cleanup path. The window between
`!is_alive()` and `is_terminated()` is the entire shutdown
sequence — including `on_stop`, drop, link-notify, registry
removal.

**Concrete failure mode:**
```rust
// Persona code somewhere:
if !child.is_alive() {
    // OLD: child was terminated; safe to restart
    // NEW: child STARTED shutdown; cleanup may still be in-flight;
    //      restarting now races the resource release.
    spawn_replacement(&child.id).await;
}
```

**Migration:** replace with explicit predicate:
- `if !child.is_accepting_messages()` if asking "can I send?"
- `if child.is_terminated()` if asking "is shutdown complete?"
- Better still: `let outcome = child.wait_for_shutdown().await;`

This is **the most important migration** — silent semantic
change in a method many actors call.

### 1.4 `ActorStopReason` is now compatibility surface

`ActorStopReason` still exists and is returned by
`shutdown_result.wait()`. The new contract is
`ActorTerminalOutcome`. Persona should migrate to the new
shape.

| Old | New |
|---|---|
| `let reason = actor.shutdown_result.wait().await;` | `let outcome = actor.wait_for_shutdown().await;` |
| `match reason { ActorStopReason::Normal => ... }` | `match outcome.reason { ActorTerminalReason::Stopped \| SupervisorRestart => ... }` |

The compat surface won't go away on its own. Persona should
plan explicit removal.

### 1.5 `ActorTerminalReason` has more variants than /204 anticipated

Operator added `SupervisorRestart`, `LinkDied`,
`PeerDisconnected` to match existing kameo semantics. Persona
supervisors that pattern-match on `outcome.reason` need to
handle all variants explicitly or use `_ =>`.

```rust
match outcome.reason {
    ActorTerminalReason::Stopped => /* clean stop */,
    ActorTerminalReason::SupervisorRestart => /* supervisor will restart */,
    ActorTerminalReason::Killed => /* killed but cleanup ran */,
    ActorTerminalReason::Panicked => /* panic */,
    ActorTerminalReason::StartupFailed => /* on_start failed */,
    ActorTerminalReason::CleanupFailed => /* on_stop failed */,
    ActorTerminalReason::LinkDied => /* linked actor died */,
    #[cfg(feature = "remote")]
    ActorTerminalReason::PeerDisconnected => /* cluster disconnect */,
}
```

## 2. Migration patterns Persona should adopt

### 2.1 Pattern — supervisor branches on `outcome.state`

The audit's most valuable consequence. Old supervisor code
treated all stops the same; new code can distinguish:

```rust
pub async fn supervise_child(&mut self, child: ActorRef<Child>) {
    let outcome = child.wait_for_shutdown().await;
    match outcome.state {
        ActorStateAbsence::Dropped => {
            // Resource released; safe to restart against same handle
            self.restart_child().await;
        }
        ActorStateAbsence::NeverAllocated => {
            // Startup failed; restart is a retry of construction
            if self.retry_budget_remaining() {
                self.restart_child().await;
            } else {
                self.escalate().await;
            }
        }
        ActorStateAbsence::Ejected => {
            // Supervised actors should not be ejection-mode
            unreachable!("supervised actors use run_to_termination");
        }
    }
}
```

This is the supervisor pattern /204 unblocks. **Persona's
component supervisors should adopt it before depending on the
new Kameo for production correctness.**

### 2.2 Pattern — falsifiable resource-release witnesses per component

The kameo `tests/lifecycle_phases.rs::lifecycle_phase_waiters_are_push_driven_and_terminal_is_post_release`
test proves resource release for a `TcpListener`. Persona
should write the equivalent for each exclusive-resource actor:

```rust
// persona-mind tests/store_kernel_release.rs
#[tokio::test(flavor = "multi_thread")]
async fn store_kernel_releases_redb_file_lock_before_terminal() {
    let temp = tempfile::tempdir().unwrap();
    let path = temp.path().join("test.redb");

    let kernel = StoreKernel::spawn_in_thread(path.clone());
    kernel.tell(WriteSomething).await.unwrap();
    kernel.stop().await.unwrap();

    let outcome = kernel.wait_for_shutdown().await;
    assert_eq!(outcome.state, ActorStateAbsence::Dropped);

    // The reason the kameo fix matters: this must succeed.
    let fresh_kernel = StoreKernel::spawn_in_thread(path);
    fresh_kernel.tell(ReadSomething).await.unwrap();
}
```

Components that need this test:
- `persona-mind::StoreKernel` — redb file lock
- `persona-terminal::TerminalCell` — control.sock unbind
- `persona-harness::HarnessChild` — child process exit
- `persona-router::HarnessDelivery` — currently Template 1
  (DelegatedReply); not exclusive, no witness needed yet

### 2.3 Pattern — replace `is_alive()` with explicit predicates

Audit Persona code for `is_alive()` calls and replace each
with the precise predicate:

```rust
// Pattern 1: send-safety check
- if actor.is_alive() { actor.tell(msg).await }
+ if actor.is_accepting_messages() { actor.tell(msg).await }
+ // or simpler — just attempt the send and handle SendError::ActorStopping

// Pattern 2: terminal-doneness check
- if !actor.is_alive() { spawn_replacement().await }
+ if actor.is_terminated() { spawn_replacement().await }

// Pattern 3: wait for done
- while actor.is_alive() { tokio::time::sleep(Duration::from_millis(10)).await; }  // POLLING — BAD
+ let _outcome = actor.wait_for_shutdown().await;                                    // PUSH — RIGHT
```

The third pattern is also a `skills/push-not-pull.md` win —
polling `is_alive()` was a hidden carve-out that the new API
makes unnecessary.

### 2.4 Pattern — `on_link_died` branches on `outcome.reason`

The new `outcome` parameter enables clean branching that the
legacy `ActorStopReason` alone couldn't express well:

```rust
async fn on_link_died(
    &mut self,
    _ref: WeakActorRef<Self>,
    id: ActorId,
    outcome: ActorTerminalOutcome,
    _legacy_reason: ActorStopReason,
) -> Result<ControlFlow<ActorStopReason>, Self::Error> {
    match outcome.reason {
        ActorTerminalReason::Stopped
        | ActorTerminalReason::SupervisorRestart => {
            // Clean stop; resource released; ignore
            Ok(ControlFlow::Continue(()))
        }
        ActorTerminalReason::CleanupFailed => {
            // Hook failed; resource state suspect
            tracing::warn!(?id, "child cleanup failed");
            self.respawn_with_fresh_state(id).await?;
            Ok(ControlFlow::Continue(()))
        }
        ActorTerminalReason::Panicked
        | ActorTerminalReason::StartupFailed => {
            // Hard failure; escalate
            Ok(ControlFlow::Break(ActorStopReason::LinkDied { /* ... */ }))
        }
        _ => Ok(ControlFlow::Continue(())),
    }
}
```

Persona's supervisors should adopt this richer branching.
Prefer `outcome.reason` over `_legacy_reason`.

## 3. Things this question didn't ask about

### 3.1 The HIGH gaps in operator/130 are adoption blockers

Per DA/98:

- **§1.1**: lifecycle/control signals share the user bounded
  mailbox. Deadlock failure mode: parent handler awaits
  child's `wait_for_shutdown`; child tries to send `LinkDied`
  through parent's mailbox; parent can't process it until the
  handler returns; child's shutdown blocks on the parent's
  send queue.
- **§1.2**: admission gate is checked before
  `send().await`; pending bounded sends can cross the
  admission close and land in a replacement actor's reused
  mailbox after supervised restart.

**Implication for Persona adoption:** pinning to operator/130
*as-is* (commit `1329a646`) ships these failure modes. The
StoreKernel single-owner topology (DA/96 §2) closes the bug
class at the application layer regardless — but components
that don't decompose this way are exposed.

**Recommendation:** wait for the next operator pass (which
addresses both HIGH gaps) before workspace-wide Kameo pin.
Until then, Path B (single-owner topology) is the safer move
for new resource-owning actors.

### 3.2 The supervised `spawn_in_thread` case is not specifically tested

Operator/130 added six lifecycle tests; the directly relevant
ones for the StoreKernel Template-2 deferral are:
- `supervisor_restart_waits_for_terminal_outcome_before_replacement_start`

But that test uses `.spawn()` (regular Tokio task), not
`.spawn_in_thread()` (dedicated OS thread). The Template-2
specific bug — supervised `spawn_in_thread` releases parent's
`wait_for_shutdown` before the OS thread runs `Drop` — is
*not* covered by operator/130's test suite.

**Recommendation:** operator's next pass adds:
```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn supervised_spawn_in_thread_releases_resource_before_supervisor_restart() {
    // Supervisor parent + child that owns TcpListener via spawn_in_thread.
    // Child panics or stops; supervisor's on_link_died receives outcome.
    // outcome.state == Dropped must be true.
    // Parent immediately tries to bind same port from replacement spawn.
}
```

Until this test passes, the `persona-mind/src/actors/store/mod.rs:295-307`
deferral comment cannot be removed even with the kameo fix —
the regression it guards against has not been falsifiably
verified in operator/130.

### 3.3 Persona component ARCHs reference stale lifecycle terms

The earlier work in this session's prior arc (the lost
`/184-/200` reports) updated multiple Persona component
ARCHs with references to `StateReleased`, `LinksNotified`,
and the 8-phase model. After /204 + operator/130, those
terms are obsolete.

Components likely affected (based on conversation summary):
- `persona/ARCHITECTURE.md`
- `persona-mind/ARCHITECTURE.md`
- `persona-router/ARCHITECTURE.md`
- `persona-terminal/ARCHITECTURE.md`
- `persona-system/ARCHITECTURE.md`
- `signal-persona-*/ARCHITECTURE.md`

**Recommendation:** designer-side sweep to update these ARCHs
to reference `ActorTerminalOutcome` + `ActorStateAbsence`
instead of the retired phase model. Per
`skills/architecture-editor.md`: ARCHs describe present, not
history.

### 3.4 `shutdown_result` compatibility surface should be deprecated

Operator/130 keeps `shutdown_result` as a compat surface that
now waits for terminal outcome before returning the legacy
`ActorStopReason`/`PanicError`. This is correct for transition
but creates two parallel APIs indefinitely.

**Recommendation:** mark `shutdown_result.wait()` /
`get_shutdown_result()` / `wait_for_shutdown_result()` with
`#[deprecated(note = "use wait_for_shutdown() returning ActorTerminalOutcome")]`
in a follow-up operator pass. Set a date for removal. Persona
should migrate off these methods before the removal date.

### 3.5 `PeerDisconnected` lies about state

`ActorTerminalOutcome::peer_disconnected()` sets
`state: Dropped`, but the local node cannot prove the remote
actor's state was actually dropped (the remote node might
have crashed mid-`on_stop`, the network might be partitioned,
etc.).

If Persona ever enables `kameo` with `feature = "remote"`
(currently off per `skills/kameo.md` §"Module map"), the
`PeerDisconnected` lie becomes real. **Recommendation:** when
Persona considers turning `remote` on, first push a kameo
fork change that introduces an `ActorStateAbsence::Unknown`
variant for the remote-disconnect case, and have
`peer_disconnected()` use that.

### 3.6 `on_stop` is unbounded — bound it explicitly per Persona actor

The new contract is "release-before-notify" but doesn't bound
how long `on_stop` can take. A Persona actor whose `on_stop`
awaits forever (or panics in a `Drop` impl after `on_stop`)
holds the entire supervisor's restart sequence forever.

This isn't introduced by the kameo fix — it was always true —
but the fix makes it more *visible* because supervisors now
correctly wait. Persona should:
- Bound `on_stop` async work with `tokio::time::timeout`.
- Keep `Drop` impls in actor state types non-blocking where
  possible (or document the bound explicitly).

The future `Shutdown::Brutal` variant (/204 §1.1) is the
OTP-shape escape hatch for when `on_stop` hangs — until that
lands, Persona's discipline is explicit timeouts inside
`on_stop`.

### 3.7 Migration ordering matters across the workspace

If Persona pins to the new kameo branch piecemeal (some
components, not others), the test infrastructure mixes
old-API and new-API actors. This isn't safe — actors talking
across the API boundary will have inconsistent `on_link_died`
signatures.

**Recommendation:** workspace-wide Kameo pin landing should be
a single coordinated PR across all Persona crates, with
preceding sweep PRs that:
1. Update each crate's `on_link_died` impls to the new
   signature.
2. Replace `is_alive()` calls with explicit predicates.
3. Update supervisor `wait_for_shutdown` callers to branch
   on outcome.

Then a single pin PR moves the workspace's `Cargo.lock`
forward.

## 4. Concrete migration checklist

For each Persona crate that uses Kameo:

- [ ] Grep for `is_alive()` → migrate to `is_accepting_messages()` or `is_terminated()` per intent
- [ ] Grep for `on_link_died` overrides → add `outcome` parameter
- [ ] Grep for `wait_for_shutdown` callers → consider whether to branch on outcome
- [ ] Grep for `shutdown_result` → plan migration to `wait_for_shutdown`
- [ ] If actor owns exclusive resource → add per-component resource-release test
- [ ] If actor's ARCH mentions `StateReleased` / `LinksNotified` / `ActorLifecyclePhase` → update to `ActorTerminalOutcome` terminology
- [ ] If actor uses `kill()` / `abort()` → verify `on_stop` is bounded with timeout

For the workspace overall:

- [ ] Wait for operator's next pass (HIGH gaps closed) before workspace pin
- [ ] Single coordinated PR for Kameo pin advancement
- [ ] StoreKernel migration (Path B per DA/96 §5.2) lands independently of Kameo version — works on vanilla 0.20

## 5. The deeper observation

The Kameo change is bigger than an API delta — it shifts the
correctness boundary from "convention you hope users follow"
to "contract the framework enforces." That's a one-way
improvement.

But the Persona side hasn't fully internalized this yet.
Components still:
- Use `is_alive()` (now ambiguous)
- Don't branch on terminal outcome
- Don't have falsifiable resource-release tests
- May rely on `shutdown_result` legacy surface

This migration is an opportunity to make Persona's actor
discipline match the framework's. Skipping it leaves
correctness gaps that the framework can no longer paper over.

## 6. Sources

- `reports/designer/204-kameo-lifecycle-canonical-design-2026-05-16.md`
- `reports/operator/130-kameo-terminal-lifecycle-implementation.md`
- `reports/designer-assistant/98-review-operator-130-kameo-lifecycle-implementation.md`
- `reports/designer-assistant/99-review-current-designer-204-kameo-lifecycle.md`
- `reports/designer-assistant/96-kameo-lifecycle-independent-pov-2026-05-16.md` — single-owner storage topology
- kameo commit `1329a646` — `actor: publish terminal lifecycle outcomes`
- `skills/kameo.md` §"Blocking-plane templates" — Template 1/2/3 patterns
- `skills/actor-systems.md` §"Supervision gotcha — Template 2"
- `skills/push-not-pull.md` — relevant to `is_alive` polling replacement
