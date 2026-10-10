Presentation.{ «Flow today» }

## 1. The Flow record

Drawing: two horizontal lines through beads, each bead a flow. The upper line, labelled `Mind.Tertiary`, runs through `4403a7 → 918df4 → …` off the right edge. The lower line, labelled `Subject ethos`, runs through `7f3a21 → b02c1e` to a round end mark. Under each bead, one record: `{ 918df4 Mind.Tertiary }`.

A flow is one run of a model. A metaflow is what continues through flows: a voice, with no known end, or a subject, a task that ends when its end is judged met. Every flow continues one metaflow; nothing in the voice is repeated in the flow.

```
Library
; what Flow's four roots share
[]
; one run; a hash, written in hex
[ FlowId.Integer
  ; the four rungs of an aspect
  Rank.[ Primary
         Secondary
         Tertiary
         Quaternary ]
  ; an aspect carrying a rank
  Voice.[ Psyche.Rank
          Mind.Rank
          Field.Rank ]
  ; what continues through flows
  Metaflow.[ Voice
             ; runs as its voice
             Subject.{ Voice
                       Name.String
                       End.String } ]
  ; a run and what it continues
  Flow.{ FlowId
         Metaflow }
  ; what the harness reports
  Event.[ Started
          ToolUsed.String
          ; percent of the window used
          ContextUsed.Integer
          Stopped ]
  ModuleName.String
  ; the words a flow is given
  Module.{ ModuleName
           Text.String
           ; where the text was read
           Path.String }
  ; modules, and where they go
  Placed.{ Placement.[ SystemPrompt
                       FirstPrompt ]
           Vector<ModuleName> }
  ; how a voice is launched
  Role.{ Voice
         Harness.[ Claude
                   Codex ]
         Model.String
         Effort.String
         Vector<Placed> } ]
[]
[]
```

Written:

```
{ 918df4 Mind.Tertiary }
{ 7f3a21 Subject.{ Mind.Secondary
                   ethos
                   «deployed» } }
```

Today a flow's role is `Caller.{ FlowId FlowAspect PowerLevel ModelName }`, FlowId is a String, and no Voice, Rank or Metaflow type exists. Proposal: this Library replaces it.

## 2. Memory: the registry

Drawing: a filing cabinet with four drawers labelled `Flow`, `Module`, `Role`, `Lock`. From the `Role` drawer an arrow to a page split in two, `system prompt` above `first prompt`, each half listing module names. From `Module` an arrow into both halves carrying text.

```
Memory
; what Flow remembers
[ flow:[ FlowId
         Metaflow
         Event
         Module
         Role ] ]
; one record per flow, ever
[ Flow.{ FlowId
         Metaflow
         ; a metaflow's current flow
         ; is its one Running flow
         State.[ Running
                 Ended ]
         Vector<Event> }
  ; the registry of context modules
  Modules.Vector<Module>
  ; one role per voice
  Roles.Vector<Role>
  ; a metaflow rolling over
  Lock.{ Metaflow
         ; the flow being replaced
         FlowId } ]
```

The registry holds each module's text, so a launch reads nothing from disk and no relative path breaks; the path stays on the record as where the text came from, so the registry can be refilled from the authored source. Filling it is one message per module and per role over the meta wire:

```
Remember.Module.{ main-flow
                  «…»
                  /abs/main-flow.md }
Remember.Role.{ Psyche.Primary
                Claude
                claude-fable-5-1
                high
                [ { SystemPrompt
                    [ spirit
                      main-flow ] }
                  { FirstPrompt
                    [ vocabulary
                      psyche ] } ] }
```

Today the launcher takes a bundle file path and a vector of source paths from the caller, reads them at compose time, and keeps no Memory root at all; the role record lives in a datom under curriculum-deploy. Proposal: the Memory above, compiled; the registry filled from the authored Curriculum sources by one loader run; the model behind a voice is in Flow and nowhere else.

## 3. Launch, refresh, lock

Drawing: a flowchart. `Launch.{ Metaflow Brief }` → `Compose` → `Spawn` → `Bind` → `Launched.Flow`. A second entry `Refresh.Metaflow` → `Lock` → `Tell: write your handover` → waits at a diamond `handover.md written and Stopped?` → `Compose from the handover` → `Spawn` → `Bind` → `Reap predecessor` → `unlock` → `Refreshed`. A side box `Current.Metaflow` reads the drawers and answers `Running`, `Locked`, `Ended` or `Unknown`.

```
Signal
; what Flow says
[ flow:[ FlowId
         Metaflow
         Flow
         Event
         Module
         Role ] ]
[ ; a metaflow's first flow
  Launch.{ Metaflow
           Brief.String }
  ; a successor for its current flow
  Refresh.Metaflow
  ; a subject judged ended
  End.Metaflow
  ; which flow is current
  Current.Metaflow
  ; the hook reporting
  Report.{ FlowId
           Event }
  ; the registry filled; meta wire
  Remember.[ Module
             Role ] ]
[ Launched.Flow
  ; successor, then predecessor
  Refreshed.{ Flow
              FlowId }
  Ended.Metaflow
  Current.[ Running.Flow
            ; rolling over: hold
            Locked.Metaflow
            Ended
            Unknown ]
  Reported
  Remembered
  Refused.[ Busy.Metaflow
            Locked.Metaflow
            NoRole.Voice
            NoModule.ModuleName
            NoFlow.Metaflow ] ]
[]
```

```
Operation
; what Flow does, one per effect
[ flow:[ FlowId
         Metaflow
         Flow
         Event ] ]
[ ; the role and the brief → prompts
  Compose.{ Metaflow
            Brief.String }
  ; the harness, started
  Spawn.{ Flow
          Composed }
  ; the Herdr pane it runs in
  Bind.Flow
  ; type into a flow's pane
  Tell.{ FlowId
         String }
  ; the metaflow held or let go
  Lock.Metaflow
  Unlock.Metaflow
  ; stop a flow; its address is gone
  Reap.FlowId
  Record.{ FlowId
           Event } ]
[ Composed.{ SystemPrompt.String
             FirstPrompt.String }
  Spawned.Flow
  Bound.Flow
  Told
  Locked
  Unlocked
  Reaped.FlowId
  Recorded
  Failed.String ]
[]
```

Compose joins the role's SystemPrompt modules into the system prompt, its FirstPrompt modules and the brief into the first prompt; nothing else is read. A subject runs as its voice: same role, its own brief and end.

The lock is taken when a refresh begins and released when the successor is bound and the predecessor reaped; while it is held, `Current` answers `Locked`, a second `Refresh` or a `Launch` of that metaflow is refused, and later Message holds a letter instead of delivering it to a flow about to vanish.

The refresh is software. The status-line command the harness runs after every turn is given the percent of the window used; Flow installs that command in every flow it launches, and it reports `ContextUsed`. At the threshold Flow locks the metaflow and tells the flow to write its handover. When `flows/<id>/handover.md` exists and the next `Stopped` lands, Flow composes the successor from the handover as its brief, spawns, binds, reaps, unlocks. No model decides any step.

Today `Replace` reaps before the successor is routable, `Start` takes a fourteen-field profile, nothing measures a flow's context, and the hook reports three events. Proposal: the Signal and Operation above replace `Start`, `Replace`, `Stop`, `ResolveRecipient` and `ResolveCaller`; the meta wire's `Deliver`, `Vet`, `ResolvePeer` and `ReadEvents` stand and answer from the Flow record.

## 4. The title

```
; the Flow record, written
{ 918df4 Mind.Tertiary }
; today's title
Mind.{ Fable 918df4 }
```

Proposal: the pane and session title is the Flow record, written.

## 5. The cut

In today's release: the Library, Memory, Signal and Operation above; the registry filled from Curriculum by a loader; `Launch` composing from Memory alone; `Refresh` by order and by threshold; the lock; `End`; `ContextUsed` from the status-line command; the title. The first flow launched by it is the next Psyche Fable.

Not in today's release, designed and waiting: the Capsule (a flow runs where today's launcher puts it); Message resolving a sender and a recipient through Flow (messenger-clj keeps its route store one more day, reading the Flow record only through `Current`); a `Loadable` placement (skills stay the harness's); Flow launching voices at boot by itself; the Codex system prompt replacing the stock base instructions; clusters.

Proposal: this cut, built in the order of the sections.

## Rulings

1. The registry holds (a) each module's text, its path as provenance, refilled by a loader. (b) paths only, read at compose. (c) both, `Source.[ Path Text ]`, per module.
2. The threshold, in percent of the window: (a) your number. (b) 50, tuned after the first refresh.
3. The refresh fires after the handover order (a) at the first `Stopped` once `handover.md` exists. (b) at the next `Stopped`, whatever is written. (c) when the flow itself sends `Refresh` on finishing its handover.
4. The title: (a) `{ 918df4 Mind.Tertiary }`. (b) `Mind.{ Fable 918df4 }`, as today.
5. The cut of section 5: yes, or amend.
