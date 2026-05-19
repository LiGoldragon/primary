# 11 — Audit of operator-assistant/157 persona-orchestrate dynamic-role MVP

*Hole-finding audit of the operator-assistant lane's MVP report at
`reports/operator-assistant/157-persona-orchestrate-dynamic-role-mvp.md`.
The audit walks the shipped work in the three repos
(`signal-persona-orchestrate`, `owner-signal-persona-orchestrate`,
`persona-orchestrate`) against the designer handoff at
`reports/designer/233-persona-orchestrate-operator-handoff.md`, the
contract-local-verbs migration guide at
`reports/designer/241-signal-architecture-migration-guide.md`, and
`ESSENCE.md`. Audit, not authority — direction back to the design
surface, not new specification.*

## 0 · TL;DR

A material amount of solid work landed: contract-local verb roots via
`signal_channel!`, round-trip witnesses, lock-file projection from
typed state, dual sockets, four named Nix checks. The migration *shape*
matches the new architecture (`signal-frame` + per-daemon executor
lowering to `signal-sema`). But the *content* of the contracts and the
runtime deviate from the load-bearing direction in
`reports/designer/233` (the operator handoff) in ten places that the
MVP report does not surface.

The largest deviation: `signal-persona-orchestrate` collapses the
Submission-versus-Order distinction the designer report names as
"structural" (/233 §2 invariant 14) by putting `Claim` / `Release` /
`Handoff` directly on the ordinary peer surface instead of on the
owner surface as authoritative orders downstream of
`persona-mind`. The owner contract carries `Create` / `Retire` /
`Refresh` — none of the sixteen owner verbs /233 §5 specifies
(`SpawnAgentOrder`, `AcquireScopeOrder`, `RegisterLaneOrder`,
scheduling/supervision/escalation policies, the
`LaneRegistry*` family, the three Subscribe streams). The MVP
implements an entirely different owner contract than /233 says.

Beneath that, eight smaller-but-load-bearing gaps: typed Subscribe
families collapsed into a single bool-flag `Watch`; role-vs-lane
concept confused (`RoleIdentifier` is `LaneIdentifier`'s job per /233
§7); `Validate` and `BlockedWorkReport` absent; `Activity` missing
the `slot` field /233 §7 explicitly mandates; only two of /233's five
typed `Scope` variants present; closed `HarnessKind` enum coupling
the contract to two specific harnesses; `RoleName = RoleIdentifier`
compatibility alias violating ESSENCE "no transitional shapes";
hardcoded eleven-entry workspace-role list bleeding workspace
coupling into the wire-vocabulary crate; lock-file projection living
as steady state rather than cutover-phase scaffolding.

Two cross-cutting concerns rounding it out: the runtime `ordinary()`
lowering is a one-to-one static map (per `lowering.rs` line 28-40,
every contract verb produces exactly one Sema operation) — the
whole reason contract-local verbs exist is that the executor decides
the Sema-effect sequence at runtime (/241 §5), so a static one-to-one
map mostly defeats the purpose. And the daemon binds two Unix sockets
with zero filesystem-permission separation, which means the typed
owner-vs-ordinary contract has no OS-level enforcement (/233 §2
invariant 4: *"Owner-only sockets are an OS security boundary, not a
convention"*).

Finally, two scope flags from the report's own Questions section
look like they need designer-side answers, not operator judgment: the
"active repository" semantics (Q3) and the retire-role
filesystem-cleanup policy (Q4). They sit downstream of architectural
decisions /233 doesn't fully settle.

## 1 · What the audit grades against

Three surfaces. Their direction settles what should be in the MVP:

`reports/designer/233-persona-orchestrate-operator-handoff.md` — the
authoritative designer handoff for this work. §1 names the
state-vs-machinery split (mind owns state; orchestrate owns
machinery). §2 lists seventeen settled architectural decisions
including the Submission-vs-Order rule, the owner-signal-is-part-of-
triad invariant, the closed-RoleName-eventually-dissolves rule, and
the typed `Scope` enum at five variants. §5 lays out the ordinary
contract family inventory (ten families) and the owner contract
family inventory (sixteen families). §6 specifies the sema-engine
state schema (one policy table for lane registry, two more policy
tables for scheduling and supervision, eleven working-state tables).
§7 answers six prior questions including the exact-scope-match
handoff rule and the required `slot` field on `Activity`. §8 lists
twelve gaps that need closing. §9 gives a concrete next-arc ordering.

`reports/designer/241-signal-architecture-migration-guide.md` — the
practical reference for any contract migration, post-redirection.
§2 gives the canonical `signal_channel!` shape. §3 the per-component
checklist. §4 the verb-form naming rule (verb form for operation
roots: `State` not `Statement`, `Submit` not `Submission`). §5 the
daemon-side lowering shape — explicitly *"may be 0 → many Sema
operations: `Submit Message` might lower to `[Assert IngressEvent,
Mutate DeliveryState]` if accepted, to nothing if rejected, or to a
forwarded request if routed."* §6 the reference contracts.

`ESSENCE.md` — the workspace upstream. Three rules bear on this work:
*"Backward compatibility is not a constraint"* §"Backward
compatibility is not a constraint"; *"A transitional shape compromises
both the old and the new to avoid breaking either. It is the wrong
shape for both, and the wrong shape, period"* same section; *"Spell
every identifier as a full English word AND names don't carry their
full ancestry"* §"Naming". The boundary rule's only exception is
*"explicitly declared boundaries — published APIs under semantic
versioning, wire contracts pinned by version, schemas externally
consumed by systems outside our control"* — which the in-flight
`persona-orchestrate` contract is not.

## 2 · Deviation 1 — the Submission-versus-Order distinction collapsed

/233 §2 invariant 14: *"Submission vs Order is structural. `Assert
ScopeAcquisitionSubmission` (caller asks) is a different verb than
`Mutate AcquireScopeOrder` (mind authoritatively orders)."* The
distinction is load-bearing — it encodes the authority chain
`persona-mind → persona-orchestrate → persona-router /
persona-harness` (/233 §2 invariant 2). A peer that wants a scope
*submits* an acquisition request to orchestrate, which routes it
through mind's policy state; mind, having decided, issues a *Mutate
AcquireScopeOrder* over the owner contract — and orchestrate executes.

What shipped: `Claim(RoleClaim { role, scopes, reason })` directly on
the ordinary peer surface (`signal-persona-orchestrate` line 444-448).
The peer claims the scope; orchestrate handles the claim and stores
it. Mind is not in the loop. The flow is peer → orchestrate, period.

This collapses two structurally different verbs into one. A
peer/CLI submitting *"I'd like this scope, decide whether I can have
it"* and mind ordering *"grant this peer this scope"* now look
identical at the contract level. The whole authority chain in /233 §4
becomes prose with no wire-shape consequence.

Either /233 is wrong (and the psyche has superseded it — but the
intent log doesn't show that) or the MVP shipped before this
deviation was named. The audit needs a designer answer: should
`Claim` route through mind, or has the Submission-vs-Order rule been
retired? Either answer changes the contract and the daemon's
dispatch.

## 3 · Deviation 2 — the owner contract carries the wrong verbs

/233 §5 owner-signal-persona-orchestrate inventory (sixteen
families): `SpawnAgentOrder`, `StopAgentOrder`, `PauseAgentOrder`,
`ResumeAgentOrder`, `AcquireScopeOrder`, `ReleaseScopeOrder`,
`SetSchedulingPolicy`, `SetSupervisionPolicy`, `EscalationOrder`,
`RegisterLaneOrder`, `RetractLaneOrder`, `UpdateLaneMetadataOrder`,
`LaneRegistrySnapshotQuery`, `OwnerSnapshotQuery`,
`AgentLifecycleSubscription`, `ExecutorCapacitySubscription`,
`ScopeEventSubscription`.

What shipped (`owner-signal-persona-orchestrate/src/lib.rs`): three
verbs — `Create(CreateRoleOrder)`, `Retire(RetireRoleOrder)`,
`Refresh(RefreshRepositoryIndexOrder)`. Zero overlap with /233's
sixteen families.

The MVP appears to have invented a different owner contract: one
that manages *role identity* (create / retire a role definition) and
one filesystem affordance (refresh the repository index). Neither
exists in /233. The `RegisterLaneOrder` family, which /233 names as
the stage-(a) deliverable for the lane-registry sweep, is absent.
The agent-lifecycle owner orders (`SpawnAgentOrder` etc.) — the
load-bearing reason owner-signal-persona-orchestrate exists at all
per /233 §1 ("`persona-orchestrate` owns MACHINERY — role claims,
activity log, agent-run lifecycle, spawn plans, scope-acquisition
workflow, executor capacity snapshots, scheduling state, escalation
state, lane registry") — are nowhere.

`Refresh` in particular looks like the wrong contract layer. It's a
filesystem-scan-and-rebuild affordance. /233 §5 doesn't carry it on
either surface; if it belongs anywhere it would be the ordinary
surface as a `Mutate`-equivalent (post-/241, an ordinary `Refresh`
verb whose executor lowers to `Match` over the filesystem + `Mutate`
of the `repositories` table). Putting it on the *owner* contract
implies it's a privileged authority operation, but it does no
authority work — it's a self-introspection mutation.

Same designer-answer question as §2: is /233's owner-verb list still
the contract direction, or has it been superseded?

## 4 · Deviation 3 — typed Subscribe families collapsed into bool-flag `Watch`

/233 §5 has four Subscribe families at the ordinary surface:
`OwnRunLifecycleSubscription`, `LaneRegistrySubscription`,
`ActivityStream`, `ClaimStream`. Each has a distinct subject and a
distinct event payload (per /233 §5 final paragraph: `AgentLifecycleStream`
states; `ScopeEventStream` states; `ExecutorCapacityStream` states;
`EscalationStream` states).

What shipped:
`Watch(ObservationSubscription { include_operations: bool,
include_sema_effects: bool })` (`signal-persona-orchestrate` line
703-706). A single `Watch` verb whose subject-selection is two
boolean flags. The reply stream carries inbound contract operations
and outbound Sema effects mixed.

This is exactly the smell `skills/typed-records-over-flags.md`
(Keystroke-tier skill) warns against: *"Closed typed records over
bool flags. Surface the variant set in the type system."* The shipped
shape says "I want operation events, sema events, both, or neither"
via two bools. The /233 shape says "I want activity events" or "I
want claim events" or "I want lane-registry events" as distinct
typed subscriptions, each with a typed close-token (per /241 §2
Streams: *"The macro validates that the close operation's payload
type matches the stream token type"*).

The right shape is multiple stream blocks in `signal_channel!`, one
per subject — `ActivityStream`, `ClaimStream`, `LaneRegistryStream`,
plus the introspection stream the MVP introduced. With per-stream
close tokens. The macro itself supports this; the contract just
hasn't declared the blocks.

## 5 · Deviation 4 — role-vs-lane concept confusion

/233 §2 invariant 9: *"Lane registry is data, not enum variants.
Lanes come from config at startup and are mutable at runtime via the
`owner-signal-persona-orchestrate` `LaneRegistry*` family. The closed
`RoleName` enum eventually dissolves."* /233 §7 stage (b): *"closed
`RoleName` enum dissolves into typed `LaneIdentifier`."*

The workspace already has a role-vs-lane distinction (per
`skills/role-lanes.md`): the four main roles are `operator`,
`designer`, `system-specialist`, `poet`; their lanes are
`operator-assistant`, `second-operator-assistant`, etc. — sharing the
main role's discipline, beads label, and skill file. Lanes are
how operational capacity scales without splitting authority.

What shipped: `RoleIdentifier(String)` named `RoleName` via alias.
The eleven-entry `CURRENT_WORKSPACE_ROLE_TOKENS` const
(`signal-persona-orchestrate` line 82-94) enumerates all eleven
*lanes*, not the four roles. The name `RoleIdentifier` is wrong;
the concept being identified is the lane. The /233 design says
"`LaneIdentifier`" — same shape, different name, different concept.

This isn't pedantry. The name determines what other components
think they're seeing. A `RoleStatus { role: RoleName, harness: HarnessKind,
claims: Vec<ClaimEntry> }` reads as "role-level status"; downstream
callers will treat each entry as a role-level fact. In reality each
entry is a *lane-level* fact (the second-operator-assistant lane is
not the operator role). When mind decides scheduling policy, the
policy attaches to the role (the discipline pool); when mind decides
who has a scope claim, the claim attaches to the lane (the specific
agent capacity). The data shape doesn't yet distinguish them.

Recommendation back to designer: settle the type names — is this
crate's identity `LaneIdentifier` per /233 §7, or `RoleIdentifier`
which fuses two concepts? If the former, the operator-assistant
lane needs a rename pass.

## 6 · Deviation 5 — missing primitives

Five primitives /233 specifies that the MVP doesn't carry:

`Validate SpawnPlanValidation` (/233 §5 ordinary surface, /233 §6
working-state `spawn_plans` table). The dry-run primitive for
"mind asking orchestrate whether this spawn plan would succeed
without actually starting the agent run." Not shipped. The /241 §4
verb-form rule applies: the verb would be `Validate`.

`Assert BlockedWorkReport` → `Submit BlockedWork` (/233 §5 ordinary).
A peer/agent reports it's blocked. Not shipped.
`signal-persona-orchestrate`'s `Submit` carries only
`ActivitySubmission`.

`slot: u64` on `Activity` (/233 §7 explicit settled answer:
*"Activity slot exposed in query records? Yes. Add `slot: u64` to
`Activity` (matching the slot in `ActivityAcknowledgment`). Required
for subscription catch-up."*). The shipped `Activity` struct
(`signal-persona-orchestrate` line 594-599) has `role`, `scope`,
`reason`, `stamped_at` — no `slot`. The /157 report does not flag
this gap; the audit confirms it directly.

`HandoffRejection::ScopeNotHeldExactly` typed variant (/233 §7
exact-scope-match rule, psyche-stated 2026-05-19: *"if an agent
claims a directory, then everything in that directory is claimed.
… If you want to claim only certain files in a subdirectory, you
have to claim them explicitly. We can't do like this minus this."*).
Shipped `HandoffRejectionReason`: `SourceRoleDoesNotHold |
TargetRoleConflict(Vec<ScopeConflict>)`. The exact-scope-match
rejection variant is absent. /157 report does not flag this.

Three of the five typed `Scope` variants (/233 §2 invariant 15:
*"Scope identity is a typed `Scope` enum: `Path`, `Task`, `ReportLane`,
`Component`, `WorkGraph`"*). Shipped `ScopeReference`:
`Path(WirePath) | Task(TaskToken)`
(`signal-persona-orchestrate` line 195-201). `ReportLane`,
`Component`, `WorkGraph` absent. The MVP took the simpler
two-variant subset.

## 7 · Deviation 6 — sema state schema not the right shape

/233 §6 specifies fourteen tables split into two categories: policy
(owner-Mutate only; bootstrapped) and working (peer-callable per
contract). Three policy tables: `lane_registry`, `scheduling_policy`,
`supervision_policies`. Eleven working tables.

What shipped (`persona-orchestrate/src/tables.rs`): five tables —
`claims`, `roles`, `repositories`, `activities`,
`activity_next_slot`. No policy/working categorization. No
`lane_registry` table. No `scheduling_policy` or
`supervision_policies` tables. No `agent_runs`, `spawn_plans`,
`agent_executors`, `scope_acquisitions`, `channel_grants`, or
`escalation_state` tables.

The `roles` table is the MVP's reinterpretation of /233's
`lane_registry` table (per §5 above) but doesn't carry the
`assistant_of?` / `beads_label` / `metadata` fields /233 §6 names —
and it's stored as working state, not policy state (the daemon
mutates it on `Create` orders without a bootstrap policy file).

The `repositories` table is novel — not in /233 §6 — and its
purpose intersects with the workspace's `repos/` symlink directory,
producing the synchronization smell flagged in the MVP report Q3.

## 8 · ESSENCE-violating shapes

Four places where the MVP uses a transitional or
backward-compatibility shape ESSENCE.md §"Backward compatibility is
not a constraint" forbids inside the workspace.

`pub type RoleName = RoleIdentifier;` (line 79). A compatibility
alias for the old name. ESSENCE: *"break the system if it makes it
more beautiful."* The right shape is renaming all `RoleName`
call-sites to `RoleIdentifier` (or to `LaneIdentifier` per the
concept clarification in §5 above) and removing the alias. No
external consumer has the wire pinned at semver yet.

`HarnessKind { Codex, Claude }` (line 162-165) — closed enum
declaring exactly two harnesses on the wire. This is the same
closed-enum trap /233 §2 invariant 9 says lane-registry must escape.
A new harness (Cursor, a future agent) breaks the contract. The
right shape is a typed-token newtype, with the *closed enum* living
only inside whichever component classifies harness behavior (per
bead `primary-es9` — *"persona-harness: daemon, closed HarnessKind,
transcript pointers"* — naming `persona-harness` as the home).

`pub const CURRENT_WORKSPACE_ROLE_TOKENS: [&'static str; 11]`
(line 82-94). A const list of current workspace lanes inside the
*wire-vocabulary* crate. The contract should not know about which
lanes currently exist; that's daemon-side seed configuration. The
list is exposed `pub` so the daemon's `seed_current_workspace_roles`
can iterate it — but that coupling belongs in the daemon, not in the
contract crate. The contract carries the *type* `RoleIdentifier`;
the daemon carries the *current values*.

Lock-file projection at `persona-orchestrate/src/lock_projection.rs`.
The MVP report frames this as "compatibility lock-file projection
from daemon-owned typed claims into `orchestrate/<role>.lock`" — and
indeed the direction is right (daemon as truth, lock files as
projection) which inverts the /233 §8 gap #6 problem. But the
projection is steady state, not cutover scaffolding. ESSENCE
forbids transitional shapes that persist. Either the cutover is
committed-to (after `persona-orchestrate` is real and supervised,
lock files disappear entirely) or the projection becomes a
permanent feature of the daemon — which it shouldn't be, because
no other agent ever needs to read those files once everyone speaks
the contract. The MVP doesn't surface the retirement plan.

## 9 · The lowering is one-to-one — defeating the redirection

/241 §5 names the executor lowering as load-bearing: *"The lowering
may be 0 → many Sema operations: `Submit Message` might lower to
`[Assert IngressEvent, Mutate DeliveryState]` if accepted, to nothing
if rejected, or to a forwarded request if routed."* The contract
declares verbs in the client's vocabulary; the daemon *decides at
runtime* what sequence of Sema effects to produce.

What shipped (`persona-orchestrate/src/lowering.rs` lines 28-49):

```
ordinary():   Claim→Assert, Release→Retract, Handoff→Mutate,
              Observe→Match, Submit→Assert, Query→Match,
              Watch→Subscribe, Unwatch→Retract
owner():      Create→Mutate, Retire→Retract, Refresh→Mutate
```

A static one-to-one map. Every contract verb produces exactly one
Sema operation, deterministically, without consulting policy state
or payload content. This is functionally equivalent to a transparent
wrapper — the redirection's whole motivation (contract-local verbs
let the *executor* decide the Sema-effect sequence) is mostly mooted.

Three places where the right runtime would emit multiple effects:

`Claim` should be `Match` (against current claims for conflicts)
+ `Assert` (the new claim, if no conflict) — or `Reject` (no Sema
op, just a typed reply). The one-to-one map says `Claim` always
produces an `Assert`, which can't be right.

`Handoff` should be `Retract` (the source role's claim) + `Assert`
(the target role's claim) under a transaction, with `Match` first
to verify exact-scope-match (per the rule from §6 above). The
one-to-one map says `Handoff → Mutate`, which doesn't even match
the table-write semantics.

`Submit Activity` should be `Mutate` (advance the activity slot
counter) + `Assert` (write the new activity record). The one-to-one
map says `Submit → Assert`.

The lowering needs to be the actual daemon-side translation logic,
not a verb-rename table. /241's worked example (§5 Rust sketch)
shows the right shape.

## 10 · OS permission boundary unenforced

/233 §2 invariant 4: *"Owner-only sockets are an OS security
boundary, not a convention. Per-component Unix users/groups for
first-pass enforcement; same-UID prototype is unsafe author-only
dev."* The MVP report acknowledges (§"Gaps"): *"the owner contract
is implemented, but filesystem permissions still do not enforce
ordinary-vs-owner access."*

What this means operationally: the two-socket separation in
`persona-orchestrate/src/daemon.rs` (`accept_ordinary` and
`accept_owner` thread loops) is a compile-time-only distinction. Any
peer with filesystem access to the daemon's socket directory can
connect to either socket — including the owner socket — and submit
owner-vocabulary frames. The frame parser will reject ordinary
vocabulary on the owner socket and vice versa, but that's
vocabulary-typed, not authority-typed: anyone who can speak the
owner vocabulary can also reach the owner socket.

The typed owner contract is buying nothing operationally until the
permission boundary lands. Until then, /233 §2 invariant 4's
*"unsafe author-only dev"* characterization applies.

This is a system-specialist-lane problem (Unix permissions, service
units, the broader `persona-daemon` engine-manager pattern per /233
§17). The MVP should flag it as a hard blocker for cutover, not as
a casual "Gap" bullet — until OS enforcement lands, the daemon
cannot replace `tools/orchestrate` in any environment with more
than one agent UID.

## 11 · Thread-per-connection isn't the destination

`persona-orchestrate/src/daemon.rs` lines 81-104 implement
synchronous thread-per-connection accept loops. The MVP report
acknowledges (§"Gaps"): *"the daemon is a synchronous
thread-per-connection MVP, not the final Kameo actor tree."*

The workspace's universal stateful-component shape is supervised
Kameo actors (`skills/actor-systems.md`, `skills/kameo.md`,
`skills/component-triad.md`). The MVP isn't *on the path* to a
Kameo actor tree — it's a side-shape. Migrating from
thread-per-connection to Kameo means rewriting concurrency
throughout: mailbox-based message dispatch, supervised restart,
release-before-notify discipline, trace-witness testing. The
acknowledgment frames this as future work; the audit notes that
"future work" here means "throw away the current daemon module
structure and start over with actors."

The MVP could have started with a minimal Kameo actor tree (one
supervisor + one ordinary-socket actor + one owner-socket actor +
one storage actor) and grown from there. That would be on the
path to the destination. What shipped is a parallel arc that has
to be replaced before cutover. Worth surfacing whether that's the
psyche's intent.

## 12 · Source-scan vs Rust visibility for the CLI boundary

`persona-orchestrate/tests/architecture.rs` enforces the CLI
boundary by `include_str!`ing the CLI source and asserting it
doesn't contain a list of forbidden tokens (`OrchestrateService`,
`OrchestrateTables`, `StoreLocation`, `sema_engine`,
`persona-orchestrate.redb`, `PERSONA_ORCHESTRATE_STORE`).

This is a textual absence check, not a structural guarantee. It
catches direct imports of named types but cannot catch indirect
imports via trait re-exports, type aliases, or new types added to
the daemon module that aren't in the forbidden list. The right
shape is Rust module visibility: the daemon's internals live in
non-public modules (or are `pub(crate)` only), making it
impossible for the CLI binary to import them. A test that the
binary compiles is then the boundary check.

The shipped witness will pass even if someone adds a new
forbidden-direction import as long as the type name isn't in the
list. The list-maintenance burden is on every future addition.
Visibility is the lower-burden, higher-strength check.

## 13 · `OrchestrateService` is a god-noun

`persona-orchestrate/src/service.rs` carries `OrchestrateService`
with four fields (`tables`, `layout`, `sequence: Mutex<()>`,
`next_observation_token: Mutex<u64>`) and methods dispatching both
ordinary requests (`handle`) and owner requests (`handle_owner`)
across five concerns (claims, activity, roles, repositories,
observation tokens).

Per `skills/abstractions.md`: verb belongs to the *right* noun.
Per `skills/naming.md`: names don't carry their full ancestry —
"Service" inside `persona-orchestrate` is redundant. The right
shape is the smaller nouns that already exist in the crate
(`ClaimLedger`, `ActivityLedger`, `RoleRegistry`,
`RepositoryRegistry`) coordinating through the daemon, not
through a central Service struct.

This is mostly a refactor smell — once Kameo actors land per §11
above, each actor becomes its own noun and `OrchestrateService`
dissolves.

## 14 · Holes in the report's own conclusions

The /157 report's framing has three soft spots worth surfacing:

The "What Works" list (§"What Works") claims thirteen working
properties of the MVP. Two of them are weaker than stated:
*"Roles are no longer compile-time enum variants on the ordinary
contract surface"* — true at the type level, but the hardcoded
`CURRENT_WORKSPACE_ROLE_TOKENS` const couples the same crate to
the same set of values the old enum would have carried, so the
dynamism is mostly cosmetic; and *"Observation subscriptions
allocate and close typed tokens on the ordinary surface"* — true,
but per the report's own "Gaps" §, no events are delivered. A
subscription primitive that doesn't deliver isn't a working
subscription; it's an allocated handle that goes nowhere.

The "Gaps" list (§"Gaps") doesn't include: the Submission-vs-Order
deviation from /233, the missing thirteen owner verbs, the missing
`Validate` verb on the ordinary surface, the missing
`BlockedWorkReport`, the missing `slot` field on `Activity`, the
missing `ScopeNotHeldExactly` rejection variant, the missing three
`Scope` variants, the missing eleven sema tables, the
ESSENCE-violating `RoleName` alias, the workspace coupling in
`CURRENT_WORKSPACE_ROLE_TOKENS`, the one-to-one lowering, and the
source-scan-vs-visibility witness shape. The audit found twelve
non-acknowledged gaps; the report acknowledges six (report-repo
creation, repository active flag, retire-role cleanup,
subscription delivery, permission enforcement, Kameo actor tree).

The "Questions" list (§"Questions") asks five operational questions.
Three (Q1 repo naming, Q3 active-repository semantics, Q4
retire-role policy) are operationally valuable but architecturally
downstream of the deviations in §§2-4 of this audit. Q5 ("supervised
workspace launch path") is the right next step but parks behind
either (a) shipping the actor-tree shape per §11 or (b) accepting
thread-per-connection as the deployment target — which itself
needs designer confirmation.

## 15 · What's worth keeping

Real work landed and should not be discarded:

The `signal_channel!` macro adoption is right. Both contracts use
the post-redirection macro shape (`signal-frame` + per-daemon
executor lowering). The verb-form naming on the surviving verbs is
right (`Claim` not `ClaimSubmission`, `Submit` not `Submission`).

Round-trip witnesses exist (19 tests in
`signal-persona-orchestrate/tests/round_trip.rs`, 5 in
`owner-signal-persona-orchestrate/tests/round_trip.rs`). Per
`skills/contract-repo.md` examples-first round-trip discipline,
that's the falsifiable specification surface. Useful regardless of
which verbs end up final.

The lock-file projection direction (daemon as truth, lock files as
output) inverts /233 §8 gap #6 correctly. The conceptual move
matters; the lifecycle (cutover-only vs steady-state) is the
remaining design call.

Four named Nix checks (`test-dynamic-role-creation`,
`test-repository-refresh`, `test-cli-boundary`, `test-daemon-cli`)
exist and exercise the load-bearing surfaces. The check naming
shape is right per `skills/architectural-truth-tests.md`.

`ScopeReference { Path(WirePath) | Task(TaskToken) }` is the right
shape for the two variants it carries — typed sum, not strings.
The remaining three /233 variants slot in cleanly.

`signal-persona-orchestrate`'s `ARCHITECTURE.md` exists at the
right level of detail (149 lines) and records migration history.
`owner-signal-persona-orchestrate`'s is similar (92 lines).
`persona-orchestrate`'s is longer (304 lines, exceeds the matklad
50-150-line guidance) but covers state ownership clearly.

## 16 · Recommendations back to the design surface

The audit doesn't authorize new design — that's the designer lane's
work. What the next designer-lane pass needs to settle:

Is /233's design still current, or has it been superseded by an
unrecorded conversation? The MVP's owner contract bears no
resemblance to /233 §5's sixteen-verb inventory; either /233 is
stale or the MVP went off-piste. If /233 is stale, what supersedes
it? If /233 is live, the MVP needs a major re-spec.

Is the contract-local-verb migration in /241 supposed to collapse
typed Subscribe families into bool-flag selections? If yes, the
`skills/typed-records-over-flags.md` discipline needs an
addendum naming the carve-out. If no, the MVP's `Watch` needs to
split into the four /233 streams.

Is `RoleIdentifier` the lane-identity per /233 §7 (in which case
rename) or is it the role-discipline-pool identity (in which case
the data model needs a separate lane abstraction)?

Should `HarnessKind` live on the `persona-orchestrate` wire at all,
or does it belong with `persona-harness` (per bead `primary-es9`)?

Is the lock-file projection cutover-only scaffolding or
steady-state? If the former, name the retirement criterion in the
daemon's ARCHITECTURE.md. If the latter, justify against ESSENCE
§"Backward compatibility is not a constraint."

Should `Refresh` (repository-index rebuild) be an owner verb at
all, or is it an ordinary self-mutation? Per /241 §5 the executor
decides — but the *vocabulary placement* (which contract carries
the verb) is the design call.

Is thread-per-connection acceptable for cutover, or does the
cutover gate on Kameo-actor-tree shape? The answer changes how
much of `persona-orchestrate/src/` is throw-away.

And — the workspace-protocol-level question that may underlie all
of this — `orchestrate/AGENTS.md` §"Command-line mind target"
still names `persona-mind` (`mind` CLI + `persona-mind` daemon +
`signal-persona-mind` contract) as the destination for the
orchestration protocol. /233 §1 names `persona-orchestrate` as the
destination for machinery (claims, activities, lanes) while mind
keeps state. Two contradictory destinations for the same protocol.
The protocol document is stale relative to /233; either /233's
state-vs-machinery split is the live direction (and
`orchestrate/AGENTS.md` needs the rewrite that names *both*
daemons) or the split was rolled back and `persona-orchestrate`
needs to fold into mind.

## 17 · References

`reports/operator-assistant/157-persona-orchestrate-dynamic-role-mvp.md`
— the implementation report under audit.

`reports/designer/233-persona-orchestrate-operator-handoff.md` — the
designer handoff this MVP responds to; the audit grades against
this report's §§2, 5, 6, 7, 8.

`reports/designer/241-signal-architecture-migration-guide.md` — the
post-redirection migration shape; §§2-5 apply.

`reports/designer/238-signal-architecture-redirection-contract-local-verbs.md`
— the broader redirection direction.

`reports/designer/240-signal-frame-operation-collapse-check-removal.md`
— the kernel cleanup the macro now reflects.

`reports/operator-assistant/156-persona-orchestrate-context-sweep.md`
— the precursor sweep where the operator-assistant lane absorbed
/233's findings into the persona-orchestrate repo's ARCHITECTURE.md.

`orchestrate/AGENTS.md` — the workspace protocol doc; §"Command-line
mind target" stale relative to /233 §1.

`ESSENCE.md` §"Backward compatibility is not a constraint", §"Naming";
`skills/typed-records-over-flags.md`; `skills/abstractions.md`;
`skills/contract-repo.md` examples-first; `skills/actor-systems.md`;
`skills/component-triad.md` invariants.

`/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs`
lines 64-94 (RoleIdentifier + workspace-tokens const), 162-183
(HarnessKind), 195-242 (ScopeReference), 444-720 (the eight ordinary
verbs and replies), 594-599 (Activity missing slot field).

`/git/github.com/LiGoldragon/owner-signal-persona-orchestrate/src/lib.rs`
lines 14-83 (the three owner verbs and reply variants).

`/git/github.com/LiGoldragon/persona-orchestrate/src/lowering.rs`
lines 28-49 (one-to-one lowering map);
`/git/github.com/LiGoldragon/persona-orchestrate/src/daemon.rs`
lines 66-104 (socket binding without permission setting,
thread-per-connection accept loops);
`/git/github.com/LiGoldragon/persona-orchestrate/src/tables.rs`
lines 13-18 (five-table schema vs /233's fourteen);
`/git/github.com/LiGoldragon/persona-orchestrate/tests/architecture.rs`
(source-scan CLI boundary witness).

Bead `primary-699g` (persona-orchestrate design); bead `primary-es9`
(persona-harness owns HarnessKind); bead `primary-ojxq`
(persona-spirit triad — apex of the orchestrate authority chain
once spirit lands per /232).
