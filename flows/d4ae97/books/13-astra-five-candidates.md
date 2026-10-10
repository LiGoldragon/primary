<!-- to-the-living:start -->
Presentation.{ «Astra's five candidates» }

Nothing here is landed. Each candidate is a private review artifact; a ruling says whether it goes forward.

## Proposal 1: The topic registry

`flow-evidence/0c85a3/topic-registry/README.md`, new

Terms. An aspect is Psyche, Mind or Field. A topic is a short name inside an aspect; Core is the topic of every flow without one. EDN is Clojure's plain text for data. Babashka is the small, fast-starting program that runs Clojure.

Added, the stored file:

```clojure
{:topics [{:aspect :psyche :topic "Core"}
          {:aspect :mind :topic "Core"}
          {:aspect :field :topic "Core"}]}
```

Added: register, list and resolve a topic. Registering the same pair twice changes nothing. Two processes registering at once are made to take turns. A stored file holding more than one form is refused and left untouched. Nine tests with 39 assertions pass. It is not connected to Flow or to a Mind nexus.

Ruling: The candidate accepts a topic only if it is words each starting with a capital letter, such as `Testing` or `FlowStart`. That check is a stand-in and does not test English. (a) keep it as a stand-in; (b) accept any non-blank topic, as the Flow prototype does; (c) refuse the registry.

## Proposal 2: The Codex server upgrade

`flow-evidence/0c85a3/codex-generations/design.md`, new

[Drawing: last, current and next, and the switch]

Terms. A generation is one installed Codex program with its own home folder, socket (the file clients connect through) and service. The controller is one small new program that holds which generation each slot names. A reservation is a launch's claim on a generation until the new session is bound to it.

Added:

- Each generation keeps one identity for its whole life. The identity comes from the package and its service recipe, never from a slot name or version.
- Three slots name generations: `next`, `current` and `last`. Moving a slot never renames a service, moves a home or touches a session.
- The controller does four things: stage a new generation, check it, select it as current, retire an old one. Selection is atomic.
- A launch asks the controller to reserve the current generation, then binds the reservation to its new session. A launch that fails releases it.
- Running sessions stay on the generation they started on. Only later launches see the switch.
- No generation copies another's login file.

Not settled, stated in the design: the old server may be stopped only when nothing is attached to it, and no existing interface proves that. Two servers may run side by side only when their logins are independent, and no tool yet shows they are. The cause of the token trouble is your report, not a finding. Nothing here is deployed.

Ruling: Slot names `last`, `current`, `next`. (a) adopt them; (b) other names; (c) hold the whole design.

Ruling: How to prove a server unused. (a) every client goes through the controller and direct use is blocked; (b) retirement also reads the operating system's list of connections to the socket; (c) retire only by hand until one is built.

## Proposal 3: Clojure under Nix

`clj-build/lib/uberjar.nix`

Terms. Nix builds programs from fixed recipes. An uberjar is one archive holding a program and all its libraries. AOT means the Clojure was compiled ahead of time into class files. clj-build is our Nix builder for Clojure.

Measured on a small example, five runs each, median start time: 5.400 s when every entry has the same timestamp, 0.560 s when class files are two seconds newer than sources, 2.023 s with matching sources removed. With equal timestamps the program compiles itself again at start; with newer classes it loads the compiled ones.

Removed:

```
        cp -r classes/. staging/
        chmod -R u+w staging
```

Added:

```
        chmod -R u+w staging
        cp -r classes/. staging/
```

Added: after the archive is written, a step sorts its entries, stamps sources 00:00:02 and class files 00:00:04, and clears extra fields. The tested step is written in Python; no Clojure version exists yet.

The unmodified builder failed on the Prometheus builder with a permission error, which the reordering above fixes. Building twice returned the same results from the Nix store; that shows reuse, not an independent rebuild. Removing sources is not recommended.

Ruling: The reordering fixes a build failure by itself. (a) land it alone now; (b) land it with the timestamp step; (c) refuse.

Ruling: The timestamp step. (a) land the Python as tested; (b) rewrite it in Clojure first.

## Proposal 4: The Clojure Flow prototype

`flow-evidence/0c85a3/clojure-flow/README.md`, new

[Drawing: the flow struct, and the chain of flow IDs]

Terms. A Metaflow is a named line of flows; its name is the key. A flow ID names one flow. The last ID in the chain is the current flow.

Added, one stored record:

```clojure
{:schema 1
 :metaflows
 {"Mind Testing Primary"
  {:aspect :mind
   :topic "Testing"
   :layer :primary
   :flow-ids ["flow-1" "flow-2"]}}}
```

Added: register a name with its first flow ID, advance by appending a successor (refused if the caller's expected current ID is stale), resolve by exact name. No topic becomes `Core`. Names are exact, case-sensitive strings and are never derived from aspect, topic and layer. Eleven tests with 21 assertions pass. It has its own file, reads no live Flow or Messenger data, and launches nothing.

Importing existing flows needs a reviewed list of names for existing IDs; names cannot be guessed from titles or models. No importer exists.

Ruling: The chain keeps every flow ID forever. (a) keep all; (b) bound it, you name the bound.

## Proposal 5: The JSON and Datom bridge

`flow-evidence/0c85a3/format-bridge/schema/bridge.ethos`, new

[Drawing: JSON and Datom meeting at one checked type]

Terms. Ethos is the language our types are written in. Datom is our text form for values. JSON is the common web text form. A variant is one alternative of a type, such as Lookup or Save.

Added, the two query variants and two answers:

```
[ Lookup.Topic Save.Topic ]
[ Found.Entry Missing.Topic ]
```

Added, the proposed JSON for a variant is one object whose only key is the variant's name:

```
{"Lookup":"alpha"}
Lookup.{ alpha }
```

The first line is JSON, the second the same value in Datom. Both are read through the type Ethos generated, so an unknown variant, a wrong shape or an extra field is refused in either direction. Five tests pass. It adds no general adapter, no Clojure adapter and no wire contract.

Ruling: The JSON shape above, one object keyed by the variant name. (a) adopt as the mapping; (b) another shape; (c) refuse.
<!-- to-the-living:end -->
