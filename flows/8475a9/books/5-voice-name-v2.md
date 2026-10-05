<!-- to-the-living:start -->
Presentation.{ «A voice's name» }

Second edition. Your comments on the secretary's copy of these types are answered here, since the types were this book's.

## Your comments

**"Well those are the types for what? First of all your ethos is wrong. You can't just throw uncontextualized ethos code around. It doesn't mean anything."**
The block below says which ethos it is: Flow's Library root, the shared types of the Flow Nexus. Today those types sit in the types section of `signal-flow/ethos/signal.ethos`, where `FlowId.String` is at line 116; the Library root is the four-root shape proposed in «The Nexus».

**"Also we don't want to repeat. This is a repetition. The seat, first of all, is a flow. We don't have seats. There's no seat. It's a flow. We're not going to repeat. The flow is just the flow ID and maybe something else but we're not going to repeat what's already in the voice. Actually yeah, we can say that the flow has a flow ID and a role, one of which is a voice."**
Seat is gone. A flow has a flow id and a role; a voice is one role.

**"Are you asking me if secondary is opus? Because the answer is yes, that should be documented somewhere."**
Logged; it belongs in Flow's voice configuration, where the model behind each voice is declared once. Ruling 4 asks whether this page's line is that document until Flow holds it.

## The ethos: Flow's Library root

```
Library                                              ; Flow's Library: what Signal, Operation and Memory share
[]                                                   ; imports
[ FlowId.Integer                                     ; types
  Aspect.[ Psyche Mind Field ]
  Layer.[ Primary Secondary Tertiary Quaternary ]
  Voice.{ Aspect Layer }                             ;   who, at what layer: what the messenger names an originator by
  Role.[ Voice                                       ;   what a flow runs as; a side flow is a job, not a voice
         Job ]
  Flow.{ FlowId Role } ]                             ;   a flow: its id and its role; nothing the voice already says
[]                                                   ; kinds
[]                                                   ; associations
```

`Job` names the side flow of vision-flow; its payload is not designed here.

## The name, in datom

Two readings of your `{ Mind Tertiary 918df4 }`, and they differ.

```
; a position expecting Flow.{ FlowId Role }: the flow, with its role the voice
{ 918df4 Voice.{ Mind Tertiary } }

; a position expecting Voice: the originator, as the messenger names it
{ Mind Tertiary }

; your example as written: a struct of Aspect, Layer and FlowId
{ Mind Tertiary 918df4 }
```

The third is the Seat type you struck as repetition. The first says the same thing with the voice kept whole inside the flow. Ruling 1 asks which the title carries.

## The skill line

`Curriculum/skills/main-flow.md`, the title line.

**Now:**
> A main flow's remote title names its aspect, model and flow id, as a Datom struct: `<Aspect>.{ <Model> <FLOW_ID> }`, for example `Mind.{ Astra 6f51ad }`.

**Proposed, under ruling 1 (a):**
> A main flow's remote title is its Flow, as one datom: `{ <FLOW_ID> Voice.{ <Aspect> <Layer> } }`, for example `{ 918df4 Voice.{ Mind Tertiary } }`.

**Proposed, under ruling 1 (b):**
> A main flow's remote title names its aspect, layer and flow id, as one datom struct: `{ <Aspect> <Layer> <FLOW_ID> }`, for example `{ Mind Tertiary 918df4 }`.

The model leaves the title either way.

## The registry

The association of a voice to its current flow is Flow's Memory: Flow launches and replaces flows, so it holds the binding it replaces. The messenger resolves a voice through Flow. Persona may describe a voice; it is not a second routing authority. A yes here settles «The Nexus» ruling 10 (Persona or Flow holds a flow's layer) for Flow. Mind Astra concurs.

```
Memory                                               ; Flow's Memory root
[ flow:[ FlowId Role ] ]                             ; imports from the Library
[ Flow.{ FlowId Role State.[ Running Ended ] } ]     ; record types: the current flow of each voice is the Running one with that Role
```

## Rulings

1. The title: (a) `{ 918df4 Voice.{ Mind Tertiary } }`, the Flow type as written. (b) `{ Mind Tertiary 918df4 }`, as you wrote it, a struct of its own.
2. The registry in Flow's Memory, the messenger resolving through Flow, settling «The Nexus» ruling 10 for Flow: yes, or amend.
3. Seat leaves the vocabulary; main-flow's "one of the twelve seats" becomes "one of the twelve voices": yes, or amend.
4. "Secondary is Opus" documented, until Flow holds the voice configuration, in the knowledge-layer-models skill as one line: yes, or name the place.
<!-- to-the-living:end -->
