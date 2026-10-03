# The tailor-made subflows

Opus counted: two thousand one hundred dispatches in two weeks, eleven names, and only one of them — the book — made for its work. Everything else was briefed from scratch each time. Here is the set, each a role in the context-module standard: a role module for its identity, a configuration naming what it carries, a cheap model. The brief then carries only the task.

## 1. What a tailored subflow is

A role whose definition already holds everything the work needs: the role text, the skills it loads, the files it may write, the model it runs on. Launching it is naming it and giving the task in a line.

Drawing: one role card with four bands — role text, skills carried, writes allowed, model — and beside it a one-line brief arrow pointing at it.

## 2. The set

Three kept as they are: the three read tiers and three write tiers, and the tester. Added, by how often the work recurred:

- **book** — a presentation or flashbook from the caller's transcript or brief, hand-drawn SVG, generator-checked ethos, fresh artifact; carries the flashbook and illustration skills. (218 dispatches)
- **psyche search** — finds the living's words on a topic across records and transcripts, returns them verbatim with provenance; carries psyche, psyche-acquisition, transcript-search. (112)
- **comment reader** — fetches the living's comments on books, verbatim with anchors, marks the newest; carries the messenger-reading knowledge. (22)
- **launcher** — launches a flow or a successor, registers it, titles it, witnesses it running; carries trial-succession, knowledge-flow, claude-harness. (84)
- **reaper** — retires or reaps a flow with an evidence file; carries trial-reaping, trial-succession, messenger. (28)
- **witness** — observes a lock, a seat, a socket, a running set, and writes a witness file with its method; carries flow-evidence, knowledge-nexus, orchestrate. (91)
- **deployer** — Home, CriomOS and Lojix deployments with rollback kept and the running set witnessed after; Field only; carries nix-workflow, lojix, breaking-upgrades. (105)
- **skill lander** — lands one approved line in a Curriculum skill, regenerates, projects to Primary; carries skill-designing, file-editing, trial-generated-projection. (28)
- **ethos checker** — runs the generator on an ethos file and returns the rejection and the smallest correction; carries knowledge-ethos, vision-ethos.
- **disk hygiene** — reclaims space and GC roots without losing work; carries disk-hygiene. (19)
- **researcher** — authorized web research with sources, prior art in three lines each; carries behavior.
- **gatherer** — collects psyche records across flows that could distil together, never composes; carries psyche-distillation.

Gone as subflow work, by your rulings: sending a message (the main flow sends), relaying your words (the relaying skill, the main flow sends), publishing to main (the Field publisher seat).

Drawing: a grid of thirteen tiles, each with the role name and a small glyph (a book, a magnifier, a speech bubble, a rocket, a scythe, an eye, a crane, a pen, a check mark, a broom, a globe, a basket, a flask), coloured by family: reading roles, writing roles, Field roles.

## 3. In the standard

Each is a Role variant; its configuration in Flow's memory names its modules per placement and its model. The generator writes the agent definition from that record, so the definition and Flow's launch read the same source.

```
Library                              ; the roles, as variants of Role
[]
[ Role.[ Voice.{ Aspect.[ Psyche      ; a voice: an aspect and a layer
                          Mind
                          Field ]
                 Layer.[ Primary
                         Secondary
                         Tertiary
                         Quaternary ] }
         SystemAudit                 ; focused roles, run once
         LivingInteraction
         Implementation
         VisionAudit
         ReadTrivial                 ; the reading tiers
         ReadOrdinary
         ReadDemanding
         WriteTrivial                ; the writing tiers
         WriteOrdinary
         WriteDemanding
         Tester
         Book                        ; the tailor-made set
         PsycheSearch
         CommentReader
         Launcher
         Reaper
         Witness
         Deployer
         SkillLander
         EthosChecker
         DiskHygiene
         Researcher
         Gatherer ] ]
[]
[]
```

The book role, as one configuration record:

```
{ Book                                           ; the role
  [ { SystemPrompt [ { Role [ book ] }            ; its identity text
                     { Operation [ flashbook      ; what it does
                                   flashbook-illustration
                                   book ] }
                     { Knowledge [ ethos ] } ] }  ; the generator it checks with
    { FirstPrompt [] }                            ; the brief is the task only
    { Loadable [ { Compensation [ messenger ] } ] } ]
  claude-sonnet-low }                             ; a Quaternary model
```

## 4. What happens next

Mind writes the twelve role modules and configurations into Curriculum's manifest; the generator produces the definitions for both harnesses; Field deploys; every main flow then launches them by name with a one-line brief.

1. Build the set as drawn.
2. Add or remove roles — name them in a comment.
3. Change what a role carries — name the role and the change.
