# Flow, the living's words digested for the ethos rewrite

Every quote is trimmed verbatim from /home/li/primary/flows/875960/reports/aggregate-flow.md, which verified each fragment against its record by script; " … " joins trimmed fragments. A citation is `flow topic, date`; `distilled` names a psyche-skills skill. Design lines are quoted from /home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md and are the design's words, not his. Lines marked (flow's inference) are this digest's own.

## 1. Anatomy

- Flow: "Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows." — vision-flow, distilled
- Flow: "The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt." — vision-flow, distilled
- Flow: "I would like to have a flow component that works, that can launch flows, and that has hooks in the harnesses that send the right events to the flow component so that it can know the state of each flow." — 01e496 flowNexus, 2026-10-02
- Flow: "Flow is obviously a session so when we restart the whole context, that's a new Flow. It's a different context." — 41fa34 flowLifecycle, 2026-10-03
- Repository: "The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it" — vision-flow, distilled
- Metaflow: "Metaflow is a major abstraction and it's what we mostly think about. The Flow abstraction is a lower-level thing and it's not user-facing in almost any cases." — f5a6e9 flow, 2026-10-07
- Metaflow: "Let's call it a Metaflow. It's something that sort of continues through several flows, one after another" — bad807 metaflow, 2026-10-04
- Metaflow: "A flow could exist and not be a metaflow … The only thing we need is for us to know that a flow is a metaflow. If a flow is a metaflow we'll be addressing it by its long-term metaflow name." — d4ae97 flow, 2026-10-07
- Metaflow: "referring to the meta flows and then having a reference in the meta flow memory to Wispr Flow's [sic] current for it and maybe its predecessor. I don't see the point of putting that data with the flow data." — f5a6e9 flow, 2026-10-07
- Metaflow: "all metaflows will essentially have an aspect. And then the struct, will contain their details, such as their- their- the name of their topic" — 445410 metaflow-ethos, 2026-10-09, notion
- Metaflow: "this metaflow entry, is sort of acting as a pointer in one of its capacities to the current flow that it corresponds with." — d4ae97 flow, 2026-10-08, notion
- Voice: "A role may be a voice or a worker. … A voice is a permanent Metaflow. It's a Metaflow that might go to sleep but can always be woken" — f5a6e9 flow, 2026-10-07
- Voice: "I want to change the name "voice" to describe the long-running seed [sic]. There's no voice, right? The variants are all of the different voice aspects directly." — d4ae97 flow, 2026-10-07
- Voice: "I think rather the voice is a struct that contains the aspect and the layer, and the flow has a role, one of which is a voice." — bad807 ethos, 2026-10-04
- Voice: "A voice is an aspect carrying a rank, `Psyche.Primary`: Psyche, Mind, Field by Primary, Secondary, Tertiary, nine voices." — vision-flow, distilled
- Role: "I don't think "worker" is the right term. Maybe "goal" or something like that." — f5a6e9 flow, 2026-10-07
- Side flow: "A side flow is a job, not a voice: focused, not long-lived, gone when its mission is done" — vision-flow, distilled
- Aspect: "The aspect is now, I think, part of any metaflow. It shows us which aspect of that topic it's actually taking care of." — ebbe30 aspects, 2026-10-09
- Aspect: "Mind would be implementing, documenting things. Field would be maintaining, debugging, deploying, using an actual mutating system" — 41fa34 clojure-flow, 2026-10-08
- Layer: "This primary-to-quaternary division is sort of universal in any type of metaflow or flow." — d4ae97 models, 2026-10-08
- Layer: "All of this stuff that has to do with layers should be explained in layers and not models, and then we should just have a layer-to-model skill." — 445410 flow, 2026-10-09
- Layer: "quaternary, for now, is the same model as tertiary with a lower effort." — f768df layers, 2026-10-05
- Model: "The model is declared once, as typed configuration in Flow, mutated only through the meta wire." — vision-model-roles, distilled
- Address: "Mind.Astra not a string; two variants!" — 91ea9f addressing, 2026-10-02
- Address: "There are two registries: - The true registry with the actual IDs - Just the voices. It doesn't have the flow ID, meaning it'll just pass it to whoever is the current voice … The syntax would be `psyche.primary`" — 5578cc flow, 2026-10-03
- Address: "messaging doesn't require knowing its flow ID at all. In fact it would be bad practice to try to send to a flow ID because the sender doesn't know if that is the current flow of that voice." — d4ae97 datom, 2026-10-07
- Topic: "every topic has its own flow. A topic could involve more than one skill but essentially that flow would be in charge of that whole topic." — d4ae97 messenger, 2026-10-08
- Topic: "the topic is always there and by, well, the topic for the current metaflows that we have that essentially are [topicless] is core." — 445410 flow, 2026-10-09
- Topic: "technically it should be uncapitalized core and ethos since theyre the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one" — 445410 flow, 2026-10-09
- Flow id: "The flow ID is not a string, it's a hash. … The Nexus just thinks of it as a hash, which is maybe an integer with certain kinds of traits." — edf227 identifiers, 2026-10-03
- Flow id: "We decided on three words … This three-word camel case format conversion" — d4ae97 datom, 2026-10-07
- Flow id: "Let's just leave it as a string for now, but let's put a comment there that says the string is very unideal, and we need a real ID based on the real hash bit" — ebbe30 ethos, 2026-10-09
- Flow id: "the word ID library that I want is not implemented specifically for Flow ID. It's generic so we can use it for any hashes of any size." — 9fb0ad ethosLibrary, 2026-10-03
- Flow id: "there's no reason for us to make the model check the flow ID. It should get it in its prompt because … we can get its session ID before it even starts." — 5578cc flow, 2026-10-03
- Title: "When we write the name of the thread in the harness, we don't actually mention the model … I'd rather see the word-based one." — d4ae97 flow, 2026-10-07
- Title: "Start these two topic flows with the psyche::{topic}, either core, flow, or ethos, and then the layer: primary and secondary. … We can put the flow ID after that" — 445410 flow, 2026-10-09
- Request kinds: "The abstractions that are sent in flows are not letters. We are going to have actual types." — f5a6e9 flow, 2026-10-07
- Request kinds: "Different messages will have different flow-waking effects." — d4ae97 messenger, 2026-10-08
- Lock: "No, Flow locks the sessions and [Orchestrate] locks the files. Those are different things." — dea0ba locking, 2026-10-03
- Lock: "the lock, which we need in order to roll over a metaflow when it's spawning itself into a new flow." — e5a0bc flow, 2026-10-07
- Delivery: "I don't think that it's Flow's job to hold messages. … The message doesn't have to know about the flows. It can also just talk in terms of metaflows." — f5a6e9 flow, 2026-10-07
- Delivery: "Who speaks to whom … is the vision-aspects skill's. Flow refuses a request that leaves those routes." — vision-flow, distilled
- Launch: "A Nexus component decides the system prompt and everything about a launch" — vision-flow, distilled
- Launch: "The brief should be actually fairly small, like a small paragraph at most. … 100:1 or 1,000:1 leverage" — d4ae97 contextModules, 2026-10-07
- Launch: "There should be only one prompt when we start a fresh flow, not two" — d8df70 launch, 2026-09-24
- Launch: "their first last response is to give a presentation of their context, to distill their context for a vision." — 445410 flow, 2026-10-09
- Modules: "The context modules need to be able to be inserted either in the system prompt or in the first prompt." — e5a0bc flow, 2026-10-07
- Modules: "it must use a registry which uses the `{ Subaspect.[Vision Knowledge ...] Topic:Name }` to store the location of each, using the containing source with hash (blake3 I believe is what we use?) and relative path of each. those payloads live on the meta signal" — f5a6e9 contextModules, 2026-10-09
- Modules: "Depending on which kind of metaflow we're starting the harness in, we're going to load different parts of the intent in the system prompt … the vision goes in the user prompt." — d4ae97 flow, 2026-10-07
- Configuration: "We need to allow the Nexus to have its configuration loaded atomically so that it can live in separate files in different repositories." — 73ada7 nexus, 2026-10-09
- Refresh: "It's more like 20% to 40%." — d4ae97 flow, 2026-10-07
- Refresh: "the only thing that isn't passed through to the next flow … are the bits … still in debate, fuzzy, or haven't been ruled into the context modules" — bad807 metaflow, 2026-10-04
- Reap: "Reaping belongs to the refresh event, not to a later sweep." — vision-flow, distilled
- Hooks: "It makes perfect sense for the flow events to call the flow CLI to let the flow nexus know the state of that flow through the harnesses' interfaces, which are the hooks." — fe945a hooks, 2026-10-01
- Capsule: "The Capsule is the component that makes where a flow runs." — vision-flow, distilled; "Flow doesn't do any sandboxing for now" — dea0ba flowCorrections, 2026-10-03
- Store: "the Clojure flow prototype, with its own database with metaflow addressing by metaflow name." — d4ae97 flow, 2026-10-08; "we need a registry to know which flow is active." — 41fa34 flow-registry, 2026-10-07

## 2. Against the current design

1. His: "The flow ID is not a string, it's a hash." — edf227 identifiers, 2026-10-03. Design: `FlowId.String ; unideal now: a real id built on the hash bits that identify a flow`.
2. His: "We decided on three words … This three-word camel case format conversion" — d4ae97 datom, 2026-10-07; "Let's do the name-based hash thing in the signal library." — fd0f97 identifiers, undated. Design: "FlowId.String is his word for now; a hash-based id is wanted later."
3. His: "nine voices" of "Primary, Secondary, Tertiary" — vision-flow, distilled. Design: `Layer.[ Primary Secondary Tertiary Quaternary ]`.
4. His: "I want ternary and quaternary voices. quaternary would be perfect to message when unsure who to message in an aspect." — bad807 voices, 2026-10-04. Design: `Layer.[ Primary Secondary Tertiary Quaternary ]` (agrees with this, against the distilled line in 3; flow's inference).
5. His: "Every native main session is titled `<Aspect> <Model> <FLOW_ID>`." — vision-model-roles, distilled. Design: "A thread's title is the address written short, then the flow's words, never the model".
6. His: "The titles of the remotes need to be the aspect, the power, and then the flow ID, always." — 03e825, 2026-09-21. Design: `{ Psyche flow Primary } startInputVital`.
7. His: "A flow is one run of a voice" — vision-flow, distilled. Design: `Metaflow.{ Address State Past Queue } ; one per address`, no Voice type.
8. His: "A voice is a permanent Metaflow." — f5a6e9 flow, 2026-10-07. Design: no voice and no permanence; every Metaflow is `Awake`, `Asleep` or `Ended`.
9. His: "A voice is an aspect carrying a rank, `Psyche.Primary`" — vision-flow, distilled. Design: `Address.{ Aspect Topic Layer }`.
10. His: "the flow has a flow ID and a role, one of which is a voice." — f768df voices, 2026-10-05; "A role may be a voice or a worker." — f5a6e9 flow, 2026-10-07. Design: `Flow.{ FlowId Session Process Events }`, no role.
11. His: "A flow could exist and not be a metaflow" — d4ae97 flow, 2026-10-07; "A side flow is a job, not a voice" — vision-flow, distilled. Design: "A launch names a metaflow by its address"; every flow belongs to one.
12. His: "It's a specialized flow so it takes another kind of variant for its specialty, like the monitor or the voice" — 88475f specializedFlows, 2026-09-25. Design: no specialty field.
13. His: "It's basically PascalCase of a certain number of words" — d4ae97 flow, 2026-10-08 (corrected 2026-10-09 to camelCase). Design: `Topic:Name ; camelCase, checked where text enters`.
14. His: "If a message can't be delivered, then we try a higher power. … if there's nothing higher then we try lower." — 836818 flowNexus, 2026-09-24. Design: "Up is the same topic, one layer above, within the sender's aspect; above Primary it is refused NoneAbove."
15. His: "If the adjacent rung is absent or unavailable, routing advances to the next running rung in that direction, so Low may reach High when Medium is not running." — vision-model-roles, distilled. Design: `Recipient.[ Address Up ] ; Up: same topic, one layer above the sender`.
16. His: "The message logic has to figure out where that's supposed to go so it can ask the flow … or maybe the flow figures it out." — 93ba9f messagingInterface, 2026-09-26. Design: "Flow resolves Up from the sender's identified address and includes it in the returned lock."
17. His: "Power remains a separate typed behavioral property. High, Medium, Low, and Ultra Low" — vision-model-roles, distilled. Design: `Layer.[ … ] ; decides the model`, no power type.
18. His: "You should make it a good practice to start when you're getting to 30% of your context" — f55ec8 flowRefresh, 2026-09-16; "At a certain maximum, at 60%, the flow basically has to change over" — 6cc91b flowLifecycle, 2026-09-14. Design: `Handover.Integer ; 20` `Refresh.Integer ; 40`.
19. His: "Let's not restart a flow that only has less than 15% of its context used … The flow can still restart if it's at 15-20% of its context and it changes direction dramatically" — 692df8 flowLifecycle, undated. Design: no floor and no change-of-direction trigger.
20. His: "The bottom of each aspect is what is going to run the flow refresh mechanism for now." — 02dda6 flow-refresh, 2026-10-07. Design: "No model decides any step."
21. His: "a component to just keep track of whether success has been launched now and it's working, which could be checked by a small model" — fd0f97 flowLifecycle, undated. Design: "No model decides any step."
22. His: "Its ancestor is known exactly, so the ancestor is the name." — vision-flow, distilled; "field Sol - of meaning: descendant of, and then the ID of your ancestor" — 33ba2b, 2026-09-18. Design: title is the address, then the flow's own words.
23. His: "I don't think that it's Flow's job to hold messages." — f5a6e9 flow, 2026-10-07. Design: "Flow keeps its queue." `Queue.Vector<Request>`.
24. His: "messages essentially get passed on to both the new and the old flow until the old flow logs out to the new flow." — e1953c flowLifecycle, undated. Design: "While a refresh is under way the metaflow is locked and a lock request is refused Locked".
25. His: "it would get woken up by Flow if the new flow was unable to start, and tell it, "There seems to be a problem with your flow. Unable to recycle your flow."" — fd0f97 flowLifecycle, undated. Design: steps end at "reap the predecessor"; no failed-successor path.
26. His: "A raw flow send … should be a meta socket operation and then we have a more lock-enabled deliver message." — 93ba9f messagingInterface, 2026-09-26. Design: "N3: … this design keeps them on the ordinary socket."
27. His: "a meta socket for debugging for adding already existing processes." — d8df70 flowTool, 2026-09-24. Design: "Bind … on the ordinary socket: a process binding itself is ordinary work".
28. His: "Things like that should not wake up the flow until there is a situation that arises … given the particular state of that flow" — d4ae97 messenger, 2026-10-08. Design: by variant only, `Notice.String ; wakes nothing`, `Order.String ; wakes`.
29. His: "If we just feed the text in the memory, that would solve the problem." — e5a0bc flow, 2026-10-07. Design: `Source.{ Repository.String Hash.Blake3 Path }`.
30. His: "But the Flow's memory will live in mind" — 9993b5 mindMemory, 2026-09-17. Design: Flow's own Memory at `StorePath`.

## 3. Behaviour he named

- Wake: "if a message is intended for it, flow would automatically... … trigger the flow to be spawned with the right context modules depending on the message." — f5a6e9 flow, 2026-10-07
- Wake: "If we're satisfied with the state of a certain topic at a given point, that flow should not be woken up." — d4ae97 messenger, 2026-10-08
- Wake: "You can't wake up all of the flows, all of the meta flows. The flows are current so we need a registry to know which flow is active." — 41fa34 flow-registry, 2026-10-07
- Sleep: "If nothing is cooking then when things calm down, the sun (meaning the primary layer) can unwind" — bad807 metaflow, 2026-10-04
- Queue: "When the message that does have the waking effect at that particular state in that flow comes in, it will also trigger checking the queue for that flow, so that the whole queue is checked in order, from the first received to the last." — d4ae97 messenger, 2026-10-08
- Drain: "The message that just got in and triggered the queue will come in at the end of the prompt and it'll be a vector of all these objects, which are typed by variant name" — d4ae97 messenger, 2026-10-08
- Drain: "inject a bunch of other stuff that has been queued in preparation for that particular flow to be woken up, so that it would know all of this as soon as it woke up." — bad807 flowContextInjection, 2026-10-04
- Hold: "If there's no registry or if the registry says "in transition" … the message can sort of be held … We can wait a few seconds at least to see if there's a new flow." — d8df70 messaging, 2026-09-23
- Lock: "The message is going to ask for a lock, which should be time-bound so that it doesn't lock forever. If it does get a lock then the message nexus can send that object over to Flow with the message" — f5a6e9 flow, 2026-10-07
- Lock: "It locks the message for the session to send the message, then it sends the message, then it removes the lock." — 1b8ac0 messaging, 2026-09-21
- Lock lapse: "if … a flow is idle … then all of its locks are automatically forfeited by protocol." — 01a03d6e locks, 2026-08-26
- Lock lapse: "any lock remains, they can be removed forcefully by another flow since any lock must be released" — 01a03d6e locks, 2026-08-26
- Refresh at threshold: "When a model reaches a certain context window, whoever is in charge of refreshing should get a message … the flow itself needs to know so that it can create a handover response. At that point that same hook system picks up the final response and essentially locks the messages" — e167d8 refresh, 2026-09-26
- Refresh at idle: "sessions can be reloaded in the new harness one at a time as they go idle. As soon as the session goes idle, the hook kicks in." — 7328f4 hooks, 2026-09-30
- Refresh lock: "It has told the messenger to block that flow inbox and outbox, and so the messenger caches both sides." — b81560, 2026-09-19
- Refresh switch: "it just blocks until the new pane or seat is ready to receive and then the old one in the same swoop. We verified it is not active and then we exit it." — 836818 flowNexus, 2026-09-24
- Refresh switch: "A new flow starts receiving as soon as it has its start prompt and then the old seat or flow is killed or removed. Its conversation or its thing is archived." — 836818 flowNexus, 2026-09-24
- Refresh outbox: "The new flow also knows what the message was that was sent to another flow by its ancestor." — b81560, 2026-09-19
- Refresh caller: "the Flow CLI will check the process that called it. We can allow flows to refresh themselves safely." — d8df70 flowTool, 2026-09-24
- Succession: "There's a check, and the new flow knows that it's the current flow. The old flow doesn't need to think that it has become the new flow." — fd0f97 flowLifecycle, undated
- Reap on refresh: "Whenever you refresh a flow, you need to reap the ancestor, right?" — b81560, 2026-09-19
- Reap on refresh: "A refreshed flow takes the replaced end out of receiving messages, so a dead end is never left registered and addressable." — vision-flow, distilled
- Reap on end: "if a flow gives its last final response and it's clearly this Datom type final response … then we don't need a lot of judgment to reap." — b05237, 2026-09-19
- Hooks report: "Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action … Polling is forbidden" — vision-flow, distilled
- Hooks report: "What about if we use hooks at the start and the end of the Claude or the Codex session to register or unregister that session from the registry?" … "then you just use the process going out as the unregistry hook." — d8df70 messaging, 2026-09-23
- Hooks report: "We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it." — cf3553, 2026-09-19
- Compose modules: "We pass a list of which type and name for the context we want to load at each layer in the system prompt and in the origin startup prompt. … the flow nexus just inserts those values in the right places." — edf227 contextModules, 2026-10-03
- Compose modules: "All that matters is that everything comes in as one block." — e51411 launch, 2026-09-24
- Compose modules: "We need to maintain this configuration in Flow that we have to update when we add a new skill to add it to the list. That would be the meta." — edf227 contextModules, 2026-10-03
- Check hashes: "using the containing source with hash (blake3 I believe is what we use?) and relative path of each." — f5a6e9 contextModules, 2026-10-09
- Reserve id: "We should not make it the subflow's job to claim an ID. That should be done for the flow as it started. … This could easily be done by code." — e51411 launch, 2026-09-24
- Identify: "Not by trusting that the flow put its ID in the message, but from the virtue of the process that called it" — 8904b1 skills, 2026-09-28
- Ended flow: "a message sent to it after that returns to its sender with notice that the flow has ended." — vision-flow, distilled
- Request id: "It is assigned a request ID, by which it asks later for status … When the subflow is done, the requester receives a message if it is still the flow in charge." — vision-flow, distilled
- Crucial start: "we can start a flow if it's missing, it needs to get a message, and it's considered crucial. All the medium and high flows are considered crucial." — 836818 flowNexus, 2026-09-24

## 4. Open before him

The design's section 4, its words (whether he answered each was not witnessed by the design):
- "Book 17, ruling 1: the whole vision-flow-ethos file … Ruling 2: the dependency line in vision-flow. Ruling 3: where a request lands in an awake flow, (a) end of prompt, (b) tool-call return outside the prompt, (c) other."
- "Book 18 (the Nexus starts), ruling 1: Blake3 and the meta-socket payloads; (c) the hash is another."
- "Book 15, ruling 1: Encodable. Ruling 2: Bytes<N> intrinsic. Ruling 3: the Library root … Ruling 4: simple and extended forms."
- "Book 11, ruling 1: the four request kinds … Ruling 2: Queue on the record. Ruling 3: the waking rule in vision-messaging. Ruling 4: the rule in vision-flow."
- "Book 14, ruling 1: the Today section in vision-flow."
- "Book 10, rulings 1 to 5: Flow manages metaflows; layer decides the model; refresh at 20 to 40 percent; modules make the flow; requests and the lock. Ruling 6: sources."
- "Book 3, rulings 4 to 6 (thresholds, refresh operations Tell, Lock, Reap, Unlock, subject end without an end-goal field): partly carried here"
- "Book 1, rulings 2 to 8 (Facet word, location, role placements): superseded in shape by Configure."
- "pending his ruling 1 of the Flow Nexus vision, third edition: the Address form, one Aspect and Address type with the Metaflow record { Address State Past Queue }"
- "Current best, not before the living: the Memory records Module.{ Key Source }, Model, Threshold, Metaflow and Lock; … the lock, Bind, Identify and Deliver queries, responses and refusals of the flow socket; the Message gate"
- "who resolves Up is before the living in 73ada7's «Who works out where send up goes»"
- "N3: Lock and Deliver on the ordinary socket or on Flow's meta socket (Message's fork F2)"
- "N8: whether queueing a busy awake flow and draining at the next Stop is right"
- "FlowId.String is his word for now; a hash-based id is wanted later."
- "The type of the dense title string." / "Whether an implementation kind survives as a topic of a Mind metaflow." / "Removal of the machine line in vision-messaging lines 8 to 9." / "73ada7's Message and Flow ethos draft"

His questions with no answer in the aggregate (flow's inference that none was given):
- "Is this a kind that can yield so we can call the Flow ID method on Flow ID that is `as_words` or something?" — 9fb0ad ethosLibrary, 2026-10-03
- "What's the name that we put them all under, these three that are very similar, or are these going to actually diverge and take their own shape?" — d4ae97 flow, 2026-10-07
- "What's this section about, with `composed`, `open`, and `spawn`?" — d4ae97 ethos, 2026-10-07
- "I'm not sure if it should be unlimited in size." — d4ae97 flow, 2026-10-07
- "There's no role type … Where is the canonical place to find those types?" — bad807 contextModules, 2026-10-04
- "Can subflows use subflows themselves?" — d4ae97 datom, 2026-10-07
- "Where are those hooks? What are those hooks calling? … Is this Flow, or is it Transcript, or is it something else?" — 6997eb pipeline, 2026-10-01
- "What's the solution to address the transcripts of both?" — 6f51ad transcripts, 2026-09-29
- "I'd also like to know what happens with archives and if they're searched differently." — 836818 flowNexus, 2026-09-24

## 5. Aggregator's own tensions

- Title: "Distilled vision-model-roles titles every native main session `<Aspect> <Model> <FLOW_ID>`. Distilled vision-flow titles a flow `{ Psyche core Secondary <id> }`, with no model. So the two distilled skills disagree with each other."
- Layer count: "distilled vision-flow says Primary, Secondary, Tertiary and nine voices. Raw records from 2026-10-03 to 2026-10-08 … speak of a fourth layer, quaternary, in every aspect."
- Topic case: "PascalCase (f5a6e9 flow, 2026-10-08) is corrected to uncapitalized camelCaseExpression core:Name (9fed42 and f5a6e9 flow, 2026-10-09), which is the later explicit correction."
- Flow id: "a three-word id is wanted … and the id is a hash … On 2026-10-09 (ebbe30) it is 'leave it as a string for now'. Distilled vision-flow says 'written in words'."
- Refresh threshold: "30 percent of context … against 20 to 40 percent (d4ae97 2026-10-07), and a restart at 15 to 20 percent on a dramatic change of direction (692df8, undated)."
- Voice and metaflow: "distilled vision-flow says 'A flow is one run of a voice' and does not name the metaflow. Raw f5a6e9 flow, 2026-10-07, says 'A voice is a permanent Metaflow'"
- Naming: "distilled vision-flow names a session after its direct ancestor. f5a6e9 flow, 2026-10-07, asks that flows be referred to through the metaflow … and not by flow id."

## Sources

- /home/li/primary/flows/875960/reports/aggregate-flow.md, read whole by this flow
- /home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md, sections 1 to 3 read by this flow; section 4 as quoted in the aggregate
- Provenance receipt: unavailable; no PROVENANCE handoff exists for this report
