# persona-orchestrate signal-executor migration vision

Date: 2026-05-21
Lane: operator-assistant
Source: `reports/operator/150-triad-signal-sema-migration-current-state.md`

## Scope

I retrieved the intent and skill surfaces named by report 150 and
then checked the current `persona-orchestrate` triad against the
2026-05-20 library substrate:

- intent: `intent/component-shape.nota`, `intent/signal.nota`,
  `intent/persona.nota`, `intent/workspace.nota`;
- workspace sources: `ESSENCE.md`, `INTENT.md`, `AGENTS.md`,
  `repos/lore/AGENTS.md`, `orchestrate/AGENTS.md`;
- skills: `skills/component-triad.md`, `skills/contract-repo.md`,
  `skills/rust-discipline.md`, `skills/actor-systems.md`,
  `skills/naming.md`, `skills/reporting.md`,
  `skills/intent-log.md`, `skills/intent-clarification.md`,
  `skills/repo-intent.md`, `skills/operator.md`,
  `skills/role-lanes.md`;
- reports: `reports/operator/150-triad-signal-sema-migration-current-state.md`,
  `reports/designer-assistant/129-mind-orchestrate-payload-and-cli-dispatch-option-a-2026-05-20.md`,
  `reports/designer/257-signal-contracts-names-and-shape-audit.md`,
  `reports/designer/258-persona-signal-triad-audit-2026-05-21.md`;
- repositories: `persona-orchestrate`,
  `signal-persona-orchestrate`,
  `owner-signal-persona-orchestrate`, `signal-frame`,
  `signal-sema`, `signal-executor`, `sema-engine`,
  and `persona-spirit` as the current working template.

This prompt did not add durable psyche intent. It asked for a
retrieval and analysis pass, so I did not append a new intent record.

## Current State

The Orchestrate triad exists and is useful as a raw prototype.
`persona-orchestrate` has ordinary and owner sockets, a daemon-owned
`persona-orchestrate.redb`, dynamic role creation, claim/release/
handoff, an activity log, local repository refresh, report lane
creation, and downstream lock-file projection. The CLI does not open
the store, and the tests already protect the basic "CLI talks only to
the daemon" rule.

That is the right minimum viable product lineage, but it is not yet
on the current triad architecture. The implementation still has an
old direct path:

- `src/lowering.rs` maps contract operations directly to
  `signal_sema::SemaOperation`;
- `src/service.rs` matches directly on working and owner operations
  and mutates the ledgers;
- `src/daemon.rs` calls the service directly and fabricates replies
  around single payloads;
- the crate does not depend on `signal-executor`;
- the contracts are still locked to the older `signal-frame`
  revision `4bdf1e1e`, before clean macro output, generated CLI
  dispatch, and the current observable block support;
- the CLI tries to decode the request as working first, then owner,
  which is the explicitly rejected Option C shape.

This means Orchestrate is structurally behind the library
infrastructure built on 2026-05-20. It should not be patched in place
by making `OperationLowering` a little smarter. It needs the same
three-layer runtime conversion that `persona-spirit` now demonstrates:
contract operation to daemon-local command, command to sema operation
class for observation, executed command to daemon-local effect, effect
to sema outcome for observation.

## Contract Drift

`signal-persona-orchestrate` is close but still pre-current:

- it has manual `OperationKind` and `operation_kind()` instead of the
  macro-generated kind;
- it has `Watch(ObservationSubscription)` and
  `Unwatch(ObservationToken)` as a generic operation/effect observer,
  but report 150 and `signal-frame` now make generic observation the
  macro-injected `Tap` / `Untap` surface;
- it has no `observable { filter default; operation_event
  OperationReceived; effect_event EffectEmitted; }` block;
- `ObservationSubscription.include_sema_effects` still carries the
  old mental model even though the event is now `EffectEmitted`
  carrying `SemaObservation`;
- `RoleObservation` is an empty record payload. That may remain
  mechanically necessary as an operation payload, but it should be
  reconsidered if the query surface is lifted into a typed `Query`
  payload.

`owner-signal-persona-orchestrate` is narrower and older:

- it carries only `Create`, `Retire`, and `Refresh`;
- `OwnerOrchestrateRequestUnimplemented` redundantly carries the
  operation kind even though the reply is already positionally
  correlated;
- it has manual kind and conversion boilerplate that the current
  macro should generate;
- its operation roots will become ambiguous when owner authority grows
  beyond roles and repository refresh.

The ordinary contract should be migrated first because the generated
CLI route table depends on both contracts exposing current operation
head metadata. The owner contract should then be migrated with the
same macro generation and with a deliberate signal-tree pass before
adding more owner powers.

## Runtime Vision

The runtime target is not "service plus lowered sema labels"; it is an
executor-centered daemon with local command and effect types.

Recommended first slice:

1. Move both contracts to the current `signal-frame`, `signal-sema`,
   and `nota-codec` pins.
2. Put generated clean names inside modules if the working and owner
   surfaces need parallel `Operation`, `Reply`, and `Frame` names.
3. Add the ordinary observable block and remove or repurpose the old
   generic `Watch` / `Unwatch` observer pair.
4. Add `signal-executor` to `persona-orchestrate`.
5. Replace `OperationLowering` with daemon-local `Command` and
   `Effect` enums.
6. Implement `ToSemaOperation` for `Command` and `ToSemaOutcome` for
   `Effect`.
7. Implement one working `Lowering` and one owner `Lowering`, both
   feeding a shared `CommandExecutor`.
8. Route daemon socket requests through `Executor::execute`.
9. Use a no-op observer set at first if live fanout is not ready, then
   bridge to the macro-generated observable set.
10. Replace CLI try-decode dispatch with `signal_cli!` head routing.

The first executor pass can follow the `persona-spirit` degenerate
atomicity pattern: reject multi-operation or multi-command batches
before committing until the Orchestrate store has a real transaction
boundary for the whole batch. That is better than the current
single-payload rejection in the daemon because it uses the accepted
`BatchAborted` semantics and keeps reply correlation inside
`signal-executor`.

The local `Command` enum should describe Orchestrate machinery, not
Sema verbs. A plausible first cut:

- acquire scopes;
- release role scopes;
- hand off scopes;
- read role snapshot;
- record activity;
- read activity;
- create role;
- retire role;
- refresh repository index;
- open observer;
- close observer;
- explicit no-change for unsupported but accepted infrastructure
  operations.

The local `Effect` enum should describe committed Orchestrate facts:
claim accepted, claim rejected as a domain reply, scopes released,
handoff accepted, role snapshot read, activity recorded, activity
listed, role created, role retired, repository index refreshed,
observer opened, observer closed, or request unimplemented. Effects
then project to `SemaOutcome` for observation.

## State And Actor Shape

The current state tables are enough for the raw helper replacement:
`roles`, `claims`, `repositories`, `activities`, and
`activity_next_slot`. The architecture document already names the
missing tables: `claim_archive`, `lane_registry`, `agent_runs`,
`spawn_plans`, `agent_executors`, `scope_acquisitions`,
`channel_grants`, `scheduling_policy`, `supervision_policies`, and
`escalation_state`.

The next implementation should separate the schema into at least four
families:

- policy state: role definitions, lane metadata, scheduling policy,
  supervision policy, repository policy;
- working state: active claims, claim archive, activity, scope
  acquisitions, agent runs, spawn plans, executor capacity, escalation
  state;
- projections: lock files and workspace `repos/` links;
- external-effect records: repository creation requests/results,
  router owner orders, harness owner orders.

The daemon does not need a large actor rewrite before the executor
migration, but the direction should be Kameo actor planes rather than
a permanent `Mutex` service. The natural planes are store, ordinary
socket, owner socket, command executor, role registry, claim ledger,
repository registry, observer bridge, lock projection, router client,
and harness client. Empty actors should not be introduced merely to
name phases; each actor should own state, backpressure, or an
external boundary.

## Naming And Binary Shape

The current binary names are `persona-orchestrate` and
`persona-orchestrate-daemon`. The current intent for this component
names the user CLI as `orchestrate` and the daemon as
`orchestrate-daemon`. This should be corrected during migration unless
the psyche explicitly wants compatibility aliases.

The existing `RoleIdentifier` string-backed shape is right for
"roles are data." The next naming problem is that role, agent, job,
and run are starting to collapse into one object. The report 129
intent says Orchestrate should keep a registry of running agents with
specialized name, typed agent type, and short description. That is not
the same thing as a role/lane definition. The schema should not hide
that distinction in strings.

## Constraint Tests To Add

The migration should add source and behavior witnesses for:

- both contracts depend on current `signal-frame`, not the old macro
  revision;
- contracts use generated operation kinds and clean macro output;
- ordinary contract declares the observable block;
- no stale generic operation/effect observation vocabulary remains;
- `RequestUnimplemented` replies do not carry redundant operation
  fields;
- CLI uses generated head routing, not working-then-owner decode;
- CLI binary accepts exactly one NOTA argument and never opens store
  state;
- ordinary and owner sockets reject each other's frames;
- daemon path instantiates `signal_executor::Executor`;
- every accepted operation lowers to a non-empty command plan;
- commands implement `ToSemaOperation`;
- effects implement `ToSemaOutcome`;
- executor publishes operation-received before effect-emitted;
- engine errors return accepted batch aborts, not rejected requests;
- multi-operation and multi-command batches are rejected before commit
  until real transaction support exists;
- role creation records role, harness, report repository path, report
  lane path, and lock projection identity;
- repository refresh indexes local checkouts and creates workspace
  links;
- `bootstrap-policy.nota` is applied once and policy mutates only
  through the owner signal after bootstrap.

## Points Needing Intent Clarification

### Role versus agent versus job

Should `Role` remain the durable work identity and report lane, with a
separate `AgentRun` or `Agent` record for live sessions, specialized
names, typed agent type, harness, and context state? Or should a
dynamic role itself be the live agent identity? I recommend separating
`RoleDefinition`, `AgentRun`, and `Job` because the current intent
talks about role skill bundles, running agent reuse, and context
compaction as related but not identical concepts.

### Owner signal expansion

Should `owner-signal-persona-orchestrate` expose abstract job and
policy programming verbs now, or should the next slice stay limited
to mechanical role/repository/claim administration while
`persona-mind`'s contract is redesigned? I recommend not expanding
`Create` / `Retire` / `Refresh` blindly. The owner signal needs a
separate signal-tree design pass for job classes, policy programs,
agent assignment, scheduling, and failure handlers.

### Generic observation versus domain watch

Is the current `Watch(ObservationSubscription)` meant to survive as a
domain stream for role, claim, and activity changes, or should it be
deleted in favor of macro-injected `Tap` / `Untap`? I recommend
moving generic operation/effect observation to `Tap` / `Untap` and
only keeping `Watch` if it becomes a domain stream with Orchestrate
payloads such as role snapshots, claim deltas, activity entries, and
agent run changes.

### Owner operation visibility through Tap

Should ordinary-socket `Tap` subscribers see owner-socket operations
and effects? Existing intent says the public observer hook should
support introspection, but owner traffic can carry policy or authority
details. I recommend publishing owner operation classes and sema
outcomes through the ordinary observable stream while redacting or
omitting owner payload fields unless an explicit owner-authorized
subscriber model exists.

### Repository creation authority

Role creation intent says Orchestrate creates a report repository and
clones it into the Git index. Should the Orchestrate daemon perform
GitHub and `ghq` effects itself, or should it record the desired
effect and delegate execution to a repository-management or harness
executor plane? I recommend Orchestrate own the policy and durable
state, then execute external GitHub/`ghq` work through an executor
boundary whose results are recorded back into Orchestrate state.

### Timestamp shape

The contract still uses `TimestampNanos`. Runtime protocol timestamps
outside intent may remain machine fields, but report 150 calls
nanosecond precision suspicious. I recommend using slots for total
ordering and second-level time fields unless a component proves it
needs nanoseconds.

## Recommended Migration Order

1. Refresh `signal-persona-orchestrate` to current `signal-frame`,
   add the observable block, and decide the `Watch` fate.
2. Refresh `owner-signal-persona-orchestrate`, drop redundant
   unimplemented fields, and clean generated boilerplate.
3. Add `Command`, `Effect`, working lowering, owner lowering, and a
   shared command executor to `persona-orchestrate`.
4. Route both daemon sockets through `signal-executor`.
5. Replace the CLI with generated `signal_cli!` dispatch and rename
   binaries to `orchestrate` / `orchestrate-daemon` if no compatibility
   alias is required.
6. Add the constraint tests before expanding the owner signal beyond
   role and repository administration.

No implementation was changed in this pass.
