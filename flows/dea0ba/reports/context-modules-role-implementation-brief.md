# Context standard: Flow and Curriculum implementation contract

Governing source: [Curriculum: the context standard](../../edf227/books/curriculum-the-context-standard.md).
This supersedes the earlier context-module brief. It carries no compatibility
shape and does not wait for every open choice.

## Living basis

> I think that the flow definition itself is a struct, and one of its fields is
> a role. The role is an enum, and one of its variants is voice. The other
> variants are going to be all the other roles that we create: a system audit;
> live psyche voice interaction; an implementation; an implementer; a vision
> audit. ... main flows ... pass everything to a sub-agent, but eventually all
> the sub-agents will themselves be flows, so that we have a fully asynchronous
> system.

— psyche, STT, 2026-10-03, [vision source](../vision/subflows.md).

## Required shape

## Exact shared types

```ethos
Library
[]
[ ModuleType.[ Spirit Intent Vision Knowledge Compensation Trial Operation Role ]
  Name.String
  Location.[ Path.String ]
  Module.{ ModuleType Name Location }
  Manifest.Vector<Module>
  Placement.[ SystemPrompt FirstPrompt Loadable ]
  Selection.{ ModuleType Vector<Name> }
  Placed.{ Placement Vector<Selection> } ]
[]
[]

Memory
[ flow:[ Role Placed Model Module ] ]
[ RoleConfiguration.{ Role Vector<Placed> Model }
  Registry.Vector<Module> ]
```

`ModuleType` names prompt provenance and permitted placement; it is not an
Ethos kind. A module name is unique within its type. `Reference` is not a
separate governing type in this book: a selection's `(ModuleType, Name)` is the
registry lookup key. Registration updates the location of that exact pair only.
Forgetting likewise requires that exact pair; it never removes another type's
same-named module.

## Registry key semantics

The registry key is exactly `(ModuleType, Name)`. Register inserts a new pair
or atomically updates the `Location` for that same pair only. Forget requires
the same pair and reports an unknown exact pair when absent; there is no
name-only operation or ambiguous fallback.

The book's numbered open choices remain open and are not implementation gates:
loadable-on-demand later, repository/revision locations later, and comments
requesting changes. Build the drawn path now.

### Superseded working shape retained for provenance

The earlier brief called the pair `Reference.{ ModuleType Name }` and named
`Register.Module` / `Forget.Reference`. That is a useful record of the
exact-pair safety requirement, but it is not the current governing type shape:
the context standard uses the selection pair as the lookup key. Its former
implementation ownership and typed-harness-identity MVP statements are
superseded by the current Flow/Curriculum boundary above.

## Flow slice — implementation owner

`Flow.{ Role ... }` uses a Role enum with `Voice.{ Aspect Layer }` plus focused
roles such as SystemAudit, LivingInteraction, Implementation, Implementer, and
VisionAudit. Future subagents are independent asynchronous Flows.

At `Launch.Role`, Flow reads `RoleConfiguration`, resolves its ordered
`Placed` selections from `Registry`, reads the paths, concatenates
SystemPrompt and FirstPrompt selections in declared order, and provides the
loadable selection to the harness-specific generated tree. This is deterministic
code: no model chooses, checks, or rearranges modules.

Compiled role definitions carry the standing role instructions. Launch supplies
`FLOW_ID` and `FLOW_DIRECTORY` through trusted launcher environment/lane marker;
the main brief carries task-only values, not repeated identity or skill preamble.
Environment values alone do not authorize callers: trusted launch/process
attribution remains required.

Preserve native first-turn constraints: one actual first turn, no dummy turn,
no reopened control session, and no claimed subagent inheritance without a
harness witness.

## Curriculum slice — implementation owner

`curriculum-deploy` is the other reader of the same Registry. It validates the
single Curriculum Manifest, registers its Modules over Flow's meta surface, and
generates from that Registry:

- Claude loadable `.claude/skills` and Codex `.agents/skills` trees;
- Claude agent definitions whose bodies are the role's SystemPrompt selections
  and whose skills field preloads its Loadable selections;
- Codex custom agents with the role's developer instructions.

No launch brief, hand-edited prompt, or second registry duplicates this data.
The generator alone knows vendor mapping; Flow knows roles and placements;
Curriculum authors modules and the manifest.

## Source implementation boundary

Opus 28d847 owns generation, implementation, and tests in the accepted
Flow/Curriculum source boundary. It must extend the existing meta/context
surface rather than create a parallel wire candidate. Field 42265e is the
witness seat; db38f8 publishes. Mind reviews concrete source and tests after
the implementation slice is available; this is not an added approval gate or
implementation stall.

Minimum tests: same Manifest drives registration and both generated trees;
SystemPrompt, FirstPrompt, and Loadable preserve declared order; a focused role
gets its generated definition and task-only brief; same-name modules in two
types resolve independently; an exact-pair removal affects only that pair; and
an independent role Flow receives no parent authority.
