Presentation.{ «The translator, first draft» }

# The translator, first draft

Created by the Primary

**Why** A Nexus thinks in typed values and holds no command string; the translator is the one component that turns typed values into text and text into typed values, for every Nexus and for the CLI. This is the first draft, for the first prototype beside Flow Nexus version 1.

### Proposal 1: vision:translator · psyche-belief › vision/translator.md — a new module

## What it is

The translator carries values between signal and text, in either direction, for whoever asks: a Nexus sending a value out into the world, a CLI turning the living's datom into signal and a reply back into datom. It is one component shared by many Nexuses, and it is not a Nexus: it keeps nothing and answers only with the translation.

An effect on the world, a pane started, a prompt placed, a file written, is an output: a typed value of its own Ethos root, Output, which a Nexus emits and which returns nothing. The translator turns an output into the system call that performs it, by a spec that names which calls exist and how each output maps onto one; the Nexus never writes a command.

Several translators run at once, one for each set of contracts in use: the stable keeps its translator while the next runs its own. A translator is identified by the hash of all the signal and output contracts it reads and writes, and a Nexus finds its translator by that hash.

## Output

```ethos
Output
[ herdr:[ Pane Home ] ]                          ; imports: the harness and pane vocabulary
[ StartPane.{ Pane Home Command.Vector<String> }  ; outputs: each one effect, returning nothing
  PlacePrompt.{ Pane Text.String }
  ClosePane.Pane ]
```

## The translator's signal

```ethos
Signal
[ protos:String  signal:Contract ]               ; imports
[ Textualize.Datomizable                         ; queries: a value to text
  Actualize.{ Contract String }                  ;   text to a value of a named contract
  Perform.Output                                 ;   an output to the system call that performs it
  Identify ]                                     ;   which contracts this translator speaks
[ Text.String                                    ; responses
  Actualized.Datomizable
  Performed  Refused.[ UnknownContract CallRefused.String ]
  Identity.ContractHash ]
[ ContractHash.String ]                          ; types: the hash of every contract read and written
```

## The datom

The Flow Nexus, starting a flow's pane, emits one output and names no program:

```datom
; Output, from the Flow Nexus to its translator
StartPane.{ psyche-core-primary
            /home/li/primary
            [ claude --disallowedTools Artifact ArtifactComments ArtifactData ] }
Performed
```

The CLI, a user of the same translator, actualizes the living's datom against the Flow contract and textualizes the reply:

```datom
Actualize.{ signal-flow-nexus «Launch.{ { Psyche core Primary } Predecessors.1 «Draft the Nexus book» }» }
Actualized.…
```

A translator identifies itself:

```datom
Identify
Identity.a7f3c9e2
```

**What comes next** The spec that maps each output onto its call, and who holds it: the translator's own configuration, over a meta socket of its own. Whether the Herdr vocabulary is one Output library among several, one per backend.
