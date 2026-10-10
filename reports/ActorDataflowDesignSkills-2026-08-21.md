# Actor/Dataflow Design Skills: Codified Prior Art

Research commissioned 2026-08-21. Purpose: survey what the field has
written down, as rules, methodologies, and checklists, about how to
design actor-based and dataflow-based systems — prior art for adding
actors to the software-design skill.

The three-part machine doctrine (agglomerate multiple types → create a
coherent type → convert it onward) and the five sub-rules (map first,
types before traits, capabilities on their subjects, conversions as the
spine, names tell the truth) are the reference frame against which
findings are evaluated. Observations, hypotheses, and open questions
are kept in separate labelled sections.

## 1. Erlang/OTP

### 1.1 Armstrong's Nine Properties — the axiom list

Source: Joe Armstrong, PhD thesis "Making Reliable Distributed Systems
in the Presence of Software Errors," Royal Institute of Technology,
Stockholm, 2003. https://erlang.org/download/armstrong_thesis_2003.pdf
(Also appears in "Concurrency Oriented Programming in Erlang," 2002.)

Form: numbered axioms presented as architectural invariants, not advice.
Armstrong calls these the properties a concurrent language must have.

> 1. Everything is a process.
> 2. Processes are strongly isolated.
> 3. Process creation and destruction is a lightweight operation.
> 4. Message passing is the only way for processes to interact.
> 5. Processes have unique names.
> 6. If you know the name of a process you can send it a message.
> 7. Processes share no resources.
> 8. Error handling is non-local.
> 9. Processes do what they are supposed to do or fail.

Items 4 and 7 are the most broadly corroborated: they appear
independently in the OTP design principles docs, "Learn You Some
Erlang" (LYSE), and Ferd's "The Zen of Erlang."

### 1.2 Armstrong's Six Laws — failure-mode requirements

Source: Armstrong, "Systems That Never Stop" (QCon London 2009);
also summarized at nodramadevops.com.

Form: explicitly called laws, numbered, presented as requirements for
high-reliability systems.

> 1. Isolation — "Errors occurring in one process must not be able to
>    damage other processes in the system."
> 2. Concurrency — "The world is concurrent and concurrency is best
>    regarded as a program structuring principle."
> 3. Failure Detection — "It must be possible to detect exceptions both
>    locally (in the processes where the exception occurred) and
>    remotely."
> 4. Fault Identification — "We should be able to identify why an error
>    occurred."
> 5. Live Code Upgrade — "There should exist mechanisms to change code
>    as it is executing, and without stopping the system."
> 6. Stable Storage — "We need to store data in a manner which
>    preserves information across system failures."

Laws 1 and 3 appear independently in the thesis, LYSE, and Ferd.

### 1.3 Prohibition on shared state — exact quotes

Source: Armstrong, Erlang Factory 2014 (Wikiquote):
> "Shared memory is evil."

Source: Armstrong, thesis 2003 (quoted at highscalability.com):
> "The commonly used threads model of programming, where resources are
> shared, makes it extremely difficult to isolate components from each
> other."

Source: Learn You Some Erlang, "The Hitchhiker's Guide to Concurrency":
> "it was decided that the cleanest way to do things was to forbid
> processes from sharing memory" and "processes should communicate by
> sending messages where all the data is copied."

Recurrence: four independent phrasings (axiom 7, six laws context,
thesis, LYSE). The most broadly corroborated single rule in this
territory.

### 1.4 "Let it crash" — where it is actually stated

The phrase does not appear as a labeled rule in the official OTP docs;
it is a community distillation. The underlying rules appear separately:

Source: Armstrong, 2013 (Wikiquote):
> "the only sensible thing to do is crash. We just crash this call
> because we don't know what to do."

Source: LYSE:
> "errors which corrupt data should cause the faulty part of the system
> to die as fast as possible in order to avoid propagating errors."

Source: Armstrong thesis (dockyard.com):
> "Isolation implies that message passing is asynchronous. If process
> communication is synchronous then a software error in the receiver
> of a message could indefinitely block the sender of the message,
> destroying the property of isolation."

The third quote is notable: async is not a performance choice but a
logical consequence of isolation.

### 1.5 Supervision tree strategy rules

Source: Erlang OTP Supervisor documentation.
https://www.erlang.org/doc/system/sup_princ.html

Form: enumerated strategy definitions — each is a named rule with a
precisely stated consequence.

> one_for_one: "If a child process terminates, only that process is
> restarted."
>
> one_for_all: "If a child process terminates, all remaining child
> processes are terminated. Subsequently, all child processes,
> including the terminated one, are restarted."
>
> rest_for_one: "If a child process terminates, the child processes
> after the terminated process in start order are terminated.
> Subsequently, the terminated child process and the remaining child
> processes are restarted."

Hard ordering invariant:
> "The child processes are started in the order specified by this list,
> and are terminated in the reverse order."

Threshold circuit breaker:
> "If more than MaxR number of restarts occur in the last MaxT seconds,
> the supervisor terminates all the child processes and then itself."

Anti-pattern warning (cascade misconfiguration):
> "If your application has multiple levels of supervision, do not set
> the restart intensities to the same values on all levels...the total
> number of restarts...will be the product of the intensity values of
> all the supervisors."

Architectural heuristic (Ferd, "The Zen of Erlang,"
ferd.ca/the-zen-of-erlang.html):
> "Everything you feel is fragile and should be allowed to fail has to
> move deeper into the hierarchy, and what is stable and critical needs
> to be reliable is higher up."

### 1.6 gen_server vs. gen_statem vs. gen_event — decision rules

Source: Erlang OTP gen_statem documentation.

Conditional decision rule:
> "You should consider using gen_statem over gen_server if your process
> logic is convenient to describe as a state machine and you need any
> of these gen_statem key features."
(Five features listed: co-located callback code per state, postponing
events, inserted events, state enter calls, easy timeout management.)

Performance-qualified carve-out:
> "For simple state machines not needing these features, gen_server is
> perfectly suitable. It also has a smaller call overhead, but we are
> talking about something like 2 vs 3.3 microseconds call roundtrip
> time here."

State vs. data design rule (gen_statem):
> "If a change in the value changes the set of events that is handled,
> the value should be in the State."

Source: LYSE, "Event Handlers":
> "If your server has many subscribers, it can keep going because it
> only needs to forward events once. If there is a lot of data to be
> transferred, it's only done once and all callbacks operate on that
> same instance of the data. You don't need to spawn processes for
> short lived tasks."

### 1.7 Process granularity and message protocol rules

Granularity rule-of-thumb (Ferd, "The Zen of Erlang"):
> "The idea is to use as many processes as you need, rather than as
> many as you can."

Encapsulation requirement for public APIs (LYSE):
> "Hiding messages! If you expect people to build on your code and
> processes, you must hide the messages in interface functions."

Module-per-process practice (Erlang OTP docs):
> "It is usually good programming practice to have the code
> corresponding to one process contained in a single module."

## 2. Akka Typed / Apache Pekko

### 2.1 No shared mutable state — exact quotes

Source: doc.akka.io/docs/akka/2.5/general/actor-systems.html:
> "Do not pass mutable objects between actors. In order to ensure
> that, prefer immutable messages."

Source: doc.akka.io/docs/akka/2.5/general/jmm.html:
> "Messages should be immutable, this is to avoid the shared mutable
> state trap."

Source: Manuel Bernhardt, "Akka anti-patterns: shared mutable state"
(manuel.bernhardt.io):
> "Simply do not share mutable state across actors, period."

Source: Akka/Pekko Typed style guide:
> "It's not recommended to place mutable state and var members in the
> enclosing class."

### 2.2 Formal JMM happens-before laws

Source: doc.akka.io/docs/akka/2.5/general/jmm.html

Form: formal laws stated as runtime guarantees.

> "the send of the message to an actor happens before the receive of
> that message by the same actor."

> "processing of one message happens before processing of the next
> message by the same actor."

Derived corollary:
> "changes to internal fields of the actor are visible when the next
> message is processed by that actor. So fields in your actor need not
> be volatile or equivalent."

### 2.3 Message protocol design rules

Source: Akka/Pekko Typed style guide
(doc.akka.io/libraries/akka-core/current/typed/style-guide.html and
pekko.apache.org equivalent).

Type-system mandate:
> "Unlike the classic API where following this best practice is
> optional, you need to formalize the set of handled messages during
> implementation."

Sealed-trait recommendation with compiler rationale:
> "It's recommended to use a sealed trait as the super type of the
> commands (incoming messages) of an actor as the compiler will emit
> a warning if a message type is forgotten in the pattern match."

Placement rule:
> "It is not recommended to define messages as top-level classes...For
> the majority of cases it's good style to define the messages in the
> companion object as static inner classes together with the Behavior."

Private messages rule:
> "Such messages should be declared private so they can't be accessed
> and sent from the outside of the actor. Note that they must still
> extend/implement the public Command trait/interface."

Naming conventions (all from style guide):
> "replyTo is the typical name for the ActorRef[Reply] parameter in
> messages to which a reply or acknowledgement should be sent."
>
> "Incoming messages to an actor are typically called commands, and
> therefore the super type of all messages that an actor can receive
> is typically sealed trait Command."
>
> "Use past tense for the events persisted by an EventSourcedBehavior
> since those represent facts that have happened, for example
> Incremented."

Source: Manuel Bernhardt, tour of Akka Typed:
> "The API is designed to be 'protocol-first': you no longer have a
> choice but to spend at least a little bit of time thinking about the
> messages each actor can deal with."

### 2.4 Supervision strategy rules

Source: doc.akka.io/docs/akka/2.5/typed/fault-tolerance.html

Validation vs. failure classification rule:
> "A validation error means that the data of a command sent to an actor
> is not valid, this should rather be modelled as a part of the actor
> protocol than make the actor throw exceptions."
>
> "A failure is instead something unexpected or outside the control of
> the actor itself, for example a database connection that broke."

Platform default rule:
> "An important difference between Typed and Untyped actors is that
> Typed actors are by default stopped if an exception is thrown and
> no supervision strategy is defined while in Untyped they are
> restarted."

Default strategy recommendation (doc.akka.io/docs/akka/2.5/general/
supervision.html):
> "Normally, you should use the OneForOneStrategy, which also is the
> default if none is specified explicitly."

Criterion for AllForOne:
> "The AllForOneStrategy is applicable in cases where the ensemble of
> children has such tight dependencies among them, that a failure of
> one child affects the function of the others."

Structural law:
> "Actors can only be created by other actors — where the top-level
> actor is provided by the library — and each created actor is
> supervised by its parent."

Error Kernel pattern with rule:
> "If one actor carries very important data (i.e. its state shall not
> be lost if avoidable), this actor should source out any possibly
> dangerous sub-tasks to children it supervises and handle failures of
> these children as appropriate."

Watching vs. supervising distinction:
> "If one actor depends on another actor for carrying out its duty, it
> should watch that other actor's liveness and act upon receiving a
> termination notice. This is different from supervision, as the
> watching party has no influence on the supervisor strategy."

### 2.5 Interaction pattern selection checklists

Source: pekko.apache.org/docs/pekko/1.0/typed/interaction-patterns.html

Form: per-pattern "useful when" checklists paired with "problems" lists.

Fire and Forget — use when:
- "It is not critical to be sure that the message was processed"
- "There is no way to act on non successful delivery or processing"
- "We want to minimize the number of messages created to get higher
  throughput"

Ask (actor-to-actor) — use when:
- "Single response queries"
- "An actor needs to know that the message was processed before
  continuing"
- "To allow an actor to resend if a timely response is not produced"

Scope rule:
> "AskPattern is only intended for request-response interaction from
> outside an actor. If the requester is inside an actor, prefer
> ActorContext.ask as it provides better thread-safety."

### 2.6 Functional vs. object-oriented style — decision checklists

Source: Akka/Pekko Typed style guide.

Functional style — when to use (bulleted):
- "The state is immutable and can be passed to 'next' behavior"
- "The Behavior is stateless"
- "The actor lifecycle has several different phases that can be
  represented by switching between different behaviors"
- "It's less risk of accessing mutable state in the actor from other
  threads, like Future or Streams callbacks"

Object-oriented style — when to use (bulleted):
- "Some state is not immutable"
- "It could be more familiar and easier to upgrade existing classic
  actors to this style"
- "Mutable state can sometimes have better performance"

Meta-rule (self-qualifying disclaimer):
> "As with all style guides, treat this as a list of rules to be
> broken. There are certainly times when alternative styles should be
> preferred over the ones given here."

## 3. Microsoft Orleans

### 3.1 Virtual actor definitional law

Source: learn.microsoft.com/en-us/dotnet/orleans/overview

> "Actors are purely logical entities that always exist, virtually.
> An actor cannot be explicitly created nor destroyed, and its virtual
> existence is unaffected by the failure of a server that executes it.
> Since actors always exist, they are always addressable."

### 3.2 Suitability checklist — when Orleans fits

Source: learn.microsoft.com/en-us/dotnet/orleans/resources/best-practices

Consider Orleans when (bulleted criteria):
- "Significant number (hundreds, millions, billions, and even
  trillions) of loosely coupled entities."
- "Entities are small enough to be single-threaded."
- "Workload is interactive."
- "More than one server is expected or may be required."
- "Global coordination is not needed or on a smaller scale between a
  few entities at a time."

Orleans is not the best fit when (anti-suitability criteria):
- "Memory must be shared between entities. Each grain maintains its
  states and should not be shared."
- "A small number of large entities may be multithreaded."
- "Global coordination and/or consistency are needed."
- "Operations that run for a long time."

### 3.3 Grain sizing rules

Source: learn.microsoft.com/en-us/dotnet/orleans/resources/
frequently-asked-questions

Too-large grain warning:
> "The rule of thumb is to be wary of individual grain receiving
> hundreds of requests per second. That may be a sign of the grain
> being too large, and decomposing it into a set of smaller grains may
> lead to a more stable and balanced system."

Too-small grain warning:
> "An application entity may be too small to be a grain if that would
> cause constant interaction of other grains with it, and as a result,
> cause too much of a messaging overhead. In such cases, it may make
> more sense to make those closely interacting entities part of a
> single grain, so that they would invoke each other directly."

### 3.4 Concurrency guarantee — architectural law

Source: learn.microsoft.com/en-us/dotnet/orleans/benefits

> "The runtime guarantees a grain never executes on more than one
> thread at a time. Combined with isolation from other grains,
> developers never face concurrency at the grain level and never need
> locks or other synchronization mechanisms to control access to
> shared data."

Prohibition:
> "Never perform a thread-blocking operation within a grain. All
> operations other than local computations must be explicitly
> asynchronous."

Deadlock warning:
> "Grains are non-reentrant by default. Deadlock can occur due to call
> cycles. Timeouts are used to automatically break deadlocks."

### 3.5 Communication rules

Anti-chattiness best practice:
> "Avoid chatty communication between grains. Direct memory use is
> significantly less expensive than message passing. Highly chatty
> grains may be better combined as a single grain."

Anti-bottleneck best practice:
> "Avoid bottleneck grains. Single coordinator/Registry/Monitor. Do
> staged aggregation if required."

Message delivery guarantee (architectural constraint):
> "Orleans provides a message delivery guarantee where each message is
> delivered at-most-once. It is the responsibility of the caller to
> retry any failed calls if needed."

## 4. Rust Actor Libraries and the Sans-IO School

### 4.1 Alice Ryhl — "Actors with Tokio"

Source: https://ryhl.io/blog/actors-with-tokio/
Author: Tokio core maintainer. Canonical reference for hand-rolled
Tokio actor pattern.

Structural definition:
> "An actor is split into two parts: the task and the handle."

Hard mandate (deadlock prevention):
> "You must make sure that there are no cycles of channels with bounded
> capacity."

Scope qualification on the above:
> "Channels whose send method always returns immediately do not count
> in this kind of cycle, as you cannot deadlock on such a send."

Bounded channel recommendation:
> "You should still make sure to use a bounded channel so that the
> number of messages waiting in the channel don't grow without bound."

Error-handling directive with rationale:
> "Ignore send errors. If this send fails, so does the recv.await
> below. There's no reason to check for the same failure twice."

Shutdown warning:
> "You need to be a bit careful if your actors form a cycle, because by
> holding on to each other's handle structs, the last sender is never
> dropped, preventing shutdown."

Form: structural definition + hard mandate + recommendations. Rules
emerge from code walkthrough, not a dedicated rules section.

### 4.2 barafael — "More Actors with Tokio"

Source: https://barafael.github.io/posts/more-actors-with-tokio/

Anti-proliferation rule:
> "If you can avoid an actor, do so. Try to delete as many actors from
> your design as possible."

Categorical prohibition on frameworks:
> "Don't use an actor framework. The ones I have seen are bad
> abstractions over tokio::spawn."

I/O ownership prohibition:
> "An actor should not own channel handles or sockets or other I/O
> resources."

DAG topology directive:
> "Strive for your channel topology to be a Directed Acyclic Graph
> (DAG)."

Ownership-as-transfer definition:
> "A message is a way to transfer ownership from one actor to another."

Call-response caution:
> "Most actors in my experience do not require and should not employ
> the call-response pattern."

### 4.3 Axiom crate — numbered axioms

Source: https://docs.rs/axiom/latest/axiom/

Form: explicitly numbered, unconditional axioms. The strongest formal
structure found in the Rust actor space.

> 1. "An actor can be interacted with only by means of messages."
> 2. "An actor processes only one message at a time."
> 3. "An actor will process a message only once."
> 4. "An actor can send a message to any other actor without knowledge
>    of that actor's internals."
> 5. "Actors send only immutable data as messages, though they may have
>    mutable internal state."
> 6. "Actors are location agnostic; they can be sent a message from
>    anywhere in the cluster."

Prohibition derived from axiom violation:
> "using an Arc or Mutex enclosing a structure as state...would
> definitely be a bad idea as it would break the rules"

### 4.4 Ractor — aspirational ideal and exclusive prescription

Source: https://docs.rs/ractor/latest/ractor/

Aspirational ideal:
> "In an ideal world, all actor structs would be empty with no stored
> values."

Qualified recommendation on self content:
> "An actor's self is passed as a read-only reference which shouldn't
> ideally contain state information, but could contain configuration /
> startup information if you want."

Exclusive prescription:
> "using &mut self would risk 'losing the safety' of initialization
> control, so state initialization occurs exclusively in pre_start."

Pre-start warning (implied design rule):
> "Pre-start panics cause spawn failures and aren't caught by
> supervision."

### 4.5 Actix — state machine specification

Source: https://actix.rs/docs/actix/actor

Absolute invariants:
> "Actors communicate exclusively by exchanging messages."
> "Actors are not referenced directly, but by means of addresses."
> "All messages are statically typed."

Message handler requirement:
> "To be able to handle a specific message the actor has to provide a
> Handler<M> implementation for this message."

Lifecycle state machine — formal specification with named states
(Started, Running, Stopping, Stopped) and stated transitions:
> "An actor always starts in the Started state."
> "After an Actor's started() method is called, the actor transitions
> to the Running state."
> "By default this method returns Running::Stop which confirms the stop
> operation."
> "An actor can restore from the stopping state to the running state
> by creating a new address or adding an event object, and by
> returning Running::Continue."

Form: most rule-dense source in the Rust survey. Guidance via formal
specification rather than recommendations.

### 4.6 Scala best practices — SHOULD/MUST actor rules

Source: github.com/alexandru/scala-best-practices, Section 5 — Actors

Form: SHOULD/MUST modal operators (RFC-style). The strongest
practitioner checklist format found. Not Rust-specific but directly
applicable and the most checklist-like resource in the whole survey.

> 5.1: "SHOULD evolve the state of actors only in response to messages
>      received from the outside" (prohibits internal scheduler-driven
>      mutation)
>
> 5.2: "SHOULD mutate state in actors only with context.become"
>      (enables functional state machine modeling)
>
> 5.3: "MUST NOT leak the internal state of an actor in asynchronous
>      closures" (use `pipeTo` instead of capturing mutable state)
>
> 5.4: "SHOULD do back-pressure" (workers signal demand; producers only
>      generate when demand exists)
>
> 5.5: "SHOULD NOT use Akka FSM" (couples business logic to Akka; use
>      `context.become` instead)

### 4.7 Sans-IO — the most prohibition-heavy source

Sources: https://sans-io.readthedocs.io/,
https://www.firezone.dev/blog/sans-io,
https://swatinem.de/blog/sans-io-pattern/

Core prohibition (Python-origin docs):
> "no code that does any form of network I/O or any form of
> asynchronous flow control"

Inversion-of-control principle:
> "allow users of the library to drive the network interactions
> themselves, not the network protocol library itself"

Architectural placement directive:
> "I/O and flow control primitives to the edges of the program"

Rust-specific prohibition list (Firezone blog):
> "Don't invoke tokio::spawn() or similar async runtime operations
> within the state machine"
> "Never call Instant::now() directly; time must be passed as a
> parameter"
> "Avoid calling UdpSocket::send(), recv(), or similar IO within
> protocol logic"
> "All functions must be synchronous and never block"

Prescribed interface structure (Firezone):
> Implementations should provide: `handle_input()`, `poll_transmit()`,
> `handle_timeout()`, `poll_timeout()`

Dependency inversion framing (swatinem.de):
> "policies (what to do) should not depend on implementation details
> (how to do it), and instead both components should depend and
> communicate via abstractions"

Self-characterization:
> "This is a specific facet of several broader software design best
> practices (Clean Architecture, MVC, separation of concerns) rather
> than a formal specification."

Observation: sans-io does not cite actor design and the actor sources
do not cite sans-io. The structural overlap is: a sans-io state machine
is structurally compatible with an actor's task body — it takes input,
updates state, emits transmit requests, but never performs I/O. The
actor's run loop becomes the sans-io "driver." barafael's "An actor
should not own channel handles or sockets or other I/O resources" is
the closest any actor source comes to stating the sans-io principle in
actor vocabulary.

### 4.8 Recurring rules across Rust actor sources (five or more
independent sources)

1. Bounded channels by default — Ryhl, barafael, SoftwarePatternslexicon,
   RustFAQ, and multiple forum posts.

2. DAG topology / avoid channel cycles — Ryhl ("must" on bounded
   cycles), barafael ("strive for DAG"), RustFAQ ("design acyclic")
   — three independent phrasings.

3. Sole ownership of actor state; no shared mutable state — Axiom,
   Actix, SoftwarePatternslexicon, RustFAQ, Axiom crate.

4. Messages own their data; no borrowed references into them — barafael,
   SoftwarePatternslexicon, Axiom ("immutable data").

5. Do not block the async runtime — SoftwarePatternslexicon ("Do Not
   Block the Async Runtime"), RustFAQ ("Keep the loop tight").

## 5. Dataflow Design Traditions

### 5.1 Flow-Based Programming (J. Paul Morrison)

Sources: https://jpaulmorrison.com/fbp/,
https://jpaulmorrison.com/fbp/concepts_book.shtml,
https://jpaulm.github.io/fbp/morrison_2005.htm

#### Scheduling rules

Source: https://jpaulmorrison.com/fbp/schedrls.shtml

Form: numbered rules specified as a scheduler contract.

> 1. "a component is called as soon as possible after a data IP
>    arrives at one of its input ports, or just as soon as possible
>    if there are no input ports."
> 6. "a process can only terminate itself — no process can terminate
>    another."
> 7. "a given process can only be in one of these states at a time,
>    and, when suspended, a process can only be waiting for a single
>    event."
> 10. "all output ports of a component...will present end of data when
>     that component terminates."

#### IP lifecycle laws — mandatory ownership accounting

> "Each IP must be disposed of positively by the process receiving it
> (much like a paper memo): by sending it on, filing it, destroying
> it or attaching it to another IP."
>
> "Any process which receives an IP has its 'number of owned IPs'
> incremented, and must reduce this number back to zero before it
> exits."
>
> "At any point in time, a given IP can only be 'owned' by a single
> process, or be in transit."
>
> "An IP cannot be reaccessed by a process once it has been disposed
> of."

Note: IP ownership accounting is structurally identical to Rust's
move semantics and to the three-part machine's "conversions consume
their inputs by value." Morrison stated these rules in the 1970s.

#### Architectural prohibitions

> "bounded buffer connections connecting processor ports are the only
> way these processors are allowed to communicate."
>
> "FBP requires code to be read-only."
>
> "FBP components must not have side-effects either."
>
> "Connections in FBP are bounded, with a finite capacity, rather than
> unbounded."

#### Named topology patterns

> "the 'divergent-convergent' visual pattern 'is one of a number of
> network topologies that visually signal to the FBP programmer the
> possibility of a deadlock'."
>
> "Any node in the network can be replaced by a subnet...or vice
> versa." (Composability rule.)
>
> "we encourage the designer to draw it as 'broadly' as is practical,
> and then subdivide it afterwards." (Top-down decomposition principle.)

### 5.2 Kahn Process Networks

Sources: https://en.wikipedia.org/wiki/Kahn_process_networks,
https://handwiki.org/wiki/Kahn_process_networks,
UT Austin EE382C course materials.

Form: mathematical axioms of the model; design rules are derived
theorems and scheduler constraints. Violating any axiom exits the
Kahn model and voids the determinism guarantee.

#### Core axioms

> "Each communication channel has one writer and one reader. Each
> communication channel is an infinite, first-in first-out (FIFO)
> queue of tokens."
>
> "Reading from a channel is blocking while writing is non-blocking."
>
> "A FIFO cannot be consumed by multiple processes, nor can multiple
> processes write to a single FIFO."
>
> "Processes are not allowed to test an input channel for existence of
> tokens without consuming them." (The no-peek rule — checking for
> emptiness without blocking introduces non-determinism.)
>
> "Given a specific input (token) history for a process, the process
> must be deterministic so that it always produces the same outputs."

#### Derived theorems

> "Kahn Process Network programs are determinate; i.e., the history
> of tokens produced on the communication channels do not depend on
> the execution order."
>
> "A monotonic process is determinate, and a network of monotonic
> processes is also determinate."
>
> "Reading more tokens can only lead to writing more tokens."
>
> "Tokens read in the future can only affect tokens written in the
> future." (Causality property.)

#### Parks' scheduler rules (bounded-memory execution)

Three rules:
1. "Block when attempting to read an empty queue."
2. "Block when attempting to write to a full queue."
3. "If we reach artificial deadlock...increase the capacity of the
   smallest full queue until the producer associated with it can
   fire."

Priority ordering:
1. Complete execution — correctness over memory.
2. Bounded execution — memory bounded is second priority.

Design limitation:
> "It is an undecidable problem to test whether a KPN is strictly
> bounded by b." (Static verification of bounded memory is impossible
> in general — a hard limit on what tooling can provide.)

### 5.3 Reactive Streams Specification

Source: https://github.com/reactive-streams/reactive-streams-jvm/blob/
master/README.md

Form: numbered rules with MUST/MAY/RECOMMENDED modal operators
(RFC 2119 convention), paired with a Technology Compatibility Kit
(TCK) that mechanically verifies conformance. The most formally
codified source in the entire survey.

#### Design axiom (from the specification's framing)

> "One of the underlying design principles is that all buffer sizes
> are to be bounded and these bounds must be known and controlled by
> the subscribers. These bounds are expressed in terms of element
> count."

#### Signal protocol grammar

> "onSubscribe onNext* (onError | onComplete)?"

Form: formal grammar specifying legal signal sequences. The majority
of TCK tests verify this grammar.

#### Selected Publisher rules (verbatim from spec)

> 1. "The total number of onNext's signalled by a Publisher to a
>    Subscriber MUST be less than or equal to the total number of
>    elements requested by that Subscriber's Subscription at all
>    times."
> 3. "onSubscribe, onNext, onError and onComplete signaled to a
>    Subscriber MUST be signaled serially."
> 7. "Once a terminal state has been signaled (onError, onComplete) it
>    is REQUIRED that no further signals occur."

#### Selected Subscriber rules (verbatim from spec)

> 1. "A Subscriber MUST signal demand via Subscription.request(long n)
>    to receive onNext signals." (Pull-based demand: subscriber
>    controls flow.)
>    - "It is RECOMMENDED that Subscribers request the upper limit of
>      what they are able to process, as requesting only one element at
>      a time results in an inherently inefficient stop-and-wait
>      protocol."
> 7. "A Subscriber MUST ensure that all calls on its Subscription's
>    request and cancel methods are performed serially."

#### Selected Subscription rules (verbatim from spec)

> 3. "Subscription.request MUST place an upper bound on possible
>    synchronous recursion between Publisher and Subscriber."
>    - "Implementations are RECOMMENDED to limit this mutual recursion
>      to a depth of ONE (ONE) — for the sake of conserving stack
>      space."
> 5. "Subscription.cancel MUST respect the responsivity of its caller
>    by returning in a timely manner, MUST be idempotent and MUST be
>    thread-safe."

#### Processor rules (verbatim from spec)

> 1. "A Processor represents a processing stage — which is both a
>    Subscriber and a Publisher and MUST obey the contracts of both."
> 2. "A Processor MAY choose to recover an onError signal. If it
>    chooses to do so, it MUST consider the Subscription cancelled,
>    otherwise it MUST propagate the onError signal to its Subscribers
>    immediately."

### 5.4 Timely Dataflow and Differential Dataflow

Sources: SOSP 2013 (Naiad paper), McSherry's blog
(frankmcsherry.org), timelydataflow.github.io.

#### Core operator contract

Source: Naiad paper / xzhu0027 gitbook.

Anti-time-travel rule (stated multiple independent ways):
> "When methods are invoked with a timestamp t, they may only call
> SENDBY or NOTIFYAT with times t' >= t."
>
> "This ensures time never flows backward through the graph."

Notification delivery guarantee:
> "v.ONNOTIFY(t) is invoked only after no further invocations of
> v.ONRECV(e,m,t'), for t' <= t, will occur."

Causality rule:
> "a 'later' timestamped message cannot possibly be the cause of an
> earlier timestamped one."

#### Structural constraints

Source: McSherry's blog, "Timely Dataflow reboot," 2014.

Static graph rule:
> "the structure of the computation is committed to in advance of the
> execution, and the only responsibility of workers is to react to
> incoming data."

Epoch-completion protocol:
> "The input source must also tell the timely dataflow graph when no
> more messages for a particular epoch will be sent (when the epoch is
> complete)."

Hierarchical encapsulation rule:
> "a subgraph presents upwards as a vertex to the graph layer above it,
> concealing implementation details."

#### Differential Dataflow invariant

Source: McSherry, "Differential Dataflow," 2015.

> "`Collection[t] = sum_{s <= t} Difference[s]`"
>
> "Everything goes horribly wrong if we let logic produce output on
> empty collections; we don't want to have to run it for all possible
> keys, but rather only the ones for which we've actually seen data."

### 5.5 Reactive Manifesto

Source: https://www.reactivemanifesto.org/ (v2.0, 2014). Authors:
Jonas Bonér, Dave Farley, Roland Kuhn, Martin Thompson.

Form: four named principles with prose elaboration. Aspiration, not
operational rules. Least codified source in the survey.

> **Responsive**: "The system responds in a timely manner if at all
> possible."
>
> **Resilient**: "The system stays responsive in the face of failure.
> Failures are contained within each component."
>
> **Elastic**: "The system stays responsive under varying workload."
> Designs eliminate "contention points or central bottlenecks."
>
> **Message Driven**: "Reactive Systems rely on asynchronous
> message-passing to establish a boundary between components."
> Enables "load management, elasticity, and flow control" through
> queue monitoring and "back-pressure" application.

Composability principle:
> "Large systems are composed of smaller ones and therefore depend on
> the Reactive properties of their constituents."

## 6. AI-Agent Skills in the Wild

### 6.1 What was searched

GitHub searches for AGENTS.md, CLAUDE.md, and .cursorrules files
containing "actor" or "dataflow"; cursor.directory categories;
anthropics/skills; proyecto26/system-design-skills; apify/agent-skills;
mcpmarket.com system-design-architect skill.

### 6.2 What was found

No published AI-agent skill file — not in CLAUDE.md, AGENTS.md,
.cursorrules, .cursor/rules, Claude Code skill marketplace, or MCP
market — teaches actor model or dataflow architecture as a design
methodology. This is confirmed, not hypothesized.

The word "actor" appears in AGENTS.md files only in two senses: the
Swift concurrency `actor` keyword (Swift/visionOS repos) and
project-specific naming conventions (rivet-gg/actor-core, apify).
Neither teaches architectural methodology.

The apify/agent-skills repo has an "apify-actor-development" skill
that teaches Apify's serverless packaging format, not the actor
concurrency model.

### 6.3 The closest existing practitioner resources

The scala-best-practices Section 5 (SHOULD/MUST rules, reproduced
in section 4.6 above) is already written in AI-targetable rule form
and could be adapted into a skill directly.

Manuel Bernhardt's Akka anti-pattern taxonomy provides the
complementary structural vocabulary: flat hierarchies (mixing business
logic and failure handling), too many ActorSystems, blocking inside
actors, not defining a protocol, naming components after Akka concepts.
His most structurally pointed entry: flat hierarchies fail not because
of flatness per se but because of "mixing business logic and failure
handling" — the symptom names the cause.

## 7. Rules That Recur Across Independent Traditions

Weighted by origin — if source B cites source A, the pair counts as
one independent origin. Sequence: how many independent origins.

### Rule 1: No shared mutable state (six independent origins)

Erlang axiom 7 + six laws context + LYSE (three phrasings, one
tradition). Akka Typed general docs + JMM docs + style guide + Bernhardt
(one tradition, multiple phrasings). Orleans anti-suitability criterion.
FBP "unique states, read-only code, no side effects." Kahn determinism
requirement (shared state would introduce non-determinism). Rust actor
school (Axiom axiom 5, Actix invariant, RustFAQ golden rule "Don't
share state. Send messages.").

This is the one rule that every tradition states explicitly, in its own
vocabulary, without citing the others.

### Rule 2: Bounded queues, controlled by the consumer (five independent
origins)

FBP: bounded connections are an architectural axiom, not configurable.
Kahn/Parks: "Block when attempting to write to a full queue"; bounded
memory is Priority 2 in scheduling. Reactive Streams: "all buffer sizes
are to be bounded and these bounds must be known and controlled by the
subscribers" — stated as "one of the underlying design principles."
Reactive Manifesto: "flow control" via queue monitoring and back-pressure.
Rust actor school: Ryhl "should use a bounded channel," barafael
"bounded is the norm," RustFAQ "Bounded channels are the norm."

### Rule 3: Message passing as the only inter-entity communication (four
independent origins)

Erlang axiom 4 (stated before the other origins existed). Akka Typed
type-system enforcement (replyTo in message definition; no implicit
sender; protocol-first). Orleans grain-to-grain calls as the
communication model. FBP exclusive channel rule ("the only way these
processors are allowed to communicate"). Rust actor school: Actix
"exclusively by exchanging messages."

### Rule 4: Single-threaded execution per actor (three independent origins)

Erlang: per-process isolation makes this a structural property. Akka
JMM happens-before laws: "processing of one message happens before
processing of the next." Orleans: runtime guarantee, stated explicitly,
enabling lock-freedom. This is not stated as a design choice but as an
invariant the system enforces.

### Rule 5: DAG topology preferred; cycles must be managed (three
independent origins)

Erlang: the supervision tree is a tree by definition (acyclic). Rust
actor school: Ryhl "must" for bounded cycles, barafael "strive for
DAG," RustFAQ "design acyclic" — three phrasings, independently arrived
at. FBP: divergent-convergent visual pattern signals deadlock risk;
Parks' deadlock resolution as the answer when cycles exist. (Timely
dataflow: the progress-tracking graph must be acyclic even if the
data graph has cycles.)

### Rule 6: Signals cannot go backward in time / terminal states cannot
be reversed (two independent origins, same structure)

Reactive Streams: once a terminal state is signaled, "no further
signals occur" (Publisher rule 7). Timely Dataflow: anti-time-travel
rule — operators may only send to timestamps >= the current timestamp.
These traditions do not cite each other; the rule emerges from the same
structural need (predictability of completeness).

### Rule 7: Do not block the execution context (four independent origins)

Erlang: async follows from isolation by logical necessity (Armstrong
thesis). Akka: async only; JMM laws make this observable. Orleans:
explicit "Never perform a thread-blocking operation within a grain."
Rust actor school: "Do Not Block the Async Runtime" (SoftwarePatternslexicon),
"Keep the loop tight" (RustFAQ), sans-io's "All functions must be
synchronous and never block" (enforces non-blocking at the protocol
level).

### Rule 8: Effects as data, not performed directly (three independent
origins with the same structure)

Erlang OTP behaviors: the developer's callbacks return values that
describe transitions; the framework executes them. Akka Typed
EventSourcedBehavior: the Effect ADT describes what the runtime should
do — side effects execute only after events are durably written. Elm
Architecture (TEA): `Cmd Msg` — effects are values interpreted by the
runtime, never performed inline. Sans-io: the state machine returns
transmit-requests and timeout queries; the driver performs I/O. FBP:
IP lifecycle laws model data as parcels, not shared references.

## 8. Analysis: Mesh and Clash with the Three-Part Machine

### Meshes

**The Elm Architecture is the three-part machine made explicit.**
TEA's `update : Msg -> Model -> (Model, Cmd Msg)` is:
agglomerate (Msg arrives from outside) → create a coherent type
(Model updated) → convert it onward (Cmd Msg handed to the runtime).
The Msg type is a sealed enum — types first. The runtime/programmer
boundary is the conversion spine. The estate research noted this as
"the deepest resonance in the entire survey"; the three-part machine
doctrine confirms the structural identity.

**Event sourcing is a three-part machine across time.** Akka
EventSourcedBehavior: Command (agglomerate from outside) →
Effect[Event, State] (coherent type) → event application as pure fold
`(State, Event) => State` (converted onward). The event handler's
purity — no side effects, just `(State, Event) => State` — is the
conversion step in the machine. The event schema is the type list. This
aligns tightly with the doctrine's conversion spine.

**OTP behaviors are the three-part machine as a process skeleton.**
The framework owns the loop; callbacks fill in agglomerate (init/1),
create coherent (handle_call/3 producing a new state), convert onward
(reply + new state returned to the framework). The developer never
writes the loop — only the domain parts of the machine.

**FBP's IP ownership accounting is Rust move semantics stated as
design rules.** Morrison's "only one owner at a time, must be disposed
before exit, cannot be reaccessed after disposal" is the exact same
principle as the doctrine's "conversions consume their inputs by value:
no references held into them." Morrison published these as FBP rules
in the 1970s; the three-part machine and Rust arrived at the same
structure independently.

**Sans-io's "I/O at the edges" is the pre-output type pattern.**
The draft's executable special case — the forced pre-output type at
the OS boundary — is structurally identical to sans-io: the state
machine (coherent type) emits events/transmit-requests (pre-output
type), and the driver (caller, edge of the program) performs the actual
I/O. The doctrine accounts for this as the output machine's special
case; sans-io names it an architectural placement rule.

**Reactive Streams' signal grammar is the output machine's protocol.**
`onSubscribe onNext* (onError | onComplete)?` is a formal grammar for
the sequence in which a publisher converts data onward. The terminal
states (onComplete, onError) are the type-level distinction between
successful and failed conversions — analogous to From vs. TryFrom in
the doctrine.

### Clashes and tensions

**Tension 1: Actors have persistent identity; the map excludes
processes.** The doctrine says "Steps are walks across the map, never
things on it" and rejects types named for processes (Resolver,
Controller, Manager). But in actor systems, processes/actors have
identity — they are named (PIDs, GrainIds, ActorRefs), they exist over
time, they hold state. Orleans' virtual actor law states this explicitly:
"actors always exist, virtually." If actors are to appear in the design,
they must appear on the map as things with identity and state, not as
processes that walk across other things. This is a genuine tension: the
map must include actors as persistent entities, not walk-steps.

Hypothesis: the resolution may be that an actor is the thing whose
state is the coherent type, and the message-handler is the conversion.
The actor's persistent identity is the type; the conversion is the
behavior. The map holds the actor type (and its state); the supervisor
tree and the message flow are the walks across the map. This would align
actors with the doctrine but has not been stated or reviewed.

**Tension 2: Supervision as map structure or walk structure.** A
supervision hierarchy (Erlang: one_for_one, one_for_all, rest_for_one)
is a structural relationship between actors. Is the supervision tree a
thing on the map, or a walk across it? The OTP design is strongly typed
about this: the supervision tree is a configuration of relationships,
not a service object. The doctrine's ban on service objects (managers,
controllers) would apply to a Supervisor if the Supervisor is named for
its role. But the OTP Supervisor's role is exactly structural — it holds
child specs and implements a restart strategy. It may be that supervision
belongs on the map as a structural thing, not as a process.

Open question: does the three-part machine need a supervision layer,
and if so, where does it appear in the type spine?

**Tension 3: Dataflow's "graph is the program" conflicts with the
types-first orientation.** In timely/differential dataflow, the program
is the wiring of operators; types flow through them but operators are
primary. The doctrine says types are primary and the conversions between
them are the spine. These are different orientations: in the doctrine,
you name every intermediate stage; in timely dataflow, you compose
operators and the intermediate types are implicit. McSherry's static
graph rule ("the structure of the computation is committed to in advance")
is consistent with the map-first principle, but the types of the
intermediate collections are not the structural entities — the operators
are.

This is a partial clash. The doctrine could be applied to dataflow by
saying: name every collection type that flows between operators, and
let the operator be the conversion between named collection types. But
this is not how timely/differential dataflow is typically designed.

**Tension 4: The call-response pattern is suspect in actor systems,
but is the backbone of the TryFrom spine.** barafael: "Most actors in
my experience do not require and should not employ the call-response
pattern." The doctrine's main as a table of contents (`let resolved =
ResolvedAssembly::try_from((registry, assembly))?`) is synchronous call-
and-response between types. But in a running actor system, synchronous
TryFrom calls inside an actor block the actor. The doctrine is about
program-scale type construction; actors run at system-time. The two
scales do not directly conflict, but the conversion spine's synchronous
character does not translate into the actor runtime model without care.
Each message handler is a TryFrom of sorts; but the chain cannot be one
synchronous chain if intermediate stages are separate actors.

### Disconfirming evidence — against codifying actor design

Found one explicit argument against codifying actor design in rules:

The Akka Typed style guide's meta-rule:
> "As with all style guides, treat this as a list of rules to be broken.
> There are certainly times when alternative styles should be preferred
> over the ones given here."

And Ferd's pragmatic heuristic:
> "The idea is to use as many processes as you need, rather than as
> many as you can."

These argue that actor design is too context-dependent for rigid rules.
The grain-sizing rules in Orleans make the same point structurally —
the "right" grain size depends entirely on the application domain model.

No source was found that argues structurally against codifying actor
design as a discipline. The Akka disclaimer is a style-guide caveat,
not a methodological objection.

## 9. What Is Unique to One Source

Rules found in only one tradition, stated strongly, that have no analog
elsewhere:

- **Kahn's no-peek rule**: processes may not test a channel for token
  existence without consuming. The specific prohibition on
  non-destructive inspection has no direct analog in actor systems.

- **FBP's IP reference counting**: explicit per-process ownership
  accounting with a zero-balance requirement at exit. Stated decades
  before Rust's ownership system; no other tradition formalizes this.

- **Reactive Streams' TCK**: mechanical verification of conformance
  via an automated test kit. No other tradition in the survey has this.

- **"Never call Instant::now() directly; time must be passed as a
  parameter"** (sans-io, Firezone). The most specific Rust-level
  design prohibition found. No analog in Erlang, Akka, or Orleans.

- **The anti-time-travel rule** (Timely Dataflow): operators can only
  send to timestamps >= current timestamp. This is the specific formal
  constraint that enables progress tracking; no analog in the actor
  traditions.

- **Orleans' at-most-once delivery guarantee as an explicit design
  constraint**: the caller is responsible for retry. Most actor
  traditions treat delivery as at-least-once with idempotency as the
  answer. Orleans explicitly inverts this.

## Sources

### Erlang/OTP

- Armstrong, Joe. "Making Reliable Distributed Systems in the Presence
  of Software Errors." PhD thesis, Royal Institute of Technology,
  Stockholm, 2003. https://erlang.org/download/armstrong_thesis_2003.pdf

- Erlang/OTP Design Principles — Supervisor Behaviour.
  https://www.erlang.org/doc/system/sup_princ.html

- Erlang OTP gen_statem documentation.
  https://www.erlang.org/doc/system/statem.html

- Hebert, Fred. "The Zen of Erlang."
  https://ferd.ca/the-zen-of-erlang.html

- Hebert, Fred. "Learn You Some Erlang for Great Good!"
  https://learnyousomeerlang.com/

### Akka Typed / Apache Pekko

- Akka Typed style guide.
  https://doc.akka.io/libraries/akka-core/current/typed/style-guide.html

- Akka Actor Systems (general docs).
  https://doc.akka.io/docs/akka/2.5/general/actor-systems.html

- Akka Java Memory Model.
  https://doc.akka.io/docs/akka/2.5/general/jmm.html

- Akka Typed fault tolerance.
  https://doc.akka.io/docs/akka/2.5/typed/fault-tolerance.html

- Pekko Typed interaction patterns.
  https://pekko.apache.org/docs/pekko/1.0/typed/interaction-patterns.html

- Bernhardt, Manuel. "Akka anti-patterns: shared mutable state."
  https://manuel.bernhardt.io/2016/08/02/akka-anti-patterns-shared-mutable-state

- Bernhardt, Manuel. "Tour of Akka Typed: Protocols and Behaviors."
  https://manuel.bernhardt.io/2019/07/11/tour-of-akka-typed-protocols-and-behaviors/

- scala-best-practices, Section 5 — Actors.
  https://github.com/alexandru/scala-best-practices/blob/master/sections/5-actors.md

### Microsoft Orleans

- Orleans overview.
  https://learn.microsoft.com/en-us/dotnet/orleans/overview

- Orleans best practices.
  https://learn.microsoft.com/en-us/dotnet/orleans/resources/best-practices

- Orleans FAQ.
  https://learn.microsoft.com/en-us/dotnet/orleans/resources/frequently-asked-questions

- Orleans grain lifecycle.
  https://learn.microsoft.com/en-us/dotnet/orleans/grains/grain-lifecycle

### Rust Actor Libraries

- Ryhl, Alice. "Actors with Tokio."
  https://ryhl.io/blog/actors-with-tokio/

- barafael. "More Actors with Tokio."
  https://barafael.github.io/posts/more-actors-with-tokio/

- Axiom crate docs.
  https://docs.rs/axiom/latest/axiom/

- Ractor crate docs.
  https://docs.rs/ractor/latest/ractor/

- Actix actor docs.
  https://actix.rs/docs/actix/actor

- Kameo GitHub.
  https://github.com/tqwewe/kameo

- RustFAQ. "How to Use the Actor Model in Rust."
  https://www.rustfaq.org/en/how-to-use-the-actor-model-in-rust/

### Sans-IO

- sans-io documentation.
  https://sans-io.readthedocs.io/

- Firezone blog. "Sans-IO in Rust."
  https://www.firezone.dev/blog/sans-io

- Swatinem. "The sans-io pattern."
  https://swatinem.de/blog/sans-io-pattern/

### Dataflow

- Morrison, J. Paul. Flow-Based Programming website.
  https://jpaulmorrison.com/fbp/

- Morrison, J. Paul. FBP Scheduling Rules.
  https://jpaulmorrison.com/fbp/schedrls.shtml

- Wikipedia: Kahn Process Networks.
  https://en.wikipedia.org/wiki/Kahn_process_networks

- UT Austin EE382C: Process Networks.
  https://users.ece.utexas.edu/~bevans/courses/ee382c/lectures/

- Reactive Streams specification.
  https://github.com/reactive-streams/reactive-streams-jvm/blob/master/README.md

- Reactive Manifesto (v2.0).
  https://www.reactivemanifesto.org/

- McSherry, Frank. "Timely Dataflow reboot." 2014.
  http://www.frankmcsherry.org/dataflow/naiad/2014/12/27/Timely-Dataflow.html

- McSherry, Frank. "Differential Dataflow." 2015.
  http://www.frankmcsherry.org/differential/dataflow/2015/04/07/differential.html

- Murray, McSherry et al. "Naiad: A Timely Dataflow System." SOSP 2013.
  https://sigops.org/s/conferences/sosp/2013/papers/p439-murray.pdf

### AI-Agent Skills

- rivet-gg/actor-core CLAUDE.md.
  https://github.com/rivet-gg/actor-core/blob/main/CLAUDE.md

- apify/agent-skills: apify-actor-development SKILL.md.
  https://github.com/apify/agent-skills

- proyecto26/system-design-skills.
  https://github.com/proyecto26/system-design-skills
