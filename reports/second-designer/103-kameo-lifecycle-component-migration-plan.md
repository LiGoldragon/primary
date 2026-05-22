# 103 — Kameo lifecycle fresh audit and component migration plan

Date: 2026-05-16
Role: designer-assistant
Audience: operator / operator-assistant
Scope: fresh audit of `reports/operator/131-kameo-control-plane-lifecycle-work.md`
and an implementation-ready migration plan for moving Persona
components to the Kameo lifecycle/control-plane fork.

## 0. Verdict

The Kameo fork is now ready for Persona component migration, with
one small Kameo consistency fix recommended before or during the
first operator pass.

Operator 131 has changed since the previous audit. The current
reported stack is:

```text
ddab7733 actor: publish terminal lifecycle outcomes
565ff25e actor: split lifecycle control mailbox
04f6e2ab actor: cover lifecycle control edge cases
```

Remote state:

```text
origin/main == origin/kameo-push-only-lifecycle == 04f6e2ab
```

The previous major blockers are now covered:

- physical control lane exists;
- generation guard exists;
- stop semantics are documented as non-draining;
- blocking receive has a control-lane wake test;
- queued `ask` abandonment has a test;
- supervised `spawn_in_thread` exclusive-resource restart has a test.

I verified the focused lifecycle suite locally against `04f6e2ab`:

```sh
CARGO_BUILD_JOBS=1 RUST_TEST_THREADS=1 \
  cargo test -p kameo --all-features --test lifecycle_phases -- --nocapture
```

Result:

```text
11 passed; 0 failed
```

## 1. Fresh Audit Findings

### 1.1 Closed: control-plane split

Kameo now has two physical lanes:

```rust
Bounded {
    messages: mpsc::Sender<QueuedMessage<A>>,
    control: mpsc::UnboundedSender<Signal<A>>,
}
```

The ordinary message lane stays bounded when users ask for a
bounded mailbox. Lifecycle/control traffic uses the unbounded
control lane, so stop/link/restart traffic cannot be blocked by
ordinary message capacity.

### 1.2 Closed: pending bounded send crossing shutdown

Ordinary messages are generation-tagged. Senders capture the
generation, wait for capacity, then re-check before committing.
Receivers also drop stale queued messages if their generation no
longer matches.

This is the correct primitive. It prevents ordinary messages from
leaking into a replacement actor after restart.

### 1.3 Closed: blocking receive edge

The previous split-lane concern was that `blocking_recv()` might
check control once and then block on ordinary messages. Current
Kameo implements blocking receive by running the async `recv()` on
a current-thread runtime:

```rust
pub fn blocking_recv(&mut self) -> Option<Signal<A>> {
    let runtime = tokio::runtime::Builder::new_current_thread()
        .build()
        .expect("current-thread runtime can drive blocking mailbox receive");
    runtime.block_on(self.recv())
}
```

The test `blocking_recv_wakes_for_late_control_signal` covers the
late-control-signal case.

### 1.4 Closed: queued `ask` stop semantics

The current test `queued_ask_dropped_by_stop_reports_actor_stopped`
proves that a queued ask discarded by stop resolves as
`SendError::ActorStopped` and does not run the queued handler.

That is the right public semantic:

- enqueue succeeded;
- stop overtook the queued ordinary message;
- caller did not get a handler reply because the actor stopped.

### 1.5 Closed: supervised `spawn_in_thread`

The test `supervised_spawn_in_thread_releases_resource_before_restart`
now combines the previously missing three facts:

- child is supervised;
- child uses `spawn_in_thread`;
- child owns an exclusive resource that the replacement reacquires.

This is the StoreKernel-critical witness. It means Kameo no longer
blocks revisiting `persona-mind`'s Template-2 deferral.

### 1.6 Still open: weak shutdown-result helpers are not gated

Operator 131 says `get_shutdown_result()` and
`with_shutdown_result()` are gated behind terminal lifecycle
publication. That is true for `ActorRef`, but not for
`WeakActorRef`.

Strong `ActorRef`:

```rust
pub fn get_shutdown_result(&self) -> Option<...> {
    if !self.is_terminated() {
        return None;
    }
    ...
}
```

Weak `WeakActorRef`:

```rust
pub fn get_shutdown_result(&self) -> Option<...> {
    match self.shutdown_result.get()? {
        ...
    }
}
```

Same issue for `with_shutdown_result()`.

This is not a Persona migration blocker if components avoid the
compatibility helpers, but it is a small correctness inconsistency
inside Kameo. Operator should fix it in the same wave:

```rust
if !self.is_terminated() {
    return None;
}
```

Add a weak-reference test mirroring the strong-reference behavior.

### 1.7 Still open: `is_alive()` is only documented, not deprecated

`ActorRef::is_alive()` now means "accepting ordinary messages."
The docs say to prefer `is_accepting_messages()` or
`is_terminated()`, but there is no deprecation attribute.

This is acceptable for migration, but workspace code should not use
Kameo `is_alive()` for actor lifecycle decisions.

### 1.8 Still open but non-blocking: future lifecycle surfaces

The following remain intentionally out of scope:

- internal lifecycle facts for test introspection;
- `run_to_state_ejection` enum-shaped API;
- `Killed` versus future `Brutal` shutdown split;
- registry `mark_unfindable` / `release_slot`;
- remote `PeerDisconnected` truthfulness.

Do not block the Persona migration on these.

## 2. Migration Scope

Current active repos still depend on crates.io `kameo = "0.20"`:

| Repo | Current features |
|---|---|
| `persona` | `default-features = false` |
| `persona-mind` | `default-features = false`, `macros`, `tracing` |
| `persona-router` | `default-features = false`, `macros`, `tracing` |
| `persona-message` | `default-features = false`, `macros` |
| `persona-introspect` | `default-features = false`, `macros` |
| `persona-system` | `default-features = false`, `macros`, `tracing` |
| `persona-harness` | `default-features = false`, `macros`, `tracing` |
| `persona-terminal` | `default-features = false`, `tracing` |
| `terminal-cell` | default features, `macros` |

No active implementation repo currently overrides `on_link_died`.
No active implementation repo currently uses Kameo
`ActorRef::is_alive()`; the `is_alive` hits I found are process
helper functions.

There are many `wait_for_shutdown()` call sites. Some in `persona`
already explicitly bind `_shutdown_completion`; other repos still
discard the returned outcome as a bare statement.

## 3. Dependency Pin Shape

Do not use raw commit revisions as the steady-state dependency
interface. Use a named reference.

The current implementation-ready named ref is the fork branch:

```toml
git = "https://github.com/LiGoldragon/kameo"
branch = "main"
```

If operators want a less moving target before the component sweep,
mint a stable named branch or tag first, then use that name across
all component repos. Either shape satisfies the workspace rule:
named references, not raw revs.

Concrete dependency replacements:

```toml
# persona
kameo = { git = "https://github.com/LiGoldragon/kameo", branch = "main", default-features = false }

# persona-mind / persona-router / persona-system / persona-harness
kameo = { git = "https://github.com/LiGoldragon/kameo", branch = "main", default-features = false, features = ["macros", "tracing"] }

# persona-message / persona-introspect
kameo = { git = "https://github.com/LiGoldragon/kameo", branch = "main", default-features = false, features = ["macros"] }

# persona-terminal
kameo = { git = "https://github.com/LiGoldragon/kameo", branch = "main", default-features = false, features = ["tracing"] }

# terminal-cell
kameo = { git = "https://github.com/LiGoldragon/kameo", branch = "main", features = ["macros"] }
```

Preserve each repo's existing feature set unless a local compile
error proves the feature set was already wrong.

## 4. Code Migration Rules

### 4.1 Treat `ActorTerminalOutcome` as the lifecycle contract

Every meaningful shutdown should capture the outcome:

```rust
let outcome = actor.wait_for_shutdown().await;
```

Use:

```rust
outcome.state
outcome.reason
```

Do not reason from legacy `ActorStopReason` unless you are handling
old compatibility detail.

### 4.2 Stop helpers should either assert or return outcome

For component roots and resource owners, prefer:

```rust
pub async fn stop(reference: ActorRef<Self>) -> Result<ActorTerminalOutcome> {
    reference.stop_gracefully().await.map_err(...)?;
    Ok(reference.wait_for_shutdown().await)
}
```

If a public/component API must stay `Result<()>`, assert locally:

```rust
let outcome = reference.wait_for_shutdown().await;
ensure!(outcome.state == ActorStateAbsence::Dropped);
ensure!(outcome.reason.is_normal());
Ok(())
```

For tests or leaf cleanup where the outcome is intentionally
irrelevant:

```rust
let _shutdown_completion = reference.wait_for_shutdown().await;
```

No bare `reference.wait_for_shutdown().await;` in migrated code.

### 4.3 Avoid `is_alive()`

Workspace actor code should not use Kameo `is_alive()`.

Use:

- `is_accepting_messages()` when asking whether ordinary messages
  can still be sent;
- `is_terminated()` when asking whether terminal lifecycle outcome
  has been published;
- `wait_for_shutdown()` when correctness depends on completion.

### 4.4 If `on_link_died` appears, use the new signature

New Kameo shape:

```rust
async fn on_link_died(
    &mut self,
    actor_reference: WeakActorRef<Self>,
    id: ActorId,
    outcome: ActorTerminalOutcome,
    reason: ActorStopReason,
) -> Result<ControlFlow<ActorStopReason>, Self::Error>
```

Lifecycle decisions should use `outcome`. The legacy `reason`
exists for detail payloads.

### 4.5 Do not use shutdown-result helpers for correctness

Avoid:

- `get_shutdown_result()`;
- `with_shutdown_result()`;
- `wait_for_shutdown_result()`;

These are compatibility surfaces. Use `wait_for_shutdown()` and
`ActorTerminalOutcome`.

If a repo already uses a shutdown-result helper, migrate it before
or during the Kameo pin change.

## 5. Component-Specific Instructions

### 5.1 `persona`

Current code already uses `_shutdown_completion` in several tests
and helpers. After the pin:

- import/use `ActorTerminalOutcome` where stop helpers should
  return it;
- keep manager process supervision separate from actor lifecycle;
- add or strengthen a ManagerStore release test that verifies the
  store can be reopened after terminal outcome.

Do not confuse Kameo actor terminal outcome with daemon process
exit in `persona-daemon`.

### 5.2 `persona-mind`

Kameo no longer blocks the StoreKernel Template-2 destination.

Operator sequence:

1. Pin Kameo.
2. Add a `StoreKernel` release witness against the real
   redb/sema-engine store path.
3. Only after that witness passes, revisit the deferral comment in
   `src/actors/store/mod.rs`.
4. If moving `StoreKernel` to supervised `spawn_in_thread`, prove
   replacement can reopen the same store path on first attempt.

Do not remove the deferral comment merely because Kameo has its own
TcpListener witness. Persona needs a store-specific witness.

### 5.3 `persona-router`

`RouterRuntime::stop_children()` currently stops multiple children
and discards outcomes.

Migration target:

- capture each child `ActorTerminalOutcome`;
- build a small child-shutdown summary, even if only local for now;
- assert normal dropped outcomes for clean shutdown tests.

This makes router shutdown inspectable and prevents silent child
cleanup failures from being flattened into "router stopped."

### 5.4 `persona-introspect`

Same shape as router. `IntrospectionRoot::stop_children()` should
capture outcomes for:

- target directory;
- query planner;
- manager client;
- router client;
- terminal client;
- store;
- projection.

This is especially important because introspect is a diagnostic
component. It should not discard lifecycle diagnostics from its own
actors.

### 5.5 `persona-harness`

Pin Kameo and capture outcomes for:

- harness root stop helper;
- transcript subscription manager;
- streaming reply handlers.

Add or strengthen tests proving subscription handlers terminate
after manager shutdown and do not retain stale subscribers.

### 5.6 `persona-terminal`

Pin Kameo and update `TerminalSupervisor::stop`.

Add/strengthen resource witnesses for:

- terminal supervisor store/session state after shutdown;
- terminal control socket behavior;
- terminal-cell session cleanup at the boundary where
  persona-terminal talks to terminal-cell.

Do not let Kameo migration touch terminal input pass-through
performance without a latency witness.

### 5.7 `terminal-cell`

Pin Kameo and keep the actor lifecycle change separate from data
plane behavior.

Add/strengthen tests for:

- child process killed/reaped after terminal outcome;
- control socket/session socket cleanup;
- no stale input relay after shutdown.

### 5.8 `persona-message`

Standard pin and compile migration. No special Kameo lifecycle
pattern found beyond root actor stop handling.

### 5.9 `persona-system`

System is architecturally paused, but it still uses Kameo. Pin it
for consistency and capture shutdown outcomes in:

- `SystemSupervisor::stop`;
- `NiriFocusTracker::stop`.

No new system-feature work should be coupled to this migration.

## 6. Operator Implementation Order

### Phase 0 — small Kameo cleanup

Before or during migration:

1. Gate `WeakActorRef::get_shutdown_result()` behind
   `is_terminated()`.
2. Gate `WeakActorRef::with_shutdown_result()` behind
   `is_terminated()`.
3. Add the weak-reference visibility test.

Optional hygiene:

- deprecate `is_alive()`, or at least update recipient wrapper docs
  away from "currently alive."

### Phase 1 — dependency pins

Update the nine repos listed in §2 to the named Kameo fork
reference.

After each repo pin:

```sh
cargo check --all-targets
cargo test
```

Use the repo's Nix checks/apps where they exist. Cargo is the inner
Rust witness; Nix remains the workspace reproducibility boundary.

### Phase 2 — mechanical API sweep

Run:

```sh
rg "wait_for_shutdown\\(\\)\\.await;" /git/github.com/LiGoldragon/{persona,persona-mind,persona-router,persona-message,persona-introspect,persona-system,persona-harness,persona-terminal,terminal-cell} -g '*.rs'
rg "fn on_link_died" /git/github.com/LiGoldragon/{persona,persona-mind,persona-router,persona-message,persona-introspect,persona-system,persona-harness,persona-terminal,terminal-cell} -g '*.rs'
rg "is_alive\\(" /git/github.com/LiGoldragon/{persona,persona-mind,persona-router,persona-message,persona-introspect,persona-system,persona-harness,persona-terminal,terminal-cell} -g '*.rs'
rg "get_shutdown_result|with_shutdown_result|wait_for_shutdown_result" /git/github.com/LiGoldragon/{persona,persona-mind,persona-router,persona-message,persona-introspect,persona-system,persona-harness,persona-terminal,terminal-cell} -g '*.rs'
```

Expected:

- no Kameo `is_alive()` use;
- no shutdown-result helper use in Persona code;
- no bare `wait_for_shutdown().await;` except where explicitly
  bound to `_shutdown_completion`;
- no old-signature `on_link_died`.

### Phase 3 — semantic outcome sweep

For component roots and supervisors, stop discarding outcomes.

Minimum acceptable:

```rust
let _shutdown_completion = child.wait_for_shutdown().await;
```

Preferred:

```rust
let outcome = child.wait_for_shutdown().await;
self.child_shutdowns.push(... outcome ...);
```

Best for resource owners:

```rust
assert_eq!(outcome.state, ActorStateAbsence::Dropped);
assert!(outcome.reason.is_normal());
```

### Phase 4 — resource witnesses

Add real component-specific witnesses:

| Repo | Witness |
|---|---|
| `persona` | ManagerStore can reopen after terminal outcome |
| `persona-mind` | StoreKernel/sema-engine store can reopen after terminal outcome |
| `persona-router` | child actor shutdown outcomes are collected and clean |
| `persona-introspect` | child actor shutdown outcomes are collected and clean |
| `persona-harness` | subscription handlers terminate and no stale subscriber remains |
| `persona-terminal` | terminal supervisor/session socket state is clean after shutdown |
| `terminal-cell` | child process and sockets are gone after terminal outcome |

These must test production code, not test-only logic.

### Phase 5 — full engine witness

After all pins and local tests:

- run the persona dev-stack smoke;
- run the sandbox/dev-stack witness if available;
- run any terminal-cell live fixture that exercises stop/restart of
  a session;
- verify no daemon process lifecycle code started treating Kameo
  actor outcomes as process outcomes.

## 7. Migration Gates

Green before declaring migration done:

- Kameo lifecycle test file passes: 11/11.
- Every listed repo builds against the Kameo fork.
- No raw Kameo `rev = ...` dependency pins.
- No Kameo `is_alive()` lifecycle checks.
- No old `on_link_died` signatures.
- Component root stop paths capture or intentionally discard
  terminal outcomes.
- Resource-owning actors have at least one real release witness.
- Persona dev-stack still runs.

## 8. Final Recommendation

Proceed with the component migration.

The old major blockers are closed. The only Kameo fix I would carry
into the migration wave is the weak-reference shutdown-result gate,
because it is small and makes operator 131's claim literally true.

Do not wait for internal lifecycle facts, ejection API cleanup,
brutal shutdown, or remote-disconnect truthfulness. They are future
framework work, not blockers for Persona's current local-engine
actor topology.
