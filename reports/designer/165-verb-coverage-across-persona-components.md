# 165 — Verb coverage across every Persona component

*Designer research-and-proposal report, 2026-05-14. Continues `/164`'s
audit by working through every component's external Signal surface,
mapping the implemented variants and the imagined-but-missing operations
each component will need as it matures, and naming the verb each
operation fits. Surfaces ten open questions where the user's intent is
load-bearing for the answer — six of them carried forward to the chat
reply per `~/primary/skills/reporting.md` §"What goes in chat when a
report exists".*

**Retires when**: the open questions in §4 are resolved (each becomes a
designer report or an ARCH edit), and the proposed verbs in §2 either
land as contracts or are explicitly deferred. At that point this report
has been absorbed into the ARCH layer and the contract crates.

---

## 0 · TL;DR

The seven-verb spine (`Assert`, `Mutate`, `Retract`, `Match`,
`Subscribe`, `Atomic`, `Validate`) covers every cross-component
operation Persona has today and every operation it plausibly needs.
**No new verb is needed**; the gaps are missing *payload variants*
inside the existing verbs, not missing root verbs.

Current count across all eight `signal-persona-*` contracts is **62
request variants**, distributed:

| Verb | Count | Use |
|---|---|---|
| `Assert` | 20 | New facts: messages, role claims, work items, prompts, terminal input, channel grants, …. |
| `Mutate` | 7 | State transitions at stable identity: handoffs, status changes, channel extensions, component lifecycle. |
| `Retract` | 7 | Withdrawals: role releases, channel retractions, gate releases, unsubscribes. |
| `Match` | 24 | One-shot reads: status queries, inbox queries, observation queries, snapshots. |
| `Subscribe` | 4 | Live streams: thoughts, relations, focus, terminal worker lifecycle. |
| `Atomic` | **0** | Reserved; no consumer. |
| `Validate` | **0** | Reserved; no consumer. |
| **Total** | **62** | |

(Recount supersedes `/164 §4.1`'s rough totals — the prior numbers were
column-skim estimates; this report walks each contract carefully.)

Proposed additions across the eight components total roughly **30 new
variants** — most are `Subscribe` (replacing poll-shaped `Match`) and
new `Assert` variants on the engine-manager contract (engine catalog
operations). The first concrete uses of `Atomic` and `Validate` need
the user's input — those are two of the open questions surfaced below.

The user-attention questions (also in the chat reply):

1. **Atomic's first use case** — which feature should drive it.
2. **Validate's first use case** — which feature should drive it.
3. **Subscribe-lifecycle pattern** — three different patterns coexist
   today; pick one canonical shape for unsubscribe.
4. **Engine adoption vs engine creation** — one `Assert` variant or two?
5. **Read-plan algebra at the CLI** — does the CLI surface
   `Constrain`/`Project`/etc. inside `Match` payloads, or stay simple?
6. **`persona-terminal`'s nine specialized binaries** — wrap, replace,
   or keep alongside a new `terminal` CLI?

(Four further questions in §4 are second-tier — important but not
blocking imminent work.)

---

## 1 · The exhaustive-coverage discipline

The verb-as-grammar discipline is structural: **every cross-component
operation in Persona is one of seven verbs**. The seven cover boundary
behavior comprehensively (per `reports/designer/162` and `/163` — the
synthesis + containment-rule decision). Specialised signals don't
escape into a different verb shape; they become typed payloads inside
the seven.

What "specialised" means in practice — operations that *feel* domain-
specific (a terminal-cell PTY resize, a Wi-Fi profile rotation, a
quorum-signature attestation, a cross-engine handshake) are all
specialised *payloads*. The boundary behavior is always one of seven
kinds:

- *Durable write a new thing* → `Assert`
- *Change an existing thing at stable identity* → `Mutate`
- *Retract / remove a thing* → `Retract`
- *Read what's stored* → `Match`
- *Watch for changes over time* → `Subscribe`
- *Bundle several operations under one commit* → `Atomic`
- *Dry-run, check against rules, don't commit* → `Validate`

The discipline applies to every component the workspace has and every
component it will have. New components join by declaring a
`signal-persona-<X>` contract with `signal_channel!` and tagging each
variant with its verb. The macro enforces the discipline at compile
time.

The exhaustive-coverage test: walk every operation a component
performs across its boundary. Every one fits into exactly one verb.
If one doesn't fit, the seven-verb closure is falsified and a designer
report names the missing verb. None has surfaced yet (per `/163 §5`'s
resolved falsifiability conditions).

The rest of this report applies that test to every existing component
and proposes the verb each unimplemented operation should fit into.

---

## 2 · Per-component analysis

Each subsection has:
- **Implemented variants** — what the contract declares today, with
  verb tags.
- **Missing or proposed variants** — operations the component will
  need as it matures, with the verb each fits into.
- **Open questions** — uncertainties surfaced by walking the surface.

### 2.1 · `signal-persona` (engine manager)

Owns the apex contract — the `persona` daemon's boundary. Two channels:
`EngineRequest` (client → manager) and `SupervisionRequest` (manager →
supervised child).

**Implemented today** (4 + 4 = 8):

| Channel | Verb | Variant | Boundary use |
|---|---|---|---|
| Engine | `Match` | `EngineStatusQuery` | Read whole-engine status. |
| Engine | `Match` | `ComponentStatusQuery` | Read one component's status. |
| Engine | `Mutate` | `ComponentStartup` | Transition a component's desired state to Running. |
| Engine | `Mutate` | `ComponentShutdown` | Transition a component's desired state to Stopped. |
| Supervision | `Match` | `ComponentHello` | Component announces identity to manager. |
| Supervision | `Match` | `ComponentReadinessQuery` | Manager probes child readiness. |
| Supervision | `Match` | `ComponentHealthQuery` | Manager probes child health. |
| Supervision | `Mutate` | `GracefulStopRequest` | Manager asks child to drain and stop. |

**Missing / proposed** (engine-level catalog operations):

| Verb | Proposed variant | Why this verb | Rationale |
|---|---|---|---|
| `Assert` | `EngineLaunch(EngineLaunchProposal)` | New catalog row asserted | Spawn + register a fresh engine in the manager's catalog. The gap from `/164 §4.3`. |
| `Assert` | `EngineAdoption(EngineAdoption)` | Same — adopting an already-running peer engine into the catalog is still an `Assert` on a catalog row, just constructed from a different source. | See §4 Q4 — possibly one variant carrying a union payload, or two distinct variants. |
| `Match` | `EngineCatalog(EngineCatalogQuery)` | Read catalog | List engines known to this manager. |
| `Retract` | `EngineRetirement(EngineRetirement)` | Withdraw a catalog row | Retire an engine cleanly. |
| `Atomic` | `EngineUpgrade(EngineUpgradePlan)` | Multi-step commit | Bundle: spawn engine v2 → migrate state via channels → retire engine v1. Per persona ARCH §1.6.5 "Multi-engine as upgrade substrate" — this is exactly an `Atomic`. |
| `Subscribe` | `EngineHealthStream(EngineHealthFilter)` | Push-not-pull | Replace status-poll loops. |
| `Subscribe` | `ComponentHealthStream(ComponentHealthFilter)` | Push-not-pull | Per-component health stream. |
| `Assert` | `EngineRoute(EngineRouteProposal)` | New cross-engine route asserted | Cross-engine routing (per ARCH §1.6.4). |
| `Retract` | `EngineRouteRetraction(EngineRouteRetraction)` | Withdraw a route | Same. |

On the supervision channel:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `ComponentLifecycle(ComponentLifecycleFilter)` | Manager subscribes to lifecycle events from each child rather than polling readiness/health. |
| `Atomic` | `CoordinatedShutdown(CoordinatedShutdownPlan)` | All-components-stop-in-order, as one commit (avoid half-drained state on engine retirement). |

**Open questions surfaced**:

- Q4 (chat-surfaced): adoption-vs-creation — same `Assert` variant or two?
- Q1 (chat-surfaced): the engine-upgrade `Atomic` is one obvious first
  consumer for `Atomic`. Is this the right first use, or should
  schema-migration take priority?

### 2.2 · `signal-persona-mind`

The largest contract surface in Persona — 24 variants — because mind is
the central state component (per persona ARCH §0: "the center of agent
state is `persona-mind`").

**Implemented today** (24): see `/164 §4.1` for the table. Distribution:
11 Assert, 3 Mutate, 2 Retract, 6 Match, 2 Subscribe.

Domains covered: thoughts/relations (sema-graph substrate), role
coordination (claim/release/handoff), activity log, work memory
(opening/note/link/status/alias/query), channel choreography
(grant/extend/retract/list, adjudication request/deny).

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Atomic` | `ClaimHandoff(...)` | Currently `RoleHandoff` is one `Mutate`; if the handoff atomically *retracts* role A's claim and *asserts* role B's claim (cleaner audit trail), this becomes an `Atomic` over `Retract` + `Assert` instead of an opaque `Mutate`. See §4 Q1 — possible first `Atomic` use. |
| `Retract` | `SubscriptionRetraction(SubscriptionToken)` or paired per-Subscribe `Retract` variants | Today `SubscribeThoughts` and `SubscribeRelations` have no explicit unsubscribe (closes implicitly on connection drop). Compare to `signal-persona-system`'s `Retract FocusUnsubscription`. See §4 Q3. |
| `Validate` | `ChannelGrantValidation(ChannelGrantProposal)` | Dry-run a channel grant: does it conflict with existing channels? Useful when mind's adjudicator wants to test a grant before committing. See §4 Q2. |
| `Validate` | `TypeProposalValidation(TypeProposal)` | Dry-run a `TypeProposal` (per `/163 §5.1` — proposal-and-recompile flow). When the flow lands, `Validate` is its natural first contract use. See §4 Q2. |
| `Match` | `ChannelEventLog(ChannelEventLogQuery)` | Read the channel event history (today only `ChannelList` exposes current channels; no historical access). |
| `Subscribe` | `RoleObservationStream(RoleObservationFilter)` | Push-not-pull replacement for the periodic `RoleObservation` poll. |
| `Subscribe` | `ActivityStream(ActivityFilter)` | Same — replace periodic activity-log polling. |

**Open questions surfaced**:

- Q1, Q2, Q3 (chat-surfaced) above.

### 2.3 · `signal-persona-message`

The sparsest contract — three variants:

**Implemented today** (3):

| Verb | Variant | Boundary use |
|---|---|---|
| `Assert` | `MessageSubmission` | A user submits a message to a recipient. |
| `Assert` | `StampedMessageSubmission` | Same, post-stamping by message-daemon. |
| `Match` | `InboxQuery` | One-shot inbox read. |

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `InboxStream(InboxFilter)` | Push-delivery of new messages. Today the CLI is one-shot. A long-running harness wants live delivery, not poll. |
| `Mutate` | `MessageMarkRead(MessageSlot)` | Update read-state on a message. |
| `Retract` | `MessageDeletion(MessageSlot)` | Delete a message from the inbox. |
| `Atomic` | `BatchSubmission(Vec<MessageSubmission>)` | Submit many messages atomically (e.g. a batched harness output). |
| `Validate` | `MessageSubmissionValidation(MessageSubmission)` | Dry-run: would this message pass the recipient's filters / channel policy? |

**Open questions surfaced**: none specific; the gaps are standard
push-not-pull and CRUD-completion patterns.

### 2.4 · `signal-persona-router`

Intentionally observation-only — per persona ARCH §1.6.3 "**Mind
decides; router enforces.**" Operational writes (channel grants etc.)
live in `signal-persona-mind`, not here.

**Implemented today** (3):

| Verb | Variant | Boundary use |
|---|---|---|
| `Match` | `RouterSummaryQuery` | Read router summary stats. |
| `Match` | `RouterMessageTraceQuery` | Read one message's delivery trace. |
| `Match` | `RouterChannelStateQuery` | Read one channel's current state. |

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `RouterEvents(RouterEventFilter)` | Push delivery / routing event stream for live observation (replaces any consumer polling RouterSummaryQuery). |
| `Match` | `RouteList(RouteListQuery)` | List active cross-engine routes (when federation lands). |

**Open questions surfaced**:

- (second-tier, §4 Q9) The router is intentionally pure-observation
  externally. Is that the long-term shape — i.e., **the router never
  has Assert/Mutate/Retract on its external surface**, with channel
  operations always going through mind? Confirming this keeps the
  router's contract well-bounded.

### 2.5 · `signal-persona-harness`

Bidirectional channel between router and harness. Router pushes
deliveries; harness pushes lifecycle/resolution events.

**Implemented today** (4):

| Verb | Variant | Direction | Boundary use |
|---|---|---|---|
| `Assert` | `MessageDelivery` | router → harness | Deliver a message through the harness's terminal. |
| `Assert` | `InteractionPrompt` | router → harness | Show a typed prompt and await a resolution. |
| `Retract` | `DeliveryCancellation` | router → harness | Cancel a pending delivery. |
| `Match` | `HarnessStatusQuery` | router → harness | Probe harness readiness. |

Note: the *reply* side carries `HarnessStarted`, `HarnessStopped`,
`HarnessCrashed` as events on the same channel — not yet a typed
Subscribe.

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `HarnessLifecycle(HarnessLifecycleFilter)` | Make the lifecycle stream a first-class subscription rather than reply-events on a bidirectional channel. |
| `Atomic` | `DeliveryBatch(Vec<MessageDelivery>)` | Atomic batch of deliveries to a harness (preserves ordering on multi-message scenarios). |
| `Validate` | `DeliveryValidation(MessageDelivery)` | Dry-run a delivery: can the harness accept *now* (gate, prompt state)? Useful for the router's pre-flight before binding the input gate. |

**Open questions surfaced**: none specific.

### 2.6 · `signal-persona-terminal`

12 variants — the second-largest contract surface after mind.

**Implemented today** (12):

| Verb | Count | Variants |
|---|---|---|
| `Assert` | 5 | `TerminalConnection`, `TerminalInput`, `RegisterPromptPattern`, `AcquireInputGate`, `WriteInjection` |
| `Mutate` | 1 | `TerminalResize` |
| `Retract` | 3 | `TerminalDetachment`, `UnregisterPromptPattern`, `ReleaseInputGate` |
| `Match` | 2 | `TerminalCapture`, `ListPromptPatterns` |
| `Subscribe` | 1 | `SubscribeTerminalWorkerLifecycle` |

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Atomic` | `TerminalSetupBundle(...)` | Atomic: register prompt pattern + acquire gate + connect, on first session bring-up. Avoids race between connect and gate-arrival. |
| `Validate` | `WriteInjectionValidation(WriteInjection)` | Dry-run that an injection wouldn't conflict with human input *right now* without committing. |

**Open questions surfaced**:

- Q6 (chat-surfaced): the CLI surface for terminal — nine specialized
  binaries vs one `terminal` CLI. Wrap, replace, or keep alongside?

### 2.7 · `signal-persona-system`

OS-fact observation contract. Skeleton today; backend is Niri-only.

**Implemented today** (4):

| Verb | Variant | Boundary use |
|---|---|---|
| `Subscribe` | `FocusSubscription` | Start watching focus state. |
| `Retract` | `FocusUnsubscription` | Stop watching. |
| `Match` | `FocusSnapshot` | One-shot focus read. |
| `Match` | `SystemStatusQuery` | Read system daemon's backend status. |

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `SystemBackendLifecycle(...)` | Push: backend started / stopped / degraded. |
| `Atomic` | `BackendTransition(BackendTransitionPlan)` | Coordinated switch between backends (e.g., Niri → Hyprland). One-shot, multi-step. |

Note: `signal-persona-system` **is the canonical example** of paired
Subscribe + Retract — `FocusSubscription` and `FocusUnsubscription` are
explicit. Other contracts should follow this pattern (see §3.3).

**Open questions surfaced**: none beyond the workspace-wide ones.

### 2.8 · `signal-persona-introspect`

Inspection-plane component. Today four `Match` variants; Slice 3 adds
Subscribe.

**Implemented today** (4):

| Verb | Variant | Boundary use |
|---|---|---|
| `Match` | `EngineSnapshot` | Whole-engine snapshot. |
| `Match` | `ComponentSnapshot` | One component's snapshot. |
| `Match` | `DeliveryTrace` | Trace one message's path. |
| `Match` | `PrototypeWitness` | Confirm prototype witness facts. |

**Missing / proposed**:

| Verb | Proposed variant | Rationale |
|---|---|---|
| `Subscribe` | `SubscribeComponent(ComponentSubscriptionFilter)` | Named in persona-introspect ARCH constraints as the Slice 3 addition. |
| `Subscribe` | `SubscribeEngineEvents(EngineEventFilter)` | Push: engine-level event stream. |
| `Subscribe` | `SubscribeDeliveryTrace(DeliveryTraceFilter)` | Push: live delivery trace stream. |
| `Retract` | `IntrospectionSubscriptionRetraction(SubscriptionToken)` | Paired with the new Subscribes. |

**Open questions surfaced**: none beyond the subscribe-lifecycle one.

---

## 3 · Cross-cutting verb-usage analysis

### 3.1 · `Atomic` is unused — what should drive its first use?

`Atomic` is the only multi-operation verb. Today it has zero
consumers. Several plausible first-uses sit on the proposed-additions
list above. The candidates differ in implementation complexity and
load-bearing-ness:

| Candidate | Component | Implementation cost | Load-bearing |
|---|---|---|---|
| `EngineUpgrade` | persona | High (multi-engine federation needed first) | Critical for cutover discipline |
| `SchemaMigration` (over `sema-engine`'s catalog table) | persona-mind / sema-engine | High (proposal-and-recompile flow needs to land) | Critical for any sema-version evolution |
| `ClaimHandoff` (Retract + Assert atomically) | persona-mind | Low | Cleaner audit trail; not critical |
| `BatchSubmission` | persona-message | Low | Optimization; not critical |
| `TerminalSetupBundle` | persona-terminal | Low | Avoids first-bring-up races |
| `CoordinatedShutdown` | persona (supervision) | Medium | Needed for clean engine retirement |

The choice affects which component owns the *reference implementation*
of `Atomic` — the first one to land sets the pattern for the rest.

### 3.2 · `Validate` is unused — what's the first?

Same shape. Candidates:

| Candidate | Component | Use |
|---|---|---|
| `TypeProposalValidation` | persona-mind | Dry-run a `TypeProposal` record before commit (per `/163 §5.1`'s proposal-and-recompile flow). |
| `SchemaCheck` | sema-engine (downstream of persona-mind) | Pre-flight constraint check before migration commit. |
| `ChannelGrantValidation` | persona-mind | Dry-run a channel grant for conflict detection. |
| `WriteInjectionValidation` | persona-terminal | Dry-run before injecting into a terminal. |
| `DeliveryValidation` | persona-harness | Dry-run a delivery (gate clean? harness ready?). |

The most natural first-Validate is probably **schema-migration
pre-flight** — `Validate` was named specifically for this case in
`/163 §2.6`. But that depends on the migration flow itself landing
first.

### 3.3 · `Subscribe`-lifecycle inconsistency

Three patterns coexist today for "stop subscribing":

| Contract | Subscribe variant | Unsubscribe variant |
|---|---|---|
| `signal-persona-system` | `Subscribe FocusSubscription` | `Retract FocusUnsubscription` (explicit, paired) |
| `signal-persona-terminal` | `Subscribe SubscribeTerminalWorkerLifecycle` | (none — implicit on connection close) |
| `signal-persona-mind` | `Subscribe SubscribeThoughts` / `SubscribeRelations` | (none) |

Three patterns is two patterns too many. Either:

- **(A)** Every Subscribe variant has a paired `Retract` variant
  (mirrors `signal-persona-system`'s explicit shape).
- **(B)** Every contract crate has a *single* `Retract SubscriptionRetraction(SubscriptionToken)` variant covering all that contract's subscriptions.
- **(C)** Subscribes close implicitly on connection drop only (the
  current `mind` and `terminal` shape); no Retract variants.

Pattern (A) is the loudest at the contract level — every subscribe
declares its lifecycle explicitly. Pattern (B) keeps the contract
smaller. Pattern (C) is the simplest but coarsest. **Pick one** — see
§4 Q3.

### 3.4 · Read-plan algebra surfacing at the CLI

The five demoted operators (`Constrain`, `Project`, `Aggregate`,
`Infer`, `Recurse`) live in `sema-engine::ReadPlan<R>`, *inside*
`Match` / `Subscribe` / `Validate` payloads — not as root verbs.

**Question**: when a CLI user types a `Match` request, do they ever
construct a ReadPlan directly?

```text
# Simple shape (what every CLI does today):
mind '(Match (Query (kind ByStatus) (limit 100)))'

# Read-plan-bearing shape (hypothetical):
mind '(Match (ReadPlan (Project (fields title body)) (Constrain (Query (kind ByStatus)) (Query (kind RecentEvents)))))'
```

The simple shape is what `mind`, `message`, `introspect` use today. The
read-plan shape would surface query algebra to the CLI grammar.
**Whether to surface it determines the CLI's expressive ceiling.**

### 3.5 · 60+ `Match` vs only 4 `Subscribe` — push-not-pull pressure

The verb distribution is heavily Match-skewed: 24 Match, 4 Subscribe.
Per `ESSENCE.md` §"Polling is forbidden", consumers that want live
updates should be on Subscribe, not poll-Match. Today's contracts
expose far more one-shot reads than streams.

Many of the proposed Subscribe additions in §2 are exactly this
correction: `RoleObservationStream`, `ActivityStream`,
`InboxStream`, `RouterEvents`, `HarnessLifecycle`,
`EngineHealthStream`, `ComponentHealthStream`,
`SubscribeEngineEvents`, etc.

This is not a verb-design issue — it's a **contract-side completeness
gap**. The Match variants stay (they cover legitimate one-shot uses);
the Subscribe variants need to be added alongside.

---

## 4 · Open questions

These need the user's input. The first six are also in the chat reply
per `~/primary/skills/reporting.md` §"What goes in chat when a report
exists".

### Q1 — What drives `Atomic`'s first contract use? (chat-surfaced)

The verb `Atomic` ("execute a group of operations under one commit
boundary") has zero consumers. Several candidates (§3.1 table). The
first to land sets the pattern.

**Recommendation**: schema migration (driven by sema-engine's
catalog table) is the cleanest match — `/163 §2.4` already named it
as the canonical Atomic use case. But that depends on the
proposal-and-recompile flow landing. **Alternate first-use**:
`ClaimHandoff` in `signal-persona-mind` is low-cost and gives the
pattern an early consumer.

Decision needed: which first?

### Q2 — What drives `Validate`'s first contract use? (chat-surfaced)

Same shape (§3.2 table). Recommendation: `Validate` first lands as a
schema-migration dry-run when the migration flow arrives.

Decision needed: which first, and is the recommendation right?

### Q3 — Which Subscribe-lifecycle pattern is canonical? (chat-surfaced)

§3.3 above names three coexisting patterns. The cleanest answer is
probably **(A) every Subscribe variant has a paired Retract variant**
(matches `signal-persona-system`'s shape; makes the wire vocabulary
explicit). But the user's intent is what decides.

Decision needed: A, B, or C?

### Q4 — Engine adoption vs engine creation: one Assert or two? (chat-surfaced)

`signal-persona`'s engine catalog will gain an `Assert` for engine
creation (per `/164 §5.1`). When cross-engine federation lands, the
manager will also need to *adopt* an already-running peer engine
into its catalog. Two operations, both `Assert` on the catalog:

- `Assert EngineLaunch(EngineLaunchProposal)` — spawn from spec
- `Assert EngineAdoption(EngineAdoptionProposal)` — pick up an
  existing peer

Both end as a catalog row, but the payload shapes differ
substantially. **One Assert variant with a union payload, or two
distinct Assert variants?**

Decision needed.

### Q5 — Does the CLI surface ReadPlan algebra? (chat-surfaced)

§3.4 above. The choice affects every CLI's expressive ceiling.

**Simple-shape vote**: keep CLIs to `verb + simple payload`. Power
users construct ReadPlans programmatically.

**Read-plan-bearing-shape vote**: CLI is the full grammar; `mind` /
`message` / etc. can express any ReadPlan the engine supports.

Decision needed: simple or full?

### Q6 — `persona-terminal`'s nine command-shaped binaries (chat-surfaced)

§2.6 + `/164 §5.3`. Options:

- **(a) Wrap as shims**: `persona-terminal-send foo` desugars to
  `terminal '(Assert (TerminalInput (bytes foo)))'`. Backward
  compatibility during cutover.
- **(b) Replace immediately**: drop the nine binaries, ship one
  `terminal '<NOTA record>'` CLI.
- **(c) Keep alongside**: `terminal` is the canonical CLI; the nine
  specialized binaries stay as ergonomic shortcuts.

Decision needed: a, b, or c?

### Q7 — Is `persona-router` permanently observation-only externally? (second-tier)

Today router's external contract is three `Match` queries. Channel
operations live in mind. Confirming this is permanent keeps the
router contract well-bounded; deferring the question leaves the
discipline ambiguous.

### Q8 — Cross-engine federation contract shape (second-tier)

When engine A's mind talks to engine B's mind, is the wire
`signal-persona-mind` over a network socket, or a new
`signal-persona-federation` contract? Today this is deferred to
post-second-engine work, but the contract shape decision will be
load-bearing.

### Q9 — Auth handshakes when network components arrive (second-tier)

Today auth is filesystem-ACL + SO_PEERCRED (per persona ARCH §1.6).
When `Network(NetworkSource)` connections arrive, do they grow an
in-band `Assert` of a `Challenge` record? Or do all challenges live
below the Signal layer (e.g., TLS-style handshake before any Signal
frame flows)?

### Q10 — Sub-component contracts inside terminal-cell (second-tier)

`terminal-cell` is consumed by `persona-terminal` (per
`active-repositories.md`). Does it have its own
`signal-terminal-cell` contract for its PTY workers, or are its
internal signals not crossing a Signal boundary?

---

## 5 · Concrete recommendations

1. **Land the engine-catalog operations on `signal-persona`**
   (Assert EngineLaunch / Match EngineCatalog / Retract
   EngineRetirement). Operator-assistant has already picked this up
   per the current operator-assistant lock; this is the first
   landing.

2. **Add `Subscribe`-shaped variants alongside every poll-shaped
   `Match`** that consumers want live (§3.5 list). This is roughly
   8–10 new Subscribe variants across mind, message, router, harness,
   persona, introspect. Each adds a few lines to the relevant
   `signal_channel!` invocation.

3. **Normalize the Subscribe-lifecycle pattern**. Pick A/B/C per Q3;
   update `signal-persona-mind` and `signal-persona-terminal` to
   match. `signal-persona-system` is the existing model for pattern
   A.

4. **Resolve Q1 + Q2**, then **land the first `Atomic` and `Validate`
   contract uses**. The reference implementation sets the pattern
   for the rest. Schema-migration is the strongest natural fit for
   both; an alternative low-cost first-Atomic is mind's `ClaimHandoff`.

5. **Resolve Q5 (ReadPlan surfacing)** before terminal-cli convergence
   (Q6) — the CLI's grammar shape depends on it.

6. **Defer** the second-tier questions (Q7–Q10) until they have
   concrete-consumer pressure. The second-engine demonstration is the
   trigger for Q8/Q9; `terminal-cell`'s own component evolution is
   the trigger for Q10.

---

## 6 · See also

- `~/primary/reports/designer/164-signal-core-vs-signal-and-cli-verb-wrapping.md`
  — the prior audit (per-contract verb mapping, CLI shape, the
  engine-catalog gap that's now being picked up).
- `~/primary/reports/designer/162-signal-verb-roots-synthesis.md` —
  the seven-verb spine, the planet bijection.
- `~/primary/reports/designer/163-seven-verbs-no-structure-eighth.md`
  — schema-as-data containment; Atomic and Validate's canonical use
  cases at §2.4 / §2.6.
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` — the
  seven-verb kernel.
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` — the apex
  Persona architecture: §1.5 engine-manager model, §1.6 local
  boundary, §1.6.5 multi-engine upgrade substrate (the natural
  `Atomic EngineUpgrade` use case).
- `~/primary/skills/contract-repo.md` §"Signal is the database
  language — every request declares a verb" — the discipline.
- `~/primary/skills/reporting.md` §"What goes in chat when a report
  exists" — the rule this report's chat-companion follows.
