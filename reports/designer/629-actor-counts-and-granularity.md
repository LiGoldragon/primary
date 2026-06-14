# How many actors do real actor systems run — and are we overreaching?

Grounded research for the daemon-engine-actor design question. Context:
each daemon runs ~3 "engine" actors (Signal / Nexus / SEMA planes) on
`kameo` (tokio-based), across dozens of daemons — low hundreds of actors
total today, with possible future per-entity or per-request actors. The
architect asks "am I overreaching for actors?" The grounded answer is the
opposite: **low hundreds of actors is deeply conservative — two to four
orders of magnitude below where any mainstream actor runtime starts to
strain.** The real design axis is not "too many actors?" but "is each
actor boundary buying isolation / serialization / supervision, or is it a
synchronous function wearing a mailbox?"

## 1. Scale in the major actor systems — real numbers, real cost model

The headline finding: every production actor runtime is engineered so the
*runtime cost* of an actor is negligible (hundreds of bytes), and real
systems run them in the **millions per node**. Actor count is essentially
never the binding constraint; memory of actor *state* and message
*throughput* are.

### Erlang / OTP & Elixir / BEAM — process-per-activity

- **Default ceiling: 1,048,576 processes per node** (the `+P` flag
  default), raisable to **268,435,456**. This is a soft system limit, not
  a practical wall — nodes routinely run hundreds of thousands of
  processes well under it.
  ([erlang.org system limits](https://www.erlang.org/doc/system/system_limits))
- **~300 bytes per process** at spawn (a few words of heap); processes are
  measured in bytes-to-kilobytes, not the 512 KB–1 MB stack an OS thread
  costs. This is what makes process-per-concurrent-activity the *default*
  idiom: one process per connection, per request, per session, per
  transient task — you don't ration them.
  ([BEAM memory model](https://medium.com/@kanishks772/memory-management-in-beam-why-erlang-never-runs-out-b35087af3612))
- **WhatsApp** is the canonical scale proof, with an important nuance:
  they *demonstrated* ~2 million TCP connections on a single server, but
  then **deliberately ran at ~1 million connections/server to keep
  headroom** — i.e., the limit was operational margin, not the runtime.
  At the cluster level: ~150 chat servers (~1M phones each), **147M peak
  concurrent connections**, **>70M Erlang messages/sec**, >11,000 cores.
  Each connection (and more) is its own process.
  ([High Scalability — WhatsApp](https://highscalability.com/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an/))

The BEAM philosophy is the strong form of "actor per X": spawn a process
for *anything* that has independent lifecycle or can fail independently,
because the cost of doing so rounds to zero.

### Akka (JVM) — and a correction on the "50 million" claim

- **~300 bytes overhead per actor instance**, stated in Akka's own
  `actor-systems` documentation. This yields the widely-quoted
  **~2.5 million actors per GB of heap**.
  ([Akka actor-systems docs](https://doc.akka.io/libraries/akka-core/current//general/actor-systems.html),
  [Bernhardt — Akka anti-patterns: too many actors](https://manuel.bernhardt.io/2018/08/06/akka-anti-patterns-many-actors))
- **Correction for the brief:** the "**50 million**" figure the architect
  recalled is **50 million *messages per second*** on commodity hardware,
  **not** 50 million actors per GB. The per-GB *actor-density* number is
  ~2.5M. The two numbers describe different axes (memory density vs
  message throughput) and shouldn't be conflated.
  ([Lightbend "High Performance Akka" slides, QCon London](https://qconlondon.com/ln2018/system/files/presentation-slides/high-performance-akka.pdf))
- Akka's documented design philosophy is **actor-per-entity at scale**:
  one actor per user / order / session / device, with **Cluster Sharding**
  distributing entity actors across machines. Practitioners run systems
  with **millions of long-lived entity actors** routinely.
  ([Polgar — "5,000,000 Akka actors"](https://medium.com/@TamasPolgar/what-to-do-with-5-000-000-akka-actors-381a915a0f78))

### Microsoft Orleans — virtual actors ("grains"), actor-per-entity by design

- Orleans is explicitly built for "**hundreds, millions, billions, and
  even trillions of loosely coupled entities**" — its docs note it "can
  easily create a grain for every person on Earth in a small cluster, so
  long as a subset of that total number is active at any point in time."
  ([Orleans best practices](https://learn.microsoft.com/en-us/dotnet/orleans/resources/best-practices))
- The trick that makes trillions tractable is the **virtual actor**
  abstraction: a grain *always exists logically* but is **activated on
  demand and deactivated when idle**. The runtime manages only the
  *active working set* in memory; the rest is addressable but dormant.
  This decouples logical entity count from physical actor count — the
  count you "design for" can be astronomically larger than what's resident.
- Born in **Xbox Live** to manage state for millions of concurrent
  gamers; reported up to **4.5M messages/sec** with a hosted client.
- Orleans' own granularity guidance (directly relevant to us, §2):
  "**Optimal throughput is achieved by using multiple smaller grains
  rather than a few larger grains**," but the boundary should follow "the
  application *domain model* — Users, Orders, etc." It also warns against
  the opposite failure: **avoid chatty grains** ("direct memory use is
  significantly less expensive than message passing"; "highly chatty
  grains may be better combined as a single grain") and **avoid
  bottleneck grains** (a single coordinator/registry/monitor).

### Pony and CAF (C++) — the same story in compiled languages

- **Pony:** ~**240–256 bytes** of overhead for an empty actor on 64-bit;
  the runtime is designed so actor count "can go into the **millions**."
  An idle actor "consumes no resources other than the few extra bytes of
  memory." ([Pony runtime FAQ](https://www.ponylang.io/faq/runtime/))
- **CAF (C++ Actor Framework):** "scales up to **millions of actors** on
  many dozens of processors"; spawning "thousands or even millions of
  actors is feasible." ([actor-framework.org](https://www.actor-framework.org/))

**Cross-system convergence:** every mainstream actor runtime puts
per-actor overhead in the **~240–400 byte** band and demonstrates
**millions of actors per node / per GB**. The number "low hundreds" does
not appear anywhere as a concern — it's the rounding error.

## 2. Granularity philosophy — actor-per-WHAT?

The literature is consistent: **actor boundaries should track units of
independent state, failure, or serialization — not units of computation.**

**When actor-per-X is right** (the affirmative case):

- **Single-writer serialization.** An actor processes its mailbox
  one message at a time, single-threaded. That makes it a *natural mutex*
  over its own state — the right tool whenever a piece of mutable state
  needs serialized access without explicit locks. (The single-writer
  pattern is exactly why log/disk writers, registries, and per-entity
  state are modeled as actors.)
  ([ActorDB / single-writer actors](https://arxiv.org/html/2509.25285))
- **Isolation & independent failure.** "The failure of one actor doesn't
  directly impact others." If X can fail, restart, or be supervised
  independently, X wants to be an actor. This is the supervision argument:
  hierarchical restart/stop/escalate only works if the failure unit *is*
  an actor.
- **Per-entity state with independent lifecycle.** One actor per user /
  session / device / order — the Akka and Orleans default. Each entity
  gets serialized access to its own state and an independent lifecycle.
- **Asynchronous boundaries** — calls to external systems or blocking
  operations. Bernhardt's explicit guidance: focus actors on "**calls to
  external systems**" and "**calls to blocking operations**," the things
  that genuinely need async handling.

**When actor-per-X is wrong** (the negative case — the actual
"overreach"):

- **A pure synchronous function does not need to be an actor.** Wrapping
  CPU-bound, stateless, synchronous work in a mailbox buys nothing and
  costs scheduling + message-passing overhead. Bernhardt's worked example:
  having millions of actors each parse an XML document on a 4-core CPU is
  *slower* than 4 actors, because you've added mailbox/scheduling overhead
  to work that was never concurrency-limited. His conclusion: "**it isn't
  because you have many actors that things will necessarily be faster**…
  actor counts should match use-case requirements, not actor model
  capabilities."
- **Over-fine granularity adds real overhead.** The general trade-off
  (GeeksforGeeks, ElasticActor research): too *fine* → high message-passing
  and scheduling overhead, complex actor management; too *coarse* →
  contention and bottlenecks. The overhead per *message hop* and per
  *schedule* is non-trivial even when per-actor *memory* is tiny.
  ([Actor granularity trade-off](https://www.geeksforgeeks.org/system-design/actor-model-in-distributed-systems/),
  [ElasticActor — automatic granularity](https://pacman.cs.tsinghua.edu.cn/npc2018/papers/ElasticActor.pdf))
- **Chatty actors that mostly talk to each other** should often be merged
  (Orleans guidance above) — the message hops between them cost more than
  the in-process call you replaced.

The synthesis of the philosophy: **the cost that matters is not the actor,
it's the message and the schedule.** Actors are cheap to *have*; the
discipline is about not routing synchronous, hot, chatty work through
mailboxes that don't need to serialize or isolate.

## 3. kameo and the Rust actor ecosystem — cost model and ceilings

### Rust actors sit between BEAM and OS threads

Rust actors are heavier than BEAM processes (no per-actor GC'd heap, but a
full tokio task + channel) and far lighter than OS threads. The cost model
is concrete and composable from tokio primitives:

- **Each kameo actor = one tokio task + one mpsc mailbox.** The author
  confirms (Show HN) that "**each actor runs as a separate Tokio task**"
  and multiple actors multiplex onto tokio's worker threads (no
  thread-per-actor). ([kameo Show HN](https://news.ycombinator.com/item?id=41723569),
  [kameo on GitHub](https://github.com/tqwewe/kameo))
- **tokio task overhead: ~64 bytes** and a single allocation per task;
  per-task scheduling overhead on the order of **~10 ns**. Spawning and
  destroying large numbers of tasks is explicitly "quite cheap."
  ([tokio task docs](https://docs.rs/tokio/latest/tokio/task/),
  [Tokio scheduler internals](https://tokio.rs/blog/2019-10-scheduler))
- So a kameo actor's *fixed* cost is roughly **the task (~64 B) + the mpsc
  channel + the actor's own state**. The dominant term in practice is the
  actor's own state, not the framework overhead. This puts the realistic
  fixed overhead in the low-hundreds-of-bytes-plus-state range — same
  order as Akka/Pony.

### Realistic ceilings for Rust actor frameworks

There is **no published hard ceiling**; the constraint is task-scheduler
throughput and the memory of actor *state*, exactly as in the other
runtimes. Tokio comfortably runs **hundreds of thousands to millions of
tasks** (it's the standard runtime behind high-connection-count Rust
servers), so a kameo system is bounded the same way. Concretely:

- **Thousands of actors:** trivial, no measurement needed.
- **Tens to hundreds of thousands:** routine for tokio-based systems;
  the binding constraint becomes per-actor *state* memory and message
  rate, not actor count.
- **Millions:** reachable but now you're explicitly budgeting state memory
  and scheduler load — the regime where you'd want the Orleans-style
  activate-on-demand trick rather than keeping all actors resident.

### Ecosystem and maturity (kameo and peers)

- **kameo:** tokio-based; built-in **distribution** (over libp2p),
  **supervision**, bounded/unbounded mailboxes, backpressure. Pre-1.0 but
  actively developed — **v0.20.0 (April 2026)**, ~1.3k GitHub stars, 22
  releases. The author has a deliberate BEAM-influenced design and chose
  Rust for the type system and WASM potential.
  ([kameo on crates.io](https://crates.io/crates/kameo),
  [Seyhun — comparing Rust actor libraries](https://tqwewe.com/blog/comparing-rust-actor-libraries/))
- **Peer cost models (all tokio-task + channel, same order of magnitude):**
  - **Actix** — fastest messaging and fastest actor spawn in Seyhun's
    comparison; mature, large ecosystem (actix-web); local-only by default,
    distribution via external crates.
  - **Ractor** — Erlang/OTP-inspired, built-in distribution; similar
    messaging perf to kameo/Coerce.
  - **Coerce** — built-in distribution + sharding; highest spawn time in
    the comparison.
  - **xtra** — minimal, **local-only**, no distribution.
  - Seyhun's comparison is **qualitative** (relative graphs, LOC), not
    absolute throughput; kameo, Coerce, and Ractor cluster together on
    messaging, Actix leads. No framework publishes a per-actor-byte or
    max-actor figure — reinforcing that count is not where Rust actor
    projects feel pressure.

**Notably, neither kameo's docs nor its author publish granularity
guidance or actor-count targets.** That absence is itself a signal: the
framework treats actor count as a non-issue and leaves boundary choice to
the application — consistent with §2.

## 4. Synthesis — the actual answer

**Low hundreds of actors is conservative, not overreaching — by two to
four orders of magnitude.** Every runtime surveyed (BEAM, Akka, Orleans,
Pony, CAF) is engineered to make actors cost ~240–400 bytes and to run
**millions per node**; kameo inherits tokio's ~64-byte-task model and the
same millions-of-tasks ceiling. A system running ~3 engine actors × dozens
of daemons is using **roughly 0.01–0.1% of the comfortable single-node
actor budget**. There is no scale-of-count risk here whatsoever.

**The question to retire and the question to keep.** "Am I overreaching
*for actors*?" is the wrong axis — the count is a rounding error. The right
axis is **per-actor: does this boundary buy isolation, single-writer
serialization, independent failure/supervision, or per-entity lifecycle?**
That's a per-boundary judgment, applied the same way at 3 actors or 3
million.

**Where the current 3-engine-actors-per-daemon design is clearly fine —
arguably under-using:**

- Three planes (Signal / Nexus / SEMA) are exactly the kind of boundary
  actors are *for*: distinct responsibilities, each wanting serialized
  access to its own plane state and independent supervision. This is the
  textbook "push each responsibility into a child" pattern from Akka's own
  docs. If anything, the survey suggests the design is **leaving actor
  affordances on the table** — supervision, per-plane backpressure, and
  failure isolation are cheap here and worth leaning into.

**Where future per-entity / per-request actors are clearly fine:**

- **Per-entity actors** (one per durable entity with independent state and
  lifecycle) are the *mainstream* pattern — it's literally what Akka
  Cluster Sharding and Orleans grains exist to do, at millions. If
  entities have independent state + lifecycle + failure, actor-per-entity
  is the well-trodden right call, not an overreach. The only caveat is the
  **resident working set**: if logical entities vastly exceed the active
  set, adopt the Orleans pattern (activate-on-demand / deactivate-on-idle)
  rather than keeping every entity actor resident.
- **Per-request actors** are right when a request has genuinely
  independent, isolatable lifecycle/failure (BEAM does process-per-request
  by default). They're the *wrong* call when the "request handler" is
  really a synchronous, stateless function — then it's a function wearing
  a mailbox (§2), and you've added a schedule + message hop for nothing.

**Where actor-per-X would genuinely overreach in *this* system:**

- **Wrapping synchronous, stateless, CPU-bound steps** inside the engine
  planes as their own actors — Bernhardt's XML-parser anti-pattern. If a
  step doesn't serialize state, isolate failure, or cross an async/blocking
  boundary, it should be a *method call inside* the owning actor, not a
  new actor. (This dovetails with the workspace's own Rust discipline:
  logic lives as a method on the owning data-bearing type — an actor is a
  heavier commitment than a method and should clear a higher bar.)
- **Fine-graining a hot, chatty internal path** into many small actors
  that mostly message each other — Orleans' "chatty grains" warning. The
  message hops cost more than the in-process calls they replace.
- **A per-X actor that's actually a bottleneck coordinator** routed
  through by everything — Orleans' "bottleneck grain." That's a contention
  point dressed as concurrency.

**The one-line frame for the architect:** you are not overreaching on
*count* — you have headroom for ~10,000–100,000× more actors before count
matters. Spend your design attention on *boundaries*: make an actor wherever
you want serialized state, isolation, supervision, or per-entity lifecycle
(lean *into* this — you're likely under-using it), and keep synchronous,
stateless, hot, or chatty work as methods inside the owning actor. The cost
you're managing is messages and schedules, not actors.

## Sources

- Erlang system limits (process ceiling 1,048,576 default → 268,435,456):
  https://www.erlang.org/doc/system/system_limits
- BEAM memory model (~300 B/process):
  https://medium.com/@kanishks772/memory-management-in-beam-why-erlang-never-runs-out-b35087af3612
- High Scalability — WhatsApp (2M demonstrated, ran ~1M/server for headroom; 147M peak conns, >70M msg/s, >11,000 cores):
  https://highscalability.com/how-whatsapp-grew-to-nearly-500-million-users-11000-cores-an/
- Akka actor-systems docs (~300 B/actor; "split tasks until small enough"; push responsibilities into children):
  https://doc.akka.io/libraries/akka-core/current//general/actor-systems.html
- Bernhardt — Akka anti-patterns: too many actors (2.5M/GB; XML-parser anti-pattern; focus on external/blocking calls):
  https://manuel.bernhardt.io/2018/08/06/akka-anti-patterns-many-actors
- Lightbend "High Performance Akka," QCon London (50M *messages*/sec — the figure to not conflate with actor density):
  https://qconlondon.com/ln2018/system/files/presentation-slides/high-performance-akka.pdf
- Polgar — millions of Akka actors in practice:
  https://medium.com/@TamasPolgar/what-to-do-with-5-000-000-akka-actors-381a915a0f78
- Orleans best practices (trillions of entities; smaller grains for throughput; avoid chatty/bottleneck grains; domain-model boundaries):
  https://learn.microsoft.com/en-us/dotnet/orleans/resources/best-practices
- Orleans Virtual Actors (Microsoft Research — activate-on-demand model):
  https://www.microsoft.com/en-us/research/project/orleans-virtual-actors/
- Pony runtime FAQ (~240–256 B/actor; millions of actors; idle actors near-free):
  https://www.ponylang.io/faq/runtime/
- CAF — C++ Actor Framework (millions of actors):
  https://www.actor-framework.org/
- kameo — GitHub (each actor = tokio task; supervision; libp2p distribution):
  https://github.com/tqwewe/kameo
- kameo — crates.io (v0.20.0, April 2026):
  https://crates.io/crates/kameo
- kameo — Show HN (author on tokio-task model, BEAM influence):
  https://news.ycombinator.com/item?id=41723569
- Seyhun — comparing Rust actor libraries (Actix/Coerce/kameo/Ractor/xtra; qualitative perf, distribution features):
  https://tqwewe.com/blog/comparing-rust-actor-libraries/
- tokio task docs (~64 B/task, single allocation, cheap spawn):
  https://docs.rs/tokio/latest/tokio/task/
- Tokio scheduler internals (low per-task overhead):
  https://tokio.rs/blog/2019-10-scheduler
- Actor granularity trade-off (fine vs coarse overhead):
  https://www.geeksforgeeks.org/system-design/actor-model-in-distributed-systems/
- ElasticActor (automatic granularity; communication overhead of fine actors):
  https://pacman.cs.tsinghua.edu.cn/npc2018/papers/ElasticActor.pdf
- ActorDB — single-writer actors / serialization:
  https://arxiv.org/html/2509.25285
