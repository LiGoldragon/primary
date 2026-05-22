# 249 — Per-component intent gap analysis

*A read-and-compile pass over every persona component (and the
overall engine design) inventorying what is settled by psyche
intent, what is settled by agent design without psyche backing,
what is openly unsettled, and what is implicitly assumed without
ever having been posed. No architecture changes here; this is a
gap audit.*

## 0 · TL;DR

The persona ecosystem has very strong intent backing for the
**cognitive layer** (spirit, mind, orchestrate boundary,
contract-local verbs, three-layer model, LLM-mediation) and very
sparse intent backing for **engine-level mechanics** (spawn order
beyond "spirit last," supervisor-as-process-vs-cognitive-authority
disambiguation, persona-introspect's universal observer hook,
owner-signal emergence rules, persona-system unpause criteria).
The biggest single gap is that the engine manager (`persona`
repo's ARCHITECTURE.md, 1513 lines) is almost entirely agent-design
without a corresponding psyche intent surface — no `INTENT.md` for
the persona meta-repo, no top-level intent file consolidating what
the engine is.

Ten highest-severity gaps, ranked:

1. **(High) Spirit-to-mind owner contract scope is open.**
   Psyche stated "spirit owns mind" and "develops as it develops";
   no current intent says what `owner-signal-persona-mind` verbs
   spirit actually issues. Blocks spirit-to-mind integration the
   moment it's attempted.
2. **(High) Owner-graph apex disambiguation.**
   `intent/persona.nota` 2026-05-19T14:00 places spirit as
   "apex…notwithstanding the supervisor." But /233's authority
   chain inserts `persona-daemon` above mind, and /232's chain
   makes the supervisor own spirit through
   `owner-signal-persona-spirit`. Who exactly is "the supervisor"
   in psyche language — `persona-daemon`? `EngineSupervisor` actor?
   Both? Never settled by psyche.
3. **(High) The persona meta-repo has no INTENT.md.**
   `/git/.../persona/ARCHITECTURE.md` is 1513 lines and ~all
   agent-design. Engine-manager model, manager event log, snapshot
   reducers, multi-engine catalog, sandbox runner, dev-stack,
   `MessageOrigin` and `ConnectionClass` semantics — none of these
   carry direct psyche citations. Most expensive single surface in
   the workspace by code volume and the one with the least intent
   backing.
4. **(High) `persona-introspect`'s universal observer-hook
   mechanism contradicts intent/component-shape.nota.**
   Intent says (2026-05-19T20:00Z) introspect consumes all
   contracts and subscribes via a universal observer hook on the
   normal (ordinary) socket. The /246-v4 spec replaces this with
   mandatory `Tap`/`Untap` macro-injected verbs on every persona
   component's ordinary contract. `signal-persona-introspect`'s
   current ARCH (258 lines) still describes per-peer client actors
   sending `RouterRequest::Summary` etc. Whether
   `ObserverFanout`/`Tap`/`Untap` IS the universal observer-hook
   the psyche intended, or is a different mechanism, has never
   been asked.
5. **(High) `persona` engine-manager is not affirmed as a triad
   component.**
   The engine manager has a daemon, a CLI (`persona`), and a
   contract (`signal-persona`); its ARCH says so. But intent never
   states whether the engine manager IS a persona component (in
   which case the persona-system component-triad rules apply
   uniformly), or is "above persona" infrastructure that components
   sit inside, or is itself a special-cased triad. The five
   invariants from `skills/component-triad.md` apply to engine
   manager only by silent assumption.
6. **(Medium) `persona-system` unpause criteria are agent-stated.**
   ARCH §0.7 + §1.5 say persona-system is "paused" until a real
   consumer surfaces; the candidates listed (window-focus-aware
   notifications, multi-engine UI, multi-monitor layout) are
   designer guesses. Psyche never said what conditions trigger
   unpause.
7. **(Medium) `persona-harness` `HarnessKind` closed-enum policy
   has no intent backing.**
   ARCH says `HarnessKind` is closed (`Codex | Claude | Pi |
   Fixture`) and new harnesses require coordinated schema bumps.
   Workspace-level workspace intent loosens fixed enums elsewhere
   (lane-registry-as-data superseded `RoleName` enum) — same
   tension applies here. Has the psyche stated that harness kind
   stays a closed enum? Not found in any intent file.
8. **(Medium) Spirit guardian timing is dependent on
   "multi-agent auditing system" with no roadmap.**
   `intent/persona.nota` 2026-05-19T17:30Z says spirit is dumb
   storage today; the spirit guardian (judging contradictions
   under the negation / certainty-lowering / escalation model
   from 2026-05-19T15:30Z) "waits for the multi-agent auditing
   arc." No intent specifies what the multi-agent auditing arc
   is or when it begins. Spirit's intent-supersession lifecycle
   is in suspension.
9. **(Medium) The 5 missing owner-signal-* repos' emergence
   criteria are deliberate-but-unscoped.**
   `intent/component-shape.nota` 2026-05-19T20:30Z says
   `owner-signal-persona-mind`, `-router`, `-harness`, `-message`,
   `-auth` are intentionally missing because "the workspace is
   moving fast" — but no intent says under what condition each
   gets created. Triad invariant #4 (`owner-signal` is part of the
   triad; ship both surfaces together) thus has five live
   violations the psyche has accepted; the unblocking rule is
   unwritten.
10. **(Medium) Spawn order beyond "spirit last" has no intent
    behind it.**
    `intent/persona.nota` 2026-05-19T14:00Z says spirit is
    spawned last. /232 §6 lists the full order
    (`supervisor → mind → orchestrate → router → harness →
    terminal → message → introspect → … → spirit`) but everything
    between supervisor and spirit is designer-chosen. Whether
    mind comes before orchestrate, whether terminal can spawn
    before harness or only after, whether introspect must be
    last-before-spirit because it depends on every other contract
    — all agent-design.

The cross-cutting pattern: **intent is densely backed at the
boundary where the psyche personally engages (spirit, intent
records, contract-local verbs, three-layer model) and sparsely
backed at the infrastructure boundary the psyche has no daily
contact with (engine manager, spawn sequencing, persona-introspect
mechanism, owner-graph apex above spirit, harness-kind closure).**
The settled-by-design surface is honest about itself — most of
`/git/.../persona/ARCHITECTURE.md` makes no false claim of psyche
backing — but the absence of an `INTENT.md` for the engine
manager leaves the largest single architectural surface in the
ecosystem unrooted in psyche intent.

## 1 · persona-spirit

### Settled by intent

- **Spirit exists as a new triad component, animating the
  persona.** `intent/persona.nota` 2026-05-19T14:00 (Decision +
  Principle). Repo created; daemon + thin CLI + bootstrap-policy
  per `skills/component-triad.md`. ESSENCE.md §"Persona is
  meta-AI; spirit animates" promotes the founding statement.
- **Apex of the cognitive authority chain.** Same record;
  "spawned last" derived from same. Authority graph in
  persona-spirit/ARCHITECTURE.md §"Authority" matches.
- **Spirit owns mind.** `intent/persona.nota` 2026-05-19T15:30Z
  (Decision): *"Yes, of course spirit owns mind."*
- **Bootstrap-policy.nota is the root intent.** Same date — the
  first intent, Bhagavad Gita-flavored sacred-teachings content,
  research arc deferred. Implemented as minimal placeholder.
- **Spirit is LLM-mediated.** Same date (Principle):
  *"there's no component that works without LLMs."* Manifested
  in workspace `INTENT.md` §"Persona is LLM-mediated end-to-end."
- **Agent-CLI flow is correct shape.** Same date (Decision): no
  separate psyche-facing wrapper tool; agents construct NOTA
  `PsycheStatement` records and invoke the spirit CLI.
- **Query surface is summary-first.** Same date (Principle):
  verbatim/context/timestamp on demand only. Manifested in
  `signal-persona-spirit::ObservationMode::SummaryOnly` per
  contract ARCH §"Constraints."
- **Intent lifecycle has 3 transitions (negation / certainty
  lowering / escalation).** Same date (Decision). NOT yet
  implemented — see §"Unsettled" below for what blocks.
- **Components ship in raw form first.** Same date (Principle):
  spirit's first slice is standalone CLI + daemon + sema state.
  Implemented; spirit-to-mind wiring deferred.
- **Spirit is dumb storage today.** `intent/persona.nota`
  2026-05-19T17:30Z (Decision): spirit doesn't classify or
  judge; agents are the thinking layer. ARCH "Status" section
  matches.
- **Spirit's intent record shape: separate records, no Vec
  verbatim, agent-supplied identifier forbidden.**
  `intent/persona.nota` 2026-05-19T17:30Z (Decision +
  Correction + Clarification). Repo ARCH constraints match
  (RecordIdentifier output-only, Entry is one psyche statement
  per record).
- **Naming inside spirit: no `Intent` prefix.**
  `intent/persona.nota` 2026-05-19T17:30Z (Correction).
  Generalised to `intent/naming.nota` 2026-05-19T15:46:23Z.
- **Implement spirit as far as clear intent allows.**
  `intent/persona.nota` 2026-05-19T18:13:52Z (Constraint).
  Operator directive captured.

### Settled by agent design (no psyche backing)

- **Actor topology** (`SpiritRoot / OwnerPlane / PolicyPlane /
  IngressPhase / NotaDecoder / DispatchPhase / StatePlane /
  SubscriptionPlane / RecordStore / ReplyShaper /
  ReplyTextEncoder / SemaWriter trace / SemaReader trace`):
  /232 §9 and the implementation. Psyche has not stated actor
  layout for spirit, just "implement actor planes" generically.
- **Six round-trip-witness states for working state** (psyche
  presence log, intent history, pending clarification
  questions, forwarded-Mutate audit): /232 §4. All sensible;
  none psyche-cited.
- **`Watch`/`Unwatch` as spirit's domain subscription verbs.**
  signal-persona-spirit ARCH §"Contract Surface (after
  migration)." `Tap`/`Untap` are mandatory per /246-v4; the
  domain `Watch`/`Unwatch` is agent-named.
- **Spirit's 5 owner verbs (`Start`, `Drain`/`Stop`, `Reload`,
  `Register`, `Retire`).** owner-signal-persona-spirit
  ARCH; standard lifecycle pattern, agent-designed.
- **"OS-level supervisor" identity vs cognitive supervisor.**
  ARCH says "the supervisor has higher infrastructure
  permission only" but doesn't name which workspace object
  IS the supervisor. /232 §2 says it's the same supervisor
  that touches every other component (persona-daemon's
  `EngineSupervisor` actor). Psyche never confirmed this
  identity.
- **Spirit's daemon takes one typed `DaemonConfiguration`
  argument** and binds two sockets. Component-triad invariant;
  agent-design driven by that invariant.

### Unsettled / open

- **Spirit-to-mind concrete verb set on
  `owner-signal-persona-mind`.** Psyche-explicitly open:
  *"the concrete verb set develops as both components flesh
  out."* (`intent/persona.nota` 2026-05-19T15:30Z.) No
  starting list given; ARCH §"Authority" only says the apex
  relationship is settled and the verb set develops.
- **What is the multi-agent auditing arc.** Spirit guardian
  (negation/lowering/escalation judge) waits for it. No
  intent describes its boundary, components, or trigger.
- **Filesystem intent projection: status.** Spirit ARCH "Not
  implemented" says "filesystem intent projection" is
  deferred. /232 §7 says filesystem becomes a projection once
  spirit ships; cutover-sequencing intent was explicitly
  rejected (`intent/workspace.nota` 2026-05-19T15:35:00Z —
  *"Stop talking to me like you're some kind of
  bureaucrat"*) so this is in agent territory but with no
  current direction beyond "ship raw form first."
- **Subscription event delivery.** ARCH "Not implemented." A
  required mechanism; nothing in intent.
- **The intent-classifier actor.** ARCH §"Status" says
  classifier is deferred until clear intent. Intent silent
  on what the classifier does; ARCH only says LLM mediation
  is intrinsic, not what the LLM call does inside spirit.

### Implicit gaps

- **What `Statement` payload IS.** ARCH and contract have
  `Statement` as the payload of `State`; no canonical example
  in intent log specifies the field layout — what fields it
  carries, whether the psyche's verbatim quote is in
  `Statement` or in `Quote` (the State payload alternative
  named in `signal-persona-spirit/ARCHITECTURE.md` MUST IMPLEMENT
  section), whether timestamp is `Statement`-side or
  `Entry`-side.
- **How spirit knows it's spirit.** Spirit's bootstrap is
  the root intent; what about spirit's own identity? Does
  the supervisor pass a `PsycheIdentity`? Spirit's `Register`
  / `Retire` owner verbs imply identity as data — but how
  does spirit know which psyche is talking to it? Implied
  answer: SO_PEERCRED + spawn-envelope identity. Never
  posed.
- **What spirit does on first start with no policy.** ARCH
  says first-start bootstrap reads bootstrap-policy.nota and
  writes once. What if the file is malformed, missing, or
  later updated? Bootstrap-once is settled
  (`intent/component-shape.nota` 2026-05-19T01:30Z); but the
  policy reload through `owner-signal-persona-spirit::Reload`
  is operator-named.
- **Whether persona-spirit can run without persona-mind
  alive.** The "raw form first" principle says yes; spirit's
  ARCH shows `MindOwnerCallerActor` in the actor tree
  (/232 §9). If mind is unreachable, what does spirit do
  when an agent submits an intent that ought to forward?
  Implied answer: it doesn't forward, just stores. Never
  posed explicitly.

## 2 · persona-mind

### Settled by intent

- **Mind owns STATE.** `intent/persona.nota` 2026-05-18T12:08:41Z
  (Principle): mind owns work graph, memory, thoughts, durable
  policy truth, channel-grant authority decisions.
- **Mind is owned by spirit.** `intent/persona.nota`
  2026-05-19T15:30Z. (For implementation, see §"Unsettled.")
- **Channel choreography family splits into multiple verbs.**
  `intent/component-shape.nota` 2026-05-19T20:30Z: Grant /
  Extend / Revoke / List / Deny (names TBD). signal-persona-mind
  ARCH §MUST IMPLEMENT matches this guidance.
- **BEADS is transitional; persona-mind is the destination.**
  Workspace `INTENT.md` §"BEADS is transitional…" Manifested
  from across the intent log; mind ARCH §6 mirrors this with
  "work graph is the typed replacement for BEADS."
- **`Mutate` flows down-tree from mind.** mind ARCH §6.6
  applies `intent/component-shape.nota` 2026-05-18T22:13:54Z
  + 2026-05-19T01:25:00Z (Mutate as authority, configuration
  is Mutate).
- **Three-layer model and Tap/Untap mandatory.**
  `intent/component-shape.nota` 2026-05-20T02:00Z. ARCH MUST
  IMPLEMENT section reflects this.

### Settled by agent design (no psyche backing)

- **`MindRoot` actor topology**: `IngressPhase`,
  `DispatchPhase`, `DomainPhase`, `StoreSupervisor` →
  (`StoreKernel`, `MemoryStore`, `GraphStore`), `ViewPhase`,
  `SubscriptionSupervisor`, `ChoreographyAdjudicator`,
  `ReplyShaper`. All implementation choices.
- **The Subscription split into `SubscriptionManager` +
  `StreamingReplyHandler` + `SubscriptionDeltaPublisher`** is
  agent-design (ARCH §3). The push-shape principle is
  psyche-backed but the three-actor decomposition isn't.
- **`Thought`/`Relation` typed graph schema and relation
  validation rules** (Authored / Supersedes endpoint rules,
  cross-kind supersession rejection): agent-design.
- **`StoreKernel` runs on a dedicated OS thread via
  `spawn_in_thread()`** following kameo Template 2: agent-design
  from `skills/kameo.md`.
- **The `MindEnvelope` shape** (Infrastructure-supplied caller
  identity + one `MindRequest`): agent-design from
  ESSENCE §"Infrastructure mints identity."
- **40+ constraint witness tests** (ARCH §10): agent-design.

### Unsettled / open

- **`owner-signal-persona-mind` does not exist as a repo.**
  `intent/component-shape.nota` 2026-05-19T20:30Z marks this as
  intentional and unscoped — *"let them emerge as each
  component's owner discipline crystallizes."* When does it
  emerge? No criterion. Spirit-to-mind owner authority cannot
  begin without it.
- **`ChoreographyAdjudicator` actor — destination shape only.**
  Mind ARCH §3 calls this "destination"; today's dispatch
  returns `MindReply::MindRequestUnimplemented(NotInPrototypeScope)`
  for choreography variants. The destination is psyche-backed
  in shape (mind is choreography decider) but the
  `ChoreographyPolicy` content is wholly open.
- **Subscription consumer-driven demand (`SubscriptionDemand(n)`).**
  ARCH §3 "Destination" describes consumer-driven backpressure;
  not yet implemented. No psyche intent on the demand shape;
  agent-derived from `skills/push-not-pull.md` and
  `skills/subscription-lifecycle.md`.

### Implicit gaps

- **Mind's intent-awareness from spirit — concrete shape.**
  /232 §8 says: *"mind gains intent-awareness from spirit as
  a starting point; specifics flesh out as both components
  build."* What records mind learns from spirit, how mind uses
  them in choreography decisions or work-graph guidance,
  whether intent records are first-class `Thought`s in the
  graph or a parallel layer — all unposed.
- **Mind's owner contract receives orders from spirit how.**
  Once `owner-signal-persona-mind` exists, who else can issue
  on it besides spirit? Persona-daemon (lifecycle)? Designer-
  picked: probably yes for `Start`/`Stop`/`Reload`. Never
  posed.
- **The `memory_graph` snapshot table coexistence with
  typed `Thought`/`Relation` graph.** ARCH §4 has both. Is
  `memory_graph` transitional? Destination has just thoughts/
  relations + items/notes/edges? The destination diagram
  doesn't include `memory_graph`. Implicit cleanup.

## 3 · persona-orchestrate

### Settled by intent

- **persona-orchestrate is a real triad component, not folded
  into mind.** `intent/persona.nota` 2026-05-18T12:23:18Z
  (Decision).
- **State-vs-machinery split.** Same file 2026-05-18T12:08:41Z
  (Principle): mind owns state, orchestrate owns machinery
  (role claims, activity log, agent-run lifecycle, spawn plans,
  scope-acquisition, executor capacity, scheduling, escalation,
  lane registry).
- **MVP shape: dynamic roles by name, harness-as-typed-field,
  emulate the shell helper.** `intent/persona.nota`
  2026-05-19T15:04:19Z (4 separate Decisions).
- **Role creation creates report-lane, lock-acquisition records,
  local repository/index wiring.** Same date (Decision).
- **Repository-index management is part of orchestrate scope.**
  Same date (Decision).
- **Sub-scope handoff is forbidden.**
  `intent/component-shape.nota` 2026-05-19T01:20:00Z
  (Constraint).
- **Move from raw MVP to usable component with constraint
  tests passing.** `intent/persona.nota` 2026-05-19T18:35:00Z
  (Decision).
- **Lane registry is data, not enum variants.** `intent/persona.nota`
  + /233 §2.9 (psyche affirmed).
- **Triad split — daemon + CLI + ordinary + owner contracts.**
  `intent/persona.nota` 2026-05-19T15:04:19Z (Clarification).
- **Three-layer model + Tap/Untap mandatory.**
  `intent/component-shape.nota` 2026-05-20T02:00Z.
  signal-persona-orchestrate ARCH and owner-signal-persona-orchestrate
  ARCH match.

### Settled by agent design (no psyche backing)

- **Specific verb set on `owner-signal-persona-orchestrate`**:
  Currently `Create / Retire / Refresh`. Destination expansion
  named in persona-orchestrate ARCH §4 (agent-runs, scope
  acquisition, scheduling, supervision policy, escalation,
  subscriptions) — all agent-design.
- **Closed enum `HarnessKind { Codex, Claude }` for MVP.**
  intent says "just these two, that's all I'm using right
  now" (intent/persona.nota 2026-05-19T15:04:19Z) — Codex and
  Claude. Whether expansion is by `HarnessKind` variant
  addition or by data-table conversion mirrors the
  RoleName-vs-LaneRegistry transition; intent only sketches
  the closed-enum vs data direction generically, not
  per-axis.
- **Lock-file projection from daemon state.** Agent-design;
  intent says lock files retire eventually and the daemon is
  destination authority (`intent/persona.nota` 2026-05-19T15:04:19Z).
- **The orchestrate's specific `claims/activities/roles/repositories`
  table schema.** Agent-design.
- **`ActivitySubmission` slot field.** /233 §7 settled — slot
  is exposed for subscription catch-up. Agent-derived from
  push-not-pull.

### Unsettled / open

- **Mind→orchestrate authority chain end-to-end.** Mind-side
  caller for `owner-signal-persona-orchestrate` doesn't exist
  (`persona-orchestrate/ARCHITECTURE.md` and /233 §8.9). When
  does it? Intent silent.
- **Working tables not yet implemented**: `agent_runs`,
  `spawn_plans`, `agent_executors`, `scope_acquisitions`,
  `channel_grants`, `escalation_state`. All called out as
  "missing" in orchestrate ARCH §5. No intent prioritizes
  ordering.
- **Daemon as workspace service (systemd-supervised) — cutover
  point.** persona-orchestrate ARCH says `tools/orchestrate`
  remains live "until the operator chooses the cutover point."
  Intent silent on the cutover criterion.
- **`bootstrap-policy.nota` content for orchestrate.** Spirit's
  bootstrap is psyche-named (sacred teachings). Orchestrate's
  bootstrap-policy.nota exists but content is operator-shaped:
  what lanes/scheduling-policies/supervision-policies seed?
  Intent has nothing specific.

### Implicit gaps

- **Concept designer's lane creation interface to
  orchestrate.** /234 names concept designer as an upstream
  role that decides when a new design lane spawns. Today's
  orchestrate has `Create(CreateRoleOrder)` — does concept
  designer call this directly? Through what authority? The
  /234 fleshing-out is open; the integration with orchestrate
  is implied.
- **Role-record retirement vs delete vs archive.** intent
  says "we're loosening roles right now"
  (`intent/workspace.nota` 2026-05-19T21:45Z); orchestrate
  has `Retire(RetireRoleOrder)`. What does retiring DO —
  archive, hide, soft-delete? Agent's call. Not framed by
  intent.
- **The lane-vs-role distinction.** Intent treats them
  interchangeably; orchestrate has `RoleIdentifier` /
  `RoleName` (data model) and `lane_registry` (table name).
  Whether a role is a lane is implicit by overlap.

## 4 · persona-router

### Settled by intent

- **Mind decides; router enforces** for channel choreography.
  Workspace mind/router design (persona/ARCHITECTURE.md §1.6.3).
  Backed by `intent/component-shape.nota` Mutate-as-authority
  records (2026-05-18T22:13:54Z, 2026-05-19T01:25:00Z).
- **Subscribe-not-poll for observation.**
  Workspace-wide principle; intent across
  `intent/component-shape.nota` and
  `intent/workspace.nota`. `skills/push-not-pull.md`
  enforces.

### Settled by agent design (no psyche backing)

- **Authorized-channel state model** (`Channel` record:
  source/destination/kinds/duration/granted_by/status):
  persona/ARCH §1.6.3 + router ARCH §2. Agent design,
  growing from the message-routing problem.
- **`ChannelEndpoint = Internal(ComponentName) |
  External(ConnectionClass)` projection.** Agent design.
- **8 structural channels pre-installed at engine setup.**
  persona/ARCH §1.6.3. Agent-chosen list.
- **`OneShot / Permanent / TimeBound` channel durations.**
  Agent design.
- **`MessageOrigin::Internal/External` stamping at message
  daemon and router boundary.** Agent design.
- **`RouterRuntime` Kameo actor tree** (`RouterRoot`,
  `HarnessRegistry`, `ChannelAuthority`,
  `MindAdjudicationOutbox`, `HarnessDelivery`,
  `RouterObservationPlane`): agent design.

### Unsettled / open

- **`owner-signal-persona-router` does not exist.**
  Listed as intentionally missing (`intent/component-shape.nota`
  2026-05-19T20:30Z). When does it emerge? No criterion.
  Orchestrate→router authority chain (channel-grant orders
  flowing from orchestrate to router) waits on this.
- **Router GC policy.** ARCH §2 says GC is "future
  development" with no design. Intent silent.
- **Multi-engine routes.** ARCH §1.6.5 calls out
  cross-engine traffic deferred. Intent silent about whether
  multi-engine federation is in scope for today's persona.

### Implicit gaps

- **`MessageOrigin` records inside `signal-persona-auth`.**
  Auth records are designer-shaped (no signal-persona-auth
  has an INTENT.md; psyche has never stated the trust model
  beyond "filesystem-ACL trust" being one paragraph in
  persona/ARCH §1.6.1). Whether the SO_PEERCRED → ConnectionClass
  mapping is psyche-validated or designer-chosen is unposed.
- **Channel kinds enumeration**
  (`ChannelMessageKind::MessageIngressSubmission` /
  `DirectMessage` / etc.). Agent design with no intent
  citation.
- **What rejects a message besides "channel inactive."** Today
  the only typed rejection is unknown-channel→adjudicate.
  Future rejection reasons (rate limits, kind mismatch,
  authority revoked) — no design surface.

## 5 · persona-harness

### Settled by intent

- **Harnesses are first-class durable runtime objects** — implicit
  in workspace INTENT.md "Persona is the durable agent."
- **`HarnessKind` is closed**: `Codex, Claude, Pi, Fixture`.
  Intent has a partial backing: `intent/persona.nota`
  2026-05-19T15:04:19Z says "harness type, Codex or Claude.
  For now, just these two, that's all I'm using right now"
  — but Pi and Fixture are agent-added.

### Settled by agent design (no psyche backing)

- **`HarnessKind` closed-enum-with-Fixture-variant.**
  Pi and Fixture are agent-added. Workspace intent generally
  prefers data-over-enums (lane registry, role names), so
  this is in tension with workspace direction.
- **Transcript subscription five-state lifecycle** with
  `TranscriptSubscriptionManager` / `TranscriptStreamingReplyHandler`
  / `TranscriptDeltaPublisher`: agent design from
  `skills/subscription-lifecycle.md`.
- **`HarnessIdentityView { Full | Redacted | Hidden }`** read-path
  projections: agent design.
- **`--kind <codex|claude|pi|fixture>` argv path.** This is
  the ONLY known workspace component that takes a typed argv
  flag (`--kind`) besides the single NOTA argument. Intent
  is clear (component-shape.nota
  2026-05-19T01:23:00Z): the single argument rule forbids
  flags. The harness daemon defends this by taking `--kind`
  as a flag NOT covered by the rule — by treating it as a
  separate identity field — but the single argument rule has
  no carve-out. Probable violation. Operator may need to fix.

### Unsettled / open

- **`owner-signal-persona-harness` does not exist.**
  Same intentional-missing as above
  (`intent/component-shape.nota` 2026-05-19T20:30Z).
- **`Lifecycle::Paused` semantics.** ARCH §1.5 has Paused as
  a closed-enum variant. What pauses a harness? Who can pause
  it? No intent.
- **Transcript fanout to mind/router observers.**
  ARCH says "typed observations + sequence pointers" but the
  observer→consumer subscription not implemented per /246
  Tap/Untap pattern.

### Implicit gaps

- **The `Fixture` variant.** Tests use `Fixture` for
  not-real harnesses. Workspace intent doesn't address
  test-only enum variants; this is in tension with
  "spelling every identifier as a full English word"
  (workspace ESSENCE §"Naming") because `Fixture` is fine
  but the closed enum has a special test variant — implicit
  schema decision.
- **What happens to a harness whose process dies.** Implicit:
  `HarnessLifecycle::Stopped` with exit-code distinction.
  Restart policy? Intent silent.
- **Bulk lifecycle queries.** ARCH has `HarnessStatusQuery`
  per-harness; nothing for "list all live harnesses."
  Implied to come from orchestrate side via lane registry.

## 6 · persona-message

### Settled by intent

- **There is a `persona-message` boundary component** — implicit
  in workspace ecosystem ARCH; psyche says (somewhere in
  general persona conversations) that user submission is a
  separate ingress. Less direct intent backing than other
  components.
- **Single-NOTA-argument rule** — intent/component-shape.nota
  2026-05-19T01:23:00Z. Message daemon takes one
  `MessageDaemonConfiguration` record per argv via `nota-config`.

### Settled by agent design (no psyche backing)

- **`message.sock` (mode 0660, group-writable) vs internal
  sockets (mode 0600).** Agent design from filesystem-ACL
  trust model.
- **`MessageOriginStamper`'s role**: stamping
  `MessageSubmission → StampedMessageSubmission` with origin,
  ingress time, and owner-identity at the message daemon.
- **`MessageDaemonRoot` actor topology**: agent design.
- **Stateless across CLI requests**: agent design from
  message-daemon being a forwarding ingress, not a state
  owner.
- **The CLI takes NOTA `Send` or `Inbox` records.** Agent
  design (verb names, payload shapes).

### Unsettled / open

- **`owner-signal-persona-message` does not exist.** Intentionally
  missing per `intent/component-shape.nota` 2026-05-19T20:30Z.
- **Future inbox-on-mind-side migration.** persona/ARCH §5
  mentions `OwnerApprovalInbox` lives in mind. Today's
  message component has no inbox state. The transition path
  is intent-silent.

### Implicit gaps

- **Multi-operation request execution**. ARCH §4 invariant:
  *"current message ingress path is deliberately one
  operation per request. Multi-operation request execution
  belongs in the shared Signal runtime slice, not in this
  component's ad hoc codec."* The "shared Signal runtime
  slice" is implicit but no intent has been recorded on
  whether the message component will get multi-op atomic
  support or remain one-op-per-request.
- **External (non-Owner) message submission.** ARCH says
  `External(Owner)` is the production path. What about
  `External(NonOwnerUser)`, `External(OtherPersona)`,
  `External(Network)` — these are typed but is the message
  daemon meant to ever serve them? Implicit answer probably
  "yes for federation; not now"; never posed.

## 7 · persona-terminal

### Settled by intent

- **Terminal-cell is library, not component daemon
  boundary.** Implicit in psyche statements about consolidating
  the terminal supervision. Workspace decisions in early
  reports settled (predating today's intent log) that the
  consolidation happens.
- **One communication socket + one supervision socket per
  component** (component-triad invariant pair): owner +
  ordinary. Backed by `intent/component-shape.nota`
  2026-05-18T22:13:54Z (no permission-signal middle tier;
  there are exactly two authority contracts).
- **Single argument rule.** Workspace-wide intent.

### Settled by agent design (no psyche backing)

- **`PromptPattern` lock-and-cache injection mechanism**
  (persona/ARCH §5.1): replaces the originally-proposed
  router-side join. Agent design; some psyche backing in
  related sessions about "prompt cleanliness."
- **`Clean | Dirty | NotChecked` prompt state.** Agent
  design.
- **Default `Dirty → defer`; clean-then-inject deferred.**
  Agent design.
- **Communication/data plane split** (terminal-cell's
  `control.sock` + `data.sock`; persona-terminal's
  communication socket + raw viewer bytes routed
  separately): Agent design — matches the
  `skills/component-triad.md` §"Data-plane bytes that cannot
  afford Signal framing" carve-out.
- **Component Sema tables**: `delivery_attempts`,
  `terminal_events`, `viewer_attachments`, `session_health`,
  `session_archive`. Agent design.
- **`owner-signal-persona-terminal` shipped with
  `CreateSession` and `RetireSession`.** Agent-design that
  follows the component-triad. /233 §4 names this in the
  authority chain; intent is consistent.

### Unsettled / open

- **Clean-then-inject for dirty prompts.** ARCH §0.7 +
  §1.5 says clean-then-inject "is deferred — multi-line and
  history-search prompts misbehave." When does it land?
  Intent silent.
- **Viewer adapter selection policy.** ARCH names
  "viewer adapter mode is explicit" but doesn't say WHICH
  adapter ships first. Operator-territory.
- **Owner-only session lifecycle authorization beyond
  filesystem ACL.** persona/ARCH §1.6.4 says "owner socket
  may accept a Mutate order; non-owner socket … does not
  know that Mutate variant." Settled in the typed-contract
  sense; the runtime Unix-permission boundary is a future
  hardening step (psyche-acknowledged in
  `intent/persona.nota` 2026-05-19T15:04:19Z Clarification).

### Implicit gaps

- **Subscription consumer-driven demand**. Terminal subscriptions
  exist per /signal-persona-terminal MUST IMPLEMENT but
  flow-control between cell→supervisor→subscriber is implicit.
- **What persona-terminal does on terminal-cell child crash.**
  Cell ownership of child process + lifecycle FSM but the
  termination semantic propagation to the harness/router/mind
  side isn't intent-backed.
- **The "transitional binaries" lifecycle.** ARCH calls
  `persona-terminal-supervisor` and the one-PTY
  `persona-terminal-daemon` transitional. When does the
  consolidation finish? No intent.

## 8 · persona-auth (signal-persona-auth — types only, no daemon)

### Settled by intent

- **There is no permission-signal middle tier.**
  `intent/component-shape.nota` 2026-05-18T22:13:54Z
  (Correction): exactly two authority contracts per
  component (`signal-<component>` ordinary,
  `owner-signal-<component>` owner-only).
- **Filesystem-ACL trust + dedicated user**: implicit in the
  filesystem-ACL paragraph in persona/ARCH §1.6.1.
  Psyche-engagement on auth specifically has been limited
  primarily to "auth/security/identity infrastructure lives
  in the auth/security ecosystem as a new sibling to
  ClaviFaber" (persona/ARCH constraint, §"Constraints"
  bullet about persona vs criome scope).

### Settled by agent design (no psyche backing)

- **`MessageOrigin / ConnectionClass / IngressContext /
  OwnerIdentity / ComponentName / EngineId / RouteId /
  ChannelId` records.** All agent-designed.
- **SO_PEERCRED → ConnectionClass mapping.** Agent design
  from filesystem-ACL trust.
- **Closed enum class system** (Owner |
  NonOwnerUser(Uid) | System | OtherPersona | Network).
  Agent design.
- **The decision to put auth as a types-only contract crate
  (no daemon).** Agent-derived from the principle that auth
  is provenance, not a process boundary.

### Unsettled / open

- **`owner-signal-persona-auth` does not exist.**
  Intentionally missing per `intent/component-shape.nota`
  2026-05-19T20:30Z. Auth is types-only — does it ever
  acquire an owner contract? Probably not; signal-persona-auth
  has no daemon to own. But the missing-by-design rule
  applies to "5 missing owner-signal-* repos" enumerated;
  signal-persona-auth doesn't have a runtime, so the
  emergence rule is implicit-N/A.
- **`OtherPersona`/`Network` SO_PEERCRED interpretation.**
  Federation is deferred; mapping unposed.

### Implicit gaps

- **Why no `Identifier` newtype but instead
  `EngineId`/`RouteId`/`ChannelId`.** Workspace intent says
  spell out `Identifier` not `Id`
  (`intent/naming.nota` 2026-05-19T18:20:00Z); these auth
  identifiers use `Id` suffix. Possible violation. Has the
  psyche reviewed these names?
- **Whether `OwnerIdentity` should be elevated to a typed
  capability or stay as provenance.** Currently provenance;
  no intent on capability progression.

## 9 · persona-system

### Settled by intent

- **OS-boundary observations are push, not poll.**
  Workspace-wide; `skills/push-not-pull.md` enforces.
- **`signal-persona-system` is the contract; persona-system
  consumes it.** Backed by component-triad pattern.

### Settled by agent design (no psyche backing)

- **persona-system is paused.** Mentioned in persona/ARCH §0.7:
  *"FocusTracker is real, plan is deferred."* Pause is
  agent-decision; replaced router-side join with terminal-cell
  lock-and-cache. Intent silent on the pause/unpause condition.
- **`FocusTracker` Kameo actor.** Real and tested, but no
  intent on the focus-tracker as the destination shape.
- **`SystemPrivilegedRequest::ForceFocus / SuppressDrift`
  (deferred).** Agent design.
- **Naming reopens on unpause** (the `ForceFocus` negative
  naming): agent design.
- **All 5 round-trip-witness constraints**: agent design.

### Unsettled / open

- **Unpause criteria.** Listed (window-focus notifications,
  multi-engine UI, multi-monitor layout) but all
  designer-stated. Psyche has never named the conditions.
- **Whether `signal-persona-system` ever gets an owner
  contract.** Same intentional-missing per
  2026-05-19T20:30Z.

### Implicit gaps

- **persona-system's ARCH says "force-focus's naming is
  reopened" — what's the new name?** Implicit re-design.
- **Multi-OS port.** ARCH mentions "later OS ports beyond
  Niri" but only Niri is implemented. No intent on cross-OS
  scope.

## 10 · persona-introspect

### Settled by intent

- **Universal observer-hook mechanism on the daemon's
  normal (ordinary) socket.** `intent/component-shape.nota`
  2026-05-19T20:00Z (Decision): introspection sees both
  public-layer operations AND Sema-effect-layer operations;
  introspect consumes all contract crates; subscribing
  to the hook is done on the daemon's normal (public)
  socket, not the owner socket.
- **Push-subscription model (Subscribe, not poll).**
  Workspace-wide push-not-pull.
- **Component-specific introspection records may split into
  `signal-persona-<X>-introspect` when heavy/high-churn.**
  persona/ARCH §0.6 — agent statement, supports an emerging
  pattern, partial intent backing from triad logic.

### Settled by agent design (no psyche backing)

- **Per-peer client actors** (`ManagerClient`, `RouterClient`,
  `TerminalClient`) in persona-introspect's ARCH §1+§3: agent
  design.
- **Specific Match queries (`RouterRequest::Summary` etc.)**:
  agent design from /246 hold direction.
- **`DeliveryTraceKey` as introspection-domain state.**
  Agent design; explicitly carved out from Signal frames.
- **`introspect.redb` storing query/reply/error audit trail
  + subscription registrations + delivery trace cache.**
  Agent design.

### Unsettled / open

- **Tap/Untap mandatory observability vs the universal
  observer-hook intent statement (Gap #4 in TL;DR).**
  These two surfaces may coexist or may be the same thing.
  The /246-v4 introduces `Tap`/`Untap` macro-injected verbs
  as mandatory on every persona component's ordinary contract.
  The earlier psyche intent (2026-05-19T20:00Z) named a
  "universal observer hook" on the daemon's normal socket —
  is `Tap`/`Untap` the implementation of that universal
  hook? Or is it a different mechanism? Designer-asserted as
  consistent; never directly posed.
- **What persona-introspect IS** beyond being the consumer:
  is it a "supervised first-stack component"
  (persona/ARCH §0.6 says so) or a passive observer
  (its own ARCH says it's "not in the message delivery
  path")? Both. The "not in delivery path / yes in
  supervision set" framing is agent-stated, no intent.
- **Subscription delivery semantics through
  `Engine::subscribe`**: gated on sema-engine's per-peer
  commit-then-emit semantics. No intent on the timeline.

### Implicit gaps

- **persona-introspect's relation to spirit-as-apex.**
  Spirit is the cognitive apex; introspect observes
  everything. Does introspect observe spirit itself
  (via `Tap` on signal-persona-spirit)? Yes by mechanism;
  intent silent on whether observation of the apex is
  symmetric with observation of subordinate components.
- **Cross-component delivery-trace correlation.**
  `DeliveryTraceKey` joins router/harness/terminal
  observations for the same delivery. Agent design;
  multi-component correlation is a foundational pattern
  but unnamed in intent.

## 11 · persona (top-level engine manager)

### Settled by intent

- **There is a Persona ecosystem.** Workspace `INTENT.md` /
  ESSENCE.md §"Persona is meta-AI; spirit animates."
- **One Persona daemon supervises multiple engines.**
  Persona/ARCH §1.5 — agent-design, but the multi-engine
  model is implicit in the durable-agent psyche framing.
- **Auth/security/identity is not in persona.**
  Persona/ARCH §"Constraints": auth lives in criome-family
  ecosystem (ClaviFaber, future eventual-Criome). This
  matches workspace `INTENT.md` §"BEADS is transitional…"
  context and various criome intent records elsewhere.

### Settled by agent design (no psyche backing)

- **The entire 1513-line `persona/ARCHITECTURE.md`** is
  almost wholly agent-designed. Key surfaces:
  - **Engine manager model**: one `persona-daemon`, one
    `persona` system user, one `manager.redb`, per-engine
    state/run trees.
  - **Manager event log + two snapshot reducers**:
    engine-lifecycle + engine-status with reducer-on-append
    semantics. Lazy reducer + eager rebuild on
    `ManagerStore::open`.
  - **`SpawnEnvelope` typed wire form** (engine_id /
    component_kind / component_name / state_dir /
    socket paths / socket modes / peer_sockets /
    manager_socket / supervision_protocol_version).
  - **`ResolvedComponentLaunch` manager-internal record**.
  - **`DirectProcessLauncher` + `EngineSupervisor` actor
    boundary**. Process supervision behind a Kameo actor
    rather than direct in request handlers.
  - **Child-exit observation as push** via
    `ExitNotifier` + watcher tasks.
  - **Orphan detection on manager restart**.
  - **Bounded reachability probe carve-out** from
    push-not-pull.
  - **Sandbox runner** (`persona-engine-sandbox`),
    bwrap profile, systemd-run sandboxing.
  - **`message-router` minimal topology** for current
    Signal refactor witnesses.
  - **The split between `persona-daemon` (engine-manager
    binary) and `persona` (thin CLI)**.
  - **Multi-engine upgrade substrate** (engine-level
    upgrade replaces component-level hot-swap).
- **`ComponentKind` closed enum**: Mind / Orchestrate /
  Router / Message / System / Harness / Terminal /
  Introspect. Agent-designed; spirit absent.
- **Pre-installed structural channels (8 of them).**
  Agent design.
- **`prototype-supervised` component set vs production
  set.** Agent design.

### Unsettled / open

- **persona meta-repo has no INTENT.md** (Gap #3 in
  TL;DR). The 1513-line ARCH carries no psyche-intent
  grounding for engine-manager mechanics. This is the
  largest single intent gap in the persona ecosystem by
  surface area.
- **`persona-spirit` not yet a `ComponentKind` variant.**
  Spirit's authority graph (workspace `INTENT.md` and /232
  §2) places it as cognitive apex; persona/ARCH does not
  yet wire spirit into the engine-manager component
  catalog. Implicit: spirit becomes a `ComponentKind`
  variant. Never posed.
- **persona meta-repo's `signal-persona` is two relations
  (engine-catalog + supervision).** Whether persona's
  contract should grow more relations (e.g. an
  `owner-signal-persona` for privileged manager operations)
  has not surfaced in intent.
- **Sandbox runner's evolution path.** Today's runner
  works for dev/test; production hosts use systemd. No
  intent on when the dev sandbox retires.

### Implicit gaps

- **persona-daemon is NOT enumerated in workspace ESSENCE
  or workspace INTENT.** The engine manager isn't named
  in the workspace's most-load-bearing surfaces; only the
  Component-triad and per-component intents are.
- **What runs persona-daemon.** Production: systemd module.
  Today: ad-hoc `nix run`. Migration path between them is
  agent-territory.
- **The `MessageProxy` retirement.** ARCH calls out that
  the `MessageProxy` name retires from variant/socket/binary/env-var.
  Agent-naming pass; was this psyche-named or
  agent-decided?

## 12 · Engine design overall (cross-component)

### Settled by intent

- **Spirit spawns last.** `intent/persona.nota`
  2026-05-19T14:00 (Decision).
- **Spirit is the cognitive apex; supervisor is higher
  infrastructure permission only.** Same record.
- **Authority graph `spirit → mind → orchestrate →
  router/harness/...`** Same record; spirit's intent on
  mind's owner. `intent/persona.nota` 2026-05-19T15:30Z
  affirms spirit owns mind.
- **Each component is a real triad (daemon + thin CLI +
  ordinary + owner contracts).**
  `intent/component-shape.nota` 2026-05-18T22:15:57Z
  (Constraint).
- **State taxonomy: policy + working state per component**
  in one sema-engine DB. 2026-05-19T01:30:00Z (Decision).
- **Mutate is the authority verb** (top-down). Cross-cutting.
  2026-05-18T22:13:54Z + 2026-05-19T01:25:00Z (Configuration
  is a Mutate).
- **Sub-scope handoff forbidden.** 2026-05-19T01:20:00Z.
- **Single argument rule for every component binary.**
  2026-05-19T01:23:00Z.
- **Three-layer model: Contract Operation / Component
  Command / Sema Operation.** 2026-05-20T02:00:00Z
  (Decision). Backed by 246-v4 spec.
- **`Tap`/`Untap` mandatory for persona components.**
  2026-05-20T02:00:00Z (Decision).
- **Backward compatibility is not a constraint.**
  ESSENCE.
- **The 5 missing `owner-signal-persona-*` repos are
  intentional.** 2026-05-19T20:30:00Z (Clarification).
- **No-`Unknown`-variant rule, polling-shape escape hatch
  forbidden.** Workspace-wide.
- **Components ship in raw form first; integration after.**
  `intent/persona.nota` 2026-05-19T15:30Z (Principle).
- **Universal observer-hook on ordinary socket.**
  2026-05-19T20:00Z. Sub-cases: observation is not
  security-sensitive; subscription is on the public
  socket, not owner.

### Settled by agent design (no psyche backing)

- **Concrete spawn order beyond "spirit last."** /232 §6
  gives an order; nothing between supervisor and spirit
  is psyche-cited. Designer-derived from "spawn what you
  depend on first." (Gap #10 in TL;DR.)
- **What "the supervisor" IS in the authority graph.**
  Is it persona-daemon? Is it `EngineSupervisor` actor inside
  persona-daemon? Is it both? Designer-asserted as the
  engine-manager binary running as the dedicated `persona`
  system user. Never directly resolved by psyche.
  (Gap #2 in TL;DR.)
- **`SupervisionRequest` relation as part of every persona
  component.** Implicit at design level — persona/ARCH §1.7
  + signal-persona ARCH "Supervision relation". Every
  daemon answers `SupervisionRequest::ComponentHello`,
  `ComponentReadinessQuery`, `ComponentHealthQuery`.
  Universal shape; psyche has not stated it.
- **The "skeleton honesty" contract.** signal-persona/ARCH:
  "every supervised daemon decodes every variant of
  `SupervisionOperation` … the three prototype variants
  — Announce, Query, Stop — are what makes a process a
  Persona component. A daemon that replies Unimplemented
  to any of those three fails the prototype readiness
  witness." Agent-designed but well-codified.
- **`Tap`/`Untap` as THE universal observer-hook
  implementation.** Whether /246-v4's `Tap`/`Untap` IS
  the universal-observer-hook intent (2026-05-19T20:00Z)
  is agent-asserted consistent. (Gap #4 in TL;DR.)
- **Subscribe-fanout three-actor split (`SubscriptionManager`
  / `StreamingReplyHandler` / `SubscriptionDeltaPublisher`).**
  Universal pattern. `skills/subscription-lifecycle.md`
  enforces it.
- **Pre-installed structural channels at engine setup.**
  persona/ARCH §1.6.3 + router ARCH. Eight channels
  written into router redb with `GrantSource::EngineSetup`.
- **Two distinct sockets per component: domain
  (ordinary) + supervision. Plus owner-signal-* gives a
  third socket when present.** Agent design.

### Unsettled / open

- **The 5 missing owner-signal-* repos' emergence rules.**
  Gap #9 in TL;DR. `intent/component-shape.nota`
  2026-05-19T20:30Z accepts the missing-by-design but
  gives no criterion. Each component's owner discipline
  is supposed to "crystallise"; what crystallisation
  looks like has never been described.
- **Mutate ordering / atomicity across components.**
  Mutate is the authority verb; sub-Mutates flow down
  through orchestrate to router/harness. What if a
  Mutate to router succeeds but the downstream Mutate
  to harness fails? Per `skills/component-triad.md`
  §"Authority chain": "the issuer transitions its own
  state from possibly-mutated to now-mutated on the
  confirmation, and only then proceeds." Partial-failure
  rollback semantics are agent-derived; intent silent.
- **Cross-component Sema-class observation
  end-to-end.** Per intent (2026-05-19T20:00Z),
  introspect should be able to observe Sema-effect
  layer too. The three-layer model says Sema classes
  are payloadless. How does the observer reconstruct
  the underlying data when it sees an `Assert`-class?
  Through the component event? Implicit.
- **Bootstrap-policy pattern across components.**
  Spirit has psyche-named bootstrap content (sacred
  teachings). Orchestrate has agent-shaped bootstrap.
  Every other component has bootstrap-policy.nota
  by triad invariant #5 (2026-05-19T01:30:00Z). The
  pattern is intent-backed; the content per component
  is agent-territory except spirit.
- **What "the persona-daemon" name implies.**
  In persona/ARCH the engine manager is named
  persona-daemon; "supervisor" is sometimes synonym,
  sometimes the `EngineSupervisor` actor inside it.
  Naming-discipline asks for full English words and
  no ambiguity. Agent-tolerated.

### Implicit gaps

- **Engine boundary vs persona-daemon boundary.**
  persona-daemon supervises multiple engines (engine_a,
  engine_b); each engine has its own component
  federation. Whether spirit-per-engine or
  spirit-shared-across-engines is an open implicit gap.
  Workspace intent says "spirit is the apex"; one
  spirit-per-engine seems implied; never posed.
- **Cross-engine federation.** persona/ARCH §1.6.5 says
  multi-engine routes are deferred. Whether the broader
  federation lives in persona at all or in the
  criome-family ecosystem is unsettled. Persona/ARCH
  §"Eventual cross-domain federation" treats it as
  future work.
- **Concept designer's relationship to spawn order.**
  /234 says concept designer is "an entry point" for
  new concepts that can spawn new lanes. Does concept
  designer-spawned lanes plug into the spawn order?
  Where does the dynamic lane's daemon (if any) sit
  in the boot sequence? Implicit; the dynamic-role
  intent (`intent/persona.nota` 2026-05-19T15:04:19Z)
  covers role identity, not daemon-lifecycle.
- **Skeleton honesty for owner-signal contracts.**
  Skeleton honesty (signal-persona/ARCH "every
  supervised daemon decodes every variant of
  `SupervisionOperation`") only mentions the
  supervision relation. Does skeleton honesty extend
  to ordinary signal-persona-* contracts? To
  owner-signal-* contracts? Agent-implicit yes for
  all three layers (return typed `Unimplemented` for
  unbuilt-but-decodable variants). Never directly
  stated in intent.
- **What happens when persona-mind crashes.** Orphan
  detection (persona/ARCH manager restore) handles
  mid-spawn-sequence crashes. What about a running
  persona-mind crashing and being restarted — does
  spirit's owner-Mutate to mind retry? Does
  orchestrate? Implicit answer probably yes; never
  posed.
- **Whether spirit observes its own state through
  introspect.** Recursive observation question. Implicit
  answer: yes via Tap; intent silent.

## 13 · Prioritized gap list

Severity legend: **High** blocks current implementation or
contradicts existing intent; **Medium** affects upcoming
Phase-3 refactors; **Low** is a design clarity issue.

| # | Gap | Severity | Component(s) | Where it surfaces |
|---|---|---|---|---|
| 1 | Spirit-to-mind owner-contract verb set is open | High | spirit, mind | spirit ARCH "Status", /232 §8 |
| 2 | Owner-graph apex disambiguation (supervisor identity) | High | spirit, persona, all | /232 §2, persona/ARCH §1.7 |
| 3 | persona meta-repo has no INTENT.md | High | persona | persona/ARCH (whole) |
| 4 | persona-introspect universal observer-hook vs `Tap`/`Untap` consistency | High | introspect, all persona components | /246-v4 §2 vs `intent/component-shape.nota` 2026-05-19T20:00Z |
| 5 | persona engine-manager triad-status undefined | High | persona | persona/ARCH (whole) |
| 6 | persona-system unpause criteria | Medium | system | persona/ARCH §0.7 |
| 7 | `HarnessKind` closed-enum vs data-table tension | Medium | harness | harness/ARCH §1, workspace `INTENT.md` data-not-enum pattern |
| 8 | Spirit guardian / multi-agent auditing arc undefined | Medium | spirit | `intent/persona.nota` 2026-05-19T15:30+17:30Z |
| 9 | 5 missing owner-signal-* repos emergence criteria | Medium | mind, router, harness, message, system | `intent/component-shape.nota` 2026-05-19T20:30Z |
| 10 | Spawn order beyond "spirit last" | Medium | persona, all | /232 §6, persona/ARCH (silent) |
| 11 | Mutate-chain partial-failure semantics | Medium | mind, orchestrate, router, harness | skills/component-triad.md §"Authority chain" |
| 12 | Skeleton honesty for ordinary + owner contracts | Medium | every persona daemon | signal-persona/ARCH "Skeleton honesty" |
| 13 | Single-argument-rule violation in harness `--kind` flag | Medium | harness | harness/ARCH §1.5 + `intent/component-shape.nota` 2026-05-19T01:23Z |
| 14 | Concept designer's relationship to spawn order / engine catalog | Medium | persona, orchestrate | /234, /232 |
| 15 | Mind→orchestrate concrete authority handoff missing | Medium | mind, orchestrate | /233 §8.9, orchestrate ARCH §"Owner Wire Surface" |
| 16 | `bootstrap-policy.nota` content per component (except spirit) | Medium | orchestrate, others | ARCH files of each component |
| 17 | Filesystem-projection cutover (spirit's intent log → spirit-mediated) | Medium | spirit | /232 §7 |
| 18 | Cross-component observer correlation via `DeliveryTraceKey` | Medium | introspect, all | introspect/ARCH §1 |
| 19 | Engine-per-spirit vs shared spirit across engines | Medium | persona, spirit | persona/ARCH §1.5, spirit/ARCH §"Authority" |
| 20 | Cross-engine federation scope (in persona vs criome ecosystem) | Medium | persona | persona/ARCH §1.6.5 + §"Eventual cross-domain federation" |
| 21 | `Statement` payload canonical example | Low | spirit | signal-persona-spirit/ARCH §"Contract Surface" |
| 22 | `ChannelMessageKind` enumeration | Low | router | persona/ARCH §1.6.3 |
| 23 | Channel duration `OneShot / Permanent / TimeBound` rationale | Low | mind, router | persona/ARCH §1.6.3 |
| 24 | Component restart policy after process crash | Low | persona, all | persona/ARCH §"Manager state" |
| 25 | Subscription consumer-driven demand specifics | Low | mind, router, harness | persona-mind/ARCH §3, others |
| 26 | `MessageProxy` retirement naming | Low | message, persona | persona/ARCH (renaming) |
| 27 | `Fixture` `HarnessKind` variant for tests | Low | harness | harness/ARCH §1 |
| 28 | Auth identifier naming (`EngineId` vs `Identifier`) | Low | auth | signal-persona-auth/ARCH + naming.nota |
| 29 | `memory_graph` transitional vs typed thoughts/relations destination | Low | mind | mind/ARCH §4 |
| 30 | Recursive observation (spirit observing itself via Tap) | Low | spirit, introspect | implicit |
| 31 | Multi-OS port for persona-system | Low | system | system/ARCH §1 |
| 32 | Cell-vs-supervisor consolidation completion (terminal) | Low | terminal | terminal/ARCH §2 |
| 33 | What rejects a router message besides "channel inactive" | Low | router | implicit |
| 34 | External (non-Owner) message submission paths | Low | message | message/ARCH §1 |
| 35 | Multi-operation request execution per component | Low | all | implicit / partial in persona-message ARCH |

**Cross-cutting patterns:**

- **The engine manager is the largest agent-design surface
  with the least intent backing.** persona/ARCH is 1513
  lines without an INTENT.md.
- **Owner-signal-* contracts cluster in the "intentionally
  missing" bucket without crystallisation criteria.** Five
  components in this state.
- **Push-subscription protocol implementations are agent-
  derived from `skills/push-not-pull.md` and
  `skills/subscription-lifecycle.md`.** Universal-looking
  three-actor pattern; psyche has not directly stated this
  pattern.
- **`Tap`/`Untap` and the universal observer-hook
  potentially-but-unverifiably equate.** This deserves a
  direct psyche clarification before the next round of
  observability implementation.
- **The supervisor's identity in the cognitive authority
  chain is ambiguous** — persona-daemon, EngineSupervisor
  actor, or both — and this ambiguity persists across
  spirit/ARCH, persona/ARCH, mind/ARCH.
- **The intent log has dense coverage where the psyche
  has personally engaged** (cognitive layer, intent
  records, three-layer model, contract-local verbs) and
  thin coverage where the psyche has not engaged
  (infrastructure mechanics, engine-manager state model,
  persona-introspect specifics, persona-system pause).
  The asymmetry is structurally inevitable but invites
  drift; surfaces with no intent backing acquire
  agent-cultivated assumptions that solidify into
  workspace direction unmoored from psyche statement.

## 14 · References

### Primary intent sources

- `/home/li/primary/intent/persona.nota`
- `/home/li/primary/intent/workspace.nota`
- `/home/li/primary/intent/component-shape.nota`
- `/home/li/primary/intent/naming.nota`
- `/home/li/primary/INTENT.md`
- `/home/li/primary/ESSENCE.md`

### Workspace skills

- `/home/li/primary/skills/component-triad.md`
- `/home/li/primary/skills/contract-repo.md`
- `/home/li/primary/skills/naming.md`
- `/home/li/primary/skills/push-not-pull.md`
- `/home/li/primary/skills/subscription-lifecycle.md`

### Designer reports

- `/home/li/primary/reports/designer/232-persona-spirit-new-component.md`
- `/home/li/primary/reports/designer/233-persona-orchestrate-operator-handoff.md`
- `/home/li/primary/reports/designer/234-concept-designer-role.md`
- `/home/li/primary/reports/designer/247-radical-rethink-or-converge.md`

### Component ARCH (per persona component)

- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-spirit/INTENT.md`
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-orchestrate/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-orchestrate/INTENT.md`
- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-harness/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-terminal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-introspect/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/persona-system/ARCHITECTURE.md`

### Contract ARCH (per signal-*)

- `/git/github.com/LiGoldragon/signal-persona/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/owner-signal-persona-spirit/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-mind/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-orchestrate/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/owner-signal-persona-orchestrate/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-router/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-harness/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-message/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-terminal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/owner-signal-persona-terminal/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-system/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-introspect/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/signal-persona-auth/ARCHITECTURE.md`
