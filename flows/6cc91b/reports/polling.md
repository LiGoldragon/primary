# Polling in the base layer

Answering the living's comment on the gap "polling sits in the base layer".

## 1. The words, and what is actually there

### "daemon" in the audit = metaNexus

The audit used **daemon** as the generic word for a long-running process that
sits there holding sockets open. In your terms that whole thing is the
**metaNexus**: signal actor, Nexus actor and Sema actor running as one
process. The audit had no word for it because the code has none either — the
type is literally spelled `BoundMultiListenerDaemon`. That naming *is* the
gap; "daemon" is the borrowed Unix word the code kept. The library it is built
from is Nexus core; one socket and its contract is a Nexus.

### What polling is, exactly

Polling is: **ask again, on a timer, whether anything arrived.** The process
never sleeps properly — it wakes, looks, finds nothing, sleeps a fraction of a
second, wakes again, forever, even with no one connected. Exactly one base
layer loop does this — `triad-runtime/src/daemon.rs`, lines 387-394:

```rust
pub fn serve_next_stream(&mut self) -> Result<(), ListenerError> {
    while self.runtime.should_continue() {
        if self.try_serve_next_stream()? { return Ok(()); }
        thread::sleep(self.listener_poll_interval.duration());
    }
    Ok(())
}
```

Default interval: **10 ms** (`ListenerPollInterval::default()`, 178-182) —
**100 wakeups per second per process, indefinitely**, doing nothing.

### Which components take which path

Witnessed by grep across `/git/github.com/LiGoldragon/*/src` and `ps`.
| Component | Path it takes | Quiet? |
|---|---|---|
| lojix-nexus (**running**) | `AsyncMultiListenerDaemon` | yes |
| message-daemon (**running**) | `AsyncMultiListenerDaemon` | yes |
| orchestrate-nexus (**running**) | its *own* `tokio::select!` loop, not the runtime's | yes, but duplicated code |
| router, mirror, system, mind, harness, terminal, terminal-cell, introspect | `AsyncMultiListenerDaemon` | yes |
| criome | hand-rolled: two non-blocking sockets + `sleep(10ms)` | **no — polls** |
| triad-runtime's own tests | `BoundMultiListenerDaemon` (the 10 ms loop) | **no — polls** |
| persona | readiness retry loops with `attempt_interval` | polls, but bounded |

**The important finding: no shipping Nexus uses the polling loop.** Sync
`BoundMultiListenerDaemon` is exercised only by `triad-runtime/tests/daemon.rs`.
The one production polling site is criome (`criome/src/daemon.rs:346-354`).

### Why it exists

Claimed, not witnessed: the introducing commit (`28d03c3`) has an **empty
body** and there is no comment at the loop, so the reason is read off the
code's shape, not a record. Synchronous `std::os::unix::net::UnixListener`
cannot wait on *two* listeners at once — blocking on the ordinary socket means
missing the meta socket — so the author took the only tool plain std offers:
set both non-blocking, try each, sleep. The same reasoning appears again in
criome, arrived at independently. **Polling here is not a choice; it is the
absence of a primitive.** Nobody decided to poll; they ran out of library.

### The other polling site: harness

`harness/src/claude.rs` watches Claude's transcript files, and has both paths:

- Good path (393-448): a `notify` watcher blocking on `recv_timeout` —
  genuinely asleep until the file changes.
- `PollingFallback` (110-138): if the watcher cannot be created, it re-reads
  the whole snapshot every **250 ms**.
- Even on the good path the wait is capped at **5 s**
  (`event_reconciliation_interval`, line 41), so it wakes and re-reads every
  5 s regardless — a hedge against the watcher missing an event.

Harness is thus mostly quiet, with a 5 s heartbeat it does not strictly need.
Claimed, not witnessed: the hedge exists because inotify can miss events on
some filesystems — no comment or commit states it.

## 2. How it should be done

The rule in `Vision/nexus.md`: *a correct system goes quiet when nothing
changes.* A process waiting on sockets should be blocked in the kernel at zero
cycles until the kernel wakes it because a byte arrived. That is what
`poll(2)`/`epoll` do and what `mio` and `tokio` wrap; waiting on many sockets
at once is exactly the problem those calls solve. The correct loop has **no
sleep in it at all**.

**The async variant already does this** — witnessed.
`AsyncMultiListenerDaemon::serve_connections` (`async_runtime.rs:691-711`)
spawns one tokio task per listener into a `JoinSet`, each blocking on
`listener.accept_connection().await`. No interval, no sleep, no
`ListenerPollInterval` anywhere in that file; tokio parks the thread on epoll.
The right answer is already written — it is just not the only one available,
and criome and orchestrate each went around it.

So the fix is not invention. It is **deletion plus one name**.

## 3. Proposal: one listener primitive

### What it owns

A `NexusListenerSet`: a metaNexus's whole set of sockets (ordinary, meta, any
further privileged ones), their file lifetimes (bind, chmod, unlink on drop),
and the one quiet wait yielding the next connection from whichever socket
spoke — tagged with which socket, so the privileged/ordinary distinction
survives into the type. No protocol, no runtime, no actors.

```rust
pub struct NexusListenerSet<Socket> { /* bound listeners, keyed by Socket */ }
pub struct Accepted<Socket> { pub socket: Socket, pub stream: UnixStream }

impl<Socket: SocketKind> NexusListenerSet<Socket> {
    pub fn bind(sockets: impl IntoIterator<Item = SocketSpec<Socket>>) -> Result<Self, BindError>;
    /// Blocks in the kernel until one socket has a peer. Never spins.
    pub async fn accept(&self) -> Result<Accepted<Socket>, AcceptError>;
    pub fn sockets(&self) -> &[SocketSpec<Socket>];
}
```

The `Socket` parameter is where your architecture guard lands: a handler typed
for the ordinary socket cannot be handed a meta connection — the same
compile-time-kind idea you described for signal/sema/Nexus, one level down.

### Which repository

**The Nexus core library**, not triad-runtime, not a new repo.

From your own words: core "has all of the interfaces and kinds defined for how
to build metaNexus." A metaNexus is defined by its sockets — at minimum
ordinary and meta — so socket-set-and-quiet-wait is the most primitive
interface it has. If that lives in triad-runtime, Nexus core depends on
triad-runtime for its own definition and triad-runtime stays the real base —
the gap the audit already named ("the nexus library is not the base of the
nexuses"). Put it in core, with triad-runtime's async daemon built on core
rather than beside it, and both gaps close in one move. A new repository would
add a third base.

### What each consumer deletes

| Consumer | Deletes |
|---|---|
| triad-runtime | `ListenerPollInterval` (the whole type), `BoundMultiListenerDaemon::serve_next_stream`'s sleep loop, `with_listener_poll_interval`, `MultiListenerDaemon`'s interval field — and the synchronous multi-listener daemon entirely, since nothing ships on it |
| criome | `serve_forever`'s non-blocking + `sleep(10ms)` loop, `try_serve_working_connection`, `try_serve_meta_connection` |
| orchestrate-nexus | its private `tokio::select!` accept loop in `transport/mod.rs` |
| every async consumer (router, mirror, system, mind, harness, terminal, terminal-cell, introspect, lojix, message) | nothing behavioural — they re-point at core's primitive through the async daemon |

Net: two hand-rolled accept loops and one sleep-based one collapse into one.

### The smallest witness that proves it goes quiet

A test asserting **no wakeups without input**: bind two sockets, spawn the
accept, measure that the process did no work while idle.

```rust
#[tokio::test]
async fn a_bound_listener_set_consumes_no_cpu_while_idle() {
    let set = NexusListenerSet::bind(two_sockets()).unwrap();
    let before = process_cpu_time();          // /proc/self/stat utime+stime
    let accept = tokio::spawn(async move { set.accept().await });
    tokio::time::sleep(Duration::from_secs(2)).await;
    assert!(!accept.is_finished());           // still waiting, nothing arrived
    assert!(process_cpu_time() - before < Duration::from_millis(5));
}
```

Two seconds of wall time must cost under 5 ms of CPU: under the 10 ms loop
that is ~200 wakeups and fails; blocked on epoll it is ~0 and passes. The
vision made checkable in one assertion, runnable against every Nexus.

## Marks

- **Witnessed** (read directly): the 10 ms loop and its default; that only
  `triad-runtime/tests/daemon.rs` uses it; that the async daemon has no
  interval and blocks on `accept().await`; criome's 10 ms sleep;
  orchestrate-nexus's own select loop; harness's 250 ms and 5 s defaults;
  which components import which daemon; that lojix-nexus, message-daemon and
  orchestrate-nexus are running (`ps`).
- **Claimed** (no record states it): why the poll interval was written (the
  introducing commit body is empty, no comment at the loop); the 5 s hedge.
- **Not witnessed**: nothing was built or run; no CPU measured — wakeup counts
  are arithmetic from the intervals.

## Sources

All under `/git/github.com/LiGoldragon/`:

- `triad-runtime/src/daemon.rs` (60, 106, 123, 178-196, 289-299, 373-402);
  `triad-runtime/src/async_runtime.rs` (652-720, 794-825);
  `triad-runtime/tests/daemon.rs` (244-290); commit `28d03c3` (body empty)
- `criome/src/daemon.rs` (323-375);
  `orchestrate/crates/orchestrate-nexus/src/transport/mod.rs` (160-220)
- `harness/src/claude.rs` (20-60, 94-138, 393-448);
  `persona/src/readiness.rs` (25-60)
- Async construction sites: `message/src/daemon.rs`, `lojix/src/daemon.rs`,
  `router/src/component_daemon.rs`, `mirror/src/component_daemon.rs`,
  `system/src/shell.rs`, `introspect/src/daemon_shell.rs`,
  `{harness,mind,terminal,terminal-cell}/src/schema/daemon.rs`
- `/home/li/primary/Vision/nexus.md`;
  `/home/li/primary/flows/6cc91b/vision/nexus.md` (2026-09-13, 09-14)
