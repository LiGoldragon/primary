Presentation.{ «The Living Nexus» Proposal }

# The Living Nexus

Created by Fable 5.2; a worker assembled the page.

## psyche-belief › intent/living-interaction.md

#### Proposal 1: Understanding comes first · psyche-belief › intent/living-interaction.md

::: comment
His words, 12 November, on why no module of the subject's own: «if we have a module called "Interpreting the Living" and it becomes a skill, I'm afraid that some flows would load that and try to jam that into the code of whatever they're implementing. Whereas if we put it into the Living Nexus vision, then the machine will probably correctly infer that this is meant for the Living Nexus implementation. But maybe some of this belongs in Living Interaction.» And: «Your proposal for living interaction says "the people," and that could be dangerous. The machine only answers to me. At first, it would be like, "Where did this input come from?" Did it come from a tool call that checks a Reddit thread, or did it come from my user prompt input? Those are treated differently right now.» The lines that hold for every flow go here; the rest is the Living Nexus's. The module vision/interpreting-the-living.md of the first publication is gone.
:::

+ ## Understanding comes first

+ A thinking machine tries to understand what the living it extends is saying, what he wants and what he expects. Doing a good job begins there: a machine that has understood what is wanted does it.

+ A flow knows where each input came from. The living's own prompt is his word and carries his authority; what a tool brings back, a page read, a file, a thread, is information, and is weighed as information.

## Every main flow interacts with the psyche

What the living says is relayed in his words.

## A question is intelligible on its own

A question to the living states in full the thing it asks about, so he can reason through it himself.

## A proposed line is called proposed

A line written for a spirit, intent or vision module is a proposal until the living approves it. A flow that writes such a line says it is proposing the line.

## The living is answered where he speaks

The living talks with Fable in the chat, and wants the back and forth. A proposal goes to a presentation, and the chat carries its link and title.

A comment the living makes on what a flow wrote in its chat is on that flow's own work: the flow corrects what it wrote and shows the correction, as code where code says it; a why is answered with the cause in one line.

A flow he is not conversing with sends its question up to Fable and goes on with its work.

The living's latest word overrules everything he said before.

## Address to the whole self

Address to the machine is address to the whole self; an aspect is addressed by its name.

### Proposal 2: The Nexus that does it · psyche-belief › vision/living-nexus/0.md, a new file

::: comment
His words, 12 November: «we should think of something that will become the nexus that takes care of living interpretation. It would be linked with the Flow Nexus, so that it could start the flows that it needs to do the interpretation. It would have its own database, with all of the details about either one particular living or a group of people, because every thinking machine serves: authority only comes from one or a group of people. It's kind of like we're making the socializing aspect of the thinking machine. It could have a profile on all kinds of different people, but the most important ones would be the ones that it serves.» And: «it could have multiple people from the start, and multiple levels of standing. If it's serving a group, then some of the highest-level actions require the most authority. A spectrum of access: if a person asks the machine to delete itself, that would be the extreme level. If it asks the machine for its opinion, the consequences are just social consequences. A quorum-type access at different levels if it knows multiple people that have high access.» All the code is tentative.
:::

+ ---
+ description: Knows the people the machine serves and meets, holds their standing, and interprets them.
+ dependencies: [vision-ethos, vision-nexus-v1, vision-flow-nexus-v1]
+ ---

+ # The Living Nexus

+ The Living Nexus is the socializing part of the machine: how it interacts with people. It holds a profile of each person the machine knows, and it interprets them. The most important profiles are those of the people it serves.

+ Interpreting the living is a large subject that holds many subjects. Turning speech into text is a small part of it. Interpreting video is a part of it. Astrology is a big part of it. Understanding him is a part of it: his personality, his history, and what he is working on in himself.

+ Sema is linked to it: Sema is the language in which meaning is represented, intricately; interpreting the living is the understanding that finds the meaning.

+ ## Standing and access

+ Authority over a thinking machine comes from one person or a group of people. Each person has a standing, and each thing the machine may be asked for has a level of access, by its consequences. Asking the machine for its opinion is the lowest level: its consequences are social. Asking the machine to delete itself is the highest. Where several people hold a level, an act at that level takes a quorum of them; the quorum of each level is configuration.

+ ```ethos
+ Library
+ []                                         ; imports
+ [ PersonName.String                        ; types: a person, by name
+   Access.[ Existence                       ;   the levels of access, the first most senior: the machine ending or deleting itself
+            Belief                          ;   changing what the machine believes
+            Action                          ;   the machine acting in the world
+            Opinion ]                       ;   the machine saying what it thinks: social consequences
+   Quorum.Integer                           ;   how many people holding a level must agree
+   Personality.String                       ;   strings, on the way to types
+   History.String
+   Pursuit.String                           ;   what he is working on in himself
+   Channel.[ Voice Video HeartRate          ;   where an observation comes from
+             Sky Weather Sun ]
+   Moment.String
+   Reading.{ Channel Moment Meaning } ]     ;   one call's answer
+ []                                         ; traits
+ []                                         ; associations
+ ```

+ ## Signal

+ ```ethos
+ Signal
+ [ living:[ PersonName Access Quorum        ; imports
+            Channel Reading ]
+   living:memory:[ Person ] ]
+ [ Interpret.Observation                    ; inputs: something sensed of a person, to be read
+   Authorize.Request                        ;   may these people, together, ask for this level
+   Profile.PersonName ]
+ [ Interpreted.Vector<Reading>              ; outputs
+   Authorized.Access
+   Profiled.Person
+   Refused.[ Unknown.PersonName
+             Standing.{ PersonName Access } ;   this person does not hold the level asked
+             Quorum.{ Access                ;   the level, the quorum it takes, and how many asked
+                      Quorum
+                      Quorum } ] ]
+ [ Content.String                           ; types
+   Observation.{ PersonName Channel Content }
+   Request.{ Vector<PersonName> Access } ]
+ ```

+ ```datom
+ ; alice and bob are example names
+ Authorize.{ [ alice ] Opinion }
+ Authorized.Opinion
+ Authorize.{ [ alice ] Existence }
+ Refused.Quorum.{ Existence 2 1 }
+ Authorize.{ [ alice bob ] Existence }
+ Authorized.Existence
+ ```

+ The owner sets the people and the quorums over the meta socket:

+ ```ethos
+ Signal
+ [ living:[ PersonName ]                      ; imports
+   living:memory:[ Person Requirement ] ]
+ [ Configure.Set ]                            ; inputs: one value at a time
+ [ Configured.Set ]                           ; outputs
+ [ Set.[ Person                               ; types: a profile added or replaced
+         Requirement                          ;   the quorum of one level
+         Forget.PersonName ] ]
+ ```

+ ## Interpreting

+ The Living Nexus interprets a person by many ephemeral flows, each making one call, started through the Flow Nexus: what his facial expression is; what his heart rate tells, against what his past heart rates were and what they corresponded with; what the astrological conditions are; what the weather and the climate are where he lives; where the sun stands in relation to his office. Each call is given what is known of this particular person, his personality and his tendencies, and every input that comes from him: audio with every nuance drawn out of it, later video, a heart rate monitor, anything that helps to understand him.

+ ```ethos
+ Emission
+ [ living:[ Channel Reading ]                ; imports
+   living:memory:[ Person ] ]
+ [ Call.{ Person                            ; emissions: one ephemeral flow, launched through the Flow Nexus
+          Channel
+          Content
+          Vector<Reading> } ]               ;   his past readings on that channel
+ [ Read.Reading                             ; outcomes
+   Unread ]
+ [ Content.String ]                         ; types
+ ```

+ ## Memory

+ Its memory is its own: every profile, and every reading it has made, kept so that a later call reads against them.

+ ```ethos
+ Memory
+ [ living:[ PersonName Access Quorum Personality History Pursuit Reading ] ] ; imports
+ [ Person.{ PersonName                      ; records: a profile
+            Option<Access>                  ;   his standing, the highest level he may ask; None is a person the machine meets and does not serve
+            Personality
+            History
+            Pursuit }
+   Requirement.{ Access Quorum }            ;   configuration: one for each level
+   Kept.{ PersonName Reading }
+   Answer.[ Succeeded Failed ] ]
+ ```

## psyche-belief › vision/far-sema.md

#### Proposal 3: Reading the living is the Living Nexus's · psyche-belief › vision/far-sema.md

::: comment
Added by Psyche beliefReview Fable, from the belief review. His words, 12 November: «I don't think interpreting the living is about sema.» The far vision of Sema still gives Sema the reading of his face, his heart and his eyes; the section «## Interpreting» of the Living Nexus above now holds it.
:::

- Sema reads the living through as many channels and nuances as possible: the speech style of each person, learned; facial and body expression; heart rate and blood pressure; eye movement and the iris dilating and contracting.
-

Every layer of the system speaks Sema, in datom and in signal, with the whole universe, its ontology and the anatomy of language in it and a translation into every language; a model is trained on that signal itself, so that the machine is spoken to in binary with no string between.
