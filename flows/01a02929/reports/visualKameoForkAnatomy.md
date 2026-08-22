# The Kameo fork, visually: what changed, why, what it buys, and what it costs

The fork's central idea is simple even though its implementation is not:

> An actor is not *terminated* merely because its mailbox closed or its cleanup hook returned. Termination is a durable fact published only after the actor's state has ceased to exist and its death has been dispatched to linked actors.

That sentence is a reconstruction from the code and tests, not a recorded psyche ruling. The repository does not record the original human or production incident that began the work. It does record enough test-driven history to show the sequence of problems the fork was solving.

## Reading the evidence

```text
● directly recorded     commit subject, code comment, source order, or test assertion
◐ reconstructed         best causal explanation of the witnessed code/tests
? unknown               the record does not establish it
```

The May 16 experimental commits are not one clean Git ancestry: three initial approaches were parallel snapshots, followed by a prototype line, later rebased into the current fork. The visual causal order below comes from timestamps, subjects, source differences, and tests. It must not be mistaken for a commit graph or a transcript of the author's thoughts.

## 1. The whole fork in one picture

```text
? Original trigger is not recorded
        │
        ▼
● mailbox closure does not prove cleanup finished
        │
        ▼
● cleanup-hook completion does not prove actor state was dropped
        │
        ▼
● live actor state can still hold a socket / DB handle / file lock
        │
        ▼
● drop state before shutdown completion and before death notification
        │
        ├──────────────────────────────────────────────┐
        ▼                                              ▼
● publish one typed terminal outcome          ● lifecycle control must progress
  state absence + terminal reason               even if ordinary mailbox is full
        │                                              │
        ▼                                              ▼
● wait_for_shutdown becomes a barrier          ● split control/message lanes
  rather than a mailbox side effect              + admission generation
        │                                              │
        └──────────────────────┬───────────────────────┘
                               ▼
                    ● linked actors and supervisors
                      see death only after state drop
                               │
                               ▼
                    ◐ replacement can safely bind the
                      old actor's released resources
```

The fork is therefore best understood as two interlocking correctness systems:

1. **Terminal truth:** define exactly what a shutdown observation proves.
2. **Control progress:** ensure the transition to that terminal truth cannot be trapped behind ordinary work.

## 2. What existed before the fork

At the common ancestor, actor shutdown looked approximately like this:

```text
ONE SIGNAL CHANNEL

 ordinary message ─┐
 Stop ─────────────┼──> [ bounded/unbounded FIFO mailbox ] ──> actor loop
 LinkDied ─────────┘

ACTOR LIFECYCLE

loop ends
   │
   ├─ shut down/wait for children
   ├─ spawn link notification in a detached Tokio task
   ├─ run on_stop(actor)
   ├─ unregister + set shutdown result
   └─ return (actor state A, stop reason)

wait_for_shutdown()
   └─ waits for mailbox receiver closure and returns ()
```

This shape left several meanings collapsed together:

```text
mailbox closed  ?=  on_stop finished  ?=  actor state gone  ?=  resource free
```

They are not equivalent. The preserved tests demonstrate the differences by delaying `on_stop`, delaying `Drop`, holding a TCP listener, and trying to bind the same address again.

## 3. The design sequence: six moves

### Move 1 — wait for cleanup, not mailbox closure

```text
BEFORE                              FIRST EXPERIMENT

wait_for_shutdown                   wait_for_shutdown
      │                                   │
      ▼                                   ▼
mailbox closed                      shutdown_result published
      │                                   │
      ▼                                   ▼
returns ()                           on_stop has completed
```

● The commit subject says `make shutdown wait for hook result`. A new test proves that a delayed `on_stop` finishes before the wait returns.

● The same test explicitly warns that this is only **hook-complete**, not **actor-state-drop**. A TCP rebind still fails after the wait because the actor value remains alive.

What it gives: the caller no longer mistakes channel closure for cleanup-hook completion.

What it does not give: proof that Rust has dropped the actor state or released resources held in its fields.

### Move 2 — destroy actor state before completion or notification

```text
on_stop finishes
      │
      ▼
drop(actor A) ──> socket / DB handle / file lock is released
      │
      ▼
notify links and publish completion
```

● The parallel experiment changes `run`, `spawn`, and `spawn_in_thread` so they no longer return actor state `A`. The lifecycle owns and explicitly drops it.

● Its test requires both a `Drop` witness and successful TCP rebind before `wait_for_shutdown` returns.

◐ The causal reason is resource ownership: a supervisor starting a replacement must not observe death while the old actor still owns a singleton resource.

Cost: callers lose the ability to recover the actor value after the task ends. That is an API break and an ownership decision, not merely internal cleanup.

### Move 3 — publish terminal truth as data

An intermediate experiment introduced pushed lifecycle phases so observers would stop inferring lifecycle from channel side effects. The current fork compresses that into one terminal value:

```text
ActorTerminalOutcome
├── state: ActorStateAbsence
│   ├── Dropped          state existed and is now destroyed
│   ├── NeverAllocated   startup never produced actor state
│   └── Ejected          public, but no producing path was found
└── reason: ActorTerminalReason
    ├── Stopped / SupervisorRestart / Killed
    ├── Panicked / LinkDied
    ├── CleanupFailed / StartupFailed
    └── PeerDisconnected (feature-gated)
```

● All references share a `SetOnce<ActorTerminalOutcome>`. `wait_for_shutdown()` returns the value. `is_terminated()` means the cell is published.

● Startup failure becomes `NeverAllocated/StartupFailed`; cleanup failure becomes `Dropped/CleanupFailed`.

What it gives:

- one durable terminal fact shared by all references;
- a distinction between **not accepting new work** and **fully terminated**;
- supervision decisions that can see cleanup/startup failure rather than only a legacy stop reason;
- an observable resource-release claim through `Dropped`.

Costs:

- a new public type system carried through refs, links, supervision, and remote paths;
- duplicate semantics remain because the compatibility shutdown result and legacy stop reason are also kept;
- `Ejected` is public but unwitnessed, suggesting unfinished taxonomy;
- terminal publication itself can fail to happen if an uncovered teardown path escapes.

### Move 4 — separate ordinary traffic from lifecycle control

The ancestor's single mailbox allowed a bounded queue to make lifecycle control compete with ordinary traffic.

```text
ONE-LANE SHAPE

[msg][msg][msg][msg][ FULL ]  <── Stop or LinkDied must join this system

FORK TWO-LANE SHAPE

ordinary bounded lane: [msg g7][msg g7][msg g7] ─┐
                                                  ├─ biased receiver ─> actor
control unbounded lane: [Stop][LinkDied] ─────────┘  control checked first
```

● Tests fill or block the ordinary mailbox and prove that Stop and LinkDied still progress.

What it gives: control signals are not backpressured by ordinary user-message capacity.

Costs:

- a second channel and more complex send/receive/poll/close bookkeeping;
- an unbounded lane trades deadlock/backpressure risk for possible memory growth;
- biased control can starve ordinary work during a sustained control flood;
- awaited remote/link dispatch can lengthen the shutdown critical path.

### Move 5 — give ordinary work an incarnation

Splitting the lanes creates a new question: what happens to ordinary sends racing with shutdown, or queued work reused by a restarted actor?

```text
actor incarnation 7

sender reads generation 7 ── waits for bounded capacity ──┐
                                                         │
Stop wins: admission=false; generation becomes 8         │
                                                         ▼
sender rechecks after reserving capacity ──> reject; it may not cross boundary

queued [message generation 7] seen by incarnation 8 ──> stale ──> discard
```

● Ordinary sends check admission and generation before enqueue. Bounded async sends check again after obtaining capacity.

● When shutdown begins, admission closes and the generation increments. Receiver paths discard old-generation messages.

● The in-flight handler may finish; queued ordinary work loses to Stop. A queued ask's dropped reply sender makes the caller observe `ActorStopped`.

What it gives:

- a clean boundary between actor incarnations;
- no send that waited on capacity can appear to succeed after shutdown won;
- a restarted actor cannot accidentally execute ordinary work admitted to its predecessor.

Cost: queued tells are lost, and the fork has no `on_undelivered` accounting hook. Restart does not preserve ordinary work. Removing stale entries costs O(number of stale entries).

### Move 6 — do not leak a weaker completion fact early

The fork retained the older compatibility shutdown result. Without another gate, weak references could observe that result before terminal publication.

```text
on_stop ── actor Drop ── notify ── compatibility result ── terminal cell
                                      ▲
                                      └─ hidden until is_terminated == true
```

● Weak shutdown-result helpers return `None` until the lifecycle cell is set, closing the small ordering window between compatibility-result publication and terminal publication.

What it gives: old helpers cannot contradict the stronger terminal meaning.

Cost: two completion systems must be ordered and kept coherent. Under the current Spirit rule against compatibility shadows, the eventual design should choose one authoritative semantic contract and update consumers rather than preserve two indefinitely.

## 4. The fork's complete shutdown sequence

```text
TIME ↓

Caller / sender      Ordinary lane       Control lane      Actor lifecycle       Links / supervisor
────────────────────────────────────────────────────────────────────────────────────────────────────
send ordinary ─────> enqueue(gen=7)
stop_gracefully ─────────────────────────> Stop
                                          Stop wins ──────> loop exits
send racing ───────> waits/reserves                         admission=false
                                                             generation=8
recheck gen=7 ─────> REJECT
                                                             wait for children
                                                             run on_stop
                                                             construct outcome
                                                             drop(actor state) ── resource released
                                                             await notify ───────> receive reason+outcome
                                                                                  decide restart
                                                             unregister
                                                             publish compat result
                                                             SetOnce(outcome)
wait_for_shutdown <────────────────────────────────────────── returns outcome
```

Two subtleties matter:

1. Awaiting link dispatch means the send was accepted or failed; it does **not** mean the linked actor finished its `on_link_died` hook.
2. A supervisor may start the replacement after receiving the post-drop notification but before the source actor publishes its own lifecycle cell. The tests prove old-state drop before replacement start, not lifecycle-cell publication before replacement.

## 5. What upstream added after the fork

Upstream did not reproduce the fork. It strengthened other parts of the same lifecycle territory.

```text
FORK-ONLY CORE                 SHARED CONCERN                UPSTREAM-ONLY EVOLUTION
─────────────────             ──────────────                ───────────────────────
typed state absence           reject new work after Stop    preserve tells on restart
post-drop terminal barrier    lifecycle result/waiters       bounce asks with original msg
separate control lane         supervision and restart        on_undelivered terminal tells
generation recheck            lifecycle/deadlock fixes       restart strategies + budgets
drop before notify            panic/error handling           per-actor ask timeout
outcome-bearing links         actor observability            pipe / FutureActor / console
                              remote actors                   single-Arc ActorRef + tracing
```

### Connection map

```text
≈ partial overlap    + complementary    × conflicting semantics    ○ largely orthogonal
```

| Fork concern | Upstream since fork | Relation | Why |
|---|---|---:|---|
| Close ordinary admission at Stop | `accepting` flag | ≈ | Same uncontended rejection goal; upstream retains one lane and lacks the post-capacity generation recheck. |
| Terminal observation | startup/shutdown result cells and waits | ≈ | Both expose results; upstream does not prove state absence or post-notification completion. |
| Control progress under full mailbox | no separate control lane | × | Upstream control still shares FIFO/capacity with ordinary work. |
| Queued work after graceful Stop | processes already queued work | × | Fork lets Stop win and discards queued ordinary work. |
| Restart message fate | preserves tells; asks get `ActorRestarting` | × / + | It conflicts with fork discard, but supplies valuable delivery accounting the fork lacks. |
| Terminal undelivered tells | `on_undelivered` | × / + | Fork silently discards; upstream makes the loss observable. The concept can complement a redesigned policy. |
| Resource release before notification | still returns actor `A`; notification is spawned before final drop | × | Upstream does not establish the fork's happens-before boundary. |
| Link/supervision reason | richer restart tracking and strategies | + / ≈ | Stronger policy machinery, but no state-absence outcome and different ownership order. |
| Panic-safe teardown | catches shutdown-hook panics | + | Upstream closes a likely fork failure hole. |
| Deadlock fixes, error chains, tracing | released | + | Improve correctness/diagnosis without replacing the fork's terminal contract. |
| Console, `pipe`, reply timeouts, `FutureActor`, cheaper refs | released | ○ / + | Ecosystem and ergonomics, not lifecycle equivalence. |
| Remote redesign, serialized restart, terminal child ownership | open PRs | dashed future | Direction only; not released or current `main` behavior. |

### The sharpest semantic conflict: queued work

```text
FORK: CONTROL PRIORITY                     UPSTREAM: WORK ACCOUNTABILITY

current handler may finish                 queued-before-Stop messages run
Stop wins over queued work                 restart tells are preserved
old-generation tells disappear             asks return retryable classifications
queued ask -> ActorStopped                  terminal tells -> on_undelivered

Goal: incarnation isolation                Goal: do not lose or obscure accepted work
```

Both goals are legitimate. Neither code line proves which goal our Nexus actors require. A terminal design could make queue fate an explicit policy rather than an accidental consequence of mailbox machinery.

## 6. What the fork gives us

```text
GUARANTEE                              PRACTICAL VALUE
───────────────────────────────────    ─────────────────────────────────────────
accepting != terminated                callers can distinguish draining from death
Dropped is an observable fact          resource reuse/rebind has a synchronization point
control bypasses ordinary capacity     shutdown/link death cannot be trapped by user load
messages belong to an incarnation      restarted state cannot consume predecessor work
drop happens before death dispatch     supervisor replacement sees old state already gone
startup/cleanup failure are terminal   supervision can classify lifecycle failure directly
one SetOnce outcome per actor          all references converge on one durable fact
```

The deepest gain is a **happens-before contract**:

```text
old actor state destroyed
          happens before
death notification is dispatched
          happens before
terminal outcome is returned to waiters
```

That contract is valuable wherever actor state owns exclusive resources or where supervisor replacement must not overlap the old incarnation.

## 7. What the fork costs us

### Semantic costs

- Accepted queued work is discarded on Stop/restart rather than preserved or reported through a tell hook.
- The policy is encoded in generation mechanics instead of named as a domain policy.
- `Ejected` exists without an observed runtime meaning.
- Compatibility result, legacy reason, and terminal outcome duplicate parts of the same truth.

### Correctness risks

- Source inspection indicates `on_stop` is awaited without the outer panic-catching path used upstream. A panic may prevent result/outcome publication. No fork test covers it.
- The control lane is unbounded and can grow under a control flood.
- Biased control selection can starve ordinary work.
- Awaited link dispatch adds link/remote latency to teardown while still not waiting for target hook completion.
- Fork tests do not directly prove tell behavior across successful supervisor restart, remote timing, sustained control load, or lifecycle-cell publication before replacement.

### API and implementation costs

- Breaking changes to `wait_for_shutdown`, `on_link_died`, spawn/run return types, link messages, and supervision decisions.
- Two channels, extra atomics, generation-tagged messages, post-reservation checks, stale-message scanning, and combined close/length/poll bookkeeping.
- More per-field `Arc` cloning than current upstream's consolidated `ActorRef` representation.
- Remote serialization and every actor-library rebase must carry the custom outcome types and ordering.

### Estate costs

- The fork manifest is still `0.20.0`; upstream has released through `0.22.2`.
- We have not received upstream's message-accounting, teardown-panic, tracing, console, timeout, and ergonomics work.
- Consumers use mutable branches, fixed commits, a deleted feature branch, and—in Lojix—both registry and fork Kameo.
- Most production code ignores the richer outcome, so the semantic dependency is implicit and difficult to inventory from API usage alone.

## 8. Alignment with how we currently design software

The written psyche settles Kameo as the Nexus actor layer and explicitly leaves its standards undesigned. It also says to distrust all prior actor work, including the fork. Alignment here is therefore a comparison with current general design principles, not approval.

### Strong conceptual alignment

```text
CURRENT DESIGN VALUE                  FORK QUALITY
──────────────────────────────────    ──────────────────────────────────────────
correctness as explicit machinery     terminal cell turns timing into a value
types as comprehension surface        state absence + reason are named types
observable external evidence          Drop, TCP rebind, channel witnesses
resource ownership made causal        release-before-notify is explicit
failure states not hidden             startup/cleanup failure are classified
```

The terminal outcome is the clearest alignment: it moves knowledge from incidental async behavior into a main type that an agent or human can reason about.

### Structural tension or clash

```text
CURRENT DESIGN VALUE                  CURRENT FORK SHAPE
──────────────────────────────────    ──────────────────────────────────────────
ontology and traits before bodies     implementation experiments came first
every method under a trait            many ActorRef operations are inherent methods
one authoritative current shape       legacy result/reason coexist with new outcome
policy named separately from mechanism queue-discard policy is embedded in generations
Nexus uses typed Signal/socket edges  Kameo remote is its own actor transport model
tests await the tested event           several race witnesses use sleeps/timeouts
living guidance governs standards      fork predates the present actor-design discussion
```

The fork contains useful concepts, but not yet the actor ontology. Its types answer **what happened at termination**; they do not define the whole map of actor capabilities, message fate, supervision, resource ownership, or the boundary between local actor calls and Nexus Signal edges.

### The trait/type map the evidence points toward

This is a comprehension map, not proposed exact Rust names:

```text
Actor lifecycle ontology
├── Admission
│   ├── accepting / closed
│   └── fate of sends already waiting for capacity
├── Incarnation
│   ├── identity of queued work
│   └── whether work crosses restart
├── Termination
│   ├── state absence
│   ├── reason
│   └── observation barrier
├── Queue-fate policy
│   ├── finish queued work
│   ├── preserve across restart
│   ├── reject and return payload
│   └── deliver to an undelivered hook
├── Supervision
│   ├── restart classification and budget
│   └── replacement ownership ordering
└── Notification
    ├── what is sent
    └── dispatch accepted vs hook completed
```

Seen this way, the fork and upstream each supply pieces:

```text
fork:     strong Termination + Incarnation boundary + Notification ordering
upstream: strong Queue-fate accounting + Supervision policy + teardown resilience
missing:  psyche-designed ontology and explicit Nexus standards of use
```

## 9. A possible synthesis—not a ruling

The evidence suggests a cleaner conceptual end-shape than either implementation currently has:

```text
Stop requested
      │
      ▼
close admission and establish incarnation boundary
      │
      ▼
apply an explicit queue-fate policy
  [finish | preserve-for-restart | reject-with-payload | undelivered-hook]
      │
      ▼
run cleanup with panic/error capture
      │
      ▼
destroy actor state and release resources
      │
      ▼
dispatch outcome-bearing death notification
      │
      ▼
publish one authoritative terminal outcome
```

This preserves the fork's strongest semantic contribution without automatically preserving its two-channel/generation implementation or its silent-discard policy. It also admits upstream's message-accounting and teardown improvements. Whether this is wanted belongs to the living; it is not established by the code.

## 10. What remains genuinely unknown

- The production incident or human observation that caused the May 16 experiments.
- Whether every mechanism was intended as one contract or accumulated during rapid experimentation.
- Whether deployed workloads require mailbox-saturation control bypass or post-drop notification ordering.
- The intended meaning of `Ejected`.
- Whether queued work should survive restart in our actor model.
- Whether notification dispatch, target-hook completion, or terminal publication is the actual supervisor synchronization boundary.
- Where the internal Kameo message model stops and the Nexus typed-binary Signal/socket boundary begins.

Typed transcript search was attempted under the transcript-search discipline, but the `transcript` command is unavailable in this workspace. No transcript-derived origin claim is made.

## Sources

- `flows/fd301d9a/reports/forkOriginHistory.md`
- `flows/fd301d9a/witnesses/forkOriginHistory.md`
- `flows/fb50d4a5/reports/kameoRuntimeAnatomy.md`
- `flows/fb50d4a5/witnesses/runtimeAnatomy.md`
- `flows/fb50d4a5/witnesses/lifecycleTests.md`
- `flows/cc4105a6/reports/alignmentMap.md`
- `flows/cc4105a6/witnesses/alignmentMap.md`
- `flows/01a02929/reports/kameoForkAndUpstream.md`
- `psyche-raw/Vision/actorLibrary.md`
- `psyche-raw/Vision/nexus.md`
- `psyche-raw/Vision/rustComponentArchitecture.md`
- `psyche-raw/Intent/mandatoryTraits.md`
- `psyche-raw/Vision/testTravesties.md`
- https://github.com/LiGoldragon/kameo/commit/1325f6aef7e13996f929d17447ddd2abaa514444
- https://github.com/LiGoldragon/kameo/commit/da0f64af20a4f3002a79a1a5aa2efae416eadfd6
- https://github.com/LiGoldragon/kameo/commit/1980e34b5e694b4eb268f24d75fcfa8e527d1472
- https://github.com/LiGoldragon/kameo/commit/8ea1e3fab5350ddd86b1bfd18dd3cbd4a0002164
- https://github.com/LiGoldragon/kameo/blob/3486e4f63ea4e87123476cfbdefeb12403540306/tests/lifecycle_phases.rs
- https://github.com/tqwewe/kameo/releases/tag/v0.22.2
- https://github.com/tqwewe/kameo/blob/main/CHANGELOG.md
- https://github.com/tqwewe/kameo/blob/main/src/actor/spawn.rs
- https://github.com/tqwewe/kameo/blob/main/src/mailbox.rs
- https://github.com/tqwewe/kameo/blob/main/src/links.rs
