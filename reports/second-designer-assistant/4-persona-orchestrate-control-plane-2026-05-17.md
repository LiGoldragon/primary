# Persona-orchestrate as a control plane — revised position

*Devil's-advocate research after report 3 said "no new component."
This report disagrees with report 3 and recommends a
`persona-orchestrate` component (and `signal-persona-orchestrate`
contract) for orchestration machinery — distinct from the
orchestration records persona-mind owns. The split is conceptual at
minimum; deployment-level co-residence vs. separate process is a
second-order decision worth deferring.*

Date: 2026-05-17

Author: second-designer-assistant

---

## TL;DR

Report 3 was right that signal-persona-mind already defines the
*records* of orchestration (`RoleClaim`, `RoleRelease`,
`RoleHandoff`, `RoleObservation`, `ActivitySubmission`). Report 3
was wrong to conclude that this collapses orchestration into mind.

The records are the **persistent outcome** of orchestration. The
**machinery** that produces those outcomes — conflict resolution,
agent spawning across harnesses, the supervision FSM for
running agents, dead-agent detection, escalation on blocked work,
scheduling across the upcoming raw-LLM-API executor — does not exist
anywhere in the workspace today. `tools/orchestrate` writes lock
files; that is its sole machinery. `persona-mind` is "central
workspace state… role claims, handoffs, activity, work items,
notes, dependencies, decisions, aliases, event history, ready/blocked
views" (per its ARCHITECTURE.md §0). `persona-harness` operates one
rung below agent scheduling — it models a harness's runtime FSM
but doesn't decide which work it gets. The gap is real.

The user's framing — *persona-mind delegates orchestration the way
Kameo hides mailbox lifecycle from actor user-code* — maps cleanly
onto the supervisor pattern that every mature actor system encodes:
**runtime/supervisor is conceptually distinct from state/work, even
when co-resident**. Erlang/OTP, Akka, and Hewitt's original actor
model all draw this line. Process-level distinctions (Kubernetes
scheduler vs. etcd, Mesos master vs. frameworks, Omega's pluralised
schedulers) are scale arguments that don't apply at workspace size,
but the conceptual line applies regardless of scale.

**Recommendation:**

1. `signal-persona-orchestrate` is its own contract repo. It defines
   orchestration-machinery verbs (spawning, supervision, scheduling,
   escalation, lifecycle events) — orthogonal to signal-persona-mind's
   record verbs.
2. `persona-orchestrate` is the daemon that implements the machinery.
   It subscribes to mind events for new work and writes orchestration
   outcomes back via existing signal-persona-mind requests.
3. Whether `persona-orchestrate` runs as a separate OS process or
   co-resides with `persona-mind` is a deployment decision. The
   evidence from similar small-scale systems (Erlang/OTP, Akka,
   Nomad) suggests co-resident-first, peel-apart-if-needed.
4. Report 2's Rust rewrite of `tools/orchestrate` stays sensible as
   the bridge — but reframed: it's a thin signal-persona-mind client
   for *persistence*, and the orchestration-machinery scope is now
   `persona-orchestrate`'s, not the rewrite's.

This report supersedes report 3 §"Recommendation." Report 3's
evidence (signal-persona-mind already has the records) remains
correct; report 3's interpretation (therefore no new component) was
wrong.

---

## The argument

### Records ≠ machinery

`signal-persona-mind`'s role verbs are *persistence primitives*. Each
records a fact:

- `RoleClaim` — "this agent claimed this scope at this time, for this
  reason."
- `RoleRelease` — "this agent released this scope."
- `RoleHandoff` — "this agent passed this work to that agent."
- `RoleObservation` — "show me current role state."
- `ActivitySubmission` — "record this activity event."

None of these decide *whether* a claim should be granted. None of
them detect *that* an agent has died and needs reclamation. None of
them allocate work to an available agent. None of them spawn a
process. None of them watch for blocked work and escalate. None of
them coordinate two pending claims on overlapping scopes.

Those are the **machinery questions**. `tools/orchestrate` (shell)
answers a narrow subset of them today — claim-conflict detection via
path-nesting/task-token-exact-match — by reading and writing flat
lock files. That's the entire machinery surface in the workspace
right now. The shell helper's design is good enough for one workspace
with eleven idle/active lanes and zero automated agent spawning. As
soon as the workspace grows automated spawning, dead-agent recovery,
or the planned raw-LLM-API executor, the shell's surface is
inadequate.

### The Kameo analogy holds — at the conceptual level

The user's framing pointed at Kameo: "an actor library user...
doesn't need to be preoccupied with all of this mailbox handling and
actor spawning and spawn down, mailbox stare down, message queuing,
dead actor notification…"

This is the **supervisor pattern**, normalised by every mature actor
system since Erlang/OTP. Hewitt's original actor model gives actors
three primitives (send, create, designate) and *nothing about
supervision*. Supervision is a runtime concern. The OTP docs are
explicit: "*a child process does not need to know anything about its
supervisor… it is instead only the supervisor which hosts the child
who must know which of its children are significant ones*" (OTP
Supervisor Principles).

Translating to our case: persona-mind is the "child" in the analogy
— it knows what state it owns, it answers requests, it doesn't need
to know about agent-lifecycle. A supervisor-shaped component
(persona-orchestrate) holds the lifecycle knowledge and the scheduling
logic. They communicate through typed channels (signal contracts),
the same way OTP processes communicate through messages.

The Kameo refactor pressure the user named is the *implementation
challenge* of getting this right — the existing teardown race
documented in `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
§"P2" shows that supervised resource-owning actors race shutdown
ordering. That's a Kameo runtime correctness issue, not an argument
for or against the architecture. If anything, it argues that
encapsulating supervision discipline in *one* place (persona-orchestrate)
is better than scattering it across every component that needs to
spawn agents.

### What "the workspace doesn't have this gap" would mean

If orchestrate-as-mind-slice were sufficient, you'd expect:

- An actor inside `MindRoot` for agent scheduling. There isn't one
  (per the daemon's topology — `IngressPhase`, `DispatchPhase`,
  `DomainPhase`, `StoreSupervisor`, `ViewPhase`,
  `SubscriptionSupervisor`, `ChoreographyAdjudicator`,
  `ReplyShaper` — all are request-side or state-side actors, none
  spawn external processes).
- Lifecycle records for spawned agents in signal-persona-mind. There
  aren't — the record vocabulary is roles and activity, not agent
  process lifecycle.
- Design reports or skills documenting the scheduling rule (which
  agent gets the next ready BEADS task, by what policy). There
  aren't.

These absences confirm the gap. The workspace currently relies on
*humans* invoking `tools/orchestrate claim`. When the workspace wants
*automated* orchestration (spawn an agent for this ready bead;
recover a dead agent; route work to the right executor), the
machinery has to land somewhere. The Persona ecosystem's micro-component
pattern says: a new capability is a new component.

---

## Similar-systems evidence

(From the parallel research stream that examined Kubernetes, Borg,
Omega, Mesos, Nomad, Erlang/OTP, Akka, systemd, and the Hewitt
actor model.)

### When systems split state from scheduling

- **Kubernetes** — `kube-scheduler` is a separate binary from
  `kube-apiserver` and from `etcd`. It watches the API server for
  unscheduled Pods, picks a node, writes the binding back. Other
  controllers follow the same pattern. The split is defended on
  horizontal scalability and independent component evolution.
- **Borg → Omega** — Borg unified state + scheduler in the cell
  master; Omega (Schwarzkopf et al., EuroSys 2013) refactored to
  shared state + multiple parallel schedulers using optimistic
  concurrency, explicitly because monolithic scheduling "restricts
  feature velocity and decreases utilization."
- **Mesos** — two-level scheduling: master allocates resources,
  frameworks schedule work onto allocated resources. Master is
  intentionally thin.

These split because of **scale, heterogeneity, and independent
failure** — drivers our workspace (one user, ~10 agents max, one
discipline) doesn't have.

### When systems unify

- **Nomad** — server holds Raft-replicated state *and* runs the
  scheduler, in-tier. Trades K8s-style component separation for
  operational simplicity at smaller scale.
- **systemd / launchd** — init is the supervisor and the state
  store. Process-level unification because there's only one
  supervisor on a machine and the bootstrap problem forbids
  dependencies.
- **Erlang/OTP, Akka** — supervisor and worker are different
  *abstractions*, but live in the same OS process. Conceptual
  split, OS-process unified.
- **Hewitt actor model** — runtime is conceptually distinct from
  actor user-code, regardless of how it's implemented.

The pattern is consistent: **process-level split is a scale
argument; conceptual split is universal**. Even Erlang and Akka,
which run everything in one VM, insist on the supervisor-vs-worker
distinction at the abstraction level.

### The mapping

Workspace persona ecosystem (one node, ~10 agents, single
discipline) is in the **conceptual-split, unified-process-OK**
regime. The right shape is Erlang/OTP-shaped: persona-mind and
persona-orchestrate are different abstractions with different
contracts, and could happily live in one OS process (or two), with
the deployment decision deferrable.

This matches Nomad's pragmatism: split when you must, otherwise
keep it operationally simple.

---

## The contract — what signal-persona-orchestrate covers

`signal-persona-mind` keeps its existing role-record verbs
unchanged. `signal-persona-orchestrate` is a new contract that
defines the orchestration-machinery vocabulary. Proposed shape (the
final design lands in a designer or designer-assistant report —
this is the directional sketch):

**Requests the orchestrator accepts:**

- `(SpawnAgent <lane> <work-item> <executor-kind>)` — start an agent
  in a lane, working on a specific item, using harness / raw-LLM /
  fixture executor.
- `(AcquireScope <lane> <scope> <reason>)` — request a claim;
  orchestrator resolves conflicts and dispatches the underlying
  mind `RoleClaim` request on success.
- `(ReleaseScope <lane> <scope>)` — symmetric to acquire; dispatches
  underlying `RoleRelease`.
- `(SuperviseAgent <lane> <supervision-policy>)` — register a
  restart policy for an agent.
- `(EscalateBlockedWork <lane> <work-item> <reason>)` — surface a
  blocker to the user / human escalation.

**Replies:**

- `(AgentSpawned <lane> <agent-id>)`, `(AgentSpawnFailed <reason>)`
- `(ScopeAcquired <lane> <scope>)`, `(ScopeRejected <lane> <conflict-detail>)`
- `(ScopeReleased <lane> <scope>)`
- `(SupervisionAck <lane>)`
- `(EscalationAck <lane> <escalation-id>)`

**Subscribed events the orchestrator emits (push, never pulled):**

- `AgentLifecycle` — `Starting | Running | Paused | Stopped | Failed | Timed-out`
- `ScopeContested` — two pending claims race; orchestrator's resolution.
- `WorkReady` — a BEADS task / mind work-item transitions to ready.
- `Escalation` — a blocked-work situation needs human attention.

**Subscribed events the orchestrator consumes (from mind, push):**

- Mind's existing `RoleClaim` / `RoleRelease` deltas (already
  emitted via mind's subscription primitives).
- Mind's work-item state changes.

The orchestrator never queries mind on a clock; it subscribes.
Mind's record verbs are how the orchestrator *persists* its
decisions; mind's subscription primitives are how the orchestrator
*observes* state changes.

This split keeps the workspace's `push-not-pull.md` discipline
intact across the orchestrator boundary, and it gives each component
exactly one responsibility per `skills/micro-components.md`.

---

## Deployment shape — start co-resident, defer the split

The conceptual split is settled. The deployment question is:

- **Option A — separate process.** `persona-orchestrate` is its own
  daemon, talks to `persona-mind` over Unix socket. Independent
  failure, independent restart, K8s-flavored. Costs: more daemons
  to operate, a bootstrap dependency.
- **Option B — co-resident actor.** `persona-orchestrate` is a
  separate Kameo actor tree, but lives inside the same OS process
  as `MindRoot`. Erlang/OTP-flavored. Costs: shared failure
  domain (orchestrator crashes take mind with them, or vice
  versa).
- **Option C — separate crate, embedded library.** `persona-orchestrate`
  is a Rust crate that exposes an API; persona-mind links it.
  Costs: tight coupling at the build level, no clear contract
  boundary, harder to peel out later.

My recommendation: **start with option B (co-resident actor),
contracted by `signal-persona-orchestrate`**. The reasoning:

1. The contract boundary is the load-bearing distinction. Once
   `signal-persona-orchestrate` exists, the implementation can move
   between processes without touching consumers.
2. At workspace scale, two daemons-on-one-node is operational
   overhead without payoff. Nomad's stance: simpler is better
   until simpler stops working.
3. The Kameo correctness work (per `reports/operator-assistant/138`)
   is in flight. Spawning supervised actors across process
   boundaries is harder than within one VM. Start in-VM.

If `persona-orchestrate` grows enough to warrant independent
failure / restart (e.g., the raw-LLM-API executor brings real-time
constraints that shouldn't be co-scheduled with mind's transactions),
peel it out as option A. The contract surface stays the same.

---

## What this means for adjacent work

### Report 2 — Rust rewrite of tools/orchestrate

Report 2 framed the rewrite as inventing a new `orchestrate-cli`
crate with its own typed Nota request/reply vocabulary. That
specific framing is wrong in two ways:

1. The vocabulary `orchestrate-cli` would invent for claim/release/
   status is *just* the persistence layer — those records already
   exist in `signal-persona-mind`. The rewrite should import and
   use them directly.
2. The orchestration *machinery* (which report 2 partly waved at)
   is `persona-orchestrate`'s scope, not the rewrite's.

The rewrite stays as the bridge — small, focused, scope-cut. It:

- Imports `signal-persona-mind` for `RoleClaim` / `RoleRelease` /
  `RoleObservation` records.
- Writes lock files at `orchestrate/<lane>.lock` (preserved
  format) as a *side effect* until `persona-mind` is the canonical
  store.
- Has no its own contract crate, no new typed vocabulary.
- Eventually becomes a thin wrapper over `mind '<NOTA>'` when
  `persona-mind` is the canonical store and persona-orchestrate
  handles automated agent flows.

Report 2 should be revised in place (per the user's earlier choice)
to reflect this scope cut. The bead `primary-68cb` description
needs a parallel update.

### The raw-LLM-API component (forward-looking)

The user named this component: a non-harness path for specialized
LLM calls (faster, less resource-intensive than full harness
invocations). It doesn't exist yet, no design report mentions it.

Once it lands, it's an *executor kind* in `persona-orchestrate`'s
SpawnAgent verb: `(SpawnAgent <lane> <work-item> RawLlm)` alongside
`(SpawnAgent <lane> <work-item> Harness)`. The orchestrator picks
the executor; the executor runs the work. This is the Mesos pattern
in miniature: orchestrator allocates work to executors; executors
own their own runtime.

This is a strong argument *for* persona-orchestrate existing as a
contract: the multi-executor pattern is exactly where a thin shared
scheduler beats per-executor scheduling. Without persona-orchestrate,
each executor (harness, raw-LLM, future others) would invent its own
work-selection logic, repeated.

### persona-mind's scope

This report doesn't propose narrowing persona-mind. The existing
role/activity/work-graph records stay where they are. Mind's job is
"central workspace state"; that's still right. What's narrowed is
the *interpretation* of that scope — mind owns the persistence of
orchestration decisions, not the *making* of them.

---

## Open questions

1. **Spawning protocol.** Persona-orchestrate spawning a harness or
   a raw-LLM agent is the new mechanism. Does it spawn via Unix
   sockets to existing persona-harness daemons (push a message
   saying "start a Codex session for this lane"), or does it
   spawn OS processes directly? Probably the former, but the
   contract needs design.
2. **Identity of "an agent."** Today, each agent is a human-driven
   Codex/Claude Code session. Automated orchestration introduces
   *non-human-attended* agents. Does the existing
   role-coordination protocol (one lock file per lane) hold, or
   do automated agents get a different identity discipline?
3. **Backpressure.** If persona-orchestrate is observing mind via
   subscription and pushing to executors, and the executors are
   slower than the work-stream, what's the discipline? Per
   `push-not-pull.md` §"Named carve-outs", backpressure-aware
   pacing is allowed — but the specific shape needs design.
4. **Authorisation.** Once orchestration is automated, who can
   say "spawn an agent that has authority to commit to repo X"?
   The Criome quorum-signature direction in `ESSENCE.md`
   §"Today and eventually" points at the eventual answer; the
   near-term answer is probably "the user's signature on the
   spawn request."

These all belong in a designer-led design report on
persona-orchestrate's actual contract shape — not in this
research report's recommendation, which is the *should it exist*
question, not the *what shape exactly* question.

---

## What I propose next

1. **This report lands** (done by the time you read this).
2. **Revise report 2 in place** — narrow the scope to "Rust rewrite
   as thin signal-persona-mind client, lock-file side effect, no
   new vocabulary." Mark the orchestration-machinery scope as
   `persona-orchestrate`'s, citing this report.
3. **Update bead `primary-68cb`** description to match the revised
   report 2 scope.
4. **File a new bead under `role:designer`** for the
   persona-orchestrate contract design: "design
   signal-persona-orchestrate + persona-orchestrate component."
   This is designer-scoped work (architecture decisions, typed
   contract design). The operator-flavored implementation bead
   comes later, after designer's report lands.

---

## See also

- this workspace's
  `reports/second-designer-assistant/3-persona-orchestrate-research-2026-05-17.md`
  — the prior conclusion this report partially supersedes.
- this workspace's
  `reports/second-designer-assistant/2-orchestrate-rust-rewrite-design-2026-05-17.md`
  — the design report whose §"End-state design" needs revision per
  this report's recommendation.
- this workspace's `orchestrate/AGENTS.md` §"Command-line mind target"
  — the existing destination this report refines.
- this workspace's `skills/kameo.md` §"Blocking-plane templates"
  Template 2 — the supervised-resource-owning actor discipline that
  grounds the Kameo analogy.
- this workspace's `skills/actor-systems.md` §"Release before notify"
  — the discipline the orchestration-machinery component would
  embody for agent lifecycle.
- this workspace's `skills/push-not-pull.md` — the discipline
  governing how persona-orchestrate subscribes to mind and emits
  events to executors.
- this workspace's `skills/micro-components.md` — one capability,
  one crate, one repo; the principle this report applies to argue
  for persona-orchestrate's existence.
- this workspace's
  `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
  §"P2" — the Kameo supervised-resource teardown race the user
  invoked.
- `/git/github.com/LiGoldragon/persona-mind/ARCHITECTURE.md` — the
  central-state daemon's owned scope (and what it doesn't own).
- `/git/github.com/LiGoldragon/persona-harness/ARCHITECTURE.md` —
  the harness lifecycle FSM (one rung below agent scheduling).
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:418-580,1756-1760`
  — the existing role-record vocabulary that persona-orchestrate
  consumes for persistence.
- Schwarzkopf et al., "Omega: flexible, scalable schedulers for
  large compute clusters," EuroSys 2013
  (https://research.google/pubs/omega-flexible-scalable-schedulers-for-large-compute-clusters/)
  — the canonical paper on splitting state from scheduling at
  scale.
- Erlang OTP Supervisor Principles
  (https://www.erlang.org/doc/system/sup_princ.html) — the
  supervisor-vs-worker conceptual split that holds at workspace
  scale.
- Mesos two-level scheduling architecture
  (https://mesos.apache.org/documentation/latest/architecture/)
  — the multi-executor pattern that becomes relevant once
  raw-LLM-API joins persona-harness as a second executor.
- Nomad architecture
  (https://developer.hashicorp.com/nomad/docs/concepts/architecture)
  — the co-resident-but-conceptually-split deployment shape this
  report recommends as the starting point.
