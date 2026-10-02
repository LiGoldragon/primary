`Presentation.{ «Flow in ethos» }`

The three parts, the revamped syntax, Flow written in it, and the datoms you would see in use. Mind Astra's evidence is folded in: Flow today reserves a start, opens the pane and submits the first turn, but hears only the window manager's pane events and keeps no table from a name to its current flow.

## 1. Three parts and their names

You named the three layers on 13 September: the process, the storage, the signal; and today you said nexus is overloaded. My proposal:

- **Nexus** stays the word for the whole running component, as you defined it ("our word for the style of component that speaks signal and uses a similar database").
- **Process** is the actor at its heart: what today is called nexus core or kernel. It is the thing that holds state, locks, and decides.
- **Signal** stays: queries in, responses out.
- **Memory** replaces storage: what the process remembers across runs, as records with keys. Sema stays the engine's name; Memory is the root in ethos.

So an ethos file is one of four roots: `Library`, `Signal`, `Process`, `Memory`. A Nexus is one of each.

## 2. The revamped syntax: inline, no invented types, bounded depth, one-screen overview

Four rules, each from your words:

1. **Declared where used.** A type used once is declared inline, at its position, with its name as head: `Failed.String`, `Exited.{ Integer }`. Only a type used in two or more places goes in the types section and is referred to by name. (Your 20 September: "the second appearance of the same type can just be described by its name".)
2. **No type invented to say what a variant carries.** The payload is written in the variant. Rust names it deterministically (today `Failed_Data`); ethos never writes that name.
3. **Depth three.** Inline nesting may go three levels down from a section entry. Anything deeper is named in the types section, or imported from a library.
4. **One screen.** The queries and responses sections of a Signal file read whole on one screen; the types section holds only what is shared. The file documents the wire by its shape.

The existing sweet form stays: root head, then sections as sibling brackets.

## 3. Flow, in ethos

The continuous named thing I call a **Voice** here; the word is yours to rule. A **Run** is one flow under a voice, with its ledger id.

**Signal**
```
Signal
[ protos:[ String Integer ] ]
[ Start.{ Voice Profile.[ Standard Light ] }
  Succeed.Voice
  Resolve.Voice
  Observe.Voice
  Report.{ Run Event }
  Ask.{ Voice Question }
  Questions.Voice
  Answer.{ Voice Integer String } ]
[ Started.{ Voice Run }
  StartRefused.[ UnknownVoice Launching.Run Bound.Run LaunchFailed.String ]
  Succeeding.{ Voice Run Run }
  Resolved.Binding
  Observed.[ Snapshot.Binding Changed.Binding Ended.Run ]
  Reported.[ Recorded Stale.Run Mismatch.Run ]
  Asked.Integer
  Answered.Vector<Question>
  Settled.Integer ]
[ Voice.{ Aspect.[ Psyche Mind Field ] Model.[ Fable Opus Sonnet Haiku Astra Sol Luna ] }
  Run.{ FlowId.String Generation.Integer }
  Binding.{ Voice Run Launch.[ Starting Bound Failed.String Uncertain ]
            Activity.[ Ready Working AwaitingInput AwaitingApproval Ended Unknown ]
            Harness.[ Claude.String Codex.String ] }
  Event.{ Integer Kind.[ SessionEstablished TurnBegun InputRequired ApprovalRequired TurnFinished.String Exited.Integer ] }
  Question.{ Integer Voice String Weight.[ High Medium Low ] } ]
```

Every struct position is a type; nothing in the file is a field name. Voice, Run, Binding, Event and Question are shared, so they are named once; everything else is inline. The deepest inline nesting is three (Binding → Launch → Failed.String).

**Memory**
```
Memory
[ signal-flow:[ Voice Run Binding Event Question ] ]
[ voices.{ Voice Binding }
  runs.{ Run Ledger.{ Voice Harness Transcript.String Started.Integer Ended.Option<Integer> } }
  events.{ Run Vector<Event> }
  questions.{ Voice Vector<Question> } ]
```

Each record is key then value. The voices table is the name-to-binding map that does not exist today; the runs table is the ledger you said flow ids are for: accounting, archive, where to search for the transcript.

**Process**
```
Process
[ signal-flow:[ Voice Run Binding Event ]  memory-flow:[ voices runs events ] ]
[ Flow.{ voices runs events Attempts.Vector<Attempt.{ Voice Run Launch }> } ]
[ Launching.[ start!{ [ Voice ] [ Result<Run StartRefused> ] }
              succeed!{ [ Voice ] [ Succeeding ] } ]
  Hearing.[ report!{ [ Run Event ] [ Reported ] } ]
  Resolving.[ resolve.{ [ Voice ] [ Option<Binding> ] } ] ]
```

The process holds the memory tables and the in-flight attempts; its kinds are the verbs the signal hands it. A duplicate Start while an attempt is open answers `StartRefused.Launching.{ … }` and launches nothing twice — the behaviour behind "if I ask for a new flow, when I come back there's a new flow".

## 4. In use: the datoms

Starting a Mind Astra:
```
flow 'Start.{ { Mind Astra } Standard }'
Started.{ { Mind Astra } { dea0ba 1 } }
flow 'Start.{ { Mind Astra } Standard }'      ; again, too soon
StartRefused.Launching.{ dea0ba 1 }
```

A harness hook reporting, with no model call and no polling:
```
flow 'Report.{ { 91ea9f 1 } { 17 TurnFinished.t42 } }'
Reported.Recorded
flow 'Report.{ { 6997eb 1 } { 3 TurnBegun } }'  ; a retired run
Reported.Stale.{ 6997eb 1 }
```

Addressing by name — the messenger asks Flow, never the flow id:
```
flow 'Resolve.{ Psyche Fable }'
Resolved.{ { Psyche Fable } { 91ea9f 1 } Bound Working Claude.91ea9f9f }
```

Succession, with the lock you described (the old stops receiving, then the new receives):
```
flow 'Succeed.{ Psyche Fable }'
Succeeding.{ { Psyche Fable } { 91ea9f 1 } { 3c0e12 1 } }
; observers see Changed.{ { Psyche Fable } { 3c0e12 1 } Bound Ready … } once the successor is bound,
; and Ended.{ 91ea9f 1 } for the predecessor.
```

**"What are your most important questions?"** — a voice records each question it has for you as it arises; the living messenger asks Flow for them and brings them as one message; your comment comes back as the answer through the same hook pipeline:
```
flow 'Ask.{ { Psyche Fable } { 0 { Psyche Fable } «Voice, Office, or another word for the seat?» High } }'
Asked.7
flow 'Questions.{ Psyche Fable }'
Answered.[ { 7 { Psyche Fable } «Voice, Office, or another word for the seat?» High }
           { 5 { Psyche Fable } «Credentials route (a) now, (b) later?» Medium } ]
flow 'Answer.{ { Psyche Fable } 7 «Voice» }'
Settled.7
```

## For your word
- Nexus / Process / Signal / Memory as the four names?
- Voice for the continuous named thing?
- The four syntax rules, and depth three?
- Is the questions proposition what you meant: each voice's open questions, kept by Flow, gathered into one message, answered by comment?
