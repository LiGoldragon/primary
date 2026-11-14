Presentation.{ «The address names the model» }

# The address names the model

*Created by Fable.*

His words: "why don't we get this new vocabulary into the next version 0 Flow Nexus? It's really not hard to change the first field variant to be one of a model. We could have a Psyche core Astra, a Psyche core Sol, a Mind core Fable, a Mind core Opus. All these possibilities then open up. I think the psyche/mind/field separation is good." And his ruling: "It's aspect topic model." Two flows of one model serve two topics. For the version after 0.48; knowledge:flow-messaging follows when that version runs. Lands without his review, on his word. It replaces the book The address names the flow.

+ ```mermaid
+ flowchart TB
+     a["Address: Aspect, Topic, Model"] -- "{ Psyche core Fable }" --> f["one metaflow"]
+     a -- "{ Mind core Opus }, { Psyche core Astra }" --> g["any model in any aspect"]
+ ```

### Proposal 1: The model in the address · psyche-belief › vision/flow-nexus.md

**Comment** Every line that put the layer in the address now puts the model there; the layer table and the route refusal go.

- The Flow Nexus manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+ The Flow Nexus manages metaflows. A metaflow is one address, { Aspect Topic Model }, that continues through several flows one after another; the flow is its current run. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
  
- A topic lives on; when idle, its flows are turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its belief modules, so the Flow Nexus knows what to start it with, together with the new input that warrants it.
+ A topic lives on; when idle, its flows are turned off. When the living touches on it again, whether to wake a flow for it, and which model, is a judgment, made by a small model; a topic is bound to its belief modules, so the Flow Nexus knows what to start it with, together with the new input that warrants it.

```datom
- Send.{ Address.{ Psyche core Secondary } Soft.Living.{ «context» «verbatim» } }
+ Send.{ Address.{ Psyche core Opus } Soft.Living.{ «context» «verbatim» } }
```

  ## Starting flows
  
- A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model. A launch names the metaflow, the belief modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
+ The address names the model, Fable, Opus, Sonnet, Haiku, Astra, Sol, Luna or Terra, in every aspect: a Psyche core Astra and a Mind core Fable are both addresses. A launch names the metaflow, the belief modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry.
  
- Short term, the Secondary starts first, then its Primary.
+ Short term, Opus starts first, then Fable.
  
- Long term, a Primary is a simplified flow, used only to render judgment: guiding a design or posing questions.
+ Long term, Fable is a simplified flow, used only to render judgment: guiding a design or posing questions.
  
- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, model and flow id: { Psyche core Opus <id> }.
  
- Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. The Flow Nexus refuses a request that leaves those routes.
+ Who speaks to whom is vision:aspects'. Version 0 refuses no request by its address; the routes are version 1's, in the complex definition.

```datom
- Rehearse.{ { Psyche core Primary } Predecessors.1 «brief» }
+ Rehearse.{ { Psyche core Fable } Predecessors.1 «brief» }
```

```datom
  Configure.Metaflow.{
-    { Psyche book Quaternary }
+    { Psyche book Haiku }
     Some.«/home/li/book»
     Claude
     [ ClaudeMd GitInstructions ] }
  
  Configure.Metaflow.{
-    { Psyche core Primary }
+    { Psyche core Fable }
     None
     Claude
     [ Artifact ClaudeMd GitInstructions ] }
```

```ethos
  Library
  []
  [ FlowId.Integer
    Topic.String
    Aspect.[ Psyche Mind Field ]
-   Layer.[ Primary Secondary Tertiary
-           Quaternary ]
-   Address.{ Aspect Topic Layer }
+   Model.[ Fable Opus Sonnet Haiku
+           Astra Sol Luna Terra ]
+   Address.{ Aspect Topic Model }
    Event.[ Started Stopped ] ]
  []
  []
```

```datom
  ; 1 Input, typed at the CLI, sent as signal
- Launch.{ { Psyche core Primary }
+ Launch.{ { Psyche core Fable }
           «Draft the Nexus book» }
  ; 2 Operation, from Signal's intend
- Start.{ { Psyche core Primary }
+ Start.{ { Psyche core Fable }
          { /home/li/primary [] } }
  ; 3 the Change Operation hands Memory
- Flow.{ 7 { Psyche core Primary } Running
+ Flow.{ 7 { Psyche core Fable } Running
         [ Started ] }
```
