# Flow and messaging: the target shape, and where the code stands

Spec: psyche-context origin/main 2d9fbb6, vision/flow.md, nexus.md, messaging.md, model-roles.md, aspects.md, criomos.md, subflows.md. Code: Flow 0.37.1 as deployed on ouranos (flow main fc53f4f: the converged 0.37.0 2ca790c, which carries 379e7a-send e8f84ad, plus the Codex rollout fix 7f5ed64), signal-flow 24.0.0 (8796628), meta-signal-flow 31.0.0 (a5ba4ab, on 30.0.0 4dcbfa8), Message 0.20.x, CriomOS-home main 9829b366, CriomOS 379e7a-codex037 2c48bc2. "Witnessed" means read in the code at those revisions, or a test run on the remote builder. Anything else is marked as this flow's inference.

## Target shape

One Nexus, Flow (`flow-nexus`), owns every flow: who it is, its start, where it can be reached, and how a message reaches it.

```
  calling process (a flow's shell)
        |
        | runs `flow '<one datom>'`
        v
  flow CLI ---- signal frame ----> flow-nexus
                                    |  reads the caller from the socket peer
                                    |  (Herdr pane, or Codex thread)
                                    v
                              metaflow { Aspect topic Layer }
                               |                 |
                     Launch: composes        Send: checks route,
                     declared modules        queues or types it
                               |                 |
                               v                 v
                         Herdr pane <---- Flow's lease (only pane writer)
```

- Identity: a flow is named by its metaflow address; its flow id is the claim of its native session (six characters). Nobody passes an id: Flow reads the calling process.
- Start: `Launch.{ Address Brief }`. The metaflow's modules come from Flow's configuration, which the Home deployment declares and the Nexus loads.
- Routing: Flow refuses a request that leaves the routes vision-aspects allows.
- Delivery: Flow queues, wakes, and types into panes. Priority is the head on the request.
- Message: by vision/flow.md:33 Message is the component that asks Flow to send and subscribes to Flow's events. By flow.md:40, for now Flow is used raw, "until Message sends through Flow's socket". In 0.37.0, flows send through Flow. Message stays deployed and still takes its old Lock/Deliver path, but no flow's skill points to it.

## Vision lines, mapped

flow.md:8. "The Flow Nexus sets up and starts a model flow: its working directory, system prompt, training files and instruction prompt." Implemented: Start/Replace composition (composition.rs, context.rs through Curriculum), launch (herdr/launch.rs). The working directory is the configured SourceRoot.

flow.md:11. "A flow the living asks for is launched, properly and surely. Flow holds the lock on flows." Implemented: Start; the AddressAwake refusal (store/metaflow.rs address_taking); Flow is the only pane writer (delivery/lease.rs).

flow.md:19. "what is addressed is always the metaflow, never a flow." Send and Launch address metaflows. Gap: Stop.FlowId, Restart.FlowId and ResolveRecipient.FlowId still take a flow id.

flow.md:21, 29, 70. "A topic's name is a camelCase identifier, uncapitalized." Gap: Topic is a String and is not checked (flow-ethos library.ethos: "check camelCase at input"). The Home generator lower-cases topics, so `PrimaryCommitting` becomes `primarycommitting`.

flow.md:25, 27, 33. A topic goes idle and never dies; a metaflow sleeps; requests are of a closed set of kinds, each with its waking effect. Implemented: Request.[ Order Question Psyche Psyches Result Notice ] (flow-ethos); wakes_for (waking.rs); queue, wake and drain (waking.rs, store/metaflow.rs). Since 0.36.0 a wake of a metaflow declared in configuration composes its declaration (waking.rs wake_plan).

flow.md:29. "A flow's id is the hash of the harness's session id, kept to six characters... No flow declares its id: every call to Flow is identified by the calling process." Implemented: launch claims (herdr/reservation.rs, `flow-id`). New in 0.37.0: BindSeat claims the id of a seat Flow did not start through the same `flow-id` claim, so no `flow-…` id is minted for it (sending.rs). Send, Launch and BindSeat read the caller from the socket peer (sending.rs IdentifiesSender, caller.rs). Gaps:
- Ordinary Bind (Message's) still mints `flow-{:016x}` ids (store/metaflow.rs bind_metaflow) when a process outside a Flow-launched pane binds.
- reserve_start (store.rs) still mints them for the legacy test start.
- The Claude hook reports with `FLOW_ID` from its environment (flow/src/hook.rs). That is a declared id.

flow.md:33. "Message asks Flow to send a request to a metaflow; Flow owns the lock and the delivery, answers sent or queued, and Message subscribes to Flow's events." Partial: Message's Send goes through Flow's Lock/Deliver/Release (signal-flow ordinary). Flow answers Queued, and since 0.37.0 Delivered for an abrupt send. Gap: Flow publishes no event stream to subscribe to; only Observe.Agent and Observe.Launch exist.

flow.md:33. "A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules." Implemented for a metaflow Flow holds: an Order, Question or the living's words wakes it (waking.rs). Gap: a Send to an address Flow holds no metaflow for is refused Unknown; it does not create one. With declarations it could, but the vision does not say who decides. That is question 4.

flow.md:40. "Flow exposes everything from the harness, the bare input: a flow is started, stopped and sent a message through Flow." New in 0.37.0: `flow 'Send.{ Address.{ Mind core Secondary } Soft.Order.«...» }'`, `flow 'Launch.{ { Mind core Secondary } «brief» }'`, `flow 'Stop.<id>'`.

flow.md:42. "A flow does not wait on a timer for another flow's work." Not enforced in code; flows follow it as conduct.

flow.md:44. Presentation. In progress on the 379e7a-vision branch (P5).

flow.md:48, 52, 54. "A launch names the metaflow, the context modules composed into its prompts, and a brief... the layer decides the model, declared once in Flow." New in 0.37.0: meta `Configure.Metaflows.[ { Address SystemModules UserModules } ]` and ordinary Launch. The model comes from Configure.Models. Effort is medium, low for an OpenAI Quaternary (sending.rs ChoosesEffort, model-roles.md:17). Leave-outs come from Configure.LeaveOuts. The one-call start (:54) is in progress on 379e7a-vision (P2).

flow.md:56, 62. The simplified flow and the Primary as a judge. Not implemented; both are long term.

flow.md:58. "A flow is specified whole, in Datom, by a domain-specific language in Ethos." Gap: the specification is EDN under Primary config/main-flow, turned into Configure datoms by Babashka in CriomOS-home. Flow has no flow ethos.

flow.md:60. "Short term, a Primary is not started without its Secondary." Implemented: StartRejection.NoSecondary (store/metaflow.rs secondary_refusal).

flow.md:64, 66, 76. Module registry, system-prompt anatomy, hash checks. Partial: Curriculum composes by module identity (context.rs). The anatomy and the hash checks are not implemented; the hash checks are long term.

flow.md:72. "Flow refuses a request that leaves those routes." New in 0.37.0: Refusal.OffRoute on Send (sending.rs RoutesBetweenAspects). Within an aspect every route is open. Across aspects only the same topic at the same layer is open, and Field reaches Psyche only after Psyche has sent to it. Inference: that permission is held in memory while the Nexus runs. Gap: Message's Lock path is not route-checked.

flow.md:86, 92. Reaping in the refresh event; refresh by model threshold. Refresh-at-rest: 0.36.0, approval branch. The threshold per model: in progress (379e7a-vision P4).

flow.md:90. "Every harness event reaches Flow through the harness's hooks calling the Flow CLI... Polling is forbidden." Implemented for Claude (flow-hook). Codex events come through the app-server subscription (codex_turns.rs).

flow.md:94, 96. Compaction refused below threshold: implemented (meta CommandRejection.CompactionRefused). Warning and investigation: in progress (379e7a-vision P6).

nexus.md:44, 52, 60. Two sockets; one CLI per socket; "one inline datom, no flags... identifies the process that called it". Implemented: `flow` and `flow-meta` (crates/flow, crates/flow-meta), and the peer is read by SO_PEERCRED (caller.rs IdentifiesPeer).

nexus.md:93. "A Nexus starts with no arguments." Gap: flow-nexus takes a Start datom of sockets, store and landing watch, and `--configure-only` (CriomOS-home initialize-declared-flow).

nexus.md:70, 146, 151. Typed Memory; subscription; no polling. Partial: Flow polls Herdr pane state in bounded waits (settle_rested). Inference from the code; the polls are not registered as the vision asks.

messaging.md:8. "The message body is a datom that lands in the recipient's prompt as a datom-formatted object. There is no envelope around it." Queued work arrives as `{ Sender.{ Aspect topic Layer } Order.«...» }` (composition.rs RendersQueuedWork). Gap: an abrupt send is typed through meta Deliver's Letter, `HardAbrupt.{ id Flow.<id> Text.«{ Sender... }» }`, which is an envelope.

messaging.md:13. "Priority.[HardAbrupt MiddleAbrupt Soft]". New in 0.37.0: Send's request carries the head, `Soft.Order.«...»`. Soft and every send to a flow that is not live are queued. Hard and Middle to a live flow go through Flow's Deliver.

messaging.md:17-23. Per-harness delivery tiers. Implemented in meta Deliver: HarnessProfile InterruptKeys `[ esc esc ]` and `[ enter ]` for Claude, `[ esc ]` for Codex (CriomOS-home initializer; delivery.rs).

messaging.md:27. "An interrupt witness is not a delivery witness." Implemented: InterruptWitness and DeliveryGrade are separate in meta Delivery. The ordinary Send answers only Delivered or Queued and does not claim consumption.

messaging.md:33, 37. Only messages that act; six-character ids. These are conduct; the code does not enforce them.

model-roles.md:39. "The model is declared once, as typed configuration in Flow, mutated only through the meta wire." Implemented: Configure.Models; Start refuses another model (ModelRefused).

model-roles.md:46. Native titles `{ Aspect topic Layer id }`. Implemented (title.rs). BindSeat does not retitle a seat it binds.

model-roles.md:58-64. "Horizontal routing selects the unique eligible cell... Busy is still eligible... Resolve the binding immediately before each attempt." Implemented: one metaflow per address; an abrupt send resolves the live flow at send time (sending.rs live_awake_flow).

aspects.md:8. Same-topic, same-layer horizontal routes; Field reaches Psyche through Mind. Implemented as Send's route check (see flow.md:72).

criomos.md:8, 17. Declarative only; store paths come from evaluation. The Flow, Message and Curriculum units and commands come from CriomOS-home (origin/main eee938fe). Metaflow declarations are added to the declared initializer (packages/flow-deployment/metaflows.clj, on the vision Home branch). Gap: config/main-flow, which is psyche-adjacent configuration, is read from the pinned Primary source and is not typed in ethos.

subflows.md:7. Actual flows replace the subagent tool. Long term; not started.

## Replaced prototypes

- hm-send, hm-send-abrupt → `flow 'Send.{ Address.{ … } <Priority>.<Kind>.… }'`. Priority is Soft, MiddleAbrupt or HardAbrupt. The kind is Order, Question, Result, Notice, Psyche.{ «context» «verbatim» } or Psyches.[ … ].
- hm-register → `flow 'BindSeat.{ Aspect topic Layer }'`, run inside the seat.
- hm-list → `flow 'Metaflows'`, `flow 'Current.{ … }'`.
- hm-retire → owner's `flow-meta 'Retire.<id>'`. A refresh reaps its predecessor in the same event.
- hm-repair, hm-rebind, hm-move, hm-deregister, hm-heartbeat-state → no replacement. Flow's records and Herdr's binding are one store, so there is no second route table to repair.
- flow-start (Primary tools/flow-start.mjs, packaged by CriomOS-home) → `flow 'Launch.{ { Aspect topic Layer } «brief» }'`. A flow launching its own address is replaced.

## Unknowns and questions for the living

1. Message's place now. vision/flow.md:40 says Flow is used raw "until Message sends through Flow's socket", and Message already reaches Flow's socket through Lock/Deliver. Is Message to come back as the send path, carrying Flow's event subscription, or does Flow stay the send path until Message is redesigned?
2. "Unless Psyche has just spoken to Field" (aspects.md:8). How long does "just" last? 0.37.0 grants the answer from the moment Psyche sends until the Nexus restarts. That is this flow's inference.
3. Psyche core Secondary as the hub. Today it reaches Mind and Field topic Secondaries directly, such as Mind flow Secondary. aspects.md allows that only within the same topic, so 0.37.0 refuses it OffRoute, and the hub goes through Mind core Secondary. Is that the intended consequence?
4. A request for a metaflow Flow has never held. Should Send create and start a declared metaflow (flow.md:33, "started whether or not it is running"), or refuse it Unknown as now?
5. The per-metaflow text in config/main-flow (topic-context, raw-psyche-paths, first-prompt-template) is not a context module. Where does it belong now that Launch composes only modules and a brief?
6. Topic names. config/main-flow mixes `Core`, `book` and `PrimaryCommitting`; the deployment lower-cases them all. vision/flow.md:29 says camelCase, uncapitalized. Should `primaryCommitting` replace `primarycommitting`?
7. Can a flow relay the living's words (Psyche, Psyches) through Send? flow.md:33 lists them among the kinds and restricts no sender; the send-tool contract (Mind's) forbids flows from sending them. 0.37.0 allows it on Send.
