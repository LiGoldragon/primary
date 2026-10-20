<!-- to-the-living:start -->
Presentation.{ «The Nexus: the vision, 2nd edition» }

# The Nexus: the vision, 2nd edition

```
            +-----------+
            |  Caller   |
            +-----------+
              |      ^
   sends      |      |  replies to
   signal to  v      |
+------------- Nexus -------------+
|           +-----------+         |
|           |  Signal   |         |
|           +-----------+         |
|             |      ^            |
|  hands its  |      | returns    |
|  intent to  v      | outcome to |
|           +-----------+         |
|           | Operation |         |
|           +-----------+         |
|             |      ^            |
|  asks a     |      | answers    |
|  change of  v      | success or |
|                    | failure to |
|           +-----------+         |
|           |  Memory   |         |
|           +-----------+         |
+---------------------------------+
                 ^
                 | enforces the one path of
      +---------------------+
      |  standard entry     |
      |  point              |
      +---------------------+
```

```
+--------------+      +--------------+
| Repository A |      | Repository B |
+--------------+      +--------------+
       |                     |
       | holds               | holds
       v                     v
+--------------+      +--------------+
| datom payload|      | datom payload|
+--------------+      +--------------+
        \                   /
         \  are read by    /
          v               v
        +-------------------+
        |        CLI        |
        +-------------------+
                  |
                  | sends each, in turn, on
                  v
        +-------------------+
        | Nexus meta socket |
        +-------------------+
                  |
                  | loads all at once into
                  v
        +-------------------+
        |      Memory       |
        +-------------------+
```

## Proposal 1: psyche-context › skills/vision-nexus.md

```
  The basic ontology of an actor and dataflow system is designed before
- implementation; signal and sema are designed against it as if new, the
+ implementation; Signal, Operation and Memory are designed against it as if new, the
  old code at most inspiration.
```

```
- The nexus and sema documents are undesigned; when they are designed
+ The Operation and Memory documents are undesigned; when they are designed
  they live in the Nexus's main repository.
```

```
  Its executable holds a default configuration as a constant. On start
- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database
  that exists holds the configuration; a database created new is
```

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › skills/vision-nexus.md

```
- ## Actors
+ ## The engine
```

```
- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed. Arc-Mutex is permitted.
+ Whether the engine inside a Nexus is built of actors, or of something better named, is settled once it has been tried in practice.
+ Arc-Mutex is permitted.
```

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › skills/vision-nexus.md

```
  A Nexus has three parts, each its own ethos specification: Signal is what it says, Operation is what it does, Memory is what it remembers. Nexus always names the whole; the part that does is Operation. Every effect has a matching operation type. A signal reaches memory only through operation; memory answers operation that the change succeeded or failed; the answer returns through operation and leaves as a signal. Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ The three parts, and how each of them divides, are most of the machine's anatomy.
+ 
+ A standard entry point, like a Rust macro, enforces the three parts and their one path, so nothing bypasses them; the bodies are written by hand.
```

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › skills/vision-nexus.md

```
  Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ An effect may be an algorithm over data or a wrapped command, such as a Nix build; its operation is the interface around it.
```

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › skills/vision-nexus.md

```
  Reading a Nexus's ethos alone shows every object and process on that path.
+ 
+ A Memory record type that changes form carries the operation that upgrades each record from its old form into its new one.
```

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › skills/vision-nexus.md

```
  A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ 
+ A Nexus's payloads, its configuration among them, are written in datom. A Nexus that needs a value from a datom file gets it through its CLI, never by reading the text itself.
```

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › skills/vision-nexus.md

```
  A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ 
+ The code that identifies a CLI's caller lives in one library that every Nexus's CLI shares, so no CLI writes it again and it reads plainly. It is never user-facing and never configurable.
```

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › skills/vision-nexus.md

```
  Signal is the messaging layer: an rkyv binary archive, typed, validated on receive, length-prefixed on the socket; nothing else rides the wire. Every reply is typed, refusals included: errors are vocabulary, never strings. The wire vocabulary's version is its contract crate's semver.
+ 
+ Signal defines the forms a message can take: a simple form, without the flow id, for common queries and replies; and an extended form for the technical side, for debugging and for other components.
```

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › skills/vision-nexus.md

```
  every Nexus has one, since without it nothing could configure the
- Nexus. A Nexus that needs more levels of access opens more sockets.
+ Nexus. A Nexus that needs more levels of access may open more sockets.
+ In the long term a Nexus knows who called each socket and checks each caller's access itself, and needs no more sockets for it.
```

Ruling: land, amend, or reject.

## Proposal 10: psyche-context › skills/vision-nexus.md

```
  Each Nexus runs on its own and is recompiled on its own, toward zero-downtime self-update, one problem at a time.
+ 
+ Functionality may be put into one Nexus and moved into another once its best anatomy and the home of its data are known; it is offloaded while it still runs on the first. A Nexus may also reuse another Nexus's function, or take it in.
```

Ruling: land, amend, or reject.

## Proposal 11: psyche-context › skills/vision-nexus.md

```
  Everything built from now on is a Nexus, and what was built in
  another shape is rewritten as one. The consistency creates
  reliability, quality, and clarity.
+ 
+ ## Short term
+ 
+ Ethos and the Nexus are the basic infrastructure; Chronos is the example built with them, as a Nexus. The Nexus then guides Flow, and Flow guides the other nexuses.
```

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

```
+ Nexuses are the long term. A component may run as a Clojure prototype derived from the same Ethos, carrying EDN payloads where a Nexus carries datom. A prototype is described in its own terms and never in a Nexus's: the meta socket is a Nexus's.
+ 
+ A Nexus's configuration may live in separate files in different repositories, each a datom payload for that Nexus. Its CLI sends them one after another on the meta socket, and the Nexus loads them atomically, even at different layers. This is how a Nexus is started until one datom can draw in another by its path.
```

Ruling: land, amend, or reject.

## Proposal 12: psyche-context › skills/vision-nexus.md

```ethos
  [ FlowId.Integer                         ; types
-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer
+   Metaflow.{ Aspect Topic Layer }
+                           ; who a flow is
    Aspect.[ Psyche Mind Field ]
+   Topic.String            ; core is the default
    Layer.[ Primary Secondary Tertiary Quaternary ]

  Signal                                   ; what Flow says, on its ordinary socket
- [ flow:[ FlowId Voice Event ] ]          ; imports from the Library
- [ Launch.{ Voice                         ; queries
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports from the Library
+ [ Launch.{ Metaflow       ; queries
             Brief.String }
    Report.{ FlowId Event } ]
  [ Launched.FlowId                        ; responses
    Refused.[ NoCapsule
-             VoiceBusy.Voice ]
+             MetaflowBusy.Metaflow ]

  Operation                                ; what Flow does: one operation for every effect
- [ flow:[ FlowId Voice Event ] ]          ; imports
- [ Start.{ Voice Capsule }                ; operations
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports
+ [ Start.{ Metaflow Capsule }
+                           ; operations

  Memory                                   ; what Flow remembers
- [ flow:[ FlowId Voice Event ] ]          ; imports
+ [ flow:[ FlowId Metaflow Event ] ]
+                           ; imports
  [ Flow.{ FlowId                          ; record types
-          Voice
+          Metaflow
           State.[ Running Ended ]

- Launch.{ { Psyche Primary } «Draft the Nexus book» }      ; 1 Query, typed at the CLI, sent as signal
- Start.{ { Psyche Primary } { /home/li/primary [] } }      ; 2 Operation, from Signal's intend
- Flow.{ 7 { Psyche Primary } Running [ Started ] }         ; 3 the Change Operation hands Memory
+ ; 1 Query, typed at the CLI, sent as signal
+ Launch.{ { Psyche core Primary }
+          «Draft the Nexus book» }
+ ; 2 Operation, from Signal's intend
+ Start.{ { Psyche core Primary }
+         { /home/li/primary [] } }
+ ; 3 the Change Operation hands Memory
+ Flow.{ 7 { Psyche core Primary }
+        Running [ Started ] }
```

Ruling: land, amend, or reject.

## Proposal 13: primary › flows/445410/vision/nexus.md

**Destroy** The working order that closes the configuration record of 2026-10-09, to ratify it and to have Mind build it, is cut out of the record. The vision in the record stays, and is archived with the landing of Proposal 11.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
