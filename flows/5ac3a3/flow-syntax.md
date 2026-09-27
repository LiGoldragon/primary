# Flow startup syntax: proposed Ethos and Datom slice

This document is a proposed illustrative contract for Flow startup, prompt
composition, native binding, skill expansion, readiness, and inspection. It
turns the design into visible syntax so that the type declarations and their
values can be reviewed together. It is not deployed and is not a final
approved schema. The current power vocabulary is Primary, Secondary, Tertiary,
and Quaternary. Astra is the Primary Mind seat. The predecessor is preserved.

Every identifier in the examples (`5ac3a3`, `7a9c21`, native session names,
and evidence names) is a declared fixture. These examples do not describe live
launches or receipts.

## Proposed asynchronous Ethos

The Signal sweet form separates an accepted launch attempt from later observed
readiness. `Observe` is one subscription: it yields an initial snapshot and
then changes. It is not a polling loop.

```text
Signal
[]
[ Start.StartRequest Observe.LaunchId ]
[ Started.LaunchId
  StartRejected.StartFailure
  Observed.LaunchState
  ObserveRejected.ObserveFailure ]
[ FlowId.String
  LaunchId.String
  NativeSessionId.String
  ModelId.String
  SkillName.String
  SourceRef.String
  Text.String
  EvidenceId.String
  Aspect.[ Psyche Mind Field ]
  Power.[ Primary Secondary Tertiary Quaternary ]
  Seat.{ Aspect ModelId Power }
  PromptPart.[ Skill.SkillName
              Psyche.{ SourceRef Text }
              Task.Text ]
  Composition.Vector<PromptPart>
  StartRequest.{ Seat Option<FlowId> Composition }
  RequiredSkills.Vector<SkillName>
  ExpandedSkills.Vector<SkillName>
  BindingFailure.[ MissingNativeSession PaneMismatch ThreadMismatch ]
  StartFailure.[ UnknownModel.ModelId
                 NativeBindingRefused.BindingFailure
                 SkillMissing.SkillName
                 SkillNotExpanded.SkillName
                 PromptOrderMismatch ]
  LaunchStage.[ Accepted
                NativeBound
                PromptAccepted
                ExpandingSkills.{ RequiredSkills ExpandedSkills }
                Ready.{ FlowId EvidenceId }
                Failed.StartFailure ]
  LaunchState.{ LaunchId Option<NativeSessionId> LaunchStage }
  ObserveFailure.[ UnknownLaunch.LaunchId ] ]
```

`StartRequest` remains positional: it carries the `Seat`, optional predecessor,
and ordered `Composition`. Prompt-part heads are enum variants, not field
labels. `Some.5ac3a3` is a fixture predecessor reference; it does not instruct
the server to restart or retire that predecessor. All exact model, identity,
and source validation remains the Nexus responsibility.

## Matching Datom input

The complete fixture request is unchanged:

```text
Start.{
  { Mind gpt-6-astra Primary }
  Some.5ac3a3
  [ Skill.main-flow
    Skill.refresh
    Skill.spirit
    Skill.behavior
    Skill.nexus
    Skill.ethos
    Skill.datom
    Psyche.{ flows/5ac3a3/vision/flow.md
             «By default, we're going to use the model name.» }
    Task.«Design Flow startup with Ethos declarations and matching Datom examples.» ]
}
```

The first tuple is the `Seat`: aspect `Mind`, exact model `gpt-6-astra`, and
power `Primary`. The second position is the optional predecessor. The vector
is ordered, with `Skill.main-flow` first. The psyche and task parts retain
source reference and text rather than becoming an untraceable summary.

## Accepted launch and subscription observations

`Started` acknowledges an accepted launch attempt; it does not claim that the
Flow is ready. The first subscription snapshot can therefore be:

```text
Started.launch-a
Observe.launch-a
Observed.{ launch-a None Accepted }
```

`LaunchId` identifies the attempt before a native session or Flow identity
exists. `None` means that native binding has not happened yet. The following
subscription update observes expansion in progress:

```text
Observed.{
  launch-a
  Some.native-session-a
  ExpandingSkills.{
    [ main-flow refresh spirit behavior nexus ethos datom ]
    [ main-flow refresh spirit behavior ]
  }
}
```

The first vector is `RequiredSkills`; the second is `ExpandedSkills`. Observed
references to `nexus`, `ethos`, and `datom` do not enter the expanded vector
merely because they were selected. The native adapter still has to prove that
the required main-flow skill is first in the expanded input; the schema alone
does not prove that ordering.

## Typed refusal and failure branches

Early rejection can happen before an attempt is accepted:

```text
StartRejected.UnknownModel.gpt-unknown
StartRejected.NativeBindingRefused.MissingNativeSession
ObserveRejected.UnknownLaunch.launch-missing
```

Binding failure can also be observed after acceptance, on that attempt:

```text
Observed.{ launch-a Some.native-session-a Failed.SkillNotExpanded.nexus }
```

The branches above are separate fixture outcomes. A failure does not silently
retry as a new launch. No automatic deletion or unchanged retry is a repair.

## Ready on a repaired or new attempt

Success is a later observation on a distinct fixture attempt:

```text
Started.launch-b
Observe.launch-b
Observed.{ launch-b Some.native-session-b Ready.{ 7a9c22 evidence-start-b } }
```

`FlowId` appears only in `Ready`, matching the first-prompt readiness boundary.
`evidence-start-b` is a fixture reference to durable startup evidence; a name
alone does not prove expansion or publication. Full Sema evidence, source
hashes, and per-harness expansion checks remain to be designed. Readiness must
resolve native binding, required content identity and order, title/model/power
readback, and predecessor preservation. This minimal slice is not a complete
production architecture.

## What this makes concrete

| Layer | Concrete responsibility | Remaining boundary |
|---|---|---|
| Ethos | Defines the positional types and typed alternatives | Final unified vocabulary and generated projection remain open |
| Datom | Fills the declared types with an ordered startup request | Parsing and round-trip behavior still needs a live witness |
| Nexus | Receives the compiled `Signal` and owns launch state | Service implementation is unimplemented |
| Native harness | Expands required skills and verifies their order | The adapter must prove main-flow-first expansion in actual input |
| Subscription | Reports the launch snapshot and subsequent changes | Durable subscription implementation is unimplemented |
| Evidence | Names binding, content identity, order, and readiness gates | Durable Sema evidence schema remains unimplemented |

The source is ready for a fresh private Claude Artifact visual report. The
visual report should use accessible code panels and a short stage list; charts
are unnecessary here. Preserve the complete code blocks, including brackets,
glyphs, and guillemets, rather than replacing syntax with decorative cards.
