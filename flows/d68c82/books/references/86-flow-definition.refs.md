# References: How a flow is defined

## The living's words

- flows/d68c82/vision/flow.md, "A flow is specified whole, in Datom"; "A lean flow: a judgment-only call whose response is its message"; "Flow starting configured in EDN, per aspect and per metaflow"; "Roles defined as datom data in their own repository" (2026-10-16 11:25: a different directory from the cluster data, a different repo); "A role may call a subagent model one rung up"; "A subflow's kind depends on its use"; "Lean flows: everything removable is a named module"
- flows/d68c82/vision/ethos.md, "A specification groups its items by variant"; "Comments on the Ethos syntax" (root a capitalised variant; not yet in files)
- flows/d68c82/vision/context-modules.md, "Subagent definitions composed from their context modules"
- flows/da2038/vision/flow.md: flow definitions as a special dialect of datom ethos
- flows/39bd0c/books/04-flow-the-design.md P3 and flows/804eb9/books/ethos-book-proposals.md P6: earlier proposals of a definition (older syntax, not used)

## Current modules, origin main 12f2558

- psyche-context vision/flow.md shown whole; no line there names the lean flow beyond "clean lean flows" (line 14)
- psyche-context vision/ethos.md "Shapes and placement": Signal vectors, queries then responses, one variant each
- mind-context inquiry/subflow-token-cost.md and psyche-context vision/inquiry.md: inquiry form

## Witnessed in code (read subflow)

- Curriculum origin/main 6596814: curriculum.ethos lines 36-42 (RoleDefinition has nine fields: RoleName Surface ModelId Effort Permission DescriptionModule ContextModules RoleTools RoleCallers); roles.datom line 26 (book row: sonnet Medium Unrestricted, modules spirit-core intent-context role-book-publishing-procedure vision-book compensation-book-crystallization, tools Read Bash Agent Artifact, callers Any); the common subflow module list repeated in each of 29 rows; illustrator tools Explicit.[]
- signal-flow 6a49664 ethos/signal.ethos 240: LaunchProfile.{ id SystemModules UserModules Address ModelName Effort ... LeaveOuts InstructionPrompt }; harness derived from model (flow-nexus codex.rs 94-102); wake effort fixed medium (waking.rs 85); live per-layer model table (meta-signal-flow ConfigureModel)
- Primary config/main-flow/psyche.edn: Psyche Secondary claude-opus-5-5 medium; lean example model claude-fable-5-1 is the Primary voice
- SKILL_VARIABLES.md: three Psyche Secondary Claude model variables; models stated in four places
- Agent files: only book and illustrator render from Curriculum today; the others were written by a retired projector (Curriculum af528cd)

## Checks

- ethos blocks checked by the pinned main ethos-zero (07714b0) as Library roots; datom blocks are balance-checked only by the builder
- Not witnessed: the lean flow's user modules, a main flow's real user-module list (shown as []), the lean example's effort and module list: example values

## Proposals

- 1: flow.md addition; 2: ethos.md addition; 3: new vision/flow-definition.md with worked example, figure 1; 4: new mind-context inquiry/flow-definition.md, figure 2
