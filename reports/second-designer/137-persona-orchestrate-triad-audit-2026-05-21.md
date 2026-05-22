# 137 — persona-orchestrate triad audit (2026-05-21)

*Audit of the `persona-orchestrate` triad: `signal-persona-orchestrate`
(working) + `owner-signal-persona-orchestrate` (policy) +
`persona-orchestrate` (daemon + thin CLI). The triad is structurally
present and partially migrated, but its contract still encodes
lock-file semantics — the very target shape the workspace has
explicitly rejected. The owner contract is too thin to carry the
policy-programmability surface mind is supposed to use, and the
daemon is not on `signal-executor`. Six new findings beyond the
universal /257 patterns.*

## 0 · TL;DR

State summary:

- **Lock-file semantics in the contract.** Working signal carries
  `Claim`, `Release`, `Handoff`, `Observe` (of role claims), `Submit`
  (of activity), `Query` (of activity), `Watch`/`Unwatch` of
  observation. This is `tools/orchestrate`'s lock-helper vocabulary
  lifted into typed wire form. Per `reports/operator/150` §6.8 and
  `intent/persona.nota` 2026-05-19T15:04Z (*"raw MVP emulates the
  shell helper"*) and 2026-05-20T17:30Z (mind/orchestrate boundary)
  the end-state surface is agent-registry / abstract-job /
  context-compaction / policy-programmability — none of which appear.
- **Owner surface is three orders deep.** `Create`, `Retire`,
  `Refresh`. Carries no orchestration-policy programmability per
  `intent/persona.nota` 2026-05-20T17:30Z (*"the mind would be able
  to program new things — when this type of job comes in, run such
  and such sequence of agent type assignments"*). The policy
  surface that makes mind→orchestrate authority load-bearing is
  absent.
- **Daemon does not use `signal-executor`.** No
  `signal-executor` in `Cargo.toml`. No `Lowering` / `CommandExecutor`
  / `ToSemaOperation` / `ToSemaOutcome` impls. `OperationLowering`
  (`persona-orchestrate/src/lowering.rs:25`) is a hand-rolled
  Sema-tag derivation that returns the `signal-sema::SemaOperation`
  class directly per request — bypassing the three-layer model
  affirmed `intent/component-shape.nota` 2026-05-20T02:00Z.
- **No `observable` block** on either channel. Per
  `intent/persona.nota` 2026-05-21T10:00Z (*"debug the debugger"*)
  every persona component is observable; orchestrate isn't.
  Hand-rolled `ObservationSubscription` / `ObservationToken` /
  `OperationReceived` / `EffectEmitted` records exist in the contract
  (signal-persona-orchestrate/src/lib.rs:702-805) but as a
  domain-shaped subscription, not the mandatory macro-injected
  `Tap`/`Untap` surface.
- **`bootstrap-policy.nota` missing.** `skills/component-triad.md`
  §"5. Policy state and working state" mandates first-start seed
  from this file. `ARCHITECTURE.md` line 199 names it; the file does
  not exist on disk. The daemon has no policy-bootstrap path
  (no first-start table check, no one-shot seed insert).
- **Ancestry prefixes inside the contract.** `RoleIdentifier`,
  `RoleName`, `RoleClaim`, `RoleRelease`, `RoleHandoff`,
  `RoleObservation`, `RoleSnapshot`, `RoleStatus`. The crate IS the
  role-coordination domain; `Role*` is restated ancestry per
  ESSENCE §Naming.
- **Lock-file projection in the daemon** (`lock_projection.rs`,
  `daemon.rs` invokes `project_locks()` after every accepted
  mutation). Per `intent/persona.nota` 2026-05-19T15:04Z, lock-file
  emulation is acceptable as a transitional projection — but the
  authority shape is still that the contract is the projection's
  schema, not orchestration's true vocabulary.

**Verdict.** The persona-orchestrate triad is *triad-shaped but
identity-confused*: the structural triad invariants are met
(daemon + two contracts; one socket per surface; one redb opened
by the daemon), but the contracts and runtime are organised around
the transitional lock-helper, not around the destination intent of
abstract-job dispatch / agent registry / policy programmability /
context compaction. It has the spirit of `tools/orchestrate`
wrapped in Signal frames, when the substance of `persona-mind`'s
body-organ should be inside.

**Recommended next slice headline**: a designer redesign of the
signal tree to express the destination intent (abstract-job
submission, agent-registry observation, policy programmability on
owner) BEFORE the operator-side `signal-executor` migration —
because migrating the current contract onto signal-executor would
ossify the lock-helper shape. Details in §4.

## 1 · /257 findings status

Status of /257's five universal patterns against this triad:

### /257 §1.1 — Old universal-verb shape (`Assert / Match / ...`)

**Status: FIXED.** Both contracts use contract-local verbs in
verb form. Working: `Claim`, `Release`, `Handoff`, `Observe`,
`Submit`, `Query`, `Watch`, `Unwatch`. Owner: `Create`, `Retire`,
`Refresh`. No `Assert`/`Match`/`Subscribe`/`Mutate`/`Retract`
prefixes on operations. ✓

### /257 §1.4 — Repeated-suffix smell

**Status: PARTIALLY CLEAN, one smell remaining.** No
`*Submission`/`*Query`/`*Listing` suffix repetition on operations.
However, the reply enum (`signal-persona-orchestrate/src/lib.rs:834`)
has ten flat variants:

```text
OrchestrateReply {
    ClaimAcceptance, ClaimRejection,
    ReleaseAcknowledgment,
    HandoffAcceptance, HandoffRejection,
    RoleSnapshot,
    ActivityAcknowledgment, ActivityList,
    ObservationOpened, ObservationClosed,
}
```

This is the same flat-reply smell /150 §3 ("Repeated suffixes lift
into typed sums") and operator/141 flagged on the request side.
The ten variants cluster into:

- Claim/Release/Handoff outcomes (acceptance/rejection pairs) —
  the `Outcome` shape, one variant per operation with
  `Outcome { Accepted, Rejected(...) }` sub-sums.
- Activity outcomes — `ActivityAcknowledgment`, `ActivityList`.
- Subscription outcomes — `ObservationOpened`, `ObservationClosed`.

Not catastrophic; smaller than mind's repeated-suffix problem.
But the flat shape doesn't structurally express that
`ClaimAcceptance`+`ClaimRejection` are the two outcomes of one
operation, not two independent reply kinds.

### /257 §1.5 — Ancestry prefixes

**Status: NOT FIXED.** The contract's domain is role
coordination; the crate name is `signal-persona-orchestrate`. Yet
the dominant prefix across types is `Role*`:

| Stale prefix | Cleaner form (use-site reads as `signal_persona_orchestrate::X`) |
|---|---|
| `RoleIdentifier` (line 77) | `Identifier`, or just keep `Role` as the noun and use `Role` (but then field accessors `claim.role: Role` are clean) |
| `RoleName` (line 79 alias) | retire — the new `Identifier`/`Role` covers it |
| `RoleClaim` (line 444) | `Claim` |
| `RoleRelease` (line 474) | `Release` |
| `RoleHandoff` (line 490) | `Handoff` |
| `RoleObservation` (line 567) | `Observation` (but this collides with the proposed observability — see §2.3 below) |
| `RoleSnapshot` (line 570) | `Snapshot` |
| `RoleStatus` (line 576) | `Status` (collides with proposed status verbs — context-dependent) |

Note the collision pressure: if the role-vocabulary types drop the
prefix AND the contract grows agent-registry types per /129
(`AgentName`, `AgentType`, `AgentDescription`, …), `RoleStatus` →
`Status` is fine but only because `Agent*` is the orthogonal axis.
This is exactly the case for the redesign in §2.1 — names will
sort themselves correctly once the right tree exists.

Also redundant: `HandoffRejectionReason` (line 512) — the parent
`HandoffRejection { from, to, reason: HandoffRejectionReason }`
already restates `Handoff`; the inner enum is just `RejectionReason`
inside `HandoffRejection`'s namespace. Same for
`RoleCreationRejectionReason` (owner/lib.rs:49) →
`RejectionReason` inside `RoleCreationRejected`.

### /257 §1.6 — `*RequestUnimplemented.operation` redundancy

**Status: NOT FIXED on owner; not present on working.** Working
contract has no `RequestUnimplemented` variant at all (every
operation has a real reply path). Owner contract has
`OwnerOrchestrateRequestUnimplemented { operation, reason }`
(owner/lib.rs:80-83). The `operation: OwnerOperationKind` field
is the redundancy /257 §1.6 calls out; positional reply alignment
already carries which operation the reply is for. Drop the field.

### /257 §1.10 — Frame type alias boilerplate

**Status: NOT FIXED on owner; not present on working.** Owner
contract has explicit aliases:

```rust
// owner-signal-persona-orchestrate/src/lib.rs:100-105
pub type OwnerOrchestrateRequest = OwnerOrchestrateOperation;
pub type Frame = OwnerOrchestrateFrame;
pub type FrameBody = OwnerOrchestrateFrameBody;
pub type ChannelRequest = OwnerOrchestrateChannelRequest;
pub type ChannelReply = OwnerOrchestrateChannelReply;
pub type RequestBuilder = OwnerOrchestrateRequestBuilder;
```

Working contract has only one alias
(`pub type OrchestrateRequest = OrchestrateOperation;` at line 857).
Once `signal-frame`'s clean-emit macro fix (bead `primary-77hh`,
per intent/component-shape.nota 2026-05-21T10:30Z) lands, the
emitted names are already unprefixed and this dance retires
entirely.

### /257 §1.11 — No `observable` block

**Status: NOT FIXED.** Neither `signal-persona-orchestrate` nor
`owner-signal-persona-orchestrate` declares an `observable` block.
Per `intent/persona.nota` 2026-05-21T10:00Z (*"debug the
debugger"*) every persona component is observable; orchestrate is
a persona component.

Confounding factor: the contract already has hand-rolled
observation records that look like the macro-emitted shape but
aren't:

```rust
// signal-persona-orchestrate/src/lib.rs:702-805
pub struct ObservationSubscription { … }      // domain Watch payload
pub struct ObservationToken(u64);              // domain Watch token
pub struct OperationReceived { operation: OperationKind }
pub struct EffectEmitted { observation: SemaObservation }
pub enum ObservationEvent { OperationReceived(…), EffectEmitted(…) }
```

These were authored to *look like* the standard observability
surface but are wired as the `Watch(ObservationSubscription)` /
`Unwatch(ObservationToken)` domain operation. The macro-injected
`Tap(ObserverFilter)`/`Untap(...)` per
`intent/component-shape.nota` 2026-05-20T02:00Z is the universal
introspection surface; the contract's domain `Watch`/`Unwatch` is
something else (role-observation subscription).

Designer call: the contract needs the macro-injected `Tap`/`Untap`
added via an `observable` block. The domain `Watch`/`Unwatch` is
separate; both can coexist (per /150 §6.8 spirit pattern). Today
the *names* are confused — the domain hand-rolled subscription is
using "ObservationReceived"/"EffectEmitted" record names that the
macro should own and emit. This is exactly the worst kind of
confusion: parallel surfaces, same vocabulary, only one of them
real.

### /257 §1.12 — single-field timestamps

**Status: NOT FIXED.** `TimestampNanos(u64)` (line 426). Used in
`Activity.stamped_at` and `StoredRepository.refreshed_at`. Per
`intent/persona.nota` 2026-05-20T18:44Z (*"fuck nanoseconds"*) and
the two-field date/time pattern landed in spirit. Open question
per /150 §8: runtime/protocol timestamps may legitimately stay
single-field; this is a designer judgment per-component, not a
forced split.

Designer lean: orchestrate activity records are human-shaped
event-log entries — same shape as spirit intent records, two-field
date+time. The `refreshed_at` on `StoredRepository` is a runtime
fact, single-field is fine.

## 2 · New findings specific to this triad

### 2.1 — Contract carries lock-helper vocabulary, not abstract-job vocabulary

This is the load-bearing finding.

The working signal's operation set is:

```text
Claim(RoleClaim)
Release(RoleRelease)
Handoff(RoleHandoff)
Observe(RoleObservation)
Submit(ActivitySubmission)
Query(ActivityQuery)
Watch(ObservationSubscription) opens ObservationStream
Unwatch(ObservationToken)
```

This is `tools/orchestrate`'s shell-helper vocabulary lifted into
typed wire form: who-holds-which-scope-claim, who-handed-off-to-
whom, what-activity-was-logged. Per
`intent/persona.nota` 2026-05-19T15:04Z this is the **explicit MVP
scope** (*"emulate sort of what the shell script does right now,
but changing the whole role topology to be dynamic"*). The MVP got
shipped.

But the destination contract per
`intent/persona.nota` 2026-05-20T17:30Z is something different:

- **Abstract-job submission**: *"we need this topic researched by
  such-and-such skill type agent"*; *"we need a new REST component
  developed to do X named Y"*. Submission shape per /129 sketch:
  `ResearchTopic { topic, skill_type, priority }`,
  `CreateComponent { component_name, behavior_description }`,
  `RefineDocument { path, refinement_intent }`.
- **Agent registry observation**: *"agents would have a name and
  a short description, a typed type-enum (designer/coding/research
  /system-specialist), and the orchestrator would have a table for
  all that"*. Per /129 §Q1 (designer-derived but psyche-touch):
  read surface for "give me all running agents" / "give me all
  agents of type X" / "give me agents I can reach via router".
- **Context-compaction**: *"orchestrate decides if context has to
  be compacted before reassignment"*. An operation to ask
  orchestrate to consider reassigning a running agent to a new job
  (compaction is an internal decision; the operation is "reassign
  to job Y", orchestrate decides whether to compact first).
- **Reuse-over-spawn allocation**: the operation that submits a
  job carries no agent reference; orchestrate decides whether to
  reuse a qualified running agent or spawn a new one. This is what
  makes the abstract-job shape load-bearing — it's the layer where
  reuse-vs-spawn becomes orchestrate's decision.

**None of these are in the contract.** The contract is at the
lock-helper layer (which-role-holds-which-scope-claim); the
destination is at the work-dispatch layer (what-work-needs-doing,
which-agents-are-running). They are different relations on the
typed schema.

**Per `reports/operator/150` §6.8 explicitly**:

> *"Orchestrate is a real component, not a role folded into mind.
> It owns coordination machinery. It should use the same triad
> structure and signal-executor path. Current architecture should
> avoid resurrecting lock-file semantics as its target model. Lock
> files are transitional workspace choreography, not the end-state
> orchestration engine."*

The current contract is exactly the resurrected lock-file
semantics. The transitional MVP intent is satisfied; the
destination shape has not started.

Two interpretations, both worth surfacing:

1. **The lock-helper layer is one *table* of the destination
   shape**, alongside agent-registry / abstract-job /
   policy-programmability tables. In that read, today's
   contract is one slice of the destination, missing the other
   slices.
2. **The lock-helper layer is *transitional only* and retires when
   abstract-job dispatch replaces it.** The destination contract
   doesn't have `Claim`/`Release`/`Handoff` at all — claim/release
   is what `tools/orchestrate` did; the orchestrate component
   doesn't think in scopes-and-claims, it thinks in jobs-and-agents.

The psyche statement that drives the answer is
2026-05-19T15:04Z's *"emulate sort of what the shell script does,
but changing the role topology to be dynamic"* — which leans
interpretation 1: lock-helper claim/release is preserved at the
table level, with dynamic roles. But there's no follow-up psyche
intent that pulls the abstract-job vocabulary into the same
contract, so interpretation 2 is possible.

**Psyche-touch item** (§4 question Q1).

### 2.2 — Owner contract does not carry the policy-programmability surface

`intent/persona.nota` 2026-05-20T17:30Z is the load-bearing
record:

> *"the persona mind would be also, because of the owner contract,
> be able to program new things. Like, oh, here's a new policy,
> which is when this type of job comes in, we need such and such
> sequence of agent type of agent, here's the first type of agent
> we need to run, here's the type of result that we need… if he
> says success, then this happens. If he says failure, then this
> happens."*

This is the **owner contract's load-bearing capability** —
orchestration policies are programmed into orchestrate by mind via
the owner channel. Without it, the mind→orchestrate authority
relationship reduces to "mind creates roles", which barely needs
an owner contract at all.

The current owner surface (`owner-signal-persona-orchestrate/src/lib.rs`):

```text
operation Create(CreateRoleOrder)            // role creation
operation Retire(RetireRoleOrder)            // role retirement
operation Refresh(RefreshRepositoryIndexOrder)  // local-repo rescan
```

What's missing for policy programmability:

- **`RegisterPolicy(OrchestrationPolicy)`** — install a new policy
  for some `JobClass`. Per /129 §N2 sketch (designer-derived,
  needs psyche read):

  ```nota
  (OrchestrationPolicy
    (JobClass NewComponent)
    (Sequence
      (Step (AgentType Infrastructure) (Goal "create repo")
            (SuccessCondition "structure exists") (OnFailure Halt))
      (Step (AgentType Auditor) (Goal "verify")
            (SuccessCondition "audit ok") (OnFailure RetryWith Infrastructure))
      (Step (AgentType Coding) (Goal "implement")
            (SuccessCondition "tests pass") (OnFailure Escalate))))
  ```

- **`RetirePolicy(PolicyIdentifier)`** — remove a previously
  installed policy.
- **`UpdatePolicy(OrchestrationPolicy)` or `ReplacePolicy(...)`** —
  superseded form.
- **`InspectPolicies(...)`** — owner-side read of installed
  policies (or this could be in the ordinary contract if peer
  inspection is OK).
- Possibly **`ConfigureAllocationDefaults`** — global tuning for
  reuse-vs-spawn lean, compaction threshold, escalation defaults.
  Per `intent/persona.nota` 2026-05-20T17:30Z, threshold is
  unspecified (*"a threshold of context where we compact. Or
  maybe it just compacts."*) — owner-policy is the natural place
  for it.

Today's owner surface treats role creation as the load-bearing
authority surface; per the psyche's mind/orchestrate boundary,
**role creation is a side effect of policy** (a policy expecting an
infrastructure-engineer agent results in that role existing), not
the primary authority verb.

Designer lean: `Create(CreateRoleOrder)` and
`Retire(RetireRoleOrder)` stay (they're load-bearing for the
dynamic-role MVP and the psyche named them explicitly
2026-05-19T15:04Z), but they're **joined** by policy verbs, not
replaced by them.

**Psyche-touch item** (§4 question Q2): is policy
programmability the right shape, and what are its concrete verbs?

### 2.3 — Daemon does not use `signal-executor`

Verified: `persona-orchestrate/Cargo.toml` has no `signal-executor`
dependency. The runtime path is:

```text
daemon.rs (socket accept)
  → service.rs (OrchestrateService::handle / handle_owner)
    → claim.rs / activity.rs / role.rs / repository.rs (per-operation)
```

`OperationLowering` (`persona-orchestrate/src/lowering.rs:25-50`)
is a static helper that, given an operation, returns a
`LoweredOperation<OperationKind> { kind, effects: Vec<SemaOperation> }`.
The daemon's `handle_ordinary_stream` /`handle_owner_stream`
(`daemon.rs:107-168`) calls `OperationLowering::ordinary` /
`OperationLowering::owner` and **discards the result**
(`let _lowered = …`). The Sema tag is computed and thrown away.

This is exactly the gap /258 §2.2 surfaced for `persona` (the
engine-manager): no `Lowering` impl, no `CommandExecutor` impl, no
`OperationPlan`, no `BatchPlan`. The daemon dispatches directly
over typed contract operations without the three-layer model.

The pattern that should apply per /150 §7 ("Migration playbook"):

```rust
// in persona-orchestrate/src
pub enum Command {
    InsertClaim(StoredClaim),
    RetractClaim(ClaimKey),
    RecordActivity(...),
    InsertRole(StoredRole),
    RetireRole(RoleIdentifier),
    // …
}

pub enum Effect {
    ClaimInserted(...),
    ClaimRetracted(...),
    ActivityRecorded(...),
    RoleInserted(...),
    // …
}

impl ToSemaOperation for Command { … }
impl ToSemaOutcome for Effect { … }
impl Lowering for OrchestrateLowering {
    type Operation = OrchestrateOperation;
    type Reply = OrchestrateReply;
    type Command = Command;
    type ComponentEffect = Effect;
    fn lower(...) -> Result<OperationPlan<Command>, OrchestrateReply> { … }
    fn reply_from_effects(...) -> OrchestrateReply { … }
}

impl CommandExecutor for OrchestrateCommandExecutor { … }
impl BatchErrorClassification for OrchestrateError { … }
```

This work has **two prerequisites that should run first**:

1. The redesign per §2.1 / §2.2 — if the destination contract
   isn't lock-helper-shaped, migrating today's lock-helper-shaped
   daemon onto signal-executor ossifies the wrong shape.
2. The bootstrap-policy.nota work per §2.4 — `OrchestrateService`
   today seeds workspace roles in `RoleRegistry::seed_current_
   workspace_roles()` (role.rs:19-33). With policy state, that
   seeding moves to bootstrap-once-from-file per
   skills/component-triad.md §5.

After both, the executor migration is mechanically the same as
spirit's per /150 §5.

### 2.4 — `bootstrap-policy.nota` missing and policy-state shape unclear

`persona-orchestrate/ARCHITECTURE.md` line 199 explicitly names
`bootstrap-policy.nota` as the first-start policy seed:

> *"The first-start policy seed is `bootstrap-policy.nota`. Once
> policy has bootstrapped into sema state, owner-signal is the
> mutation path."*

The file does not exist in the repo. Verified:

```text
/git/github.com/LiGoldragon/persona-orchestrate/
  AGENTS.md  ARCHITECTURE.md  Cargo.toml  flake.nix  INTENT.md
  README.md  skills.md  src/  tests/
  # no bootstrap-policy.nota
```

Per `skills/component-triad.md` §5 ("Policy state and working
state"), the absence of this file is a triad invariant failure:
*"The first-start policy seed is `bootstrap-policy.nota`. The
daemon reads this file exactly once — on first start, when the
policy tables are empty — writes the declared records as if they
had been Mutated, then records bootstrap-complete in a one-shot
table."*

Today's startup path (`service.rs:25-33`):

```rust
RoleRegistry::new(&tables, &layout).seed_current_workspace_roles()?;
```

…hard-codes the 11 current workspace role names (`signal-persona-
orchestrate/src/lib.rs:82-94`'s `CURRENT_WORKSPACE_ROLE_TOKENS`
constant) and seeds them every startup unconditionally
(role.rs:19-33 uses `insert_role_if_missing`). This is not the
bootstrap-once-from-nota pattern; it's bake-the-roles-into-the-
contract-source-code.

The two paths look similar but are very different:

| Today | Triad shape |
|---|---|
| Roles are baked into `RoleName::CURRENT_WORKSPACE_ROLE_TOKENS` array constant in the contract crate | Roles are declared in `bootstrap-policy.nota` in the runtime repo |
| Seeding runs every startup (idempotent via `insert_if_missing`) | Bootstrap runs exactly once, witnessed by a one-shot table; file is never read again |
| Changing the role set is a source edit in the contract | Changing the role set is an owner-Mutate after bootstrap |
| Factory reset is editing the constant + recompile | Factory reset is delete-the-redb + re-bootstrap, or an explicit reset verb |

The current shape also has a content boundary error: the contract
crate owns workspace policy data (the hard-coded role list). Per
ESSENCE and triad invariant, contract crates declare wire
vocabulary and nothing else; policy belongs in the daemon's seeded
state, sourced from `bootstrap-policy.nota` in the runtime repo.

### 2.5 — Lock-file projection is daemon-side, not the issue

`persona-orchestrate/src/lock_projection.rs` projects accepted
typed state into `orchestrate/<role>.lock` files. This is
correctly placed (daemon-side projection from authoritative
typed state). Per `intent/persona.nota` 2026-05-19T15:04Z this
is the explicit MVP scope.

The concern is **not** the projection code — it's that the
projection's *schema* is what shapes the contract. The contract
inherited the lock-helper relations (`Claim`, `Release`,
`Handoff`, …) because lock files are the projection. Per
/150 §6.8 the projection retires when lock files retire; the
contract should be shaped by orchestration's true domain, with
lock projection as an opt-in compatibility layer on top.

Today's `LockProjection::new(&tables, &layout).project()` is called
on every accepted mutation (`service.rs:43, 49, 54, 86, 91`),
which is the right pattern — the projection follows state. Keep
the projection mechanism; reshape what it projects.

### 2.6 — Activity log is a separate observability axis, not a feature

The contract carries `Submit(ActivitySubmission)` and
`Query(ActivityQuery)` for an "activity log" that records who
touched what scope with what reason. Per
`signal-persona-orchestrate/src/lib.rs:588-696`. This is the
same data shape as the lock-file claim (role + scope + reason),
plus a daemon-stamped timestamp.

Two readings:

- **Activity log is the audit trail for claims** — every claim
  insert/release/handoff also writes an activity record;
  `Submit`/`Query` exposes the audit trail to peers. In this
  reading, `Submit` shouldn't exist as a peer-callable operation —
  activity is daemon-internal, peers read it back via `Query` only.
  Today the contract exposes both.
- **Activity log is generic "agent told us what happened"** —
  agents `Submit(ActivitySubmission { role, scope, reason })`
  with arbitrary content; orchestrate persists it. In this reading,
  Submit/Query is a small message-passing surface that doesn't
  belong in orchestrate at all — it overlaps with what
  persona-router is for.

Either way, the activity-log surface as currently shaped is
either redundant (with claim mutations) or misplaced (vs router).
Worth surfacing in the redesign per §2.1.

Less load-bearing than §2.1–§2.4; flagging for the redesign pass.

## 3 · Owner signal audit

The owner contract's policy-programmability surface is load-bearing
per `intent/persona.nota` 2026-05-20T17:30Z; this section audits
it thoroughly.

### 3.1 — Surface area is small (three verbs)

`owner-signal-persona-orchestrate/src/lib.rs:85-98`:

```rust
signal_channel! {
    channel OwnerOrchestrate {
        operation Create(CreateRoleOrder),
        operation Retire(RetireRoleOrder),
        operation Refresh(RefreshRepositoryIndexOrder),
    }
    reply OwnerOrchestrateReply {
        RoleCreated, RoleRetired, RoleCreationRejected,
        RepositoryIndexRefreshed, OwnerOrchestrateRequestUnimplemented,
    }
}
```

Three operations. Per /150 §6 and /129, the destination surface
needs to carry:

- Role creation (`Create`) — ✓
- Role retirement (`Retire`) — ✓
- Local repository index refresh (`Refresh`) — ✓ (this is
  borderline owner-vs-working; psyche-call territory but a
  reasonable owner verb because it touches local-filesystem
  paths)
- **Policy programmability** — install/update/retire orchestration
  policies (§2.2 above) — MISSING
- **Allocation tuning** — defaults for reuse-over-spawn, context-
  compaction threshold, supervision policies — MISSING
- **Lane/registry management** — beyond role creation, owner-Mutate
  on the `lane_registry`, `scheduling_policy`,
  `supervision_policies` tables named in ARCH §5 — MISSING
- **Agent lifecycle override** — owner-only verbs for "stop this
  running agent", "reassign this agent", "block this agent from
  new work" — MISSING

The current owner contract is the **role-administration** subset
of what orchestrate's owner surface is meant to be. The
authority-and-configuration shape implied by the mind/orchestrate
boundary is much richer.

### 3.2 — Verb names are appropriate verb-form

`Create`, `Retire`, `Refresh` are verb-form, contract-local, no
ancestry prefix (record types `CreateRoleOrder`,
`RetireRoleOrder`, `RefreshRepositoryIndexOrder` are payload
nouns). ✓ This is correctly done.

`RoleCreationRejected.reason: RoleCreationRejectionReason` —
restates `Role` (already in `RoleCreationRejected`) and
`Creation` (also already in `RoleCreationRejected`). Should be
`reason: RejectionReason` per ESSENCE §Naming.

### 3.3 — Three Sema-class projections are wrong direction

`ARCHITECTURE.md` §1 (Contract Surface) maps:

| Operation | Projected Sema class |
|---|---|
| `Create` | `Mutate` |
| `Retire` | `Retract` |
| `Refresh` | `Mutate` |

The `Refresh → Mutate` is plausible (the local repository index
is replaced wholesale) but borderline — it could equally be
`Match` (the operation queries the filesystem and projects facts
into the index, which is more an `Assert` of newly observed
records). Per psyche
`intent/persona.nota` 2026-05-19T15:04Z (*"refresh the state of
repositories"*) this is a refresh-of-cached-facts. The Sema class
is genuinely ambiguous here; the right answer depends on whether
"the index" is policy state (which would justify `Mutate`) or
working state derived from observation (which would lean
`Assert`).

The current `OperationLowering::owner` in `lowering.rs:42-49`
matches the ARCH table. The wider question (§2.3) — that the
daemon doesn't use signal-executor, so the lowering doesn't
actually flow into the executor — supersedes the per-verb Sema
choice for now.

### 3.4 — No `observable` block; no Tap/Untap on the owner socket

Per /150 §6 every persona component is observable; the owner
socket should also expose the mandatory `Tap`/`Untap` surface so
introspect can debug orchestration policy decisions through the
owner channel. Today there's no observable block on either
socket.

Designer lean per /258 §1 (similar question for engine-manager):
**Tap/Untap on the working socket** (consistent universal
introspection — agent-registry observation, claim flow, activity
flow); **Tap/Untap on the owner socket too** — policy changes
should be observable. Confirm psyche.

### 3.5 — `OwnerOrchestrateRequestUnimplemented` is the only frame-alias-dance smell here

Already flagged in §1 above (alias dance + redundant
`operation` field). The owner contract has six alias lines at
lines 100-105 that the clean-emit macro fix will retire entirely.

### 3.6 — Owner contract is correctly split from working

The split between owner-only orders and peer-callable working
operations is correctly drawn:

- `Create`/`Retire` (mutating the role registry) → owner ✓
- `Refresh` (mutating the local repository index) → owner ✓
- `Claim`/`Release`/`Handoff` (per-role authority over their own
  scope) → working ✓
- `Observe`/`Query`/`Watch`/`Submit` (read + activity submit) →
  working ✓

This is the right boundary by who-can-call. No owner-only verbs
are leaking into the working contract, no peer-callable verbs are
trapped in owner.

The boundary issue is that the **scope is wrong on both
sides**, not that the boundary between them is misdrawn.

## 4 · Recommended next slice

In priority order. **The redesign work in (1) and (2) should
land before (3-6) because the executor migration would ossify a
shape that needs reshaping.**

1. **Designer pass on the working contract's destination scope**
   (§2.1). The deliverable is a successor signal tree that
   carries:
   - Today's claim/release/handoff (per
     `intent/persona.nota` 2026-05-19T15:04Z — keep as a slice).
   - Abstract-job submission (per /129 sketch + 2026-05-20T17:30Z
     — `Submit(JobRequest)` with a typed Job sum:
     `ResearchTopic`, `CreateComponent`, `RefineDocument`, …).
   - Agent registry observation (per 2026-05-20T17:30Z —
     `Observe(AgentRegistry)` returning all running agents and
     their typed types).
   - Reachability query (delegated to router per /129 §Q2 — NOT
     in orchestrate's contract).
   - Reassignment + compaction-decision request.

   **Psyche-touch item Q1**: is the destination contract a
   superset of today's lock-helper relations, or does it
   *replace* claim/release/handoff with the abstract-job
   vocabulary? Two readings, both plausible; psyche to choose.

2. **Designer pass on the owner contract's policy-programmability
   surface** (§2.2). The deliverable is a successor signal tree
   that carries:
   - `Create(CreateRoleOrder)` / `Retire(RetireRoleOrder)` (keep).
   - `Refresh(RefreshRepositoryIndexOrder)` (keep, or move to
     working — see §3.3).
   - Policy verbs per /129 §N2 — `RegisterPolicy(...)`,
     `RetirePolicy(...)`, `UpdatePolicy(...)`,
     `InspectPolicies(...)`.
   - Allocation tuning per /129 §N5 — context-compaction
     threshold, reuse-vs-spawn defaults.

   **Psyche-touch item Q2**: confirm the policy-record shape
   from /129 §N2 (`OrchestrationPolicy` with `JobClass`,
   `Sequence` of steps with `AgentType`, `Goal`,
   `SuccessCondition`, `OnFailure`) is the right destination.
   Mostly designer-derivable from the psyche statement, but the
   record shape itself is large enough to want a checkpoint.

3. **`bootstrap-policy.nota` creation + bootstrap-once code path**
   (§2.4). Create the file with today's 11 workspace roles as
   declared records; replace `seed_current_workspace_roles`
   logic with the one-shot bootstrap pattern per
   `skills/component-triad.md` §5. Retire the
   `CURRENT_WORKSPACE_ROLE_TOKENS` constant in the contract
   (policy data leaving the contract crate).

4. **Add the `observable` block to both signal contracts**
   (§/257 §1.11). Macro-injected `Tap`/`Untap` on both working
   and owner sockets per /150 §6 / `intent/persona.nota`
   2026-05-21T10:00Z.

   Side concern: the contract's hand-rolled
   `ObservationSubscription`/`OperationReceived`/`EffectEmitted`
   records are namespace pollution with the macro-emitted forms.
   When `observable` is added, these need disambiguation —
   probably rename the domain
   `Watch(ObservationSubscription)`/`Unwatch(ObservationToken)`
   into something role-specific
   (`WatchClaims(ClaimSubscription)` /
   `UnwatchClaims(ClaimWatchToken)`?) so the names don't
   collide.

5. **Migrate the daemon onto `signal-executor`** (§2.3). Define
   `Command` / `Effect` enums; impl `ToSemaOperation` /
   `ToSemaOutcome` / `Lowering` / `CommandExecutor` /
   `BatchErrorClassification`. Wire through
   `signal_executor::Executor::execute(request)`. **Do this
   after (1) and (2)** — the executor migration is mechanical
   once the contracts are right.

6. **Smaller cleanups** in arbitrary order:
   - Drop `Role*` ancestry prefixes (§1.5 / /257 §1.5).
   - Lift reply variants into outcome sums (§/257 §1.4).
   - Drop `operation: OwnerOperationKind` field from
     `OwnerOrchestrateRequestUnimplemented` (/257 §1.6).
   - Drop frame-alias-dance (/257 §1.10; auto-retires on macro
     clean-emit landing).
   - Rename `HandoffRejectionReason` →
     `HandoffRejection::RejectionReason` (no longer needs the
     ancestry prefix once nested inside its parent).
   - Two-field timestamp for `Activity` records (§/257 §1.12;
     not for `StoredRepository.refreshed_at`).
   - Drop `RoleName` alias once consumers migrate to
     `RoleIdentifier` (or to `Role` post-prefix-drop).

### Cross-cutting notes

- Today's MVP code is correctly placed and structurally sound
  for *what it implements*; this audit is overwhelmingly about
  scope (the contract doesn't carry what it needs to carry) and
  shape (the existing slices need the standard cleanups). The
  daemon's lock-file projection, redb store, dual-socket binding,
  one-NOTA-argument CLI — all of that is built correctly.
- Per `intent/persona.nota` 2026-05-19T15:04Z (*"raw MVP"*) and
  2026-05-19T18:35Z (*"go ahead and implement the component
  with all the constrained tests in place"*), the MVP scope was
  authorized and shipped. The redesign work is a successor
  arc, not a rollback of what shipped.
- Per `intent/workspace.nota` 2026-05-19T20:30Z
  (*"backward compatibility is not a constraint; the better
  long-term logic wins"*), redesigning the contract surface
  from the lock-helper vocabulary to the abstract-job
  vocabulary is the right move regardless of churn.

## 5 · References

- `intent/persona.nota` 2026-05-18T12:08Z — mind owns state /
  orchestrate owns machinery.
- `intent/persona.nota` 2026-05-19T15:04Z — raw orchestrate MVP
  decision; emulate the shell helper, dynamic roles.
- `intent/persona.nota` 2026-05-19T15:04Z — claim by directory
  or by explicit file list; no minus-handoff.
- `intent/persona.nota` 2026-05-20T17:30Z — abstract-job vocabulary
  / agent registry / context compaction / policy programmability /
  skills-bundle-into-roles / router as channel-gate.
- `intent/persona.nota` 2026-05-21T10:00Z — every persona
  component is observable (debug the debugger).
- `intent/signal.nota` 2026-05-20T13:30Z — orchestrate owns
  router; mind→orchestrate→router authority chain.
- `intent/component-shape.nota` 2026-05-20T02:00Z — three-layer
  model affirmation (Contract Operation / Component Command /
  Sema Operation).
- `intent/component-shape.nota` 2026-05-21T10:30Z — macros emit
  unprefixed names; modules for disambiguation.
- `skills/component-triad.md` — five invariants and the single-
  argument rule.
- `skills/naming.md` — ancestry-prefix and repeated-suffix rules.
- `reports/operator/150-triad-signal-sema-migration-current-state.md`
  §6.8 (orchestrate is a real component; avoid resurrecting
  lock-file semantics as the target).
- `reports/designer/257-signal-contracts-names-and-shape-audit.md`
  — workspace-wide naming/shape patterns.
- `reports/second-designer/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`
  — abstract-job submission shape, agent-type enum,
  orchestration-policy record, extension-skill request shape.
- `reports/second-operator-assistant/11-signal-type-naming-and-shape-design-guideline.md`
  — signal-type naming principles applied to working-vs-policy
  signal shapes.
- Code: `signal-persona-orchestrate/src/lib.rs:1-873`;
  `owner-signal-persona-orchestrate/src/lib.rs:1-163`;
  `persona-orchestrate/src/lib.rs`, `src/daemon.rs`,
  `src/service.rs`, `src/lowering.rs`, `src/role.rs`,
  `src/tables.rs`, `src/configuration.rs`,
  `src/bin/persona-orchestrate.rs`, `src/main.rs`;
  `persona-orchestrate/ARCHITECTURE.md` line 199 (missing
  bootstrap file).

This report retires when (a) the destination scope per §4(1) and
§4(2) is psyche-answered AND a successor signal tree lands AND
the daemon migrates onto signal-executor AND `bootstrap-policy.nota`
lands AND the observable block is added; OR (b) a successor audit
supersedes.
