Presentation.{ «Skills and Curriculum» }

Where skills are written, who stands behind each kind, how they speak, and the tool that turns them into what each agent program reads. A skill is a written set of instructions an agent loads for a kind of task. Curriculum is the tool that generates skills for each harness, meaning each agent program, such as Claude or Codex. The three aspects of the psyche are psyche (his vision), mind (designs and knowledge) and field (builds and runs things).

## Part 1. What he wants

### The vision is the skill

The distilled vision is the skill. What he says is stored once, and the skills are generated from it.

> And that vision becomes skills. It's the same thing, right? The data ends up in the skill.

-- spoken, 3 October

> That's what vision distillation is now, because when you distill vision, you put it into a vision file, which is a skill. I want that whole knowledge/vision/operations/everything logging to be the source that we use to generate our skills. We only store the stuff once, and we have different rules for who can edit what and what type.

-- typed, 3 October

### Three source repositories, one per aspect

The skills are written in three repositories, one for each aspect: psyche, mind and field. Each aspect is in charge of its own. Curriculum holds none of them. Where exactly the text is written is question 1.

The repositories were meant to keep the distilled part apart from the logs.

> Each of these repos is actually where I think we should keep the distilled part separate. We could have another repo for psyche logs, mind logs, and field logs for the actual logs.

-- typed, late September

A flow, a running agent session, that wants a change in another aspect's skills asks that aspect. A change to psyche's skills goes to him.

> If he wants to change, if he has a suggestion or a need for a change in any other skill, he has to message the corresponding aspect so that that aspect can investigate and analyze the merits of the suggestion. If that suggestion is toward Psyche, then obviously Psyche is going to have to bring it up to the Living.

-- 28 September

### Kinds of skill, and who stands behind each

Every skill has a kind, and the kind says who approved it. Psyche holds the vision, approved only by him. Mind holds operation and knowledge. Field holds compensation and trial.

> I want to point out that operation and documentation would be for Mind and tests and compensation would be for field.

-- spoken, 28 September

> We would have what we call the golden skills, basically the vision of what I want to see or what I see as the desired result. It's only approved by psyche, which means approved by the living psyche.

-- spoken, 28 September

An operation skill is deployed on his description; he does not need to read it.

> they can be deployed essentially on me saying, "Okay I want an operation skill that does this" or "I want an operation skill to be modified to do this." I don't need to glance because I basically told them what I want. It's a low-effort skill.

-- spoken, 28 September

A trial skill is a candidate, named with the trial prefix; it becomes compensation once it has proven itself.

> A test skill is like a skill that's being tested for how useful it can become as a compensation skill.

-- spoken, 28 September

Knowledge is the Mind kind that holds what is true now; documentation becomes knowledge.

> We have operation and/or maybe knowledge.
> - Documentation becomes knowledge.

-- typed, 2 October

Every skill carries its kind in its name. The generator adds the prefix, from the source's declared aspect and kind, never typed by hand into a file name.

> We would prefix all the skills and then we would know what all skills are.

-- spoken, 28 September

### A skill leans only on what is above it

A skill may depend only on its own kind or a higher one.

> a vision can only depend on something above it, like an intent or spirit, or another vision. Operation can depend on vision or anything higher and this goes all the way down: documentation, operation, and then whatever the hierarchy is in the field, which is trial at the bottom

-- spoken, 29 September

### Skills speak in layers

No skill names a model. Skills say primary, secondary, tertiary, quaternary, meaning the layers of agents from the most capable down. One knowledge skill says which model holds each layer today.

> Let's make sure that all the skills refer to layers

-- typed, 3 October

> Yeah let's make it four layers and we can make the quaternary layer be equivalent to Sonnet low effort and Luna low effort in the two different stacks.

-- typed, 3 October

### Many sources for any kind

Curriculum takes more than one source of the same kind, so people can bring their own and borrow others'. It refuses to write when two sources define the same skill.

> I also want curriculum to support generating skills from more than one source for any type so people could:
> - write their own knowledge skills
> - in a plugin kind of way use other people's knowledge skills and some people's vision skills

-- typed, 3 October

### A recurring failure means a skill lacks a line

When the same thing goes wrong twice, the fix is a line in a skill.

> See, every time there's a failure like that, it means that something wasn't written to a skill.

-- spoken, 3 October

The lines arrive as a steady stream of small proposals, each answerable with a yes.

> I want skills that do skill edits. I want a constant flow of small skill edit proposals, not huge ones, so that I can say yes quickly.

-- typed, 3 October

### Context modules: one standard for skills and the system prompt

A skill is one kind of context module. The same modules can go into the system prompt, into the prompt, or stay loadable. Flow, the program that launches and tracks flows, keeps a registry of modules by type, name and location. A launch names, per type, the modules it wants, and Flow inserts them. Curriculum implements the same standard.

> Essentially, the system that we have for skill is really just like a prompt system, so we can use these either in the system prompt or in the prompt, or just let the agent have these skills available to load. So these would be different kinds of context modules, let's say.

-- spoken, 3 October

> It could be a vector with the variant, like vision, and each of the variants contains all of the names of the modules that it wants. Somewhere else in the database, those module names correspond with the path, so that's configured separately, right?

-- typed, 3 October

### Curriculum: the generator, by that name

Curriculum is only the generator. It reads the declared sources and writes, into a workspace, what each harness needs, emitting the blocks that differ between Claude and Codex. The name stays Curriculum.

> We use curriculum, and we can edit in our workspace. The files that have been modified will be regenerated or added, if they're missing, into that workspace. Depending on Codex, Claude, or all of the harnesses that we're going to support, it's going to emit the different blocks that depend on whether or not it's Claude or Codex

-- typed, 3 October

> It's a standard for now that Flow can use and that we'll also implement in curriculum, which we could possibly rename context or maybe keep it curriculum (because the word context is used a lot so I think it's better to keep it curriculum).

-- typed, 3 October

### What it never does

Curriculum never holds skill data, and source repositories never hold generated output. Generated trees are read-only evidence: a change is made at the source and regenerated.

> I dont want to see any .claude or .agent in the skills repo

-- 10 August

A skill written for one harness never appears as an empty shell in another.

> that doesn't work because then you'll create an empty skill for Codex, which will just take up context, telling him there's a skill there when there isn't.

-- spoken, early September

## Part 2. What exists today

Witnessed on 3 October 2026.

- All 69 skills are still written in Curriculum. By name, 39 carry no kind prefix, 3 are vision, 4 knowledge, 4 operation, 7 compensation and 12 trial.
- The three skill repositories exist, made on 29 September. Each holds one page naming the aspect in charge.
- No skill has moved.
- The generator's new version, out today, reads several declared sources, merges them, refuses a skill defined twice, and imposes no layout inside a repository.
- Primary, the one shared repository, still runs the old generator, which reads Curriculum alone and is 51 changes behind.
- Primary's generated copy holds 68 skills: two recent ones missing, one removed one still there.
- No skill maps layers to models. Model names still sit in the variables file.

## Part 3. Questions

Answer each with its number and "1" or "2", or "yes".

1. **Where is the skill text written?** Both readings are from 3 October.

> Why the fuck are the skills not living in three repositories right now: psyche, mind, and field?

-- spoken, 3 October

> We write the data in a place that is used by the curriculum tool to generate the skills.

-- spoken, 3 October

Are skills written in the three skill repositories and copied from the vision (1), or are the distilled records themselves the source, read straight from it (2)? Yes means 1.

2. **Where is a skill's kind declared?** Three repositories each holding two kinds needs a kind on each skill.

> There's just going to be a repository of a certain type. The type is assigned to the repo. It's centrally controlled: which type comes from which repositories.

-- typed, 24 September

> No the skills will be typed. Just copying the directory name is dirty.

-- typed, late September

Does the folder carry the kind (1), or each skill in a typed record (2)? Yes means 2.

3. **Where does the layer-to-model map live?**

> there would be a skill that makes a correspondence of layers to models in the knowledge type skill.

-- typed, 3 October, 15:41

> No the configuration flow does not live in a Markdown file in every story. It lives in its own database and its memory.

-- typed, 3 October, 18:13

Does it live in a knowledge skill (1), or in Flow's database, with one knowledge skill generated from it so skills can read it (2)? Yes means 2.

4. **Which skill goes to which aspect?** Of today's 69, the 30 with a kind prefix place themselves. The 39 without one need a home, and three of those (design, realization, main flow) are loaded only by you and fit no kind cleanly. The rule: what you want the result to be goes to psyche; what is true of a tool, or how a tool is spoken to, goes to Mind as knowledge; how a recurring job is done goes to Mind as operation. Spirit stays under psyche until its own question is answered. Proposed, for your yes or edits:

| Goes to | Skills |
|---|---|
| Psyche, vision (23) | spirit, behavior, correction, vocabulary, psyche, psyche interaction, psyche distillation, psyche acquisition, psyche grasp, skill designing, context strata, documentation placement, testing, versioning, breaking upgrades, prompt crafting, flow evidence, main flow, design, realization, vision ethos, vision flow, vision nexus |
| Mind, knowledge (12) | datom, protos, knowledge codex, knowledge ethos, knowledge flow, knowledge nexus, Claude harness, Codex harness, transcript search, orchestrate, lojix, beads |
| Mind, operation (15) | agent harness packaging, nix workflow, nix input upgrade, operating system, disk hygiene, secrets, edit coordination, stale lock, feature development, repository lifecycle, file editing, operation book, operation flashbook, operation flashbook illustration, operation relaying the living |
| Field, compensation (7) | the seven compensation skills, unchanged |
| Field, trial (12) | the twelve trial skills, unchanged |

Yes accepts the table as written.
