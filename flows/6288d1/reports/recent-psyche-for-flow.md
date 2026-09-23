# Recent Psyche for Flow

**Flow:** Mind Sol `6288d1`  
**Date:** 2026-09-23  
**Scope:** Recent Psyche relevant to Flow, prepared for Mind High `47764b` and Field `9ddcbc`.

This report separates direct living words, distilled Vision, machine-authored architecture and operational evidence, and this flow's synthesis. A design statement is not treated as deployed behavior, and an operational report is not treated as living authority.

## 1. Direct living words

The newest direct records carry the greatest weight.

### Model-named seats and behavioral power

Typed directly to Field Medium `9ddcbc` on 2026-09-23:

> Not soul
>
> And that's what I want them to be named by model when they're given a title and stuff. We know that mind, medium, is soul but we call it mind sol
>
> Make this how it works by default and annotate the right architecture documents or whatever. Operatively for you, the vision for this is that all the sessions are named after their aspect and their model, and the power equivalence is still in effect for behavior. Medium levels speak to each other, right? The same aspect goes up and down one rung at a time, depending on what is running at the time. If low is running and there's no medium, he can message high. Let's make this all operative. It should already be but maybe clarify it with me or send this to Field Astra to think about too.

The source preserves “soul” verbatim and interprets it from the immediate correction as the sound of “Sol.” The ruling distinguishes model display in the native name from behavioral power used for equivalence and routing.

### Flow first; Message plugs in after; Flow composes prompts

Typed directly to Psyche High `836818` on 2026-09-23:

> Can you get in touch with Mind Astra, or any kind of highest field that you can find, if you can't find one, to implement your best design of Flow (so we can spawn Flow and message into pains using the Flow CLI)? We'll plug message into that after we deploy Flow and we can use it to start a session.
>
> It has to have a way to compose the prompts: the first prompt and eventually a way to compose the system prompt but we can start with the prompt. What's the situation with injecting a bunch of skills in a single prompt in Claude?

The record keeps “pains” unchanged and notes the intended reading as Herdr panes. This directs the order of work: Flow establishes launch and identity; Message integrates afterward. It also sets an incremental prompt boundary: first-prompt composition now, system-prompt composition later.

### Nexus anatomy remains a living-led design topic

Typed directly to Psyche High `836818` over Remote Control on 2026-09-23:

> Ask me questions to design everything with the flow and the message. Let's get this new infrastructure up:
>
> - the persona
> - all of the nexuses
> - the main nexuses
> - how they fit with each other
> - how they interact with each other
>
> The message highly depends on flow and probably many things will then depend on message.

This does not settle which Nexuses are “main,” Persona's final boundary, or the edges among them. It expressly keeps those subjects in dialogue with the living.

### Supporting recent direct records

Direct to Field High `6fb948` on 2026-09-23, the living proposed Persona's first use as checking that services are running and described behavior as configuration-driven. That is a proposal for Persona's initial role, not evidence of a running Persona observer.

Typed directly to Psyche Medium `d8df70` on 2026-09-23, the living described one-call message sending when the desired match and pane still exist, and asked whether harness start/end hooks should register and unregister sessions. These are current design directions; the hook proposal is still a question.

Earlier direct records add continuity without outranking the newer words:

- On 2026-09-19: “Starting a new session should be done with the Flow Nexus using the Flow CLI.”
- On 2026-09-19, relayed with weaker provenance: the requester holds only a request ID for an independent subflow, using it for status and later messages.
- On 2026-09-19, relayed verbatim: “Whenever you refresh a flow, you need to reap the ancestor, right?” The meaning of “reap” across routing, stopping, and archival remains unresolved below.

## 2. Distilled Vision

### Flow Nexus

`Vision/flowNexus.md` describes Flow Nexus as the long-running component that prepares and starts a model flow, including working directory, system prompt, training files, and instruction prompt. The Flow repository holds runtime machinery; skills remain outside it so their changes do not require a Nix rebuild.

Its durable subflow shape is asynchronous: harness-native synchronous subagents are replaced by independent flows with their own system prompts. A requester holds only a request ID, not the subflow. That ID supports status, detail, and further messages while the subflow lives; completion returns to the requester if it is still in charge.

The document assigns removal of the replaced receiving endpoint to the refresh event itself. It does not, by itself, define whether that removal also means native-process stop, evidence archival, or deletion.

### Model roles, identity, and routing

`Vision/modelRoles.md` says one typed configuration declaration in Flow sets the exact model everywhere and is carried by named skill variables into skills, launchers, and briefs. It keeps these facts separate: aspect, exact native model identifier, model display, behavioral power, Flow ID, and native binding.

Native main-session display is `<Aspect> <Model> <FLOW_ID>`. Behavioral power—High, Medium, Low, or Ultra Low—governs peer equivalence, delegation ceilings, escalation, and routing; it is not substituted for model display. Horizontal routing selects the eligible cell at equivalent behavioral power. Vertical routing stays within an aspect and normally moves one rung; if the adjacent rung is absent, it may reach the next running rung while reporting the gap.

Resolution is per attempt. Busy remains eligible; missing or unavailable needs fresh lifecycle and route evidence; multiple bindings are a conflict rather than fanout. An ambiguous attempt stays attached to its recipient and is reconciled instead of being silently resent elsewhere.

These are authoritative design statements, not proof that the present Flow Nexus runtime implements them.

## 3. Machine-authored architecture and operational evidence

### Replacement and delivery contract

Mind Astra `4b0f60`'s `flow-nexus-main-replacement-contract.md` is explicitly an owner-scoped architecture and implementation packet. It grants no authority to edit source, reserve ownership, launch, restart, stop, archive, or change routes.

The packet distinguishes a stable logical destination from Flow ID, native UUID, harness binding generation, lifecycle generation, and request ID. Its proposed replacement operation uses admission, readiness, continuity acceptance, a binding commit, and then explicit ancestor retirement. Before binding commit, a failed successor remains held. After commit, delivery queues only to the exact new binding; retirement failure becomes blocked coexistence rather than automatic rollback.

Message remains a separate durable-attempt and receipt component. It consumes a versioned Flow binding event and rechecks committed binding generation before delivery. It does not become Flow meta control. Transport acceptance, target read, and completed work remain different receipt boundaries.

### Observed runtime boundary

Read-only observations on 2026-09-23 between 18:21:34Z and 18:22:12Z found a running Flow Nexus process, owned ordinary and meta sockets, and codec replies. Typed resolution of two named targets returned `UnknownFlow`. This witnesses a process, sockets, and codec behavior only; it does not witness target registration, liveness, availability, manager state, or installed/source parity.

The inspected source schema had Pending/Active lifecycle and ordinary Start only for one profile, without the typed aspect/main-peer occupancy, replacement, and retirement policies described above. No installed Metaflow binary was found. A historical Rust mutation error was corrected in one candidate source revision, but neither compilation nor a coherent accepted dependency graph was witnessed. The report states that no required process-observable replacement tests had run.

### Protected ownership boundary

The packet reports source and lock ownership distributed across existing Flow, Signal Flow, Message, Codex/Herdr adapter, and controller holders. Some routes were unavailable or unresolved, one source slice had dirty competing work, and the meta attester provider was absent. It expressly forbids inventing ownership, arbitrarily registering known mains, restarting protected services, or overwriting competing work.

Psyche High `836818`'s log later records a witnessed Herdr delivery to Mind High `47764b` and continuing absence of an HM registration for that seat. The log is operational testimony; it is not living authority and does not prove that the route remains current now.

## 4. Mind Sol synthesis

The strongest current direction is:

1. Flow is the launch, identity, and prompt-composition substrate. The Flow CLI is the intended interface for starting flows and placing them in Herdr panes.
2. Flow composes the first prompt now and later the base/system prompt. The exact skill-composition mechanism still needs a falsifiable native-harness contract.
3. Message integrates only after Flow is deployed because durable delivery needs Flow's exact logical identity and current binding. Message owns attempts and receipts, not Flow lifecycle control.
4. Independent subflows are asynchronous flows. The requester retains a request ID, not the subflow or its native handle.
5. Model/profile is declared once as typed Flow configuration. Model display belongs in the native title; behavioral power separately governs communication and delegation.
6. The desired replacement design needs exact identity, admission, independently witnessed readiness, continuity acceptance, atomic binding change, and separately evidenced retirement stages. Present observations do not establish that runtime.
7. Persona, the main Nexuses, the complete Nexus set, and their ordinary/meta edges remain living-led design work. Current proposals must not be mistaken for settled topology.

The most important implementation boundary is therefore not “build a second launcher.” It is to establish one coherent owner and accepted source graph for Flow, then prove the minimal native pipeline from typed profile and composed prompt through Herdr placement, accepted binding registration, and exact resolution. Message can then consume that identity boundary. This is synthesis, not authorization to implement it.

## 5. Open questions and tensions

1. **What are the main Nexuses?** Which components are vertices, which are repositories or libraries, and what ordinary and meta contracts join them? The living explicitly retained this question.
2. **What is Persona's boundary?** Is service-health supervision its first domain, and which observations or actions require its meta surface rather than ordinary edges?
3. **What exact Flow identity does Message address?** The desired separation among logical destination, Flow ID, native binding, lifecycle generation, and request ID is described, but the canonical public Message address and handoff semantics remain unsettled.
4. **What does “reap” mean at each stage?** The direct record favors reaping the ancestor on refresh; the newer safety contract separates receiver removal, binding commit, authorized native stop, and later archive. The living should rule which effects belong to refresh and which require separate judgment.
5. **When is a registration resolvable?** The supplied material leaves open whether Registered resolves before Confirmed while admission is held, and when a `SuccessorOf` relationship begins forwarding.
6. **How are prompts composed?** The first prompt is the immediate target and the base/system prompt is later. The source of ordering, de-duplication, provenance, skill expansion receipts, and model-specific limits remains to be designed and tested.
7. **Which source graph and owner are canonical now?** Installed/source parity is unknown, protected work is distributed, and several candidate revisions remain separate. No ownership transfer follows from this report.
8. **How is the title rule projected into operational skills?** The newest direct words and `Vision/modelRoles.md` use `<Aspect> <Model> <FLOW_ID>`, while some currently loaded operational title instructions still specify `<Aspect> <Power> <FLOW_ID>`. The current launcher read back `Mind Sol 6288d1`, consistent with the newer direct direction. The authored operational sources need an owner-approved reconciliation; this report does not edit them.

## Sources

### Direct living-authored records

- `flows/9ddcbc/vision/modelNamedSeatsAndAdaptiveRouting.md` — typed directly to Field Medium `9ddcbc`, 2026-09-23.
- `flows/836818/vision/flowNexus.md` — typed directly to Psyche High `836818`, 2026-09-23.
- `flows/836818/vision/nexusAnatomy.md` — typed directly to Psyche High `836818` over Remote Control, 2026-09-23.
- `flows/6fb948/vision/personaServiceAndNexusImagery-20260923.md` — direct to Field High `6fb948`, 2026-09-23.
- `flows/d8df70/vision/messaging.md` — typed directly to Psyche Medium `d8df70`, 2026-09-23.
- `flows/b81560/vision/operational-mindMediumIsSol.md` — spoken directly to Psyche Opus `b81560`, 2026-09-20; source interprets “Soul” as Sol.
- `flows/b81560/vision/operational-flowCLIStartsSessions.md` — direct living words, 2026-09-19.
- `flows/b81560/vision/archive-operational-subflowRequestIdAndAsync.md` — living words relayed from Psyche Fable `f38926`; input mode not established, 2026-09-19.
- `flows/b81560/vision/operational-reapingOnRefreshAndFlowEndHook.md` — relayed verbatim living words, 2026-09-19.

### Distilled Vision

- `Vision/flowNexus.md` — Flow Nexus, asynchronous subflows, request IDs, and refresh-owned receiver removal.
- `Vision/modelRoles.md` — typed model declaration, model-named seats, behavioral power, and routing.

### Machine-authored evidence and mission provenance

- `flows/9ddcbc/mind-sol-flow-psyche-20260923/mission.md` — mission contract and provenance packet, 2026-09-23.
- `flows/4b0f60/reports/flow-nexus-main-replacement-contract.md` — owner-scoped architecture plus bounded runtime/source observations, 2026-09-23.
- `flows/836818/log.md` — Psyche High operational log and delivery claims, 2026-09-22 through 2026-09-23.
- Read-only judgment companion for Flow `6288d1` — inspected the listed sources and searched newest applicable `Vision/`, `vision-raw/`, and `flows/*/vision/` records on 2026-09-23; found no newer applicable `vision-raw/` record than the September 19–23 flow records.
