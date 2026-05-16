# 139 — Kameo 0.20 supervised `spawn_in_thread` shutdown-ordering bug

Date: 2026-05-16
Role: operator-assistant
Scope: document the Kameo 0.20 supervised-actor shutdown-ordering bug
that the persona-mind StoreKernel Template-2 migration surfaced, name
the workaround currently in code, and record the upstream fix paths
that resolve it.

## 0. Summary

Kameo 0.20's supervised `spawn_in_thread` releases the parent's
`wait_for_shutdown()` **before** the actor's `Self` value is dropped.
When `Self` owns a durable resource — a redb `Database`, an open
file lock, a bound socket — the resource outlives the "child closed"
signal. The next restart races the still-held resource. Tests fail
with `UnexpectedEof`, hang on the second `bind()`, or return
`redb::DatabaseError::DatabaseAlreadyOpen`.

The persona-mind `StoreKernel` is the worked example. Its destination
shape is Template 2 from `skills/kameo.md` (dedicated OS thread, off
the shared Tokio worker pool), because every message touches sync
redb + sema-engine transactions. The bug forced reverting to the
standard `.spawn()` path and accepting the mailbox-blocking cost of
inline redb transactions until the framework lands a post-drop
shutdown hook.

## 1. Failure mode

Reproduced inside `persona-mind`'s supervised `StoreKernel`. The
parent (`StoreSupervisor` or `MindRoot`) spawns the kernel via
`StoreKernel::supervise(&self, args).spawn_in_thread()`. Restart-
discipline tests then:

1. Open the redb file through `Self::on_start`, which calls
   `redb::Database::create(...)` and stores the handle on `Self`.
2. Kill the supervised kernel (graceful stop or panic).
3. `wait_for_shutdown()` returns.
4. The parent's restart logic constructs a fresh kernel and calls
   `redb::Database::create(...)` on the **same path**.
5. `redb::Database::create` returns
   `DatabaseError::DatabaseAlreadyOpen` — the prior thread is still
   holding the lock.

Symptom variants observed:

- `redb::DatabaseError::DatabaseAlreadyOpen` on second open.
- `UnexpectedEof` from a peer probing a socket that the prior
  kernel had bound and that has not yet been released.
- A hang on the second `UnixListener::bind` when the kernel binds
  a supervised socket of its own.

## 2. Root cause — Kameo 0.20 shutdown ordering

Kameo 0.20's supervised `spawn_in_thread` path drives shutdown like
this:

```
parent observes child stop
  → parent's `wait_for_shutdown()` future resolves
  → (caller proceeds, including any restart logic)
  ...
  → child thread eventually unwinds, drops `Self`, releases resources
```

The window between (3) and (5) above is the bug. The "child closed"
signal arrives at the parent before `Self::drop()` runs in the
child's dedicated OS thread. A parent that immediately restarts the
child observes the prior `Self`'s resources still held.

The standard `.spawn()` path on the shared Tokio runtime does **not**
have this ordering gap. There, the actor's state is dropped within
the same Tokio task that the parent waits on; by the time
`wait_for_shutdown` resolves, `Self::drop()` has run.

The bug surfaces only under **supervision**. An unsupervised
`spawn_in_thread` actor — a top-level dedicated-thread actor whose
parent does not track a restart contract — does not depend on this
ordering, because nothing observes the wait-for-shutdown signal. The
`chroma::StateStore` pattern (`src/state.rs:61`) uses unsupervised
`spawn_in_thread` and is unaffected.

## 3. Current workaround (in code)

Persona-mind's `StoreKernel` reverts to the standard `.spawn()` path:

```rust
// src/actors/store/mod.rs:295-307
let kernel = StoreKernel::supervise(
    &actor_reference,
    kernel::Arguments {
        store: arguments.store.clone(),
        subscription: arguments.subscription.clone(),
    },
)
.spawn();
```

The cost: every handler runs on a Tokio worker thread, and sync redb
transactions inside the handler stall that thread for the duration
of the transaction. Sibling actors scheduled on the same worker
share that stall. Template 1 (`spawn_blocking` + `DelegatedReply`)
remains available for the kernel's longest blocking calls.

The code carries an inline comment block (`src/actors/store/mod.rs:
286-303`) describing the failure mode and the deferral. The
component's `ARCHITECTURE.md` §4 names the kernel's current vs
destination shape and the deferral explicitly.

## 4. Upstream fix paths

Two shapes resolve the bug at the framework boundary:

- **Post-drop shutdown hook in Kameo.** Add a hook that fires after
  the actor's `Self` value is dropped, on the dedicated-thread path,
  and gate `wait_for_shutdown` on that hook. Equivalent: rename the
  existing `pre_notify_links` semantics so they fire after `Self::
  drop()` for the `spawn_in_thread` path.
- **Actor-owned close-then-confirm protocol.** Add a typed message
  the parent sends before believing the child closed; the child
  releases its `Self`-owned resources, then replies; only after the
  reply does the parent treat the child as gone. This shifts the
  contract from "wait for the framework's shutdown signal" to "wait
  for the typed acknowledgement my actor promises."

Either resolves the bug for state-bearing supervised actors. The
first is simpler for framework users; the second is more explicit at
the actor's contract and survives framework version churn.

## 5. Workspace impact

Components currently using `.spawn()` (the safe path) for
state-bearing supervised actors that would otherwise want Template 2:

- `persona-mind::StoreKernel` — owns the mind redb `Database`;
  reverted to `.spawn()` per /138.
- Other state-bearing supervised actors in the workspace should
  audit their spawn path before migrating to `spawn_in_thread`.

Components safely using `spawn_in_thread` (unsupervised pattern):

- `chroma::StateStore` (`src/state.rs:61`) — top-level
  dedicated-thread actor, no parent supervision contract.

Adjacent gotcha: parallel `*_survives_process_restart` tests under
`#[tokio::test(flavor = "multi_thread")]` hang against each other
on shared redb resources even on the `.spawn()` path. Single-thread
(`current_thread`) flavor passes. Independent of the `spawn_in_thread`
bug; tracked in `skills/kameo.md` §"Anti-patterns and gotchas".

## 6. Discipline update landed

`/home/li/primary/skills/kameo.md` now carries the warning in two
places:

- §"Blocking-plane templates" → Template 2 → new sub-§
  "Supervised-actor warning — Kameo 0.20 shutdown ordering bug"
  documents the failure mode, the workaround, the upstream fix
  paths, and the unsupervised carve-out (chroma's pattern stays
  valid).
- §"Anti-patterns and gotchas" carries a one-line entry pointing
  at the Template 2 section, plus a separate entry for the
  `flavor = "multi_thread"` parallel-restart-test hang.

`/home/li/primary/skills/actor-systems.md` does not need a change —
the rule it carries (Blocking is a design bug → Template selection
in `kameo.md`) is unchanged; the warning lives downstream in the
tool reference where the bug is operational.

## 7. See also

- `/home/li/primary/skills/kameo.md` §"Blocking-plane templates"
  → Template 2 → "Supervised-actor warning" (the canonical
  discipline home).
- `/home/li/primary/skills/actor-systems.md` §"Blocking is a
  design bug" (the architectural rule the templates serve).
- `/home/li/primary/reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
  §"P2 StoreKernel Template 2 deferred" — the phase-1 mind
  continuation report that first documented the bug.
- `/git/github.com/LiGoldragon/persona-mind/src/actors/store/mod.rs:286-307`
  — the inline deferral comment in code.
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` §4 —
  the StoreKernel's current vs destination shape.
- `https://github.com/tqwewe/kameo` — upstream Kameo. An issue or
  PR upstream tracking the post-drop shutdown hook would resolve
  the workspace deferral.
