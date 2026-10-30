Presentation.{ «The Flow Nexus, bare» }

# The Flow Nexus, bare

Created by the Primary

### Proposal 1: vision:flow-nexus · psyche-belief › vision/flow-nexus.md — whole, retaken

**Why** The module is cut to what the Nexus needs to function. The Nexus gives a flow its id, and a message lands as one datom, so your words are found in a transcript by its form. The harness map is your idea of 2026-10-26 (flows/63aef7/vision/flow.md). Your four comments are in: the metaflow is a name on the user side, the id is minted by the Nexus, sleeping and waking move to the long vision, the one-model line is gone.

---
description: The Flow Nexus, which starts, messages, refreshes and ends flows.
dependencies: [vision-nexus, vision-model-roles]
---

## Address

A flow is addressed by { Aspect topic Layer }. Inside the Nexus the unit is the flow: one harness session, one id, one address. The metaflow is the user-facing name for the flows that have run at one address, one after another; in the chat a flow is called by its address.

The Nexus mints a flow's id, six characters, and tells the flow its id and its address in its system prompt; it remembers which harness session is the flow's, so the transcript is found from the id whatever the harness. Every call to the Flow CLI is identified by the calling process.

## Start

A launch names an address, a remembering and a brief. The Nexus composes the flow's prompts from the belief modules declared for that address: spirit and intent in the system prompt, the other modules, the remembering and the brief in the first prompt. The layer selects the model. A flow's tools and prompt are the harness's, less its blacklist. The Capsule gives the flow its place to run, one Herdr pane; a permission prompt reaching the living is a launch failure.

## Message

A request is sent to an address and the Nexus delivers it into the flow's prompt. When the flow is busy, the request queues and is delivered when the flow is idle, the queue whole and oldest first; when no flow is running at the address, one is started with the queue as its first prompt. The living's words, a comment among them, reach a flow by this path.

A message lands in the flow's prompt as one datom: the sender's address, the kind and the words. Because the form is fixed, a transcript is searched for the living's words by it.

A request is one of a closed set: an order, a question, the living's words, a result, a notice. The Nexus refuses a request that leaves the routes of vision:aspects.

## The harness

The harness's own system prompt is reproduced as a datom, sectioned and labeled by what each part is about, and the Nexus injects that reproduction in place of the stock one. A harness module is one section, named by the harness's own term, and says which tool it teaches; a tool and its teaching are one module. A declaration's blacklist names the harness modules a flow goes without, and each leaves with its tool and its section together. A separate tool extracts the stock prompt at each harness version and diffs it against the sections, so the modules a new version touches are known. What is universal is one abstraction; what differs per harness is its configuration, nothing hardwired.


The Ethos:

```ethos
Library
[ flow:[ Address ModuleId ] ]                      ; imports
[ Harness.[ ClaudeCode Codex ]                     ; types
  HarnessVersion.String                            ;   as the harness prints it
  HarnessModuleName.String                         ;   the harness's own term for the part
  ToolName.String                                  ;   the tool's name as the harness names it
  HarnessModule.{ HarnessModuleName                ;   one labeled section of the stock prompt
                  Option<ToolName>                 ;     the tool it teaches, when it teaches one
                  Text.String }                    ;     the section's text, verbatim
  HarnessPrompt.{ Harness HarnessVersion           ;   the stock system prompt, whole, sectioned
                  Vector<HarnessModule> }
  Blacklist.Vector<HarnessModuleName>              ;   the harness modules a flow goes without
  Declaration.{ Address                            ;   what a metaflow is started with
                Vector<ModuleId>                   ;     its belief modules
                Blacklist } ]
[ Extractable.[ extract:{ [ Harness HarnessVersion ] [ HarnessPrompt ] } ]      ; traits: the separate tool
  Composable.[ compose.{ [ HarnessPrompt Blacklist ] [ Vector<String> ] } ] ]   ;   the harness's launch arguments
[ HarnessPrompt.[ Composable ] ]                   ; associations
```

The datom, real: Claude Code 2.1.294 as installed today, two of its modules, each the tool's name and the first words of the text the harness gives for it; the text is the harness's, verbatim, so it is cut here:

```datom
; HarnessPrompt
{ ClaudeCode 2.1.294
  [ { Artifact Some.Artifact
      «The Artifact tool renders an HTML file as an Artifact: a web page hosted on claude.ai that is private by default. …» }
    { ArtifactComments Some.ArtifactComments
      «Read and answer the comment threads people leave on a published artifact, and manage this session's artifact watches. …» }
    { ArtifactData Some.ArtifactData
      «Read and write the small shared database an artifact's page code keeps. …» }
    { Environment None
      «Primary working directory: /home/li/primary …» } ] }
```

The Psyche core Primary's declaration, with its blacklist:

```datom
; Declaration
{ { Psyche core Primary }
  [ spirit:core spirit:psyche spirit:ghost intent:psyche intent:living-interaction vision:psyche-primary ]
  [ Artifact ArtifactComments ArtifactData ] }
```

What the Nexus composes from the two for Claude Code, and runs today:

```sh
claude --disallowedTools Artifact ArtifactComments ArtifactData --system-prompt-file <the prompt, the three sections left out>
```

## State

Every harness event reaches the Nexus through the harness's hooks calling the Flow CLI, so the Nexus knows each flow's state as it changes: started, working, idle, ended.

## Refresh

A flow past its model's context threshold is refreshed as it goes idle: a successor is launched at the same address with a remembering of its predecessor, the predecessor is ended, and what queues meanwhile goes to the successor. The threshold is configured per model. A compaction is a refresh that was missed.

## End

A flow is ended by request, by refresh, or when it is abandoned or superseded; its transcript stays.

## Signal

```ethos
Signal
[ flow:[ Address Remembering FlowId Request ] ]      ; imports
[ Launch.{ Address Remembering Brief.String }         ; queries
  Send.{ Address Request }
  Refresh.FlowId
  End.FlowId ]
[ Launched.FlowId                                     ; responses
  Delivered  Queued  Started.FlowId
  Refreshed.FlowId
  Ended
  Refused.[ NoCapsule RouteClosed AddressBusy ] ]
[]                                                    ; types

```
```datom
; the living's comment on a book, carried to the Psyche core Primary
Send.{ { Psyche core Primary }
       Words.«This is not necessary.» }
Delivered
```

## Operation

What the Nexus does; every effect is one operation type. A signal reaches memory only through an operation, and the answer returns the same way.

```ethos
Operation
[ flow:[ Address Remembering FlowId Request Declaration ] ]   ; imports
[ Start.{ Address Remembering Brief.String Declaration }      ; operations
  Deliver.{ FlowId Request }
  Enqueue.{ Address Request }
  Replace.FlowId
  Stop.FlowId ]
[ Started.FlowId                                              ; outcomes
  Delivered  Enqueued
  Replaced.FlowId
  Stopped
  Failed.[ CapsuleRefused HarnessRefused StoreRefused ] ]
[ Capsule.{ Home.String Pane.String } ]                       ; types
```

## Memory

What the Nexus remembers: one record per flow, and the queue of each address.

```ethos
Memory
[ flow:[ Address FlowId Request Declaration ] ]               ; imports
[ Flow.{ FlowId Address                                       ; record types
         State.[ Started Working Idle Ended ]
         Predecessor.Option<FlowId> }
  Queue.{ Address Vector<Request> }
  Answer.[ Succeeded Failed ] ]
```

## Meta signal

The owner's socket: configuration alone passes through it, the declarations and the thresholds among it.

```ethos
Signal
[ flow:[ Address Declaration ] ]                              ; imports
[ Declare.Declaration                                         ; queries
  Threshold.{ Model.String Tokens.Integer }
  Observe ]
[ Declared  Thresholded                                       ; responses
  Observed.Vector<Declaration>
  Refused.NotOwner ]
[]                                                            ; types
```

```datom
; the Psyche core Primary declared over the meta socket, with its blacklist
Declare.{ { Psyche core Primary }
          [ spirit:core spirit:psyche spirit:ghost intent:psyche intent:living-interaction vision:psyche-primary ]
          [ Artifact ArtifactComments ArtifactData ] }
Declared
```

**Moved, not removed** These leave the module for vision:long:flow-nexus, as they stand today, under the same headings: a metaflow sleeping and waking; the topic enum; the judgment by a small model of whether to wake a topic; the simplified flow; a Primary as a simplified flow; the flow ethos specifying a flow whole; the heartbeat; the ephemeral flow; restarting without waking; versions; the Capsule's later encryption; the real-world test; Herdr as one exchangeable backend.

**Removed** The one-model line. Id lengthening on collision. "What it does", which said the Nexus three times. "Repository and belief modules", held by vision:belief-modules. "What a refresh carries", said once under Refresh.

### Proposal 2: vision:messaging · psyche-belief › vision/messaging.md — Destroy

**Why** The Nexus is the one send path, and Message is said under it. The priority head and the four witnesses go with it; a request's datom form is the Signal above.
