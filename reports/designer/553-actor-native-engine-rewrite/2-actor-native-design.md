# 2 — actor-native design (the to-be)

designer, 2026-06-07. The authoritative design for rewriting the schema-derived
triad daemon stack as kameo 0.20 actors (Spirit `zk6y`). Builds on `1-current-stack-map.md`
and the grounding workflow `w63hfqahs`. The synthesis/overview of this session.

## The decided fork: sync engine logic, async actor shell

Two grounding readers independently flagged this as the one fork to raise to the
psyche; it is **decided** (and was explained to the psyche in chat before this
report): the engine traits' computation stays **sync-pure**; only the actor shell
is async. Concretely:

- `SignalEngine::triage_inner`/`reply_inner` — stay sync `&self` transforms.
- `NexusEngine::decide(&mut self, Work) -> Action` — stays sync, the per-step
  decision. Pure, testable with a plain `#[test] fn`, no tokio.
- `SemaEngine::apply_inner(&mut self)`/`observe_inner(&self)` — stay sync.
- The **driver loop** (today `Runner::drive`, today a default method *on*
  `NexusEngine`) moves **out** of the trait into the Nexus **actor's** async
  `handle`. The loop interprets each `decide` result and performs effects by
  `ask`-ing sibling actors.

Why this holds by construction: the `NexusWork → NexusAction` mechanism (Spirit
`1486`) already expresses effects **as data** — `decide` returns
`CommandSemaWrite`/`CommandSemaRead`/`CommandEffect`/`ReplyToSignal`/`Continue`
values, it never performs them. So there is nothing in the logic to `.await`; the
async driver performs the actions. The existing substrate was already the right
shape for sync-logic-under-async-shell. This preserves the pure-transform
testability the architectural-truth-tests rely on, and keeps redb's synchronous
API matched to synchronous logic.

## Target topology (per daemon)

A supervised actor tree, replacing `GeneratedDaemonRuntime` + the blocking
listener spine. Modeled on `chroma`'s `ChromaRoot` and `harness`:

- **`RuntimeRoot` actor** (the supervised root; replaces
  `Single`/`MultiListenerDaemon`). Owns child `ActorRef`s as state. `on_start`
  binds sockets and spawns children under supervision; `on_stop` releases them.
  The daemon bin stays a one-liner — `run_to_exit_code()` now establishes a
  multi-thread tokio runtime and blocks on the root's `wait_for_shutdown`.
- **`ListenerActor` per authority tier** (Working / Meta, or lojix's
  Ordinary / Owner). The **mailbox replaces the blocking accept loop** — async
  `tokio::net::UnixListener::accept().await`, deleting the `set_nonblocking` +
  `WouldBlock` + `thread::sleep(poll_interval)` busy-poll entirely. Per accepted
  stream it spawns/dispatches a request driver; it does NOT handle inline.
- **Per-request Nexus driver** (NOT one god-actor). Each connection drives its own
  continuation loop with its own in-flight cursor (lojix's
  `active_deploy`/`active_operation`), mirroring `SchemaRuntime::with_store`.
  Concurrency bound = a permit cap (replacing `BoundedWorkers` cap 64). The driver
  runs the `decide`→act loop, `ask`-ing the SEMA actor for sema steps and the
  effect plane for effects.
- **`SemaActor` — single-writer, owns the durable store.** The `Mutex<…>` over
  state evaporates: one actor owns it, the mailbox serializes writes. `apply`
  (`&mut self`) is an ask serialized by the mailbox.
- **Blocking-plane effect actor(s).** Long effects (lojix's nix build) run OFF any
  mailbox so the SEMA and listener actors keep serving.
- **`SubscriptionActor`** — owns the registry + per-subscriber writers + publisher
  (replaces `EmittedSubscriptions`'s `Mutex<SubscriptionState>`); `Register` /
  `Publish` messages.

The naming map: `MultiListenerDaemon` → `RuntimeRoot` + `ListenerActor`s;
`BoundedWorkers` → permit-capped per-request drivers (mailbox backpressure);
`Runner::drive` → the Nexus driver's `handle` (in-handler loop; `Continue` is
in-handler recursion, **never** `self.ask()` — that deadlocks); `Mutex<Nexus>`/
`Mutex<Store>` → `SemaActor`; `Mutex<SubscriptionState>` → `SubscriptionActor`.

## The genuine sub-forks — decisions taken (reversible; psyche may redirect)

1. **SEMA parallel reads → redb MVCC, not a serialized mailbox.** A single SEMA
   actor whose mailbox processes every message in order would serialize reads
   behind writes, losing the `&self` parallel-read property. Decision: the
   `SemaActor` owns the redb `Database`; **writes** (`apply`) go through its
   mailbox (single-writer); **reads** (`observe`) are served via concurrent redb
   **read-transactions / snapshots** that do not block the writer — redb supports
   MVCC natively. This preserves the `&mut self`/`&self` contract physically. (The
   simpler "serialize everything through one mailbox" is correct but regresses read
   concurrency; rejected.)
2. **Per-request Nexus → spawn-per-request, permit-capped.** Mirrors
   `SchemaRuntime::with_store` + cap 64 most directly and keeps per-request cursor
   isolation natural. (A fixed pool is the alternative — more resource-stable, less
   faithful to today's model.)
3. **lojix nix build → Template 3 (`tokio::process`), cancellation per-operation
   and schema-visible.** `nix`/`ssh` have clean async process APIs; no short
   timeout (a legitimate build runs minutes). The cancellation policy is NOT a
   blanket `kill_on_drop` — it is declared per operation in schema: a *speculative*
   query/build couples to the request (`kill_on_drop(true)`); a *durable deploy*
   survives client disconnect (a job actor owns the process and persists job state,
   reporting status later). Tokio child processes outlive a dropped handle by
   default, so the durable case is the natural one; the speculative case opts into
   kill-on-drop. Stream/bound the build log rather than buffering it all as
   `.output()` does. (Q1 below — the durable-deploy default is the psyche's to
   confirm.)
4. **Frame transport → `tokio::net::UnixStream` (async codec).** Cleaner than
   wrapping every blocking `read_exact`/`write_all` in `spawn_blocking`, and the
   listener needs async accept anyway. SO_PEERCRED (`ConnectionContext::from_stream`,
   security-load-bearing owner-vs-non-owner) read via `AsRawFd` on the tokio
   stream, before any IO.
5. **`triad-runtime` gains kameo-native primitives; stays the shared library.**
   An async listener actor + a continuation-driver helper live in `triad-runtime`;
   the emitter targets them. (The alternative — daemons drop the triad-runtime
   daemon module entirely — loses the shared-runner value.) `daemon.rs`'s blocking
   spine and `workers.rs`'s `BoundedWorkers` become dead and are deleted.
6. **`SemaActor` supervision → `.spawn()` + Template-1 `spawn_blocking`, NOT
   `spawn_in_thread`.** Forced by a kameo 0.20 hazard (below): the redb-backed
   single-writer is exactly the supervised-state-bearing actor that
   `spawn_in_thread` races on shutdown.
7. **Meta tier → a generated typed tier, not a raw stream hook.** Today the meta
   listener calls `ComponentDaemon::handle_meta_stream(engine, stream)` — a raw
   stream each component reimplements transport for. The emitter instead generates
   the meta tier with the same decode→handle→encode shape as the working tier:
   components receive *decoded* meta input and return typed meta output; raw-stream
   hooks become a rare, explicitly-named escape hatch, not the default.
8. **Effect taxonomy — three shapes, not one.** Short blocking work (a redb point
   txn) → `spawn_blocking`; long external commands (nix/cloud API) → a
   `tokio::process`/async effect actor (`spawn_blocking` started tasks can't be
   aborted, so they are wrong here); indefinite watchers (repository-ledger's spool
   loop) → an actor with an async interval/watch source. SEMA reads are sync redb
   work: a read snapshot is minted from the store actor and served on a blocking
   boundary (dedicated read actor/pool), with long scans bounded separately from
   point lookups. The generic subscription actor and the read-snapshot pattern live
   in `triad-runtime`/`sema-engine`, emitted once — not duplicated per component.

## Hazards baked into the design (from the grounding's risk lists)

- **`spawn_in_thread` on a supervised state-bearing actor is forbidden in kameo
  0.20** — `wait_for_shutdown` returns before `Self` (the redb `Database`/socket)
  drops, racing the next open (`Io(UnexpectedEof)`/bind hang). Documented at
  `persona-mind/src/actors/store/mod.rs:295-307`. → SemaActor uses `.spawn()` and
  runs redb calls via `spawn_blocking` inside the handler.
- **`tell` to a fallible handler crashes the actor** (`PanicReason::OnMessage`). →
  use `ask` for every fallible plane op, never `tell`. **Self-ask deadlocks** →
  `Continue` is in-handler recursion.
- **Restart reconstructs `Self` from `Args`, losing in-memory state.** →
  transient-state actors (per-request Nexus, Signal) default
  `RestartPolicy::Never`; only the sema-backed `SemaActor` is safe on `Permanent`.
- **Multi-thread test hang** on daemon-restart witnesses (drop root, reopen same
  on-disk state) under `flavor = multi_thread` + cargo's parallel runner. →
  restart density tests stay on single-thread `#[tokio::test]`.
- **Blocking IO in an async handler stalls the tokio worker.** → uniform async
  sockets (decision 4); any unavoidable sync work goes through `spawn_blocking`.
- **Continuation budget** (default 32, `budget_exhausted_reply`) must travel with
  the loop and survive the async conversion; the common short request must not
  regress on per-hop mailbox latency.
- **Store-poison error path changes**: `Store::lock` → `Error::StorePoisoned`
  becomes actor-death/restart; the ~10 call sites need the kameo-equivalent
  contract, not a silent change.
- **Don't over-build the deferred machinery** (`1483`/`1487`/`zk6y`): bounded
  mailboxes + the two lifecycle hooks + simple supervision land now; backpressure,
  scheduling/prioritization, and the runtime-control trait surface stay deferred.
  Over-building them is as much a violation as not adopting kameo.

## The leverage point and the sequence

The **emitter is the load-bearing change.** Fix `schema-rust-next/daemon_emit.rs`
(+ the engine-trait emission in `lib.rs`) and `triad-runtime`'s primitives once,
regenerate, and `message`/`spirit`/`cloud`-emitted become actors. Sequence:

1. **Toolchain + deps.** Rust 1.88, fenix lockstep; add `kameo = "0.20"` + tokio
   to `triad-runtime` and the daemon crates.
2. **`triad-runtime` kameo primitives.** Async `ListenerActor`, the continuation
   driver helper, the permit cap; delete `daemon.rs` blocking spine + `workers.rs`.
3. **Emitter rewrite.** `daemon_emit.rs` emits the `RuntimeRoot`/`ListenerActor`/
   per-request-driver/`SemaActor`/`SubscriptionActor` tree; `lib.rs` keeps the
   engine `_inner` methods sync and emits the actor wrappers. Rewrite the golden
   tests (`tests/daemon_emission.rs`, `runner_generated.rs`) to the actor shape.
4. **Regenerate pilots in risk order: `message` → `spirit` → `cloud`.** `message`
   first proves actor transport with the smallest state surface (no store); `spirit`
   second proves durable SEMA; `cloud` third proves multi-listener + meta. Start a
   pilot, force the tests green, then move on — NOT all components at once. (lojix
   first is tempting but mixes runtime migration with nix-effect semantics; defer.)
   Each pilot converts its hand-written `impl ComponentDaemon` to the new lifecycle
   (`build_runtime` → `on_start`).
5. **Hand-migrate holdouts.** lojix (the nix blocking-plane is component-specific;
   it converges onto the emitted listener/SEMA tree but keeps its effect actor),
   cloud, repository-ledger (spool poll → timer-driven `IngestSpool` message,
   ending the spool-vs-request lock contention).
6. **Ship actor-density + behavioral tests** (next section). The concrete operator
   test suite (source-shape assertions, concurrency witnesses, effect/cancellation
   tests) and the M1-M9 migration invariants are enumerated in the system-operator
   audit `reports/system-operator/200-…` — adopted in full; not duplicated here.
7. **Update per-repo `INTENT.md`/`ARCHITECTURE.md` on the same branch** — lojix's
   stale "Each daemon actor is a Kameo actor" becomes true again;
   `schema-rust-next/ARCHITECTURE.md:264-271` and `triad-runtime` docs drop the
   sync-substrate framing.

## Actor-density tests to ship (architectural-truth-tests §600-635)

The rewrite must be falsifiable, so the next emitter pass can't silently drop
kameo: **no-zst-actor** (`size_of::<Actor>() > 0`, the `kameo-testing/tests/topology.rs`
shape), **topology-manifest** + **actor-count**, **trace-pattern** (reuse the
existing testing-trace socket as the Layer-2 witness that Signal/Nexus/SEMA
engine methods actually ran), **forbidden-edge** (a query cannot reach the SEMA
writer's write path), **no-blocking-handler** (a sibling stays responsive while
one plane waits on a long effect). These encode `zk6y` as tests, not prose.

## What stays deferred (scope fence)

Per `1483`/`1487`/`zk6y`: backpressure handling, the runtime-control trait
surface, and actor scheduling/prioritization are NOT built here. The lifecycle
hooks (`on_start`/`on_stop`) map onto kameo's, supervision is `OneForOne`
defaults, mailboxes are bounded-at-a-fixed-cap. The deferral records are not
retired — only the sync-substrate interpretation layered on them is corrected.

## Lane handoff

This is a large multi-repo integration (the ~15 crates depending on
`triad-runtime`, plus a toolchain bump) — operator-owned on main. Designer
deliverable: this design + the `skills/component-triad.md` correction (landed on
primary/main here) + a worktree **proof of the core** (the `triad-runtime`
primitives + emitter actor emission + one regenerated pilot, compiling and
serving). Operator integrates across the stack and migrates the remaining
daemons from this design.
