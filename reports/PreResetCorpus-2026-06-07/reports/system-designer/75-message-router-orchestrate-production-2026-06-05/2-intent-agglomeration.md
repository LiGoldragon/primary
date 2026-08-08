---
title: 75.2 — Intent agglomeration — the binding intent governing message / router / orchestrate production on the triad base
role: system-designer
variant: Psyche
date: 2026-06-05
topics: [triad, runner, runtime, schema, nexus, sema, signal, engine, message, router, orchestrate, supervision, persona, delivery, meta-signal, bootstrap, introspect, mazv, authority, correlation, typed-feedback]
description: |
  Deep Spirit sweep across every topic governing the message / router / orchestrate
  ports onto the schema/triad-engine base. The binding intent grouped into four blocks
  (the triad-engine mechanism, the per-component intent, supervision + the running
  orchestrated system, the contract/authority shape), then the genuinely-open forks vs
  settled questions, then the superseded/duplicated records to ignore. Citations are
  description-first; short codes are secondary because they were re-minted recently.
---

# 75.2 — Intent agglomeration: what binds the three ports

Kind: psyche (intent synthesis). Date: 2026-06-05. READ-ONLY sweep.

Method note. Every claim below is a Spirit `Observe` result, cross-checked against
source where a source fact is asserted. Short codes were re-minted during a recent
hash migration (report 73 §3), so each record is cited **description-first**; the code
is a secondary handle. Two topic words that one might expect — `message`, `delivery`,
`channel`, `supervision`, `supervisor`, `manager` — return ZERO records as exact topic
tags; the relevant intent is tagged under `persona`, `messaging`, `runtime`,
`component-shape`, and `correlation` instead. That is itself a finding: the
message/router delivery intent is filed under `persona`, not under a delivery topic.

## A. The triad-engine mechanism (the base every port copies)

This is the spine. It is settled, High-to-VeryHigh certainty, and none of it is
superseded.

### A.1 The runner is extracted now; authors write three engines + two surfaces

`(Spirit Decision 7ca4)` [Extract the generic triad runtime runner now: every
schema-derived daemon plugs component logic into shared Signal, Nexus, and SEMA runner
objects instead of hand-writing repetitive daemon boilerplate.] This is the lever the
whole port turns on — the three target daemons are hand-written Kameo boilerplate
exactly of the kind 7ca4 says to stop writing.

`(Spirit Decision rpr5)` [The bundled triad runner adapter is GENERATED GLUE ONLY.
Component authors implement the three plane engines PLUS the effect handler and the
budget-exhausted reply; the generator bundles those surfaces for the shared runner
instead of making authors hand-write a fourth engine surface.] So a port author writes
exactly five things: SignalEngine, NexusEngine, SemaEngine, the effect handler, and the
budget-exhausted reply. Everything else is generated.

`(Spirit Decision hyng)` [Schema source carries the triad engine mechanism as the
baseline so schema authors get the runner shape, trace plumbing, and continuation
substrate through generation; per-component variation uses explicit escape hatches for
real domain differences, not hand-implemented daemon preference.] The corollary for our
three: any per-component cleverness in their current hand-written daemons that is NOT a
real domain difference must dissolve into the generated runner, not survive as an escape
hatch.

`(Spirit Decision czw0)` [Generated Signal, Nexus, and SEMA engine traits carry MINIMAL
lifecycle hooks: `on_start` and `on_stop` with typed start/stop failure results. Full
actor mailbox, backpressure, and runtime-control traits stay deferred; lifecycle hooks
are the minimum addressable surface persona supervision can use.] This is the join
between the mechanism (A) and supervision (C): the only lifecycle surface a port must
expose is on_start/on_stop, and that is exactly what persona supervises.

`(Spirit Decision njqm)` ratifies the engine-mechanism pattern in designer report 482 as
the direction. `(Spirit Decision 59dr)` defers backpressure and deeper runtime-control
as future work — NOT part of the production slice. `(Spirit Decision opvx)` keeps runner
concurrency mode out of the contract: it is a runtime/deployment choice; schema may
declare semantic constraints (ordering, idempotence, single-writer) only when real.

### A.2 The three planes — strict ownership, strict separation

`(Spirit Principle t2iy)` [A daemon has three execution centers: Signal handles
communication and wire messaging, Nexus handles execution and in-flight mail, SEMA
handles durable state messages and replies.] `(Spirit Constraint 3d5z, VeryHigh)` makes
the separation absolute: [SEMA owns ALL database/durable-state code, Nexus owns ALL
decision-making, Signal owns ALL communication; a daemon contains NO database
boilerplate, NO decision-making, and NO communication code outside its respective
engine.] This is the single hardest constraint for the three ports, because all three
current daemons mix these concerns in hand-written Kameo actors.

`(Spirit Decision h3u7)` is the schema-layer statement: [THREE schema types map to the
three planes — Signal (wire), Nexus (execution IO, formerly "Executor"), SEMA (durable
state); each declares its own input/output enums; the ROOT TYPE of a schema is the
message surface; file extensions `.signal.schema` / `.nexus.schema` / `.sema.schema` or
the first-record-is-the-variant form.] `(Spirit Principle tgch)` is the interface-first
flow: [schema-defined roots generate the Signal/Nexus/SEMA message types and traits;
hand-written runtime stays terse — match decisions, invoke algorithms, route replies,
never bypass the schema-defined trait boundaries; flow is Signal-in → Nexus-in →
SEMA-in (when state needed) → SEMA-out → Nexus-out → Signal-out → client.]

The per-plane ROLE split (load-bearing for deciding what goes where in each port):
- `(Spirit Decision u7fj)` [Signal engine role is message triage ONLY — admission,
  dispatch, identity-stamping, validation, wire-frame handling. No heavy logic.]
- `(Spirit Decision mvfe)` [Nexus is where the heavy logic lives — algorithms, deeper
  decision-making, DB queries, bidirectional Signal↔SEMA translation. Most computation.]
- `(Spirit Decision e440)` [SEMA implements durable state as a SINGLE-WRITER actor;
  reads run in parallel (redb MVCC); the single-writer invariant applies to writes only.]
- `(Spirit Clarification str0)` [Each engine trait's method count matches the count of
  distinct wire events that plane handles — SignalEngine TWO methods (triage on input,
  reply on output), NexusEngine ONE (execute), SemaEngine TWO (apply for writes, observe
  for parallel reads).] This gives each port a concrete method count to emit.

### A.3 Nexus = the visible internal feature catalog (the newest, highest-certainty)

`(Spirit Principle z6qu, VeryHigh, 2026-06-05)` [The Nexus interface — verbs and objects
in the nexus schema — IS the engine's INTERNAL FEATURE INTERFACE; its MAIN reason to
exist is VISIBILITY. EVERY engine feature (any computation, any filtering/condition on
results, any conditional write, any internal logic-feature) MUST be a declared Nexus
verb+object in the schema. Internal features must NOT live as inline hand-written logic
hidden from the schema. The nexus schema is the readable catalog of everything the
engine can do internally.] This is the most consequential record for the three ports:
every piece of router's adjudication logic, orchestrate's claim/role/divergence logic,
and message's stamping/validation logic must surface as a NAMED Nexus verb+object — not
survive as the inline match arms they are today.

Supporting Nexus shape:
- `(Spirit Correction xq4z)` [Nexus input ≠ Nexus output as symmetric lists; input is
  facts/replies/events to decide from, output is what Nexus commands/emits next.]
- `(Spirit Clarification 9ypt)` [Nexus sits between two worlds — Signal is the OUTER
  world (clients), SEMA is the INNER world (durable state); Nexus is the center making
  decisions.]
- `(Spirit Decision 3c7h)` [Nexus is the runtime mail keeper: a message Nexus holds is
  in processing state between Signal ingress and SEMA state handling.]
- `(Spirit Decision iq57)` + `(Spirit Clarification 4vi4)` — Nexus as recursive
  computation continuation (future runtime-control substrate); flagged as exploration,
  not a production requirement for these ports.
- `(Spirit Clarification k4d9, Medium)` [Internal Nexus nouns should not be promoted to
  the crate root or public contract; they belong in the plane schema/module.]

### A.4 Terseness criterion — the leak detector

`(Spirit Principle vpi8)` [Rust implementation code should be TERSE: match decisions,
import the algorithms, route the response back (signal-in nexus-out sema-in sema-out).
When hand-written Rust accumulates behavior beyond match+algorithm+forward, that signals
architecture leakage out of schema.] This is the acceptance test for a finished port:
if the ported daemon still carries thick hand-written logic, the schema is incomplete.

### A.5 The schema is NOTA; SEMA is the storage word; trace is typed

`(Spirit Decision 0fdy)` [Component databases use a `.sema` file extension instead of
`.redb`.] Relevant to router (`router.redb` today) and orchestrate (sema store today).
`(Spirit Principle 819r)` / `(Spirit Principle qyny)` [internal SEMA/DB work is itself a
schema language of messages; a component may keep storage inside the daemon first and
split it into its own daemon later using the same message language] — so the SEMA plane
is in-daemon, not a separate crate now. `(Spirit Clarification en7k, Medium)` [splitting
SEMA out of the daemon is a DISTANT future consideration, not the current per-plane-crate
design — do not emphasize it in a way that confuses agents.]

Trace (witness substrate the ports use to prove the planes are wired): `(Spirit
Clarification tpcm)` [Signal admission/reply, Nexus execution/decision, SEMA write/read
can each emit trace events so tests assert the intended interface was actually used].
`(Spirit Decision xqkv)` [optional testing/instrumentation build surface emitting trace
to a logging socket — the trace exists to PROVE actual use of the interfaces, not merely
that symbols exist]. `(Spirit Constraint 6u98, Maximum)` [daemon-side trace must NOT
print through println/eprintln]. `(Spirit Decision pj6w)` [the generic CLI trace-siting
path lives as a triad-runtime helper, not one-off schema-rust-next glue]. These give the
witness-test discipline for each port map.

## B. Per-component intent — message, router, orchestrate

### B.1 message — the stateless boundary; delivery is NOT its fact

The message intent is filed under `persona`. The defining records:

`(Spirit Decision l3k4)` [Router declares message-delivered as a durable fact upon
receiving acknowledgement from the harness channel (one per agent). MESSAGE creates a
LOG EVENT for the existence of the message; but DELIVERY is established only when the
ROUTER gets the harness-side acknowledgement; the router is the authoritative source for
delivery facts.] `(Spirit Principle 17ss)` [Router-acknowledgement = delivery durable on
harness-side ack.] Together these draw the message/router split sharply: message is a
log-the-existence boundary; router owns delivery truth.

Source confirms the shape (message/INTENT.md): message owns the `message` CLI + a
`message-daemon` that is a STATELESS boundary — "Neither carries a durable message
ledger. Both are stateless boundary surfaces. Routing policy, delivery state, and channel
authority remain in router." The daemon stamps `MessageSubmission` with owner identity,
SO_PEERCRED origin, ingress timestamp, then forwards `StampedMessageSubmission` to
router's internal socket. Provenance is typed, never inferred from uid or payload.

The consequence for the port (carried to map 4, flagged OPEN in §D): if message holds
NO durable state, its SEMA plane may be empty or near-empty — a candidate for the
stateless carve-out. That is a genuine open design question, not a settled fact.

`(Spirit Decision w4jp)` and `(Spirit Decision gdbf)` add the agent-abstraction
direction: [agent is a new component abstraction; persona-claude/-codex/-gemini/-pi/
-open-code are BACKENDS for agent; router talks to AGENT (not harness directly); harness
is abstracted behind agent — a cleaner abstraction for router and the message-routing
layer.] This is a forward direction that reshapes router's delivery target; whether it
lands before or after the triad port is OPEN (§D).

### B.2 router — owns delivery truth, adjudication, channel authority; HAS state

Source (router/src): `adjudication.rs`, `channel.rs`, `delivery.rs`,
`harness_delivery.rs`, `harness_registry.rs`, `observation.rs`, `supervision.rs`,
`tables.rs`, and a `sema` dependency (Cargo.toml: `sema = github:LiGoldragon/sema`) for
`router.redb`. So router is genuinely stateful (delivery facts, channel grants, harness
registry) and a port must give it a real SEMA plane and the richest Nexus plane of the
three (adjudication is the decision logic z6qu demands be surfaced).

`(Spirit Decision my4g)` / `(Spirit Constraint kzk5)` / `(Spirit Clarification h90n)` —
persona supervises component daemons; persona is a permissioned system daemon — frame the
supervised context router runs in. The persona engine already names the pair: source
(persona/src/engine.rs:364) defines `MESSAGE_ROUTER_COMPONENTS` (2 entries) and
`operational_delivery_components()` returns 6 — but neither message nor router consumes
triad-runtime yet (report 74 anchor), so the delivery round-trip is asserted by name only.

### B.3 orchestrate — the most advanced daemon; the runtime that RUNS the set

`(Spirit Clarification tq18)` [In the running-orchestrated-system goal, "Orchestrate"
refers to the orchestrate COMPONENT — the orchestration component runtime, repo
/git/.../orchestrate — NOT the act of orchestrating. The orchestrate component RUNS the
set of component daemons: persona (the manager of the whole thing), the introspector, the
schema daemon, and the others. persona is the engine manager; orchestrate is the runtime
that runs them together.]

orchestrate/INTENT.md goals (source): orchestrate is a real triad component (daemon, thin
CLI, ordinary `signal-orchestrate`, owner-only `owner-signal-orchestrate`); MVP creates
dynamic roles named by the work they own, creates report lanes, tracks typed claim state
to replace the fixed assistant-lane lock files. Boundaries: persona-mind owns STATE (work
graph, memory, policy truth, channel-grant authority); orchestrate owns MACHINERY (role
claims, activity log, agent-run lifecycle, spawn plans, scope-acquisition, executor
capacity, scheduling, escalation, lane registry). Principles: lane definitions are DATA,
not enum variants — the runtime registry lives in orchestrate state and owner authority
mutates it; harness assignment is a typed role field (Codex/Claude), not hidden in a
string. orchestrate/INTENT.md sequence note: "Orchestrate cuts over AFTER Spirit and mind
because the authority chain mind → orchestrate → router/harness means orchestrate's
outbound owner calls should land on the schema engine after the contracts at both ends."

`(Spirit Decision ojuh)` confirms the priority: [the priority destinations are (a)
persona-mind as the beads replacement and (b) persona-orchestrate as the tools/orchestrate
shell-helper replacement; get both daemons usable enough to substitute for their current
ad-hoc/shell substitutes.] orchestrate is genuinely stateful (sema store, role registry,
claim state, divergence, lock projection — source src/ files) so it needs a full SEMA
plane and a Nexus plane carrying all the claim/role/escalation decision logic.

`(Spirit Constraint 29s6)` / `(Spirit Correction q402)` are the orchestrate-as-coordination
rules (lock selectively, reports are claim-exempt) — these are about the workspace
coordination role, not the daemon port; noted so a port author does not conflate them.

## C. Supervision + the running orchestrated system (mazv / tq18)

`(Spirit Decision mazv)` is the apex target: [The engine target running state is a LIVE
ORCHESTRATED SYSTEM: persona — the manager and supervisor of the whole thing — runs and
supervises the introspector (persona-introspect), the schema daemon, and the other triad
components together as ONE running orchestrated whole, not just proven in-tree. Moving
toward this running orchestrated system is the direction for engine-forward effort.]
This is what "production" means for the three ports: not green tests in isolation, but
message+router+orchestrate running under persona supervision as one whole.

`(Spirit Decision 2nyd)` [the introspection component is named `introspect` (dropping the
persona prefix), uses schema-next triad interfaces, is a configurable trace destination
for all components, decides what/how to log, and is a queriable source of
tracing-derived intelligence.] introspect is a peer in the orchestrated set the three
ports join.

The supervision TEMPLATE (source, verified): orchestrate has ZERO supervision today
(grep for "supervis" in orchestrate/src returns nothing). The working template is
`mind/src/supervision.rs` — a `SupervisionPhase` Kameo actor whose `reply()` handles
`SupervisionRequest::Announce` → `Identified(ComponentIdentity{...})`,
`Query(ReadinessStatus)` → `Ready`, `Query(HealthStatus)` → `HealthReport`, `Stop` →
`StopAcknowledged`. router ALSO already has a `supervision.rs` (source). So the
supervision surface mind defines is the one persona supervision drives, and it maps
directly onto the czw0 minimal `on_start`/`on_stop` lifecycle hooks. The
orchestrate-component-forward move (report 74 P1) is to give orchestrate this same
surface.

Federation context (forward, not gating): `(Spirit Principle b9ao)` [the persona system
is federated at its core; each persona triad — mind + orchestrator + spirit plus future
components — is one federated unit; orchestrators across personas become aware of each
other's subtasks; each persona offers itself as a thing-with-context whose opinion can be
queried.] This is the eventual shape the orchestrated system grows into; not a port
blocker.

Deployment reality the running system must satisfy: `(Spirit Principle veqq)` [the update
mechanism (sema-upgrade) is a structural prerequisite for any DEPLOYED persona component:
deploy→restart→update means a daemon coming up against an existing redb must find no
schema drift OR have a migration path through sema-upgrade; without it, any contract edit
after first deploy breaks the next restart.] So router and orchestrate (both stateful)
cannot be DEPLOYED-and-iterated until either their schema is stable or sema-upgrade covers
them — a real sequencing dependency for the running-system target, distinct from getting
them to compile on the base. `(Spirit Decision hg78)` / `(Spirit Decision qvj3)` —
every code/logic change bumps the version (patch for small, minor for functionality,
major needs psyche authorization) — applies to each port commit.

## D. The contract / authority shape (meta-signal rename, two tiers, typed feedback, correlation)

### D.1 The meta-signal rename — active fleet work, names all three

`(Spirit Decision r9qy)` [The owner-signal → meta-signal rename is ACTIVE work, not
tentative. The workspace policy-contract naming standard is `meta-signal-<component>`
uniformly; `owner-signal` is stale. Run a deep rename pass auditing the workspace
guidance and the affected contract repos. As a FLEET operation, all existing owner-signal
contract repos rename to meta-signal — the 13 named repos INCLUDE `owner-signal-orchestrate`
and `owner-signal-router`. Future components are born meta-signal. For lojix specifically:
born meta-signal-lojix, never owner-signal-lojix.]

Source confirms the gap: `owner-signal-router` and `owner-signal-orchestrate` exist on
disk (not yet renamed); `signal-router`, `signal-orchestrate`, `signal-message` exist.
message has NO owner/meta contract repo (only `signal-message`) — consistent with
`(Spirit Clarification e2px)` + `(Spirit Clarification kvg1)` [meta-signal is OPTIONAL;
components with no owner relationship need only the ordinary signal contract]. So:
**router and orchestrate carry the rename; message does not get a meta-signal repo at
all** (it has no owner operations — its config arrives as typed argv per its INTENT.md,
and delivery authority lives in router).

Tension to flag (genuinely confusing, marked OPEN-ish in §E): the spirit lineage has a
COMPETING rename direction. `(Spirit Decision edgt)` / `(Spirit Decision 9npk)` /
`(Spirit Decision e9gr)` say owner-signal → **core-signal** (owner-signal-persona-spirit →
core-signal-spirit; "core owns the privileged control/library layer"). The component-triad
skill §"meta-signal is the canonical prefix" RESOLVES this: it states both
`owner-signal-*` AND `core-signal-*` are migration leftovers to retire toward
`meta-signal-*`. So for OUR three ports the target is unambiguous — `meta-signal-router`,
`meta-signal-orchestrate` — and the core-signal direction is superseded by the
meta-signal standard. Worth restating in the per-component maps so an author does not
follow the stale core-signal records.

### D.2 The two tiers — wire-only signal vs owner-only meta-signal

`(Spirit Correction l6zw)` [A component contract (`signal-<component>` and
`meta-signal-<component>`) carries ONLY the wire messaging vocabulary: the Signal Input
and Output roots, their record types, and the wire codec. Nexus and SEMA are
daemon-internal planes and must NOT appear in any contract schema. The client sends/
receives only Signal messages; never a Nexus or SEMA object. The contract emits wire types
and codec only, NOT engine traits; SignalEngine/NexusEngine/SemaEngine all live in the
daemon, which imports the contract Input and Output.] `(Spirit Clarification bodd)` makes
the audit workspace-wide [every contract repo must be audited for whether it incorrectly
carries internal Nexus or SEMA surfaces]. `(Spirit Clarification yjik, Maximum)` [signal
repos carry ONLY the signal schema; non-signal schema for runtime planes, storage, REST,
broader behavior belongs in the runtime component].

`(Spirit Correction lc2r, VeryHigh)` [The triad is NOT one daemon schema file with
Signal/Nexus/SEMA sections. A component is AT LEAST THREE separate plane schema files.
The Signal wire contract lives in the contract repos and stays wire-only. The Nexus and
SEMA plane schemas are separate schema files INSIDE the daemon crate (e.g.
`cloud/schema/nexus.schema`, `cloud/schema/sema.schema`), each declaring its own
imports/exports/input/output/namespace and importing the wire-contract Signal IO. Plane
schemas are NOT separate crates or repos. The all-in-one Spirit pilot is a NAMED
BOOTSTRAP EXCEPTION and must NOT be treated as the canonical split shape.] This is the
single most important shape record for the ports: each of the three gets a wire-only
`signal-<c>` (+ `meta-signal-<c>` for router/orchestrate) in the contract repo, and
`<c>/schema/nexus.schema` + `<c>/schema/sema.schema` inside the daemon crate. The spirit
reference's single-file schema is the exception, NOT the template — a port author must
NOT copy spirit's all-in-one layout into the contract repos (exactly the cloud mistake
l6zw records).

The owner/meta tier authority: `(Spirit Decision cgd8)` [daemon configuration is changed
through the meta-signal socket; configuration verbs live in the meta-signal contract].
`(Spirit Principle 7541)` [execution uses current-state + permission/owner message types
to authorize work, preserving a SINGLE-OWNER system so state mutation cannot race across
competing writers]. component-triad skill: meta-signal variants are owner-only, ordinary
signal variants are peer-callable; two authority surfaces = two sockets = two listener
actors. So router and orchestrate each run TWO listeners (ordinary + meta); message runs
ONE (no meta tier).

### D.3 SEMA classification words forbidden on the wire — names router + orchestrate

`(Spirit Decision 7l7l)` [Sema classification vocabulary is FORBIDDEN on the public
contract wire. The six Sema words — Assert, Mutate, Retract, Match, Subscribe, Validate —
must NOT appear as request-root tags in any signal/meta-signal contract; a contract must
NOT mirror them as an `AuthorizedSignalVerb` enum; a contract event must NOT carry the
payloadless `SemaObservation` label. These words belong to sema-engine execution and
observation only. Mandates a cleanup pass across six legacy contracts — INCLUDING
`signal-router` (and its AuthorizedSignalVerb enum) and `signal-orchestrate` (whose
`EffectEmitted SemaObservation` event gets a non-Sema label).] This is a concrete,
named, must-do cleanup on TWO of our three contract repos. Contract operation roots are
DOMAIN VERBS; the Sema class is derived internally. (signal-message is not in the six.)

### D.4 Typed feedback — no string messages

`(Spirit Principle bexd)` [Component feedback, status, and error reporting is expressed
as typed self-descriptive NOTA enums and structs whose NAMES carry the meaning, not as
long string description messages. A result type should be so well named it needs no
message string — our own feedback language built from enums/structs decoded through NOTA.
Specializes strings-only-at-the-edges to the messaging surface; should be manifested into
the architecture.] Reinforced by `(Spirit Constraint mlq0)` and `(Spirit Decision vq9b)`
(Spirit-specific applications). For the ports: every reply, rejection, and status across
message/router/orchestrate must be a typed NOTA enum (message/INTENT.md already does this
with `RequestRejectionReason`; router/orchestrate must match).

### D.5 Correlation ids — async mail correlation

`(Spirit Principle h4mn)` [Inter-component messaging uses unique identifiers for agents
and messages so asynchronous mail delivery can be correlated and complex clients can
synchronize channels WITHOUT blocking unrelated requests.] `(Spirit Clarification z821)`
[the origin route / origin identifier is carried through Signal, Nexus, and SEMA so async
replies correlate back to the initiating Signal message; SEMA replies return to Nexus with
that route, Nexus to the waiting Signal actor, Signal on the wire with the same
correlation context.] message/INTENT.md already implements the frame-level form
(`ExchangeIdentifier` echoed on every reply); the port must thread an origin-route through
all three planes, matching z821. `(Spirit Clarification b559, Medium)` proposes the
concrete carrying shape [the data-carrying Plane enum folds the origin route into each
variant as the leading tuple element] — but it is Medium-certainty, system-designer-
proposed, PENDING psyche confirmation of tuple-leading-element vs named struct field. That
is an OPEN shape detail (§E).

### D.6 Bootstrap policy — pre-encoded binary, no NOTA at runtime

`(Spirit Decision 7x50)` [Bootstrap policy is authored as NOTA source in the repo, but
production daemons consume a PRE-ENCODED typed binary artifact at first start. Live
daemons do NOT parse NOTA for bootstrap; later policy changes enter through meta-signal
authority.] For router/orchestrate, initial policy (channel grants, lane registry seed)
is a binary artifact at first start, then mutated only via the meta-signal socket — not
re-read from NOTA. This couples to D.2's meta-signal tier.

## E. Open questions / unresolved forks affecting these ports

Marked GENUINELY OPEN vs SETTLED.

1. **GENUINELY OPEN — does message need a SEMA plane at all?** message is a stateless
   boundary (INTENT.md, l3k4: it only logs message existence; delivery is router's fact).
   lc2r says a component is "at least three plane schema files," but a stateless component
   has no durable state for SEMA to own. Is message's SEMA plane empty/trivial, or does
   "log the existence of the message" (l3k4) imply a small durable log SEMA owns? No record
   resolves this. The port author must ask the psyche or carry it as a design choice.

2. **GENUINELY OPEN — does supervision live in orchestrate or persona?** tq18 says
   "persona is the engine MANAGER; orchestrate is the runtime that RUNS them together" —
   two supervisory-sounding roles. mazv says persona "runs and supervises" the set. Report
   74 P1 proposes giving ORCHESTRATE the engine-management supervision surface (porting
   mind's template). But the records consistently name PERSONA as the supervisor/manager.
   The boundary between "persona manages/supervises" and "orchestrate runs them together"
   is not crisply drawn in intent. orchestrate/INTENT.md gives orchestrate "agent-run
   lifecycle, spawn plans, executor capacity, scheduling, escalation" — which IS
   supervisory machinery — while persona-mind owns "policy truth, channel-grant
   authority." A reading that holds: persona is the privileged system daemon that
   start/stop/health-supervises DAEMONS (the OS-process layer, my4g/kzk5); orchestrate
   manages AGENT-RUNS and roles (the work layer). But that synthesis is inferred, not
   stated. This is the #1 open question the per-component maps must surface to the psyche.

3. **GENUINELY OPEN — does the agent abstraction land before or after the triad port?**
   w4jp/gdbf say router should talk to a NEW `agent` component (backends:
   persona-claude/-codex/-…), not to the harness directly. That reshapes router's delivery
   target. Porting router onto the triad base while its delivery target is itself being
   abstracted is a sequencing fork: port router-as-is then re-target, or wait for agent.
   No record sequences these.

4. **OPEN (Medium) — the origin-route carrying shape.** b559 proposes the route as the
   leading tuple element of each Plane variant; it is explicitly PENDING psyche
   confirmation (tuple-leading-element vs named struct field). The ports thread a
   correlation route (z821, settled in principle), but the concrete encoding is unsettled.

5. **OPEN — flat-vs-per-variant contract shape (carried from report 73, not yet resolved).**
   Report 73 §5 clarification A (flat record with Optional privacy vs per-kind variants)
   is still psyche-gated. It primarily gates the Spirit record redesign, but it touches
   the general question of whether contract records are flat-with-optionals or
   per-variant-shaped. Not specific to these three, but it is the workspace's open
   record-shape fork and a port author choosing record shapes should know it is open.

6. **SETTLED — the rename target is meta-signal, not core-signal.** The edgt/9npk/e9gr
   core-signal direction looked like a competing fork; the component-triad skill resolves
   it (both owner-signal AND core-signal are leftovers to retire toward meta-signal). For
   router/orchestrate the target is meta-signal-router / meta-signal-orchestrate. Treat as
   settled; just do not follow the stale core-signal records.

7. **SETTLED — the all-in-one schema is NOT the template.** lc2r (VeryHigh) settles that
   the spirit single-file schema is a named bootstrap exception; the ports use wire-only
   contracts + separate in-daemon nexus/sema schema files. No fork here despite spirit
   being the reference daemon.

8. **SETTLED — backpressure/concurrency are out of scope.** 59dr + opvx settle that
   backpressure and concurrency mode are deferred / not contract-encoded. A port author
   should not build them.

9. **DEPENDENCY (not a fork, but gating the RUNNING target) — sema-upgrade for stateful
   ports.** veqq: deployed stateful daemons need sema-upgrade or stable schema or they
   break on the next restart. router and orchestrate are stateful. This gates DEPLOYING +
   ITERATING them in the running system (mazv), not getting them to compile on the base.
   The per-component maps must state this explicitly per landed-vs-proposed honesty.

## F. Records to ignore — superseded / duplicated / out-of-scope

- **`12mi` is OUT OF SCOPE / effectively superseded for the new-base question.** `(Spirit
  Decision 12mi)` [Cloud component implementation should use the existing OLD NOTA / old
  signal macro stack, matching the production Spirit-era approach, rather than waiting for
  the new schema stack.] This is the OPPOSITE of our task (port ONTO the new base) and is
  cloud-specific and superseded by the later vnnx/ey5p/545o cloud-on-triad decisions. Do
  not let it leak into the message/router/orchestrate port reasoning.
- **The `router` topic is dominated by the Prometheus NETWORK router** (h16n, d1wr, l01b,
  wn7q, zs04, cmn7, wqfj, qkdi) — a completely different concern (cluster networking, not
  the router COMPONENT). Filter these out when sweeping `router`.
- **edgt / 9npk / e9gr (core-signal direction)** — superseded by the meta-signal standard
  per the component-triad skill (see §E.6). Cite only to note they are stale.
- **qe9z RETRACTS records 660/665** (interact-trait / interaction-actor) — the InteractTrait
  and InteractionActor abstractions are retracted; methods ARE interactions; schema-rust
  should NOT emit Interact<Input>/InteractionActor traits. A port author reading older
  reports that mention interact-traits should know they are retracted.
- **The persona FD-handoff cluster** (plr7, ns7t, n2te, my4g, a5u7, zcga, y35z, 6px0) is
  persona-cutover / Spirit-cutover machinery — relevant to the RUNNING system's no-downtime
  story but NOT to the three component ports themselves. Out of scope for the port shape.
- **Short codes re-minted** (report 73 §3): any code cited in reports older than this
  session may be stale; trust the bracket-description.

## See also

- `0-frame-and-method.md` — the frame and the anchoring finding.
- `reports/system-designer/74-engine-forward-exploration-2026-06-05/8-overview.md` —
  the start-porting-now set (P1 orchestrate supervision, P2 message+router delivery).
- `reports/system-designer/73-improved-nota-schema-situate-2026-06-05/6-overview.md` —
  the schema mechanism + the still-open flat-vs-per-kind record shape (§E.5).
- `skills/component-triad.md` — the 5 invariants, the meta-signal canonical-prefix rule
  resolving §E.6, the two-tier authority shape.
