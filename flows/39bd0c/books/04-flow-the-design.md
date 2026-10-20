<!-- to-the-living:start -->
Presentation.{ «Flow, the design» }

Flow as you want it now, written as the lines it lands and the code that specifies it. A proposal marked ruled carries your words; one marked open is written at one default for you to amend. The Mind metaflow that takes Flow to production implements from these lines.

### Proposal 1: What Flow is for now · psyche-context › skills/vision-flow.md

Ruled. Marked short-term, because it names the work of this season and will go stale.

+ ## Short term: Flow lands, is merged and deployed, and runs in production
+ Flow is respecified, reironed and retested until it works: it accepts a system prompt, a user prompt, and a specialized flow from a flow definition, written in a dialect of datom that Ethos specifies. A metaflow of Mind takes it to production; every major effort of that metaflow is published as a report.

Ruling: land, amend, or reject.

### Proposal 2: A flow starts with its whole context · psyche-context › skills/vision-flow.md

Ruled. The launch names the metaflow and a brief; the modules are the definition's, and every one of them reaches the flow as text.

- A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+ A launch names the metaflow and a brief of a small paragraph; the modules composed into its prompts are the metaflow's, named in its definition. Flow has them composed from the three aspect context repositories, each module checked against its source: spirit and intent as the system prompt, every other module in the first message, which names the modules it carries and says they are given here and are not to be reloaded. A first message too large for one delivery goes in parts at module boundaries, in order, the brief last. No skill and no command is loaded at start.

```
Start.{ { Psyche core Secondary }
        «Crystallize today's records on Flow» }
```

Ruling: land, amend, or reject.

### Proposal 3: A metaflow is defined in datom, in its own repository · psyche-context › skills/vision-flow.md

Ruled: definitions as datom against Ethos types, in a repository of their own apart from the cluster data; a role may reach one rung up; what a flow is leaned of is named per role and overridden per call. Open: the model stays the layer's, so a definition carries no model name; amend to put the model in the role.

+ A metaflow is defined in a datom file against Flow's library, in the public metaflow repository, apart from the cluster data. The definition gives the address whose layer is the one to contact, and one role per layer: the layer, the effort, the modules the role's context is composed of, the layers above its own it may reach for a subagent, and the parts of the harness's startup it is leaned of; a call may override the leaning. The model is the layer's.

```
{ { Field publishing Quaternary }
  [ { Tertiary Medium
      [ { Vision book } ]
      []
      [] }
    { Quaternary Medium
      [ { Compensation orders }
        { Compensation messengerClj } ]
      [ Tertiary ]
      [ ClaudeMd GitInstructions ] } ] }
```

Ruling: land, amend, or reject.

### Proposal 4: Sleeping and waking · psyche-context › skills/vision-flow.md

Ruled: a metaflow not running keeps no harness; a request wakes it and the whole queue comes with the waking; a young transcript is resumed, an old one replaced by a fresh start; no Primary without a Secondary, short term. Open: what young is, written at the layer's refresh threshold, never past 100,000 tokens.

- A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started. A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A metaflow sleeps as soon as its turn ends with nothing in its queue: its harness closes, its transcript and address stay. An order, a question or the living's words wake it; a result or a notice waits in its queue until a waking. A woken metaflow receives its whole queue, oldest first, in its first prompt. A transcript still young, below the layer's refresh threshold, is resumed; otherwise the metaflow starts fresh with its whole context and the prompt it is to get now. The threshold of every layer is at most 100,000 tokens, where a context starts to degrade quickly. A metaflow under refresh or waking queues what arrives until its new flow has started, while Flow keeps serving every other request.
+ ## Short term: no Primary without a Secondary
+ A Primary is not started or woken unless its Secondary is awake, and a Primary never wakes on a message alone; its requests wait in its queue. Long term, when waking is reliable enough that no Primary is woken wrongly, a Primary wakes like any other layer.

```
Send.{ { Psyche core Secondary }
       Order.«Publish the book» }
```
```
Queued
```

Ruling: land, amend, or reject.

### Proposal 5: A heartbeat on the important topics · psyche-context › skills/vision-flow.md

Open. You almost want a timer; this writes it at one default: every six hours, the topics named important are looked at, and one nobody is tackling is sent an order to its Mind metaflow, Psyche guiding.

+ A heartbeat, every six hours, looks at the important topics. A topic no metaflow is tackling is sent an order to its Mind metaflow, with Psyche's guidance; which topics are important is set over the meta wire.

```
{ [ flow ethos nexus ] 6 }
```

Ruling: land, amend, or reject.

### Proposal 6: The Flow library, in ethos · psyche-context › vision/flow-ethos.md, a new file

Ruled: Flow's ethos stands whole, with its traits, since a type with no trait does nothing. The capabilities: an address is titled and has a layer, a brief is read, a request knows whether it wakes, a metaflow sleeps and wakes, prompts are delivered in parts, a role composes its prompts, a definition seats a layer, the heartbeat pulses. A capability's input is a trait, never a concrete type.

+ ---
+ description: The Flow Nexus in ethos; its types, traits and layout are read or judged.
+ dependencies: [vision-ethos, vision-flow]
+ ---

```ethos
Library.
{
[ protos:[ String Integer Boolean ] ]     ; imports
[ FlowId.String                           ; types
  Aspect.[ Psyche Mind Field ]
  Topic.String
  Layer.[ Primary Secondary
          Tertiary Quaternary ]
  Address.{ Aspect Topic Layer }
  Subaspect.[ Spirit Intent Vision
              Knowledge Inquiry Compensation ]
  Key.{ Subaspect Topic }                 ; a module
  Brief.String
  Request.[ Order.Brief               ; what reaches
            Question.Brief            ;   a metaflow
            Psyche.Brief
            Result.Brief
            Notice.Brief ]
  Prompts.{ String String }          ; system, first
  Tokens.Integer
  State.[ Awake.FlowId
          Asleep.Vector<Request> ]       ; its queue
  Metaflow.{ Address State }
  Effort.[ Low Medium High ]
  LeaveOut.String
  Role.{ Layer                            ; one seat
         Effort
         Vector<Key>                      ; modules
         Vector<Layer>                    ; reach
         Vector<LeaveOut> }
  Definition.{ Address                    ; contact
               Vector<Role> }
  Heartbeat.{ Vector<Topic> Integer } ]   ; hours
[ Titled.[ title.[ String ] ]             ; traits
  Layered.[ layer.[ Layer ] ]
  Briefing.[ brief.[ String ] ]
  Waking.[ wakes.[ Boolean ] ]
  Sleepable.[ sleep![ Vector<Request> ] ]
  Wakeable.[ wake!{ [ Waking ]
                    [ FlowId ] } ]
  Parted.[ parts.[ Vector<String> ] ]
  Composable.[ compose.{ [ Briefing ]
                         [ Prompts ] } ]
  Seating.[ role.{ [ Layered ]
                   [ Option<Role> ] } ]
  Pulsing.[ pulse.[ Vector<Topic> ] ] ]
[ Address.[ Titled Layered ]          ; associations
  Brief.[ Briefing ]
  Request.[ Waking ]
  Metaflow.[ Sleepable Wakeable ]
  Prompts.[ Parted ]
  Role.[ Composable ]
  Definition.[ Seating ]
  Heartbeat.[ Pulsing ] ] }
```

Ruling: land, amend, or reject.

### Proposal 7: What Flow says, in ethos · psyche-context › vision/flow-ethos.md, a new file

Ruled: a start, a send, a stop, a report from every hook, and the heartbeat; each refusal typed.

```ethos
Signal.
{
[ flow:[ FlowId Address Key Brief
         Request Tokens ] ]               ; imports
[ Start.{ Address Brief }                 ; queries
  Send.{ Address Request }
  Stop.Address
  Report.{ FlowId Tokens }             ; from a hook
  Pulse ]
[ Started.FlowId                         ; responses
  Sent.FlowId
  Queued
  Stopped
  Reported
  Pulsed.Vector<Address>
  Refused.[ NoSecondary
            NoDefinition.Address
            ChangedModule.Key
            OffRoute ] ]
[] }
```
```
Start.{ { Mind flow Primary }
        «Take Flow to production» }
```
```
Started.quietRiverStone
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
