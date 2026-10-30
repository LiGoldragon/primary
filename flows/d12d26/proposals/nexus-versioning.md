Presentation.{ «Versioning a Nexus» }

# Versioning a Nexus

Created by Fable (ruling and text); source by Sonnet

### Proposal 1: vision:nexus · psyche-belief › vision/nexus.md

**Comment** The three records become one statement, placed after the module's last section; its example is drawn, as the third record asks. No line of the module is removed or rewritten.

  ## A Nexus is the whole
    
  A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.
    
  ## A kind of thing
    
  Nexus is our word for the style of component that speaks signal and uses a similar database.
    
  ## Library and daemon
    
  The nexus repository is
  the library that defines the core of a Nexus component.
    
  ## Universal traits first
    
  For now, the basic ontology of an actor and dataflow system is designed
  before implementation; signal and memory are designed against it as if
  new, the old code at most inspiration.
    
  Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.
    
  ## Long term: traits in ethos
    
  Long term, every trait a Nexus uses is declared in ethos; short term, a Nexus goes without declared traits.
    
  ## Processing is for the effect
    
  An object enters a Nexus for the effect; the response follows as an
  effect of it. Conversion is the wrong frame for it.
    
  ## Sockets
    
  A Nexus opens at least two sockets. The ordinary socket serves
  ordinary peers. The meta socket is privileged — the root user of the
  Nexus — and configuration and privileged operations pass through it;
  every Nexus has one, since without it nothing could configure the
  Nexus. A Nexus that needs more levels of access opens more sockets.
    
  ## Default clients
    
  A client is a separate program from the Nexus. For now the default
  clients are packaged with the Nexus as separate crates of its
  repository, which is a multi-crate repository: one datom-converting
  CLI per socket, however many sockets the Nexus has, at least two. A
  default client serves bootstrap first, then debugging and testing,
  long after production has stopped using it. The meta CLI is named
  component-meta.
    
  A CLI turns text into Signal: it takes one inline datom as its whole input; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process. A CLI speaks to one Nexus and stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
    
  ## Signal only
    
  Every client speaks to a Nexus in pure signal, fully binary. A Nexus
  speaks only the signal contracts it is compiled with; two of these
  are its own, one per socket. A Nexus thinks in typed values — enums,
  structs, scalars — and the string fields it still carries are
  records on the way to a fully typed form.
    
  The running Nexus holds its whole domain as typed values, a specific type for every kind, and its wire carries typed values alone. Its Memory is its own typed store, reached only through the memory engine; policy state and working state live in that one store, and policy changes only over the meta socket.
    
  Signal is the messaging layer and the wire's only traffic: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket. Every reply is typed, refusals included: errors are vocabulary. The wire vocabulary's version is its contract crate's semver.
    
  ## The graph
    
  A Nexus is a vertex in the graph of nexuses. An edge joins two
  vertices and carries one contract. Every connected pair has an
  ordinary edge; only some pairs have a meta edge. A Nexus is compiled
  with the contracts of its own sockets and of every edge it has.
    
  Peers depend on each other's wire repositories.
    
  ## Routing
    
  Signals cross the network through a router. The router tells signal
  types apart by an enum that wraps the objects, held in the signal
  repository, which every component depends on. That repository also
  holds what every signal needs in common — the handshake payload
  among it.
    
  ## Configuration
    
  For now, a Nexus starts with no arguments and there is no bootstrap
  binary. Its executable holds a default configuration as a constant. On
  start it looks for its memory at the default location: a memory that
  exists holds the configuration; a memory created new is seeded with the
  defaults. The meta socket carries a Configure interface, and changed
  values are accepted through it.
    
  ## First configuration
    
  A Nexus keeps a standard metadata tree. In it a type records whether
  the meta Configure was ever done; that record is reversed only on the
  meta socket, and while it is unset Configure is accessible on the
  ordinary socket. The tree holds everything standard about the Nexus:
  its socket paths — its own and those of every edge-socket it connects
  to — and whatever else comes up as standard nexus configuration data.
  The built-in default configuration is independent of this and is
  what gives the socket path on which the Configure signal arrives.
    
  ## Repositories
    
  A component has three repositories: its main repository, holding all
  its code, and two signal repositories — one for the ordinary
  socket's contract, one for the meta socket's. Shared kinds go into
  reusable libraries, which are encouraged.
    
  `<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, always present, since configuration flows through it. The CLI is `<nexus>`.
    
  A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary stays inside the Nexus.
    
  ## Why everything is a Nexus
    
  The Nexus is an architecture concept, not one specific Nexus: everything made is a Nexus.
    
  Everything built from now on is a Nexus, and what was built in
  another shape is rewritten as one. The consistency creates
  reliability, quality, and clarity.
    
  ## Actors
    
  The engine inside a Nexus is driven by Kameo actors. The standards
  of their use are still to be designed.
    
  ## Splitting a Nexus
    
  A Nexus deals with a domain. When its features grow too many,
  splitting one or more nexuses out of it is considered.
    
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
    
  ## Observation by subscription
    
  State is observed by subscription: the subscriber receives the state
  on open, then each change as it happens.
    
  ## Change is pushed
    
  A correct system goes quiet when nothing changes; every change arrives as an event.
    
  ## Three parts and one path
    
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
    
  The library, shared by the three parts:
    
  ```ethos
  Library
  []
  [ FlowId.Integer
    Topic.String
    Aspect.[ Psyche Mind Field ]
    Layer.[ Primary Secondary Tertiary
            Quaternary ]
    Address.{ Aspect Topic Layer }
    Event.[ Started Stopped ] ]
  []
  []
  ```
    
  Signal, what the Flow Nexus says:
    
  ```ethos
  Signal
  [ flow:[ FlowId Address Event ] ]
  [ Launch.{ Address Brief.String }
    Report.{ FlowId Event } ]
  [ Launched.FlowId
    Refused.[ NoCapsule
              AddressBusy.Address ]
    Reported ]
  []
  ```
    
  Operation, what the Flow Nexus does:
    
  ```ethos
  Operation
  [ flow:[ FlowId Address Event ] ]
  [ Start.{ Address Capsule }
    Record.{ FlowId Event } ]
  [ Started.FlowId
    Recorded
    Failed.[ CapsuleRefused StoreRefused ] ]
  [ Capsule.{ Home.String
              Login.Vector<String> } ]
  ```
    
  Memory, what the Flow Nexus remembers:
    
  ```ethos
  Memory
  [ flow:[ FlowId Address Event ] ]
  [ Flow.{ FlowId Address
           State.[ Running Ended ]
           Vector<Event> }
    Answer.[ Succeeded Failed ] ]
  ```
    
  ```datom
  ; 1 Query, typed at the CLI, sent as signal
  Launch.{ { Psyche core Primary }
           «Draft the Nexus book» }
  ; 2 Operation, from Signal's intend
  Start.{ { Psyche core Primary }
          { /home/li/primary [] } }
  ; 3 the Change Operation hands Memory
  Flow.{ 7 { Psyche core Primary } Running
         [ Started ] }
  ; 4 Memory's answer to Operation
  Succeeded
  ; 5 Outcome
  Started.7
  ; 6 Response, from Signal's answer, to the CLI
  Launched.7
  ```
  
+ ## A Nexus's version
+ 
+ A Nexus's version has three numbers. Any change that leaves the memory format alone is a new revision; a change of the memory format is a new subversion, and carries the upgrade from the previous format; a complete rewrite is a new version.
+ 
+ This is an example: the Flow Nexus's line this week as it should have run, and beside it a complete rewrite.
+ 
```
+ +-----------------------+
+ | 0.40.4 (a revision)   |
+ +-----------------------+
+     | subversion: the logical-delivery
+     | table's format changed (shipped
+     | as 0.40.11); upgrade on open
+     v
+ +--------+
+ | 0.41.0 |
+ +--------+
+     | revision: the upgrade order
+     | fixed (today)
+     v
+ +--------+
+ | 0.41.1 |
+ +--------+
+ 
+ +--------------------------------------+
+ | 1.0.0: a complete rewrite, forked    |
+ | from the root commit, shares nothing |
+ +--------------------------------------+
```
