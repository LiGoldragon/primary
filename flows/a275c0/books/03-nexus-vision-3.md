<!-- to-the-living:start -->
Presentation.{ «The Nexus: the vision, 3rd edition» }

# The Nexus: the vision, 3rd edition

## psyche-context › vision/nexus.md

## A Nexus is the whole

A Nexus is the whole long-running component: the process, its sockets, and the signal contracts it is compiled with. Nexus is its name; daemon is not. A Nexus is like a daemon, said only so that a thinking machine which thinks in daemons understands what a Nexus is. Every Nexus is named component-nexus — orchestrate-nexus, ethos-nexus — and in everyday speech orchestrate-nexus is called orchestrate.

## A kind of thing

Nexus is our word for the style of component that speaks signal and uses a similar database.

## Library and daemon

Every component built from now on is a Nexus. The nexus repository is
the library that defines the core of a Nexus component.

## Universal traits first

The basic ontology of an actor and dataflow system is designed before
implementation; signal and sema are designed against it as if new, the
old code at most inspiration.

Every method lives in a trait; an inherent method is a trait not yet extracted. The traits and types of a Nexus are one ontology designed before any body is written; defaults wherever expressible, through rich sub-trait chains. Traits live on data-bearing types; a zero-sized type with behaviour is a namespace pretending. Identity is trait-borne: an encoded form fingerprints itself, by default the hash of its rkyv archive, and every reference names its target by that name. `fn main()` is the only free function; a missing owner is a missing type.

## Processing is for the effect

An object enters a Nexus for the effect; the response follows as an
effect of it. Conversion is the wrong frame for it. The name is open,
Apply liked.

## Documents

The nexus and sema documents are undesigned; when they are designed
they live in the Nexus's main repository.

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

A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.

## Signal only

Every client speaks to a Nexus in pure signal, fully binary. A Nexus
speaks only the signal contracts it is compiled with; two of these
are its own, one per socket. A Nexus thinks in typed values — enums,
structs, scalars — and the string fields it still carries are
records on the way to a fully typed form.

The running Nexus holds its whole domain as typed values, a specific type for every kind; no text arrives on its wire and none leaves it. Its Memory is its own typed store, reached only through the memory engine; there is no central store; policy state and working state live in that one store, and policy changes only over the meta socket.

Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.

## The graph

A Nexus is a vertex in the graph of nexuses. An edge joins two
vertices and carries one contract. Every connected pair has an
ordinary edge; only some pairs have a meta edge. A Nexus is compiled
with the contracts of its own sockets and of every edge it has.

Peers depend on each other's wire repositories, never on each other's Nexuses.

## Routing

Signals cross the network through a router. The router tells signal
types apart by an enum that wraps the objects, held in the signal
repository, which every component depends on. That repository also
holds what every signal needs in common — the handshake payload
among it.

## Configuration

A Nexus starts with no arguments and there is no bootstrap binary.
Its executable holds a default configuration as a constant. On start
it looks for its Sema database at the default location: a database
that exists holds the configuration; a database created new is
seeded with the defaults. The meta socket carries a Configure
interface, and changed values are accepted through it.

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

`<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, never optional, since configuration flows through it. The CLI is `<nexus>`.

A wire type repository is written in ethos and declares vocabulary only: the frame envelope, the protocol version, a closed enum of operations with their paired replies, the typed payload of each; no catch-all. Operations are verbs, `Submit`; replies the past tense, `Submitted`; rejections name themselves. Storage vocabulary never appears on the public wire.

## Why everything is a Nexus

The Nexus is an architecture concept, not one specific Nexus: everything made is a Nexus.

A Nexus's vision is split by its code modules.

Everything built from now on is a Nexus, and what was built in
another shape is rewritten as one. The consistency creates
reliability, quality, and clarity.

## Actors

The engine inside a Nexus is driven by Kameo actors. The standards
of their use are still to be designed. Arc-Mutex is permitted.

## Splitting a Nexus

A Nexus deals with a domain. When its features grow too many,
splitting one or more nexuses out of it is considered.

Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.

## Observation by subscription

State is observed by subscription: the subscriber receives the state
on open, then each change as it happens.

## Polling is forbidden

Polling is forbidden; a correct system goes quiet when nothing
changes.

## Three parts and one path

A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.

```
Library                                  ; what the three parts share
[]                                       ; imports: none
[ FlowId.Integer                         ; types
  Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Event.[ Started Stopped ] ]
[]                                       ; kinds
[]                                       ; associations

Signal                                   ; what Flow says, on its ordinary socket
[ flow:[ FlowId Voice Event ] ]          ; imports from the Library
[ Launch.{ Voice                         ; queries
           Brief.String }
  Report.{ FlowId Event } ]
[ Launched.FlowId                        ; responses
  Refused.[ NoCapsule
            VoiceBusy.Voice ]
  Reported ]
[]                                       ; types

Operation                                ; what Flow does: one operation for every effect
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Start.{ Voice Capsule }                ; operations
  Record.{ FlowId Event } ]
[ Started.FlowId                         ; outcomes
  Recorded
  Failed.[ CapsuleRefused StoreRefused ] ]
[ Capsule.{ Home.String                  ; types
            Login.Vector<String> } ]

Memory                                   ; what Flow remembers
[ flow:[ FlowId Voice Event ] ]          ; imports
[ Flow.{ FlowId                          ; record types
         Voice
         State.[ Running Ended ]
         Vector<Event> } ]
```

```
Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
Succeeded                                             ; 4 Memory's answer to Operation
Started.7                                             ; 5 Outcome
Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

## Proposal 1: Memory names the store · psyche-context › vision/nexus.md

- implementation; signal and sema are designed against it as if new, the
+ implementation; Signal, Operation and Memory are designed against it as if new, the

- The nexus and sema documents are undesigned; when they are designed
+ The Operation and Memory documents are undesigned; when they are designed

- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database

Ruling: land, amend, or reject.

## Proposal 2: The engine, in place of Actors · psyche-context › vision/nexus.md

- ## Actors
- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed. Arc-Mutex is permitted.
+ ## The engine
+ Whether the engine inside a Nexus is built of actors, or of something better named, is settled once it has been tried in practice.
+ Arc-Mutex is permitted.

Ruling: land, amend, or reject.

## Proposal 3: Under Three parts and one path · psyche-context › vision/nexus.md

+ The three parts, and how each of them divides, are most of the machine's anatomy.
+ A standard entry point, like a Rust macro, enforces the three parts and their one path, so nothing bypasses them.
+ The bodies are written by hand.

Ruling: land, amend, or reject.

## Proposal 4: Under Three parts and one path · psyche-context › vision/nexus.md

+ An effect may be an algorithm over data or a wrapped command, such as a Nix build.
+ Its operation is the interface around it.

Ruling: land, amend, or reject.

## Proposal 5: Under Three parts and one path · psyche-context › vision/nexus.md

+ A Memory record type that changes form carries the operation that upgrades each record from its old form into its new one.

Ruling: land, amend, or reject.

## Proposal 6: Under Default clients · psyche-context › vision/nexus.md

+ A Nexus's payloads, its configuration among them, are written in datom.
+ A Nexus that needs a value from a datom file gets it through its CLI, never by reading the text itself.

Ruling: land, amend, or reject.

## Proposal 7: Under Default clients · psyche-context › vision/nexus.md

+ The code that identifies a CLI's caller lives in one library that every Nexus's CLI shares, so no CLI writes it again and it reads plainly.
+ It is never user-facing and never configurable.

Ruling: land, amend, or reject.

## Proposal 8: Under Signal only · psyche-context › vision/nexus.md

+ Signal defines the forms a message can take.
+ The simple form, without the flow id, is for common queries and replies.
+ The extended form is for the technical side, for debugging and for other components.

Ruling: land, amend, or reject.

## Proposal 9: Under Sockets · psyche-context › vision/nexus.md

- Nexus. A Nexus that needs more levels of access opens more sockets.
+ Nexus. A Nexus that needs more levels of access may open more sockets.
+ In the long term a Nexus knows who called each socket and checks each caller's access itself, and needs no more sockets for it.

Ruling: land, amend, or reject.

## Proposal 10: Under Splitting a Nexus · psyche-context › vision/nexus.md

+ Functionality may be put into one Nexus and moved into another once its best anatomy and the home of its data are known.
+ It is offloaded while it still runs on the first.
+ A Nexus may also reuse another Nexus's function, or take it in.

Ruling: land, amend, or reject.

## Proposal 11: Short term, a new section after Why everything is a Nexus · psyche-context › vision/nexus.md

+ ## Short term
+ Ethos and the Nexus are the basic infrastructure, and Chronos is the example built with them, as a Nexus.
+ The Nexus then guides Flow, and Flow guides the other nexuses.

```figure
+-- basic infrastructure -+
|   +-------+             |
|   | Ethos |             |
|   +-------+             |
|       | specifies       |
|       v                 |
|   +-------+             |   +-------------+
|   | Nexus |<------------+---| Chronos,    |
|   +-------+  is built as|   | the example |
+-------|-----------------+   +-------------+
        | guides
        v
    +------+
    | Flow |
    +------+
        | then guides
        v
 +---------------+
 | other nexuses |
 +---------------+
```

+ Nexuses are the long term.
+ A component may run as a Clojure prototype derived from the same Ethos, carrying EDN payloads where a Nexus carries datom.
+ A prototype is described in its own terms and never in a Nexus's: the meta socket is a Nexus's.
+ A Nexus's configuration may live in separate files in different repositories, each a datom payload for that Nexus.
+ Its CLI sends them one after another on the meta socket, and the Nexus loads them atomically, even at different layers.
+ This is how a Nexus is started until one datom can draw in another by its path.

Ruling: land, amend, or reject.

## Proposal 12: The Flow example under Three parts and one path · psyche-context › vision/nexus.md

```text
- Library                                  ; what the three parts share
- []                                       ; imports: none
- [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
-   Aspect.[ Psyche Mind Field ]
-   Layer.[ Primary Secondary Tertiary Quaternary ]
-   Event.[ Started Stopped ] ]
- []                                       ; kinds
- []                                       ; associations
-
- Signal                                   ; what Flow says, on its ordinary socket
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
-            Brief.String }
-   Report.{ FlowId Event } ]
- [ Launched.FlowId                        ; responses
-   Refused.[ NoCapsule
-             VoiceBusy.Voice ]
-   Reported ]
- []                                       ; types
-
- Operation                                ; what Flow does: one operation for every effect
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
-   Record.{ FlowId Event } ]
- [ Started.FlowId                         ; outcomes
-   Recorded
-   Failed.[ CapsuleRefused StoreRefused ] ]
- [ Capsule.{ Home.String                  ; types
-             Login.Vector<String> } ]
-
- Memory                                   ; what Flow remembers
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Flow.{ FlowId                          ; record types
-          Voice
-          State.[ Running Ended ]
-          Vector<Event> } ]
-
- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
- Succeeded                                             ; 4 Memory's answer to Operation
- Started.7                                             ; 5 Outcome
- Launched.7                                            ; 6 Response, from Signal's answer, back to the CLI
```

```ethos
+ ; what the three parts share
+ Library.
+ {
+ ; imports: none
+ []
+ ; types
+ [ FlowId.Integer
+   ; who a flow is
+   Metaflow.{ Aspect Topic Layer }
+   Aspect.[ Psyche Mind Field ]
+   ; core is the default
+   Topic.String
+   Layer.[ Primary Secondary Tertiary Quaternary ]
+   Event.[ Started Stopped ] ]
+ ; traits
+ []
+ ; associations
+ [] }
```

```ethos
+ ; what Flow says, on its ordinary socket
+ Signal.
+ {
+ ; imports from the Library
+ [ flow:[ FlowId Metaflow Event ] ]
+ ; queries
+ [ Launch.{ Metaflow
+            Brief.String }
+   Report.{ FlowId Event } ]
+ ; responses
+ [ Launched.FlowId
+   Refused.[ NoCapsule
+             MetaflowBusy.Metaflow ]
+   Reported ]
+ ; types
+ [] }
```

```ethos
+ ; what Flow does: one operation for every effect
+ Operation.
+ {
+ ; imports
+ [ flow:[ FlowId Metaflow Event ] ]
+ ; operations
+ [ Start.{ Metaflow Capsule }
+   Record.{ FlowId Event } ]
+ ; outcomes
+ [ Started.FlowId
+   Recorded
+   Failed.[ CapsuleRefused StoreRefused ] ]
+ ; types
+ [ Capsule.{ Home.String
+             Login.⟦ String ⟧ } ] }
```

```ethos
+ ; what Flow remembers
+ Memory.
+ {
+ ; imports
+ [ flow:[ FlowId Metaflow Event ] ]
+ ; record types
+ [ Answer.[ Succeeded Failed ]
+   Flow.{ FlowId
+          Metaflow
+          State.[ Running Ended ]
+          ⟦ Event ⟧ } ] }
```

```datom
+ ; 1 Query, typed at the CLI, sent as signal
+ Launch.{ { Psyche core Primary }
+          «Draft the Nexus book» }
+ ; 2 Operation, from Signal's intend
+ Start.{ { Psyche core Primary }
+         { /home/li/primary [] } }
+ ; 3 the Change Operation hands Memory
+ { 7 { Psyche core Primary }
+   Running [ Started ] }
+ ; 4 Memory's answer to Operation
+ Succeeded
+ ; 5 Outcome
+ Started.7
+ ; 6 Response, from Signal's answer,
+ ;   back to the CLI
+ Launched.7
```

Ruling: land, amend, or reject.

## Proposal 13: primary › flows/445410/vision/nexus.md

**Destroy** The working order that closes the configuration record of 2026-10-09, to ratify it and to have Mind build it, is cut out of the record; the vision in it is archived with the landing of Proposal 11.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
