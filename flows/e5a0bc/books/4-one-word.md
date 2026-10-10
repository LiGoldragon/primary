Presentation.{ «One word for skills and subagents» }

A skill is text read into a flow's context at a placement. A subagent is a role launched as a fresh flow: a model, its placed modules, a permission. Both are one thing from the caller's side: something the flow can call on. In the role record of «Context modules» they already share a shape, so the umbrella is one type with two variants:

```
Library                                   ; Curriculum's Library
[]
[ Placement.[ SystemPrompt
              FirstPrompt
              Loadable ]
  «Term».[ Skill.{ Name.String            ; read into the calling flow's context
                   Placement }
           Subflow.{ Name.String          ; run in a fresh flow, its own context
                     Role } ] ]           ;   the role record: model, placed modules, permission
[]
[]
```

Written, the two the book work uses:

```
Skill.{ operation-book Loadable }
Subflow.{ book { Voice.{ Psyche Secondary }
                 [ { SystemPrompt [ { Operation [ subflow-role operation-flashbook ] } ] } ]
                 { claude-sonnet None } } }
```

The pre-prompted book subagent is the second line: what the brief repeated moves into the `operation-flashbook` module of that role, and the brief shrinks to the title.

## The word

| term | for | against |
|---|---|---|
| Faculty | a mind's powers, as speech or sight are; unused anywhere in psyche or code | — |
| Capacity | your first word | names load in the metaflow notes: "more or less capacity" |
| Capability | your second word | already a term of ethos: a kind is the bearer of capabilities; you ruled once that skills are not capabilities |
| Power | the force a flow can call on | names the power tier: `PowerLevel.[ High Medium Low UltraLow ]` |
| Śakti | the Sanskrit ontology you are heading into: power as what a being can do | a loan word in every skill line |

## The vocabulary line

`Curriculum/skills/vocabulary.md`, after "Illustrated book".

Proposed:
> «Term»: what a flow can call on: a skill, read into its own context at a placement, or a subflow, a role run in a fresh flow. A subagent is a subflow.

## Rulings

1. The umbrella as one type, `«Term».[ Skill Subflow ]`, on the role record: yes, or amend.
2. The term: (a) Faculty. (b) Capacity. (c) Capability, and ethos's word for a kind's bearing changes. (d) Śakti. (e) another.
