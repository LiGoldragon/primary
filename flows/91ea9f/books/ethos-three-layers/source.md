`Presentation.{ «Ethos in three layers, redone» }`

Your nine comments on «Flow in ethos», each answered, then the three specifications rewritten the way you asked: vertical, flows not runs, voices, Memory, kinds as qualifiers with the voice as Self. Written with Mind Astra.

## 1. Your comments, answered

> "Yes they're going to be called voices."

Taken. A voice is the continuous named thing; Psyche Fable and Mind Astra are voices.

> "What you're calling a run is a flow. ... If it's refused how is it launching?"

Taken: a flow is one life under a voice, and Flow the component manages flows. The refusal was wrong. A Start carries a request id; the same request asked again replays `Started`; a different request against a name that already has a flow is refused as `Occupied`. Nothing is "refused but launching".

> "I don't want these Sonnet comments anymore."

Removed from the book skill; this book has none.

> "Yeah the memory is good ... signal, operation, and memory."

The three names stand: Signal, Operation, Memory. The Operation file now lists the operation types — every effect has one — and point 3 shows the path signal → operation → memory → operation → signal that you described.

> "We don't have key-value in Ethos anymore. Everything is a type."

Taken. A memory record is a type; nothing is a key column. What identifies a record is a kind it bears, not a position.

> "What the hell is a question 4 here?"

It was my questions queue, an invention with no words of yours behind it. Dropped from Memory; it is point 4's last ruling, kept or killed by you.

> "Launching, hearing, and resolving are not good names for kinds ... `launchable`."

Taken: Launchable, Reportable, Resolvable, Observable.

> "I want it to be a language that expands vertically ... a bit like Nix or Python."

Every file below is laid out that way: a bracket with more than one element opens on its own line, each element on a line, closing bracket aligned, depth by indentation. Nothing wraps. Three depths is the soft limit; past it, a Library.

> "I don't understand how there's a specific type as an input for a kind ... The voice is launchable, right, so it uses self. ... Do some actual real-world Rust checks."

Checked with the compiler, four forms, all compile. My form made the Process the launchable thing and passed the voice in as an input: legal Rust, wrong model. Your rule — the qualified thing is Self, inputs are kinds — is expressible and is the idiomatic Rust: either a bounded parameter (`fn start<P: Profiled>(&mut self, p: P)`) or an associated type chosen per implementor (`type Profile: Profiled; fn start(&mut self, p: Self::Profile)`). The second is the most Rust-native, and it is what the Operation file uses. My pushback is one line: Rust also allows a concrete type as an input, and the ethos skill today allows it (`push!{ [ String ] … }`); your rule is stricter than the language, which is fine, and it should say so in the knowledge skill: *a capability's inputs are kinds or associated types; a concrete type as input is a kind not yet named.*

## 2. Signal — the way it talks

```
Library
[ protos:[ String Integer ] ]
[
  Name.{
    String
    Role.[ Psyche Mind Field ]
    Backend.String
  }
  FlowId.String
  Flow.{ FlowId Epoch.Integer }
  RequestId.String
  Profile.[ Standard Light ]
  Binding.{
    Name
    Flow
    Launch.[
      Starting
      Bound
      Failed.String
      Uncertain
    ]
    Activity.[
      Ready
      Working
      AwaitingInput
      AwaitingApproval
      Ended
      Unknown
    ]
    Harness.[ Claude.String Codex.String ]
  }
  Event.{
    Sequence.Integer
    Kind.[
      SessionEstablished
      TurnBegun
      InputRequired
      ApprovalRequired
      TurnFinished.String
      Exited.Integer
    ]
  }
]
[]
[]
```

```
Signal
[
  flow:[
    Name
    Flow
    RequestId
    Profile
    Binding
    Event
  ]
]
[
  Start.{ RequestId Name Profile }
  Succeed.{ RequestId Name }
  Resolve.Name
  Observe.Name
  Report.{ Flow Event }
]
[
  Started.{ Name Flow }
  StartRefused.[
    UnknownName
    Occupied.Flow
    ChangedIntent.RequestId
    LaunchFailed.String
    Uncertain.RequestId
  ]
  Succeeding.{ Name Flow Flow }
  Resolved.Binding
  Observed.[
    Snapshot.Binding
    Changed.Binding
  ]
  Reported.[
    Recorded
    Stale.Flow
    Mismatch.Flow
  ]
]
[]
```

A Name is configured, with role and backend as attributes, so replacing a model never renames an addressee.

## 3. Operation — the way it treats signals and memory changes

```
Operation
[
  flow:[
    Name
    Flow
    RequestId
    Profile
    Binding
    Event
  ]
  memory-flow:[
    Attempt
    Current
    Fact
  ]
]
[
  Launchable.{
    [ ]
    [ Profile<Profiled> ]
    [ ]
    [
      start!{
        [ RequestId Profile ]
        [ Result<Flow StartRefused> ]
      }
      succeed!{
        [ RequestId ]
        [ Succeeding ]
      }
    ]
  }
  Resolvable.[
    resolve.[ Option<Binding> ]
  ]
  Observable.[ observe![ Subscription ] ]
  Reportable.[
    report!{ [ Event ] [ Reported ] }
  ]
]
[
  Name.[ Launchable Resolvable Observable ]
  Flow.[ Reportable ]
]
[
  Start.[
    Claim.Name
    Persist.Attempt
    Launch.Native
    Await.Identity
    Send.FirstTurn
    Await.Receipt
    Commit.Current
    Reply.Started
  ]
  Report.[
    Authenticate.Source
    Check.Flow
    Append.Fact
    Advance.Current
    Emit.Change
  ]
  Succeed.[
    Prepare.Successor
    Confirm.Readiness
    Swap.Current
    Retire.Predecessor
  ]
]
```

The voice is Self: a Name is Launchable, Resolvable, Observable; a Flow is Reportable. The fourth section is the one you asked for: the operation types. Each clause is an effect, each effect a type; `Persist`, `Append`, `Advance`, `Commit`, `Swap` are memory changes and come back as a memory result; `Reply` and `Emit` are the signal going out. That is the path: a signal enters, operations run, memory changes answer each operation, the last operation is a signal back. *This fourth section is proposed syntax: nothing compiles it today.*

## 4. Memory — what is remembered

```
Memory
[
  flow:[
    Name
    Flow
    RequestId
    Profile
    Binding
    Event
  ]
]
[
  Origin.{ Flow Name Transcript.String }
  Fact.{ Flow Sequence.Integer Event }
  Current.{
    Name
    Option<Binding>
    Pending.Option<RequestId>
  }
  Attempt.{
    RequestId
    Name
    Profile
    Phase.[
      Starting
      Bound
      Failed.String
      Uncertain
    ]
  }
]
[
  Origin.[ Memorable Immutable ]
  Fact.[ Memorable Immutable ]
  Current.[ Memorable ]
  Attempt.[ Memorable ]
]
```

Every record is a type and bears the memory kind. The kind is what you described:

```
Memorable.{
  [ ]
  [ Previous<Memorable> ]
  [ ]
  [
    change!{
      [ Self ]
      [ Result<Changed Unchanged> ]
    }
    upgrade:{ [ Previous ] [ Self ] }
  ]
}
```

`change!` is the standard successful-or-unsuccessful edit every record implements; `upgrade:` is upgrade-from, the previous version to this one. The edit to the ethos file *is* that upgrade: the operation the type needs to become its new shape. Origin and Fact are append-only, so a flow's end is one more Fact, never a rewritten field. Current is the one mutable answer to a name, with a pending successor while the old flow still receives.

**One example through all three.** `Start.{ r7 «Mind Astra» Standard }` enters Signal. Operation claims the name, persists `Attempt.{ r7 «Mind Astra» Standard Starting }`, launches, awaits the harness identity, sends the first turn, awaits its receipt, commits `Current.{ «Mind Astra» Some.{ … } None }`, replies `Started.{ «Mind Astra» { dea0ba 1 } }`. `Start.{ r7 … }` again replays `Started`. `Start.{ r8 «Mind Astra» … }` answers `StartRefused.Occupied.{ dea0ba 1 }`. Each hook `Report` authenticates its source, appends a Fact, advances Current, emits a change; nothing polls.

## Rulings
1. Signal, Operation, Memory as the three names.
2. Name as a configured address with role and backend attributes.
3. The operation-types section (effects as types) as the fourth section of the Operation root.
4. The Memorable kind with `change!` and `upgrade:` as the memory kind.
5. The questions queue: dropped, or kept with words of yours behind it.
6. The knowledge-skill line on kinds: "a capability's inputs are kinds or associated types; a concrete type as input is a kind not yet named."
