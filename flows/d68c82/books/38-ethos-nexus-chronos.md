<!-- to-the-living:start -->
Presentation.{ «Ethos, Nexus and Chronos: the vision» }

# Ethos, Nexus and Chronos: the vision

Ethos is the language of types and traits. A Nexus is the long-running component Ethos specifies, in three parts: Signal, Operation and Memory. Chronos is the first simple Nexus, built as the golden example. Flow follows from it, then the other nexuses.

```
 Ethos: the language of types and traits
   │ specifies
   ▼
 Nexus: Signal · Operation · Memory
   │ first built as
   ▼
 Chronos: the golden example
   │ then
   ▼
 Flow, then the other nexuses
```

## Proposal 1: psyche-context › vision/ethos.md

Your records disagree on which example comes first. This proposal takes your latest word, from 2026-10-16.

- ## Flow, a current best example
- Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+ ## The golden example
+ Ethos, the Nexus and the Chronos example project together are the golden example.
+ Flow is implemented properly from that golden example, then the other nexuses.

Ruling: land, amend, or reject.

## Proposal 2: psyche-context › vision/ethos.md

+ Where types are shown, the Ethos is shown, never the Rust it generates, unless the work is on how Ethos generates Rust.
+ Ethos is never shown out of context: it says what its types are for.
+ A datom is never shown without its Ethos specification.
+ A type ethos opens with `type` and defines a single type, everything inline; it may use the inline import.
+ A type ethos may carry one or more examples of its datom, inline.

Ruling: land, amend, or reject.

## Proposal 3: psyche-context › vision/ethos.md

Your words from 2026-10-02 to 2026-10-12 all name the stored part Memory, where this paragraph says Sema. This proposal takes Memory.

- Library, Signal, Operation, Memory. No version in a file. Signal's sections are
- queries and responses, since there is communication; Sema's are record
- types, the rest to be decided. Signal gives a Nexus its main types and
- Sema its database types.
+ Library, Signal, Operation, Memory. No version in a file.
+ Signal's sections are queries and responses, since there is communication; Memory's are record types, the rest to be decided.
+ Signal gives a Nexus its main types and Memory its database types.

Ruling: land, amend, or reject.

## Proposal 4: psyche-context › vision/ethos.md

The module still allows type aliases. Your later word, from 2026-10-09, wants new types, not type aliases.

- Ethos Zero emits `Datomizable` and `Compositional` on every struct and
- enum it generates, so every ethos-declared type always bears both
- traits and no declared type can exist without them. An alias bears them
- through the type it names: an alias is not a new type and cannot carry
- a derive.
+ Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates, so every ethos-declared type always bears both traits.
+ A type of one position is a new type, never a type alias.
+ A struct of one field is forbidden.
+ A new type never wraps another new type: if a job is a flow id, it is written flow id.

Ruling: land, amend, or reject.

## Proposal 5: psyche-context › vision/ethos.md

+ Inline declaration is mandatory, unless the type is so deep that it needs too much recursion; an algorithm decides which.
+ Structs are preferred over chains of variants.
+ Variants are ordered by seniority: the first is the most senior.

Ruling: land, amend, or reject.

## Proposal 6: psyche-context › vision/ethos.md

Your later words, from 2026-10-06 and 2026-10-07, prefer a new line to opening beside the declaring head.

- Ethos expands vertically: a structure with more than one element opens on its line and its elements hang beneath the first, aligned; the closing delimiter ends the last element's line. Nothing that has a next layer sits on one line.
+ Ethos expands vertically, not horizontally: where a structure would run far to the right, its first element opens on a new line, indented, and each element with a next layer takes its own line.
+ The closing delimiter ends the last element's line; it never takes a line of its own.
+ Nothing that has a next layer sits on one line.
+ Ethos indents by three spaces.
+ A comment sits above or beside what it comments on, never below, lined up with that object's indentation.
+ A vector may hold several items per line; past a width it wraps and lines up with its first item.

```
+ Metaflow.{                    ; who a flow is
+    Aspect.[ Psyche Mind Field ]
+    Topic                      ; core by default
+    Layer.[ Primary Secondary
+            Tertiary Quaternary ] }
```

Ruling: land, amend, or reject.

## Proposal 7: psyche-context › vision/ethos.md

The pinned ethos-zero generates types only, not traits, and Flow already holds 209 hand-written traits. You ruled: "Long term we want all the traits in ethos and short term we just do without."

+ Long term: Ethos declares every trait and ethos-zero generates it, and every implementation sits under one of those traits, so no hand-written trait remains.
+ Short term: hand-written traits are allowed.
+ Every feature is a capability, borne by a trait; a trait is named for the capability its type of object has.
+ A trait carries real weight: a trait with one function is suspicious, and one implemented by only one type is doubly so.

Ruling: land, amend, or reject.

## Proposal 8: psyche-context › vision/ethos.md

+ A hand-maintained vector lists the types imported directly from Rust into Ethos, so the Ethos-to-Rust compiler knows what to link to.
+ An implementer reports whatever seems hard to express in Ethos.

Ruling: land, amend, or reject.

## Proposal 9: psyche-context › vision/ethos.md

+ A type whose datom form differs from its runtime form bears a special representation trait: its own datom encoding and decoding.
+ Ethos describes the real type and the representation type, which fixes the input and output types; Rust does the implementation.
+ A hash is held as bytes in memory and written in datom in an alphanumeric encoding; a flow id is written as three camelCase words.

Ruling: land, amend, or reject.

## Proposal 10: psyche-context › vision/ethos.md

+ The Ethos Nexus has the three parts: Signal, Memory and Operation.
+ It keeps the registry of Ethos sources, filled from datom files that the repositories carry, loaded together atomically into one full registry.
+ Every Ethos source added, edited or renamed changes the registry.

Ruling: land, amend, or reject.

## Proposal 11: psyche-context › skills/vision-flow.md

Your later word, from 2026-10-12, rejects Name as the identifier's name and puts its check in a shared library rather than in its own Nexus.

- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect.
+ A topic is an uncapitalized camelCase identifier made of words, checked when created; its lowercase first letter tells it from a variant.
+ The name of this identifier type is still to be found; Name and Word are not it.
+ Its check sits in a shared library, perhaps protos, for use across dialects: a cheap, light check that the parts are words, falling back to a System 1 call with a certainty threshold.
+ A flow's title names its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

Ruling: land, amend, or reject.

## Proposal 12: psyche-context › skills/vision-nexus.md

On 2026-10-05 you said no Nexus should hold any datom. Your later word, from 2026-10-14, says a Nexus uses datom, and this proposal takes it.

- A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands; it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim. A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A CLI turns text into Signal and nothing more: it takes one inline datom, no flags, no subcommands.
+ It identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim.
+ A CLI speaks to one Nexus, opens no store, stays thin.
+ A Clojure prototype uses an EDN payload for everything; a Nexus uses datom.

Ruling: land, amend, or reject.

## Proposal 13: psyche-context › skills/vision-nexus.md

On 2026-10-03 you said the flow id is a hash. Your later word, from 2026-10-09, keeps it a string for now, with a comment saying so.

```
- [ FlowId.Integer                         ; types
+ [ FlowId.String  ; types; the string is very
+                  ;   unideal: a real id from
+                  ;   the flow's hash is needed
```

Ruling: land, amend, or reject.

## Proposal 14: psyche-context › skills/vision-nexus.md

Your later word, from 2026-10-11, drops the voice. Every other Voice in this example becomes Metaflow.

-   Voice.{ Aspect Layer }                 ;   who a flow speaks for, and at which layer

```
+   Metaflow.{ Aspect Topic Layer }  ; who a flow is
```

+ The voice concept is gone; the default topic is core, the permanent topic, the last to stand.

Ruling: land, amend, or reject.

## Proposal 15: psyche-context › skills/vision-nexus.md

Your later word, from 2026-10-09, says trait, and every place is renamed.

```
- []                                       ; kinds
+ []                                       ; traits
```

Ruling: land, amend, or reject.

## Proposal 16: psyche-context › skills/vision-nexus.md

Your later word, from 2026-10-09, loads configuration atomically from many files; starting with no arguments stays.

+ A Nexus's configuration may live in separate files in different repositories, each a datom payload, and is loaded atomically.
+ The CLI sends those payloads one after another on the meta socket, so the Nexus starts with the right configuration, even at different layers.
+ The meta socket belongs to the Nexus, never to the short-term Clojure prototype.

Ruling: land, amend, or reject.

## Proposal 17: psyche-context › skills/vision-nexus.md

Your word of 2026-10-04 leaves open whether a Nexus is actor-based until it is tried, so the Kameo line goes.

- The engine inside a Nexus is driven by Kameo actors. The standards
- of their use are still to be designed. Arc-Mutex is permitted.
+ Whether the engine inside a Nexus is actor-based or something else is refined after practice.
+ Signal talks only to Operation, Memory talks only to Operation, and Operation talks to both.
+ Arc-Mutex is permitted.

Ruling: land, amend, or reject.

## Proposal 18: psyche-context › skills/vision-nexus.md

+ The three parts, Signal, Operation and Memory, and how each divides, are most of the machine's anatomy.
+ A standard entry point, like a Rust macro, enforces the three parts and their one path, so nothing bypasses them; the bodies are written by hand.
+ Ethos, the Nexus architecture and Flow are developed together: the language, the runtime architecture, and the component to bootstrap.
+ Signal defines the formats a message can take: the simple form, without the flow id, for common queries and responses; the extended form for the technical side, debugging and other components.
+ Nexuses are the long term; Clojure prototypes are the short term, derived from the same Ethos.

Ruling: land, amend, or reject.

## Proposal 19: psyche-context › skills/vision-source.md, a new file

+ ---
+ description: The Source nexus, which holds and verifies sources, is being designed or judged.
+ dependencies: [vision-nexus]
+ ---
+ ## Source
+ One Source nexus holds the sources for all components; to get a source is to send it a source request.
+ A source is a Git repository at a revision, or a local path on a host, fetched by its own kind of backend fetcher.
+ The Source nexus keeps its own Blake3 hash of the whole snapshot, without the Git directory, as Nix does.
+ It keeps several registries; the Git equivalence registry is dropped when Git is cut off.
+ The hash is there to verify that the files are the right files; a smart store that knows what to keep comes later.
+ Ethos and curriculum share one sources library, with Memory objects for the registry of sources; a skill refers to a source by name.

Ruling: land, amend, or reject.

## Proposal 20: psyche-context › skills/vision-chronos.md, a new file

+ ---
+ description: Chronos, the Nexus that tells astrological time, is being designed or judged against what the living wants it to be.
+ dependencies: [vision-nexus, vision-ethos]
+ ---
+ ## Chronos tells astrological time
+ Chronos tells astrological time for the present moment, or for a given time and location.
+ It tells it in a purely solar or a purely lunar format, and may tell more, the lunar nodes, the apogee and the aphelion among them.
+ ## Tropical, on the ecliptic
+ Everything is tropical, the nakṣatras included: Aśvinī begins at 0° Aries.
+ Everything is reckoned around the ecliptic of the Sun.
+ ## Positions are arcs
+ Sign and nakṣatra are not kept; they are obtained from an arc, absolute or relative.
+ A lunation of 31° between the Sun and the Moon reads as Taurus.
+ ## The golden example
+ Chronos is a simple, idiomatic Nexus with a full Ethos specification.
+ With Ethos and the Nexus it is the golden example, from which Flow is implemented, then the other nexuses.
+ It is the MVP Nexus: the mind builds it with Astra in prototype-making mode, following the vision and the Ethos, and the living reviews it.

Ruling: land, amend, or reject.

## Fable's view

### Proposal 21: psyche-context › skills/vision-nexus.md

Amends Proposal 12; your word of 2026-10-14 says which text a payload is written in, Clojure EDN or Nexus datom, and does not undo your word of 2026-10-05 that no datom and no string handling sit inside a running Nexus, so the two do not conflict and the struck line stays.

- A Clojure prototype uses an EDN payload for everything; a Nexus uses datom.
+ A CLI speaks to one Nexus, opens no store, stays thin; datom and all text handling are compiled out of the Nexus, which decodes only known types in their rkyv form and so stays small, since it keeps running and there may be many.
+ A Nexus's payloads, its configuration files among them, are written in datom; a Clojure prototype's are written in EDN.
+ A Nexus reads a datom file only through an outside tool, the CLI it is meant to work with, never by handling the text itself.

Ruling: land, amend, or reject.

### Proposal 22: psyche-context › vision/ethos.md

Amends Proposal 3; the rename to Memory also reaches the Associations paragraph, which still says Sema.

- dot, a bracket of its traits. In the Signal and Sema roots the
+ dot, a bracket of its traits. In the Signal and Memory roots the

Ruling: land, amend, or reject.

### Proposal 23: psyche-context › skills/vision-nexus.md

Amends Proposal 16; your word of 2026-10-09 calls loading configuration files in succession a hack to get the Nexus started until datom path expansion is solved, and the Configuration paragraph still says Sema.

- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database
+ Until datom path expansion is solved, the CLI sends the configuration files one after another on the meta socket; this is the way to start a Nexus for now, not the lasting design.

Ruling: land, amend, or reject.

### Proposal 24: psyche-context › skills/vision-nexus.md

The book keeps the caller identity in the CLI but misses your words of 2026-10-03 and 2026-10-12 that these pieces live in libraries shared by every component, not in one Nexus's library.

+ The process object that identifies a CLI's caller lives in a shared library that many nexuses use, so no CLI rewrites it and the code reads plainly; it is never user-facing and never configurable.
+ The word id conversion lives in a library every component reuses, generic over hash sizes, so a flow id is one use of it and not its owner.

Ruling: land, amend, or reject.

### Proposal 25: psyche-context › vision/ethos.md

Amends Proposal 1; you approved the section "Flow, a current best example" on 2026-10-09 and told us to point at the Flow Ethos skill rather than duplicate its code, and your word of 2026-10-16 adds the golden example project without taking that back, so the removed lines stay and the new ones are added beside them.

+ ## Flow, a current best example
+ Flow is one of the best current examples of ethos; its ethos lives in the vision-flow-ethos skill, which carries the code.
+ ## The golden example
+ The golden ethos is the ethos of ethos itself, the one that defines the types ethos goes into.
+ Ethos, the Nexus and the Chronos example project together are the golden example, from which Flow is implemented properly, then the other nexuses.

Ruling: land, amend, or reject.

<!-- to-the-living:end -->
