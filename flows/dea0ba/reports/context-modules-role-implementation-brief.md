# Context modules and Flow roles: implementation brief

## Living basis

> I think that the flow definition itself is a struct, and one of its fields is
> a role. The role is an enum, and one of its variants is voice. The other
> variants are going to be all the other roles that we create: a system audit;
> live psyche voice interaction; an implementation; an implementer; a vision
> audit. ... main flows ... pass everything to a sub-agent, but eventually all
> the sub-agents will themselves be flows, so that we have a fully asynchronous
> system.

— psyche, STT, approximately 2026-10-03 19:15Z,
[vision source](../vision/subflows.md).

The context-module contract follows the four-root anatomy source: a module is
`Module.{ ModuleType Name Location }`; its registry identity is
`Reference.{ ModuleType Name }`. `ModuleType` is distinct from an Ethos kind
and includes Spirit, Intent, Vision, Knowledge, Compensation, Trial, Operation,
and Role. Meta registration and forgetting retain `Register.Module` and
`Forget.Reference`.


## Required shape

`Flow` becomes a struct containing `Role`. `Role` is an enum whose first
variant is `Voice.{ Aspect Layer }`, with focused roles including SystemAudit,
LivingInteraction, Implementation, and VisionAudit. `Aspect` is Psyche, Mind,
or Field; `Layer` is Primary through Quaternary. `Psyche.Primary` is a Signal
display projection, not a type variant. New roles are additive variants. Future
subagents are independent asynchronous Flows; they are not an authority
extension of their parent or an assumed native subagent.

Context modules configure each role through ordered `Placed` groups for
`SystemPrompt`, `FirstPrompt`, and `Loadable`. Each group contains an ordered
vector of `Selection.{ ModuleType Vector<Name> }`: a ModuleType occurs once per
group, and name order is insertion order. Flow resolves every selected
`(ModuleType, Name)` through the separate registry to its `Location`, rejects a
duplicate reference before a turn, and inserts only the resolved text at the
selected placement. Model, harness, and effort selection are separate
Flow-owned Memory/database meta configuration, not a Markdown context module
or knowledge skill. For the MVP, Flow identity remains the existing typed
harness-hash identity; word rendering is deferred and does not gate launch. Existing native first-turn constraints remain: one actual
first turn, no dummy turn, no reopened control session, and no assumption that
subagents inherit or omit a module without a harness witness.

## Registry key semantics

`Reference.{ ModuleType Name }` identifies a module. The registry key is
exactly `(ModuleType, Name)`. `Register.Module` atomically inserts a new pair
or updates `Location` for that same pair; it has no effect on another module
with the same name.

`Forget.Reference` removes only the exact `(ModuleType, Name)` pair and returns
`Unknown.Reference` when absent. There is no name-only operation or ambiguous
fallback.

## Source implementation boundary

Field is the sole builder. The earlier direct Field handoff returned an
uncertain Messenger timeout and is not evidence of delivery; it is not retried.
For source retrieval, Field should inspect the accepted current Flow source and
extend its existing meta/context surface rather than create another parallel
prompt-composition wire candidate. Mind reviews the concrete key semantics,
Role/Flow data shape, and first-turn-preservation tests.

Required test cases: group order and name order produce deterministic insertion;
a ModuleType occurs once per placement; a duplicate `(ModuleType, Name)` refuses
before a turn; `Forget.Reference` removes only that key; and an independent
role Flow cannot receive ungranted parent authority.
