# Actor System Boundaries

Research session, 2026-08-21. Psyche direction in `psyche/Vision/actorLibrary.md`:
the whole actor subject deserves its own discussion.

This report investigates the proper, reasonable boundaries of an actor system:
where the field draws the line between "this deserves to be an actor" and "this
is an actor costume on a function/struct." It does not propose a ruling; the
ruling belongs to the psyche.

Context files read: `reports/SkillDrafts/softwareDesign/draft.md`,
`reports/ActorLibraryNexusSkillReview-2026-08-21.md`,
`reports/KameoForkReview-2026-08-21.md`.

## Table of Contents

1. [The Erlang School's Boundary](#1-the-erlang-schools-boundary)
2. [Actor Anti-Patterns: Documented and Sourced](#2-actor-anti-patterns-documented-and-sourced)
3. [The Sans-IO Argument](#3-the-sans-io-argument)
4. [CSP vs. Actors](#4-csp-vs-actors)
5. [Disconfirming Evidence: Fine-Grained Actors That Worked](#5-disconfirming-evidence-fine-grained-actors-that-worked)
6. [Convergent Boundary Criteria](#6-convergent-boundary-criteria)
7. [Reading the Boundary Against the Three-Part Machine](#7-reading-the-boundary-against-the-three-part-machine)
8. [Observations, Hypotheses, and Unknowns](#8-observations-hypotheses-and-unknowns)
9. [Sources](#9-sources)

## 1. The Erlang School's Boundary

The foundational text is the Erlang Programming Rules and Conventions document,
co-authored by Armstrong, Eriksson, and Williams (Ericsson EPK/NP 95:035, 1996).
Two sections are directly on point.

Section 5.2:

> "Processes are the basic system structuring elements. But don't use processes
> and message passing when a function call can be used instead."

Section 5.4:

> "When deciding whether to implement things using sequential or parallel
> processes then the structure implied by the intrinsic structure of the problem
> should be used. The main rule is: 'Use one parallel process to model each
> truly concurrent activity in the real world'. If there is a one-to-one mapping
> between the number of parallel processes and the number of truly parallel
> activities in the real world, the program will be easy to understand."

Armstrong's PhD thesis (2003) states the 1:1 mapping principle even more
sharply (secondary-verified via multiple derivative sources):

> "It is extremely important that the mapping is exactly 1:1. The reason for
> this is that it minimizes the conceptual gap between the problem and the
> solution. If this mapping is not 1:1 the program will quickly degenerate, and
> become difficult to understand."

Armstrong in "Programming Erlang" on granularity:

> "The best thing to do is create a lagom number of processes. Erlang comes from
> Sweden, and the word lagom loosely translated means 'not too few, not too
> many, just about right.'"

Armstrong in an Erlang Solutions interview (2014):

> "If we have 100,000 people using a telephone exchange, we have 100,000
> parallel activities going on. The natural way to model this is with 100,000
> processes grouped into pairs."

Fred Hebert in "Learn You Some Erlang" (the practitioner's counterweight):

> "Parallelism is not the answer to every problem. In some cases, going parallel
> will even slow down your application."

> "It should be noted that using one process per event to be reminded of is
> likely going to be overkill and hard to scale in a real world application."

**Key observation about the Erlang school's negative case.** Armstrong never
enumerates what should NOT be a process. The negative case is defined entirely
by the absence of its positive criterion: if an activity is not concurrent in
the real world, use a function call. No list of prohibited actor uses exists in
the Erlang tradition's own writings. The Programming Rules document provides
the only explicit negative formulation (5.2 above). The official OTP Design
Principles documentation (erlang.org) contains no guidance on when NOT to use a
process; it exclusively describes how to structure processes that already exist.

## 2. Actor Anti-Patterns: Documented and Sourced

### 2.1 Actors as Code Organization

The strongest documented anti-pattern, and the only one explicitly named by an
official language authority.

Official Elixir GenServer documentation (v1.20):

> "A GenServer, or a process in general, must be used to model runtime
> characteristics of your system. A GenServer must never be used for code
> organization purposes."

> "Use processes only to model runtime properties, such as mutable state,
> concurrency and failures, never for code organization."

Official Elixir Process Anti-Patterns guide:

> "code organization must be done only through modules and functions"

> "If the number of calls to this single process grows, this code organization
> can compromise the system performance"

Source weight: this is official language documentation from the Elixir core
team, not a blog post. It is the strongest possible authority short of
Armstrong's own writings.

### 2.2 Actor-per-Object

The OOP mapping failure: treating actors as class instances rather than
concurrent activities.

Manuel Bernhardt, "Akka anti-patterns: too many actors" (2018):

> "It is true that actors are lightweight and you can run millions of them on
> a single JVM. You can. But should you?"

> "your system will perform a lot better with just 4 actors, because there will
> only be minimal overhead"

From underjord.io, "Unpacking Elixir: The Actor Model":

> "For people coming from OOP to Elixir there is often an attempt to map a
> class to a GenServer module and object instantiation to `start_link` and
> `init`. This is generally an anti-pattern."

Source weight: Bernhardt's series is the most-cited community reference for
Akka anti-patterns, referenced in conference talks and training materials, but
it is a practitioner blog. The underjord.io post is a single practitioner
source.

### 2.3 Stateless Actors

Manuel Bernhardt, "Akka anti-patterns: stateless actors" (2018):

> "using actors that don't have state is somewhat odd, to say the least"

> "don't use actors if you don't have state - that's not what they're meant for"

> "actors are really meant to deal with long-lasting computation that holds state"

> "For those [one-shot computations], Futures are an excellent abstraction"

### 2.4 Ask-Pattern Overuse

Ask-pattern overuse turns actors into synchronous RPC services, inverting the
purpose of asynchronous message passing.

Bartosz Sypytkowski, "Don't Ask, Tell":

> "Unlike `Tell` - which simply sends a message with fire and forget semantics -
> `Ask` is request/response based communication pattern."

> "`Ask` a lot heavier - and we're talking about dozens times heavier - operation
> than using simple `Tell`."

> "request/response is inherently blocking communication pattern"

> "each `Ask` call is actually allocating a special kind of lightweight
> listener-actor"

Official Akka documentation, "Interaction Patterns" -- under problems with
ask between two actors:

> "There can only be a single response to one `ask`"

> "When `ask` times out, the receiving actor does not know and may still process
> it to completion, or even start processing it after the fact"

> "Finding a good value for the timeout, especially when `ask` triggers chained
> `ask`s in the receiving actor"

**Observation on our codebase.** Both persona and persona-spirit use the ask
pattern (`actor_ref.ask(SomeMessage).await`) as the primary call pattern. The
`SpiritActorRuntime` wrapper explicitly hides `.ask()` machinery behind a typed
non-actor-aware public API (`submit_text`, `submit_request`), which is the
correct mitigation: ask is internal plumbing, not the public contract. The
external ask-pattern exposure is present but partially contained.

### 2.5 Deep Supervision Over Trivial State

No source was found that names this anti-pattern directly in those words. The
documented principle is its inverse: supervision depth should be proportional
to the importance of the state being protected.

Official Akka documentation, "Actor Systems":

> "Top-level actors are the innermost part of your Error Kernel, so create them
> sparingly"

> "If one actor carries very important data (i.e. its state shall not be lost if
> avoidable), this actor should source out any possibly dangerous sub-tasks to
> children it supervises"

The anti-pattern -- unnecessary supervision depth over stateless or replaceable
actors -- is implied by these criteria but not explicitly named in any found
source.

## 3. The Sans-IO Argument

The sans-IO position is that protocol logic should be a pure state machine --
no I/O, no actor, no runtime. This structurally removes the need for actors in
the logic layer without explicitly arguing against them.

The canonical Python-ecosystem source (sans-io.readthedocs.io):

> "By implementing network protocols without any I/O and instead operating on
> bytes or text alone, libraries allow for reuse by other code regardless of
> their I/O decisions."

> "by not simply abstracting out the I/O it allows users of the library to drive
> the network interactions themselves, not the network protocol library itself"

> "Writing to and reading from memory never fails"

Brett Cannon's essay:

> "to work with any sort of I/O the network protocol library needs to operate
> sans I/O; working directly off of the bytes or text coming off the network is
> the most flexible."

Rust ecosystem -- Firezone blog, "Sans-IO Pattern in Rust Networking Code":

> "The core idea of sans-IO is similar to the dependency inversion principle
> from the OOP world."

> "Our protocols are implemented as pure state machines. Even time is abstracted
> away."

> "In a sans-IO design we only have synchronous APIs, i.e. none of the functions
> on a state machines ever block on IO or time."

> "sans-IO code is essentially side-effect free and thus lends itself extremely
> well for (unit) tests."

The Firezone article explicitly contrasts sans-IO with actor-based approaches:
actors require channels and data copying, whereas sans-IO avoids that overhead
through direct state mutation using `&mut self`.

The canonical Rust implementation of this principle is `quinn-proto`:

> "quinn-proto: Deterministic state machine of the protocol which performs no
> I/O internally and is suitable for use with custom event loops"

> "quinn-proto contains a fully deterministic implementation of QUIC protocol
> logic and contains no networking code and does not get any relevant timestamps
> from the operating system."

**Structural implication.** Once protocol logic is a pure `&mut self` state
machine, no actor infrastructure is needed for the logic itself. I/O,
scheduling, and concurrency become caller concerns. The sans-IO model is not a
statement against actors; it is a statement about where in the design actors can
live. An actor can own a sans-IO state machine; the state machine itself is not
an actor.

## 4. CSP vs. Actors

CSP and actors answer structurally different questions, which means debates
between them often talk past each other.

> "CSP lets you name the pipe of communication; Actor lets you name the other
> end of communication."

Source: harold2017.github.io (synthesizing the Go/Erlang design traditions)

In CSP (Go channels): goroutines are anonymous; channels have identity, can
have multiple readers and writers, and can be passed around. In actors
(Erlang/Akka): processes have identity (PID); you send to a process; each
process has one mailbox; only one receiver.

CSP advantages (from golang-nuts community discussion):

> "In general with CSP-style concurrency it is much easier to get process
> synchronization right."

CSP's synchronous blocking prevents unbounded mailbox growth (a documented
actor failure mode), makes backpressure natural, and enables `select`-based
composition. CSP wins for: pipelines, worker pools, cancellation signaling,
bounded queues, local concurrency, cases where ordering guarantees matter.

Actor advantages:

> "Actors have an advantage when used for distributed systems...through the
> principle of supervision."

> "When a process has identity, you can monitor its lifetime...when they
> terminate, other processes will have a message delivered."

> "Actors don't share memory, they can be distributed or can even migrate from
> one node to another."

Actors win for: long-lived stateful entities, distributed systems requiring
location transparency, systems requiring OTP-style fault tolerance and hot
upgrades.

**Key asymmetry.** CSP is a synchronization primitive (shared channel); actors
are an encapsulation primitive (identity + mailbox). Choosing between them is
not "which concurrency model is better" but "what is the primary design
requirement: synchronization or encapsulation?"

## 5. Disconfirming Evidence: Fine-Grained Actors That Worked

### 5.1 Microsoft Orleans Virtual Actors

Official Microsoft documentation:

> "Actors are purely logical entities that always exist, virtually. An actor
> cannot be explicitly created nor destroyed, and its virtual existence is
> unaffected by the failure of a server that executes it. Since actors always
> exist, they are always addressable."

> "Orleans targets applications with a significant number of loosely coupled
> entities (hundreds, millions, billions, and even trillions)."

Production scale: Halo statistics service used a PlayerGrain per player -- one
grain per game entity, serving tens of millions of players. Used in Azure, Xbox,
Skype, Halo, PlayFab, Gears of War.

What made fine granularity work in Orleans: the runtime absorbs four problems
the developer would otherwise manage manually: (1) actor placement across
servers, (2) automatic activation on demand, (3) deactivation of idle actors to
free memory, (4) transparent recovery after server failure. Without these four
runtime properties, per-entity granularity would be impractical.

### 5.2 Erlang/BEAM Lightweight Processes

Official Erlang efficiency guide:

> "A newly spawned Erlang process uses 327 words of memory."

> "The default initial heap size of 233 words is quite conservative to support
> Erlang systems with hundreds of thousands or even millions of processes."

On 64-bit systems, 327 words is approximately 2,616 bytes per process. 1 million
Erlang processes cost approximately 0.93 GiB of RAM.

WhatsApp production evidence (getstream.io, citing WhatsApp's published
engineering):

> "Each WhatsApp user connection runs in its own Erlang process. These aren't
> operating system processes or threads; they're Erlang's internal concept using
> just 300 bytes of memory each."

> "A server with 64GB of RAM can theoretically run over 200 million of these
> processes, though practical limits like network sockets cap it at 2-3 million
> connections per server."

WhatsApp ran one Erlang process per TCP connection. At 2 million connections per
server, that is 2 million Erlang processes on a single machine.

### 5.3 Akka

Official Akka documentation:

> "they weigh in at an overhead of only roughly 300 bytes per instance"

> "there may be millions of actors within one such system, after all the mantra
> is to view them as abundant"

### 5.4 What Made Fine Granularity Work -- Common Properties

Across all three systems, five properties enabled fine-grained actors to be
practical rather than catastrophic:

1. Sub-kilobyte per-actor memory cost (BEAM ~2.6 KB, Akka ~300 bytes)
2. Runtime-managed lifecycle -- Orleans activates/deactivates automatically;
   Erlang processes are GC'd on termination
3. Single-threaded execution per actor -- eliminates locks within an actor
4. Scheduler independence from OS threads -- BEAM and Akka multiplex millions
   of actors over a fixed thread pool
5. Location transparency (Orleans) -- per-entity granularity works at cluster
   scale without developer-managed placement

The design question is not "can the developer manage this many actors?" but
"can the runtime manage this many actors?" Fine-grained actors fail when the
runtime does not absorb these costs.

**Weight note.** The WhatsApp figure is cited via getstream.io, not directly
from WhatsApp's engineering blog. The Erlang efficiency guide figures are
primary-source verified.

## 6. Convergent Boundary Criteria

The criterion most universally stated across all literature:

**Isolated Turn Principle** -- De Koster, Van Cutsem, De Meuter (2016),
"43 Years of Actors":

> "Each actor is an independent processing unit with its local state shielded
> from other actors. Actors can only interact by sending asynchronous messages
> to each other to tell them what to do."

This is the foundational criterion: an actor owns mutable state and processes
messages sequentially. Every other criterion flows from this.

The six properties that the field converges on as justifications for actor-hood:

**1. Own mutable state (serialized access).** If state mutation must be
serialized across concurrent callers, an actor is a natural solution. If state
is immutable after creation, or if only one thread ever touches it, an actor
adds only overhead.

**2. Own lifecycle.** If a component has a distinct start, running, and
stop phase -- and if managing that lifecycle manually in calling code would be
burden -- an actor lifecycle (`on_start`, `on_stop`) pays for itself. If the
lifecycle is just "exists as long as its caller," a struct suffices.

**3. Own failure domain.** Armstrong in Erlang Solutions (2014):

> "I wasn't really interested in concurrency as such. I was interested in how
> you make fault-tolerant systems."

If a component can fail independently and the rest of the system must survive
its failure, supervision and `let it crash` justify actor-hood. If failure of
the component equals failure of the whole program, supervision adds nothing.

**4. True concurrency in the world.** Armstrong's 1:1 mapping principle: one
actor per concurrent activity in the real world. If the component does not model
something that is concurrent in the world, an actor misrepresents the problem.

**5. Own pacing / backpressure.** If a component produces or consumes at its
own rate, and the mailbox is the natural place to absorb burst, an actor's
bounded mailbox is legitimate. If throughput is determined entirely by the
caller's rate, an actor's mailbox is unnecessary buffering.

**6. Distribution / location transparency.** If the component must run on
another machine or migrate, actor identity across nodes (Erlang PID,
Orleans grain key) pays for itself. For in-process work, this criterion does
not apply.

The most direct prescriptive statement found in the literature is from
Microsoft Orleans best practices:

Use actors when:
> "Significant number (hundreds, millions, billions, and even trillions) of
> loosely coupled entities."
> "Entities are small enough to be single-threaded."
> "Workload is interactive." -- "request-response, start/monitor/complete."
> "More than one server is expected or may be required."

Do NOT use actors when:
> "Memory must be shared between entities."
> "A small number of large entities may be multithreaded."
> "Global coordination and/or consistency are needed."
> "Operations that run for a long time. Batch jobs, Single Instruction Multiple
> Data (SIMD) tasks."

**No source found** offers a systematic checklist of all six criteria together
as explicit go/no-go tests for actor-hood. The closest is the Orleans best
practices page. The academic literature (Hewitt 1973, Agha 1986) is prescriptive
about what actors ARE, not prescriptive about when NOT to use them.

**The least-documented criterion relative to its practitioner importance:** own
failure domain. Hewitt and Agha barely mention it; it dominates Erlang/OTP
design philosophy and is Armstrong's stated primary motivation.

**Convergence table:**

| Criterion | Hewitt 1973 | Agha 1986 | De Koster 2016 | Akka | Orleans | Armstrong/Erlang |
|---|---|---|---|---|---|---|
| Own mutable state (serialized) | definitional | definitional | Isolated Turn | yes | yes | yes |
| Own lifecycle | implicit | yes | -- | explicit | explicit | yes |
| Own failure domain | -- | -- | -- | explicit (supervision) | explicit | yes (primary) |
| True concurrency in world | definitional | definitional | yes | yes | yes | yes (COP thesis) |
| Own mailbox/pacing | definitional | yes | yes | explicit | -- | yes |
| Location transparency | definitional | yes | -- | explicit | yes (virtual actor) | yes |

## 7. Reading the Boundary Against the Three-Part Machine

This section frames the research as an assessment, not a ruling. The ruling
belongs to the psyche.

**The three-part machine:**

    agglomerate multiple types --> create a coherent type --> convert it onward

**Where actors have no claim.**

The conversion arrow (`-->`) is the clearest case. Conversions in the machine
are demand-driven, stateless transformations: `TryFrom<(Registry, AssemblyFile)>`
produces a `ResolvedAssembly`; `TryFrom<ResolvedAssembly>` produces
`AssembledRust`. These conversions have no ongoing lifecycle, no failure domain
independent of the calling program, no pacing need, and no concurrency in the
world. The Elixir official documentation names the anti-pattern exactly:
"A GenServer must never be used for code organization purposes. Use processes
only to model runtime properties, such as mutable state, concurrency and
failures, never for code organization." Using actors to implement the conversion
arrows is code organization under the name of concurrency.

The pre-output type in the machine (the `AssembledRust` assembled whole in
memory before writing) has the same profile: it is immutable after creation, it
has no lifecycle, and it needs no serialized access. The actor criterion for own
mutable state does not apply.

**Where actors may have a claim.**

The input side of the agglomerate step, when inputs arrive concurrently over
time. If `Registry` is updated by concurrent writers while being read by the
conversion, a `RegistryStore` actor (own mutable state, serialized access) is
justified. This is the pattern already in use in `ManagerStore` (persona) and
`RecordStore` (persona-spirit): actors that wrap mutable persistent state with
their own lifecycle and their own failure domain.

A coherent type that is long-lived and serves concurrent requests is also a
plausible actor home. The persona-spirit `SpiritRoot` and its supervised
children model this: the root is a long-lived stateful entity with an
independent failure domain and supervised children that can restart
independently.

**The risk specific to the three-part machine.**

The machine's design discipline -- types first, conversions as the spine, map
before code -- creates an ordering temptation: one actor per stage. The risk is
that the three-part decomposition (agglomerate, coherent, convert) is mistaken
for a runtime pipeline, and each part becomes an actor. This would produce
exactly what Bernhardt calls "too many actors" and what the Elixir documentation
calls actors used for code organization: actors with no own lifecycle, no failure
domain, and no pacing need, chained by ask-pattern calls that turn the pipeline
into synchronous RPC.

The sans-IO argument is relevant here. If the agglomerate and coherent steps
are pure state machines -- bytes in, events out, `&mut self` -- they can run
inside an actor that owns the I/O boundary without themselves being actors. The
actor sits at the I/O boundary; the machine logic inside it is a pure function.
This is the structure of `quinn-proto`: the protocol is a pure state machine;
the actor (or any other I/O driver) is a thin shell around it.

**The legitimate actor positions in the machine:**

- An actor that holds mutable persistent state read and written by multiple
  concurrent instances of the machine running in parallel (a `RegistryActor`
  shared across requests)
- An actor that owns a connection or session with its own lifecycle and failure
  domain, driving the three-part machine for each request it receives
- An actor at the system boundary (network ingress, storage) that translates
  external events into typed inputs for the machine

**The anti-pattern positions:**

- An actor per conversion step, where the conversion is a pure function
- An actor per coherent type, where the type is immutable after creation
- A supervision tree over conversion actors that have no independent failure
  domain (failure of one = failure of all)
- Ask-pattern chains connecting conversion actors, producing synchronous RPC
  across actor boundaries where a function call would serve

## 8. Observations, Hypotheses, and Unknowns

**Observations (documented, sourced):**

- The canonical Erlang rule is narrow and structural: one process per concurrent
  activity in the real world; function calls for everything else. Armstrong
  never enumerates what should NOT be a process.
- The Elixir official documentation is the only language-level authority that
  explicitly names "actors as code organization" as an anti-pattern.
- The Bernhardt anti-patterns series is the most-cited community reference for
  Akka anti-patterns, but it is a practitioner blog.
- Sans-IO structurally removes the need for actors in the protocol logic layer
  without explicitly arguing against actors.
- CSP and actors answer different questions (synchronization vs. encapsulation);
  the debate between them often treats them as alternatives to the same problem.
- Fine-grained actors (BEAM, Orleans, Akka) work when the runtime absorbs
  lifecycle management, placement, and proliferation costs.
- The "actors as code organization" anti-pattern exactly matches the risk of
  using actors to model the conversion arrows in the three-part machine.
- The ask-pattern overuse described in the Akka literature is structurally
  present in persona and persona-spirit's internal actor plumbing, but is
  partially mitigated by the `SpiritActorRuntime` wrapper.
- Both `Arc<Mutex>` occurrences in the codebase are intra-actor coordination,
  consistent with the criterion that inter-actor shared state is the violation,
  not intra-actor coordination.

**Hypotheses (not directly documented, implied by the evidence):**

- The "actors become ridiculous" boundary is reached when an entity lacks ALL
  of: own lifecycle, own failure domain, own pacing, true concurrency, mutable
  state needing serialized access, and distribution needs. If none of these
  apply, an actor adds only overhead and conceptual distance.
- The OOP-to-actors mapping failure (class = actor) occurs because OOP objects
  have identity and encapsulated state but lack the concurrency/lifecycle/failure
  properties that justify actor-hood.
- The ask-pattern overuse problem is fundamentally about using an asynchronous
  abstraction to simulate synchronous semantics, which is the inverse of what
  actors are designed for. When every message is an ask, the actor system has
  become an RPC framework with more overhead than needed.

**Unknowns:**

- No academic paper systematically cataloguing actor anti-patterns was found.
  The anti-pattern literature is entirely practitioner-sourced.
- Armstrong's "Programming Erlang" book likely contains more detailed guidance
  on process granularity than is available via search; relevant sections were
  behind paywalls and could not be fetched directly.
- The Armstrong PhD thesis PDF (2003) was unreadable by fetch tools; several
  quotes attributed to it are secondary-verified only.
- No source names the "deep supervision trees over trivial state" anti-pattern
  explicitly; it is implied by the supervision criteria but not catalogued.
- Whether the specific actors in persona and persona-spirit all individually
  satisfy the boundary criteria stated here has not been assessed. This report
  examines the boundary in the field, not the full actor inventory of the
  codebase.

## 9. Sources

All sources are web-retrievable unless noted as secondary-verified.

- Erlang Programming Rules and Conventions (Armstrong, Eriksson, Williams,
  Ericsson EPK/NP 95:035, 1996):
  https://cndoc.github.io/Erlang-ProgrammingRules-cn/doc_en.html

- Armstrong, Joe. "Programming Erlang." (Pragmatic Bookshelf, 2007 / 2013).
  Quotes verified via Goodreads and derivative sources; book not directly fetched.

- Armstrong, Joe. PhD thesis, "Making reliable distributed systems in the
  presence of software errors" (2003). Quotes are secondary-verified.

- Armstrong, Joe. Erlang Solutions interview (2014):
  https://www.erlang-solutions.com/blog/lets-talkconcurrency-with-joe-armstrong/

- Hebert, Fred. "Learn You Some Erlang" -- concurrency chapters:
  https://learnyousomeerlang.com/the-hitchhikers-guide-to-concurrency
  https://learnyousomeerlang.com/designing-a-concurrent-application

- De Koster, Joeri; Van Cutsem, Tom; De Meuter, Wolfgang. "43 Years of Actors."
  AGERE 2016. https://dl.acm.org/doi/10.1145/3001886.3001890

- Elixir GenServer documentation (v1.20):
  https://hexdocs.pm/elixir/GenServer.html

- Elixir Process Anti-Patterns guide:
  https://hexdocs.pm/elixir/process-anti-patterns.html

- Erlang Efficiency Guide -- Processes:
  https://www.erlang.org/doc/system/eff_guide_processes.html

- Akka documentation, "Actor Systems":
  https://doc.akka.io/libraries/akka-core/current/general/actor-systems.html

- Akka documentation, "Actors Introduction":
  https://doc.akka.io/libraries/akka-core/current/typed/guide/actors-intro.html

- Akka documentation, "Interaction Patterns":
  https://doc.akka.io/libraries/akka-core/current/typed/interaction-patterns.html

- Bernhardt, Manuel. "Akka anti-patterns: too many actors" (2018):
  https://manuel.bernhardt.io/2018/08/06/akka-anti-patterns-many-actors

- Bernhardt, Manuel. "Akka anti-patterns: stateless actors" (2018):
  https://manuel.bernhardt.io/2018/05/30/akka-anti-patterns-stateless-actors

- Bernhardt, Manuel. "Akka anti-patterns: flat actor hierarchies" (2016):
  https://manuel.bernhardt.io/2016/08/09/akka-anti-patterns-flat-actor-hierarchies-or-mixing-business-logic-and-failure-handling

- Sypytkowski, Bartosz. "Don't Ask, Tell":
  https://www.bartoszsypytkowski.com/dont-ask-tell-2/

- underjord.io. "Unpacking Elixir: The Actor Model":
  https://underjord.io/unpacking-elixir-the-actor-model.html

- Microsoft Orleans overview:
  https://learn.microsoft.com/en-us/dotnet/orleans/overview

- Microsoft Orleans best practices:
  https://learn.microsoft.com/en-us/dotnet/orleans/resources/best-practices

- Orleans (software framework), Wikipedia:
  https://en.wikipedia.org/wiki/Orleans_(software_framework)

- sans-io.readthedocs.io:
  https://sans-io.readthedocs.io/

- Cannon, Brett. "Network Protocols, Sans I/O":
  https://snarky.ca/network-protocols-sans-i-o/

- Firezone, "Sans-IO Pattern in Rust Networking Code":
  https://www.firezone.dev/blog/sans-io

- quinn-proto:
  https://github.com/quinn-rs/quinn
  https://docs.rs/crate/quinn-proto/latest

- GetStream.io, "How WhatsApp Works":
  https://getstream.io/blog/whatsapp-works/ (secondary; citing WhatsApp
  engineering publications)

- harold2017.github.io, "Actor vs. Channel":
  https://harold2017.github.io/posts/actor_in_action/actor_vs_channel/
