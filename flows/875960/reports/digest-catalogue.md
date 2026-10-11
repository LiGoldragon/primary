# Digest of the Flow, Nexus and Ethos record catalogue

Drawn from flows/9519a1/reports/flow-ethos-records.md: its section 1 (comparison) and the verbatim records of its section 3. Each point gives the living's words, then record id, flow, topic file, date, then the design (flows/f5a6e9/reports/flow-buildable-design.md) or stage line the catalogue says they contradict. What a design or stage line says is the catalogue's claim; [W] and [I] are its subflows' marks (W: literal in the text; I: their interpretation); [9519a1] marks a point that flow says it witnessed itself. "cat:" marks the catalogue's own inference. Words a record does not quote from the living are marked (heading) or (agent-written).
## 1. Disagreements
### Flow id
- "We can use 6 characters easily to fit that in" (the pair plus the flow) — R0530 e1953c flowIdentity undated — design L22-25, L954: FlowId.String, hash id later [I]. cat: possibly superseded by the word id (R0439, R0457, R0481).
- "we use the first 2 to identify the cluster" — R0531 e1953c flowIdentity undated — design L22-25, L72-75: no cluster or triad in id or Address [I].
- "The flow ID is not a string, it's a hash." — R1181 edf227 identifiers 2026-10-03 — design L22-25 and stage flow-ethos L7: FlowId.String [W]. cat: possibly superseded by R1117.
- "Let's just leave it as a string for now, but let's put a comment there that says the string is very unide[al]" — R1117 ebbe30 ethos 2026-10-09 — stage flow-ethos L7: `FlowId.String` with no comment [W].
- "We should not make it the subflow's job to claim an ID. That should be done for the flow as it started." — R0226 e51411 launch 2026-09-24 — stage flow-ethos L86-87, L133, L155: Codex reserves no FlowId, `Option<FlowId>` claimed at Bind [W].
- "we can get its session ID before it even starts" — R0341 5578cc flow 2026-10-03 — design L626-628, stage flow-ethos L86-87: Codex gets an id only at bind [I].
- "its Flow ID in a file, even there in a Git-ignored file" — R0088 f55ec8 flowIdentity 2026-09-16 — design L622-626, stage operation L85: id through the FLOW_ID environment variable [I].
### Layers and voices
- "nine voices" (vision-flow line 22, distilled) — design L31-35, stage flow-ethos L12: four layers, Quaternary included [9519a1].
- "a paired flow between Claude and Codex"; "There's going to be a codex and a Claude equivalent." — R0059 bcd02a paired-flows 2026-09-13; R0083 b49251 psycheFlows 2026-09-16 — design L72-75, L80-81, L219-222: Address { Aspect Topic Layer }, one Harness per Layer; stage flow-ethos L30 [I].
- "We should also have Codex primary, secondary, and tertiary." — R0296 caf622 Luna-Flow 2026-09-29 (R0523 b666e7 flows undated) — design L219-222: Model keyed by Layer alone, Address has no harness [I].
- "the effort ... it's a property, the data of the model variant" — R0264 b7ba00 flowAnatomy 2026-09-26 — design L219-222 Model {Layer Harness Native}; stage meta L92 ConfigureModel {Layer Native} [W].
- "It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary" — R0288 5ac3a3 flow 2026-09-27 — stage signal L186, L189, L255, meta L121: PowerLevel.[ High Medium Low UltraLow ] [W].
- "All of this stuff that has to do with layers should be explained in layers and not models" — R0467 445410 flow 2026-10-09 — stage signal L189, L255: PowerLevel, ModelName, Effort [I]; stage meta L92 ConfigureModel lacks the design's Harness [W].
- "The syntax would be `psyche.primary` because it only has one." — R0339 5578cc flow 2026-10-03 — design L72-79: Address a three-field struct with Topic [I].
- "It's not a hard rule; it's guidance." — R0340 5578cc flow 2026-10-03 — design L380-384, L797-800: OffRoute a hard Lock refusal [I]. cat: possibly superseded by the approval at design L905-908.
- "A flow could exist and not be a metaflow" — R0430 d4ae97 flow 2026-10-07 — design L58-75, L619-622, L752-770: every Launch, Wake, Bind carries an Address [I].
- "If we have the metaflow type and it doesn't have any vectors" (notion) — R0450 d4ae97 notion/flow 2026-10-08 — design L80-89: Metaflow carries Past.Vector, Queue.Vector [I].
- "each one uh, variant of either psyche, mind, or field" (notion) — R0458 445410 notion/metaflow-ethos 2026-10-09 — design L68-75: Aspect a field of Address [I]. cat: possibly settled by R0454.
- "we're going to replace the system prompt with the spirit"; "three levels within: spirit, intent, and vision" — R0434, R0442 d4ae97 flow 2026-10-07 — design L36-42, stage flow-ethos L13: Subaspect has no Spirit [I].
- "spirit being first and, in the field, compensation is above trial" — R1113 d4ae97 ethos 2026-10-07 — design L36-42: Trial listed before Compensation, no Spirit [I].
- "Metaflow is a major abstraction and it's what we mostly think about." — R0544 f5a6e9 flow undated — stage signal L104-121, L216-217 keyed by FlowId; design L302-307 Stop, Report, Observe by FlowId [I].
- "Again you're centering this around Flow and not Metaflow" — R0545 f5a6e9 flow undated — stage signal L190-209: LaunchAttempt, FlowNode flow-centred [I].
### Title
- "Maybe you want to keep the flow ID there, but as a suffix" (notion) — R0068 dc1c58 notion/meta-flow 2026-09-14 — design L269-271: title is address then the flow's words [I].
- "It should also say Psyche Opus of." — R0151 1f96fc fieldMaintenanceAndRefresh 2026-09-19 (R0162 b81560 same words) — design L269-272: "never the model" [I].
- "I [also] want the session names to be by aspect and layer only" — R0337 5578cc flow 2026-10-03 — design L72-75, L269-271: title carries the Topic [I].
- "{ Mind Tertiary 918df4 }" — R0382 8475a9 voices 2026-10-05 — design L269-271: title never an id [I].
- "It should be Psyche Fable or Psyche Opus" (notion) — R0623 e51411 notion/message 2026-09-25 — design L269-271, L322-323, L389-395: Identify returns an Address, titles never the model [I]. cat: possibly superseded by R0666.
### Topics and names
- "which should also be followed by a colon" (the `Topic.custom:Name` form, vision/ethos.md line 191) — R0973 1d0733 ethos 2026-10-09 — design L26-29: `Topic:Name` [I]; distilled form against design L26 [9519a1]. R0986 081064 ethos 2026-10-10: "let's not block on it right now."
- "the core:Name type which is "camelCaseExpression" type with runtime checks" — R0970 1d0733 ethos 2026-10-09 — stage flow-ethos L8-9: `Topic.String` [I].
- "these will even become variants in actual Nexus components like Mind" — R0945 edf227 topics 2026-10-03 — design L26-29: Topic a checked string [I].
- "it should be an imperative voice, right, as in list" — R0873 01a03d6e archive-ethosInterfaces 2026-08-26 — design L290, L309, L339, L479 and stage signal L111-121: Metaflows, Current.Address, Configuration [I].
### Start and configuration
- "There should be no bootstrap binary ... a constant in the executable with a default configuration." — R0702 01a03d6e archive-nexus 2026-08-26 — design L137-150: Start requires socket and store paths, "no derived default names the store path" [W]; vision-nexus lines 89-94 ("starts with no arguments") against the same [9519a1].
- "first it should try to get its state from the default location for its Sema database" — R0703 01a03d6e archive-nexus 2026-08-26 — design L141-146, L864-866: empty Memory at the supplied StorePath [I].
- "new values must be accepted otherwise it's not doing what we want" — R0705 01a03d6e archive-nexus 2026-08-26 — stage meta L43-44, L107 Conflict; design L550-552 updates only Model, Threshold, Module [I].
- "socket paths (its own and the paths of all its other edge-sockets)" — R0714 acbb6006 archive-nexus 2026-08-27 — design L152-153, L503: Configure.Nexus carries no socket path [I]; vision-nexus lines 96-105 against design L462-479, L503 [9519a1].
- "There should be no datom in any Nexus." — R0792 8475a9 datom 2026-10-05 — design L137-140, L158-163: datom Start argument, Topic.String, Blake3.String; stage lib L8-11 [W]; vision-nexus line 56 against design L139-149 [9519a1].
- "The CLI translates datom into signal" — R0811 05c604 nexus undated — design L137-140, stage lib L39-45 [I]. cat: possibly superseded by R0795.
- "The Nexus component is not going to do the textualization at all." — R1216 564f55 archive-signal 2026-09-09 — design L139-150: Nexus parses datom Start, prints StartRefusal as datom [I].
### Store and errors
- "It's not going to be where the memory lives, so the mind is going to use it." — R0101 9993b5 flowAnatomy 2026-09-17 — design L205-212, stage operation L88-90: Flow keeps harness Events in Memory [I].
- "But the Flow's memory will live in mind" — R1246 9993b5 mindMemory 2026-09-17 — design L139-150, L199-236: own Memory root and store [I]. cat: possibly superseded.
- "We don't need to keep old stores of Flow and message." — R0199 836818 flowNexus, R0207 d8df70 deployment, 2026-09-24 — design L861-876: old file kept pending an answer [I].
- "The step to change the data is the same as the edit that's made to the source code" — R0935 c64ee3 ethos 2026-09-29 — design L142-146, L861-876: no migration, Memory has no upgrade trait [I].
- "the registry would become this Datomic" — R0630 e51411 messaging 2026-09-25 — design L843-859: sema-style Memory [I]. cat: possibly superseded by R0649.
- "errors are vocabulary, never strings" (vision-nexus line 68, distilled) — design L398, L497 Refused.Store.String; stage signal L277, meta L170 [9519a1].
### Requests and priority
- "Message priority is a datom head — `Priority.[HardAbrupt MiddleAbrupt Soft]`" (agent-written) — R0090 108ab0 operational-designMosaic 2026-09-17 — design L300-301: Deliver.{ Lock Request } has no priority; only stage meta L142-144 has it [W]; vision-messaging line 100 against the design [9519a1].
- "soft and hard was the wrong approach" (heading) — R0648 b7ba00 messaging 2026-09-26 — stage meta L142-144: HardAbrupt, MiddleAbrupt, Soft [W].
- "We shouldn't get the message ID." — R0644 (R0640) b7ba00 messaging 2026-09-26 — stage meta L8-12, L132, L141: Letter starts with MessageId [W].
- "the sender being called "owner" is fucking ridiculous" — R0644 b7ba00, R0640 93ba9f messagingInterface 2026-09-26 — stage meta L135-136: Sender.[ Flow Owner ] [W].
- "you have a vector of psyches with context" — R0652 b860be messageSize 2026-09-26 — stage meta L139-140: Content has Text and one Psyche [W].
- "The abstractions that are sent in flows are not letters." — R0546 f5a6e9 flow undated — stage meta L135-148: Deliver carries Letter { MessageId Sender Content } [I].
- "a programmatically provided origin of where the Flow is requested from" — R0103 9993b5 flowOriginClue 2026-09-17 — design L281-284: Launch carries no origin (stage has OriginClue, signal L213-214) [W].
- "if the flow ID matches the flow's provenance, then we can restart it" — R0104 9993b5 flowRestart 2026-09-17 — design L288, L604-606: Restart removed, no caller-authority rule [W].
- "Starting a new session should be done with the Flow Nexus using the Flow CLI." (R0157 b81560 operational-flowCLIStartsSessions 2026-09-19); "where MetaFlow is the ancestor of the next" (R0446 f5a6e9 flow 2026-10-07); "eventually flow spawning is going to get automated" (R0415 8475a9 flow 2026-10-06); "that flow should not be woken up" (R0666 f5a6e9 messaging 2026-10-08) — stage signal L104-121, L278-280: Start, Restart, Replace, no Launch, Wake, Refresh, ContextMeasured [W].
- "We just then have the vector of structs that have the context type" — R0353 edf227 contextModules 2026-10-03 — design L281-284, L818-825: one Vector<Key>, placement in prose [I].
- "Curriculum provides all of the skill files for that workspace." — R0111 9993b5 workspaceProvisioning 2026-09-17 — design L568-579: Flow's own module registry [I]. cat: possibly superseded.
- "a command that is more convenient and more biased, like ensure or start" — R0158 b81560 operational-flowDatomCLIAndSignalLibrary 2026-09-19 — design L344-346 [I], "weak conflict" (cat).
- "I very much dislike options. I think that they're really a last resort" — R0543 f5a6e9 flow undated — stage signal L111, L189, L207-209, L261, flow-ethos L133, L155: Option throughout [W].
- "It can get its origin without the user having to say, "Hey I'm Psyche Fable."" — R1233 b7ba00 callerIdentity 2026-09-26 — stage signal L73-76, L111, L255-257: ResolveCaller with an optional FlowId claim [I].
- "I don't want any more features." — R0202 88475f flow, R0223 e51411 authority, R0189 752e0f flowDeploy, 2026-09-24 — design L843-859: the to-build list [I]. cat: possibly superseded.
### Locks and delivery
- "message wouldn't need to make this a two-part thing" — R0597 1b8ac0 messaging 2026-09-21 — design L587-594, L689-696: Lock then Deliver [I].
- "Message takes a datom + recipient flow-id, asks Flow for the recipient's herdr position, and delivers through Herdr's primitives." (agent-written) — R0090 108ab0 2026-09-17 — design L689-696, stage meta L3-6: Flow the only pane writer [W]. cat: possibly superseded.
- "the messenger caches both sides" — R0592 b81560 operational-refreshFlowAndMessageFlowCoordination 2026-09-19 — design L697-699: Locked refusal, nothing held [I]; stage signal L14-21, L108: Replace with no lock [I].
- "the message can sort of be held" — R0603 d8df70 messaging 2026-09-23 — design L697-699 [I].
- "then the message is just relayed to the new flow" — R0532 e1953c flowLifecycle undated — design L697-699 [I]. cat: possibly superseded by R0546.
- "You're all allowed to bypass failing messages and send each other straight into your panes." — R0613 e51411 messaging 2026-09-24 — stage meta L3-6 [I]. cat: superseded by R0622.
- "every refreshed/new session must START IN HERDR, with exact live pane binding before HM messaging is trusted" — R0173 f38926 refresh 2026-09-20 — design L428-431, L752-771: Bind trusts any running process [I].
### Refresh, reap, handover
- "there's no handoff file; the flow *reads its previous flow(s)*" — R0014 5c8be3ca flowArtifacts 2026-08-21 — design L682-687: handover as the brief [I]. cat: possibly superseded by R0075, R0089, R0114.
- "at 60%, the flow basically has to change over" (R0061 6cc91b flowLifecycle 2026-09-14); "start when you're getting to 30% of your context as a Fable agent" and "the subflow will put together the refresh" (R0089 f55ec8 flowRefresh 2026-09-16); "above 30% ... above 39" (R0137 af762b 2026-09-18); "above 30%, like 200,000 to 300,000 tokens" (R0171 b80e55 2026-09-20) — design L231-235, L671-687: per-layer 20 and 40, no subflow step [W for R0061, I for the rest].
- "flowcharts * visuals * concepts" — R0075 48cff7 refreshPurpose 2026-09-16 — design L686-687: one small paragraph [I].
- "don't limit yourself from restarting yourself" — R0113 f55ec8 flowRefresh 2026-09-17 — design L679-681: no model decides a step [I].
- "you always absorb everything below you when you refresh" — R0114 f55ec8 flowRefresh 2026-09-17 — design L682-687 [I].
- "programmatically injected, not output by an agent" — R0117 1ac573 operational-refreshKeyProgrammaticallyInjected 2026-09-18 — design L680-688: the flow writes its handover [I].
- "the outgoing Field is crossover-only until both are ready" (heading) — R0119 33ba2b operational-fieldRefreshSuccession 2026-09-18 — design L683-684: predecessor reaped in the sequence [I].
- "you inform it of all your... useful... knowledge" — R0134 8393ca operational-herdrVoiceAccess 2026-09-18 — design L686-688: only the undecided [I].
- "It'll be like an addendum that the next one starts with" — R0176 1b8ac0 refresh 2026-09-21 — design L687-688: no merge or push step [I].
- "it needs to have a flow handover in its transcript somewhere" — R0209 d8df70 flowLifecycle 2026-09-24 (R0197 836818 flowNexus) — design L675-684: refresh at 40% without one [I].
- "refreshed with all of its important presentations or illustrations and the raw psyche" — R0257 e51411 refresh 2026-09-25 — design L685-688 [I]. cat: possibly superseded by R0376.
- "sessions can be reloaded in the new harness one at a time as they go idle" — R0302 7328f4 hooks 2026-09-30 — design L604-607: Restart removed [I].
- "The bottom of each aspect is what is going to run the flow refresh mechanism for now." — R0426 02dda6 flow-refresh 2026-10-07 — design L671-687 [I]. cat: interim, possibly superseded by R0432.
- "which could be checked by a small model making sure that the flow is working properly" — R0549 fd0f97 flowLifecycle undated — design L680-687: no model step, no failed-spawn path [I].
- "we put hooks to give us event updates with some data" — R0160 b81560 operational-hooksAsEventSource 2026-09-19 — stage signal L278-280: Event lacks ContextMeasured [W]; same for R0279 b860be refreshAutomation 2026-09-26 ("When a model reaches a certain context window") and R0412 8475a9 flow 2026-10-06 ("we don't have a way to monitor that yet") [W].
### Modules and sources
- "using the containing source with hash" — R0797 73ada7 nexus 2026-10-09 — design L577 "the blake3 of that file" against L43-46 [I].
- "we're going to hash the whole thing" — R0999 d68c82 source undated — design L575-578 [W].
- "just make the nexus for all the sources and reuse it for all components" — R0988 081064 ethos 2026-10-10 — design L43-46, L205-217, L554-579; stage flow L16-20, meta L91-96 [W].
- "We can create a shared library between them, which is about sources" — R0984 081064 ethos 2026-10-10 — design L43-46, L205-217 [I].
- "curriculum can have the capacity to get/check the hash ... according to the operation (write or read)" — R1239 f5a6e9 contextModules 2026-10-09 — stage flow-ethos L20, L66-71: Hash only stored [I].
### Subflows and request ids; Capsule
- No disagreement: every point is uncovered (part 2).
### Meta socket
- "a meta socket for debugging for adding already existing processes" — R0200 836818 flowNexus, R0213 d8df70 flowTool, 2026-09-24 — design L428-431, L752-771: Bind on the ordinary socket, one process at a time [I].
- "create the features that the message will probably need on the meta socket" — R0622 88475f message 2026-09-25 — design L941-946: Lock, Deliver on the ordinary socket [I].
- "we can just expose the meta socket to everybody" — R0595 1b8ac0 messaging 2026-09-21 — stage meta L28-30: MetaRefused [I]. cat: possibly superseded by R0597, R0622.
### Stage layout
- "maybe we can try three" — R0962 f5a6e9 ethos 2026-10-07 — all stage files indent two spaces [W].
- "I prefer vertical expansion rather than horizontal" — R0961 e5a0bc ethos 2026-10-07 — stage flow L23-35, signal L189-249 [W]; design L17-125 partly [I]; vision/ethos.md lines 478-480 [9519a1].
- "I would put `voice` on a new line, indented right" — R0953 d4ae97 ethos 2026-10-06 — stage signal L189, L202, L207 [W].
- "all of the Ethos code to get way more comments" — R0944 edf227 ethosComments 2026-10-03 — stage Request, Refusal, Event uncommented [W].
- "the new line indentation style, which should be favored" — R0955 db38f8 ethosAndBookComments 2026-10-06 — stage flow L32-35, L64-71 [I].
- "a single-field struct, which would be really bad design" — R1034 e4a40e archive-newtypeWrappingAndSingleFieldStructs 2026-09-03; "single-field structs are forbidden" R1117 — stage signal L259 `Presentation.{ Title }` [W].
- "I would want to make the inline declaration mandatory" — R1106 d4ae97 ethos 2026-10-06 — stage flow L14-20, L39-45, L49-60 [W]; design L47-50, L106-111 [I]; R1105 same date ("defined inline up until a decent level of recursion") against stage signal L153-259, meta L86-170 [I].
- "if there's another type called psyche with the same name, that's what data that variant carries" — R1098 7328f4 ethos 2026-09-30 — stage signal L268 `Address.Address Lock.Lock` [W].
- "this block is not ethos because it's lacking a type" — R1096 c64ee3 ethos 2026-09-29 (R0996 62022e8f archive-designPractice undated) — design L169-177, L586-594 bare fragments [W].
- "it's not going to be an integer. It's going to be like volume" — R1086 9993b5 typedString 2026-09-17 — design L93, L97-98, L123, L235, L248-250 bare Integer [I].
### Other: the Operation root
- "All nexuses have to have all three." (R0794 d4ae97 nexus 2026-10-07); "signal, operation, and memory" (R0937 91ea9f ethos 2026-10-02); "Signal can only talk to operation. Memory can only talk to operation." (R0827 aa887c undated, R0789 bad807 2026-10-04); "the signal has to go through the operation actor/system" (R0787 5ed94b nexusEntryPoint 2026-10-04, R0813 28d847 undated); "the signal - the process - the storage" (R0936 91ea9f 2026-10-02; R1236 same date); "the signal - the memory - the operation" (R0983 081064 2026-10-10, R0991 23824a 2026-10-10, R1242 d68c82 undated); "it belongs in operation ethos as the main operation" (R1109 d4ae97 2026-10-06; R1112 2026-10-07) — design L9-12 "One Library, two Signals, one Memory", no Operation [W]; stage has no Memory ethos [W]; vision/ethos.md lines 57-62 against design L11 [9519a1].
## 2. Subjects the catalogue says the design does not cover
- Flow id derivation, collision rule and a word-id codec or library (R0032-R0037, R0314, R0439, R0457, R0942, R1101, R1240).
- Who names a flow, archive or concluded markers in titles, "of"-ancestry naming (R0003, R0061, R0119, R0139; vision-flow lines 36-40).
- Launch working directory, permission flags, remote control, desktop visibility (R0004, R0106, R0230, R0533, R0479, R0553).
- A base-prompt module, typed module kinds, a subagent-excluded prompt part, placement by subaspect, non-loadable modules, flow-edited modules (R0008, R0054, R0073, R0342, R0434, R0534, R0943, R0931).
- Subflows: Flow-started subflows, subflow lanes and hooks, ending questions routed by authority, request ids and status (R0028, R0038, R0155, R0156, R0245; vision-flow lines 50-74).
- Role, specialty, voice-as-metaflow, metaflow clusters, non-pane ephemeral flows (R0242, R0358, R0390, R0374, R0435, R0436, R0445).
- Effort on Model, quota-aware model choice, a declared launch roster, checks on effort (R0080, R0111, R0193, R0263, R0266, R0267).
- Authority: who may Launch, Refresh, Stop; caller-process checks; layered spawn authentication (R0158, R0212, R0237, R0268, R0415, R0736, R1225, R1228).
- Reaping abandoned flows, archives of finished sessions, judged retirement, FinalResponse and EndOfTurn reports (R0115, R0143, R0144, R0148, R0153, R0163, R0166, R0177, R0241, R0269).
- Interrupting an unfinished turn, outstanding subagents at refresh, compaction fallback, failed-successor path, refresh floor (R0176, R0279, R0258, R0549, R0518).
- Hook-injected context, reply-boundary events, periodic skill reload (R0141, R0221, R0291, R0371).
- Undelivered-message escalation, noise rules for awake flows, orders marked as orders, outbox after lock (R0197, R0610, R0661, R0681, R0593).
- Psyche-has-just-spoken routing state; route records in Memory (R0470, R0447; vision-aspects line 8).
- One Herdr container, flow container type, theme-switch reattach (R0190, R0215, R0214, R0162).
- A Source Nexus with backends; who checks the hash; text-in-memory registry (R0800, R0801, R0987, R0978, R0443).
- Nexus-wide: configured-flag metadata tree, ordinary-socket first Configure, store upgrades, Kameo actors, caller identity as a Signal standard, simple/extended responses (R0713, R0781, R0866, R1233, R1237, R1241).
- Traits declared in ethos for Flow's behaviour (R1174, R1183, R1186); the Flow Ethos skill (R1189, R1191; vision/ethos.md line 8).
- Observation by subscription, a universal Observe root (vision-nexus line 138, R1017).
- Marked transcript blocks becoming actions, registered pollers (vision-flow line 48).
- The Capsule (vision-flow line 14); Persona (vision-persona; R0832); OpenCode (R0277); Clojure tools (R0294); a usage reset on the meta socket (R0690); a soft Codex app-server upgrade (R0557).
## 3. Chains where his records changed (oldest to newest)
- Refresh threshold: 2026-09-14 R0061 6cc91b: "At a certain maximum, at 60%, the flow basically has to change over" → 2026-09-16 R0081 b49251: "if the context is large, let's say thirty or forty percent [transcribed "3,740%"], it might just start the whole thing on a new flow" → 2026-09-16 R0089 f55ec8: "start when you're getting to 30% of your context as a Fable agent, right? That's 300,000 tokens." → 2026-09-18 R0137 af762b: "refresh yourself if you're above 30% context for sure. Again, if you're above 39" → 2026-09-20 R0171 b80e55: "especially if it's above 30%, like 200,000 to 300,000 tokens, which is different for Claude" → undated R0518 692df8: "Let's not restart a flow that only has less than 15% of its context used, at least, right, or maybe even 20"
- Id length: 2026-08-26 R0027 01a03d6e: "I think six characters of the part which is not repetitive" → 2026-08-31 R0033 01a05826: "I dont think we need more than 4 characters." → 2026-08-31 R0035 01a05826: "Then let's use 6 chart." → 2026-09-14 R0068 dc1c58 (notion): "I think the flow ID is too long right now" → undated R0530 e1953c: "We can use 6 characters easily to fit that in" → undated R0531 e1953c: "we shorten the session ID to the first 4 characters we were using before, instead of 6" → 2026-10-02 R0314 01e496: "I'd also like the Flow ID to be converted into words." → 2026-10-03 R1181 edf227: "The flow ID is not a string, it's a hash." → 2026-10-09 R0457 0c85a3 (notion): "the first 33 bits of the identifier we use for the harness and the word thing" → 2026-10-09 R1117 ebbe30: "Let's just leave it as a string for now"
- PowerLevel to layers: 2026-09-16 R0083 b49251: "There are going to be three levels of psyche flows: low, medium, and high effort." → 2026-09-17 R0111 9993b5: "It just asks for medium, and by default, medium means Claude." → 2026-09-26 R0264 b7ba00: "I don't see the primary, secondary, tertiary part. I see: - high, medium, low, ultra low" → 2026-09-27 R0288 5ac3a3: "It's not high, medium, and low now. It's primary, secondary, tertiary, and quaternary" → 2026-10-03 R0338 5578cc: "now the model is replaced by the layer" → 2026-10-09 R0467 445410: "explained in layers and not models, and then we should just have a layer-to-model skill"
- Role to voice and metaflow: 2026-09-25 R0242 88475f: "it takes another kind of variant for its specialty, like the monitor or the voice concept" → 2026-10-02 R0937 91ea9f: "Yes they're going to be called voices. That's the right term." → 2026-10-03 R0358 edf227: "one of its fields is a role. The role is an enum, and one of its variants is voice." → 2026-10-03 R0361 edf227: "Voice.{ Aspect.[ Psyche Mind Field ] Layer.[ Primary Secondary Tertiary Quaternary }" → 2026-10-04 R0373 bad807: "What we're calling a voice, really, is this: a Metaflow with no known ending." → 2026-10-05 R0385 8475a9: "the flow has a flow ID and a role, one of which is a voice." → 2026-10-05 R0390 8475a9: "The voice is a type of metaflow and then there are specialized metaflows." → 2026-10-07 R0433 d4ae97: "There's no voice, right? The variants are all of the different voice aspects directly." → 2026-10-08 R0454 d4ae97: "the non-topiced flows would just be the topic of core."
## Sources
- flows/9519a1/reports/flow-ethos-records.md (Primary working tree, 2026-10-11), sections 1 and 3, read by heading grep, the comparison lines 34-432, and per-record extraction. No provenance receipt handle was available.
