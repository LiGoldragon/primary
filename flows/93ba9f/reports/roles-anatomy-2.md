# Configured flow roles — anatomy, second draft

Psyche Opus 93ba9f, 2026-09-26. Redrawn after the living's correction: data belongs in variants, effort is the model's data, harness optional, layer vocabulary primary/secondary/tertiary/quaternary.

## The living's words this rests on

- "Oh and I think you're right on the layer words: it's primary, secondary, tertiary, quaternary. That's the vocabulary I was actually looking for." (STT, 2026-09-26, to e167d8)
- "You have a set of roles and they all have their model effort already set so you don't have to make it up. You just start the same old premade templates, like: the psyche fable, the psyche, the psyche primary, the psyche secondary, the psyche tertiary, the psyche quaternary. The same for the mind. Then you set the model if it's not set. It's just the default, which is medium, but datom is explicit." (STT, 2026-09-26, to e167d8)
- "When you're talking about the effort, there are different effort levels for different models so it's a property, the data of the model variant." (STT, 2026-09-26, to 93ba9f)
- Intent (distilled): harness calls go out at medium effort by default; effort may be set light where a task needs speed, voice among them; never raised to buy quality.

## What already exists

The Curriculum repository already has a models list in datom, each model with its provider and the efforts it supports. Today every model, Claude and Codex alike, declares Low Medium High Xhigh. No model runs in both harnesses. Terra is out.

## Anatomy

```
Aspect.[ Psyche Mind Field ]
Layer.[ Primary Secondary Tertiary Quaternary ]
Seat.[ Psyche.Layer Mind.Layer Field.Layer ]
Effort.[ Low Medium High Xhigh ]
Model.[ Fable.Effort Opus.Effort Sonnet.Effort Haiku.Effort Astra.Effort Sol.Effort Luna.Effort ]
Source.[ File.Path Vision.Topic Skill.SkillName Mind.Reference ]
Role.{ Seat Model Vector<Source> }
Roster.Vector<Role>
```

A role written as datom:

```
{ Psyche.Primary Opus.Medium [ Skill.main-flow Vision.messaging ] }
{ Field.Quaternary Luna.Low [ Skill.main-flow ] }
```

- The seat is a variant of the aspect carrying its layer: `Psyche.Primary`.
- The model is a variant carrying its effort: `Opus.Medium`. If Claude and Codex ever support different efforts, each model variant carries its own harness's effort type instead of the shared one.
- The harness is not written: each model names its harness. It is added only if one model ever runs in two harnesses.
- Source is what is added to the new flow's first prompt, one variant per kind of source. `Mind.Reference` waits for the Mind Nexus.
- A launch names a seat. Flow refuses a second live flow on a seat; replacing a seat stops the old flow first. A seat at an effort above medium exists only if the living writes one into the roster.

## Questions

1. The template list names "the psyche fable" and "the psyche" beside the four layers. Is Fable just the model of one layer's seat (for example `Psyche.Primary Fable.Medium`), or are "the psyche fable" and "the psyche" seats of their own, above the layers?
2. Is every seat exactly one live flow?
3. Is this the shape you meant — the seat as the aspect variant carrying its layer, the model variant carrying its effort?
4. Besides a file, a vision topic, a skill and a Mind reference, what kinds of prompt source are there?
5. Three instruction lines await your approval:
   - psyche-interraction, new line: "A question about a type's shape shows its Ethos declaration: every variant of every type it names."
   - main-flow, replacing "The living never types a startup command": "The living never starts, closes, or types into a harness; a flow never hands such an act to the living."
   - psyche-interraction, new line: "After a presentation that asks the living to rule, a Sonnet subflow publishes it as a Claude Artifact, and the reply carries the link."
