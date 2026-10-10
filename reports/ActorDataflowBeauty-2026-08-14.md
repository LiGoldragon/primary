# Beautiful Designs in the Actor and Dataflow Space

Study material for the psyche and the Designer, feeding the
rust-component-architecture skill proposal. No proposals or verdicts
on estate design -- study material with clearly separated analysis.

2026-08-14. Researcher session for Designer ba906ae2.

---

## Table of Contents

1. [Erlang/OTP and the BEAM](#1-erlangotp-and-the-beam)
2. [Akka/Pekko Typed](#2-akkapekko-typed)
3. [Pony](#3-pony)
4. [Microsoft Orleans](#4-microsoft-orleans)
5. [Timely Dataflow](#5-timely-dataflow)
6. [Differential Dataflow](#6-differential-dataflow)
7. [Kafka Streams](#7-kafka-streams)
8. [Apache Flink](#8-apache-flink)
9. [The Elm Architecture](#9-the-elm-architecture)
10. [Rust Actor Crates](#10-rust-actor-crates)
11. [Sources](#sources)

---

## 1. Erlang/OTP and the BEAM

### 1.1 The Behavior Abstraction

**Core idea.** An OTP behavior (gen_server, gen_statem, gen_event) is a
reusable process skeleton. The framework owns the message loop, the
system-message protocol (tracing, suspend/resume, code upgrade), and
the integration with supervisors. The developer fills in a callback
module that answers specific questions: what is the initial state? how
should this call be handled? what is the new state?

In gen_server: the framework calls `Module:init/1` to boot, enters a
receive loop, dispatches `$gen_call` to `Module:handle_call/3`,
`$gen_cast` to `Module:handle_cast/2`, anything else to
`Module:handle_info/2`. The developer never writes `receive`. In
gen_statem: the process has explicit named states alongside data,
separating control flow from payload. Transitions carry actions --
generating new events, setting timeouts, postponing events -- all
expressed as return values, not direct scheduler calls.

**Problem dissolved.** Before behaviors, every server process was an
ad-hoc receive loop. The boilerplate for robust loops -- handling EXIT
signals, system messages, timeout management, shutdown -- was
duplicated and typically wrong. Behaviors centralize that machinery
once, tested, in the standard library. The developer's callback module
handles only domain concerns.

**Cost.** You cannot do blocking work in a handle_call without blocking
that process for all callers. Long-running synchronous operations must
be pushed to worker processes. Developers must learn which callback
maps to which message type.

> **--- Estate analysis ---**
>
> The behavior abstraction resonates deeply with the estate's ground:
> "every behavior under a trait (an ontology in code)." The OTP
> behavior is exactly the pattern of a trait whose implementor fills in
> the domain-specific callbacks while the framework owns the
> structural machinery. The psyche's vision of each daemon's Nexus
> having its operations visible as an ethos-authored interface is the
> same separation: the trait (behavior) specifies what operations
> exist; the implementation fills them in.
>
> The difference: OTP behaviors are a small fixed set (gen_server,
> gen_statem, etc.). The estate envisions an open set of traits -- the
> component architect defines them per domain. This is closer to what
> Akka Typed does with Behavior[T] (section 2).

### 1.2 Supervision Trees and Let-It-Crash

**Core idea.** A supervisor is a process whose sole job is to watch
children and restart them according to a declared strategy when they
crash. The four strategies -- one_for_one, one_for_all, rest_for_one,
simple_one_for_one -- encode structural recovery policies. A restart
intensity limit (MaxRestarts in MaxSeconds) acts as a circuit breaker:
too many restarts means the problem is not transient, and the
supervisor itself exits, propagating failure upward.

The let-it-crash principle, precisely stated: when a process
encounters an unexpected condition it cannot safely handle -- a
violated invariant, a resource it cannot acquire -- it crashes. The
supervisor, not the process, is responsible for recovery. Error
handling is separated from business logic as a structural property, not
a code style preference.

This works because each Erlang process has an isolated heap. A
crashing process cannot corrupt another's memory. The supervisor
receives a structured exit signal, not a heap corruption.

**Problem dissolved.** Defensive error handling (try/catch everywhere)
interleaves domain logic with recovery logic, making both harder to
reason about. Supervision makes recovery a property of the process
graph, not the call graph.

**Cost.** Supervision works well for stateless or re-derivable state.
If a process holds state not recoverable from external sources, a
crash destroys it. OTP's answer: externalize critical state (ETS
tables, mnesia, durable sources).

> **--- Estate analysis ---**
>
> The estate's daemon architecture already implies structural fault
> isolation -- each daemon is its own process with its own database
> (SEMA). A crashed daemon can be restarted and rehydrate from its
> typed store. The let-it-crash principle aligns naturally with the
> single-writer store: the store survives the crash, so the daemon's
> state is always recoverable.
>
> What the estate does not yet have is a formal supervision hierarchy
> between daemons (Ethos supervising Nomos?). The inter-daemon
> relationship is currently message-based coordination, not structural
> supervision. Whether supervision trees are needed at the
> inter-daemon level or only within a daemon's internal actor graph is
> an open question.

### 1.3 The BEAM Process Model

**Core idea.** BEAM processes are lightweight continuations with
isolated heaps, individual mailboxes, and per-process garbage
collection. Creating a process costs microseconds and a few hundred
bytes. The scheduler achieves soft-realtime fairness via reduction
counting: each function call costs one reduction; after ~4000
reductions, the process is preempted. Per-process GC means no global
pause -- each process collects independently, bounded by its own heap
size.

Selective receive lets a process pattern-match its mailbox, taking the
first matching message while leaving others queued. This enables clean
protocol implementations where out-of-order messages are held without
explicit buffering.

Hot code loading allows two versions of a module to coexist. A fully
qualified call (Module:function) goes to the current version; an
unqualified call stays on the caller's version. Migration happens at
well-defined points the process controls.

Location transparency: the send operator `!` works identically for
local and remote PIDs. The runtime handles serialization and TCP
transport. Links and monitors are also transparent across nodes.
Network failure manifests as process failure (nodedown signals), so the
same supervision machinery handles both.

**Problem dissolved.** The mutual reinforcement is the beauty: lightweight
processes make structural decomposition cheap; per-process GC makes
them safe for latency-sensitive work; location-transparent messaging
makes them composable across machines; hot code loading makes the
whole thing operable without downtime.

**Cost.** Message passing copies data between heaps (except large
binaries, which are reference-counted on a shared heap). Selective
receive with many non-matching messages incurs O(n) scanning.
Location transparency does not imply equivalence -- remote sends have
higher latency and can fail in ways local sends cannot.

> **--- Estate analysis ---**
>
> The BEAM's per-process heap with no shared mutable state is the
> purest existing implementation of what the estate calls "single-writer
> typed store per daemon." Each BEAM process owns its state; mutation
> is local; communication is by message. The estate's SEMA is a more
> elaborate version -- a typed database engine rather than a heap --
> but the isolation principle is identical.
>
> Selective receive is interesting for the estate's staged processing
> (triage/execute/apply-observe). A daemon could use selective receive
> to prioritize certain signal types during different processing
> stages, though the estate's model is more structured than mailbox
> scanning.
>
> The BEAM's location transparency resonates with signal messaging
> across the network via a router. The estate's "routable signal"
> concept (threeStacks.md 2026-08-11) is the same idea: the router
> differentiates signal types and sorts them, so the daemon code does
> not change when the peer moves to another node.

---

## 2. Akka/Pekko Typed

### 2.1 Behavior-as-Value

**Core idea.** An actor IS its current behavior. A `Behavior[T]` is a
value -- essentially a function from `(T, ActorContext[T])` to the
next `Behavior[T]`. The runtime invokes the current behavior on each
incoming message; the return value becomes the behavior for the next
message. There is no implicit mutable state other than what the
behavior value captures.

Behaviors compose through combinators: `Behaviors.setup`,
`Behaviors.receive`, `Behaviors.same`, `Behaviors.stopped`,
`Behaviors.withTimers`. A state machine is a sequence of behavior
values, each returning the next. The full protocol is visible in the
type parameter: `ActorRef[T]` constrains what messages can be sent.
The compiler rejects the wrong message type.

**Problem dissolved.** Classic Akka's `Actor` with `receive: Any => Unit`
gave no compile-time protocol checking. State was implicit mutable
fields plus `become`/`unbecome`. Behavior-as-value makes the state
machine explicit and the protocol typed.

**Cost.** Behaviors that evolve through many state transitions via
returned closures can be hard to read. Multi-protocol actors require
`context.messageAdapter[R](f: R => T)` to wrap responses from other
actors into the local protocol type -- deliberate but verbose.

> **--- Estate analysis ---**
>
> Behavior-as-value is the closest existing model to what the estate
> is building. The psyche's vision: "every behavior under a trait"
> where traits constrain implementers to think in concepts. A
> `Behavior[T]` in Akka is exactly a trait-bounded protocol type. The
> estate's Signal layer (the typed message edge) maps to the type
> parameter T -- the fully typed signal messages. The Nexus
> (execution/decision layer) maps to the behavior implementation --
> the function that receives a signal and produces the next state.
>
> The adapter pattern (wrapping external responses into local protocol
> types) is relevant for inter-daemon communication. When Ethos sends
> a request to Nomos and receives a response, that response arrives as
> a foreign signal type that must be adapted into Ethos's own signal
> vocabulary. The estate's approach -- each daemon has its own signal
> repos -- already implies this separation.
>
> The key difference: Akka's Behavior[T] is a single type parameter.
> The estate's signal is a richer structure -- an interface file with
> input, output, refusal, and stream sections, each with its own shape-
> defined type. This is a more elaborate protocol specification than
> a single sum type.

### 2.2 Persistence as a Behavior (EventSourcedBehavior)

**Core idea.** Event sourcing is expressed as a specialization of
`Behavior[Command]`. The constructor takes four things: a persistence
ID, an empty state, a command handler
`(State, Command) => Effect[Event, State]`, and an event handler
`(State, Event) => State`. The Effect ADT describes what the runtime
should do: persist events, then fold them via the event handler, then
optionally reply or run side-effects. Side-effects execute only after
events are durably written.

The event handler is always a pure fold. No I/O, no messages, no
side-effects. The runtime replays the full event stream from the
journal to reconstruct state after a crash.

**Problem dissolved.** The dual-write problem -- updating a database and
sending a message atomically. In event sourcing you write the event
first; all downstream consequences derive from events.

**Cost.** The event schema is the permanent API. Changing events
requires migration strategies (event adapters, upcasters). The journal
grows and must be snapshotted.

> **--- Estate analysis ---**
>
> This resonates powerfully with the estate's operational editing
> vision. The psyche said SEMA "was way more important than Nexus
> because the whole point of creating a real code evolution engine was
> that through operational editing, we could have database migration
> operations come out instantly or along with the editing operation."
>
> EventSourcedBehavior's command/event separation maps to the estate's
> signal/operation separation: a signal arrives (command), the Nexus
> decides what happens (command handler producing effects), and SEMA
> applies the resulting operations to the store (event handler as pure
> fold). The event handler's purity -- no side effects, just
> `(State, Event) => State` -- is exactly what makes operational
> editing yield deterministic database migrations.
>
> The estate could go further than Akka: because ethos types are fully
> specified and the store is typed, the "event schema" is not a
> separate concern -- it is the ethos type system itself. Schema
> evolution is ethos evolution, and operational edits carry their
> migrations alongside.

### 2.3 Typed Service Discovery (Receptionist)

**Core idea.** A `ServiceKey[T]` pairs a string identifier with a type
parameter. Actors register with the Receptionist; consumers subscribe
and receive `Listing` messages carrying `Set[ActorRef[T]]`. The type
parameter is preserved through the entire chain -- you get back typed
refs. In cluster mode, the Receptionist is backed by a CRDT.

**Problem dissolved.** Path-based actor selection with no type safety.
Service discovery becomes a typed protocol.

**Cost.** Listings are eventually consistent.

> **--- Estate analysis ---**
>
> The estate's router concept (routable signal, the enum in a
> universal signal repo) serves a similar purpose: typed routing of
> signals to daemons. The Receptionist's `ServiceKey[T]` is analogous
> to a variant in the router enum -- it names a signal type and the
> daemon that handles it. The estate's approach is more static (the
> router enum is generated from ethos, not discovered at runtime), which
> is consistent with the "both sides know the full schema" principle.

---

## 3. Pony

### 3.1 Reference Capabilities

**Core idea.** Every reference in Pony carries a type-level annotation
-- a reference capability -- that encodes what access the holder has
and what access others may have concurrently. Six capabilities:

- **iso** (isolated): read/write, no other aliases exist anywhere.
  Can be sent to another actor by consuming the reference -- zero-copy
  transfer of mutable data. The compiler ensures the original alias is
  destroyed at the send site.
- **val** (value): deeply immutable. Freely shareable across actors
  since nothing can write.
- **trn** (transition): read/write, but others may hold read-only
  (box) aliases. Can be frozen into val by consuming it.
- **ref** (reference): mutable, multiple aliases within the same
  actor. Not sendable.
- **box** (read-only): readable, others may be writing within the
  same actor. Not sendable.
- **tag** (identity only): no read or write; only identity comparison
  and behavior dispatch (async calls). All actor references held by
  other actors are tag.

These are erased at compile time after verification. The type system
enforces viewpoint adaptation: accessing a field through a reference
narrows the effective capability based on the access path.

**Problem dissolved.** Data races are a category error at the type level.
The program cannot be written with a race. No locks, no atomics, no
copying needed for safe sharing. The runtime has no synchronization
primitives because the type checker has proven they are not needed.

**Cost.** Substantial cognitive overhead. The capability subtype lattice
and recovery rules (the `recover` block) require deep understanding.
Builder patterns need deliberate use of trn.

> **--- Estate analysis ---**
>
> Pony's reference capabilities are the most rigorous existing answer
> to "how do you prove at compile time that actors do not share mutable
> state." The estate's Rust implementation cannot match this at the
> language level -- Rust's ownership system prevents data races in
> concurrent code but does not have Pony's fine-grained capability
> vocabulary for actor messaging specifically.
>
> However, the estate's architecture achieves the same property by
> construction: the single-writer typed store (SEMA) means each
> daemon owns its state exclusively. Signal messages are typed and
> presumably serialized (rkyv/CapnProto), so they are always copied or
> zero-copy-read (val-equivalent). The iso/val distinction matters
> most when actors share a process and heap; the estate's daemons are
> separate processes with separate stores, so the isolation is
> structural rather than type-level.
>
> The val capability (deeply immutable, freely shareable) is worth
> studying for the estate's observation model. Push-only observation
> means observers receive immutable snapshots of events -- val
> semantics. An ObservationEvent in the observer interface is a val by
> nature: the observer cannot mutate what it observes.

### 3.2 Causal Messaging and Per-Actor GC

**Core idea.** Messages between actors are delivered in causal order: if
A sends m1, and m1's processing causes m2 to be sent to C, then C
sees m1's effects before m2. Each actor has its own heap; GC runs
per-actor without stopping others. The ORCA garbage collection
protocol uses reference counting augmented with ownership tracking,
and requires causal delivery as a correctness precondition -- credits
must arrive before messages that depend on them.

An idle, unreferenced actor can be collected entirely: heap reclaimed,
data freed. The cost model is local and predictable.

**Problem dissolved.** Stop-the-world GC pauses. The actor boundary is
the GC boundary. Tail latency from GC is bounded by individual actor
heap size.

**Cost.** The capability system is required for this to work -- ORCA is
unsound without it. GC and type system are co-designed (hence "Orca:
GC and Type System Co-Design for Actor Languages").

> **--- Estate analysis ---**
>
> The co-design of GC and type system is a deep lesson. In the
> estate, the co-design is between the store engine (SEMA) and the
> signal types: the store knows exactly what types it holds because
> they are ethos-generated, and the signal types define exactly what
> can enter or leave. This is not GC co-design, but it is the same
> principle: the runtime mechanism and the type system are designed
> together, not independently.

---

## 4. Microsoft Orleans

### 4.1 Virtual Actors (Grains)

**Core idea.** A grain is a "virtual actor" -- its logical identity is
permanent (it can always be addressed by key), but its physical
instantiation is managed by the runtime. You obtain a grain reference
via `GetGrain<IGrainInterface>(key)` -- this always succeeds
regardless of whether an activation exists. On first message, the
runtime selects a silo, instantiates the grain, loads persisted state,
and routes the call. When idle, the runtime deactivates it. The grain
never explicitly starts or stops.

Each grain activation executes single-threaded: requests are processed
one at a time. No locks needed on grain state.

**Problem dissolved.** Explicit lifecycle management. No "create actor",
"kill actor", "restart actor." The developer writes a class; the
runtime handles placement, activation, deactivation, failure recovery.

**Cost.** You cannot control placement (matters for data locality). The
always-available illusion hides activation latency. Persistence is
single-document snapshot, not event sourcing -- no audit trail.

> **--- Estate analysis ---**
>
> The virtual actor concept clashes with the estate's explicit daemon
> model. The estate's daemons are explicitly started, explicitly hold
> their database, and explicitly communicate. There is no transparent
> activation/deactivation -- the daemon IS its running process plus
> its store. This is a deliberate choice: the psyche wants to "see
> the main operations," and transparent lifecycle hides exactly that.
>
> However, Orleans' single-threaded execution guarantee per grain
> resonates with the estate's single-writer store. Both achieve the
> same property -- no concurrent mutation of a grain/daemon's state --
> through different mechanisms: Orleans uses a TaskScheduler; the
> estate uses process-level ownership of the SEMA engine.
>
> The grain persistence model (snapshot, not event sourcing) is a
> weaker version of what the estate envisions. The estate's operational
> editing is closer to Akka's EventSourcedBehavior -- operations are
> the permanent record, and the current state is derived.

---

## 5. Timely Dataflow

### 5.1 Progress Tracking (Frontiers)

**Core idea.** Every message carries a timestamp. Every in-flight
message occupies a location in the dataflow graph. The pair (location,
timestamp) is a "pointstamp." A partial order on pointstamps defines
what could-result-in what: pointstamp A could-result-in B if a path
exists from A's location to B's whose time-adjustment function maps
A's timestamp to something at or before B's.

A frontier is the set of pointstamps below which no further work is
possible. When a frontier advances past timestamp t at an operator's
input, the operator receives a notification: no more records with
timestamp t will arrive. This notification triggers aggregation,
window completion, or fixed-point detection.

The distributed protocol is conservative reference counting: workers
exchange small delta messages about active pointstamps. Coordination
traffic is sub-linear in data volume.

(Source: Murray, McSherry, Isaacs, Isard, Barham, Abadi. "Naiad: A
Timely Dataflow System." SOSP 2013.)

**Problem dissolved.** Before this, iterative and streaming computations
required either centralized barriers (stop-the-world epochs) or could
not know when output was safe. Naiad lets workers run asynchronously
with correct, timely notifications.

**Cost.** The partial order must be finite and well-founded. Designing
correct timestamp types for complex nested loops is non-trivial. The
protocol assumes reliable delivery and crash-stop failures.

> **--- Estate analysis ---**
>
> Progress tracking is relevant to the estate's push-only observation
> model. An observer needs to know when an observation window is
> complete -- when all operations for a given "version" of the store
> have been applied. The frontier concept (no more records with this
> timestamp will arrive) is exactly the completeness guarantee an
> observer needs. The ObservationLagged and ObservationEnded events in
> the blessed observer fixture serve a similar purpose, though less
> formally.
>
> The estate does not currently have a formal progress-tracking
> protocol between daemons. If Ethos sends a batch of objects to
> Nomos for transformation, how does Ethos know the transformation is
> complete? Timely's frontier mechanism -- the daemon that has finished
> producing output for a given version announces it -- would answer
> this precisely.

### 5.2 The Dataflow Graph as the Program

**Core idea.** Operators are vertices, channels are directed edges. The
program IS the graph -- not a description interpreted by a runtime,
but the graph itself. Each operator is a closure with callbacks
(on_recv, on_notify). Higher-level abstractions are built by wiring
operators. There is no separate query planner or execution plan.

Each worker runs the full graph on its data partition. Workers
communicate only progress messages and data records. No master
assigns tasks.

**Problem dissolved.** The gap between logical plan and physical
execution. What you write is what runs.

**Cost.** Lower abstraction level. Optimization must be applied manually
or via library-level graph transformations.

> **--- Estate analysis ---**
>
> The dataflow-graph-as-program model is structurally different from
> the estate's daemon model. Daemons are long-lived processes that
> hold state and respond to signals; dataflow operators are stateless
> transformations wired into a graph. The estate's staged processing
> (triage/execute/apply-observe) is closer to a pipeline within a
> single daemon than to a dataflow graph across daemons.
>
> However, the Nomos transformation pipeline -- Ethos input goes
> through transformers and comes out as Logos objects -- could be
> modeled as a dataflow graph within the Nomos daemon. The transformer
> index is a set of operators; the ethos objects flow through them.
> Whether this is a useful framing depends on whether the
> transformations are independent (pipeline-parallelizable) or
> inherently sequential.

---

## 6. Differential Dataflow

### 6.1 Incremental Computation via Differences

**Core idea.** The fundamental unit is a triple (data, time, diff)
where diff is +1 or -1 (or any integer for multiplicity). A
collection at any time is the sum of all diffs at or before that time.
Every operator -- map, filter, join, reduce -- transforms streams of
difference triples. Operators propagate only the changes, not the
full collection.

**Problem dissolved.** The "recompute from scratch" tax. Prior
incremental systems could not efficiently handle deletions or nested
iterations. Differential handles both via signed diffs.

**Cost.** The system retains historical diffs to answer queries at
earlier times and compute deltas correctly. Memory grows with the
number of live times unless compacted.

(Source: McSherry, Murray, Isaacs, Isard. "Differential Dataflow."
CIDR 2013.)

### 6.2 Partially Ordered Time (Lattice Timestamps)

**Core idea.** Timestamps form a lattice -- a partially ordered set with
join and meet. A concrete example: time is a pair
(input_version, loop_iteration). Version 3, iteration 5 and version 4,
iteration 2 are incomparable. This lets a single computation
simultaneously track multiple input versions and multiple loop depths.

Frontiers are antichains of the lattice. Operators receive
notifications when the frontier advances past a lattice element.

**Problem dissolved.** Systems with total time ordering could not
express interleaved versioning and iteration. Lattice time allows
both simultaneously.

**Cost.** Reasoning about lattice timestamps is complex. Bugs in
timestamp design produce subtly wrong outputs, not crashes.

### 6.3 Arrangements (Shared Indexed Collections)

**Core idea.** An arrangement is a collection that has been sorted,
indexed, and shared across multiple consumers. It is incrementally
maintained via a log-structured merge strategy. Multiple queries can
share an arrangement, each seeing a consistent view without
independent indexing costs.

(Source: McSherry. "Shared Arrangements." VLDB 2020.)

**Problem dissolved.** Each operator maintaining its own index
multiplies memory and CPU cost. Arrangements achieve sub-linear
scaling across concurrent queries.

**Cost.** Explicitly introduced. Compaction interacts with the lattice
-- you can only compact layers whose timestamps are unreachable by
any live frontier.

> **--- Estate analysis ---**
>
> Differential dataflow's core idea -- propagating differences rather
> than full state -- resonates with operational editing. An operational
> edit IS a difference: it describes what changed, not the full new
> state. The estate's vision of edits yielding database migrations is
> exactly the differential principle: the migration is the diff, and
> the new database state is the old state plus the diff.
>
> Arrangements (indexed, shared, incrementally maintained) are
> analogous to what SEMA should be: a typed, indexed store that
> multiple consumers (Nexus operations, observers, CLI queries) can
> read from a consistent view. The arrangement's incremental
> maintenance -- new diffs are merged into the index -- is the
> operational editing model applied to the store.
>
> Lattice timestamps are relevant if the estate ever needs to track
> multiple versions of a capsule simultaneously (e.g., a draft edit
> alongside the committed state). This is not currently in the vision
> but could arise from the operational editing model.

---

## 7. Kafka Streams

### 7.1 The Log as Fundamental Abstraction

**Core idea.** Jay Kreps' insight: a durable, ordered, replayable log
unifies messaging, storage, and processing. A log is simultaneously a
buffer between producers and consumers, a replayable history for state
reconstruction, and a coordination mechanism that assigns canonical
order to events. Processing state is itself stored as a compacted log.
Failure recovery is replaying the changelog.

(Source: Kreps, "The Log: What Every Software Engineer Should Know
About Real-Time Data's Unifying Abstraction." LinkedIn Engineering,
2013.)

**Problem dissolved.** The distinction between message bus and database.
The log collapses them: the write-ahead log externalized and made the
primary interface.

**Cost.** Total ordering is guaranteed only within a partition.
Cross-partition ordering requires application-level coordination.

### 7.2 KTable/KStream Duality

**Core idea.** A KStream treats each record as an independent event. A
KTable treats each record as an upsert -- the latest value per key.
The duality: every KTable has an implicit KStream (its changelog), and
every KStream can be aggregated into a KTable. Stream-table joins look
up the table's current state at processing time.

**Problem dissolved.** The impedance mismatch between "events" (what
happened) and "state" (what is true now). The duality makes conversion
explicit and reversible.

**Cost.** The duality breaks at the total-ordering boundary. A table
read during a stream-table join reflects current state, not historical
state at the event's time. Reproducibility requires synchronized
changelog replay.

### 7.3 Exactly-Once Semantics

**Core idea.** Idempotent producers (sequence-number deduplication) plus
transactions (atomic writes across partitions) compose into
read-process-write transactions. The processor consumes, processes,
writes output and advances offsets atomically. Crash mid-cycle aborts
the transaction; replay is deduplicated.

**Problem dissolved.** The at-least-once vs. at-most-once choice for
stateful processors.

**Cost.** Transactional throughput is lower. Side effects to external
systems are outside the transaction boundary.

> **--- Estate analysis ---**
>
> The log-as-abstraction is interesting but at odds with the estate's
> model. The estate's SEMA is a typed database, not a log. The
> operational editing model is closer to event sourcing (the operations
> are the log, the state is derived) but the store is queryable and
> indexed, not append-only.
>
> The KTable/KStream duality is relevant for push-only observation.
> An observer watching a daemon's operations sees a KStream (events).
> The daemon's store is the KTable (current state). The observer can
> derive its own view of the store by folding the operation stream --
> this is exactly what push-only observation enables without polling.
>
> Exactly-once semantics matter for inter-daemon communication. When
> Ethos sends operations to Nomos and Nomos sends results to Logos,
> each step should be atomic. The estate does not yet have a
> transaction protocol for multi-daemon operations. This is a gap
> the component architecture will need to address.

---

## 8. Apache Flink

### 8.1 Event Time and Watermarks

**Core idea.** Flink distinguishes event time (when it happened),
ingestion time (when the system saw it), and processing time (wall
clock). A watermark is a control record asserting "no record with
event time earlier than W will arrive after this." Watermarks
propagate through the operator graph; when an operator receives
watermark W, it can close windows ending at or before W.

Out-of-order records arriving before the watermark are processed
correctly. Late data (after watermark) is handled by configurable
policy: drop, emit corrections, or side-output.

**Problem dissolved.** In processing-time-only systems, windowing is
non-reproducible and incorrect under delay. Event time makes results
deterministic with respect to event history.

**Cost.** Choosing the right watermark heuristic is application-specific
-- a latency/completeness tradeoff.

### 8.2 Chandy-Lamport Checkpointing

**Core idea.** Flink adapts the Chandy-Lamport distributed snapshot
algorithm for DAG dataflows. The coordinator injects checkpoint
barriers into source streams. Barriers flow with data, in-order.
When an operator receives barriers on all inputs, it snapshots state
to durable storage and forwards the barrier. No global processing
stop -- operators not yet at the barrier continue processing.

The snapshot is a globally consistent cut. On failure, all operators
roll back to the last completed checkpoint.

**Problem dissolved.** Stopping the world to take a consistent snapshot.
ABS achieves consistency without global pauses.

**Cost.** Multi-input operators must buffer records from fast inputs
while waiting for slow inputs' barriers -- memory pressure
proportional to throughput imbalance.

### 8.3 Unified Batch and Stream

**Core idea.** Batch processing is stream processing where the input is
bounded. Same runtime, same operators, same fault tolerance. Batch
mode enables bounded-input optimizations (blocking operators, no
checkpointing within stages).

**Problem dissolved.** Maintaining two codebases and APIs with different
semantics.

**Cost.** The runtime must accommodate both low-latency streaming and
high-throughput batch requirements dynamically.

> **--- Estate analysis ---**
>
> Flink's watermark concept is relevant for the estate's observation
> model. When an observer subscribes to a daemon's operations, it
> needs to know "all operations for this editing session have been
> applied." A watermark-like mechanism -- the daemon declares
> "version N is complete, no more operations for version N will
> arrive" -- would give observers a precise completeness guarantee.
>
> Chandy-Lamport checkpointing is relevant if the estate ever needs
> consistent snapshots across multiple daemons. A coordinated
> checkpoint of the Ethos, Nomos, and Logos stores would give a
> globally consistent view of the entire language processing pipeline.
> This is not currently in the vision but is the natural extension of
> operational editing across daemon boundaries.

---

## 9. The Elm Architecture

### 9.1 TEA: Model, Update, View

**Core idea.** The entire application is a pure function:
`update : Msg -> Model -> (Model, Cmd Msg)`. The runtime owns the
event loop, calls update when a message arrives, diffs the output, and
interprets any Cmd returned. The programmer never calls these
functions directly -- the runtime/programmer boundary is the point
where effects are exchanged.

The Msg type is a closed union -- the complete vocabulary of everything
that can happen. The compiler checks exhaustiveness. You can read the
Msg type and know every event the system handles.

Commands and subscriptions are effects described as data (Cmd Msg),
not performed. `Http.get` does not make an HTTP request -- it returns
a value that the runtime interprets. Side effects are values.

(Source: Evan Czaplicki, Elm guide, guide.elm-lang.org.)

**Problem dissolved.** In traditional systems, event handlers mutate
state, fire requests, and update UI -- all interleaved. TEA enforces
every state change through one function with one signature. Time-
travel debugging falls out for free: every transition is
(old_model, msg) -> new_model, fully reproducible.

**Cost.** All state must fit in the Model. Nested update functions
threading state slices downward and bubbling Cmds upward become
verbose at scale. The Msg type does not compose well -- large apps
need wrapper types. Local purity over modularity.

> **--- Estate analysis ---**
>
> TEA's Msg type as a closed union of everything that can happen is
> exactly the estate's signal interface: the input section of an
> interface file is an enum whose variants are every operation the
> daemon can receive. Record, Subscribe -- these are the Msg
> constructors. The compiler checks exhaustiveness. You can read the
> interface file and know every signal the daemon handles.
>
> Effects-as-data (Cmd Msg) resonates with the estate's separation of
> Signal and Nexus. A signal arrives; the Nexus decides what effect to
> produce; the effect is described as data (operations to apply to
> SEMA, signals to send to other daemons) and the runtime interprets
> it. The Nexus does not perform I/O directly -- it returns
> descriptions of effects. This is the same architecture as TEA, with
> the daemon's staged processing (triage/execute/apply-observe)
> playing the role of the Elm runtime.
>
> This is perhaps the deepest resonance in the entire survey. The
> estate's Signal/Nexus/SEMA separation, viewed through TEA, is:
> Signal = Msg (the vocabulary of what can happen), Nexus = update
> (the pure function from state and message to effects), SEMA = Model
> (the single source of state). The runtime that ties them together is
> the daemon's main loop -- which, like OTP behaviors, should be
> framework-owned rather than hand-written.

---

## 10. Rust Actor Crates

### 10.1 What Is Genuinely New

Most Rust actor crates re-express Erlang/Akka patterns in Rust's
async/await syntax. The genuinely new contributions come from two
Rust-specific sources:

**a) Typed reply channels in the message type.** Kameo
(github.com/tqwewe/kameo) embeds the reply type as an associated type
on the message trait:

```rust
struct Increment { amount: u32 }
impl Message<MyActor> for Increment {
    type Reply = u64; // caller knows the response type
}
```

In Erlang, `gen_server:call` returns any term. In Kameo, the compiler
enforces the reply type. This exploits Rust's associated type system
in a way Erlang and Akka (before typed actors) cannot match.

**b) Ownership enforcing isolation.** Ractor (docs.rs/ractor) makes the
actor's State type owned entirely by the actor task. `ActorRef<A>` is
Clone + Send -- a typed channel endpoint that the borrow checker
prevents from aliasing the actor's internals. Ownership enforces
isolation at the type level with no runtime overhead, replacing
Erlang's process-heap enforcement.

**c) Handler-per-message-type (open extension).** Actix (actix.rs)
separates Actor from Handler<M>. Each message type gets its own
`impl Handler<M>` block with an associated Result type. Adding a new
message type means adding a new impl, not modifying existing code.
This is the inverse of Elm's closed Msg type -- Actix favors
extensibility, Elm favors exhaustiveness.

**d) Polymorphic actor references.** xactor (now unmaintained)
introduced `Caller<T>` -- a type-erased handle to any actor that
handles message type T. Useful for dependency injection.

### 10.2 What Is Not New

Supervision trees (Kameo), gen_server semantics (Ractor), and
backpressure via bounded channels are direct ports from Erlang/Akka
with no novel design ideas.

> **--- Estate analysis ---**
>
> The typed reply channel (Kameo's approach) is directly relevant. The
> estate's signal interface already defines what messages a daemon
> accepts (input section) and what it responds with (output section).
> The estate could go further: the interface file could specify, for
> each input variant, which output variant is its response -- making
> the request-response pairing part of the schema rather than
> convention.
>
> Ownership enforcing isolation (Ractor) is what the estate already
> gets by making each daemon a separate process with its own SEMA
> store. The Rust type system adds a belt to the suspenders: even
> within a daemon's internal actor graph, owned state types prevent
> accidental sharing.
>
> The open-vs-closed message type question (Actix vs. Elm) is
> interesting for the estate. The psyche's interface files define a
> closed set of operations (the input enum). This is the Elm/TEA
> approach -- exhaustive, readable, the compiler checks that every
> variant is handled. The estate should not adopt Actix's open
> extension model, which trades exhaustiveness for extensibility.
> The signal interface is a specification, not an extension point.

---

## Recurring Themes Across All Systems

### Structure carries semantics

In Erlang, fault recovery is encoded in supervisor topology, not
try/catch. In Akka Typed, protocol safety is encoded in type
parameters, not documentation. In Pony, data-race freedom is encoded
in reference capabilities, not locking discipline. In TEA, the Msg
type encodes the complete event vocabulary, not scattered callbacks.
The recurring insight: when a property is structural (enforced by the
system's architecture) rather than conventional (enforced by developer
discipline), it composes and scales.

### The runtime/programmer boundary

TEA, OTP behaviors, and Akka Typed all draw the same line: the
runtime owns the event loop, manages lifecycle, and interprets
effects. The programmer writes pure transformations within a framework-
owned skeleton. The specific name varies (behavior, update function,
command handler) but the pattern is identical: declare what happens,
not how the loop works.

### State ownership as the fundamental invariant

Every beautiful system in this survey enforces single-owner state:
BEAM process heaps, Pony iso/val capabilities, Orleans' single-
threaded grain activation, TEA's single Model, differential
dataflow's per-operator state. The mechanism varies (VM heap
isolation, type system, runtime scheduler, architectural convention)
but the property is the same: one writer, no concurrent mutation,
state changes are visible only through the message/effect protocol.

### Effects as data

TEA makes this explicit (Cmd Msg), but it appears everywhere: Akka
Typed's Effect ADT, Erlang's return-value-driven behavior transitions,
Flink's checkpoint barriers as in-band control messages. Describing
effects as data rather than performing them directly enables
inspection, composition, replay, and testing.

---

## Sources

### Papers and Theses

- Armstrong, Joe. "Making reliable distributed systems in the presence
  of software errors." PhD thesis, Royal Institute of Technology,
  Stockholm, 2003.
  https://erlang.org/download/armstrong_thesis_2003.pdf

- Clebsch, Sylvan et al. "Orca: GC and Type System Co-Design for
  Actor Languages." OOPSLA 2017. http://janvitek.org/pubs/oopsla17a.pdf

- Clebsch, Sylvan. "Ownership and Reference Counting based Garbage
  Collection in the Actor World." OGC paper.
  https://www.ponylang.io/media/papers/OGC.pdf

- Murray, McSherry, Isaacs, Isard, Barham, Abadi. "Naiad: A Timely
  Dataflow System." SOSP 2013.
  https://sigops.org/s/conferences/sosp/2013/papers/p439-murray.pdf

- McSherry, Murray, Isaacs, Isard. "Differential Dataflow." CIDR 2013.
  https://www.cidrdb.org/cidr2013/Papers/CIDR13_Paper111.pdf

- McSherry. "Shared Arrangements: practical inter-query sharing for
  streaming dataflows." VLDB 2020.
  http://www.vldb.org/pvldb/vol13/p1793-mcsherry.pdf

- Bernstein, Bykov, Geller, Kliot, Thelin. "Orleans: Distributed
  Virtual Actors for Programmability and Scalability." MSR-TR-2014-41.
  https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Orleans-MSR-TR-2014-41.pdf

- Carbone, Katsifodimos, Ewen, Markl, Haridi, Tzoumas. "Apache Flink:
  Stream and Batch Processing in a Single Engine." IEEE Data
  Engineering Bulletin, 2015.

- Carbone, Fora, Ewen, Haridi, Tzoumas. "Lightweight Asynchronous
  Snapshots for Distributed Dataflows." arXiv 2015.

### Books

- Armstrong, Virding, Wikstrom, Williams. "Concurrent Programming in
  Erlang." 2nd ed., Prentice Hall, 1996. Part 1:
  https://erlang.org/download/erlang-book-part1.pdf

### Blog Posts and Essays

- Kreps, Jay. "The Log: What Every Software Engineer Should Know About
  Real-Time Data's Unifying Abstraction." LinkedIn Engineering, 2013.
  https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying

- McSherry, Frank. "Differential Dataflow." Blog post, 2015.
  http://www.frankmcsherry.org/differential/dataflow/2015/04/07/differential.html

- McSherry, Frank. "Timely Dataflow reboot." Blog post, 2014.
  http://www.frankmcsherry.org/dataflow/naiad/2014/12/27/Timely-Dataflow.html

### Documentation

- Erlang/OTP Design Principles:
  https://www.erlang.org/doc/system/sup_princ.html
- Pony Tutorial — Reference Capabilities:
  https://tutorial.ponylang.io/reference-capabilities/reference-capabilities.html
- Akka/Pekko Typed documentation:
  https://pekko.apache.org/docs/pekko/current/typed/persistence.html
- Orleans documentation:
  https://learn.microsoft.com/en-us/dotnet/orleans/
- Apache Flink documentation:
  https://nightlies.apache.org/flink/flink-docs-stable/
- Apache Kafka Streams Core Concepts:
  https://kafka.apache.org/streams/core-concepts/
- Elm Guide: https://guide.elm-lang.org/architecture/
- Timely Dataflow Progress Tracking:
  https://timelydataflow.github.io/timely-dataflow/chapter_5/chapter_5_2.html

### Talks

- Clebsch, Sylvan. "Pony, Actors, Causality, Types, and Garbage
  Collection." InfoQ presentation.
  https://www.infoq.com/presentations/pony-types-garbage-collection/

### Rust Crates

- Kameo: https://github.com/tqwewe/kameo
- Ractor: https://docs.rs/ractor
- Actix: https://github.com/actix/actix
- xactor: https://github.com/sunli829/xactor

### Verified Formalization

- "Verified Progress Tracking for Timely Dataflow." ITP 2021.
  https://drops.dagstuhl.de/storage/00lipics/lipics-vol193-itp2021/LIPIcs.ITP.2021.10/LIPIcs.ITP.2021.10.pdf
