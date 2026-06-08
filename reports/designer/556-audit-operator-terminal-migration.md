# 556 — audit: operator terminal emitted-daemon migration (report 338)

designer, 2026-06-08. Deep adversarial audit of the operator's terminal
actor-migration slice (`reports/operator/338-…`): `signal-terminal`
`e313a55f`/`46c92b58` + `terminal` `74ae7677`. Method: a six-dimension
fan-out (45 agents — design-553 conformance, kameo hazards, rust/triad
discipline, emitter shape, scope/honesty, and a build-truth runner that
actually executed the verification commands), each finding adversarially
re-verified against the real code, plus my own independent reads of
`triad-runtime/src/actor_runtime.rs`, `terminal/src/{daemon,schema/daemon}.rs`,
and `supervisor.rs`. Baselines: design `553`, the discipline skills, and Spirit
`zk6y`/`r310`/`1g8y`/`59dr`/`k6w1`.

## Verdict

**The slice works and is honestly built; it is not "actors all the way
down," and it carries real lifecycle gaps.** Every verification command in
report 338 genuinely passes (below), the busy-poll spine is gone from the live
path, the shell is emitted by the *shared* emitter, the triad single-binary /
no-flags / no-NOTA overrides are honored and witnessed, and the deferral fence
(`59dr`) held. Terminal also has **zero `signal-executor` references**, so it is
not a `ng1x` "wrap-don't-remove" offender — this migration is the process-shell
axis, orthogonal to the executor-removal gate in `555`. The gaps are
architecture and lifecycle: the runtime is actor-native only at the admission
gate and the state actor, the supervised-root lifecycle is absent, and a
handful of correctness hazards ride along.

## Build-truth — report 338's Verification section is TRUE

The build-runner executed every command in clean working copies, forcing fresh
recompiles (not cache hits):

- `signal-terminal` @ `46c92b58`: `fmt` clean; `clippy -D warnings` clean
  (verified by forced recompile); `cargo test` 4 binaries ok.
- `terminal` @ `74ae7677`: `fmt` clean; `TERMINAL_UPDATE_SCHEMA_ARTIFACTS=1
  cargo test` ran the emitter and passed 18 test binaries, 0 failed (incl.
  `actor_runtime_truth` 5, `actor_size_truth` 1, `schema_generated` 2,
  `terminal_supervisor` 10); `clippy -D warnings` clean (forced recompile); the
  `nix build … terminal-supervisor-answers-component-supervision-relation`
  check produced a valid result.
- **No artifact drift**: running the schema-update test left the working copy
  byte-identical — the checked-in generated artifacts are fresh.
- **`NotBuiltYet` is honestly typed**: `supervisor.rs` `event_for_meta_request`
  returns a typed unimplemented reply for `CreateSession`/`RetireSession`, not a
  silent `Ok` or panic.

So the operator's verification claims are accurate, and the "Remaining" gap
(meta `NotBuiltYet`) is candidly disclosed.

## Findings (verified-real, severity-ordered)

### High

1. **The listener is an async tokio task named `Actor*`, not a kameo actor.**
   The entire runtime contains exactly one `impl kameo::Actor` —
   `RequestGate` (`actor_runtime.rs:358`). `ActorMultiListenerDaemon` /
   `ActorListenerTask` hold no mailbox and impl no `Actor`; the accept path is
   `tokio::task::JoinSet` tasks running `accept().await` in a bare loop
   (`:659-678`, `:883-912`). Design 553 §topology specified a `ListenerActor`
   whose "mailbox replaces the blocking accept loop." The `Actor*` prefix
   asserts a topology the code does not implement. *(This is the API-truth
   issue the operator is already correcting via Spirit `ilxh`.)*

2. **Working-tier connection concurrency defaults to 1, and a subscription
   holds its admission permit for the whole stream — one subscriber starves all
   other terminal working requests.** *(My own cross-check; the fan-out praised
   the permit cap but did not check the default value or the
   permit-held-during-subscription interaction.)* The generated
   `DaemonBinder::bind` constructs `ActorMultiListenerDaemon::new(...)` with **no**
   `.with_concurrency_limit(...)` (`terminal/src/schema/daemon.rs:160-166`), so
   it inherits `RequestConcurrencyLimit::one()` (`actor_runtime.rs:508`). The
   per-tier gate acquires the permit in the accept loop *before* dispatch
   (`:725-736`), and an `AcceptedConnection` holds its `_permit` for the entire
   `handle_connection`. A `SubscribeTerminalWorkerLifecycle` runs
   `TerminalSubscriptionRelay::run` until EOF (`daemon.rs:341-375`) — so a single
   live subscription pins the working tier's only permit and blocks every other
   terminal control request indefinitely. Effectively critical for any
   deployment that uses worker-lifecycle subscriptions (a core terminal
   feature). Fix: emit `.with_concurrency_limit(N)` (the BoundedWorkers cap-64
   the design called for), and/or move subscription relays off the admission
   permit so long-lived streams don't consume a request slot.

3. **`RuntimeRoot` supervised-root actor is absent.** The generated shell has no
   `on_start`/`on_stop` lifecycle root and no `wait_for_shutdown`
   (`schema/daemon.rs:101-111,133-168`); the supervisor is started lazily and
   unsupervised via `OnceCell::get_or_try_init` on the first connection
   (`daemon.rs:63-67`). Design 553 specified a supervised root that spawns
   children under supervision in `on_start`.

4. **Dropped supervision handle leaks a detached OS thread owning a bound
   `UnixListener`.** `from_configuration` does `let _supervision =
   configuration.supervision_listener().spawn()?;` and drops it
   (`daemon.rs:55-61`). The spawned listener thread is detached with no join
   handle and no shutdown path.

5. **`TerminalSupervisor` has no `RestartPolicy` and is transient-state** — a
   restart reconstructs from `Args` and silently resets the in-memory worker
   registry (`supervisor.rs:652-662`). Per the design hazard list, transient-state
   actors must declare `RestartPolicy::Never` (or persist), not default.

6. **Synchronous redb (sema-engine) I/O runs inline in the supervisor's async
   handlers** with no `spawn_blocking` (`supervisor.rs:515-543`, and
   `:521,546,559,580,786`). Blocking I/O in an async handler stalls the tokio
   worker — the exact hazard the design names. Pre-existing, not introduced by
   this slice, but now on the async path.

7. **Meta tier does raw frame decode inside the component**
   (`daemon.rs:131-152`), the raw-stream hook design decision 7 wants retired in
   favor of a generated typed meta tier.

8. **The subscription test validates the LEGACY blocking spine, not the new
   emitted relay** (`tests/terminal_supervisor.rs:614-680` vs the new
   `daemon.rs:316-375`). The report's "existing subscription test still passes"
   is true but misleading — it does not exercise the migrated path.

9. **The old blocking spine is still present and re-exported**
   (`triad-runtime/src/{daemon.rs,workers.rs,lib.rs}`), which design decision 5
   said would "become dead and be deleted." Expected mid-migration (lojix/cloud
   still consume it), but it is an open deletion debt, not a finished state.

### Medium

- Per-request work is bare `tokio::spawn`, not a supervised continuation-driver
  actor (the "per-request Nexus driver" element is a task).
- `SubscriptionActor` topology element is absent — the relay is an inline async
  loop on the connection task, not an actor owning a registry.
- `TerminalActorCall { detail: String }` is a stringly error that flattens every
  actor-failure variant (`daemon.rs:496-513`, `error.rs:19-21`).
- The daemon hand-writes a parallel single-payload codec, duplicating the
  contract helper and the sibling sync codec, and loses the count detail
  (`daemon.rs:216-225,280-289`).
- The emitted topology is a flatter spawn-per-connection + single `RequestGate`,
  not design 553's named actor tree — the divergence is not recorded anywhere.
- Two parallel supervisor stacks coexist (emitted `daemon.rs` + legacy blocking
  `supervisor.rs`); the orphaned blocking `TerminalSupervisorDaemon` library
  surface is unmentioned in "Remaining."

### Low

- Terminal parks on the emitter's `component_decoded()` working escape hatch
  rather than the typed-input spine (downgraded from high — it is an
  emitter-sanctioned, explicitly-named hatch, not bespoke).
- Import alias `TerminalFrameBody as FrameBody` is a mild ancestry/clarity smell.
- The report's 204 caveat is accurate but misframes a strict superset
  (terminal builds on a *later* pushed stack) as a divergence; no integration
  hazard exists.

### What is genuinely right (praise)

Build/test/clippy/nix all pass on forced recompile; busy-poll is gone
(`accept().await`, no `set_nonblocking`/`WouldBlock`/`thread::sleep` on the live
path); `RequestGate` is a real kameo actor with a delegated reply so its mailbox
stays free while permits wait; `TerminalSupervisor` is a real actor and the
single mailbox-serialized state owner; every fallible op uses `.ask()` (never
`.tell()`); no self-ask deadlock; no `spawn_in_thread` on the state actor; the
shell is emitted by the shared `schema-rust-next` emitter with deterministic,
Nix-clean artifacts; triad overrides honored and witnessed; deferral fence held;
`NotBuiltYet` honestly typed; synthetic helper types are data-bearing (pass the
ZST test). The discipline here is real.

## The decision this surfaces: actor listeners vs honest task naming

Design 553 specified actor listeners; the implementation chose **task listeners
+ one gate actor + one state actor**. `r310` explicitly licenses revising the
approach when implementation evidence shows a better design — and a listener
that only accepts-and-dispatches has no state to justify actor overhead, so the
task shape is defensible. The honest resolutions are the two the operator and
psyche are converging on: either **make the listeners real kameo actors** (match
553), or **rename the `Actor*` shell to its true shape** (`Async*`/task) and
amend 553 to record that the listener tier is a task, not a mailbox. Either
closes finding 1; the second is cheaper and, given `r310`, legitimate. The
`RequestGate` stays the one real actor regardless.

## triad-runtime repo-intent correction (the "incorrectly worded" intent)

The psyche flagged that the repo intent is incorrectly worded. Confirmed, and
precisely: `triad-runtime/INTENT.md` and `ARCHITECTURE.md` describe the shells
as **`AsyncMultiListenerDaemon`/`AsyncSingleListenerDaemon`/`AsyncListenerSocket`**
while the *code* names them **`ActorMultiListenerDaemon`/…** — the doc and the
code have diverged on the names. The INTENT also overstates: "`triad-runtime`
should provide **Kameo/Tokio** runtime nouns … those nouns must keep **actor
mailboxes** available while requests wait" — but only `RequestGate` is a Kameo
actor with a mailbox; the listener/connection nouns are tokio tasks. Yet the
same INTENT already states, correctly, "the listener accept loops are
independent Tokio tasks." So it is internally inconsistent. The correction
(operator to land on the rename branch, since `triad-runtime` is operator-owned
code and `INTENT.md` updates on the same branch as the work): align the doc
names to whatever the rename picks, and reword the overstatement to "one Kameo
admission actor (`RequestGate`) per listener keeps its mailbox available while
permits wait; the listener and connection shells are tokio tasks, not actors."

## Recommended operator follow-ups, ranked

1. Finding 2 (concurrency-1 + subscription-permit starvation) — correctness,
   fix first: emit a real `with_concurrency_limit`, and/or take subscription
   relays off the request permit.
2. Findings 3-5 (supervised root, leaked supervision thread, RestartPolicy) —
   lifecycle correctness.
3. Finding 6 (`spawn_blocking` the redb I/O).
4. Finding 1 + the INTENT/naming correction — resolve the actor-vs-task naming
   honestly and fix the repo intent.
5. Findings 7-8 (typed meta tier; a test that exercises the *new* relay).
6. Decision-5 spine deletion (finding 9) tracked for when lojix/cloud migrate.
