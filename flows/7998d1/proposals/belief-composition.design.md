# Design: Belief is composed, for a flow or a subagent

Author: Psyche core Fable (Fable 5.2). A worker assembles the presentation source from this file, in the in-place form, the module shown whole. Title: «Belief is composed, for a flow or a subagent». Kind: Proposal. Signature line: Created by Fable 5.2; a worker assembled the page. Wording marked ADD, REPLACE or COMMENT is final. Module: /git/github.com/LiGoldragon/psyche-belief/vision/belief-nexus-v1.md. Its sections from «## The ordinary single-reply boundary» to the end are not touched; they may be shown collapsed or left out if the builder allows, else as they stand.

His words, 12 November: «I'd also like to be able to configure everything. You could have the modules come from different repositories, so they're configured in the belief nexus. Getting a new basic belief module that can be completely configured would be like a per-call thing. We should keep these configurations saved somewhere, so that the new Flow Nexus version 1 could refer to these configurations. References can be per repo, which is more pure, or per local path, which is really dirty but can save us time when we're developing or debugging. Subagents should be composed of the same modules as well. Composing a subagent should be the same thing as composing a flow. It just has a different kind of effect. Their content would just be inserted with the delimiters of where each module starts and ends, so that the subagent is aware of where its beliefs come from. This is useful for self-awareness and self-debugging, knowing where and when their actions were probably influenced. Which belief modules are for its startup prompt, which for its system prompt, which are to become skills that are visible to it, or skills that are not visible to it. Any belief would be accessible through the belief nexus.» Whole: the transcript of flow 7998d1.

---

## Proposal 1: A composition names the placement · psyche-belief › vision/belief-nexus-v1.md

REPLACE, in the section «## Signal», only the changed words marked:
was: A module is named by kind and subject; its front matter names its placement, system prompt or skill.
becomes: A module is named by kind and subject; a composition names its placement.

REPLACE, in the section «## Meta», only the changed words marked:
was: A module's front matter names its placement; the default per Kind is a meta setting, set one value at a time, never in the Rust.
becomes: A composition names each module's placement; the default per Kind is a meta setting, set one value at a time, never in the Rust.

REPLACE, in the Library ethos, the Placement type:
was:
  Placement.[ SystemPrompt Skill ]   ; named in front matter;
                                     ;   default per Kind: meta
becomes:
  Placement.[ SystemPrompt           ; named by the composition; default per Kind: meta
              StartupPrompt          ;   in the first prompt
              VisibleSkill           ;   a skill the flow sees listed
              HiddenSkill            ;   a skill it is not shown
              Held ]                 ;   reached through the Belief Nexus alone

ADD, to the Library ethos types, after ModuleName:
  CompositionName.String
  Placed.{ ModuleName Placement }
  Composition.{ CompositionName      ; a saved configuration of belief
                Vector<Placed> }
  SubagentName.String
  Target.[ Flow                      ; furnished as a flow's prompts and skills
           Subagent.SubagentName ]   ; furnished as one subagent file, for the flow of that workspace

REPLACE, in the first Signal ethos, the Furnish input:
was:
  Furnish.{ Workspace Harness        ; the harness's
            Vector<ModuleName> }     ;   skills directory
becomes:
  Furnish.{ Workspace Harness        ; the harness's skills directory
            CompositionName Target }

ADD, in the first Signal ethos: to its imports, CompositionName, Composition and Target; to its inputs, after Register:
  Compose.Composition                ; a composition saved, or replaced, under its name
to its outputs, after Registered:
  Composed.CompositionName
and to Refused:
            UnknownComposition.CompositionName

ADD, a new section after the section «## Library»:
## Composition

Everything about belief is configuration. Modules come from several sources at once, each configured in the Belief Nexus: a repository, the pure reference, or a local path, the quick one, for developing and debugging.

A composition is a saved configuration of belief: the modules, and for each its placement: the system prompt, the startup prompt, a skill the flow sees, a skill it is not shown, or held in the Belief Nexus alone. Every belief is reached through the Belief Nexus. A composition is kept in the Belief Nexus under its name, and a definition in the Flow Nexus refers to it by that name.

A subagent is composed as a flow is, from the same modules, by a composition. The effect differs: the composition is written as one subagent file, for the flow it is intended for.

Each module's content is inserted between delimiters that name it, where it starts and where it ends, so a flow or a subagent knows where each of its beliefs comes from, and which one probably influenced an action.

```datom
Compose.{ reviewer
          [ { { Spirit core } SystemPrompt }
            { { Intent design } SystemPrompt }
            { { Vision ethos } StartupPrompt }
            { { Knowledge search } VisibleSkill } ] }
Composed.reviewer
Furnish.{ /home/example/workspace Claude reviewer Subagent.reviewer }
```

```markdown
<!-- module: spirit:core -->
The purpose of a thinking machine is to extend a living psyche.
<!-- end-module: spirit:core -->
```
