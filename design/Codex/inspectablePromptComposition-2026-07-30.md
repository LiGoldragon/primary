# Inspectable prompt composition

## Psyche ruling — 2026-07-30

Agent text answered:

> A defensible arrangement would be:
>
> - Per-model data: only small, measured behavior corrections required by that
>   model.
> - Shared user policy: coding autonomy, scope, validation, communication style,
>   and destructive-action policy—maintained by you.
> - Runtime protocol: available channels, rendering capabilities, session state,
>   and tool mechanics generated structurally when needed.
> - Hard enforcement: permissions, sandboxing, credentials, and tool restrictions
>   outside the prompt.
>
> A brutally minimal shared default:
>
> You are a coding agent working in the user’s workspace. Follow the user’s
> request and applicable repository instructions. Inspect and report without
> changing state unless a change is requested. For requested changes, preserve
> unrelated work and run proportionate validation. Require authority for
> destructive, external, costly, or scope-expanding actions. Report the outcome,
> evidence, caveats, and blockers.

The only natural-language instructions that may belong to a model by default are
instructions justified by that model. Other policy is not made valid by being
built in.

Prompt policy is composed from independent segments rather than delivered as one
opaque body. Each segment can be inspected, maintained, selected, and removed on
its own.

Terms such as `costly`, `destructive`, `external`, `scope-expanding`,
`authorization`, `unrelated work`, and `proportionate validation` are defined by
observable boundaries. They are not left as adjectives for the model to
interpret freely.

Brevity is a design constraint. Addition dilutes the force of every instruction,
so a segment earns prompt space only through a documented requirement or a
measured failure that it corrects.

Pi’s built-in prompt is a comparison baseline for this design, not its authority.
