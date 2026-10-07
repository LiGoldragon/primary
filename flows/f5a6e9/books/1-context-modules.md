<!-- to-the-living:start -->
Presentation.{ «Context modules» }

The Intent text before you in «Context modules, into Intent» is the ground of this book; nothing here restates it. This book is the design under it: what a module is, how its chain loads, where Flow keeps the registry, where a module lands, and how a launch names modules.

## 0. Your comments, answered where

"the whole context modules concept has been completely omitted": this book is the concept, placed at the top of Flow's design; book 2 (the metaflow) and book 3 (stored types) are written under it. "95%+ of the context that we feed it will come from modules": section 5 measures the leverage as it is today and names where the growth goes. "Where is the canonical place to find those types?": section 1, one Library root.

## 1. The module

A context module is one file of prompt text with a name, a facet, a description, and the names of the modules it rests on. It exists today: 71 authored skills in Curriculum, each with `description` and, in 67 of them, `dependencies` in its frontmatter. What does not exist is the type in one place, a registry, a placement, and a loader that follows the chain.

The types are declared once, in Curriculum's Library root; Flow imports them the way it imports signal-flow today, and curriculum-deploy generates from the same root. No second list anywhere.

```
Library              ; Curriculum's
[]
[ Name.String        ; the file's name
  Facet.[            ; of awareness
    Spirit
    Intent
    Vision
    Knowledge
    Operation ]
  Module.{
    Name
    Facet
    Description.String
    ; loaded with it, before it
    Dependencies.Vector<Name>
    Location.[
      Path.String    ; absolute
      Text.String ] }  ; the words
  Placement.[
    SystemPrompt     ; top stratum
    FirstPrompt      ; middle stratum
    Loadable ] ]     ; the catalog
[]
[]
```

Facet is the word offered for what you called the aspects of awareness, since aspect is taken. The five facets are the five you named. A notion is not a facet: it binds nothing, so no flow starts its thinking from it; it stays in the flows' notion records.

Today the type rides in the file name: vision-, knowledge-, operation-, trial-, compensation-, psyche-. Under this design the facet is a field; the prefix stays in the name only where it carries meaning. A trial and a compensation are operations of a kind, so `trial-no-polling` is an Operation named trial-no-polling; `datom`, `protos`, `lojix`, `testing` are Knowledge; `main-flow`, `edit-coordination` are Operation; `spirit` is Spirit; `vocabulary` is Vision.

## 2. The chain

Measured over the 71 skills: the `dependencies` field gives 52 edges. Naming the six startup skills of this flow loads nine through the chain, 19,472 bytes becoming 23,304 (about 4,900 to 5,800 tokens). The whole set is 125,610 bytes, about 31,000 tokens. The chain is shallow because skills were written to be loaded one at a time, with "Load the spirit skill" in prose; the field already carries what the prose says.

Rule: a module's dependencies load with it, before it, so its words land after what they rest on; each module loads once per flow, at the strongest placement any module that needs it was given (SystemPrompt over FirstPrompt over Loadable); a cycle is refused at registration, and a dependency not in the registry is refused too. Naming seven loads thirty-seven when the knowledge modules rest on each other as code does; nothing in the rule changes between today's nine and that.

## 3. The registry is Flow's Memory

```
Memory
[ curriculum:[ Module Name ] ]
[ Module ]           ; one per Name
```

```
Signal               ; the meta socket
[ curriculum:[ Module Name ] ]
[ Register.Module
  Forget.Name
  Modules ]          ; the whole registry
[ Registered.Name
  Forgotten.Name
  Modules.Vector<Module>
  Refused.[
    Unknown.Name     ; a dependency
    Cycle.Vector<Name>
    NoFile.Path
    Relative.Path ] ]
[]
```

Location, your pros and cons: a path is live (edit the file, the next launch reads it, nothing re-registered) but a relative path breaks; text is self-contained but stale until re-registered. Proposed: Path now, absolute only, refused otherwise; Flow reads the file at compose time and records in the flow record the content hash of what it composed (the hash newtype of book 3), so what a flow actually read is known afterwards. Text stays in the enum for a module that has no file of its own.

Who registers: curriculum-deploy, the one program that already reads every authored file, registers the whole set at each deploy. Flow scans no directory.

## 4. Placement

What each placement is on each harness, witnessed in Flow 0.24.0:

Claude. SystemPrompt: Flow passes a system prompt file that replaces the stock prompt whole. FirstPrompt: one line of at most 800 characters, opening with up to five stacked `/skill` tokens the harness expands into the conversation. Loadable: the skills catalog, whose names and descriptions the model sees every turn and loads through the Skill tool.

Codex. SystemPrompt: Flow keeps the stock base and places the bundle text at the top of the first turn; the key that replaces the base instructions with a file exists and is unused. FirstPrompt: skill input items and the prompt text. Loadable: the catalog the app-server lists.

A module placed in SystemPrompt or FirstPrompt for a flow and absent from its catalog is what `Intent/startupPrompt.md` calls a startup skill; today the `user-only` flag hides it. Under this design hiding is nothing but a module that is placed and not Loadable; the flag goes when the catalog is composed per role.

Which modules qualify for the system prompt, your open question. Two facts decide it. The harness sends the system prompt whole with every call and compaction never rewrites it (claim from how the harness works); compaction rewrites the conversation, where the first prompt and loaded modules sit: one flow went from 436,667 to 15,332 tokens in a single compaction, witnessed in its transcript. And every token in either place is paid on every turn.

Rule proposed: words that must hold for the whole flow on every turn, Spirit, the role's Operation, vocabulary, go in the system prompt; words about this flow's task, the subject's Vision and Knowledge, go in the first prompt, where a refresh replaces them and compaction may condense them; what is needed on occasion stays Loadable.

## 5. The role and the launch

A flow has a flow id and a role, one of which is a voice; the role record carries the placements, so a launch repeats none of them.

```
Role.{
  Voice.{
    Aspect
    Layer }
  Model.String
  Placements.Vector<
    Placed.{
      Placement
      Names.Vector<Name> }> }
```

```
Launch.{
  Voice              ; the role, by name
  ; this flow's own, first prompt
  Modules.Vector<Name>
  Brief.String }     ; a small paragraph
```

Written, a launch of this seat for this work:

```
Launch.{
  { Psyche Primary }
  [ vision-flow
    knowledge-ethos ]
  «Design Flow's module registry.» }
```

The composed context, in order: for each placement, the role's names in role order, then the launch's names, each preceded by its dependencies not yet placed, none twice. The launch's own modules land in the first prompt: a launch adds this flow's topic, the role owns what stands. The metaflow field of a launch is book 2's.

Leverage as it is: the launch line is about 200 tokens; today's six startup modules make 5,800 tokens through the chain, about 30:1; the whole catalog would make 150:1. The 1,000:1 you want is not reached by the mechanism alone but by the corpus: 31,000 tokens of modules today, where the knowledge of each repository, each design and each ruling is what grows it.

## 6. Curriculum and Flow, one standard

Curriculum authors a module: its file, with `description`, `facet` and `dependencies` in its frontmatter until your word on an `index.datom`; curriculum-deploy generates each harness's catalog from it and registers it in Flow. Flow composes from the registry and the role, never from paths a caller writes by hand. The name Curriculum stays.

## Rulings

1. The module and the placement types, declared once in Curriculum's Library and imported by Flow: yes, or amend.
2. The word for the type: (a) Facet. (b) Faculty. (c) your word.
3. The five facets, trial and compensation modules as Operation, no Notion facet: yes, or amend.
4. The chain rule of section 2: yes, or amend.
5. Location: (a) absolute Path now, the content hash recorded at compose, Text kept in the enum. (b) both now.
6. The placement rule of section 4: yes, or amend.
7. The role carries placements; a launch names the voice, its own first-prompt modules, and a brief: (a) yes. (b) a launch's modules carry a placement too.
8. curriculum-deploy registers the whole set at deploy over the meta socket; Flow scans nothing: yes, or amend.
<!-- to-the-living:end -->
