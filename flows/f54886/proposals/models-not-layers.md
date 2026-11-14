Presentation.{ «Models, not layers» }

# Models, not layers

*Created by Fable.*

His words: "I want to abandon this primary, secondary, tertiary vocabulary. The models have personality, and I have to stop pretending they don't exist. All the complexes are configured custom. That whole vocabulary is going to either go away, or people are going to choose it voluntarily. What will be visible in the configuration is the model. I want to start talking about models more than this layering, which is artificial and actually just confusing." Lands without his review, on his word. The layer lines in vision:flow-nexus and knowledge:flow-messaging go with the version 1 landing, which replaces the address they belong to.

+ ```mermaid
+ flowchart TB
+     c["a complex, configured in datom"] -- "names each member's" --> m["model: Fable, Opus, Sonnet, Haiku, Astra, Sol, Luna"]
+     m -- "has" --> p["personality: what it designs, does, speaks"]
+     c -- "names" --> r["routes: who speaks to whom"]
+ ```

### Proposal 1: Models have personality · psyche-belief › vision/model-roles.md

**Comment** Every line that explained a role by layer now explains it by the model's name. The ranks, the ceiling and the routes stay as facts about models.

  ## Beliefs about models live here
  
- What is believed about a model, its rank, its cost, what it is given,
- is written in this module alone; every other module names a layer.
+ What is believed about a model, its personality, its rank, its cost,
+ what it is given, is written in this module alone; every other module
+ names a model by its name.
  
- The system is understood energetically. The living's attention is a thousand times dearer than any flow's; within the system a Primary's input and output are the dearest, far above a Secondary's, and a Secondary's above its subflows'. A message that saves a cheaper flow's words and makes a dearer one fetch has cost more, not less.
+ The system is understood energetically. The living's attention is a thousand times dearer than any flow's; within the system Fable's input and output are the dearest, far above Opus's, and Opus's above Sonnet's and Haiku's. A message that saves a cheaper flow's words and makes a dearer one fetch has cost more, not less.
  
- ## Roles are explained by layer, not by model
+ ## Models have personality
  
- Roles are explained by layer, not by model; one skill maps layer to model.
+ The models have personality, and a flow is spoken of by its model's name. A complex names each member's model in its datom definition, and that is where the model is visible.
  
- | Layer | Claude (Psyche) | OpenAI (Mind, Field) |
- |---|---|---|
- | Primary | Fable | Astra |
- | Secondary | Opus | Sol |
- | Tertiary | Sonnet | Luna |
- | Quaternary | Haiku | Luna, low effort |
+ | Claude | OpenAI | Personality |
+ |---|---|---|
+ | Fable | Astra | designs, judges, speaks with the living |
+ | Opus | Sol | choreographs, publishes, lands |
+ | Sonnet | Luna | large plain work |
+ | Haiku | Luna, low effort | small jobs |
  
  ## Delegation ceiling
  
- The most complex reasoning goes to a Primary. A Secondary is third, and
- stands in only when there is no Primary usage left for the design. A
- Tertiary does large plain work and designs nothing. A Primary is the
- costly layer and is main-flow only.
+ The most complex reasoning goes to Fable. Opus stands in for a design
+ only when there is no Fable usage left. Sonnet does large plain work
+ and designs nothing. Fable is the costly model and is main-flow only.
  
- Every layer launches the lowest layer that does the job, its own layer
- rarely, and a Primary never: a Quaternary launches Quaternaries; a
- Tertiary launches Tertiaries and Quaternaries; a Secondary launches
- Tertiaries and Quaternaries; a Primary launches Secondaries and
- Tertiaries, and Quaternaries for small jobs.
+ Every model launches the cheapest model that does the job, its own
+ rarely, and Fable never: Haiku launches Haiku; Sonnet launches Sonnet
+ and Haiku; Opus launches Sonnet and Haiku; Fable launches Opus and
+ Sonnet, and Haiku for small jobs.
  
  The one difference between the two sides: Opus stands in for Fable;
  Sol stands in for nothing, since it designs nothing.
  
  ## One declaration sets the model everywhere
  
- The model is declared once, as typed configuration in the Flow Nexus, mutated only
- through the meta wire. Skill variables carry that value by name into every
- skill, launcher and brief. Nothing else holds a model name, so a launcher
- never writes one by hand and no flow is started in a metaflow by accident.
+ The model is declared once, in the complex definition the Flow Nexus
+ runs, in datom. Nothing else holds a model name, so a launcher never
+ writes one by hand and no flow is started by accident.
  
- ## Native names use aspect, topic and layer
+ ## Native names use the complex and the member
  
- Every native main session is titled `{ <Aspect> <Topic> <Layer> <FLOW_ID> }`.
- The layer selects the configured model through the table above, so the
- title names the layer, never the model.
+ Every native main session is titled `{ <Complex> <Member> <FLOW_ID> }`,
+ the member being the name the definition gives the flow; tentative
+ until version 1 runs.
  
- Aspect, topic, layer, exact model identifier, Flow ID, and native binding
- remain separate typed facts. The title grants none of the identity,
- authority, availability, or routing those facts establish.
+ Complex, member, exact model identifier, Flow ID, and native binding
+ remain separate typed facts. The title grants none of the identity,
+ authority, availability, or routing those facts establish.
  
  ## A grunt job goes down, not up
  
- A simple job — a book rebuilt, a page published, a module located, a file moved — goes to a Tertiary or a Quaternary; a Secondary is never in charge of redoing a book. Once a Secondary has figured out what to do, the doing is handed down.
+ A simple job — a book rebuilt, a page published, a module located, a file moved — goes to Sonnet or Haiku. Once Opus has figured out what to do, the doing is handed down.
  
- ## A design decision goes up, to the Primary
+ ## A design decision goes up, to Fable
  
- A Secondary passes every design decision through its own Primary and acts on the Primary's decision. A Secondary uses its Primary freely.
+ Opus passes every design decision to its Fable and acts on Fable's decision. Opus uses its Fable freely.
  
- A Primary is reached through its Secondary for a question, a design or a judgment; the core Primary of an aspect reaches a topic Primary of its aspect directly when it helps a design while the living is talking to it. When no Secondary is live, the flow that needs the Primary starts one. When one cannot be started and something depends on the Primary being reached, the flow messages the Primary itself and says in that message that the Secondary route failed and why.
+ Who reaches whom is the complex's routes, in its definition; Fable is reached through its Opus where the routes say so.

### Proposal 2: Routes are the definition's · psyche-belief › vision/aspects.md

**Comment** Both sections explained the routes by layer; the routes are now each complex's own, written in its definition.

- ## Flows of one topic talk at the same layer across aspects
+ ## Routes are the definition's
  
- Flows of the same topic talk at the same layer across aspects, so a Psyche topic Secondary and the Mind Secondary of that topic speak directly. Field reaches Psyche through Mind, unless Psyche has just spoken to Field. This holds for every aspect.
+ Who speaks to whom, within an aspect and across aspects, is the routes each complex names in its definition; a message off the routes is refused. Field reaches Psyche through Mind, unless Psyche has just spoken to Field.
  
- ## Within an aspect, a flow speaks to the layer next to it
- 
- Within an aspect, a flow speaks only to the layer next to it: a Quaternary to its Tertiary, a Tertiary to its Secondary, a Secondary to its Primary.
- 
- The tracker, a Quaternary, reaches any Secondary directly, in any aspect, and a Primary only through its Secondary.

```datom
+ ; a complex, each member by its model
+ { designer
+   [ { fable Claude claude-fable-5-1 Medium
+       Perma Path.«/home/li/primary»
+       { [ spirit:core ] Refuse }
+       HarnessDefault
+       [ Speaks.opus Speaks.Living ] } ]
+   fable }
```
